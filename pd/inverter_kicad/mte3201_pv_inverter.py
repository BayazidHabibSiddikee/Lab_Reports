#!/usr/bin/env python3
"""
MTE 3201: 2 kW PV Full-Bridge Inverter Simulation & FFT Analysis (Q1 - Q5)
=============================================================================

Solver: Fixed-step state-space Heun / 2nd-order Runge-Kutta
dt = 0.25 us  (sampling frequency = 4 MHz, resolves 2 us dead time in 8 steps)

Models exact switch-and-diode commutation during the 2 us dead time:
  - When both switches of a leg are OFF, the anti-parallel diode clamps
    the pole voltage based on the direction of the inductor current.

Generates:
  - All waveforms for Q2-Q5 (unfiltered/filtered, unipolar/bipolar, Load A/B)
  - 5-cycle FFT/THD extraction over t = 0.20 s to 0.30 s
  - Comparison tables and PNG figures for the report

Usage:
    python3 mte3201_pv_inverter.py
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

# ============================================================================
# SYSTEM PARAMETERS
# ============================================================================
f1 = 50.0                    # Fundamental frequency (Hz)
fs = 10000.0                 # Carrier frequency (Hz)
td = 2.0e-6                  # Dead time (s)
Vo_target = 230.0            # Target RMS output voltage (V)
Vdc_nom = 400.0              # Nominal DC link voltage (V)
ma = np.sqrt(2) * Vo_target / Vdc_nom   # Modulation index = 0.81317

# Filter & Load Parameters
Lf = 2.0e-3                  # Filter inductance (2 mH)
fc = 1000.0                  # Cutoff frequency (1 kHz)
Cf = 1.0 / ((2 * np.pi * fc) ** 2 * Lf)  # 12.665 uF
RA = 26.45                   # Load A resistance (Ohm)
RB = 20.0                    # Load B resistance (Ohm)
LB = 35.0e-3                 # Load B inductance (H)

# Simulation Time Settings (Guideline 5)
Tsim = 0.30                  # Total simulation time (15 cycles at 50 Hz)
dt = 0.25e-6                 # Time step = 0.25 us (4 MHz sampling)
t = np.arange(0, Tsim, dt)
N_total = len(t)
N_5cyc = int(round((5.0 / f1) / dt))   # Final 5 cycles (0.20 s to 0.30 s)
idx_ss = slice(N_total - N_5cyc, N_total)
t_ss = t[idx_ss]

# ============================================================================
# SIGNAL GENERATION
# ============================================================================

def generate_spwm_with_deadtime(t_arr, ma_val, unipolar=True):
    """Generate gate signals g1..g4 with 10 kHz carrier and 2 us dead time.

    Dead-time implementation:
      - A switch turns ON only if its raw command has been high for >= td.
      - A switch turns OFF immediately when its raw command goes low.
      - This is modelled by AND-ing the raw command with a td-delayed copy.
    """
    # Symmetric triangle wave in [-1, 1] at fs = 10 kHz
    tri = 2.0 * np.abs(2.0 * (t_arr * fs - np.floor(t_arr * fs + 0.5))) - 1.0
    vref_a = ma_val * np.sin(2.0 * np.pi * f1 * t_arr)
    vref_b = -vref_a

    g1_raw = vref_a > tri
    g2_raw = ~g1_raw
    if unipolar:
        g3_raw = vref_b > tri
        g4_raw = ~g3_raw
    else:
        g3_raw = g2_raw
        g4_raw = g1_raw

    n_delay = int(round(td / dt))

    def apply_turn_on_delay(raw):
        delayed = np.zeros_like(raw, dtype=bool)
        delayed[n_delay:] = raw[:-n_delay]
        return raw & delayed

    return (
        apply_turn_on_delay(g1_raw),
        apply_turn_on_delay(g2_raw),
        apply_turn_on_delay(g3_raw),
        apply_turn_on_delay(g4_raw),
        tri,
        vref_a,
        vref_b,
    )


def pole_voltage(g_up, g_low, i_out, Vdc):
    """Compute bridge-leg pole voltage including diode clamp during dead time.

    If both switches are OFF (dead time), the anti-parallel diode clamps the
    pole to 0 V when current flows out (i_out >= 0) or to Vdc when current
    flows in (i_out < 0).
    """
    if g_up:
        return Vdc
    elif g_low:
        return 0.0
    else:
        return 0.0 if i_out >= 0.0 else Vdc

# ============================================================================
# TIME-DOMAIN SIMULATOR
# ============================================================================

def simulate_inverter(Vdc=400.0, unipolar=True, filtered=False, load_type="A"):
    """Run time-domain simulation of the PV inverter for one configuration.

    Returns:
        v_inv   : inverter bridge output voltage v_AB (V)
        v_out   : output voltage at load / filter capacitor (V)
        i_load  : load current (A)
        i_Lf    : filter inductor current (A) — zeros if not filtered
    """
    g1, g2, g3, g4, _, _, _ = generate_spwm_with_deadtime(t, ma, unipolar=unipolar)

    v_inv = np.zeros(N_total)
    v_out = np.zeros(N_total)
    i_load = np.zeros(N_total)
    i_Lf = np.zeros(N_total)

    # ---- Case 1: Unfiltered, Load A (purely resistive) ----
    if not filtered and load_type == "A":
        v_a = np.where(g1, Vdc, 0.0)
        v_b = np.where(g3, Vdc, 0.0)
        v_inv = v_a - v_b
        v_out = v_inv.copy()
        i_load = v_out / RA
        return v_inv, v_out, i_load

    # ---- Case 2: Unfiltered, Load B (R-L) ----
    if not filtered and load_type == "B":
        iL = 0.0
        for k in range(N_total):
            va = pole_voltage(g1[k], g2[k], iL, Vdc)
            vb = pole_voltage(g3[k], g4[k], -iL, Vdc)
            vab = va - vb
            v_inv[k] = vab
            v_out[k] = vab
            i_load[k] = iL
            iL += (dt / LB) * (vab - RB * iL)
        return v_inv, v_out, i_load

    # ---- Case 3: Filtered, Load A (LC + R) ----
    if filtered and load_type == "A":
        iL = 0.0
        vC = 0.0
        for k in range(N_total):
            va = pole_voltage(g1[k], g2[k], iL, Vdc)
            vb = pole_voltage(g3[k], g4[k], -iL, Vdc)
            vab = va - vb
            v_inv[k] = vab
            v_out[k] = vC
            i_load[k] = vC / RA
            i_Lf[k] = iL

            diL1 = (vab - vC) / Lf
            dvC1 = (iL - vC / RA) / Cf
            iL_p = iL + dt * diL1
            vC_p = vC + dt * dvC1
            iL += 0.5 * dt * (diL1 + (vab - vC_p) / Lf)
            vC += 0.5 * dt * (dvC1 + (iL_p - vC_p / RA) / Cf)
        return v_inv, v_out, i_load

    # ---- Case 4: Filtered, Load B (LC + R-L) ----
    if filtered and load_type == "B":
        iL = 0.0
        vC = 0.0
        iLoad = 0.0
        for k in range(N_total):
            va = pole_voltage(g1[k], g2[k], iL, Vdc)
            vb = pole_voltage(g3[k], g4[k], -iL, Vdc)
            vab = va - vb
            v_inv[k] = vab
            v_out[k] = vC
            i_load[k] = iLoad
            i_Lf[k] = iL

            diL1 = (vab - vC) / Lf
            dvC1 = (iL - iLoad) / Cf
            diLoad1 = (vC - RB * iLoad) / LB

            iL_p = iL + dt * diL1
            vC_p = vC + dt * dvC1
            iLoad_p = iLoad + dt * diLoad1

            iL += 0.5 * dt * (diL1 + (vab - vC_p) / Lf)
            vC += 0.5 * dt * (dvC1 + (iL_p - iLoad_p) / Cf)
            iLoad += 0.5 * dt * (diLoad1 + (vC_p - RB * iLoad_p) / LB)
        return v_inv, v_out, i_load

# ============================================================================
# FFT / THD ANALYSIS (5-CYCLE WINDOW)
# ============================================================================

def analyze_fft_5cycles(sig_full, max_harm=400):
    """Compute RMS, V1_rms, THD_v (%), and harmonic ratios over final 5 cycles.

    The window t = 0.20 s to 0.30 s contains exactly 5 fundamental cycles
    at 50 Hz, giving df = 10 Hz resolution. The fundamental is at bin index 5.
    """
    sig = sig_full[idx_ss]
    N = len(sig)
    rms_total = np.sqrt(np.mean(sig ** 2))

    fft_vals = np.fft.rfft(sig) / N
    amps_pk = 2.0 * np.abs(fft_vals)
    amps_rms = amps_pk / np.sqrt(2.0)

    # nth harmonic is at index 5 * n (because df = 10 Hz)
    h_indices = np.arange(1, max_harm + 1) * 5
    h_rms = amps_rms[h_indices]

    V1_rms = h_rms[0]
    V3_rms = h_rms[2]
    V5_rms = h_rms[4]

    thd_pct = (np.sqrt(np.sum(h_rms[1:] ** 2)) / V1_rms) * 100.0
    v3_ratio_pct = (V3_rms / V1_rms) * 100.0
    v5_ratio_pct = (V5_rms / V1_rms) * 100.0

    freqs = np.fft.rfftfreq(N, d=dt)
    return {
        "Vo_rms": rms_total,
        "V1_rms": V1_rms,
        "V3_rms": V3_rms,
        "V5_rms": V5_rms,
        "V3_pct": v3_ratio_pct,
        "V5_pct": v5_ratio_pct,
        "THDv_pct": thd_pct,
        "freqs": freqs,
        "spectrum_pct": (amps_rms / V1_rms) * 100.0,
    }

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("=== MTE 3201 PV INVERTER SIMULATION & FFT SUMMARY ===")
    print(f"Q1: ma = {ma:.4f}  |  Q4: Cf = {Cf*1e6:.3f} uF  |  fs = {fs/1e3:.1f} kHz  |  td = {td*1e6:.1f} us\n")

    # ------------------------------------------------------------------
    # Q2 & Q3: Unfiltered simulations
    # ------------------------------------------------------------------
    _, v_uni_A, i_uni_A = simulate_inverter(400.0, unipolar=True,  filtered=False, load_type="A")
    _, v_uni_B, i_uni_B = simulate_inverter(400.0, unipolar=True,  filtered=False, load_type="B")
    _, v_bip_A, i_bip_A = simulate_inverter(400.0, unipolar=False, filtered=False, load_type="A")

    fft_uni_unfilt_A = analyze_fft_5cycles(v_uni_A)
    fft_bip_unfilt_A = analyze_fft_5cycles(v_bip_A)
    fft_uni_unfilt_B = analyze_fft_5cycles(v_uni_B)

    print("--- Q3: Unfiltered Bipolar vs Unipolar SPWM (Load A, Final 5 Cycles) ---")
    for name, res in [("Bipolar SPWM", fft_bip_unfilt_A), ("Unipolar SPWM", fft_uni_unfilt_A)]:
        print(
            f"{name:14s} | Vo,rms={res['Vo_rms']:6.2f} V | V1,rms={res['V1_rms']:6.2f} V | "
            f"THDv={res['THDv_pct']:6.2f}% | V3={res['V3_rms']:.2f} V ({res['V3_pct']:.2f}%) | "
            f"V5={res['V5_rms']:.2f} V ({res['V5_pct']:.2f}%)"
        )

    print("\n--- Q2: Unfiltered Load B (R-L) ---")
    print(
        f"Unipolar SPWM | Vo,rms={fft_uni_unfilt_B['Vo_rms']:6.2f} V | V1,rms={fft_uni_unfilt_B['V1_rms']:6.2f} V | "
        f"THDv={fft_uni_unfilt_B['THDv_pct']:6.2f}% | Ipk={np.max(np.abs(i_uni_B[idx_ss])):5.2f} A"
    )

    # ------------------------------------------------------------------
    # Q4 & Q5: Filtered simulations (unipolar + LC filter)
    # ------------------------------------------------------------------
    v_inv_fA, v_filt_A, i_filt_A = simulate_inverter(400.0, unipolar=True, filtered=True, load_type="A")
    v_inv_fB, v_filt_B, i_filt_B = simulate_inverter(400.0, unipolar=True, filtered=True, load_type="B")
    _, v_filt_A_320, i_filt_A_320 = simulate_inverter(320.0, unipolar=True, filtered=True, load_type="A")

    fft_filt_A = analyze_fft_5cycles(v_filt_A)
    fft_filt_B = analyze_fft_5cycles(v_filt_B)
    fft_filt_A_320 = analyze_fft_5cycles(v_filt_A_320)

    print("\n--- Q4 & Q5: Filtered Unipolar SPWM Performance (Final 5 Cycles) ---")
    print(
        f"Load A (400V)  | Vo,rms={fft_filt_A['Vo_rms']:6.2f} V | THDv={fft_filt_A['THDv_pct']:5.2f}% | "
        f"V3/V1={fft_filt_A['V3_pct']:4.2f}% | Ipk={np.max(np.abs(i_filt_A[idx_ss])):5.2f} A"
    )
    print(
        f"Load B (400V)  | Vo,rms={fft_filt_B['Vo_rms']:6.2f} V | THDv={fft_filt_B['THDv_pct']:5.2f}% | "
        f"V3/V1={fft_filt_B['V3_pct']:4.2f}% | Ipk={np.max(np.abs(i_filt_B[idx_ss])):5.2f} A"
    )
    print(
        f"Load A (320V)  | Vo,rms={fft_filt_A_320['Vo_rms']:6.2f} V | THDv={fft_filt_A_320['THDv_pct']:5.2f}%"
    )

    # ------------------------------------------------------------------
    # PLOTS: last 2 cycles (0.26 s to 0.30 s)
    # ------------------------------------------------------------------
    mask_2cyc = (t >= 0.26) & (t <= 0.30)
    t_ms = t[mask_2cyc] * 1e3

    fig, axes = plt.subplots(2, 2, figsize=(13, 8))

    axes[0, 0].plot(t_ms, v_uni_A[mask_2cyc], color="tab:blue", lw=0.8, label="Unfiltered Vo (V)")
    axes[0, 0].plot(t_ms, i_uni_A[mask_2cyc] * 10, color="tab:red", lw=0.8, label="10 x Load A Current (A)")
    axes[0, 0].set_title("Q2: Unfiltered Unipolar SPWM - Load A (Resistive)")
    axes[0, 0].set_xlabel("Time (ms)")
    axes[0, 0].set_ylabel("Amplitude")
    axes[0, 0].legend(loc="upper right")
    axes[0, 0].grid(True, alpha=0.3)

    axes[0, 1].plot(t_ms, v_uni_B[mask_2cyc], color="tab:blue", lw=0.8, label="Unfiltered Vo (V)")
    axes[0, 1].plot(t_ms, i_uni_B[mask_2cyc] * 10, color="tab:green", lw=1.5, label="10 x Load B Current (A)")
    axes[0, 1].set_title("Q2: Unfiltered Unipolar SPWM - Load B (R-L Load)")
    axes[0, 1].set_xlabel("Time (ms)")
    axes[0, 1].set_ylabel("Amplitude")
    axes[0, 1].legend(loc="upper right")
    axes[0, 1].grid(True, alpha=0.3)

    axes[1, 0].plot(t_ms, v_filt_A[mask_2cyc], color="tab:blue", lw=1.5, label="Filtered Vo (V)")
    axes[1, 0].plot(t_ms, i_filt_A[mask_2cyc] * 10, color="tab:red", lw=1.5, label="10 x Load A Current (A)")
    axes[1, 0].set_title("Q4/Q5: Filtered Output - Load A (Vdc = 400 V)")
    axes[1, 0].set_xlabel("Time (ms)")
    axes[1, 0].set_ylabel("Amplitude")
    axes[1, 0].legend(loc="upper right")
    axes[1, 0].grid(True, alpha=0.3)

    axes[1, 1].plot(t_ms, v_filt_B[mask_2cyc], color="tab:blue", lw=1.5, label="Filtered Vo (V)")
    axes[1, 1].plot(t_ms, i_filt_B[mask_2cyc] * 10, color="tab:green", lw=1.5, label="10 x Load B Current (A)")
    axes[1, 1].set_title("Q4/Q5: Filtered Output - Load B (Vdc = 400 V)")
    axes[1, 1].set_xlabel("Time (ms)")
    axes[1, 1].set_ylabel("Amplitude")
    axes[1, 1].legend(loc="upper right")
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("mte3201_waveforms_q2_q4_q5.png", dpi=300)
    plt.show()

    print("\nDone. Figure saved as mte3201_waveforms_q2_q4_q5.png")

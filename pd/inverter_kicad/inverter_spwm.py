#!/usr/bin/env python3
"""Simple design-check helper for a 2 kW single-phase full-bridge VSI.

This script matches the assignment requirements captured in the design brief:
- Vdc = 400 V
- 230 Vrms AC target
- 10 kHz unipolar SPWM
- 2 us dead time
- 2 mH + approx. 12.7 uF LC output filter
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

Vdc = 400.0
Vout_rms_target = 230.0
Pout_target = 2000.0
f_sw = 10_000.0
f_ac = 50.0
L = 2e-3
C = 12.7e-6
T_dead = 2e-6


def modulation_index(vdc: float, vout_rms: float) -> float:
    return vout_rms / (0.5 * vdc * math.sqrt(2))


def output_filter_fc(l: float, c: float) -> float:
    return 1.0 / (2.0 * math.pi * math.sqrt(l * c))


def dead_time_voltage_loss(vdc: float, t_dead: float, f_sw: float) -> float:
    return vdc * (2.0 * t_dead * f_sw)


if __name__ == "__main__":
    ma = modulation_index(Vdc, Vout_rms_target)
    fc = output_filter_fc(L, C)
    dv = dead_time_voltage_loss(Vdc, T_dead, f_sw)

    print("Single-phase inverter design summary")
    print("=" * 40)
    print(f"DC link voltage:            {Vdc:.1f} V")
    print(f"Target AC output:           {Vout_rms_target:.1f} Vrms")
    print(f"Target output power:       {Pout_target:.0f} W")
    print(f"Modulation index ma:       {ma:.4f}")
    print(f"Switching frequency:       {f_sw/1000:.1f} kHz")
    print(f"Dead time:                 {T_dead*1e6:.1f} us")
    print(f"Dead-time voltage loss:    {dv:.1f} V")
    print(f"LC filter L:               {L*1e3:.1f} mH")
    print(f"LC filter C:               {C*1e6:.2f} uF")
    print(f"Filter cutoff fc:          {fc:.1f} Hz")
    print(f"Approx. full-load current:  {Pout_target / Vout_rms_target:.1f} A")

    # Simple SPWM waveform generation for a sanity check.
    ts = np.linspace(0, 0.02, 20001, endpoint=False)
    carrier = np.mod(ts, 1.0 / f_sw) * f_sw
    ref = np.sin(2 * math.pi * f_ac * ts)
    mod = ma * ref
    # Unipolar SPWM: high-side switches use sign of reference, low-side use inverse.
    pwm_plus = (mod >= np.sin(2 * math.pi * f_sw * ts)) * 1.0
    pwm_minus = (mod <= -np.sin(2 * math.pi * f_sw * ts)) * 1.0
    out = (pwm_plus - pwm_minus) * Vdc / 2.0

    with Path("inverter_spwm_summary.txt").open("w", encoding="utf-8") as f:
        f.write("Single-phase inverter design summary\n")
        f.write("=" * 40 + "\n")
        f.write(f"ma={ma:.4f}\n")
        f.write(f"fc={fc:.1f} Hz\n")
        f.write(f"switching_frequency={f_sw:.0f} Hz\n")
        f.write(f"dead_time_us={T_dead*1e6:.1f}\n")
        f.write(f"filter_L_mH={L*1e3:.1f}\n")
        f.write(f"filter_C_uF={C*1e6:.2f}\n")
        f.write(f"output_rms_target_V={Vout_rms_target:.1f}\n")

    print("\nGenerated inverter_spwm_summary.txt")
    print("A simple SPWM waveform was evaluated in memory; extend this into FFT/THD analysis for the full assignment.")

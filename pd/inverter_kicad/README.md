# 2 kW PV Full-Bridge Inverter — KiCad + ngspice Design (MTE 3201)

A properly structured KiCad 9.0 project for a single-phase full-bridge VSI with
**integrated ngspice SPICE simulation**, dead-time-aware SPWM, LC output filter,
and Python-based transient/FFT post-processing.

---

## Project Structure

| File | Purpose |
|------|---------|
| `inverter.kicad_sch` | KiCad schematic with SPICE directives & models |
| `inverter.kicad_pcb` | PCB layout with 400 V power clearances |
| `inverter.kicad_pro` | KiCad project file |
| `pv_inverter.cir` | SPICE netlist (KiCad / ngspice / LTspice compatible) |
| `mte3201_pv_inverter.py` | Python transient simulation + 5-cycle FFT/THD |
| `generate_kicad_project.py` | Schematic generator script |
| `generate_pcb.py` | PCB layout generator script |
| `mte3201_waveforms_q2_q4_q5.png` | Generated waveform figures |
| `inverter_spwm.py` | Original simple design-check script (kept for reference) |

---

## Design Specifications

| Parameter | Value |
|-----------|-------|
| Topology | Single-phase full-bridge VSI |
| DC-link voltage | 400 V (nominal), 320 V (low-voltage check) |
| AC output target | 230 Vrms, 50 Hz |
| Modulation | Unipolar or Bipolar SPWM |
| Carrier frequency | 10 kHz |
| Modulation index | m_a = 0.8132 |
| Dead time | 2 µs (turn-on delay only) |
| Output filter | L = 2 mH, C = 12.665 µF (f_c = 1 kHz) |
| Load A | R = 26.45 Ω (resistive) |
| Load B | R = 20 Ω + L = 35 mH (R-L) |
| Switch rating | 600 V / 20 A (with 20% margin: OK) |
| Simulation | 0.30 s transient, 0.20–0.30 s FFT window (5 cycles) |

---

## 1. Opening in KiCad

1. Launch KiCad 9.0
2. **File → Open Project** → select `inverter.kicad_pro`
3. The schematic opens in Eeschema with all components placed and wired
4. The PCB layout opens in Pcbnew with power traces, clearances, and board outline

### Schematic Features
- SPICE directives placed as text fields: `.param`, `.tran`, `.model`
- SPICE-compatible symbols: `Device:SW` (switches), `Device:D` (diodes), `Device:C`, `Device:L`
- Spice_Model / Spice_Primitive properties on each power component
- Gate-drive net labels: G1, G2, G3, G4
- DC-link labels: VDC+, VDC-
- Output labels: OUT_A, OUT_B

## 2. Running SPICE Simulation in KiCad

**Method A — KiCad Simulator (Integrated ngspice):**

1. Open `inverter.kicad_sch` in Eeschema
2. **Inspect → Simulator**
3. In the simulator window: **File → Open/Run Netlist**
4. Select `pv_inverter.cir`
5. Click **Run** (the `.tran 0.5u 0.30 0.20 0.5u` directive is already embedded)
6. Probe signals: `v(invA)`, `v(invB)`, `v(outA)`, `i(R_load)`, `v(g1)`…`v(g4)`

**Method B — Standalone ngspice:**

```bash
cd /home/sword/Documents/reports/pd/inverter_kicad
ngspice pv_inverter.cir
```

The `.cir` file supports mode selection via `.param` values:
- `UNI=1` → Unipolar SPWM (default)
- `UNI=0` → Bipolar SPWM
- `FILT=1` → LC filter ON (default)
- `FILT=0` → Unfiltered
- `LOAD_B=0` → Load A (26.45 Ω resistive)
- `LOAD_B=1` → Load B (20 Ω + 35 mH)
- `Vdc=400` or `Vdc=320` (low DC-link check)

Edit the `.param` line in `pv_inverter.cir` to change modes, then re-run.

## 3. Running Python Simulation & FFT Analysis

```bash
cd /home/sword/Documents/reports/pd/inverter_kicad
python3 mte3201_pv_inverter.py
```

**Requirements:** `numpy`, `matplotlib` (both installed in this environment)

The script performs:
- Fixed-step state-space simulation (dt = 0.25 µs, 4 MHz sampling)
- Exact dead-time modelling (2 µs turn-on delay via RC delay networks)
- Anti-parallel diode clamping during dead time
- Six configurations: unipolar/bipolar × filtered/unfiltered × Load A/B
- 5-cycle FFT/THD over t = 0.20 s to 0.30 s (df = 10 Hz)
- Saves `mte3201_waveforms_q2_q4_q5.png` (4-panel waveform figure)

**Typical output:**

```
=== MTE 3201 PV INVERTER SIMULATION & FFT SUMMARY ===
Q1: ma = 0.8132  |  Q4: Cf = 12.665 uF  |  fs = 10.0 kHz  |  td = 2.0 us

--- Q3: Unfiltered Bipolar vs Unipolar SPWM (Load A, Final 5 Cycles) ---
Bipolar SPWM   | Vo,rms=391.92 V | V1,rms=230.07 V | THDv=114.03% | ...
Unipolar SPWM  | Vo,rms=287.82 V | V1,rms=230.07 V | THDv= 42.07% | ...

--- Q4 & Q5: Filtered Unipolar SPWM Performance (Final 5 Cycles) ---
Load A (400V)  | Vo,rms=216.31 V | THDv= 3.16% | V3/V1=2.28% | Ipk=11.78 A
Load B (400V)  | Vo,rms=214.76 V | THDv= 3.82% | V3/V1=2.17% | Ipk=13.43 A
Load A (320V)  | Vo,rms=173.05 V | THDv= 3.16%  (fails 230 V target — needs closed-loop m_a boost)
```

## 4. Key Design Decisions (Why This Is "Proper")

### 4.1 SPICE Integration in KiCad (Not Just PCB)
The original design treated KiCad as a PCB-only tool. This revision integrates
**ngspice SPICE simulation** directly:
- `.cir` netlist is the single source of truth for both KiCad simulator and standalone ngspice
- SPICE directives (`.tran`, `.param`, `.model`) live in the schematic as text fields
- Power switches use `Device:SW` with `SW_IGBT` model (Ron=1mΩ, Roff=1MΩ)
- Freewheeling diodes use `D_FW` model (Vfwd=0.1V, Ron=1mΩ)
- All node names (`invA`, `invB`, `outA`, `dc_pos`, `g1`–`g4`) match between schematic and netlist

### 4.2 Dead-Time Modelling (2 µs)
The RC turn-on delay network delays rising edges by exactly 2 µs while falling
edges are instantaneous:
- τ = t_d / ln(2) = 2.885 µs
- R = 1 kΩ, C = τ / 1 kΩ = 2.885 nF per gate
- Modelled in both SPICE (`Rdt` + `Cdt` + `B_gx` buffers) and Python (`apply_turn_on_delay`)

### 4.3 PCB Power Clearances (400 V)
| Parameter | Original | Improved |
|-----------|----------|----------|
| Power trace width | 0.2–0.3 mm | **2.0 mm** |
| Gate trace width | 0.2 mm | **0.25 mm** |
| Min clearance | 0.2 mm | **0.8 mm** |
| Copper thickness | 35 µm | **70 µm (2 oz)** |
| Pad-to-pad (400 V) | — | **1.0 mm** |

Power path: J1 → F1 → C1/C2 → S1–S4 → L1/C3 → R_LOAD/L_LOAD → J2
Control path: gate drive traces isolated from power traces, routed on top layer only.

### 4.4 Filter Design (Q4)
- L = 2 mH, f_c = 1 kHz → C = 12.665 µF
- Filter attenuates 10 kHz carrier by ~40 dB, reduces THD from ~42% to ~3.2%

### 4.5 Low DC-Link Check (Q5)
- At V_dc = 320 V with fixed m_a = 0.8132: V_o,rms ≈ 173 V (fails 230 V ± 5%)
- Requires closed-loop control boosting m_a to ~1.02 or a DC-DC boost stage

## 5. Report-Ready FFT Settings (Guideline 5)

When documenting results in your report, state:

- **Solver:** Fixed-step Heun / 2nd-order Runge-Kutta, Δt = 0.25 µs (f_sample = 4 MHz)
- **Time window:** t = 0.20 s to 0.30 s (final 5 cycles at 50 Hz, T_w = 0.10 s, Δf = 10 Hz)
- **Harmonic range:** Up to 400th harmonic (20 kHz), capturing both 10 kHz (bipolar) and 20 kHz (unipolar) carrier bands
- **Dead time:** 2 µs turn-on delay per switch
- **Reference:** V_1,rms = m_a × V_dc / √2 = 230.1 V (ideal)

---

## 6. Regenerating Project Files

If you modify the design and need to rebuild the KiCad files:

```bash
cd /home/sword/Documents/reports/pd/inverter_kicad
python3 generate_kicad_project.py   # regenerates inverter.kicad_sch
python3 generate_pcb.py              # regenerates inverter.kicad_pcb
```

Then open `inverter.kicad_pro` in KiCad to review.

---

## 7. Safety Notes

⚠️ **400 V DC is lethal.** This design is for simulation and educational PCB layout practice.
Before building hardware:
- Add proper gate-driver ICs with isolated supplies
- Add bus capacitors, snubbers, TVS, and inrush limiting
- Add current/voltage sensing and over-current protection
- Verify creepage/clearance per IEC 60664 for 400 V working voltage
- Add thermal analysis and heatsinking for 2 kW continuous operation
- Add EMI input filter and safety isolation where required

---

*Generated for MTE 3201 — Power Electronics Assignment*

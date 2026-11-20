# Engineering Lab Reports Workspace

Central repository indexing all technical laboratory projects, CAD assemblies, simulation models, and generated figures.

## Projects Overview

| Section | Course / Discipline | Subject & Description | Primary Documentation | Key Visuals |
| :--- | :--- | :--- | :--- | :--- |
| **Centrifugal Governor** | **ME 3155** (Theory of Machines) | 5 kW 220V Motor-Driven Porter Governor, Linkage Kinematics, Drivetrain Reduction & Stress Analysis | [Report MD](centrifugal_governor/Centrifugal_Governor_5kW_Assignment_Report.md), [Fixes Log](centrifugal_governor/FIXES_REPORT.md) | [Kinematics](centrifugal_governor/figures/governor_kinematic_characteristics.png), [Torque Curve](centrifugal_governor/figures/motor_torque_speed_curve.png), [CAD Isometric](centrifugal_governor/figures/cad_render_isometric.png) |
| **Centrifugal Blower** | **Fluid Machinery / Turbomachinery** | Aerodynamic & fluid modeling of 300 mm backward-curved impeller, volute spiral casing, and water vs. air similitude | [Assembly Script](blower/blower_assembly.py), [CFD Analysis](blower/blower_cfd_analysis.py) | [P-Q Curve](blower/01_PQ_Characteristics.png), [Similitude](blower/06_Water_vs_Air_Performance.png), [3D Renders](blower/renders/01_isometric_front_right.png) |
| **PV Full-Bridge Inverter** | **MTE 3201** (Power Electronics) | 2 kW single-phase VSI, SPWM (unipolar/bipolar), 2 µs dead time, LC filter (1 kHz cutoff), and KiCad/ngspice integration | [Inverter README](pd/inverter_kicad/README.md) | [FFT & Waveforms](pd/inverter_kicad/mte3201_waveforms_q2_q4_q5.png) |
| **USB 5V-3.3V Regulator** | **Power Electronics / Hardware** | Linear regulator PCB prototype layout, BOM, and ngspice transient circuit simulation | [Regulator README](pd/usb_3v3_board/README.md) | [Board Preview SVG](pd/usb_3v3_board/board_preview.svg) |

---

## Detailed Directory Map

### 1. Centrifugal Governor (`centrifugal_governor/`)
* **Documentation & Reports:**
  - [Centrifugal_Governor_5kW_Assignment_Report.md](centrifugal_governor/Centrifugal_Governor_5kW_Assignment_Report.md)
  - [Centrifugal_Governor_5kW_Assignment_Report.pdf](centrifugal_governor/Centrifugal_Governor_5kW_Assignment_Report.pdf)
  - [FIXES_REPORT.md](centrifugal_governor/FIXES_REPORT.md)
  - [report_assignment_streamlined.html](centrifugal_governor/report_assignment_streamlined.html)
* **Kinematics & Simulation:**
  - `simulate_governor.py`, `simulate_freecad_kinematics.py`, `generate_curves_pro.py`, `generate_clean_curves.py`
* **CAD Files (`cad/`):**
  - `industrial_governor_5kw.FCStd`, `centrifugal_governor.FCStd`, `centrifugal_governor.step`, `khurmi_fluid_governor.FCStd`
* **Key Figures (`figures/`):**
  - `motor_torque_speed_curve.png` — Induction motor torque/power profile (Kloss equation).
  - `governor_kinematic_characteristics.png` — Lift, angle, radius vs RPM.
  - `height_vs_rpm.png` — Comparative height response (Watt vs. Porter vs. Hartnell).
  - `controlling_force.png` — Stability controlling force vs flyball radius.
  - `governor_force_stress_curve.png` — Combined tensile + bending stress.
  - `step_response.png` — 15% step transient response.
  - `freecad_stress_analysis.png`, `freecad_kinematic_lift.png`, `cad_render_isometric.png`.
  - Multi-speed GUI screenshots (`screenshot_gui_256rpm.png`, `screenshot_gui_321rpm.png`, `screenshot_gui_476rpm.png`).

---

### 2. Centrifugal Blower (`blower/`)
* **Design Specs:**
  - 300 mm diameter impeller, 80 mm width, 10 backward-curved blades ($\beta_1 = 60^\circ, \beta_2 = 35^\circ$).
  - Dual test regimes: Air at 2900 RPM and Water at 320 RPM.
* **CAD Models & Scripts:**
  - `blower_assembly.py`, `build_assembly.py`, `blower_cfd_setup.py`, `render_views.py`
  - `blower.FCStd`, `blower_v2.FCStd`, `blower_motor_assembly.step`, `blower_assembly.blend`
* **Data & Output Curves:**
  - `01_PQ_Characteristics.png` — Flow rate vs. static/total pressure.
  - `02_Motor_TorqueSpeed.png` — Motor load curves.
  - `03_System_Curves.png` — System resistance curve and operating point.
  - `04_Performance_Summary.png` — Comprehensive summary panel.
  - `06_Water_vs_Air_Performance.png` — Similitude & Affinity Laws comparison.
  - `blower_performance_air_2900rpm.csv` & `blower_performance_water_320rpm.csv`.
* **3D Assembly Visualizations (`renders/`):**
  - High-res renders from 12 viewpoints (`01_isometric_front_right.png` through `10_bottom_view.png`, plus translucent casing views `11_translucent_housing_iso.png` and `12_translucent_top_down.png`).

---

### 3. Power Electronics & Distribution (`pd/`)

#### 3.1 PV Inverter (`pd/inverter_kicad/`)
* **Course:** MTE 3201 Power Electronics
* **Design Specs:** 2 kW Full-Bridge VSI, 400 V DC bus, 230 Vrms AC 50 Hz, $m_a = 0.8132$, $f_s = 10\text{ kHz}$, 2 µs dead time, LC filter (2 mH / 12.665 µF).
* **KiCad 9.0 Files:** `inverter.kicad_sch`, `inverter.kicad_pcb`, `inverter.kicad_pro`.
* **Simulation:** `pv_inverter.cir`, `mte3201_pv_inverter.py`.
* **Visual Asset:** `mte3201_waveforms_q2_q4_q5.png` (Transients, dead-time switching, 5-cycle FFT spectrum).

#### 3.2 USB 5V to 3.3V Board (`pd/usb_3v3_board/`)
* **Design Specs:** Compact 5V to 3.3V LDO regulator board with decoupling capacitors, status LED, and breakout pins.
* **Layout & Simulation:** `board_preview.svg`, `regulator_sim.cir`, `bom.csv`, `generate_pcb_svg.py`.

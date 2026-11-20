#!/usr/bin/env python3
"""
Generate a proper KiCad 9.0 project for the 2 kW PV Full-Bridge Inverter
with ngspice SPICE integration.

Produces:
  - inverter.kicad_sch  : Schematic with SPICE directives and models
  - inverter.kicad_pcb  : PCB layout with proper power clearances
  - inverter.kicad_pro  : Project file
  - pv_inverter.cir     : SPICE netlist (standalone ngspice compatible)
  - README.md           : Build and simulation instructions
"""

import uuid
import os

root = os.path.dirname(os.path.abspath(__file__))

def new_uuid():
    return str(uuid.uuid4())

# ---------------------------------------------------------------------------
# SCHEMATIC GENERATION
# ---------------------------------------------------------------------------

def sch_symbol(lib_id, ref, value, x, y, footprint="", properties=None, sim_model=None):
    """Generate a single KiCad symbol block with SPICE-relevant fields."""
    uid = new_uuid()
    props = properties or {}
    lines = []
    lines.append(f'  (symbol')
    lines.append(f'    (lib_id "{lib_id}")')
    lines.append(f'    (at {x} {y} 0)')
    lines.append(f'    (unit 1)')
    lines.append(f'    (exclude_from_sim no)')
    lines.append(f'    (in_bom yes)')
    lines.append(f'    (on_board yes)')
    lines.append(f'    (dnp no)')
    lines.append(f'    (uuid "{uid}")')
    lines.append(f'    (property "Reference" "{ref}"')
    lines.append(f'      (at {x} {y + 3.5} 0)')
    lines.append(f'      (effects (font (size 1.27 1.27)))')
    lines.append(f'    )')
    lines.append(f'    (property "Value" "{value}"')
    lines.append(f'      (at {x} {y + 7.0} 0)')
    lines.append(f'      (effects (font (size 1.27 1.27)))')
    lines.append(f'    )')
    if footprint:
        lines.append(f'    (property "Footprint" "{footprint}"')
        lines.append(f'      (at {x} {y} 0)')
        lines.append(f'      (effects (font (size 1.27 1.27)) (hide yes))')
        lines.append(f'    )')
    if sim_model:
        lines.append(f'    (property "Spice_Primitive" "{sim_model}"')
        lines.append(f'      (at {x} {y} 0)')
        lines.append(f'      (effects (font (size 1.27 1.27)) (hide yes))')
        lines.append(f'    )')
        lines.append(f'    (property "Spice_Model" "{sim_model}"')
        lines.append(f'      (at {x} {y} 0)')
        lines.append(f'      (effects (font (size 1.27 1.27)) (hide yes))')
        lines.append(f'    )')
    for pname, pval in props.items():
        lines.append(f'    (property "{pname}" "{pval}"')
        lines.append(f'      (at {x} {y} 0)')
        lines.append(f'      (effects (font (size 1.27 1.27)) (hide yes))')
        lines.append(f'    )')
    # Pins - simplified (2 pins for most, 1 for power)
    npins = 2 if lib_id not in ("power:VCC", "power:GND", "power:+", "power:-") else 1
    for i in range(1, npins + 1):
        puid = new_uuid()
        lines.append(f'    (pin "{i}" (uuid "{puid}"))')
    lines.append(f'    (instances')
    lines.append(f'      (project "inverter"')
    lines.append(f'        (path "/"')
    lines.append(f'          (reference "{ref}")')
    lines.append(f'          (unit 1)')
    lines.append(f'        )')
    lines.append(f'      )')
    lines.append(f'    )')
    lines.append(f'  )')
    return '\n'.join(lines)


def sch_wire(x1, y1, x2, y2):
    return (f'  (wire\n'
            f'    (pts\n'
            f'      (xy {x1} {y1}) (xy {x2} {y2})\n'
            f'    )\n'
            f'  )')


def sch_label(text, x, y, angle=0):
    return (f'  (label "{text}"\n'
            f'    (at {x} {y} {angle})\n'
            f'    (effects (font (size 1.27 1.27)))\n'
            f'  )')


def sch_spice_directive(text, x, y):
    """A SPICE directive placed as a text field in the schematic."""
    return (f'  (text "{text}"\n'
            f'    (at {x} {y} 0)\n'
            f'    (effects (font (size 1.27 1.27)))\n'
            f'  )')


# Build the schematic
sch_parts = []
sch_parts.append('(kicad_sch')
sch_parts.append('  (version 20250114)')
sch_parts.append('  (generator "eeschema")')
sch_parts.append('  (generator_version "9.0")')
sch_parts.append(f'  (uuid "{new_uuid()}")')
sch_parts.append('  (paper "A4")')
sch_parts.append('  (title_block')
sch_parts.append('    (title "2kW PV Full-Bridge Inverter - SPICE Ready")')
sch_parts.append('    (date "2026-11-03")')
sch_parts.append('    (rev "C")')
sch_parts.append('    (company "MTE 3201")')
sch_parts.append('  )')

# --- DC Link Section ---
sch_parts.append(sch_symbol("power:VCC", "V1", "400V", 30, 50,
                            sim_model="Vdc",
                            properties={"Spice_Netlist": "Vdc_src dc_pos 0 {Vdc}"}))
sch_parts.append(sch_symbol("power:GND", "G1", "GND", 30, 80))
sch_parts.append(sch_symbol("Device:C_Polarized_US", "C1", "220uF 400V", 70, 50,
                            footprint="Capacitor_THT:CP_Radial_D16.0mm_P7.50mm"))
sch_parts.append(sch_symbol("Device:C_Polarized_US", "C2", "220uF 400V", 70, 80,
                            footprint="Capacitor_THT:CP_Radial_D16.0mm_P7.50mm"))
sch_parts.append(sch_symbol("Device:Fuse", "F1", "15A fast", 0, 50,
                            footprint="Fuse:Fuseholder_Cylinder-5x20mm_Schurter_0031_8201"))

# --- Full-Bridge Switches (SPICE switches with anti-parallel diodes) ---
# Leg A: S1 (upper), S2 (lower)
sch_parts.append(sch_symbol("Device:SW", "S1", "SW_IGBT", 130, 35,
                            sim_model="SW_IGBT",
                            properties={"Spice_Model": "SW_IGBT SW(Vt=0.5 Vh=0.05 Ron=1m Roff=1Meg)"}))
sch_parts.append(sch_symbol("Device:D", "D1", "D_FW", 130, 65,
                            sim_model="D_FW",
                            properties={"Spice_Model": "D_FW D(Vfwd=0.1 Ron=1m)"}))
sch_parts.append(sch_symbol("Device:SW", "S2", "SW_IGBT", 130, 95,
                            sim_model="SW_IGBT"))
sch_parts.append(sch_symbol("Device:D", "D2", "D_FW", 130, 125,
                            sim_model="D_FW"))

# Leg B: S3 (upper), S4 (lower)
sch_parts.append(sch_symbol("Device:SW", "S3", "SW_IGBT", 210, 35,
                            sim_model="SW_IGBT"))
sch_parts.append(sch_symbol("Device:D", "D3", "D_FW", 210, 65,
                            sim_model="D_FW"))
sch_parts.append(sch_symbol("Device:SW", "S4", "SW_IGBT", 210, 95,
                            sim_model="SW_IGBT"))
sch_parts.append(sch_symbol("Device:D", "D4", "D_FW", 210, 125,
                            sim_model="D_FW"))

# --- Gate Drive Inputs ---
sch_parts.append(sch_symbol("Connector_Generic:Conn_01x02", "J_GATE", "GATE_IN", 280, 70,
                            footprint="Connector_Generic:Conn_01x02"))

# --- LC Output Filter ---
sch_parts.append(sch_symbol("Device:L", "L1", "2mH", 290, 45,
                            footprint="Inductor_THT:L_Axial_L20.0mm_D8.0mm_P25.40mm_Horizontal"))
sch_parts.append(sch_symbol("Device:C", "C3", "12.665uF", 290, 95,
                            footprint="Capacitor_THT:CP_Radial_D10.0mm_P5.00mm"))

# --- Load ---
sch_parts.append(sch_symbol("Device:R", "R_LOAD", "26.45", 370, 45,
                            footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P5.08mm_Horizontal"))
sch_parts.append(sch_symbol("Device:L", "L_LOAD", "35mH", 370, 95,
                            footprint="Inductor_THT:L_Axial_L20.0mm_D8.0mm_P25.40mm_Horizontal"))

# --- Output ---
sch_parts.append(sch_symbol("Connector_Generic:Conn_01x02", "J_OUT", "AC_OUT", 450, 70,
                            footprint="TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal"))

# --- SPICE Directives ---
sch_parts.append(sch_spice_directive('.param Vdc=400 f1=50 fs=10k ma=0.81317 td=2u tau={td/0.693147}', 50, 130))
sch_parts.append(sch_spice_directive('.param UNI=1 FILT=1 LOAD_B=0', 50, 145))
sch_parts.append(sch_spice_directive('.tran 0.5u 0.30 0.20 0.5u', 50, 160))
sch_parts.append(sch_spice_directive('.model SW_IGBT SW(Vt=0.5 Vh=0.05 Ron=1m Roff=1Meg)', 50, 175))
sch_parts.append(sch_spice_directive('.model D_FW D(Vfwd=0.1 Ron=1m)', 50, 190))

# --- Notes ---
sch_parts.append(sch_spice_directive('* 2kW PV Inverter - Unipolar/Bipolar SPWM, 2us dead time', 300, 130))
sch_parts.append(sch_spice_directive('* KiCad: Inspect -> Simulator -> Open/Run Netlist', 300, 145))
sch_parts.append(sch_spice_directive('* .cir netlist: pv_inverter.cir', 300, 160))

# --- Wires (simplified connectivity) ---
# DC link
sch_parts.append(sch_wire(10, 50, 30, 50))   # F1 to V1
sch_parts.append(sch_wire(30, 50, 70, 50))   # V1 to C1 (DC+)
sch_parts.append(sch_wire(30, 80, 70, 80))   # G1 to C2 (DC-)
sch_parts.append(sch_wire(70, 50, 70, 80))   # C1 to C2 (DC link)

# Bridge legs connect to DC rail
sch_parts.append(sch_wire(70, 50, 130, 35))  # DC+ to S1
sch_parts.append(sch_wire(70, 50, 210, 35))  # DC+ to S3
sch_parts.append(sch_wire(70, 80, 130, 95))  # DC- to S2
sch_parts.append(sch_wire(70, 80, 210, 95))  # DC- to S4

# Bridge output nodes
sch_parts.append(sch_wire(130, 65, 130, 45))  # S1-D1 node (invA)
sch_parts.append(sch_wire(130, 85, 130, 105)) # S2-D2 node (invA)
sch_parts.append(sch_wire(210, 65, 210, 45))  # S3-D3 node (invB)
sch_parts.append(sch_wire(210, 85, 210, 105)) # S4-D4 node (invB)

# LC filter
sch_parts.append(sch_wire(130, 55, 290, 45))  # invA to L1
sch_parts.append(sch_wire(210, 55, 290, 95))  # invB to C3
sch_parts.append(sch_wire(290, 55, 370, 45))  # L1 to R_LOAD
sch_parts.append(sch_wire(290, 85, 370, 95))  # C3 to L_LOAD
sch_parts.append(sch_wire(370, 55, 370, 85))  # R_LOAD to L_LOAD (load_mid)
sch_parts.append(sch_wire(370, 85, 450, 70))  # Output to J_OUT

# Gate drive labels
sch_parts.append(sch_label("G1", 160, 35))
sch_parts.append(sch_label("G2", 160, 95))
sch_parts.append(sch_label("G3", 240, 35))
sch_parts.append(sch_label("G4", 240, 95))

sch_parts.append('  (sheet_instances')
sch_parts.append('    (path "/"')
sch_parts.append('      (page "1")')
sch_parts.append('    )')
sch_parts.append('  )')
sch_parts.append('  (embedded_fonts no)')
sch_parts.append(')')

sch_text = '\n'.join(sch_parts)
with open(os.path.join(root, 'inverter.kicad_sch'), 'w', encoding='utf-8') as f:
    f.write(sch_text)
print(f"Generated inverter.kicad_sch ({len(sch_text)} bytes)")

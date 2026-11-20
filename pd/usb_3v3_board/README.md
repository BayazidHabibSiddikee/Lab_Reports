# USB 5V to 3.3V regulator board

This project is a compact, printable PCB concept for a small regulator board. It is intentionally simple so it can be adjusted to your real hardware quickly.

## What this design includes
- 5V input (USB or barrel supply)
- 3.3V LDO regulator stage
- Input and output decoupling capacitors
- Status LED with current-limit resistor
- 6-pin breakout header for VCC, GND, and GPIO signals
- Printable SVG board layout suitable for prototype fabrication or paper mockups

## Files
- `generate_pcb_svg.py` — generates the printable board layout
- `board_preview.svg` — rendered board preview
- `regulator_sim.cir` — ngspice-ready circuit simulation
- `bom.csv` — simple component list

## How to use
1. Edit `generate_pcb_svg.py` to match your preferred dimensions and pins.
2. Run:
   `python3 generate_pcb_svg.py`
3. Open `board_preview.svg` in a browser or print it to PDF.
4. Use `ngspice regulator_sim.cir` to verify the 5V to 3.3V stage is stable.

## Recommended next edits for a real product
- Replace the generic linear regulator with your exact part number.
- Add a reset circuit and ESD protection if the board connects to external modules.
- Expand the board to a 2-layer PCB if you need more routing density.
- Export gerbers from KiCad if you want a full fabrication-ready board.

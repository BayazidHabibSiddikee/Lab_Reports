#!/usr/bin/env python3
"""Generate a printable PCB concept as SVG.

This is a simple starter board for a 5V input -> 3.3V LDO breakout.
It is designed to be easy to tweak before moving to a full KiCad layout.
"""

from pathlib import Path

OUT = Path(__file__).with_name("board_preview.svg")

BOARD_W = 120
BOARD_H = 80


def rect(x, y, w, h, fill="#dfe7ef", stroke="#1a1d24", stroke_w=1.5, rx=3):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}" rx="{rx}"/>'


def line(x1, y1, x2, y2, color="#1a1d24", stroke_w=2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{stroke_w}" stroke-linecap="round"/>'


def circle(cx, cy, r, fill="#ffffff", stroke="#1a1d24", stroke_w=1.5):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}"/>'


def text(x, y, label, size=12, anchor="middle", weight="normal", fill="#1b1b1b"):
    return f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}">{label}</text>'


def build_svg():
    parts = []
    parts.append('<?xml version="1.0" encoding="UTF-8"?>')
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{BOARD_W*4}" height="{BOARD_H*4}" viewBox="0 0 {BOARD_W} {BOARD_H}">')
    parts.append('<rect x="0" y="0" width="100%" height="100%" fill="#f6f8fb"/>')

    parts.append(rect(3, 3, BOARD_W - 6, BOARD_H - 6, fill="#eef3f8", stroke="#2b2f36", stroke_w=1.1, rx=3))

    parts.append(line(12, 35, 27, 35, stroke_w=2.5))
    parts.append(line(12, 53, 27, 53, stroke_w=2.5))
    parts.append(line(27, 35, 27, 53, stroke_w=2.5))
    parts.append(line(30, 44, 70, 44, stroke_w=2.5))
    parts.append(line(70, 44, 70, 30, stroke_w=2.5))
    parts.append(line(70, 44, 89, 44, stroke_w=2.5))
    parts.append(line(89, 44, 89, 28, stroke_w=2.5))
    parts.append(line(89, 44, 97, 44, stroke_w=2.5))

    parts.append(rect(9, 28, 12, 20, fill="#d7e0ea", stroke="#1a1d24", stroke_w=1.2, rx=2))
    parts.append(text(15, 30.5, "USB", 5.5, anchor="middle", weight="bold"))
    parts.append(text(15, 36, "5V", 4.5, anchor="middle"))
    parts.append(line(21, 28, 27, 28, stroke_w=1.7))
    parts.append(line(21, 48, 27, 48, stroke_w=1.7))

    parts.append(rect(32, 25, 14, 14, fill="#d7e0ea", stroke="#1a1d24", stroke_w=1.2, rx=2))
    parts.append(text(39, 33.5, "LDO", 5.5, anchor="middle", weight="bold"))
    parts.append(text(39, 39.5, "AMS1117", 4.5, anchor="middle"))

    parts.append(rect(31, 44, 5, 6, fill="#f4d6a0", stroke="#1a1d24", stroke_w=1.2, rx=1))
    parts.append(text(33.5, 48.5, "10u", 4, anchor="middle"))

    parts.append(rect(58, 25, 5, 6, fill="#f4d6a0", stroke="#1a1d24", stroke_w=1.2, rx=1))
    parts.append(text(60.5, 29.5, "10u", 4, anchor="middle"))

    parts.append(rect(76, 38, 10, 10, fill="#f9d4d4", stroke="#1a1d24", stroke_w=1.2, rx=2))
    parts.append(circle(81, 43, 3.2, fill="#ffffff", stroke="#1a1d24", stroke_w=1.1))
    parts.append(text(81, 47, "LED", 4.5, anchor="middle"))
    parts.append(line(74, 43, 76, 43, stroke_w=1.8))
    parts.append(line(86, 43, 89, 43, stroke_w=1.8))
    parts.append(rect(90, 39, 7, 8, fill="#f0f1c8", stroke="#1a1d24", stroke_w=1.2, rx=1))
    parts.append(text(93.5, 43.5, "330R", 4, anchor="middle"))

    parts.append(rect(95, 22, 15, 16, fill="#dfe7ef", stroke="#1a1d24", stroke_w=1.2, rx=2))
    parts.append(text(102.5, 27.5, "OUT", 5, anchor="middle", weight="bold"))
    parts.append(line(95, 29, 92, 29, stroke_w=1.7))
    parts.append(line(95, 33.2, 92, 33.2, stroke_w=1.7))
    for i, lbl in enumerate(["3.3V", "GND", "GPIO0", "GPIO1"]):
        y = 25 + i * 5.4
        parts.append(text(100, y, lbl, 4, anchor="middle"))

    parts.append(text(40, 18, "VIN 5V", 4.6, anchor="middle"))
    parts.append(text(80, 18, "VOUT 3.3V", 4.6, anchor="middle"))
    parts.append(text(60, 67, "Printable prototype board concept", 5.6, anchor="middle", weight="bold"))
    parts.append(text(60, 72, "Adjust trace routing and pads to match your exact part library", 4.2, anchor="middle"))

    parts.append('</svg>')
    return "\n".join(parts)


if __name__ == "__main__":
    OUT.write_text(build_svg(), encoding="utf-8")
    print(f"Generated {OUT}")

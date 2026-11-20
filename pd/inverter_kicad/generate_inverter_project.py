#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parent

proj = {
    "meta": {"filename": "inverter.kicad_pro", "version": 1},
    "board": {
        "design_settings": {
            "defaults": {"board_outline_line_width": 0.1, "copper_line_width": 0.15},
            "rule_severities": {"clearance": "error"},
            "rules": {"min_track_width": 0.2, "min_hole_to_hole": 0.25}
        }
    },
    "lib": {"pinned_footprint_libs": [], "pinned_symbol_libs": []},
    "net_settings": {"classes": [{"name": "Default","clearance": 0.2,"diff_pair_gap": 0.25,"diff_pair_via_gap": 0.25,"diff_pair_width": 0.2,"microvia_diameter": 0.4,"microvia_drill": 0.1,"name": "Default","solder_mask_clearance": 0.0,"solder_mask_min_width": 0.0,"track_width": 0.2,"via_diameter": 0.6,"via_drill": 0.3,"wire_width": 0.2,"nets": []}]},
    "pcbnew": {"last_paths": {"file": ""}, "page_layout": ""},
    "schematic": {"sheet": [{"name": "Sheet1", "page": 1}]},
}

# Minimal KiCad project file.
project_text = '''{
  "meta": {
    "filename": "inverter.kicad_pro",
    "version": 1
  },
  "board": {
    "design_settings": {
      "defaults": {
        "board_outline_line_width": 0.1,
        "copper_line_width": 0.15,
        "copper_text_size_h": 1.5,
        "copper_text_size_v": 1.5,
        "copper_text_thickness": 0.3,
        "fab_line_width": 0.1,
        "fab_text_size_h": 1.0,
        "fab_text_size_v": 1.0,
        "fab_text_thickness": 0.15,
        "other_line_width": 0.1,
        "silk_line_width": 0.15,
        "silk_text_size_h": 1.0,
        "silk_text_size_v": 1.0,
        "silk_text_thickness": 0.15,
        "zones": { "45_degree_only": false, "min_clearance": 0.508 }
      },
      "rule_severities": {
        "clearance": "error",
        "connection_width": "warning",
        "copper_edge_clearance": "error",
        "courtyards_overlap": "error",
        "diff_pair_gap_out_of_range": "error",
        "drill_out_of_range": "error",
        "duplicate_footprints": "warning",
        "footprint": "error",
        "hole_clearance": "error",
        "missing_footprint": "warning",
        "shorting_items": "error",
        "track_dangling": "warning"
      },
      "rules": {
        "min_clearance": 0.0,
        "min_connection": 0.0,
        "min_copper_edge_clearance": 0.05,
        "min_hole_clearance": 0.0,
        "min_hole_to_hole": 0.25,
        "min_track_width": 0.2,
        "min_via_annular_width": 0.05,
        "min_via_diameter": 0.4,
        "solder_mask_to_copper_clearance": 0.0,
        "use_height_for_length_calcs": true
      }
    }
  },
  "lib": {
    "pinned_footprint_libs": [],
    "pinned_symbol_libs": []
  },
  "net_settings": {
    "classes": [
      {
        "clearance": 0.2,
        "diff_pair_gap": 0.25,
        "diff_pair_via_gap": 0.25,
        "diff_pair_width": 0.2,
        "microvia_diameter": 0.4,
        "microvia_drill": 0.1,
        "name": "Default",
        "solder_mask_clearance": 0.0,
        "solder_mask_min_width": 0.0,
        "track_width": 0.2,
        "via_diameter": 0.6,
        "via_drill": 0.3,
        "wire_width": 0.2,
        "nets": []
      }
    ]
  },
  "pcbnew": {
    "last_paths": {
      "file": ""
    },
    "page_layout": ""
  },
  "schematic": {
    "sheet": [
      {
        "name": "Sheet1",
        "page": 1
      }
    ]
  }
}
'''

sch = '''(kicad_sch
    (version 20250114)
    (generator "eeschema")
    (generator_version "9.0")
    (uuid "9a59a81d-fd85-4fc4-a1ce-dff7f16584b7")
    (paper "A4")
    (title_block
        (title "12V to 230VAC Inverter")
        (date "2026-11-01")
        (rev "A")
        (company "Conceptual prototype")
    )
    (symbol
        (lib_id "Connector_Generic:Conn_01x02")
        (at 17.78 45.72 0)
        (unit 1)
        (exclude_from_sim no)
        (in_bom yes)
        (on_board yes)
        (dnp no)
        (uuid "dfb99b94-62ce-43e9-8f15-a8e057b6631b")
        (property "Reference" "J1"
            (at 17.78 41.91 0)
            (effects (font (size 1.27 1.27)))
        )
        (property "Value" "DC_IN"
            (at 17.78 49.53 0)
            (effects (font (size 1.27 1.27)))
        )
        (property "Footprint" ""
            (at 17.78 45.72 0)
            (effects (font (size 1.27 1.27)) (hide yes))
        )
        (property "Datasheet" "~"
            (at 17.78 45.72 0)
            (effects (font (size 1.27 1.27)) (hide yes))
        )
        (property "Description" "Generic connector, single row, 01x02"
            (at 17.78 45.72 0)
            (effects (font (size 1.27 1.27)) (hide yes))
        )
        (pin "1" (uuid "1d2e5d19-d0bc-4258-aa0b-17a3f769a3db"))
        (pin "2" (uuid "b83d0af7-7b1e-4f20-bf2a-8501126926db"))
        (instances
            (project "inverter"
                (path "/"
                    (reference "J1")
                    (unit 1)
                )
            )
        )
    )
    (symbol
        (lib_id "Device:Fuse")
        (at 27.94 45.72 0)
        (unit 1)
        (exclude_from_sim no)
        (in_bom yes)
        (on_board yes)
        (dnp no)
        (uuid "3bca51d9-93e3-4f13-8dc0-8f9308df6304")
        (property "Reference" "F1"
            (at 27.94 41.91 0)
            (effects (font (size 1.27 1.27)))
        )
        (property "Value" "20A"
            (at 27.94 48.26 0)
            (effects (font (size 1.27 1.27)))
        )
        (property "Footprint" ""
            (at 27.94 45.72 0)
            (effects (font (size 1.27 1.27)) (hide yes))
        )
        (property "Datasheet" "~"
            (at 27.94 45.72 0)
            (effects (font (size 1.27 1.27)) (hide yes))
        )
        (pin "1" (uuid "c23765f9-fbce-437d-9d15-f49cc10b0d39"))
        (pin "2" (uuid "32bdb6ea-53cc-49d1-8d92-2cf6e6e38f62"))
        (instances
            (project "inverter"
                (path "/"
                    (reference "F1")
                    (unit 1)
                )
            )
        )
    )
    (symbol
        (lib_id "Device:C_Polarized")
        (at 39.37 45.72 0)
        (unit 1)
        (exclude_from_sim no)
        (in_bom yes)
        (on_board yes)
        (dnp no)
        (uuid "d2201c54-f66e-40d2-b73d-9369238e1add")
        (property "Reference" "C1"
            (at 39.37 41.91 0)
            (effects (font (size 1.27 1.27)))
        )
        (property "Value" "1000uF"
            (at 39.37 49.53 0)
            (effects (font (size 1.27 1.27)))
        )
        (property "Footprint" ""
            (at 39.37 45.72 0)
            (effects (font (size 1.27 1.27)) (hide yes))
        )
        (pin "1" (uuid "d697c2d7-1e48-4ea8-b1bb-1ef4b82311df"))
        (pin "2" (uuid "a911d6c9-2a4f-4df3-8d79-1ec1b7eb16fb"))
        (instances
            (project "inverter"
                (path "/"
                    (reference "C1")
                    (unit 1)
                )
            )
        )
    )
    (symbol
        (lib_id "Connector_Generic:Conn_01x04")
        (at 53.34 45.72 0)
        (unit 1)
        (exclude_from_sim no)
        (in_bom yes)
        (on_board yes)
        (dnp no)
        (uuid "15d4d6be-867d-426c-b93d-9f5f1d426b7c")
        (property "Reference" "U1"
            (at 53.34 41.91 0)
            (effects (font (size 1.27 1.27)))
        )
        (property "Value" "Oscillator / Driver"
            (at 53.34 53.34 0)
            (effects (font (size 1.27 1.27)))
        )
        (property "Footprint" ""
            (at 53.34 45.72 0)
            (effects (font (size 1.27 1.27)) (hide yes))
        )
        (pin "1" (uuid "b8e7c9dc-3d22-4feb-bd59-ab4cf040bb2c"))
        (pin "2" (uuid "62380ff4-d4ab-4e1e-9fe7-57af0e3d5b85"))
        (pin "3" (uuid "3d4e8c8e-d4a3-4707-9865-0173d24875d7"))
        (pin "4" (uuid "0db47631-cd08-4a4b-b2df-81eb5f7a16a5"))
        (instances
            (project "inverter"
                (path "/"
                    (reference "U1")
                    (unit 1)
                )
            )
        )
    )
    (symbol
        (lib_id "Device:Transformer_1P_2S")
        (at 68.58 45.72 0)
        (unit 1)
        (exclude_from_sim no)
        (in_bom yes)
        (on_board yes)
        (dnp no)
        (uuid "a07c87d8-96df-49f6-990f-8aef6add19a1")
        (property "Reference" "T1"
            (at 68.58 41.91 0)
            (effects (font (size 1.27 1.27)))
        )
        (property "Value" "12-0-12 to 230VAC"
            (at 68.58 53.34 0)
            (effects (font (size 1.27 1.27)))
        )
        (property "Footprint" ""
            (at 68.58 45.72 0)
            (effects (font (size 1.27 1.27)) (hide yes))
        )
        (pin "1" (uuid "7930a643-9bf1-4fe6-97bc-f90d5d87c2d2"))
        (pin "2" (uuid "496f8ef4-0cdb-4045-9f94-9ef2d3d0da01"))
        (pin "3" (uuid "a83e4bcd-72a9-4558-be9c-a5e8dd48d5d5"))
        (pin "4" (uuid "269edd7b-00a8-4e31-a563-d0468eb56b2a"))
        (instances
            (project "inverter"
                (path "/"
                    (reference "T1")
                    (unit 1)
                )
            )
        )
    )
    (symbol
        (lib_id "Connector_Generic:Conn_01x02")
        (at 82.55 45.72 0)
        (unit 1)
        (exclude_from_sim no)
        (in_bom yes)
        (on_board yes)
        (dnp no)
        (uuid "2fbe2b2d-10b7-4d27-a7d6-c26a892d5d65")
        (property "Reference" "J2"
            (at 82.55 41.91 0)
            (effects (font (size 1.27 1.27)))
        )
        (property "Value" "AC_OUT"
            (at 82.55 49.53 0)
            (effects (font (size 1.27 1.27)))
        )
        (property "Footprint" ""
            (at 82.55 45.72 0)
            (effects (font (size 1.27 1.27)) (hide yes))
        )
        (pin "1" (uuid "6eb28ee9-b2ff-4ba1-a911-6f789f07d631"))
        (pin "2" (uuid "4f7f6ef7-f2d4-4ef7-9af6-7ea08ccb6a5d"))
        (instances
            (project "inverter"
                (path "/"
                    (reference "J2")
                    (unit 1)
                )
            )
        )
    )
    (symbol
        (lib_id "power:GND")
        (at 41.91 58.42 0)
        (unit 1)
        (exclude_from_sim no)
        (in_bom yes)
        (on_board yes)
        (dnp no)
        (uuid "162f4a6e-c3d4-49d8-a2cb-4001630d5798")
        (property "Reference" "#PWR01"
            (at 41.91 63.5 0)
            (effects (font (size 1.27 1.27)) (hide yes))
        )
        (property "Value" "GND"
            (at 41.91 60.96 0)
            (effects (font (size 1.27 1.27)))
        )
        (pin "1" (uuid "37597901-3d8f-4d6e-b88b-1d6c7b0616d7"))
        (instances
            (project "inverter"
                (path "/"
                    (reference "#PWR01")
                    (unit 1)
                )
            )
        )
    )
    (wire
        (pts
            (xy 20.32 45.72) (xy 24.13 45.72)
        )
    )
    (wire
        (pts
            (xy 31.75 45.72) (xy 35.56 45.72)
        )
    )
    (wire
        (pts
            (xy 43.18 45.72) (xy 48.26 45.72)
        )
    )
    (wire
        (pts
            (xy 58.42 45.72) (xy 64.77 45.72)
        )
    )
    (wire
        (pts
            (xy 73.66 45.72) (xy 78.74 45.72)
        )
    )
    (wire
        (pts
            (xy 39.37 58.42) (xy 39.37 49.53)
        )
    )
    (wire
        (pts
            (xy 39.37 58.42) (xy 41.91 58.42)
        )
    )
    (label "VIN+"
        (at 22.86 45.72 0)
        (effects (font (size 1.27 1.27)))
    )
    (label "VIN-"
        (at 39.37 54.61 90)
        (effects (font (size 1.27 1.27)))
    )
    (label "DRV_A"
        (at 55.88 45.72 0)
        (effects (font (size 1.27 1.27)))
    )
    (label "DRV_B"
        (at 68.58 45.72 0)
        (effects (font (size 1.27 1.27)))
    )
    (label "AC_L"
        (at 84.09 45.72 0)
        (effects (font (size 1.27 1.27)))
    )
    (label "AC_N"
        (at 84.09 48.26 0)
        (effects (font (size 1.27 1.27)))
    )
    (sheet_instances
        (path "/"
            (page "1")
        )
    )
    (embedded_fonts no)
)
'''

(root / 'inverter.kicad_pro').write_text(project_text, encoding='utf-8')
(root / 'inverter.kicad_sch').write_text(sch, encoding='utf-8')
(root / 'README.md').write_text('''# Conceptual inverter KiCad project\n\nThis project is a simple low-power DC-to-AC inverter concept drawn in KiCad: 12V input -> fuse -> bulk capacitor -> oscillator/driver -> transformer -> 230VAC output.\n\nFiles:\n- inverter.kicad_pro\n- inverter.kicad_sch\n- generate_inverter_project.py\n\nImportant: this is a conceptual schematic for an initial design. A real inverter must include proper gate drive, snubbers, thermal management, safety isolation, and tested transformer design before being built or used at mains voltage.\n''', encoding='utf-8')
print('Generated inverter project files in', root)

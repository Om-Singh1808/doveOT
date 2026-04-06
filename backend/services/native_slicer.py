from pathlib import Path
from typing import List

import numpy as np
import trimesh


class NativeSlicer:
    """Minimal in-process slicer for MVP independence."""

    def __init__(self, output_dir: str | None = None):
        default_output = Path(__file__).resolve().parents[2] / "output" / "gcode"
        self.output_dir = Path(output_dir) if output_dir else default_output
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def slice_to_gcode(self, stl_path: str, settings: dict) -> str:
        mesh = trimesh.load(stl_path, file_type="stl")
        if mesh.is_empty:
            raise ValueError("Cannot slice empty mesh")

        layer_height = float(settings.get("layer_height_mm", 0.2))
        perimeters = max(1, int(settings.get("perimeters", 2)))
        nozzle_temp = int(settings.get("nozzle_temp_c", 200))
        bed_temp = int(settings.get("bed_temp_c", 60))
        speed = float(settings.get("print_speed_mm_s", 50.0))

        filename = Path(stl_path).with_suffix(".gcode").name
        output_path = self.output_dir / filename

        bounds = mesh.bounds
        z_min = float(bounds[0][2])
        z_max = float(bounds[1][2])
        layers = np.arange(z_min + layer_height, z_max + (layer_height * 0.5), layer_height)

        lines: List[str] = []
        e_value = 0.0
        e_per_mm = self._extrusion_per_mm(layer_height)
        feed_xy = int(speed * 60.0)

        lines.extend(
            [
                "; DoveOT native slicer output",
                f"; source={Path(stl_path).name}",
                "G90",
                "M82",
                "G21",
                f"M104 S{nozzle_temp}",
                f"M140 S{bed_temp}",
                "M109 S200",
                "M190 S60",
                "G28",
                "G92 E0",
                "G1 Z5 F3000",
            ]
        )

        for layer_idx, z in enumerate(layers, start=1):
            section = mesh.section(plane_origin=[0.0, 0.0, float(z)], plane_normal=[0.0, 0.0, 1.0])
            if section is None:
                continue

            planar, _ = section.to_planar()
            polygons = planar.polygons_full
            if not polygons:
                continue

            lines.append(f";LAYER:{layer_idx}")
            lines.append(f"G1 Z{z:.3f} F1200")

            for poly in polygons:
                coords = list(poly.exterior.coords)
                if len(coords) < 3:
                    continue

                # Repeat perimeter loops as an MVP approximation.
                for _ in range(perimeters):
                    start_x, start_y = coords[0][0], coords[0][1]
                    lines.append(f"G0 X{start_x:.3f} Y{start_y:.3f} F6000")

                    prev_x, prev_y = start_x, start_y
                    for x, y in coords[1:]:
                        segment = float(np.hypot(x - prev_x, y - prev_y))
                        e_value += segment * e_per_mm
                        lines.append(f"G1 X{x:.3f} Y{y:.3f} E{e_value:.5f} F{feed_xy}")
                        prev_x, prev_y = x, y

        lines.extend(
            [
                "G1 E-1 F1800",
                "G1 Z10 F3000",
                "M104 S0",
                "M140 S0",
                "M84",
            ]
        )

        output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return str(output_path)

    def _extrusion_per_mm(self, layer_height: float) -> float:
        filament_diameter = 1.75
        line_width = 0.42
        filament_area = np.pi * ((filament_diameter / 2.0) ** 2)
        bead_area = line_width * layer_height
        return bead_area / filament_area

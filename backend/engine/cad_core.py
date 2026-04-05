import math
import uuid
from pathlib import Path
from typing import Dict, Tuple

import trimesh

try:
    import bpy  # type: ignore
except Exception:
    bpy = None


class NativeCadEngine:
    """Embedded CAD engine using bpy when available."""

    def __init__(self, output_dir: str | None = None):
        default_output = Path(__file__).resolve().parents[2] / "output" / "stl"
        self.output_dir = Path(output_dir) if output_dir else default_output
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_backend_name(self) -> str:
        return "bpy" if bpy is not None else "trimesh-fallback"

    def generate_stl(self, vibe_params: Dict) -> str:
        job_id = str(uuid.uuid4())
        output_stl_path = self.output_dir / f"{job_id}.stl"

        if bpy is not None:
            self._generate_with_bpy(vibe_params, output_stl_path)
        else:
            self._generate_with_trimesh_fallback(vibe_params, output_stl_path)

        return str(output_stl_path)

    def _generate_with_bpy(self, vibe_params: Dict, output_path: Path) -> None:
        self._cleanup_scene()

        archetype = vibe_params.get("archetype", "stand")
        if archetype == "stand":
            obj = self._generate_stand(vibe_params)
        else:
            obj = self._generate_stand(vibe_params)

        if obj is None:
            raise ValueError(f"Failed to generate geometry for archetype '{archetype}'")

        bpy.ops.object.select_all(action="DESELECT")
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        bpy.ops.export_mesh.stl(
            filepath=str(output_path),
            use_selection=True,
            global_scale=1.0,
            use_scene_unit=False,
        )

    def _cleanup_scene(self) -> None:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        for obj in list(bpy.data.objects):
            bpy.data.objects.remove(obj)

    def _generate_stand(self, params: Dict):
        softness = float(params.get("softness", 0.5))
        weight = float(params.get("weight", 0.5))
        height_ratio = float(params.get("height_ratio", 0.5))
        fluidity = float(params.get("fluidity", 0.5))

        stand_angle = 50 + (30 * fluidity)
        thickness = 2.0 + (3.0 * weight)
        z_scale = 0.5 + (2.0 * height_ratio)
        extrude_depth = 80.0

        curve_data = bpy.data.curves.new("StandProfile", type="CURVE")
        curve_data.dimensions = "2D"
        curve_data.extrude = extrude_depth / 2.0

        spline = curve_data.splines.new("BEZIER")

        base_length = 50.0 * z_scale
        back_length = 80.0 * z_scale
        lip_length = 15.0

        p0 = (0, lip_length, thickness)
        p1 = (0, 0, thickness)
        angle_rad = math.radians(stand_angle)
        p2_y = -base_length
        p2_z = thickness + (math.sin(angle_rad) * back_length)
        p2 = (0, p2_y, p2_z)

        points = [p0, p1, p2]
        spline.bezier_points.add(len(points) - 1)

        for i, p in enumerate(points):
            bp = spline.bezier_points[i]
            bp.co = p
            bp.handle_left_type = "AUTO"
            bp.handle_right_type = "AUTO"

        stand_obj = bpy.data.objects.new("NativeStand", curve_data)
        bpy.context.collection.objects.link(stand_obj)

        bpy.context.view_layer.objects.active = stand_obj
        stand_obj.select_set(True)
        bpy.ops.object.convert(target="MESH")

        solidify = stand_obj.modifiers.new("Solidify", "SOLIDIFY")
        solidify.thickness = thickness
        solidify.offset = 0
        bpy.ops.object.modifier_apply(modifier="Solidify")

        if softness > 0.1:
            bevel = stand_obj.modifiers.new("Bevel", "BEVEL")
            bevel.segments = int(softness * 10) + 2
            bevel.width = softness * 5.0
            bevel.limit_method = "ANGLE"
            bpy.ops.object.modifier_apply(modifier="Bevel")

        return stand_obj

    def _generate_with_trimesh_fallback(self, vibe_params: Dict, output_path: Path) -> None:
        width, depth, height = self._fallback_extents(vibe_params)
        mesh = trimesh.creation.box(extents=[width, depth, height])
        mesh.export(str(output_path))

    def _fallback_extents(self, vibe_params: Dict) -> Tuple[float, float, float]:
        weight = float(vibe_params.get("weight", 0.5))
        height_ratio = float(vibe_params.get("height_ratio", 0.5))
        complexity = float(vibe_params.get("complexity", 0.5))

        width = 50.0 + (weight * 35.0)
        depth = 40.0 + (complexity * 30.0)
        height = 20.0 + (height_ratio * 70.0)
        return width, depth, height

import trimesh
import numpy as np
from pydantic import BaseModel

class PrintabilityReport(BaseModel):
    overhang_face_count: int
    overhang_area_mm2: float
    overhang_percentage: float
    needs_support: bool
    bounding_box_mm: tuple[float, float, float]
    score: float

class PrintAnalyzer:
    def __init__(self, overhang_threshold_deg: float = 45.0):
        self.overhang_threshold_deg = overhang_threshold_deg
        
    def analyze_stl(self, stl_path: str) -> PrintabilityReport:
        mesh = trimesh.load(stl_path, file_type='stl')
        
        # 1. Bounding box
        extents = mesh.extents
        bbox = (float(extents[0]), float(extents[1]), float(extents[2]))
        
        # 2. Overhang Detection
        build_dir = np.array([0, 0, -1])  # gravity direction
        normals = mesh.face_normals
        
        # Angle between face normal and gravity
        # clip to handle floating point inaccuracies before arccos
        dot = np.clip(np.dot(normals, build_dir), -1.0, 1.0)
        angles = np.degrees(np.arccos(dot))
        
        # Faces where angle to gravity is less than (90 - threshold) need support
        # Example: if normal points exactly down (0 degrees), it's 100% overhang.
        # Threshold 45 means anything less than 45 degrees to gravity requires support.
        overhang_mask = angles < (self.overhang_threshold_deg)
        overhang_faces = np.where(overhang_mask)[0]
        
        overhang_area = float(mesh.area_faces[overhang_mask].sum())
        total_area = float(mesh.area)
        overhang_percentage = (overhang_area / total_area * 100) if total_area > 0 else 0.0
        
        needs_support = overhang_percentage > 2.0  # Allow some noise
        
        # Simple score based on overhang percentage (100 = perfect, 0 = terrible)
        score = max(0.0, 100.0 - (overhang_percentage * 2))
        
        return PrintabilityReport(
            overhang_face_count=len(overhang_faces),
            overhang_area_mm2=overhang_area,
            overhang_percentage=overhang_percentage,
            needs_support=needs_support,
            bounding_box_mm=bbox,
            score=score
        )

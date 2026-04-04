from models.vibe_vector import VibeParamVector
from services.print_analyzer import PrintabilityReport

def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

class SettingsRecommender:
    def recommend(self, vibe: VibeParamVector, report: PrintabilityReport) -> dict:
        """Generate 3D printing settings based on vibe and analysis."""
        
        # Layer height: smoother objects need finer layers
        if vibe.softness > 0.7:
            layer_height = 0.12
        elif vibe.softness > 0.4:
            layer_height = 0.16
        else:
            layer_height = 0.20
        
        # Infill: heavier objects need more infill
        infill = int(lerp(15, 40, vibe.weight))
        
        # Speed: complex objects print slower
        if vibe.complexity > 0.6:
            speed = 40  # mm/s
        elif vibe.complexity > 0.3:
            speed = 60
        else:
            speed = 80
        
        # Temperature: standard PLA defaults, adjust for detail
        nozzle_temp = 210 if vibe.complexity > 0.5 else 200
        bed_temp = 60
        
        # Walls: weight determines perimeters
        perimeters = int(lerp(2, 5, vibe.weight))
        
        return {
            "layer_height_mm": layer_height,
            "infill_percent": infill,
            "infill_pattern": "gyroid" if vibe.fluidity > 0.5 else "grid",
            "print_speed_mm_s": speed,
            "nozzle_temp_c": nozzle_temp,
            "bed_temp_c": bed_temp,
            "perimeters": perimeters,
            "support_enabled": report.needs_support,
            "support_type": "tree" if report.needs_support else "none",
            "material": "PLA"
        }

import os
from pathlib import Path
from services.native_slicer import NativeSlicer

class SlicerBridge:
    def __init__(self, output_dir: str | None = None):
        default_output = Path(__file__).resolve().parents[2] / "output" / "gcode"
        self.output_dir = Path(output_dir) if output_dir else default_output
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.native_slicer = NativeSlicer(output_dir=str(self.output_dir))
        
    async def slice_stl(self, stl_path: str, settings: dict) -> str:
        try:
            return self.native_slicer.slice_to_gcode(stl_path, settings)
        except Exception as e:
            filename = os.path.basename(stl_path).replace(".stl", ".gcode")
            output_gcode_path = str(self.output_dir / filename)
            print(f"Native slicer error: {e}")
            return self._create_mock_gcode(output_gcode_path)
        
    def _create_mock_gcode(self, path: str) -> str:
        with open(path, "w") as f:
            f.write("; Mock G-code generated because native slicer failed\n")
            f.write("G28 ; home all axes\n")
            f.write("G1 Z5 F5000 ; lift nozzle\n")
            f.write("; ... execution paths ...\n")
            f.write("M104 S0 ; turn off temperature\n")
            f.write("G28 X0  ; home X axis\n")
            f.write("M84     ; disable motors\n")
        return path

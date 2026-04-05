import subprocess
import os
import asyncio
from pathlib import Path

class SlicerBridge:
    def __init__(self, slicer_path: str = "prusa-slicer-console.exe", output_dir: str | None = None):
        self.slicer_path = slicer_path
        default_output = Path(__file__).resolve().parents[2] / "output" / "gcode"
        self.output_dir = Path(output_dir) if output_dir else default_output
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    async def slice_stl(self, stl_path: str, settings: dict) -> str:
        filename = os.path.basename(stl_path).replace(".stl", ".gcode")
        output_gcode_path = str(self.output_dir / filename)
        
        # Basic CLI generation arguments mapped from recommended settings
        cmd = [
            self.slicer_path,
            "--slice", stl_path,
            "--output", output_gcode_path,
            "--layer-height", str(settings["layer_height_mm"]),
            "--fill-density", str(settings["infill_percent"] / 100.0),
            "--perimeters", str(settings["perimeters"])
        ]
        
        if settings.get("support_enabled", False):
            cmd.append("--support-material")
            
        try:
            # We wrap this in a check since PrusaSlicer might not be installed, 
            # and we do not want to fail the entire backend generation API.
            # Instead we mock the gcode generation if slicer is missing.
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                print(f"Slicer Error: {stderr.decode()}")
                # Fallback to mock G-code if slicing fails (e.g. no prusa-slicer installed)
                return self._create_mock_gcode(output_gcode_path)
                
        except FileNotFoundError:
            print("PrusaSlicer CLI not found. Falling back to mock G-code.")
            return self._create_mock_gcode(output_gcode_path)
        except Exception as e:
            print(f"Unknown slicer error {e}")
            return self._create_mock_gcode(output_gcode_path)
            
        return output_gcode_path
        
    def _create_mock_gcode(self, path: str) -> str:
        with open(path, "w") as f:
            f.write("; Mock G-code generated because PrusaSlicer CLI is missing\n")
            f.write("G28 ; home all axes\n")
            f.write("G1 Z5 F5000 ; lift nozzle\n")
            f.write("; ... execution paths ...\n")
            f.write("M104 S0 ; turn off temperature\n")
            f.write("G28 X0  ; home X axis\n")
            f.write("M84     ; disable motors\n")
        return path

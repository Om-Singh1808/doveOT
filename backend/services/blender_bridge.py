import subprocess
import json
import os
import uuid
import asyncio
from typing import Optional

class BlenderBridge:
    def __init__(self, output_dir: str = "../output"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "stl"), exist_ok=True)
        
    async def generate_stl(self, vibe_params: dict) -> str:
        job_id = str(uuid.uuid4())
        
        # Save params to temp json
        params_path = os.path.join(self.output_dir, f"{job_id}_params.json")
        output_stl_path = os.path.join(self.output_dir, "stl", f"{job_id}.stl")
        
        with open(params_path, "w") as f:
            json.dump(vibe_params, f)
            
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "blender", "generate_model.py")
        
        # Replace 'blender' with path to your blender executable if not in PATH
        cmd = [
            "blender",
            "--background",
            "--python", script_path,
            "--",
            "--params", params_path,
            "--output", output_stl_path
        ]
        
        try:
            # Using asyncio to not block the FastAPI loop
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                print(f"Blender Error: {stderr.decode()}")
                raise Exception(f"Blender execution failed: {stderr.decode()}")
                
        finally:
            if os.path.exists(params_path):
                os.remove(params_path)
                
        return output_stl_path

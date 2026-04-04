from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

from models.vibe_vector import VibeParamVector
from services.vibe_interpreter import VibeInterpreter

router = APIRouter()
vibe_interpreter = VibeInterpreter()

class GenerateRequest(BaseModel):
    prompt: str
    slider_overrides: Optional[Dict[str, float]] = None

class GenerateResponse(BaseModel):
    vibe_vector: VibeParamVector
    # Will add STL path, G-code path, and print report later

@router.post("/generate", response_model=GenerateResponse)
async def generate_model(request: GenerateRequest):
    try:
        # Step 1: Interpret the vibe
        vibe_vector = await vibe_interpreter.interpret_prompt(
            prompt=request.prompt,
            overrides=request.slider_overrides
        )
        
        # TODO: Step 2: Blender Bridge
        # TODO: Step 3: Print Analyzer
        # TODO: Step 4: Slicer Bridge
        
        return GenerateResponse(vibe_vector=vibe_vector)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

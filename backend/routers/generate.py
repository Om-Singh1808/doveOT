from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

from models.vibe_vector import VibeParamVector
from engine.cad_core import NativeCadEngine
from services.print_analyzer import PrintAnalyzer, PrintabilityReport
from services.settings_recommender import SettingsRecommender
from services.slicer_bridge import SlicerBridge
from services.vibe_interpreter import VibeInterpreter

router = APIRouter()
vibe_interpreter = VibeInterpreter()
cad_engine = NativeCadEngine()
print_analyzer = PrintAnalyzer()
settings_recommender = SettingsRecommender()
slicer = SlicerBridge()

class GenerateRequest(BaseModel):
    prompt: str
    slider_overrides: Optional[Dict[str, float]] = None

class GenerateResponse(BaseModel):
    vibe_vector: VibeParamVector
    engine_backend: str
    stl_path: str
    gcode_path: str
    print_settings: Dict[str, object]
    print_report: PrintabilityReport

@router.post("/generate", response_model=GenerateResponse)
async def generate_model(request: GenerateRequest):
    try:
        # Step 1: Interpret semantic intent into a normalized parameter vector.
        vibe_vector = await vibe_interpreter.interpret_prompt(
            prompt=request.prompt,
            overrides=request.slider_overrides
        )

        vibe_params = vibe_vector.model_dump()

        # Step 2: Build geometry with embedded engine.
        stl_path = cad_engine.generate_stl(vibe_params)

        # Step 3: Analyze printability and derive print profile.
        print_report = print_analyzer.analyze_stl(stl_path)
        print_settings = settings_recommender.recommend(vibe_vector, print_report)

        # Step 4: Slice STL to G-code.
        gcode_path = await slicer.slice_stl(stl_path, print_settings)

        return GenerateResponse(
            vibe_vector=vibe_vector,
            engine_backend=cad_engine.get_backend_name(),
            stl_path=stl_path,
            gcode_path=gcode_path,
            print_settings=print_settings,
            print_report=print_report,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

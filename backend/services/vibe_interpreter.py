import os
from openai import AsyncOpenAI
import json
from models.vibe_vector import VibeParamVector
from typing import Dict, Optional

class VibeInterpreter:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if self.api_key:
            self.client = AsyncOpenAI(api_key=self.api_key)
        else:
            self.client = None

    async def interpret_prompt(self, prompt: str, overrides: Optional[Dict[str, float]] = None) -> VibeParamVector:
        if not self.client:
            # Fallback to a default vector if no API key is provided
            print("WARNING: No OPENAI_API_KEY set. Returning default vibe vector.")
            vibe = VibeParamVector(
                archetype="stand",
                softness=0.5,
                complexity=0.5,
                weight=0.5,
                symmetry=0.8,
                fluidity=0.2,
                density=0.5,
                height_ratio=0.5,
                taper=0.3,
                description=prompt
            )
            if overrides:
                vibe.apply_overrides(overrides)
            return vibe

        system_message = """You are a design parameter interpreter. Given a natural language description 
of a desired 3D-printed object, output a JSON object with these fields representing the vibe.

- archetype: one of ["stand", "vessel", "box", "sculpture", "bracket", "lamp"]
- softness: float [0,1] — 0=sharp/angular, 1=soft/rounded
- complexity: float [0,1] — 0=minimal, 1=ornate
- weight: float [0,1] — 0=delicate, 1=heavy/solid
- symmetry: float [0,1] — 0=asymmetric, 1=perfectly symmetric
- fluidity: float [0,1] — 0=static/geometric, 1=flowing/dynamic
- density: float [0,1] — 0=open/airy, 1=dense/compact
- height_ratio: float [0,1] — 0=squat/wide, 1=tall/slender
- taper: float [0,1] — 0=uniform, 1=narrowing toward top
- description: brief text describing the intended form

Respond ONLY with valid JSON."""

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" }
            )
            content = response.choices[0].message.content
            vibe_data = json.loads(content)
            
            vibe = VibeParamVector(**vibe_data)
            
            if overrides:
                vibe.apply_overrides(overrides)
                
            return vibe
            
        except Exception as e:
            print(f"Error interpreting vibe: {e}")
            raise e

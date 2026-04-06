import os
import json
import re
import httpx
from models.vibe_vector import VibeParamVector
from typing import Dict, Optional

class VibeInterpreter:
    def __init__(self):
        self.ollama_base_url = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
        self.ollama_model = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")
        self.timeout_sec = float(os.environ.get("OLLAMA_TIMEOUT_SEC", "60"))

    async def interpret_prompt(self, prompt: str, overrides: Optional[Dict[str, float]] = None) -> VibeParamVector:
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
            vibe_data = await self._ask_ollama(system_message, prompt)
            
            vibe = VibeParamVector(**vibe_data)
            
            if overrides:
                vibe.apply_overrides(overrides)
                
            return vibe
            
        except Exception as e:
            print(f"Ollama interpretation error: {e}. Falling back to defaults.")
            vibe = self._default_vector(prompt)
            if overrides:
                vibe.apply_overrides(overrides)
            return vibe

    async def _ask_ollama(self, system_message: str, prompt: str) -> Dict:
        url = f"{self.ollama_base_url.rstrip('/')}/api/chat"
        payload = {
            "model": self.ollama_model,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.2,
            },
        }

        async with httpx.AsyncClient(timeout=self.timeout_sec) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()

        content = data.get("message", {}).get("content", "")
        if not content:
            raise ValueError("Ollama returned an empty response")

        return self._safe_json_parse(content)

    def _safe_json_parse(self, content: str) -> Dict:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if not match:
                raise
            return json.loads(match.group(0))

    def _default_vector(self, prompt: str) -> VibeParamVector:
        return VibeParamVector(
            archetype="stand",
            softness=0.5,
            complexity=0.5,
            weight=0.5,
            symmetry=0.8,
            fluidity=0.2,
            density=0.5,
            height_ratio=0.5,
            taper=0.3,
            description=prompt,
        )

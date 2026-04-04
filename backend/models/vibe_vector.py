from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Dict

class ObjectArchetype(str, Enum):
    STAND = "stand"
    VESSEL = "vessel"
    BOX = "box"
    SCULPTURE = "sculpture"
    BRACKET = "bracket"
    LAMP = "lamp"

class VibeParamVector(BaseModel):
    """
    Core mathematical model for mapping vibes to geometry.
    All dimensions are normalized [0.0, 1.0].
    """
    archetype: ObjectArchetype = Field(description="The structural base type of the object.")
    
    softness: float = Field(ge=0.0, le=1.0, description="0=sharp/angular, 1=soft/rounded")
    complexity: float = Field(ge=0.0, le=1.0, description="0=minimal, 1=ornate/intricate")
    weight: float = Field(ge=0.0, le=1.0, description="0=delicate/light, 1=heavy/solid/thick")
    symmetry: float = Field(ge=0.0, le=1.0, description="0=asymmetric/organic, 1=perfectly symmetric")
    fluidity: float = Field(ge=0.0, le=1.0, description="0=static/geometric, 1=flowing/dynamic")
    density: float = Field(ge=0.0, le=1.0, description="0=open/airy, 1=dense/compact")
    height_ratio: float = Field(ge=0.0, le=1.0, description="0=squat/wide, 1=tall/slender")
    taper: float = Field(ge=0.0, le=1.0, description="0=uniform cross-section, 1=narrowing toward top")
    
    description: str = Field(description="Brief text describing the interpreted form")
    
    # Allow overriding specific values (used for real-time frontend sliders)
    def apply_overrides(self, overrides: Dict[str, float]):
        for key, value in overrides.items():
            if hasattr(self, key) and key != "archetype" and key != "description":
                setattr(self, key, max(0.0, min(1.0, value)))

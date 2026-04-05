# Pivot to Independent AI-CAD Software

This document outlines the architectural shift to a completely standalone professional AI-driven 3D CAD and printing software. 

Based on the requirement to be a fully independent product, we will **remove the requirement for users to have Blender installed**. Because Blender is open-source, we will embed its core directly into our backend using the `bpy` Python module. This allows our software to silently possess all of Blender's modeling power natively inside our own app.

## User Review Required

> [!IMPORTANT]
> **Embedding the Blender Engine (`bpy`)**
> We will run `pip install bpy` in our backend. This effectively imports the entire Blender C++ math/mesh engine directly into our Python app. We no longer need to "bridge" or launch an external Blender application. The AI will generate script logic, and our backend will execute it natively in-memory to generate the 3D model. This fulfills your goal of creating an independent software product!

> [!CAUTION]
> **Computational Load**
> Embedding the 3D engine natively means the local machine's CPU/RAM will handle the mesh generation algorithms directly inside the backend process. 

## Proposed Changes

### Core Architecture & Engine Layer

#### [MODIFY] `backend/requirements.txt`
Add `bpy` to our Python dependencies. This replaces the need for an external Blender executable.

#### [NEW] `backend/engine/cad_core.py`
Establish the native 3D engine. This file will `import bpy` natively and expose functions for creating geometries, applying modifiers, and exporting STLs directly from RAM to the filesystem, eliminating the subprocess bridging completely.

#### [DELETE] `backend/services/blender_bridge.py`
Subprocess spawning is removed. We no longer need a "bridge" because the 3D engine is built directly into our software.

---

### AI Generation Layer

#### [MODIFY] `backend/services/ai_cad_agent.py`
The AI service behaves as a Professional CAD prompt interpreter. 
- The user uses conversational chat to describe what they want to construct (ex: "Build a junction box 80mm long with 5mm walls").
- The AI dynamically utilizes the internal `bpy` engine natively, executing Python instructions to construct the object parametrically.
- The system incorporates self-healing: if the `bpy` execution results in an invalid model, it automatically passes the error back to the AI for instant correction.

---

### Frontend UI Redesign

#### [MODIFY] `frontend/src/App.tsx`
- **Left Panel:** Convert to a "CAD Assistant Chat" for conversational prompts to allow iterations (e.g., "Make it slightly wider").
- **Center Panel:** Refine the Three.js Viewer to act like a true CAD viewport (adding grid measurements, measurement overlays in mm).
- **Right Panel:** Printability Analysis (Overhangs, Support toggles) and Export to STL / Direct G-Code slicing.

#### [DELETE] `frontend/src/components/VibeSliders.tsx`
#### [DELETE] `frontend/src/components/VibeSummary.tsx`
Remove all subjective/vibe components securely.

## Open Questions

> [!WARNING]  
> **1. PrusaSlicer Embedding:** Currently we rely on PrusaSlicer being installed externally to slice the created STL into G-code. If we want this to be **100% independent**, do you want me to also package/embed a command-line slicer engine (like CuraEngine or Slic3r binaries) natively inside the app's folders so the user literally installs nothing else?
> 
> **2. Initial CAD Capabilities:** Since the AI is writing code from scratch, what are the primary "types" of objects you expect professionals to use this for? (e.g., Mechanical gears, architectural mockups, enclosures, etc.)

## Verification Plan
1. Install `bpy` module locally into the python virtual environment.
2. Verify native Python can construct a complex 3D shape and export `.stl` without `blender.exe` present on the system.
3. Validate that the AI successfully interprets practical dimensions into the internal engine securely.

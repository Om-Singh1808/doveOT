# DoveOT — AI-Wrapped 3D Printing Software

Design and 3D print real-world objects using AI intent interpretation and an embedded 3D geometry engine.

---

## Requirements

- **Python** 3.10+ with pip
- **Node.js** 18+ with npm
- **No standalone Blender install required** (backend embeds Blender engine through `bpy`)
- **PrusaSlicer** (optional for G-code, mock used if missing)
- **OpenAI API Key**

---

## Quick Start

### 1. Backend

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp ../.env.example .env   # Add your OPENAI_API_KEY
python main.py
```

Backend runs at: `http://127.0.0.1:8000`

### 2. Frontend (Dev Mode)

```bash
cd frontend
npm install
npm run dev
```

Open browser at: `http://localhost:5173`

### 3. Full Electron App (built)

```bash
cd frontend
npm run start
```

---

## Usage

1. Type a prompt for the object you want (e.g., *"minimal premium soft phone stand"*)
2. Click **✦ Generate Model**
3. Backend interprets intent into geometry parameters
4. Embedded CAD engine generates STL internally (`bpy` backend, with local fallback)
5. Printability analyzer scores overhang risk and generates print settings
6. Slicer creates G-code (or mock output when slicer CLI is unavailable)

---

## Project Structure

```
DoveOT/
├── backend/        FastAPI backend (Python)
├── frontend/       Electron + React + Three.js
├── blender/        Headless Blender automation scripts
├── slicer/         PrusaSlicer profiles
└── output/         Generated STL and G-code files
```

---

## Key Technical Notes

- **Vibe Vector**: An 8-dimensional normalized [0,1] vector mapping aesthetic descriptions to geometry parameters
- **Embedded CAD Engine**: Native generation path in backend via `backend/engine/cad_core.py`
- **Archetypes**: MVP currently ships with native `stand` generation; others can be added incrementally
- **Transfer Functions**: Mathematical mappings from interpreted dimensions to CAD parameters
- **Overhang Detection**: Face-normal analysis with trimesh (45° threshold)
- **Slicer**: PrusaSlicer CLI with graceful fallback to mock G-code

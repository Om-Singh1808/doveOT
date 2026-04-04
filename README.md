# VibePrint — Vibe-Based 3D Printing System

Design and 3D print real-world objects using emotions, aesthetics, and "vibes" as inputs.

---

## Requirements

- **Python** 3.10+ with pip
- **Node.js** 18+ with npm
- **Blender** 4.0+ (must be in PATH or configured in `.env`)
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

1. Type a vibe prompt (e.g., *"minimal premium soft phone stand"*)
2. Adjust vibe sliders to fine-tune dimensions
3. Select object archetype (or let AI pick)
4. Click **✦ Generate Model**
5. Watch the 3D preview update live as you adjust sliders
6. Export STL or G-code when ready

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
- **Archetypes**: 6 base geometries (stand, vessel, box, sculpture, bracket, lamp)
- **Transfer Functions**: Mathematical mappings from vibe dimensions to Blender parameters
- **Overhang Detection**: Face-normal analysis with trimesh (45° threshold)
- **Slicer**: PrusaSlicer CLI with graceful fallback to mock G-code

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import generate
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="VibePrint API", description="Backend for Vibe-Based 3D Printing System")

# Configure CORS for Electron frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate.router, prefix="/api")

@app.get("/")
def read_root():
    return {"status": "VibePrint API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

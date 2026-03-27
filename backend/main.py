import sys
import os
import json
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- 1. Fix Path BEFORE Imports ---
# This ensures that 'learning' is recognized as a package
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# --- 2. Now Import Project Modules ---
from learning.database import init_db
from learning.routes import router as learning_router
from learning.generation import populate_unit # This replaces the old bulk generator
# from placement.generator import exam_cache # Uncomment when placement folder is ready

app = FastAPI(title="BMSCE Stock Market Simulator")

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Startup ---
@app.on_event("startup")
def startup_event():
    # print("🚀 Pre-loading Placement Exam Cache...")
    # exam_cache.refresh_cache()

    print("🧱 Initializing Learning DB...")
    init_db()

    print("🧬 Checking & Filling Missing Questions via Groq...")

    try:
        # Adjusted path to find themes.json inside the learning folder
        themes_path = os.path.join(BASE_DIR, "learning", "themes.json")

        if not os.path.exists(themes_path):
            print(f"⚠️ themes.json not found at {themes_path}")
            return

        with open(themes_path, "r") as f:
            curriculum = json.load(f)

        for section in curriculum["sections"]:
            league = section["league"]
            for unit in section["units"]:
                print(f"📦 Processing: {unit['unit_id']}")
                # Using the new Groq-powered 5-5-10 logic
                populate_unit(
                    unit_id=unit["unit_id"],
                    topics=unit["topics"],
                    league=league
                )

        print("✨ Generation Pass Complete.")
    except Exception as e:
        print(f"❌ Auto-Generation Failed: {e}")

# --- Routes ---
@app.get("/")
def health_check():
    return {"status": "online", "project": "BMSCE Stock Simulator"}

app.include_router(learning_router, prefix="/learning", tags=["Learning"])

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
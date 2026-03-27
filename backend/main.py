import uvicorn
import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Existing Placement Imports
from placement.generator import exam_cache

# New Learning Directory Imports
from learning.routes import router as learning_router
from learning.database import init_db, is_db_empty
from learning.generator import mass_generate_questions

app = FastAPI(title="BMSCE Stock Market Simulator")

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Startup Events ---
@app.on_event("startup")
def startup_event():
    # 1. Your existing placement cache preload
    print("🚀 Pre-loading Placement Exam Cache...")
    exam_cache.refresh_cache()
    
    # 2. Initialize the Learning SQLite database tables
    init_db()
    
    # 3. AUTO-SEEDING LOGIC
    # Checks if the database is empty. If yes, it populates all 24 units once.
    if is_db_empty():
        print("🧬 Question Bank is empty. Starting Auto-Generation for 24 Units...")
        try:
            # Adjust path if themes.json is located elsewhere
            themes_path = os.path.join("learning", "themes.json")
            with open(themes_path, "r") as f:
                curriculum = json.load(f)
            
            for section in curriculum["sections"]:
                league = section["league"]
                for unit in section["units"]:
                    print(f"📦 Populating Unit: {unit['unit_id']} ({unit['title']})...")
                    # Calls Groq to generate the hardware/AI focused questions
                    mass_generate_questions(unit["unit_id"], unit["topics"], league)
            
            print("✨ Auto-Generation Complete. 24 Units seeded.")
        except Exception as e:
            print(f"❌ Auto-Generation Failed: {e}")
    else:
        print("📊 Question Bank already populated. Skipping AI generation.")

    print("✅ System Ready: Placement Cache & Learning DB online.")

# --- Routes: Placement (Existing) ---
@app.get("/quiz/all")
def get_all():
    return {"questions": exam_cache.cached_questions}

@app.get("/quiz/refresh")
def refresh():
    exam_cache.refresh_cache()
    return {"status": "success", "count": len(exam_cache.cached_questions)}

@app.get("/")
def health_check():
    return {
        "status": "online", 
        "project": "BMSCE Stock Simulator",
        "units_available": 24
    }

# --- Routes: Learning Directory (New) ---
# This includes endpoints: 
# GET  /learning/unit/{unit_id}/{user_id}
# POST /learning/submit
app.include_router(learning_router)

# --- Entry Point ---
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
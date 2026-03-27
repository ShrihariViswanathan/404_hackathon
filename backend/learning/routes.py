from fastapi import APIRouter, HTTPException
from .engine import engine
from .generation import populate_unit

router = APIRouter()

@router.get("/quiz/{user_id}/{unit_id}")
async def get_quiz(user_id: str, unit_id: str, league: str = "Bronze"):
    # 1. Check if we have enough questions in DB
    questions = engine.get_unit_quiz(user_id, unit_id)
    
    # 2. If DB is low (e.g., < 15), trigger Groq to fill it
    if len(questions) < 15:
        # Note: In production, you'd pass the actual topics list from your config
        topics = ["Market Foundations"] 
        populate_unit(unit_id, topics, league)
        # Re-fetch after population
        questions = engine.get_unit_quiz(user_id, unit_id)

    if not questions:
        raise HTTPException(status_code=404, detail="Could not generate questions")
        
    return {"unit_id": unit_id, "questions": questions}
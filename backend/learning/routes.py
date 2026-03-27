from fastapi import APIRouter, Body
from .engine import engine
import json

router = APIRouter(prefix="/learning", tags=["Duolingo Learning"])

@router.get("/unit/{unit_id}/{user_id}")
def get_unit_lesson(unit_id: str, user_id: str):
    """Fetch 10 unique questions for this specific user."""
    raw_questions = engine.get_next_lesson(user_id, unit_id)
    
    # Process JSON options
    for q in raw_questions:
        q['options'] = json.loads(q['options'])
        
    return {"unit_id": unit_id, "questions": raw_questions}

@router.post("/submit")
def submit_answer(user_id: str = Body(...), question_id: int = Body(...), is_correct: bool = Body(...)):
    """Update user progress so they don't see this question again immediately."""
    engine.record_attempt(user_id, question_id, is_correct)
    return {"status": "success"}

@router.get("/debug/all-questions")
def get_all_questions_debug():
    """
    Returns the entire database content for testing.
    DO NOT use this in the production frontend.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fetch everything
    cursor.execute("SELECT * FROM questions ORDER BY unit_id ASC")
    rows = cursor.fetchall()
    conn.close()

    # Organize by unit for easier reading
    all_content = {}
    for r in rows:
        unit = r['unit_id']
        if unit not in all_content:
            all_content[unit] = []
        
        all_content[unit].append({
            "id": r['id'],
            "topic": r['topic'],
            "type": r['q_type'],
            "question": r['question_text'],
            "options": json.loads(r['options']),
            "answer_index": r['correct_index'],
            "context": r['market_context']
        })
        
    return {
        "total_count": len(rows),
        "units": all_content
    }
from fastapi import APIRouter, HTTPException, Body
from .engine import engine

router = APIRouter(prefix="/api")


@router.get("/quiz/{user_id}/{unit_id}")
async def get_unit_quiz(user_id: str, unit_id: str):

    questions = engine.get_unit_quiz(user_id, unit_id, limit=15)

    if not questions:
        raise HTTPException(
            status_code=404,
            detail=f"No questions found for unit {unit_id}"
        )

    return {
        "unit_id": unit_id,
        "questions": questions
    }


@router.post("/quiz/record")
async def record_question_result(
    user_id: str = Body(...),
    question_id: int = Body(...),
    is_correct: bool = Body(...)
):
    engine.record_attempt(user_id, question_id, is_correct)
    return {"status": "recorded"}


@router.get("/curriculum/directory")
async def get_full_directory():
    return engine.get_curriculum()
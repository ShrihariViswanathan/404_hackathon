from fastapi import APIRouter, HTTPException, Body, Request
from .engine import engine

router = APIRouter(prefix="/api")


def get_user_id(request: Request):
    user_id = request.headers.get("x-user-id")
    print("🔥 USER HEADER:", user_id)  # debug
    return user_id


@router.get("/quiz/{unit_id}")
async def get_unit_quiz(unit_id: str, request: Request):

    user_id = get_user_id(request)

    # 🔥 TEMP fallback (so you don't get empty)
    if not user_id:
        user_id = "user_3BY6Wb35eFWrcrohYhOKFCHTjlI"

    questions = engine.get_unit_quiz(user_id, unit_id, limit=15)

    print("🔥 QUESTIONS COUNT:", len(questions))  # debug

    return {
        "unit_id": unit_id,
        "questions": questions
    }


@router.post("/quiz/record")
async def record_question_result(
    request: Request,
    question_id: int = Body(...),
    is_correct: bool = Body(...)
):
    user_id = get_user_id(request)

    if not user_id:
        raise HTTPException(400, "Missing user_id header")

    print("🔥 RECORD HIT:", user_id, question_id, is_correct)

    engine.record_attempt(user_id, question_id, is_correct)

    return {"status": "recorded"}
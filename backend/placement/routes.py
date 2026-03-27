from fastapi import APIRouter, HTTPException, Query
from .generator import exam_cache

router = APIRouter(prefix="/placement", tags=["Placement"])


# 🔥 Get all cached questions
@router.get("/quiz")
def get_all_questions():
    if not exam_cache.cached_questions:
        raise HTTPException(
            status_code=500,
            detail="Question cache is empty. Try /placement/refresh"
        )

    return {
        "count": len(exam_cache.cached_questions),
        "questions": exam_cache.cached_questions
    }


# 🔥 Get limited questions (for quiz session)
@router.get("/quiz/random")
def get_random_questions(limit: int = Query(10, ge=1, le=30)):
    if not exam_cache.cached_questions:
        raise HTTPException(
            status_code=500,
            detail="Cache not initialized"
        )

    return {
        "questions": exam_cache.cached_questions[:limit]
    }


# 🔥 Filter by difficulty
@router.get("/quiz/difficulty/{level}")
def get_by_difficulty(level: str):
    level = level.lower()

    filtered = [
        q for q in exam_cache.cached_questions
        if q.get("difficulty") == level
    ]

    if not filtered:
        raise HTTPException(
            status_code=404,
            detail=f"No questions found for difficulty '{level}'"
        )

    return {
        "count": len(filtered),
        "questions": filtered
    }


# 🔥 Filter by topic
@router.get("/quiz/topic/{topic}")
def get_by_topic(topic: str):
    filtered = [
        q for q in exam_cache.cached_questions
        if topic.lower() in q.get("topic", "").lower()
    ]

    if not filtered:
        raise HTTPException(
            status_code=404,
            detail=f"No questions found for topic '{topic}'"
        )

    return {
        "count": len(filtered),
        "questions": filtered
    }


# 🔥 Refresh cache manually
@router.get("/refresh")
def refresh_cache():
    exam_cache.refresh_cache()

    return {
        "status": "refreshed",
        "count": len(exam_cache.cached_questions)
    }

@router.get("/quiz/all")
def get_all_questions():
    if not exam_cache.cached_questions:
        raise HTTPException(
            status_code=500,
            detail="Cache is empty. Run /placement/refresh"
        )

    return {
        "count": len(exam_cache.cached_questions),
        "questions": exam_cache.cached_questions
    }
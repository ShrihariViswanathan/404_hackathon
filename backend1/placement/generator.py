import os
import json
import random
import time
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

from fastapi import APIRouter, HTTPException, Query

# --- Path Resolution ---
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent.parent
load_dotenv(dotenv_path=ROOT_DIR / ".env", override=True)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# =========================
# CONFIG
# =========================
TOTAL_QUESTIONS = 9
PER_LEVEL = TOTAL_QUESTIONS // 3  # 3 each

# =========================
# QUESTION CACHE
# =========================
class QuestionCache:
    def __init__(self):
        self.cached_questions = []

    def refresh_cache(self):
        print("🚀 Generating 9 questions (3 Easy, 3 Medium, 3 Hard)...")

        new_batch = []
        difficulties = ["easy", "medium", "hard"]

        for diff in difficulties:
            topics = self._get_topics(diff, PER_LEVEL)

            for topic in topics:
                q = self._generate_with_retry(topic, diff)
                if q:
                    new_batch.append(q)

                time.sleep(0.4)  # avoid rate limit

        random.shuffle(new_batch)
        self.cached_questions = new_batch

        print(f"✅ Cache ready: {len(self.cached_questions)} questions")

    def _get_topics(self, diff, count):
        topic_path = CURRENT_DIR / "topics.json"

        try:
            with open(topic_path, "r") as f:
                data = json.load(f)

            all_topics = data.get("stock_market_curriculum", {}).get(f"{diff}_topics", [])

            if not all_topics:
                return ["General Trading"] * count

            return (
                random.sample(all_topics, count)
                if len(all_topics) >= count
                else [random.choice(all_topics) for _ in range(count)]
            )

        except:
            return ["General Trading"] * count

    def _generate_with_retry(self, topic, diff, retries=2):
        model = "llama-3.1-8b-instant" if diff != "hard" else "llama-3.3-70b-versatile"

        system_msg = (
            "You are a professional Financial Examiner. Output ONLY valid JSON. "
            '{"question": "...", "options": ["..."], "answer": 0, "explanation": "..."}'
        )

        prompt = f"Generate ONE {diff} level MCQ about Indian Stock Market topic: {topic}"

        for _ in range(retries):
            try:
                completion = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.5
                )

                data = json.loads(completion.choices[0].message.content)
                data.update({"topic": topic, "difficulty": diff})

                return data

            except Exception:
                print(f"⚠️ Retry for {topic}")
                continue

        return None


# Global cache
exam_cache = QuestionCache()

# =========================
# ROUTER
# =========================
router = APIRouter(prefix="/placement", tags=["Placement"])


# 🔥 Get ALL questions (9)
@router.get("/quiz")
def get_all_questions():
    if not exam_cache.cached_questions:
        raise HTTPException(500, "Cache empty. Run /placement/refresh")

    return {
        "count": len(exam_cache.cached_questions),
        "questions": exam_cache.cached_questions
    }


# 🔥 Get RANDOM questions (default 9)
@router.get("/quiz/random")
def get_random_questions(limit: int = Query(9, ge=1, le=9)):
    if not exam_cache.cached_questions:
        raise HTTPException(500, "Cache not initialized")

    questions = exam_cache.cached_questions

    selected = (
        questions if len(questions) <= limit
        else random.sample(questions, limit)
    )

    return {
        "count": len(selected),
        "questions": selected
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
        raise HTTPException(404, f"No questions for '{level}'")

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
        raise HTTPException(404, f"No questions for '{topic}'")

    return {
        "count": len(filtered),
        "questions": filtered
    }


# 🔥 Refresh cache (NEW questions every time)
@router.get("/refresh")
def refresh_cache():
    exam_cache.refresh_cache()

    return {
        "status": "refreshed",
        "count": len(exam_cache.cached_questions)
    }
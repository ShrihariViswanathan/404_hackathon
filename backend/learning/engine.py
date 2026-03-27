import json
import os
from .database import get_db_connection

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEMES_PATH = os.path.join(BASE_DIR, "learning", "themes.json")


class LearningEngine:

    # 🔥 normalize unit_id (fix your main bug)
    def normalize_unit(self, unit_id: str):
        if unit_id.isdigit():
            return f"B_U{unit_id}"
        return unit_id

    # 🔥 MAIN FUNCTION (what your route expects)
    def get_unit_quiz(self, user_id: str, unit_id: str, limit=15):

        unit_id = self.normalize_unit(unit_id)

        conn = get_db_connection()

        rows = conn.execute("""
        SELECT q.*
        FROM questions q
        LEFT JOIN user_progress p 
        ON q.id = p.question_id AND p.user_id = ?
        WHERE q.unit_id = ?
        ORDER BY 
            CASE 
                WHEN p.status IS NULL THEN 1
                WHEN p.status = 'failed' THEN 2
                ELSE 3
            END,
            RANDOM()
        LIMIT ?
        """, (user_id, unit_id, limit)).fetchall()

        conn.close()

        result = []

        for r in rows:
            r = dict(r)

            if isinstance(r["options"], str):
                r["options"] = json.loads(r["options"])

            result.append(r)

        return result

    # 🔥 RECORD ATTEMPT
    def record_attempt(self, user_id, question_id, is_correct):
        status = "mastered" if is_correct else "failed"

        conn = get_db_connection()

        conn.execute("""
        INSERT INTO user_progress (user_id, question_id, status, attempts, last_attempted)
        VALUES (?, ?, ?, 1, CURRENT_TIMESTAMP)
        ON CONFLICT(user_id, question_id) DO UPDATE SET
            status = excluded.status,
            attempts = attempts + 1,
            last_attempted = CURRENT_TIMESTAMP
        """, (user_id, question_id, status))

        conn.commit()
        conn.close()

    # 🔥 RETURN FULL CURRICULUM
    def get_curriculum(self):
        with open(THEMES_PATH, "r") as f:
            return json.load(f)


engine = LearningEngine()
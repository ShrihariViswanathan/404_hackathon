import json
import os
from .database import get_db_connection

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEMES_PATH = os.path.join(BASE_DIR, "learning", "themes.json")


class LearningEngine:

    def normalize_unit(self, unit_id: str):
        if unit_id.isdigit():
            return f"B_U{unit_id}"
        return unit_id

    def get_unit_quiz(self, user_id: str, unit_id: str, limit=15):
        unit_id = self.normalize_unit(unit_id)
        conn = get_db_connection()

        rows = conn.execute("""
        SELECT q.*
        FROM questions q
        WHERE q.unit_id = ?
        ORDER BY RANDOM()
        LIMIT ?
        """, (unit_id, limit)).fetchall()

        conn.close()

        result = []
        for r in rows:
            r = dict(r)
            if isinstance(r["options"], str):
                r["options"] = json.loads(r["options"])
            result.append(r)

        return result

    # 🔥 UPDATED LOGIC
    def record_attempt(self, user_id, question_id, is_correct):

        conn = get_db_connection()

        row = conn.execute("""
        SELECT attempts, correct_count
        FROM user_progress
        WHERE user_id=? AND question_id=?
        """, (user_id, question_id)).fetchone()

        if row:
            attempts = row["attempts"] + 1
            correct_count = row["correct_count"] + (1 if is_correct else 0)
        else:
            attempts = 1
            correct_count = 1 if is_correct else 0

        # 🔥 mastery rule
        status = "mastered" if correct_count >= 3 else "learning"

        conn.execute("""
        INSERT INTO user_progress (user_id, question_id, status, attempts, correct_count, last_attempted)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(user_id, question_id) DO UPDATE SET
            status = excluded.status,
            attempts = attempts + 1,
            correct_count = correct_count + ?,
            last_attempted = CURRENT_TIMESTAMP
        """, (user_id, question_id, status, attempts, correct_count, 1 if is_correct else 0))

        conn.commit()
        conn.close()

    def get_curriculum(self):
        with open(THEMES_PATH, "r") as f:
            return json.load(f)


engine = LearningEngine()
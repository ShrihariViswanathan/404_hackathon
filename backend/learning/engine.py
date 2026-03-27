import json
from learning.database import get_db_connection

class LearningEngine:
    def get_unit_quiz(self, user_id: str, unit_id: str, limit=15):
        """Fetches 15 questions for the user's current unit."""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Logic: 1. New questions, 2. Failed questions, 3. Random
        query = """
        SELECT q.* FROM questions q
        LEFT JOIN user_progress p ON q.id = p.question_id AND p.user_id = ?
        WHERE q.unit_id = ?
        ORDER BY 
            CASE 
                WHEN p.status IS NULL THEN 1
                WHEN p.status = 'failed' THEN 2
                ELSE 3
            END,
            RANDOM()
        LIMIT ?
        """
        cursor.execute(query, (user_id, unit_id, limit))
        rows = cursor.fetchall()
        conn.close()

        questions = []
        for r in rows:
            item = dict(r)
            item['options'] = json.loads(item['options'])
            questions.append(item)
        return questions

    def record_attempt(self, user_id: str, question_id: int, is_correct: bool):
        status = 'mastered' if is_correct else 'failed'
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

engine = LearningEngine()
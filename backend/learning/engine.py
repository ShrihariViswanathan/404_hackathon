from .database import get_db_connection
import json

class LearningEngine:
    def get_next_lesson(self, user_id: str, unit_id: str, limit=10):
        conn = get_db_connection()
        cursor = conn.cursor()

        # PRIORITY: Unseen questions first, then Failed questions
        query = '''
            SELECT q.* FROM questions q
            LEFT JOIN user_progress up ON q.id = up.question_id AND up.user_id = ?
            WHERE q.unit_id = ? 
            AND (up.status IS NULL OR up.status = 'failed')
            ORDER BY RANDOM()
            LIMIT ?
        '''
        cursor.execute(query, (user_id, unit_id, limit))
        rows = cursor.fetchall()
        
        # Fallback: If pool is exhausted, show Mastered questions for review
        if len(rows) < limit:
            cursor.execute('SELECT * FROM questions WHERE unit_id = ? ORDER BY RANDOM() LIMIT ?', (unit_id, limit))
            rows = cursor.fetchall()

        conn.close()
        return [dict(row) for row in rows]

    def record_attempt(self, user_id, question_id, is_correct):
        conn = get_db_connection()
        cursor = conn.cursor()
        status = 'mastered' if is_correct else 'failed'
        
        cursor.execute('''
            INSERT INTO user_progress (user_id, question_id, status, attempts)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(user_id, question_id) DO UPDATE SET
                status = excluded.status,
                attempts = attempts + 1,
                last_attempted = CURRENT_TIMESTAMP
        ''', (user_id, question_id, status))
        conn.commit()
        conn.close()

engine = LearningEngine()
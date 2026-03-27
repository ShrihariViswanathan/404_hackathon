import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "quiz_bank.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def is_db_empty():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM questions")
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Table 1: The Master Question Pool
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unit_id TEXT,
            topic TEXT,
            q_type TEXT,           -- 'acronym', 'synonym', 'scenario', 'hardware_analogy'
            question_text TEXT,
            options TEXT,          -- JSON string
            correct_index INTEGER,
            explanation TEXT,
            market_context TEXT
        )
    ''')
    # Table 2: User Progress Tracking (The Anti-Repeat Filter)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_progress (
            user_id TEXT,
            question_id INTEGER,
            status TEXT,           -- 'seen', 'mastered', 'failed'
            attempts INTEGER DEFAULT 1,
            last_attempted DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, question_id)
        )
    ''')
    conn.commit()
    conn.close()
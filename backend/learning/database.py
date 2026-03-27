import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "quiz.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        unit_id TEXT,
        topic TEXT,
        q_type TEXT,
        question_text TEXT,
        options TEXT,
        correct_index INTEGER,
        explanation TEXT,
        market_context TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS user_progress (
        user_id TEXT,
        question_id INTEGER,
        status TEXT,
        attempts INTEGER DEFAULT 0,
        last_attempted TIMESTAMP,
        PRIMARY KEY (user_id, question_id)
    )
    """)

    conn.commit()
    conn.close()

    print(f"✅ DB READY @ {DB_PATH}")
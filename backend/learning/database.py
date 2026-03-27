import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "quiz.db")

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
            attempts INTEGER,
            last_attempted TIMESTAMP,
            PRIMARY KEY (user_id, question_id)
        )
    """)
    conn.commit()
    conn.close()
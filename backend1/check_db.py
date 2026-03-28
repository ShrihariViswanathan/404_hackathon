from backend.learning.database import get_db_connection

conn = get_db_connection()
row = conn.execute("SELECT COUNT(*) FROM questions").fetchone()
print(f"Total questions found in DB: {row[0]}")

# Print the first question to see if data is readable
if row[0] > 0:
    q = conn.execute("SELECT unit_id, question_text FROM questions LIMIT 1").fetchone()
    print(f"Sample data from {q['unit_id']}: {q['question_text']}")
conn.close()
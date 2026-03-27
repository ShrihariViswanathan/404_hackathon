import json
import os
import time
from groq import Groq
from learning.database import get_db_connection

# --- PASTE YOUR NEW KEY HERE ---
GROQ_API_KEY = "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" 

client = Groq(api_key=GROQ_API_KEY)
MODEL = "llama-3.1-8b-instant" 

def turbo_generate(unit_id, topic, league):
    """Pulls 50 questions in one shot."""
    # Note: We ask for 50 but 8B models sometimes cap at 30-40 due to token limits.
    # We will run this to fill the DB as fast as the API allows.
    prompt = f"GENERATE 50 MCQs for {topic} ({league}). RETURN ONLY JSON with keys: type, question, options, answer, explanation. Format: {{'questions': [...]}}"
    
    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.1 # Max speed, minimum 'thinking'
        )
        return json.loads(completion.choices[0].message.content).get("questions", [])
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def populate_unit(unit_id, topics, league):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # We check if we have at least 40 questions (safe 'full' mark)
    count = cursor.execute("SELECT COUNT(*) FROM questions WHERE unit_id=?", (unit_id,)).fetchone()[0]
    if count >= 40:
        print(f"✅ {unit_id} Ready.")
        conn.close()
        return

    main_topic = topics[0] if topics else "Trading"
    print(f"🚀 RAPID-FIRE: {unit_id} ({league})")
    
    batch = turbo_generate(unit_id, main_topic, league)
    
    if batch:
        data = [
            (unit_id, main_topic, q.get('type', 'direct'), q.get('question'), 
             json.dumps(q.get('options')), q.get('answer', 0), q.get('explanation'))
            for q in batch
        ]
        cursor.executemany("INSERT INTO questions (unit_id, topic, q_type, question_text, options, correct_index, explanation) VALUES (?,?,?,?,?,?,?)", data)
        conn.commit()
        print(f"   ⚡ Added {len(data)} questions.")
    
    conn.close()
    # Tiny sleep to prevent 429 Rate Limits
    time.sleep(0.5)
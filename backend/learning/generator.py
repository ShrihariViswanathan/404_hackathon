import json
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from .database import get_db_connection

# --- Path Resolution ---
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent 
load_dotenv(dotenv_path=ROOT_DIR / ".env", override=True)

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def mass_generate_questions(unit_id, topics, league):
    """
    Generates a deep pool of questions (approx 48 per topic) by 
    looping through 4 distinct 'Style Personas'.
    """
    
    styles = [
        {"type": "direct", "desc": "raw Indian market facts, definitions, and acronyms."},
        {"type": "scenario", "desc": "real-world 'What-if' trading situations and decision making."},
        {"type": "hardware_analogy", "desc": "comparisons to CS hardware (CPU, RAM, GPU, Latency, Throughput)."},
        {"type": "logic_puzzle", "desc": "mathematical market relationships or logical deductions."}
    ]

    for topic in topics:
        for style in styles:
            print(f"🎭 Generating {style['type']} questions for: {topic}...")
            
            # This system message is key to preventing the "json_validate_failed" error
            system_msg = (
                "You are a strict JSON generator. Output ONLY a valid JSON object. "
                "Do not include any introductory text, markdown, or code blocks. "
                "CRITICAL: Do not use backslashes or special escape characters in strings. "
                "Ensure 'options' is a simple list of exactly 4 strings."
            )

            prompt = f"""
            Create 12 unique MCQ questions for the topic '{topic}' for a {league} level user.
            STYLE: Focus strictly on {style['desc']}
            
            Output strictly in this JSON format:
            {{
              "questions": [
                {{
                  "type": "{style['type']}",
                  "question": "...",
                  "options": ["...", "...", "...", "..."],
                  "answer": 0,
                  "explanation": "...",
                  "context": "{topic} - {style['type']}"
                }}
              ]
            }}
            
            STRICT RULES:
            1. No labels like 'A)' or '1.' in the options.
            2. Use Indian stock market context (NSE/BSE/SEBI).
            3. Answer must be an integer (0-3) representing the index of the correct option.
            """
            
            success = False
            retries = 2
            
            while not success and retries > 0:
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": system_msg},
                            {"role": "user", "content": prompt}
                        ],
                        response_format={"type": "json_object"},
                        temperature=0.3  # Keeps the AI focused on the format
                    )
                    
                    content = json.loads(response.choices[0].message.content)
                    batch = content.get("questions", [])
                    
                    if batch:
                        save_batch_to_db(unit_id, topic, batch)
                        print(f"✅ Successfully added {len(batch)} {style['type']} questions.")
                        success = True
                    
                    time.sleep(4) # Rate limit protection

                except Exception as e:
                    retries -= 1
                    print(f"⚠️ JSON Attempt failed for {topic} ({style['type']}). Retries left: {retries}. Error: {e}")
                    time.sleep(10) # Cool down before retry

def save_batch_to_db(unit_id, topic, batch):
    """Saves the AI-generated batch to the SQLite database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        for q in batch:
            # Ensure the options list is converted to a string for SQLite
            options_json = json.dumps(q.get('options', []))
            
            cursor.execute('''
                INSERT INTO questions (
                    unit_id, topic, q_type, question_text, 
                    options, correct_index, explanation, market_context
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                unit_id, 
                topic, 
                q.get('type', 'general'), 
                q.get('question', 'Missing Question?'), 
                options_json, 
                q.get('answer', 0), 
                q.get('explanation', ''), 
                q.get('context', 'General')
            ))
        
        conn.commit()
    except Exception as e:
        print(f"❌ Database Insert Error: {e}")
        conn.rollback()
    finally:
        conn.close()
import json
import time
import ollama
# ADD THIS LINE AT THE TOP:
from .database import get_db_connection 

def mass_generate_bulk(unit_id, topics, league="Intermediate"):
    styles = [
        {"type": "direct", "desc": "SEBI regs, T+1 settlement, NSE/BSE rules."},
        {"type": "scenario", "desc": "Intraday trading dilemmas and SL-M execution."},
        {"type": "analogy", "desc": "Market mechanics via CS hardware (HFT=Overclocking, RAM=Liquidity)."},
        {"type": "quant", "desc": "Quantitative math: Greeks, Lot sizes, and Arbitrage logic."}
    ]

    conn = get_db_connection()
    
    for style in styles:
        # Check current count for this style/unit
        cursor = conn.cursor()
        cursor.execute(
            'SELECT COUNT(*) FROM questions WHERE unit_id=? AND q_type=?', 
            (unit_id, style['type'])
        )
        count = cursor.fetchone()[0]

        if count >= 20:
            print(f"  ⏩ Style '{style['type']}' already has {count} questions. Skipping.")
            continue

        needed = 20 - count
        print(f"  🔥 Generating {needed} '{style['type']}' questions for {unit_id}...")
        
        prompt = f"""
        Act as a Senior Quant Dev. Generate {needed} UNIQUE MCQs for Unit: {unit_id}.
        Topics: {', '.join(topics)}. Style: {style['desc']} | Difficulty: {league}.
        Return ONLY JSON: {{ "questions": [ {{ "type": "{style['type']}", "question": "...", "options": ["A","B","C","D"], "answer": 0, "explanation": "...", "context": "topic" }} ] }}
        """

        try:
            response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}], format='json')
            content = json.loads(response['message']['content'])
            batch = content.get("questions", [])
            
            if batch:
                with conn:
                    for q in batch:
                        conn.execute('''INSERT INTO questions 
                            (unit_id, topic, q_type, question_text, options, correct_index, explanation, market_context)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                            (unit_id, q.get('context', 'General'), style['type'], q['question'], 
                             json.dumps(q['options']), q['answer'], q['explanation'], q.get('context')))
                print(f"  ✅ Added {len(batch)} questions.")
        except Exception as e:
            print(f"  ⚠️ Error generating {style['type']}: {e}")
            time.sleep(2)
            
    conn.close()
import os
import json
import random
import time
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# --- Path Resolution ---
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent.parent
load_dotenv(dotenv_path=ROOT_DIR / ".env", override=True)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class QuestionCache:
    def __init__(self):
        self.cached_questions = []
        # Path to the persistent backup file
        self.backup_path = CURRENT_DIR / "placement_backup.json"

    def refresh_cache(self):
        # 1. Check if backup exists to avoid re-generating on every server reload
        if self.backup_path.exists():
            try:
                with open(self.backup_path, "r") as f:
                    self.cached_questions = json.load(f)
                
                if len(self.cached_questions) >= 30:
                    print(f"📦 Placement Questions loaded from local backup: {len(self.cached_questions)} questions.")
                    return
            except Exception as e:
                print(f"⚠️ Backup file corrupted or unreadable: {e}. Re-generating...")

        # 2. If no backup, proceed with AI generation
        print("🚀 Pre-generating 30 questions (10 Easy, 10 Medium, 10 Hard) via AI...")
        new_batch = []
        difficulties = ["easy", "medium", "hard"]
        
        for diff in difficulties:
            topics = self._get_topics(diff, 10)
            for topic in topics:
                q = self._generate_with_retry(topic, diff)
                if q:
                    new_batch.append(q)
                time.sleep(0.5) # Prevent aggressive rate limiting
        
        random.shuffle(new_batch)
        self.cached_questions = new_batch
        
        # 3. SAVE TO BACKUP FILE
        try:
            with open(self.backup_path, "w") as f:
                json.dump(self.cached_questions, f, indent=4)
            print(f"💾 Placement backup saved to {self.backup_path}")
        except Exception as e:
            print(f"❌ Could not save placement backup: {e}")

        print(f"✅ Cache Loaded: {len(self.cached_questions)} questions ready.")

    def _get_topics(self, diff, count):
        topic_path = CURRENT_DIR / "topics.json"
        try:
            with open(topic_path, "r") as f:
                data = json.load(f)
            all_topics = data.get("stock_market_curriculum", {}).get(f"{diff}_topics", [])
            return random.sample(all_topics, count) if len(all_topics) >= count else [random.choice(all_topics) for _ in range(count)]
        except:
            return ["General Trading"] * count

    def _generate_with_retry(self, topic, diff, retries=2):
        model = "llama-3.1-8b-instant" if diff != "hard" else "llama-3.3-70b-versatile"
        
        system_msg = (
            "You are a professional Financial Examiner. Output ONLY valid JSON. "
            "Do not include labels like 'A)' or '1)' inside the options strings. "
            "Example format: "
            '{"question": "What is a bull market?", "options": ["Rising prices", "Falling prices", "Sideways", "No change"], "answer": 0, "explanation": "Prices are rising."}'
        )
        
        prompt = f"Generate ONE {diff} level MCQ about the Indian Stock Market topic: {topic}."
        
        for _ in range(retries):
            try:
                completion = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.5
                )
                content = completion.choices[0].message.content
                data = json.loads(content)
                data.update({"topic": topic, "difficulty": diff})
                return data
            except Exception as e:
                print(f"⚠️ Retrying {topic} due to JSON structure error...")
                continue
        return None

# Global Instance
exam_cache = QuestionCache()
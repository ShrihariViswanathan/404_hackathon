# learning/scripts/seed_data.py
import sys
import os
import json

# Add parent directory to path so we can import 'learning' modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from learning.database import init_db
from learning.generator import mass_generate_questions

def run_seeding():
    print("🚀 Initializing Database...")
    init_db()

    # Load the 24 units from your themes.json
    with open("learning/themes.json", "r") as f:
        curriculum = json.load(f)

    print("🧠 Starting AI Generation (this may take a while)...")
    
    for section in curriculum["sections"]:
        league = section["league"]
        for unit in section["units"]:
            unit_id = unit["unit_id"]
            topics = unit["topics"]
            
            print(f"📦 Generating 20 questions for {unit['title']}...")
            # CALLS: learning.generator.mass_generate_questions
            mass_generate_questions(unit_id, topics, league)
            print(f"✅ Finished {unit_id}")

    print("✨ Database fully seeded with unique, hardware-aware questions!")

if __name__ == "__main__":
    run_seeding()
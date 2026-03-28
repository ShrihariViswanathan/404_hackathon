import sys
import os
import json

# 1. PATH DISCOVERY: Find the 'backend' root directory
# This gets the directory where seed_all.py is, then goes up two levels
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.learning.database import init_db, get_db_connection
from learning.generator import mass_generate_bulk

def seed_entire_curriculum():
    print("🚀 INITIALIZING GOLD-STANDARD SEEDING...")
    init_db()

    # 2. FIXED PATH: Explicitly point to backend/learning/themes.json
    theme_path = os.path.join(BASE_DIR, "learning", "themes.json")
    
    if not os.path.exists(theme_path):
        print(f"❌ CRITICAL ERROR: Could not find themes.json at: {theme_path}")
        print("Please ensure themes.json is inside the 'learning' folder.")
        return

    with open(theme_path, "r") as f:
        curriculum = json.load(f)

    # ... rest of your loop logic ...

    conn = get_db_connection()

    for section in curriculum["sections"]:
        league = section["league"]
        print(f"\n🏆 LEAGUE: {league.upper()}")
        print("="*30)

        for unit in section["units"]:
            unit_id = unit["unit_id"]
            topics = unit["topics"]
            
            # Check current count for this unit
            current_count = conn.execute(
                'SELECT COUNT(*) FROM questions WHERE unit_id=?', (unit_id,)
            ).fetchone()[0]

            print(f"📦 Unit: {unit['title']} (ID: {unit_id})")
            print(f"📊 Current questions in DB: {current_count}")

            if current_count >= 80:
                print(f"⏩ skipping {unit_id} - already has {current_count} questions.")
                continue

            # This triggers the 4-style loop in generator.py
            # We pass topics as a list; Llama 3 will handle the bulk creation
            mass_generate_bulk(unit_id, topics, league)

    print("\n" + "="*40)
    print("✨ ALL UNITS SEEDED SUCCESSFULLY ✨")
    
    # Final Inventory
    final_total = conn.execute('SELECT COUNT(*) FROM questions').fetchone()[0]
    print(f"📚 Total Questions in Local Bank: {final_total}")
    conn.close()

if __name__ == "__main__":
    seed_entire_curriculum()
import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from learning.database import init_db, get_db_connection
from backend.learning.generation import mass_generate_bulk

def run_seeding():
    print("🚀 Initializing DB...")
    init_db()

    theme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "themes.json")

    with open(theme_path, "r") as f:
        curriculum = json.load(f)

    for section in curriculum["sections"]:
        league = section["league"]

        for unit in section["units"]:
            print(f"\n📦 {unit['title']}")

            mass_generate_bulk(
                unit_id=unit["unit_id"],
                topics=unit["topics"],
                league=league
            )

    conn = get_db_connection()
    total = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    conn.close()

    print(f"\n🔥 TOTAL QUESTIONS: {total}")


if __name__ == "__main__":
    run_seeding()
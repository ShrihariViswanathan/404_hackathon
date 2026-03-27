import ollama
import json
import random
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
TOPIC_PATH = Path(__file__).resolve().parent / "topics.json"

def get_topic(diff):
    try:
        with open(TOPIC_PATH, "r") as f:
            data = json.load(f)
        curriculum = data.get("stock_market_curriculum", {})
        topics = curriculum.get(f"{diff}_topics", [])
        return random.choice(topics) if topics else "Technical Analysis"
    except Exception as e:
        return "Trading Strategies"

def generate_question(topic, difficulty):
    # System prompt forces the model to stay on Stock Market topics
    system_instruction = (
        "You are an expert Wall Street Trading Instructor. "
        "You only generate questions related to the Stock Market, Trading, and Finance. "
        "Never generate questions about sports, cooking, or unrelated fields."
    )
    
    user_prompt = f"""
    Generate ONE {difficulty} level MCQ about the trading topic: {topic}.
    Use a professional tone and realistic market scenarios.
    
    Format the output as a JSON object with:
    {{
      "question": "...",
      "options": ["...", "...", "...", "..."],
      "answer": 0,
      "explanation": "..."
    }}
    """

    try:
        response = ollama.chat(
            model='llama3',
            messages=[
                {'role': 'system', 'content': system_instruction},
                {'role': 'user', 'content': user_prompt}
            ],
            format='json' # This prevents the "line 1 column 1" error
        )

        return json.loads(response['message']['content'])

    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "question": f"Explain the role of {topic} in risk management.",
            "options": ["Hedging", "Speculation", "Arbitrage", "Scalping"],
            "answer": 0,
            "explanation": "Local model failed to generate. Please check Ollama logs."
        }

def get_question(diff="medium"):
    topic = get_topic(diff)
    q_data = generate_question(topic, diff)
    q_data["difficulty"] = diff
    q_data["topic"] = topic
    return q_data
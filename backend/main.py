from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from placement.generator import get_question

app = FastAPI(title="BMSCE Placement Prep API")

# Enable CORS so your frontend can access the local server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "Running", "engine": "Ollama (Llama-3)"}

@app.get("/question")
def fetch_question(difficulty: str = "medium"):
    """
    Returns a generated trading question.
    Example: http://127.0.0.1:8000/question?difficulty=hard
    """
    return get_question(difficulty)
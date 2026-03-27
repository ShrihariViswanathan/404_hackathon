from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from placement.generator import exam_cache
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def preload():
    exam_cache.refresh_cache()

@app.get("/quiz/all")
def get_all():
    return {"questions": exam_cache.cached_questions}

@app.get("/quiz/refresh")
def refresh():
    exam_cache.refresh_cache()
    return {"status": "success", "count": len(exam_cache.cached_questions)}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
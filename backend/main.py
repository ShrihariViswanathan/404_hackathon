import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from learning.routes import router as learning_router
from learning.database import init_db

app = FastAPI()
from placement.routes import router as placement_router

app.include_router(placement_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()
    print("✅ Server Ready (DB only mode)")


app.include_router(learning_router)


@app.get("/")
def home():
    return {"status": "running"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
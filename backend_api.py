from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.pipeline import answer_question

#create the backend server
app = FastAPI()

# Enabling CORS to block requests different ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default dev server port
    allow_methods=["*"],
    allow_headers=["*"],
)
#define the request format
class QuestionRequest(BaseModel):
    question: str

#the api endpoint
@app.post("/api/ask")
def ask(request: QuestionRequest):
    #trigger the rag pipeline
    result = answer_question(request.question)
    return result

@app.get("/api/health")
def health():
    return {"status": "ok"}
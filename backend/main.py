# main.py - FastAPI backend with /chat endpoint
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import process_user_query

app = FastAPI(title="AI Chatbot Backend")

# Allow Streamlit frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserQuery(BaseModel):
    question: str

@app.post("/chat")
async def chat(query: UserQuery):
    response_text = process_user_query(query.question)
    return {"response": response_text}

# Health check
@app.get("/")
async def root():
    return {"status": "Chatbot backend is running! 🚀"}
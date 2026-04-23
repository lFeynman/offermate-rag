from fastapi import FastAPI
from pydantic import BaseModel
from rag.pipeline import answer_query

app = FastAPI(title="OfferMate-RAG API")


class ChatRequest(BaseModel):
    query: str
    data_dir: str = "data"
    top_k: int = 3


@app.get("/")
def root():
    return {"message": "OfferMate-RAG backend is running."}


@app.post("/chat")
def chat(req: ChatRequest):
    result = answer_query(req.query, req.data_dir, req.top_k)
    return result.model_dump()
from fastapi import FastAPI
from pydantic import BaseModel

from rag.pipeline import answer_query
from agent.workflow import run_workflow


app = FastAPI(title="OfferMate-RAG API")


class ChatRequest(BaseModel):
    query: str
    data_dir: str = "data"
    top_k: int = 3


class WorkflowRequest(BaseModel):
    query: str
    jd_text: str = ""
    resume_text: str = ""
    doc_text: str = ""


@app.get("/")
def root():
    return {"message": "OfferMate-RAG backend is running."}


@app.post("/chat")
def chat(req: ChatRequest):
    result = answer_query(req.query, req.data_dir, req.top_k)
    return result.model_dump()


@app.post("/workflow")
def workflow(req: WorkflowRequest):
    result = run_workflow(
        query=req.query,
        jd_text=req.jd_text,
        resume_text=req.resume_text,
        doc_text=req.doc_text
    )
    return result.model_dump()
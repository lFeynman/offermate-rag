from fastapi import FastAPI

app=FastAPI(title="OfferMate-RAG API")

@app.get("/")
def read():
    return {"message": "OfferMate-RAG API is running!"}
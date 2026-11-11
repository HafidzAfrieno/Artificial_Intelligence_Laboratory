from fastapi import FastAPI

app = FastAPI(
    title="Document RAG System",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "project": "Document RAG System",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
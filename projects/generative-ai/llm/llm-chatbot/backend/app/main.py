from fastapi import FastAPI

app = FastAPI(
    title="LLM Chatbot",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "project": "LLM Chatbot",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
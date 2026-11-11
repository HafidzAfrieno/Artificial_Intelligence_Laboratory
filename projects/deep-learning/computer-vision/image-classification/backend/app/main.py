from fastapi import FastAPI

app = FastAPI(
    title="Image Classification",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "project": "Image Classification",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
from fastapi import FastAPI

app = FastAPI(
    title="Heart Disease Risk Classification",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "project": "Heart Disease Risk Classification",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
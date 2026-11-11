from fastapi import FastAPI

app = FastAPI(
    title="Heart Disease Prediction",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "project": "Heart Disease Prediction",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
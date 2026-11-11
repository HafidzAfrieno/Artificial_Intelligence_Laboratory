from fastapi import FastAPI

app = FastAPI(
    title="{{cookiecutter.project_name}}",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "project": "{{cookiecutter.project_name}}",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
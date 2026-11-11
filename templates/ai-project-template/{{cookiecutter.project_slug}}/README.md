# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

## Project Information

| Attribute | Value |
|---|---|
| Category | {{cookiecutter.category}} |
| Type | {{cookiecutter.project_type}} |
| Framework | {{cookiecutter.model_framework}} |
| Author | {{cookiecutter.author_name}} |

## Tech Stack

- Python
- FastAPI
- React
- Docker
- Hugging Face

## Project Structure

- backend: FastAPI
- frontend: React
- model: AI/ML development
- deployment: Docker Compose

## Installation

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
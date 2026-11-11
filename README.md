# AI Engineering Lab

Repository untuk mengembangkan berbagai project Artificial Intelligence (AI), Machine Learning, Deep Learning, Generative AI, dan AI Engineering menggunakan arsitektur Monorepo.

## Project Generator

Repository ini menggunakan **Cookiecutter** untuk membuat struktur project secara otomatis berdasarkan kategori dan tipe project.

### Command Template

Format dasar:

```bash
python scripts/create_project.py --name "NAMA PROJECT" --category KATEGORI --type TIPE_PROJECT --framework FRAMEWORK --description "DESKRIPSI PROJECT"
```

## 1. Machine Learning

### Classification

```bash
python scripts/create_project.py --name "Heart Disease Prediction" --category machine-learning --type classification --framework scikit-learn --description "Heart disease prediction using machine learning"
```

### Regression

```bash
python scripts/create_project.py --name "House Price Prediction" --category machine-learning --type regression --framework scikit-learn --description "House price prediction system"
```

### Clustering

```bash
python scripts/create_project.py --name "Customer Segmentation" --category machine-learning --type clustering --framework scikit-learn --description "Customer segmentation using clustering"
```

## 2. Deep Learning

### Computer Vision

```bash
python scripts/create_project.py --name "Image Classification" --category deep-learning --type computer-vision --framework pytorch --description "Image classification using CNN"
```

### NLP

```bash
python scripts/create_project.py --name "Sentiment Analysis" --category deep-learning --type nlp --framework pytorch --description "Text sentiment analysis using deep learning"
```

### Neural Networks

```bash
python scripts/create_project.py --name "Neural Network Playground" --category deep-learning --type neural-networks --framework pytorch --description "Neural network experimentation project"
```

## 3. Generative AI

### LLM

```bash
python scripts/create_project.py --name "LLM Chatbot" --category generative-ai --type llm --framework transformers --huggingface-model-id "google/flan-t5-base" --description "LLM chatbot application"
```

### RAG

```bash
python scripts/create_project.py --name "Document RAG System" --category generative-ai --type rag --framework langchain --description "Retrieval augmented generation for documents"
```

### AI Agents

```bash
python scripts/create_project.py --name "Research AI Agent" --category generative-ai --type ai-agents --framework langchain --description "AI agent for research assistance"
```

### Fine-Tuning

```bash
python scripts/create_project.py --name "LLM Fine Tuning" --category generative-ai --type fine-tuning --framework transformers --description "LLM fine tuning experimentation"
```

## 4. AI Engineering

### MLOps

```bash
python scripts/create_project.py --name "ML Model Deployment" --category ai-engineering --type mlops --framework mlflow --description "Machine learning deployment and lifecycle management"
```

### Data Pipeline

```bash
python scripts/create_project.py --name "AI Data Pipeline" --category ai-engineering --type data-pipeline --framework pandas --description "Automated data processing pipeline"
```

### Model Monitoring

```bash
python scripts/create_project.py --name "ML Model Monitoring" --category ai-engineering --type model-monitoring --framework evidently --description "Machine learning model monitoring system"
```

## 5. Generator Options

| Argument | Keterangan | Default |
|---|---|---|
| `--name` | Nama project | Wajib |
| `--category` | Kategori project | Wajib |
| `--type` | Tipe project | Wajib |
| `--framework` | Framework AI/ML | `scikit-learn` |
| `--description` | Deskripsi project | `AI-powered application` |
| `--author` | Nama author | `AI Engineering Lab` |
| `--huggingface-model-id` | Hugging Face Model ID | Kosong |
| `--python-version` | Versi Python | `3.11` |
| `--debug` | Menampilkan traceback ketika error | `False` |

## 6. Kategori dan Tipe Project

| Category | Available Types |
|---|---|
| `machine-learning` | classification, regression, clustering |
| `deep-learning` | computer-vision, nlp, neural-networks |
| `generative-ai` | llm, rag, ai-agents, fine-tuning |
| `ai-engineering` | mlops, data-pipeline, model-monitoring |

## 7. Output Directory

Setiap project akan dibuat secara otomatis berdasarkan kategori dan tipe project.

```text
AI-Engineering-Lab/
│
├── projects/
│   ├── machine-learning/
│   │   ├── classification/
│   │   │   └── heart-disease-prediction/
│   │   ├── regression/
│   │   │   └── house-price-prediction/
│   │   └── clustering/
│   │       └── customer-segmentation/
│   │
│   ├── deep-learning/
│   │   ├── computer-vision/
│   │   ├── nlp/
│   │   └── neural-networks/
│   │
│   ├── generative-ai/
│   │   ├── llm/
│   │   ├── rag/
│   │   ├── ai-agents/
│   │   └── fine-tuning/
│   │
│   └── ai-engineering/
│       ├── mlops/
│       ├── data-pipeline/
│       └── model-monitoring/
│
├── templates/
│   └── ai-project-template/
│
├── scripts/
│   └── create_project.py
│
├── shared/
├── .github/
├── README.md
└── LICENSE
```

## 8. Cara Menjalankan Generator

Pastikan terminal berada di root repository.

Install Cookiecutter:

```bash
pip install cookiecutter
```

Contoh menjalankan generator:

```bash
python scripts/create_project.py --name "Heart Disease Prediction" --category machine-learning --type classification --framework scikit-learn
```

Setelah project berhasil dibuat, masuk ke direktori project dan mulai pengembangan.

## Notes

- Setiap project memiliki direktori dan konfigurasi independen.
- Setiap project dapat memiliki dependency berbeda.
- Docker dan Docker Compose dikonfigurasi per project.
- Deployment dapat dilakukan secara independen.
- Hugging Face dapat digunakan untuk menyimpan dan mengelola model.
- Jangan menyimpan API key, token, atau credential di repository.
- Folder project yang sudah ada tidak akan ditimpa oleh generator.

---

**AI Engineering Lab — Build, Experiment, Deploy.**
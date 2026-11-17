# AI-Engineering-Lab

**AI-Engineering-Lab** adalah repository berbasis monorepo yang dirancang untuk membantu proses pengembangan berbagai project Artificial Intelligence secara terstruktur dan konsisten.

Repository ini menggunakan **Cookiecutter** sebagai template generator untuk membuat project baru secara otomatis berdasarkan struktur dan konfigurasi yang telah disediakan.

## Objectives

- Menyediakan struktur project AI yang konsisten.
- Mempercepat proses inisialisasi project baru.
- Memisahkan kebutuhan pengembangan model, backend, frontend, dan deployment.
- Mempermudah pengelolaan serta pemeliharaan setiap project.
- Menyediakan template yang dapat dikembangkan sesuai kebutuhan.

## Project Structure

```text
AI-Engineering-Lab/
│
├── projects/
│   └── machine-learning/
│       └── project-name/
│
├── templates/
│   └── machine-learning/
│       ├── cookiecutter.json
│       └── {{cookiecutter.project_slug}}/
│
├── scripts/
│   └── create_project.py
│
├── README.md
└── .gitignore
```

### Directory Description

| Directory / File | Description |
|---|---|
| `projects/` | Menyimpan seluruh project yang dihasilkan. |
| `templates/` | Menyimpan template untuk membuat project baru. |
| `scripts/` | Menyimpan script otomatisasi pembuatan project. |
| `create_project.py` | Menjalankan proses pembuatan project menggunakan Cookiecutter. |
| `cookiecutter.json` | Menyimpan konfigurasi dan informasi default template. |

## Technology Stack

Teknologi yang digunakan dapat disesuaikan dengan kebutuhan setiap project.

| Category | Technology |
|---|---|
| Project Generator | Python, Cookiecutter |
| Machine Learning | Python, Scikit-learn |
| Backend | FastAPI |
| Frontend | React, Vite |
| Model Hosting | Hugging Face Spaces |
| Containerization | Docker, Docker Compose |

## Getting Started

### 1. Clone Repository

```bash
git clone https://github.com/username/AI-Engineering-Lab.git

cd AI-Engineering-Lab
```

Ganti `username` dengan username GitHub milikmu.

### 2. Create Python Environment

Menggunakan Conda:

```bash
conda create -n ai-engineering-lab python=3.11
```

Aktifkan environment:

```bash
conda activate ai-engineering-lab
```

### 3. Install Dependencies

Instal Cookiecutter:

```bash
python -m pip install cookiecutter
```

Periksa instalasi:

```bash
python -m pip show cookiecutter
```

### 4. Generate New Project

Gunakan perintah berikut untuk membuat project baru:

```bash
python scripts/create_project.py machine-learning <project-name>
```

Contoh:

```bash
python scripts/create_project.py machine-learning house-price-prediction
```

Project akan dibuat secara otomatis pada:

```text
projects/
└── machine-learning/
    └── house-price-prediction/
```

## Machine Learning Project Structure

Setiap project Machine Learning yang dihasilkan memiliki pemisahan tanggung jawab sebagai berikut:

| Directory | Responsibility |
|---|---|
| `model/` | Eksplorasi data, preprocessing, training, dan evaluasi model. |
| `backend/` | Menyediakan REST API menggunakan FastAPI. |
| `frontend/` | Menyediakan antarmuka pengguna menggunakan React. |
| `docker/` | Mengatur containerization dan deployment. |

Backend bertanggung jawab menangani komunikasi dengan model yang telah di-host di Hugging Face Spaces.

## Docker

Project yang dihasilkan menyediakan konfigurasi Docker untuk menjalankan layanan backend dan frontend.

Jalankan dari direktori project:

```bash
docker compose -f docker/docker-compose.yml up --build -d
```

Periksa container:

```bash
docker compose -f docker/docker-compose.yml ps
```

Hentikan container:

```bash
docker compose -f docker/docker-compose.yml down
```

## Development Notes

- Setiap project dibuat secara terpisah di dalam direktori `projects/`.
- Template dikelola secara terpusat di dalam direktori `templates/`.
- Perubahan template tidak secara otomatis mengubah project yang sudah dibuat.
- Konfigurasi sensitif seperti API token harus disimpan dalam file `.env`.
- Jangan mengunggah file `.env` atau credentials ke repository.
- Gunakan `.env.example` sebagai referensi konfigurasi environment.

## License

Repository ini digunakan sebagai learning laboratory dan pengembangan project Artificial Intelligence.

---

**AI-Engineering-Lab**  
*Build, Experiment, and Develop Artificial Intelligence Projects.*
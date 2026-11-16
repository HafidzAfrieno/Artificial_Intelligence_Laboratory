# AI-Engineering-Lab

Repository untuk membangun, mengembangkan, dan mengelola berbagai proyek Artificial Intelligence (AI) dan Machine Learning dalam satu tempat.

AI-Engineering-Lab menggunakan pendekatan **Monorepo** dengan sistem template berbasis Cookiecutter. Setiap kategori AI memiliki template proyek masing-masing sehingga pembuatan proyek baru dapat dilakukan dengan struktur yang konsisten tanpa harus membuat direktori dan konfigurasi dari awal.

## 1. Tujuan Project

AI-Engineering-Lab dibuat untuk:

- Mengelola berbagai proyek AI dalam satu repository.
- Menyediakan template proyek yang dapat digunakan berulang kali.
- Mempermudah pembuatan proyek baru.
- Menjaga konsistensi struktur folder dan konfigurasi.
- Memisahkan kode pengembangan model dengan aplikasi yang menjalankan model.
- Mempermudah integrasi model AI dengan backend, frontend, dan Docker.

## 2. Struktur Repository

```text
AI-Engineering-Lab/
│
├── projects/
│   ├── machine-learning/
│   ├── deep-learning/
│   ├── nlp/
│   ├── llm/
│   ├── ai-agent/
│   └── computer-vision/
│
├── templates/
│   ├── machine-learning/
│   ├── deep-learning/
│   ├── nlp/
│   ├── llm/
│   ├── ai-agent/
│   └── computer-vision/
│
├── scripts/
│   └── create_project.py
│
├── README.md
└── .gitignore
```

### Penjelasan Direktori

| Direktori | Fungsi |
|---|---|
| `projects/` | Menyimpan seluruh proyek yang telah dibuat |
| `templates/` | Menyimpan template Cookiecutter berdasarkan kategori AI |
| `scripts/` | Menyimpan script untuk mempermudah pembuatan proyek |
| `README.md` | Dokumentasi utama repository |
| `.gitignore` | Mengatur file dan direktori yang tidak perlu disimpan ke Git |

### Kategori Proyek

| Kategori | Deskripsi |
|---|---|
| Machine Learning | Proyek klasifikasi, regresi, dan clustering |
| Deep Learning | Proyek neural network dan deep learning |
| NLP | Proyek Natural Language Processing |
| LLM | Proyek berbasis Large Language Models |
| AI Agent | Proyek intelligent agent dan agentic workflow |
| Computer Vision | Proyek pengolahan dan analisis citra |

## 3. Teknologi yang Digunakan

| Teknologi | Kegunaan |
|---|---|
| Python | Bahasa pemrograman utama untuk pengembangan AI |
| Cookiecutter | Membuat proyek dari template |
| Git | Version control |
| React.js | Pengembangan frontend aplikasi |
| FastAPI | Pengembangan backend API |
| Docker | Containerization aplikasi |
| Docker Compose | Mengelola beberapa container |

Teknologi tambahan dapat berbeda pada setiap kategori proyek sesuai kebutuhan masing-masing.

## 4. Persyaratan Sistem

Sebelum menggunakan repository, pastikan perangkat sudah memiliki:

- Python 3.10 atau lebih baru.
- pip.
- Git.
- Cookiecutter.
- Node.js dan npm (untuk proyek yang menggunakan React.js).
- Docker Desktop (untuk menjalankan aplikasi menggunakan Docker).

Periksa instalasi:

```powershell
python --version
python -m pip --version
git --version
node --version
npm --version
docker --version
```

## 5. Instalasi Repository

Clone repository:

```powershell
git clone <repository-url>
```

Masuk ke direktori:

```powershell
cd AI-Engineering-Lab
```

### Instalasi Cookiecutter

Instal Cookiecutter menggunakan pip:

```powershell
python -m pip install cookiecutter
```

Periksa instalasi:

```powershell
cookiecutter --version
```

## 6. Membuat Project Baru

AI-Engineering-Lab menyediakan dua cara untuk membuat proyek baru.

### Cara 1. Menggunakan Script Generator

Gunakan script generator yang tersedia di direktori `scripts/`.

Format command:

```powershell
python scripts/create_project.py <kategori> <nama-project>
```

Contoh membuat proyek Machine Learning:

```powershell
python scripts/create_project.py machine-learning house-price-prediction
```

Contoh kategori lainnya:

```powershell
python scripts/create_project.py deep-learning image-classification

python scripts/create_project.py nlp sentiment-analysis

python scripts/create_project.py llm document-assistant

python scripts/create_project.py ai-agent research-agent

python scripts/create_project.py computer-vision object-detection
```

Proyek yang berhasil dibuat akan ditempatkan pada direktori kategori yang sesuai di dalam `projects/`.

Contoh hasil:

```text
projects/
└── machine-learning/
    └── house-price-prediction/
```

### Cara 2. Menggunakan Cookiecutter Secara Langsung

Jika ingin membuat proyek tanpa script generator, jalankan Cookiecutter secara langsung.

Contoh untuk template Machine Learning:

```powershell
cookiecutter templates/machine-learning --output-dir projects/machine-learning
```

Cookiecutter akan meminta informasi proyek seperti:

- `project_name`: Nama proyek.
- `project_slug`: Nama direktori proyek.
- `package_name`: Nama package Python.
- `description`: Deskripsi proyek.
- `author`: Nama pembuat proyek.

Setelah semua informasi diisi, Cookiecutter akan menghasilkan direktori proyek di dalam `projects/machine-learning/`.

## 7. Menggunakan Template Machine Learning

Template Machine Learning menyediakan struktur awal untuk membangun aplikasi berbasis model Machine Learning.

### Fitur Template

- Data exploration menggunakan Jupyter Notebook.
- Data preprocessing.
- Feature engineering.
- Model training.
- Model evaluation.
- Model prediction.
- Penyimpanan model dalam folder artifacts.
- Backend API menggunakan FastAPI.
- Frontend menggunakan React.js.
- Deployment menggunakan Docker.

### Struktur Umum Proyek Machine Learning

```text
house-price-prediction/
│
├── model/
│   ├── notebooks/
│   ├── data/
│   │   ├── raw/
│   │   └── processed/
│   ├── src/
│   ├── artifacts/
│   ├── pyproject.toml
│   └── requirements.txt
│
├── backend/
├── frontend/
├── docker/
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

Untuk panduan instalasi, penggunaan, dan penjelasan lebih lengkap, lihat README pada template Machine Learning:

```text
templates/machine-learning/
```

## 8. Prinsip Pengembangan

AI-Engineering-Lab menggunakan beberapa prinsip berikut:

**1. Sederhana dan Mudah Dipelihara**

Setiap proyek memiliki struktur yang disesuaikan dengan kebutuhan teknologinya. Hindari menambahkan konfigurasi atau direktori yang belum diperlukan.

**2. Setiap Proyek Berdiri Sendiri**

Setiap proyek memiliki dependency, konfigurasi, dokumentasi, dan kebutuhan pengembangannya masing-masing.

**3. Template yang Dapat Digunakan Kembali**

Template digunakan untuk mempercepat pembuatan proyek baru dengan struktur dasar yang konsisten.

**4. Pemisahan Model dan Aplikasi**

Kode eksplorasi, training, dan eksperimen model ditempatkan di direktori `model/`. Backend bertanggung jawab untuk menjalankan inference melalui API.

**5. Fleksibilitas Deployment**

Setiap proyek dapat menggunakan metode deployment yang sesuai dengan kebutuhan, baik secara lokal, menggunakan Docker, maupun layanan cloud.

## 9. Roadmap Pengembangan

| Status | Kategori |
|---|---|
| Dalam pengembangan | Machine Learning |
| Direncanakan | Deep Learning |
| Direncanakan | NLP |
| Direncanakan | LLM |
| Direncanakan | AI Agent |
| Direncanakan | Computer Vision |

## 10. Kontribusi

Pengembangan repository dapat dilakukan dengan cara:

1. Membuat atau memperbarui template.
2. Memperbaiki struktur proyek.
3. Menambahkan dokumentasi.
4. Memperbaiki bug.
5. Mengembangkan contoh implementasi proyek AI.

Pastikan setiap perubahan tetap mengikuti prinsip sederhana, konsisten, dan mudah dipelihara.

---

**AI-Engineering-Lab**  
*A collection of reusable templates and projects for AI Engineering.*
# House Price Prediction

Machine Learning project

Proyek Machine Learning yang menggunakan Python untuk membangun, melatih, mengevaluasi, dan menjalankan model prediksi. Proyek ini dilengkapi dengan backend FastAPI, frontend React.js, serta Docker untuk mempermudah proses deployment.

## 1. Teknologi yang Digunakan

| Teknologi | Kegunaan |
|---|---|
| Python | Bahasa pemrograman utama untuk Machine Learning |
| Pandas | Manipulasi dan analisis data |
| NumPy | Operasi numerik |
| Scikit-learn | Preprocessing, training, dan evaluasi model |
| Matplotlib | Visualisasi data |
| Seaborn | Visualisasi statistik |
| Joblib | Menyimpan dan memuat model |
| Jupyter Notebook | Eksplorasi dan eksperimen Machine Learning |
| FastAPI | Backend API untuk menjalankan prediksi |
| React.js | Frontend aplikasi web |
| Docker | Menjalankan aplikasi dalam container |
| Docker Compose | Mengelola frontend dan backend |

## 2. Struktur Project

```text
Heart-Disease-Risk-Classification/
├── model/
│   ├── notebooks/
│   ├── data/
│   │   ├── raw/
│   │   └── processed/
│   ├── src/
│   │   └── house_price_prediction/
│   │       ├── __init__.py
│   │       ├── preprocessing.py
│   │       ├── feature_engineering.py
│   │       ├── train.py
│   │       ├── evaluate.py
│   │       └── predict.py
│   ├── artifacts/
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── README.md
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── README.md
│
├── docker/
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## 3. Persyaratan Sistem

Pastikan perangkat sudah memiliki:

- Python 3.10 atau lebih baru.
- Node.js dan npm.
- Git.
- Docker Desktop (jika ingin menjalankan aplikasi menggunakan Docker).

Periksa instalasi melalui terminal:

```powershell
python --version
node --version
npm --version
git --version
docker --version
```

## 4. Instalasi Project

### 4.1. Clone Repository

Jika proyek sudah berada di GitHub:

```powershell
git clone <repository-url>
cd Heart-Disease-Risk-Classification
```

Jika proyek sudah dihasilkan melalui Cookiecutter di komputer lokal, cukup masuk ke direktori proyek tersebut.

### 4.2. Instalasi Environment Machine Learning

Masuk ke direktori model:

```powershell
cd model
```

Buat virtual environment:

```powershell
python -m venv .venv
```

Aktifkan environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instal dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Instal package dalam mode editable:

```powershell
python -m pip install -e .
```

Mode editable memungkinkan modul di dalam `src/` diimpor tanpa harus menginstal ulang package setiap kali kode sumber diubah.

### 4.3. Menjalankan Jupyter Notebook

Pastikan environment sudah aktif, kemudian jalankan:

```powershell
jupyter notebook
```

Notebook tersedia di:

```text
model/notebooks/
```

Urutan pengerjaan notebook:

1. `01_data_exploration.ipynb`: Eksplorasi dan analisis dataset.
2. `02_data_preprocessing.ipynb`: Persiapan dan transformasi data.
3. `03_model_training.ipynb`: Training, evaluasi, dan penyimpanan model.

### 4.4. Menyiapkan Dataset

Letakkan dataset mentah di:

```text
model/data/raw/
```

Hasil preprocessing atau dataset yang sudah ditransformasi dapat disimpan di:

```text
model/data/processed/
```

Sesuaikan nama file dan lokasi dataset dengan konfigurasi notebook yang digunakan.

## 5. Penggunaan Pipeline Machine Learning

Package Machine Learning menyediakan beberapa fungsi utama.

| Modul | Kegunaan |
|---|---|
| `preprocessing.py` | Membaca dataset dan membagi fitur-target serta data training-testing |
| `feature_engineering.py` | Membuat pipeline transformasi fitur |
| `train.py` | Melatih dan menyimpan model |
| `evaluate.py` | Mengevaluasi performa model |
| `predict.py` | Memuat model dan menghasilkan prediksi |

Contoh import:

```python
from house_price_prediction.preprocessing import (
    load_data,
    split_features_target,
    split_data
)

from house_price_prediction.feature_engineering import (
    create_preprocessor
)

from house_price_prediction.train import train_model

from house_price_prediction.evaluate import (
    evaluate_regression,
    evaluate_classification
)

from house_price_prediction.predict import (
    load_model,
    predict
)
```

Model hasil training disimpan di:

```text
model/artifacts/
```

## 6. Menjalankan Backend FastAPI

Masuk ke direktori backend:

```powershell
cd ../backend
```

Buat dan aktifkan virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instal dependencies:

```powershell
python -m pip install -r requirements.txt
```

Jalankan server:

```powershell
uvicorn app.main:app --reload
```

Backend secara default dapat diakses melalui:

```text
http://127.0.0.1:8000
```

Dokumentasi API FastAPI:

```text
http://127.0.0.1:8000/docs
```

Pastikan model yang sudah dilatih tersedia di folder `model/artifacts/` dan lokasi model sudah disesuaikan dengan konfigurasi backend.

## 7. Menjalankan Frontend React.js

Buka terminal baru, kemudian masuk ke direktori frontend:

```powershell
cd frontend
```

Instal dependencies:

```powershell
npm install
```

Jalankan development server:

```powershell
npm run dev
```

Alamat frontend mengikuti konfigurasi development server pada proyek React.

Pastikan alamat backend yang digunakan frontend sudah sesuai dengan konfigurasi API.

## 8. Menjalankan Menggunakan Docker

Pastikan Docker Desktop sudah aktif.

Dari direktori root proyek, jalankan:

```powershell
docker compose up --build
```

Untuk menjalankan container di background:

```powershell
docker compose up --build -d
```

Melihat container yang berjalan:

```powershell
docker compose ps
```

Menghentikan container:

```powershell
docker compose down
```

Pastikan konfigurasi Dockerfile dan `docker-compose.yml` sudah disesuaikan dengan struktur proyek.

## 9. Alur Kerja Machine Learning

Alur umum pengembangan proyek:

1. Mengumpulkan dan menyiapkan dataset.
2. Melakukan eksplorasi data.
3. Melakukan preprocessing dan feature engineering.
4. Membagi dataset menjadi training dan testing.
5. Melatih model Machine Learning.
6. Mengevaluasi performa model.
7. Menyimpan model hasil training.
8. Mengintegrasikan model ke backend FastAPI.
9. Menghubungkan frontend React.js dengan backend.
10. Menjalankan aplikasi menggunakan Docker.

## 10. Catatan Pengembangan

- Gunakan `model/notebooks/` untuk eksplorasi dan eksperimen.
- Gunakan `model/src/` untuk menyimpan kode Python yang dapat digunakan kembali.
- Simpan model hasil training di `model/artifacts/`.
- Jangan mencampurkan kode training dengan kode backend.
- Backend bertanggung jawab untuk memuat model dan menjalankan inference.
- Sesuaikan preprocessing dengan karakteristik dataset.
- Jangan memasukkan dataset berukuran besar, model, atau file sensitif ke Git tanpa pertimbangan.

## 11. Author

**Author:** Hafidz Akmal

**Project:** House Price Prediction
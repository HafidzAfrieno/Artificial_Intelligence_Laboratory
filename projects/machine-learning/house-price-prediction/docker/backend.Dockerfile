
# Menggunakan Python 3.11
FROM python:3.11-slim

# Mengatur direktori kerja
WORKDIR /app

# Mencegah Python membuat file .pyc
ENV PYTHONDONTWRITEBYTECODE=1

# Menampilkan output Python secara langsung
ENV PYTHONUNBUFFERED=1

# Menyalin requirements backend
COPY backend/requirements.txt ./requirements.txt

# Menginstal dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Menyalin source code backend
COPY backend/app ./app

# Membuka port FastAPI
EXPOSE 8000

# Menjalankan FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

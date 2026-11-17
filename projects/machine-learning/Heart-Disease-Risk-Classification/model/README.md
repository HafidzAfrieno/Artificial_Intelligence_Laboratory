# Model Development

Direktori ini digunakan untuk seluruh proses pengembangan Machine Learning, mulai dari eksplorasi data hingga evaluasi dan penyimpanan model.

## Directory Structure

- `notebooks/`: Eksperimen dan eksplorasi data menggunakan Jupyter Notebook.
- `data/raw/`: Dataset asli.
- `data/processed/`: Dataset yang telah diproses.
- `src/`: Source code Python untuk pengembangan Machine Learning.
- `artifacts/`: Model hasil training dan artefak pendukung.

## Installation

Masuk ke direktori `model/`, kemudian jalankan:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Import Package

Contoh penggunaan package:

```python
from Heart_Disease_Risk_Classification.preprocessing import preprocess_data
```

## Development Workflow

1. Explore dataset menggunakan notebooks.
2. Lakukan preprocessing.
3. Lakukan feature engineering jika diperlukan.
4. Latih model.
5. Evaluasi model.
6. Simpan model ke direktori `artifacts/`.

from pathlib import Path
import joblib
import pandas as pd


def load_model(model_path: str):
    """
    Memuat model dari file artifacts.
    """

    path = Path(model_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Model tidak ditemukan: {path}"
        )

    return joblib.load(path)


def predict(model, data):
    """
    Melakukan prediksi menggunakan model.
    """

    # Memastikan input berbentuk DataFrame
    if isinstance(data, dict):
        data = pd.DataFrame([data])

    elif not isinstance(data, pd.DataFrame):
        raise TypeError(
            "Input harus berupa dictionary atau pandas DataFrame."
        )

    predictions = model.predict(data)

    return predictions.tolist()


from pathlib import Path
import joblib

from sklearn.pipeline import Pipeline

from .feature_engineering import create_preprocessor


def train_model(
    model,
    X_train,
    y_train,
    model_name: str = "model",
    artifacts_dir: str = "artifacts"
):
    """
    Melatih model dengan preprocessing pipeline
    dan menyimpan model hasil training.
    """

    # Membuat preprocessing
    preprocessor = create_preprocessor(X_train)

    # Menggabungkan preprocessing dan model
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    # Melatih model
    pipeline.fit(X_train, y_train)

    # Membuat direktori artifacts jika belum tersedia
    artifacts_path = Path(artifacts_dir)
    artifacts_path.mkdir(parents=True, exist_ok=True)

    # Menyimpan model
    model_path = artifacts_path / f"{model_name}.joblib"
    joblib.dump(pipeline, model_path)

    print(f"Model berhasil disimpan: {model_path}")

    return pipeline

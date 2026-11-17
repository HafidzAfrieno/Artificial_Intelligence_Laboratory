
import pandas as pd
from sklearn.model_selection import train_test_split


def load_data(file_path: str) -> pd.DataFrame:
    """
    Membaca dataset dari file CSV.
    """
    return pd.read_csv(file_path)


def split_features_target(
    data: pd.DataFrame,
    target_column: str
):
    """
    Memisahkan fitur dan target.
    """
    if target_column not in data.columns:
        raise ValueError(
            f"Kolom target '{target_column}' tidak ditemukan."
        )

    X = data.drop(columns=[target_column])
    y = data[target_column]

    return X, y


def split_data(
    X,
    y,
    test_size: float = 0.2,
    random_state: int = 42
):
    """
    Membagi dataset menjadi training dan testing.
    """
    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state
    )

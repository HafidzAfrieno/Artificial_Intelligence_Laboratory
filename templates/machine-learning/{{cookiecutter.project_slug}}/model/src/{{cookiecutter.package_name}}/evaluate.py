
import numpy as np

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


def evaluate_classification(model, X_test, y_test):
    """
    Mengevaluasi model klasifikasi.
    """

    y_pred = model.predict(X_test)

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(
            y_test, y_pred, average="weighted", zero_division=0
        ),
        "recall": recall_score(
            y_test, y_pred, average="weighted", zero_division=0
        ),
        "f1_score": f1_score(
            y_test, y_pred, average="weighted", zero_division=0
        ),
        "confusion_matrix": confusion_matrix(
            y_test, y_pred
        ).tolist()
    }

    return metrics


def evaluate_regression(model, X_test, y_test):
    """
    Mengevaluasi model regresi.
    """

    y_pred = model.predict(X_test)

    metrics = {
        "mae": mean_absolute_error(y_test, y_pred),
        "mse": mean_squared_error(y_test, y_pred),
        "rmse": np.sqrt(mean_squared_error(y_test, y_pred)),
        "r2_score": r2_score(y_test, y_pred)
    }

    return metrics

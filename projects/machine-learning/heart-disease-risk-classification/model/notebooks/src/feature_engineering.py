import numpy as np
import pandas as pd
from typing import Callable, Dict, List, Optional, Tuple,Any

def create_features_engineering(
    df: pd.DataFrame,
    interactions: Optional[List[Tuple[str, str, str]]] = None,
    ratios: Optional[List[Tuple[str, str, str]]] = None,
    date_cols: Optional[List[str]] = None,
    group_aggs: Optional[List[Dict[str, str]]] = None,
    custom_funcs: Optional[Dict[str, Callable[[pd.DataFrame], pd.Series]]] = None,
    eps: float = 1e-8,
) -> pd.DataFrame:
    """
    Membuat fitur baru secara fleksibel untuk regresi, klasifikasi, maupun clustering.

    Parameters:
    - interactions: List tuple (col_a, col_b, operasi) -> operasi: 'add', 'sub', 'mul'
    - ratios: List tuple (pembilang, penyebut, nama_fitur_baru)
    - date_cols: List kolom bertipe datetime untuk diekstrak komponen waktunya
    - group_aggs: List dict, contoh: [{'group_col': 'kategori', 'target_col': 'harga', 'agg': 'mean'}]
    - custom_funcs: Dict {nama_kolom_baru: fungsi_terdefinisi}
    """
    data = df.copy()

    if interactions:
        for col_a, col_b, op in interactions:
            if op == "add":
                data[f"{col_a}_plus_{col_b}"] = data[col_a] + data[col_b]
            elif op == "sub":
                data[f"{col_a}_minus_{col_b}"] = data[col_a] - data[col_b]
            elif op == "mul":
                data[f"{col_a}_mul_{col_b}"] = data[col_a] * data[col_b]
            else:
                raise ValueError(f"Operasi '{op}' tidak didukung. Gunakan 'add', 'sub', atau 'mul'.")

    if ratios:
        for num_col, den_col, new_name in ratios:
            data[new_name] = data[num_col] / (data[den_col] + eps)

    if date_cols:
        for col in date_cols:
            dt_series = pd.to_datetime(data[col])
            data[f"{col}_year"] = dt_series.dt.year
            data[f"{col}_month"] = dt_series.dt.month
            data[f"{col}_day"] = dt_series.dt.day
            data[f"{col}_dayofweek"] = dt_series.dt.dayofweek
            data[f"{col}_is_weekend"] = (dt_series.dt.dayofweek >= 5).astype(int)

    # 4. Agregasi berbasis grup (sangat efektif untuk tabular & clustering perilaku)
    if group_aggs:
        for spec in group_aggs:
            g_col = spec["group_col"]
            t_col = spec["target_col"]
            agg_func = spec["agg"]
            new_col_name = spec.get("new_col", f"{t_col}_{agg_func}_by_{g_col}")
            data[new_col_name] = data.groupby(g_col)[t_col].transform(agg_func)

    # 5. Fungsi kustom berbasis pengetahuan domain
    if custom_funcs:
        for new_col, func in custom_funcs.items():
            data[new_col] = func(data)

    return data


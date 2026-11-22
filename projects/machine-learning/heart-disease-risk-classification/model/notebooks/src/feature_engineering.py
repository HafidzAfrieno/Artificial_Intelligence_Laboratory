import numpy as np
import pandas as pd
from typing import Callable, Dict, List, Optional, Tuple,Any
from sklearn.preprocessing import OneHotEncoder, TargetEncoder
from sklearn.preprocessing import PowerTransformer, QuantileTransformer
from sklearn.preprocessing import (MaxAbsScaler,MinMaxScaler,Normalizer,RobustScaler,StandardScaler)

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

    if group_aggs:
        for spec in group_aggs:
            g_col = spec["group_col"]
            t_col = spec["target_col"]
            agg_func = spec["agg"]
            new_col_name = spec.get("new_col", f"{t_col}_{agg_func}_by_{g_col}")
            data[new_col_name] = data.groupby(g_col)[t_col].transform(agg_func)

    if custom_funcs:
        for new_col, func in custom_funcs.items():
            data[new_col] = func(data)

    return data


def transform_features_engineering(
    df: pd.DataFrame,
    log_cols: Optional[List[str]] = None,
    power_cols: Optional[List[str]] = None,
    power_method: str = "yeo-johnson",
    quantile_cols: Optional[List[str]] = None,
    quantile_output: str = "normal",
    clip_quantiles: Optional[Dict[str, Tuple[float, float]]] = None,
    fitted_transformers: Optional[Dict[str, Any]] = None,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Melakukan transformasi distribusi fitur dan penanganan outlier secara stateful.

    Parameters:
    - log_cols: Kolom yang akan ditransformasi dengan np.log1p (khusus nilai >= 0)
    - power_cols: Kolom untuk PowerTransformer ('yeo-johnson' atau 'box-cox')
    - quantile_cols: Kolom untuk QuantileTransformer ('normal' atau 'uniform')
    - clip_quantiles: Dict {nama_kolom: (batas_bawah_kuantil, batas_atas_kuantil)}, misal {'gaji': (0.01, 0.99)}
    - fitted_transformers: Objek hasil fit dari data latih (isi None saat fase fit/train)
    """
    data = df.copy()
    is_fitting = fitted_transformers is None
    transformers = {} if is_fitting else fitted_transformers

    # 1. Winsorization / Outlier Clipping berbasis kuantil
    if clip_quantiles:
        if is_fitting:
            transformers["clip_bounds"] = {}
        for col, (low_q, high_q) in clip_quantiles.items():
            if is_fitting:
                low_val = data[col].quantile(low_q)
                high_val = data[col].quantile(high_q)
                transformers["clip_bounds"][col] = (low_val, high_val)
            else:
                low_val, high_val = transformers["clip_bounds"][col]
            data[col] = data[col].clip(lower=low_val, upper=high_val)

    # 2. Log1p Transformation (deterministik, tidak butuh state)
    if log_cols:
        for col in log_cols:
            if (data[col] < 0).any():
                raise ValueError(f"Kolom '{col}' memiliki nilai negatif; gunakan power_cols ('yeo-johnson').")
            data[col] = np.log1p(data[col])

    # 3. Power Transformation (Box-Cox / Yeo-Johnson)
    if power_cols:
        if is_fitting:
            pt = PowerTransformer(method=power_method, standardize=False)
            data[power_cols] = pt.fit_transform(data[power_cols])
            transformers["power"] = pt
        else:
            data[power_cols] = transformers["power"].transform(data[power_cols])

    # 4. Quantile Transformation (memaksa distribusi ke Normal atau Uniform)
    if quantile_cols:
        if is_fitting:
            qt = QuantileTransformer(output_distribution=quantile_output, random_state=42)
            data[quantile_cols] = qt.fit_transform(data[quantile_cols])
            transformers["quantile"] = qt
        else:
            data[quantile_cols] = transformers["quantile"].transform(data[quantile_cols])

    return data, transformers

def encode_features_engineering(
    df: pd.DataFrame,
    onehot_cols: Optional[List[str]] = None,
    ordinal_mappings: Optional[Dict[str, Dict[Any, int]]] = None,
    frequency_cols: Optional[List[str]] = None,
    target_encode_cols: Optional[List[str]] = None,
    target_series: Optional[pd.Series] = None,
    target_type: str = "auto",
    drop_first: bool = False,
    fitted_encoders: Optional[Dict[str, Any]] = None,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Mengubah fitur kategorikal menjadi numerik dengan berbagai strategi dalam satu fungsi.

    Parameters:
    - onehot_cols: Kolom nominal untuk OneHotEncoder
    - ordinal_mappings: Dict {kolom: {kategori: urutan_angka}}, misal {'pendidikan': {'SMA': 1, 'S1': 2, 'S2': 3}}
    - frequency_cols: Kolom yang dikodekan berdasarkan proporsi kemunculannya (aman untuk clustering)
    - target_encode_cols: Kolom kardinalitas tinggi untuk TargetEncoder (butuh target_series saat fit)
    - target_type: 'continuous' (regresi), 'binary'/'multiclass' (klasifikasi), atau 'auto'
    - fitted_encoders: Objek encoder hasil fit dari data latih
    """
    data = df.copy()
    is_fitting = fitted_encoders is None
    encoders = {} if is_fitting else fitted_encoders

    # 1. Ordinal Encoding (berbasis pemetaan eksplisit)
    if ordinal_mappings:
        for col, mapping in ordinal_mappings.items():
            data[col] = data[col].map(mapping).fillna(-1).astype(int)

    # 2. Frequency Encoding
    if frequency_cols:
        if is_fitting:
            encoders["frequency"] = {}
        for col in frequency_cols:
            if is_fitting:
                freq_map = data[col].value_counts(normalize=True).to_dict()
                encoders["frequency"][col] = freq_map
            else:
                freq_map = encoders["frequency"][col]
            data[col] = data[col].map(freq_map).fillna(0.0)

    # 3. Target Encoding (khusus Regresi & Klasifikasi)
    if target_encode_cols:
        if is_fitting:
            if target_series is None:
                raise ValueError("target_series wajib diisi saat fitting TargetEncoder.")
            te = TargetEncoder(target_type=target_type, random_state=42)
            data[target_encode_cols] = te.fit_transform(data[target_encode_cols], target_series)
            encoders["target"] = te
        else:
            data[target_encode_cols] = encoders["target"].transform(data[target_encode_cols])

    # 4. One-Hot Encoding
    if onehot_cols:
        if is_fitting:
            ohe = OneHotEncoder(
                drop="first" if drop_first else None,
                sparse_output=False,
                handle_unknown="ignore",
            )
            encoded_arr = ohe.fit_transform(data[onehot_cols])
            encoders["onehot"] = ohe
        else:
            ohe = encoders["onehot"]
            encoded_arr = ohe.transform(data[onehot_cols])

        encoded_cols = ohe.get_feature_names_out(onehot_cols)
        encoded_df = pd.DataFrame(encoded_arr, columns=encoded_cols, index=data.index)
        data = pd.concat([data.drop(columns=onehot_cols), encoded_df], axis=1)

    return data, encoders

def scale_features_engineering(
    df: pd.DataFrame,
    cols: Optional[List[str]] = None,
    method: str = "standard",
    fitted_scaler: Optional[Any] = None,
    **scaler_kwargs: Any,
) -> Tuple[pd.DataFrame, Optional[Any]]:
    """
    Menyamakan skala fitur numerik secara fleksibel.

    Parameters:
    - cols: Daftar kolom yang akan di-scale. Jika None, otomatis memilih semua kolom numerik.
    - method: Pilihan scaler -> 'standard', 'minmax', 'robust', 'maxabs', 'normalize', atau 'none'
    - fitted_scaler: Scaler hasil fit dari data latih
    - scaler_kwargs: Argumen tambahan langsung ke scikit-learn scaler (misal feature_range=(0, 1))
    """
    data = df.copy()
    method_clean = method.lower()

    if method_clean == "none":
        return data, None

    target_cols = cols if cols is not None else data.select_dtypes(include=[np.number]).columns.tolist()

    scaler_registry = {
        "standard": StandardScaler,
        "minmax": MinMaxScaler,
        "robust": RobustScaler,
        "maxabs": MaxAbsScaler,
        "normalize": Normalizer,
    }

    if method_clean not in scaler_registry:
        raise ValueError(f"Metode '{method}' tidak dikenali. Pilih dari: {list(scaler_registry.keys())} atau 'none'.")

    if fitted_scaler is None:
        scaler = scaler_registry[method_clean](**scaler_kwargs)
        data[target_cols] = scaler.fit_transform(data[target_cols])
    else:
        scaler = fitted_scaler
        data[target_cols] = scaler.transform(data[target_cols])

    return data, scaler

#pokoknya besok masih perlu diperbaiki lo yaaa!!
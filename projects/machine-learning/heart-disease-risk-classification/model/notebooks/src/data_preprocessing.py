import pandas as pd
import numpy as np
import seaborn as sns
import io
from IPython.display import display
from src.exploratory_data_analysis import separate_feature_types
from typing import Dict, List, Literal, Optional, Tuple, Union
from pathlib import Path
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")

def analyze_missing_values(df: pd.DataFrame, plot: bool = True) -> pd.DataFrame:
    """ Menganalisis jumlah dan persentase nilai kosong (NaN/Null) pada setiap kolom. """

    total_missing = df.isnull().sum()
    percent_missing = (total_missing / len(df)) * 100

    missing_df = pd.DataFrame({
        "Jumlah_Kosong": total_missing,
        "Persentase (%)": percent_missing.round(2),
        "Tipe_Data": df.dtypes
    })

    missing_filtered = missing_df[missing_df["Jumlah_Kosong"] > 0].sort_values( by="Persentase (%)", ascending=False)
    if missing_filtered.empty:
        print("Tidak ditemukan missing value pada dataset.\n")
        return missing_filtered

    display(missing_filtered)

    if plot:
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        sns.barplot(
            x=missing_filtered["Persentase (%)"],
            y=missing_filtered.index,
            hue=missing_filtered.index,
            palette="Reds_r",
            legend=False,
            ax=axes[0]
        )
        axes[0].set_title("Persentase Missing Value per Kolom")
        axes[0].set_xlabel("Persentase (%)")
        axes[0].set_ylabel("Kolom")

        # Heatmap sebaran missing value
        sns.heatmap(df[missing_filtered.index].isnull(), cbar=False, cmap="viridis", ax=axes[1])
        axes[1].set_title("Peta Sebaran Missing Value (Kuning = Kosong)")
        axes[1].set_ylabel("Index Baris")

        plt.tight_layout()
        plt.show()

    return missing_filtered


def analyze_duplicates(df: pd.DataFrame, subset_cols: list = None, plot: bool = True) -> pd.DataFrame:
    """Menganalisis duplikasi baris secara keseluruhan maupun berdasarkan kolom kunci (subset)."""
    total_rows = len(df)
    exact_dups = df.duplicated(keep=False)
    num_exact_dups = df.duplicated(keep="first").sum()

    print(f"Total Baris Dataset        : {total_rows}")
    print(f"Duplikat Persis (Full Row) : {num_exact_dups} baris ({(num_exact_dups/total_rows)*100:.2f}%)")

    if subset_cols:
        subset_dups = df.duplicated(subset=subset_cols, keep="first").sum()
        print(f"Duplikat Kolom {subset_cols} : {subset_dups} baris ({(subset_dups/total_rows)*100:.2f}%)")

    dup_records = df[exact_dups]
    if not dup_records.empty:
        print("\nContoh Data Duplikat (maksimal 5 baris pertama):")
        display(dup_records.head())
    else:
        print("Tidak ditemukan baris duplikat persis.\n")

    if plot:
        unique_count = total_rows - num_exact_dups
        plt.figure(figsize=(6, 4))
        sns.barplot(
            x=["Data Unik", "Data Duplikat"],
            y=[unique_count, num_exact_dups],
            hue=["Data Unik", "Data Duplikat"],
            palette=["#2ecc71", "#e74c3c"],
            legend=False
        )
        plt.title("Perbandingan Jumlah Data Unik vs Duplikat")
        plt.ylabel("Jumlah Baris")
        for i, val in enumerate([unique_count, num_exact_dups]):
            plt.text(i, val + (total_rows * 0.01), str(val), ha="center", fontweight="bold")
        plt.tight_layout()
        plt.show()

    return dup_records

def analyze_outliers(df: pd.DataFrame,plot: bool = True,exclude_cols: Optional[list[str]] = None,cat_threshold: int = 10,force_cat: Optional[list[str]] = None,
                     force_num: Optional[list[str]] = None,verbose: bool = False,) -> pd.DataFrame:
    """Mengidentifikasi outlier pada kolom numerik menggunakan metode IQR (Interquartile Range)."""

    num_cols, _ = separate_feature_types(df=df,exclude_cols=exclude_cols,cat_threshold=cat_threshold,force_cat=force_cat,force_num=force_num,verbose=verbose,)
    if not num_cols:
        print("Tidak ada kolom numerik untuk dianalisis.\n")
        return pd.DataFrame()

    outlier_summary = []

    for col in num_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        count_outliers = len(outliers)
        pct_outliers = (count_outliers / len(df)) * 100

        outlier_summary.append({
            "Kolom": col,
            "Batas_Bawah": round(lower_bound, 2),
            "Batas_Atas": round(upper_bound, 2),
            "Jumlah_Outlier": count_outliers,
            "Persentase (%)": round(pct_outliers, 2),
            "Min_Aktual": df[col].min(),
            "Max_Aktual": df[col].max()
        })

    outlier_df = pd.DataFrame(outlier_summary).set_index("Kolom")
    display(outlier_df)

    if plot:
        max_cols = 4
        total_plots = len(num_cols)
        n_rows = (total_plots + max_cols - 1) // max_cols
        fig, axes = plt.subplots(n_rows, max_cols, figsize=(4 * max_cols, 4 * n_rows))
        axes = np.array(axes).flatten()
        for i, col in enumerate(num_cols):
            sns.boxplot(y=df[col], ax=axes[i], color="#3498db")
            axes[i].set_title(f"Boxplot: {col}")
            axes[i].set_ylabel("Nilai")
        for j in range(total_plots, len(axes)):
            axes[j].set_visible(False)
        plt.tight_layout()
        plt.show()

    return outlier_df

def analyze_inconsistency(df: pd.DataFrame,max_unique_display: int = 15,exclude_cols: Optional[list[str]] = None,cat_threshold: int = 10,force_cat: Optional[list[str]] = None,
                          force_num: Optional[list[str]] = None,verbose: bool = False,) -> dict:
    """
    Mendeteksi ketidakkonsistenan data:
    1. Perbedaan huruf besar/kecil (case sensitivity) & spasi berlebih pada kolom teks.
    2. Kolom bertipe object yang seharusnya numerik/tanggal.
    3. Nilai tidak logis (misalnya nilai negatif pada kolom numerik).
    """
    report = {}
    found_inconsistency = False
    cat_cols = df.select_dtypes(include=["object", "string", "category"]).columns.tolist()

    for col in cat_cols:
        series_clean = df[col].dropna().astype(str)
        unique_raw = series_clean.unique()
        unique_normalized = series_clean.str.strip().str.lower().unique()

        has_whitespace = any(val != val.strip() for val in unique_raw)
        has_case_mismatch = len(unique_raw) != len(unique_normalized)
        numeric_convertible = pd.to_numeric(series_clean, errors="coerce").notnull().mean()

        issues = []
        if has_whitespace:
            issues.append("Terdapat spasi berlebih di awal/akhir teks (leading/trailing space)")
        if has_case_mismatch:
            issues.append(f"Inkonsistensi huruf kapital ({len(unique_raw)} variasi vs {len(unique_normalized)} nilai unik)")
        if 0.5 < numeric_convertible < 1.0:
            issues.append("Campuran teks dan angka dalam satu kolom")
        elif numeric_convertible == 1.0:
            issues.append("Seluruh nilai berupa angka tetapi tersimpan sebagai teks (object)")

        if issues or len(unique_raw) <= max_unique_display:
            print(f"Kolom '{col}' (Tipe: {df[col].dtype}):")
            if issues:
                for issue in issues:
                    print(f"  [!] Masalah: {issue}")
            if len(unique_raw) <= max_unique_display:
                print(f"  [-] Nilai unik ({len(unique_raw)}): {list(unique_raw)}")
            print()

        report[col] = {
            "issues": issues,
            "unique_values": list(unique_raw[:max_unique_display])
        }

    num_cols, _ = separate_feature_types(df=df,exclude_cols=exclude_cols,cat_threshold=cat_threshold,force_cat=force_cat,force_num=force_num,verbose=verbose,)
    for col in num_cols:
        neg_count = (df[col] < 0).sum()
        if neg_count > 0:
            found_inconsistency = True
            print(f"Kolom Numerik '{col}':")
            print(f"  [!] Ditemukan {neg_count} nilai negatif (Min: {df[col].min()}). Periksa apakah valid.\n")
            report[col] = {"negative_values_count": int(neg_count)}

    if not found_inconsistency:
        print("tidak ditemukan masalah, namun perlu di cek ulang lagi\n")

    return report


def convert_data_types(df: pd.DataFrame,dtype_map: Optional[Dict[str, str]] = None,date_cols: Optional[List[str]] = None,verbose: bool = True) -> pd.DataFrame:
    """Memperbaiki tipe data kolom (numerik, kategorikal, dan datetime)."""
    data = df.copy()
    converted = []

    if date_cols:
        for col in date_cols:
            if col in data.columns:
                data[col] = pd.to_datetime(data[col], errors='coerce')
                converted.append(f"{col} -> datetime64")

    if dtype_map:
        for col, target_type in dtype_map.items():
            if col in data.columns:
                if 'int' in target_type or 'float' in target_type:
                    if data[col].dtype == 'object':
                        data[col] = data[col].astype(str).str.replace(r'[^\d.-]', '', regex=True)
                    data[col] = pd.to_numeric(data[col], errors='coerce')
                    if 'int' in target_type:
                        data[col] = data[col].astype('Int64')
                else:
                    data[col] = data[col].astype(target_type)
                converted.append(f"{col} -> {target_type}")

    if verbose:
        print(f"[Type Conversion] Kolom dikonversi: {converted if converted else 'Tidak ada'}")

    return data

def handle_duplicates(df: pd.DataFrame,subset: Optional[List[str]] = None,keep: Union[str, bool] = 'first',verbose: bool = True) -> pd.DataFrame:
    """Menghapus data duplikat berdasarkan seluruh kolom atau subset kolom tertentu."""
    data = df.copy()
    initial_rows = len(data)
    
    data = data.drop_duplicates(subset=subset, keep=keep).reset_index(drop=True)
    removed = initial_rows - len(data)

    if verbose:
        print(f"[Duplicate Handling] Dihapus {removed} baris duplikat (Sisa: {len(data)} baris)")

    return data

def handle_missing_values(df: pd.DataFrame,strategy: Optional[Dict[str, Union[str, int, float]]] = None,drop_col_thresh: float = 0.51,skew_thresh: float = 0.5,exclude_cols: Optional[list[str]] = None,cat_threshold: int = 10,force_cat: Optional[list[str]] = None,
                           force_num: Optional[list[str]] = None, verbose: bool = True) -> pd.DataFrame:
    """
    Menangani missing values dengan parameter yang selaras dengan separate_feature_types():
    1. Hapus kolom (numerik & kategori) jika missing > 51% (0.51).
    2. Fitur numerik (num_cols): Mean jika distribusi normal (|skew| <= 0.5), Median jika tidak normal.
    3. Fitur kategori (cat_cols, termasuk encoded-categorical): Mode.
    """
    data = df.copy()
    strategy = strategy or {}
    logs = []
    total_rows = len(data)

    if total_rows == 0:
        return data

    num_cols, cat_cols = separate_feature_types(df=data,exclude_cols=exclude_cols,cat_threshold=cat_threshold,force_cat=force_cat,force_num=force_num,verbose=verbose)
    num_cols_set = set(num_cols)
    cat_cols_set = set(cat_cols)
    exclude_set = set(exclude_cols or [])

    for col in list(data.columns):
        if col in exclude_set:
            continue

        missing_count = data[col].isna().sum()
        if missing_count == 0:
            continue

        missing_ratio = missing_count / total_rows

        if col not in strategy and missing_ratio > drop_col_thresh:
            data = data.drop(columns=[col])
            logs.append(
                f"{col}: kolom dihapus ({missing_ratio*100:.1f}% > {drop_col_thresh*100:.0f}% kosong)"
            )
            continue

        col_strategy = strategy.get(col)
        dist_note = ""

        # Aturan otomatis saat strategy=None
        if col_strategy is None:
            if col in num_cols_set:
                skew_val = data[col].skew()
                if pd.notna(skew_val) and abs(skew_val) <= skew_thresh:
                    col_strategy = 'mean'
                    dist_note = f" [numerik normal, skew={skew_val:.2f}]"
                else:
                    col_strategy = 'median'
                    skew_str = f"{skew_val:.2f}" if pd.notna(skew_val) else "N/A"
                    dist_note = f" [numerik tidak normal, skew={skew_str}]"
            elif col in cat_cols_set:
                col_strategy = 'mode'
                dist_note = " [kategori]"

        if col_strategy == 'drop':
            data = data.dropna(subset=[col]).reset_index(drop=True)
            logs.append(f"{col}: hapus {missing_count} baris")
        elif col_strategy == 'mean':
            val = data[col].mean()
            data[col] = data[col].astype('float64').fillna(val)
            logs.append(f"{col}: imputasi mean ({val:.2f}){dist_note}")
        elif col_strategy == 'median':
            val = data[col].median()
            data[col] = data[col].fillna(val)
            logs.append(f"{col}: imputasi median ({val:.2f}){dist_note}")
        elif col_strategy == 'mode':
            mode_series = data[col].mode()
            val = mode_series[0] if not mode_series.empty else "Unknown"
            data[col] = data[col].fillna(val)
            logs.append(f"{col}: imputasi mode ({val}){dist_note}")
        else:
            data[col] = data[col].fillna(col_strategy)
            logs.append(f"{col}: imputasi konstan ({col_strategy})")

    if verbose:
        if logs:
            print("[Missing Values]")
            for log in logs:
                print(f"  - {log}")
        else:
            print("[Missing Values] Tidak ada missing value.")

    return data

# besok menganalisa fungsi handle_outliers

def handle_outliers( df: pd.DataFrame,cols: List[str],method: str = 'iqr',action: str = 'cap',factor: float = 1.5,custom_bounds: Optional[Dict[str, Tuple[Optional[float], Optional[float]]]] = None,verbose: bool = True) -> pd.DataFrame:
    """
    Menangani outlier berdasarkan statistik (IQR/Z-Score) atau aturan domain (custom_bounds).
    
    Parameters:
    -----------
    custom_bounds : dict, optional
        Batas manual sesuai konteks bisnis, misal: {'umur': (0, 100), 'harga': (1000, None)}
    """
    data = df.copy()
    custom_bounds = custom_bounds or {}
    logs = []

    for col in cols:
        if col not in data.columns or not pd.api.types.is_numeric_dtype(data[col]):
            continue

        if col in custom_bounds:
            lower_bound, upper_bound = custom_bounds[col]
            lower_bound = lower_bound if lower_bound is not None else data[col].min()
            upper_bound = upper_bound if upper_bound is not None else data[col].max()
        elif method == 'iqr':
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - (factor * IQR)
            upper_bound = Q3 + (factor * IQR)
        elif method == 'zscore':
            mean = data[col].mean()
            std = data[col].std()
            lower_bound = mean - (factor * std)
            upper_bound = mean + (factor * std)
        else:
            raise ValueError("Parameter 'method' harus 'iqr' atau 'zscore'.")

        outlier_mask = (data[col] < lower_bound) | (data[col] > upper_bound)
        num_outliers = outlier_mask.sum()

        if num_outliers > 0:
            if action == 'cap':
                data[col] = np.clip(data[col], lower_bound, upper_bound)
                logs.append(f"{col}: {num_outliers} nilai di-cap ke [{lower_bound:.2f}, {upper_bound:.2f}]")
            elif action == 'drop':
                data = data[~outlier_mask].reset_index(drop=True)
                logs.append(f"{col}: {num_outliers} baris outlier dihapus")
            else:
                raise ValueError("Parameter 'action' harus 'cap' atau 'drop'.")

    if verbose:
        print(f"[Outlier Handling] {', '.join(logs) if logs else 'Tidak ada outlier terdeteksi'}")

    return data

path_folder = "../data/processed"
def save_cleaned_data(df: pd.DataFrame,filename: str,folder_path: str = path_folder,file_format: Literal["csv", "excel", "json"] = "csv",verbose: bool = True) -> pd.DataFrame:
    """Menyimpan DataFrame bersih dengan akhiran '_CLEAN', melewati jika isi sama, atau memperbarui jika berubah."""
    target_dir = Path(folder_path)
    target_dir.mkdir(parents=True, exist_ok=True)

    base_name = Path(filename).stem
    if not base_name.endswith("_CLEAN"):
        base_name = f"{base_name}_CLEAN"

    fmt = file_format.lower().strip()

    if fmt == "csv":
        full_path = target_dir / f"{base_name}.csv"
        new_content = df.to_csv(index=False, lineterminator="\n")

        if full_path.exists():
            old_content = full_path.read_text(encoding="utf-8").replace("\r\n", "\n")
            if old_content == new_content:
                if verbose:
                    print("[Save Data] file yang sama sudah dibuat")
                return df
            full_path.write_text(new_content, encoding="utf-8")
            if verbose:
                print("[Save Data] file sudah di update")
        else:
            full_path.write_text(new_content, encoding="utf-8")
            if verbose:
                print(f"[Save Data] Berhasil disimpan ke: {full_path.resolve()}")

    elif fmt in ("excel", "xlsx"):
        full_path = target_dir / f"{base_name}.xlsx"

        if full_path.exists():
            buf = io.BytesIO()
            df.to_excel(buf, index=False)
            buf.seek(0)

            existing_df = pd.read_excel(full_path)
            new_df_parsed = pd.read_excel(buf)

            if existing_df.equals(new_df_parsed):
                if verbose:
                    print("[Save Data] file yang sama sudah dibuat")
                return df
            df.to_excel(full_path, index=False)
            if verbose:
                print("[Save Data] file sudah di update")
        else:
            df.to_excel(full_path, index=False)
            if verbose:
                print(f"[Save Data] Berhasil disimpan ke: {full_path.resolve()}")

    elif fmt == "json":
        full_path = target_dir / f"{base_name}.json"
        new_content = df.to_json(orient="records", indent=4, date_format="iso")

        if full_path.exists():
            old_content = full_path.read_text(encoding="utf-8").replace("\r\n", "\n")
            if old_content == new_content.replace("\r\n", "\n"):
                if verbose:
                    print("[Save Data] file yang sama sudah dibuat")
                return df
            full_path.write_text(new_content, encoding="utf-8")
            if verbose:
                print("[Save Data] file sudah di update")
        else:
            full_path.write_text(new_content, encoding="utf-8")
            if verbose:
                print(f"[Save Data] Berhasil disimpan ke: {full_path.resolve()}")

    else:
        raise ValueError("Format file tidak didukung. Pilih antara 'csv', 'excel', atau 'json'.")

    return df

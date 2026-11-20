from pathlib import Path
from typing import Any,Union,Literal
from IPython.display import display
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def load_data(file_path:Union[str,Path],**kwargs:Any)->pd.DataFrame:
    """Memuat data secara otomatis dari CSV, JSON, Excel, atau SQL."""
    result = None
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f'file tidak ditemukan : {path}')
    ext = path.suffix.lower()
    if ext == '.csv':
        result = pd.read_csv(path,**kwargs)
    elif exit == '.json':
        result = pd.read_json(path,**kwargs)
    elif exit in {".xlsx", ".xls", ".xlsm"}:
        result =  pd.read_excel(path,**kwargs)
    else:
        raise ValueError(f"Format '{ext}' tidak didukung. Gunakan CSV, JSON, atau Excel.")
    return result

def data_understanding(df:pd.DataFrame)->None:
    """Menampilkan overview struktur, dimensi, tipe data, dan statistik deskriptif dataset."""
    print("=== 1. SHAPE & DATA TYPES ===")
    print(f"Jumlah Baris  : {df.shape[0]}")
    print(f"Jumlah Kolom  : {df.shape[1]}")
    print(f"Baris Duplikat: {df.duplicated().sum()}\n")
    info_df = pd.DataFrame({
        "Dtype": df.dtypes,
        "Non-Null": df.notna().sum(),
        "Missing": df.isna().sum(),
        "Missing-Percentage": (df.isna().mean() * 100).round(2),
        "Unique": df.nunique(),
    })
    display(info_df)

    print("\n=== 2. DATASET OVERVIEW (5 BARIS PERTAMA) ===")
    display(df.head())

    print("\n=== 3. STATISTICAL SUMMARY ===")
    num_cols = df.select_dtypes(include='number')
    if not num_cols.empty:
        print("Fitur Numerik")
        display(num_cols.describe().T)
    cat_cols = df.select_dtypes(exclude='number')
    if not cat_cols.empty:
        print("Fitur Kategorikal / Non-Numerik:")
        display(cat_cols.describe().T)

def target_analysis(df: pd.DataFrame,target_col:str,task_type : Literal["auto", "classification", "regression"] = "auto",
                    plot: bool = True,palette: str = "Set2")->None:
    """Menganalisis distribusi variabel target untuk Supervised Learning."""
    if target_col not in df.columns:
        raise ValueError(f"Kolom target '{target_col}' tidak ditemukan dalam dataset.")
    
    target = df[target_col]
    missing_count = target.isna().sum()

    if task_type == 'auto':
        is_numeric = pd.api.types.is_numeric_dtype(target)
        is_bool = pd.api.types.is_bool_dtype(target)
        if is_bool or not is_numeric or target.nunique() <= 15:
            task_type = "classification"
        else:
            task_type = "regression"

    print(f"=== TARGET ANALYSIS: '{target_col}' ({task_type.upper()}) ===")
    print(f"Missing Values: {missing_count} ({target.isna().mean() * 100:.2f}%)\n")

    if task_type == "classification":
        counts = target.value_counts()
        dist_df = pd.DataFrame({
            "Count": counts,
            "Percentage (%)": (target.value_counts(normalize=True) * 100).round(2),
        })
        display(dist_df)

        if len(dist_df) > 1:
            imbalance_ratio = dist_df["Count"].max() / dist_df["Count"].min()
            print(f"Imbalance Ratio (Majority : Minority) = {imbalance_ratio:.2f} : 1")

        if plot:
            colors = sns.color_palette(palette, n_colors=len(counts))
            fig, axes = plt.subplots(1, 2, figsize=(13, 5))

            # 1. Bar Chart (Countplot)
            sns.countplot(data=df,x=target_col,hue=target_col,order=counts.index,palette=colors,legend=False,ax=axes[0],)
            for p in axes[0].patches:
                height = p.get_height()
                if height > 0:
                    pct = (height / len(target.dropna())) * 100
                    axes[0].annotate(f"{int(height)}\n({pct:.1f}%)",(p.get_x() + p.get_width() / 2.0, height),ha="center",va="bottom",fontsize=10,)
            axes[0].set_title(f"Jumlah Sampel per Kelas: {target_col}")
            axes[0].set_ylabel("Jumlah Sampel")

            # 2. Pie Chart
            axes[1].pie(counts.values,labels=counts.index, autopct="%1.1f%%",startangle=90,colors=colors,wedgeprops={"edgecolor": "white", "linewidth": 1.5},)
            axes[1].set_title(f"Proporsi Kelas: {target_col}")
            plt.tight_layout()
            plt.show()

    elif task_type == "regression":
        stats_df = target.describe().to_frame().T
        stats_df["skewness"] = target.skew()
        stats_df["kurtosis"] = target.kurt()
        display(stats_df.round(4))
        if plot:
            fig, axes = plt.subplots(1, 2, figsize=(12, 4))
            sns.histplot(target.dropna(), kde=True, ax=axes[0])
            axes[0].set_title(f"Histogram & KDE: {target_col}")
            sns.boxplot(x=target.dropna(), ax=axes[1])
            axes[1].set_title(f"Boxplot Outlier: {target_col}")
            plt.tight_layout()
            plt.show()
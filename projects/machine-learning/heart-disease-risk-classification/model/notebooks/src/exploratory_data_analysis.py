from pathlib import Path
from typing import Any,Union,Literal,Optional
from IPython.display import display
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import math

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


def separate_feature_types(df: pd.DataFrame,exclude_cols: Optional[list[str]] = None,cat_threshold: int = 10,force_cat: Optional[list[str]] = None,
                           force_num: Optional[list[str]] = None,verbose: bool = True)->tuple[list[str],list[str]]:
    """Memisahkan fitur numerik dan kategorikal, termasuk mendeteksi fitur kategorikal yang sudah di-encoding menjadi angka (integer)."""
    exclude_set = set(exclude_cols or [])
    force_cat_set = set(force_cat or [])
    force_num_set = set(force_num or [])

    num_cols: list[str] = []
    cat_cols: list[str] = []
    detected_encoded: list[str] = []

    for col in df.columns:
        if col in exclude_set:
            continue

        if col in force_num_set:
            num_cols.append(col)
            continue
        if col in force_cat_set:
            cat_cols.append(col)
            continue
        series = df[col].dropna()
        if pd.api.types.is_bool_dtype(df[col]) or not pd.api.types.is_numeric_dtype(df[col]):
            cat_cols.append(col)
            continue
        n_unique = series.nunique()
        is_integer_values = (series % 1 == 0).all() if not series.empty else False

        if n_unique <= cat_threshold and is_integer_values:
            cat_cols.append(col)
            detected_encoded.append(col)
        else:
            num_cols.append(col)
    if verbose and detected_encoded:
        print(f"[Info] Fitur numerik terdeteksi sebagai encoded-categorical: {detected_encoded}")

    return num_cols, cat_cols


def univariate_analysis(df: pd.DataFrame,exclude_cols: Optional[list[str]] = None,cat_threshold: int = 10,force_cat: Optional[list[str]] = None,
                        force_num: Optional[list[str]] = None, max_cat_unique: int = 20,n_cols: int = 3,palette: str = "Set2",)->None:
    """Menganalisis distribusi setiap fitur secara individual (numerik & kategorikal)."""
    data = df.drop(columns=exclude_cols, errors="ignore") if exclude_cols else df.copy()
    num_cols,cat_cols = separate_feature_types(df=df,exclude_cols=exclude_cols,cat_threshold=cat_threshold,force_cat=force_cat,force_num=force_num)

    # 1. Analisis Numerik
    if num_cols:
        print(f"=== 1. UNIVARIATE NUMERICAL FEATURES ({len(num_cols)} Fitur) ===")
        num_summary = []
        for col in num_cols:
            series = data[col].dropna()
            q1, q3 = series.quantile(0.25), series.quantile(0.75)
            iqr = q3 - q1
            outliers = ((series < (q1 - 1.5 * iqr)) | (series > (q3 + 1.5 * iqr))).sum()
            num_summary.append({
                "Feature": col,
                "Mean": series.mean(),
                "Median": series.median(),
                "Std": series.std(),
                "Min": series.min(),
                "Max": series.max(),
                "Skewness": series.skew(),
                "Outliers (IQR)": outliers,
                "Outliers (%)": (outliers / len(series) * 100) if len(series) > 0 else 0,
            })
        display(pd.DataFrame(num_summary).set_index("Feature").round(3))

        # Grid Plot: Histogram + KDE
        n_rows = math.ceil(len(num_cols) / n_cols)
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 3.8 * n_rows))
        axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

        for idx, col in enumerate(num_cols):
            sns.histplot(data[col].dropna(), kde=True, ax=axes[idx], color="#2563EB")
            axes[idx].set_title(f"{col} (Skew: {data[col].skew():.2f})", fontsize=10)
            axes[idx].set_xlabel("")

        for idx in range(len(num_cols), len(axes)):
            axes[idx].set_visible(False)

        plt.suptitle("Distribusi Fitur Numerik (Histogram & KDE)", fontsize=13, y=1.02)
        plt.tight_layout()
        plt.show()

        # Grid Plot: Boxplot (Deteksi Outlier)
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 2.8 * n_rows))
        axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

        for idx, col in enumerate(num_cols):
            sns.boxplot(x=data[col].dropna(), ax=axes[idx], color="#60A5FA")
            axes[idx].set_title(f"Boxplot: {col}", fontsize=10)
            axes[idx].set_xlabel("")

        for idx in range(len(num_cols), len(axes)):
            axes[idx].set_visible(False)

        plt.suptitle("Deteksi Outlier Fitur Numerik (Boxplot)", fontsize=13, y=1.02)
        plt.tight_layout()
        plt.show()

        # 2. Analisis Kategorical
        if cat_cols:
            print(f"\n=== 2. UNIVARIATE CATEGORICAL FEATURES ({len(cat_cols)} Fitur) ===")
            cat_summary = []
            plot_cats = []

            for col in cat_cols:
                n_uniq = data[col].nunique(dropna=True)
                top_val = data[col].mode().iloc[0] if not data[col].mode().empty else None
                top_freq = (data[col] == top_val).sum() if top_val is not None else 0
                top_pct = (top_freq / len(data) * 100) if len(data) > 0 else 0
                is_plotted = n_uniq <= max_cat_unique

                cat_summary.append({
                    "Feature": col,
                    "Unique": n_uniq,
                    "Mode (Modus)": top_val,
                    "Mode Freq": top_freq,
                    "Mode (%)": top_pct,
                    "Plot Status": "Plotted" if is_plotted else f"Skipped (> {max_cat_unique})",
                })

                if is_plotted:
                    plot_cats.append(col)

            display(pd.DataFrame(cat_summary).set_index("Feature").round({"Mode (%)": 2}))

            if plot_cats:
                n_rows = math.ceil(len(plot_cats) / n_cols)
                fig, axes = plt.subplots(n_rows, n_cols, figsize=(5.5 * n_cols, 3.8 * n_rows))
                axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

                for idx, col in enumerate(plot_cats):
                    order = data[col].value_counts().index
                    colors = sns.color_palette(palette, n_colors=len(order))
                    sns.countplot(data=data,y=col,hue=col,order=order,palette=colors,legend=False,ax=axes[idx],)
                    axes[idx].set_title(f"Distribusi: {col}", fontsize=10)
                    axes[idx].set_ylabel("")

                for idx in range(len(plot_cats), len(axes)):
                    axes[idx].set_visible(False)

                plt.tight_layout()
                plt.show()

def bivariate_analysis(df: pd.DataFrame,target_col: Optional[str] = None,task_type: Literal["auto", "classification", "regression", "clustering"] = "auto",exclude_cols: Optional[list[str]] = None,
                       cat_threshold: int = 10,force_cat: Optional[list[str]] = None,force_num: Optional[list[str]] = None,n_cols: int = 3,palette: str = "Set2")->None:
    """Menganalisis hubungan dua variabel untuk Classification, Regression, atau Clustering."""
    if target_col and target_col not in df.columns:
        raise ValueError(f"Kolom target '{target_col}' tidak ditemukan dalam dataset.")
    if task_type == "auto":
        if target_col is None:
            task_type = "clustering"
        else:
            target = df[target_col]
            is_num = pd.api.types.is_numeric_dtype(target)
            is_bool = pd.api.types.is_bool_dtype(target)
            task_type = (
                "classification"
                if (is_bool or not is_num or target.nunique() <= 15)
                else "regression"
            )

    excl = list(exclude_cols or [])
    if target_col:
        excl.append(target_col)

    num_cols, cat_cols = separate_feature_types(
        df=df,
        exclude_cols=excl,
        cat_threshold=cat_threshold,
        force_cat=force_cat,
        force_num=force_num,
        verbose=False,
    )
    print(f"=== BIVARIATE ANALYSIS ({task_type.upper()}) ===")
    if task_type == "classification" and target_col:
        if num_cols:
            print(f"\n[1] Numerical Features vs '{target_col}' (Mean per Kelas)")
            display(df.groupby(target_col, observed=False)[num_cols].mean().T.round(3))

            n_rows = math.ceil(len(num_cols) / n_cols)
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 3.8 * n_rows))
            axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

            for idx, col in enumerate(num_cols):
                sns.boxplot(
                    data=df, x=target_col, y=col, hue=target_col,
                    palette=palette, legend=False, ax=axes[idx],
                )
                axes[idx].set_title(f"{col} vs {target_col}", fontsize=10)

            for idx in range(len(num_cols), len(axes)):
                axes[idx].set_visible(False)
            plt.tight_layout()
            plt.show()

        if cat_cols:
            print(f"\n[2] Categorical Features vs '{target_col}'")
            n_rows = math.ceil(len(cat_cols) / n_cols)
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(5.2 * n_cols, 3.8 * n_rows))
            axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

            for idx, col in enumerate(cat_cols):
                sns.countplot(data=df, x=col, hue=target_col, palette=palette, ax=axes[idx])
                axes[idx].set_title(f"{col} vs {target_col}", fontsize=10)
                axes[idx].tick_params(axis="x", rotation=25)

            for idx in range(len(cat_cols), len(axes)):
                axes[idx].set_visible(False)
            plt.tight_layout()
            plt.show()

    elif task_type == "regression" and target_col:
        if num_cols:
            print(f"\n[1] Numerical Features vs '{target_col}' (Korelasi)")
            corr_df = pd.DataFrame({
                "Pearson": [df[col].corr(df[target_col], method="pearson") for col in num_cols],
                "Spearman": [df[col].corr(df[target_col], method="spearman") for col in num_cols],
            }, index=num_cols).sort_values(by="Pearson", key=abs, ascending=False)
            display(corr_df.round(3))

            n_rows = math.ceil(len(num_cols) / n_cols)
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 3.8 * n_rows))
            axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

            for idx, col in enumerate(num_cols):
                sns.regplot(
                    data=df, x=col, y=target_col, ax=axes[idx],
                    scatter_kws={"alpha": 0.5, "color": "#2563EB"},
                    line_kws={"color": "#DC2626"},
                )
                r_val = corr_df.loc[col, "Pearson"]
                axes[idx].set_title(f"{col} vs {target_col} (r = {r_val:.2f})", fontsize=10)

            for idx in range(len(num_cols), len(axes)):
                axes[idx].set_visible(False)
            plt.tight_layout()
            plt.show()

        if cat_cols:
            print(f"\n[2] Categorical Features vs '{target_col}'")
            n_rows = math.ceil(len(cat_cols) / n_cols)
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 3.8 * n_rows))
            axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

            for idx, col in enumerate(cat_cols):
                sns.boxplot(
                    data=df, x=col, y=target_col, hue=col,
                    palette=palette, legend=False, ax=axes[idx],
                )
                axes[idx].set_title(f"{target_col} per {col}", fontsize=10)
                axes[idx].tick_params(axis="x", rotation=25)

            for idx in range(len(cat_cols), len(axes)):
                axes[idx].set_visible(False)
            plt.tight_layout()
            plt.show()

    elif task_type == "clustering":
        if len(num_cols) >= 2:
            print("\n[1] Top Pasangan Fitur Numerik Paling Berkorelasi")
            corr_matrix = df[num_cols].corr()
            pairs = (
                corr_matrix.where(
                    pd.DataFrame(
                        [[i < j for j in range(len(num_cols))] for i in range(len(num_cols))],
                        index=num_cols, columns=num_cols,
                    )
                )
                .stack()
                .reset_index()
            )
            pairs.columns = ["Feature 1", "Feature 2", "Correlation"]
            pairs["Abs_Corr"] = pairs["Correlation"].abs()
            top_pairs = pairs.sort_values(by="Abs_Corr", ascending=False).head(6)
            display(top_pairs[["Feature 1", "Feature 2", "Correlation"]].round(3))

            n_plots = len(top_pairs)
            n_rows = math.ceil(n_plots / n_cols)
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 3.8 * n_rows))
            axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

            for idx, (_, row) in enumerate(top_pairs.iterrows()):
                f1, f2, r_val = row["Feature 1"], row["Feature 2"], row["Correlation"]
                sns.scatterplot(data=df, x=f1, y=f2, alpha=0.6, color="#2563EB", ax=axes[idx])
                axes[idx].set_title(f"{f1} vs {f2} (r = {r_val:.2f})", fontsize=10)

            for idx in range(n_plots, len(axes)):
                axes[idx].set_visible(False)
            plt.tight_layout()
            plt.show()
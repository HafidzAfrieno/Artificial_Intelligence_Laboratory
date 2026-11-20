from pathlib import Path
from typing import Any,Union
import pandas as pd

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

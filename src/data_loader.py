"""
data_loader.py — carregamento do dataset CSEDM (ProgSnap2 v6)

Splits disponíveis:
  - All/  : semestre Fall-2019 (set–dez 2019), 506 estudantes; usar para EDA completa
  - Release/ : semestre Spring-2019 (fev–mai 2019), 329 estudantes; usar para comparação
               reproduzível com Shi et al. (2022) e Pankiewicz et al. (2025)

Cada split contém Train/ e Test/ com Data/MainTable.csv, early.csv, late.csv.
"""

from pathlib import Path
import pandas as pd

_SPLITS = {
    "all":             ("All/Data/MainTable.csv", None),
    "all_train":       ("Train/Data/MainTable.csv", "Train/early.csv"),
    "all_test":        ("Test/Data/MainTable.csv",  "Test/early.csv"),
    "release_train":   ("Release/Train/Data/MainTable.csv", "Release/Train/early.csv"),
    "release_test":    ("Release/Test/Data/MainTable.csv",  "Release/Test/early.csv"),
}


def load_main_table(split: str, data_root: Path | str) -> pd.DataFrame:
    """Carrega MainTable.csv do split especificado e normaliza tipos.

    Parameters
    ----------
    split : str
        Um de: 'all', 'all_train', 'all_test', 'release_train', 'release_test'.
    data_root : Path | str
        Raiz do dataset — diretório que contém All/, Release/, Train/, Test/.

    Returns
    -------
    pd.DataFrame
        MainTable com ServerTimestamp convertido para datetime e AssignmentID
        como inteiro (colunas extras de Release/ mantidas).

    Notes
    -----
    Release/Train correto-rate ≈ 23.70% (Shi et al. (2022) reporta 23.68% — margem
    de arredondamento esperada; benchmark de reprodutibilidade).
    """
    data_root = Path(data_root)
    if split not in _SPLITS:
        raise ValueError(f"split deve ser um de {list(_SPLITS)}; recebido: {split!r}")

    main_path, _ = _SPLITS[split]
    df = pd.read_csv(data_root / main_path)

    df["ServerTimestamp"] = pd.to_datetime(df["ServerTimestamp"], utc=True, errors="coerce")

    if "AssignmentID" in df.columns:
        df["AssignmentID"] = pd.to_numeric(df["AssignmentID"], errors="coerce").astype("Int64")

    if "ProblemID" in df.columns:
        df["ProblemID"] = pd.to_numeric(df["ProblemID"], errors="coerce").astype("Int64")

    return df


def load_labels(split: str, data_root: Path | str, which: str = "early") -> pd.DataFrame:
    """Carrega early.csv ou late.csv do split especificado.

    Parameters
    ----------
    split : str
        Um de: 'all_train', 'all_test', 'release_train', 'release_test'.
        'all' não possui early/late no nível raiz.
    data_root : Path | str
        Raiz do dataset.
    which : str
        'early' ou 'late'.

    Returns
    -------
    pd.DataFrame
        DataFrame com colunas SubjectID, AssignmentID e Label (0/1).
    """
    data_root = Path(data_root)
    if split not in _SPLITS or _SPLITS[split][1] is None:
        raise ValueError(f"Labels não disponíveis para split={split!r}. Use 'all_train', 'all_test', 'release_train' ou 'release_test'.")

    _, label_base = _SPLITS[split]
    label_path = data_root / label_base.replace("early.csv", f"{which}.csv")

    if not label_path.exists():
        raise FileNotFoundError(f"Arquivo de labels não encontrado: {label_path}")

    return pd.read_csv(label_path)

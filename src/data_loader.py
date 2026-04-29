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


def filter_for_bkt_dkt(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra eventos para BKT e DKT: apenas Run.Program com label binária.

    Parameters
    ----------
    df : pd.DataFrame
        MainTable carregada via load_main_table.

    Returns
    -------
    pd.DataFrame
        Subset com apenas EventType=='Run.Program'; coluna 'correct' adicionada
        (1 se Score==1.0, 0 caso contrário). Índice resetado.

    Notes
    -----
    BKT e DKT usam apenas tentativas de execução (Run.Program). Compile.Error não
    entra na sequência porque esses modelos não processam informação do código-fonte.
    """
    filtered = df[df["EventType"] == "Run.Program"].copy()
    assert filtered["EventType"].nunique() == 1, "EventType inesperado passou pelo filtro BKT/DKT"
    assert set(filtered["EventType"].unique()) == {"Run.Program"}, "Filtro BKT/DKT corrompido"
    filtered["correct"] = (filtered["Score"] == 1.0).astype(int)
    return filtered.reset_index(drop=True)


def filter_for_code_dkt(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra eventos para Code-DKT: Run.Program e Compile.Error com label binária.

    Parameters
    ----------
    df : pd.DataFrame
        MainTable carregada via load_main_table.

    Returns
    -------
    pd.DataFrame
        Subset com EventType em {'Run.Program', 'Compile.Error'}; coluna 'correct'
        adicionada (1 se Run.Program com Score==1.0, 0 em todos os outros casos).
        Ordenado por (SubjectID, AssignmentID, ServerTimestamp). Índice resetado.

    Notes
    -----
    Code-DKT inclui Compile.Error como correct=0 para capturar a evolução
    incremental do código do estudante (Shi et al., 2022; Pankiewicz et al., 2025).
    srcML extrai features AST mesmo de código não-compilável, viabilizando este protocolo.
    """
    allowed = {"Run.Program", "Compile.Error"}
    filtered = df[df["EventType"].isin(allowed)].copy()
    assert set(filtered["EventType"].unique()).issubset(allowed), "EventType inesperado passou pelo filtro Code-DKT"
    filtered["correct"] = (
        (filtered["EventType"] == "Run.Program") & (filtered["Score"] == 1.0)
    ).astype(int)
    filtered = filtered.sort_values(["SubjectID", "AssignmentID", "ServerTimestamp"])
    return filtered.reset_index(drop=True)


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

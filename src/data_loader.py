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


def build_sequences(df: pd.DataFrame, assignment_id: int) -> list[dict]:
    """Constrói sequências KT por estudante para um assignment específico.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame filtrado via filter_for_bkt_dkt ou filter_for_code_dkt.
        Deve conter as colunas: SubjectID, AssignmentID, ProblemID,
        ServerTimestamp, EventType, correct, CodeStateID.
    assignment_id : int
        ID do assignment a processar (coluna AssignmentID).

    Returns
    -------
    list[dict]
        Lista de dicionários, um por estudante que participou do assignment.
        Cada dicionário contém:
        - 'subject_id'    (str)          — identificador do estudante
        - 'assignment_id' (int)          — ID do assignment
        - 'events'        (pd.DataFrame) — eventos do estudante ordenados por
          ServerTimestamp, com todas as colunas do df de entrada mais
          'is_first_attempt' (bool): True para a primeira ocorrência de cada
          ProblemID na sequência cronológica do estudante (usada para calcular
          first-attempt AUC conforme Shi et al., 2022).

    Notes
    -----
    is_first_attempt marca a primeira tentativa do estudante em cada problema
    dentro do assignment — independentemente do EventType. Para Code-DKT, mesmo
    um Compile.Error pode ser a primeira tentativa em um problema (o estudante
    nunca compilou com sucesso antes). Para BKT/DKT, is_first_attempt marca
    o primeiro Run.Program por problema.

    A ordenação cronológica é garantida por ServerTimestamp (UTC) antes de
    marcar is_first_attempt — eventos com mesmo timestamp são desambiguados
    pela ordem original do DataFrame.
    """
    assign_df = df[df["AssignmentID"] == assignment_id].copy()

    # Ordenar cronologicamente antes de marcar a primeira tentativa
    assign_df = assign_df.sort_values(
        ["SubjectID", "ServerTimestamp"], kind="stable"
    )

    # is_first_attempt: primeira ocorrência de (SubjectID, ProblemID) no tempo
    assign_df["is_first_attempt"] = ~assign_df.duplicated(
        subset=["SubjectID", "ProblemID"], keep="first"
    )

    sequences = []
    for subject_id, student_df in assign_df.groupby("SubjectID", sort=True):
        sequences.append({
            "subject_id": subject_id,
            "assignment_id": int(assignment_id),
            "events": student_df.reset_index(drop=True),
        })

    return sequences


def truncate_sequences(sequences: list[dict], max_len: int = 50) -> list[dict]:
    """Trunca sequências KT para as últimas max_len tentativas por estudante.

    Parameters
    ----------
    sequences : list[dict]
        Saída de build_sequences — lista de dicionários com chaves
        'subject_id', 'assignment_id', 'events'.
    max_len : int
        Comprimento máximo da janela. Padrão: 50, conforme Shi et al. (2022).

    Returns
    -------
    list[dict]
        Lista de dicionários com as mesmas chaves; sequências longas são truncadas
        para os últimos max_len eventos (os mais recentes cronologicamente).
        A flag 'is_first_attempt' é recalculada dentro da janela truncada:
        True para a primeira ocorrência de cada ProblemID na janela resultante.

    Notes
    -----
    A truncagem mantém os eventos MAIS RECENTES (tail) porque captura o estado
    de conhecimento mais próximo do momento de avaliação. Recalcular
    is_first_attempt é necessário: a primeira tentativa na janela truncada pode
    ser diferente da primeira tentativa na sequência completa, caso os eventos
    iniciais tenham sido removidos.
    """
    truncated = []
    for seq in sequences:
        events = seq["events"]
        if len(events) > max_len:
            events = events.iloc[-max_len:].copy()
            events["is_first_attempt"] = ~events.duplicated(
                subset=["ProblemID"], keep="first"
            )
            events = events.reset_index(drop=True)
        truncated.append({
            "subject_id": seq["subject_id"],
            "assignment_id": seq["assignment_id"],
            "events": events,
        })
    return truncated


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

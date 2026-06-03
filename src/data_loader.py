#data_loader.py — carregamento do dataset CSEDM (ProgSnap2 v6)

from pathlib import Path
import pandas as pd

_SPLITS = {}


def load_main_table(split: str, data_root: Path | str) -> pd.DataFrame:
    #Carrega MainTable.csv do split especificado e normaliza tipos.

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
    #Filtra eventos para BKT e DKT: apenas Run.Program com label binária.

    filtered = df[df["EventType"] == "Run.Program"].copy()
    assert filtered["EventType"].nunique() == 1, "EventType inesperado passou pelo filtro BKT/DKT"
    assert set(filtered["EventType"].unique()) == {"Run.Program"}, "Filtro BKT/DKT corrompido"
    filtered["correct"] = (filtered["Score"] == 1.0).astype(int)
    return filtered.reset_index(drop=True)


def filter_for_code_dkt(df: pd.DataFrame) -> pd.DataFrame:
    #Filtra eventos para Code-DKT: Run.Program e Compile.Error com label binária.

    allowed = {"Run.Program", "Compile.Error"}
    filtered = df[df["EventType"].isin(allowed)].copy()
    assert set(filtered["EventType"].unique()).issubset(allowed), "EventType inesperado passou pelo filtro Code-DKT"
    filtered["correct"] = (
        (filtered["EventType"] == "Run.Program") & (filtered["Score"] == 1.0)
    ).astype(int)
    filtered = filtered.sort_values(["SubjectID", "AssignmentID", "ServerTimestamp"])
    return filtered.reset_index(drop=True)


def build_sequences(df: pd.DataFrame, assignment_id: int) -> list[dict]:
    #Constrói sequências KT por estudante para um assignment específico.

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
    #Trunca sequências KT para as últimas max_len tentativas por estudante.

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
    #Carrega early.csv ou late.csv do split especificado.

    data_root = Path(data_root)
    if split not in _SPLITS or _SPLITS[split][1] is None:
        raise ValueError(f"Labels não disponíveis para split={split!r}. Use 'all_train', 'all_test', 'release_train' ou 'release_test'.")

    _, label_base = _SPLITS[split]
    label_path = data_root / label_base.replace("early.csv", f"{which}.csv")

    if not label_path.exists():
        raise FileNotFoundError(f"Arquivo de labels não encontrado: {label_path}")

    return pd.read_csv(label_path)


def load_spring2019_split(
    data_dir: "Path | str",
    test_size: float = 0.2,
    random_state: int = 1,
    min_attempts: int = 3,
) -> "tuple[pd.DataFrame, pd.DataFrame]":
    #Carrega MainTable.csv, filtra min_attempts e split 80/20 por SubjectID.

    from sklearn.model_selection import train_test_split as _split

    data_dir = Path(data_dir)
    df = pd.read_csv(data_dir / "MainTable.csv")
    df["ServerTimestamp"] = pd.to_datetime(df["ServerTimestamp"], utc=True, errors="coerce")
    if "AssignmentID" in df.columns:
        df["AssignmentID"] = pd.to_numeric(df["AssignmentID"], errors="coerce").astype("Int64")
    if "ProblemID" in df.columns:
        df["ProblemID"] = pd.to_numeric(df["ProblemID"], errors="coerce").astype("Int64")

    run = df[df["EventType"] == "Run.Program"]
    attempts = run.groupby("SubjectID").size()
    eligible = attempts[attempts >= min_attempts].index
    df_filtered = df[df["SubjectID"].isin(eligible)]

    students = df_filtered["SubjectID"].unique()
    train_s, test_s = _split(students, test_size=test_size, random_state=random_state)

    train_df = df_filtered[df_filtered["SubjectID"].isin(train_s)].reset_index(drop=True)
    test_df  = df_filtered[df_filtered["SubjectID"].isin(test_s)].reset_index(drop=True)
    return train_df, test_df

"""
BKT (Bayesian Knowledge Tracing) — Corbett & Anderson (1995).
KC = ProblemID, um modelo pyBKT por assignment, treinado no Spring 2019 train split (80/20).
"""

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from pyBKT.models import Model


def sequences_to_pyBKT_df(sequences: list[dict]) -> pd.DataFrame:
    """Converte lista de sequências para long-format compatível com pyBKT.

    Args:
        sequences: lista de dicts com keys subject_id, assignment_id,
                   events (DataFrame com ServerTimestamp, ProblemID, correct,
                   is_first_attempt).

    Returns:
        DataFrame com colunas user_id, skill_name, correct, is_first_attempt,
        ordenado por (user_id, skill_name, ServerTimestamp).
    """
    rows = []
    for seq in sequences:
        df = seq["events"].copy()
        df["user_id"] = str(seq["subject_id"])
        df["skill_name"] = df["ProblemID"].astype(str)
        rows.append(
            df[["user_id", "skill_name", "ServerTimestamp", "correct", "is_first_attempt"]]
        )
    if not rows:
        return pd.DataFrame(columns=["user_id", "skill_name", "correct", "is_first_attempt"])
    out = pd.concat(rows, ignore_index=True)
    out = out.sort_values(["user_id", "skill_name", "ServerTimestamp"]).reset_index(drop=True)
    return out


def train_bkt(train_sequences: list[dict], seed: int = 42) -> Model:
    """Treina um Model pyBKT com EM nos train_sequences.

    Args:
        train_sequences: output de data_loader.build_sequences (Spring 2019 train split).
        seed: semente para reprodutibilidade.

    Returns:
        Modelo pyBKT fitado.
    """
    df = sequences_to_pyBKT_df(train_sequences)
    model = Model(seed=seed)
    model.fit(data=df[["user_id", "skill_name", "correct"]])
    return model


def predict_bkt(model: Model, sequences: list[dict]) -> pd.DataFrame:
    """Predição BKT sobre sequências de teste.

    Args:
        model: Model pyBKT fitado.
        sequences: sequências de teste.

    Returns:
        DataFrame com colunas user_id, skill_name, correct,
        is_first_attempt, correct_predictions.
    """
    df = sequences_to_pyBKT_df(sequences)
    preds = model.predict(data=df[["user_id", "skill_name", "correct"]])
    df = df.reset_index(drop=True)
    preds = preds.reset_index(drop=True)
    df["correct_predictions"] = preds["correct_predictions"].values
    return df


def compute_auc(pred_df: pd.DataFrame, first_attempt_only: bool = False) -> float:
    """Calcula AUC-ROC sobre predições BKT.

    Args:
        pred_df: DataFrame retornado por predict_bkt (com correct_predictions).
        first_attempt_only: se True, avalia apenas linhas com is_first_attempt=True.

    Returns:
        AUC-ROC; np.nan se não há amostras suficientes.
    """
    df = pred_df.copy()
    if first_attempt_only:
        df = df[df["is_first_attempt"] == True]

    df = df.dropna(subset=["correct_predictions"])
    if len(df) == 0 or df["correct"].nunique() < 2:
        return np.nan

    return float(roc_auc_score(df["correct"].astype(int), df["correct_predictions"]))


def train_and_evaluate(
    train_sequences: list[dict],
    test_sequences: list[dict],
    seed: int = 42,
) -> dict:
    """Pipeline completo: treina, prediz e calcula ambas as métricas AUC.

    Args:
        train_sequences: sequências do train split.
        test_sequences: sequências do test split.
        seed: semente.

    Returns:
        Dict com keys: model, params, all_auc, first_auc, n_train, n_test.
    """
    model = train_bkt(train_sequences, seed=seed)
    pred_df = predict_bkt(model, test_sequences)

    train_df = sequences_to_pyBKT_df(train_sequences)
    return {
        "model": model,
        "params": model.params(),
        "all_auc": compute_auc(pred_df, first_attempt_only=False),
        "first_auc": compute_auc(pred_df, first_attempt_only=True),
        "n_train": len(train_df),
        "n_test": len(pred_df),
    }

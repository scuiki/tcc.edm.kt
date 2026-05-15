"""
Utilitários de avaliação compartilhados entre DKT e Code-DKT.

A métrica principal é AUC-ROC pooled: todas as predições de todos os
estudantes são concatenadas antes de calcular roc_auc_score, sem média
por estudante. Esse protocolo segue Shi et al. (2022) e Piech et al. (2015):
o evaluation.py do repositório Code-DKT acumula first_total_gts e
all_total_gts em listas únicas antes de chamar roc_auc_score uma vez.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score


def build_problem_index(sequences_all: list[dict]) -> dict[int, int]:
    """Mapeia ProblemID para índice inteiro via global scan de todas as sequências.

    O scan é global (train + test, todos os estudantes do assignment) para
    garantir que o índice seja consistente mesmo que um estudante individual
    não tenha tentado todos os M problemas.

    Args:
        sequences_all: concatenação de train + test sequences de um assignment.
            Cada elemento é dict com key 'events' (pd.DataFrame com ProblemID).

    Returns:
        Dict {problem_id (int): index (int)} ordenado por problem_id crescente.
        O índice varia de 0 a M-1, onde M = número de ProblemIDs distintos.
    """
    problem_ids: set[int] = set()
    for seq in sequences_all:
        for pid in seq["events"]["ProblemID"].unique():
            problem_ids.add(int(pid))
    return {pid: idx for idx, pid in enumerate(sorted(problem_ids))}


def compute_auc(pred_df: pd.DataFrame, first_attempt_only: bool = False) -> float:
    """Calcula AUC-ROC pooled sobre predições de qualquer modelo KT.

    Protocolo pooled: todas as linhas do pred_df são tratadas como uma única
    lista de pares (y_true, y_score), sem média por estudante.

    Args:
        pred_df: DataFrame com colunas correct, correct_predictions e
            is_first_attempt. Formato idêntico ao retorno de predict_bkt
            (bkt.py) e predict_dkt (dkt.py).
        first_attempt_only: se True, avalia apenas linhas is_first_attempt==True.

    Returns:
        AUC-ROC como float; np.nan se não há amostras ou correct tem uma classe.
    """
    df = pred_df.copy()
    if first_attempt_only:
        df = df[df["is_first_attempt"] == True]

    df = df.dropna(subset=["correct_predictions"])
    if len(df) == 0 or df["correct"].nunique() < 2:
        return np.nan

    return float(roc_auc_score(df["correct"].astype(int), df["correct_predictions"]))

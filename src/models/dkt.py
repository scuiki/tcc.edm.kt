"""
DKT (Deep Knowledge Tracing) — Piech et al. (2015), NeurIPS.

Implementação para o dataset CSEDM com protocolo de Shi et al. (2022):
KC = ProblemID, um modelo independente por assignment, split 80/20,
Adam lr=0.0005, 40 épocas, max_seq_len=50 (últimas 50 tentativas).

Input: one-hot 2M por tentativa (M problemas por assignment, M=10 no CSEDM).
Output: M probabilidades de acerto no próximo passo (sigmoid).
"""

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor

from src.evaluation import compute_auc


class DKTModel(nn.Module):
    """LSTM DKT — Piech et al. (2015), Section 3.

    Equações implementadas (Piech et al., 2015, Apêndice A):
        h_t = LSTM(x_t, h_{t-1})           — transição de estado interna ao nn.LSTM
        y_t = sigmoid(W_hy * dropout(h_t))  — vetor de probabilidades M-dimensional
    """

    def __init__(
        self,
        input_dim: int,
        hidden_dim: int,
        output_dim: int,
        n_layers: int = 1,
        dropout: float = 0.0,
    ):
        super().__init__()
        # Piech et al. (2015), Apêndice A: LSTM com n_layers camadas.
        # dropout=0.0 no nn.LSTM — Piech et al.: dropout aplicado em h_t→y_t,
        # não na transição de estado do LSTM (seria dropout entre camadas internas).
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=n_layers,
            batch_first=True,
            dropout=0.0,
        )
        # Piech et al. (2015), Section 3: dropout em h_t ao computar y_t,
        # não na transição de estado do LSTM.
        self.drop = nn.Dropout(p=dropout)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x: Tensor, mask: Tensor) -> Tensor:
        """Passa forward pelo LSTM e projeta para probabilidades.

        Args:
            x: (batch, seq_len, input_dim=2M) — one-hot inputs com left-padding.
            mask: (batch, seq_len) — True onde há dado real; aceito para
                uniformidade de interface, mas o LSTM processa todos os passos.

        Returns:
            (batch, seq_len, output_dim=M) com Sigmoid aplicado.
        """
        # h_t calculado pelo LSTM para todos os passos (incluindo padding zeros)
        h, _ = self.lstm(x)  # (batch, seq_len, hidden_dim)
        # Piech et al. (2015), Section 3: dropout aplicado em h_t antes da projeção
        h = self.drop(h)
        # y_t = sigmoid(W_hy * h_t + b_y) — Piech et al. (2015), Section 3
        return torch.sigmoid(self.fc(h))  # (batch, seq_len, M)


def build_input_tensor(
    sequences: list[dict],
    problem_to_idx: dict,
    max_len: int = 50,
) -> tuple[Tensor, Tensor, Tensor]:
    """Converte sequências KT para tensores PyTorch com left-zero-padding.

    Conforme readdata.py do repositório Code-DKT (variável 'extra'):
    sequências mais curtas que max_len são zero-padded à esquerda; sequências
    mais longas são truncadas para as últimas max_len tentativas (as mais recentes).

    Codificação one-hot (Piech et al., 2015, Section 3):
        Acerto no problema i:  x_t[i]     = 1  (posições 0..M-1)
        Erro no problema i:    x_t[i + M]  = 1  (posições M..2M-1)

    Args:
        sequences: lista de dicts com keys subject_id, assignment_id, events.
            events é DataFrame com colunas ProblemID (Int64), correct (int),
            is_first_attempt (bool), ServerTimestamp.
        problem_to_idx: mapeamento global {problem_id (int): index (int)}.
        max_len: comprimento máximo da sequência. Padrão: 50.

    Returns:
        X: (N, max_len, 2M) — inputs one-hot.
        Y_next: (N, max_len, M) — one-hot do próximo problema delta(q_{t+1}).
            Zero no último passo de cada sequência (sem próximo passo).
        mask: (N, max_len) — bool, True onde há dado real (não padding).
    """
    M = len(problem_to_idx)
    N = len(sequences)

    X = torch.zeros(N, max_len, 2 * M, dtype=torch.float32)
    Y_next = torch.zeros(N, max_len, M, dtype=torch.float32)
    mask = torch.zeros(N, max_len, dtype=torch.bool)

    for i, seq in enumerate(sequences):
        events = seq["events"]
        # Shi et al. (2022): últimas max_len tentativas quando L > max_len
        if len(events) > max_len:
            events = events.iloc[-max_len:]
        L = len(events)
        start = max_len - L  # offset de left-padding (readdata.py: 'extra')

        pids = events["ProblemID"].values
        corrects = events["correct"].values

        for t_rel in range(L):
            t = start + t_rel
            m = problem_to_idx[int(pids[t_rel])]
            # Piech et al. (2015), Section 3: one-hot 2M
            if corrects[t_rel]:
                X[i, t, m] = 1.0      # acerto: posição i (0..M-1)
            else:
                X[i, t, m + M] = 1.0  # erro: posição i+M (M..2M-1)
            mask[i, t] = True

        # Y_next[t] = delta(q_{t+1}): one-hot do próximo problema
        for t_rel in range(L - 1):
            t = start + t_rel
            m_next = problem_to_idx[int(pids[t_rel + 1])]
            Y_next[i, t, m_next] = 1.0

    return X, Y_next, mask


def dkt_loss(
    y_pred: Tensor,
    y_true: Tensor,
    next_q: Tensor,
    mask: Tensor,
) -> Tensor:
    """Loss do DKT — Piech et al. (2015), Eq. 3.

    L = sum_t BCE(y_t^T * delta(q_{t+1}), a_{t+1})

    onde delta(q_{t+1}) é o one-hot do próximo problema e a_{t+1} é a
    correção da próxima tentativa. Apenas passos com mask=True E com
    próximo passo disponível contribuem para a loss.

    Args:
        y_pred: (N, max_len, M) — saída do DKTModel (após Sigmoid).
        y_true: (N, max_len) — correctness do próximo passo a_{t+1}.
        next_q: (N, max_len, M) — one-hot do próximo problema delta(q_{t+1}).
        mask: (N, max_len) — True onde há dado real (não padding).

    Returns:
        Scalar: loss média por evento válido não-mascarado.
    """
    # Piech et al. (2015) Eq. 3: y^T * delta(q_{t+1}) seleciona a predicao
    # para o proximo problema dentre as M saidas do LSTM
    pred_for_next = (y_pred * next_q).sum(dim=-1)  # (N, max_len)

    # Passos válidos: dado real E existe próximo problema (não é o último passo)
    valid = mask & (next_q.sum(dim=-1) > 0)

    if valid.sum() == 0:
        return torch.tensor(0.0, requires_grad=True, device=y_pred.device)

    loss = F.binary_cross_entropy(
        pred_for_next[valid],
        y_true[valid].float(),
        reduction="mean",
    )
    return loss


def train_dkt(
    train_sequences: list[dict],
    problem_to_idx: dict,
    config: dict,
    seed: int = 42,
) -> DKTModel:
    """Treina DKTModel com Adam e gradient clipping.

    Args:
        train_sequences: sequências do split de treino.
        problem_to_idx: mapeamento global {problem_id: index}.
        config: dict com keys obrigatórias hidden_dim, dropout, lr,
            batch_size, epochs, max_len.
        seed: SEED=42 conforme CLAUDE.md (reprodutibilidade).

    Returns:
        DKTModel treinado (em CPU ou GPU conforme disponibilidade).
    """
    torch.manual_seed(seed)
    np.random.seed(seed)

    M = len(problem_to_idx)
    hidden_dim = config["hidden_dim"]
    dropout = config.get("dropout", 0.0)
    # Shi et al. (2022) config.py: lr=0.0005, batch_size=128, epochs=40
    lr = config.get("lr", 0.0005)
    batch_size = config.get("batch_size", 128)
    epochs = config.get("epochs", 40)
    max_len = config.get("max_len", 50)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = DKTModel(
        input_dim=2 * M,
        hidden_dim=hidden_dim,
        output_dim=M,
        n_layers=1,
        dropout=dropout,
    ).to(device)

    # Shi et al. (2022) config.py: Adam optimizer
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    X, Y_next, mask = build_input_tensor(train_sequences, problem_to_idx, max_len)

    # y_true: correctness do próximo passo a_{t+1}
    # X[:,:,:M].sum(-1) = 1 se correto no passo t, 0 se errado
    correct_t = X[:, :, :M].sum(dim=-1)   # (N, max_len)
    y_true = torch.zeros_like(correct_t)
    y_true[:, :-1] = correct_t[:, 1:]     # shift left: y_true[t] = correct[t+1]

    X = X.to(device)
    Y_next = Y_next.to(device)
    mask = mask.to(device)
    y_true = y_true.to(device)

    N = len(train_sequences)
    indices = np.arange(N)

    model.train()
    for epoch in range(1, epochs + 1):
        np.random.shuffle(indices)
        epoch_loss = 0.0
        n_batches = 0

        for start_idx in range(0, N, batch_size):
            batch_idx = indices[start_idx : start_idx + batch_size]
            bt = torch.tensor(batch_idx, dtype=torch.long, device=device)

            y_pred = model(X[bt], mask[bt])
            loss = dkt_loss(y_pred, y_true[bt], Y_next[bt], mask[bt])

            optimizer.zero_grad()
            loss.backward()
            # Piech et al. (2015): gradient clipping para evitar exploding gradients
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=10.0)
            optimizer.step()

            epoch_loss += loss.item()
            n_batches += 1

        avg_loss = epoch_loss / n_batches if n_batches > 0 else 0.0
        print(f"  Época {epoch:2d}/{epochs} — loss: {avg_loss:.4f}")

    return model


def predict_dkt(
    model: DKTModel,
    sequences: list[dict],
    problem_to_idx: dict,
    max_len: int = 50,
) -> pd.DataFrame:
    """Predições DKT sobre sequências de teste.

    Para cada evento t+1, a predição é y_t[q_{t+1}]: a entrada do vetor
    de saída do LSTM no passo t correspondente ao problema de t+1. O primeiro
    evento de cada sequência não tem predição (sem histórico anterior).

    Args:
        model: DKTModel treinado.
        sequences: sequências de teste.
        problem_to_idx: mapeamento global {problem_id: index}.
        max_len: comprimento máximo (deve ser igual ao usado no treino).

    Returns:
        DataFrame com colunas: user_id, skill_name (ProblemID como str),
        correct, is_first_attempt, correct_predictions.
        Mesmo formato que predict_bkt em bkt.py.
    """
    if not sequences:
        return pd.DataFrame(
            columns=["user_id", "skill_name", "correct", "is_first_attempt",
                     "correct_predictions"]
        )

    device = next(model.parameters()).device
    model.eval()

    with torch.no_grad():
        X, _Y_next, mask = build_input_tensor(sequences, problem_to_idx, max_len)
        y_pred_np = model(X.to(device), mask.to(device)).cpu().numpy()

    rows = []
    for i, seq in enumerate(sequences):
        events = seq["events"]
        if len(events) > max_len:
            events = events.iloc[-max_len:]
        L = len(events)
        start = max_len - L

        # t_rel=0: primeiro evento, sem estado anterior — sem predição
        # t_rel=1..L-1: predição vem de y_pred[i, start+t_rel-1, q_{t_rel}]
        for t_rel in range(1, L):
            t_prev = start + t_rel - 1
            row = events.iloc[t_rel]
            m = problem_to_idx[int(row["ProblemID"])]
            rows.append({
                "user_id": str(seq["subject_id"]),
                "skill_name": str(int(row["ProblemID"])),
                "correct": int(row["correct"]),
                "is_first_attempt": bool(row["is_first_attempt"]),
                "correct_predictions": float(y_pred_np[i, t_prev, m]),
            })

    return pd.DataFrame(rows)


def train_and_evaluate(
    train_sequences: list[dict],
    test_sequences: list[dict],
    problem_to_idx: dict,
    config: dict,
    seed: int = 42,
) -> dict:
    """Pipeline completo: treina, prediz e calcula AUC para um assignment.

    Args:
        train_sequences: sequências do split de treino.
        test_sequences: sequências do split de teste.
        problem_to_idx: mapeamento global {problem_id: index}.
        config: hiperparâmetros com keys hidden_dim, dropout, lr,
            batch_size, epochs, max_len.
        seed: semente.

    Returns:
        Dict com keys: model, config, all_auc, first_auc,
        n_train_events, n_test_events.
    """
    max_len = config.get("max_len", 50)

    model = train_dkt(train_sequences, problem_to_idx, config, seed=seed)
    pred_df = predict_dkt(model, test_sequences, problem_to_idx, max_len=max_len)

    n_train_events = sum(
        min(len(s["events"]), max_len) for s in train_sequences
    )
    n_test_events = len(pred_df)

    return {
        "model": model,
        "config": config,
        "all_auc": compute_auc(pred_df, first_attempt_only=False),
        "first_auc": compute_auc(pred_df, first_attempt_only=True),
        "n_train_events": n_train_events,
        "n_test_events": n_test_events,
    }

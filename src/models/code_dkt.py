"""
Code-DKT — Shi et al. (2022), EDM 2022.

Arquitetura: LSTM + mecanismo de atenção score-attended sobre paths AST
(code2vec). Fiel ao repositório oficial Code-DKT (c2vRNNModel.py).

Diferenças em relação ao DKT (Piech et al., 2015):
  Input LSTM: concat(x_t, z_t) ∈ R^{2M+320=340}  (vs R^{20} no DKT)
  z_t: vetor de código via atenção sobre R paths AST embedados (320-dim)
  Embeddings: embed_nodes(100) + embed_paths(100) + embed_nodes(100) + x_t(20) = 320

Interface pública idêntica à de dkt.py para consumo uniforme em 07_comparison.ipynb.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor

from src.code_features import build_code_input_tensor
from src.evaluation import compute_auc
from src.models.dkt import dkt_loss


class CodeDKTModel(nn.Module):
    """Code-DKT — LSTM com atenção code2vec sobre paths AST.

    Fiel à arquitetura de c2vRNNModel.py (Code-DKT, Shi et al., 2022):
    - embed_nodes compartilhado para start e end tokens (100-dim cada)
    - embed_paths exclusivo para sequências de nós (100-dim)
    - embed_dropout 0.2 no full_embed (ativo apenas em model.train())
    - path_transformation_layer: Linear(input_dim+300, input_dim+300) + tanh
    - attention_layer: Linear(input_dim+300, 1) + Softmax(dim=2, sobre R paths)
    - LSTM input: concat(x_t, code_vector) ∈ R^{2*input_dim+300}
    - dropout configurável em h_t antes de fc (para grid search)
    """

    def __init__(
        self,
        input_dim: int,
        hidden_dim: int,
        output_dim: int,
        node_count: int,
        path_count: int,
        n_layers: int = 1,
        dropout: float = 0.0,
        R: int = 50,
        node_embed_dim: int = 100,
        path_embed_dim: int = 100,
    ):
        """
        Args:
            input_dim: dimensão DKT one-hot (2M).
            hidden_dim: tamanho do hidden state do LSTM.
            output_dim: número de problemas (M).
            node_count: tamanho do vocabulário de tokens (sem contar PAD/UNK).
            path_count: tamanho do vocabulário de path strings.
            R: número de paths por submissão (Shi et al., 2022, Table 3: 50).
            node_embed_dim, path_embed_dim: dimensão de cada embedding (100).
        """
        super().__init__()
        self.input_dim = input_dim
        self.R = R
        embed_dim = node_embed_dim + path_embed_dim + node_embed_dim  # 300

        # +2 reserva slots para PAD (0) e UNK — c2vRNNModel.py linha 14
        self.embed_nodes = nn.Embedding(node_count + 2, node_embed_dim)
        self.embed_paths = nn.Embedding(path_count + 2, path_embed_dim)
        self.embed_dropout = nn.Dropout(0.2)  # ativo apenas em model.train()

        full_dim = input_dim + embed_dim  # 2M + 300 = 320

        # Score-attended path selection — Shi et al. (2022), Section 3
        self.path_transformation_layer = nn.Linear(full_dim, full_dim)
        # Softmax dim=2 (sobre R paths): atenção semântica conforme paper;
        # o repositório oficial usa dim=1 (sequência) — interpretamos o paper.
        self.attention_layer = nn.Linear(full_dim, 1)

        # LSTM: input = concat(x_t, code_vector) = 2M + (2M+300) = 340
        self.rnn = nn.LSTM(
            input_size=2 * input_dim + embed_dim,  # 2*2M+300=340 para M=10
            hidden_size=hidden_dim,
            num_layers=n_layers,
            batch_first=True,
        )
        self.dropout = nn.Dropout(p=dropout)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x: Tensor) -> Tensor:
        """Forward pass.

        Args:
            x: (B, L, input_dim + R*3) — DKT one-hot || índices de paths.
               Índices são armazenados como float32 e convertidos para long.

        Returns:
            (B, L, M) probabilidades de acerto (Sigmoid).
        """
        B, L, _ = x.shape

        # Separação do tensor combinado — c2vRNNModel.py linhas 39-42
        rnn_first_part = x[:, :, : self.input_dim]                   # (B, L, 2M)
        c2v_input = (
            x[:, :, self.input_dim :]
            .reshape(B, L, self.R, 3)
            .long()
        )                                                              # (B, L, R, 3)

        # Embeddings dos três componentes do path — c2vRNNModel.py linhas 48-50
        start_embed = self.embed_nodes(c2v_input[:, :, :, 0])        # (B, L, R, 100)
        path_embed = self.embed_paths(c2v_input[:, :, :, 1])         # (B, L, R, 100)
        end_embed = self.embed_nodes(c2v_input[:, :, :, 2])          # (B, L, R, 100)

        # x_t replicado para cada path — c2vRNNModel.py linha 40
        rnn_rep = rnn_first_part.unsqueeze(2).expand(-1, -1, self.R, -1)  # (B,L,R,2M)

        # full_embed: concat(start, end, path, x_t) — c2vRNNModel.py linha 52
        full_embed = torch.cat(
            [start_embed, end_embed, path_embed, rnn_rep], dim=3
        )                                                              # (B, L, R, 2M+300)
        full_embed = self.embed_dropout(full_embed)                   # desligado em eval

        # Transformação + atenção — Shi et al. (2022), Section 3
        transformed = torch.tanh(self.path_transformation_layer(full_embed))  # (B,L,R,320)
        attn_weights = torch.softmax(
            self.attention_layer(transformed), dim=2
        )                                                              # (B, L, R, 1)
        code_vectors = (full_embed * attn_weights).sum(dim=2)         # (B, L, 320)

        # Input do LSTM: concat(x_t, code_vector) — Shi et al. (2022), Section 3
        rnn_input = torch.cat([rnn_first_part, code_vectors], dim=2)  # (B, L, 340)

        out, _ = self.rnn(rnn_input)                                  # (B, L, hidden)
        out = self.dropout(out)
        return torch.sigmoid(self.fc(out))                            # (B, L, M)


# ---------------------------------------------------------------------------
# Funções de treino e predição
# ---------------------------------------------------------------------------

def train_code_dkt(
    train_sequences: list[dict],
    problem_to_idx: dict[int, int],
    vocab: dict,
    config: dict,
    cache_raw: dict[str, list],
    seed: int = 42,
) -> CodeDKTModel:
    """Treina CodeDKTModel com Adam e gradient clipping.

    Args:
        train_sequences: sequências do split de treino.
        problem_to_idx: {problem_id: index}, consistente com train+test.
        vocab: dict com chaves token_to_idx, path_to_idx, node_count, path_count.
        config: hiperparâmetros — hidden_dim, dropout, lr, batch_size, epochs, max_len, R.
        cache_raw: dict {CodeStateID: list[paths]} pré-computado.
        seed: semente para reprodutibilidade.

    Returns:
        CodeDKTModel treinado (no device CUDA ou CPU disponível).
    """
    torch.manual_seed(seed)
    np.random.seed(seed)

    M = len(problem_to_idx)
    hidden_dim = config["hidden_dim"]
    dropout = config.get("dropout", 0.0)
    lr = config.get("lr", 0.0005)
    batch_size = config.get("batch_size", 128)
    epochs = config.get("epochs", 40)
    max_len = config.get("max_len", 50)
    R = config.get("R", 50)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = CodeDKTModel(
        input_dim=2 * M,
        hidden_dim=hidden_dim,
        output_dim=M,
        node_count=vocab["node_count"],
        path_count=vocab["path_count"],
        n_layers=1,
        dropout=dropout,
        R=R,
    ).to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    X, Y_next, mask = build_code_input_tensor(
        train_sequences, cache_raw,
        vocab["token_to_idx"], vocab["path_to_idx"],
        problem_to_idx, max_len=max_len, R=R,
    )

    # y_true: correctness do próximo passo a_{t+1}
    correct_t = X[:, :, :M].sum(dim=-1)        # (N, max_len) — 1 se acerto no passo t
    y_true = torch.zeros_like(correct_t)
    y_true[:, :-1] = correct_t[:, 1:]          # shift: y_true[t] = correct[t+1]

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

        for start_i in range(0, N, batch_size):
            batch_idx = indices[start_i : start_i + batch_size]
            bt = torch.tensor(batch_idx, dtype=torch.long, device=device)

            y_pred = model(X[bt])
            loss = dkt_loss(y_pred, y_true[bt], Y_next[bt], mask[bt])

            optimizer.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=10.0)
            optimizer.step()

            epoch_loss += loss.item()
            n_batches += 1

        avg_loss = epoch_loss / n_batches if n_batches > 0 else 0.0
        print(f"  Época {epoch:2d}/{epochs} — loss: {avg_loss:.4f}")

    return model


def predict_code_dkt(
    model: CodeDKTModel,
    sequences: list[dict],
    problem_to_idx: dict[int, int],
    vocab: dict,
    cache_raw: dict[str, list],
    max_len: int = 50,
    R: int = 50,
) -> pd.DataFrame:
    """Predições Code-DKT sobre sequências de teste.

    Para cada evento t+1, a predição é y_t[q_{t+1}]: componente do vetor de
    saída do LSTM no passo t correspondente ao problema de t+1. O primeiro
    evento de cada sequência não tem predição (sem histórico anterior).

    Args:
        model: CodeDKTModel treinado.
        sequences: sequências de teste.
        problem_to_idx: mapeamento global {problem_id: index}.
        vocab: dict com token_to_idx, path_to_idx.
        cache_raw: dict {CodeStateID: list[paths]} pré-computado.
        max_len, R: devem coincidir com os usados no treino.

    Returns:
        DataFrame com colunas: user_id, skill_name, correct,
        is_first_attempt, correct_predictions.
    """
    if not sequences:
        return pd.DataFrame(
            columns=["user_id", "skill_name", "correct",
                     "is_first_attempt", "correct_predictions"]
        )

    device = next(model.parameters()).device
    model.eval()

    with torch.no_grad():
        X, _Y_next, mask = build_code_input_tensor(
            sequences, cache_raw,
            vocab["token_to_idx"], vocab["path_to_idx"],
            problem_to_idx, max_len=max_len, R=R,
        )
        y_pred_np = model(X.to(device)).cpu().numpy()

    rows = []
    for i, seq in enumerate(sequences):
        events = seq["events"]
        if len(events) > max_len:
            events = events.iloc[-max_len:]
        L = len(events)
        start_idx = max_len - L

        for t_rel in range(1, L):
            t_prev = start_idx + t_rel - 1
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
    problem_to_idx: dict[int, int],
    vocab: dict,
    config: dict,
    cache_raw: dict[str, list],
    seed: int = 42,
) -> dict:
    """Pipeline completo: treina, prediz e calcula AUC para um assignment.

    Args:
        train_sequences, test_sequences: splits do assignment.
        problem_to_idx: {problem_id: index} global (train + test).
        vocab: dict com token_to_idx, path_to_idx, node_count, path_count.
        config: hiperparâmetros.
        cache_raw: dict {CodeStateID: list[paths]} pré-computado.
        seed: semente.

    Returns:
        Dict com keys: model, config, all_auc, first_auc,
        n_train_events, n_test_events, pred_df.
    """
    max_len = config.get("max_len", 50)
    R = config.get("R", 50)

    model = train_code_dkt(
        train_sequences, problem_to_idx, vocab, config, cache_raw, seed=seed
    )
    pred_df = predict_code_dkt(
        model, test_sequences, problem_to_idx, vocab, cache_raw,
        max_len=max_len, R=R,
    )

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
        "pred_df": pred_df,
    }

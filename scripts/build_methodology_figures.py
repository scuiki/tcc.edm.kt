"""Gera as figuras de docs/METODOLOGIA_FERRAMENTAS.md.

Saída: PNGs em docs/figures/. Tudo via matplotlib puro (sem dependência de
graphviz CLI). As árvores AST/srcML usam layout hierárquico calculado a mão.

Uso:
    python scripts/build_methodology_figures.py            # gera todas
    python scripts/build_methodology_figures.py --only f4  # só uma
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from anytree import Node
from anytree.walker import Walker
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.code_features import _build_tree as _javalang_build_tree
from src.code_features import _get_children, _get_token, _parse_java
from src.srcml_features import _NS_PREFIX, _srcml_build_tree, _strip_ns

FIG_DIR = ROOT / "docs" / "figures"
SNIPPET_DIR = FIG_DIR / "snippets"


# ---------------------------------------------------------------------------
# Helpers de plotagem
# ---------------------------------------------------------------------------

def _box(ax, x, y, w, h, text, *, fc="#EAF2FB", ec="#1F4E79", fs=10, lw=1.2, bold=False):
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.04,rounding_size=0.08",
        linewidth=lw, edgecolor=ec, facecolor=fc,
    )
    ax.add_patch(box)
    ax.text(
        x, y, text, ha="center", va="center", fontsize=fs,
        fontweight=("bold" if bold else "normal"),
        wrap=True,
    )


def _arrow(ax, x1, y1, x2, y2, *, color="#1F4E79", lw=1.4, style="-|>", rad=0.0, label=None, label_offset=(0, 0)):
    arr = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style, mutation_scale=14,
        linewidth=lw, color=color,
        connectionstyle=f"arc3,rad={rad}",
    )
    ax.add_patch(arr)
    if label:
        mx, my = (x1 + x2) / 2 + label_offset[0], (y1 + y2) / 2 + label_offset[1]
        ax.text(mx, my, label, fontsize=9, ha="center", va="center",
                bbox=dict(facecolor="white", edgecolor="none", pad=1.0))


def _setup_axes(figsize, xlim, ylim, title=None):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=12, pad=8)
    return fig, ax


def _save(fig, name):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    out = FIG_DIR / name
    fig.savefig(out, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[ok] {out.relative_to(ROOT)}")


# ---------------------------------------------------------------------------
# Layout hierárquico (Reingold-Tilford simplificado)
# ---------------------------------------------------------------------------

def _assign_layout(root) -> dict:
    """Atribui (x, y) a cada nó anytree usando in-order com largura uniforme.

    Cada folha ocupa 1 unidade de x; cada pai fica centralizado sobre seus filhos.
    y = -depth (raiz no topo).
    """
    positions: dict[int, tuple[float, float]] = {}

    def assign(node, depth, next_x):
        children = list(node.children)
        if not children:
            positions[id(node)] = (next_x, -depth)
            return next_x + 1.0
        first_x = next_x
        x = next_x
        for c in children:
            x = assign(c, depth + 1, x)
        last_child_x = positions[id(children[-1])][0]
        first_child_x = positions[id(children[0])][0]
        positions[id(node)] = ((first_child_x + last_child_x) / 2, -depth)
        return x

    assign(root, 0, 0.0)
    return positions


def _draw_tree(ax, root, positions, *, highlight_nodes=None, highlight_color="#C0392B",
               default_fc="#F4F6F7", default_ec="#566573", node_fs=9, edge_alpha=0.75,
               node_size=900):
    highlight_nodes = set(id(n) for n in (highlight_nodes or []))
    # arestas primeiro
    for node in _iter_nodes(root):
        x, y = positions[id(node)]
        for child in node.children:
            cx, cy = positions[id(child)]
            color = highlight_color if (id(node) in highlight_nodes and id(child) in highlight_nodes) else "#95A5A6"
            lw = 2.2 if color == highlight_color else 0.9
            ax.plot([x, cx], [y, cy], color=color, lw=lw, alpha=edge_alpha, zorder=1)
    # nós
    for node in _iter_nodes(root):
        x, y = positions[id(node)]
        token = _node_label(node)
        # Trunca tokens longos para legibilidade
        if len(token) > 9:
            token = token[:8] + "…"
        fc = highlight_color if id(node) in highlight_nodes else default_fc
        ec = "#922B21" if id(node) in highlight_nodes else default_ec
        text_color = "white" if id(node) in highlight_nodes else "black"
        bold = id(node) in highlight_nodes
        ax.scatter([x], [y], s=node_size, marker="o", facecolor=fc, edgecolor=ec, linewidth=1.1, zorder=2)
        ax.text(x, y, token, fontsize=node_fs, ha="center", va="center",
                color=text_color, fontweight=("bold" if bold else "normal"), zorder=3)


def _iter_nodes(root):
    yield root
    for c in root.children:
        yield from _iter_nodes(c)


def _node_label(node):
    """Extrai a string de token de um Node anytree (compatível com formato após
    padding numérico ou string)."""
    if hasattr(node, "name") and isinstance(node.name, list) and len(node.name) >= 2:
        return str(node.name[1])
    return str(getattr(node, "name", "?"))


def _all_leaves(root):
    return [n for n in _iter_nodes(root) if not n.children]


def _walk_path_nodes(a, b):
    walker = Walker()
    upstream, lca, downstream = walker.walk(a, b)
    return list(upstream) + [lca] + list(downstream)


# ---------------------------------------------------------------------------
# Construtores de árvore (sem mutação do node.name)
# ---------------------------------------------------------------------------

def _build_javalang_tree(code: str):
    parsed = _parse_java(code)
    head = Node(["1", _get_token(parsed)])
    for i, child in enumerate(_get_children(parsed)):
        _javalang_build_tree(child, head, "1" + str(i + 1))
    return head


def _build_srcml_tree(code: str):
    result = subprocess.run(
        ["srcml", "--language=Java"],
        input=code.encode("utf-8", errors="replace"),
        capture_output=True, timeout=10,
    )
    if result.returncode != 0 or not result.stdout:
        raise RuntimeError("srcML CLI falhou")
    root_elem = ET.fromstring(result.stdout.decode("utf-8", errors="replace"))
    head = Node(["1", "unit"])
    for i, child in enumerate(list(root_elem)):
        _srcml_build_tree(child, head, "1" + str(i + 1))
    return head


# ---------------------------------------------------------------------------
# F1 — Modelo HMM de 2 estados do BKT
# ---------------------------------------------------------------------------

def fig1_bkt_hmm():
    fig, ax = _setup_axes((9, 5), (-1, 10), (-1.5, 4.5),
                          title="Modelo BKT: HMM de dois estados latentes")

    # Dois estados
    _box(ax, 2.0, 2.0, 2.6, 1.1, "Não-aprendido\n(L = 0)", fc="#FCE4D6", ec="#C0392B", fs=11, bold=True)
    _box(ax, 7.0, 2.0, 2.6, 1.1, "Aprendido\n(L = 1)", fc="#D6ECF3", ec="#1F618D", fs=11, bold=True)

    # Transição: Não-aprendido -> Aprendido com p(T)
    _arrow(ax, 3.3, 2.2, 5.7, 2.2, color="#1F618D", lw=1.6, rad=0.0, label="p(T)")

    # Auto-loop: Não-aprendido permanece com 1 - p(T)
    arr = FancyArrowPatch((1.4, 2.55), (1.4, 2.55), connectionstyle="arc3,rad=-3.5",
                          arrowstyle="-|>", mutation_scale=12, color="#566573")
    ax.add_patch(arr)
    ax.text(0.85, 3.4, "1 − p(T)", fontsize=9, color="#566573")

    # Sem forgetting (sem aresta de volta)
    ax.text(4.5, 1.4, "Sem forgetting: transição Aprendido → Não-aprendido proibida",
            fontsize=9, ha="center", color="#566573", style="italic")

    # Estado inicial p(L0)
    _arrow(ax, 0.5, 4.2, 1.5, 2.45, color="#27AE60", lw=1.4, rad=-0.15, label="p(L₀)")

    # Emissões observáveis
    _box(ax, 2.0, -0.2, 2.4, 0.8, "P(acerto | ¬L) = p(G)", fc="#FFF2CC", ec="#A67C00", fs=9)
    _box(ax, 7.0, -0.2, 2.4, 0.8, "P(acerto | L) = 1 − p(S)", fc="#FFF2CC", ec="#A67C00", fs=9)
    _arrow(ax, 2.0, 1.4, 2.0, 0.25, color="#A67C00", lw=1.0, style="->")
    _arrow(ax, 7.0, 1.4, 7.0, 0.25, color="#A67C00", lw=1.0, style="->")

    # Legenda de parâmetros
    ax.text(4.5, 4.0,
            "Quatro parâmetros por KC:\n"
            "p(L₀) prior, p(T) aprendizado, p(G) chute, p(S) deslize",
            ha="center", fontsize=9,
            bbox=dict(facecolor="#FBFCFC", edgecolor="#85929E", boxstyle="round,pad=0.3"))

    ax.text(4.5, -1.2, "Adaptado de Corbett e Anderson (1995), Figura 4",
            ha="center", fontsize=8, style="italic", color="#566573")

    _save(fig, "fig1_bkt_hmm.png")


# ---------------------------------------------------------------------------
# F3 — Arquitetura DKT (LSTM unrolled)
# ---------------------------------------------------------------------------

def fig3_dkt_unrolled():
    fig, ax = _setup_axes((11, 5.6), (-0.5, 13), (-1, 5.5),
                          title="Arquitetura DKT: LSTM desenrolada no tempo (3 passos)")

    xs = [2.0, 6.0, 10.0]
    labels_t = ["t = 1", "t = 2", "t = 3"]

    for i, x in enumerate(xs):
        # input one-hot
        _box(ax, x, 0.4, 2.0, 0.7, f"x_{i+1} ∈ {{0,1}}^{{2M}}\n(qₜ, aₜ) one-hot", fs=8, fc="#FDF2E9", ec="#B9770E")
        # célula LSTM
        _box(ax, x, 2.2, 2.0, 1.0, f"LSTM\nhₜ ∈ ℝ^H", fs=10, fc="#D6EAF8", ec="#1F618D", bold=True)
        # output
        _box(ax, x, 4.0, 2.0, 0.7, f"yₜ = σ(W_hy hₜ + b_y)\nyₜ ∈ [0,1]^M", fs=8, fc="#E8DAEF", ec="#6C3483")
        # input -> LSTM
        _arrow(ax, x, 0.8, x, 1.7)
        # LSTM -> output
        _arrow(ax, x, 2.75, x, 3.65)
        # rótulo do passo
        ax.text(x, -0.4, labels_t[i], fontsize=9, ha="center", color="#566573")

    # arestas recorrentes h_{t-1} -> h_t
    for i in range(2):
        _arrow(ax, xs[i] + 1.0, 2.2, xs[i+1] - 1.0, 2.2,
               color="#1F618D", lw=1.4, label="hₜ recorrente")

    # legenda inferior
    ax.text(6.5, -0.9,
            "Adaptado de Piech et al. (2015), Figura 2. "
            "Loss: L = Σₜ BCE(yₜᵀ δ(q_{t+1}), a_{t+1})",
            ha="center", fontsize=8, style="italic", color="#566573")

    _save(fig, "fig3_dkt_unrolled.png")


# ---------------------------------------------------------------------------
# F4 — AST javalang com paths code2vec destacados
# ---------------------------------------------------------------------------

def _read_snippet(name: str) -> str:
    return (SNIPPET_DIR / name).read_text(encoding="utf-8")


def fig4_ast_javalang():
    code = _read_snippet("snippet_correct.java")
    root = _build_javalang_tree(code)
    positions = _assign_layout(root)

    # Escolhe 2 pares de folhas didáticos para destacar
    leaves = _all_leaves(root)
    leaf_by_label: dict[str, list] = {}
    for leaf in leaves:
        leaf_by_label.setdefault(_node_label(leaf), []).append(leaf)

    highlight = set()
    # par 1: as duas ocorrências de "goal" (se houver pelo menos 2)
    if len(leaf_by_label.get("goal", [])) >= 2:
        path = _walk_path_nodes(leaf_by_label["goal"][0], leaf_by_label["goal"][-1])
        highlight.update(path)
    # par 2: "big" -> "small" (mostrando relação entre parâmetros)
    if leaf_by_label.get("big") and leaf_by_label.get("small"):
        path = _walk_path_nodes(leaf_by_label["big"][0], leaf_by_label["small"][0])
        highlight.update(path)

    xs = [p[0] for p in positions.values()]
    ys = [p[1] for p in positions.values()]
    pad_x, pad_y = 1.2, 1.0
    width_units = max(xs) - min(xs)
    height_units = max(ys) - min(ys)
    fig_w = max(28, 0.75 * width_units + 4)
    fig_h = max(13, 1.4 * height_units + 3)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(min(xs) - pad_x, max(xs) + pad_x)
    ax.set_ylim(min(ys) - pad_y, max(ys) + pad_y)
    ax.axis("off")
    ax.set_title(
        "AST javalang do snippet makeChocolate (CSEDM A487/P101) — 2 paths code2vec destacados em vermelho",
        fontsize=13, pad=10,
    )
    _draw_tree(ax, root, positions, highlight_nodes=highlight, node_fs=8, node_size=820)
    ax.text(
        (min(xs) + max(xs)) / 2, min(ys) - 0.8,
        "Snippet: docs/figures/snippets/snippet_correct.java  |  Adaptado de Shi et al. (2022), Figura 2",
        ha="center", fontsize=10, style="italic", color="#566573",
    )
    _save(fig, "fig4_ast_javalang.png")


# ---------------------------------------------------------------------------
# F5 — Pipeline Code-DKT
# ---------------------------------------------------------------------------

def fig5_code_dkt_pipeline():
    fig, ax = _setup_axes((13, 5.5), (-0.3, 14), (-0.5, 5),
                          title="Pipeline Code-DKT: do código-fonte à predição")

    nodes = [
        (1.2, 2.5, 1.8, 1.0, "Código\nJava (CSEDM)", "#FDF2E9", "#B9770E"),
        (3.6, 2.5, 1.8, 1.0, "AST\n(javalang)", "#FCF3CF", "#9A7D0A"),
        (6.0, 3.6, 1.9, 0.9, "Embed. de\nnós + paths\n(d = 300)", "#D6ECF3", "#1F618D"),
        (6.0, 1.4, 1.9, 0.9, "R = 50 paths\ncode2vec\n(s, o, q)", "#D6EAF8", "#1F618D"),
        (8.6, 2.5, 1.8, 1.0, "Atenção\nα = SoftMax(E·W_a)", "#E8DAEF", "#6C3483"),
        (11.0, 2.5, 1.8, 1.0, "Concat\nx_t ⊕ z_t", "#D5F5E3", "#1E8449"),
        (13.4, 2.5, 1.8, 1.0, "LSTM\n→ y_t", "#FADBD8", "#922B21"),
    ]
    for x, y, w, h, text, fc, ec in nodes:
        _box(ax, x, y, w, h, text, fc=fc, ec=ec, fs=9, bold=True)

    # arestas principais
    _arrow(ax, 2.1, 2.5, 2.7, 2.5)
    _arrow(ax, 4.5, 2.5, 5.05, 3.2)
    _arrow(ax, 4.5, 2.5, 5.05, 1.8)
    _arrow(ax, 6.95, 3.6, 7.7, 2.75)
    _arrow(ax, 6.95, 1.4, 7.7, 2.25)
    _arrow(ax, 9.5, 2.5, 10.1, 2.5)
    _arrow(ax, 11.9, 2.5, 12.5, 2.5)

    ax.text(7.0, 4.6,
            "z_t = W₀(Σ αᵢ eᵢ) é o vetor de código contextualizado, concatenado ao one-hot DKT x_t",
            ha="center", fontsize=9, style="italic", color="#1F618D",
            bbox=dict(facecolor="#FBFCFC", edgecolor="#85929E", boxstyle="round,pad=0.3"))

    ax.text(7.0, -0.25,
            "Adaptado de Shi et al. (2022), Figura 3. Implementação: src/code_features.py + src/models/code_dkt.py",
            ha="center", fontsize=8, style="italic", color="#566573")

    _save(fig, "fig5_code_dkt_pipeline.png")


# ---------------------------------------------------------------------------
# F6 — Árvore srcML do mesmo snippet
# ---------------------------------------------------------------------------

def fig6_srcml_tree():
    code = _read_snippet("snippet_correct.java")
    root = _build_srcml_tree(code)
    positions = _assign_layout(root)

    leaves = _all_leaves(root)
    leaf_by_label: dict[str, list] = {}
    for leaf in leaves:
        leaf_by_label.setdefault(_node_label(leaf), []).append(leaf)

    highlight = set()
    if len(leaf_by_label.get("goal", [])) >= 2:
        highlight.update(_walk_path_nodes(leaf_by_label["goal"][0], leaf_by_label["goal"][-1]))
    if leaf_by_label.get("big") and leaf_by_label.get("small"):
        highlight.update(_walk_path_nodes(leaf_by_label["big"][0], leaf_by_label["small"][0]))

    xs = [p[0] for p in positions.values()]
    ys = [p[1] for p in positions.values()]
    pad_x, pad_y = 1.2, 1.0
    width_units = max(xs) - min(xs)
    height_units = max(ys) - min(ys)
    fig_w = max(28, 0.75 * width_units + 4)
    fig_h = max(13, 1.4 * height_units + 3)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(min(xs) - pad_x, max(xs) + pad_x)
    ax.set_ylim(min(ys) - pad_y, max(ys) + pad_y)
    ax.axis("off")
    ax.set_title(
        "Árvore srcML do MESMO snippet makeChocolate — tags XML como nós internos",
        fontsize=13, pad=10,
    )
    _draw_tree(ax, root, positions, highlight_nodes=highlight, node_fs=8, node_size=820)
    ax.text(
        (min(xs) + max(xs)) / 2, min(ys) - 0.8,
        "Comparar com F4. Tags genéricas (expr, call, decl) substituem nomes de classes javalang. Adaptado de Pankiewicz et al. (2025), Figura 1(b)",
        ha="center", fontsize=10, style="italic", color="#566573",
    )
    _save(fig, "fig6_srcml_tree.png")


# ---------------------------------------------------------------------------
# F7 — srcML em código com Compile.Error (javalang falha)
# ---------------------------------------------------------------------------

def fig7_srcml_error():
    code_err = _read_snippet("snippet_compile_error.java")

    # Verifica que javalang FALHA
    try:
        _parse_java(code_err)
        jl_status = "PARSE OK (inesperado)"
        jl_ok = True
    except Exception as e:
        jl_status = f"FALHA: {type(e).__name__}"
        jl_ok = False

    # Constrói árvore srcML (esperado: passar)
    root = _build_srcml_tree(code_err)
    positions = _assign_layout(root)

    xs = [p[0] for p in positions.values()]
    ys = [p[1] for p in positions.values()]
    tree_width = max(xs) - min(xs)
    tree_height = max(ys) - min(ys)

    # Layout: caixa de falha javalang à esquerda, árvore srcML à direita
    fig_w = max(20, 0.45 * tree_width + 8)
    fig_h = max(10, 1.2 * tree_height + 3)
    fig = plt.figure(figsize=(fig_w, fig_h))
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 2.6], wspace=0.05)
    ax_left = fig.add_subplot(gs[0])
    ax_right = fig.add_subplot(gs[1])

    # Esquerda: snippet + status javalang
    ax_left.axis("off")
    ax_left.set_xlim(0, 10)
    ax_left.set_ylim(0, 10)
    ax_left.text(5, 9.3, "Snippet com Compile.Error (CSEDM A487/P101)",
                 ha="center", fontsize=11, fontweight="bold")
    ax_left.text(0.3, 8.5, code_err.rstrip(),
                 fontsize=9, family="monospace", va="top",
                 bbox=dict(facecolor="#FDFEFE", edgecolor="#85929E", boxstyle="round,pad=0.4"))
    color_jl = "#C0392B" if not jl_ok else "#27AE60"
    ax_left.text(5, 2.0, f"javalang: {jl_status}\n(parser tradicional descarta o snippet)",
                 ha="center", fontsize=10, color=color_jl, fontweight="bold",
                 bbox=dict(facecolor="#FDEDEC", edgecolor=color_jl, boxstyle="round,pad=0.4"))
    ax_left.text(5, 0.7, "srcML: PARSE OK → árvore parcial preservada (→)",
                 ha="center", fontsize=10, color="#1E8449", fontweight="bold",
                 bbox=dict(facecolor="#E8F8F5", edgecolor="#1E8449", boxstyle="round,pad=0.4"))

    # Direita: árvore srcML
    ax_right.set_xlim(min(xs) - 1.0, max(xs) + 1.0)
    ax_right.set_ylim(min(ys) - 1.0, max(ys) + 1.0)
    ax_right.axis("off")
    ax_right.set_title("Árvore srcML (estrutura parcial recuperada do snippet quebrado)", fontsize=12)
    _draw_tree(ax_right, root, positions, node_fs=9, node_size=1100)
    ax_right.text(
        (min(xs) + max(xs)) / 2, min(ys) - 0.85,
        "Argumento central de Pankiewicz et al. (2025): srcML cobre Compile.Error (30,27% do CSEDM)",
        ha="center", fontsize=10, style="italic", color="#566573",
    )

    fig.suptitle("F7: srcML vs javalang em código sintaticamente quebrado", fontsize=13, y=0.98)
    out = FIG_DIR / "fig7_srcml_error.png"
    fig.savefig(out, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[ok] {out.relative_to(ROOT)}")


# ---------------------------------------------------------------------------
# F8 — Fluxograma KCGen-KT
# ---------------------------------------------------------------------------

def fig8_kcgen_pipeline():
    fig, ax = _setup_axes((14, 5.8), (-0.5, 15), (-1, 5.5),
                          title="Pipeline KCGen-KT (Duan et al., 2025) — 5 etapas reproduzidas em 03b_kc_generation.ipynb")

    steps = [
        (1.4, 2.5, 2.0, 1.4, "Etapa 1\nSeleção de\nn = 5 submissões\ncorretas/problema", "#FDF2E9", "#B9770E"),
        (4.2, 2.5, 2.0, 1.4, "Etapa 2\nLLM com few-shot\n→ KCs por problema\n(Tabela 8 Duan)", "#D6ECF3", "#1F618D"),
        (7.0, 2.5, 2.0, 1.4, "Etapa 3\nEmbedding semântico\nSentence-BERT\n(all-MiniLM-L6-v2)", "#E8DAEF", "#6C3483"),
        (9.8, 2.5, 2.0, 1.4, "Etapa 4\nClustering HAC\ncosine + average\nn_k via silhouette", "#D5F5E3", "#1E8449"),
        (12.6, 2.5, 2.0, 1.4, "Etapa 5\nLLM sumariza\ncluster → KC final\n(Tabela 9 Duan)", "#FADBD8", "#922B21"),
    ]
    for x, y, w, h, text, fc, ec in steps:
        _box(ax, x, y, w, h, text, fc=fc, ec=ec, fs=9, bold=True)

    for i in range(len(steps) - 1):
        x1 = steps[i][0] + steps[i][2] / 2
        x2 = steps[i + 1][0] - steps[i + 1][2] / 2
        _arrow(ax, x1, 2.5, x2, 2.5)

    # Caixa de validação post-hoc (Etapa 7) — em cima da Etapa 3
    _box(ax, 7.0, 4.7, 5.2, 0.7,
         "Etapa 7 (nossa): validação AST post-hoc via srcML",
         fc="#FFF2CC", ec="#A67C00", fs=9)
    _arrow(ax, 7.0, 3.3, 7.0, 4.3, color="#A67C00")

    # Caixa de Etapa 6 pendente — à direita, abaixo (não no topo)
    _box(ax, 12.6, 0.4, 5.2, 0.7,
         "Etapa 6 (não implementada): rotulagem de KCs em submissões incorretas (Tabela 10 Duan)",
         fc="#FADBD8", ec="#922B21", fs=9)
    _arrow(ax, 12.6, 1.7, 12.6, 0.85, color="#922B21", style="-|>")

    ax.text(7.0, -0.7,
            "Adaptado de Duan et al. (2025), Figura 1. LLM substituída: Claude Haiku (claude-haiku-4-5) em vez de GPT-4o",
            ha="center", fontsize=9, style="italic", color="#566573")

    _save(fig, "fig8_kcgen_pipeline.png")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

ALL_FIGS = {
    "f1": fig1_bkt_hmm,
    "f3": fig3_dkt_unrolled,
    "f4": fig4_ast_javalang,
    "f5": fig5_code_dkt_pipeline,
    "f6": fig6_srcml_tree,
    "f7": fig7_srcml_error,
    "f8": fig8_kcgen_pipeline,
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", nargs="*", choices=list(ALL_FIGS.keys()), default=None,
                        help="Gerar apenas as figuras listadas (ex.: --only f4 f6)")
    args = parser.parse_args()
    targets = args.only or list(ALL_FIGS.keys())
    for name in targets:
        ALL_FIGS[name]()


if __name__ == "__main__":
    main()

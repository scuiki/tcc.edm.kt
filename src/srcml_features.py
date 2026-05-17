"""
Extração de features de código para srcML-DKT (Pankiewicz, Shi & Baker, 2025).

Pipeline: código Java → srcML XML → paths AST → vocabulário → tensores.

Análogo a src/code_features.py, mas usa o CLI srcML em vez de javalang.
Vantagem: srcML parseia código não-compilável (Compile.Error events), produzindo
XML parcial em vez de falhar — aumenta cobertura vs. ~86% do javalang.

Path format (code2vec): (start_token, path_str, end_token) com path_str
"@"-separado. Mesmos filtros do Code-DKT: max_path_length=8, max_path_width=2, R=50.

O vocabulário (build_vocab), tensorização (paths_to_tensor, build_code_input_tensor)
e o modelo (CodeDKTModel) são reutilizados de code_features.py e code_dkt.py
sem alteração — apenas o extrator de paths muda.

Referência: Pankiewicz, Shi & Baker (2025). srcML-DKT, EDM 2025.
"""

from __future__ import annotations

import multiprocessing as mp
import random
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
from anytree import Node
from anytree.search import findall_by_attr
from anytree.walker import Walker

_NS_URI = "http://www.srcML.org/srcML/src"
_NS_PREFIX = "{" + _NS_URI + "}"


# ---------------------------------------------------------------------------
# Carregamento de CodeStates (idêntico ao de code_features.py)
# ---------------------------------------------------------------------------

def load_code_states(data_dir: Path) -> dict[str, str]:
    """Carrega CodeStates.csv como dict {CodeStateID: code_string}."""
    df = pd.read_csv(Path(data_dir) / "CodeStates" / "CodeStates.csv")
    return dict(zip(df["CodeStateID"].astype(str), df["Code"].fillna("")))


# ---------------------------------------------------------------------------
# Construção da anytree a partir do XML srcML
# ---------------------------------------------------------------------------

def _strip_ns(tag: str) -> str:
    """Remove prefixo de namespace srcML de uma tag XML."""
    return tag.replace(_NS_PREFIX, "")


def _srcml_token(elem: ET.Element) -> str:
    """Token de um elemento XML (análogo a _get_token para javalang).

    Folhas (sem filhos) → .text.strip() se não-vazio, senão tag local.
    Interiores → tag local (estrutura, não conteúdo textual).
    """
    tag = _strip_ns(elem.tag)
    children = list(elem)
    if not children:
        text = (elem.text or "").strip()
        return text if text else tag
    return tag


def _srcml_build_tree(elem: ET.Element, parent_node: Node, order: str) -> None:
    """Constrói anytree recursivamente a partir de XML srcML.

    Análogo a _build_tree em code_features.py, mas alimentado por ElementTree
    em vez de javalang.ast.Node.
    """
    token = _srcml_token(elem)
    node = Node([order, token], parent=parent_node, order=order)
    for i, child in enumerate(list(elem)):
        _srcml_build_tree(child, node, order + str(i + 1))


# ---------------------------------------------------------------------------
# Extração de paths AST via srcML
# ---------------------------------------------------------------------------

def extract_paths_srcml(
    code: str,
    max_path_length: int = 8,
    max_path_width: int = 2,
    R: int = 50,
    seed: int = 42,
) -> list[tuple[str, str, str]]:
    """Extrai até R paths AST do código Java via srcML CLI.

    Fiel aos filtros do Code-DKT (Shi et al., 2022):
    - Comprimento máximo (nós totais): max_path_length
    - Largura máxima: diferença inteira entre ordens dos nós filhos da LCA
    - Amostragem de R paths quando há mais disponíveis

    Diferença em relação a extract_paths_javalang: usa srcML em vez de
    javalang, tolerando código não-compilável (Compile.Error events).

    Args:
        code: string de código Java (pode ser sintaticamente inválido).
        max_path_length: máximo de nós no caminho (inclusive start e end).
        max_path_width: máxima diferença inteira entre ordens dos nós à LCA.
        R: máximo de paths a retornar.
        seed: semente para amostragem reprodutível.

    Returns:
        Lista de (start_token, path_str, end_token). Vazia se parse falhar.
    """
    if not code or not code.strip():
        return []

    try:
        result = subprocess.run(
            ["srcml", "--language=Java"],
            input=code.encode("utf-8", errors="replace"),
            capture_output=True,
            timeout=10,
        )
    except Exception:
        return []

    if not result.stdout:
        return []

    try:
        root_elem = ET.fromstring(result.stdout.decode("utf-8", errors="replace"))
    except ET.ParseError:
        return []

    children_of_unit = list(root_elem)
    if not children_of_unit:
        return []

    # Constrói anytree com <unit> como raiz virtual (order="1")
    head = Node(["1", "unit"], order="1")
    for i, child_elem in enumerate(children_of_unit):
        _srcml_build_tree(child_elem, head, "1" + str(i + 1))

    leaf_nodes = findall_by_attr(head, name="is_leaf", value=True)
    if not leaf_nodes:
        return []

    # Padding dos order strings (idêntico a code_features.py)
    max_depth = max(len(node.name[0]) for node in leaf_nodes)
    for leaf in leaf_nodes:
        while len(leaf.name[0]) < max_depth:
            leaf.name[0] += "0"
        leaf.name = [int(leaf.name[0]), leaf.name[1]]

    walker = Walker()
    paths: list[tuple[str, str, str]] = []

    for i in range(len(leaf_nodes) - 1):
        for j in range(i + 1, len(leaf_nodes)):
            try:
                upstream, lca, downstream = walker.walk(leaf_nodes[i], leaf_nodes[j])
            except Exception:
                continue

            walk_path = (
                [n.name[1] for n in upstream]
                + [lca.name[1]]
                + [n.name[1] for n in downstream]
            )

            if len(walk_path) > max_path_length:
                continue

            try:
                width = (
                    abs(int(upstream[-1].order) - int(downstream[0].order))
                    if (upstream and downstream)
                    else 0
                )
            except (ValueError, IndexError):
                continue

            if width > max_path_width:
                continue

            paths.append((walk_path[0], "@".join(walk_path), walk_path[-1]))

    if not paths:
        return []

    if len(paths) > R:
        rng = random.Random(seed)
        paths = rng.sample(paths, R)

    return paths


# ---------------------------------------------------------------------------
# Cache de paths (extração paralela via multiprocessing.Pool)
# ---------------------------------------------------------------------------

def _worker_extract_srcml(args: tuple) -> tuple[str, list]:
    """Worker picklável para multiprocessing.Pool."""
    code_state_id, code, max_path_length, max_path_width, R, seed = args
    paths = extract_paths_srcml(code, max_path_length, max_path_width, R, seed)
    return code_state_id, paths


def build_cache_srcml(
    code_state_ids: list[str],
    code_states: dict[str, str],
    max_path_length: int = 8,
    max_path_width: int = 2,
    R: int = 50,
    seed: int = 42,
    n_workers: Optional[int] = None,
) -> dict[str, list[tuple[str, str, str]]]:
    """Extrai paths para todos os CodeStateIDs via multiprocessing.Pool.

    Análogo a build_cache em code_features.py, mas usando extract_paths_srcml.

    Args:
        code_state_ids: lista de CodeStateIDs únicos a processar.
        code_states: dict {CodeStateID: code_string}.
        n_workers: número de processos worker (padrão: os.cpu_count()).

    Returns:
        dict {CodeStateID: list[tuple[str, str, str]]}.
        CodeStateIDs com parse falho mapeiam para lista vazia.
    """
    args_list = [
        (csid, code_states.get(csid, ""), max_path_length, max_path_width, R, seed)
        for csid in code_state_ids
    ]
    cache: dict[str, list] = {}
    with mp.Pool(n_workers) as pool:
        for csid, p in pool.imap_unordered(
            _worker_extract_srcml, args_list, chunksize=64
        ):
            cache[csid] = p
    return cache

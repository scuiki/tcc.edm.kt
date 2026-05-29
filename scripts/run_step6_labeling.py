"""
Passo 6 (Etapa 6 KCGen-KT) — KC Correctness Labeling, execução standalone.

Replica fielmente a célula 22 de notebooks/03b_kc_generation.ipynb:
  - mesmos prompts (Duan et al. 2025, Table 10 — adaptado)
  - mesmo formato de chave: f"{subject_id}__{pid}__{codestate_id}"
  - checkpoint por problema + resume de cache parcial
  - BudgetTracker idêntico, BUDGET_USD=9.50 / parada 9.30
  - dados: SOMENTE train, SOMENTE Run.Program incorreto (sequences_bkt_dkt.pkl)
  - ASSIGN_ORDER [502, 439, 494, 492, 487]: 502/439 já completos (0 novas),
    494 retoma de parcial, 492/487 do zero.

Saída idêntica ao notebook: results/kc_correctness_A{aid}.json
"""
from __future__ import annotations
import json, pickle, sys, time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import anthropic

REPO = Path(__file__).resolve().parents[1]
RESULTS_ROOT = REPO / "results"
DATA_ROOT = REPO / "data" / "CSEDM"
SEQUENCES_PATH = RESULTS_ROOT / "sequences_bkt_dkt.pkl"
CODE_STATES_PATH = DATA_ROOT / "CodeStates" / "CodeStates.csv"
LLM_MODEL = "claude-haiku-4-5-20251001"
ASSIGNMENTS = [439, 487, 492, 494, 502]

# ── Pricing & budget ──────────────────────────────────────────────────────────
_PRICE_INPUT       = 0.80 / 1_000_000
_PRICE_OUTPUT      = 4.00 / 1_000_000
_PRICE_CACHE_WRITE = 1.00 / 1_000_000
_PRICE_CACHE_READ  = 0.08 / 1_000_000

BUDGET_USD  = 9.50
BUDGET_STOP = 9.30   # safety margin of $0.20
ASSIGN_ORDER = [502, 439, 494, 492, 487]


@dataclass
class BudgetTracker:
    budget: float = BUDGET_STOP
    total_cost: float = 0.0
    calls: int = 0
    _tok_in: int = 0
    _tok_out: int = 0
    _tok_cw: int = 0
    _tok_cr: int = 0

    def record(self, usage) -> None:
        ti  = getattr(usage, "input_tokens",               0) or 0
        to  = getattr(usage, "output_tokens",              0) or 0
        tcw = getattr(usage, "cache_creation_input_tokens",0) or 0
        tcr = getattr(usage, "cache_read_input_tokens",    0) or 0
        self.total_cost += (ti  * _PRICE_INPUT  + to  * _PRICE_OUTPUT
                           + tcw * _PRICE_CACHE_WRITE + tcr * _PRICE_CACHE_READ)
        self.calls += 1
        self._tok_in += ti;  self._tok_out += to
        self._tok_cw += tcw; self._tok_cr  += tcr

    @property
    def over_budget(self) -> bool:
        return self.total_cost >= self.budget

    @property
    def remaining(self) -> float:
        return self.budget - self.total_cost

    def report(self) -> str:
        cpp = self.total_cost / self.calls if self.calls else 0.0
        return (f"calls={self.calls:,}  cost=${self.total_cost:.4f}  "
                f"$/call={cpp:.6f}  remaining=${self.remaining:.4f}")


_CORRECTNESS_SYSTEM = (
    "You are an expert CS educator analyzing incorrect student submissions "
    "for an introductory Java programming course. "
    "For each Knowledge Component (KC) listed, label 1 if the student FAILED "
    "to demonstrate it in the submission, 0 if demonstrated despite the error."
)


def _build_ctx(problem_id: int, description: str, kc_names: list[str]) -> str:
    return (
        f"Problem {problem_id}: {description}\n\nKCs to label:\n"
        + "\n".join(f"- {n}" for n in kc_names)
    )


def _build_code_msg(code: str, kc_names: list[str]) -> str:
    template = ", ".join(f'"{n}": <0_or_1>' for n in kc_names)
    return (
        f"Incorrect submission:\n```java\n{code[:3000]}\n```\n\n"
        'Respond ONLY with valid JSON: {"kc_errors": {' + template + "}}"
    )


def _parse_correctness(raw: str, kc_names: list[str]) -> dict[str, int]:
    for fence in ("```json", "```"):
        if fence in raw:
            raw = raw.split(fence, 1)[1].split("```", 1)[0].strip()
            break
    s, e = raw.find("{"), raw.rfind("}") + 1
    try:
        errs = json.loads(raw[s:e]).get("kc_errors", {})
        return {n: int(bool(errs.get(n, 1))) for n in kc_names}
    except (json.JSONDecodeError, ValueError, IndexError):
        return {n: 1 for n in kc_names}   # conservative: all KCs failed on parse error


def _call_llm(cached_ctx, code, kc_names, client, tracker):
    if tracker.over_budget:
        return None
    for _attempt in range(4):
        try:
            resp = client.messages.create(
                model=LLM_MODEL,
                max_tokens=512,
                system=[{"type": "text", "text": _CORRECTNESS_SYSTEM,
                         "cache_control": {"type": "ephemeral"}}],
                messages=[{"role": "user", "content": [
                    {"type": "text", "text": cached_ctx,
                     "cache_control": {"type": "ephemeral"}},
                    {"type": "text", "text": _build_code_msg(code, kc_names)},
                ]}],
            )
            tracker.record(resp.usage)
            return _parse_correctness(resp.content[0].text.strip(), kc_names)
        except (anthropic.APITimeoutError, anthropic.APIConnectionError) as _e:
            if _attempt == 3:
                raise
            _wait = 15 * (2 ** _attempt)
            print(f"    [retry {_attempt+1}/3 após {_wait}s: {type(_e).__name__}]", flush=True)
            time.sleep(_wait)


def main():
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY

    # dependências (mesma origem das células 9/15/19)
    qmatrix_all = {aid: pd.read_csv(RESULTS_ROOT / f"qmatrix_A{aid}.csv").set_index("ProblemID")
                   for aid in ASSIGNMENTS}
    kc_descriptions_all = {f"A{aid}": json.load((RESULTS_ROOT / f"kc_descriptions_A{aid}.json").open())
                           for aid in ASSIGNMENTS}
    kc_raw_all = {aid: {int(k): v for k, v in json.load((RESULTS_ROOT / f"kc_raw_A{aid}.json").open()).items()}
                  for aid in ASSIGNMENTS}

    artifact = pickle.load(open(SEQUENCES_PATH, "rb"))
    cs_df = pd.read_csv(CODE_STATES_PATH)
    code_map = dict(zip(cs_df["CodeStateID"].astype(str), cs_df["Code"]))
    del cs_df

    incorrect: dict[tuple[int, int], list[dict]] = defaultdict(list)
    for aid, seqs in artifact["train"].items():
        for seq in seqs:
            sid = str(seq["subject_id"])
            ev = seq["events"]
            for _, row in ev[ev["correct"] == 0].iterrows():
                incorrect[(int(aid), int(row["ProblemID"]))].append(
                    {"subject_id": sid, "codestate_id": str(row["CodeStateID"])}
                )

    total_incorrect = sum(len(v) for v in incorrect.values())
    print(f"[train-only] incorrect events: {total_incorrect:,}", flush=True)
    print(f"Budget: ${BUDGET_USD:.2f} (para em ${BUDGET_STOP:.2f})", flush=True)
    print(f"Ordem: {['A'+str(a) for a in ASSIGN_ORDER]}\n", flush=True)

    tracker = BudgetTracker()
    kc_correctness_all: dict[int, dict] = {}

    for assignment_id in ASSIGN_ORDER:
        aid_str = f"A{assignment_id}"
        cache_path = RESULTS_ROOT / f"kc_correctness_{aid_str}.json"

        results: dict[str, dict] = {}
        if cache_path.exists():
            _cached = json.load(cache_path.open())
            if _cached:
                results = _cached
                print(f"{aid_str}: {len(results):,} entradas em cache", flush=True)
        existing_keys = set(results.keys())

        if tracker.over_budget and not results:
            print(f"{aid_str}: orçamento esgotado — pulado", flush=True)
            break

        budget_hit = False
        new_calls = 0

        for pid in sorted({k[1] for k in incorrect if k[0] == assignment_id}):
            subs = incorrect.get((assignment_id, pid), [])
            if not subs:
                continue
            qmat = qmatrix_all[assignment_id]
            if pid not in qmat.index:
                continue
            kc_row = qmat.loc[pid]
            kc_ids = sorted(int(c.split("_")[1]) for c in kc_row.index if kc_row[c] == 1)
            descs = {d["kc_id"]: d["name"] for d in kc_descriptions_all[aid_str]}
            kc_names = [descs[i] for i in kc_ids if i in descs]
            if not kc_names:
                continue
            prob_desc = kc_raw_all.get(assignment_id, {}).get(pid, {}).get(
                "problem_description", f"Problem {pid}")
            cached_ctx = _build_ctx(pid, prob_desc, kc_names)

            n_done = n_skipped = 0
            for sub in subs:
                key = f"{sub['subject_id']}__{pid}__{sub['codestate_id']}"
                if key in existing_keys:
                    n_skipped += 1
                    continue
                if tracker.over_budget:
                    budget_hit = True
                    break
                code = code_map.get(sub["codestate_id"])
                if not code or (isinstance(code, float) and pd.isna(code)):
                    existing_keys.add(key)
                    continue
                res = _call_llm(cached_ctx, code, kc_names, client, tracker)
                if res is None:
                    budget_hit = True
                    break
                results[key] = {"kc_errors": res}
                existing_keys.add(key)
                n_done += 1
                new_calls += 1

            if n_done > 0:
                json.dump(results, cache_path.open("w"), ensure_ascii=False)
                print(f"  {aid_str} P{pid}: {n_done}/{len(subs)} novos"
                      f"{f' ({n_skipped} skip)' if n_skipped else ''}"
                      f" | {tracker.report()}", flush=True)
            if budget_hit:
                break

        kc_correctness_all[assignment_id] = results

        if new_calls == 0:
            print(f"{aid_str}: cache completo — {len(results):,} entries\n", flush=True)
            continue

        status = "PARCIAL" if budget_hit else "completo"
        print(f"  → {cache_path.name} [{status}] {len(results):,} entries ({new_calls:,} novas)\n", flush=True)
        if budget_hit:
            print(f"Orçamento atingido: ${tracker.total_cost:.4f} ≥ ${BUDGET_STOP:.2f}", flush=True)
            break

    print("\n" + "=" * 55, flush=True)
    print(f"Relatório | Budget ${BUDGET_USD:.2f} | parada ${BUDGET_STOP:.2f}", flush=True)
    print(tracker.report(), flush=True)
    if tracker.calls:
        cpp = tracker.total_cost / tracker.calls
        print(f"Custo real por chamada: ${cpp:.6f}", flush=True)
        print(f"Projeção p/ 26.289 chamadas: ${cpp * 26289:.2f}", flush=True)
    print(flush=True)
    for aid in ASSIGN_ORDER:
        n = len(kc_correctness_all.get(aid, {}))
        print(f"  A{aid}: {n:,} submissões rotuladas", flush=True)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Content Validator (Layer 3) for the TCC EDM/KT harness.

Spawns an independent Claude session that evaluates notebook quality against research
objectives — WITHOUT seeing the Generator prompts, plan JSONs, or Format Evaluator criteria.
Designed to catch content issues that format compliance cannot detect.

Usage:
    python .harness/validator.py --notebook notebooks/01_eda.ipynb
    python .harness/validator.py --all
    python .harness/validator.py --notebook notebooks/01_eda.ipynb --dry-run
"""

import argparse
import re
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CRITERIA_DIR = ROOT / ".harness" / "validation_criteria"
REPORTS_DIR = ROOT / "results" / "validation_reports"
NOTEBOOKS_DIR = ROOT / "notebooks"
CLAUDE_MD_PATH = ROOT / "CLAUDE.md"
PAPER_REFS_PATH = ROOT / "docs" / "refs" / "INDEX.md"


# ---------------------------------------------------------------------------
# Notebook → criteria mapping
# ---------------------------------------------------------------------------


def notebook_stem_to_criteria(stem: str) -> str:
    """Strip leading NN_ from notebook stem to get the criteria filename.

    Examples:
        "01_eda"              → "eda_criteria.md"
        "00_problem_definition" → "problem_definition_criteria.md"
        "02_preprocessing"    → "preprocessing_criteria.md"
    """
    clean = re.sub(r"^\d+_", "", stem)
    return f"{clean}_criteria.md"


def find_criteria_file(notebook_path: Path) -> Path | None:
    criteria_name = notebook_stem_to_criteria(notebook_path.stem)
    criteria_path = CRITERIA_DIR / criteria_name
    return criteria_path if criteria_path.exists() else None


# ---------------------------------------------------------------------------
# Context helpers
# ---------------------------------------------------------------------------


def read_file_safe(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def find_relevant_artefacts() -> list[Path]:
    """Return up to 10 results/ artefacts (non-report files)."""
    results_dir = ROOT / "results"
    if not results_dir.exists():
        return []
    return [
        p
        for p in results_dir.glob("*")
        if p.is_file()
        and p.suffix in (".csv", ".pkl", ".pt", ".json", ".txt")
        and "validation_report" not in p.name
    ][:10]


# ---------------------------------------------------------------------------
# Prompt builder (no plan JSONs, no generator prompts, no evaluator criteria)
# ---------------------------------------------------------------------------


def build_validator_prompt(notebook_path: Path, criteria_text: str) -> str:
    claude_md = read_file_safe(CLAUDE_MD_PATH)
    paper_refs = read_file_safe(PAPER_REFS_PATH)

    if paper_refs:
        paper_refs_section = textwrap.dedent(
            f"""\
            ## Paper References (docs/refs/INDEX.md)

            {paper_refs}

            For full details on a specific paper, read docs/refs/<author><year>_<topic>.md
            (e.g., docs/refs/shi2022_code_dkt.md, docs/refs/pankiewicz2025_srcml_dkt.md).
        """
        )
    else:
        paper_refs_section = textwrap.dedent(
            """\
            ## Paper References

            docs/refs/INDEX.md is not available. Evaluate based on CLAUDE.md context only;
            do not penalise for missing citations to specific paper values when the index is absent.
        """
        )

    artefacts = find_relevant_artefacts()
    if artefacts:
        artefact_list = "\n".join(f"- {p.relative_to(ROOT)}" for p in artefacts)
        artefacts_section = textwrap.dedent(
            f"""\
            ## Available Artefacts in results/

            {artefact_list}

            Read these to verify that analysis results are correctly reflected in the notebook.
        """
        )
    else:
        artefacts_section = ""

    notebook_rel = notebook_path.relative_to(ROOT)

    return textwrap.dedent(
        f"""\
        You are an independent research quality validator. You are evaluating the notebook
        `{notebook_rel}` as an external reviewer would evaluate a research paper.

        IMPORTANT: You do not have access to the implementation instructions, plan files, or
        the format evaluator's checklist. Assess the notebook purely against the research
        objectives and validation criteria below.

        ## Project Context

        {claude_md}

        {paper_refs_section}

        ## Validation Criteria

        Evaluate the notebook against each of the following research-level criteria.
        Each criterion is written in terms of research objectives, not implementation steps.

        {criteria_text}

        {artefacts_section}

        ## Instructions

        1. Read the notebook at `{notebook_rel}` (Jupyter notebook in JSON format).
        2. Read any relevant artefacts listed above.
        3. For each validation criterion:
           a. Find the relevant cells or sections in the notebook.
           b. Assess whether the criterion is met, with specific evidence (cell content,
              numbers found, markdown text).
           c. If a value diverges from a paper value, check whether the notebook explains
              the divergence. A explained divergence is acceptable; an unexplained one is not.
        4. Write a detailed validation report following the format below.

        ## Report Format

        Your response IS the validation report — it will be saved verbatim.
        The very first line must be the STATUS line:

        STATUS: PASS|CRITICAL_ISSUES|MINOR_ISSUES

        Then structure your report as follows:

        ## Summary

        One paragraph overall assessment.

        ## Criteria Evaluation

        For each criterion: assessment with specific evidence.
        Mark each as one of: [PASS], [MINOR], [CRITICAL].

        ## Recommendations

        Specific actionable recommendations (if any issues found).

        ## Verdict

        Repeat the STATUS line as the last line of the report.

        ---

        Definitions:
        - PASS: All or nearly all criteria met; any divergences from papers are explained.
        - MINOR_ISSUES: Some criteria partially met but nothing fundamentally wrong with
          the research integrity of the notebook.
        - CRITICAL_ISSUES: Key research claims are unverifiable, statistics appear to be
          invented or hardcoded, required analyses are missing, or divergences from paper
          values are unexplained and analytically suspicious.
    """
    )


# ---------------------------------------------------------------------------
# Validation runner
# ---------------------------------------------------------------------------


def run_validation(notebook_path: Path, dry_run: bool = False) -> tuple[str, int]:
    """Validate one notebook. Returns (status, exit_code)."""
    if not notebook_path.exists():
        print(f"Notebook not found: {notebook_path}")
        return "CRITICAL_ISSUES", 1

    criteria_file = find_criteria_file(notebook_path)
    if not criteria_file:
        expected = CRITERIA_DIR / notebook_stem_to_criteria(notebook_path.stem)
        print(f"No criteria file for {notebook_path.name}")
        print(f"Expected at: {expected.relative_to(ROOT)}")
        return "CRITICAL_ISSUES", 1

    criteria_text = criteria_file.read_text(encoding="utf-8")
    prompt = build_validator_prompt(notebook_path, criteria_text)

    if dry_run:
        print(f"\n[dry-run] Validator prompt for {notebook_path.name}:")
        print("=" * 60)
        print(prompt)
        print("=" * 60)
        # Confirm the prompt doesn't contain plan JSON content
        suspicious = ["verify_cmd", "slug", "depends_on", "\"tasks\""]
        found = [s for s in suspicious if s in prompt]
        if found:
            print(f"\n[dry-run] WARNING: prompt may contain plan JSON content: {found}")
        else:
            print(
                "\n[dry-run] OK: prompt does not appear to contain plan JSON or generator instructions."
            )
        return "PASS", 0

    print(f"\n── Validating: {notebook_path.name} ──")

    result = subprocess.run(
        [
            "claude",
            "-p",
            prompt,
            "--allowedTools",
            "Read,Glob,Grep",
            "--output-format",
            "text",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    raw_output = result.stdout or ""
    if result.returncode != 0:
        print(f"Claude session failed (exit code {result.returncode})")
        if result.stderr:
            print(result.stderr[:2000])
        return "CRITICAL_ISSUES", 1

    status_match = re.search(
        r"^STATUS:\s*(PASS|CRITICAL_ISSUES|MINOR_ISSUES)", raw_output, re.MULTILINE
    )
    status = status_match.group(1) if status_match else "CRITICAL_ISSUES"

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_name = f"{notebook_path.stem}_validation.md"
    report_path = REPORTS_DIR / report_name
    report_path.write_text(raw_output, encoding="utf-8")

    rel_report = report_path.relative_to(ROOT)
    print(f"Report written: {rel_report}")
    print(f"Status: {status}")

    exit_code = 0 if status in ("PASS", "MINOR_ISSUES") else 1
    return status, exit_code


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Content Validator (Layer 3) — independent research quality check.\n"
            "Runs a Claude session blind to implementation details."
        )
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--notebook", metavar="PATH", help="Notebook to validate")
    group.add_argument(
        "--all", action="store_true", help="Validate all notebooks with criteria files"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the validator prompt without running Claude",
    )
    args = parser.parse_args()

    if args.notebook:
        notebook_path = Path(args.notebook)
        if not notebook_path.is_absolute():
            notebook_path = ROOT / notebook_path
        _, exit_code = run_validation(notebook_path, dry_run=args.dry_run)
        sys.exit(exit_code)

    # --all: discover notebooks that have matching criteria files
    notebooks = sorted(NOTEBOOKS_DIR.glob("*.ipynb"))
    if not notebooks:
        print(f"No notebooks found in {NOTEBOOKS_DIR.relative_to(ROOT)}")
        sys.exit(1)

    eligible = [nb for nb in notebooks if find_criteria_file(nb) is not None]
    if not eligible:
        print(
            "No notebooks found with matching criteria files in"
            f" {CRITERIA_DIR.relative_to(ROOT)}"
        )
        sys.exit(1)

    print(f"Found {len(eligible)} notebook(s) to validate.")
    results: list[tuple[str, str, int]] = []

    for nb in eligible:
        status, code = run_validation(nb, dry_run=args.dry_run)
        results.append((nb.name, status, code))

    print(f"\n{'='*50}")
    print("Validation Summary")
    print(f"{'='*50}")
    overall_exit = 0
    for name, status, code in results:
        mark = "[ok]" if code == 0 else "[!!]"
        print(f"  {mark} {name}: {status}")
        if code != 0:
            overall_exit = 1

    sys.exit(overall_exit)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Format Evaluator (Layer 2) for the TCC EDM/KT harness.

Spawns a separate Claude Code session that checks STRUCTURAL FORMAT compliance only.
Does NOT evaluate content quality, statistical correctness, or research validity.

Usage:
    python .harness/evaluator.py --plan .harness/plans/eda.json --task 3
    python .harness/evaluator.py --plan .harness/plans/eda.json --task 3 --verbose
"""

import argparse
import json
import re
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FEEDBACK_DIR = ROOT / ".harness" / "eval_feedback"

SOURCE_DIRS: list[str] = ["notebooks/", "src/"]


def load_plan(plan_path: Path) -> dict:
    return json.loads(plan_path.read_text())


def find_task(plan: dict, task_id: str):
    for task in plan["tasks"]:
        if task["id"] == task_id:
            return plan, task
    return None, None


def build_ac_section(task: dict) -> str:
    acs = task.get("acceptance_criteria", [])
    if not acs:
        return textwrap.dedent(
            """\
            ## Acceptance Criteria

            This task has no explicit acceptance criteria.
            Mark acceptance_criteria: N/A in the verdict.
        """
        )
    ac_list = "\n".join(f"- {ac}" for ac in acs)
    return textwrap.dedent(
        f"""\
        ## Acceptance Criteria to Verify

        For each criterion below, check whether the notebook or source file contains evidence
        that it is satisfied. Do NOT assess quality — check presence and basic correctness only.

        {ac_list}
    """
    )


def build_eval_prompt(plan: dict, task: dict) -> str:
    ac_section = build_ac_section(task)
    context_line = f"This is part of: {plan['title']} ({plan['slug']})"
    source_dirs_str = ", ".join(f"`{d}`" for d in SOURCE_DIRS)
    files_list = "\n".join(f"- {f}" for f in task.get("files", []))

    return textwrap.dedent(
        f"""\
        You are a structural format evaluator. Your job is to check FORMAT COMPLIANCE only
        for task {task["id"]}: {task["title"]}

        {context_line}

        ## Your Scope (FORMAT ONLY)

        Evaluate ONLY structural and format compliance. Do NOT assess:
        - Content quality or analytical depth
        - Statistical correctness or numerical values
        - Research validity or interpretation quality

        When in doubt about a format criterion, mark FAIL — false positives are preferable
        to missing real format violations.

        ## Files to examine

        {files_list}

        Also search in {source_dirs_str} for any source modules touched by this task.

        ## Evaluation Steps (do IN ORDER, do not skip)

        ### Step 1: Check notebook_executes
        Read the notebook JSON file(s) listed above. Look for cells where the outputs list
        contains an element with `"output_type": "error"`.
        - If any such cell exists → notebook_executes: FAIL
        - If no error outputs are found → notebook_executes: PASS
        (The runner already executed the notebook; you are checking the stored cell outputs.)

        ### Step 2: Check template_compliance
        For each analytical section (a code cell that performs data analysis or modelling):
        a) Is there a markdown cell before the code containing ALL of:
           - **Contexto:** (explains why this analysis matters for the KT problem)
           - **Hipótese:** (what we expect to find based on papers)
           - **Referência:** (at least one paper citation in "Author (year)" format)
        b) Is there a markdown cell after the code containing ALL of:
           - **Achado:** (quantitative result)
           - **Implicação para modelagem:** (impact on BKT/DKT/Code-DKT)

        Scoring:
        - ALL analytical sections satisfy both a) and b) → PASS
        - ≤30% of sections missing some elements → WARN
        - >30% of sections missing elements → FAIL

        ### Step 3: Check no_placeholders
        Search code cells in the notebook and source files in {source_dirs_str} for:
        - `TODO` or `FIXME` in any comment
        - `pass` as the sole statement of a function body
        - `NotImplementedError` anywhere
        - `...` used as an Ellipsis placeholder in a function body
        Any occurrence → no_placeholders: FAIL

        ### Step 4: Check SEED=42 where applicable
        If the task involves random operations (clustering, train/test split, sampling):
        does `SEED = 42` or `random_state=42` or `np.random.seed(42)` or `torch.manual_seed`
        appear in the relevant code cells? If not present when expected → add to issues list
        (does not cause OVERALL FAIL on its own, but note it).

        ### Step 5: Verify acceptance criteria
        {ac_section}
        For each AC, find the specific cell or code that implements it.
        Check: is the required element present? Does it match the AC description?

        ## Output Format

        End your response with EXACTLY this block. The runner's parser reads it literally.

        VERDICT
        task: {task["id"]}
        title: {task["title"]}

        notebook_executes: PASS|FAIL
        acceptance_criteria: PASS|FAIL|N/A
        template_compliance: PASS|FAIL|WARN
        no_placeholders: PASS|FAIL

        ac_checklist:
        - [x] AC text (PASS)
        - [ ] AC text (FAIL — what is missing)

        issues:
        - Issue description 1
        - Issue description 2

        OVERALL: PASS|FAIL

        ## Scoring Rules

        - OVERALL = FAIL if ANY of these is FAIL: notebook_executes, acceptance_criteria,
          no_placeholders
        - template_compliance: WARN does NOT cause OVERALL FAIL (recorded as warning only)
        - acceptance_criteria: N/A does not affect OVERALL
        - When in doubt, mark FAIL
    """
    )


def parse_verdict(output: str) -> dict:
    verdict_match = re.search(r"VERDICT\s*\n(.+?)$", output, re.DOTALL)
    if not verdict_match:
        return {
            "overall": "FAIL",
            "parse_error": "Could not find VERDICT block in evaluator output",
            "issues": ["VERDICT block missing from evaluator output"],
        }

    verdict_text = verdict_match.group(1)

    overall_match = re.search(r"OVERALL:\s*(PASS|FAIL)", verdict_text)
    overall = overall_match.group(1) if overall_match else "FAIL"

    result: dict = {"overall": overall}
    for field in [
        "notebook_executes",
        "acceptance_criteria",
        "template_compliance",
        "no_placeholders",
    ]:
        match = re.search(rf"{field}:\s*(PASS|FAIL|WARN|N/A)", verdict_text)
        result[field] = match.group(1) if match else "UNKNOWN"

    issues: list[str] = []
    issues_match = re.search(r"issues:\s*\n((?:- .+\n?)+)", verdict_text)
    if issues_match:
        issues = [
            line.lstrip("- ").strip()
            for line in issues_match.group(1).strip().split("\n")
            if line.strip().startswith("-")
        ]
    result["issues"] = issues

    return result


def print_verdict(verdict: dict, task_id: str, verbose: bool, raw_output: str) -> None:
    if verbose:
        print(raw_output)
        print()

    overall = verdict["overall"]
    icon = "PASS" if overall == "PASS" else "FAIL"
    print(f"\n{'='*50}")
    print(f"  Evaluator Verdict: {icon}  (task {task_id})")
    print(f"{'='*50}")

    for field in [
        "notebook_executes",
        "acceptance_criteria",
        "template_compliance",
        "no_placeholders",
    ]:
        val = verdict.get(field, "UNKNOWN")
        if val in ("PASS", "N/A"):
            mark = "[ok]"
        elif val == "FAIL":
            mark = "[!!]"
        elif val == "WARN":
            mark = "[~~]"
        else:
            mark = "[??]"
        print(f"  {mark} {field}: {val}")

    issues = verdict.get("issues", [])
    if issues:
        print(f"\n  Issues ({len(issues)}):")
        for issue in issues:
            print(f"    - {issue}")

    if "parse_error" in verdict:
        print(f"\n  Parse error: {verdict['parse_error']}")

    print()


def main():
    parser = argparse.ArgumentParser(
        description="Format evaluator (Layer 2) for TCC EDM/KT harness"
    )
    parser.add_argument("--task", required=True, help="Task ID to evaluate (e.g., 3)")
    parser.add_argument("--plan", required=True, help="Path to plan JSON file")
    parser.add_argument(
        "--verbose", action="store_true", help="Show full evaluator output"
    )
    args = parser.parse_args()

    plan_path = Path(args.plan)
    if not plan_path.is_absolute():
        plan_path = ROOT / plan_path

    if not plan_path.exists():
        print(f"Plan file not found: {plan_path}")
        sys.exit(1)

    plan = load_plan(plan_path)
    _, task = find_task(plan, args.task)

    if not task:
        print(f"Task {args.task} not found in plan.")
        sys.exit(1)

    print(f"\n── Evaluating task {task['id']}: {task['title']} ──")

    prompt = build_eval_prompt(plan, task)

    result = subprocess.run(
        [
            "claude",
            "-p",
            prompt,
            "--model", "claude-sonnet-4-6",
            "--allowedTools",
            "Bash,Read,Glob,Grep",
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
        sys.exit(1)

    verdict = parse_verdict(raw_output)
    print_verdict(verdict, args.task, verbose=args.verbose, raw_output=raw_output)

    FEEDBACK_DIR.mkdir(exist_ok=True)
    feedback_path = FEEDBACK_DIR / f"{plan['slug']}_{args.task}.json"
    feedback_path.write_text(json.dumps(verdict, indent=2) + "\n")

    sys.exit(0 if verdict["overall"] == "PASS" else 1)


if __name__ == "__main__":
    main()

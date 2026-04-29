#!/usr/bin/env python3
"""
Headless agent runner for the TCC EDM/KT harness.

Orchestrates Claude Code sessions to implement notebook tasks from per-plan JSON files,
then runs verification (notebook execution) and format evaluation.

Usage:
    python .harness/runner.py --plan .harness/plans/eda.json
    python .harness/runner.py --plan .harness/plans/eda.json --loop
    python .harness/runner.py --plan .harness/plans/eda.json --task 3
    python .harness/runner.py --plan .harness/plans/eda.json --dry-run
    python .harness/runner.py --plan .harness/plans/eda.json --skip-eval
    python .harness/runner.py --plan .harness/plans/eda.json --eval-only 3
    python .harness/runner.py --plan .harness/plans/eda.json --fix 3
"""

import argparse
import json
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROGRESS_PATH = ROOT / ".harness" / "progress.md"
FEEDBACK_DIR = ROOT / ".harness" / "eval_feedback"

MAX_RETRIES = 2

CLAUDE_MD_PATH: str = "CLAUDE.md"
SOURCE_DIRS: list[str] = ["notebooks/", "src/"]


# ---------------------------------------------------------------------------
# Plan I/O
# ---------------------------------------------------------------------------


def load_plan(plan_path: Path) -> dict:
    return json.loads(plan_path.read_text())


def save_plan(plan: dict, plan_path: Path) -> None:
    plan_path.write_text(json.dumps(plan, indent=2) + "\n")


# ---------------------------------------------------------------------------
# Task finding
# ---------------------------------------------------------------------------


def find_next_task(plan: dict, task_id: str | None = None):
    """Return (plan, task) for the next pending task, respecting depends_on."""
    for task in plan["tasks"]:
        if task_id and task["id"] != task_id:
            continue
        if task["status"] == "pending":
            deps = task.get("depends_on", [])
            if deps:
                all_done = all(
                    any(t["id"] == dep and t["status"] == "complete" for t in plan["tasks"])
                    for dep in deps
                )
                if not all_done:
                    continue
            return plan, task
    return None, None


def find_task(plan: dict, task_id: str):
    """Find any task by ID regardless of status."""
    for task in plan["tasks"]:
        if task["id"] == task_id:
            return plan, task
    return None, None


# ---------------------------------------------------------------------------
# Prompt building
# ---------------------------------------------------------------------------


def build_prompt(plan: dict, task: dict, plan_path: Path) -> str:
    ac_text = "\n".join(f"- {ac}" for ac in task.get("acceptance_criteria", []))
    files_text = "\n".join(f"- {f}" for f in task.get("files", []))
    verify_cmd = plan.get("verify_cmd", [])
    verify_cmd_str = " ".join(verify_cmd)
    source_dirs_str = ", ".join(f"`{d}`" for d in SOURCE_DIRS)

    return textwrap.dedent(
        f"""\
        You are implementing task {task["id"]}: {task["title"]}

        This is part of: {plan["title"]} ({plan["slug"]})
        Type: {plan["type"]}
        Context: {plan.get("context", "")}

        ## Acceptance Criteria

        {ac_text}

        ## Files likely affected

        {files_text}

        ## Instructions — Read in order before implementing

        1. Read {CLAUDE_MD_PATH} for project rules (SEED=42, Release/ split, BKT/DKT/Code-DKT protocol).
        2. Read docs/paper_references.md for citations to include in markdown cells (if the file exists).
        3. Check `git log --oneline -10` to understand recent changes.
        4. Search in {source_dirs_str} before implementing — functions may already exist in src/.
        5. For REVISION of existing notebook sections: keep the correct analytical content, add or
           adjust markdown cells to follow the didactic template (Contexto, Hipótese, Referência /
           Achado, Implicação para modelagem).
        6. For NEW notebook sections: write the pre-code markdown cell first (Contexto, Hipótese,
           Referência), then the code cell, then the post-code markdown cell (Achado, Implicação).
        7. Do NOT invent statistics — calculate from the dataset. If a value diverges from a paper,
           explain the divergence explicitly in the markdown cell.
        8. No placeholders — every function fully implemented: no `pass`, `TODO`, `NotImplementedError`.
        9. Run `{verify_cmd_str}` to verify the notebook executes without errors.
        10. Mark task {task["id"]} as "complete" in {plan_path.relative_to(ROOT)}.
        11. Commit your changes with a descriptive message.
        12. Append session notes to .harness/progress.md following the established format.

        ## Required Didactic Template (every analytical section)

        Pre-code markdown cell:
        ```
        ### N.X — Section Title

        **Contexto:** Why this analysis matters for the KT problem.
        **Hipótese:** What we expect to find based on the papers.
        **Referência:** Author (year); Author (year).
        ```

        Post-code markdown cell:
        ```
        **Achado:** [main quantitative result — must be calculated, not hardcoded]
        **Implicação para modelagem:** How this finding affects BKT/DKT/Code-DKT choice.
        ```

        ## Task Focus

        Implement ONLY task {task["id"]}: {task["title"]}
        Do NOT work on other tasks. Note bugs or dataset inconsistencies in progress.md instead.
    """
    )


def build_fix_prompt(plan: dict, task: dict, feedback: dict, plan_path: Path) -> str:
    issues_text = "\n".join(f"- {issue}" for issue in feedback.get("issues", []))
    ac_text = "\n".join(f"- {ac}" for ac in task.get("acceptance_criteria", []))
    verify_cmd = plan.get("verify_cmd", [])
    verify_cmd_str = " ".join(verify_cmd)

    return textwrap.dedent(
        f"""\
        You are fixing issues flagged by the evaluator for task {task["id"]}: {task["title"]}

        This is part of: {plan["title"]} ({plan["slug"]})

        ## Evaluator Feedback

        The evaluator found the following issues:

        {issues_text}

        Verdict summary:
        - notebook_executes: {feedback.get("notebook_executes", "UNKNOWN")}
        - acceptance_criteria: {feedback.get("acceptance_criteria", "UNKNOWN")}
        - template_compliance: {feedback.get("template_compliance", "UNKNOWN")}
        - no_placeholders: {feedback.get("no_placeholders", "UNKNOWN")}

        ## Acceptance Criteria

        {ac_text}

        ## Instructions

        1. Read {CLAUDE_MD_PATH} for project context.
        2. Read the plan at {plan_path.relative_to(ROOT)}.
        3. Fix EACH issue listed above. Do not skip any.
        4. Run `{verify_cmd_str}` to verify the notebook executes without errors after your fix.
        5. Commit your fixes with a descriptive message.
        6. Append a note about what you fixed to .harness/progress.md.

        ## Task Focus

        Fix ONLY the issues listed above for task {task["id"]}: {task["title"]}
        Do NOT work on other tasks or refactor unrelated code.
    """
    )


def build_verify_fix_prompt(
    task: dict, check_output: str, context_name: str, verify_cmd: list[str]
) -> str:
    max_chars = 4000
    if len(check_output) > max_chars:
        check_output = "...(truncated)...\n" + check_output[-max_chars:]
    verify_cmd_str = " ".join(verify_cmd)

    return textwrap.dedent(
        f"""\
        You are fixing notebook execution failures for task {task["id"]}: {task["title"]}

        This is part of {context_name}.

        ## Execution Output

        `{verify_cmd_str}` failed with the following output:

        ```
        {check_output}
        ```

        ## Instructions

        1. Read {CLAUDE_MD_PATH} for project context.
        2. Analyze the errors above — identify which cells failed and why.
        3. Fix EACH failure. Common causes:
           - Import errors: add missing imports.
           - NameError: variable or function not defined — check cell execution order.
           - FileNotFoundError: check data paths against CSEDM dataset structure.
           - ValueError/TypeError: check data types and column names against CLAUDE.md.
        4. Run `{verify_cmd_str}` to verify the notebook now executes without errors.
        5. Commit your fixes with a descriptive message.

        ## Task Focus

        Fix ONLY the execution failures for task {task["id"]}: {task["title"]}
        Do NOT work on other tasks or refactor unrelated code.
    """
    )


# ---------------------------------------------------------------------------
# Execution helpers
# ---------------------------------------------------------------------------


def load_eval_feedback(task_id: str, slug: str | None = None) -> dict | None:
    if slug:
        feedback_path = FEEDBACK_DIR / f"{slug}_{task_id}.json"
        if feedback_path.exists():
            return json.loads(feedback_path.read_text())
    feedback_path = FEEDBACK_DIR / f"{task_id}.json"
    if feedback_path.exists():
        return json.loads(feedback_path.read_text())
    return None


def run_verification(verify_cmd: list[str]) -> tuple[bool, str]:
    cmd_str = " ".join(verify_cmd)
    print(f"\n── Verification: {cmd_str} ──")
    result = subprocess.run(
        verify_cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    output = (result.stdout or "") + (result.stderr or "")
    if output.strip():
        print(output)
    return result.returncode == 0, output


def run_evaluator(task_id: str, plan_path: Path, verbose: bool = False) -> bool:
    print(f"\n── Evaluator: task {task_id} ──")
    cmd = [
        sys.executable,
        str(ROOT / ".harness" / "evaluator.py"),
        "--task", task_id,
        "--plan", str(plan_path),
    ]
    if verbose:
        cmd.append("--verbose")
    result = subprocess.run(cmd, cwd=ROOT, capture_output=False)
    return result.returncode == 0


def run_claude_session(prompt: str) -> int:
    print("\n── Launching Claude Code session ──")
    result = subprocess.run(
        [
            "claude", "-p", prompt,
            "--allowedTools", "Bash,Read,Edit,Write,Glob,Grep,NotebookEdit",
        ],
        cwd=ROOT,
        capture_output=False,
    )
    return result.returncode


def update_plan_status(plan: dict) -> None:
    tasks = plan.get("tasks", [])
    if all(t["status"] == "complete" for t in tasks):
        plan["status"] = "complete"
    elif any(t["status"] in ("in_progress", "complete") for t in tasks):
        plan["status"] = "in_progress"


def print_status(plan: dict) -> None:
    done = sum(1 for t in plan["tasks"] if t["status"] == "complete")
    total = len(plan["tasks"])
    status = "DONE" if done == total else f"{done}/{total}"
    print(f"  {plan['slug']}: {plan['title']} [{status}]")


# ---------------------------------------------------------------------------
# Fix mode (manual retry after human review)
# ---------------------------------------------------------------------------


def run_fix_mode(plan: dict, plan_path: Path, task_id: str, verbose: bool) -> None:
    """Load saved eval feedback for task_id, run fix generator, verify, evaluate."""
    _, task = find_task(plan, task_id)
    if not task:
        print(f"Task {task_id} not found in plan.")
        sys.exit(1)

    slug = plan.get("slug")
    feedback = load_eval_feedback(task_id, slug=slug)
    if not feedback or not feedback.get("issues"):
        print(f"No feedback found for task {task_id} (slug={slug}). Run evaluator first.")
        sys.exit(1)

    print(f"\n── Fix mode: task {task_id}: {task['title']} ──")
    fix_prompt = build_fix_prompt(plan, task, feedback, plan_path)
    fix_exit = run_claude_session(fix_prompt)
    if fix_exit != 0:
        print(f"\nFix session exited with code {fix_exit}")
        sys.exit(1)

    verify_cmd = plan.get("verify_cmd", [])
    if verify_cmd:
        verify_passed, check_output = run_verification(verify_cmd)
        if not verify_passed:
            print("\nVerification failed after fix.")
            sys.exit(1)

    eval_passed = run_evaluator(task_id, plan_path, verbose=verbose)
    if eval_passed:
        task["status"] = "complete"
        update_plan_status(plan)
        save_plan(plan, plan_path)
        print(f"\nTask {task_id} fixed and marked complete.")
    else:
        print(f"\nEvaluator still failing after fix. Task NOT marked complete.")
        sys.exit(1)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Agent harness runner for TCC EDM/KT notebooks"
    )
    parser.add_argument("--plan", required=True, help="Path to plan JSON file")
    parser.add_argument("--task", help="Run a specific task by ID (e.g., 3)")
    parser.add_argument(
        "--dry-run", action="store_true", help="Print prompt without executing"
    )
    parser.add_argument(
        "--skip-eval", action="store_true", help="Skip evaluator after task"
    )
    parser.add_argument(
        "--loop", action="store_true", help="Keep running tasks until all done"
    )
    parser.add_argument(
        "--eval-only",
        metavar="TASK_ID",
        help="Run evaluator on a task without running the generator",
    )
    parser.add_argument(
        "--fix",
        metavar="TASK_ID",
        help="Manual fix retry: load last eval feedback and re-run generator for task",
    )
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

    # --eval-only: run evaluator on existing task, no generation
    if args.eval_only:
        _, task = find_task(plan, args.eval_only)
        if not task:
            print(f"Task {args.eval_only} not found in plan.")
            sys.exit(1)
        passed = run_evaluator(args.eval_only, plan_path, verbose=args.verbose)
        sys.exit(0 if passed else 1)

    # --fix: manual retry using saved eval feedback
    if args.fix:
        run_fix_mode(plan, plan_path, args.fix, verbose=args.verbose)
        sys.exit(0)

    verify_cmd = plan.get("verify_cmd", [])
    if not verify_cmd:
        print("Warning: plan has no verify_cmd. Verification step will be skipped.")

    while True:
        _, task = find_next_task(plan, task_id=args.task)
        context_name = f"{plan['title']} ({plan['slug']})"

        if not task:
            print("No pending tasks found.")
            break

        task_label = f"Task {task['id']}: {task['title']}"
        print(f"\n{'='*60}")
        print(task_label)
        print(f"Context: {context_name}")
        print(f"{'='*60}")

        if args.dry_run:
            print("\n[dry-run] Would execute this task. Prompt:")
            print(build_prompt(plan, task, plan_path))
            if not args.loop:
                break
            task["status"] = "complete"
            continue

        task["status"] = "in_progress"
        save_plan(plan, plan_path)

        prompt = build_prompt(plan, task, plan_path)
        exit_code = run_claude_session(prompt)

        if exit_code != 0:
            print(f"\nClaude session exited with code {exit_code}")
            task["status"] = "pending"
            save_plan(plan, plan_path)
            sys.exit(1)

        # Verification loop
        if verify_cmd:
            verify_passed, check_output = run_verification(verify_cmd)
            verify_retries = 0

            while not verify_passed and verify_retries < MAX_RETRIES:
                verify_retries += 1
                print(f"\n── Verify retry {verify_retries}/{MAX_RETRIES} ──")
                fix_prompt = build_verify_fix_prompt(
                    task, check_output, context_name, verify_cmd
                )
                fix_exit = run_claude_session(fix_prompt)
                if fix_exit != 0:
                    print(f"\nFix session exited with code {fix_exit}")
                    break
                verify_passed, check_output = run_verification(verify_cmd)

            if not verify_passed:
                print(
                    f"\nVerification still failing after {verify_retries} retries."
                    " Task NOT marked complete."
                )
                task["status"] = "pending"
                save_plan(plan, plan_path)
                sys.exit(1)

        # Evaluator loop
        if not args.skip_eval:
            eval_passed = run_evaluator(task["id"], plan_path, verbose=args.verbose)
            retries = 0
            slug = plan.get("slug")

            while not eval_passed and retries < MAX_RETRIES:
                retries += 1
                print(
                    f"\n── Retry {retries}/{MAX_RETRIES}:"
                    " feeding evaluator issues back to generator ──"
                )

                feedback = load_eval_feedback(task["id"], slug=slug)
                if not feedback or not feedback.get("issues"):
                    print("No actionable feedback found. Cannot retry.")
                    break

                fix_prompt = build_fix_prompt(plan, task, feedback, plan_path)
                fix_exit = run_claude_session(fix_prompt)
                if fix_exit != 0:
                    print(f"\nFix session exited with code {fix_exit}")
                    break

                if verify_cmd:
                    verify_ok, _ = run_verification(verify_cmd)
                    if not verify_ok:
                        print("\nVerification failed after fix attempt.")
                        break

                eval_passed = run_evaluator(task["id"], plan_path, verbose=args.verbose)

            if not eval_passed:
                print(
                    f"\nEvaluator still failing after {retries} retries."
                    " Task NOT marked complete."
                )
                task["status"] = "pending"
                save_plan(plan, plan_path)
                sys.exit(1)

        task["status"] = "complete"
        update_plan_status(plan)
        save_plan(plan, plan_path)
        print(f"\nTask {task['id']} completed successfully.")

        # Reload plan in case the agent modified it
        plan = load_plan(plan_path)

        if not args.loop:
            break
        if args.task:
            break

    plan = load_plan(plan_path)
    print_status(plan)


if __name__ == "__main__":
    main()

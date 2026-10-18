"""Multi-Lab & Multi-File Workspace Management and Verification Engine.
Compliant with ISO/IEC/IEEE 29148:2018 (SPEC-TERMLEARN-LAB-2026-V1) and RFC 2119.
"""
from __future__ import annotations

import difflib
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

DENYLIST = ["rm -rf", "curl", "wget", "ssh", "mkfs", ":(){", "shutdown", "reboot"]
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def get_labs_base_dir() -> Path:
    """Returns the base directory for lab workspaces."""
    return PROJECT_ROOT / "labs"


def get_lab_dir(book: str, chapter: str, lab_id: str) -> Path:
    """Returns the physical workspace directory for a specific lab (REQ-LAB-DIR-001)."""
    return get_labs_base_dir() / book / chapter / lab_id


def is_safe_path(rel_path: str) -> bool:
    """Verifies that a relative file path does not escape the workspace."""
    p = Path(rel_path)
    if p.is_absolute():
        return False
    parts = p.parts
    if ".." in parts:
        return False
    return True


def scan_command_denylist(command: str) -> list[str]:
    """Scans command string for dangerous shell patterns (REQ-LAB-EXE-007)."""
    return [b for b in DENYLIST if b in (command or "")]


def provision_lab_workspace(book: str, chapter: str, lab_def: dict[str, Any],
                            reset: bool = False) -> Path:
    """Provisions a multi-file lab workspace on disk (REQ-LAB-DIR-002..005).

    - If workspace does not exist, creates it and writes all initial files.
    - If reset is True, re-writes all initial files declared in lab_def.
    - If workspace exists and reset is False, existing student modifications are preserved.
    """
    lab_id = str(lab_def.get("id", "lab1"))
    lab_dir = get_lab_dir(book, chapter, lab_id)
    lab_dir.mkdir(parents=True, exist_ok=True)

    files = lab_def.get("files", [])
    for file_info in files:
        rel_path = str(file_info.get("path", "")).strip()
        if not rel_path or not is_safe_path(rel_path):
            continue
        dest_file = lab_dir / rel_path
        dest_file.parent.mkdir(parents=True, exist_ok=True)

        # Write if missing or reset requested (REQ-LAB-DIR-004)
        if reset or not dest_file.exists():
            dest_file.write_text(file_info.get("content", ""), encoding="utf-8")

    return lab_dir


def list_workspace_files(workspace_dir: Path) -> list[str]:
    """Lists relative paths of all regular files in the workspace, sorted."""
    if not workspace_dir.exists():
        return []
    rel_files = []
    for root, _, filenames in os.walk(workspace_dir):
        for fname in filenames:
            # Skip hidden files and build binaries / object files
            if fname.startswith(".") or fname.endswith((".o", ".out", ".bin", ".exe")):
                continue
            full_path = Path(root) / fname
            rel_files.append(str(full_path.relative_to(workspace_dir)))
    return sorted(rel_files)


def read_workspace_file(workspace_dir: Path, rel_path: str) -> str:
    """Reads content of a workspace file."""
    if not is_safe_path(rel_path):
        raise ValueError(f"Unsafe path: {rel_path}")
    p = workspace_dir / rel_path
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8", errors="replace")


def write_workspace_file(workspace_dir: Path, rel_path: str, content: str) -> None:
    """Writes content to a workspace file."""
    if not is_safe_path(rel_path):
        raise ValueError(f"Unsafe path: {rel_path}")
    p = workspace_dir / rel_path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def run_command_in_workspace(workspace_dir: Path, command: str, stdin: str = "",
                             timeout_s: int = 5) -> dict[str, Any]:
    """Executes a shell command with cwd set to the workspace directory (REQ-LAB-EXE-001..003)."""
    res = {
        "command": command,
        "stdout": "",
        "stderr": "",
        "returncode": -1,
        "elapsed_ms": 0,
        "timed_out": False,
        "denied": False,
        "error": ""
    }

    hits = scan_command_denylist(command)
    if hits:
        res["denied"] = True
        res["error"] = f"Command rejected: contains prohibited pattern(s): {', '.join(hits)}"
        return res

    workspace_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()

    try:
        proc = subprocess.run(
            command,
            input=stdin,
            capture_output=True,
            text=True,
            shell=True,
            cwd=str(workspace_dir),
            timeout=timeout_s
        )
        elapsed_ms = int((time.perf_counter() - t0) * 1000)
        res["stdout"] = proc.stdout
        res["stderr"] = proc.stderr
        res["returncode"] = proc.returncode
        res["elapsed_ms"] = elapsed_ms
    except subprocess.TimeoutExpired as exc:
        res["timed_out"] = True
        res["stdout"] = exc.stdout or "" if isinstance(exc.stdout, str) else ""
        res["stderr"] = exc.stderr or "" if isinstance(exc.stderr, str) else ""
        res["error"] = f"Execution timed out after {timeout_s}s"
        res["elapsed_ms"] = timeout_s * 1000
    except Exception as exc:
        res["error"] = str(exc)

    return res


def run_lab_verification(workspace_dir: Path, lab_def: dict[str, Any]) -> dict[str, Any]:
    """Executes the full correctness verification suite for a lab (REQ-LAB-EXE-004..005).

    Evaluates:
    1. Primary test command (`commands.test`) if defined.
    2. Input vs. Expected Output test cases (`test_cases`) with unified diffing.
    """
    commands = lab_def.get("commands", {})
    test_cases = lab_def.get("test_cases", [])
    timeout_s = int(commands.get("timeout_s", 5))

    report: dict[str, Any] = {
        "passed": False,
        "test_cmd_run": False,
        "test_cmd_passed": True,
        "test_cmd_output": "",
        "cases_run": 0,
        "cases_passed": 0,
        "case_results": [],
        "diff": "",
        "summary": "",
        "elapsed_ms": 0
    }

    total_t0 = time.perf_counter()

    # Step 1: Run automated test binary/command if specified
    test_cmd = commands.get("test", "").strip()
    if test_cmd:
        report["test_cmd_run"] = True
        run_res = run_command_in_workspace(workspace_dir, test_cmd, timeout_s=timeout_s)
        report["test_cmd_output"] = (run_res["stdout"] + "\n" + run_res["stderr"]).strip()
        if run_res["returncode"] != 0 or run_res["timed_out"] or run_res["denied"]:
            report["test_cmd_passed"] = False
            report["passed"] = False
            if run_res["denied"]:
                report["summary"] = run_res["error"]
            elif run_res["timed_out"]:
                report["summary"] = f"Test command timed out ({timeout_s}s)"
            else:
                report["summary"] = f"Test command failed with exit code {run_res['returncode']}"
            report["elapsed_ms"] = int((time.perf_counter() - total_t0) * 1000)
            return report

    # Step 2: Run Input vs. Expected Output Test Cases
    if test_cases:
        report["cases_run"] = len(test_cases)
        for idx, case in enumerate(test_cases, 1):
            c_name = case.get("name", f"Test Case #{idx}")
            cmd = case.get("command", commands.get("run", "")).strip()
            args = case.get("args", [])
            if args:
                cmd = f"{cmd} {' '.join(str(a) for a in args)}"
            c_stdin = str(case.get("stdin", ""))
            c_expect = str(case.get("expect", ""))
            c_expect_exit = int(case.get("expect_exit", 0))

            c_res = run_command_in_workspace(workspace_dir, cmd, stdin=c_stdin, timeout_s=timeout_s)

            actual_out = c_res["stdout"]
            exit_matches = (c_res["returncode"] == c_expect_exit)
            out_matches = (actual_out == c_expect)

            case_passed = out_matches and exit_matches and not c_res["timed_out"] and not c_res["denied"]
            case_diff = ""
            if not out_matches:
                case_diff = "".join(difflib.unified_diff(
                    c_expect.splitlines(keepends=True),
                    actual_out.splitlines(keepends=True),
                    fromfile="expected",
                    tofile="actual"
                ))

            c_result = {
                "name": c_name,
                "passed": case_passed,
                "stdout": actual_out,
                "stderr": c_res["stderr"],
                "returncode": c_res["returncode"],
                "expected_exit": c_expect_exit,
                "diff": case_diff,
                "timed_out": c_res["timed_out"],
                "elapsed_ms": c_res["elapsed_ms"]
            }
            report["case_results"].append(c_result)

            if case_passed:
                report["cases_passed"] += 1
            else:
                # First failing case diff becomes the primary diff
                if not report["diff"]:
                    report["diff"] = case_diff or f"Exit code mismatch: expected {c_expect_exit}, got {c_res['returncode']}\nstderr:\n{c_res['stderr']}"

        all_cases_ok = (report["cases_passed"] == report["cases_run"])
        report["passed"] = report["test_cmd_passed"] and all_cases_ok
        if report["passed"]:
            report["summary"] = f"All {report['cases_run']} test cases passed!"
        else:
            report["summary"] = f"{report['cases_passed']}/{report['cases_run']} test cases passed."
    else:
        # If no explicit test_cases, verdict is solely determined by commands.test
        report["passed"] = report["test_cmd_passed"] and report["test_cmd_run"]
        if report["passed"]:
            report["summary"] = "Test command executed successfully with exit code 0."
        elif not report["test_cmd_run"]:
            report["summary"] = "No tests or test cases declared in lab."

    report["elapsed_ms"] = int((time.perf_counter() - total_t0) * 1000)
    return report

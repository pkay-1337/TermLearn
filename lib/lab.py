"""Lab harness: gcc compile+run + hidden tests. (SRS FR-LAB-001..003, FR-STUDY-005, NFR-SEC-001..002)"""
import difflib
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

DENYLIST = ["rm -rf", "curl", "wget", "ssh", "mkfs", ":(){"]

CFLAGS = ["-Wall", "-std=c99", "-O0"]

#: Languages with a local runner in this version. Anything else goes through
#: the book's AI-authored generated runner (§4.9) or an explicit result.
#: The pilot language is C; others follow the same contract once declared.
SUPPORTED_LANGS = ("c",)

EXT_BY_LANG = {"python": "py", "javascript": "js", "typescript": "ts",
               "ruby": "rb", "go": "go", "rust": "rs", "java": "java",
               "bash": "sh", "c": "c", "cpp": "cpp"}


def _parse_json_blob(text: str, what: str) -> tuple[dict | None, str]:
    import json
    try:
        data = json.loads(text.strip().splitlines()[-1] if text.strip() else "")
        return (data if isinstance(data, dict) else None,
                "" if isinstance(data, dict) else f"{what}: not a JSON object")
    except Exception as e:
        return None, f"{what}: unparsable ({e}); raw={text[:200]!r}"


def check_runner(runner: Path, src: Path) -> tuple[bool, str, str]:
    """RUNNER-CHECK verb. Returns (ok, diagnostics, runner_error)."""
    try:
        pr = subprocess.run([str(runner), "check", str(src)],
                            capture_output=True, text=True, timeout=30,
                            cwd=str(src.parent))
    except subprocess.TimeoutExpired:
        return False, "", "runner timed out on check"
    except OSError as e:
        return False, "", f"runner not executable: {e}"
    if pr.returncode != 0:
        return False, "", f"runner exit {pr.returncode}: {(pr.stderr or '')[:300]}"
    data, err = _parse_json_blob(pr.stdout, "check")
    if err:
        return False, "", err
    return bool(data.get("ok")), str(data.get("diagnostics", "")), ""


def exec_runner(runner: Path, src: Path, expect: str, timeout: int,
                stdin_text: str = "") -> dict:
    """RUNNER-EXEC verb. App compares output itself (defense in depth);
    returns run_c-shaped dict with via='runner'."""
    res: dict = {"compiled": True, "stderr": "", "tests_passed": False,
                 "diff": "", "timed_out": False, "output": "",
                 "returncode": None, "unsupported": False, "via": "runner",
                 "runner_error": ""}
    with tempfile.TemporaryDirectory(prefix="termlearn-rexp-") as td:
        expf = Path(td) / "expect.txt"
        expf.write_text(expect, encoding="utf-8")
        cmd = [str(runner), "exec", str(src), "--expect", str(expf),
               "--timeout", str(timeout)]
        if stdin_text:
            inf = Path(td) / "stdin.txt"
            inf.write_text(stdin_text, encoding="utf-8")
            cmd += ["--stdin", str(inf)]
        try:
            pr = subprocess.run(cmd, capture_output=True, text=True,
                                timeout=timeout + 10, cwd=str(src.parent))
        except subprocess.TimeoutExpired:
            res["timed_out"] = True
            res["diff"] = f"runner exceeded outer timeout ({timeout + 10}s)"
            return res
        except OSError as e:
            res["runner_error"] = f"runner not executable: {e}"
            return res
        if pr.returncode != 0:
            res["runner_error"] = (f"runner exit {pr.returncode}: "
                                   f"{(pr.stderr or '')[:300]}")
            return res
        data, err = _parse_json_blob(pr.stdout, "exec")
        if err:
            res["runner_error"] = err
            return res
        out = str(data.get("output", ""))
        res["output"] = out
        res["returncode"] = data.get("returncode")
        if data.get("timed_out"):
            res["timed_out"] = True
            res["diff"] = "runner reported timeout"
            return res
        if out != expect:
            res["diff"] = "".join(difflib.unified_diff(
                expect.splitlines(True), out.splitlines(True),
                fromfile="expected", tofile="got"))
        res["tests_passed"] = bool(data.get("passed")) and out == expect
        return res


def get_runner_verbs(runner: Path) -> list[str]:
    """RUNNER-VERBS query (SPEC-RUNNER-002)."""
    try:
        pr = subprocess.run([str(runner), "verbs"], capture_output=True, text=True,
                            timeout=5, cwd=str(runner.parent))
        if pr.returncode == 0:
            data, _ = _parse_json_blob(pr.stdout, "verbs")
            if data and isinstance(data.get("verbs"), list):
                return [str(v) for v in data["verbs"]]
    except Exception:
        pass
    return ["check", "exec"]


def inspect_runner(runner: Path, src: Path, mode: str = "symbols", timeout: int = 10) -> dict:
    """RUNNER-INSPECT verb (SPEC-RUNNER-002)."""
    try:
        pr = subprocess.run([str(runner), "inspect", str(src), "--mode", mode],
                            capture_output=True, text=True, timeout=timeout, cwd=str(src.parent))
    except subprocess.TimeoutExpired:
        return {"ok": False, "diagnostics": "runner timed out on inspect", "mode": mode, "content": "", "format": "text"}
    except OSError as e:
        return {"ok": False, "diagnostics": f"runner not executable: {e}", "mode": mode, "content": "", "format": "text"}
    if pr.returncode != 0:
        return {"ok": False, "diagnostics": f"runner exit {pr.returncode}: {(pr.stderr or '')[:300]}", "mode": mode, "content": "", "format": "text"}
    data, err = _parse_json_blob(pr.stdout, "inspect")
    if err:
        return {"ok": False, "diagnostics": err, "mode": mode, "content": "", "format": "text"}
    return {
        "ok": bool(data.get("ok")),
        "diagnostics": str(data.get("diagnostics", "")),
        "mode": str(data.get("mode", mode)),
        "content": str(data.get("content", "")),
        "format": str(data.get("format", "text"))
    }


def lint_runner(runner: Path, src: Path, timeout: int = 10) -> dict:
    """RUNNER-LINT verb (SPEC-RUNNER-002)."""
    try:
        pr = subprocess.run([str(runner), "lint", str(src)],
                            capture_output=True, text=True, timeout=timeout, cwd=str(src.parent))
    except subprocess.TimeoutExpired:
        return {"ok": False, "diagnostics": [{"message": "runner timed out on lint"}]}
    except OSError as e:
        return {"ok": False, "diagnostics": [{"message": f"runner not executable: {e}"}]}
    if pr.returncode != 0:
        return {"ok": False, "diagnostics": [{"message": f"runner exit {pr.returncode}: {(pr.stderr or '')[:300]}"}]}
    data, err = _parse_json_blob(pr.stdout, "lint")
    if err or not isinstance(data, dict):
        return {"ok": False, "diagnostics": [{"message": err or "malformed lint response"}]}
    return {"ok": bool(data.get("ok")), "diagnostics": data.get("diagnostics", [])}


def inspect_c(code: str, mode: str = "symbols") -> dict:
    """Built-in pilot inspector for C code using host gcc, nm, objdump, readelf."""
    if not gcc_available():
        return {"ok": False, "diagnostics": "gcc not found on PATH", "mode": mode, "content": "", "format": "text"}
    with tempfile.TemporaryDirectory(prefix="termlearn-cinsp-") as td:
        src = Path(td) / "code.c"
        obj = Path(td) / "code.o"
        src.write_text(code, encoding="utf-8")
        cr = subprocess.run(["gcc", "-c", "-Wall", "-std=c99", "-O0", str(src), "-o", str(obj)],
                            capture_output=True, text=True, timeout=10)
        if cr.returncode != 0:
            return {"ok": False, "diagnostics": f"Compilation failed:\n{cr.stderr}", "mode": mode, "content": "", "format": "text"}
        if mode == "symbols":
            cmd = ["nm", "-C", str(obj)]
            fmt = "text"
        elif mode == "disasm":
            cmd = ["objdump", "-d", "-M", "intel", str(obj)]
            fmt = "asm"
        elif mode == "sections":
            cmd = ["readelf", "-S", str(obj)]
            fmt = "text"
        else:
            return {"ok": False, "diagnostics": f"Unknown inspect mode: {mode!r}", "mode": mode, "content": "", "format": "text"}
        tool = cmd[0]
        if not shutil.which(tool):
            return {"ok": False, "diagnostics": f"Tool '{tool}' not found on host", "mode": mode, "content": "", "format": fmt}
        try:
            ir = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if ir.returncode != 0:
                return {"ok": False, "diagnostics": f"{tool} failed: {ir.stderr}", "mode": mode, "content": "", "format": fmt}
            return {"ok": True, "diagnostics": "", "mode": mode, "content": ir.stdout, "format": fmt}
        except Exception as e:
            return {"ok": False, "diagnostics": f"Error running {tool}: {e}", "mode": mode, "content": "", "format": fmt}


def inspect_code(book: str | None, code: str, lang: str = "c", mode: str = "symbols", packs_root=None) -> dict:
    """High-level inspector dispatcher. Resolves runner or pilot C fallback."""
    lang = (lang or "c").lower()
    if book:
        from lib.pack import load_book_toolchain
        try:
            tc = load_book_toolchain(book, packs_root)
            rel = (tc or {}).get("runner", "")
            if rel:
                from pathlib import Path as _P
                _root = _P(packs_root) if packs_root else _P(__file__).resolve().parents[1] / "packs"
                runner = _root / book / rel
                if runner.exists() and os.access(str(runner), os.X_OK):
                    verbs = get_runner_verbs(runner)
                    if "inspect" in verbs:
                        ext = EXT_BY_LANG.get(lang, "src")
                        with tempfile.TemporaryDirectory(prefix="termlearn-rinsp-") as td:
                            src = Path(td) / f"prog.{ext}"
                            src.write_text(code, encoding="utf-8")
                            return inspect_runner(runner, src, mode=mode)
        except Exception:
            pass
    if lang in ("c", "cpp"):
        return inspect_c(code, mode=mode)
    return {"ok": False, "diagnostics": f"Inspector mode '{mode}' not available for language '{lang}' without a runner.",
            "mode": mode, "content": "", "format": "text"}



def run_via_runner(book: str, code: str, lang: str,
                   tests: list[dict] | None = None, timeout: int = 2,
                   packs_root=None) -> dict:
    """Full generated-runner flow (FR-LAB-004 precedence level 2)."""
    from lib.pack import load_book_toolchain  # local import: pack imports lab
    base = {"compiled": False, "stderr": "", "tests_passed": False,
            "diff": "", "timed_out": False, "output": "",
            "returncode": None, "unsupported": False, "via": "runner",
            "runner_error": ""}
    try:
        tc = load_book_toolchain(book, packs_root)
    except FileNotFoundError as e:
        base["stderr"] = str(e)
        return base
    rel = (tc or {}).get("runner", "")
    if not rel:
        base["unsupported"] = True
        return base
    from pathlib import Path as _P
    _root = _P(packs_root) if packs_root else _P(__file__).resolve().parents[1] / "packs"
    runner = _root / book / rel
    if not (runner.exists() and os.access(str(runner), os.X_OK)):
        base["runner_error"] = f"runner declared but missing/not executable: {runner}"
        return base
    ext = EXT_BY_LANG.get(lang, "src")
    with tempfile.TemporaryDirectory(prefix="termlearn-rsrc-") as td:
        src = Path(td) / f"prog.{ext}"
        src.write_text(code, encoding="utf-8")
        ok, diag, rerr = check_runner(runner, src)
        if rerr:
            base["runner_error"] = rerr
            return base
        if not ok:
            base["stderr"] = diag[-2000:]
            return base
        base["compiled"] = True
        cases = tests or [{"args": [], "stdin": "", "expect": ""}]
        for t in cases:
            r = exec_runner(runner, src, t.get("expect", ""),
                            timeout, t.get("stdin", ""))
            if r.get("runner_error") or r.get("timed_out"):
                return {**base, **{k: r[k] for k in ("timed_out", "diff", "runner_error", "output") if k in r}}
            if not r["tests_passed"]:
                base.update(output=r["output"], returncode=r["returncode"],
                            diff=r["diff"])
                return base
        base["tests_passed"] = True
        return base


def run_code(code: str, lang: str = "c", tests: list[dict] | None = None,
             timeout: int = 2, cflags: list[str] | None = None,
             book: str | None = None, packs_root=None) -> dict:
    """Language dispatch for runnable code. (SRS FR-LAB-004)

    Precedence: (1) built-in local runner (pilot: C); (2) the book's
    AI-authored generated runner (`toolchain.runner`, §4.9) — needs `book`;
    (3) explicit unsupported result. `lang` comes from `example.lang` /
    `lab.lang` / check `lang` (default "c" for pilot packs).
    """
    lang = (lang or "c").lower()
    if lang in SUPPORTED_LANGS:
        res = run_c(code, tests=tests, timeout=timeout, cflags=cflags)
        res.update(unsupported=False, lang=lang, via="builtin", runner_error="")
        return res
    if book is None:
        return {"compiled": False, "stderr": "", "tests_passed": False,
                "diff": "", "timed_out": False, "output": "",
                "returncode": None, "unsupported": True, "via": "none",
                "runner_error": "", "lang": lang}
    return run_via_runner(book, code, lang, tests, timeout, packs_root)


def gcc_available() -> bool:
    return shutil.which("gcc") is not None


def run_c(code: str, tests: list[dict] | None = None,
          timeout: int = 2, cflags: list[str] | None = None) -> dict:
    """Pure compile-and-run helper (testable, VR-003). No shell=True. Temp dir only.

    tests: [{args:[], stdin:"", expect:""}]. Returns dict with keys:
      compiled(bool), stderr(str), tests_passed(bool), diff(str),
      timed_out(bool), output(str of last case), returncode(int|None)
    """
    res: dict = {"compiled": False, "stderr": "", "tests_passed": False,
                 "diff": "", "timed_out": False, "output": "", "returncode": None}
    if not gcc_available():
        res["stderr"] = "gcc not found — install gcc to run labs (CR-ENV-002)"
        return res
    with tempfile.TemporaryDirectory(prefix="termlearn-lab-") as td:
        src = Path(td) / "prog.c"
        exe = Path(td) / "prog"
        src.write_text(code, encoding="utf-8")
        try:
            cr = subprocess.run(["gcc", * (cflags or CFLAGS), str(src), "-o", str(exe)],
                                capture_output=True, text=True, timeout=15)
        except subprocess.TimeoutExpired:
            res["stderr"] = "gcc compile timeout"
            return res
        if cr.returncode != 0:
            res["stderr"] = (cr.stderr or "")[-2000:]
            return res
        res["compiled"] = True
        cases = tests or [{"args": [], "stdin": "", "expect": ""}]
        all_ok = True
        last_diff = ""
        for t in cases:
            try:
                pr = subprocess.run([str(exe), *(t.get("args") or [])],
                                    input=t.get("stdin", ""), capture_output=True,
                                    text=True, timeout=timeout)
            except subprocess.TimeoutExpired:
                res["timed_out"] = True
                all_ok = False
                last_diff = f"timeout after {timeout}s"
                break
            out = pr.stdout or ""
            res["output"] = out
            res["returncode"] = pr.returncode
            exp = t.get("expect", "")
            if out != exp or pr.returncode != 0:
                all_ok = False
                last_diff = "".join(difflib.unified_diff(
                    exp.splitlines(True), out.splitlines(True),
                    fromfile="expected", tofile="got"))
                if pr.returncode != 0 and not last_diff:
                    last_diff = f"exit code {pr.returncode}, stderr: {(pr.stderr or '')[:500]}"
                break
        res["tests_passed"] = all_ok
        res["diff"] = last_diff
        return res


def scan_denylist(tests_sh: str) -> list[str]:
    return [b for b in DENYLIST if b in (tests_sh or "")]


def save_solution(book: str, chapter: str, code: str, passed: bool) -> str:
    """SHA-256 content hash + retention, deduplicated by hash. (FR-LAB-003, D-10)"""
    import hashlib
    import time
    from lib.srs import init_db
    h = hashlib.sha256(code.encode("utf-8")).hexdigest()
    con = init_db()
    con.execute("INSERT OR IGNORE INTO solutions(hash,ts,book,chapter,passed,code) VALUES(?,?,?,?,?,?)",
                (h, int(time.time()), book, chapter, 1 if passed else 0, code))
    con.commit()
    con.close()
    return h


def run(book: str, chapter: str, save_solution_on_test: bool = True):
    """Interactive lab: edit starter, r=run, t=hidden tests, h=hint. (FR-LAB-001)"""
    import yaml
    from rich.console import Console
    from lib.pack import load_chapter_mode
    c = Console()
    try:
        data = load_chapter_mode(book, chapter, "lab")
    except FileNotFoundError:
        c.print(f"[yellow]No pack for {book}/{chapter} yet: run gen-prompt, then validate.[/yellow]")
        return
    lab = data.get("lab")
    if not lab and data.get("labs"):
        first_lab = data["labs"][0]
        starter = ""
        for f in first_lab.get("files", []):
            if f.get("content"):
                starter = f.get("content")
                break
        lab = {
            "title": first_lab.get("title", "Lab"),
            "prompt_md": first_lab.get("instruction_md", ""),
            "starter_c": starter,
            "hints": first_lab.get("hints", []),
        }
    if not lab:
        c.print("[yellow]No lab in this chapter pack.[/yellow]")
        return
    c.print(f"[bold]{lab.get('title', 'Lab')}[/bold]\n{lab.get('prompt_md', '')}")
    code = lab.get("starter_c", "")
    c.print("[dim]Commands: e=edit($EDITOR) r=run t=hidden-tests d=last diff h=hint ?=help q=quit[/dim]")
    import os
    from lib import keys as _k
    last: dict | None = None
    while True:
        cmd = _k.ask(c, "> ", "lab").lower()
        if cmd == "q":
            break
        elif cmd == "e":
            ed = os.environ.get("VISUAL") or os.environ.get("EDITOR")
            with tempfile.NamedTemporaryFile("w", suffix=".c", delete=False) as f:
                f.write(code)
                path = f.name
            if ed:
                subprocess.run([ed, path])
                code = Path(path).read_text(encoding="utf-8")
            else:
                c.print("[yellow]$EDITOR unset — paste code, end with a single '.' line:[/yellow]")
                buf = []
                while True:
                    line = input()
                    if line.strip() == ".":
                        break
                    buf.append(line)
                code = "\n".join(buf) + "\n"
        elif cmd in ("r", "t"):
            lang = (lab.get("lang", "c") or "c")
            r = run_code(code, lang, tests=[{"args": [], "expect": ""}], timeout=2, book=book)
            if r.get("unsupported"):
                c.print(f"[yellow]no local runner for '{lang}' in this version — "
                        f"run it in the book's toolchain and continue.[/yellow]")
            elif not r["compiled"]:
                c.print(f"[red]compile error:[/red]\n{r['stderr']}")
            elif r["timed_out"]:
                c.print("[red]timeout (2s). Infinite loop?[/red]")
            else:
                c.print(f"[green]ran OK[/green] output:\n{r['output'][:2000]}")
            last = r
            if cmd == "t":
                c.print("[dim]hidden-test diffing against pack expectations needs pack tests wiring (next iteration).[/dim]")
                verdict = bool(r.get("compiled") and not r.get("timed_out")
                               and not r.get("unsupported") and not r.get("runner_error"))
                if save_solution_on_test:
                    h = save_solution(book, chapter, code, verdict)
                    c.print(f"[dim]solution recorded: {h[:12]}… "
                            f"({'pass' if verdict else 'fail'})[/dim]")
                else:
                    c.print("[dim]--no-save-solution: verdict logged, code not retained.[/dim]")
        elif cmd == "d":
            if not last:
                c.print("[yellow]nothing run yet — press r first.[/yellow]")
            else:
                c.print(f"[bold]last output:[/bold]\n{(last.get('output') or '(empty)')[:2000]}")
                if last.get("diff"):
                    c.print(f"[bold]diff vs expected:[/bold]\n{last['diff'][:2000]}")
                elif last.get("stderr"):
                    c.print(f"[bold]diagnostics:[/bold]\n{last['stderr'][:2000]}")
                else:
                    c.print("[dim]no diff — output matched.[/dim]")
        elif cmd == "h":
            hints = lab.get("hints", [])
            c.print(hints[0] if hints else "No hints in pack.")
        else:
            c.print("keys: e r t d h ? q")


def check_lab(book: str, chapter: str, non_interactive=True, packs_root=None):
    from lib.pack import load_chapter_mode
    data = load_chapter_mode(book, chapter, "lab", packs_root=packs_root)
    labs = data.get("labs")
    if isinstance(labs, list) and labs:
        from lib import lab_workspace as lw
        from lib import progress
        all_passed = True
        reasons = []
        for l in labs:
            lid = l.get("id", "lab1")
            if progress.is_lab_passed(book, chapter, lid):
                continue
            wdir = lw.provision_lab_workspace(book, chapter, l)
            v = lw.run_lab_verification(wdir, l)
            if not v["passed"]:
                all_passed = False
                reasons.append(f"{lid}: {v.get('summary', 'failed')}")
        return {
            "passed": all_passed,
            "reason": "all labs pass verification" if all_passed else "; ".join(reasons)
        }
    lab = data.get("lab")
    if not lab:
        return {"passed": None, "reason": "no lab in pack"}
    lang = (lab.get("lang", "c") or "c").lower()
    if lang in SUPPORTED_LANGS:
        r = run_c(lab.get("starter_c", ""), timeout=2)
        return {"passed": bool(r["compiled"]), "reason": r["stderr"][:200] if not r["compiled"] else "starter compiles"}
    r = run_code(lab.get("starter_c", ""), lang, timeout=2, book=book,
                 packs_root=packs_root)
    if r.get("runner_error"):
        return {"passed": False, "reason": r["runner_error"][:200]}
    if r.get("unsupported"):
        return {"passed": None, "reason": "no runner declared for '%s' — lab not gateable" % lang}
    return {"passed": bool(r["compiled"]), "reason": r["stderr"][:200] if not r["compiled"] else "starter checks clean"}

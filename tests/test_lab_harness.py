"""Lab harness unit tests on synthetic C snippets — no book. (SRS VR-003)"""
import shutil
import pytest
from lib import lab

gcc = shutil.which("gcc")

def test_run_c_success():
    if not gcc:
        pytest.skip("gcc absent — harness must skip cleanly (FR-VAL-001)")
    r = lab.run_c("int main(void){return 0;}\n", tests=[{"args": [], "expect": ""}])
    assert r["compiled"] and r["tests_passed"]

def test_compiler_error_surfaced():
    if not gcc:
        pytest.skip("gcc absent")
    r = lab.run_c("int main(void){ return }\n")
    assert not r["compiled"] and "error" in r["stderr"].lower()

def test_output_diff_reported():
    if not gcc:
        pytest.skip("gcc absent")
    r = lab.run_c('#include <stdio.h>\nint main(void){printf("hi\\n");return 0;}\n',
                  tests=[{"args": [], "expect": "bye\n"}])
    assert r["compiled"] and not r["tests_passed"] and r["diff"]

def test_timeout_kills():
    if not gcc:
        pytest.skip("gcc absent")
    r = lab.run_c("int main(void){while(1){}return 0;}\n",
                  tests=[{"args": [], "expect": ""}], timeout=1)
    assert r["compiled"] and r["timed_out"]

def test_gcc_absent_graceful(monkeypatch):
    monkeypatch.setattr(lab, "gcc_available", lambda: False)
    r = lab.run_c("int main(void){return 0;}\n")
    assert not r["compiled"] and "gcc not found" in r["stderr"]

def test_nonzero_exit_reports():
    if not gcc:
        pytest.skip("gcc absent")
    r = lab.run_c("int main(void){return 3;}\n",
                  tests=[{"args": [], "expect": ""}])
    assert r["compiled"] and not r["tests_passed"] and "exit code 3" in r["diff"]

def test_stdin_case():
    if not gcc:
        pytest.skip("gcc absent")
    r = lab.run_c("#include <stdio.h>\nint main(void){int c=getchar();putchar(c);return 0;}\n",
                  tests=[{"args": [], "stdin": "q", "expect": "q"}])
    assert r["tests_passed"]

def test_lab_compile_failure_path():
    if not gcc:
        pytest.skip("gcc absent")
    ch = {"meta": {"book": "t", "chapter_id": "c", "title": "T",
                   "source_ref": "x", "level": "intro", "prereqs": []},
          "objectives": ["o"],
          "blocks": [{"id": "b1", "type": "model", "title": "B",
                      "explain_md": "x",
                      "checks": [{"kind": "mcq", "q": "Q",
                                  "choices": ["A", "B"], "answer": 0,
                                  "why": "W"}]}],
          "lab": {"starter_c": "this is not C at all (((\n"}}
    from lib import pack as _pack
    errs, _ = _pack.validate_chapter_data(ch)
    assert any("LAB-COMPILE" in e for e in errs), errs


def test_save_solution_dedup_and_optout(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    h1 = lab.save_solution("b", "c", "code", True)
    h2 = lab.save_solution("b", "c", "code", True)
    assert h1 == h2 and len(h1) == 64
    import sqlite3
    from lib import progress
    con = sqlite3.connect(str(progress.db_path()))
    n = con.execute("SELECT COUNT(*) FROM solutions").fetchone()[0]
    con.close()
    assert n == 1

def test_dispatch_c_runs():
    if not gcc:
        pytest.skip("gcc absent")
    r = lab.run_code("int main(void){return 0;}\n", "c")
    assert not r.get("unsupported") and r["compiled"]

def test_dispatch_unknown_lang_is_explicit():
    r = lab.run_code("print('hi')\n", "python")
    assert r.get("unsupported") and r["lang"] == "python"
    assert not r["compiled"]

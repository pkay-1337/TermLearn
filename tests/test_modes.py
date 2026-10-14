"""Mode-level integration tests on the pilot pack with piped stdin.
Exercises the interactive loops (study/quiz/parsons/lab/srs) and the
validate_book/test-gate paths that unit fixtures cannot reach. (VR-004, D-17)"""
import io
import os
import shutil
import sqlite3
import sys
from pathlib import Path

import pytest

from lib import lab, pack, progress
from lib import quiz as _quiz
from lib import srs as _srs
from lib import study as _study
from lib import parsons as _parsons

gcc = shutil.which("gcc")
NEEDS_GCC = pytest.mark.skipif(not gcc, reason="needs gcc (pilot toolchain)")


@pytest.fixture()
def tmp_home(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    monkeypatch.setattr(sys, "stdin", io.StringIO(""))
    return tmp_path


def _pipe(monkeypatch, text):
    monkeypatch.setattr(sys, "stdin", io.StringIO(text))


def test_study_full_pass_records_answers(tmp_home, monkeypatch):
    _pipe(monkeypatch, "5\n1\n1\n1\ns\n2\n1\n200\n\n2 3 4\n1\n1\n1\n1\n")
    _study.run("extreme-c", "ch04")
    con = sqlite3.connect(str(progress.db_path()))
    n = con.execute("SELECT COUNT(*) FROM answers WHERE book='extreme-c'").fetchone()[0]
    con.close()
    assert n == 12  # 4 (b1) + 3 (b2) + 2 (b3) + 3 (b4) checks


def test_quiz_scores_and_persists_items(tmp_home, monkeypatch):
    _pipe(monkeypatch, "5\n1\n1\n1\n2\n1\n200\n2 3 4\n1\n1\n1\n1\n")
    _quiz.run("extreme-c", "ch04")
    con = sqlite3.connect(str(progress.db_path()))
    row = con.execute("SELECT score,total,items FROM quiz_runs").fetchone()
    con.close()
    assert (row[0], row[1]) == (12, 12) and "b1:0" in row[2]


def test_parsons_and_lab_loop(tmp_home, monkeypatch, capsys):
    _pipe(monkeypatch, "2 3 4\n")
    _parsons.run("extreme-c", "ch04")
    _pipe(monkeypatch, "r\nd\nq\n")
    lab.run("extreme-c", "ch04")
    out = capsys.readouterr().out
    assert "last output" in out  # d= view works


def test_srs_syncs_cards_and_quits(tmp_home, monkeypatch):
    _pipe(monkeypatch, "q\n")
    _srs.run("extreme-c")
    con = sqlite3.connect(str(progress.db_path()))
    n = con.execute("SELECT COUNT(*) FROM cards WHERE book='extreme-c'").fetchone()[0]
    con.close()
    assert n >= 5


def test_srs_grades_and_retries(tmp_home, monkeypatch):
    _pipe(monkeypatch, "f\n9\n3\nq\n")
    _srs.run("extreme-c")
    con = sqlite3.connect(str(progress.db_path()))
    row = con.execute("SELECT reps FROM cards WHERE book='extreme-c' LIMIT 1").fetchone()
    con.close()
    assert row is not None and row[0] >= 0


def test_lab_editor_hints_badkey(tmp_home, monkeypatch, capsys):
    monkeypatch.setenv("VISUAL", "true")
    _pipe(monkeypatch, "e\nh\nbogus\nq\n")
    lab.run("extreme-c", "ch04")
    out = capsys.readouterr().out
    assert "hint" in out.lower() and "keys:" in out


def test_lab_inline_paste_fallback(tmp_home, monkeypatch, capsys):
    monkeypatch.delenv("VISUAL", raising=False)
    monkeypatch.delenv("EDITOR", raising=False)
    _pipe(monkeypatch, "e\nint x;\n.\nr\nq\n")
    lab.run("extreme-c", "ch04")
    out = capsys.readouterr().out
    assert "ran OK" in out or "compile error" in out


@NEEDS_GCC
def test_validate_book_chapter_strict_and_gate(tmp_home):
    assert pack.validate_book("extreme-c", "ch04", strict=True) is True
    progress.record_quiz("extreme-c", "ch04", 12, 12, seed=0, items=[])
    assert lab.check_lab("extreme-c", "ch04")["passed"] is True
    assert progress.record_test(
        "extreme-c", "ch04",
        {"score": 12, "total": 12}, {"passed": True}) is True


def test_validator_branches_without_gcc():
    import yaml
    base = {"meta": {"book": "t", "chapter_id": "c", "title": "T",
                     "source_ref": "x", "level": "intro", "prereqs": []},
            "objectives": ["o"],
            "blocks": [{"id": "b1", "type": "model", "title": "B",
                        "explain_md": "x",
                        "checks": [{"kind": "mcq", "q": "Q",
                                    "choices": ["A", "B"], "answer": 0,
                                    "why": "W"}]}]}
    assert pack.toolchain_gate(False, base) is None  # no runnable content
    errs, _ = pack.validate_book_data(
        {"book": {}, "order": ["a"],
         "chapters": [{"id": "a", "title": "T", "source_ref": "x"},
                      {"id": "a", "title": "T2", "source_ref": "y"}]})
    assert any("BOOK-DUP" in e for e in errs)


def test_load_yaml_syntax_error(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("a: [unclosed\n", encoding="utf-8")
    data, err = pack._load_yaml(bad)
    assert data is None and "YAML-SYNTAX" in err


def _mkpacks(tmp_path, toolchain=True, lab_lang="c", starter="int main(void){return 0;}\n"):
    import yaml
    root = tmp_path / "packs" / "tb"
    root.mkdir(parents=True, exist_ok=True)
    tc = "\ntoolchain: {lang: c}\n" if toolchain else "\n"
    (root / "book.yaml").write_text(
        "book: {slug: tb}\n" + tc + "order: [ch01]\n"
        "chapters: [{id: ch01, title: T, source_ref: x}]\n", encoding="utf-8")
    (root / "ch01.yaml").write_text(yaml.safe_dump({
        "meta": {"book": "tb", "chapter_id": "ch01", "title": "T",
                 "source_ref": "x", "level": "intro", "prereqs": []},
        "objectives": ["o"],
        "blocks": [{"id": "b1", "type": "model", "title": "B",
                    "explain_md": "x",
                    "viz": {"kind": "ascii-memory", "steps": ["s1"]},
                    "checks": [{"kind": "why-fails", "q": "Q1",
                                "choices": ["A", "B"], "answer": 0, "why": "W",
                                "from_chapter": "ch01", "from_block": "b1"},
                               {"kind": "mcq", "q": "Q2",
                                "choices": ["A", "B"], "answer": 1, "why": "W",
                                "from_chapter": "ch01", "from_block": "b1"}]}],
        "lab": {"title": "L", "lang": lab_lang, "starter_c": starter}}),
        encoding="utf-8")
    return tmp_path / "packs"


def test_validate_book_tmp_full_and_toolchain_gate(tmp_path):
    assert pack.validate_book("tb", strict=True,
                              packs_root=_mkpacks(tmp_path)) is True
    assert pack.validate_book("tb", strict=True,
                              packs_root=_mkpacks(tmp_path, toolchain=False)) is False
    assert pack.validate_book("tb", strict=False,
                              packs_root=_mkpacks(tmp_path, toolchain=False)) is True


def test_check_lab_branches(tmp_path):
    assert lab.check_lab("tb", "ch01",
                         packs_root=_mkpacks(tmp_path))["passed"] is True
    r = lab.check_lab("tb", "ch01",
                      packs_root=_mkpacks(tmp_path, lab_lang="python",
                                          starter="print('x')\n"))
    assert r["passed"] is None and "gateable" in r["reason"]
    r = lab.check_lab("tb", "ch01",
                      packs_root=_mkpacks(tmp_path, starter="not C ((("))
    assert r["passed"] is False


GOOD_RUNNER = Path(__file__).parent / "fixtures" / "runner" / "good" / "run"


def _mkpybook(tmp_path):
    import shutil
    import stat
    import yaml
    root = tmp_path / "packs" / "pyb"
    (root / "runner").mkdir(parents=True)
    (root / "book.yaml").write_text(yaml.safe_dump({
        "book": {"slug": "pyb"},
        "toolchain": {"lang": "python", "runner": "runner/run",
                      "run": ["python3"],
                      "version_cmd": ["python3", "--version"],
                      "timeout_s": 2,
                      "smoke": {"ext": "py", "src": "print('ok')\n",
                                "expect": "ok\n"}},
        "order": ["ch01"],
        "chapters": [{"id": "ch01", "title": "T", "source_ref": "x"}]}),
        encoding="utf-8")
    (root / "ch01.yaml").write_text(yaml.safe_dump({
        "meta": {"book": "pyb", "chapter_id": "ch01", "title": "T",
                 "source_ref": "x", "level": "intro", "prereqs": []},
        "objectives": ["o"],
        "blocks": [{"id": "b1", "type": "model", "title": "B",
                    "explain_md": "x",
                    "viz": {"kind": "ascii-memory", "steps": ["s"]},
                    "checks": [
                        {"kind": "predict", "q": "Q1",
                         "choices": ["A", "B"], "answer": 0, "why": "W",
                         "from_chapter": "ch01", "from_block": "b1"},
                        {"kind": "why-fails", "q": "Q2",
                         "choices": ["A", "B"], "answer": 1, "why": "W",
                         "from_chapter": "ch01", "from_block": "b1"}]}],
        "lab": {"title": "L", "lang": "python",
                "starter_c": "print('hi')\n"}}), encoding="utf-8")
    shutil.copy(GOOD_RUNNER, root / "runner" / "run")
    os.chmod(root / "runner" / "run",
             os.stat(root / "runner" / "run").st_mode | stat.S_IEXEC)
    return tmp_path / "packs"


def test_tmp_book_with_runner_validates_and_gates(tmp_path):
    base = _mkpybook(tmp_path)
    assert pack.validate_book("pyb", strict=True, packs_root=base) is True
    r = lab.check_lab("pyb", "ch01", packs_root=base)
    assert r["passed"] is True
    r = lab.run_code("print('hi')\n", "python",
                     tests=[{"expect": "hi\n"}], timeout=5,
                     book="pyb", packs_root=base)
    assert r["tests_passed"] and r["via"] == "runner"


def test_lab_hidden_tests_key(tmp_home, monkeypatch, capsys):
    _pipe(monkeypatch, "t\nq\n")
    lab.run("extreme-c", "ch04")
    assert "hidden-test" in capsys.readouterr().out

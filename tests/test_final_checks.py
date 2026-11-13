import io
import sqlite3
import sys
from pathlib import Path

import yaml
from typer.testing import CliRunner

from lib import pack, progress, quiz


def test_collect_final_checks_ignores_non_mappings():
    data = {"test": {"final_checks": [
        {"kind": "mcq", "q": "Q", "choices": ["A", "B"], "answer": 0, "why": "W"},
        "bogus",
    ]}}
    checks = quiz.collect_final_checks(data)
    assert len(checks) == 1
    assert checks[0][0] == "final"
    assert checks[0][2]["q"] == "Q"


def test_run_final_checks_scores_and_logs(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    monkeypatch.setattr(sys, "stdin", io.StringIO("1\n2\n3\n1\n2\n"))
    result = quiz.run_final_checks("extreme-c", "ch23")
    assert result["aborted"] is False
    assert result["score"] == result["total"] == 5
    con = sqlite3.connect(str(progress.db_path()))
    n = con.execute("SELECT COUNT(*) FROM answers WHERE block='final'").fetchone()[0]
    con.close()
    assert n == 5


def test_record_test_requires_final_checks(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    quiz_score = {"score": 10, "total": 10}
    lab = {"passed": True}
    assert progress.record_test(
        "extreme-c", "ch23", quiz_score, lab,
        final_score={"score": 4, "total": 5}, require_final=True) is False
    assert progress.record_test(
        "extreme-c", "ch23", quiz_score, lab,
        final_score={"score": 5, "total": 5}, require_final=True) is True
    assert progress.record_test(
        "extreme-c", "ch23", quiz_score, lab, require_final=False) is True


def test_cli_test_no_final_skips_interactive_checks(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    from main import app
    from lib import lab

    monkeypatch.setattr(lab, "check_lab", lambda *a, **k: {"passed": True})
    seen = {}

    def fake_record(book, chapter, q, l, **kwargs):
        seen.update(kwargs)
        return True

    monkeypatch.setattr(progress, "record_test", fake_record)
    result = CliRunner().invoke(
        app, ["test", "--book", "extreme-c", "--chapter", "ch23", "--no-final"])
    assert result.exit_code == 0
    assert seen["require_final"] is False
    assert seen["final_score"] is None


def test_validator_rejects_bad_final_checks_and_min_final(tmp_path):
    fixture = Path(__file__).parent / "fixtures" / "valid_ch.yaml"
    data = yaml.safe_load(fixture.read_text(encoding="utf-8"))
    data["test"]["gates"][0]["min_final"] = 101
    data["test"]["final_checks"] = [{"kind": "mcq"}]
    errors, _ = pack.validate_chapter_data(data, "ch.yaml")
    assert any("TEST-GATE" in e for e in errors)
    assert any("CHECK-SHAPE" in e and "final_checks" in e for e in errors)

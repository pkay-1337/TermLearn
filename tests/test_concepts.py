"""Concept-system tests: filter, tally, migration, rollup, end-to-end.
(FR-QUIZ-001/002, FR-STAT-001/002; D-02/D-03/D-08)"""
import io
import sqlite3
import sys

from lib import progress
from lib import quiz as _quiz

CHECKS = [("b1", 0, {"kind": "mcq", "concept": "alpha"}),
          ("b1", 1, {"kind": "mcq", "concept": "beta"}),
          ("b2", 0, {"kind": "mcq"})]


def test_filter_checks():
    assert len(_quiz.filter_checks(CHECKS)) == 3
    assert len(_quiz.filter_checks(CHECKS, "")) == 3
    got = _quiz.filter_checks(CHECKS, "alpha")
    assert [(b, i) for b, i, _ in got] == [("b1", 0)]
    assert _quiz.filter_checks(CHECKS, "missing") == []


def test_tally():
    t = _quiz.tally([("a", True), ("a", False), ("b", True)])
    assert t == {"a": [1, 2], "b": [1, 1]}
    assert _quiz.tally([]) == {}


def test_answers_migration_and_concept_rollup(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    p = progress.db_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(p))
    con.execute("""CREATE TABLE answers(id INTEGER PRIMARY KEY, ts INTEGER,
      book TEXT, chapter TEXT, block TEXT, check_idx INTEGER,
      correct INTEGER, ms INTEGER)""")
    con.commit()
    con.close()
    con = progress.init_db()  # migrates, keeps working
    progress_module_log(con)
    rows = progress.concept_stats("b")
    con.close()
    by = {r["concept"]: (r["hits"], r["total"], r["block"]) for r in rows}
    assert by["alpha"] == (1, 2, "b1"), by
    assert by["beta"] == (1, 1, "b1"), by


def progress_module_log(con):
    from lib.srs import log_answer
    log_answer(con, "b", "ch", "b1", 0, True, concept="alpha")
    log_answer(con, "b", "ch", "b1", 1, False, concept="alpha")
    log_answer(con, "b", "ch", "b1", 2, True, concept="beta")


def test_quiz_concept_filter_end_to_end(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    monkeypatch.setattr(sys, "stdin", io.StringIO("2 3 4\n1\n"))
    _quiz.run("extreme-c", "ch04", concept="pass-by-value")
    out = capsys.readouterr().out
    assert "score: 2/2" in out and "pass-by-value" in out


def test_stats_shows_concepts(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    con = progress.init_db()
    progress_module_log(con)
    con.close()
    from lib import stats as _stats
    _stats.run("b")
    out = capsys.readouterr().out
    assert "concepts" in out and "alpha" in out and "weakest concepts" in out

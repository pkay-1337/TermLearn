"""Progress-store tests: quiz item IDs + legacy migration. (FR-QUIZ-003, D-04)"""
import json
import sqlite3

from lib import progress


def test_record_quiz_persists_items(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    progress.record_quiz("b", "ch01", 3, 4, seed=7, items=["b1:0", "b1:1"])
    con = sqlite3.connect(str(progress.db_path()))
    row = con.execute("SELECT score,total,seed,items FROM quiz_runs").fetchone()
    con.close()
    assert (row[0], row[1], row[2]) == (3, 4, 7)
    assert json.loads(row[3]) == ["b1:0", "b1:1"]


def test_legacy_db_gains_items_column(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    p = progress.db_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(p))
    con.execute("""CREATE TABLE quiz_runs(id INTEGER PRIMARY KEY, ts INTEGER,
      book TEXT, chapter TEXT, score INTEGER, total INTEGER, seed INTEGER)""")
    con.execute("INSERT INTO quiz_runs VALUES(1,2,'b','c',1,1,0)")
    con.commit()
    con.close()
    progress.record_quiz("b", "ch01", 1, 1)  # must migrate, not crash
    con = sqlite3.connect(str(p))
    cols = [r[1] for r in con.execute("PRAGMA table_info(quiz_runs)").fetchall()]
    n = con.execute("SELECT COUNT(*) FROM quiz_runs").fetchone()[0]
    con.close()
    assert "items" in cols and n == 2


def test_picker_helpers(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    assert progress.book_mastery("b", 3) == "—"
    assert progress.chapter_status("b", "ch01") == "new"
    assert progress.chapter_due_count("b", "ch01") == 0
    assert progress.chapter_lab_state("b", "ch01", True) == "—"
    assert progress.chapter_lab_state("b", "ch01", False) == "—"
    progress.record_quiz("b", "ch01", 4, 4)
    assert progress.chapter_status("b", "ch01") == "studying"
    assert progress.book_mastery("b", 3) == "0/3"

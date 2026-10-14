"""SRS unit tests on synthetic data — no book. (SRS VR-002)"""
import io
import sqlite3
import sys

import pytest

from lib import srs

def test_sm2_first_pass():
    e, iv, reps = srs.sm2_update(2.5, 0, 0, 5)
    assert (iv, reps) == (1, 1) and e > 2.5

def test_sm2_env_tunability(monkeypatch):
    monkeypatch.setenv("TERMLEARN_INTERVAL_1_DAYS", "3")
    monkeypatch.setenv("TERMLEARN_INTERVAL_2_DAYS", "9")
    _, iv, _ = srs.sm2_update(2.5, 0, 0, 5)
    assert iv == 3
    _, iv, _ = srs.sm2_update(2.5, 1, 1, 4)
    assert iv == 9
    monkeypatch.setenv("TERMLEARN_INTERVAL_1_DAYS", "bogus")
    _, iv, _ = srs.sm2_update(2.5, 0, 0, 5)
    assert iv == 1  # unparseable falls back, never crashes
    monkeypatch.setenv("TERMLEARN_EASINESS_INIT", "3.0")
    import sqlite3
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE cards(id INTEGER PRIMARY KEY, book TEXT, chapter TEXT, front TEXT, back TEXT, concept TEXT, easiness REAL DEFAULT 2.5, interval INTEGER DEFAULT 0, reps INTEGER DEFAULT 0, next_due INTEGER DEFAULT 0)")
    srs.upsert_cards(con, "b", "c", [{"front": "F", "back": "B"}])
    assert con.execute("SELECT easiness FROM cards").fetchone()[0] == 3.0

def test_sm2_second_pass_six_days():
    e, iv, reps = srs.sm2_update(2.5, 1, 1, 4)
    assert iv == 6 and reps == 2

def test_sm2_fail_resets():
    e, iv, reps = srs.sm2_update(2.5, 10, 3, 1)
    assert (iv, reps) == (1, 0) and e < 2.5

def test_due_ordering_and_grade(tmp_path):
    con = sqlite3.connect(":memory:")
    con.execute("""CREATE TABLE cards(id INTEGER PRIMARY KEY, book TEXT, chapter TEXT,
      front TEXT, back TEXT, concept TEXT, easiness REAL DEFAULT 2.5,
      interval INTEGER DEFAULT 0, reps INTEGER DEFAULT 0, next_due INTEGER DEFAULT 0)""")
    con.execute("""CREATE TABLE answers(id INTEGER PRIMARY KEY, ts INTEGER, book TEXT,
      chapter TEXT, block TEXT, check_idx INTEGER, correct INTEGER, ms INTEGER)""")
    import time
    now = int(time.time())
    con.execute("INSERT INTO cards(book,chapter,front,back,next_due) VALUES(?,?,?,?,?)",
                ("b", "ch01", "overdue", "x", now - 10))
    con.execute("INSERT INTO cards(book,chapter,front,back,next_due) VALUES(?,?,?,?,?)",
                ("b", "ch01", "future", "y", now + 99999))
    due = srs.due_cards(con)
    assert [d["front"] for d in due] == ["overdue"]
    cid = due[0]["id"]
    srs.grade(con, cid, 5)
    assert srs.due_cards(con) == []  # rescheduled to future

def test_update_card_and_key_error():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE cards(id INTEGER PRIMARY KEY, front TEXT, back TEXT)")
    con.execute("INSERT INTO cards(front,back) VALUES('F','B')")
    f, b = srs.update_card(con, 1, "F2", None)
    assert (f, b) == ("F2", "B")
    with pytest.raises(KeyError):
        srs.update_card(con, 999, "x")


def test_edit_flow_inline(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    monkeypatch.delenv("VISUAL", raising=False)
    monkeypatch.delenv("EDITOR", raising=False)
    monkeypatch.setattr(sys, "stdin", io.StringIO("e\nEdited front\nEdited back\nq\n"))
    srs.run("extreme-c")
    from lib import progress
    con = sqlite3.connect(str(progress.db_path()))
    row = con.execute("SELECT front,back FROM cards WHERE book='extreme-c' LIMIT 1").fetchone()
    con.close()
    assert row[0] == "Edited front" and row[1] == "Edited back"


def test_topup_from_mastered(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    from lib import progress
    con = progress.init_db()
    con.execute("INSERT INTO test_runs(ts,book,chapter,passed,detail) VALUES(1,'extreme-c','ch04',1,'quiz=100% lab_ok=True')")
    con.commit()
    con.close()
    assert srs.mastered_topup(["extreme-c"], 2)[0][:2] == ("extreme-c", "ch04")
    monkeypatch.setattr(sys, "stdin", io.StringIO("f\n4\nf\n4\nf\n4\nf\n4\nf\n4\n"))
    srs.run("extreme-c")  # grades all 5 cards into the future
    monkeypatch.setattr(sys, "stdin", io.StringIO("5\n1\n"))
    srs.run("extreme-c")  # due=0 -> 2 top-up checks
    out = capsys.readouterr().out
    con = sqlite3.connect(str(progress.db_path()))
    rows = con.execute("SELECT concept FROM answers WHERE book='extreme-c'").fetchall()
    con.close()
    assert "Interleaved review" in out
    assert [r[0] for r in rows][-2:] == ["macro-expansion", "macro-expansion"]

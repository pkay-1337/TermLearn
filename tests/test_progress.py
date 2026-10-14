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


def test_block_progress_helpers(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    # 1. Unstarted block with 3 checks
    s0 = progress.block_status("extreme-c", "ch04", "b1", n_checks=3)
    assert s0["status"] == "not_started"
    assert s0["completed"] is False
    assert s0["attempted"] == 0

    # 2. Block with 0 checks (pure viz/theory)
    s_viz = progress.block_status("extreme-c", "ch04", "b_viz", n_checks=0)
    assert s_viz["status"] == "not_started"
    assert s_viz["completed"] is False
    progress.mark_block_completed("extreme-c", "ch04", "b_viz")
    s_viz_done = progress.block_status("extreme-c", "ch04", "b_viz", n_checks=0)
    assert s_viz_done["status"] == "completed"
    assert s_viz_done["completed"] is True

    # 3. Partially attempted block
    con = progress.init_db()
    con.execute("INSERT INTO answers(ts,book,chapter,block,check_idx,correct) VALUES(1,'extreme-c','ch04','b1',0,1)")
    con.commit()
    con.close()
    s_part = progress.block_status("extreme-c", "ch04", "b1", n_checks=3)
    assert s_part["status"] == "in_progress"
    assert s_part["completed"] is False
    assert s_part["attempted"] == 1
    assert s_part["correct"] == 1

    # 4. Fully answered block
    con = progress.init_db()
    con.execute("INSERT INTO answers(ts,book,chapter,block,check_idx,correct) VALUES(2,'extreme-c','ch04','b1',1,0)")
    con.execute("INSERT INTO answers(ts,book,chapter,block,check_idx,correct) VALUES(3,'extreme-c','ch04','b1',2,1)")
    con.commit()
    con.close()
    s_full = progress.block_status("extreme-c", "ch04", "b1", n_checks=3)
    assert s_full["status"] == "completed"
    assert s_full["completed"] is True
    assert s_full["attempted"] == 3
    assert s_full["correct"] == 2

    # 5. chapter_blocks_progress
    blocks = [
        {"id": "b1", "title": "Macros", "checks": [{}, {}, {}]},
        {"id": "b_viz", "title": "Memory Layout", "checks": []},
        {"id": "b2", "title": "Pointers", "checks": [{}]}
    ]
    all_p = progress.chapter_blocks_progress("extreme-c", "ch04", blocks)
    assert len(all_p) == 3
    assert all_p[0]["status"] == "completed"
    assert all_p[1]["status"] == "completed"
    assert all_p[2]["status"] == "not_started"


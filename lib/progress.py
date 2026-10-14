"""SQLite progress / SRS / telemetry. Single writer module. (SRS IF-SW-003, FR-STAT, FR-SRS)"""
import sqlite3
import time
from pathlib import Path


def db_path() -> Path:
    import os
    base = Path(os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local/share"))) / "termlearn"
    base.mkdir(parents=True, exist_ok=True)
    return base / "progress.db"


def init_db(db: Path | None = None) -> sqlite3.Connection:
    p = db or db_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(p))
    con.execute("""CREATE TABLE IF NOT EXISTS cards(
      id INTEGER PRIMARY KEY, book TEXT, chapter TEXT, front TEXT, back TEXT,
      concept TEXT, easiness REAL DEFAULT 2.5, interval INTEGER DEFAULT 0,
      reps INTEGER DEFAULT 0, next_due INTEGER DEFAULT 0)""")
    con.execute("""CREATE TABLE IF NOT EXISTS answers(
      id INTEGER PRIMARY KEY, ts INTEGER, book TEXT, chapter TEXT,
      block TEXT, check_idx INTEGER, correct INTEGER, ms INTEGER,
      concept TEXT DEFAULT '')""")
    con.execute("""CREATE TABLE IF NOT EXISTS quiz_runs(
      id INTEGER PRIMARY KEY, ts INTEGER, book TEXT, chapter TEXT,
      score INTEGER, total INTEGER, seed INTEGER, items TEXT DEFAULT '')""")
    con.execute("""CREATE TABLE IF NOT EXISTS test_runs(
      id INTEGER PRIMARY KEY, ts INTEGER, book TEXT, chapter TEXT,
      passed INTEGER, detail TEXT)""")
    con.execute("""CREATE TABLE IF NOT EXISTS solutions(
      hash TEXT PRIMARY KEY, ts INTEGER, book TEXT, chapter TEXT,
      passed INTEGER, code TEXT)""")
    # migrate pre-concept databases (D-02/03/08): answers.concept, quiz_runs.items
    cols_a = [r[1] for r in con.execute("PRAGMA table_info(answers)").fetchall()]
    if "concept" not in cols_a:
        con.execute("ALTER TABLE answers ADD COLUMN concept TEXT DEFAULT ''")
    cols = [r[1] for r in con.execute("PRAGMA table_info(quiz_runs)").fetchall()]
    if "items" not in cols:
        con.execute("ALTER TABLE quiz_runs ADD COLUMN items TEXT DEFAULT ''")
    con.commit()
    return con


def record_quiz(book: str, chapter: str, score: int, total: int,
                seed: int | None = None, items: list[str] | None = None):
    import json
    con = init_db()
    con.execute("INSERT INTO quiz_runs(ts,book,chapter,score,total,seed,items) VALUES(?,?,?,?,?,?,?)",
                (int(time.time()), book, chapter, score, total, seed or 0,
                 json.dumps(items or [])))
    con.commit()
    con.close()


def get_last_quiz(book: str, chapter: str) -> dict | None:
    con = init_db()
    row = con.execute("SELECT score,total,ts FROM quiz_runs WHERE book=? AND chapter=? "
                      "ORDER BY id DESC LIMIT 1", (book, chapter)).fetchone()
    con.close()
    if row is None:
        return None
    return {"score": row[0], "total": row[1], "ts": row[2]}


def record_test(book: str, chapter: str, quiz_score: dict | None,
                lab_result: dict | None, force: bool = False) -> bool:
    """Chapter gate: needs recorded quiz >= min_quiz (from pack test.gates) + lab pass.
    Returns True on pass (or --force override, logged). (FR-TEST-002..003)"""
    from rich.console import Console
    from lib.pack import load_chapter
    c = Console()
    try:
        data = load_chapter(book, chapter)
    except FileNotFoundError as e:
        c.print(f"[red]{e}[/red]")
        return False
    test = data.get("test") or {}
    min_quiz = 80
    for g in test.get("gates", []):
        min_quiz = g.get("min_quiz", min_quiz)
    quiz_pct = 0.0
    if quiz_score and quiz_score.get("total"):
        quiz_pct = 100.0 * quiz_score["score"] / quiz_score["total"]
    elif (last := get_last_quiz(book, chapter)) and last["total"]:
        quiz_pct = 100.0 * last["score"] / last["total"]
    lab_na = bool(lab_result and lab_result.get("passed") is None and data.get("lab"))
    lab_ok = bool(lab_result and lab_result.get("passed") is True)
    lab_required = bool(data.get("lab") or test.get("gates")) and not lab_na
    passed = quiz_pct >= min_quiz and (lab_ok or not lab_required)
    con = init_db()
    con.execute("INSERT INTO test_runs(ts,book,chapter,passed,detail) VALUES(?,?,?,?,?)",
                (int(time.time()), book, chapter, 1 if passed or force else 0,
                 f"quiz={quiz_pct:.0f}% lab_ok={lab_ok} force={force}"))
    con.commit()
    con.close()
    if passed:
        c.print(f"[green]PASS {book}/{chapter}: quiz {quiz_pct:.0f}% (>= {min_quiz}%), lab_ok={lab_ok}[/green]")
        return True
    c.print(f"[red]FAIL {book}/{chapter}: quiz {quiz_pct:.0f}% (need {min_quiz}%), lab_ok={lab_ok}[/red]")
    if force:
        c.print("[yellow]--force: advancing anyway (logged).[/yellow]")
        return True
    c.print("[dim]Improve with: study, quiz, lab — then re-run test.[/dim]")
    return False


def chapter_stats(book: str) -> list[dict]:
    """Per-chapter accuracy + counts for stats mode. (FR-STAT-001)"""
    con = init_db()
    rows = con.execute("SELECT chapter, SUM(correct), COUNT(*) FROM answers "
                       "WHERE book=? GROUP BY chapter", (book,)).fetchall()
    latest: dict = {}
    for r in con.execute("SELECT chapter,score,total FROM quiz_runs WHERE book=? ORDER BY id DESC", (book,)):
        latest.setdefault(r[0], {"score": r[1], "total": r[2]})
    con.close()
    return [{"chapter": ch, "hits": hits, "total": tot,
             "last_quiz": latest.get(ch)} for ch, hits, tot in rows]


def _db_or_none():
    try:
        return init_db()
    except Exception:
        return None


def book_mastery(book: str, n_pack_chapters: int = 0) -> str:
    """Mastery display for the book picker (FR-BOOK-002, D-13): passed-test
    chapters over pack chapters, e.g. '1/3'. '—' when nothing recorded."""
    con = _db_or_none()
    if con is None:
        return "—"
    try:
        passed = {r[0] for r in con.execute(
            "SELECT DISTINCT chapter FROM test_runs WHERE book=? AND passed=1",
            (book,)).fetchall()}
        active = {r[0] for r in con.execute(
            "SELECT DISTINCT chapter FROM answers WHERE book=?", (book,)).fetchall()}
        active |= {r[0] for r in con.execute(
            "SELECT DISTINCT chapter FROM quiz_runs WHERE book=?", (book,)).fetchall()}
    finally:
        con.close()
    if not active and not passed:
        return "—"
    denom = n_pack_chapters or max(len(passed | active), 1)
    return f"{len(passed)}/{denom}"


def chapter_status(book: str, chapter: str) -> str:
    """new | studying | mastered (FR-CHAP-001, D-14)."""
    con = _db_or_none()
    if con is None:
        return "new"
    try:
        row = con.execute("SELECT passed FROM test_runs WHERE book=? AND chapter=? "
                          "ORDER BY id DESC LIMIT 1", (book, chapter)).fetchone()
        if row and row[0]:
            return "mastered"
        n = con.execute("SELECT COUNT(*) FROM answers WHERE book=? AND chapter=?",
                        (book, chapter)).fetchone()[0]
        n += con.execute("SELECT COUNT(*) FROM quiz_runs WHERE book=? AND chapter=?",
                         (book, chapter)).fetchone()[0]
        return "studying" if n else "new"
    finally:
        con.close()


def chapter_due_count(book: str, chapter: str) -> int:
    """SRS due cards for one chapter (FR-CHAP-001, D-14)."""
    import time
    con = _db_or_none()
    if con is None:
        return 0
    try:
        return con.execute("SELECT COUNT(*) FROM cards WHERE book=? AND chapter=? "
                           "AND next_due<=?", (book, chapter, int(time.time()))).fetchone()[0]
    except Exception:
        return 0
    finally:
        con.close()


def chapter_lab_state(book: str, chapter: str, has_lab: bool = False) -> str:
    """pass | fail | — from the latest test_runs detail (FR-CHAP-001, D-14).
    '—' when the pack has no lab (nothing gateable)."""
    if not has_lab:
        return "—"
    con = _db_or_none()
    if con is None:
        return "—"
    try:
        row = con.execute("SELECT detail FROM test_runs WHERE book=? AND chapter=? "
                          "ORDER BY id DESC LIMIT 1", (book, chapter)).fetchone()
    finally:
        con.close()
    if not row or not row[0]:
        return "—"
    return "pass" if "lab_ok=True" in row[0] else "fail"


def concept_stats(book: str) -> list[dict]:
    """Per-concept hits/total + representative block (most-missed block for
    the concept). (FR-STAT-001, D-08.)"""
    con = _db_or_none()
    if con is None:
        return []
    try:
        rows = con.execute(
            "SELECT concept, SUM(correct), COUNT(*) FROM answers "
            "WHERE book=? GROUP BY concept", (book,)).fetchall()
        out = []
        for concept, hits, tot in rows:
            brow = con.execute(
                "SELECT block, SUM(correct), COUNT(*) FROM answers "
                "WHERE book=? AND concept=? GROUP BY block "
                "ORDER BY CAST(SUM(correct) AS FLOAT)/COUNT(*) ASC LIMIT 1",
                (book, concept)).fetchone()
            out.append({"concept": concept or "—", "hits": hits or 0,
                        "total": tot,
                        "block": brow[0] if brow else "—"})
        return out
    finally:
        con.close()

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
    con.execute("""CREATE TABLE IF NOT EXISTS block_progress(
      id INTEGER PRIMARY KEY, ts INTEGER, book TEXT, chapter TEXT,
      block TEXT, completed INTEGER DEFAULT 1,
      UNIQUE(book, chapter, block))""")
    con.execute("""CREATE TABLE IF NOT EXISTS lab_runs(
      id INTEGER PRIMARY KEY AUTOINCREMENT, ts INTEGER, book TEXT, chapter TEXT,
      lab_id TEXT, passed INTEGER, output TEXT DEFAULT '', elapsed_ms INTEGER DEFAULT 0)""")
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


def mark_block_completed(book: str, chapter: str, block: str) -> None:
    """Record that a study block was completed by the user."""
    con = _db_or_none()
    if con is None:
        return
    try:
        con.execute(
            "INSERT INTO block_progress(ts, book, chapter, block, completed) "
            "VALUES(?, ?, ?, ?, 1) "
            "ON CONFLICT(book, chapter, block) DO UPDATE SET ts=excluded.ts, completed=1",
            (int(time.time()), book, chapter, block),
        )
        con.commit()
    finally:
        con.close()


def block_status(book: str, chapter: str, block_id: str, n_checks: int = 0) -> dict:
    """Returns detailed completion status for a specific block."""
    con = _db_or_none()
    if con is None:
        return {"status": "not_started", "completed": False, "attempted": 0, "correct": 0, "total": n_checks}
    try:
        bp = con.execute(
            "SELECT completed FROM block_progress WHERE book=? AND chapter=? AND block=?",
            (book, chapter, block_id)
        ).fetchone()
        is_done = bool(bp and bp[0])

        rows = con.execute(
            "SELECT check_idx, correct FROM answers WHERE book=? AND chapter=? AND block=?",
            (book, chapter, block_id)
        ).fetchall()
        attempted_indices = {r[0] for r in rows}
        correct_count = sum(1 for r in rows if r[1] == 1)

        if n_checks > 0:
            if is_done or len(attempted_indices) >= n_checks:
                status = "completed"
                completed = True
            elif len(attempted_indices) > 0:
                status = "in_progress"
                completed = False
            else:
                status = "not_started"
                completed = False
        else:
            status = "completed" if is_done else "not_started"
            completed = is_done

        return {
            "status": status,
            "completed": completed,
            "attempted": len(attempted_indices),
            "correct": correct_count,
            "total": n_checks,
        }
    finally:
        con.close()


def chapter_blocks_progress(book: str, chapter: str, blocks: list[dict]) -> list[dict]:
    """Batch-fetches progress status for all blocks in a chapter."""
    out = []
    for b in blocks:
        bid = b.get("id", "?")
        n_ck = len(b.get("checks", []) or [])
        st = block_status(book, chapter, bid, n_ck)
        st["id"] = bid
        st["title"] = b.get("title", bid)
        out.append(st)
    return out


def wipe_chapter_progress(book: str, chapter: str) -> None:
    """Wipe all recorded progress and analytics for a specific chapter."""
    con = _db_or_none()
    if con is None:
        return
    try:
        for tbl in ("answers", "quiz_runs", "test_runs", "cards", "block_progress", "solutions", "lab_runs"):
            try:
                con.execute(f"DELETE FROM {tbl} WHERE book=? AND chapter=?", (book, chapter))
            except Exception:
                pass
        con.commit()
    finally:
        con.close()


def record_lab_run(book: str, chapter: str, lab_id: str, passed: bool,
                   output: str = "", elapsed_ms: int = 0) -> None:
    """Records the outcome of a lab test execution."""
    con = init_db()
    con.execute("INSERT INTO lab_runs(ts,book,chapter,lab_id,passed,output,elapsed_ms) VALUES(?,?,?,?,?,?,?)",
                (int(time.time()), book, chapter, lab_id, 1 if passed else 0, output, elapsed_ms))
    con.commit()
    con.close()


record_lab_result = record_lab_run


def is_lab_passed(book: str, chapter: str, lab_id: str) -> bool:
    """Returns True if the lab has been successfully passed."""
    con = _db_or_none()
    if con is None:
        return False
    try:
        row = con.execute("SELECT MAX(passed) FROM lab_runs WHERE book=? AND chapter=? AND lab_id=?",
                          (book, chapter, lab_id)).fetchone()
        return bool(row and row[0] == 1)
    finally:
        con.close()


def get_chapter_labs_status(book: str, chapter: str, labs: list[dict]) -> list[dict]:
    """Batch-fetches pass status for all labs in a chapter."""
    out = []
    con = _db_or_none()
    try:
        for lb in labs:
            lid = lb.get("id", "lab1")
            passed = False
            if con is not None:
                row = con.execute("SELECT MAX(passed) FROM lab_runs WHERE book=? AND chapter=? AND lab_id=?",
                                  (book, chapter, lid)).fetchone()
                passed = bool(row and row[0] == 1)
            out.append({
                "id": lid,
                "title": lb.get("title", lid),
                "passed": passed
            })
    finally:
        if con is not None:
            con.close()
    return out




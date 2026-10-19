"""SM-2 scheduler + due queue + SQLite backing. (SRS FR-SRS-001..004)"""
import os
import sqlite3
import time
from pathlib import Path

from lib.progress import db_path


def sm2_config() -> dict:
    """Scheduling parameters from TERMLEARN_* env (FR-SRS-004, D-12).
    Unparseable values fall back to defaults — scheduling never crashes."""

    def num(name: str, default: float) -> float:
        try:
            return float(os.environ.get(name, default))
        except (TypeError, ValueError):
            return default

    return {
        "easiness_init": num("TERMLEARN_EASINESS_INIT", 2.5),
        "easiness_min": num("TERMLEARN_EASINESS_MIN", 1.3),
        "interval_1": int(num("TERMLEARN_INTERVAL_1_DAYS", 1)),
        "interval_2": int(num("TERMLEARN_INTERVAL_2_DAYS", 6)),
    }


def sm2_update(easiness: float, interval: int, reps: int, quality: int):
    """Pure SM-2 step (testable, VR-002). quality 0..5."""
    cfg = sm2_config()
    emin = cfg["easiness_min"]
    if not (0 <= quality <= 5):
        raise ValueError("quality must be 0..5")
    if quality < 3:
        return (max(emin, easiness - 0.2), 1, 0)
    if reps == 0:
        interval = cfg["interval_1"]
    elif reps == 1:
        interval = cfg["interval_2"]
    else:
        interval = round(interval * easiness)
    easiness = max(emin, easiness + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    return (easiness, interval, reps + 1)


def init_db(db: Path | None = None) -> sqlite3.Connection:
    from lib.progress import init_db as _pinit
    return _pinit(db)


def upsert_cards(con: sqlite3.Connection, book: str, chapter: str, cards: list[dict]):
    now = int(time.time())
    einit = sm2_config()["easiness_init"]
    for cd in cards:
        row = con.execute("SELECT id FROM cards WHERE book=? AND chapter=? AND front=?",
                          (book, chapter, cd.get("front", ""))).fetchone()
        if row is None:
            con.execute("INSERT INTO cards(book,chapter,front,back,concept,easiness,next_due) VALUES(?,?,?,?,?,?,?)",
                        (book, chapter, cd.get("front", ""), cd.get("back", ""),
                         cd.get("concept", ""), einit, now))
    con.commit()


def due_cards(con: sqlite3.Connection, book: str | None = None, limit: int = 50) -> list[dict]:
    now = int(time.time())
    q = "SELECT id,book,chapter,front,back,concept,easiness,interval,reps FROM cards WHERE next_due<=?"
    args: list = [now]
    if book:
        q += " AND book=?"
        args.append(book)
    q += " ORDER BY next_due LIMIT ?"
    args.append(limit)
    cols = ["id", "book", "chapter", "front", "back", "concept", "easiness", "interval", "reps"]
    return [dict(zip(cols, r)) for r in con.execute(q, args).fetchall()]


def grade(con: sqlite3.Connection, card_id: int, quality: int):
    row = con.execute("SELECT easiness,interval,reps FROM cards WHERE id=?", (card_id,)).fetchone()
    if row is None:
        raise KeyError(card_id)
    e, iv, reps = sm2_update(float(row[0]), int(row[1]), int(row[2]), quality)
    nxt = int(time.time()) + iv * 86400
    con.execute("UPDATE cards SET easiness=?,interval=?,reps=?,next_due=? WHERE id=?",
                (e, iv, reps, nxt, card_id))
    con.commit()


def update_card(con: sqlite3.Connection, card_id: int,
                front: str | None = None, back: str | None = None):
    """In-place card edit; empty/None keeps the old side. (FR-SRS-002, D-07)"""
    row = con.execute("SELECT front,back FROM cards WHERE id=?", (card_id,)).fetchone()
    if row is None:
        raise KeyError(card_id)
    new_front = front if front else row[0]
    new_back = back if back else row[1]
    con.execute("UPDATE cards SET front=?,back=? WHERE id=?",
                (new_front, new_back, card_id))
    con.commit()
    return new_front, new_back


def mastered_topup(slugs: list[str], n: int) -> list[tuple[str, str, str, int, dict]]:
    """Up to n quiz checks (author order) from mastered chapters.
    Returns (book, chapter, block, idx, check) tuples. (FR-SRS-003, D-11)"""
    import yaml
    from lib.books import discover_chapters
    from lib.progress import chapter_status
    from lib.quiz import collect_checks
    out = []
    for slug in slugs:
        for ch in discover_chapters(slug):
            if chapter_status(slug, ch["id"]) != "mastered":
                continue
            try:
                from lib.pack import load_chapter_mode
                data = load_chapter_mode(slug, ch["id"], "study")
            except Exception:
                continue
            for block_id, idx, ck in collect_checks(data):
                out.append((slug, ch["id"], block_id, idx, ck))
                if len(out) >= n:
                    return out
    return out


def log_answer(con: sqlite3.Connection, book: str, chapter: str, block: str,
               idx: int, correct: bool, ms: int = 0, concept: str = ""):
    con.execute("INSERT INTO answers(ts,book,chapter,block,check_idx,correct,ms,concept) VALUES(?,?,?,?,?,?,?,?)",
                (int(time.time()), book, chapter, block, idx, 1 if correct else 0, ms, concept or ""))
    con.commit()


def run(book=None):
    from rich.console import Console
    con = init_db()
    # sync cards from packs into db (idempotent)
    import yaml
    from lib.books import discover_chapters
    from lib.pack import load_chapter_mode
    slugs = [book] if book else [b["slug"] for b in __import__("lib.books", fromlist=["x"]).discover_books()]
    for slug in slugs:
        for ch in discover_chapters(slug):
            if not ch.get("has_pack"):
                continue
            try:
                data = load_chapter_mode(slug, ch["id"], "cards")
                if data.get("cards"):
                    upsert_cards(con, slug, ch["id"], data["cards"])
            except Exception:
                continue
    due = due_cards(con, book)
    c = Console()
    topup = mastered_topup(slugs, max(0, min(2, 5 - len(due)))) if len(due) < 5 else []
    if not due and not topup:
        c.print("[green]Nothing due. Add packs with cards first, or come back tomorrow.[/green]")
        return
    if due:
        c.print(f"[bold]{len(due)} card(s) due. Keys: f=flip, e=edit, 1-4 grade, ?=help, q=quit[/bold]")
    from lib import keys as _k
    quit_early = False
    for card in due:
        c.print(f"\n[bold cyan]Q:[/bold cyan] {card['front']}")
        cmd = _k.ask(c, "flip? [f/e/?/q] ", "srs").lower()
        if cmd == "q":
            quit_early = True
            break
        if cmd == "e":
            front, back = edit_card(c, con, card)
            card["front"], card["back"] = front, back
            c.print(f"\n[bold cyan]Q:[/bold cyan] {card['front']}")
            cmd = _k.ask(c, "flip? [f/?/q] ", "srs").lower()
            if cmd == "q":
                quit_early = True
                break
        c.print(f"[green]A:[/green] {card['back']}")
        while True:
            g = _k.ask(c, "grade 1 forgot · 2 hard · 3 good · 4 easy · ? help · q quit: ", "srs")
            if g == "q":
                quit_early = True
                break
            if g in ("1", "2", "3", "4"):
                qmap = {"1": 0, "2": 3, "3": 4, "4": 5}
                grade(con, card["id"], qmap[g])
                break
        if quit_early:
            break
    if quit_early:
        con.close()
        return
    if topup:
        from lib.quiz import run_check
        c.print("[bold]\nInterleaved review from mastered chapters:[/bold]")
        for tb, tch, tbl, tidx, tck in topup:
            try:
                ok, ms = run_check(c, tbl, tidx, tck, None, tb)
            except KeyboardInterrupt:
                break
            log_answer(con, tb, tch, tbl, tidx, ok, ms,
                       concept=str(tck.get("concept", "")))
    con.close()


def edit_card(c, con: sqlite3.Connection, card: dict) -> tuple[str, str]:
    """Edit front/back via $EDITOR (whole card) or inline prompts.
    Empty input keeps the old side. (FR-SRS-002, D-07)"""
    import os
    import subprocess
    import tempfile
    from lib import keys as _k
    ed = os.environ.get("VISUAL") or os.environ.get("EDITOR")
    if ed:
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write(f"{card['front']}\n---\n{card['back']}\n")
            path = f.name
        subprocess.run([ed, path])
        parts = Path(path).read_text(encoding="utf-8").split("\n---\n", 1)
        front = parts[0].strip()
        back = parts[1].strip() if len(parts) > 1 else ""
        return update_card(con, card["id"], front or None, back or None)
    front = _k.ask(c, "new front (empty keeps) · ? help: ", "srs")
    back = _k.ask(c, "new back (empty keeps) · ? help: ", "srs")
    return update_card(con, card["id"], front or None, back or None)

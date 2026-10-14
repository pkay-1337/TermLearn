"""Stats / telemetry reporting + progress reset. Local-only. (SRS FR-STAT-001..003)"""

def reset_progress(book: str, chapter: str | None = None):
    """Wipe progress for a book (or chapter) after explicit confirmation. (FR-STAT-003)"""
    from rich.console import Console
    from lib.srs import init_db
    console = Console()
    scope = f"{book}/{chapter}" if chapter else book
    confirm = console.input(f"Type DELETE to wipe all progress for {scope}: ").strip()
    if confirm != "DELETE":
        console.print("[dim]cancelled — nothing wiped.[/dim]")
        return
    con = init_db()
    for tbl in ("answers", "quiz_runs", "test_runs", "cards"):
        if chapter:
            con.execute(f"DELETE FROM {tbl} WHERE book=? AND chapter=?", (book, chapter))
        else:
            con.execute(f"DELETE FROM {tbl} WHERE book=?", (book,))
    con.commit()
    con.close()
    console.print(f"[green]wiped {scope}.[/green]")


def run(book: str):
    from rich.console import Console
    from rich.table import Table
    from lib.srs import init_db, due_cards
    from lib.progress import concept_stats
    console = Console()
    con = init_db()
    rows = con.execute("SELECT chapter,block,SUM(correct),COUNT(*) FROM answers "
                       "WHERE book=? GROUP BY chapter,block", (book,)).fetchall()
    runs = list(con.execute("SELECT chapter,score,total,ts FROM quiz_runs WHERE book=? "
                            "ORDER BY id DESC LIMIT 20", (book,)).fetchall())
    due = due_cards(con, book, limit=1000)
    con.close()
    if not rows and not runs:
        console.print("[yellow]No data yet — run study/quiz first.[/yellow]")
        return
    if rows:
        t = Table(title=f"accuracy — {book}")
        t.add_column("chapter"); t.add_column("block"); t.add_column("hits"); t.add_column("total"); t.add_column("pct")
        for ch, bl, hits, tot in sorted(rows):
            pct = f"{100.0 * (hits or 0) / tot:.0f}%" if tot else "-"
            t.add_row(ch, bl, str(hits or 0), str(tot), pct)
        console.print(t)
        weak = sorted([r for r in rows if ((r[2] or 0) / r[3]) < 1],
                      key=lambda r: ((r[2] or 0) / r[3]) if r[3] else 1)[:3]
        console.print("[bold]weakest:[/bold] " + ", ".join(f"{r[0]}/{r[1]}" for r in weak)
                      if weak else "[green]no weak spots — all 100%[/green]")
    concepts = concept_stats(book)
    if concepts:
        ct = Table(title=f"concepts — {book}")
        ct.add_column("concept"); ct.add_column("hits"); ct.add_column("total")
        ct.add_column("pct"); ct.add_column("see block")
        for c in sorted(concepts, key=lambda r: r["concept"]):
            pct = f"{100.0 * c['hits'] / c['total']:.0f}%" if c["total"] else "-"
            ct.add_row(c["concept"], str(c["hits"]), str(c["total"]), pct, c["block"])
        console.print(ct)
        weak_c = sorted([c for c in concepts if c["hits"] < c["total"]],
                        key=lambda r: r["hits"] / r["total"])[:3]
        console.print("[bold]weakest concepts:[/bold] " + ", ".join(c["concept"] for c in weak_c)
                      if weak_c else "[green]no weak concepts — all 100%[/green]")
    if runs:
        console.print("[bold]recent quiz runs:[/bold] " +
                      ", ".join(f"{r[0]}:{r[1]}/{r[2]}" for r in runs[:5]))
    console.print(f"[bold]srs due:[/bold] {len(due)} card(s)")

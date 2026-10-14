"""Study mode: learn-first traversal of concept blocks. (SRS FR-STUDY-001..006)"""
import random


def run(book: str, chapter: str):
    import yaml
    from rich.console import Console
    from rich.syntax import Syntax
    from rich.panel import Panel
    from lib.pack import require_chapter
    from lib.quiz import run_check
    from lib.srs import init_db, log_answer
    from lib import keys as _k
    from lib import pager as _pager
    console = Console()
    try:
        data = yaml.safe_load(require_chapter(book, chapter).read_text(encoding="utf-8"))
    except FileNotFoundError:
        console.print(f"[yellow]No pack for {book}/{chapter} yet.[/yellow]")
        return
    console.print(f"[bold]{data.get('meta', {}).get('title', chapter)}[/bold]")
    objs = data.get("objectives", [])
    if objs:
        console.print(Panel("\n".join(f"- {o}" for o in objs), title="objectives"))
    con = init_db()
    try:
        for b in data.get("blocks", []):
            console.print(f"\n[bold cyan]━━ {b.get('title', b.get('id'))}[/bold cyan]")
            if not _pager.show(console, str(b.get("explain_md", ""))):
                break
            ex = b.get("example") or {}
            if ex.get("code"):
                console.print(Syntax(ex["code"], ex.get("lang", "c"), theme="monokai",
                                     line_numbers=False))
                if ex.get("run_expected"):
                    cmd = _k.ask(console, "r run example · Enter continue · ? help · q quit: ",
                                 "study").lower()
                    if cmd == "q":
                        break
                    if cmd == "r":
                        from lib.lab import run_code
                        r = run_code(ex["code"], ex.get("lang", "c"), timeout=2, book=book)
                        if r.get("unsupported"):
                            console.print(f"[yellow]no local runner for '{r['lang']}' — "
                                          f"run it in the book's toolchain.[/yellow]")
                        elif not r["compiled"]:
                            console.print(f"[red]compile error:[/red]\n{r['stderr'][:1500]}")
                        elif r["timed_out"]:
                            console.print("[red]timeout[/red]")
                        else:
                            console.print(f"[green]output:[/green]\n{r['output'][:2000]}")
            viz = b.get("viz") or {}
            steps = viz.get("steps", [])
            if steps:
                console.print(f"[dim]visualization ({viz.get('kind', 'steps')}): n step · s skip · ? help[/dim]")
                for s in steps:
                    k = _k.ask(console, f"  {s} [n/s/q/?]: ", "study").lower()
                    if k == "q":
                        con.close()
                        return
                    if k == "s":
                        break
            rng = None  # study keeps author order (teaching moment, reproducible);
            # shuffling lives in quiz mode via --seed (FR-QUIZ-001)
            for i, ck in enumerate(b.get("checks", [])):
                try:
                    ok, ms = run_check(console, b.get("id", "?"), i, ck, rng, book)
                except KeyboardInterrupt:
                    con.close()
                    return
                log_answer(con, book, chapter, b.get("id", "?"), i, ok, ms,
                           concept=str(ck.get("concept", "")))
                if not ok:
                    # FR-STUDY-002: remediation, not bare "wrong"
                    console.print(f"[yellow]revisit:[/yellow] {ck.get('why', '')}")
                    more = _k.ask(console, "see example again? [y/N/?] ", "study").lower()
                    if more == "y" and ex.get("code"):
                        console.print(Syntax(ex["code"], ex.get("lang", "c"), theme="monokai"))
    finally:
        con.close()
    console.print("\n[green]chapter study pass complete — try `quiz`, `parsons`, `lab`, then `test`.[/green]")

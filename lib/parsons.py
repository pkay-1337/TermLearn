"""Parsons ordering interaction. (SRS FR-PAR-001..003)

Contract: check = {lines: [...pool...], answer_order: [idx...], why, distractor_why?: {line: reason}}.
`lines` is the author-scrambled pool; `answer_order` lists pool indices in correct
sequence (distractor lines are simply absent from answer_order).
User enters 1-based numbers, e.g. `3 1 2`.
"""
import random


def display_order(console, ck: dict, rng=None) -> tuple[list[str], list[int]]:
    lines = list(ck.get("lines", []))
    idx = list(range(len(lines)))
    if rng is None:
        return lines, idx  # author order; answer_order refers to these positions
    rng.shuffle(idx)
    return [lines[i] for i in idx], idx


def ask_order(console, ck: dict, rng=None) -> bool:
    from lib import keys as _k
    shown, pos = display_order(console, ck, rng)
    # map displayed position -> original index
    for i, line in enumerate(shown, 1):
        console.print(f"  {i}. {line}")
    raw = _k.ask(console, "order e.g. `2 1 3` · s reshuffle · h hint · ? help · q quit: ",
                 "parsons").lower()
    if raw == "q":
        raise KeyboardInterrupt
    if raw == "h":
        console.print(f"[dim]hint: {ck.get('hint', ck.get('why', 'look for the setup line first'))}[/dim]")
        return ask_order(console, ck, rng=None)  # keep same display
    if raw == "s":
        return ask_order(console, ck, rng=rng)
    try:
        picked = [int(x) - 1 for x in raw.split()]
    except ValueError:
        picked = []
    # translate displayed picks back to original indices
    try:
        picked_orig = [pos[p] for p in picked]
    except IndexError:
        picked_orig = []
    want = list(ck.get("answer_order", []))
    ok = (picked_orig == want)
    if ok:
        console.print("[green]correct order[/green]")
    else:
        # FR-PAR-002: name the bug class when a distractor was chosen
        dwhy = ck.get("distractor_why", {}) or {}
        named = [dwhy.get(shown[p], "") for p in picked if 0 <= p < len(shown)]
        named = [n for n in named if n]
        if named:
            console.print(f"[red]distractor picked — {named[0]}[/red]")
        else:
            console.print("[red]wrong order[/red]")
    console.print(f"[dim]why: {ck.get('why', '')}[/dim]")
    return ok


def run(book: str, chapter: str):
    """Ordering-only session over the chapter's `order` checks."""
    import yaml
    from rich.console import Console
    from lib.pack import require_chapter
    from lib.srs import init_db, log_answer
    console = Console()
    try:
        data = yaml.safe_load(require_chapter(book, chapter).read_text(encoding="utf-8"))
    except FileNotFoundError:
        console.print(f"[yellow]No pack for {book}/{chapter} yet: run gen-prompt, paste YAML to packs/{book}/{chapter}.yaml, then validate.[/yellow]")
        return
    items = [(b.get("id", "?"), i, ck) for b in data.get("blocks", [])
             for i, ck in enumerate(b.get("checks", [])) if ck.get("kind") == "order"]
    if not items:
        console.print("[yellow]No order (Parsons) checks in this pack.[/yellow]")
        return
    con = init_db()
    try:
        for block_id, idx, ck in items:
            console.print(f"\n[bold][order][/bold] {ck.get('q', '')}")
            try:
                ok = ask_order(console, ck)
            except KeyboardInterrupt:
                break
            log_answer(con, book, chapter, block_id, idx, ok,
                       concept=str(ck.get("concept", "")))
    finally:
        con.close()

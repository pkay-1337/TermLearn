"""Revise mode: passive notes + concepts, no scoring. (SRS FR-REV-001..002)"""

def run(book: str, chapter: str):
    import yaml
    from rich.console import Console
    from rich.syntax import Syntax
    from lib.pack import load_chapter_mode
    from lib import pager as _pager
    console = Console()
    try:
        data = load_chapter_mode(book, chapter, "revise")
    except FileNotFoundError:
        console.print(f"[yellow]No pack for {book}/{chapter} yet.[/yellow]")
        return
    console.print(f"[bold]{data.get('meta', {}).get('title', chapter)}[/bold] [dim](revise — no scoring)[/dim]")
    for b in data.get("blocks", []):
        console.print(f"\n[bold cyan]━━ {b.get('title', b.get('id'))}[/bold cyan]")
        if not _pager.show(console, str(b.get("explain_md", ""))):
            return
        ex = b.get("example") or {}
        if ex.get("code"):
            console.print(Syntax(ex["code"], ex.get("lang", "c"), theme="monokai"))
            # SPEC-EXPL-003 F1: explanation right after the code (no scoring)
            emd = ex.get("explain_md")
            if isinstance(emd, str) and emd.strip() and not _pager.show(console, emd):
                return
        # SPEC-EXPL-003 F2: diagram, final step only, unstepped/unscored
        diag = b.get("diagram") or {}
        if isinstance(diag, dict) and diag.get("kind"):
            from lib.diagram import render as _diagram_render
            darts = _diagram_render(diag)
            if darts:
                if diag.get("caption"):
                    console.print(f"[dim]{diag['caption']}[/dim]")
                console.print(darts[-1])
        bugs = b.get("common_bugs", [])
        if bugs:
            console.print("[yellow]common bugs:[/yellow] " + "; ".join(bugs))

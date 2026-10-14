"""Revise mode: passive notes + concepts, no scoring. (SRS FR-REV-001..002)"""

def run(book: str, chapter: str):
    import yaml
    from rich.console import Console
    from rich.syntax import Syntax
    from lib.pack import require_chapter
    from lib import pager as _pager
    console = Console()
    try:
        data = yaml.safe_load(require_chapter(book, chapter).read_text(encoding="utf-8"))
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
        bugs = b.get("common_bugs", [])
        if bugs:
            console.print("[yellow]common bugs:[/yellow] " + "; ".join(bugs))

"""Markdown export. Hidden tests excluded. (SRS FR-EXP-001..002)"""

def build_markdown(data: dict) -> str:
    L = [f"# {data.get('meta', {}).get('title', '')}", ""]
    for o in data.get("objectives", []):
        L.append(f"- {o}")
    L.append("")
    for b in data.get("blocks", []):
        L.append(f"## {b.get('title', b.get('id'))}")
        L.append("")
        L.append(str(b.get("explain_md", "")))
        L.append("")
        ex = b.get("example") or {}
        if ex.get("code"):
            L.append(f"```{ex.get('lang', 'c')}")
            L.append(ex["code"])
            L.append("```")
            L.append("")
            # SPEC-EXPL-003 F1 (FR-EXPL-003): explanation follows the code
            emd = ex.get("explain_md")
            if isinstance(emd, str) and emd.strip():
                L.append(emd)
                L.append("")
        # SPEC-EXPL-003 F2 (FR-DIAG-005): diagram as fenced block (final step)
        diag = b.get("diagram") or {}
        if isinstance(diag, dict) and diag.get("kind"):
            from lib.diagram import render as _diagram_render
            darts = _diagram_render(diag)
            if darts:
                if diag.get("caption"):
                    L.append(f"*{diag['caption']}*")
                    L.append("")
                L.append("```text")
                L.append(darts[-1])
                L.append("```")
                L.append("")
        L.append(f"*source: {data.get('meta', {}).get('source_ref', '')} / block {b.get('id')}*")
        L.append("")
    lab = data.get("lab") or {}
    if lab:
        # FR-EXP-002: prompt + starter only; hidden test bodies excluded
        L.append(f"## Lab: {lab.get('title', '')}")
        L.append("")
        L.append(str(lab.get("prompt_md", "")))
        L.append("")
        if lab.get("starter_c"):
            L.append("```c")
            L.append(lab["starter_c"])
            L.append("```")
    return "\n".join(L)


def run(book: str, chapter=None, fmt: str = "md", out: str | None = None):
    import yaml
    from rich.console import Console
    from lib.pack import require_chapter
    from lib.books import discover_chapters
    from pathlib import Path
    console = Console()
    if fmt != "md":
        console.print("[red]only --format md is supported in v0.1[/red]")
        return
    targets = [chapter] if chapter else [c["id"] for c in discover_chapters(book)]
    pieces = []
    for cid in targets:
        try:
            from lib.pack import load_chapter
            data = load_chapter(book, cid)
        except FileNotFoundError:
            console.print(f"[yellow]skip {cid}: no pack yet.[/yellow]")
            continue
        pieces.append(build_markdown(data))
    if not pieces:
        console.print("[yellow]Nothing to export — generate + validate a pack first.[/yellow]")
        return
    text = "\n\n".join(pieces)
    if out:
        Path(out).write_text(text + "\n", encoding="utf-8")
        console.print(f"[green]wrote {out}[/green]")
    else:
        console.print(text)

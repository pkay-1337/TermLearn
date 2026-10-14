"""--more pager for long-form renders. (SRS IF-CLI-005, D-16)

Rationale: working-memory chunking — a screenful per idea. Renders longer
than `threshold` source lines pause; Enter continues, q stops (caller exits
cleanly on False), ? helps via the shared helper.
"""
from __future__ import annotations
from typing import Protocol


class _Console(Protocol):
    def input(self, prompt: str) -> str: ...
    def print(self, *args, **kwargs) -> None: ...


def _pages(text: str, threshold: int) -> list[str]:
    """Split into pages of <= threshold lines, snapping at blank lines so
    code fences and paragraphs are never torn across pages."""
    paras: list[list[str]] = [[]]
    for ln in (text or "").splitlines() or [""]:
        if not ln.strip() and paras[-1]:
            paras.append([])
        else:
            paras[-1].append(ln)
    pages, cur, n = [], [], 0
    for par in paras:
        if n + len(par) > threshold and cur:
            pages.append("\n".join(cur))
            cur, n = [], 0
        if len(par) > threshold:  # oversize paragraph: hard-split
            if cur:
                pages.append("\n".join(cur))
                cur, n = [], 0
            for i in range(0, len(par), threshold):
                pages.append("\n".join(par[i:i + threshold]))
        else:
            cur += par + [""]
            n += len(par) + 1
    if cur:
        pages.append("\n".join(cur).rstrip())
    return pages or [""]


def show(console: _Console, text: str, threshold: int = 40) -> bool:
    """Print Markdown a page at a time. Returns False if the user quit
    (caller should stop), True when fully shown."""
    from rich.markdown import Markdown
    from lib import keys as _k
    pages = _pages(text, threshold)
    console.print(Markdown(pages[0]))
    for i in range(1, len(pages)):
        cmd = _k.ask(console,
                     f"—more— ({i}/{len(pages)}) [Enter/q/?]: ",
                     "pager").lower()
        if cmd == "q":
            return False
        console.print(Markdown(pages[i]))
    return True

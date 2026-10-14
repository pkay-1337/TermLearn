"""Contextual `?` help for every interactive prompt. (SRS IF-CLI-006)

Research basis: recognition over recall (Nielsen H6) — options must be visible
or retrievable, never memorized; feature discoverability precedes learnability
(Norman; HCI discoverability literature — most users never find hidden
shortcuts); GNOME HIG mnemonic guidance (keys should abbreviate their action:
r=run, e=explain/edit, h=hint, s=skip/shuffle, n=next, f=flip).

Contract: `keys.ask(console, prompt, mode)` behaves like `console.input`
but intercepts `?`/`help` to print the mode's key list and re-prompt.
`?` and `help` are therefore reserved words — no check answer or code input
in single-line prompts may be exactly `?`/`help` (documented in GENERATE.md
constraints for pack authors; C answers are never affected).
"""
from __future__ import annotations
from typing import Protocol

HELP: dict[str, str] = {
    "quiz": ("[bold]quiz keys:[/bold] 1-N answer · "
             "type the blank (fillblank) · ? this help · q quit"),
    "parsons": ("[bold]parsons keys:[/bold] order numbers e.g. `3 1 2` · "
                "s reshuffle · h hint · ? this help · q quit"),
    "study": ("[bold]study keys:[/bold] r run example · Enter continue · "
              "n next viz step · s skip viz · y/N re-show example · "
              "1-N answer checks · ? this help · q quit"),
    "lab": ("[bold]lab keys:[/bold] e edit ($EDITOR) · r compile+run · "
            "t hidden tests · d last diff · h next hint · ? this help · q quit"),
    "srs": ("[bold]srs keys:[/bold] f flip card · e edit card · 1 forgot · 2 hard · "
            "3 good · 4 easy · ? this help · q quit"),
    "pager": "[bold]pager keys:[/bold] Enter continue · q stop · ? this help",
    "default": "[bold]keys:[/bold] ? this help · q quit",
}

RESERVED = {"?", "help"}


class _Console(Protocol):
    def input(self, prompt: str) -> str: ...
    def print(self, *args, **kwargs) -> None: ...


def ask(console: _Console, prompt: str, mode: str = "default") -> str:
    """Prompt, intercepting `?`/`help`. Returns stripped raw input."""
    while True:
        raw = console.input(prompt).strip()
        if raw.lower() in RESERVED:
            console.print(HELP.get(mode, HELP["default"]))
            continue
        return raw

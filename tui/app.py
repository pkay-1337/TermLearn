"""LearnApp: screen router + shared state. (IF-TUI-001..004)

State: `book` / `chapter` slugs selected on Home/Chapters screens.
Every screen defines its own BINDINGS (same letters as the CLI); the Footer
renders them as the persistent hint bar (IF-TUI-003). `?` pushes HelpModal.
`q` pops back (Home quits). Mouse works by default; everything stays
keyboard-operable (IF-TUI-002: mouse MAY, keyboard MUST).
"""
from __future__ import annotations

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header


class LearnApp(App):
    TITLE = "termlearn"
    SUB_TITLE = "learn technical books in the terminal"
    CSS_PATH = "style.tcss"

    BINDINGS = [
        Binding("question_mark", "help", "Help", show=True),
    ]

    def __init__(self, book: str = "", chapter: str = "") -> None:
        super().__init__()
        self.book = book
        self.chapter = chapter
        self._help_lines: list[tuple[str, str]] = []

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def on_mount(self) -> None:
        from tui.screens import ChapterMenu, ChaptersScreen, HomeScreen
        if self.book and self.chapter:
            from lib.books import discover_chapters
            known = {c["id"]: c for c in discover_chapters(self.book)}
            if known.get(self.chapter, {}).get("has_pack"):
                self.push_screen(ChapterMenu(self.book, self.chapter))
                return
        if self.book:
            self.push_screen(ChaptersScreen(self.book))
        else:
            self.push_screen(HomeScreen())

    def action_help(self) -> None:
        from tui.widgets import HelpModal
        self.push_screen(HelpModal(self._help_title(), self._help_lines))

    def _help_title(self) -> str:
        return getattr(self.screen, "HELP_TITLE", type(self.screen).__name__)

    def set_help(self, title: str, lines: list[tuple[str, str]]) -> None:
        self._help_lines = lines
        try:
            self.screen.HELP_TITLE = title  # type: ignore[attr-defined]
        except Exception:
            pass


def run(book: str = "", chapter: str = "") -> None:
    """Entry point used by `main.py tui`. Packs are only read, never written."""
    LearnApp(book=book, chapter=chapter).run()

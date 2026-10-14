"""Shared TUI widgets: help overlay + reusable question widget. (IF-TUI-003..005)"""
from __future__ import annotations

from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Static

GLOBAL_KEYS = [
    ("q", "back / quit"),
    ("?", "this help"),
]


class HelpModal(ModalScreen):
    """Key overlay opened by `?` on any screen. (IF-TUI-003)"""

    BINDINGS = [("escape", "close", "Close")]

    def __init__(self, title: str, lines: list[tuple[str, str]]) -> None:
        super().__init__()
        self._title = title
        self._lines = lines

    def action_close(self) -> None:
        self.dismiss(None)

    def compose(self) -> ComposeResult:
        keys = "\n".join(f"[bold cyan]{k:>4}[/]  [white]{desc}[/]" for k, desc in self._lines + GLOBAL_KEYS)
        with Vertical(id="help-box"):
            yield Label(f"Keys — {self._title}", id="help-title")
            yield Static(keys)
            yield Button("Close (q / Esc)", id="help-close")

    @on(Button.Pressed, "#help-close")
    def _close(self) -> None:
        self.app.pop_screen()


class QuestionWidget(Static):
    """One check: prompt + answer controls + feedback + why.

    Covers choice kinds (buttons + parent-forwarded 1-4), fillblank/order/
    micro-lab (Input). Calls `on_done(ok: bool)` exactly once per question.
    Pure presentation — scoring facts come from the pack dict; persistence is
    the parent screen's job (same lib functions as the CLI).
    """

    def __init__(self, check: dict, on_done, *, compact: bool = False) -> None:
        super().__init__()
        self.check = check
        self.on_done = on_done
        self.compact = compact
        self._done = False

    def compose(self) -> ComposeResult:
        ck = self.check
        yield Label(f"[{ck.get('kind', '?').upper()}] {ck.get('q', '')}", classes="question-prompt")
        if ck.get("code"):
            try:
                from textual.widgets import Syntax
                yield Syntax(ck["code"], ck.get("lang", "c"), theme="monokai")
            except Exception:
                yield Static(ck["code"])
        kind = ck.get("kind")
        if kind in ("predict", "why-fails", "mcq", "eipe", "choose-better"):
            for i, opt in enumerate(ck.get("choices", []), 1):
                yield Button(f"({i})  {opt}", id=f"opt-{i}", classes="question-opt-btn")
        elif kind == "order":
            for i, line in enumerate(ck.get("lines", []), 1):
                yield Static(f"  [{i}] {line}")
            yield Input(placeholder="type line order e.g. 3 1 2", id="order-in", classes="question-input")
        elif kind == "fillblank":
            yield Input(placeholder="type the missing token", id="fill-in", classes="question-input")
        elif kind == "micro-lab":
            yield Input(placeholder="expected output (r runs the code first)",
                        id="micro-in", classes="question-input")
        yield Static("", id="feedback", classes="feedback-msg")

    # -- answering API used by parent screens (buttons AND key aliases) --
    def answer_choice(self, pick: int) -> None:
        if self._done:
            return
        ans = int(self.check.get("answer", -1))
        self._finish(pick == ans, f"answer was {ans + 1}" if pick != ans else "")

    def _feedback(self, text: str) -> None:
        self.query_one("#feedback", Static).update(text)

    def _finish(self, ok: bool, extra: str = "") -> None:
        self._done = True
        why = str(self.check.get("why", ""))
        mark = "correct" if ok else f"not quite{f' — {extra}' if extra else ''}"
        fb = self.query_one("#feedback", Static)
        if ok:
            fb.remove_class("feedback-msg-error")
            fb.add_class("feedback-msg-success")
            prefix = "✔  "
        else:
            fb.remove_class("feedback-msg-success")
            fb.add_class("feedback-msg-error")
            prefix = "✖  "
        fb.update(f"{prefix}{mark}\n\nwhy: {why}")
        self.on_done(ok)

    @on(Button.Pressed)
    def _choice_pressed(self, event: Button.Pressed) -> None:
        if event.button.id and event.button.id.startswith("opt-"):
            self.answer_choice(int(event.button.id.split("-")[1]) - 1)

    @on(Input.Submitted)
    def _text_submitted(self, event: Input.Submitted) -> None:
        if self._done:
            return
        ck = self.check
        kind = ck.get("kind")
        raw = event.value.strip()
        if kind == "fillblank":
            ok = raw == str(ck.get("answer_text", "")).strip()
            self._finish(ok, f"expected: {ck.get('answer_text')}" if not ok else "")
        elif kind == "order":
            try:
                picked = [int(x) - 1 for x in raw.split()]
            except ValueError:
                picked = []
            want = list(ck.get("answer_order", []))
            ok = picked == want
            if not ok:
                dwhy = (ck.get("distractor_why", {}) or {})
                shown = ck.get("lines", [])
                named = [dwhy.get(shown[p], "") for p in picked
                         if 0 <= p < len(shown)]
                named = [n for n in named if n]
                self._finish(False, named[0] if named else "wrong order")
            else:
                self._finish(True)
        elif kind == "micro-lab":
            if raw.lower() == "r" and ck.get("code"):
                self._feedback("run it from the Lab screen, then answer here")
                return
            expect = str(ck.get("expect", ""))
            self._finish((raw == expect) if expect else True,
                         f"expected: {expect!r}" if expect and raw != expect else "")

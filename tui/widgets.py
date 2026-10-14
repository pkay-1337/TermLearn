"""Shared TUI widgets: help overlay + reusable question widget. (IF-TUI-003..005)"""
from __future__ import annotations

from textual import events, on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Static

GLOBAL_KEYS = [
    ("q", "back / quit"),
    ("?", "this help"),
]


class VimScrollMixin:
    """Provides standard Vim scrolling bindings for Textual screens/containers."""

    VIM_BINDINGS = [
        Binding("j", "vim_down", "Down (j)", show=False),
        Binding("k", "vim_up", "Up (k)", show=False),
        Binding("d", "vim_pagedown", "Half Down (d)", show=False),
        Binding("u", "vim_pageup", "Half Up (u)", show=False),
        Binding("ctrl+d", "vim_pagedown", "Half Down", show=False),
        Binding("ctrl+u", "vim_pageup", "Half Up", show=False),
        Binding("g", "vim_top", "Top (g)", show=False),
        Binding("G", "vim_bottom", "Bottom (G)", show=False),
    ]

    def get_scroll_target(self):
        from textual.containers import ScrollableContainer
        for w in self.query(ScrollableContainer):
            return w
        return None

    def action_vim_down(self) -> None:
        focused = getattr(self.app, "focused", None)
        from textual.widgets import Input, TextArea
        if isinstance(focused, (Input, TextArea)):
            return
        tgt = self.get_scroll_target()
        if tgt:
            tgt.scroll_relative(y=2, animate=False)

    def action_vim_up(self) -> None:
        focused = getattr(self.app, "focused", None)
        from textual.widgets import Input, TextArea
        if isinstance(focused, (Input, TextArea)):
            return
        tgt = self.get_scroll_target()
        if tgt:
            tgt.scroll_relative(y=-2, animate=False)

    def action_vim_pagedown(self) -> None:
        focused = getattr(self.app, "focused", None)
        from textual.widgets import Input, TextArea
        if isinstance(focused, (Input, TextArea)):
            return
        tgt = self.get_scroll_target()
        if tgt:
            step = max(4, tgt.size.height // 2)
            tgt.scroll_relative(y=step, animate=False)

    def action_vim_pageup(self) -> None:
        focused = getattr(self.app, "focused", None)
        from textual.widgets import Input, TextArea
        if isinstance(focused, (Input, TextArea)):
            return
        tgt = self.get_scroll_target()
        if tgt:
            step = max(4, tgt.size.height // 2)
            tgt.scroll_relative(y=-step, animate=False)

    def action_vim_top(self) -> None:
        focused = getattr(self.app, "focused", None)
        from textual.widgets import Input, TextArea
        if isinstance(focused, (Input, TextArea)):
            return
        tgt = self.get_scroll_target()
        if tgt:
            tgt.scroll_home(animate=False)

    def action_vim_bottom(self) -> None:
        focused = getattr(self.app, "focused", None)
        from textual.widgets import Input, TextArea
        if isinstance(focused, (Input, TextArea)):
            return
        tgt = self.get_scroll_target()
        if tgt:
            tgt.scroll_end(animate=False)


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


class ChoiceCard(Static):
    """A focusable, multi-line choice card that wraps cleanly across terminal widths."""

    can_focus = True

    class Selected(Message):
        """Posted when card is selected by click, Enter, or Space."""

        def __init__(self, index: int) -> None:
            super().__init__()
            self.index = index

    def __init__(self, index: int, text: str, id: str | None = None) -> None:
        super().__init__(id=id)
        self.index = index
        self.raw_text = text

    def compose(self) -> ComposeResult:
        yield Label(f"({self.index})  {self.raw_text}", classes="choice-card-text")

    def on_click(self) -> None:
        self.post_message(self.Selected(self.index - 1))

    def on_key(self, event: events.Key) -> None:
        if event.key in ("enter", "space"):
            event.stop()
            self.post_message(self.Selected(self.index - 1))
        elif event.key in ("j", "down"):
            event.stop()
            self.screen.focus_next()
        elif event.key in ("k", "up"):
            event.stop()
            self.screen.focus_previous()


class QuestionWidget(Static):
    """One check: prompt + answer controls + feedback + why.

    Covers choice kinds (ChoiceCards + parent-forwarded 1-4), fillblank/order/
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
                yield ChoiceCard(i, opt, id=f"opt-{i}")
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

    # -- answering API used by parent screens (buttons, cards AND key aliases) --
    def answer_choice(self, pick: int) -> None:
        if self._done:
            return
        ans = int(self.check.get("answer", -1))
        # Highlight selected card
        try:
            card = self.query_one(f"#opt-{pick + 1}", ChoiceCard)
            card.add_class("choice-card-selected")
        except Exception:
            pass
        self._finish(pick == ans, f"answer was {ans + 1}" if pick != ans else "")

    def _feedback(self, text: str) -> None:
        self.query_one("#feedback", Static).update(text)

    def _scroll_to_feedback(self) -> None:
        try:
            self.query_one("#feedback", Static).scroll_visible(animate=True, top=False)
        except Exception:
            pass

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
        self.call_after_refresh(self._scroll_to_feedback)
        self.on_done(ok)

    @on(ChoiceCard.Selected)
    def _card_selected(self, event: ChoiceCard.Selected) -> None:
        self.answer_choice(event.index)

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


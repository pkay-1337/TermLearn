"""Shared TUI widgets: help overlay + reusable question widget. (IF-TUI-003..005)"""
from __future__ import annotations

from textual import events, on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, ScrollableContainer, Vertical
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


class ConfirmDeleteModal(ModalScreen[bool]):
    """Confirmation modal to wipe chapter analytics. (FR-STAT-003)"""

    BINDINGS = [
        Binding("y", "confirm", "Yes", show=False),
        Binding("n", "cancel", "No", show=False),
        Binding("escape", "cancel", "Cancel", show=False),
        Binding("q", "cancel", "Cancel", show=False),
    ]

    def __init__(self, book: str, chapter: str) -> None:
        super().__init__()
        self.book = book
        self.chapter = chapter

    def compose(self) -> ComposeResult:
        from textual.containers import Horizontal
        with Vertical(id="confirm-delete-box"):
            yield Label("⚠️  Reset Chapter Analytics?", id="confirm-delete-title")
            yield Static(
                f"Are you sure you want to delete all analytics for [bold cyan]{self.book} / {self.chapter}[/]?\n\n"
                f"[dim]This will wipe recorded answers, quiz scores, test runs, and block completion for this chapter.[/dim]",
                classes="confirm-delete-body",
            )
            with Horizontal(classes="confirm-delete-actions"):
                yield Button("Cancel (n / Esc)", id="btn-cancel-delete")
                yield Button("Delete (y / Enter)", id="btn-confirm-delete")

    @on(Button.Pressed, "#btn-confirm-delete")
    def _on_confirm(self) -> None:
        self.dismiss(True)

    @on(Button.Pressed, "#btn-cancel-delete")
    def _on_cancel(self) -> None:
        self.dismiss(False)

    def action_confirm(self) -> None:
        self.dismiss(True)

    def action_cancel(self) -> None:
        self.dismiss(False)


class SubgoalCodeView(Static):
    """Renders a code block partitioned into labeled functional subgoals (SPEC-PED-001)."""

    def __init__(self, code: str, lang: str = "c", subgoals: list[dict] | None = None) -> None:
        super().__init__()
        self.code = code
        self.lang = lang
        self.subgoals = subgoals or []

    def compose(self) -> ComposeResult:
        lines = self.code.splitlines()
        with Vertical(classes="subgoal-container"):
            for sg in self.subgoals:
                label = sg.get("label", "Subgoal")
                sg_lines = sg.get("lines", [])
                sub_code = "\n".join(lines[i - 1] for i in sg_lines if 1 <= i <= len(lines))
                with Vertical(classes="subgoal-frame"):
                    yield Label(f"🎯  Subgoal: {label}", classes="subgoal-header")
                    try:
                        from textual.widgets import Syntax
                        yield Syntax(sub_code, self.lang, theme="monokai", classes="subgoal-code")
                    except Exception:
                        yield Static(sub_code, classes="subgoal-code")


class ToolchainInspectModal(ModalScreen):
    """Live interactive toolchain inspector modal (nm, objdump, readelf, AST). (SPEC-RUNNER-002)"""

    BINDINGS = [
        Binding("1", "mode_symbols", "Symbols (1)", show=False),
        Binding("2", "mode_disasm", "Disassembly (2)", show=False),
        Binding("3", "mode_sections", "Sections (3)", show=False),
        Binding("4", "mode_ast", "AST (4)", show=False),
        Binding("j", "scroll_down", "Down", show=False),
        Binding("k", "scroll_up", "Up", show=False),
        Binding("escape", "close", "Close"),
        Binding("q", "close", "Close"),
    ]

    def __init__(self, book: str | None, code: str, lang: str = "c") -> None:
        super().__init__()
        self.book = book
        self.code = code
        self.lang = lang
        self.current_mode = "symbols"

    def compose(self) -> ComposeResult:
        with Vertical(id="inspect-modal-box"):
            yield Label(f"🔍  Toolchain Inspector — Language: [bold cyan]{self.lang}[/]", id="inspect-modal-title")
            with Horizontal(id="inspect-tabs-bar"):
                yield Button("1. Symbols (nm)", id="tab-symbols", classes="inspect-tab-btn")
                yield Button("2. Disassembly (objdump)", id="tab-disasm", classes="inspect-tab-btn")
                yield Button("3. Sections (readelf)", id="tab-sections", classes="inspect-tab-btn")
                yield Button("4. AST / Syntax", id="tab-ast", classes="inspect-tab-btn")
            with ScrollableContainer(id="inspect-output-container"):
                yield Static("Loading inspector output...", id="inspect-content")
            yield Button("Close (q / Esc)", id="inspect-close")

    def on_mount(self) -> None:
        self._load_mode("symbols")

    def _load_mode(self, mode: str) -> None:
        self.current_mode = mode
        from lib.lab import inspect_code
        res = inspect_code(self.book, self.code, lang=self.lang, mode=mode)
        out = self.query_one("#inspect-content", Static)
        if res.get("ok"):
            content = res.get("content", "") or "(No output generated)"
            out.update(content)
        else:
            diag = res.get("diagnostics", "Inspector failed")
            out.update(f"[bold red]Inspection Error:[/] {diag}")

    @on(Button.Pressed, "#tab-symbols")
    def _tab_symbols(self) -> None:
        self._load_mode("symbols")

    @on(Button.Pressed, "#tab-disasm")
    def _tab_disasm(self) -> None:
        self._load_mode("disasm")

    @on(Button.Pressed, "#tab-sections")
    def _tab_sections(self) -> None:
        self._load_mode("sections")

    @on(Button.Pressed, "#tab-ast")
    def _tab_ast(self) -> None:
        self._load_mode("ast")

    @on(Button.Pressed, "#inspect-close")
    def _close(self) -> None:
        self.app.pop_screen()

    def action_close(self) -> None:
        self.app.pop_screen()

    def action_mode_symbols(self) -> None:
        self._load_mode("symbols")

    def action_mode_disasm(self) -> None:
        self._load_mode("disasm")

    def action_mode_sections(self) -> None:
        self._load_mode("sections")

    def action_mode_ast(self) -> None:
        self._load_mode("ast")

    def action_scroll_down(self) -> None:
        try:
            self.query_one("#inspect-output-container").scroll_relative(y=3, animate=False)
        except Exception:
            pass

    def action_scroll_up(self) -> None:
        try:
            self.query_one("#inspect-output-container").scroll_relative(y=-3, animate=False)
        except Exception:
            pass


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
        yield Static(f"({self.index})  {self.raw_text}", classes="choice-card-text")

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
        yield Static(f"[{ck.get('kind', '?').upper()}] {ck.get('q', '')}", classes="question-prompt")
        if ck.get("code"):
            try:
                from textual.widgets import Syntax
                yield Syntax(ck["code"], ck.get("lang", "c"), theme="monokai")
            except Exception:
                yield Static(ck["code"])
        kind = ck.get("kind")
        if kind in ("predict", "why-fails", "mcq", "eipe", "choose-better", "spot-bug"):
            if kind == "spot-bug" and ck.get("diagnostic_log"):
                yield Static(f"🚨  Diagnostic Log:\n{ck['diagnostic_log']}", classes="bug-diag-box")
            for i, opt in enumerate(ck.get("choices", []), 1):
                yield ChoiceCard(i, opt, id=f"opt-{i}")
        elif kind == "order":
            if ck.get("faded") is True:
                yield Static("Faded Parsons: Order lines and fill in missing tokens:", classes="faded-instruction")
            for i, line in enumerate(ck.get("lines", []), 1):
                yield Static(f"  [{i}] {line}")
            yield Input(placeholder="type line order e.g. 3 1 2", id="order-in", classes="question-input")
            if ck.get("faded") is True:
                for bi, blk in enumerate(ck.get("blanks", [])):
                    l_idx = blk.get("line_idx", 0)
                    yield Input(placeholder=f"Line {l_idx + 1} missing token", id=f"faded-blank-{bi}", classes="question-input")
                yield Button("Submit Answer (Enter)", id="btn-submit-faded")
        elif kind == "fillblank":
            yield Input(placeholder="type the missing token", id="fill-in", classes="question-input")
        elif kind == "trace":
            tr = ck.get("trace", {})
            self._trace_step = 1
            self._max_trace_step = max((r.get("step", 1) for r in tr.get("rows", [])), default=1)
            yield Static(self._render_trace_table(), id="trace-table-view", classes="trace-table-box")
            with Horizontal(classes="trace-nav-bar"):
                yield Button("◀ Prev Step (p)", id="btn-trace-prev")
                yield Button("Next Step (n) ▶", id="btn-trace-next")
            if ck.get("choices"):
                for i, opt in enumerate(ck.get("choices", []), 1):
                    yield ChoiceCard(i, opt, id=f"opt-{i}")
            else:
                yield Input(placeholder="enter value for target cell [ ??? ]", id="trace-in", classes="question-input")
        elif kind == "micro-lab":
            yield Input(placeholder="expected output (r runs the code first)",
                        id="micro-in", classes="question-input")
        yield Static("", id="feedback", classes="feedback-msg")

    def _render_trace_table(self) -> str:
        ck = self.check
        tr = ck.get("trace", {})
        headers = tr.get("headers", ["Step", "Variable", "Address", "Value"])
        rows = tr.get("rows", [])
        tgt = ck.get("target", {})
        lines = []
        lines.append(" | ".join(headers))
        lines.append("-|-".join(["---" * max(3, len(h)) for h in headers]))
        for r_idx, r in enumerate(rows):
            if r.get("step", 1) <= getattr(self, "_trace_step", 1):
                cells = list(r.get("cells", []))
                if r_idx == tgt.get("row") and 0 <= tgt.get("col", -1) < len(cells):
                    cells[tgt["col"]] = "[ ??? ]"
                lines.append(" | ".join(str(c) for c in cells))
        return "\n".join(lines)

    @on(Button.Pressed, "#btn-trace-prev")
    def _trace_prev(self) -> None:
        if getattr(self, "_trace_step", 1) > 1:
            self._trace_step -= 1
            self.query_one("#trace-table-view", Static).update(self._render_trace_table())

    @on(Button.Pressed, "#btn-trace-next")
    def _trace_next(self) -> None:
        if getattr(self, "_trace_step", 1) < getattr(self, "_max_trace_step", 1):
            self._trace_step += 1
            self.query_one("#trace-table-view", Static).update(self._render_trace_table())

    def _submit_faded_order(self) -> None:
        if self._done:
            return
        ck = self.check
        order_val = ""
        try:
            order_val = self.query_one("#order-in", Input).value.strip()
            picked = [int(x) - 1 for x in order_val.split()]
        except Exception:
            picked = []
        want = list(ck.get("answer_order", []))
        if picked != want:
            self._finish(False, "wrong line ordering")
            return
        blanks = ck.get("blanks", [])
        for bi, blk in enumerate(blanks):
            try:
                user_token = self.query_one(f"#faded-blank-{bi}", Input).value.strip()
            except Exception:
                user_token = ""
            exp_text = str(blk.get("answer_text", "")).strip()
            accepted = [str(a).strip() for a in blk.get("accepted", [])]
            if user_token != exp_text and user_token not in accepted:
                self._finish(False, f"blank {bi + 1} incorrect: expected {exp_text!r}")
                return
        self._finish(True)

    @on(Button.Pressed, "#btn-submit-faded")
    def _faded_btn(self) -> None:
        self._submit_faded_order()

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
        elif kind == "trace":
            exp_text = str(ck.get("answer_text", "")).strip()
            ok = raw.lower() == exp_text.lower()
            self._finish(ok, f"expected: {exp_text}" if not ok else "")
        elif kind == "order":
            if ck.get("faded") is True:
                self._submit_faded_order()
                return
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


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


class ConfirmResetModal(ModalScreen[bool]):
    """Confirmation modal to reset lab workspace files."""

    BINDINGS = [
        Binding("y", "confirm", "Yes", show=False),
        Binding("n", "cancel", "No", show=False),
        Binding("escape", "cancel", "Cancel", show=False),
        Binding("q", "cancel", "Cancel", show=False),
    ]

    def __init__(self, lab_title: str) -> None:
        super().__init__()
        self.lab_title = lab_title

    def compose(self) -> ComposeResult:
        from textual.containers import Horizontal
        with Vertical(id="confirm-delete-box"):
            yield Label("⚠️  Reset Lab Workspace?", id="confirm-delete-title")
            yield Static(
                f"Reset workspace files for [bold cyan]{self.lab_title}[/] to initial starter state?\n\n"
                f"[dim yellow]Any edits made in this lab directory will be overwritten.[/dim yellow]",
                classes="confirm-delete-body",
            )
            with Horizontal(classes="confirm-delete-actions"):
                yield Button("Cancel (n / Esc)", id="btn-cancel-delete")
                yield Button("Reset (y)", id="btn-confirm-delete")

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

    def _get_comment_prefix(self) -> str:
        lang = (self.lang or "").lower()
        if lang in ("python", "py", "bash", "sh", "yaml", "yml", "ruby", "rb", "perl", "r"):
            return "#"
        elif lang in ("sql", "lua", "haskell", "hs", "ada"):
            return "--"
        elif lang in ("lisp", "clojure", "scheme"):
            return ";;"
        return "//"

    def _build_annotated_code(self) -> str:
        lines = self.code.splitlines()
        prefix = self._get_comment_prefix()

        sg_map: dict[int, list[str]] = {}
        for sg in self.subgoals:
            label = sg.get("label", "Subgoal")
            sg_lines = sg.get("lines", [])
            if sg_lines:
                start_line = min(sg_lines)
                if 1 <= start_line <= len(lines):
                    sg_map.setdefault(start_line, []).append(label)

        annotated_lines = []
        for i, line in enumerate(lines, 1):
            if i in sg_map:
                indent = line[: len(line) - len(line.lstrip())]
                for lbl in sg_map[i]:
                    annotated_lines.append(f"{indent}{prefix} ── Subgoal: {lbl} ──")
            annotated_lines.append(line)

        return "\n".join(annotated_lines)

    def compose(self) -> ComposeResult:
        annotated_code = self._build_annotated_code()
        if len(self.subgoals) == 1:
            title = f"🎯 Subgoal: {self.subgoals[0].get('label', '')}"
        elif len(self.subgoals) > 1:
            labels_str = " · ".join(sg.get("label", "") for sg in self.subgoals)
            title = f"🎯 Subgoals: {labels_str}"
        else:
            title = "🎯 Code Example"

        with Vertical(classes="subgoal-container"):
            yield Label(title, classes="subgoal-summary-label")
            try:
                from textual.widgets import Syntax
                yield Syntax(annotated_code, self.lang, theme="monokai", classes="study-example-box")
            except Exception:
                yield Static(annotated_code, classes="study-example-box")


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
        """Posted when card is selected by click, Enter, Space, or digit keys."""

        def __init__(self, index: int) -> None:
            super().__init__()
            self.index = index

    def __init__(self, index: int, text: str, id: str | None = None) -> None:
        super().__init__(id=id)
        self.index = index
        self.raw_text = text

    def compose(self) -> ComposeResult:
        yield Static(f"[{self.index}]  {self.raw_text}", classes="choice-card-text")

    def on_click(self, event: events.Click | None = None) -> None:
        self.post_message(self.Selected(self.index - 1))

    def on_key(self, event: events.Key) -> None:
        if event.key in ("enter", "space"):
            event.stop()
            self.post_message(self.Selected(self.index - 1))
        elif event.key in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
            event.stop()
            self.post_message(self.Selected(int(event.key) - 1))
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

    def __init__(self, check: dict, on_done, *, compact: bool = False,
                 shuffle: bool = False, seed: int | None = None) -> None:
        super().__init__()
        self.check = check
        self.on_done = on_done
        self.compact = compact
        self.shuffle = shuffle
        self._done = False

        chs = list(check.get("choices", []))
        raw_ans = check.get("answer")
        if chs and raw_ans is not None and shuffle:
            import random
            rng = random.Random(seed) if seed is not None else random.Random()
            order = list(range(len(chs)))
            rng.shuffle(order)
            self._display_choices = [chs[i] for i in order]
            try:
                self._ans_idx = order.index(int(raw_ans))
            except ValueError:
                self._ans_idx = -1
        else:
            self._display_choices = chs
            self._ans_idx = int(raw_ans) if raw_ans is not None else -1

        tr = check.get("trace", {})
        self._trace_step = 1
        self._norm_trace_rows()

    def _norm_trace_rows(self) -> None:
        """Trace rows come in two shapes: legacy dicts ({step, cells}) and
        plain header-aligned cell lists; normalize to (step, cells) pairs."""
        tr = self.check.get("trace", {})
        norm: list[tuple[int, list[str]]] = []
        for i, r in enumerate(tr.get("rows", [])):
            if isinstance(r, dict):
                norm.append((int(r.get("step", i + 1)) or i + 1,
                             [str(c) for c in r.get("cells", [])]))
            elif isinstance(r, list):
                norm.append((i + 1, [str(c) for c in r]))
            else:
                norm.append((i + 1, [str(r)]))
        self._trace_rows = norm
        self._max_trace_step = max((s for s, _ in norm), default=1)

    def compose(self) -> ComposeResult:
        ck = self.check
        level_tag = f" · {ck['level'].upper()}" if ck.get("level") else ""
        yield Static(f"[{ck.get('kind', '?').upper()}{level_tag}] {ck.get('q', '')}", classes="question-prompt")
        if ck.get("code"):
            try:
                from textual.widgets import Syntax
                yield Syntax(ck["code"], ck.get("lang", "c"), theme="monokai")
            except Exception:
                yield Static(ck["code"])
        kind = ck.get("kind")
        if kind in ("predict", "why-fails", "mcq", "eipe", "choose-better", "spot-bug") or (kind not in ("order", "fillblank", "trace", "micro-lab") and self._display_choices):
            if kind == "spot-bug" and ck.get("diagnostic_log"):
                yield Static(f"🚨  Diagnostic Log:\n{ck['diagnostic_log']}", classes="bug-diag-box")
            for i, opt in enumerate(self._display_choices, 1):
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
            self._trace_step = 1
            yield Static(self._render_trace_table(), id="trace-table-view", classes="trace-table-box")
            with Horizontal(classes="trace-nav-bar"):
                yield Button("◀ Prev Step (p)", id="btn-trace-prev")
                yield Button("Next Step (n) ▶", id="btn-trace-next")
            if self._display_choices:
                for i, opt in enumerate(self._display_choices, 1):
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
        tgt = ck.get("target", {})
        lines = []
        lines.append(" | ".join(headers))
        lines.append("-|-".join(["---" * max(3, len(h)) for h in headers]))
        for r_idx, (step, cells) in enumerate(getattr(self, "_trace_rows", [])):
            if step <= getattr(self, "_trace_step", 1):
                cells = list(cells)
                if r_idx == tgt.get("row") and 0 <= tgt.get("col", -1) < len(cells):
                    cells[tgt["col"]] = "[ ??? ]"
                lines.append(" | ".join(str(c) for c in cells))
        return "\n".join(lines)

    def trace_step_prev(self) -> bool:
        if self.check.get("kind") == "trace" and getattr(self, "_trace_step", 1) > 1:
            self._trace_step -= 1
            self.query_one("#trace-table-view", Static).update(self._render_trace_table())
            return True
        return False

    def trace_step_next(self) -> bool:
        if self.check.get("kind") == "trace" and getattr(self, "_trace_step", 1) < getattr(self, "_max_trace_step", 1):
            self._trace_step += 1
            self.query_one("#trace-table-view", Static).update(self._render_trace_table())
            return True
        return False

    @on(Button.Pressed, "#btn-trace-prev")
    def _trace_prev(self, event: Button.Pressed | None = None) -> None:
        if event is not None:
            event.stop()
        self.trace_step_prev()

    @on(Button.Pressed, "#btn-trace-next")
    def _trace_next(self, event: Button.Pressed | None = None) -> None:
        if event is not None:
            event.stop()
        self.trace_step_next()

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
        if not (0 <= pick < len(self._display_choices)):
            return
        ans = self._ans_idx
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


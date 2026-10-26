"""Interactive TUI screens: Study, Quiz, Cards, Lab. (IF-TUI-001..005)

Same packs, same lib data/persistence functions as the CLI — only the
presentation is Textual-native (the CLI run-loops block on stdin and cannot
be wrapped; scoring, SM-2, validation and gcc paths are shared verbatim).
Packs are read, never written.
"""
from __future__ import annotations

from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, ScrollableContainer, Vertical
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, DataTable, Input, Label, Markdown, Static

from tui.widgets import QuestionWidget, VimScrollMixin

CHOICE_KINDS = ("predict", "why-fails", "mcq", "eipe", "choose-better", "spot-bug")


class _Base(Screen):
    HELP_TITLE = "screen"
    HELP_LINES: list[tuple[str, str]] = []

    def on_mount(self) -> None:
        self.app.set_help(self.HELP_TITLE, self.HELP_LINES)

    def action_help(self) -> None:
        self.app.action_help()

    def on_unmount(self) -> None:
        con = getattr(self, "_con", None)
        if con is not None:
            try:
                con.close()
            except Exception:
                pass
            self._con = None


class StudyScreen(VimScrollMixin, _Base):
    HELP_TITLE = "study"
    HELP_LINES = [("1-4", "answer check"), ("n", "next page / step"),
                  ("p", "previous page / step"), ("s", "skip check"),
                  ("r", "run example"), ("i", "inspect example (toolchain)"),
                  ("j/k", "scroll"), ("d/u", "half page"), ("q/h", "back")]
    BINDINGS = ([Binding(str(i), f"ans{i}", "", show=False) for i in range(1, 10)] +
                [Binding("n", "next", "Next"),
                 Binding("p", "prev", "Previous"),
                 Binding("s", "skip_check", "Skip", show=False),
                 Binding("r", "run_ex", "Run"),
                 Binding("i", "inspect_example", "Inspect"),
                 Binding("q", "back", "Back"),
                 Binding("h", "back", "Back", show=False),
                 Binding("question_mark", "help", "Help")] +
                VimScrollMixin.VIM_BINDINGS)

    def __init__(self, book: str, chapter: str, start_block: int = 0) -> None:
        super().__init__()
        self.book = book
        self.chapter = chapter
        self.bi = max(0, start_block)
        self.stage = "explain"  # explain | diagram | viz | check-i | done
        self.vi = 0
        self.di = 0
        self._check_answered = False

    def _screen_title_text(self) -> str:
        w = self.size.width or 80
        ch_title = getattr(self, "data", {}).get("meta", {}).get("title", self.chapter)
        if w < 55:
            return f"📖 STUDY — {self.book}/{self.chapter}"
        elif w < 80:
            return f"📖  STUDY — {self.book} / {self.chapter}"
        else:
            return f"📖  STUDY — {self.book} / {self.chapter}: {ch_title}"

    def compose(self) -> ComposeResult:
        from lib.pack import load_chapter
        from lib.srs import init_db
        self.data = load_chapter(self.book, self.chapter)
        self.blocks = self.data.get("blocks", [])
        if self.blocks:
            self.bi = max(0, min(self.bi, len(self.blocks) - 1))
        self._con = init_db()
        with ScrollableContainer(classes="study-container"):
            yield Label(self._screen_title_text(), id="study-screen-title", classes="screen-title")
            yield Vertical(id="body")

    def on_mount(self) -> None:
        super().on_mount()
        # Defer first paint past the mount transition: pushing during a
        # modal dismiss can otherwise fire on_mount before compose children
        # attach (NoMatches on #body). Refresh-then-render is always safe.
        self.call_after_refresh(self._show_body)

    def on_resize(self) -> None:
        try:
            self.query_one("#study-screen-title", Label).update(self._screen_title_text())
        except Exception:
            pass

    def _block(self):
        return self.blocks[self.bi]

    def _diagram_arts(self):
        # SPEC-EXPL-003 F2 (FR-DIAG-003): renderer errors are fatal-invalid at
        # pack time, so render() can only fail on malformed runtime data —
        # degrade to no diagram rather than crash the screen.
        try:
            from lib.diagram import render as _diagram_render
            return _diagram_render(self._block().get("diagram") or {})
        except Exception:
            return []

    def _show_body(self) -> None:
        try:
            self.query_one(".study-container", ScrollableContainer).scroll_to(y=0, animate=False)
        except Exception:
            pass
        body = self.query_one("#body", Vertical)
        body.remove_children()
        b = self._block()
        w = self.size.width or 80
        b_title = b.get("title", b.get("id"))
        if w < 55:
            hdr = f"Block {self.bi + 1}/{len(self.blocks)}: {b_title}"
        else:
            hdr = f"📖  STUDY: {b_title} (Block {self.bi + 1} of {len(self.blocks)})"
        body.mount(Label(hdr, classes="study-header-bar"))
        if self.stage == "explain":
            body.mount(Markdown(str(b.get("explain_md", "")), classes="study-block-card"))
            ex = b.get("example") or {}
            if ex.get("code"):
                if ex.get("subgoals"):
                    from tui.widgets import SubgoalCodeView
                    body.mount(SubgoalCodeView(ex["code"], ex.get("lang", "c"), ex["subgoals"]))
                else:
                    try:
                        from textual.widgets import Syntax
                        body.mount(Syntax(ex["code"], ex.get("lang", "c"), theme="monokai", classes="study-example-box"))
                    except Exception:
                        body.mount(Static(ex["code"], classes="study-example-box"))
                # SPEC-EXPL-003 F1 (FR-EXPL-003): authored explanation right
                # after the code
                emd = ex.get("explain_md")
                if isinstance(emd, str) and emd.strip():
                    body.mount(Markdown(emd, classes="study-block-card"))
            if (b.get("diagram") or {}).get("kind"):
                body.mount(Static("👉 Press [bold cyan]n[/] to step through the flow diagram · [bold cyan]i[/] inspect toolchain", classes="study-nav-box"))
            elif (b.get("viz") or {}).get("steps"):
                body.mount(Static("👉 Press [bold cyan]n[/] to step through memory visualization · [bold cyan]i[/] inspect toolchain", classes="study-nav-box"))
            elif (b.get("checks") or []):
                body.mount(Static("👉 Press [bold cyan]n[/] to answer the checks · [bold cyan]i[/] inspect toolchain", classes="study-nav-box"))
            else:
                body.mount(Static("👉 Press [bold cyan]n[/] to proceed to next block · [bold cyan]i[/] inspect toolchain", classes="study-nav-box"))
        elif self.stage == "diagram":
            # SPEC-EXPL-003 F2 (FR-DIAG-004): stepped reveal, same keys as viz
            darts = self._diagram_arts() or []
            body.mount(Static("\n\n".join(darts[:self.di + 1]), classes="study-viz-box"))
            dots = "● " * (self.di + 1) + "○ " * max(0, len(darts) - self.di - 1)
            body.mount(Static(f"Diagram step {self.di + 1} of {len(darts)}  ({dots.strip()})  —  Press [bold cyan]n[/] to advance · [bold cyan]s[/] skip", classes="study-nav-box"))
        elif self.stage == "viz":
            steps = (b.get("viz") or {}).get("steps", [])
            body.mount(Static("\n".join(steps[:self.vi + 1]), classes="study-viz-box"))
            dots = "● " * (self.vi + 1) + "○ " * max(0, len(steps) - self.vi - 1)
            body.mount(Static(f"Step {self.vi + 1} of {len(steps)}  ({dots.strip()})  —  Press [bold cyan]n[/] to advance", classes="study-nav-box"))
        elif self.stage.startswith("check"):
            self._check_answered = False
            i = int(self.stage.split("-")[1])
            ck = (b.get("checks") or [])[i]
            body.mount(QuestionWidget(ck, self._checked))
        elif self.stage == "done":
            body.mount(Static("🎉  Block complete! Press [bold cyan]n[/]: next block · [bold cyan]p[/]: previous · [bold cyan]q[/]: back.", classes="feedback-msg-success"))

    def _checked(self, ok: bool) -> None:
        from lib.srs import log_answer
        self._check_answered = True
        b = self._block()
        i = int(self.stage.split("-")[1])
        ck = (b.get("checks") or [])[i]
        log_answer(self._con, self.book, self.chapter, b.get("id", "?"), i,
                   ok, concept=str(ck.get("concept", "")))
        body = self.query_one("#body", Vertical)
        body.mount(Button("Next Question (n)", id="next-btn"))
        body.query_one("#next-btn", Button).focus()
        self.call_after_refresh(self._scroll_to_next)

    def _scroll_to_next(self) -> None:
        try:
            self.query_one("#next-btn").scroll_visible(animate=True, top=False)
        except Exception:
            pass

    @on(Button.Pressed, "#next-btn")
    def _next_btn(self) -> None:
        self.action_next()

    def _mark_current_block_done(self) -> None:
        from lib.progress import mark_block_completed
        try:
            b = self._block()
            mark_block_completed(self.book, self.chapter, b.get("id", "?"))
        except Exception:
            pass

    def action_next(self) -> None:
        b = self._block()
        checks = b.get("checks", []) or []
        steps = (b.get("viz") or {}).get("steps", []) or []
        darts = self._diagram_arts() or []
        if self.stage == "explain":
            if darts:
                self.stage, self.di = "diagram", 0
            elif steps:
                self.stage, self.vi = "viz", 0
            elif checks:
                self.stage = "check-0"
            else:
                self._mark_current_block_done()
                self._advance_block()
        elif self.stage == "diagram":
            self.di += 1
            if self.di >= len(darts):
                if steps:
                    self.stage, self.vi = "viz", 0
                elif checks:
                    self.stage = "check-0"
                else:
                    self.stage = "done"
                    self._mark_current_block_done()
        elif self.stage == "viz":
            self.vi += 1
            if self.vi >= len(steps):
                if checks:
                    self.stage = "check-0"
                else:
                    self.stage = "done"
                    self._mark_current_block_done()
        elif self.stage.startswith("check"):
            qw = self.query(QuestionWidget).first() if self.query(QuestionWidget) else None
            if qw is not None and qw.check.get("kind") == "trace" and not getattr(self, "_check_answered", False):
                if qw.trace_step_next():
                    return
            if not getattr(self, "_check_answered", False):
                self.app.notify("Please answer the question to proceed (or press s to skip).")
                return
            i = int(self.stage.split("-")[1]) + 1
            if i < len(checks):
                self.stage = f"check-{i}"
            else:
                self.stage = "done"
                self._mark_current_block_done()
        elif self.stage == "done":
            self._advance_block()
        self._show_body()

    def action_skip_check(self) -> None:
        if self.stage == "diagram":
            # SPEC-EXPL-003 F2: s skips the remaining diagram steps
            b = self._block()
            steps = (b.get("viz") or {}).get("steps", []) or []
            if steps:
                self.stage, self.vi = "viz", 0
            elif b.get("checks"):
                self.stage = "check-0"
            else:
                self.stage = "done"
                self._mark_current_block_done()
            self._show_body()
            return
        if self.stage.startswith("check"):
            self._check_answered = True
            b = self._block()
            checks = b.get("checks", []) or []
            i = int(self.stage.split("-")[1]) + 1
            if i < len(checks):
                self.stage = f"check-{i}"
            else:
                self.stage = "done"
                self._mark_current_block_done()
            self._show_body()

    def _advance_block(self) -> None:
        self._mark_current_block_done()
        if self.bi + 1 < len(self.blocks):
            self.bi += 1
            self.stage = "explain"
            self.vi = 0
            self.di = 0
        else:
            self.app.pop_screen()
            self.app.notify("Chapter pass complete — try quiz, lab, then test.")

    def action_prev(self) -> None:
        b = self._block()
        checks = b.get("checks", []) or []
        steps = (b.get("viz") or {}).get("steps", []) or []
        darts = self._diagram_arts() or []
        if self.stage == "done":
            if checks:
                self.stage = f"check-{len(checks) - 1}"
            elif steps:
                self.stage = "viz"
                self.vi = max(0, len(steps) - 1)
            elif darts:
                self.stage = "diagram"
                self.di = max(0, len(darts) - 1)
            else:
                self.stage = "explain"
        elif self.stage.startswith("check"):
            qw = self.query(QuestionWidget).first() if self.query(QuestionWidget) else None
            if qw is not None and qw.check.get("kind") == "trace" and getattr(qw, "_trace_step", 1) > 1:
                if qw.trace_step_prev():
                    return
            i = int(self.stage.split("-")[1])
            if i > 0:
                self.stage = f"check-{i - 1}"
            else:
                if steps:
                    self.stage = "viz"
                    self.vi = max(0, len(steps) - 1)
                elif darts:
                    self.stage = "diagram"
                    self.di = max(0, len(darts) - 1)
                else:
                    self.stage = "explain"
        elif self.stage == "viz":
            if self.vi > 0:
                self.vi -= 1
            elif darts:
                self.stage = "diagram"
                self.di = max(0, len(darts) - 1)
            else:
                self.stage = "explain"
        elif self.stage == "diagram":
            if self.di > 0:
                self.di -= 1
            else:
                self.stage = "explain"
        elif self.stage == "explain":
            if self.bi > 0:
                self.bi -= 1
                self.stage = "explain"
                self.vi = 0
            else:
                self.app.notify("Already at first block.")
                return
        self._show_body()

    def action_run_ex(self) -> None:
        if self.stage != "explain":
            return
        ex = (self._block().get("example") or {})
        if not ex.get("code"):
            return
        from lib.lab import run_code
        r = run_code(ex["code"], ex.get("lang", "c"), timeout=2, book=self.book)
        if r.get("unsupported"):
            text = f"no local runner for '{r.get('lang')}' — use the book toolchain"
        elif not r["compiled"]:
            text = f"compile error:\n{r['stderr'][:1500]}"
        elif r.get("timed_out"):
            text = "timeout"
        else:
            text = f"output:\n{r['output'][:2000]}"
        self.query_one("#body", Vertical).mount(Static(f"[bold cyan]Console Output:[/] {text}", classes="study-example-box"))

    def action_inspect_example(self) -> None:
        ex = (self._block().get("example") or {})
        code = ex.get("code", "")
        if not code:
            self.app.notify("No code example in this block to inspect.")
            return
        from tui.widgets import ToolchainInspectModal
        self.app.push_screen(ToolchainInspectModal(self.book, code, lang=ex.get("lang", "c")))

    def _answer_digit(self, n: int) -> None:
        if not self.stage.startswith("check"):
            return
        if getattr(self, "_check_answered", False):
            return
        for w in self.query(QuestionWidget):
            w.answer_choice(n - 1)

    def action_ans1(self) -> None: self._answer_digit(1)
    def action_ans2(self) -> None: self._answer_digit(2)
    def action_ans3(self) -> None: self._answer_digit(3)
    def action_ans4(self) -> None: self._answer_digit(4)
    def action_ans5(self) -> None: self._answer_digit(5)
    def action_ans6(self) -> None: self._answer_digit(6)
    def action_ans7(self) -> None: self._answer_digit(7)
    def action_ans8(self) -> None: self._answer_digit(8)
    def action_ans9(self) -> None: self._answer_digit(9)

    def action_back(self) -> None:
        self.app.pop_screen()


class QuizScreen(VimScrollMixin, _Base):
    HELP_TITLE = "quiz"
    HELP_LINES = [("1-4", "answer choice"), ("n", "next / trace step"),
                  ("p", "previous trace step"), ("j/k", "scroll / nav"),
                  ("d/u", "half page"), ("q", "back")]
    BINDINGS = ([Binding(str(i), f"ans{i}", "", show=False) for i in range(1, 10)] +
                [Binding("n", "next", "Next"),
                 Binding("p", "prev", "Previous", show=False),
                 Binding("q", "back", "Back"),
                 Binding("question_mark", "help", "Help")] +
                VimScrollMixin.VIM_BINDINGS)

    def __init__(self, book: str, chapter: str, kind: str | None = None) -> None:
        super().__init__()
        self.book = book
        self.chapter = chapter
        self.kind = kind
        self.idx = 0
        self.score = 0
        self.done = 0
        self.results: list[tuple[str, bool]] = []
        self._answered = False
        self.checks: list[tuple[str, int, dict]] = []

    def compose(self) -> ComposeResult:
        from lib.pack import load_chapter
        from lib.quiz import collect_quiz_questions
        from lib.srs import init_db
        if not self.checks:
            data = load_chapter(self.book, self.chapter)
            raw_checks = collect_quiz_questions(data)
            has_dedicated_quiz = bool(isinstance(data.get("quiz"), list) and data.get("quiz"))
            if self.kind is None:
                if has_dedicated_quiz and getattr(self, "shuffle", True):
                    import random
                    shuffled = list(raw_checks)
                    random.shuffle(shuffled)
                    self.checks = shuffled
                else:
                    self.checks = list(raw_checks)
            else:
                self.checks = [(b, i, ck) for b, i, ck in raw_checks
                               if ck.get("kind") == self.kind]
        self._con = init_db()
        with ScrollableContainer(classes="study-container"):
            yield Label(self._screen_title_text(), id="quiz-screen-title", classes="screen-title")
            yield Vertical(id="body")

    def _screen_title_text(self) -> str:
        w = self.size.width or 80
        mode_label = "QUIZ" if self.kind is None else "PARSONS"
        full_mode = "QUIZ & CHECKS" if self.kind is None else "PARSONS (ORDERING)"
        if w < 55:
            return f"⚡ {mode_label} — {self.book}/{self.chapter}"
        elif w < 80:
            return f"⚡  {full_mode} — {self.book} / {self.chapter}"
        return f"⚡  {full_mode} — {self.book} / {self.chapter}"

    def on_mount(self) -> None:
        super().on_mount()
        self.call_after_refresh(self._first_show)

    def on_resize(self) -> None:
        try:
            self.query_one("#quiz-screen-title", Label).update(self._screen_title_text())
        except Exception:
            pass

    def _first_show(self) -> None:
        if not self.checks:
            self.query_one("#body", Vertical).mount(Static("No checks found in this pack."))
            return
        self._show_body()

    def _current(self):
        return self.checks[self.idx][2]

    def _show_body(self) -> None:
        self._answered = False
        try:
            self.query_one(".study-container", ScrollableContainer).scroll_to(y=0, animate=False)
        except Exception:
            pass
        body = self.query_one("#body", Vertical)
        body.remove_children()
        b, i, ck = self.checks[self.idx]
        w = self.size.width or 80
        if w < 55:
            hdr = f"Q{self.idx + 1}/{len(self.checks)} · Score: {self.score}"
        else:
            hdr = f"QUESTION {self.idx + 1} OF {len(self.checks)}  ·  CURRENT SCORE: {self.score}"
        body.mount(Label(hdr, classes="study-header-bar"))
        body.mount(QuestionWidget(ck, self._checked, shuffle=True))

    def _checked(self, ok: bool) -> None:
        from lib.srs import log_answer
        b, i, ck = self.checks[self.idx]
        log_answer(self._con, self.book, self.chapter, b, i, ok,
                   concept=str(ck.get("concept", "")))
        self._answered = True
        self.score += ok
        self.done += 1
        self.results.append((str(ck.get("concept", "")), bool(ok)))
        body = self.query_one("#body", Vertical)
        body.mount(Button("Next Question (n)", id="next-btn"))
        body.query_one("#next-btn", Button).focus()
        self.call_after_refresh(self._scroll_to_next)

    def _scroll_to_next(self) -> None:
        try:
            self.query_one("#next-btn").scroll_visible(animate=True, top=False)
        except Exception:
            pass

    @on(Button.Pressed, "#next-btn")
    def _next_btn(self) -> None:
        self.action_next()

    def _answer_digit(self, n: int) -> None:
        if self._answered or self.idx >= len(self.checks):
            return
        curr = self._current()
        if not curr.get("choices") and curr.get("kind") not in CHOICE_KINDS:
            return
        for w in self.query(QuestionWidget):
            w.answer_choice(n - 1)

    def action_ans1(self) -> None: self._answer_digit(1)
    def action_ans2(self) -> None: self._answer_digit(2)
    def action_ans3(self) -> None: self._answer_digit(3)
    def action_ans4(self) -> None: self._answer_digit(4)
    def action_ans5(self) -> None: self._answer_digit(5)
    def action_ans6(self) -> None: self._answer_digit(6)
    def action_ans7(self) -> None: self._answer_digit(7)
    def action_ans8(self) -> None: self._answer_digit(8)
    def action_ans9(self) -> None: self._answer_digit(9)

    def action_next(self) -> None:
        if not self._answered:
            qw = self.query(QuestionWidget).first() if self.query(QuestionWidget) else None
            if qw is not None and qw.check.get("kind") == "trace":
                if qw.trace_step_next():
                    return
            return
        self.idx += 1
        if self.idx >= len(self.checks):
            self._finish()
        else:
            self._show_body()

    def action_prev(self) -> None:
        qw = self.query(QuestionWidget).first() if self.query(QuestionWidget) else None
        if qw is not None and qw.check.get("kind") == "trace":
            qw.trace_step_prev()

    def _finish(self) -> None:
        from lib.progress import record_quiz
        from lib.quiz import tally
        record_quiz(self.book, self.chapter, self.score, self.done, None,
                    items=[f"{b}:{i}" for b, i, _ in self.checks[:self.done]])
        body = self.query_one("#body", Vertical)
        body.remove_children()
        by = tally(self.results)
        pct = (100.0 * self.score / self.done) if self.done else 0
        lines = [
            f"[bold green]Session Finished![/]\n",
            f"Final Score: [bold cyan]{self.score}/{self.done}[/] ({pct:.0f}%)\n",
            "[bold white]Concept Breakdown:[/]"
        ]
        for c, (h, n) in sorted(by.items()):
            lines.append(f"  • [cyan]{c}[/]: {h}/{n} ({100.0*h/n:.0f}%)")
        weak = sorted(((c, h / n) for c, (h, n) in by.items() if h < n),
                      key=lambda r: r[1])
        if weak:
            lines.append("\n[bold yellow]Focus Areas (Weakest Concepts):[/] " + ", ".join(c for c, _ in weak[:3]))
        else:
            lines.append("\n[bold green]Outstanding! 100% on all concepts tested.[/]")
        body.mount(Static("\n".join(lines), classes="study-block-card"))
        body.mount(Static("Press [bold cyan]q[/] to return to chapter menu.", classes="study-nav-box"))

    def action_back(self) -> None:
        self.app.pop_screen()


class EditCardModal(ModalScreen):
    def __init__(self, front: str, back: str) -> None:
        super().__init__()
        self._front = front
        self._back = back
        self.saved: tuple[str, str] | None = None

    def compose(self) -> ComposeResult:
        with Vertical(id="help-box"):
            yield Label("Edit Card (empty input keeps existing)", id="help-title")
            yield Label("Front (Question):", classes="details-header")
            yield Input(value=self._front, id="edit-front", classes="question-input")
            yield Label("Back (Answer):", classes="details-header")
            yield Input(value=self._back, id="edit-back", classes="question-input")
            yield Button("Save Changes", id="edit-save", classes="btn-grade-4")
            yield Button("Cancel", id="edit-cancel", classes="btn-grade-1")

    @on(Button.Pressed, "#edit-save")
    def _save(self) -> None:
        f = self.query_one("#edit-front", Input).value.strip()
        b = self.query_one("#edit-back", Input).value.strip()
        self.dismiss((f or None, b or None))

    @on(Button.Pressed, "#edit-cancel")
    def _cancel(self) -> None:
        self.dismiss(None)


class CardsScreen(_Base):
    HELP_TITLE = "srs cards"
    HELP_LINES = [("space/f", "flip"), ("1-4/hjkl", "grade"), ("e", "edit card"), ("q", "back")]
    BINDINGS = ([Binding(str(i), f"grade{i}", "", show=False) for i in range(1, 5)] +
                [Binding("f", "flip", "Flip"),
                 Binding("space", "flip_or_space", "Flip", show=False),
                 Binding("enter", "flip_or_enter", "Flip", show=False),
                 Binding("l", "key_l", "", show=False),
                 Binding("h", "key_h", "", show=False),
                 Binding("j", "key_j", "", show=False),
                 Binding("k", "key_k", "", show=False),
                 Binding("e", "edit", "Edit"),
                 Binding("n", "next", "Next"),
                 Binding("q", "back", "Back"),
                 Binding("question_mark", "help", "Help")])

    def __init__(self, book: str) -> None:
        super().__init__()
        self.book = book
        self.idx = 0
        self.flipped = False
        self.topup_idx = 0
        self.topup: list = []
        self.topup_done = False

    def compose(self) -> ComposeResult:
        import yaml
        from lib.books import discover_chapters
        from lib.srs import due_cards, init_db, upsert_cards
        from lib.pack import load_chapter_mode
        self._con = init_db()
        for ch in discover_chapters(self.book):
            if not ch.get("has_pack"):
                continue
            try:
                data = load_chapter_mode(self.book, ch["id"], "cards")
                if data.get("cards"):
                    upsert_cards(self._con, self.book, ch["id"], data["cards"])
            except Exception:
                continue
        self.due = due_cards(self._con, self.book)
        with ScrollableContainer(classes="cards-outer"):
            yield Label(self._title_text(), id="cards-screen-title", classes="screen-title")
            yield Vertical(id="body")

    def _title_text(self) -> str:
        w = self.size.width or 80
        if w < 55:
            return f"🗂️ SRS — {self.book} ({len(self.due)} due)"
        return f"🗂️  SPACED REPETITION (SRS) — {self.book} ({len(self.due)} due)"

    def on_mount(self) -> None:
        super().on_mount()
        self.call_after_refresh(self._render_card)

    def on_resize(self) -> None:
        try:
            self.query_one("#cards-screen-title", Label).update(self._title_text())
        except Exception:
            pass

    def _render_card(self) -> None:
        body = self.query_one("#body", Vertical)
        body.remove_children()
        if self.idx >= len(self.due):
            self._start_topup()
            return
        self.flipped = False
        card = self.due[self.idx]
        card_box = Vertical(
            Label(f"🏷️  CARD {self.idx + 1} OF {len(self.due)} · DUE TODAY", classes="card-tag"),
            Static(f"Q: {card['front']}", classes="card-content"),
            Static("Press [bold cyan]Space / f[/] to flip card · [bold cyan]e[/] to edit · [bold cyan]q[/] to back", classes="card-hint"),
            classes="flashcard-frame"
        )
        body.mount(card_box)

    def action_flip_or_space(self) -> None:
        if not self.flipped:
            self.action_flip()

    def action_flip_or_enter(self) -> None:
        if not self.flipped:
            self.action_flip()

    def action_key_l(self) -> None:
        if not self.flipped:
            self.action_flip()
        else:
            self._grade_digit(4)

    def action_key_h(self) -> None:
        if self.flipped:
            self._grade_digit(1)

    def action_key_j(self) -> None:
        if self.flipped:
            self._grade_digit(2)
        else:
            try:
                self.query_one(".flashcard-frame").scroll_relative(y=2, animate=False)
            except Exception:
                pass

    def action_key_k(self) -> None:
        if self.flipped:
            self._grade_digit(3)
        else:
            try:
                self.query_one(".flashcard-frame").scroll_relative(y=-2, animate=False)
            except Exception:
                pass

    def action_flip(self) -> None:
        if self.idx < len(self.due) and not self.flipped:
            self.flipped = True
            body = self.query_one("#body", Vertical)
            card = self.due[self.idx]
            ans_box = Vertical(
                Label("💡  REVEALED ANSWER", classes="card-tag"),
                Static(f"A: {card['back']}", classes="card-content"),
                classes="flashcard-frame flashcard-flipped"
            )
            body.mount(ans_box)
            deck_class = "grade-deck-grid" if getattr(self, "size", None) and self.size.width < 70 else "grade-deck"
            deck = Horizontal(
                Button("[1] Again (<10m)", id="grade-1", classes="btn-grade-1"),
                Button("[2] Hard (1d)", id="grade-2", classes="btn-grade-2"),
                Button("[3] Good (3d)", id="grade-3", classes="btn-grade-3"),
                Button("[4] Easy (6d)", id="grade-4", classes="btn-grade-4"),
                classes=deck_class
            )
            body.mount(deck)

    @on(Button.Pressed)
    def _btn_grade(self, event: Button.Pressed) -> None:
        if event.button.id and event.button.id.startswith("grade-"):
            n = int(event.button.id.split("-")[1])
            self._grade_digit(n)

    def action_edit(self) -> None:
        if self.idx < len(self.due):
            card = self.due[self.idx]
            self.app.push_screen(EditCardModal(card["front"], card["back"]),
                                 self._edited)

    def _edited(self, result) -> None:
        """Callback from EditCardModal.dismiss: (front|None, back|None) or None."""
        if not result:
            return
        from lib.srs import update_card
        front, back = result
        card = self.due[self.idx]
        card["front"], card["back"] = update_card(self._con, card["id"],
                                                 front, back)
        self._render_card()

    def _grade_digit(self, n: int) -> None:
        from lib.srs import grade
        if self.idx < len(self.due) and self.flipped:
            qmap = {1: 0, 2: 3, 3: 4, 4: 5}
            grade(self._con, self.due[self.idx]["id"], qmap[n])
            self.idx += 1
            self._render_card()

    def action_grade1(self) -> None: self._grade_digit(1)
    def action_grade2(self) -> None: self._grade_digit(2)
    def action_grade3(self) -> None: self._grade_digit(3)
    def action_grade4(self) -> None: self._grade_digit(4)

    def action_next(self) -> None:
        pass

    def _start_topup(self) -> None:
        from lib.srs import mastered_topup
        self.topup = mastered_topup([self.book], 2 if len(self.due) < 5 else 0)
        body = self.query_one("#body", Vertical)
        if not self.topup:
            body.mount(Static("🎉 All cards reviewed! Come back tomorrow for your next SRS session.", classes="feedback-msg-success"))
            return
        body.mount(Static("Interleaved review from mastered chapters:", classes="details-header"))
        self.topup_idx = 0
        self._render_topup()

    def _render_topup(self) -> None:
        if self.topup_idx >= len(self.topup):
            self.query_one("#body", Vertical).mount(Static("Done. Press [bold cyan]q[/] to return.", classes="feedback-msg-success"))
            return
        _, _, _, _, ck = self.topup[self.topup_idx]
        self.query_one("#body", Vertical).mount(QuestionWidget(ck, self._topup_done, shuffle=True))

    def _topup_done(self, ok: bool) -> None:
        from lib.srs import log_answer
        tb, tch, tbl, tidx, tck = self.topup[self.topup_idx]
        log_answer(self._con, tb, tch, tbl, tidx, ok,
                   concept=str(tck.get("concept", "")))
        self.topup_idx += 1
        body = self.query_one("#body", Vertical)
        body.mount(Button("Next (n)", id="topup-next"))
        body.query_one("#topup-next", Button).focus()

    @on(Button.Pressed, "#topup-next")
    def _topup_next_btn(self) -> None:
        for w in list(self.query(QuestionWidget)):
            w.remove()
        for w in list(self.query("#topup-next", Button)):
            w.remove()
        self._render_topup()

    def action_back(self) -> None:
        self.app.pop_screen()


class LabScreen(_Base):
    HELP_TITLE = "lab"
    HELP_LINES = [
        ("r", "run project"),
        ("t", "test suite / verify"),
        ("e", "open in $EDITOR"),
        ("R", "reset files to starter"),
        ("h", "hint"),
        ("p/[", "previous lab"),
        ("n/]", "next lab"),
        ("tab", "switch pane"),
        ("q", "back"),
    ]
    BINDINGS = [
        Binding("r", "run_code", "Run"),
        Binding("t", "run_tests", "Test"),
        Binding("e", "open_editor", "Edit ($EDITOR)"),
        Binding("R", "reset_workspace", "Reset", show=False),
        Binding("h", "hint", "Hint"),
        Binding("p", "prev_lab", "Prev Lab"),
        Binding("n", "next_lab", "Next Lab"),
        Binding("left_square_bracket", "prev_lab", "Prev", show=False),
        Binding("right_square_bracket", "next_lab", "Next", show=False),
        Binding("tab", "switch_pane", "Switch Pane", show=False),
        Binding("q", "back", "Back"),
        Binding("question_mark", "help", "Help"),
    ]

    def __init__(self, book: str, chapter: str, lab_id: str | None = None) -> None:
        super().__init__()
        self.book = book
        self.chapter = chapter
        self.requested_lab_id = lab_id
        self.hint_idx = 0
        self.lab_idx = 0
        self.labs: list[dict] = []
        self.workspace_dir: Path | None = None
        self.files: list[str] = []
        self.active_file_idx = 0
        self.console_output = "Press 'r' to Run or 't' to Test."
        self._load_labs_data()

    def _load_labs_data(self) -> None:
        from lib.pack import load_chapter
        data = load_chapter(self.book, self.chapter)
        raw_labs = data.get("labs")
        if isinstance(raw_labs, list) and raw_labs:
            self.labs = raw_labs
        elif isinstance(data.get("lab"), dict):
            l_single = data["lab"]
            self.labs = [{
                "id": "lab1",
                "title": l_single.get("title", "Lab"),
                "instruction_md": l_single.get("prompt_md", ""),
                "files": [{"path": "starter.c", "content": l_single.get("starter_c", "")}],
                "commands": {
                    "run": l_single.get("tests_sh", ""),
                    "test": l_single.get("tests_sh", "")
                },
                "hints": l_single.get("hints", [])
            }]
        else:
            self.labs = []

        if self.requested_lab_id:
            for i, lb in enumerate(self.labs):
                if lb.get("id") == self.requested_lab_id:
                    self.lab_idx = i
                    break

        self._setup_workspace()

    def _current_lab(self) -> dict:
        if not self.labs:
            return {}
        return self.labs[self.lab_idx]

    def _setup_workspace(self, reset: bool = False) -> None:
        from lib import lab_workspace as lw
        cur = self._current_lab()
        if not cur:
            self.files = []
            return
        self.workspace_dir = lw.provision_lab_workspace(self.book, self.chapter, cur, reset=reset)
        disk_files = lw.list_workspace_files(self.workspace_dir)
        declared_files = [str(f.get("path")) for f in cur.get("files", []) if f.get("path")]
        # Combine disk files and declared files, keeping unique order
        all_files = list(dict.fromkeys(declared_files + disk_files))
        self.files = all_files
        if self.active_file_idx >= len(self.files):
            self.active_file_idx = 0

    def _detect_lang(self, fname: str) -> str:
        ext = fname.rsplit(".", 1)[-1].lower() if "." in fname else ""
        if ext in ("c", "h"):
            return "c"
        if ext in ("cpp", "cc", "cxx", "hpp"):
            return "cpp"
        if ext in ("py", "pyw"):
            return "python"
        if ext in ("js", "ts", "json"):
            return "javascript"
        if ext in ("sh", "bash"):
            return "bash"
        if ext in ("md", "markdown"):
            return "markdown"
        if ext in ("yaml", "yml"):
            return "yaml"
        return "c"

    def _active_file_path(self) -> str:
        if 0 <= self.active_file_idx < len(self.files):
            return self.files[self.active_file_idx]
        return ""

    def _active_file_content(self) -> str:
        if not self.workspace_dir:
            return ""
        rel = self._active_file_path()
        if not rel:
            return ""
        from lib import lab_workspace as lw
        return lw.read_workspace_file(self.workspace_dir, rel)

    def _save_active_file(self) -> None:
        if not self.workspace_dir:
            return
        rel = self._active_file_path()
        if not rel:
            return
        try:
            from textual.widgets import TextArea
            editor = self.query_one("#lab-code", TextArea)
            from lib import lab_workspace as lw
            lw.write_workspace_file(self.workspace_dir, rel, editor.text)
        except Exception:
            pass

    def _load_active_file_into_editor(self) -> None:
        if not self.workspace_dir:
            return
        rel = self._active_file_path()
        if not rel:
            return
        from lib import lab_workspace as lw
        text = lw.read_workspace_file(self.workspace_dir, rel)
        try:
            from textual.widgets import TextArea
            editor = self.query_one("#lab-code", TextArea)
            editor.text = text
            editor.language = self._detect_lang(rel)
        except Exception:
            pass

    def _status_badge_text(self) -> str:
        from lib.progress import is_lab_passed
        cur = self._current_lab()
        lid = cur.get("id", "lab1")
        if is_lab_passed(self.book, self.chapter, lid):
            return "PASSING ✔"
        return "UNTESTED"

    def _title_text(self) -> str:
        cur = self._current_lab()
        w = self.size.width or 80
        total = max(1, len(self.labs))
        ltitle = cur.get("title", "Lab")
        if w < 55:
            return f"💻 LAB [{self.lab_idx + 1}/{total}]: {ltitle}"
        return f"💻  CODE LAB [{self.lab_idx + 1}/{total}]: {ltitle}"

    def on_resize(self) -> None:
        try:
            self.query_one("#lab-title-label", Label).update(self._title_text())
        except Exception:
            pass

    def compose(self) -> ComposeResult:
        from textual.widgets import TextArea
        cur = self._current_lab()
        with ScrollableContainer(classes="lab-container", id="lab-scroll"):
            with Horizontal(classes="lab-header-bar"):
                yield Label(self._title_text(), id="lab-title-label", classes="screen-title")
                yield Label(self._status_badge_text(), id="lab-status-badge", classes="lab-status-pill")

            with Horizontal(classes="lab-split-top"):
                with Vertical(classes="lab-info-pane"):
                    yield Label("Task Instructions", classes="details-header")
                    inst = cur.get("instruction_md") or cur.get("prompt_md", "No instructions.")
                    yield Markdown(str(inst), id="lab-instructions")
                    yield Static("", id="lab-hint-out", classes="feedback-msg")

                with Vertical(classes="lab-editor-pane"):
                    with Horizontal(classes="lab-file-tabs-bar", id="lab-file-tabs"):
                        for idx, f_rel in enumerate(self.files):
                            variant = "primary" if idx == self.active_file_idx else "default"
                            yield Button(f_rel, id=f"tab-file-{idx}", classes="lab-file-tab-btn", variant=variant)
                    yield TextArea(self._active_file_content(), language=self._detect_lang(self._active_file_path()), id="lab-code")

            with Horizontal(classes="lab-actions-bar"):
                yield Button("▶ Run (r)", id="lab-run", variant="primary")
                yield Button("🧪 Test Suite (t)", id="lab-tests", variant="success")
                yield Button("📝 Open in $EDITOR (e)", id="lab-editor")
                yield Button("🔄 Reset (R)", id="lab-reset", variant="error")
                yield Button("💡 Hint (h)", id="lab-hint")
                if len(self.labs) > 1:
                    yield Button("◀ Prev (p)", id="lab-prev")
                    yield Button("Next (n) ▶", id="lab-next")

            with ScrollableContainer(classes="lab-console-pane", id="lab-console-scroll"):
                yield Label("Execution & Verification Console:", classes="details-header")
                yield Static(self.console_output, id="lab-out")

    def on_mount(self) -> None:
        super().on_mount()
        self.query_one("#lab-scroll").focus()

    def _show_output(self, text: str) -> None:
        self.console_output = text
        try:
            self.query_one("#lab-out", Static).update(text)
        except Exception:
            pass

    def _update_status_badge(self, passed: bool) -> None:
        try:
            badge = self.query_one("#lab-status-badge", Label)
            badge.update("PASSING ✔" if passed else "FAILING ✖")
        except Exception:
            pass

    def _update_tab_buttons(self) -> None:
        try:
            bar = self.query_one("#lab-file-tabs", Horizontal)
        except Exception:
            return
        for idx, btn in enumerate(bar.children):
            if isinstance(btn, Button):
                btn.variant = "primary" if idx == self.active_file_idx else "default"

    def _rebuild_file_tabs(self) -> None:
        """Rebuild #lab-file-tabs children from self.files so labels always
        reflect the CURRENT lab (LAB-TAB-001, SPEC-EXPL-003). Buttons are
        identified positionally (no ids) to avoid DuplicateIds races with
        Textual's asynchronous removal."""
        try:
            bar = self.query_one("#lab-file-tabs", Horizontal)
        except Exception:
            return
        old = list(bar.children)
        overlap = min(len(old), len(self.files))
        for idx in range(overlap):
            btn = old[idx]
            if isinstance(btn, Button):
                btn.label = str(self.files[idx])
                btn.variant = "primary" if idx == self.active_file_idx else "default"
        for btn in old[len(self.files):]:
            btn.remove()
        for idx in range(overlap, len(self.files)):
            bar.mount(Button(str(self.files[idx]), classes="lab-file-tab-btn",
                             variant="primary" if idx == self.active_file_idx else "default"))

    def _rebuild_screen(self) -> None:
        self._setup_workspace()
        cur = self._current_lab()
        try:
            self.query_one("#lab-title-label", Label).update(self._title_text())
            self.query_one("#lab-status-badge", Label).update(self._status_badge_text())
            inst = cur.get("instruction_md") or cur.get("prompt_md", "No instructions.")
            self.query_one("#lab-instructions", Markdown).update(str(inst))
            self.query_one("#lab-hint-out", Static).update("")
            self._load_active_file_into_editor()
            self._rebuild_file_tabs()
            self._update_tab_buttons()
        except Exception:
            # Fallback: re-mount screen
            pass

    def action_switch_pane(self) -> None:
        try:
            code = self.query_one("#lab-code")
            if getattr(self.app, "focused", None) == code:
                self.query_one("#lab-scroll").focus()
            else:
                code.focus()
        except Exception:
            pass

    def action_prev_lab(self) -> None:
        if self.lab_idx > 0:
            self._save_active_file()
            self.lab_idx -= 1
            self.hint_idx = 0
            self.active_file_idx = 0
            self._rebuild_screen()

    def action_next_lab(self) -> None:
        if self.lab_idx < len(self.labs) - 1:
            self._save_active_file()
            self.lab_idx += 1
            self.hint_idx = 0
            self.active_file_idx = 0
            self._rebuild_screen()

    def action_run_code(self) -> None:
        self._save_active_file()
        cur = self._current_lab()
        cmd = cur.get("commands", {}).get("run", "").strip()
        if not cmd:
            self._show_output("No 'run' command declared in this lab.")
            return
        from lib import lab_workspace as lw
        timeout_s = int(cur.get("commands", {}).get("timeout_s", 5))
        res = lw.run_command_in_workspace(self.workspace_dir, cmd, timeout_s=timeout_s)
        out = [f"💻 Executed: {cmd}",
               f"Status: Exit code {res['returncode']} ({res['elapsed_ms']}ms)"]
        if res.get("denied"):
            out.append(f"\n❌ ERROR: {res['error']}")
        elif res.get("timed_out"):
            out.append(f"\n❌ TIMEOUT: {res['error']}")
        else:
            if res["stdout"]:
                out.append(f"\n--- Standard Output ---\n{res['stdout']}")
            if res["stderr"]:
                out.append(f"\n--- Standard Error ---\n{res['stderr']}")
        self._show_output("\n".join(out))

    def action_run_tests(self) -> None:
        self._save_active_file()
        cur = self._current_lab()
        from lib import lab_workspace as lw
        report = lw.run_lab_verification(self.workspace_dir, cur)

        from lib.progress import record_lab_run
        record_lab_run(self.book, self.chapter, cur.get("id", "lab1"), report["passed"],
                       report["summary"], report["elapsed_ms"])

        out = []
        status_str = "PASS ✔" if report["passed"] else "FAIL ✖"
        out.append(f"🧪 Verification: {status_str}")
        out.append(f"Summary: {report['summary']} (Total time: {report['elapsed_ms']}ms)")

        if report.get("test_cmd_run"):
            out.append(f"\n--- Test Command Output ---\n{report['test_cmd_output']}")

        if report.get("case_results"):
            out.append("\n--- Input vs Expected Output Test Cases ---")
            for cr in report["case_results"]:
                tag = "[PASS ✔]" if cr["passed"] else "[FAIL ✖]"
                out.append(f"{tag} {cr['name']} (Exit {cr['returncode']}, {cr['elapsed_ms']}ms)")
                if not cr["passed"]:
                    if cr.get("diff"):
                        out.append(f"Diff:\n{cr['diff']}")
                    elif cr["returncode"] != cr["expected_exit"]:
                        out.append(f"Exit code mismatch: expected {cr['expected_exit']}, got {cr['returncode']}")
                    if cr.get("stderr"):
                        out.append(f"Stderr:\n{cr['stderr']}")

        if report.get("diff") and not report.get("case_results"):
            out.append(f"\n--- Unified Diff ---\n{report['diff']}")

        self._show_output("\n".join(out))
        self._update_status_badge(report["passed"])

    def action_open_editor(self) -> None:
        self._save_active_file()
        if not self.workspace_dir:
            return
        import os
        import subprocess
        editor = os.environ.get("EDITOR") or os.environ.get("VISUAL") or "nano"
        target = self.workspace_dir / self._active_file_path()
        try:
            with self.app.suspend():
                subprocess.run([editor, str(target)])
        except Exception as e:
            self._show_output(f"Error launching editor '{editor}': {e}")
            return
        self._load_active_file_into_editor()
        self.app.notify(f"Reloaded {self._active_file_path()} from disk")

    def action_reset_workspace(self) -> None:
        from tui.widgets import ConfirmResetModal
        cur = self._current_lab()

        def _on_confirm(confirmed: bool) -> None:
            if confirmed:
                self._setup_workspace(reset=True)
                self._load_active_file_into_editor()
                self._show_output("Workspace reset to initial starter files.")
                self.app.notify("Workspace reset to initial state")

        self.app.push_screen(ConfirmResetModal(cur.get("title", "Lab")), _on_confirm)

    def action_hint(self) -> None:
        cur = self._current_lab()
        hints = cur.get("hints", [])
        if not hints:
            self.query_one("#lab-hint-out", Static).update("No hints in pack.")
            return
        self.query_one("#lab-hint-out", Static).update(
            f"💡 Hint {self.hint_idx + 1}/{len(hints)}: {hints[self.hint_idx]}")
        self.hint_idx = (self.hint_idx + 1) % len(hints)

    @on(Button.Pressed, ".lab-file-tab-btn")
    def _file_tab_pressed(self, event: Button.Pressed) -> None:
        try:
            bar = self.query_one("#lab-file-tabs", Horizontal)
            new_idx = list(bar.children).index(event.button)
            if 0 <= new_idx < len(self.files) and new_idx != self.active_file_idx:
                self._save_active_file()
                self.active_file_idx = new_idx
                self._load_active_file_into_editor()
                self._update_tab_buttons()
        except Exception:
            pass

    @on(Button.Pressed, "#lab-run")
    def _run_btn(self) -> None:
        self.action_run_code()

    @on(Button.Pressed, "#lab-tests")
    def _tests_btn(self) -> None:
        self.action_run_tests()

    @on(Button.Pressed, "#lab-editor")
    def _editor_btn(self) -> None:
        self.action_open_editor()

    @on(Button.Pressed, "#lab-reset")
    def _reset_btn(self) -> None:
        self.action_reset_workspace()

    @on(Button.Pressed, "#lab-hint")
    def _hint_btn(self) -> None:
        self.action_hint()

    @on(Button.Pressed, "#lab-prev")
    def _prev_btn(self) -> None:
        self.action_prev_lab()

    @on(Button.Pressed, "#lab-next")
    def _next_btn(self) -> None:
        self.action_next_lab()

    def action_back(self) -> None:
        self._save_active_file()
        self.app.pop_screen()



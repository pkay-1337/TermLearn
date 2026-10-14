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

CHOICE_KINDS = ("predict", "why-fails", "mcq", "eipe", "choose-better")


class _Base(Screen):
    HELP_TITLE = "screen"
    HELP_LINES: list[tuple[str, str]] = []

    def on_mount(self) -> None:
        self.app.set_help(self.HELP_TITLE, self.HELP_LINES)

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
    HELP_LINES = [("n", "next"), ("p", "previous block"), ("r", "run example"),
                  ("j/k", "scroll"), ("d/u", "half page"), ("q", "back")]
    BINDINGS = ([Binding("n", "next", "Next"),
                 Binding("p", "prev", "Previous"),
                 Binding("r", "run_ex", "Run"),
                 Binding("q", "back", "Back"),
                 Binding("question_mark", "help", "Help")] +
                VimScrollMixin.VIM_BINDINGS)

    def __init__(self, book: str, chapter: str) -> None:
        super().__init__()
        self.book = book
        self.chapter = chapter
        self.bi = 0
        self.stage = "explain"  # explain | viz | check-i | done
        self.vi = 0

    def compose(self) -> ComposeResult:
        from lib.pack import load_chapter
        from lib.srs import init_db
        self.data = load_chapter(self.book, self.chapter)
        self.blocks = self.data.get("blocks", [])
        self._con = init_db()
        with ScrollableContainer(classes="study-container"):
            yield Vertical(id="body")

    def on_mount(self) -> None:
        super().on_mount()
        # Defer first paint past the mount transition: pushing during a
        # modal dismiss can otherwise fire on_mount before compose children
        # attach (NoMatches on #body). Refresh-then-render is always safe.
        self.call_after_refresh(self._show_body)

    def _block(self):
        return self.blocks[self.bi]

    def _show_body(self) -> None:
        body = self.query_one("#body", Vertical)
        body.remove_children()
        b = self._block()
        body.mount(Label(
            f"📖  STUDY: {b.get('title', b.get('id'))} (Block {self.bi + 1} of {len(self.blocks)})",
            classes="study-header-bar"
        ))
        if self.stage == "explain":
            body.mount(Markdown(str(b.get("explain_md", "")), classes="study-block-card"))
            ex = b.get("example") or {}
            if ex.get("code"):
                try:
                    from textual.widgets import Syntax
                    body.mount(Syntax(ex["code"], ex.get("lang", "c"), theme="monokai", classes="study-example-box"))
                except Exception:
                    body.mount(Static(ex["code"], classes="study-example-box"))
            if (b.get("viz") or {}).get("steps"):
                body.mount(Static("👉 Press [bold cyan]n[/] to step through memory visualization", classes="study-nav-box"))
            elif (b.get("checks") or []):
                body.mount(Static("👉 Press [bold cyan]n[/] to answer the checks", classes="study-nav-box"))
            else:
                body.mount(Static("👉 Press [bold cyan]n[/] to proceed to next block", classes="study-nav-box"))
        elif self.stage == "viz":
            steps = (b.get("viz") or {}).get("steps", [])
            body.mount(Static("\n".join(steps[:self.vi + 1]), classes="study-viz-box"))
            dots = "● " * (self.vi + 1) + "○ " * max(0, len(steps) - self.vi - 1)
            body.mount(Static(f"Step {self.vi + 1} of {len(steps)}  ({dots.strip()})  —  Press [bold cyan]n[/] to advance", classes="study-nav-box"))
        elif self.stage.startswith("check"):
            i = int(self.stage.split("-")[1])
            ck = (b.get("checks") or [])[i]
            body.mount(QuestionWidget(ck, self._checked))
        elif self.stage == "done":
            body.mount(Static("🎉  Block complete! Press [bold cyan]n[/]: next block · [bold cyan]p[/]: previous · [bold cyan]q[/]: back.", classes="feedback-msg-success"))

    def _checked(self, ok: bool) -> None:
        from lib.srs import log_answer
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

    def action_next(self) -> None:
        b = self._block()
        checks = b.get("checks", []) or []
        steps = (b.get("viz") or {}).get("steps", []) or []
        if self.stage == "explain":
            if steps:
                self.stage, self.vi = "viz", 0
            elif checks:
                self.stage = "check-0"
            else:
                self._advance_block()
        elif self.stage == "viz":
            self.vi += 1
            if self.vi >= len(steps):
                self.stage = "check-0" if checks else "done"
        elif self.stage.startswith("check"):
            i = int(self.stage.split("-")[1]) + 1
            self.stage = f"check-{i}" if i < len(checks) else "done"
        elif self.stage == "done":
            self._advance_block()
        self._show_body()

    def _advance_block(self) -> None:
        if self.bi + 1 < len(self.blocks):
            self.bi += 1
            self.stage = "explain"
            self.vi = 0
        else:
            self.app.pop_screen()
            self.app.notify("Chapter pass complete — try quiz, lab, then test.")

    def action_prev(self) -> None:
        if self.bi > 0:
            self.bi -= 1
            self.stage = "explain"
            self.vi = 0
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

    def action_back(self) -> None:
        self.app.pop_screen()


class QuizScreen(VimScrollMixin, _Base):
    HELP_TITLE = "quiz"
    HELP_LINES = [("1-4", "answer choice"), ("n", "next"), ("j/k", "scroll / nav"),
                  ("d/u", "half page"), ("q", "back")]
    BINDINGS = ([Binding(str(i), f"ans{i}", "", show=False) for i in range(1, 5)] +
                [Binding("n", "next", "Next"),
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

    def compose(self) -> ComposeResult:
        from lib.pack import load_chapter
        from lib.quiz import collect_checks
        from lib.srs import init_db
        data = load_chapter(self.book, self.chapter)
        self.checks = [(b, i, ck) for b, i, ck in collect_checks(data)
                       if self.kind is None or ck.get("kind") == self.kind]
        self._con = init_db()
        title = "QUIZ & CHECKS" if self.kind is None else "PARSONS (ORDERING)"
        with ScrollableContainer(classes="study-container"):
            yield Label(f"⚡  {title} — {self.book} / {self.chapter}", classes="screen-title")
            yield Vertical(id="body")

    def on_mount(self) -> None:
        super().on_mount()
        self.call_after_refresh(self._first_show)

    def _first_show(self) -> None:
        if not self.checks:
            self.query_one("#body", Vertical).mount(Static("No checks found in this pack."))
            return
        self._show_body()

    def _current(self):
        return self.checks[self.idx][2]

    def _show_body(self) -> None:
        self._answered = False
        body = self.query_one("#body", Vertical)
        body.remove_children()
        b, i, ck = self.checks[self.idx]
        body.mount(Label(
            f"QUESTION {self.idx + 1} OF {len(self.checks)}  ·  CURRENT SCORE: {self.score}",
            classes="study-header-bar"
        ))
        body.mount(QuestionWidget(ck, self._checked))

    def _checked(self, ok: bool) -> None:
        from lib.srs import log_answer
        b, i, ck = self.checks[self.idx]
        log_answer(self._con, self.book, self.chapter, b, i, ok,
                   concept=str(ck.get("concept", "")))
        self._answered = True
        self.score += ok
        self.done += 1
        self.results.append((str(ck.get("concept", "")), bool(ok)))
        self.query_one("#body", Vertical).mount(Button("Next Question (n)", id="next-btn"))
        self.query_one("#next-btn", Button).focus()
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
        if self._current().get("kind") not in CHOICE_KINDS:
            return
        for w in self.query(QuestionWidget):
            w.answer_choice(n - 1)

    def action_ans1(self) -> None: self._answer_digit(1)
    def action_ans2(self) -> None: self._answer_digit(2)
    def action_ans3(self) -> None: self._answer_digit(3)
    def action_ans4(self) -> None: self._answer_digit(4)

    def action_next(self) -> None:
        if not self._answered:
            return
        self.idx += 1
        if self.idx >= len(self.checks):
            self._finish()
        else:
            self._show_body()

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
        self._con = init_db()
        for ch in discover_chapters(self.book):
            p = Path(__file__).resolve().parents[1] / "packs" / self.book / f"{ch['id']}.yaml"
            if p.exists():
                data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
                if data.get("cards"):
                    upsert_cards(self._con, self.book, ch["id"], data["cards"])
        self.due = due_cards(self._con, self.book)
        with ScrollableContainer(classes="cards-outer"):
            yield Label(f"🗂️  SPACED REPETITION (SRS) — {self.book} ({len(self.due)} due)", classes="screen-title")
            yield Vertical(id="body")

    def on_mount(self) -> None:
        super().on_mount()
        self.call_after_refresh(self._render_card)

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
        self.query_one("#body", Vertical).mount(QuestionWidget(ck, self._topup_done))

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
    HELP_LINES = [("r", "run"), ("t", "hidden tests + snapshot"), ("h", "hint"),
                  ("tab", "switch pane"), ("q", "back")]
    BINDINGS = [Binding("r", "run_code", "Run"),
                Binding("t", "run_tests", "Tests"),
                Binding("h", "hint", "Hint"),
                Binding("tab", "switch_pane", "Switch Pane", show=False),
                Binding("q", "back", "Back"),
                Binding("question_mark", "help", "Help")]

    def __init__(self, book: str, chapter: str) -> None:
        super().__init__()
        self.book = book
        self.chapter = chapter
        self.hint_idx = 0

    def action_switch_pane(self) -> None:
        try:
            code = self.query_one("#lab-code")
            if getattr(self.app, "focused", None) == code:
                self.query_one("#lab-scroll").focus()
            else:
                code.focus()
        except Exception:
            pass

    def compose(self) -> ComposeResult:
        from textual.widgets import TextArea
        from lib.pack import load_chapter
        data = load_chapter(self.book, self.chapter)
        self.lab = data.get("lab") or {}
        with ScrollableContainer(classes="lab-container", id="lab-scroll"):
            yield Label(f"💻  CODE LAB: {self.lab.get('title', 'Lab')}", classes="screen-title")
            with Horizontal(classes="lab-split-top"):
                with Vertical(classes="lab-info-pane"):
                    yield Label("Task Instructions", classes="details-header")
                    yield Markdown(str(self.lab.get("prompt_md", "")))
                    yield Static("", id="lab-hint-out", classes="feedback-msg")
                with Vertical(classes="lab-editor-pane"):
                    yield TextArea(self.lab.get("starter_c", ""),
                                   language="c", id="lab-code")
            with Horizontal(classes="lab-actions-bar"):
                yield Button("▶ Run (r)", id="lab-run")
                yield Button("🧪 Hidden tests (t)", id="lab-tests")
                yield Button("💡 Hint (h)", id="lab-hint")
            with ScrollableContainer(classes="lab-console-pane"):
                yield Label("Terminal Console Output:", classes="details-header")
                yield Static("", id="lab-out")

    def on_mount(self) -> None:
        super().on_mount()
        self.query_one("#lab-scroll").focus()

    def _code(self) -> str:
        from textual.widgets import TextArea
        return self.query_one("#lab-code", TextArea).text

    def _show(self, text: str) -> None:
        self.query_one("#lab-out", Static).update(text)

    def action_run_code(self) -> None:
        from lib.lab import run_code
        lang = (self.lab.get("lang", "c") or "c")
        r = run_code(self._code(), lang, tests=[{"args": [], "expect": ""}],
                     timeout=2, book=self.book)
        if r.get("unsupported"):
            self._show(f"no local runner for '{lang}' — use the book toolchain")
        elif not r["compiled"]:
            self._show(f"compile error:\n{r['stderr'][:1500]}")
        elif r.get("timed_out"):
            self._show("timeout (2s). Infinite loop?")
        else:
            self._show(f"ran OK output:\n{r['output'][:2000]}")

    def action_run_tests(self) -> None:
        from lib.lab import run_code, save_solution
        lang = (self.lab.get("lang", "c") or "c")
        r = run_code(self._code(), lang, tests=[{"args": [], "expect": ""}],
                     timeout=2, book=self.book)
        verdict = bool(r.get("compiled") and not r.get("timed_out")
                       and not r.get("unsupported") and not r.get("runner_error"))
        h = save_solution(self.book, self.chapter, self._code(), verdict)
        self._show(f"snapshot {h[:12]}… ({'pass' if verdict else 'fail'})"
                   + (f"\n{r['diff'][:1000]}" if r.get("diff") else ""))

    def action_hint(self) -> None:
        hints = self.lab.get("hints", [])
        if not hints:
            self.query_one("#lab-hint-out", Static).update("No hints in pack.")
            return
        self.query_one("#lab-hint-out", Static).update(
            f"💡 Hint {self.hint_idx + 1}/{len(hints)}: {hints[self.hint_idx]}")
        self.hint_idx = (self.hint_idx + 1) % len(hints)

    @on(Button.Pressed, "#lab-run")
    def _run_btn(self) -> None:
        self.action_run_code()

    @on(Button.Pressed, "#lab-tests")
    def _tests_btn(self) -> None:
        self.action_run_tests()

    @on(Button.Pressed, "#lab-hint")
    def _hint_btn(self) -> None:
        self.action_hint()

    def action_back(self) -> None:
        self.app.pop_screen()

"""Read-only TUI screens: Home, Chapters, ChapterMenu, Revise, Stats, Test.
All data comes from lib (books/pack/progress/srs); packs are never written.
(IF-TUI-001, IF-TUI-003..005)"""
from __future__ import annotations

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, ScrollableContainer, Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Label, Markdown, OptionList, Static
from textual.widgets._option_list import Option


class _Base(Screen):
    HELP_TITLE = "screen"
    HELP_LINES: list[tuple[str, str]] = []

    def on_mount(self) -> None:
        self.app.set_help(self.HELP_TITLE, self.HELP_LINES)


class HomeScreen(_Base):
    HELP_TITLE = "books"
    HELP_LINES = [("enter", "open book"), ("q", "quit")]
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("question_mark", "help", "Help"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._slugs: list[str] = []

    def compose(self) -> ComposeResult:
        with Horizontal(classes="master-detail-row"):
            with Vertical(classes="sidebar-pane"):
                yield Label("📚  YOUR LIBRARY", classes="screen-title")
                yield OptionList(id="book-list")
            with Vertical(classes="content-pane", id="book-details"):
                yield Label("📖  BOOK DOSSIER", classes="details-header")
                yield Markdown("Select a book to preview details...", id="book-details-md")

    def on_mount(self) -> None:
        super().on_mount()
        from lib.books import discover_books
        from lib.progress import book_mastery
        lst = self.query_one("#book-list", OptionList)
        books = discover_books()
        for b in books:
            self._slugs.append(b["slug"])
            authors = ", ".join(b["authors"][:2]) if b["authors"] else "Unknown"
            mastery = book_mastery(b['slug'], b['pack_chapters'])
            opt_text = (
                f"[bold cyan]{b['slug']}[/]\n"
                f"  [white]{b['title'][:34]}[/]\n"
                f"  [dim]by {authors} · pack {b['pack_chapters']} · {mastery}[/]"
            )
            lst.add_option(Option(opt_text, id=b["slug"]))
        if self._slugs:
            lst.highlighted = 0
            self._update_details(self._slugs[0])
        lst.focus()

    def _update_details(self, slug: str) -> None:
        from lib.books import discover_books, discover_chapters
        from lib.progress import book_mastery, chapter_status
        info = next((b for b in discover_books() if b["slug"] == slug), None)
        if not info:
            return
        authors = ", ".join(info["authors"]) if info["authors"] else "Unknown"
        mastery = book_mastery(slug, info["pack_chapters"])
        chaps = discover_chapters(slug)
        chap_lines = []
        for c in chaps:
            if c["has_pack"]:
                st = chapter_status(slug, c["id"])
                badge = f"`[✔ {st.upper()}]`"
            else:
                badge = "`[○ NO PACK]`"
            chap_lines.append(f"- **{c['id']}** {badge} {c['title']}")
        curriculum_md = "\n".join(chap_lines) if chap_lines else "_No chapters discovered._"
        md_text = (
            f"## {info['title']}\n\n"
            f"- **Author(s):** {authors}\n"
            f"- **Slug:** `{slug}`\n"
            f"- **Source:** `{info.get('source', 'books/' + slug)}`\n"
            f"- **Curriculum Progress:** `{info['pack_chapters']}` chapter pack(s)\n"
            f"- **Mastery Score:** **{mastery}**\n\n"
            f"---\n\n"
            f"### 🗺️ Curriculum Roadmap ({len(chaps)} Chapters)\n\n"
            f"{curriculum_md}\n\n"
            f"---\n\n"
            f"Press **Enter** to explore chapters, or **q** to quit."
        )
        try:
            self.query_one("#book-details-md", Markdown).update(md_text)
        except Exception:
            pass

    @on(OptionList.OptionHighlighted, "#book-list")
    def _highlighted(self, event: OptionList.OptionHighlighted) -> None:
        if event.option and event.option.id:
            self._update_details(str(event.option.id))

    @on(OptionList.OptionSelected, "#book-list")
    def _open(self, event: OptionList.OptionSelected) -> None:
        self.app.book = str(event.option.id)
        from tui.screens import ChaptersScreen
        self.app.push_screen(ChaptersScreen(str(event.option.id)))

    def action_quit(self) -> None:
        self.app.exit()


class ChaptersScreen(_Base):
    HELP_TITLE = "chapters"
    HELP_LINES = [("enter", "open chapter"), ("q", "back")]
    BINDINGS = [
        Binding("q", "back", "Back"),
        Binding("question_mark", "help", "Help"),
    ]

    def __init__(self, book: str) -> None:
        super().__init__()
        self.book = book
        self._ch_ids: list[str] = []

    def compose(self) -> ComposeResult:
        with Horizontal(classes="master-detail-row"):
            with Vertical(classes="sidebar-pane"):
                yield Label(f"🗺️  CURRICULUM: {self.book}", classes="screen-title")
                yield OptionList(id="ch-list")
            with Vertical(classes="content-pane", id="ch-details"):
                yield Label("📑  CHAPTER DOSSIER", classes="details-header")
                yield Markdown("Select a chapter to view overview...", id="ch-details-md")

    def on_mount(self) -> None:
        super().on_mount()
        from lib.books import discover_chapters
        from lib.progress import chapter_due_count, chapter_lab_state, chapter_status
        lst = self.query_one("#ch-list", OptionList)
        chapters = discover_chapters(self.book)
        for ch in chapters:
            self._ch_ids.append(ch["id"])
            if ch["has_pack"]:
                status = chapter_status(self.book, ch['id'])
                due = chapter_due_count(self.book, ch['id'])
                lab = chapter_lab_state(self.book, ch['id'], ch.get('has_lab', False))
                badge = "[bold green]✔ READY[/]"
                meta = f"[cyan]{status}[/] · due: [yellow]{due}[/] · lab: [magenta]{lab}[/]"
            else:
                badge = "[dim]○ NO PACK[/]"
                meta = "[dim]run gen-prompt to generate pack[/]"
            opt_text = (
                f"[bold white]{ch['id']}[/] • {ch['title']}\n"
                f"  {badge}  {meta}"
            )
            lst.add_option(Option(opt_text, id=ch["id"]))
        if self._ch_ids:
            lst.highlighted = 0
            self._update_details(self._ch_ids[0])
        lst.focus()

    def _update_details(self, cid: str) -> None:
        from lib.books import discover_chapters
        from lib.pack import load_chapter
        from lib.progress import chapter_due_count, chapter_lab_state, chapter_status
        ch = next((c for c in discover_chapters(self.book) if c["id"] == cid), None)
        if not ch:
            return
        if not ch["has_pack"]:
            md_text = (
                f"## {cid}: {ch['title']}\n\n"
                f"- **Chapter ID:** `{cid}`\n"
                f"- **Title:** **{ch['title']}**\n\n"
                f"> [!WARNING]\n"
                f"> **No Pack Available**\n"
                f"> Generate a course pack first via `python main.py gen-prompt --book {self.book} --chapter {cid}`."
            )
        else:
            try:
                pack = load_chapter(self.book, cid)
            except Exception:
                pack = {}
            status = chapter_status(self.book, cid)
            due = chapter_due_count(self.book, cid)
            lab = chapter_lab_state(self.book, cid, ch.get("has_lab", False))
            objs = pack.get("objectives", [])
            objs_list = "\n".join(f"- {o}" for o in objs) if objs else "- No explicit objectives stated."
            title = pack.get('meta', {}).get('title', ch['title'])
            md_text = (
                f"## {cid}: {title}\n\n"
                f"- **Chapter ID:** `{cid}`\n"
                f"- **Title:** **{title}**\n"
                f"- **Source Reference:** `{pack.get('meta', {}).get('source_ref', 'N/A')}`\n"
                f"- **Status:** **{status.upper()}**\n"
                f"- **SRS Flashcards Due:** **{due}**\n"
                f"- **Lab Verification:** **{lab}**\n\n"
                f"### Learning Objectives\n"
                f"{objs_list}\n\n"
                f"---\n\n"
                f"Press **Enter** to launch learning modes for this chapter."
            )
        try:
            self.query_one("#ch-details-md", Markdown).update(md_text)
        except Exception:
            pass

    @on(OptionList.OptionHighlighted, "#ch-list")
    def _highlighted(self, event: OptionList.OptionHighlighted) -> None:
        if event.option and event.option.id:
            self._update_details(str(event.option.id))

    @on(OptionList.OptionSelected, "#ch-list")
    def _open(self, event: OptionList.OptionSelected) -> None:
        from lib.books import discover_chapters
        cid = str(event.option.id)
        info = {c["id"]: c for c in discover_chapters(self.book)}.get(cid, {})
        if not info.get("has_pack"):
            self.app.notify(f"No pack for {cid} yet — run gen-prompt first.")
            return
        self.app.chapter = cid
        from tui.screens import ChapterMenu
        self.app.push_screen(ChapterMenu(self.book, cid))

    def action_back(self) -> None:
        self.app.pop_screen()


class ChapterMenu(_Base):
    HELP_TITLE = "chapter menu"
    HELP_LINES = [("1-8", "open mode"), ("enter", "open highlighted"), ("q", "back")]
    BINDINGS = ([Binding(str(i), f"mode{i}", "", show=False) for i in range(1, 9)] +
                [Binding("q", "back", "Back"),
                 Binding("question_mark", "help", "Help")])
    MODES = ["study", "revise", "quiz", "parsons", "lab", "test", "cards", "stats"]
    MODE_TITLES = {
        "study": "📖  Study — Step-by-step walkthrough with checks & memory steppers",
        "revise": "📝  Revise — Rapid summary of notes, code examples & common bugs",
        "quiz": "⚡  Quiz — Diagnostic conceptual checks & output prediction",
        "parsons": "🧩  Parsons — Code line ordering & distractor elimination",
        "lab": "💻  Code Lab — Hands-on code challenge with test harness",
        "test": "🏆  Chapter Test — Prove mastery against gate criteria",
        "cards": "🗂️  Flashcards — Spaced repetition memory deck (SM-2)",
        "stats": "📊  Analytics — Performance accuracy & weak concept tracking",
    }

    def __init__(self, book: str, chapter: str) -> None:
        super().__init__()
        self.book = book
        self.chapter = chapter

    def compose(self) -> ComposeResult:
        from lib.books import discover_chapters
        ch_title = next((c["title"] for c in discover_chapters(self.book) if c["id"] == self.chapter), self.chapter)
        with Vertical(classes="menu-container"):
            yield Label(f"🎯  {self.book} / {self.chapter} — {ch_title}", classes="menu-banner")
            with ScrollableContainer(classes="menu-list-box"):
                yield OptionList(*[Option(f"[{i}] {self.MODE_TITLES.get(m, m)}", id=m)
                                   for i, m in enumerate(self.MODES, 1)],
                                 id="mode-list")

    def on_mount(self) -> None:
        super().on_mount()
        try:
            lst = self.query_one("#mode-list", OptionList)
            lst.highlighted = 0
            lst.focus()
        except Exception:
            pass

    def _go(self, mode: str) -> None:
        from tui import practice
        from tui.screens import ReviseScreen, StatsScreen, TestScreen
        dest = {"study": practice.StudyScreen(self.book, self.chapter),
                "revise": ReviseScreen(self.book, self.chapter),
                "quiz": practice.QuizScreen(self.book, self.chapter),
                "parsons": practice.QuizScreen(self.book, self.chapter, kind="order"),
                "lab": practice.LabScreen(self.book, self.chapter),
                "test": TestScreen(self.book, self.chapter),
                "cards": practice.CardsScreen(self.book),
                "stats": StatsScreen(self.book)}[mode]
        self.app.push_screen(dest)

    @on(OptionList.OptionSelected, "#mode-list")
    def _open(self, event: OptionList.OptionSelected) -> None:
        self._go(str(event.option.id))

    def __getattr__(self, name: str):  # action_mode1..8 -> _go(MODES[i])
        if name.startswith("action_mode") and name[len("action_mode"):].isdigit():
            i = int(name[len("action_mode"):]) - 1
            if 0 <= i < len(ChapterMenu.MODES):
                mode = ChapterMenu.MODES[i]
                return lambda: self._go(mode)
        raise AttributeError(name)

    def action_back(self) -> None:
        self.app.pop_screen()


class ReviseScreen(_Base):
    HELP_TITLE = "revise"
    HELP_LINES = [("q", "back")]
    BINDINGS = [Binding("q", "back", "Back"),
                Binding("question_mark", "help", "Help")]

    def __init__(self, book: str, chapter: str) -> None:
        super().__init__()
        self.book = book
        self.chapter = chapter

    def compose(self) -> ComposeResult:
        from lib.pack import load_chapter
        data = load_chapter(self.book, self.chapter)
        with ScrollableContainer(classes="study-container"):
            yield Label(f"📝  REVISE: {data.get('meta', {}).get('title', self.chapter)} (No Scoring)",
                        classes="study-header-bar")
            for b in data.get("blocks", []):
                with Vertical(classes="study-block-card"):
                    yield Label(f"━━ {b.get('title', b.get('id'))}", classes="details-header")
                    yield Markdown(str(b.get("explain_md", "")))
                    ex = b.get("example") or {}
                    if ex.get("code"):
                        try:
                            from textual.widgets import Syntax
                            yield Syntax(ex["code"], ex.get("lang", "c"), theme="monokai")
                        except Exception:
                            yield Static(ex["code"])
                    if b.get("common_bugs"):
                        yield Static(f"[bold yellow]Common Pitfalls:[/] " + "; ".join(b["common_bugs"]),
                                     classes="feedback-msg")

    def action_back(self) -> None:
        self.app.pop_screen()


class StatsScreen(_Base):
    HELP_TITLE = "stats"
    HELP_LINES = [("q", "back")]
    BINDINGS = [Binding("q", "back", "Back"),
                Binding("question_mark", "help", "Help")]

    def __init__(self, book: str) -> None:
        super().__init__()
        self.book = book

    def compose(self) -> ComposeResult:
        from lib.progress import chapter_stats, concept_stats
        from lib.srs import due_cards, init_db
        con = init_db()
        try:
            due_count = len(due_cards(con, self.book, limit=1000))
            block_rows = con.execute(
                "SELECT chapter, block, SUM(correct), COUNT(*) FROM answers "
                "WHERE book=? GROUP BY chapter, block ORDER BY chapter, block",
                (self.book,)
            ).fetchall()
        finally:
            con.close()

        ch_data = chapter_stats(self.book)
        c_data = concept_stats(self.book)
        total_hits = sum(r[2] or 0 for r in block_rows)
        total_attempts = sum(r[3] or 0 for r in block_rows)
        acc_pct = f"{100.0 * total_hits / total_attempts:.0f}%" if total_attempts else "—"

        with ScrollableContainer(classes="stats-container"):
            yield Label(f"📊  LEARNING ANALYTICS — {self.book}", classes="screen-title")

            with Horizontal(classes="kpi-row"):
                with Vertical(classes="kpi-card"):
                    yield Label("ACCURACY", classes="kpi-label")
                    yield Label(acc_pct, classes="kpi-value")
                with Vertical(classes="kpi-card"):
                    yield Label("SRS DUE", classes="kpi-label")
                    yield Label(f"{due_count} Cards", classes="kpi-value")
                with Vertical(classes="kpi-card"):
                    yield Label("BLOCKS STUDIED", classes="kpi-label")
                    yield Label(str(len(block_rows)), classes="kpi-value")
                with Vertical(classes="kpi-card"):
                    yield Label("CONCEPTS", classes="kpi-label")
                    yield Label(str(len(c_data)), classes="kpi-value")

            yield Label("Block Accuracy Breakdown", classes="details-section-title")
            acc = DataTable(id="acc")
            acc.add_column("Chapter"); acc.add_column("Block")
            acc.add_column("Hits"); acc.add_column("Total"); acc.add_column("Accuracy")
            for ch, bl, hits, tot in block_rows:
                pct = f"{100.0 * (hits or 0) / tot:.0f}%" if tot else "-"
                acc.add_row(ch, bl, str(hits or 0), str(tot), pct)
            yield acc

            yield Label("Concept Mastery Breakdown", classes="details-section-title")
            ct = DataTable(id="concepts")
            ct.add_column("Concept Tag"); ct.add_column("Hits"); ct.add_column("Total")
            ct.add_column("Accuracy"); ct.add_column("Review In Block")
            for r in c_data:
                pct = f"{100.0 * r['hits'] / r['total']:.0f}%" if r["total"] else "-"
                ct.add_row(r["concept"], str(r["hits"]), str(r["total"]), pct, r["block"])
            yield ct

            yield Static(f"[bold cyan]SRS Due Queue:[/] [yellow]{due_count}[/] card(s) ready for review today.")

    def action_back(self) -> None:
        self.app.pop_screen()


class TestScreen(_Base):
    HELP_TITLE = "chapter test"
    HELP_LINES = [("q", "back")]
    BINDINGS = [Binding("q", "back", "Back"),
                Binding("question_mark", "help", "Help")]

    def __init__(self, book: str, chapter: str) -> None:
        super().__init__()
        self.book = book
        self.chapter = chapter

    def compose(self) -> ComposeResult:
        from lib import lab as _lab
        from lib import progress as _prog
        from lib import quiz as _quiz
        with ScrollableContainer(classes="study-container"):
            yield Label(f"🏆  MASTERY GATE TEST — {self.book} / {self.chapter}", classes="screen-title")
            q = _quiz.score_chapter(self.book, self.chapter) or {}
            lab_result = _lab.check_lab(self.book, self.chapter)
            ok = _prog.record_test(self.book, self.chapter, q, lab_result)

            if isinstance(lab_result, dict):
                if lab_result.get("passed") is True:
                    lab_str = f"PASS ({lab_result.get('reason', 'starter compiles')})"
                elif lab_result.get("passed") is False:
                    lab_str = f"FAIL ({lab_result.get('reason', 'check failed')})"
                else:
                    lab_str = f"N/A ({lab_result.get('reason', 'no lab')})"
            else:
                lab_str = str(lab_result).upper()

            score = q.get('score', 0)
            total = q.get('total', 0)
            quiz_pct = (100.0 * score / total) if total else 0.0
            detail = f"Quiz: {score}/{total} ({quiz_pct:.0f}%) · Lab Verification: {lab_str}"

            with Vertical(classes="details-card"):
                if ok:
                    yield Label("✔  PASS — CHAPTER MASTERED!", classes="feedback-msg-success")
                else:
                    yield Label("✖  FAIL — GATE NOT PASSED", classes="feedback-msg-error")
                yield Static(detail, classes="details-meta")
                if not ok:
                    yield Static(
                        "\nTo pass this gate, review weak spots in [bold cyan]study[/], "
                        "drill checks in [bold cyan]quiz[/], and verify your code in [bold cyan]lab[/].",
                        classes="card-hint"
                    )

    def action_back(self) -> None:
        self.app.pop_screen()

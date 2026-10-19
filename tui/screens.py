"""Read-only TUI screens: Home, Chapters, ChapterMenu, Revise, Stats, Test.
All data comes from lib (books/pack/progress/srs); packs are never written.
(IF-TUI-001, IF-TUI-003..005)"""
from __future__ import annotations

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, ScrollableContainer, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Label, Markdown, OptionList, Static
from textual.widgets._option_list import Option

from tui.widgets import VimScrollMixin


class _Base(Screen):
    HELP_TITLE = "screen"
    HELP_LINES: list[tuple[str, str]] = []

    def on_mount(self) -> None:
        self.app.set_help(self.HELP_TITLE, self.HELP_LINES)

    def action_help(self) -> None:
        self.app.action_help()


class HomeScreen(_Base):
    HELP_TITLE = "books"
    HELP_LINES = [("enter", "open book"), ("j/k", "move cursor / scroll"),
                  ("l/tab", "dossier"), ("h", "back to list"), ("q", "quit")]
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        Binding("g", "cursor_home", "First", show=False),
        Binding("G", "cursor_end", "Last", show=False),
        Binding("d", "page_down", "Half Down", show=False),
        Binding("u", "page_up", "Half Up", show=False),
        Binding("l", "switch_right", "Dossier", show=False),
        Binding("h", "switch_left", "List", show=False),
        Binding("tab", "toggle_pane", "Toggle Pane", show=False),
        Binding("question_mark", "help", "Help"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._slugs: list[str] = []
        self._active_pane: str = "list"

    def _title_text(self) -> str:
        w = self.size.width or 80
        if w < 55:
            return "📚 LIBRARY"
        return "📚  YOUR LIBRARY"

    def compose(self) -> ComposeResult:
        with Horizontal(classes="master-detail-row"):
            with Vertical(classes="sidebar-pane"):
                yield Label(self._title_text(), id="home-screen-title", classes="screen-title")
                yield OptionList(id="book-list")
            with Vertical(classes="content-pane", id="book-details"):
                yield Label("📖  BOOK DOSSIER", classes="details-header")
                yield Markdown("Select a book to preview details...", id="book-details-md")

    def on_mount(self) -> None:
        super().on_mount()
        from lib.books import discover_books
        from lib.progress import book_mastery
        lst = self.query_one("#book-list", OptionList)
        dossier = self.query_one("#book-details", Vertical)
        dossier.can_focus = True
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
        self._apply_responsive_layout()

    def on_resize(self) -> None:
        self._apply_responsive_layout()

    def _apply_responsive_layout(self) -> None:
        try:
            width = self.size.width or 80
            self.query_one("#home-screen-title", Label).update(self._title_text())
            sidebar = self.query_one(".sidebar-pane")
            dossier = self.query_one("#book-details")
            if width < 70:
                if self._active_pane == "dossier":
                    sidebar.add_class("pane-hidden")
                    sidebar.remove_class("pane-full")
                    dossier.remove_class("pane-hidden")
                    dossier.add_class("pane-full")
                    dossier.focus()
                else:
                    sidebar.remove_class("pane-hidden")
                    sidebar.add_class("pane-full")
                    dossier.add_class("pane-hidden")
                    dossier.remove_class("pane-full")
                    self.query_one("#book-list").focus()
            else:
                sidebar.remove_class("pane-hidden")
                sidebar.remove_class("pane-full")
                dossier.remove_class("pane-hidden")
                dossier.remove_class("pane-full")
        except Exception:
            pass

    def action_switch_right(self) -> None:
        self._active_pane = "dossier"
        self._apply_responsive_layout()
        try:
            self.query_one("#book-details").focus()
        except Exception:
            pass

    def action_switch_left(self) -> None:
        self._active_pane = "list"
        self._apply_responsive_layout()
        try:
            self.query_one("#book-list").focus()
        except Exception:
            pass

    def action_toggle_pane(self) -> None:
        if self._active_pane == "list":
            self.action_switch_right()
        else:
            self.action_switch_left()

    def action_cursor_down(self) -> None:
        if self._active_pane == "dossier" or getattr(self.app, "focused", None) == self.query_one("#book-details"):
            try:
                self.query_one("#book-details").scroll_relative(y=2, animate=False)
            except Exception:
                pass
        else:
            try:
                self.query_one("#book-list", OptionList).action_cursor_down()
            except Exception:
                pass

    def action_cursor_up(self) -> None:
        if self._active_pane == "dossier" or getattr(self.app, "focused", None) == self.query_one("#book-details"):
            try:
                self.query_one("#book-details").scroll_relative(y=-2, animate=False)
            except Exception:
                pass
        else:
            try:
                self.query_one("#book-list", OptionList).action_cursor_up()
            except Exception:
                pass

    def action_cursor_home(self) -> None:
        if self._active_pane == "dossier" or getattr(self.app, "focused", None) == self.query_one("#book-details"):
            try:
                self.query_one("#book-details").scroll_home(animate=False)
            except Exception:
                pass
        else:
            try:
                self.query_one("#book-list", OptionList).action_first()
            except Exception:
                pass

    def action_cursor_end(self) -> None:
        if self._active_pane == "dossier" or getattr(self.app, "focused", None) == self.query_one("#book-details"):
            try:
                self.query_one("#book-details").scroll_end(animate=False)
            except Exception:
                pass
        else:
            try:
                self.query_one("#book-list", OptionList).action_last()
            except Exception:
                pass

    def action_page_down(self) -> None:
        try:
            dossier = self.query_one("#book-details")
            dossier.scroll_relative(y=max(4, dossier.size.height // 2), animate=False)
        except Exception:
            pass

    def action_page_up(self) -> None:
        try:
            dossier = self.query_one("#book-details")
            dossier.scroll_relative(y=-max(4, dossier.size.height // 2), animate=False)
        except Exception:
            pass

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
            f"Press **Enter** to explore chapters, **l/tab** to read roadmap, or **q** to quit."
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
    HELP_LINES = [("enter", "open chapter"), ("j/k", "move cursor / scroll"),
                  ("p", "generate prompts"), ("l/tab", "dossier"),
                  ("h", "back to list"), ("x", "delete chapter stats"), ("q", "back")]
    BINDINGS = [
        Binding("q", "back", "Back"),
        Binding("p", "generate_prompts", "Prompts"),
        Binding("P", "generate_prompts", "Prompts", show=False),
        Binding("x", "delete_analytics", "Delete Chapter Analytics", show=False),
        Binding("X", "delete_analytics", "Delete Chapter Analytics", show=False),
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        Binding("g", "cursor_home", "First", show=False),
        Binding("G", "cursor_end", "Last", show=False),
        Binding("d", "page_down", "Half Down", show=False),
        Binding("u", "page_up", "Half Up", show=False),
        Binding("l", "switch_right", "Dossier", show=False),
        Binding("h", "switch_left", "List", show=False),
        Binding("tab", "toggle_pane", "Toggle Pane", show=False),
        Binding("question_mark", "help", "Help"),
    ]

    def __init__(self, book: str) -> None:
        super().__init__()
        self.book = book
        self._ch_ids: list[str] = []
        self._active_pane: str = "list"

    def _title_text(self) -> str:
        w = self.size.width or 80
        if w < 55:
            return f"🗺️ {self.book}"
        return f"🗺️  CURRICULUM: {self.book}"

    def compose(self) -> ComposeResult:
        with Horizontal(classes="master-detail-row"):
            with Vertical(classes="sidebar-pane"):
                yield Label(self._title_text(), id="chapters-screen-title", classes="screen-title")
                yield OptionList(id="ch-list")
            with Vertical(classes="content-pane", id="ch-details"):
                yield Label("📑  CHAPTER DOSSIER", classes="details-header")
                yield Markdown("Select a chapter to view overview...", id="ch-details-md")

    def on_mount(self) -> None:
        super().on_mount()
        from lib.books import discover_chapters
        from lib.progress import chapter_due_count, chapter_lab_state, chapter_status
        lst = self.query_one("#ch-list", OptionList)
        dossier = self.query_one("#ch-details", Vertical)
        dossier.can_focus = True
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
        self._apply_responsive_layout()

    def on_resize(self) -> None:
        self._apply_responsive_layout()

    def _apply_responsive_layout(self) -> None:
        try:
            width = self.size.width or 80
            self.query_one("#chapters-screen-title", Label).update(self._title_text())
            sidebar = self.query_one(".sidebar-pane")
            dossier = self.query_one("#ch-details")
            if width < 70:
                if self._active_pane == "dossier":
                    sidebar.add_class("pane-hidden")
                    sidebar.remove_class("pane-full")
                    dossier.remove_class("pane-hidden")
                    dossier.add_class("pane-full")
                    dossier.focus()
                else:
                    sidebar.remove_class("pane-hidden")
                    sidebar.add_class("pane-full")
                    dossier.add_class("pane-hidden")
                    dossier.remove_class("pane-full")
                    self.query_one("#ch-list").focus()
            else:
                sidebar.remove_class("pane-hidden")
                sidebar.remove_class("pane-full")
                dossier.remove_class("pane-hidden")
                dossier.remove_class("pane-full")
        except Exception:
            pass

    def action_switch_right(self) -> None:
        self._active_pane = "dossier"
        self._apply_responsive_layout()
        try:
            self.query_one("#ch-details").focus()
        except Exception:
            pass

    def action_switch_left(self) -> None:
        self._active_pane = "list"
        self._apply_responsive_layout()
        try:
            self.query_one("#ch-list").focus()
        except Exception:
            pass

    def action_toggle_pane(self) -> None:
        if self._active_pane == "list":
            self.action_switch_right()
        else:
            self.action_switch_left()

    def action_cursor_down(self) -> None:
        if self._active_pane == "dossier" or getattr(self.app, "focused", None) == self.query_one("#ch-details"):
            try:
                self.query_one("#ch-details").scroll_relative(y=2, animate=False)
            except Exception:
                pass
        else:
            try:
                self.query_one("#ch-list", OptionList).action_cursor_down()
            except Exception:
                pass

    def action_cursor_up(self) -> None:
        if self._active_pane == "dossier" or getattr(self.app, "focused", None) == self.query_one("#ch-details"):
            try:
                self.query_one("#ch-details").scroll_relative(y=-2, animate=False)
            except Exception:
                pass
        else:
            try:
                self.query_one("#ch-list", OptionList).action_cursor_up()
            except Exception:
                pass

    def action_cursor_home(self) -> None:
        if self._active_pane == "dossier" or getattr(self.app, "focused", None) == self.query_one("#ch-details"):
            try:
                self.query_one("#ch-details").scroll_home(animate=False)
            except Exception:
                pass
        else:
            try:
                self.query_one("#ch-list", OptionList).action_first()
            except Exception:
                pass

    def action_cursor_end(self) -> None:
        if self._active_pane == "dossier" or getattr(self.app, "focused", None) == self.query_one("#ch-details"):
            try:
                self.query_one("#ch-details").scroll_end(animate=False)
            except Exception:
                pass
        else:
            try:
                self.query_one("#ch-list", OptionList).action_last()
            except Exception:
                pass

    def action_page_down(self) -> None:
        try:
            dossier = self.query_one("#ch-details")
            dossier.scroll_relative(y=max(4, dossier.size.height // 2), animate=False)
        except Exception:
            pass

    def action_page_up(self) -> None:
        try:
            dossier = self.query_one("#ch-details")
            dossier.scroll_relative(y=-max(4, dossier.size.height // 2), animate=False)
        except Exception:
            pass

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
                f"> Press **p** to generate modular AI prompts in `prompts/{self.book}/{cid}-prompts/`,\n"
                f"> or run `python main.py gen-prompt --book {self.book} --chapter {cid}`."
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
                f"Press **Enter** to launch learning modes, **p** to re-generate prompts, **l/tab** to read objectives, or **q** to back."
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
            self.app.notify(f"No pack for {cid} yet — press 'p' to generate prompts.")
            return
        self.app.chapter = cid
        from tui.screens import ChapterMenu
        self.app.push_screen(ChapterMenu(self.book, cid))

    def action_generate_prompts(self) -> None:
        try:
            lst = self.query_one("#ch-list", OptionList)
            if lst.highlighted is not None and 0 <= lst.highlighted < len(self._ch_ids):
                cid = self._ch_ids[lst.highlighted]
            else:
                return
        except Exception:
            return
        try:
            from lib.ai_prompt import emit_prompt_bundle, ROOT
            dest = emit_prompt_bundle(self.book, cid)
            rel = dest.relative_to(ROOT) if dest.is_relative_to(ROOT) else dest
            self.app.notify(f"Prompts generated in {rel}", title="Prompts Ready")
            self._update_details(cid)
        except Exception as e:
            self.app.notify(f"Failed to generate prompts: {e}", severity="error")

    def action_delete_analytics(self) -> None:
        try:
            lst = self.query_one("#ch-list", OptionList)
            if lst.highlighted is not None and 0 <= lst.highlighted < len(self._ch_ids):
                cid = self._ch_ids[lst.highlighted]
            else:
                return
        except Exception:
            return

        def _on_confirm(confirmed: bool) -> None:
            if confirmed:
                from lib.progress import wipe_chapter_progress
                wipe_chapter_progress(self.book, cid)
                self.app.notify(f"Analytics wiped for {self.book} / {cid}")
                self._update_details(cid)

        from tui.widgets import ConfirmDeleteModal
        self.app.push_screen(ConfirmDeleteModal(self.book, cid), _on_confirm)


class StudyBlockListScreen(_Base):
    HELP_TITLE = "study blocks"
    HELP_LINES = [
        ("1-9", "jump to block"),
        ("j/k", "move cursor / scroll dossier"),
        ("d/u", "half page scroll"),
        ("g/G", "first / last block"),
        ("enter/l", "start studying block"),
        ("tab", "switch list / preview pane"),
        ("q/h", "back to chapter menu"),
    ]
    BINDINGS = ([Binding(str(i), f"block{i}", "", show=False) for i in range(1, 10)] +
                [Binding("j", "cursor_down", "Down", show=False),
                 Binding("k", "cursor_up", "Up", show=False),
                 Binding("g", "cursor_first", "First", show=False),
                 Binding("G", "cursor_last", "Last", show=False),
                 Binding("d", "page_down", "Half Down", show=False),
                 Binding("u", "page_up", "Half Up", show=False),
                 Binding("l", "open_or_right", "Open", show=False),
                 Binding("h", "back_or_left", "Back", show=False),
                 Binding("tab", "toggle_pane", "Toggle Pane", show=False),
                 Binding("q", "back", "Back"),
                 Binding("question_mark", "help", "Help")])

    def __init__(self, book: str, chapter: str) -> None:
        super().__init__()
        self.book = book
        self.chapter = chapter
        self._active_pane = "list"
        self._blocks: list[dict] = []
        self._progress: list[dict] = []

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("", id="study-blocks-banner", classes="block-status-banner")
            with Horizontal(classes="master-detail-row"):
                with Vertical(id="study-blocks-list-pane", classes="sidebar-pane"):
                    yield OptionList(id="block-list")
                with ScrollableContainer(id="study-block-details", classes="content-pane"):
                    yield Markdown(id="study-block-details-md")

    def on_mount(self) -> None:
        super().on_mount()
        try:
            dossier = self.query_one("#study-block-details")
            dossier.can_focus = True
        except Exception:
            pass
        self._refresh_blocks()
        self._apply_responsive_layout()

    def on_screen_resume(self) -> None:
        self._refresh_blocks()

    def on_resize(self) -> None:
        self._apply_responsive_layout()

    def _banner_text(self) -> str:
        if not hasattr(self, "_banner_info"):
            return ""
        completed_count, total_count, pct, ch_title = self._banner_info
        w = self.size.width or 80
        if w < 55:
            return f"📖 {self.book}/{self.chapter} · Completed: {completed_count}/{total_count} ({pct}%)"
        elif w < 85:
            return f"📖 {self.book}/{self.chapter}: {ch_title} [Completed: {completed_count}/{total_count}]"
        return (
            f"📖  STUDY BLOCKS — {self.book} / {self.chapter}: {ch_title}  "
            f"[Completed: {completed_count}/{total_count} blocks · {pct}%]"
        )

    def _apply_responsive_layout(self) -> None:
        try:
            self.query_one("#study-blocks-banner", Label).update(self._banner_text())
            sidebar = self.query_one("#study-blocks-list-pane")
            dossier = self.query_one("#study-block-details")
            if (self.size.width or 80) < 70:
                if self._active_pane == "list":
                    sidebar.remove_class("pane-hidden")
                    sidebar.add_class("pane-full")
                    dossier.add_class("pane-hidden")
                    dossier.remove_class("pane-full")
                    self.query_one("#block-list").focus()
                else:
                    sidebar.add_class("pane-hidden")
                    sidebar.remove_class("pane-full")
                    dossier.remove_class("pane-hidden")
                    dossier.add_class("pane-full")
                    dossier.focus()
            else:
                sidebar.remove_class("pane-hidden")
                sidebar.remove_class("pane-full")
                dossier.remove_class("pane-hidden")
                dossier.remove_class("pane-full")
        except Exception:
            pass

    def _refresh_blocks(self) -> None:
        from lib.pack import load_chapter
        from lib.progress import chapter_blocks_progress
        try:
            data = load_chapter(self.book, self.chapter)
        except Exception:
            data = {}
        self._blocks = data.get("blocks", []) or []
        self._progress = chapter_blocks_progress(self.book, self.chapter, self._blocks)

        completed_count = sum(1 for p in self._progress if p.get("completed"))
        total_count = len(self._blocks)
        pct = int(100.0 * completed_count / total_count) if total_count else 0
        ch_title = data.get("meta", {}).get("title", self.chapter)
        self._banner_info = (completed_count, total_count, pct, ch_title)

        try:
            banner = self.query_one("#study-blocks-banner", Label)
            banner.update(self._banner_text())
        except Exception:
            pass

        try:
            lst = self.query_one("#block-list", OptionList)
        except Exception:
            return

        lst = self.query_one("#block-list", OptionList)
        prev_highlighted = lst.highlighted if lst.option_count > 0 else 0
        lst.clear_options()

        for i, (b, prog) in enumerate(zip(self._blocks, self._progress)):
            bid = b.get("id", f"b{i+1}")
            title = b.get("title", bid)
            status = prog.get("status", "not_started")
            att = prog.get("attempted", 0)
            tot = prog.get("total", 0)

            if status == "completed":
                badge = "[bold green]✔ DONE[/]"
            elif status == "in_progress":
                badge = f"[bold yellow]◐ {att}/{tot}[/]"
            else:
                badge = "[dim]○ TODO[/]"

            opt_label = f"[{i + 1}]  {badge}  {bid}: {title}"
            lst.add_option(Option(opt_label, id=str(i)))

        if total_count > 0:
            target_idx = min(prev_highlighted if prev_highlighted is not None else 0, total_count - 1)
            lst.highlighted = target_idx
            self._update_details(target_idx)
            if self._active_pane == "list":
                lst.focus()

    def _update_details(self, idx: int) -> None:
        if not (0 <= idx < len(self._blocks)):
            return
        b = self._blocks[idx]
        prog = self._progress[idx] if idx < len(self._progress) else {}
        bid = b.get("id", f"b{idx+1}")
        title = b.get("title", bid)
        b_type = str(b.get("type", "concept")).title()
        status = prog.get("status", "not_started")
        att = prog.get("attempted", 0)
        tot = prog.get("total", 0)
        cor = prog.get("correct", 0)

        if status == "completed":
            status_desc = "✔ COMPLETED"
        elif status == "in_progress":
            status_desc = f"◐ IN PROGRESS ({att}/{tot} checks attempted, {cor} correct)"
        else:
            status_desc = "○ NOT STARTED"

        concepts = set()
        for ck in b.get("checks", []) or []:
            if ck.get("concept"):
                concepts.add(ck["concept"])
        concepts_str = ", ".join(sorted(concepts)) if concepts else "—"

        viz = b.get("viz") or {}
        viz_steps = viz.get("steps", [])
        viz_info = f"{len(viz_steps)} steps" if viz_steps else "None"

        explain = str(b.get("explain_md", "")).strip()
        lines = explain.splitlines()
        preview_text = "\n".join(lines[:8]) + ("\n\n*(...more in study mode)*" if len(lines) > 8 else "")

        code_preview = ""
        ex = b.get("example") or {}
        if ex.get("code"):
            lang = ex.get("lang", "c")
            code_preview = f"\n\n### Example Code\n```{lang}\n{ex['code'].strip()}\n```"

        md_text = (
            f"## Block {idx + 1}: {title}\n\n"
            f"- **Block ID:** `{bid}`\n"
            f"- **Type:** `{b_type}`\n"
            f"- **Status:** **{status_desc}**\n"
            f"- **Checks:** **{tot}** total\n"
            f"- **Key Concepts:** `{concepts_str}`\n"
            f"- **Visualizer:** {viz_info}\n\n"
            f"### Summary\n{preview_text}"
            f"{code_preview}\n\n"
            f"---\n"
            f"👉 Press **Enter** or **l** to study this block. **Tab** toggles preview pane."
        )

        try:
            self.query_one("#study-block-details-md", Markdown).update(md_text)
        except Exception:
            pass

    @on(OptionList.OptionHighlighted, "#block-list")
    def _highlighted(self, event: OptionList.OptionHighlighted) -> None:
        if event.option and event.option.id is not None:
            try:
                self._update_details(int(event.option.id))
            except Exception:
                pass

    @on(OptionList.OptionSelected, "#block-list")
    def _selected(self, event: OptionList.OptionSelected) -> None:
        if event.option and event.option.id is not None:
            self._start_study(int(event.option.id))

    def _start_study(self, bi: int) -> None:
        from tui import practice
        self.app.push_screen(practice.StudyScreen(self.book, self.chapter, start_block=bi))

    def action_cursor_down(self) -> None:
        if self._active_pane == "dossier" or getattr(self.app, "focused", None) == self.query_one("#study-block-details"):
            try:
                self.query_one("#study-block-details").scroll_relative(y=2, animate=False)
            except Exception:
                pass
        else:
            try:
                self.query_one("#block-list", OptionList).action_cursor_down()
            except Exception:
                pass

    def action_cursor_up(self) -> None:
        if self._active_pane == "dossier" or getattr(self.app, "focused", None) == self.query_one("#study-block-details"):
            try:
                self.query_one("#study-block-details").scroll_relative(y=-2, animate=False)
            except Exception:
                pass
        else:
            try:
                self.query_one("#block-list", OptionList).action_cursor_up()
            except Exception:
                pass

    def action_cursor_first(self) -> None:
        if self._active_pane == "dossier" or getattr(self.app, "focused", None) == self.query_one("#study-block-details"):
            try:
                self.query_one("#study-block-details").scroll_home(animate=False)
            except Exception:
                pass
        else:
            try:
                self.query_one("#block-list", OptionList).action_first()
            except Exception:
                pass

    def action_cursor_last(self) -> None:
        if self._active_pane == "dossier" or getattr(self.app, "focused", None) == self.query_one("#study-block-details"):
            try:
                self.query_one("#study-block-details").scroll_end(animate=False)
            except Exception:
                pass
        else:
            try:
                self.query_one("#block-list", OptionList).action_last()
            except Exception:
                pass

    def action_page_down(self) -> None:
        try:
            dossier = self.query_one("#study-block-details")
            dossier.scroll_relative(y=max(4, dossier.size.height // 2), animate=False)
        except Exception:
            pass

    def action_page_up(self) -> None:
        try:
            dossier = self.query_one("#study-block-details")
            dossier.scroll_relative(y=-max(4, dossier.size.height // 2), animate=False)
        except Exception:
            pass

    def action_open_or_right(self) -> None:
        if (self.size.width or 80) < 70 and self._active_pane == "list":
            self.action_toggle_pane()
        else:
            try:
                lst = self.query_one("#block-list", OptionList)
                if lst.highlighted is not None:
                    opt = lst.get_option_at_index(lst.highlighted)
                    if opt and opt.id is not None:
                        self._start_study(int(opt.id))
            except Exception:
                pass

    def action_back_or_left(self) -> None:
        if (self.size.width or 80) < 70 and self._active_pane == "dossier":
            self.action_toggle_pane()
        else:
            self.action_back()

    def action_toggle_pane(self) -> None:
        if self._active_pane == "list":
            self._active_pane = "dossier"
            self._apply_responsive_layout()
            try:
                self.query_one("#study-block-details").focus()
            except Exception:
                pass
        else:
            self._active_pane = "list"
            self._apply_responsive_layout()
            try:
                self.query_one("#block-list").focus()
            except Exception:
                pass

    def __getattr__(self, name: str):  # action_block1..9 -> _start_study(i)
        if name.startswith("action_block") and name[len("action_block"):].isdigit():
            i = int(name[len("action_block"):]) - 1
            if 0 <= i < len(self._blocks):
                return lambda: self._start_study(i)
        raise AttributeError(name)

    def action_back(self) -> None:
        self.app.pop_screen()


class ChapterMenu(_Base):
    HELP_TITLE = "chapter menu"
    HELP_LINES = [("1-8", "open mode"), ("j/k", "move cursor"), ("enter/l", "open mode"), ("x", "delete chapter stats"), ("q/h", "back")]
    BINDINGS = ([Binding(str(i), f"mode{i}", "", show=False) for i in range(1, 9)] +
                [Binding("j", "cursor_down", "Down", show=False),
                 Binding("k", "cursor_up", "Up", show=False),
                 Binding("g", "cursor_first", "First", show=False),
                 Binding("G", "cursor_last", "Last", show=False),
                 Binding("l", "open_highlighted", "Open", show=False),
                 Binding("h", "back", "Back", show=False),
                 Binding("x", "delete_analytics", "Delete Chapter Analytics", show=False),
                 Binding("X", "delete_analytics", "Delete Chapter Analytics", show=False),
                 Binding("q", "back", "Back"),
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

    def _banner_text(self) -> str:
        from lib.books import discover_chapters
        ch_title = next((c["title"] for c in discover_chapters(self.book) if c["id"] == self.chapter), self.chapter)
        w = self.size.width or 80
        if w < 50:
            return f"🎯 {self.book}/{self.chapter}"
        elif w < 75:
            return f"🎯 {self.book}/{self.chapter} — {ch_title}"
        return f"🎯  {self.book} / {self.chapter} — {ch_title}"

    def compose(self) -> ComposeResult:
        with Vertical(classes="menu-container"):
            yield Label(self._banner_text(), id="menu-banner-label", classes="menu-banner")
            with ScrollableContainer(classes="menu-list-box"):
                yield OptionList(*[Option(f"[{i}] {self.MODE_TITLES.get(m, m)}", id=m)
                                   for i, m in enumerate(self.MODES, 1)],
                                 id="mode-list")

    def on_resize(self) -> None:
        try:
            self.query_one("#menu-banner-label", Label).update(self._banner_text())
        except Exception:
            pass

    def on_mount(self) -> None:
        super().on_mount()
        try:
            lst = self.query_one("#mode-list", OptionList)
            lst.highlighted = 0
            lst.focus()
        except Exception:
            pass

    def action_cursor_down(self) -> None:
        try:
            self.query_one("#mode-list", OptionList).action_cursor_down()
        except Exception:
            pass

    def action_cursor_up(self) -> None:
        try:
            self.query_one("#mode-list", OptionList).action_cursor_up()
        except Exception:
            pass

    def action_cursor_first(self) -> None:
        try:
            self.query_one("#mode-list", OptionList).action_first()
        except Exception:
            pass

    def action_cursor_last(self) -> None:
        try:
            self.query_one("#mode-list", OptionList).action_last()
        except Exception:
            pass

    def action_open_highlighted(self) -> None:
        try:
            lst = self.query_one("#mode-list", OptionList)
            if lst.highlighted is not None:
                opt = lst.get_option_at_index(lst.highlighted)
                if opt and opt.id:
                    self._go(str(opt.id))
        except Exception:
            pass

    def _go(self, mode: str) -> None:
        from tui import practice
        from tui.screens import ReviseScreen, StatsScreen, TestScreen
        dest = {"study": StudyBlockListScreen(self.book, self.chapter),
                "revise": ReviseScreen(self.book, self.chapter),
                "quiz": practice.QuizScreen(self.book, self.chapter),
                "parsons": practice.QuizScreen(self.book, self.chapter, kind="order"),
                "lab": practice.LabScreen(self.book, self.chapter),
                "test": TestScreen(self.book, self.chapter),
                "cards": practice.CardsScreen(self.book),
                "stats": StatsScreen(self.book, chapter=self.chapter)}[mode]
        self.app.push_screen(dest)

    @on(OptionList.OptionSelected, "#mode-list")
    def _open(self, event: OptionList.OptionSelected) -> None:
        self._go(str(event.option.id))

    def action_delete_analytics(self) -> None:
        def _on_confirm(confirmed: bool) -> None:
            if confirmed:
                from lib.progress import wipe_chapter_progress
                wipe_chapter_progress(self.book, self.chapter)
                self.app.notify(f"Analytics wiped for {self.book} / {self.chapter}")

        from tui.widgets import ConfirmDeleteModal
        self.app.push_screen(ConfirmDeleteModal(self.book, self.chapter), _on_confirm)

    def __getattr__(self, name: str):  # action_mode1..8 -> _go(MODES[i])
        if name.startswith("action_mode") and name[len("action_mode"):].isdigit():
            i = int(name[len("action_mode"):]) - 1
            if 0 <= i < len(ChapterMenu.MODES):
                mode = ChapterMenu.MODES[i]
                return lambda: self._go(mode)
        raise AttributeError(name)

    def action_back(self) -> None:
        self.app.pop_screen()


class ReviseScreen(VimScrollMixin, _Base):
    HELP_TITLE = "revise"
    HELP_LINES = [("j/k", "scroll 2 lines"), ("d/u", "half page"), ("g/G", "top / bottom"), ("q/h", "back")]
    BINDINGS = ([Binding("q", "back", "Back"),
                 Binding("h", "back", "Back", show=False),
                 Binding("question_mark", "help", "Help")] +
                VimScrollMixin.VIM_BINDINGS)

    def __init__(self, book: str, chapter: str) -> None:
        super().__init__()
        self.book = book
        self.chapter = chapter

    def _title_text(self) -> str:
        w = self.size.width or 80
        ch_title = getattr(self, "data", {}).get("meta", {}).get("title", self.chapter)
        if w < 55:
            return f"📝 REVISE — {self.book}/{self.chapter}"
        elif w < 80:
            return f"📝  REVISE — {self.book} / {self.chapter}"
        return f"📝  REVISE: {self.book} / {self.chapter} — {ch_title} (No Scoring)"

    def compose(self) -> ComposeResult:
        from lib.pack import load_chapter
        self.data = load_chapter(self.book, self.chapter)
        with ScrollableContainer(classes="study-container"):
            yield Label(self._title_text(), id="revise-screen-title", classes="study-header-bar")

    def on_resize(self) -> None:
        try:
            self.query_one("#revise-screen-title", Label).update(self._title_text())
        except Exception:
            pass
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


class StatsScreen(VimScrollMixin, _Base):
    HELP_TITLE = "stats"
    HELP_LINES = [("j/k", "scroll / row"), ("tab", "toggle table"), ("d/u", "half page"), ("x", "delete chapter stats"), ("q/h", "back")]
    BINDINGS = ([Binding("q", "back", "Back"),
                 Binding("h", "back", "Back", show=False),
                 Binding("tab", "switch_table", "Toggle Table", show=False),
                 Binding("x", "delete_analytics", "Delete Chapter Analytics"),
                 Binding("X", "delete_analytics", "Delete Chapter Analytics", show=False),
                 Binding("question_mark", "help", "Help")] +
                VimScrollMixin.VIM_BINDINGS)

    def __init__(self, book: str, chapter: str | None = None) -> None:
        super().__init__()
        self.book = book
        self.chapter = chapter

    def _title_text(self) -> str:
        w = self.size.width or 80
        ch_suffix = f"/{self.chapter}" if self.chapter else ""
        ch_suffix_long = f" / {self.chapter}" if self.chapter else ""
        if w < 55:
            return f"📊 STATS — {self.book}{ch_suffix}"
        return f"📊  LEARNING ANALYTICS — {self.book}{ch_suffix_long}"

    def compose(self) -> ComposeResult:
        with ScrollableContainer(classes="stats-container"):
            yield Label(self._title_text(), id="stats-screen-title", classes="screen-title")

            with Horizontal(classes="kpi-row"):
                with Vertical(classes="kpi-card"):
                    yield Label("ACCURACY", classes="kpi-label")
                    yield Label("—", classes="kpi-value", id="kpi-acc")
                with Vertical(classes="kpi-card"):
                    yield Label("SRS DUE", classes="kpi-label")
                    yield Label("—", classes="kpi-value", id="kpi-due")
                with Vertical(classes="kpi-card"):
                    yield Label("BLOCKS STUDIED", classes="kpi-label")
                    yield Label("—", classes="kpi-value", id="kpi-blocks")
                with Vertical(classes="kpi-card"):
                    yield Label("CONCEPTS", classes="kpi-label")
                    yield Label("—", classes="kpi-value", id="kpi-concepts")

            yield Label("Block Accuracy Breakdown", classes="details-section-title")
            acc = DataTable(id="acc")
            acc.add_column("Chapter"); acc.add_column("Block")
            acc.add_column("Hits"); acc.add_column("Total"); acc.add_column("Accuracy")
            yield acc

            yield Label("Concept Mastery Breakdown", classes="details-section-title")
            ct = DataTable(id="concepts")
            ct.add_column("Concept Tag"); ct.add_column("Hits"); ct.add_column("Total")
            ct.add_column("Accuracy"); ct.add_column("Review In Block")
            yield ct

            yield Static("", id="srs-status-msg")

            btn_label = f"🗑️  Delete {self.chapter} Analytics (x)" if self.chapter else "🗑️  Delete Chapter Analytics (x)"
            yield Button(btn_label, id="btn-delete-chapter", classes="delete-stats-btn")

    def on_resize(self) -> None:
        try:
            self.query_one("#stats-screen-title", Label).update(self._title_text())
        except Exception:
            pass

    def on_mount(self) -> None:
        super().on_mount()
        self._reload_data()

    def _reload_data(self) -> None:
        from lib.progress import concept_stats
        from lib.srs import due_cards, init_db
        con = init_db()
        try:
            due_count = len(due_cards(con, self.book, limit=1000))
            if self.chapter:
                block_rows = con.execute(
                    "SELECT chapter, block, SUM(correct), COUNT(*) FROM answers "
                    "WHERE book=? AND chapter=? GROUP BY chapter, block ORDER BY chapter, block",
                    (self.book, self.chapter)
                ).fetchall()
            else:
                block_rows = con.execute(
                    "SELECT chapter, block, SUM(correct), COUNT(*) FROM answers "
                    "WHERE book=? GROUP BY chapter, block ORDER BY chapter, block",
                    (self.book,)
                ).fetchall()
        finally:
            con.close()

        c_data = concept_stats(self.book)
        total_hits = sum(r[2] or 0 for r in block_rows)
        total_attempts = sum(r[3] or 0 for r in block_rows)
        acc_pct = f"{100.0 * total_hits / total_attempts:.0f}%" if total_attempts else "—"

        try:
            self.query_one("#kpi-acc", Label).update(acc_pct)
            self.query_one("#kpi-due", Label).update(f"{due_count} Cards")
            self.query_one("#kpi-blocks", Label).update(str(len(block_rows)))
            self.query_one("#kpi-concepts", Label).update(str(len(c_data)))

            acc = self.query_one("#acc", DataTable)
            acc.clear()
            for ch, bl, hits, tot in block_rows:
                pct = f"{100.0 * (hits or 0) / tot:.0f}%" if tot else "-"
                acc.add_row(ch, bl, str(hits or 0), str(tot), pct)

            ct = self.query_one("#concepts", DataTable)
            ct.clear()
            for r in c_data:
                pct = f"{100.0 * r['hits'] / r['total']:.0f}%" if r["total"] else "-"
                ct.add_row(r["concept"], str(r["hits"]), str(r["total"]), pct, r["block"])

            msg = self.query_one("#srs-status-msg", Static)
            msg.update(f"[bold cyan]SRS Due Queue:[/] [yellow]{due_count}[/] card(s) ready for review today.")
        except Exception:
            pass

    def _get_target_chapter(self) -> str | None:
        if self.chapter:
            return self.chapter
        try:
            acc = self.query_one("#acc", DataTable)
            if acc.cursor_row is not None and acc.row_count > 0:
                row_data = acc.get_row_at(acc.cursor_row)
                if row_data and len(row_data) > 0:
                    return str(row_data[0])
        except Exception:
            pass
        return None

    def action_delete_analytics(self) -> None:
        target = self._get_target_chapter()
        if not target:
            self.app.notify("No chapter selected or available to delete.", severity="warning")
            return

        def _on_confirm(confirmed: bool) -> None:
            if confirmed:
                from lib.progress import wipe_chapter_progress
                wipe_chapter_progress(self.book, target)
                self.app.notify(f"Analytics wiped for {self.book} / {target}")
                self._reload_data()

        from tui.widgets import ConfirmDeleteModal
        self.app.push_screen(ConfirmDeleteModal(self.book, target), _on_confirm)

    @on(Button.Pressed, "#btn-delete-chapter")
    def _delete_button(self) -> None:
        self.action_delete_analytics()

    def action_switch_table(self) -> None:
        try:
            acc = self.query_one("#acc", DataTable)
            concepts = self.query_one("#concepts", DataTable)
            if getattr(self.app, "focused", None) == acc:
                concepts.focus()
            else:
                acc.focus()
        except Exception:
            pass

    def action_back(self) -> None:
        self.app.pop_screen()


class TestScreen(VimScrollMixin, _Base):
    HELP_TITLE = "chapter test"
    HELP_LINES = [("j/k", "scroll"), ("d/u", "half page"), ("q/h", "back")]
    BINDINGS = ([Binding("q", "back", "Back"),
                 Binding("h", "back", "Back", show=False),
                 Binding("question_mark", "help", "Help")] +
                VimScrollMixin.VIM_BINDINGS)

    def __init__(self, book: str, chapter: str) -> None:
        super().__init__()
        self.book = book
        self.chapter = chapter

    def _title_text(self) -> str:
        w = self.size.width or 80
        if w < 55:
            return f"🏆 TEST — {self.book}/{self.chapter}"
        return f"🏆  MASTERY GATE TEST — {self.book} / {self.chapter}"

    def compose(self) -> ComposeResult:
        from lib import lab as _lab
        from lib import progress as _prog
        from lib import quiz as _quiz
        with ScrollableContainer(classes="study-container"):
            yield Label(self._title_text(), id="test-screen-title", classes="screen-title")
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

    def on_resize(self) -> None:
        try:
            self.query_one("#test-screen-title", Label).update(self._title_text())
        except Exception:
            pass

    def action_back(self) -> None:
        self.app.pop_screen()

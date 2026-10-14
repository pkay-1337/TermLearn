"""Textual TUI pilot tests: navigation, help, quiz scoring, cards, lab, stats.
Same packs as the CLI; packs are only read. (IF-TUI-001..004, VR-008+)"""
import sqlite3

import pytest

from textual.containers import Vertical
from textual.css.query import NoMatches
from textual.widgets import Input, OptionList, Static

from tui.app import LearnApp
from tui.practice import CardsScreen, LabScreen, QuizScreen

pytestmark = pytest.mark.asyncio


async def _wait_screen(app, pilot, cls, tries=120):
    for _ in range(tries):
        if isinstance(app.screen, cls):
            return app.screen
        await pilot.pause()
    raise AssertionError(f"never got {cls}: {type(app.screen)}")


async def _wait_body(app, pilot, tries=120):
    for _ in range(tries):
        try:
            return app.screen.query_one("#body", Vertical)
        except NoMatches:
            await pilot.pause()
    raise AssertionError("no #body")


async def test_nav_home_to_study_and_help(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    from tui.screens import ChapterMenu, ChaptersScreen, HomeScreen, StudyBlockListScreen
    from tui.practice import StudyScreen
    from tui.widgets import HelpModal
    app = LearnApp()
    async with app.run_test() as pilot:
        await _wait_screen(app, pilot, HomeScreen)
        assert app.screen.query_one("#book-list", OptionList).option_count >= 1
        await pilot.press("enter")
        await _wait_screen(app, pilot, ChaptersScreen)
        for _ in range(3):
            await pilot.press("down")
        await pilot.press("enter")
        menu = await _wait_screen(app, pilot, ChapterMenu)
        assert (menu.book, menu.chapter) == ("extreme-c", "ch04")
        await pilot.press("1")
        block_screen = await _wait_screen(app, pilot, StudyBlockListScreen)
        assert block_screen.query_one("#block-list", OptionList).option_count >= 1
        await pilot.press("enter")
        await _wait_screen(app, pilot, StudyScreen)
        await _wait_body(app, pilot)
        await pilot.press("question_mark")
        await pilot.pause()
        assert isinstance(app.screen, HelpModal)
        await pilot.press("escape")
        await _wait_screen(app, pilot, StudyScreen)
        await pilot.press("q")
        await _wait_screen(app, pilot, StudyBlockListScreen)
        await pilot.press("q")
        await _wait_screen(app, pilot, ChapterMenu)


async def test_quiz_parsons_scores_and_persists(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    from lib import progress
    app = LearnApp()
    async with app.run_test() as pilot:
        app.push_screen(QuizScreen("extreme-c", "ch04", kind="order"))
        await _wait_screen(app, pilot, QuizScreen)
        await _wait_body(app, pilot)
        inp = app.screen.query_one("#order-in", Input)
        inp.focus()
        await pilot.pause()
        await pilot.press(*"2 3 4")
        await pilot.press("enter")
        await pilot.pause()
        fb = app.screen.query_one("#feedback", Static)
        assert "correct" in str(fb.content).lower()
        await pilot.press("n")
        await pilot.pause()
        con = sqlite3.connect(str(progress.db_path()))
        row = con.execute("SELECT score,total FROM quiz_runs").fetchone()
        con.close()
        assert (row[0], row[1]) == (1, 1)


async def test_cards_flip_grade_persists(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    from lib import progress
    app = LearnApp()
    async with app.run_test() as pilot:
        app.push_screen(CardsScreen("extreme-c"))
        await _wait_screen(app, pilot, CardsScreen)
        await _wait_body(app, pilot)
        await pilot.press("f")
        await pilot.pause()
        await pilot.press("4")
        await pilot.pause()
        con = sqlite3.connect(str(progress.db_path()))
        n = con.execute("SELECT COUNT(*) FROM cards WHERE reps>0").fetchone()[0]
        con.close()
        assert n >= 1


async def test_lab_run_and_stats_render(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    from tui.screens import StatsScreen
    app = LearnApp()
    async with app.run_test() as pilot:
        app.push_screen(LabScreen("extreme-c", "ch04"))
        await _wait_screen(app, pilot, LabScreen)
        await pilot.press("r")
        await pilot.pause(); await pilot.pause()
        out = str(app.screen.query_one("#lab-out", Static).content)
        assert "3 7" in out, out
        app.push_screen(StatsScreen("extreme-c"))
        await _wait_screen(app, pilot, StatsScreen)
        await pilot.pause()


async def test_stats_and_test_screens_with_data(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    from lib import progress
    from tui.screens import StatsScreen, TestScreen

    # Seed data mimicking user session
    con = sqlite3.connect(str(progress.db_path()))
    con.execute("CREATE TABLE IF NOT EXISTS answers(ts INT, book TEXT, chapter TEXT, block TEXT, check_idx INT, correct INT, concept TEXT)")
    con.execute("CREATE TABLE IF NOT EXISTS quiz_runs(id INTEGER PRIMARY KEY, ts INT, book TEXT, chapter TEXT, score INT, total INT, seed INT, items TEXT)")
    con.execute("INSERT INTO answers VALUES(1, 'extreme-c', 'ch04', 'b1', 0, 1, 'pointer-basics')")
    con.execute("INSERT INTO answers VALUES(2, 'extreme-c', 'ch04', 'b2', 0, 0, 'pointer-arithmetic')")
    con.execute("INSERT INTO quiz_runs(ts, book, chapter, score, total) VALUES(1, 'extreme-c', 'ch04', 10, 12)")
    con.commit()
    con.close()

    app = LearnApp()
    async with app.run_test() as pilot:
        # Verify StatsScreen renders with data without KeyError
        app.push_screen(StatsScreen("extreme-c"))
        await _wait_screen(app, pilot, StatsScreen)
        await pilot.pause()

        # Verify TestScreen renders with data without AttributeError
        app.push_screen(TestScreen("extreme-c", "ch04"))
        await _wait_screen(app, pilot, TestScreen)
        await pilot.pause()


async def test_curriculum_chapter_names_rendered(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    from textual.widgets import Label, Markdown
    from tui.screens import ChapterMenu, ChaptersScreen, HomeScreen

    app = LearnApp()
    async with app.run_test() as pilot:
        await _wait_screen(app, pilot, HomeScreen)
        # Check HomeScreen book dossier markdown contains curriculum with chapter names
        home_md = app.screen.query_one("#book-details-md", Markdown).source
        assert "Curriculum Roadmap" in home_md
        assert "Chapter 01 — Essential Features" in home_md

        # Open ChaptersScreen
        app.push_screen(ChaptersScreen("extreme-c"))
        ch_screen = await _wait_screen(app, pilot, ChaptersScreen)
        await pilot.pause()
        ch_list = ch_screen.query_one("#ch-list", OptionList)
        assert ch_list.option_count >= 20
        # Check option text includes chapter title
        first_opt = ch_list.get_option_at_index(3)  # ch04
        assert "Chapter 01 — Essential Features" in str(first_opt.prompt)

        # Check ChapterMenu banner contains chapter name
        app.push_screen(ChapterMenu("extreme-c", "ch04"))
        menu_screen = await _wait_screen(app, pilot, ChapterMenu)
        await pilot.pause()
        banner = menu_screen.query_one(".menu-banner", Label).render()
        assert "Chapter 01 — Essential Features" in str(banner)


async def test_choice_card_multi_line_and_selection(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    from tui.widgets import ChoiceCard, QuestionWidget
    check = {
        "kind": "mcq",
        "q": "What does the preprocessor do with `#define ABC 5` and `int y = ABC;`?",
        "choices": [
            "ABC is replaced by 5 everywhere; the directive line is removed before compiling.",
            "ABC becomes a const int variable allocated in the data segment.",
            "ABC is evaluated at runtime by the preprocessor engine.",
            "The compiler replaces ABC during the code generation pass.",
        ],
        "answer": 0,
        "why": "Preprocessing happens purely as text substitution before the compiler runs.",
    }
    app = LearnApp()
    async with app.run_test() as pilot:
        done_flag = []
        qw = QuestionWidget(check, lambda ok: done_flag.append(ok))
        app.screen.mount(qw)
        await pilot.pause()
        cards = list(qw.query(ChoiceCard))
        assert len(cards) == 4
        # Check ChoiceCard has can_focus and wraps text
        assert cards[0].can_focus is True
        assert "ABC is replaced by 5" in cards[0].raw_text
        # Click or answer card 0
        cards[0].on_click()
        await pilot.pause()
        assert done_flag == [True]
        fb = qw.query_one("#feedback", Static)
        assert "correct" in str(fb.content).lower()


async def test_vim_movements_and_pane_switching(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    from tui.screens import ChapterMenu, HomeScreen
    app = LearnApp()
    async with app.run_test() as pilot:
        await _wait_screen(app, pilot, HomeScreen)
        # Test j in HomeScreen
        await pilot.press("j")
        await pilot.pause()
        # Test l to switch right to dossier
        await pilot.press("l")
        await pilot.pause()
        dossier = app.screen.query_one("#book-details")
        assert dossier.has_focus or app.screen._active_pane == "dossier"
        # Test j to scroll dossier
        await pilot.press("j")
        await pilot.pause()
        # Test h to switch back to list
        await pilot.press("h")
        await pilot.pause()
        assert app.screen._active_pane == "list"

        # Open ChapterMenu and test j/k
        app.push_screen(ChapterMenu("extreme-c", "ch04"))
        menu = await _wait_screen(app, pilot, ChapterMenu)
        for _ in range(5):
            await pilot.pause()
        lst = menu.query_one("#mode-list", OptionList)
        assert lst.highlighted == 0
        await pilot.press("j")
        await pilot.pause()
        assert lst.highlighted == 1
        await pilot.press("k")
        await pilot.pause()
        assert lst.highlighted == 0


async def test_cards_vim_space_flip(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    from lib import progress
    app = LearnApp()
    async with app.run_test() as pilot:
        app.push_screen(CardsScreen("extreme-c"))
        await _wait_screen(app, pilot, CardsScreen)
        await _wait_body(app, pilot)
        # Test space to flip
        await pilot.press("space")
        await pilot.pause()
        assert app.screen.flipped is True
        # Test l to grade (key_l grades 4 when flipped)
        await pilot.press("l")
        await pilot.pause()
        con = sqlite3.connect(str(progress.db_path()))
        n = con.execute("SELECT COUNT(*) FROM cards WHERE reps>0").fetchone()[0]
        con.close()
        assert n >= 1


async def test_small_terminal_wrapping_and_scrolling(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    from tui.practice import QuizScreen
    from tui.widgets import ChoiceCard
    app = LearnApp()
    async with app.run_test(size=(40, 12)) as pilot:
        quiz = QuizScreen("extreme-c", "ch04")
        quiz.idx = 1  # MCQ question
        app.push_screen(quiz)
        for _ in range(8):
            await pilot.pause()
        sc = app.screen.query_one(".study-container")
        assert sc.max_scroll_y > 0
        prompt = app.screen.query_one(".question-prompt")
        assert prompt.size.height >= 2
        cards = list(app.screen.query(ChoiceCard))
        assert len(cards) >= 2
        assert cards[0].size.height >= 2
        # Scroll down with j
        assert sc.scroll_y == 0
        await pilot.press("j")
        await pilot.pause()
        assert sc.scroll_y > 0
        # Scroll up with k
        await pilot.press("k")
        await pilot.pause()
        assert sc.scroll_y == 0


async def test_study_block_list_indicators_and_selection(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    from lib import progress
    from tui.screens import StudyBlockListScreen
    from tui.practice import StudyScreen
    from textual.widgets import OptionList, Markdown, Label

    # Seed progress in DB:
    # Mark block b1 completed explicitly
    progress.mark_block_completed("extreme-c", "ch04", "b1")
    # Partially answer block b2 (1 check)
    con = progress.init_db()
    con.execute("INSERT INTO answers(ts,book,chapter,block,check_idx,correct) VALUES(1,'extreme-c','ch04','b2',0,1)")
    con.commit()
    con.close()

    app = LearnApp()
    async with app.run_test() as pilot:
        screen = StudyBlockListScreen("extreme-c", "ch04")
        app.push_screen(screen)
        await _wait_screen(app, pilot, StudyBlockListScreen)
        await pilot.pause()

        lst = screen.query_one("#block-list", OptionList)
        assert lst.option_count >= 3

        # Verify indicators on options
        opt0_prompt = str(lst.get_option_at_index(0).prompt)
        opt1_prompt = str(lst.get_option_at_index(1).prompt)
        opt2_prompt = str(lst.get_option_at_index(2).prompt)

        assert "DONE" in opt0_prompt
        assert "◐" in opt1_prompt
        assert "TODO" in opt2_prompt

        # Verify banner progress
        banner = screen.query_one("#study-blocks-banner", Label)
        assert "Completed: 1/" in str(banner.render())

        # Verify dossier preview updates with block details
        dossier = screen.query_one("#study-block-details-md", Markdown)
        assert "b1" in str(dossier.source)

        # Test Vim j navigation updates highlighted and dossier
        await pilot.press("j")
        await pilot.pause()
        assert lst.highlighted == 1
        assert "b2" in str(dossier.source)

        # Test Tab to switch focus to dossier
        await pilot.press("tab")
        await pilot.pause()
        assert screen._active_pane == "dossier"

        # Tab back to list
        await pilot.press("tab")
        await pilot.pause()
        assert screen._active_pane == "list"

        # Press Enter on highlighted block (b2, index 1)
        await pilot.press("enter")
        study = await _wait_screen(app, pilot, StudyScreen)
        assert study.bi == 1
        await _wait_body(app, pilot)

        # Press h to return to block list
        await pilot.press("h")
        await _wait_screen(app, pilot, StudyBlockListScreen)




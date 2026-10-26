"""Textual TUI pilot tests: navigation, help, quiz scoring, cards, lab, stats.
Same packs as the CLI; packs are only read. (IF-TUI-001..004, VR-008+)"""
import sqlite3

import pytest

from textual.containers import Vertical
from textual.css.query import NoMatches
from textual.widgets import Input, Label, OptionList, Static

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
        for _ in range(9):
            await pilot.press("down")
        await pilot.press("enter")
        menu = await _wait_screen(app, pilot, ChapterMenu)
        assert (menu.book, menu.chapter) == ("extreme-c", "ch10")
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
        app.push_screen(QuizScreen("extreme-c", "ch10", kind="order"))
        await _wait_screen(app, pilot, QuizScreen)
        await _wait_body(app, pilot)
        inp = app.screen.query_one("#order-in", Input)
        inp.focus()
        await pilot.pause()
        await pilot.press(*"3 1 2 4")
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
        app.push_screen(LabScreen("extreme-c", "ch10"))
        await _wait_screen(app, pilot, LabScreen)
        await pilot.press("r")
        await pilot.pause(); await pilot.pause()
        out = str(app.screen.query_one("#lab-out", Static).content)
        assert len(out) > 0
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
    con.execute("INSERT INTO answers VALUES(1, 'extreme-c', 'ch10', 'b1', 0, 1, 'distinct-instance-state')")
    con.execute("INSERT INTO answers VALUES(2, 'extreme-c', 'ch10', 'b2', 0, 0, 'resource-ownership-cleanup')")
    con.execute("INSERT INTO quiz_runs(ts, book, chapter, score, total) VALUES(1, 'extreme-c', 'ch10', 10, 12)")
    con.commit()
    con.close()

    app = LearnApp()
    async with app.run_test() as pilot:
        # Verify StatsScreen renders with data without KeyError
        app.push_screen(StatsScreen("extreme-c"))
        await _wait_screen(app, pilot, StatsScreen)
        await pilot.pause()

        # Verify TestScreen renders with data without AttributeError
        app.push_screen(TestScreen("extreme-c", "ch10"))
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
        opt_ch10 = ch_list.get_option_at_index(9)  # ch10
        assert "Chapter 07 — Composition and Aggregation" in str(opt_ch10.prompt)

        # Check ChapterMenu banner contains chapter name
        app.push_screen(ChapterMenu("extreme-c", "ch10"))
        menu_screen = await _wait_screen(app, pilot, ChapterMenu)
        await pilot.pause()
        banner = menu_screen.query_one(".menu-banner", Label).render()
        assert "Chapter 07 — Composition and Aggregation" in str(banner)


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


async def test_question_widget_shuffling(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    from tui.widgets import ChoiceCard, QuestionWidget
    check = {
        "kind": "mcq",
        "q": "Which option is correct?",
        "choices": ["First (Correct)", "Second", "Third", "Fourth"],
        "answer": 0,
        "why": "First is correct.",
    }
    app = LearnApp()
    async with app.run_test() as pilot:
        done_flag = []
        # Seed 42 permutes choices
        qw = QuestionWidget(check, lambda ok: done_flag.append(ok), shuffle=True, seed=42)
        app.screen.mount(qw)
        await pilot.pause()
        cards = list(qw.query(ChoiceCard))
        assert len(cards) == 4
        # Verify choices were permuted
        assert [c.raw_text for c in cards] != check["choices"]
        # Verify the remapped correct choice card index works
        correct_card_idx = qw._ans_idx
        assert 0 <= correct_card_idx < 4
        cards[correct_card_idx].on_click()
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
        app.push_screen(ChapterMenu("extreme-c", "ch10"))
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
        quiz = QuizScreen("extreme-c", "ch10")
        quiz.idx = 1  # MCQ question (long enough to overflow a tiny terminal)
        quiz.shuffle = False  # deterministic order so idx 1 is a long question
        app.push_screen(quiz)
        # Wait for the small-terminal layout to settle: cards render and the
        # container reports scrollable overflow (proof that text wraps).
        settled = False
        for _ in range(60):
            await pilot.pause()
            cards = list(app.screen.query(ChoiceCard))
            sc = app.screen.query_one(".study-container")
            if len(cards) >= 2 and sc.max_scroll_y > 0:
                settled = True
                break
        assert settled, "quiz cards did not settle on small terminal"
        sc = app.screen.query_one(".study-container")
        assert sc.max_scroll_y > 0
        prompt = app.screen.query_one(".question-prompt")
        assert prompt.size.height >= 2
        cards = list(app.screen.query(ChoiceCard))
        assert len(cards) >= 2
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
    progress.mark_block_completed("extreme-c", "ch10", "b1")
    # Partially answer block b2 (1 check)
    con = progress.init_db()
    con.execute("INSERT INTO answers(ts,book,chapter,block,check_idx,correct) VALUES(1,'extreme-c','ch10','b2',0,1)")
    con.commit()
    con.close()

    app = LearnApp()
    async with app.run_test() as pilot:
        screen = StudyBlockListScreen("extreme-c", "ch10")
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


async def test_delete_chapter_analytics_and_help_modal(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    from lib import progress
    from textual.widgets import Label, Static
    from tui.screens import ChapterMenu, StatsScreen
    from tui.widgets import ConfirmDeleteModal, HelpModal

    # Seed data mimicking user progress
    con = sqlite3.connect(str(progress.db_path()))
    con.execute("CREATE TABLE IF NOT EXISTS answers(ts INT, book TEXT, chapter TEXT, block TEXT, check_idx INT, correct INT, concept TEXT)")
    con.execute("CREATE TABLE IF NOT EXISTS quiz_runs(id INTEGER PRIMARY KEY, ts INT, book TEXT, chapter TEXT, score INT, total INT, seed INT, items TEXT)")
    con.execute("CREATE TABLE IF NOT EXISTS block_progress(ts INT, book TEXT, chapter TEXT, block TEXT, completed INT, PRIMARY KEY(book, chapter, block))")
    con.execute("CREATE TABLE IF NOT EXISTS solutions(id INTEGER PRIMARY KEY, ts INT, book TEXT, chapter TEXT, code TEXT, lang TEXT, passed INT)")
    con.execute("INSERT INTO answers VALUES(1, 'extreme-c', 'ch10', 'b1', 0, 1, 'distinct-instance-state')")
    con.execute("INSERT INTO quiz_runs(ts, book, chapter, score, total) VALUES(1, 'extreme-c', 'ch10', 10, 12)")
    con.execute("INSERT INTO block_progress VALUES(1, 'extreme-c', 'ch10', 'b1', 1)")
    con.execute("INSERT INTO solutions(ts, book, chapter, code, lang, passed) VALUES(1, 'extreme-c', 'ch10', 'int main(){}', 'c', 1)")
    con.commit()
    con.close()

    app = LearnApp()
    async with app.run_test() as pilot:
        # 1. Open StatsScreen for chapter
        app.push_screen(StatsScreen("extreme-c", chapter="ch10"))
        screen = await _wait_screen(app, pilot, StatsScreen)
        await pilot.pause()

        # Verify initial data loaded
        blocks_label = screen.query_one("#kpi-blocks", Label)
        assert str(blocks_label.render()) == "1"

        # 2. Check ? help overlay displays x delete shortcut
        await pilot.press("question_mark")
        help_modal = await _wait_screen(app, pilot, HelpModal)
        help_text = "".join(str(s.render()) for s in help_modal.query(Static))
        assert "delete chapter stats" in help_text
        assert "x" in help_text

        # Close help modal
        await pilot.press("escape")
        await _wait_screen(app, pilot, StatsScreen)
        await pilot.pause()

        # 3. Press x to trigger analytics deletion
        await pilot.press("x")
        confirm_modal = await _wait_screen(app, pilot, ConfirmDeleteModal)
        assert confirm_modal.chapter == "ch10"

        # Confirm with 'y'
        await pilot.press("y")
        await _wait_screen(app, pilot, StatsScreen)
        await pilot.pause()

        # Verify SQLite wiped for this chapter
        con = sqlite3.connect(str(progress.db_path()))
        ans_count = con.execute("SELECT COUNT(*) FROM answers WHERE book='extreme-c' AND chapter='ch10'").fetchone()[0]
        quiz_count = con.execute("SELECT COUNT(*) FROM quiz_runs WHERE book='extreme-c' AND chapter='ch10'").fetchone()[0]
        bp_count = con.execute("SELECT COUNT(*) FROM block_progress WHERE book='extreme-c' AND chapter='ch10'").fetchone()[0]
        sol_count = con.execute("SELECT COUNT(*) FROM solutions WHERE book='extreme-c' AND chapter='ch10'").fetchone()[0]
        con.close()
        assert ans_count == 0
        assert quiz_count == 0
        assert bp_count == 0
        assert sol_count == 0

        # Verify StatsScreen reactive refresh
        assert str(screen.query_one("#kpi-blocks", Label).render()) == "0"
        assert str(screen.query_one("#kpi-acc", Label).render()) == "—"

        # 4. Check ChapterMenu also has ? info and cancel flow
        app.push_screen(ChapterMenu("extreme-c", "ch10"))
        await _wait_screen(app, pilot, ChapterMenu)
        await pilot.pause()

        await pilot.press("question_mark")
        help_modal2 = await _wait_screen(app, pilot, HelpModal)
        help_text2 = "".join(str(s.render()) for s in help_modal2.query(Static))
        assert "delete chapter stats" in help_text2
        await pilot.press("escape")
        await _wait_screen(app, pilot, ChapterMenu)
        await pilot.pause()

        # Press x and cancel with n
        await pilot.press("x")
        modal = await _wait_screen(app, pilot, ConfirmDeleteModal)
        await pilot.press("n")
        await _wait_screen(app, pilot, ChapterMenu)


async def test_study_screen_p_and_n_navigation_and_trace(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    from tui.practice import StudyScreen
    from tui.widgets import QuestionWidget, HelpModal
    app = LearnApp()
    async with app.run_test() as pilot:
        # Load ch10 at block 0
        app.push_screen(StudyScreen("extreme-c", "ch10", start_block=0))
        await _wait_screen(app, pilot, StudyScreen)
        await _wait_body(app, pilot)
        s = app.screen
        assert s.stage == "explain"

        # Test help modal with '?'
        await pilot.press("?")
        await pilot.pause()
        assert isinstance(app.screen, HelpModal)
        await pilot.press("escape")
        await _wait_screen(app, pilot, StudyScreen)

        # Advance to viz
        await pilot.press("n")
        await pilot.pause()
        assert s.stage == "viz"
        assert s.vi == 0

        # Advance viz step
        await pilot.press("n")
        await pilot.pause()
        assert s.stage == "viz"
        assert s.vi == 1

        # Press p to go back to viz step 0
        await pilot.press("p")
        await pilot.pause()
        assert s.stage == "viz"
        assert s.vi == 0

        # Press p to go back to explain
        await pilot.press("p")
        await pilot.pause()
        assert s.stage == "explain"

        # Press p at explain when bi==0 (should notify and remain at explain)
        await pilot.press("p")
        await pilot.pause()
        assert s.stage == "explain"

        # Advance directly to the trace check in block 0
        s.stage = "check-3"
        s._show_body()
        await pilot.pause()
        qw = s.query_one(QuestionWidget)
        assert qw.check.get("kind") == "trace"
        assert qw._trace_step == 1

        # Press 'n' to step forward in trace (does NOT advance to check-4)
        await pilot.press("n")
        await pilot.pause()
        assert s.stage == "check-3"
        assert qw._trace_step == 2

        # Press 'p' to step back in trace (does NOT jump block)
        await pilot.press("p")
        await pilot.pause()
        assert s.stage == "check-3"
        assert qw._trace_step == 1

        # Press 'p' when at trace step 1 (goes back to check-2)
        await pilot.press("p")
        await pilot.pause()
        assert s.stage == "check-2"


async def test_quiz_screen_trace_stepping(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    from tui.practice import QuizScreen
    from tui.widgets import QuestionWidget
    trace_check = {
        "kind": "trace",
        "level": "core",
        "q": "Trace memory addresses",
        "code": "int x = 42;",
        "trace": {
            "headers": ["Step", "Variable", "Address", "Value"],
            "rows": [
                {"step": 1, "cells": ["1", "x", "0x1000", "42"]},
                {"step": 2, "cells": ["2", "x", "0x1000", "99"]}
            ]
        },
        "target": {"row": 1, "col": 3},
        "answer_text": "99",
        "why": "x was modified to 99"
    }
    app = LearnApp()
    async with app.run_test() as pilot:
        qs = QuizScreen("extreme-c", "ch10")
        qs.checks = [("ch10", 0, trace_check)]
        app.push_screen(qs)
        await _wait_screen(app, pilot, QuizScreen)
        await _wait_body(app, pilot)
        qw = qs.query_one(QuestionWidget)
        assert qw._trace_step == 1

        # Press 'n': advances trace step, does not advance question
        await pilot.press("n")
        await pilot.pause()
        assert qs.idx == 0
        assert qw._trace_step == 2

        # Press 'p': steps back trace
        await pilot.press("p")
        await pilot.pause()
        assert qs.idx == 0
        assert qw._trace_step == 1


async def test_quiz_option_selection_via_digits_and_clicks(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    from tui.widgets import ChoiceCard
    app = LearnApp()
    async with app.run_test() as pilot:
        quiz = QuizScreen("extreme-c", "ch10")
        app.push_screen(quiz)
        await _wait_screen(app, pilot, QuizScreen)
        await _wait_body(app, pilot)

        # 1. Spot-bug check with digit key 1
        sb_idx = next(i for i, (_, _, ck) in enumerate(quiz.checks) if ck.get("kind") == "spot-bug")
        quiz.idx = sb_idx
        quiz._show_body()
        await pilot.pause()
        assert not quiz._answered
        await pilot.press("1")
        await pilot.pause()
        assert quiz._answered

        # 2. MCQ check with mouse click
        quiz.idx = next(i for i, (_, _, ck) in enumerate(quiz.checks) if ck.get("kind") == "mcq")
        quiz._show_body()
        await pilot.pause()
        assert not quiz._answered
        cards = list(quiz.query(ChoiceCard))
        assert len(cards) >= 2
        cards[0].scroll_visible(animate=False)
        await pilot.pause()
        await pilot.click(cards[0])
        await pilot.pause()
        assert quiz._answered

        # 3. Out-of-bounds digit press is ignored
        quiz.idx = next(i for i, (_, _, ck) in enumerate(quiz.checks) if ck.get("choices"))
        quiz._show_body()
        await pilot.pause()
        assert not quiz._answered
        await pilot.press("9")
        await pilot.pause()
        assert not quiz._answered


async def test_study_option_selection_via_digits(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    from tui.practice import StudyScreen
    app = LearnApp()
    async with app.run_test() as pilot:
        study = StudyScreen("extreme-c", "ch10")
        app.push_screen(study)
        await _wait_screen(app, pilot, StudyScreen)
        await _wait_body(app, pilot)

        # Move to check stage
        study.stage = "check-0"
        study._show_body()
        await pilot.pause()
        assert not study._check_answered

        # Press digit 2 to answer check
        await pilot.press("2")
        await pilot.pause()
        assert study._check_answered


CAR_SOLUTION = """#include <stdlib.h>
#include "car.h"
#include "engine.h"

struct car_t {
  engine_t* engine;
};

car_t* car_new(void) {
  car_t* car = (car_t*)malloc(sizeof(car_t));
  if (!car) return NULL;
  car->engine = engine_new();
  if (!car->engine) { free(car); return NULL; }
  return car;
}

void car_free(car_t* car) {
  if (!car) return;
  engine_free(car->engine);
  free(car);
}

void car_start(car_t* car) { if (car) engine_turn_on(car->engine); }
void car_stop(car_t* car) { if (car) engine_turn_off(car->engine); }
double car_get_engine_temperature(const car_t* car) {
  return car ? engine_get_temperature(car->engine) : 0.0;
}
"""


async def test_multi_lab_workspace_tui(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    from lib import lab_workspace as lw
    # Hermetic: provision workspaces under tmp_path, not the developer's labs/.
    monkeypatch.setattr(lw, "PROJECT_ROOT", tmp_path)
    app = LearnApp()
    async with app.run_test() as pilot:
        lab_screen = LabScreen("extreme-c", "ch10")
        app.push_screen(lab_screen)
        await _wait_screen(app, pilot, LabScreen)
        await pilot.pause()
        await pilot.pause()
        assert len(lab_screen.labs) == 3
        assert lab_screen.lab_idx == 0

        # Title shows [1/3]
        title_lbl = app.screen.query_one("#lab-title-label")
        assert "[1/3]" in str(title_lbl.render())

        # File tabs are present and show lab1's files (4 files)
        tabs = app.screen.query(".lab-file-tab-btn")
        assert len(tabs) == 4
        assert str(app.screen.query(".lab-file-tab-btn")[2].label) == "main.c"

        # Switch to Next Lab (lab2) via 'n'
        await pilot.press("n")
        await pilot.pause()
        await pilot.pause()
        assert lab_screen.lab_idx == 1
        title_lbl2 = app.screen.query_one("#lab-title-label")
        assert "[2/3]" in str(title_lbl2.render())

        # Tab bar rebuilt for lab2's 6 files — labels refreshed (LAB-TAB-001)
        assert len(app.screen.query(".lab-file-tab-btn")) == 6
        assert str(app.screen.query(".lab-file-tab-btn")[2].label) == "car.h"
        assert str(app.screen.query(".lab-file-tab-btn")[3].label) == "car.c"

        # Back to lab1 via 'p' — labels return to lab1's files
        await pilot.press("p")
        await pilot.pause()
        await pilot.pause()
        assert lab_screen.lab_idx == 0
        assert len(app.screen.query(".lab-file-tab-btn")) == 4
        assert str(app.screen.query(".lab-file-tab-btn")[2].label) == "main.c"

        # Run test verification via 't': solve car.c first (fresh workspace
        # starts blank per FR-AI-006), then hidden tests must pass.
        await pilot.press("n")
        await pilot.pause()
        await pilot.pause()
        lw.write_workspace_file(lab_screen.workspace_dir, "car.c", CAR_SOLUTION)
        await pilot.press("t")
        await pilot.pause()
        await pilot.pause()
        out = str(app.screen.query_one("#lab-out", Static).content)
        assert "PASS" in out

        # Status badge is updated to PASSING
        badge = app.screen.query_one("#lab-status-badge")
        assert "PASSING" in str(badge.render())

async def test_revise_screen_renders_content(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    from tui.screens import ReviseScreen
    app = LearnApp()
    async with app.run_test() as pilot:
        screen = ReviseScreen("extreme-c", "ch10")
        app.push_screen(screen)
        await _wait_screen(app, pilot, ReviseScreen)
        await pilot.pause()
        cards = screen.query(".study-block-card")
        assert len(cards) >= 1

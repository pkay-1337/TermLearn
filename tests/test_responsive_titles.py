"""Tests for responsive non-wrapping top titles across narrow viewports (Termux/mobile)."""
import pytest
from textual.widgets import Label
from tui.app import LearnApp
from tui.practice import StudyScreen, QuizScreen, CardsScreen
from tui.screens import StudyBlockListScreen, ChapterMenu, ReviseScreen, StatsScreen, TestScreen


@pytest.mark.asyncio
async def test_screen_title_css_properties():
    app = LearnApp()
    async with app.run_test(size=(40, 20)) as pilot:
        screen = QuizScreen("extreme-c", "ch10")
        app.push_screen(screen)
        await pilot.pause()
        
        lbl = screen.query_one("#quiz-screen-title", Label)
        assert lbl.styles.text_wrap == "nowrap"
        assert lbl.styles.text_overflow == "ellipsis"
        assert lbl.styles.overflow_x == "hidden"


@pytest.mark.asyncio
async def test_narrow_titles_concise_formatting():
    app = LearnApp()
    async with app.run_test(size=(40, 20)) as pilot:
        study = StudyScreen("extreme-c", "ch10")
        app.push_screen(study)
        await pilot.pause()
        lbl = study.query_one("#study-screen-title", Label)
        assert str(lbl.render()) == "📖 STUDY — extreme-c/ch10"

        quiz = QuizScreen("extreme-c", "ch10")
        app.push_screen(quiz)
        await pilot.pause()
        lbl = quiz.query_one("#quiz-screen-title", Label)
        assert str(lbl.render()) == "⚡ QUIZ — extreme-c/ch10"

        menu = ChapterMenu("extreme-c", "ch10")
        app.push_screen(menu)
        await pilot.pause()
        lbl = menu.query_one("#menu-banner-label", Label)
        assert str(lbl.render()) == "🎯 extreme-c/ch10"

        revise = ReviseScreen("extreme-c", "ch10")
        app.push_screen(revise)
        await pilot.pause()
        lbl = revise.query_one("#revise-screen-title", Label)
        assert str(lbl.render()) == "📝 REVISE — extreme-c/ch10"

        test_s = TestScreen("extreme-c", "ch10")
        app.push_screen(test_s)
        await pilot.pause()
        lbl = test_s.query_one("#test-screen-title", Label)
        assert str(lbl.render()) == "🏆 TEST — extreme-c/ch10"

        stats = StatsScreen("extreme-c", chapter="ch10")
        app.push_screen(stats)
        await pilot.pause()
        lbl = stats.query_one("#stats-screen-title", Label)
        assert str(lbl.render()) == "📊 STATS — extreme-c/ch10"


@pytest.mark.asyncio
async def test_wide_titles_full_formatting():
    app = LearnApp()
    async with app.run_test(size=(100, 30)) as pilot:
        study = StudyScreen("extreme-c", "ch10")
        app.push_screen(study)
        await pilot.pause()
        lbl = study.query_one("#study-screen-title", Label)
        assert "Chapter 07 — Composition and Aggregation" in str(lbl.render())

        quiz = QuizScreen("extreme-c", "ch10")
        app.push_screen(quiz)
        await pilot.pause()
        lbl = quiz.query_one("#quiz-screen-title", Label)
        assert "QUIZ & CHECKS" in str(lbl.render())

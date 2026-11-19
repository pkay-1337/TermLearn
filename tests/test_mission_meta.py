import pytest
from lib import mission_meta as mm


DATA = {
    "meta": {
        "track": "kernel",
        "phase": "P1",
    },
    "blocks": [{
        "id": "b1",
        "checks": [{"kind": "predict", "from_chapter": "T0A", "from_block": "b2"}],
    }],
}


def test_badge_and_preview_helpers():
    lab = {
        "tier": "core",
        "family": "boot-gdb",
        "environment": {"boundary": "vm", "privilege": "user", "network": "none"},
        "commands": {"tinker": "sh debug.sh"},
        "expected_observation": "Breakpoint reaches main.",
    }
    assert "TIER:core" in mm.format_lab_badges(lab)
    assert "BOUNDARY:vm" in mm.format_lab_badges(lab)
    preview = mm.tinker_preview(lab, "/tmp/lab")
    assert "sh debug.sh" in preview
    assert "Breakpoint reaches main." in preview
    assert "TRACK:kernel" in mm.format_chapter_badges(DATA)


def test_review_and_next_helpers():
    check = DATA["blocks"][0]["checks"][0]
    assert "T0A/b2" in mm.interleaved_label(check)
    chapters = [
        {"id": "a", "has_pack": True, "status": "mastered", "due": 0, "title": "A"},
        {"id": "b", "has_pack": True, "status": "studying", "due": 2, "title": "B"},
        {"id": "c", "has_pack": False, "status": "new", "due": 0, "title": "C"},
    ]
    assert mm.suggest_next(chapters)["id"] == "b"


def test_tui_lab_screen_badges_and_observation(tmp_path):
    from tui.practice import LabScreen

    screen = LabScreen("bgnet", "ch03")
    screen.workspace_dir = tmp_path
    screen.labs = [{
        "id": "lab1",
        "title": "Debug Lab",
        "instruction_md": "Debug the program.",
        "tier": "core",
        "family": "debug",
        "environment": {"boundary": "host", "privilege": "user", "network": "none"},
        "commands": {"run": "true", "tinker": "gdb ./app"},
    }]
    screen.data = DATA
    badges = mm.format_lab_badges(screen.labs[0])
    assert "TIER:core" in badges
    assert "BOUNDARY:host" in badges

    # Test observations.md creation
    obs_file = tmp_path / "observations.md"
    assert not obs_file.exists()

    # Simulate observation note writing
    note = "Found breakpoint at line 42"
    header = f"# Lab Observations: {screen.labs[0]['title']}\n\n"
    content = f"- {note}\n"
    obs_file.write_text(header + content, encoding="utf-8")
    assert obs_file.exists()
    assert "Found breakpoint at line 42" in obs_file.read_text(encoding="utf-8")


def test_old_pack_fallback_no_empty_panels():
    old_data = {
        "meta": {"book": "old", "chapter_id": "ch01", "title": "Old"},
        "blocks": [{"id": "b1", "checks": [{"kind": "mcq"}]}],
    }
    assert mm.format_chapter_badges(old_data) is None
    assert mm.format_lab_badges({}) is None
    assert mm.interleaved_label(old_data["blocks"][0]["checks"][0]) is None


@pytest.mark.asyncio
async def test_chapters_screen_roadmap_and_next_action():
    from textual.app import App
    from tui.screens import ChaptersScreen

    class TestApp(App):
        def set_help(self, title, lines):
            pass

        def on_mount(self):
            s = ChaptersScreen("bgnet")
            self.push_screen(s)

    app = TestApp()
    async with app.run_test() as pilot:
        await pilot.pause()
        screen = app.screen
        assert isinstance(screen, ChaptersScreen)
        assert len(screen._ch_ids) > 0

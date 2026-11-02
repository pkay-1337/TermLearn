from typer.testing import CliRunner


def test_bare_invocation_launches_tui(monkeypatch):
    import tui.app

    calls = []
    monkeypatch.setattr(tui.app, "run", lambda book="", chapter="": calls.append((book, chapter)))
    from main import app

    result = CliRunner().invoke(app, [])

    assert result.exit_code == 0
    assert calls == [("", "")]


def test_tui_command_forwards_selection(monkeypatch):
    import tui.app

    calls = []
    monkeypatch.setattr(tui.app, "run", lambda book="", chapter="": calls.append((book, chapter)))
    from main import app

    result = CliRunner().invoke(app, ["tui", "--book", "extreme-c", "--chapter", "ch10"])

    assert result.exit_code == 0
    assert calls == [("extreme-c", "ch10")]

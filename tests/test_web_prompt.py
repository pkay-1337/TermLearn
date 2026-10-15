from pathlib import Path
import pytest
from typer.testing import CliRunner

from main import app
from lib import web_prompt

runner = CliRunner()


def test_chunk():
    text = "A" * 25000
    chunks = web_prompt.chunk(text, budget=10000, overlap=1000)
    assert len(chunks) >= 3
    assert chunks[0][:100] == "A" * 100


def test_research_excerpts():
    excerpts = web_prompt.get_research_excerpts()
    assert len(excerpts) > 500
    assert "Empirical Cognitive Research" in excerpts
    assert "Taxonomy of Brilliant.org Interactive Archetypes" in excerpts or "Taxonomy of Visual Aids" in excerpts or "Archetypes" in excerpts


def test_server_template_contains_critical_features():
    tmpl = web_prompt.get_server_template("extreme-c", "ch09")
    assert "Dedicated Local Chapter Server for extreme-c - ch09" in tmpl
    assert "mimetypes.add_type(\"application/wasm\", \".wasm\")" in tmpl
    assert "mimetypes.add_type(\"image/svg+xml\", \".svg\")" in tmpl
    assert "find_free_port" in tmpl
    assert "webbrowser.open" in tmpl
    assert "/api/compile" in tmpl


def test_build_web_prompt_success():
    prompt = web_prompt.build_web_prompt("extreme-c", "ch09")
    assert "TARGET OUTPUT DIRECTORY: web_pack/extreme-c/ch09/" in prompt
    assert "index.html" in prompt
    assert "style.css" in prompt
    assert "app.js" in prompt
    assert "server.py" in prompt
    assert "meta.json" in prompt
    assert "GENERATE_WEB.md" in prompt or "5-Stage Micro-Stepping Progression" in prompt
    assert "ASK_USER_WEB.md" in prompt or "Target Audience & Prior Knowledge" in prompt
    assert "CHAPTER ch09 OF extreme-c" in prompt


def test_build_web_prompt_missing_chapter():
    with pytest.raises(FileNotFoundError):
        web_prompt.build_web_prompt("nonexistent-book", "ch999")


def test_scaffold_chapter(tmp_path, monkeypatch):
    monkeypatch.setattr(web_prompt, "ROOT", tmp_path)
    target = web_prompt.scaffold_chapter("test-book", "ch01", title="Test Chapter")
    assert target.exists()
    assert (target / "server.py").exists()
    assert (target / "meta.json").exists()
    
    # Verify meta.json content
    import json
    meta = json.loads((target / "meta.json").read_text())
    assert meta["book"] == "test-book"
    assert meta["chapter_id"] == "ch01"
    assert meta["title"] == "Test Chapter"


def test_cli_gen_web_prompt(tmp_path):
    out_file = tmp_path / "web_prompt_out.md"
    result = runner.invoke(app, [
        "gen-web-prompt",
        "--book", "extreme-c",
        "--chapter", "ch09",
        "--out", str(out_file)
    ])
    assert result.exit_code == 0
    assert out_file.exists()
    content = out_file.read_text(encoding="utf-8")
    assert "TARGET OUTPUT DIRECTORY: web_pack/extreme-c/ch09/" in content


def test_cli_gen_prompt_target_web(tmp_path):
    out_file = tmp_path / "target_web_out.md"
    result = runner.invoke(app, [
        "gen-prompt",
        "--book", "extreme-c",
        "--chapter", "ch09",
        "--out", str(out_file),
        "--target", "web"
    ])
    assert result.exit_code == 0
    assert out_file.exists()
    content = out_file.read_text(encoding="utf-8")
    assert "TARGET OUTPUT DIRECTORY: web_pack/extreme-c/ch09/" in content

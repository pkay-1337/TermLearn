"""Export tests on synthetic pack dicts — no book. (FR-EXP-001..002)"""
from lib import export_md

DATA = {"meta": {"title": "T", "source_ref": "Ch.1"},
        "objectives": ["o1"],
        "blocks": [{"id": "b1", "title": "B1", "explain_md": "idea",
                    "example": {"lang": "c", "code": "int x;\n"}}],
        "lab": {"title": "L", "prompt_md": "do it",
                "starter_c": "int main(void){return 0;}\n",
                "tests_sh": "secret suite"}}


def test_build_markdown_sections():
    md = export_md.build_markdown(DATA)
    assert "# T" in md and "- o1" in md and "## B1" in md
    assert "```c\nint x;" in md and "Ch.1" in md


def test_hidden_tests_excluded(tmp_path):
    out = tmp_path / "n.md"
    import yaml
    from unittest.mock import patch
    with patch("lib.pack.require_chapter") as rq, \
         patch("lib.books.discover_chapters",
               return_value=[{"id": "ch01"}]):
        rq.return_value.read_text.return_value = yaml.safe_dump(DATA)
        export_md.run("b", "ch01", "md", str(out))
    text = out.read_text(encoding="utf-8")
    assert "secret suite" not in text and "do it" in text

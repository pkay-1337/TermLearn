"""Tests for modular directory-based chapter packs and caching."""
import pytest
import yaml
from pathlib import Path
from lib import pack
from lib.books import discover_chapters, _pack_has_lab

def test_modular_pack_loading_and_modes(tmp_path):
    book = "testbook"
    book_dir = tmp_path / book
    book_dir.mkdir(parents=True)
    
    # Create book.yaml
    (book_dir / "book.yaml").write_text(yaml.safe_dump({
        "book": {"slug": book, "title": "Test Book", "authors": ["Author"], "source": "s.epub"},
        "order": ["ch01"],
        "chapters": [{"id": "ch01", "title": "Chapter 1", "source_ref": "Ch1", "prereqs": []}],
    }))
    
    ch_dir = book_dir / "ch01"
    ch_dir.mkdir()
    
    # 1. meta.yaml
    (ch_dir / "meta.yaml").write_text(yaml.safe_dump({
        "meta": {
            "book": book,
            "chapter_id": "ch01",
            "title": "Modular Chapter 1",
            "source_ref": "Ch.1",
            "level": "intro",
            "prereqs": [],
        },
        "objectives": ["Understand modular packs"],
    }))
    
    # 2. study.yaml
    (ch_dir / "study.yaml").write_text(yaml.safe_dump({
        "blocks": [
            {
                "id": "b1",
                "type": "syntax",
                "title": "Syntax Block",
                "explain_md": "Markdown explanation here",
                "checks": [
                    {
                        "kind": "mcq",
                        "q": "What is modular?",
                        "choices": ["Separate files", "Monolith", "Nothing"],
                        "answer": 0,
                        "why": "Separate files allow focused reasoning.",
                    }
                ]
            }
        ]
    }))
    
    # 3. quiz.yaml
    (ch_dir / "quiz.yaml").write_text(yaml.safe_dump({
        "quiz": [
            {
                "kind": "mcq",
                "level": "core",
                "q": "Quiz Question 1",
                "choices": ["A", "B", "C"],
                "answer": 1,
                "why": "B is correct.",
            }
        ]
    }))
    
    # 4. cards.yaml
    (ch_dir / "cards.yaml").write_text(yaml.safe_dump({
        "cards": [
            {"front": "What is modular?", "back": "Split into mode files.", "concept": "modular"}
        ]
    }))
    
    # 5. labs.yaml
    (ch_dir / "labs.yaml").write_text(yaml.safe_dump({
        "labs": [
            {
                "id": "lab1",
                "title": "Test Lab",
                "instruction_md": "Do something",
                "files": [{"path": "main.c", "content": "int main() { return 0; }"}],
                "commands": {"run": "echo ok", "test": "echo test"},
            }
        ]
    }))
    
    # 6. test.yaml
    (ch_dir / "test.yaml").write_text(yaml.safe_dump({
        "test": {
            "gates": [{"needs": ["b1"], "min_quiz": 80}]
        }
    }))
    
    # Test require_chapter resolves directory
    p = pack.require_chapter(book, "ch01", packs_root=tmp_path)
    assert p.is_dir()
    assert p == ch_dir
    
    # Test load_chapter merges all mode files
    full = pack.load_chapter(book, "ch01", packs_root=tmp_path)
    assert full["meta"]["title"] == "Modular Chapter 1"
    assert len(full["objectives"]) == 1
    assert len(full["blocks"]) == 1
    assert len(full["quiz"]) == 1
    assert len(full["cards"]) == 1
    assert len(full["labs"]) == 1
    assert "gates" in full["test"]
    
    # Test selective mode loading
    meta_only = pack.load_chapter_mode(book, "ch01", "meta", packs_root=tmp_path)
    assert "meta" in meta_only
    assert "blocks" not in meta_only
    assert "quiz" not in meta_only
    
    cards_only = pack.load_chapter_mode(book, "ch01", "cards", packs_root=tmp_path)
    assert "cards" in cards_only
    assert "blocks" not in cards_only
    
    quiz_only = pack.load_chapter_mode(book, "ch01", "quiz", packs_root=tmp_path)
    assert "quiz" in quiz_only
    
    lab_only = pack.load_chapter_mode(book, "ch01", "lab", packs_root=tmp_path)
    assert "labs" in lab_only
    
    # Test books.py discovery and lab detection
    assert _pack_has_lab(book, "ch01", packs_root=tmp_path) is True
    chaps = discover_chapters(book, packs_root=tmp_path)
    assert len(chaps) == 1
    assert chaps[0]["has_pack"] is True
    assert chaps[0]["has_lab"] is True
    assert chaps[0]["title"] == "Modular Chapter 1"
    
    # Test validation on modular pack
    ok = pack.validate_book(book, "ch01", strict=False, packs_root=tmp_path)
    assert ok is True


def test_split_chapter_to_modular(tmp_path):
    book = "splittest"
    book_dir = tmp_path / book
    book_dir.mkdir(parents=True)
    
    # Create monolithic ch01.yaml
    mono_content = {
        "meta": {
            "book": book,
            "chapter_id": "ch01",
            "title": "Split Test Chapter",
            "source_ref": "Ch.1",
            "level": "intro",
            "prereqs": [],
        },
        "objectives": ["Test splitting"],
        "blocks": [
            {
                "id": "b1",
                "type": "syntax",
                "title": "Syntax 1",
                "explain_md": "Explain 1",
                "checks": [
                    {"kind": "mcq", "q": "Q?", "choices": ["A", "B"], "answer": 0, "why": "A is correct"}
                ]
            }
        ],
        "quiz": [
            {"kind": "mcq", "level": "core", "q": "Q quiz?", "choices": ["A", "B"], "answer": 0, "why": "A"}
        ],
        "cards": [
            {"front": "Card F", "back": "Card B", "concept": "c1"}
        ],
        "labs": [
            {
                "id": "lab1",
                "title": "Lab 1",
                "instruction_md": "Do lab",
                "files": [{"path": "code.c", "content": "/* stub */"}],
                "commands": {"run": "echo 1"},
            }
        ],
        "test": {
            "gates": [{"needs": ["b1"], "min_quiz": 80}]
        }
    }
    
    mono_file = book_dir / "ch01.yaml"
    mono_file.write_text(yaml.safe_dump(mono_content))
    
    # Run split
    dest_dir = pack.split_chapter_to_modular(book, "ch01", backup=True, packs_root=tmp_path)
    assert dest_dir.is_dir()
    assert (book_dir / "ch01.yaml.bak").is_file()
    assert not (book_dir / "ch01.yaml").exists()
    
    # Check all modular files exist
    assert (dest_dir / "meta.yaml").is_file()
    assert (dest_dir / "study.yaml").is_file()
    assert (dest_dir / "quiz.yaml").is_file()
    assert (dest_dir / "labs.yaml").is_file()
    assert (dest_dir / "cards.yaml").is_file()
    assert (dest_dir / "test.yaml").is_file()
    
    # Test loading the split pack
    loaded = pack.load_chapter(book, "ch01", packs_root=tmp_path)
    assert loaded["meta"]["title"] == "Split Test Chapter"
    assert len(loaded["blocks"]) == 1
    assert len(loaded["quiz"]) == 1
    assert len(loaded["cards"]) == 1
    assert len(loaded["labs"]) == 1


def test_ai_prompt_bundle_generation(tmp_path):
    from lib import ai_prompt
    book = "extreme-c"
    chapter = "ch10"
    
    # Test mode-specific prompt generation
    quiz_prompt = ai_prompt.build_prompt(book, chapter, mode="quiz")
    assert "TARGET OUTPUT FILE: packs/extreme-c/ch10/quiz.yaml" in quiz_prompt
    assert "30 to 50 dedicated" in quiz_prompt
    assert "books/extreme-c/raw_chapters/ch10.txt" in quiz_prompt
    # Mode files contain only their specific directives — no GENERATE.md/ASK_USER/SRS duplication.
    assert "[SOURCE ASSET LOCATIONS — WHERE TO FIND CHAPTER DATA]" not in quiz_prompt
    assert "FR-PACK-001" not in quiz_prompt
    assert "def chunk" not in quiz_prompt

    study_prompt = ai_prompt.build_prompt(book, chapter, mode="study")
    assert "TARGET OUTPUT FILE: packs/extreme-c/ch10/study.yaml" in study_prompt
    assert "single-concept blocks" in study_prompt
    assert "books/extreme-c/raw_chapters/ch10.txt" in study_prompt
    assert "FR-PACK-001" not in study_prompt

    # Test bundle emission
    out_dir = tmp_path / "prompts_bundle"
    res = ai_prompt.emit_prompt_bundle(book, chapter, dest_dir=out_dir)
    assert res == out_dir
    assert (out_dir / "01_meta.md").is_file()
    assert (out_dir / "02_study.md").is_file()
    assert (out_dir / "03_quiz.md").is_file()
    assert (out_dir / "04_labs.md").is_file()
    assert (out_dir / "05_cards.md").is_file()
    assert (out_dir / "06_test.md").is_file()
    assert (out_dir / "master_prompt.md").is_file()
    assert (out_dir / "README.md").is_file()

    readme_text = (out_dir / "README.md").read_text(encoding="utf-8")
    assert "books/extreme-c/raw_chapters/ch10.txt" in readme_text
    master_text = (out_dir / "master_prompt.md").read_text(encoding="utf-8")
    # Master prompt holds all common normative content (non-redundant across mode files).
    assert "books/extreme-c/raw_chapters/ch10.txt" in master_text
    assert "[SOURCE ASSET LOCATIONS — WHERE TO FIND CHAPTER DATA]" in master_text
    assert "FR-PACK-001" in master_text
    # Chapter text is bundled as a single copy, not embedded in each prompt file.
    assert (out_dir / "chapter.txt").is_file()
    assert "## part 1/" not in master_text
    assert "## part 1/" not in (out_dir / "03_quiz.md").read_text(encoding="utf-8")



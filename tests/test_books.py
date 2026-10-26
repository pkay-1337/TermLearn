"""Book discovery tests — pack coverage incl. modular packs. (SRS FR-BOOK-002)"""
import pytest

from lib import books


@pytest.fixture
def fake_root(tmp_path, monkeypatch):
    (tmp_path / "books" / "demo").mkdir(parents=True)
    (tmp_path / "books" / "demo" / "source.epub").write_text("")
    (tmp_path / "packs" / "demo").mkdir(parents=True)
    (tmp_path / "packs" / "demo" / "ch01.yaml").write_text("meta: {}\n")
    (tmp_path / "packs" / "demo" / "ch02").mkdir()
    (tmp_path / "packs" / "demo" / "ch02" / "study.yaml").write_text("meta: {}\n")
    (tmp_path / "packs" / "demo" / "ch03").mkdir()  # empty dir: no YAML yet
    (tmp_path / "packs" / "demo" / "runner").mkdir()  # not a chapter id
    (tmp_path / "packs" / "demo" / "gen_notes.md").write_text("")
    (tmp_path / "packs" / "demo" / "ch99.yaml.bak").write_text("")
    monkeypatch.setattr(books, "ROOT", tmp_path)
    return tmp_path


def test_pack_coverage_counts_modular_dirs(fake_root):
    rows = {r["slug"]: r for r in books.discover_books()}
    assert rows["demo"]["pack_chapters"] == 2


def test_pack_coverage_packs_only_book(fake_root):
    (fake_root / "packs" / "packonly" / "ch07").mkdir(parents=True)
    (fake_root / "packs" / "packonly" / "ch07" / "cards.yaml").write_text("cards: []\n")
    rows = {r["slug"]: r for r in books.discover_books()}
    assert rows["packonly"]["pack_chapters"] == 1
    assert rows["packonly"]["n_chapters"] == 0

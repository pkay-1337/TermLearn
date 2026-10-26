"""Extractor metadata normalization. (SRS FR-EXT-001)"""
from lib.epub_extract import _tidy


def test_tidy_drops_empty_parentheticals():
    assert _tidy("Extreme C (for \u200b \u200b)") == "Extreme C"
    assert _tidy("Book ()") == "Book"
    assert _tidy("Book (by )") == "Book"
    assert _tidy("Book (for)") == "Book"


def test_tidy_keeps_real_parentheticals():
    assert _tidy("Learning (for Dummies)") == "Learning (for Dummies)"
    assert _tidy("C (2nd edition)") == "C (2nd edition)"
    assert _tidy("C (2019)") == "C (2019)"


def test_tidy_collapse_and_strip():
    assert _tidy("  A\u200bB   C  ") == "AB C"

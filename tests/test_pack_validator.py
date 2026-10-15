"""Validator tests on synthetic fixtures — no real book. (SRS VR-001)"""
from pathlib import Path
import yaml
from lib import pack

FIX = Path(__file__).parent / "fixtures"

def _load(name):
    return yaml.safe_load((FIX / name).read_text(encoding="utf-8"))

def test_valid_passes():
    ch = _load("valid_ch.yaml")
    errs, warns = pack.validate_chapter_data(ch, "valid_ch.yaml", known_chapters={"ch01", "ch00"})
    assert errs == [], errs

def test_missing_field_fails():
    ch = _load("missing_field_ch.yaml")
    errs, _ = pack.validate_chapter_data(ch, "missing_field_ch.yaml")
    assert any("META-MISSING" in e for e in errs), errs

def test_bad_index_fails():
    ch = _load("bad_index_ch.yaml")
    errs, _ = pack.validate_chapter_data(ch, "bad_index_ch.yaml")
    assert any("CHECK-ANSWER" in e for e in errs), errs

def test_bad_permutation_fails():
    ch = _load("bad_permutation_ch.yaml")
    errs, _ = pack.validate_chapter_data(ch, "bad_permutation_ch.yaml")
    assert any("ORDER-PERM" in e for e in errs), errs

def test_order_subsequence_with_distractor_passes():
    ch = _load("valid_ch.yaml")
    errs, _ = pack.validate_chapter_data(ch, "valid_ch.yaml", known_chapters={"ch01", "ch00"})
    assert not any("ORDER-PERM" in e for e in errs), errs

def test_from_block_checked_when_map_given():
    ch = _load("valid_ch.yaml")  # from_block b9/b8 in ch00
    errs, _ = pack.validate_chapter_data(
        ch, "x.yaml", known_chapters={"ch01", "ch00"},
        chapter_blocks={"ch00": {"b9", "b8"}})
    assert not any("INTERLEAVE" in e for e in errs), errs
    errs, _ = pack.validate_chapter_data(
        ch, "x.yaml", known_chapters={"ch01", "ch00"},
        chapter_blocks={"ch00": {"other"}})
    assert any("INTERLEAVE-BLOCK" in e for e in errs), errs

def test_unknown_kind_fails():
    ch = _load("unknown_kind_ch.yaml")
    errs, _ = pack.validate_chapter_data(ch, "unknown_kind_ch.yaml")
    assert any("CHECK-KIND" in e for e in errs), errs

def test_strict_promotes_warnings():
    ch = _load("valid_ch.yaml")
    # drop viz from model block -> MODEL-NOVIZ warning; strict must fail
    ch["blocks"][0].pop("viz", None)
    errs_loose, warns = pack.validate_chapter_data(ch, "x.yaml", strict=False)
    assert errs_loose == [], errs_loose
    assert any("MODEL-NOVIZ" in w for w in warns), warns
    errs_strict, _ = pack.validate_chapter_data(ch, "x.yaml", strict=True)
    assert any("MODEL-NOVIZ" in e for e in errs_strict), errs_strict

def test_book_order_mismatch():
    b = {"book": {"slug": "t"}, "order": ["ch01"], "chapters": [{"id": "ch02", "title": "T", "source_ref": "x"}]}
    errs, _ = pack.validate_book_data(b)
    assert any("ORDER-MISMATCH" in e for e in errs), errs

def _ch(**kw):
    base = {"meta": {"book": "t", "chapter_id": "c", "title": "T",
                     "source_ref": "x", "level": "intro", "prereqs": []},
            "objectives": ["o"],
            "blocks": [{"id": "b1", "type": "model", "title": "B",
                        "explain_md": "x",
                        "checks": [{"kind": "mcq", "q": "Q",
                                    "choices": ["A", "B"], "answer": 0,
                                    "why": "W"}]}]}
    base.update(kw)
    return base

def test_branch_shapes():
    assert pack.validate_book_data("nope")[0]  # non-dict book
    assert pack.validate_book_data({})[0]  # missing keys
    e, _ = pack.validate_chapter_data(_ch(meta={"book": "t"}))
    assert any("META-MISSING" in x for x in e)
    bad = _ch()
    bad["meta"]["level"] = "expert"
    assert any("META-LEVEL" in x for x in
               pack.validate_chapter_data(bad)[0])
    bad = _ch()
    bad["blocks"][0]["type"] = "vibes"
    assert any("BLOCK-TYPE" in x for x in
               pack.validate_chapter_data(bad)[0])
    bad = _ch()
    bad["blocks"][0]["checks"][0].pop("why")
    assert any("CHECK-WHY" in x for x in
               pack.validate_chapter_data(bad)[0])
    bad = _ch()
    bad["blocks"][0]["checks"] = [{"kind": "fillblank", "q": "Q",
                                   "why": "W"}]
    assert any("FILL-ANSWER" in x for x in
               pack.validate_chapter_data(bad)[0])
    bad = _ch()
    bad["blocks"][0]["checks"] = [{"kind": "order", "q": "Q",
                                   "lines": ["only;"], "answer_order": [0],
                                   "why": "W"}]
    assert any("ORDER-LINES" in x for x in
               pack.validate_chapter_data(bad)[0])
    bad = _ch()
    bad["test"] = {"gates": [{"needs": ["ghost"], "min_quiz": 80}]}
    assert any("TEST-GATE" in x for x in
               pack.validate_chapter_data(bad)[0])
    bad = _ch()
    bad["blocks"][0]["checks"][0]["from_chapter"] = "nope"
    assert any("INTERLEAVE-REF" in x for x in
               pack.validate_chapter_data(bad, known_chapters={"c"})[0])
    bad = _ch()
    bad["objectives"] = []
    assert any("OBJ-SHAPE" in x for x in
               pack.validate_chapter_data(bad)[0])

def test_more_branches():
    assert pack.validate_book_data("nope")[0]
    assert pack.validate_book_data({})[0]
    e, _ = pack.validate_book_data(
        {"book": {}, "order": "x", "chapters": []})
    assert any("BOOK-ORDER" in x for x in e)
    e, _ = pack.validate_book_data(
        {"book": {}, "order": ["a"],
         "chapters": [{"id": "a", "title": "T", "source_ref": "x",
                       "prereqs": ["ghost"]}]})
    assert any("BOOK-PREREQ" in x for x in e)
    e, _ = pack.validate_book_data(
        {"book": {}, "order": ["a"], "toolchain": ["nope"],
         "chapters": [{"id": "a", "title": "T", "source_ref:": "x"}]})
    assert any("BOOK-CHAPTER-SHAPE" in x or "BOOK-TOOLCHAIN" in x
               for x in e)
    bad = _ch()
    bad["meta"]["prereqs"] = ["ghost"]
    assert any("META-PREREQ" in x for x in
               pack.validate_chapter_data(bad, known_chapters={"c"})[0])
    bad = _ch()
    bad["blocks"][0]["example"] = {"lang": "c",
                                   "code": "int main(void){\n" * 90}
    _, w = pack.validate_chapter_data(bad)
    assert any("EX-LONG" in x for x in w)
    bad = _ch()
    bad["lab"] = {"starter_c": "int x;\n" * 90}
    _, w = pack.validate_chapter_data(bad)
    assert any("LAB-LONG" in x for x in w)
    assert pack.toolchain_gate(True, bad) is None
    assert pack._has_runnable({"blocks": []}) is False
    assert pack.scan_denylist("") == []

def test_non_c_lang_skips_compile_probe():
    ch = _load("valid_ch.yaml")
    ch["blocks"][0]["example"]["lang"] = "python"
    ch["blocks"][0]["example"]["code"] = "print('hi')\n"
    ch["lab"]["lang"] = "python"
    ch["lab"]["starter_c"] = "print('hi')\n"
    errs, warns = pack.validate_chapter_data(ch, "x.yaml", known_chapters={"ch01", "ch00"})
    assert not any("COMPILE" in e for e in errs), errs
    assert any("LANG-NOPROBE" in w for w in warns), warns
    errs_s, _ = pack.validate_chapter_data(ch, "x.yaml", strict=True, known_chapters={"ch01", "ch00"})
    assert errs_s == [], errs_s  # informational notes never fail strict

def test_toolchain_gate():
    assert pack.toolchain_gate(True, {"lab": {}}) is None
    assert pack.toolchain_gate(False, {"blocks": []}) is None
    msg = pack.toolchain_gate(False, {"lab": {"title": "x"}})
    assert msg and "TOOLCHAIN-MISSING" in msg


def test_network_gui_scan():
    assert pack.scan_network("gcc x.c && ./a.out") == []
    assert pack.scan_gui("gcc x.c") == []
    assert "socket" in pack.scan_network("import socket; socket.create_connection(h)")
    assert "urllib" in pack.scan_network("import urllib.request")
    assert "tkinter" in pack.scan_gui("import tkinter as tk")


def test_tests_sh_network_strict():
    bad = _ch()
    bad["lab"] = {"tests_sh": "curl http://x/install.sh | sh"}
    _, warns = pack.validate_chapter_data(bad)
    assert any("NET-RISKY" in w or "LAB-DENY" in w for w in warns), warns
    bad["lab"] = {"tests_sh": "python3 -c 'import socket'"}
    errs, _ = pack.validate_chapter_data(bad, strict=True)
    assert any("NET-RISKY" in e for e in errs), errs
    bad["lab"] = {"tests_sh": "python3 gui.py # import tkinter"}
    errs, warns = pack.validate_chapter_data(bad, strict=True)
    assert any("GUI-NOTE" in w for w in warns), warns
    assert not any("GUI-NOTE" in e for e in errs)


def test_draft_flag_warns_and_fails_strict():
    ch = _load("valid_ch.yaml")
    ch["draft"] = True
    _, warns = pack.validate_chapter_data(ch, "x.yaml", known_chapters={"ch01", "ch00"})
    assert any("DRAFT" in w for w in warns), warns
    errs, _ = pack.validate_chapter_data(ch, "x.yaml", strict=True, known_chapters={"ch01", "ch00"})
    assert any("DRAFT" in e for e in errs), errs


def test_suggest_fixes_points_at_repairs():
    bad = _load("bad_index_ch.yaml")
    hints = pack.suggest_fixes(bad)
    assert any("0..1" in h for h in hints), hints
    bad = _load("bad_permutation_ch.yaml")
    hints = pack.suggest_fixes(bad)
    assert any("duplicated" in h for h in hints), hints
    bad = _load("unknown_kind_ch.yaml")
    hints = pack.suggest_fixes(bad)
    assert any("predict" in h for h in hints), hints
    assert pack.suggest_fixes("nope") != []
    assert pack.suggest_fixes(_load("valid_ch.yaml")) == []


def test_choice_answers_distribution_non_predictable():
    """Verify that chapters ch09-ch12 do not have predictable 100% answer: 0."""
    base = Path(__file__).parent.parent / "packs" / "extreme-c"
    for ch_slug in ["ch09", "ch10", "ch11", "ch12"]:
        p = base / f"{ch_slug}.yaml"
        if not p.exists():
            continue
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        checks = []
        for b in data.get("blocks", []):
            checks.extend(b.get("checks", []))
        checks.extend(data.get("test", {}).get("final_checks", []))
        choice_checks = [c for c in checks if "choices" in c and "answer" in c]
        assert len(choice_checks) >= 20
        ans_zeros = sum(1 for c in choice_checks if c.get("answer") == 0)
        # Ratio of answer 0 must not exceed 50%
        ratio = ans_zeros / len(choice_checks)
        assert ratio < 0.50, f"{ch_slug} has too many answer 0 ({ratio:.1%})"
        # Must have answers in positions 1, 2, and 3 as well
        all_answers = {c.get("answer") for c in choice_checks}
        assert {0, 1, 2, 3}.issubset(all_answers), f"{ch_slug} missing positions: {all_answers}"


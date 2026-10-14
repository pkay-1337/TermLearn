import pytest
from textual.app import App, ComposeResult
from textual.widgets import Input, Label, Static

from lib import lab, pack
from tui.widgets import ChoiceCard, QuestionWidget, SubgoalCodeView, ToolchainInspectModal


def test_trace_check_validation():
    valid_trace = {
        "kind": "trace",
        "q": "Trace pointer state",
        "code": "int a = 10; int *p = &a; *p = 20;",
        "trace": {
            "headers": ["Step", "Variable", "Address", "Value"],
            "rows": [
                {"step": 1, "line": 1, "cells": ["1", "a", "0x10", "10"]},
                {"step": 2, "line": 2, "cells": ["2", "p", "0x20", "0x10"]},
                {"step": 3, "line": 3, "cells": ["3", "*p", "0x10", "20"]}
            ]
        },
        "target": {"row": 2, "col": 3},
        "answer_text": "20",
        "why": "p dereferences address of a and updates its value"
    }
    block = {
        "id": "b1", "type": "model", "title": "Pointer Tracing",
        "explain_md": "Trace pointers step by step in memory.",
        "checks": [valid_trace]
    }
    ch = {
        "meta": {"book": "tbook", "chapter_id": "ch01", "title": "T", "source_ref": "1", "level": "intro", "prereqs": []},
        "objectives": ["trace pointers"],
        "blocks": [block]
    }
    errs, _ = pack.validate_chapter_data(ch, "ch01.yaml")
    assert not any("TRACE" in e for e in errs), errs

    # Test TRACE-SHAPE error: missing headers
    bad_ch = {
        "meta": {"book": "tbook", "chapter_id": "ch01", "title": "T", "source_ref": "1", "level": "intro", "prereqs": []},
        "objectives": ["trace pointers"],
        "blocks": [{
            "id": "b1", "type": "model", "title": "T", "explain_md": "...",
            "checks": [{
                "kind": "trace", "q": "q", "why": "w", "answer_text": "1",
                "trace": {"headers": ["Step"], "rows": []},
                "target": {"row": 0, "col": 0}
            }]
        }]
    }
    errs, _ = pack.validate_chapter_data(bad_ch, "ch01.yaml")
    assert any("TRACE-SHAPE" in e for e in errs), errs

    # Test TRACE-TARGET error: out of bounds
    bad_target = {
        "meta": {"book": "tbook", "chapter_id": "ch01", "title": "T", "source_ref": "1", "level": "intro", "prereqs": []},
        "objectives": ["trace pointers"],
        "blocks": [{
            "id": "b1", "type": "model", "title": "T", "explain_md": "...",
            "checks": [{
                "kind": "trace", "q": "q", "why": "w", "answer_text": "1",
                "trace": {
                    "headers": ["Step", "Val"],
                    "rows": [{"step": 1, "line": 1, "cells": ["1", "10"]}]
                },
                "target": {"row": 5, "col": 10}
            }]
        }]
    }
    errs, _ = pack.validate_chapter_data(bad_target, "ch01.yaml")
    assert any("TRACE-TARGET" in e for e in errs), errs


def test_faded_parsons_validation():
    valid_faded = {
        "kind": "order",
        "faded": True,
        "q": "Order and fill",
        "lines": ["car_t* c = malloc(_____);", "if (!c) return NULL;", "return c;"],
        "answer_order": [0, 1, 2],
        "blanks": [
            {"line_idx": 0, "answer_text": "sizeof(car_t)", "accepted": ["sizeof(*c)"]}
        ],
        "why": "malloc must take struct size"
    }
    ch = {
        "meta": {"book": "tbook", "chapter_id": "ch01", "title": "T", "source_ref": "1", "level": "intro", "prereqs": []},
        "objectives": ["faded ordering"],
        "blocks": [{
            "id": "b1", "type": "syntax", "title": "T", "explain_md": "...",
            "checks": [valid_faded]
        }]
    }
    errs, _ = pack.validate_chapter_data(ch, "ch01.yaml")
    assert not any("FADED" in e for e in errs), errs

    # Test FADED-BLANK error: empty blanks
    bad_faded = {
        "meta": {"book": "tbook", "chapter_id": "ch01", "title": "T", "source_ref": "1", "level": "intro", "prereqs": []},
        "objectives": ["faded ordering"],
        "blocks": [{
            "id": "b1", "type": "syntax", "title": "T", "explain_md": "...",
            "checks": [{
                "kind": "order", "faded": True, "q": "q", "why": "w",
                "lines": ["a", "b"], "answer_order": [0, 1],
                "blanks": []
            }]
        }]
    }
    errs, _ = pack.validate_chapter_data(bad_faded, "ch01.yaml")
    assert any("FADED-BLANK" in e for e in errs), errs


def test_spot_bug_validation():
    valid_bug = {
        "kind": "spot-bug",
        "q": "Spot the bug in sanitizer report",
        "code": "int *p = NULL;\n*p = 10;",
        "diagnostic_log": "AddressSanitizer: SEGV on unknown address 0x0",
        "choices": ["Line 1: allocation", "Line 2: null pointer dereference"],
        "answer": 1,
        "why": "p is NULL so *p dereferences 0"
    }
    ch = {
        "meta": {"book": "tbook", "chapter_id": "ch01", "title": "T", "source_ref": "1", "level": "intro", "prereqs": []},
        "objectives": ["debug bugs"],
        "blocks": [{
            "id": "b1", "type": "syntax", "title": "T", "explain_md": "...",
            "checks": [valid_bug]
        }]
    }
    errs, _ = pack.validate_chapter_data(ch, "ch01.yaml")
    assert not any("BUG" in e for e in errs), errs

    # Test BUG-CODE and BUG-LOG errors
    bad_bug = {
        "meta": {"book": "tbook", "chapter_id": "ch01", "title": "T", "source_ref": "1", "level": "intro", "prereqs": []},
        "objectives": ["debug bugs"],
        "blocks": [{
            "id": "b1", "type": "syntax", "title": "T", "explain_md": "...",
            "checks": [{
                "kind": "spot-bug", "q": "q", "why": "w",
                "code": "", "diagnostic_log": "",
                "choices": ["a", "b"], "answer": 0
            }]
        }]
    }
    errs, _ = pack.validate_chapter_data(bad_bug, "ch01.yaml")
    assert any("BUG-CODE" in e for e in errs) and any("BUG-LOG" in e for e in errs), errs


def test_subgoals_validation():
    valid_sg = {
        "lang": "c",
        "code": "int a = 1;\nint b = 2;\nreturn a + b;",
        "subgoals": [
            {"label": "Init", "lines": [1, 2]},
            {"label": "Return sum", "lines": [3]}
        ]
    }
    ch = {
        "meta": {"book": "tbook", "chapter_id": "ch01", "title": "T", "source_ref": "1", "level": "intro", "prereqs": []},
        "objectives": ["subgoals"],
        "blocks": [{
            "id": "b1", "type": "design", "title": "T", "explain_md": "...",
            "example": valid_sg,
            "checks": [{"kind": "mcq", "q": "q", "choices": ["a", "b"], "answer": 0, "why": "w"}]
        }]
    }
    errs, _ = pack.validate_chapter_data(ch, "ch01.yaml")
    assert not any("SUBGOAL" in e for e in errs), errs

    # Test SUBGOAL-SPAN error: line out of bounds
    bad_sg = {
        "lang": "c",
        "code": "int a = 1;",
        "subgoals": [{"label": "Invalid", "lines": [10]}]
    }
    ch["blocks"][0]["example"] = bad_sg
    errs, _ = pack.validate_chapter_data(ch, "ch01.yaml")
    assert any("SUBGOAL-SPAN" in e for e in errs), errs


def test_runner_verbs_and_c_inspector(tmp_path):
    # Test C inspector
    if lab.gcc_available():
        res_sym = lab.inspect_c("int my_exported_fn(int x) { return x * 2; }", mode="symbols")
        assert res_sym["ok"] is True
        assert "my_exported_fn" in res_sym["content"]

        res_dis = lab.inspect_c("int my_fn(void) { return 42; }", mode="disasm")
        assert res_dis["ok"] is True
        assert res_dis["format"] == "asm"
        assert "my_fn" in res_dis["content"]

        res_sec = lab.inspect_c("int x = 10;", mode="sections")
        assert res_sec["ok"] is True
        assert ".text" in res_sec["content"] or ".data" in res_sec["content"]

    # Test high-level inspect_code fallback
    res = lab.inspect_code(None, "def foo(): pass", lang="python", mode="symbols")
    assert res["ok"] is False  # No runner for Python


class QuestionHostApp(App):
    def __init__(self, check_data, on_done_cb):
        super().__init__()
        self.check_data = check_data
        self.on_done_cb = on_done_cb

    def compose(self) -> ComposeResult:
        yield QuestionWidget(self.check_data, self.on_done_cb)


async def test_tui_trace_check_interaction():
    done_results = []
    trace_check = {
        "kind": "trace",
        "q": "Trace state",
        "trace": {
            "headers": ["Step", "Var", "Val"],
            "rows": [
                {"step": 1, "cells": ["1", "a", "10"]},
                {"step": 2, "cells": ["2", "a", "25"]}
            ]
        },
        "target": {"row": 1, "col": 2},
        "answer_text": "25",
        "why": "a updated to 25"
    }

    app = QuestionHostApp(trace_check, lambda ok: done_results.append(ok))
    async with app.run_test() as pilot:
        qw = app.query_one(QuestionWidget)
        # Verify trace view exists
        tv = qw.query_one("#trace-table-view", Static)

        # Step forward to step 2 (which reveals target cell)
        await pilot.click("#btn-trace-next")
        assert qw._trace_step == 2
        assert "???" in str(tv.render())

        # Step back
        await pilot.click("#btn-trace-prev")
        assert qw._trace_step == 1

        # Submit answer
        inp = qw.query_one("#trace-in", Input)
        inp.value = "25"
        inp.focus()
        await pilot.press("enter")
        await pilot.pause()

        assert done_results == [True]


async def test_tui_spot_bug_interaction():
    done_results = []
    bug_check = {
        "kind": "spot-bug",
        "q": "Which line causes heap-use-after-free?",
        "code": "free(p);\n*p = 5;",
        "diagnostic_log": "ERROR: AddressSanitizer: heap-use-after-free",
        "choices": ["Line 1: freed too early", "Line 2: writing to freed pointer"],
        "answer": 1,
        "why": "p was freed on line 1"
    }

    app = QuestionHostApp(bug_check, lambda ok: done_results.append(ok))
    async with app.run_test() as pilot:
        # Check diagnostic box renders
        qw = app.query_one(QuestionWidget)
        diag = qw.query_one(".bug-diag-box", Static)
        assert "AddressSanitizer" in str(diag.render())

        # Select choice 2 (index 1)
        card = qw.query_one("#opt-2", ChoiceCard)
        await pilot.click(card)
        await pilot.pause()

        assert done_results == [True]


async def test_tui_faded_parsons_interaction():
    done_results = []
    faded_check = {
        "kind": "order",
        "faded": True,
        "q": "Order and fill",
        "lines": ["int x = _____;", "return x;"],
        "answer_order": [0, 1],
        "blanks": [
            {"line_idx": 0, "answer_text": "42"}
        ],
        "why": "sets x to 42 and returns it"
    }

    app = QuestionHostApp(faded_check, lambda ok: done_results.append(ok))
    async with app.run_test() as pilot:
        qw = app.query_one(QuestionWidget)
        # Enter line order
        order_in = qw.query_one("#order-in", Input)
        order_in.value = "1 2"

        # Enter blank
        blank_in = qw.query_one("#faded-blank-0", Input)
        blank_in.value = "42"

        # Submit
        await pilot.click("#btn-submit-faded")
        await pilot.pause()

        assert done_results == [True]


async def test_tui_subgoal_and_inspect_modal():
    class ModalHostApp(App):
        def compose(self) -> ComposeResult:
            yield SubgoalCodeView("int a = 10;\nreturn a;", "c", [{"label": "Init", "lines": [1]}])

    app = ModalHostApp()
    async with app.run_test() as pilot:
        lbl = app.query_one(Label)
        assert "Subgoal: Init" in str(lbl.render())

        # Open inspect modal
        modal = ToolchainInspectModal(None, "int test(void) { return 0; }", "c")
        app.push_screen(modal)
        await pilot.pause()

        # Switch tabs
        await pilot.press("2")  # Disassembly mode
        await pilot.pause()

        # Close modal
        await pilot.press("escape")
        await pilot.pause()
        assert not isinstance(app.screen, ToolchainInspectModal)

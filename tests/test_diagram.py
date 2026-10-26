"""Pure ASCII diagram renderer tests. (SPEC-EXPL-003, VR-EXPL-004, FR-DIAG-003)"""
import re

from lib.diagram import MAX_COLS, SHAPES, render


def _linear():
    return {"kind": "flow",
            "nodes": [{"id": "A", "label": "read"},
                      {"id": "B", "label": "compute"},
                      {"id": "C", "label": "write"}],
            "edges": [{"from": "A", "to": "B"}, {"from": "B", "to": "C", "label": "ok"}]}


def test_linear_flow_draws_boxes_and_arrows():
    [art] = render(_linear())
    assert "read" in art and "compute" in art and "write" in art
    assert "▼" in art or "▶" in art
    lines = art.splitlines()
    assert len(lines) >= 3 * 3  # three stacked node boxes


def test_step_reveal_sequence():
    d = _linear()
    d["steps"] = [{"focus": ["A"], "note": "start"},
                  {"focus": ["A", "B"]},
                  {"focus": ["A", "B", "C"]}]
    arts = render(d)
    assert len(arts) == 3
    assert "compute" not in arts[0]
    assert "compute" in arts[1] and "write" not in arts[1]
    assert "write" in arts[2]
    assert arts[0].endswith("note: start")


def test_art_kind_verbatim():
    [art] = render({"kind": "art", "art": "  A ──▶ B\n"})
    assert art == "  A ──▶ B"


def test_all_shapes_render_within_width():
    d = {"kind": "flow",
         "nodes": [{"id": s, "label": "x" * 8, "shape": s} for s in SHAPES],
         "edges": [{"from": "box", "to": "round"},
                   {"from": "round", "to": "decision"},
                   {"from": "decision", "to": "io"}]}
    [art] = render(d)
    assert max(len(l) for l in art.splitlines()) <= MAX_COLS


def test_wide_graph_falls_back_to_edge_list():
    d = {"kind": "flow",
         "nodes": [{"id": "root", "label": "root"}]
                  + [{"id": f"n{i:02d}", "label": "node" * 8} for i in range(11)],
         "edges": [{"from": "root", "to": f"n{i:02d}"} for i in range(11)]}
    [art] = render(d)
    assert max(len(l) for l in art.splitlines()) <= MAX_COLS
    assert "──▶" in art


def test_cyclic_graph_terminates_and_renders():
    d = {"kind": "flow",
         "nodes": [{"id": "A", "label": "loop-a"},
                   {"id": "B", "label": "loop-b"}],
         "edges": [{"from": "A", "to": "B"}, {"from": "B", "to": "A"}]}
    [art] = render(d)
    assert art  # renders something, no infinite loop
    assert max(len(l) for l in art.splitlines()) <= MAX_COLS


def test_deterministic():
    assert render(_linear()) == render(_linear())
    d = dict(_linear())
    d["steps"] = [{"focus": ["A", "B"]}]
    assert render(d) == render(d)


def test_empty_and_malformed_do_not_raise():
    # degenerate input yields [] — callers treat it as "no diagram" (FR-DIAG-003)
    assert render({}) == []
    assert render({"kind": "flow"}) == []
    assert render({"kind": "flow", "nodes": [], "edges": []}) == []
    assert render(None) == []


def _n(i, lab):
    return {"id": i, "label": lab}


def test_heavy_boxes_with_exact_centres():
    [art] = render(_linear())
    assert "┏" in art and "┗" in art and "┃" in art  # heavy family
    for line in art.splitlines():                   # stems never punch walls
        assert "┏▼" not in line and "▼┓" not in line


def test_fork_bar_junctions_and_center_entries():
    d = {"kind": "flow",
         "nodes": [_n("S", "source"), _n("L", "left"), _n("R", "right")],
         "edges": [{"from": "S", "to": "L", "label": "a"},
                   {"from": "S", "to": "R", "label": "b"}]}
    [art] = render(d)
    assert "┴" in art or "├" in art                 # fork junction on the bar
    assert art.count("▼") == 2                      # one head per target
    assert "a" in art and "b" in art                # edge labels survive


def test_join_bar_into_single_target():
    d = {"kind": "flow",
         "nodes": [_n("A", "app-1"), _n("B", "app-2"), _n("D", "db")],
         "edges": [{"from": "A", "to": "D", "label": "w1"},
                   {"from": "B", "to": "D", "label": "w2"}]}
    [art] = render(d)
    assert "┬" in art and "└" in art and "┘" in art  # join funnel
    assert art.count("▼") == 1                       # single entry into db


def test_back_edge_wraps_through_side_channel():
    d = {"kind": "flow",
         "nodes": [_n("A", "loop-a"), _n("B", "loop-b")],
         "edges": [{"from": "A", "to": "B"}, {"from": "B", "to": "A", "label": "again"}]}
    [art] = render(d)
    assert "──▶" not in art                          # routed, not a footnote
    assert "▶" in art and "└" in art and "┌" in art  # channel wrap corners
    lines = art.splitlines()
    chan = [i for i, l in enumerate(lines) if l[1:2] == "│"]
    assert len(chan) >= 2 and len({lines[i][1] for i in chan}) == 1


def test_back_edge_label_rides_exit_run_with_one_margin():
    # demo-approved: the exit run may carry the label with a single free
    # cell on each side (the approved art showed `└──hit──┃`)
    d = {"kind": "flow",
         "nodes": [_n("A", "aaaaaaaaaa"), _n("B", "bbb"), _n("C", "ccc")],
         "edges": [{"from": "A", "to": "B"}, {"from": "B", "to": "C"},
                   {"from": "C", "to": "A", "label": "ok"}]}
    [art] = render(d)
    m = re.search(r"└─+ok─+┃", art)
    assert m, "label should ride the exit run with 1-cell margins: " + art


def test_z_path_and_pass_through_crossing():
    d = {"kind": "flow",
         "nodes": [_n("a", "a"), _n("b", "b"), _n("c", "c"), _n("d", "d")],
         "edges": [{"from": "a", "to": "c"}, {"from": "a", "to": "d"},
                   {"from": "b", "to": "d"}]}
    [art] = render(d)
    assert "┼" in art          # b's stem crosses a's fork bar
    assert art.count("▼") == 3  # c, d (x2 spread entries)
    assert max(len(l) for l in art.splitlines()) <= MAX_COLS


def test_multilevel_jump_falls_back_to_footnote():
    d = {"kind": "flow",
         "nodes": [_n("A", "one"), _n("B", "two"), _n("C", "three")],
         "edges": [{"from": "A", "to": "B"}, {"from": "B", "to": "C"},
                   {"from": "A", "to": "C", "label": "skip"}]}
    [art] = render(d)
    assert "one ──▶ three [skip]" in art  # skipped-level edge becomes a footnote

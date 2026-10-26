"""ASCII diagram renderer for pack `diagram:` stanzas. (SPEC-EXPL-003, FR-DIAG-001..003)

Pure functions only: no Rich, no RNG, no wall-clock, no I/O (NFR-MAIN-001,
CR-EXPL-004). `render(diagram)` returns one string per reveal `steps[]`
entry (a single string when the diagram has no steps) and MUST NOT raise
on schema-valid input (NFR-REL-001) — layout trouble falls back to a plain
edge-list rendering. Deterministic: identical input -> byte-identical output.

Visual language (user-approved 2026-10-26): heavy boxes `┏━┓ ┃ ┗━┛`, total
widths even so every box has an exact centre column; edges leave and enter
box middles; a single inbound arrow enters the top-centre, several inbounds
spread symmetrically along the top edge; heads touch their destination
(`▼` just above a top edge, `▶/◀` against a side wall); stems are thin `│`
of any length; corner glyphs follow connected directions (`└`=up+right,
`┘`=up+left, `┌`=down+right, `┐`=down+left); forks and joins are T-junctions
(`┴`/`├` bar out of a source, `┬` funnel into a target, `┼` where two lines
cross); back-edges wrap around the picture through side channels. Edges the
router cannot place fall back to `──▶` footnote lines.
"""

MAX_COLS = 100
SHAPES = ("box", "round", "decision", "io")


def _label(n: dict) -> str:
    return str(n.get("label") or n.get("id") or "?").strip()


def _box_rows(label: str) -> tuple[list[str], int]:
    """Heavy three-row box; total width forced even so the centre column
    (left + width // 2) is exact."""
    w = len(label) + 4
    if w % 2:
        w += 1
    inner = w - 2
    return [f"┏{'━' * inner}┓", f"┃{label.center(inner)}┃", f"┗{'━' * inner}┛"], w


def _layers(ids: list[str], edges: list[dict]) -> list[list[str]]:
    """Kahn-style top-down layering in author order; cycle leftovers form
    the final layer (same-level edges become footnotes, so no infinite loop)."""
    indeg = {i: 0 for i in ids}
    for e in edges:
        f, t = str(e.get("from")), str(e.get("to"))
        if f in indeg and t in indeg and f != t:
            indeg[t] += 1
    levels: list[list[str]] = []
    placed: set[str] = set()
    frontier = [i for i in ids if indeg[i] == 0]
    while len(placed) < len(ids):
        if not frontier:
            # cycle: deterministically break it at the first unplaced id
            frontier = [next(i for i in ids if i not in placed)]
        levels.append(frontier)
        placed |= set(frontier)
        nxt: list[str] = []
        for e in edges:
            f, t = str(e.get("from")), str(e.get("to"))
            if f in placed and t in indeg and t not in placed:
                indeg[t] -= 1
                if indeg[t] == 0:
                    nxt.append(t)
        frontier = [i for i in ids if i not in placed and i in nxt]
    return levels


def _edge_list(ids: list[str], edges: list[dict], labels: dict[str, str]) -> list[str]:
    """Fallback: deterministic adjacency rendering, always narrow."""
    lines = []
    for e in edges:
        f, t = str(e.get("from")), str(e.get("to"))
        lab = str(e.get("label", "")).strip()
        lines.append(f"{labels.get(f, f)} ──▶ {labels.get(t, t)}" + (f" [{lab}]" if lab else ""))
    connected = {str(e.get("from")) for e in edges} | {str(e.get("to")) for e in edges}
    for i in ids:
        if i not in connected:
            lines.append(f"{labels.get(i, i)} (isolated)")
    return lines or [labels.get(i, i) for i in ids]


def _foot(labels: dict[str, str], f: str, t: str, lab: str) -> str:
    return f"{labels.get(f, f)} ──▶ {labels.get(t, t)}" + (f" [{lab}]" if lab else "")


def _junc(up: bool, down: bool, left: bool, right: bool) -> str:
    """Glyph for a junction cell from its connected directions."""
    if up and down and left and right:
        return "┼"
    if up and down:
        return "├" if right else ("┤" if left else "│")
    if up:
        return "┴" if left and right else ("└" if right else ("┘" if left else "│"))
    if down:
        return "┬" if left and right else ("┌" if right else ("┐" if left else "│"))
    return "─" if left and right else "│"


class _Cv:
    """Fixed-size character canvas with merge-aware line writing."""

    def __init__(self, n_rows: int):
        self.rows: list[str] = [""] * n_rows

    def cell(self, r: int, c: int) -> str:
        if 0 <= r < len(self.rows) and 0 <= c < len(self.rows[r]):
            return self.rows[r][c]
        return " "

    def free(self, r: int, c0: int, c1: int) -> bool:
        return all(self.cell(r, c) == " " for c in range(c0, c1 + 1))

    def put(self, r: int, c: int, s: str, force: bool = True) -> None:
        if r < 0 or r >= len(self.rows) or c < 0:
            return
        row = self.rows[r]
        if c > len(row):
            row += " " * (c - len(row))
        seg = list(row)
        end = c + len(s)
        if end > len(seg):
            seg.extend(" " * (end - len(seg)))
        for j, ch in enumerate(s):
            if force or seg[c + j] == " ":
                seg[c + j] = ch
        self.rows[r] = "".join(seg)

    def vstem(self, r: int, c: int) -> None:
        """One vertical stem cell; merges with a horizontal dash into ┼ and
        never destroys junction/corner glyphs."""
        cur = self.cell(r, c)
        if cur == "─":
            self.put(r, c, "┼")
        elif cur in " │":
            self.put(r, c, "│")

    def hrun(self, r: int, c0: int, c1: int, lab: str = "",
             slack: int = 4) -> bool:
        """Horizontal dash run, merging with vertical stems; label rides the
        middle only when every cell under it is a plain dash. True when the
        label was placed. slack = free cells demanded around the label
        (2 = one margin per side, for channel exit runs per the demo)."""
        if c1 < c0:
            return False
        for c in range(c0, c1 + 1):
            cur = self.cell(r, c)
            if cur == "│":
                self.put(r, c, "┼")     # crossing stem
            elif cur in " ─┼":
                self.put(r, c, "─" if cur != "┼" else "┼")
            # anything else (junctions, corners, labels) is left untouched
        span = c1 - c0 + 1
        if lab and len(lab) <= span - slack:
            mid = c0 + (span - len(lab)) // 2
            if all(self.cell(r, c) == "─" for c in range(mid, mid + len(lab))):
                self.put(r, mid, lab)
                return True
        return False

    def art(self) -> str:
        return "\n".join(r.rstrip() for r in self.rows)


def _beside(cv: _Cv, row: int, col: int, lab: str) -> bool:
    """Label next to a head: right side first, then left; only into free cells."""
    if not lab:
        return False
    n = len(lab)
    if cv.free(row, col + 2, col + 1 + n):
        cv.put(row, col + 2, lab, force=False)
        return True
    if col - 2 - n >= 0 and cv.free(row, col - 1 - n, col - 2):
        cv.put(row, col - 1 - n, lab, force=False)
        return True
    return False


def _flow_art(nodes: list[dict], edges: list[dict], vis: set[str] | None) -> str:
    """Top-down layered ASCII in the user-approved visual language. Falls
    back to the plain edge list on any layout trouble or width overflow."""
    try:
        ids = [str(n.get("id")) for n in nodes]
        labels = {str(n.get("id")): _label(n) for n in nodes}
        vnodes = [n for n in nodes if vis is None or str(n.get("id")) in vis]
        vedges = [e for e in edges
                  if str(e.get("from")) in ids and str(e.get("to")) in ids
                  and (vis is None or (str(e.get("from")) in vis and str(e.get("to")) in vis))]
        if not vnodes:
            return ""
        vids = [str(n.get("id")) for n in vnodes]
        levels = _layers(vids, vedges)

        widths: dict[str, int] = {}
        for nid in vids:
            widths[nid] = _box_rows(labels[nid])[1]
        pos: dict[str, int] = {}
        for li, layer in enumerate(levels):
            if li == 0:
                x = 4
            else:  # centre this layer under the previous one
                prev = levels[li - 1]
                plo = min(pos[n] for n in prev)
                phi = max(pos[n] + widths[n] - 1 for n in prev)
                total = sum(widths[n] for n in layer) + 4 * (len(layer) - 1)
                x = max(4, (plo + phi + 1) // 2 - total // 2)
            for nid in layer:
                pos[nid] = x
                x += widths[nid] + 4
        max_right = max(pos[n] + widths[n] - 1 for n in vids)
        center = {nid: pos[nid] + widths[nid] // 2 for nid in vids}
        lv_of = {nid: li for li, layer in enumerate(levels) for nid in layer}

        # ---- classify edges -------------------------------------------------
        fwd: dict[int, list[tuple[str, str, str]]] = {}
        back: list[tuple[int, int, str, str, str]] = []
        foot: list[str] = []
        for e in vedges:
            f, t = str(e.get("from")), str(e.get("to"))
            lab = str(e.get("label", "")).strip()
            lf, lt = lv_of.get(f), lv_of.get(t)
            if lf is None or lt is None or f == t:
                foot.append(_foot(labels, f, t, lab))
            elif lt == lf + 1:
                fwd.setdefault(lf, []).append((f, t, lab))
            elif lt < lf:
                back.append((lf, lt, f, t, lab))
            else:
                foot.append(_foot(labels, f, t, lab))
        back.sort(key=lambda b: (b[0], pos[b[2]], pos[b[3]], b[4]))

        # ---- per-pair plans --------------------------------------------------
        plans: dict[int, dict] = {}
        for lf in sorted(fwd):
            es = fwd[lf]
            lab_of: dict[tuple[str, str], str] = {}
            out_by_src: dict[str, list[str]] = {}
            in_by_tgt: dict[str, list[str]] = {}
            for f, t, lab in es:
                lab_of.setdefault((f, t), lab)
                out_by_src.setdefault(f, []).append(t)
                in_by_tgt.setdefault(t, []).append(f)
            fork_set = {f for f, outs in out_by_src.items() if len(outs) > 1}
            join_tgts = {t for t, srcs in in_by_tgt.items()
                         if len(srcs) >= 2 and all(s not in fork_set for s in srcs)}
            entry: dict[tuple[str, str], int] = {}
            g0c = {center[f] for f, _t, _l in es}
            for t, srcs in in_by_tgt.items():
                wl, wr = pos[t] + 1, pos[t] + widths[t] - 2
                if t in join_tgts or len(srcs) == 1:
                    for s in srcs:
                        col = center[t] if t in join_tgts \
                            else _avoid(center[t], g0c - {center[s]}, wl, wr)
                        entry[(s, t)] = col
                    continue
                # several separate inbounds: anti-correlated spread (outermost
                # source gets the innermost entry) — fewer line crossings
                order = sorted(srcs, key=lambda s: -center[s])
                used: set[int] = set()
                for i, s in enumerate(order):
                    off = (2 * i - (len(order) - 1)) * 2
                    col = min(max(center[t] + off, wl), wr)
                    while col in used and col < wr:
                        col += 1
                    col = _avoid(col, g0c - {center[s]}, wl, wr)
                    used.add(col)
                    entry[(s, t)] = col
            bars: list[dict] = []
            for f in sorted(fork_set, key=lambda s: center[s]):
                cols = [(entry[(f, t)], t, lab_of[(f, t)]) for t in out_by_src[f]]
                jc = center[f]
                bars.append({"kind": "fork", "key": f, "jc": jc, "cols": cols,
                             "lo": min([jc] + [c for c, _, _ in cols]),
                             "hi": max([jc] + [c for c, _, _ in cols])})
            for t in sorted(join_tgts, key=lambda s: center[s]):
                jc = center[t]
                srcs = sorted(((center[s], s, lab_of[(s, t)]) for s in in_by_tgt[t]),
                              key=lambda v: v[0])
                bars.append({"kind": "join", "key": t, "jc": jc, "srcs": srcs,
                             "lo": min([jc] + [c for c, _, _ in srcs]),
                             "hi": max([jc] + [c for c, _, _ in srcs])})
            placed_b: list[tuple[int, int, int]] = []
            for b in sorted(bars, key=lambda b: (b["lo"], b["hi"], b["jc"], b["kind"], b["key"])):
                off = 0
                while any(o == off and b["lo"] <= h and l <= b["hi"] for o, l, h in placed_b):
                    off += 1
                b["off"] = off
                placed_b.append((off, b["lo"], b["hi"]))
            drops = [{"src": f, "t": t, "lab": lab_of[(f, t)], "xc": center[f],
                      "entry": entry[(f, t)]}
                     for f, outs in out_by_src.items() if f not in fork_set
                     for t in outs if t not in join_tgts]
            seen_d: set[tuple[int, int]] = set()
            for d in drops:
                k = (d["xc"], d["entry"])
                if k in seen_d:
                    foot.append(_foot(labels, d["src"], d["t"], d["lab"]))
                    d["skip"] = True
                seen_d.add(k)
            zc = sum(1 for d in drops if not d.get("skip") and d["xc"] != d["entry"])
            bar_offs = {b["off"] for b in bars}
            gap = max([2] + [o + 3 for o in bar_offs])
            while zc and sum(1 for r in range(1, gap - 1) if r not in bar_offs) < zc:
                gap += 1
            plans[lf] = {"bars": bars, "drops": drops, "gap": gap}

        # ---- canvas + boxes --------------------------------------------------
        starts = [0]
        for li in range(len(levels) - 1):
            starts.append(starts[-1] + 3 + plans.get(li, {"gap": 2})["gap"])
        cv = _Cv(starts[-1] + 3)
        for li, layer in enumerate(levels):
            for nid in layer:
                br, _w = _box_rows(labels[nid])
                for i, row in enumerate(br):
                    cv.put(starts[li] + i, pos[nid], row)

        # ---- phase 1: stems (verticals first so bars merge into ┼) -----------
        for lf, plan in plans.items():
            g0 = starts[lf] + 3
            g_last = starts[lf] + 2 + plan["gap"]
            for b in plan["bars"]:
                jrow = g0 + b["off"]
                jc = b["jc"]
                if b["kind"] == "fork":
                    if jrow > g0:
                        for r in range(g0, jrow):
                            cv.vstem(r, jc)
                    for col, _t, _l in b["cols"]:
                        for r in range(jrow + 1, g_last):
                            cv.vstem(r, col)
                else:
                    for c, _s, _l in b["srcs"]:
                        for r in range(g0, jrow):
                            cv.vstem(r, c)
                    for r in range(jrow + 1, g_last):
                        cv.vstem(r, jc)
            bar_rows = {g0 + b["off"] for b in plan["bars"]}
            taken: dict[int, list[tuple[int, int]]] = {}
            for d in plan["drops"]:
                if d.get("skip"):
                    continue
                if d["xc"] != d["entry"]:
                    lo, hi = min(d["xc"], d["entry"]), max(d["xc"], d["entry"])
                    r_run = next((r for r in range(g0 + 1, g_last) if r not in bar_rows
                                  and all(not (lo <= h and l <= hi)
                                          for l, h in taken.get(r, []))), None)
                    if r_run is None:
                        foot.append(_foot(labels, d["src"], d["t"], d["lab"]))
                        d["skip"] = True
                        continue
                    taken.setdefault(r_run, []).append((lo, hi))
                    d["r_run"] = r_run
                    for r in range(g0, r_run):
                        cv.vstem(r, d["xc"])
                    cv.put(r_run, d["xc"], "└" if d["entry"] > d["xc"] else "┘")
                    cv.hrun(r_run, lo + 1, hi - 1)
                    cv.put(r_run, d["entry"], "┐" if d["entry"] > d["xc"] else "┌")
                    for r in range(r_run + 1, g_last):
                        cv.vstem(r, d["entry"])
                else:
                    for r in range(g0, g_last):
                        cv.vstem(r, d["xc"])

        # ---- phase 2: bars (junctions, corners, merge-aware dashes) ----------
        for lf, plan in plans.items():
            g0 = starts[lf] + 3
            for b in plan["bars"]:
                jrow = g0 + b["off"]
                jc = b["jc"]
                others = [c for c, _, _ in (b["cols"] if b["kind"] == "fork"
                                            else b["srcs"])]
                if b["kind"] == "fork":
                    cv.put(jrow, jc, _junc(True, jc in others,
                                           jc > b["lo"], jc < b["hi"]))
                    for c in sorted(set(others)):
                        if c != jc:
                            # bar may continue past a corner -> ┬ mid-bar
                            cv.put(jrow, c, _junc(False, True, c > b["lo"], c < b["hi"]))
                else:
                    cv.put(jrow, jc, _junc(jc in others, True,
                                           jc > b["lo"], jc < b["hi"]))
                    for c in sorted(set(others)):
                        if c != jc:
                            # source stem may pass a mid-bar join corner -> ┴
                            cv.put(jrow, c, _junc(True, False, c > b["lo"], c < b["hi"]))
                specials = sorted({jc, *others})
                for a, z in zip(specials, specials[1:]):
                    if z - a > 1:
                        cv.hrun(jrow, a + 1, z - 1)

        # ---- phase 3: heads ---------------------------------------------------
        for lf, plan in plans.items():
            g_last = starts[lf] + 2 + plan["gap"]
            for b in plan["bars"]:
                cols = ({c for c, _, _ in b["cols"]} if b["kind"] == "fork"
                        else {b["jc"]})
                for c in cols:
                    cv.put(g_last, c, "▼")
            for d in plan["drops"]:
                if not d.get("skip"):
                    cv.put(g_last, d["entry"], "▼")

        # ---- phase 4: labels --------------------------------------------------
        for lf, plan in plans.items():
            g0 = starts[lf] + 3
            g_last = starts[lf] + 2 + plan["gap"]
            for b in plan["bars"]:
                ridden = False  # at most one label per bar line (user rule)
                if b["kind"] == "fork":
                    jc = b["jc"]
                    for col, _t, lab in b["cols"]:
                        seg = ((col + 1, jc - 1) if col < jc
                               else (jc + 1, col - 1) if col > jc
                               else (b["lo"], b["hi"]))
                        if (lab and not ridden
                                and seg[1] - seg[0] + 1 >= len(lab) + 4
                                and cv.hrun(g0 + b["off"], seg[0], seg[1],
                                            lab)):
                            ridden = True
                        else:
                            _beside(cv, g_last, col, lab)
                else:
                    jc = b["jc"]
                    for c, _s, lab in b["srcs"]:
                        seg = (min(c, jc) + 1, max(c, jc) - 1) if c != jc else \
                              (b["lo"], b["hi"])
                        if (lab and not ridden
                                and seg[1] - seg[0] + 1 >= len(lab) + 4
                                and cv.hrun(g0 + b["off"], seg[0], seg[1],
                                            lab)):
                            ridden = True
                        else:
                            _beside(cv, g_last, jc, lab)
            for d in plan["drops"]:
                if d.get("skip"):
                    continue
                if d["xc"] == d["entry"]:
                    _beside(cv, g_last, d["entry"], d["lab"])
                else:
                    lo, hi = min(d["xc"], d["entry"]), max(d["xc"], d["entry"])
                    if not (d["lab"] and hi - lo - 1 >= len(d["lab"]) + 4
                            and cv.hrun(d["r_run"], lo + 1, hi - 1, d["lab"])):
                        _beside(cv, g_last, d["entry"], d["lab"])

        # ---- back-edges: side-channel wraps -----------------------------------
        used_ch: set[int] = set()
        for lf, lt, f, t, lab in back:
            mid_f, mid_t = starts[lf] + 1, starts[lt] + 1
            wl_f, wr_f = pos[f], pos[f] + widths[f] - 1
            wl_t, wr_t = pos[t], pos[t] + widths[t] - 1
            cands = [("L", 1), ("R", max_right + 2), ("L", 0),
                     ("R", max_right + 3), ("R", max_right + 4)]
            done = False
            for side, ch in cands:
                if ch in used_ch:
                    continue
                if side == "L":
                    exit_ok = (wl_f - 1 >= ch + 1
                               and cv.free(mid_f, ch + 1, wl_f - 1))
                    ent_ok = (wl_t - 1 >= ch + 1
                              and cv.free(mid_t, ch + 1, wl_t - 1))
                    vert_ok = all(cv.cell(r, ch) == " "
                                  for r in range(mid_t, mid_f + 1))
                    head_c, exit_j, ent_j, head_g = wl_t - 1, "└", "┌", "▶"
                else:
                    exit_ok = (ch - 1 >= wr_f + 1
                               and cv.free(mid_f, wr_f + 1, ch - 1))
                    ent_ok = (ch - 1 >= wr_t + 1
                              and cv.free(mid_t, wr_t + 1, ch - 1))
                    vert_ok = all(cv.cell(r, ch) == " "
                                  for r in range(mid_t, mid_f + 1))
                    head_c, exit_j, ent_j, head_g = wr_t + 1, "┘", "┐", "◀"
                if not (exit_ok and ent_ok and vert_ok):
                    continue
                rode = cv.hrun(mid_f, *([ch + 1, wl_f - 1] if side == "L"
                                        else [wr_f + 1, ch - 1]), lab,
                               slack=2)
                cv.put(mid_f, ch, exit_j)
                for r in range(mid_t + 1, mid_f):
                    cv.put(r, ch, "│")
                cv.put(mid_t, ch, ent_j)
                if side == "L":
                    cv.hrun(mid_t, ch + 1, wl_t - 2)
                else:
                    cv.hrun(mid_t, wr_t + 1, ch - 1)
                cv.put(mid_t, head_c, head_g)
                if lab and not rode:
                    n = len(lab)
                    for r in range(mid_t + 1, mid_f):
                        sp = (ch + 2, ch + 1 + n) if side == "L" else (ch - 1 - n, ch - 2)
                        if sp[0] >= 0 and cv.free(r, *sp):
                            cv.put(r, sp[0], lab, force=False)
                            break
                    else:
                        # demo-approved fallback: clip the label into the
                        # longest free run beside the channel vertical
                        for r in range(mid_t + 1, mid_f):
                            k = 0
                            if side == "L":
                                while (k < n
                                       and cv.cell(r, ch + 2 + k) == " "):
                                    k += 1
                            else:
                                while (k < n
                                       and cv.cell(r, ch - 2 - k) == " "):
                                    k += 1
                            if k < 3:
                                continue
                            clip = (lab.split()[0] if " " in lab
                                    and len(lab.split()[0]) <= k else lab[:k])
                            st = ch + 2 if side == "L" else ch - 1 - k
                            cv.put(r, st, clip, force=False)
                            break
                used_ch.add(ch)
                done = True
                break
            if not done:
                foot.append(_foot(labels, f, t, lab))

        art = cv.art()
        if foot:
            art += "\n" + "\n".join(foot)
        if max((len(r) for r in art.splitlines()), default=0) > MAX_COLS:
            return "\n".join(_edge_list(ids, vedges, labels))
        return art
    except Exception:
        return "\n".join(_edge_list([str(n.get("id")) for n in nodes], edges, labels))


def _wrap(prefix: str, text: str, width: int = 98) -> str:
    """Greedy word wrap: first line starts with `prefix`, continuation lines
    hang indented so prose notes never break the 100-column bound."""
    hang = " " * (len(prefix) + 1)
    budget = width - len(prefix) - 1
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = f"{cur} {w}" if cur else w
        if cur and len(trial) > budget:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return "\n".join(f"{prefix} {lines[0]}" if not i else hang + l
                     for i, l in enumerate(lines))


def _avoid(col: int, g0c: set[int], wl: int, wr: int) -> int:
    """Nudge an entry column away from other edges' first-gap-row stems so no
    two verticals belonging to different edges sit 1 col apart on a row."""
    for _ in range(6):
        near = [c for c in g0c if abs(c - col) <= 1]
        if not near:
            return col
        step = -2 if min(near, key=lambda c: abs(c - col)) > col else 2
        if not wl <= col + step <= wr:
            step = -step
        if not wl <= col + step <= wr:
            return col
        col += step
    return col


def _delim(art: str) -> str:
    """End-of-diagram delimiter: heavy rule matching the art's widest line
    (capped at MAX_COLS), separating the picture from what follows."""
    w = min(max((len(r) for r in art.splitlines()), default=0), MAX_COLS)
    return "━" * max(w, 3)


def render(diagram: dict) -> list[str]:
    """Public entry: diagram dict -> list of step strings (FR-DIAG-003).

    Degenerate/blank input yields [] so callers treat it as "no diagram".
    """
    d = diagram or {}
    kind = str(d.get("kind", "flow")).lower()
    if kind == "art":
        art = str(d.get("art", ""))
        return [art.rstrip("\n")] if art.strip() else []
    nodes = [n for n in (d.get("nodes") or []) if isinstance(n, dict)]
    edges = [e for e in (d.get("edges") or []) if isinstance(e, dict)]
    steps = [s for s in (d.get("steps") or []) if isinstance(s, dict)]
    out = []
    for st in steps or [None]:
        vis = {str(x) for x in ((st or {}).get("focus") or [])}
        art = _flow_art(nodes, edges, vis or None)
        note = str((st or {}).get("note", "")).strip() if st else ""
        if note:
            art += "\n" + _wrap("note:", note)
        out.append(art.strip("\n"))
    res = [s for s in out if s.strip()]
    if res:
        res[-1] += "\n\n" + _delim(res[-1])
    return res

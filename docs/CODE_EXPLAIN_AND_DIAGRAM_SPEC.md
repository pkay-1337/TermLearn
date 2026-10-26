# Lab Tab Refresh, Code Explain & Diagram Specification
**Document ID:** SPEC-EXPL-003
**Target Subsystems:** `tui/practice.py`, `tui/screens.py`, `tui/widgets.py`, `lib/study.py`, `lib/revise.py`, `lib/export_md.py`, `lib/pack.py`, `lib/diagram.py` (new), `lib/ai_prompt.py`, `prompts/GENERATE.md`, `docs/SRS.md`
**Status:** APPROVED — implemented 2026-10-26
**Applies to:** `termlearn` v0.9.0+
**Standards & Baselines:** RFC 2119, IEEE Std 29148-2018, `docs/SRS.md` (§4.6–§4.8, §5.1–§5.2, §5.8, §9), `docs/INTERACTIVE_LEARNING_SPEC.md` (SPEC-PED-001)
**Date:** October 2026

---

## 0. Scope

This spec covers three changes to be implemented together:

| ID | Change | Type |
|----|--------|------|
| F0 | Lab file-tab bar does not refresh when switching labs (`p`/`n`) | Bug fix |
| F1 | Authored explanation rendered immediately after each code example | Feature |
| F2 | Optional `diagram:` block stanza (flowcharts / ASCII diagrams) | Feature |

None of these changes move normative paths (`FR-TREE-001`); `lib/diagram.py` is an additional module under `lib/`, which SRS §2.5 permits ("Additional modules MAY be added under `lib/`").

---

## 1. F0 — Bug: stale file-tab labels on lab switch (LAB-TAB)

### 1.1 Observed defect
On the TUI Lab screen, pressing `n` (next lab) or `p` (previous lab) updates the title, badge, instructions, and editor content, but the file-tab bar (`#lab-file-tabs`) keeps showing the **previous lab's file names**.

### 1.2 Root cause (inspection)
`tui/practice.py`:
- `LabScreen.compose()` (line ~955) builds one `Button` per entry of `self.files` **once at mount**.
- `action_next_lab`/`action_prev_lab` → `_rebuild_screen()` (line ~1001) calls `_setup_workspace()`, which correctly refreshes `self.files` for the new lab, then calls `_update_tab_buttons()` (line ~993), which only updates the **variant** of buttons `#tab-file-{idx}` — labels are never touched, surplus buttons persist, and missing buttons are silently skipped (bare `except Exception`).

### 1.3 Requirement

`LAB-TAB-001`: The lab file-tab bar **MUST** render exactly the current lab's workspace files (union of declared `files[].path` and on-disk workspace files, unique, order-preserving) after every lab switch, reset, and remount. Stale labels from another lab **MUST NOT** be shown.

`LAB-TAB-002`: The fix **MUST** be a single rebuild point: `_rebuild_screen()` **SHALL** rebuild the children of `#lab-file-tabs` from `self.files` (deterministic order), and `_update_tab_buttons()` **SHALL** keep its current variant-highlighting role. No new keys, no behavior change to `@on(Button.Pressed, ".lab-file-tab-btn")`.

### 1.4 Verification

`VR-EXPL-001` (Method: T): Extend `tests/test_tui.py` — after pressing `n`, query `#tab-file-0` and assert its label equals lab 2's first file path; press `p` and assert the label returns to lab 1's first file. The test **MUST** be hermetic (must not depend on pre-solved workspace state; see the note recorded against `test_multi_lab_workspace_tui` during the 2b8bbae verification — that dependency is out of scope here but **SHOULD** be resolved when this VR lands, by pointing the workspace root at `tmp_path`).

---

## 2. F1 — Code explain block (CODE-EXPLAIN)

### 2.1 Educational rationale
Retrieval practice research (SRS §1.5) favors worked examples with integrated explanation (Sweller's split-attention; Renkl's self-explanation prompts). Code shown without an adjacent mechanism explanation forces learners to self-generate causal links; an authored, immediately-following explanation closes that gap and pairs naturally with existing `subgoals` chunking (SPEC-PED-001).

### 2.2 Pack schema addition (extends SRS §4.8 / FR-PACK-002)

```yaml
example:                     # as today
  lang: c
  code: "..."                # verbatim or adapted:true
  adapted: false
  run_expected: "..."
  subgoals: [...]            # unchanged (SPEC-PED-001)
  explain_md: "..."          # NEW, OPTIONAL: Markdown explanation of the code
```

`FR-EXPL-001`: `example.explain_md` **MUST** be a UTF-8 Markdown string that renders in Rich without exception (FR-PACK-004) and **MUST** explain the *shown code only* — mechanism, state changes, and idioms — using only concepts present in the block or its declared prereqs (FR-AI-002 fidelity applies). It **MUST NOT** duplicate `explain_md` prose verbatim.

`FR-EXPL-002`: The AI generation contract (`prompts/GENERATE.md`, study prompts in `lib/ai_prompt.py`) **MUST** instruct: whenever a block carries `example.code`, author `explain_md` — line-grouped, concept-first (why it works), 3–15 lines, ≤120 cols per line (FR-PACK-005 prose bound). Packs already shipped **MAY** omit it; absence is a warning, not an error.

### 2.3 Rendering contract

`FR-EXPL-003`: Wherever `example.code` is rendered, `explain_md` **MUST** render immediately **after** the code (before `viz`/`diagram`/checks), in all surfaces that show examples:
1. CLI `study` (`lib/study.py`) and CLI `revise` (`lib/revise.py`) — through the `--more` pager (`IF-CLI-005`).
2. TUI `StudyScreen` (`tui/practice.py`) — mounted directly after the `SubgoalCodeView`/`Syntax` widget; TUI `ReviseScreen` (`tui/screens.py`).
3. `export` (`lib/export_md.py`) — as a subsection under the example.
`explain_md` **MUST NOT** be treated as a check, card, or gate input.

`FR-EXPL-004`: A block without `example` **MUST NOT** render any explain section; an empty/whitespace `explain_md` **MUST** be treated as absent.

### 2.4 Validation additions (`lib/pack.py`, FR-VAL-001..002 family)

| Code | Level | Condition |
|------|-------|-----------|
| `EXPL-SHAPE` | ERR | `example.explain_md` present but not a non-empty string |
| `EXPL-RENDER` | ERR | `explain_md` crashes the Rich renderer (reuse `_rich_renders`) |
| `EXPL-MISSING` | WARN | `example.code` present without `explain_md` (SHOULD-level; informational in `--strict` — legacy packs predate the F1 contract; new packs are bound via GENERATE.md) |

### 2.5 Verification

`VR-EXPL-002` (Method: T): `tests/test_pack_validator.py` — fixture with `explain_md` present/absent/malformed asserts the three codes and non-strict vs `--strict` behavior.
`VR-EXPL-003` (Method: T): TUI pilot — a study block with code+explain renders the explain widget after the code; a codeless block renders none (FR-EXPL-004).

---

## 3. F2 — Diagram block (DIAGRAM)

### 3.1 Educational rationale
Dual coding (SRS §1.5(6); Weinstein) improves retention when verbal and visual channels co-present. `viz` (ascii-memory) covers *memory state*; it does not cover *control/data flow* — request handling, message passing (IPC framing), allocation lifecycles as decision graphs. A structured, language-agnostic flowchart stanza lets packs teach these flows stepwise in the terminal.

### 3.2 Pack schema addition (extends SRS §4.8 / FR-PACK-002)

Block-level, OPTIONAL, independent of `example` and `viz`:

```yaml
diagram:                     # NEW, OPTIONAL stanza
  kind: flow                 # REQUIRED: flow | art
  caption: "..."             # OPTIONAL one-liner
  nodes:                     # REQUIRED iff kind==flow, >=2
    - {id: A, label: "recv()", shape: io}        # shape: box|round|decision|io (default box)
    - {id: B, label: "parse header", shape: box}
    - {id: C, label: "valid?", shape: decision}
  edges:                     # REQUIRED iff kind==flow, >=1
    - {from: A, to: B}
    - {from: B, to: C, label: "ok"}              # label OPTIONAL
  steps:                     # OPTIONAL progressive reveal, >=1 when present
    - {focus: [A], note: "client sends the request"}      # focus: node ids shown so far
    - {focus: [A, B, C], note: "now the validity check"}
  art: |                     # REQUIRED iff kind==art: pre-authored ASCII art
    ┌──────┐    ┌──────┐
    │ src  │───▶│ sink │
    └──────┘    └──────┘
```

`FR-DIAG-001`: `diagram.kind` **MUST** be `flow` or `art` (unknown values fail per FR-PACK-003). `kind==flow` **MUST** carry well-formed `nodes` (unique ids, non-empty labels) and `edges` whose `from`/`to` reference existing node ids. `kind==art` **MUST** carry non-empty `art`.

`FR-DIAG-002`: Node/edge/step labels **MUST** render in Rich without exception (FR-PACK-004) and **MUST NOT** contain embedded ANSI escapes.

`FR-DIAG-003`: The renderer **MUST** be a pure function in a new `lib/diagram.py` (NFR-MAIN-001): `render(diagram: dict) -> list[str]` returning one string per `steps[]` entry (or a single-element list when absent), drawing `flow` as deterministic top-down layered ASCII in the user-approved heavy-line style: node boxes `┏━┓ ┃ ┗━┛` with even total width so edges attach at exact box centers (`▼` directly above the top edge, `▶`/`◀` against a side wall), thin `│` stems, corner glyphs chosen by connected directions (`└ ┘ ┌ ┐`), fork/join bars with T-junctions (`┴`/`├` on the source bar, `┬` on the target funnel), `┼` where a stem crosses a bar, back-edges routed through side wrap channels with the edge label beside the channel (clipped only if nothing fits, per the approved demo), and edges that cannot be placed rendered as `──▶` footnote lines; at most one ridden label per bar line, additional labels beside their arrowheads. Node `shape` remains schema vocabulary (`DIAGRAM-VOCAB`) but is decorative: every shape draws as the same heavy box. `art` renders verbatim. Output **MUST** be ≤100 columns per line after wrapping-aware layout (wider layouts fall back to a plain edge list), deterministic (no RNG, no wall-clock), and **MUST NOT** raise on any schema-valid input (NFR-REL-001).

`FR-DIAG-004`: Study traversal order per block **SHALL** be: `explain_md` → `example.code` → `example.explain_md` (F1) → `diagram` → `viz` → checks. The diagram **SHOULD** use the existing `n`/`s` step vocabulary (`IF-TUI-004` — no new keys; `n` advances a reveal step, `s` skips to the end). Stepping state **MUST NOT** persist across blocks. `revise` **MAY** render the final step only, unstepped, unscored (FR-REV-002).

`FR-DIAG-005`: `export` **MUST** include the diagram as a fenced code block (final step, plus caption); hidden-test rules (FR-EXP-002) are unaffected.

`FR-DIAG-006`: The generation contract (`prompts/GENERATE.md`, study prompts) **MUST** map `diagram.kind: flow` to `algorithm`/`design` blocks with multi-step flows, and keep memory-state teaching on `viz` (`MAP-001` unchanged). A block **MAY** carry both `diagram` and `viz`. Chapters without flow-teachable content **MUST NOT** invent diagrams (same spirit as FR-AI-006).

### 3.3 Validation additions

| Code | Level | Condition |
|------|-------|-----------|
| `DIAGRAM-SHAPE` | ERR | Missing/malformed `kind`/`nodes`/`edges`/`art`; `nodes` <2; duplicate node ids; non-list `steps` |
| `DIAGRAM-REF` | ERR | Edge endpoint or `steps[].focus` id not in `nodes` |
| `DIAGRAM-VOCAB` | ERR | Unknown `kind` or node `shape` value |
| `DIAGRAM-RENDER` | ERR | Label/art crashes Rich or contains ANSI escapes |
| `DIAGRAM-WIDE` | WARN | Rendered output exceeds 100 columns on any step |

### 3.4 Verification

`VR-EXPL-004` (Method: T): `tests/test_diagram.py` — pure renderer: linear flow with centered boxes and Z-path jogs, fork/join bars with junction glyphs and ridden labels, back-edge side-channel wrap with clipped label, pass-through `┼`, multilevel-jump footnote fallback, `art` passthrough, step sequencing, width bound with edge-list fallback, determinism (two calls byte-identical).
`VR-EXPL-005` (Method: T): validator fixtures for all five codes + strict behavior.
`VR-EXPL-006` (Method: T): TUI pilot — block with `diagram` renders after example/explain; `n` advances reveal steps; codeless flow still renders.

---

## 4. Cross-cutting constraints

1. `CR-EXPL-001`: No new dependencies (CR-DES-005). The renderer is stdlib-only text layout.
2. `CR-EXPL-002`: Packs without `explain_md`/`diagram` **MUST** validate exactly as today; both features are additive and **MUST NOT** break any existing fixture (VR-001/VR-EXPL regression).
3. `CR-EXPL-003`: TUI and CLI **MUST** consume the same pure lib functions (`IF-TUI-001`); no duplicated layout logic in `tui/`.
4. `CR-EXPL-004`: `main.py` stays routing-only (CR-DES-001).

---

## 5. SRS integration (applied at implementation)

1. §4.8 schema excerpt: add `explain_md` under `example` and the `diagram` stanza between `example` and `viz`, inside the `SCHEMA-BEGIN/END` markers.
2. §4.7 palette table: add row `diagram` — renderer `lib/diagram.py`, use when `algorithm`/`design` flows aid understanding — status **SHOULD**.
3. §9 traceability: new row `Code explain / diagram | FR-EXPL-001..004, FR-DIAG-001..006 | VR-EXPL-001..006 | lib/diagram.py, lib/pack.py, lib/study.py, lib/revise.py, lib/export_md.py, tui/*`.
4. Appendix B: add FR-EXPL-001..004, FR-DIAG-001..006, LAB-TAB-001..002, VR-EXPL-001..006, CR-EXPL-001..004.
5. Version bump SRS 0.6.0 → 0.7.0 with change note.

---

## 6. Acceptance criteria

1. Full `pytest` suite green including new VR-EXPL tests.
2. `validate --strict` passes on all shipped extreme-c packs (existing packs have neither field — only `EXPL-MISSING`-class additions must not appear for packs without code, and must not fail non-strict runs).
3. Lab switch (`n`/`p`) shows the new lab's file names in tabs (manual + VR-EXPL-001).
4. A study block with code shows explain text directly after the code in CLI and TUI.
5. A block with `diagram` steps through with `n` in CLI and TUI; `export` includes it.

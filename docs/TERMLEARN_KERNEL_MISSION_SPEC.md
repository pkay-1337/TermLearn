# Termlearn Compatibility-Preserving Mission Update Specification

**Document Identifier**: `SPEC-TERMLEARN-MISSION-2026-V1`
**Standard Compliance**: ISO/IEC/IEEE 29148:2018
**Requirements Normative Language**: RFC 2119
**Status**: Draft / Proposed Specification
**Date**: 2026-11-19
**Applies to**: current Termlearn v0.x codebase, target next minor release
**Location**: `docs/TERMLEARN_KERNEL_MISSION_SPEC.md`
**Related References**: `docs/SRS.md`, `docs/LAB_SPEC.md`, `docs/TUI_REDESIGN_SPEC.md`, `docs/INTERACTIVE_LEARNING_SPEC.md`

---

## 1. Purpose

This specification defines a backward-compatible update to Termlearn so the app supports an evidence-first, tinkering-first Linux kernel curriculum without breaking existing books, chapter packs, progress databases, validators, CLI commands, or TUI flows.

The update adds generic capabilities for provenance, lab taxonomy, experiment context, and next-action guidance. It MUST NOT turn Termlearn into a kernel-specific IDE.

## 2. Compatibility Promise

The primary constraint of this specification is compatibility:

> Existing packs MUST continue to load, validate, study, quiz, lab, test, export, and display exactly as before, with no new required fields, no migrations, and no new default warnings or errors.

This spec is a later compatibility amendment to presentation and metadata handling. It does not remove legacy support for `lab`, `labs`, `study`, `quiz`, `srs`, `parsons`, `revise`, `test`, `stats`, or `export`.

## 3. Conformance

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** are to be interpreted as described in RFC 2119.

## 4. Scope

### 4.1 In scope

1. Optional additive pack metadata for evidence, lab taxonomy, environment context, and roadmap phase/track.
2. Validator support that accepts new metadata without making it required.
3. Display-only UI enhancements that degrade cleanly when metadata is absent.
4. Tinker UX improvements: command preview, safety/environment badges, output capture, and observation notes.
5. Roadmap/next-action guidance derived from existing prereq, progress, SRS, and lab state.
6. Regression tests proving old packs are unaffected.

### 4.2 Out of scope

1. Kernel-specific TUI screens.
2. Embedded QEMU, GDB, crash, drgn, ftrace, perf, or packet-capture protocols.
3. A full source-code IDE.
4. Root automation, host network mutation, VM image mutation, or privileged setup.
5. Changes to scoring math, SRS scheduling, quiz semantics, lab pass/fail semantics, or chapter mastery gates.
6. Required migrations of YAML packs or `progress.db`.
7. Graphical/browser UI or gamification.

## 5. Compatibility Matrix

| Case | Required behavior |
|------|-------------------|
| Existing pack + new runtime | MUST behave identically to current runtime for all existing commands and screens. |
| Existing pack + strict validation | MUST produce the same exit status and no new warnings/errors. |
| New pack + new runtime | New metadata is displayed when present and ignored when absent. |
| New pack + old runtime | Core teaching content MUST still work; new metadata SHOULD be ignored without warnings. |
| Existing `progress.db` + new runtime | MUST remain readable; any new optional state MUST be lazily created and non-destructive. |
| TUI sessions | MUST NOT rewrite packs, evidence files, or source files. |

To satisfy new-pack compatibility with old runtimes, all new metadata MUST live inside already-known containers (`meta`, `blocks[]`, checks inside `blocks[]`, `labs[]`, and legacy `lab`). This specification MUST NOT introduce new top-level chapter keys, because `lib/pack.py:394-396` currently warns on unknown top-level keys and strict validation can promote warnings to failure.

## 6. Additive Metadata Model

All fields in this section are OPTIONAL. Absence MUST be treated as "metadata unavailable", not as an error.

### 6.1 Chapter metadata

Extend `meta` with optional fields:

```yaml
meta:
  book: linux-kernel
  chapter_id: T0A
  title: "First contact: compile, run, diagnose"
  source_ref: "evidence/T0A/transcript.md; E-T0A-01..E-T0A-11"
  level: intro
  prereqs: []

  track: tooling                 # OPTIONAL: book/tooling/kernel/networking/capstone
  phase: P0                      # OPTIONAL: free-form roadmap label
  evidence_bundle: "evidence/T0A"  # OPTIONAL: human-readable bundle path
  evidence:
    - id: E-T0A-05
      label: "gcc diagnostic for bad.c"
      path: "evidence/T0A/transcript.md"
      kind: command-output       # OPTIONAL: source|command-output|trace|diff|artifact
```

Rules:

- `track`, `phase`, and `evidence_bundle` MUST be strings when present.
- `evidence` MUST be a list when present.
- Each `evidence[]` item MUST have a string `id` and `label`.
- `path` MUST be a relative path string when present. It is display metadata; the app MUST NOT execute it.
- The app MUST NOT require evidence files to exist in order to study, quiz, lab, test, or export.
- `meta.source_ref` keeps its current meaning and remains REQUIRED by existing schema.

### 6.2 Block metadata

Extend each block with optional evidence references:

```yaml
blocks:
  - id: b4
    type: algorithm
    title: "Diagnostic to fix to rerun"
    explain_md: "..."
    evidence: [E-T0A-05, E-T0A-06]
    checks:
      - kind: why-fails
        q: "..."
        choices: ["...", "...", "..."]
        answer: 1
        why: "..."
        evidence: [E-T0A-05]
```

Rules:

- `blocks[].evidence` MUST be a list of strings when present.
- Check-level `evidence` MUST be a list of strings when present.
- Evidence IDs SHOULD refer to `meta.evidence[].id`, but unresolved IDs MUST NOT fail existing validation modes.
- A future opt-in strict evidence mode MAY validate ID resolution, but it MUST NOT be the default.

### 6.3 Lab metadata

Extend existing lab objects with optional pedagogical and environment metadata:

```yaml
labs:
  - id: lab1
    title: "Read a compiler diagnostic"
    instruction_md: "..."
    files: []
    commands:
      run: "sh run.sh"
      test: "sh check.sh"
      tinker: "sh"

    family: compiler-diagnostics       # OPTIONAL grouping label
    tier: core                         # OPTIONAL: core|stretch
    difficulty: intro                  # OPTIONAL: free-form
    evidence: [E-T0A-05, E-T0A-06]
    expected_observation: "The first failing line is reported before runtime."
    artifacts: ["build.log", "diff.txt"]
    environment:
      name: host-user
      boundary: host                   # host|vm|container|namespace
      privilege: user                  # user|root|vm-root
      network: none                    # none|isolated|host
      timeout_s: 30
```

Legacy single `lab` objects MAY carry the same optional fields.

Rules:

- `tier` MUST be `core` or `stretch` when present.
- Absence of `tier` MUST NOT imply `stretch`, `core`, or a changed gate.
- `environment.boundary`, `environment.privilege`, and `environment.network` are display/safety context only in v1.
- No new lab field MAY affect `commands.test`, `test_cases`, mastery gates, or progress recording in v1.
- `artifacts` MUST be a list of relative path strings when present.
- The app MUST NOT create, delete, or modify artifacts; it only displays them and may show captured tinker output in the lab workspace.

## 7. Validator Requirements

### 7.1 Default behavior

- `REQ-VAL-BC-001`: Existing validation commands and flags MUST remain unchanged.
- `REQ-VAL-BC-002`: `python main.py validate --book <slug> [--chapter <id>] [--strict]` MUST NOT emit warnings for absent optional metadata.
- `REQ-VAL-BC-003`: Existing packs MUST produce identical validation results before and after the update.
- `REQ-VAL-BC-004`: New metadata fields MUST be accepted inside known containers without generating `CH-UNKNOWN-KEY` or equivalent warnings.
- `REQ-VAL-BC-005`: If new metadata is malformed, validation SHOULD report the first concrete field error, but only for packs that contain that metadata.
- `REQ-VAL-BC-006`: Evidence path existence MUST NOT be checked by default.
- `REQ-VAL-BC-007`: The validator MUST NOT reject unresolved evidence IDs by default.
- `REQ-VAL-BC-008`: A future evidence-strict mode MUST be opt-in via a new command flag or config; it MUST NOT alter current `--strict`.

### 7.2 Validation error codes

New codes MAY be added, but only when the offending field is present:

| Code | Meaning |
|------|---------|
| `EVIDENCE-SHAPE` | `meta.evidence`, `*.evidence`, or `artifacts` has the wrong shape. |
| `EVIDENCE-ID` | An evidence item has a missing or non-string `id`/`label`. |
| `LAB-TIER` | `labs[].tier` is present but not `core` or `stretch`. |
| `LAB-ENV` | `labs[].environment` is present but not a mapping or has invalid scalar field types. |

These codes MUST NOT be emitted for old packs that omit the fields.

## 8. TUI Requirements

### 8.1 Graceful fallback

- `REQ-UI-BC-001`: Every new UI panel MUST be feature-detected from metadata presence.
- `REQ-UI-BC-002`: If metadata is absent, the UI MUST render the existing screen without placeholder warnings.
- `REQ-UI-BC-003`: Existing keybindings MUST NOT be removed or rebound.
- `REQ-UI-BC-004`: New keybindings MUST be additive and shown in contextual help.
- `REQ-UI-BC-005`: The UI MUST NOT modify pack YAML when displaying optional metadata.

### 8.2 Evidence separation (Authoring vs. Runtime)

Evidence transcripts and captures are authoring-time ground-truth artifacts located in `curriculum/linux-kernel/evidence/`. They are strictly for authoring and verifying packs.
- Evidence metadata, keys, rails, and `v` toggles are NOT part of the Termlearn runtime or pack schema.
- Termlearn runtime focuses purely on learning interactions: study blocks, quizzes, labs, cards, and test gates.

### 8.3 Lab taxonomy display

- `REQ-UI-LAB-001`: Lab lists SHOULD display badges for `tier`, `family`, `environment.name`, `environment.boundary`, `environment.privilege`, and `environment.network` when present.
- `REQ-UI-LAB-002`: A core-only filter MAY be added, but old packs without `tier` MUST remain visible in the default list.
- `REQ-UI-LAB-003`: Lab order MUST remain pack order unless a new explicit sort is selected.
- `REQ-UI-LAB-004`: Stretch labs MUST NOT be hidden by default when no core label exists anywhere in the chapter.
- `REQ-UI-LAB-005`: Lab status and mastery logic MUST remain unchanged.

### 8.4 Tinker experiment UX

The existing tinker command is the correct primitive and MUST be preserved.

- `REQ-UI-TINK-001`: Before launching tinker, the UI SHOULD show command, working directory, timeout, environment badges, and expected observation when available.
- `REQ-UI-TINK-002`: Separate-terminal launch MUST remain available and default behavior MUST NOT regress.
- `REQ-UI-TINK-003`: In-inline/fallback mode, captured stdout/stderr SHOULD remain visible in the TUI console.
- `REQ-UI-TINK-004`: After a tinker session, the learner SHOULD be able to save a short observation note into the lab workspace, for example `observations.md`.
- `REQ-UI-TINK-005`: Observation notes MUST NOT affect scoring or gate state.
- `REQ-UI-TINK-006`: Risky-looking commands MUST show labels from metadata when present; the UI MUST NOT auto-escalate privileges.
- `REQ-UI-TINK-007`: Denylist and path-safety behavior in `lib/lab_workspace.py` MUST remain enforced.

### 8.5 Roadmap and next action

- `REQ-UI-ROAD-001`: If `meta.track` or `meta.phase` is present, chapter lists SHOULD display them as badges.
- `REQ-UI-ROAD-002`: A `Next` action SHOULD be computed from existing prereqs, chapter status, SRS due count, lab state, and optional lab tier.
- `REQ-UI-ROAD-003`: When no new metadata exists, the next-action logic MUST fall back to current chapter order/progress behavior.
- `REQ-UI-ROAD-004`: The roadmap MUST be advisory; it MUST NOT lock chapters or change mode availability.

### 8.6 Interleaving display

- `REQ-UI-INTER-001`: Checks with existing `from_chapter` and `from_block` metadata SHOULD be labeled as review or interleaved practice.
- `REQ-UI-INTER-002`: No new interleaving field is required.
- `REQ-UI-INTER-003`: Interleaved labels MUST NOT change check scoring.

## 9. CLI Requirements

- `REQ-CLI-BC-001`: All current commands and flags MUST remain valid.
- `REQ-CLI-BC-002`: No command output that scripts might parse MAY change by default.
- `REQ-CLI-BC-003`: Optional evidence checking MUST be behind a new flag, not enabled by default.
- `REQ-CLI-BC-004`: `export` MAY include optional metadata when present, but old exports MUST remain byte-stable when metadata is absent.
- `REQ-CLI-BC-005`: `validate --fix-hints` MUST remain backward compatible and need not produce hints for optional metadata in v1.

## 10. Data and Persistence Requirements

- `REQ-DATA-BC-001`: No existing `progress.db` table, column, or row semantic MUST be removed or renamed.
- `REQ-DATA-BC-002`: If observation notes or evidence UI state are persisted, they MUST be stored either in lab workspace files or in additive tables/columns with safe defaults.
- `REQ-DATA-BC-003`: A fresh install and an upgraded install MUST produce equivalent learning behavior.
- `REQ-DATA-BC-004`: Deleting optional metadata MUST NOT corrupt progress.

## 11. Security and Safety Requirements

- `REQ-SEC-001`: Evidence paths and artifact paths MUST be strings; the app MUST NOT open, execute, or render them as commands.
- `REQ-SEC-002`: Display metadata MUST NOT bypass existing denylists in `lib/pack.py` or safety checks in `lib/lab_workspace.py`.
- `REQ-SEC-003`: Environment labels are advisory and MUST NOT grant privileges.
- `REQ-SEC-004`: Tinker output capture MUST stay within the lab workspace unless the user explicitly chooses another location.
- `REQ-SEC-005`: The UI MUST NOT automatically run root, network, VM, or destructive setup actions.

## 12. Implementation Plan

### Phase 0 — Lock the compatibility baseline

1. Snapshot validation output for every existing pack under `packs/`.
2. Snapshot TUI render smoke results for Home, Chapters, Menu, Study, Quiz, Cards, Lab, Stats, Revise, and Test.
3. Snapshot strict validation exit codes for all existing books.
4. Add regression fixtures that use packs with no new metadata.

### Phase 1 — Additive metadata support

1. Extend validators to accept optional nested metadata.
2. Add new validation codes only for malformed present fields.
3. Update `docs/SRS.md` §4.8 documentation without changing required fields.
4. Update generation prompts so new metadata is optional, not mandatory.

### Phase 2 — Display-only UI metadata

1. Add evidence panel with hidden-by-default behavior.
2. Add lab badges.
3. Add interleaved labels.
4. Add roadmap badges and advisory next action.

### Phase 3 — Tinker workflow improvements

1. Add command preview and environment badges.
2. Add captured-output display for fallback mode.
3. Add observation note capture.
4. Keep separate-terminal behavior intact.

### Phase 4 — Optional tooling workflows

Only after phases 0–3 pass:

1. Add lab-authored QEMU/gdb helper templates as pack files or scripts.
2. Add artifact display for `serial.log`, `gdb.txt`, trace files, and diffs.
3. Do not add native QEMU/GDB protocol handling.

## 13. Test Requirements

- `REQ-TEST-001`: All existing tests MUST pass after every phase.
- `REQ-TEST-002`: A regression test MUST load every existing pack and assert no new warnings/errors versus the Phase 0 baseline.
- `REQ-TEST-003`: A test MUST prove old packs render with new UI code without evidence panels or lab badges.
- `REQ-TEST-004`: A test MUST prove new optional metadata parses and displays when present.
- `REQ-TEST-005`: A test MUST prove malformed optional metadata errors only when the field is present.
- `REQ-TEST-006`: A Textual Pilot test MUST cover Home → Chapters → Menu → Study → Quiz → Lab → Stats with both old-style and new-style fixture packs.
- `REQ-TEST-007`: A test MUST prove TUI navigation does not rewrite pack files.
- `REQ-TEST-008`: A test MUST prove old `progress.db` files remain readable.
- `REQ-TEST-009`: `python main.py validate --book <slug> --strict` MUST pass for every existing book.
- `REQ-TEST-010`: `python -m pytest -q` MUST pass with zero new skips or xfails.

## 14. Acceptance Criteria

The update is accepted only when all of the following are true:

1. No existing pack requires edits.
2. No existing pack gains a new warning or error under default or strict validation.
3. No existing CLI command or keybinding is removed or changed.
4. Existing progress databases continue to work.
5. New metadata is optional and display-only in v1.
6. Tinker remains the experiment primitive; no embedded debugger/VM is introduced.
7. Old packs show the old UI, with no empty placeholder panels.
8. New packs show evidence, lab taxonomy, environment context, and advisory next actions when metadata exists.
9. Full regression suite passes.
10. Pack files remain byte-identical after study, quiz, lab, tinker, test, and export.

## 15. Explicit Non-Changes

This specification explicitly does **not**:

- rename `blocks`, `checks`, `labs`, `lab`, `cards`, `test`, or `quiz`;
- make `evidence`, `track`, `phase`, `family`, `tier`, or `environment` required;
- add a new top-level chapter key;
- change `meta.source_ref`;
- change `answer`, `answer_order`, `why`, `concept`, `from_chapter`, or `from_block`;
- change SRS scheduling;
- change lab pass/fail logic;
- change chapter mastery gates;
- rewrite old packs into a new format.

## 16. Rationale

The Linux kernel mission needs provenance, experiment context, and lab taxonomy, but those are presentation and authoring concerns. Termlearn can remain a generic terminal learning system if the new information is modeled as optional metadata rendered by generic UI components.

The safest design is therefore additive and nested: old packs do not notice the update; new packs gain richer UI; nothing in the core learning engine changes.

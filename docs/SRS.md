# Software Requirements Specification — termlearn
**Terminal Interactive Learning from Technical Books**

- Version: 0.6.0 (Textual TUI: tui/ package with Home/Chapters/Menu/Study/
  Quiz/Cards/Lab/Stats + ? overlay + hint-bar Footer; CLI run-loops stay
  Rich, TUI interactions are Textual-native over shared lib data/scoring/
  persistence; VR-009 pilot tests)
- Previous: 0.5.3, 0.5.2, 0.5.1, 0.5.0, 0.4.1, 0.4.0, 0.3.1, 0.3.0, 0.2.0, 0.1.0
- Date: 2026-10-13
- Standards: IEEE Std 29148-2018 (SRS structure and content), RFC 2119 (requirement levels)
- Project root: `~/Apps/termlearn/`
- Stack decision (locked): Python 3.11+, Rich CLI first → Textual TUI later; external extractor + manual AI-chat pack generation; project lives in `~/Apps/termlearn/`

---

## 0. RFC 2119 conformance and requirement language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in RFC 2119.

Conventions used in this SRS:

1. Every verifiable requirement **SHALL** have a unique identifier of the form `<PREFIX>-<NNN>` (e.g. `FR-BOOK-001`, `NFR-PERF-001`). Prefixes: `FR` = functional system requirement, `IF` = external interface requirement, `NFR` = nonfunctional / quality requirement, `VR` = verification requirement, `CR` = constraint.
2. The requirement verb determines obligation:
   - **MUST / SHALL / REQUIRED** = mandatory for conformance.
   - **SHOULD / RECOMMENDED** = strongly desired; deviation **MUST** be justified and recorded.
   - **MAY / OPTIONAL** = permitted implementation choice.
3. Each requirement **SHALL** be verifiable by at least one method in §8 (inspection, demonstration, test, analysis).
4. The word `chapter` means one author-defined major division of a source book as detected in the EPUB spine/TOC. The word `pack` means the AI-generated, machine-parsable teaching representation of one book, stored under `packs/<book-slug>/`. The word `block` means one single-concept teaching unit inside a chapter YAML.

---

## 1. Introduction (IEEE 29148 §9.5.1)

### 1.1 Purpose

This SRS specifies **termlearn**, a terminal-based system that turns EPUB technical books into specialized, interactive, learn-first courses. The system **SHALL** enable a learner to learn directly from the terminal without opening the source book, and **SHALL** also support revision, spaced-repetition, practice, and verifiable testing.

This document is the authoritative requirements baseline for design, implementation, AI pack generation, and acceptance. It **SHALL** be read together with the file tree in §2.5 and the YAML contract in §4.8.

### 1.2 Scope

In scope:

1. A single-entry application (`main.py`) with the flow: select book → select chapter → select mode (`study`, `revise`, `quiz`, `srs`, `parsons`, `lab`, `test`, `stats`, `gen-prompt`, `validate`, `export`).
2. Helper libraries in `lib/` for books, EPUB extraction, pack loading/validation, each learning mode, progress persistence, and AI-prompt emission.
3. A `books/` source area holding user-supplied EPUBs and extracted `raw_chapters/*.txt` plus `meta.json`.
4. A `packs/` area holding AI-generated, YAML-based teaching packs (`book.yaml` + `chNN.yaml` per chapter).
5. A `prompts/` area holding the normative AI instruction set (`GENERATE.md`) and the user-interrogation template (`ASK_USER.md`).
6. Offline progress and telemetry storage in SQLite.
7. Runnable-code execution under the book's declared toolchain (pilot domain:
   C books via system `gcc`; the contract is language-agnostic — C is one
   example, see FR-LAB-004 and the `toolchain` stanza in FR-PACK-001).

Out of scope for v0.3:

- A hosted web service, multi-user server, or LMS integration.
- Automatic LLM API calls from within the app (generation is manual via external AI chat).
- Non-textbook media (video, DRM-protected EPUBs, scanned-image PDFs).
- Full Textual multi-pane TUI (v0.3 **SHALL** deliver Rich CLI; Textual **SHOULD** reuse the same `lib/` and packs without pack rewrite — see `IF-TUI-001`).

### 1.3 Product overview and problem statement

Passive re-reading of technical books yields poor retention and transfer. Evidence-based strategies — retrieval practice, spacing, interleaving, elaboration, concrete examples, dual coding — plus code-specific interactions (predict-output/tracing, Parsons ordering, fix-broken, Explain-in-Plain-English, micro-labs with immediate toolchain feedback) significantly improve learning, but are absent from static EPUBs.

termlearn **SHALL** close this gap by:

1. Preserving the source book's order, examples, and terminology (fidelity).
2. Distilling each chapter into terminal-teachable concept blocks (compression, not dumping 20 pages to scroll).
3. Interleaving exposition with formative micro-checks at the point of learning (not quiz-only at the end).
4. Selecting interaction types based on chapter content (`model` vs `syntax` vs `design` vs `algorithm`), not a fixed per-chapter quota.
5. Persisting mastery, SRS due dates, and per-concept telemetry locally for adaptive review.

The system is learn-first: a compliant installation **MUST** allow a motivated novice to reach chapter objectives using only the terminal. Revision and SRS are supporting modes, not the primary path.

### 1.4 Definitions, acronyms, abbreviations

| Term | Definition |
|------|------------|
| EPUB | IDPF EPUB 2/3 publication consumed as source. |
| Block | One single-concept teaching unit (`blocks[]` in chapter YAML). A block teaches exactly one falsifiable skill. |
| Pack | `packs/<book-slug>/book.yaml` + `chNN.yaml` files constituting the teachable form of one book. |
| Study mode | Primary learn-first traversal of blocks: goal → idea → example → micro-check → remediation/variation. |
| Revise mode | Passive re-exposure: notes, key concepts, examples; no scoring. |
| SRS | Spaced-repetition system using SM-2 or equivalent; due queue across chapters. |
| Parsons | Code-ordering exercise: order scrambled lines (with optional distractors) via number keys. |
| Lab | Small editable run-and-verify task in the book's language, checked against hidden tests (pilot runner: `gcc`). |
| Test | Chapter gate: quiz threshold + lab pass required to mark mastery (skippable with explicit override). |
| Telemetry | Local, anonymous-by-design log of answers used to compute weak concepts (offline analogue of Brown Rust-book profiling). |
| AI chat | External LLM conversation (e.g. opencode/Claude/chat) where chapter YAML is produced manually and pasted back. |
| TUI | Terminal user interface (Rich CLI in v0.3, Textual later). |

### 1.5 References

1. IEEE Std 29148-2018, *Systems and software engineering — Life cycle processes — Requirements engineering*.
2. Bradner, S., RFC 2119, *Key words for use in RFCs to Indicate Requirement Levels*, 1997.
3. Crichton & Krishnamurthi, *Profiling Programming Language Learning* (OOPSLA 2024) — inline quizzes, conceptual `why` > `whether`, +20% from targeted text interventions.
4. Ericson et al., Parsons problems efficiency/effectiveness studies (ICER/Koli) — ordering ≈ writing in outcomes at ~50% time.
5. Weinstein et al. / Cepeda et al. — spacing, interleaving, retrieval practice reviews.
6. Runestone / OpenDSA interaction catalog — activecode, MCQ with feedback, fill-in-blank, Parsons, CodeLens, peer instruction.
7. EDBook (2024) — dialogic LLM learning aligned to goals.
8. Source decisions: `~/Apps/` location; CLI-first→TUI; external extractor + manual AI generation.
9. Nielsen, J., *10 Usability Heuristics* (1994; H1–H10: status visibility,
   real-world match, user control, consistency, error prevention, recognition
   over recall, accelerators, minimalism, plain-language errors, help/docs).
10. Norman / HCI discoverability literature: visibility, signifiers,
   feedback/feedforward precede learnability; feature discoverability problem
   (most users never find hidden shortcuts); KeyMap natural-mapping study
   (CHI 2020).
11. GNOME Human Interface Guidelines, Keyboard: every action keyboard-possible;
   mnemonic shortcuts; one-hand-reachable; don't overload every action.
12. ACM *Accessibility of Command Line Interfaces* (2020): CLIs perceived
   accessible but high-effort; unstructured text is the core barrier; provide
   linear/plain consumption and export to navigable formats.
13. TUIKit foundations (GitHub 2025): respect NO_COLOR/FORCE_COLOR; degrade
   truecolor→16→none; APCA contrast tiers; animations invisible to screen
   readers; scannable `--help` + hint bars.
14. no-color.org: NO_COLOR convention (command-line software honors an empty
   or present NO_COLOR env var by disabling color).

### 1.6 Overview of remainder

§2 describes overall product perspective, users, environment, constraints, assumptions. §3–§4 state functional system requirements. §5 states learning-mode requirements. §6 states external interface requirements. §7 states nonfunctional requirements and constraints. §8 states verification and acceptance. §9 states traceability. Appendices give the glossary, requirement ID index, and pilot notes.

---

## 2. Overall description (IEEE 29148 §9.5.2)

### 2.1 Product perspective

termlearn is a new, self-contained, offline-first terminal application. It is **NOT** an EPUB reader, **NOT** a generic flashcard app, and **NOT** a web LMS. Its context diagram is:

```
[ EPUB files in books/<slug>/ ] --extract--> [ raw_chapters/*.txt + meta.json ]
        |
        +--gen-prompt--> [ prompt text ] --(manual copy to AI chat)--> [ chNN.yaml draft ]
        |                                                                  |
        +--validate--> [ packs/<slug>/ ] <---------------------------------+
        |
[ main.py + lib/* ] --reads packs + progress.db--> [ study/revise/quiz/srs/parsons/lab/test/stats ]
```

The system **SHALL** consist of the layers above. No network service **SHALL** be required at runtime.

### 2.2 Product functions (summary; detailed in §3–§4)

1. Discover and register books from EPUBs.
2. Extract chapters to reviewable plain text while preserving code blocks and heading structure.
3. Emit a copy-paste AI generation prompt per chapter and validate returned YAML.
4. Teach chapters learn-first via concept blocks with inline formative checks.
5. Offer revision, quiz/practice, Parsons, lab, chapter test, cross-chapter SRS, and stats.
6. Persist progress, SRS scheduling, and answer telemetry in SQLite.
7. Export notes and support upgrade from Rich CLI to Textual TUI without pack migration.

### 2.3 User classes and characteristics

| Class | Description | Technical level |
|-------|-------------|-----------------|
| Learner (primary) | Self-directed learner studying from terminal; selects book/chapter/mode; runs labs. | Comfortable with shell, `python`, and the book's toolchain (`gcc` for C books). |
| Pack author (same human + external AI) | Runs extractor, prompts AI chat, reviews YAML, runs validator, iterates. | Can read chapter text and judge fidelity. |
| Maintainer | Extends `lib/`, adds interaction kinds, ports CLI screens to Textual. | Python, Textual/Rich, YAML, SQLite. |

Accessibility: all functionality **MUST** be keyboard-operable. Mouse support **MAY** be offered in the later Textual port but **MUST NOT** be required.

### 2.4 Operating environment

1. `CR-ENV-001`: The system **MUST** run on Linux (primary target: the developer's Linux host) with Python 3.11 or later. Support for macOS/WSL **SHOULD** follow without code forks.
2. `CR-ENV-002`: Labs **REQUIRE** the book's declared toolchain (see `toolchain` in FR-PACK-001; pilot: system `gcc` supporting `-Wall -std=c99` or later). If the declared toolchain is absent — or the language has no local runner yet (FR-LAB-004) — lab/test modes **MUST** degrade gracefully with a clear diagnostic and **MUST NOT** crash other modes.
3. `CR-ENV-003`: The terminal **SHALL** be assumed to support UTF-8, ANSI color, and at least 80×24 cells. No graphical display **SHALL** be assumed.
4. `CR-ENV-004`: All runtime state **MUST** reside under the project root plus `${XDG_DATA_HOME:-~/.local/share}/termlearn/` for the SQLite DB. No root privileges **SHALL** be required.

### 2.5 Project file tree (normative for v0.3)

The following tree **SHALL** exist. Files marked `(gen)` are user/AI-generated, not hand-committed logic:

```
~/Apps/termlearn/
  main.py                 # REQUIRED entry point; arg parsing + mode routing only
  requirements.txt        # REQUIRED pinned deps
  README.md               # REQUIRED operator quickstart
  docs/
    SRS.md                # THIS document (REQUIRED, normative)
    USER_MANUAL.md        # REQUIRED operator manual (IF-CLI-002 companion)
  lib/
    __init__.py
    books.py              # book discovery + meta handling    epub_extract.py       # EPUB -> raw_chapters + meta.json
    keys.py               # REQUIRED shared `?`/`help` helper (IF-CLI-006)
    pager.py              # REQUIRED --more pager (IF-CLI-005)
    pack.py               # YAML load + schema validation
    progress.py           # SQLite progress/SRS/telemetry
    study.py              # study-mode renderer
    revise.py             # revise-mode renderer
    quiz.py               # mcq / predict / why-fails / fillblank runner
    parsons.py            # ordering interaction
    lab.py                # language-dispatched run + hidden-test harness (pilot: gcc)
    srs.py                # SM-2 scheduler + due queue
    ai_prompt.py          # gen-prompt emitter
    stats.py              # mastery + weak-concept reporting + --reset
    export_md.py          # markdown export
  tui/                    # Textual presentation layer (packs read-only)
    __init__.py
    app.py                # LearnApp router + global ? (IF-TUI-001..004)
    widgets.py            # HelpModal + QuestionWidget (IF-TUI-003..005)
    screens.py            # Home/Chapters/Menu/Revise/Stats/Test
    practice.py           # Study/Quiz/Cards/Lab (Textual-native interactions)
  prompts/
    GENERATE.md           # REQUIRED normative AI instructions
    ASK_USER.md           # REQUIRED interrogation template
  books/
    README.md
    <book-slug>/          # (gen) one dir per EPUB
      source.epub
      meta.json           # (gen)
      raw_chapters/
        ch01.txt          # (gen)
  packs/
    <book-slug>/          # (gen) one dir per book
      book.yaml           # (gen) index + prereqs (+ toolchain)
      ch01.yaml           # (gen) chapter teaching pack
      runner/run          # (gen) AI-authored executable runner (§4.9), when declared
  tests/
    test_pack_validator.py
    test_srs.py
    test_lab_harness.py
    test_keys.py            # REQUIRED `?`-help tests (VR-007)
    test_runner.py          # REQUIRED runner-protocol tests (VR-008)
    test_tui.py             # REQUIRED TUI pilot tests (VR-009)
    fixtures/
      runner/             # fixture generated runners (good + broken)
```

`FR-TREE-001`: The implementation **MUST** conform to this layout. Additional modules **MAY** be added under `lib/` but **MUST NOT** move the normative paths above without updating this SRS.

### 2.6 Design and implementation constraints

1. `CR-DES-001`: `main.py` **MUST** contain only CLI routing and top-level flow; domain logic **MUST** live in `lib/`.
2. `CR-DES-002`: Packs **MUST** be plain YAML (UTF-8, `---` documents where applicable) conforming to the schema in §4.8. Binary or JSON-only packs **MUST NOT** be accepted as conformant.
3. `CR-DES-003`: The v0.3 UI **MUST** be built on Rich (or Typer+Rich). A later Textual port **MUST** reuse `lib/pack.py`, `lib/progress.py`, `lib/srs.py`, and the pack schema unchanged.
4. `CR-DES-004`: AI generation **MUST** be external/manual in v0.3. The app **MUST NOT** require LLM API keys or network access to study, revise, quiz, or test.
5. `CR-DES-005`: Dependencies **MUST** be limited to: `rich`, `typer`, `pyyaml`, `ebooklib`, `beautifulsoup4`, `textual` (for later phase, allowed early as optional), plus Python stdlib (`sqlite3`, `subprocess`, `pathlib`, `argparse` if not using Typer). New runtime dependencies **SHOULD NOT** be added without updating this SRS.

### 2.7 Assumptions and dependencies

1. `AS-001`: It is assumed the user legally possesses the EPUBs placed in `books/`.
2. `AS-002`: It is assumed EPUBs are text-based (not scanned images) and parseable by `ebooklib`/`BeautifulSoup`. Image-only EPUBs are out of scope.
3. `AS-003`: It is assumed the external AI can read pasted chapter text (possibly chunked) and return YAML. Chunking strategy is defined in `prompts/GENERATE.md`.
4. `AS-004`: It is assumed the learner wants learn-first behavior (not revision-only) and accepts short terminal expositions linked to `source_ref`s rather than full book pagination.

---

## 3. System features — book and chapter management

### 3.1 Feature F1: Book discovery and selection

`FR-BOOK-001`: The system **MUST** discover books by scanning `books/*/` for `source.epub` and/or `meta.json` and `packs/*/` for `book.yaml`.
`FR-BOOK-002`: The book picker **MUST** display for each book: slug, title, author (if known), chapter count, pack coverage (how many chapters have YAML), and mastery as passed-test chapters over pack chapters (`n/m`, `—` when nothing recorded).
`FR-BOOK-003`: Book slugs **SHOULD** be filesystem-safe, lowercase, hyphen-separated, derived deterministically from title (e.g. `fluent-c`). (Downgraded from MUST in v0.3.1: no tool derives slugs automatically yet — directories are created by hand. Collisions **MUST** still be resolved with a numeric suffix and recorded in `meta.json`.)
`FR-BOOK-004`: Selecting a book with no pack **MUST** guide the user to extraction + generation (show next actions) and **MUST NOT** crash.
`FR-BOOK-005`: The system **SHOULD** support ignoring non-book directories via a `.ignore` marker file inside such a directory.

### 3.2 Feature F2: Chapter discovery and selection

`FR-CHAP-001`: The chapter picker **MUST** list chapters in author order with pack presence, status (`new`/`studying`/`mastered`, `—` without a pack), SRS due count, and lab state (`pass`/`fail`/`—`, `—` when the pack has no lab).
`FR-CHAP-002`: Chapter order **MUST** follow `packs/<slug>/book.yaml` when present; otherwise it **MUST** fall back to `books/<slug>/meta.json` spine order.
`FR-CHAP-003`: A chapter lacking `chNN.yaml` **MUST** be selectable for `gen-prompt`/`validate` but **MUST** disable `study`/`quiz`/`lab`/`test` with an explanatory message.
`FR-CHAP-004`: The system **SHOULD** support `--book` and `--chapter` CLI flags to skip pickers for repeat use.

### 3.3 Feature F3: EPUB extraction (external script + in-app option)

`FR-EXT-001`: `lib/epub_extract.py` **MUST** accept a path to `source.epub` and emit `meta.json` (title, authors, language, spine order with per-chapter titles) plus `raw_chapters/chNN.txt` files.
`FR-EXT-002`: Extraction **MUST** preserve heading hierarchy (as Markdown `#`/`##`), paragraph breaks, lists, tables (as Markdown or aligned text), image alt-text/captions where present, and code blocks as fenced blocks with language hints when detectable.
`FR-EXT-003`: Extraction **MUST NOT** silently drop chapters. Unparseable spine items **MUST** be listed in `meta.json` under `warnings[]`, printed by `extract`, and surfaced by `validate` as WARN (informational in all modes — source gaps, not pack defects).
`FR-EXT-004`: The extractor **MUST** be runnable both standalone (`python -m lib.epub_extract <epub> --out books/<slug>/`) and via `main.py extract --book <slug>`.
`FR-EXT-005`: Re-running extraction over an existing `raw_chapters/` **MUST** require `--force` or create timestamped backups; silent overwrite **MUST NOT** occur.
`FR-EXT-006`: The extractor **SHOULD** handle EPUB 2 and EPUB 3, NCX and Nav TOCs, and common entities/footnotes by inlining or appending them as `[Note]` sections.

---

## 4. System features — AI pack generation and pack contract

### 4.1 Feature F4: Generation prompt emission

`FR-GEN-001`: `main.py gen-prompt --book <slug> --chapter <id>` **MUST** emit to stdout (and optionally to a file) the concatenation of `prompts/GENERATE.md` + `prompts/ASK_USER.md` + the corresponding `raw_chapters/<id>.txt` (chunked if over a documented character budget, default 12000 chars with overlap) + the normative excerpts auto-extracted from `docs/SRS.md` between the `SCHEMA` markers (§4.8) and the `RUNNER-PROTOCOL` markers (§4.9), so the prompt is self-contained. Every SRS cross-reference inside `prompts/` **MUST** cite the `docs/SRS.md` path explicitly (not bare section numbers).
`FR-GEN-002`: Chunking **MUST** be deterministic, overlap by at least 500 characters at boundaries, and label each chunk `part i/N` so the AI can reassemble context.
`FR-GEN-003`: The emitted prompt **MUST** instruct the AI to interrogate the user **before** emitting YAML (scope, depth, examples to keep, lab difficulty, toolchain/language detail), per `ASK_USER.md`. Packs produced without interrogation **MUST** arrive with top-level `draft: true`; `validate` flags drafts (WARN, ERR in `--strict` so drafts never gate advancement).

### 4.2 Feature F5: Normative AI instructions (`prompts/GENERATE.md`)

`FR-AI-001`: `prompts/GENERATE.md` **MUST** exist and **MUST** normatively define: fidelity rules, chunking/blocking rules, interaction palette and when-to-use mapping, question-quality bar, lab/test rules, SRS card rules, YAML output envelope (single YAML document in a fenced block, no surrounding prose), and refusal/uncertainty handling.
`FR-AI-002`: Fidelity: generated exposition **MUST** use only concepts and APIs present in the pasted chapter; external knowledge **MUST NOT** be introduced as normative unless marked `enrichment: true` with a `source_ref` distinct from the book. All code examples taken from the book **MUST** be verbatim unless explicitly marked `adapted: true` with a reason.
`FR-AI-003`: Blocking: each chapter **MUST** be split into concept-dependency-ordered blocks with exactly one new falsifiable skill per block. A block **MUST NOT** bundle two independent new APIs without justification.
`FR-AI-004`: Interaction selection **MUST** be content-dependent per block `type` (`model`, `syntax`, `design`, `algorithm`) as mapped in §4.7. Fixed quotas (e.g. always 5 MCQ) **MUST NOT** be required; the AI **SHOULD** choose 2–4 checks per block that best fit the type.
`FR-AI-005`: Question quality: at least half of `predict`/`mcq` checks per chapter **SHOULD** be conceptual `why`/`why-fails` rather than mere `whether/output-only`, with distractors drawn from authentic bugs (e.g. off-by-one; pilot instances: missing `&`, dangling pointer, format-string mismatch). Every check **MUST** carry a `why` explanation linking back to its block. All questions and checks **MUST** be fully self-contained with complete scenario and code context; the AI **MUST NOT** refer to external questions, exercises, or page numbers in the book.
`FR-AI-006`: Labs: each chapter with code **SHOULD** include at least one `lab` with `starter_c` (key name stable across languages) ≤ ~30 lines, explicit task, `tests_sh` or `tests` list, 2-second timeout default, 1–3 hints, and `lang` matching the book's toolchain. Labs **MUST** run under the declared toolchain (pilot: compile under `gcc -Wall -std=c99` or the book's stated standard). For languages without a local runner, the AI **MUST** additionally author `packs/<slug>/runner/run` per §4.9 (with `toolchain.runner`, `version_cmd`, and `smoke` vectors). Chapters without executable code **MUST** omit labs rather than invent them.
`FR-AI-007`: The AI **MUST** output exactly one YAML document per chapter conforming to §4.8, inside a single fenced `yaml` block when responding in chat. Surrounding explanation **SHOULD** be outside the fence and **MUST NOT** be required for parsing.

### 4.3 Feature F6: User interrogation (`prompts/ASK_USER.md`)

`FR-ASK-001`: `prompts/ASK_USER.md` **MUST** define a short question set the AI **MUST** ask before generating: (a) learner level, (b) depth vs speed, (c) which book examples/sections to prioritize or skip, (d) lab difficulty and toolchain (language + runner; pilot default C/`gcc` version/flags — the book's own MUST be stated), (e) output language of explanations, (f) how much interleaved review to inject.
`FR-ASK-002`: The AI **MUST NOT** emit final YAML until the user answers or explicitly says `use defaults`. Defaults **MUST** be documented in `ASK_USER.md`.
`FR-ASK-003`: Answers **SHOULD** be recorded by the human as a `gen_notes.md` alongside the pack for reproducibility (non-normative but **RECOMMENDED**).

### 4.4 Feature F7: Pack validation

`FR-VAL-001`: `main.py validate --book <slug> [--chapter <id>] [--strict]` **MUST** validate YAML syntax, schema conformance (§4.8), answer-index bounds, `answer_order` validity (≥2 unique valid indices; distractor lines omitted), runnable-code probes for languages with a local runner (pilot: C examples/labs when `gcc` present; other languages noted as `LANG-NOPROBE`, which **MUST NOT** fail `--strict`), generated-runner smoke test when `toolchain.runner` is declared (RUNNER-SMOKE: check+exec verbs against `toolchain.smoke`; shape/output violations **MUST** fail), the `toolchain` gate (`TOOLCHAIN-MISSING` when runnable content lacks a declared stanza), and cross-references (`prereqs`, `source_ref`, interleaved `from_chapter` targets).
`FR-VAL-002`: Validation **MUST** exit non-zero and print machine-actionable errors (`file: CODE: message`) on failure. (Line numbers are not reported: `yaml.safe_load` does not retain marks; the `CODE` pinpoints the rule instead.) Warnings (e.g. missing `viz` for a `model` block, low `why`-ratio) **MUST** be printed but **MUST NOT** fail in non-strict mode; in `--strict` they **SHALL** fail, except informational notes (`LANG-NOPROBE`), which **MUST NOT** fail either mode.
`FR-VAL-003`: `validate` **MUST** verify that every `blocks[].id` referenced by `test.gates[].needs` exists, that every interleaved check's `from_chapter` references an existing chapter id, and that `from_block` exists in the referenced chapter whenever that chapter's pack is loadable (unloadable chapters stay chapter-level).
`FR-VAL-004`: `validate --fix-hints` **MUST**, after reporting errors, print per-error repair suggestions without modifying files: valid answer-index ranges with the choice list, duplicate/missing `answer_order` indices, the valid `kind`/`type` vocabularies for unknown values, and missing-field stubs naming block/check. Suggestions are advisory; they **MUST NOT** change the pass/fail verdict.

### 4.5 Feature F8: Tests created by AI and verifiable in app

`FR-TEST-001`: Each chapter YAML **MAY** contain a `test:` stanza defining chapter mastery gates (`min_quiz`, required blocks) plus `final_checks[]` in check shape for future interactive execution.
`FR-TEST-002`: `main.py test --book <slug> --chapter <id>` judges recorded evidence deterministically: last recorded quiz score for the chapter plus the lab probe result, reporting pass/fail. Interactive execution of `final_checks`, hidden-test runs beyond the starter probe, and per-concept breakdown are deferred (see Appendix D, D-06).
`FR-TEST-003`: Test outcomes **MUST** be recorded in `progress.db` and reflected in chapter status. A `--force` flag **MAY** allow advancing despite failure; its use **MUST** be logged.
`FR-TEST-004`: Flaky tests (timing/network-dependent) **MUST NOT** be accepted; `validate` **MUST** reject denylisted destructive commands and network-capable constructs (`socket`, `urllib`/`http.client`, `requests`, shell `/dev/tcp` redirections, `nc`, fetch-pipes) in `tests_sh` and runner sources (WARN, ERR in `--strict`). GUI imports (`tkinter`, Qt, `pygame`/SDL) produce WARN-only notes (hosts vary).

### 4.6 Content-type taxonomy (normative vocabulary)

Block `type` **MUST** be one of:

| `type` | Meaning | Example instances (pilot: C) |
|--------|---------|----------------------|
| `model` | Mental-model / semantics; invisible mechanism. | pointers/addresses, storage duration, `malloc` lifecycle, stack vs heap |
| `syntax` | Surface form / idiom / API shape. | `for`/`switch`, `scanf` formats, header guards, `const` placement |
| `design` | Judgment / trade-off / best practice. | header organization, error-handling policy, ownership conventions |
| `algorithm` | Multi-step procedure over data. | string handling, sorting, linked-list ops |

### 4.7 Interaction palette and when-to-use mapping

The following interaction `kind`s **MUST** be supported by v0.3 unless marked OPTIONAL. Selection per block **MUST** follow the mapping; arbitrary substitution **SHOULD** be justified in `gen_notes.md`.

| `kind` | Terminal realization | Use when | Normative status |
|--------|----------------------|----------|------------------|
| `predict` | MCQ: given code, predict output/value. Keys `1-4`. | `model`, `algorithm` — tracing and mental simulation. | **REQUIRED** |
| `why-fails` | MCQ: given broken code + error/behavior, choose cause. | `model`, `syntax` — diagnose authentic bugs. | **REQUIRED** |
| `mcq` | Conceptual MCQ (no code or short snippet). | Any type for definitions, contrasts. | **REQUIRED** |
| `fillblank` | Single-token completion (`&`, `*`, `;`, format). | `syntax` — fast reps. | **REQUIRED** |
| `order` (Parsons) | Order scrambled lines via `3 1 2 4`; distractors supported. | `syntax`, `algorithm` — sequencing without full authoring load. | **REQUIRED** |
| `eipe` | Explain-in-Plain-English: choose best 1-sentence description from options (free-text OPTIONAL, matched by keywords). | `design`, `algorithm` — comprehension/transfer. | **REQUIRED** (options form); free-text scoring **OPTIONAL** |
| `choose-better` | Two snippets, pick idiomatic/correct + why. | `design` — judgment. | **REQUIRED** |
| `trace` | Stepped memory/state trace table; predict mutated cell value. | `model`, `algorithm` — Notional Machine tracing. | **REQUIRED** (v0.8+) |
| `spot-bug` | Pinpoint buggy line and patch given compiler/sanitizer diagnostic log. | `model`, `syntax` — authentic debugging. | **REQUIRED** (v0.8+) |
| `micro-lab` | Edit ≤15 lines in `$EDITOR` or inline, `r=run`, `t=test`. | Any type where execution cements the idea. | **REQUIRED** via `lab.py` |
| `ascii-viz` | Stepwise `stack/heap/pointer` diagram rendered as text; `n=next` steps. | `model` — dual coding in terminal. | **REQUIRED** renderer; per-block diagrams **SHOULD** exist for `model` blocks |
| `dialog-ask` | Constrained Q&A: tutor answers only from current + prerequisite blocks, then redirects to a check. | Remediation inside `study`. | **OPTIONAL** in v0.3 (stub allowed); **SHOULD** be a later enhancement |

Mapping rules:

1. `MAP-001`: `model` blocks **MUST** include at least one of `predict` or `why-fails` and **SHOULD** include an `ascii-viz` where a spatial/memory model aids understanding.
2. `MAP-002`: `syntax` blocks **SHOULD** include `order` (with at least one distractor where a classic mistake exists) or `fillblank` plus one `why-fails`.
3. `MAP-003`: `design` blocks **SHOULD** include `eipe` or `choose-better`.
4. `MAP-004`: `algorithm` blocks **SHOULD** include `predict` (trace) + `order` or `micro-lab`.
5. `MAP-005`: Every chapter **SHOULD** include at least two interleaved checks referencing prior chapters (`from_chapter` + `from_block`), realizing spacing without a separate mode.

<!-- SCHEMA-BEGIN: normative pack contract, auto-appended to gen-prompt output (FR-GEN-001). Do not break these markers. -->
### 4.8 Pack YAML contract (normative schema)

`FR-PACK-001`: Each book **MUST** have `packs/<slug>/book.yaml`:

```yaml
book: {slug: fluent-c, title: "Fluent C", authors: ["..."], source: "books/fluent-c/source.epub"}
toolchain: {lang: c, compile: [gcc, -Wall, -std=c99, -O0], run: ['./prog'], timeout_s: 2}
# books in other languages declare their own, e.g.:
# toolchain: {lang: python, runner: runner/run, run: [python3], version_cmd: [python3, --version],
#             timeout_s: 2, smoke: {ext: py, src: "print('ok')\n", expect: "ok\n"}}
order: [ch01, ch02]            # REQUIRED author order
chapters:                      # REQUIRED one entry per id in order
  - {id: ch01, title: "...", source_ref: "Ch.1", prereqs: []}
  - {id: ch02, title: "...", source_ref: "Ch.2", prereqs: [ch01]}
```

`toolchain` is RECOMMENDED whenever the pack has runnable content (examples
with `run_expected`, labs, micro-labs with code) and **REQUIRED** in `--strict`
validation for such packs (`TOOLCHAIN-MISSING`); it declares the language and
reference commands (pilot example above is C — Python/networking/theory books
declare their own or omit it when nothing runs). Optional keys: `runner`
(relative path to the AI-authored runner, §4.9), `version_cmd` (diagnostic
probe the validator **SHOULD** run and display, non-fatal if absent),
`timeout_s` (default 2), `smoke` (`{ext, src, expect}` hello-world vectors the
validator smoke-tests a generated runner with). `order` is REQUIRED.

`FR-PACK-002`: Each chapter file `packs/<slug>/<id>.yaml` **MUST** conform to the following shape (keys marked REQUIRED **MUST** be present; others **MAY** be omitted where inapplicable but **SHOULD** be present per §4.7):

```yaml
meta:                          # REQUIRED
  book: fluent-c               # REQUIRED == parent slug
  chapter_id: ch01             # REQUIRED == filename stem
  title: "..."                 # REQUIRED
  source_ref: "Ch.1 pp.1-20"   # REQUIRED, trace to book
  level: intro                 # REQUIRED: intro|core|advanced
  prereqs: [ ]                 # REQUIRED (possibly empty)
objectives: [...]              # REQUIRED, 1-6 falsifiable skills
blocks:                        # REQUIRED, >=1
  - id: b1                     # REQUIRED, unique in file
    type: model                # REQUIRED, §4.6 vocabulary
    title: "..."               # REQUIRED
    explain_md: "..."          # REQUIRED, 5-15 lines Markdown
    example:                   # OPTIONAL but RECOMMENDED when code exists
      lang: c
      code: "..."              # verbatim or adapted:true
      adapted: false
      run_expected: "..."
      subgoals:                # OPTIONAL, cognitive chunking for complex examples
        - {label: "...", lines: [1,2]}
    viz:                       # SHOULD for model; otherwise OPTIONAL
      kind: ascii-memory
      steps: ["...","..."]
    checks:                    # REQUIRED, >=1 per block
      - kind: predict          # REQUIRED, §4.7 vocabulary: predict|why-fails|mcq|fillblank|order|eipe|choose-better|trace|spot-bug
        q: "..."               # REQUIRED
        code: "..."            # OPTIONAL
        choices: [...]         # REQUIRED for choice kinds, 2-5 items (schema); GENERATE prefers 2-4
        answer: 1              # REQUIRED index (0-based) for choice kinds
        answer_order: [1,0,2]  # REQUIRED iff kind==order: >=2 unique valid line indices (distractors omitted)
        faded: true            # OPTIONAL iff kind==order: enables faded Parsons problem
        blanks: [{line_idx: 0, answer_text: "..."}] # REQUIRED iff kind==order and faded==true
        answer_text: "&"       # REQUIRED iff kind==fillblank or kind==trace (text mode)
        trace:                 # REQUIRED iff kind==trace
          headers: ["Step", "Variable", "Address", "Value"]
          rows: [{step: 1, line: 1, cells: ["..."]}]
        target: {row: 2, col: 3} # REQUIRED iff kind==trace
        diagnostic_log: "..."  # REQUIRED iff kind==spot-bug: compiler/sanitizer report
        target_line: 3         # RECOMMENDED iff kind==spot-bug
        why: "..."             # REQUIRED for every check
        concept: "..."         # RECOMMENDED tag for telemetry
        from_chapter: ch00     # OPTIONAL, REQUIRED iff interleaved review
        from_block: b2         # OPTIONAL, with from_chapter
    common_bugs: [...]         # OPTIONAL but RECOMMENDED
cards:                         # SHOULD, >=3 when chapter introduces durable facts
  - {front: "...", back: "...", concept: "..."}
lab:                           # SHOULD when chapter has code; else OMIT (never invent)
  lang: c                      # OPTIONAL, default c; the book's toolchain language
  title: "..."
  prompt_md: "..."
  starter_c: "..."             # key name stable across languages
  tests_sh: "..."              # OR tests: [...]
  hints: ["..."]
test:                          # SHOULD; REQUIRED for chapters that gate advancement
  gates: [{needs: [b1,b2], min_quiz: 80}]
  final_checks: [...]          # same shape as block checks
```

`FR-PACK-003`: Unknown top-level keys **MUST** cause a warning; unknown `kind`/`type` values **MUST** cause validation failure.
`FR-PACK-004`: All Markdown fields **MUST** be UTF-8 and **MUST** render without exception in Rich. Embedded ANSI escapes **MUST NOT** appear in YAML.
`FR-PACK-005`: Line length **SHOULD** be ≤120 chars for terminal readability; code lines **SHOULD** be ≤80 cols.
`FR-PACK-006`: `packs/` content **MUST** be the sole teaching source at runtime. The app **MUST NOT** read `raw_chapters/*.txt` during `study`/`quiz`/`test` (those are authoring inputs only).
<!-- SCHEMA-END -->

<!-- RUNNER-PROTOCOL-BEGIN: normative runner contract, auto-appended to gen-prompt output (FR-GEN-001). Do not break these markers. -->
### 4.9 AI-authored runner protocol (normative)

Instead of hand-writing one runner per language, the AI authors a per-book
runner alongside the pack. The app invokes it through this fixed protocol;
a runner that breaks the protocol fails validation like a broken pack.

1. `RUNNER-LOC`: The runner **MUST** live at `packs/<slug>/<toolchain.runner>`
   (conventionally `runner/run`), be executable, and start with a shebang for
   an interpreter expected on the learner's host. It **MAY** be written in any
   language (shell, Python, …).
2. `RUNNER-CHECK`: Invocation `run check <source-file>` **MUST** print exactly
   one JSON object to stdout: `{"ok": true|false, "diagnostics": "..."}` —
   the parse/compile gate. `diagnostics` **MUST** be human-readable tool output
   (empty when ok).
3. `RUNNER-EXEC`: Invocation `run exec <source-file> --expect <file> --timeout <secs> [--stdin <file>]`
   **MUST** print exactly one JSON object: `{"passed": true|false,
   "output": "<captured stdout>", "timed_out": true|false,
   "returncode": <int|null>}`. Comparison against `--expect` happens
   inside the app (diff display), not the runner; the runner reports raw facts.
4. `RUNNER-EXIT`: The runner **MUST** exit `0` whenever it operated the protocol
   correctly — even for `ok: false` / `passed: false` verdicts. Non-zero exit,
   non-JSON output, or timeout **MUST** be treated by the app as runner error
   (distinct from learner-code failure) and reported as such.
5. `RUNNER-SANDBOX`: The runner **MUST** work with cwd set to a fresh temp dir
   supplied by the app, read the (absolute-path) source read-only, write only
   inside cwd, open no network connections, and complete well within `--timeout`
   (the app kills and reports `timed_out` regardless). Runner source **MUST**
   pass the NFR-SEC-002 denylist scan and is human-reviewed on paste, like YAML.
6. `RUNNER-SMOKE`: `toolchain.smoke` (`{ext, src, expect}`) **SHOULD**
   accompany every generated runner. `validate` writes `smoke.src` to
   `hello.<ext>` in a temp dir and runs the check+exec verbs against
   `smoke.expect`; shape violations or mismatches **MUST** fail validation.
   Absent `smoke` vectors produce a warning, not a failure.
7. `RUNNER-VERSION`: `toolchain.version_cmd` (e.g. `[python3, --version]`)
   **SHOULD** be declared; `validate` runs it and prints the result for
   reproducibility diagnostics. Failure/missing command is non-fatal.
8. `RUNNER-VERBS` (v0.8+): Invocation `run verbs` **SHOULD** print exactly one
   JSON object: `{"verbs": ["check", "exec", ...]}`, declaring the capabilities
   supported by the book's runner. Absent or failing command defaults to `["check", "exec"]`.
9. `RUNNER-INSPECT` (v0.8+): Invocation `run inspect <source-file> --mode <symbols|disasm|sections|ast>`
   **MAY** be implemented. Returns JSON `{"ok": bool, "mode": str, "content": "...", "format": "text|asm|json"}`.
   The terminal app displays this in the live Toolchain Inspector tab (`i` hotkey).
10. `RUNNER-LINT` (v0.8+): Invocation `run lint <source-file>` **MAY** be implemented.
    Returns JSON `{"ok": bool, "diagnostics": [{"line": int, "col": int, "severity": "error|warning|note", "message": "..."}]}`.
<!-- RUNNER-PROTOCOL-END -->

---

## 5. System features — learning modes

### 5.1 Feature F9: Study mode (primary, learn-first)

`FR-STUDY-001`: `main.py study --book <slug> --chapter <id>` **MUST** traverse the chapter's blocks in order, rendering for each: objectives remnant, `explain_md`, `example` with syntax highlighting, optional `viz` stepper, then each check with immediate feedback (`correct/incorrect` + `why` + link to block).
`FR-STUDY-002`: On an incorrect check, the system **MUST** show the `why` explanation and **SHOULD** offer one remediation: re-show the example, step the `viz`, or pose one follow-up variation. Bare `wrong, answer is B` **MUST NOT** be the only feedback.
`FR-STUDY-003`: Study **MUST** record per-block outcomes (seen, checks passed/failed, attempts) to `progress.db`.
`FR-STUDY-004`: Study **MUST** support the on-screen keys `n=next viz step`, `s=skip viz`, `r=run example` (when runnable), `y/N=re-show example` after a miss, `1-N` for checks, `?`=help, `q=quit & save`. Keybindings **MUST** be documented on-screen.
`FR-STUDY-005`: Running an example **MUST** dispatch on `example.lang` through the declared toolchain (pilot: C compiles to a temp dir with `gcc -Wall -std=c99 -O0`) and enforce a default 2 s timeout. Tool errors **MUST** be shown verbatim with a one-line hint where available; unsupported languages **MUST** show the FR-LAB-004 guidance instead.
`FR-STUDY-006`: Study **SHOULD** inject the chapter's interleaved checks at natural breaks (not only at the end).

### 5.2 Feature F10: Revise mode

`FR-REV-001`: `main.py revise` **MUST** render `explain_md` per block, examples, and `common_bugs` without scoring or gating. (Objectives header deferred, see Appendix D, D-21.)
`FR-REV-002`: Revise **MUST NOT** write quiz scores; it **MAY** mark blocks `seen`.

### 5.3 Feature F11: Quiz / Practice mode

`FR-QUIZ-001`: `main.py quiz` **MUST** run all (or `--sample N`, `--concept X` for an exact `concept`-tag match, combinable) checks from the chapter's blocks (shuffled when `--seed` is given, author order otherwise), supporting `predict`, `why-fails`, `mcq`, `fillblank`, `eipe`, `choose-better`.
`FR-QUIZ-002`: Each response **MUST** receive immediate `why` feedback. End-of-run **MUST** show score plus a per-concept breakdown (hits/total per `concept` tag) and weakest concepts.
`FR-QUIZ-003`: Scores **MUST** persist to `progress.db` with timestamp, seed, and sampled item IDs (`block:idx` list) for reproducibility. (Legacy databases gain the column by migration.)

### 5.4 Feature F12: Parsons mode

`FR-PAR-001`: `main.py parsons` **MUST** render `order` checks as numbered lines (shuffled only when an RNG/seed is supplied; author order otherwise) including distractors marked internally but not revealed, and accept space-separated order input (e.g. `3 1 2 4`), plus `s=shuffle`, `h=hint`, `q=quit`.
`FR-PAR-002`: Distractor lines chosen by the learner **MUST** trigger specific feedback naming the bug class (e.g. `missing-&`, `off-by-one`) when the pack provides `distractor_why`; otherwise generic feedback **MAY** be shown.
`FR-PAR-003`: Parsons outcomes **MUST** persist like quiz outcomes.

### 5.5 Feature F13: Lab mode (practice + hidden tests)

`FR-LAB-001`: `main.py lab` **MUST** present `prompt_md`, write `starter_c` to a temp file, open `$EDITOR` (or inline fallback), then support `r=run`, `t=run hidden tests`, `d=show last output/diff`, `h=next hint`.
`FR-LAB-002`: Hidden tests **MUST** run in a temp dir, with no network, 2 s default timeout, and output diffing. Failures **MUST** show the first failing case plus its hint, not the full hidden suite when the pack marks cases `hidden: true`.
`FR-LAB-003`: Submitting to hidden tests (`t`) **MUST** record the solution's SHA-256 content hash with pass/fail verdict and timestamp in a `solutions` table (deduplicated by hash), retaining the code for review. `--no-save-solution` **MUST** skip retention (the hash + verdict are still recorded in the run log).
`FR-LAB-004`: Runnable execution **MUST** dispatch on the content's `lang`
(`example.lang` / `lab.lang` / check `lang`, default `c`) with the following
precedence: (1) built-in local runner if the language has one (pilot: C);
(2) the book's AI-authored generated runner at `toolchain.runner` (§4.9);
(3) an explicit unsupported result (never a crash, never a silent skip),
surfaced as guidance ("run it in the book's toolchain").
A `test` gate whose lab has no runnable runner **MUST** judge quiz evidence only
and note the lab as non-gateable. Rationale: the system is language-agnostic;
C is the pilot runner, not the scope; per-book runners scale where hand-written
ones cannot.

### 5.6 Feature F14: SRS mode

`FR-SRS-001`: `main.py srs [--book <slug>]` **MUST** build a due queue across chapters using SM-2 (or documented equivalent): each card tracks `easiness`, `interval`, `reps`, `next_due`.
`FR-SRS-002`: Review prompts **MUST** support `f=flip`, `e=edit card` (new front/back via `$EDITOR` or inline prompts, empty keeps), `1-4` quality grades, `q=quit`. Grading **MUST** reschedule per SM-2 and persist immediately; edits **MUST** persist immediately.
`FR-SRS-003`: The due queue **SHOULD** be topped up with up to 2 interleaved quiz checks from mastered chapters when fewer than 5 cards are due, to preserve spacing. (Deferred in v0.3, see Appendix D, D-11.)
`FR-SRS-004`: SRS scheduling parameters **MUST** be documented in `USER_MANUAL.md` and tunable via `TERMLEARN_*` env vars without code edits: `TERMLEARN_EASINESS_INIT` (default 2.5), `TERMLEARN_EASINESS_MIN` (1.3), `TERMLEARN_INTERVAL_1_DAYS` (1), `TERMLEARN_INTERVAL_2_DAYS` (6). Unparseable values **MUST** fall back to defaults (never crash scheduling).

### 5.7 Feature F15: Stats / telemetry

`FR-STAT-001`: `main.py stats --book <slug>` **MUST** show per-block accuracy, per-concept accuracy (hits/total per `concept` tag with a representative block), recent quiz runs, SRS due counts, weakest blocks and concepts. (Lab state and streaks deferred, see Appendix D, D-08.)
`FR-STAT-002`: Telemetry logging **MUST** be local-only by default. No network exfiltration **SHALL** occur. Each answer log **MUST** include timestamp, `book/chapter/block/check`, `concept` tag (migrated for legacy rows), correctness (one row per attempt, so attempts = row count per check), and latency in ms (no keystroke logging).
`FR-STAT-003`: A `--reset` function **MUST** exist to wipe progress for a book/chapter after explicit confirmation. Silent data loss **MUST NOT** occur.

### 5.8 Feature F16: Export

`FR-EXP-001`: `main.py export --book <slug> [--chapter <id>] --format md [--out <file>]` **MUST** emit the book/chapter as Markdown to stdout by default, or to `--out` when given, with objectives, condensed notes, examples, and `source_ref`s.
`FR-EXP-002`: Export **MUST NOT** include hidden test bodies marked `hidden: true`; it **MAY** include their titles.

---

## 6. External interface requirements (IEEE 29148 §9.5.4)

### 6.1 User interface (CLI, v0.3 normative)

`IF-CLI-001`: All interaction **MUST** occur in a text terminal via `stdin`/`stdout`/`stderr`. The app **MUST** exit with code `0` on success and non-zero on validation/test failure or fatal error.
`IF-CLI-002`: Every command **MUST** support `--help` documenting arguments and examples. (Exit codes follow IF-CLI-001 by convention: 0 success, non-zero failure.)
`IF-CLI-003`: Output **MUST** use Rich panels, Markdown rendering, and syntax highlighting for code; color **MUST** degrade gracefully when `NO_COLOR` is set or output is piped.
`IF-CLI-004`: Interactive prompts **MUST** show available keys on every screen (e.g. `[1-4] answer · e explain · q quit`).
`IF-CLI-005`: Long-form renders over 40 source lines **MUST** pause with a `--more` continuation in the `study`/`revise` readers (Enter continues, `q` quits, `?` helps). Rationale: working-memory chunking — a screenful per idea, never a 20-page scroll.
`IF-CLI-006`: Every interactive prompt **MUST** answer `?` (and `help`) with a
contextual key list and re-prompt, via the single shared helper `lib/keys.py`.
Rationale: recognition over recall (Nielsen H6) and feature discoverability —
hidden shortcuts are never found (Norman; HCI literature). `?`/`help` are
consequently reserved words and **MUST NOT** be valid answers in single-line
prompts; pack authors are constrained accordingly (see GENERATE.md §3.3).
`IF-CLI-007`: Meaning **MUST NOT** be conveyed by color alone: every verdict
**MUST** also carry text (`correct`, `PASS`, `FAIL`, `weakest`). The app
**MUST** respect `NO_COLOR` (disable color) and `FORCE_COLOR`, and degrade
gracefully when piped (TUIKit/No-color.org practice; WCAG-equivalent
non-color-redundancy for terminals).
`IF-CLI-008`: Interaction **MUST** be linear: prompts **MUST NOT** redraw or
reposition the screen while awaiting input, so output stays consumable by
pipes and screen readers, which parse terminals linearly without landmarks
(ACM CLI-accessibility findings). Tables **SHOULD** additionally be consumable
via `export` (Markdown), which **MUST** exist as the navigable alternative.

### 6.2 Textual TUI — research-grounded rules (normative for the port)

The findings below convert the CLI evidence into port constraints so the
future TUI keeps what works. Packs conformant under this SRS **MUST** work
unchanged in the TUI (unchanged IF-TUI-001).

`IF-TUI-001`: The Textual port implements screens `Home/Chapters/Menu/Study/Quiz/Cards/Lab/Stats/Revise/Test` over the same lib data, scoring and persistence functions (`books`, `pack`, `quiz.collect_checks/filter/tally`, `srs` SM-2/persistence, `progress`, `lab.run_c/run_code`, `export`) and the unchanged pack schema. Interactive run-loops are Textual-native rather than wrapped CLI loops (the CLI loops block on stdin and cannot be embedded); scoring facts, SM-2 math, validation and toolchain execution are shared verbatim. Packs conformant under this SRS **MUST** work unchanged in the TUI.
`IF-TUI-002`: The TUI **MAY** add mouse and multi-pane layout but **MUST** preserve all CLI keybindings as aliases.
`IF-TUI-003`: The TUI **MUST** show a persistent one-line hint bar with the
current screen's keys plus a `?` overlay listing all keys (Nielsen H6/H10;
discoverability research: visibility and signifiers precede learnability;
KeyMap result that mapped, visible shortcuts are remembered).
`IF-TUI-004`: Keybindings **MUST** stay single-letter, mnemonic (`r`un,
`e`xplain/`e`dit, `h`int, `s`kip/`s`huffle, `n`ext, `f`lip), identical across
screens, one-hand reachable; no screen **MAY** introduce a conflicting reuse
(GNOME HIG keyboard guidance; shortcut research: tiny consistent vocabularies
win — shortcuts execute ~2x faster but only when discoverable).
`IF-TUI-005`: One concept per screen; progressive disclosure (summary →
detail on demand, hints general → specific); errors in plain language naming
the problem and the fix (Nielsen H1/H5/H8/H9). A screen that needs a paragraph
of instructions to be understood **MUST** be redesigned, not documented.
`IF-TUI-006`: Accessibility is a design constraint, not an edge case (ACM CLI
study; TUIKit foundations): every color/icon/progress signal **MUST** have a
text alternative; decorative elements (borders, spinners) **MUST** be
suppressible/hidden in linear output; animation **MUST** be static when a
screen reader is detected or output is piped; a `--plain` (or `NO_COLOR` +
linear) mode **MUST** reproduce every screen's content as plain scrolling text;
tabular data **MUST** remain available via `export`.

### 6.3 Software interfaces

`IF-SW-001`: Python **MUST** be 3.11+. Third-party packages **MUST** be declared in `requirements.txt` with minimum versions.
`IF-SW-002`: Toolchain execution **MUST** occur via `subprocess` with argument lists (no shell interpolation of learner code), working directory set to a fresh temp dir, env sanitized of `LD_PRELOAD`-style overrides where feasible. (Pilot instance: `gcc`.)
`IF-SW-003`: SQLite access **MUST** go through `lib/progress.py` (runs/stats tables) and `lib/srs.py` (cards/answers tables) — the two co-owner modules. Direct SQL from any other mode module **MUST NOT** occur.
`IF-SW-004`: `$EDITOR` integration **MUST** respect `VISUAL`/`EDITOR` with fallback to inline editing when unset.

### 6.4 Hardware and communications interfaces

`IF-HW-001`: No special hardware **SHALL** be required beyond a general-purpose computer capable of running Python and the book's toolchain (pilot: `gcc`).
`IF-COM-001`: The runtime **MUST NOT** require network access. Any future network feature **MUST** be opt-in and documented in a revision of this SRS.

---

## 7. Nonfunctional requirements (IEEE 29148 §9.5.5 — quality attributes)

### 7.1 Performance

`NFR-PERF-001`: Startup to book picker on a typical laptop **SHOULD** complete in ≤1 s (cold) excluding Python interpreter first import. (Measured 2026-10-13: 182 ms total incl. interpreter — 5x margin.)
`NFR-PERF-002`: Quiz/parsons interactions **MUST** respond to a keypress in <100 ms (excluding deliberate `run`/`test` compile time and human think time). (Measured: app-side per-keypress work ≈0.002 ms avg — the bound covers framework response, not the human. Unmeasured wording retired in v0.5.3.)
`NFR-PERF-003`: Toolchain run for examples ≤30 lines **SHOULD** complete in ≤3 s on a typical host; timeout default **MUST** be 2 s per run and **MUST** be configurable. (Measured: gcc hello roundtrip 34 ms — 100x margin.)
`NFR-PERF-004`: `validate` over a 10-chapter pack **SHOULD** complete in ≤10 s (excluding toolchain probes). (Measured: single chapter incl. probes 368 ms.)

### 7.2 Reliability and robustness

`NFR-REL-001`: Malformed YAML or missing fields **MUST** produce a actionable error naming file/line/field; a traceback alone **MUST NOT** be the user-facing output.
`NFR-REL-002`: Learner progress writes **MUST** be atomic per interaction (commit after each answer/lab result). A crash **MUST NOT** lose more than the in-flight interaction.
`NFR-REL-003`: Toolchain failures, timeouts, missing toolchains, and unsupported languages **MUST** be caught and reported as mode-level diagnostics preserving prior progress.

### 7.3 Usability (learn-first priority)

`NFR-USE-001`: A first-time user with an EPUB in `books/` **MUST** be able to reach `study` for chapter 1 within ≤5 commands following `README.md`, excluding AI generation time.
`NFR-USE-002`: Every scoring screen **MUST** explain how to improve (link to block/`source_ref`), not just a number.
`NFR-USE-003`: All interactive lists **MUST** be operable with number/letter keys plus `q` to quit and `?` for help.
`NFR-USE-004`: A new user **MUST** be able to discover every key of any mode
via on-screen hints and `?` alone, without opening the manual (discoverability
acceptance: unprompted key discovery). The manual documents; it **MUST NOT**
be required.

### 7.4 Maintainability and portability

`NFR-MAIN-001`: Mode logic **MUST** be isolated per `lib/<mode>.py` with pure functions for rendering/scoring to enable Textual reuse. Cyclic imports **MUST NOT** exist.
`NFR-MAIN-002`: The codebase **MUST** achieve ≥80% branch coverage on `pack.py`, `srs.py`, and `lab.py` harnesses via `tests/`. (Measured 2026-10-13: pack 85%, srs 88%, lab 82% — target met; re-measure on harness changes. Promoted from SHOULD in v0.4.1 on the evidence.)
`NFR-MAIN-003`: The system **MUST** run from a checkout with `pip install -r requirements.txt` and no build step; no compiled extensions **SHALL** be required.

### 7.5 Security, privacy, safety

`NFR-SEC-001`: Learner C code **MUST** be compiled and executed only in a fresh temp directory with a timeout, without elevated privileges, and **MUST NOT** be executed with shell `True`.
`NFR-SEC-002`: Hidden tests and generated-runner sources **MUST NOT** contain destructive commands (`rm -rf /`, network exfiltration). `validate` **SHOULD** scan `tests_sh` and `runner/run` sources for a denylist (`rm -rf`, `curl|wget`, `ssh`, `mkfs`, `:(){`) and warn/fail in `--strict`.
`NFR-SEC-003`: Telemetry **MUST** stay on local disk. No identifier beyond a random install UUID **MAY** be stored, and no telemetry **MUST** leave the host without explicit user action (e.g. `export --include-telemetry`, default off).
`NFR-SEC-004`: `books/<slug>/source.epub` files **MUST NOT** be copied outside the project by the app except to temp extraction dirs.

### 7.6 Constraints (restated as requirements)

`CR-GEN-001`: v0.3 **MUST NOT** call external LLM APIs at runtime.
`CR-GEN-002`: Packs **MUST** remain human-readable YAML; minified or encrypted packs **MUST NOT** conform.
`CR-GEN-003`: The normative language of code identifiers, CLI flags, and YAML keys **SHALL** be English. Explanatory prose **MAY** be in another language per `ASK_USER.md` answer, but keys **MUST** stay English.

---

## 8. Verification and acceptance (IEEE 29148 §9.5.6)

### 8.1 Verification methods

Each requirement **SHALL** be verified by one or more of: Inspection (I), Demonstration (D), Test (T), Analysis (A).

`VR-001`: `tests/test_pack_validator.py` **MUST** cover `FR-VAL-001..004`, `FR-PACK-001..006` with valid, missing-field, bad-index, bad-permutation, and unknown-kind fixtures. Method: T.
`VR-002`: `tests/test_srs.py` **MUST** verify SM-2 rescheduling, due ordering, and interleaved top-up (`FR-SRS-001..003`). Method: T.
`VR-003`: `tests/test_lab_harness.py` **MUST** verify compile success, compiler-error surfacing, hidden-test pass/fail/diff, timeout kill, C dispatch, and explicit unsupported-language results (`FR-LAB-001..002`, `FR-LAB-004`, `FR-STUDY-005`). Method: T. Requires `gcc` for the C cases; skips cleanly otherwise.
`VR-004`: End-to-end demonstration **MUST** show: place EPUB → extract → gen-prompt → validate sample pack → study ch01 → quiz → parsons → lab → test → srs → stats → export, pressing `?` in at least two modes to show contextual help. Method: D. Acceptance gate for v0.3.
`VR-005`: Requirement inspection **MUST** confirm every `MUST/SHALL` has an ID and a verification method. Method: I.
`VR-006`: `validate --strict` on the pilot book **MUST** pass before v0.3 is declared complete. Method: T + I.
`VR-007`: `tests/test_keys.py` **MUST** verify `?`/`help` interception, mode-specific help text, unknown-mode fallback, and the RESERVED set, using scripted fake consoles (no Rich I/O). Method: T.
`VR-008`: `tests/test_runner.py` **MUST** verify the §4.9 protocol against fixture runners in `tests/fixtures/runner/`: dispatch precedence (built-in → generated → unsupported), check/exec JSON shapes, runner-error vs learner-failure distinction, timeout kill, denylist scan of runner source, and smoke pass/fail on `toolchain.smoke` vectors. Method: T.
`VR-009`: `tests/test_tui.py` **MUST** verify via Textual Pilot: Home→Chapters→Menu→Study navigation, `?` overlay open/dismiss, Parsons scoring persisted to `quiz_runs`, cards flip/grade persisted, lab run output, Stats render. Packs **MUST** be unmodified by every TUI path. Method: T.

### 8.2 Acceptance criteria for v0.3

1. File tree in §2.5 exists with all REQUIRED files present and importable.
2. `main.py --help` lists all modes in §1.2(1) and each supports `--help`.
3. At least one pilot book (C domain — language example, not product scope) ships with `book.yaml` (including `toolchain`) + one validated `chNN.yaml` demonstrating every REQUIRED interaction kind at least once across its blocks.
4. `VR-004` demonstration passes on Linux with Python 3.11+ and the pilot toolchain (`gcc`) present.
5. No `MUST/SHALL` requirement is deferred without a recorded entry in Appendix D.
6. `?` answers with contextual help in every interactive mode (VR-007 green).
7. `docs/USER_MANUAL.md` exists and matches implemented keys/commands.
8. Runner protocol specified (§4.9) with dispatch precedence implemented and VR-008 green; hand-written per-language runners are out of scope (superseded).
9. TUI smoke (VR-009 green): full navigation, help overlay, scoring/grading persistence, lab run, stats render; packs byte-identical before/after.

---

## 9. Traceability

| Feature | Requirements | Verifies via | Implements in |
|---------|--------------|--------------|---------------|
| Books/chapters | FR-BOOK-001..005, FR-CHAP-001..004 | VR-004 | `main.py`, `lib/books.py` |
| Extraction | FR-EXT-001..006 | VR-004 | `lib/epub_extract.py` |
| AI prompt/contract | FR-GEN-001..003, FR-AI-001..007, FR-ASK-001..003 | VR-005, VR-006 | `lib/ai_prompt.py`, `prompts/*` |
| Pack schema/validation | FR-PACK-001..006, FR-VAL-001..004 | VR-001, VR-006 | `lib/pack.py` |
| Study/learn-first | FR-STUDY-001..006 | VR-004 | `lib/study.py`, `lib/lab.py` |
| Revise/quiz/parsons | FR-REV-001..002, FR-QUIZ-001..003, FR-PAR-001..003 | VR-004 | `lib/revise.py`, `lib/quiz.py`, `lib/parsons.py` |
| Lab/test (AI-made, verifiable) | FR-LAB-001..004, FR-TEST-001..004 | VR-003, VR-004, VR-008 | `lib/lab.py` |
| SRS/stats/export | FR-SRS-001..004, FR-STAT-001..003, FR-EXP-001..002 | VR-002, VR-004 | `lib/srs.py`, `lib/stats.py`, `lib/export_md.py` |
| Interfaces | IF-CLI-001..008, IF-TUI-001..006, IF-SW-001..004, IF-HW-001, IF-COM-001 | VR-004, VR-005, VR-007, VR-009 | `main.py`, `lib/*` (keys in `lib/keys.py`), `tui/` |
| Quality | NFR-PERF-001..004, NFR-REL-001..003, NFR-USE-001..004, NFR-MAIN-001..003, NFR-SEC-001..004 | VR-001..007 | whole tree |

New requirements added later **MUST** extend this table. Requirements removed **MUST** retain their IDs as `withdrawn` and **MUST NOT** be renumbered.

---

## Appendix A — Glossary (supplement to §1.4)

- `book-slug`: filesystem-safe book identifier.
- `source_ref`: human-readable pointer to the source book location (chapter + pages if known).
- `concept`: telemetry tag shared across checks/cards to compute weak spots.
- `gen_notes.md`: optional human record of AI interrogation answers.

## Appendix B — Requirement ID index (v0.3.1)

Functional: FR-TREE-001, FR-BOOK-001..005, FR-CHAP-001..004, FR-EXT-001..006, FR-GEN-001..003, FR-AI-001..007, FR-ASK-001..003, FR-VAL-001..004, FR-TEST-001..004, FR-PACK-001..006, FR-STUDY-001..006, FR-REV-001..002, FR-QUIZ-001..003, FR-PAR-001..003, FR-LAB-001..004, FR-SRS-001..004, FR-STAT-001..003, FR-EXP-001..002.
Mapping: MAP-001..005 (normative selection rules in §4.7).
Interfaces: IF-CLI-001..008, IF-TUI-001..006, IF-SW-001..004, IF-HW-001, IF-COM-001.
Nonfunctional/constraints: NFR-PERF-001..004, NFR-REL-001..003, NFR-USE-001..004, NFR-MAIN-001..003, NFR-SEC-001..004, CR-ENV-001..004, CR-DES-001..005, CR-GEN-001..003, AS-001..004 (assumptions, non-verifiable).
Verification: VR-001..009.

## Appendix C — Pilot suggestion (non-normative)

Pilot with a C book — one language example, not the product scope (e.g. `Fluent C` or K&R-style text lawfully possessed): Ch.1 (tooling/syntax) exercises `fillblank`+`order`; pointers/memory chapter exercises `predict`+`why-fails`+`ascii-viz`; strings/algorithms chapter exercises `predict`+`micro-lab`. This spread demonstrates every REQUIRED interaction kind at least once, satisfying §8.2(3).

## Appendix D — Recorded deviations and deferrals (normative ledger)

Per §0(2) and §8.2(5): everything below is an explicit, justified deviation —
no silent gaps. Each entry is either *amended* (spec text already adjusted
above) or *deferred* (spec keeps the MUST; implementation follows later).
Nothing here may be closed without a spec edit.

| ID | Requirement | Status | Reason / plan |
|----|-------------|--------|---------------|
| D-01 | FR-GEN-003 draft flagging | Resolved in v0.5.3 | `draft: true` warn / strict-fail; GENERATE.md instructs it. |
| D-02 | FR-QUIZ-001 `--concept` filter | Resolved in v0.5.0 | Exact tag match via `filter_checks`, combinable with sample/seed. |
| D-03 | FR-QUIZ-002 breakdown/weakest-3 | Resolved in v0.5.0 | In-memory `tally` per concept + weakest line at end of run. |
| D-04 | FR-QUIZ-003 sampled item IDs | Resolved in v0.4.1 | `quiz_runs.items` JSON column + legacy migration; tests/test_progress.py. |
| D-05 | FR-VAL-003 `from_block` check | Resolved in v0.4.1 | `INTERLEAVE-BLOCK` via preload blockmap; unloadable chapters stay chapter-level. |
| D-06 | FR-TEST-002 interactive execution | Amended | Gate judges recorded evidence (last quiz + lab probe) instead of running `final_checks`/hidden suites live. Rationale: deterministic, pipe-friendly; revisit for proctored use. |
| D-07 | FR-SRS-002 `e` card edit | Resolved in v0.5.1 | $EDITOR round-trip or inline prompts; persists immediately. |
| D-08 | FR-STAT-001 concepts/lab/streak | Partially resolved in v0.5.0 | Per-concept table + weakest concepts via `answers.concept` (migrated); lab state + streaks still deferred. |
| D-09 | FR-LAB-001 `d` diff view | Resolved in v0.4.1 | Loop retains last result; `d` shows output/diff/diagnostics. |
| D-10 | FR-LAB-003 hashes/retention | Resolved in v0.5.1 | `solutions` table (SHA-256 dedup) + `--no-save-solution` flag. |
| D-11 | FR-SRS-003 interleaved top-up | Resolved in v0.5.1 | Up to 2 checks from mastered chapters after cards; answers logged. |
| D-12 | FR-SRS-004 tunability | Resolved in v0.5.2 | `TERMLEARN_*` env layer with fallback-to-default; documented in manual. |
| D-13 | FR-BOOK-002 author/mastery cols | Resolved in v0.4.1 | Author + passed/pack mastery via progress helpers. |
| D-14 | FR-CHAP-001 status/due/lab cols | Resolved in v0.4.1 | Status/due/lab-state columns via progress helpers. |
| D-15 | FR-VAL-004 `--fix-hints` | Resolved in v0.5.3 | Advisory `suggest_fixes` + `--fix-hints` flag; verdicts untouched. |
| D-16 | IF-CLI-005 pagination | Resolved in v0.5.3 | `lib/pager.py` paragraph-snapping --more in study/revise. |
| D-17 | NFR-MAIN-002 coverage | Resolved in v0.4.1 | Measured: pack 85 / srs 88 / lab 82 branch; NFR promoted to MUST. |
| D-18 | FR-TEST-004 net/GUI detection | Resolved in v0.5.3 | NET/GUI pattern scans; net fails strict, GUI stays WARN-only. |
| D-19 | FR-EXP-001 file output | Resolved in v0.4.1 | `--out` writes file; tests/test_export.py. |
| D-20 | NFR-PERF-001/002/003 | Resolved in v0.5.3 | startup 182ms / validate 368ms / run_c 34ms / keypress 0.002ms — all within bounds. |
| D-21 | FR-REV-001 objectives header | Amended | Revise renders explain/examples/bugs; objectives live in `study` + `export`. Revisit if users miss them. |
| D-22 | FR-EXT-003 validate ingestion | Resolved in v0.5.3 | validate prints EXT-SOURCE WARNs (informational, all modes). |

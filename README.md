# termlearn — terminal interactive learning from technical books

See `docs/SRS.md` (IEEE 29148 + RFC 2119, normative).

## Quickstart

Launch the interactive Textual TUI:
```bash
pip install -r requirements.txt
python main.py                # launches modern TUI with Vim navigation
```

Or run headless CLI modes:
```bash
python main.py books                  # list books (FR-BOOK)
python main.py chapters --book extreme-c
python main.py extract --book extreme-c
python main.py gen-prompt --book extreme-c --chapter ch01 [--mode master|quiz|study|all]
python main.py split --book extreme-c --chapter ch01    # split monolithic YAML to modular folder
python main.py validate --book extreme-c [--chapter ch01] [--strict]
python main.py study --book extreme-c --chapter ch01
python main.py revise --book extreme-c --chapter ch01
python main.py quiz --book extreme-c --chapter ch01
python main.py parsons --book extreme-c --chapter ch01
python main.py lab --book extreme-c --chapter ch01
python main.py test --book extreme-c --chapter ch01
python main.py srs --book extreme-c
python main.py stats --book extreme-c
python main.py export --book extreme-c --format md
```

## Language-Agnostic Interactive Learning Palette

`termlearn` combines cognitive learning science with active terminal interactivity across any programming language:
- **`trace`**: Stepped Notional Machine state tables (trace variables/memory addresses across execution steps).
- **`order` (with `faded: true`)**: Faded Parsons problems (order scrambled logic + fill in masked syntax tokens).
- **`spot-bug`**: Authentic diagnostic debugging (inspect compiler/sanitizer logs, highlight the faulty line, select the fix).
- **`subgoals`**: Worked examples labeled with cognitive subgoal banners to reduce split-attention effect.
- **Pluggable Runner Verbs**: AI-authored per-book runners supporting `run check`, `run exec`, and optional `run inspect` (live symbols/disassembly/AST via `i` hotkey).

## Layout (SRS §2.5)

- `main.py` — CLI routing & TUI app launcher
- `lib/` — core domain logic, pack validator, and runner dispatch
- `tui/` — modern Textual TUI screens, custom TCSS themes, and interactive widgets
- `books/<slug>/source.epub` — source truth; `raw_chapters/*.txt` + `meta.json` generated
- `packs/<slug>/book.yaml` + `chNN.yaml` or `chNN/` directory — AI-generated teaching packs (sole runtime source)
- `prompts/<slug>/chNN-prompts/` — modular AI generation prompts (meta, study, quiz, labs, cards, test)
- `prompts/GENERATE.md`, `ASK_USER.md` — normative AI generation contract
- `docs/` — specifications (`docs/SRS.md`, `docs/INTERACTIVE_LEARNING_SPEC.md`, `docs/USER_MANUAL.md`)
- `tests/` — automated test suite (`pytest`)

Pilot book: `books/extreme-c/source.epub` (Extreme C).


# termlearn User Manual

Learn any technical book without opening it — in your terminal. (The C book
in the examples below is just the pilot: the same flow serves Python,
networking, math, or any other text — see §3b.)

## 0. The 30-second version

```bash
pip install -r requirements.txt
python main.py books                          # what do I have?
python main.py chapters --book extreme-c      # what's inside?
python main.py study --book extreme-c --chapter ch04   # learn
```

Stuck on any key? Press **`?`** — every interactive prompt answers it.

## 1. Install

- Linux (or macOS/WSL), Python 3.11+, plus your book's toolchain for labs.
  Pilot toolchain is `gcc` (C books) — everything except compile-and-run
  works without any toolchain at all.
- `pip install -r requirements.txt` (add `--break-system-packages` only if
  your distro Python demands it — PEP 668 systems do).
- No network, no API keys, no build step. All state stays on your disk:
  code in `~/Apps/termlearn/`, progress in
  `${XDG_DATA_HOME:-~/.local/share}/termlearn/progress.db`.

## 2. Add a book

1. Make a folder: `books/<slug>/` (lowercase, hyphens, e.g. `extreme-c`).
2. Copy your lawfully-possessed EPUB there as `source.epub`.
3. Extract: `python main.py extract --book <slug>`
   → `meta.json` + `raw_chapters/ch01.txt …`. Re-running refuses to
   overwrite; add `--force` to re-extract (old output is timestamp-backed-up).
4. Read a chapter as text any time: it's just Markdown-ish `.txt` with code
   blocks preserved.

## 3. Turn a chapter into a course (the AI loop)

The app teaches from `packs/<slug>/chNN.yaml` — YAML you generate once per
chapter with any AI chat:

```bash
python main.py gen-prompt --book <slug> --chapter ch04 > /tmp/gen.md
```

1. Paste `/tmp/gen.md` into your AI chat. It contains the normative
   `GENERATE.md` instructions, the `ASK_USER.md` questions, and the chapter.
2. **Answer the AI's 6 questions** (level, depth, prioritize/skip, lab
   difficulty, language, interleaved review) — or say `use defaults`.
3. The AI first posts an **audit trail** (idea-unit count, code-box
   dispositions), then one `yaml`-fenced block. Save the fence contents to
   `packs/<slug>/ch04.yaml` (create `packs/<slug>/book.yaml` index first —
   copy the pilot's shape).
4. `python main.py validate --book <slug> --chapter ch04 --strict`
   Must print `OK`. Fix what it names (`file: CODE: message`); `--strict`
   treats warnings (missing viz, weak conceptual ratio) as errors.

What the AI was instructed to build (so you know what to demand): one concept
per block with a functional title, worked example → completion → lab arc,
conceptual `why`-questions over verdict questions, distractors from real
misconceptions, stepwise memory diagrams for mental-model blocks, atomic
flashcards, 2+ interleaved review questions from older chapters. If a pack
feels like trivia, send it back citing `prompts/GENERATE.md §3`.

## 3b. Other languages and non-code books

C/`gcc` above is the pilot example, not the product scope. For any other
book, answer the AI's toolchain question with your runner (e.g. `python3`,
`node`, `go run`) and declare it once in `packs/<slug>/book.yaml`:

```yaml
toolchain: {lang: python, run: [python3], timeout_s: 2}
```

`validate` probes only languages with a local runner (C today) and notes —
never fails — the rest; labs in other languages run in your own toolchain
while the app tracks scores, hints, and gates. Books with no executable code
at all (theory, protocols) simply omit labs: tracing-by-hand, ordering, and
explain-in-plain-English carry the chapter.

### Runners: how other languages execute (AI-authored, per book)

Only C runs built-in. For any other language the AI authors
`packs/<slug>/runner/run` (executable, any shebang) next to the YAML,
implementing two verbs that print one JSON object each (full contract:
`docs/SRS.md` §4.9, auto-appended to every generation prompt):

- `run check <src>` → `{"ok": bool, "diagnostics": "..."}` (parse/compile gate)
- `run exec <src> --expect <file> --timeout <s>` → `{"passed", "output", "timed_out", "returncode"}`

`book.yaml: toolchain:` names it (`runner: runner/run`) plus `version_cmd`
(diagnostic probe), `timeout_s`, and `smoke` hello-world vectors. `validate`
smoke-tests the runner (shape/output violations fail), scans its source with
the destructive-command denylist, and prints the toolchain version. Dispatch
order: built-in C → generated runner → explicit "run it in your toolchain"
message (never a crash, never silent). Review the runner file like you review
the YAML — it executes learner code, sandboxed to a temp dir with timeouts.

## 3c. The Textual UI (`main.py tui`)

Same packs, same progress DB as the CLI — a full-screen alternative, not a
fork. Launch with `python main.py tui [--book SLUG]`.

- Navigate: Home (books) → Enter → Chapters → Enter → chapter menu
  (1 study, 2 revise, 3 quiz, 4 parsons, 5 lab, 6 test, 7 cards, 8 stats).
- Every screen shows its keys in the Footer bar; **`?`** opens the key
  overlay anywhere (Esc closes it); **`q`** goes back (Home quits).
- Quiz: buttons or `1-4` for choices (focus jumps to Next after answering,
  so `n` always advances); type + Enter for blanks/ordering; `n` continues.
- Cards: `f` flip, `e` edit (saves immediately), `1-4` grade; interleaved
  review from mastered chapters follows the due queue automatically.
- Lab: editable code pane, `r` run, `t` hidden tests (+snapshot), `h` hints.
- Mouse works, but nothing needs it — all keys mirror the CLI.
- Prefer pipes, screen readers, or SSH without a TTY? The Rich CLI is the
  `--plain` linear mode: identical content, top-to-bottom text.

## 4. Learn: the modes

Flow: pick book → pick chapter → pick mode. `study` is the main path; the
rest harden, prove, and maintain.

| Mode | Command | What happens |
|------|---------|--------------|
| study | `study --book B --chapter C` | Objectives → idea → runnable example (`r`) → memory stepper → micro-checks with instant `why` + remediation. Progress saved per block. |
| revise | `revise --book B --chapter C` | Notes + examples + common bugs. No scoring. |
| quiz | `quiz --book B --chapter C [--sample N] [--seed S] [--concept TAG]` | Checks shuffled (`--seed` reproduces); `--concept` drills one tag. Score + per-concept breakdown saved. |
| parsons | `parsons --book B --chapter C` | Ordering-only: type `3 1 2`, distractors named when picked. |
| lab | `lab --book B --chapter C [--no-save-solution]` | Edit starter in `$EDITOR`, compile+run, hidden tests, progressive hints. `t` records a SHA-256 solution snapshot (skipped with the flag). |
| test | `test --book B --chapter C [--force]` | Chapter gate: recorded quiz% + lab. `--force` advances but is logged. |
| srs | `srs [--book B]` | Due flashcards across chapters (SM-2). Empty = all books. |
| stats | `stats --book B` | Per-block and per-concept accuracy, weakest spots (with representative blocks), recent runs, SRS due. |
| export | `export --book B [--chapter C] --format md` | Markdown notes (hidden tests excluded). |
| books/chapters | `books`, `chapters --book B` | Library pickers with pack coverage. |

## 5. Keys (also via `?` anywhere)

Global: **`?`** help · **`q`** quit (saves first — a crash loses at most the
in-flight question).

| Where | Keys |
|-------|------|
| quiz choice | `1-N` answer |
| quiz fillblank / micro-lab | type text · `r` runs the code (micro-lab) |
| quiz trace | `n` next step · `p` prev step · type value or `1-N` for target cell |
| quiz spot-bug | `j`/`k` select buggy line · `1-N` choose diagnosis and patch |
| parsons | numbers `3 1 2` · `s` reshuffle · `h` hint |
| faded parsons | `Tab` switch between line ordering and blank fields · type token |
| study example | `r` run · `i` inspect toolchain (symbols/disasm/AST) · `Enter` continue |
| study viz | `n` next step · `s` skip chapter-viz |
| study remediation | `y` re-show example · `N` move on |
| lab | `e` edit · `r` run · `t` hidden tests (+snapshot) · `d` last diff · `i` inspect · `h` hint |
| srs | `f` / `Space` flip · `e` edit card · `1` forgot `2` hard `3` good `4` easy |

Keys are single letters, mnemonic (`r`un, `e`dit, `h`int, `s`kip/`s`huffle,
`n`ext, `f`lip), identical across modes. `?` and `help` are reserved — they
always print help, never count as answers.

## 6. Accessibility

- Honors `NO_COLOR` (plain output) automatically; never means anything by
  color alone — every verdict also says the word (`correct`, `FAIL`, `PASS`).
- Linear interaction: prompts never redraw the screen, so output pipes and
  screen readers consume it top-to-bottom. `export` gives you the same content
  as Markdown for reading elsewhere.
- Everything is keyboard-only by construction; no mouse needed now or in the
  planned Textual UI (which will keep a plain linear mode).

## 7. Troubleshooting

| Symptom | Fix |
|---------|-----|
| `No pack for B/C yet` | Run the §3 AI loop, save YAML, `validate`. |
| `validate` prints `ERR …` | Read the code: `CHECK-ANSWER` = answer index out of range; `ORDER-PERM` = bad `answer_order`; `LAB-COMPILE` = starter doesn't build (paste `stderr` to your AI). |
| `gcc not found` / lab won't run | Install the pilot toolchain (C books). Study/quiz/revise work regardless; other languages use their own runner (§3b). |
| `raw_chapters already has content` | Re-run `extract` with `--force` (backs up first). |
| Start over | `stats --book B --reset [--chapter C]` — types `DELETE` to confirm. |
| Piped input aborts (`Aborted.`) | The pipe ran dry — every prompt consumes a line, including `y/N` remediations after wrong answers and viz steps. Count prompts or answer interactively. |

## 8. How progress works

Every answer is logged locally (timestamp, book/chapter/block, correct,
latency) — the offline analogue of the Rust-book quiz profiling. `stats`
turns it into per-block accuracy and weakest concepts; `srs` schedules cards
by SM-2 (1 day → 6 days → scaled intervals; a failed card resets). Tune it
without code edits: `TERMLEARN_EASINESS_INIT` (2.5), `TERMLEARN_EASINESS_MIN`
(1.3), `TERMLEARN_INTERVAL_1_DAYS` (1), `TERMLEARN_INTERVAL_2_DAYS` (6).
Quiz runs and test gates are timestamped, so `test` judges recorded evidence, and
`--force` overrides are on the record.

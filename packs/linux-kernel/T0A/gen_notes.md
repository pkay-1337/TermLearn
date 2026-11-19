# T0A Authoring Notes

Status: chapter-pack authoring notes. These notes are not learner-facing and are not
required by the pack runtime.

## Evidence inventory

| ID | What it proves |
|----|----------------|
| E-T0A-01 | GCC version and a shell command transcript in the workload directory. |
| E-T0A-02 | GNU Make version in the same workload directory. |
| E-T0A-03 | Clean `gcc -std=c99 -Wall -Wextra -g main.c -o app` compile, followed by successful `./app` output `5`. |
| E-T0A-04 | `./app` prints `5` and the harness records exit 0. |
| E-T0A-05 | bad.c diagnostic: line/column, three missing semicolons in the source, two reported errors, warning, exit 1. |
| E-T0A-06 | `make clean` runs `rm -f app` and exits 0. |
| E-T0A-07 | `make` rebuilds `app` with the recorded compile recipe and exits 0. |
| E-T0A-08 | `size app` columns: text 1502, data 584, bss 8, dec 2094, hex 82e. |
| E-T0A-09 | Git untracked -> staged -> committed -> clean status, with commit `f71d88d`. |
| E-T0A-10 | Git short status ` M hello.c` and unified diff with hunk `@@ -1,4 +1,4 @@`. |
| E-T0A-11 | SHA-256 hashes of the exact `main.c`, `Makefile`, and `bad.c` inputs. |

`manifest.json` status: `captured`. Transcript and artifact paths are present.
No unknown evidence IDs are referenced by the pack.

## Idea units

- A transcript exposes command text, output, and exit status as separate observations.
- `./app` is an explicit path form; a bare `app` would be resolved by PATH rules.
- The workload never inspects arguments, so no `argc`/`argv` claim is made.
- stdout, stderr, and exit status are separate channels; printed text is not the status byte.
- A GCC invocation has a command name, flags, source file, and output filename.
- `-g` adds debug metadata; `-o` chooses the executable name; omitting `-o` yields `a.out`.
- A compiler diagnostic names file, line, column, severity, and message before the program runs.
- The first diagnostic can be caused by a missing token on the preceding line; the exact
  bad.c has three missing semicolons on lines 5, 6, and 7, but the captured run reports
  only the first error and an end-of-input error.
- Make rebuilds from target/prerequisite timestamps and recipe lines.
- `make clean` and `make` produce different, predictable actions on the same tree.
- `.PHONY` is standard Make semantics for symbolic targets; it is taught as general
  tool behavior, not as a captured claim.
- `size` reports text/data/bss and total columns; bss records reserved zeroed memory rather than stored zero bytes.
- Git has working tree, index, and commit-graph states visible in short status.
- Unified diff headers describe old/new line ranges and removed/added lines.
- Symptom-to-action triage must use the lifecycle stage of the observed failure.

## Block-to-evidence map

```text
b1 <- E-T0A-01, E-T0A-03, E-T0A-04, E-T0A-09
  objective: read command form, printed output, and recorded exit status from a transcript.
  misconception: printed output and exit status are the same observation.

b2 <- E-T0A-04, E-T0A-05
  objective: separate program output, diagnostic text, and exit code.
  misconception: text on stderr is the exit status.

b3 <- E-T0A-03
  objective: construct and explain the captured GCC invocation.
  misconception: flags are decorative rather than state-changing options.

b4 <- E-T0A-05
  objective: read the first compiler diagnostic, make one minimal repair, rerun, and repeat for the two remaining terminators.
  misconception: the line named in a diagnostic is always the line that must be edited.

b5 <- E-T0A-02, E-T0A-06, E-T0A-07
  objective: predict make rebuild/up-to-date decisions from targets and prerequisites.
  misconception: make always recompiles every time it runs.

b6 <- E-T0A-06, E-T0A-07 plus general Make semantics
  objective: use .PHONY to keep symbolic targets from being treated as files.
  misconception: every make target name is a real file on disk.

b7 <- E-T0A-08
  objective: interpret size columns and connect bss to zero-initialized memory.
  misconception: bss reserves disk space equal to its runtime size.

b8 <- E-T0A-09
  objective: track working tree, index, and commit state transitions.
  misconception: git add creates a commit or stages the whole future working tree.

b9 <- E-T0A-10
  objective: read short-status columns and unified diff headers.
  misconception: a diff hunk header is a line number of the changed line only.

b10 <- E-T0A-03, E-T0A-05, E-T0A-06, E-T0A-07, E-T0A-08, E-T0A-09, E-T0A-10
  objective: choose a diagnostic action from the lifecycle stage of an observed symptom.
  misconception: random flag changes are a valid debugging strategy.
```

Tool semantics not directly visible in a transcript, such as PATH lookup internals,
shell redirection rules, `.PHONY`, ELF/DWARF details, and `git diff --staged`, are
presented as notional-machine explanations anchored to the observed
command/output/exit-code pairs. They are not presented as newly captured evidence.

## Source and code-box disposition

- `main.c`, `Makefile`, `bad.c`, `size app`, and git output come from the T0A bundle
  and the pinned hashes in E-T0A-11.
- Lab 1 uses `bad.c` exactly as captured, including missing semicolons on lines 5, 6, and 7. No adaptation.
- Lab 2 starter Makefile is intentionally incomplete; the completed recipe matches E-T0A-07.
- Lab 3 starter `hello.c` and verification workflow mirror E-T0A-09/E-T0A-10.
- Kernel source is out of scope for T0A; no `sources/early-history.git` or harness claims are used.
- C examples use `lang: c`; command/output/source excerpts use `lang: text`.

## Interleaving

T0A is the first chapter, so it has no earlier chapter to interleave from. Two checks
revisit earlier blocks with `from_block`; no check uses a self-referential
`from_chapter: T0A`.

## Learner-facing text

Raw evidence IDs appear only in `meta.source_ref` and in this authoring note.
Question stems, explanations, cards, lab instructions, and final checks use
descriptive references such as "the captured diagnostic" rather than evidence IDs.

## Open questions

None for the captured claims.

## Validation

```bash
python main.py validate --book linux-kernel --chapter T0A --strict
```

Lab lifecycle: untouched starters fail for both `commands.run` (`r`) and
`commands.test` (`t`); reference solutions make both pass.

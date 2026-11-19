# Checks After Creating a Linux-Kernel Chapter

**Read and execute this checklist immediately after creating or editing a `linux-kernel` chapter pack, and before declaring the chapter complete.** Do not stop at schema validation: verify evidence fidelity, source fidelity, pedagogy, self-containedness, and lab lifecycle below.

This is the local adaptation of `prompts/checks_after_chapter_creation.md` for the Linux-kernel book. Use it together with `BLOCK_AUTHORING.md`, `PLAN.md`, `SOURCES.md`, `ENVIRONMENT.md`, `TINKERING.md`, `docs/SRS.md` §4.8, and `prompts/GENERATE.md`. If this file conflicts with `docs/SRS.md`, the SRS wins; if it conflicts with a vague memory of a textbook or kernel subsystem, this file wins.

Run the strict validator at the end:

```bash
python main.py validate --book linux-kernel --chapter <id> --strict
```

It must exit with code 0 and zero errors.

## 1. Output Structure and Book Registration

- [ ] All required files exist under `packs/linux-kernel/<id>/`: `meta.yaml`, `study.yaml`, `quiz.yaml`, `labs.yaml`, `cards.yaml`, and `test.yaml` (or the documented monolithic equivalent).
- [ ] An authoring-only `gen_notes.md` exists and records the evidence-to-block map, idea-unit count, and code-box/source-snippet disposition.
- [ ] YAML parses successfully; required keys are present; there are no unknown top-level keys.
- [ ] `kind:` and `type:` use only their exact allowed vocabularies.
- [ ] `meta.book` is `linux-kernel`, and `meta.chapter_id` matches the chapter directory/file stem, including uppercase IDs such as `T0A` and `A1`.
- [ ] The chapter `id` is registered in `packs/linux-kernel/book.yaml` `order:` and `chapters:`.
- [ ] `books/linux-kernel/meta.json` remains consistent with the pack book slug and title.
- [ ] `meta.source_ref` is present and points to the correct evidence bundle, pinned source, or source path for this chapter.
- [ ] `meta.prereqs` match `PLAN.md` and `packs/linux-kernel/book.yaml`; no chapter depends on a later chapter.
- [ ] There are 1–6 falsifiable, measurable learning objectives; no objective says only “understand”, “know”, “learn”, or “appreciate”.
- [ ] Every `answer:` is a valid 0-based index; every `answer_order:` has at least two unique valid indices with distractors omitted.
- [ ] No pack is still marked `draft: true`.

## 2. Evidence-First Gate

- [ ] An evidence bundle exists at `curriculum/linux-kernel/evidence/<chapter>/` before chapter prose is written.
- [ ] `manifest.json` has a definite status such as `captured`, names `transcript.md`, and lists every artifact used by the chapter.
- [ ] `transcript.md` contains the actual stdout/stderr and exit codes for every command-backed claim.
- [ ] Every evidence ID used in the pack exists in the chapter manifest.
- [ ] Every factual claim in `explain_md`, `why`, lab instructions, cards, and final checks traces to an evidence ID, a pinned source path, or an explicitly marked contrast/enrichment.
- [ ] Worked outputs are copied from captured output, with only volatile fields normalized.
- [ ] No output, flag, diagnostic, register value, packet path, line number, or behavior was invented to make a nicer story.
- [ ] If evidence is missing or ambiguous, `gen_notes.md` records an open question instead of the chapter guessing.
- [ ] Raw evidence IDs are kept in `meta.source_ref` and authoring notes, not sprinkled into learner-facing stems unless the ID is genuinely part of the diagnostic artifact.
- [ ] Evidence remains author-time provenance for the AI author; it is not required to appear as a learner-facing UI panel.

## 3. Source-of-Truth Fidelity

- [ ] Tooling chapters use actual tool runs from the chapter evidence bundle as their source of truth.
- [ ] Kernel chapters cite `sources/early-history.git@<tag-or-commit>` for pristine historical source claims.
- [ ] Runtime build/boot/gdb claims from the modified harness cite `sources/Linux-0.11-fork@<commit>` and are not presented as pristine source behavior.
- [ ] Modern-kernel claims cite the pinned `sources/linux-*` tree and version declared in `SOURCES.md`.
- [ ] Source line references use `commit:path:line` or an explicit tag/path form; no vague “somewhere in the kernel” claims.
- [ ] Kernel excerpts use `lang: text` or `lang: asm`, never `lang: c`.
- [ ] Source snippets are exact or marked `adapted: true` with a reason in `gen_notes.md`.
- [ ] A code path teaches the handoff: entry → function → state mutation → callee/return → observable effect.
- [ ] A structure teaches owner, lifetime, key fields, invariant, and failure mode if the invariant breaks.
- [ ] Boot/assembly blocks name the current execution context and what state is or is not available yet.
- [ ] Modern source is not read into old-kernel explanations except as an explicitly marked contrast.

## 4. Self-Contained Questions and Checks

- [ ] Every block check, quiz question, card, lab instruction, and explanation is understandable without the book, plan, or evidence bundle open.
- [ ] Questions and `why:` explanations contain **zero** references to chapters, books, examples, code boxes, listings, figures, exercises, problem numbers, or unseen material, except valid `from_chapter`/`from_block` review metadata.
- [ ] Any question about code, output, state, a bug, or a kernel path embeds the complete code, transcript, path excerpt, or full concrete scenario.
- [ ] No question depends on remembering constants, defaults, flags, source lines, register values, or implementation details that are not shown.
- [ ] Explanations teach the principle directly and may cite an internal block ID, not an external book location.
- [ ] The pack does not claim an evidence item proved something the transcript/manifest does not contain.

## 5. Every Block Check and Quiz Question

- [ ] Rule 1.1: stem is positively worded, not a confusing negative or verdict question.
- [ ] Rule 1.2: 2–4 choices, with 3 preferred.
- [ ] Rule 1.2b: choices in one set are roughly uniform in length and grammatical form; the correct answer is not identifiable by being the longest or shortest (aim for max/min length ratio ≤1.3, and keep the correct option within 20% of the longest distractor).
- [ ] Rule 1.3: the correct answer index is within bounds.
- [ ] Rule 1.4: correct answers are distributed across positions 0, 1, 2, and 3, not mostly or entirely `0`.
- [ ] Rule 1.5: fully self-contained with embedded code, output, source excerpt, or concrete scenario.
- [ ] Rule 1.6: `why:` gives the core principle and explicitly names the misconception trapped by every distractor.
- [ ] Rule 1.7: `kind:` is exactly one of `mcq`, `predict`, `why-fails`, `fillblank`, `order`, `trace`, `spot-bug`, `eipe`, `choose-better`.
- [ ] Rule 1.8: `order` lines are scrambled; `answer_order` uses the correct pool indices and excludes paired distractors. The stem states how many correct lines to place, or says all displayed lines are used; when a distractor is present, the stem says so (e.g. "Order the 5 correct lines; one line is a distractor").
- [ ] Rule 1.9: `fillblank` has exactly one load-bearing token, the program/command is visible in `code:`, and the answer is not `?` or `help`. The answer is one word/token; if a multi-word expression or a line is unavoidable, the stem states the exact answer format (e.g. "Answer format: `res->field`" or "Answer format: one line of C code").
- [ ] Rule 1.10: prose is at most 120 columns; code lines have no column cap.
- [ ] Each block has 5–10 scaffolded checks appropriate to its depth.
- [ ] Checks cover several cognitive actions: recognition, prediction, ordering, diagnosis, discrimination, and transfer.
- [ ] At least two checks interleave earlier blocks; for chapters after the first, at least two use earlier chapters with valid `from_chapter` and `from_block`.
- [ ] The first chapter does not fake interleaving with self-referential `from_chapter` to itself.
- [ ] At least half of the choice checks test concepts, mechanisms, diagnosis, or contrast rather than pure recall.
- [ ] `predict` checks name the tracing strategy and include state-by-state reasoning where required.
- [ ] `trace` checks include a valid trace table; `spot-bug` checks include an authentic diagnostic log where relevant.
- [ ] `eipe` and `choose-better` checks compare relational alternatives or design trade-offs, not isolated facts.
- [ ] Distractors come from real misconceptions: wrong tool for symptom, right tool wrong scope, wrong source version, compile-time vs runtime confusion, wrong current state, or fix that hides the cause.

## 6. Study Content, Code, and Diagrams

- [ ] Every idea unit in the chapter is accounted for as taught, checked, or explicitly deferred in `gen_notes.md`.
- [ ] Each block has one falsifiable objective and one explicit notional machine.
- [ ] `model` blocks have prediction/diagnosis plus a state or structure artifact.
- [ ] `syntax` blocks have order/fillblank plus a failure mode.
- [ ] `algorithm` blocks have trace/order/micro-lab.
- [ ] `design` blocks have `eipe` or `choose-better`.
- [ ] `explain_md` follows the five-job recipe: frame, notional machine, worked case, boundary, compressed rule.
- [ ] Every idea is taught causally: what changes state, what observes it, what can go wrong, and why the evidence has that shape.
- [ ] Every `blocks[].example.code` compiles, assembles, parses, or runs correctly under the declared `book.yaml` toolchain where applicable.
- [ ] Every declared `run_expected` matches actual stdout byte-for-byte for a correct execution.
- [ ] Non-C textual excerpts use `lang: text`; assembly uses `lang: asm`; no kernel source excerpt is mislabeled as `lang: c`.
- [ ] Every non-trivial example has a self-contained 2–6 line `explain_md`.
- [ ] `diagram` stanzas use valid kinds, resolvable node/edge references, no ANSI escapes, and at most six steps.
- [ ] Truncated source material is not silently completed or invented.

## 7. Tool-Chapter Mastery

Use this section for `T0*` tool chapters, `T1*` debugger chapters, and tooling capstones.

- [ ] Each tool block answers: what the tool observes, what it cannot observe, smallest useful workload, important columns/fields, noise filter, controlled failure, confirming second signal, and choosing symptom.
- [ ] There is a real question before the tool is used; the lab is not “run this command and paste output”.
- [ ] Each tool lab includes a prediction, one controlled change, one observed difference, one failure-mode question, and a teach-back prompt.
- [ ] Output fields and columns are explained from the captured evidence, not from memory.
- [ ] Filters remove noise without hiding the signal.
- [ ] At least one second signal confirms or challenges the first tool observation.
- [ ] The chapter teaches when the tool is the wrong instrument for the symptom.
- [ ] No lab merely demonstrates a command without requiring diagnosis or transfer.

## 8. Kernel-Chapter Mastery

Use this section for `A*`, `M*`, and modern networking/kernel chapters.

- [ ] Every source claim names the pinned tree, tag/commit, path, and line where relevant.
- [ ] Canonical source evidence and runtime harness evidence are never mixed in one unexplained claim.
- [ ] Boot, syscall, scheduling, memory, filesystem, and packet-path blocks name the state before and after the handoff.
- [ ] Structures include owner, lifetime, key fields, invariant, and failure mode.
- [ ] Assembly/context blocks say what registers, stack, memory, or services are available at that point.
- [ ] Claims about historical versions do not assume modern behavior unless explicitly marked as contrast.
- [ ] Observed runtime behavior comes from QEMU/gdb/trace/capture evidence and cites the harness source, not pristine tree source.

## 9. Quiz

- [ ] The quiz contains 30–50 standalone questions.
- [ ] `intro`, `core`, and `advanced` levels are all present and balanced.
- [ ] Questions are interleaved, not grouped by level or concept.
- [ ] No quiz stem is identical to any block-check stem.
- [ ] Coverage spans the chapter's core themes and includes synthesis, edge cases, and diagnostic discrimination.
- [ ] Quiz items do not cite evidence IDs merely to look grounded; any cited artifact must actually support the answer.
- [ ] Every quiz item satisfies all rules in section 5.

## 10. Labs, Core/Stretch, and Tinker

- [ ] There is no fixed lab cap; the chapter has as many labs and lab families as the material requires.
- [ ] Every lab begins with a plain-language **What You Are Building** section that explains the behavior without jargon.
- [ ] Each lab declares `tier: core` or `tier: stretch`; core labs are required and stretch labs are optional depth.
- [ ] `family`, `difficulty`, `expected_observation`, `artifacts`, and `environment` are present when useful and match the observed evidence.
- [ ] Write `instruction_md` as an unambiguous contract: exact behavior, commands, expected output, state transition, and boundary case.
- [ ] Name the exact API signatures, constants, and struct fields to use; define vague terms such as "size", "handle", "object", and "survives", and avoid ambiguous pronouns or "handle it appropriately" wording.
- [ ] Specify the order of validation when multiple errors can apply (for example, size-before-fullness and capacity-before-emptiness), plus the expected result for empty, full, zero-length, maximum-size, invalid, and closed cases.
- [ ] Include one concrete worked example or exact expected `run` transcript, and verify it does not contradict evidence, headers, hints, tests, or the reference solution.
- [ ] Ask whether two reasonable implementations could differ observably; if yes, add the missing tie-breaker, ordering rule, or lifecycle detail to `instruction_md`.
- [ ] Each lab has `id`, `title`, complete `instruction_md`, non-empty safe files, at least one of `commands.run`, `commands.test`, or `commands.tinker`, `test_cases[].expect`, and 1–3 progressive hints.
- [ ] Student implementation files are blank or TODO-stubbed; headers, drivers, scripts, and test runners are complete.
- [ ] On untouched starter files, both `commands.run` (TUI `r`) and `commands.test` (TUI `t`) fail for the intended reason.
- [ ] Reset removes generated artifacts and hidden state from prior attempts, so a solved workspace returns to fail-first.
- [ ] Commands contain no destructive operations, network access, unbounded waits, or workspace escapes.
- [ ] Interactive `commands.tinker` is tested; TUI/CLI instructions use `x`, not `t`, for tinker.
- [ ] Tinker commands inherit stdio, run in the lab workspace, and obey the denylist.
- [ ] Environment labels are advisory and never grant privileges automatically.
- [ ] Hints progress from general to specific to concrete operation.
- [ ] A real reference solution makes `commands.run` output byte-match `test_cases[].expect` and `commands.test` exit 0.
- [ ] With that reference solution, both TUI `r` and `t` change from fail to pass.
- [ ] Observation notes, if used, stay in the lab workspace and do not affect scoring or gate state.
- [ ] If the chapter has no executable code, labs are omitted and the reason is recorded in `gen_notes.md`.

## 11. Cards and Mastery Test

- [ ] Cards are atomic, have one fact/contrast/procedure each, and are answerable in under 10 seconds.
- [ ] Card fronts are concise; backs contain the answer plus a one-line why.
- [ ] Cards include `why`/`when` retrieval, not only `what` recall.
- [ ] Cards do not depend on evidence IDs or unseen artifacts.
- [ ] There are no multi-part cards or “list all...” cards.
- [ ] Every card has a descriptive `concept:` tag.
- [ ] `test.gates` reference real block IDs and have sensible `min_quiz` thresholds.
- [ ] `test.final_checks` reference valid checks and represent chapter-level mastery.
- [ ] Final checks use only commands, tools, flags, source paths, and behaviors taught or explicitly marked as transfer from earlier chapters.

## 12. Toolchain, Runner, and Safety

- [ ] The pack teaches the correct language/toolchain from `packs/linux-kernel/book.yaml`.
- [ ] For C content, no runner script is emitted and `example.lang`/`lab.lang` are `c` unless the excerpt is text or assembly.
- [ ] `toolchain:` includes `runner`, `version_cmd`, and `smoke` where required by the spec.
- [ ] No pre-solved solution is present anywhere in a lab or prompt.
- [ ] No command uses `rm -rf`, `curl`, `wget`, `ssh`, `mkfs`, fork bombs, `dd if=`, `chmod 777`, `shutdown`, or `reboot`.
- [ ] QEMU, gdb, tracing, and network-namespace commands are bounded and do not require automatic root escalation.
- [ ] Artifact paths stay inside the intended evidence/workspace directories.

## 13. Final Acceptance

- [ ] `gen_notes.md` reports evidence ID coverage, idea-unit count, source-path disposition, and code-box disposition: taught, checked, or deferred.
- [ ] Every open question is resolved or explicitly marked unresolved for human review.
- [ ] No unresolved warnings remain.
- [ ] `python main.py validate --book linux-kernel --chapter <id> --strict` returns exit code 0 with zero errors.
- [ ] Only after all checks above pass: mark the chapter complete.

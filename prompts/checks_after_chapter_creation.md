# Checks After Creating a Chapter

**Read and execute this checklist immediately after creating or editing a chapter pack, and before declaring the chapter complete.** Do not stop at schema validation: verify the content, pedagogy, self-containedness, and lab lifecycle below.

Run the strict validator at the end:

```bash
python main.py validate --book <slug> --chapter <id> --strict
```

It must exit with code 0 and zero errors.

## 1. Output Structure and Schema

- [ ] All required files exist: `meta.yaml`, `study.yaml`, `quiz.yaml`, `labs.yaml`, `cards.yaml`, and `test.yaml` (or the documented monolithic equivalent).
- [ ] YAML parses successfully; required keys are present; there are no unknown top-level keys.
- [ ] `kind:` and `type:` use only their exact allowed vocabularies.
- [ ] `meta.book` matches the pack slug, and `meta.chapter_id` matches the chapter directory/file stem.
- [ ] `meta.source_ref` is present, and every block inherits or refines it where appropriate.
- [ ] There are 1–6 falsifiable, measurable learning objectives; prerequisites are correct.
- [ ] Every `answer:` is a valid 0-based index; every `answer_order:` has at least two unique valid indices with distractors omitted.
- [ ] No pack is still marked `draft: true`.

## 2. Self-Contained Questions and Checks

- [ ] Every block check, quiz question, card, lab instruction, and explanation is understandable without the book open.
- [ ] Questions and `why:` explanations contain **zero** references to chapters, books, examples, code boxes, listings, figures, exercises, problem numbers, or any unseen material.
- [ ] Any question about code, output, state, or a bug embeds the complete code via `code: |` or spells out the full concrete scenario and declarations in the stem.
- [ ] No question depends on remembering constants, defaults, or implementation details that are not shown in the question.
- [ ] Explanations teach the principle directly and may cite an internal block ID, not an external book location.

## 3. Every Block Check and Quiz Question

- [ ] Rule 1.1: stem is positively worded, not a confusing negative or verdict question.
- [ ] Rule 1.2: 2–4 choices, with 3 preferred.
- [ ] Rule 1.2b: choices in one set are roughly uniform in length and grammatical form; the correct answer is not identifiable by being the longest or shortest (aim for max/min length ratio ≤1.3, and keep the correct option within 20% of the longest distractor).
- [ ] Rule 1.3: the correct answer index is within bounds.
- [ ] Rule 1.4: correct answers are distributed across positions 0, 1, 2, and 3, not mostly or entirely `0`.
- [ ] Rule 1.5: fully self-contained with embedded code and no external references.
- [ ] Rule 1.6: `why:` gives the core principle and explicitly names the misconception trapped by every distractor.
- [ ] Rule 1.7: `kind:` is exactly one of `mcq`, `predict`, `why-fails`, `fillblank`, `order`, `trace`, `spot-bug`, `eipe`, `choose-better`.
- [ ] Rule 1.8: `order` lines are scrambled; `answer_order` uses the correct pool indices and excludes paired distractors. The stem states how many correct lines to place, or says all displayed lines are used; when a distractor is present, the stem says so (e.g. "Order the 5 correct lines; one line is a distractor").
- [ ] Rule 1.9: `fillblank` has exactly one load-bearing token, the program is visible in `code:`, and the answer is not `?` or `help`. The answer is one word/token; if a multi-word expression or a line is unavoidable, the stem states the exact answer format (e.g. "Answer format: `res->field`" or "Answer format: one line of C code").
- [ ] Rule 1.10: prose is at most 120 columns; code lines have no column cap.
- [ ] Each block has 5–10 scaffolded checks appropriate to its depth.
- [ ] At least two interleaved checks use valid `from_chapter` and `from_block` metadata.
- [ ] At least half of the choice checks test concepts, mechanisms, diagnosis, or contrast rather than pure recall.
- [ ] `predict` checks name the tracing strategy and include a state-by-state `why` where required.
- [ ] `trace` checks include a valid trace table; `spot-bug` checks include an authentic diagnostic log where relevant.
- [ ] `eipe` and `choose-better` checks compare relational alternatives rather than isolated facts.

## 4. Study Content, Code, and Diagrams

- [ ] Every idea unit in the chapter is accounted for as taught, checked, or explicitly deferred in the audit trail.
- [ ] Every chapter code box is quoted verbatim or marked `adapted: true` with a note explaining what changed.
- [ ] External knowledge is absent unless marked `enrichment: true` with a source.
- [ ] Every `blocks[].example.code` compiles cleanly under the declared `book.yaml` toolchain.
- [ ] Every declared `run_expected` matches actual stdout byte-for-byte for a correct execution.
- [ ] Every non-trivial example has a self-contained 2–6 line `explain_md`.
- [ ] Explanations make the Notional Machine explicit: line-by-line state, memory mutations, and the reason the code works.
- [ ] Model blocks have stepped `viz`; design blocks have `eipe` or `choose-better`; syntax/algorithm blocks have `order`.
- [ ] `diagram` stanzas use `kind: flow|art`, have resolvable node/edge references, contain no ANSI escapes, and have at most six steps.
- [ ] Truncated source material is not invented; provisional blocks are marked `adapted: true` with a note.

## 5. Quiz

- [ ] The quiz contains 30–50 standalone questions.
- [ ] `intro`, `core`, and `advanced` levels are all present and balanced.
- [ ] Questions are interleaved, not grouped by level or concept.
- [ ] No quiz stem is identical to any block-check stem.
- [ ] Coverage spans the chapter's core themes and includes synthesis, edge cases, and diagnostic discrimination.
- [ ] Every quiz item satisfies all rules 1.1–1.10.

## 6. Labs

- [ ] Every lab begins with a plain-language **What You Are Building** section (or equivalent heading) that explains, without jargon, the object or behavior the student will create and how it behaves; the technical requirements follow after it.
- [ ] **Write `instruction_md` as an unambiguous contract.** Assume the implementer sees only this text. Every required behavior, return value, error code, state transition, and boundary case must be stated explicitly, not inferred from headers, hints, tests, or the reference solution.
- [ ] Name the exact API signatures, constants, and struct fields to use; define vague terms such as "size", "handle", "object", and "survives", and avoid ambiguous pronouns or "handle it appropriately" wording.
- [ ] Specify the order of validation when multiple errors can apply (for example, size-before-fullness and capacity-before-emptiness), plus the expected result for empty, full, zero-length, maximum-size, invalid, and closed cases.
- [ ] Include one concrete worked example or the exact expected `run` transcript, and confirm the instructions do not contradict the headers, hints, tests, or reference solution.
- [ ] Ask: "Could two reasonable implementations differ in observable behavior?" If yes, add the missing tie-breaker, ordering rule, or lifecycle detail to `instruction_md`.
- [ ] Each lab has `id`, `title`, a complete `instruction_md`, non-empty safe files, `commands.run`, `commands.test`, `test_cases[].expect`, and 1–3 progressive hints.
- [ ] Student implementation files are blank or TODO-stubbed; headers, drivers, and test runners are complete and compilable.
- [ ] Running `commands.test` on untouched starter files fails for the intended reason.
- [ ] Commands contain no destructive operations, network access, unbounded waits, or workspace escapes.
- [ ] Hints progress from general to specific to concrete operation.
- [ ] A real reference solution makes `commands.run` output byte-match `test_cases[].expect`.
- [ ] With that reference solution, the lifecycle changes from fail to pass.
- [ ] If the book has no executable code, labs are omitted and the reason is recorded in the audit trail.

## 7. Cards and Mastery Test

- [ ] Cards are atomic, have one fact/contrast/procedure each, and are answerable in under 10 seconds.
- [ ] Card fronts are concise; backs contain the answer plus a one-line why.
- [ ] Cards include `why`/`when` retrieval, not only `what` recall.
- [ ] There are no multi-part cards or "list all..." cards.
- [ ] Every card has a descriptive `concept:` tag.
- [ ] `test.gates` reference real block IDs and have sensible `min_quiz` thresholds.
- [ ] `test.final_checks` reference valid checks and represent chapter-level mastery.

## 8. Language and Runner

- [ ] The pack teaches the correct language/toolchain from `book.yaml`; C is not assumed for non-C books.
- [ ] For a C book, no runner script is emitted and `example.lang`/`lab.lang` are `c`.
- [ ] For a non-C book, `packs/<slug>/runner/run` is executable, has a shebang, and implements the documented runner protocol.
- [ ] `toolchain:` includes `runner`, `version_cmd`, and `smoke` where required by the spec.
- [ ] No pre-solved solution is present anywhere in a lab or prompt.

## 9. Final Acceptance

- [ ] The audit trail reports idea-unit count and code-box disposition: taught, checked, or deferred.
- [ ] No unresolved warnings remain.
- [ ] `python main.py validate --book <slug> --chapter <id> --strict` returns exit code 0 with zero errors.
- [ ] Only after all checks above pass: mark the chapter complete.

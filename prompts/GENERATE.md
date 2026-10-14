# GENERATE.md — normative AI instructions for chapter → YAML packs
# (Implements docs/SRS.md FR-AI-001..007; output schema docs/SRS.md §4.8.
#  Read with prompts/ASK_USER.md. The docs/SRS.md §4.8 schema excerpt and the
#  docs/SRS.md §4.9 runner-protocol excerpt are appended to this prompt text;
#  every other docs/SRS.md cross-reference below cites its path explicitly.)
#
# LANGUAGE POLICY (MUST): this system is language-agnostic. It teaches ANY
# technical book — Python, networking, math, C, anything. Whenever these
# instructions name C / `gcc` / pointers, that is ONE worked example of the
# general contract, never the product scope. For the book in front of you,
# substitute its language and toolchain into every rule below: `example.lang`
# names the language, `lab` runs in it, hidden tests check it. If the book has
# no executable code at all (theory, protocols, math), OMIT labs/micro-labs
# and spend the weight on tracing-by-hand (`predict`), `order`, `eipe`, and
# `choose-better` instead — say so in the audit trail.
#
# Every per-mode rule below is grounded in cited learning-science findings.
# Rules marked MUST/SHOULD follow RFC 2119. Do not soften them.

You turn ONE pasted book chapter (plain text, code kept verbatim) into ONE
chapter YAML file for the `termlearn` terminal course. The learner will study
ONLY from your YAML — never from the book. Teach, don't summarize.

### Source paths you are working with (MUST respect)

- `docs/SRS.md` — the normative spec. Its §4.8 (pack schema) and §4.9
  (runner protocol) excerpts are appended to this prompt; treat them as
  binding. All other `docs/SRS.md` references below name their section.
- `prompts/ASK_USER.md` — interrogate the user per that file first.
- `books/<slug>/raw_chapters/<id>.txt` — the pasted chapter source.
- `packs/<slug>/` — where your YAML lands as `<id>.yaml`, plus
  `packs/<slug>/runner/run` when you must author a runner (§7).

## 0. Output envelope + full-coverage protocol (MUST)

- First interrogate the user per ASK_USER.md. MUST NOT emit final YAML until
  the user answers or says `use defaults`.
- Then output exactly ONE `yaml`-fenced block with the full chapter file.
  Surrounding prose goes OUTSIDE the fence and is ignored by the parser.
- If you emit without interrogation answers (user said nothing and gave no
  defaults), set top-level `draft: true` — validators flag drafts and strict
  mode fails them (docs/SRS.md FR-GEN-003).
- Keys MUST stay English. `kind`/`type` values MUST be exactly the vocabularies
  below — anything else fails validation.

### 0.1 Read everything; skip nothing (MUST)

- Read the ENTIRE pasted chapter before writing a single block — beginning to
  end, including intros, asides, footnotes, shell sessions, and every code box.
  Skimming to the "main" sections is a defect.
- FIRST, enumerate every checkable idea unit in the chapter (one line each:
  concept, procedure, fact, warning, example). This mirrors the idea-unit
  method retrieval research uses to score understanding (Karpicke & Blunt 2011:
  texts are divided into idea units; each must be recallable).
- THEN group idea units into blocks (block = one single-concept teaching
  unit, docs/SRS.md §4.8). Every idea unit MUST be either
  taught in a block, practiced in a check/card/lab, or listed under an explicit
  `deferred:` note with a reason (e.g. "needs Ch.5 heap model — forward ref").
  Silent omission is a defect. The validator cannot check this; your enumeration
  (pasted OUTSIDE the fence, before the YAML) is the audit trail.
- Every code box in the chapter MUST be either quoted verbatim as a block
  `example`, turned into a check (predict/order/fillblank/micro-lab), or
  deferred with reason. Count them and say the count in the audit trail.

## 1. Fidelity (MUST)

- Use ONLY concepts/APIs present in the pasted chapter. External knowledge
  MUST NOT appear as fact unless marked `enrichment: true` with its own source.
- Book code examples MUST be verbatim. If you trim for terminal length, set
  `adapted: true` and say what was cut. Trimmed examples MUST still compile
  where the book's did.
- Every file MUST set `meta.source_ref` (e.g. `Ch.1 pp.1-20`) and every block
  SHOULD inherit/refine it. `meta.book` MUST equal the pack slug,
  `meta.chapter_id` MUST equal the file stem (`ch04.yaml` → `ch04`).
- **Self-Contained Questions & Checks (MUST)**: When authoring quizzes, checks,
  labs, or flashcards, NEVER refer or point to questions, exercises, or problem
  numbers in the book (e.g. NEVER write "Refer to question 3 in the book",
  "See exercise 4", or "As asked in Problem 5"). The learner studies ONLY
  from your YAML in the terminal and does not have the book open. You MUST put
  the entire question with its full background scenario, code snippet, and context
  directly inside the question prompt/stem.

## 2. Blocking: one concept per block (MUST)

- Split the chapter into concept-dependency order: each block teaches exactly
  ONE new falsifiable skill (e.g. `& takes an address`, not `pointers`).
- Block shape: `id, type, title, explain_md (5-15 lines Markdown, ≤120 cols),
  example? (≤30 lines, ≤80 cols), viz? (for model), checks[>=1], common_bugs?`.
- `type` MUST be one of `model | syntax | design | algorithm` (meanings in the docs/SRS.md §4.6 table).
- Each block title MUST be a functional subgoal label, NOT a comment:
  [Research: subgoal labels group procedure steps under their purpose, cut
  cognitive load, and improve transfer (Catrambone 1998; Margulieux et al.
  2012–2016, d≈.2–.3). Labels describe what the steps ACHIEVE
  ("Swap through a copied address"), never what they literally do
  ("Use temp variable"). Giving labels beats asking novices to invent them.]

## 3. Per-mode directives — what to author and why

### 3.1 `predict` — trace first, because tracing precedes writing (MUST for model/algorithm)

- [Research: tracing + explaining skill explains 46% of variance in later
  performance, and tracing is a prerequisite step before writing (Lopez et al.
  2008; Lister's hierarchy: pre-tracing → tracing → post-tracing → writing).
  Novices trace poorly and linearly; experts follow execution order (ITiCSE
  studies; Busjahn eye-tracking). Teaching an explicit line-by-line +
  memory-table strategy takes 5–10 minutes and measurably improves tracing
  (Xie et al. 2017).]
- Every `predict` MUST name the tracing strategy in the stem: e.g.
  "Trace line by line, tracking `var` and `ptr`: ...". For pointer/state
  questions, point at the block's `viz` steps ("use the memory steps above").
- Distractors MUST be the classic tracing failures: stale value (pre-store),
  address/value confusion (`&var` vs `var` vs `*ptr`), off-by-one, skipped
  first element, wrong branch taken. Never random numbers.
- One `predict` per model block MINIMUM; the `why` MUST walk the trace
  (state after each line), not just assert the answer.

### 3.2 `mcq` / `why-fails` — distractors from misconceptions, three options (MUST)

- [Research: distractors built from real student misconceptions give far higher
  reliability and discrimination (KR-20 .81 vs .40) and distractor efficiency
  than teacher-invented ones (M distractor-functionality study 2026; Gierl et
  al. 2017 review). Three options are optimal — a 4th is usually an unselected
  filler (80-year meta-analysis; Haladyna & Downing: "three options may be a
  natural limit"). A distractor is functional only if >5% of learners pick it.
  Negatively-worded stems ("which is NOT...") threaten validity (PARE 2017).
  Ordered/diagnostic MCQ turns each distractor into misconception data
  (Briggs et al. 2006). Choice order is randomized at runtime, so author
  answers in any position.]
- 2–4 choices per question (3 preferred). EVERY distractor MUST name the
  misconception it traps, in `distractor_why`-style reasoning inside `why`
  (e.g. "B traps address/value confusion: `&var` is where it lives, not what
  it holds"). A distractor you cannot attach to a named misconception MUST be
  cut — filler options are worse than fewer options.
- Stems MUST be positively worded and fully self-contained. NEVER refer to
  questions or exercises in the book — always embed the complete question,
  scenario, and code context directly into the prompt. Prefer `why`/`why-fails`
  over `whether`: conceptual questions discriminate; verdict questions do not
  (Brown Rust-book experiment, 62k readers: ask WHY it fails, not WHETHER it compiles).
- ≥half of choice checks per chapter SHOULD be conceptual (`why-fails`,
  mechanism, contrast) rather than recall.

### 3.3 `fillblank` — program completion, not trivia (SHOULD for syntax)

- [Research: for novices, COMPLETING a given program beats GENERATING one from
  scratch (van Merriënboer 1990 — the completion effect). Completion is the
  mid-fade step between studying an example and solving independently.]
- Blanks MUST be load-bearing tokens (`&`, `*`, format spec, operator, keyword),
  exactly one per check, with the full program visible in `code`. The `why`
  MUST state the rule that determines the token (not "the answer is &").
- Never blank two interdependent tokens in one check; never blank names the
  learner could not derive (no trivia).
- `answer_text` MUST NOT be `?` or `help` (reserved: the app intercepts them
  to show key help, IF-CLI-006).

### 3.4 `order` (Parsons) — paired distractors, execution feedback (MUST for syntax/algorithm)

- [Research: 2-D Parsons with paired distractors takes significantly less time
  than fixing or writing the same code, with equal learning and 1-week
  retention (Ericson et al. 2017). Distractors force attention to details —
  without them learners place blocks without reading (ITiCSE 2024). Paired
  distractors (buggy twin next to correct line) give desirable difficulty;
  unpaired/random mixing is harder; more distractors = harder (Ericson, Denny,
  Ihantola & Karavirta). Parsons scores correlate highly with write-code
  scores. Help progression that works: remove a distractor → give indentation
  → merge two blocks (adaptive Parsons, Ericson et al. 2018–19). Faded Parsons
  (blank-inside-block) bridges toward writing (Fromont et al. 2023). Caution:
  distractors can overload very young novices — always pair them.]
- `lines` = author-scrambled pool INCLUDING 1–2 distractor lines;
  `answer_order` = pool indices of the correct lines in execution order
  (distractors omitted). Distractors MUST be authentic near-misses from the
  chapter (missing `&`, wrong format, off-by-one, swapped operands) — each
  with a `distractor_why` naming the bug class.
- Provide `hint` that orients without giving order ("find the line that
  creates storage first"). The block's `why` MUST explain the ordering
  principle (data flow / execution order), so the learner gains a sequencing
  schema, not one puzzle solution.
- Order tasks MUST follow a worked `example` of the same pattern earlier in
  the block (fade: study intact → assemble scrambled → write in lab).

### 3.5 `eipe` — relational answers only (SHOULD for design/algorithm)

- [Research: self-explanation prompts give g≈.55 across conditions (Bisra et
  al. 2018 meta-analysis, 69 effects). Explaining BEFORE predicting beats
  predicting first; explanation volume predicts learning; it works across prior
  knowledge. EiPE answers at the relational (purpose) level vs line-by-line
  (multistructural) level differentiate comprehenders; relational skill
  correlates with writing skill (Corney, Murphy, Fowler et al.). Assisted
  prompts beat open prompts with multiple representations. Prompts must align
  with the target outcome and ask about GIVEN code, not the learner's own
  choices (Rittle-Johnson constraints). Terminal grading can't score prose —
  hence options form — but the options MUST preserve the relational-vs-literal
  discrimination.]
- Correct option MUST state purpose/goal without jargon ("exchanges the two
  callers' values through their addresses"). Distractors MUST be
  line-by-line paraphrases ("sets a to 5 then returns") and plausible
  wrong-purpose summaries — the exact confusions novices produce.
- Stem MUST say: "in one sentence, what is this code FOR?" Never "what does
  line 3 do?" (that rewards multistructural reading).

### 3.6 `choose-better` — compare examples, mine the contrast (SHOULD for design)

- [Research: comparing correct vs incorrect worked examples drives principle
  learning (Booth et al.). Contrasting cases teach discrimination between
  similar concepts — the same mechanism behind interleaving benefits
  (discriminative-contrast).]
- The two options MUST differ by exactly one design decision from the chapter
  (`NULL` vs `0`, function vs macro, check-then-use vs use-then-check).
  The `why` MUST state the principle AND its boundary ("prefer functions —
  except measured hot paths, aligned with the team").

### 3.7 `micro-lab` + `lab` — fade to independence, hint in levels (MUST run; SHOULD fade)

- [Research: worked-example effect is robust for novices (Sweller & Cooper);
  guidance MUST fade as expertise grows or it becomes harmful redundancy
  (expertise reversal: Kalyuga; guidance-fading: Renkl et al. 2004; adaptive
  fading beats fixed: Salden et al. 2010). Sequence per skill: intact example →
  completion/faded → full problem. Feedback levels that work: knowledge of
  result → where it failed → elaborated how-to-fix tied to the misconception
  (Narciss & Huth; Haldeman). Hint design: 4 levels from orientation to
  bottom-out snippet, one problem at a time, economy of words (LLM Hint
  Factory, Hou et al. 2024, after Shute 2008 + Cognitive Tutor). For Parsons/
  ordering tasks, execution-based feedback beats arrangement feedback
  (Helminen et al. 2013). Timing: immediate vs delayed feedback differs
  negligibly on average (g=.03, 2024 meta-analysis) — immediate elaborated
  feedback is safe and more efficient.]
- Block arc MUST be: `example` (intact, studied) → `order`/`fillblank`
  (completion) → `micro-lab`/`lab` (independent). A lab that demands skills
  with no prior faded step MUST be re-scoped.
- Runnable contract (language-agnostic): every `example` with `run_expected`
  and every `lab.starter_c` (name it `starter.<ext>` mentally — the key stays
  `starter_c` for schema stability) MUST run under the book's declared
  toolchain with `book.yaml: toolchain:` (example: C →
  `compile: [gcc, -Wall, -std=c99]`; Python → `run: [python3]`; adapt the
  COMMAND, never weaken the rule: compiles/runs clean, 2 s default timeout,
  temp dir, no shell interpolation of learner code).
  Hidden tests MUST check behavior (output/exit/state), never trivia; first
  failing case MUST map to a hint. `hints[]` MUST be ordered general →
  specific (1. where to look, 2. what rule applies, 3. the operation/shape —
  never the full solution until the last hint).
- `run_expected` on examples SHOULD be exact stdout so predict-run-observe
  closes the loop: predict first, then run, then explain any mismatch.
  For non-executable books, `predict` means trace-by-hand against the book's
  own worked traces, and `run_expected` is OMITTED (never invented).

### 3.8 `viz` — external memory, not decoration (SHOULD for every model block)

- [Research: sketching program state / memory tables offloads working memory
  and cuts retrieval errors during tracing (Xie et al. 2017). Verbal + visual
  codes combine additively (dual coding: Paivio). Experts "doodle" execution;
  novices must be taught the habit (ITiCSE tracing studies).]
- `steps[]` MUST show state AFTER each executed line (var values, pointer
  targets, null-ness), 2–6 steps, aligned with the block's `example` line
  order. A viz that merely restates prose MUST be cut.

### 3.9 `cards` — atomic retrieval units (SHOULD ≥3 per fact-dense chapter)

- [Research: retrieval practice beats elaborative studying for meaningful
  learning (Karpicke & Blunt 2011, Science; retrieval-specific mechanisms,
  not just elaboration). Texts are scored as atomic idea units — cards MUST
  match that grain: one fact/contrast/procedure each. Learners underestimate
  retrieval and avoid it (metacognition: Karpicke) — so packs MUST supply
  cards rather than hoping learners make them. Elaborative-retrieval hybrids
  (why/when cards, not just what) are preferred.]
- Front = single question answerable in <10s; back = answer + 1-line why.
  Include `why/when` cards ("WHEN must a pointer be NULL-initialized?")
  alongside `what` cards. No multi-part cards, no "list all…" cards.

### 3.10 `why` + interleaving on every check (MUST)

- `why` is elaborated feedback, not answer reveal [Research: response-specific
  elaborated feedback beats verification-only (Shute 2008; Corbett &
  Anderson)]. Every `why` MUST contain: (a) the principle, (b) which
  misconception each distractor trapped, (c) a pointer back to the block/
  `source_ref`. "The answer is B" alone is a defect.
- Every chapter SHOULD include ≥2 interleaved checks with `from_chapter` +
  `from_block` [Research: interleaving forces discrimination between similar
  concepts — e.g. `*p++` vs `(*p)++`, `malloc` vs `calloc` — which blocked
  practice never teaches (Rohrer; discriminative-contrast). Spacing falls out
  of interleaving for free.]

## 4. Lab + test gates (SHOULD; verifiable)

- Chapters with code SHOULD include `lab: {title, prompt_md, starter_c,
  tests_sh|tests, hints[1-3]}` per §3.7 (`starter_c` keeps its key name for
  schema stability in every language). `tests_sh` MUST NOT need
  network/GUI/unbounded time; MUST NOT contain destructive commands
  (examples: `rm -rf`, `curl`, `wget`, `ssh`, `mkfs`, fork bombs).
- Chapters that gate advancement SHOULD include `test: {gates: [{needs:
  [block ids], min_quiz: 80}], final_checks: [...]}` referencing real blocks.

## 5. Runner authoring — only when the book's language has no local runner (MUST follow docs/SRS.md §4.9)

- The app ships exactly one built-in runner: C. If the book in front of you
  is C, SKIP this section entirely — set `example.lang: c` / `lab.lang: c`
  and declare the C toolchain.
- Otherwise you MUST author `packs/<slug>/runner/run` (executable, shebang
  line) implementing the appended docs/SRS.md §4.9 protocol exactly:
  `run check <src>` → one-line `{"ok", "diagnostics"}` JSON;
  `run exec <src> --expect <file> --timeout <secs> [--stdin <file>]` →
  one-line `{"passed", "output", "timed_out", "returncode"}` JSON;
  exit 0 on correct protocol operation even for failing verdicts.
- Prohibitions (validator scans for these, NFR-SEC-002): no network access,
  no writing outside the supplied temp cwd, no shell-string execution of
  learner code (argument lists only), no unbounded waits (honor `--timeout`,
  and the app kills regardless).
- With the runner you MUST deliver in `book.yaml: toolchain:`: `lang`,
  `runner: runner/run`, `run` reference command, `version_cmd`
  (e.g. `[python3, --version]`), `timeout_s`, and `smoke: {ext, src, expect}`
  hello-world vectors. Before emitting, trace your runner against the smoke
  vectors by hand: check-verb verdict, exec-verb output bytes, JSON shapes.
- Keep the runner SMALL (under ~80 lines): parse/check via the language's own
  compiler (`py_compile`, `node --check`), execute the file as a subprocess
  with timeout, print the JSON. Portability beats features — no dependencies
  beyond the language itself plus POSIX shell utilities.

## 6. Uncertainty handling

- If the pasted text is truncated mid-concept, mark the block
  `adapted: true` + `note: "source truncated; block provisional"` and keep the
  check easy. NEVER invent the missing half.
- If two readings are plausible, pick the book-literal one and note the
  alternative in `why`, not in the question stem.

## 7. Self-check before emitting

1. Audit trail OUTSIDE the fence: idea-unit count, code-box count with
   disposition (taught/checked/deferred) for each. Any unit unaccounted for?
2. Valid YAML, required keys present (docs/SRS.md §4.8, appended below)? `answer` in bounds?
   `answer_order` = ≥2 unique valid indices (distractors omitted)?
3. `kind`/`type` vocabularies exact? No unknown top-level keys?
4. `why` on EVERY check with principle + distractor diagnoses + source pointer?
5. All quizzes, checks, and questions 100% self-contained with full context?
   (Zero references to book questions/exercises like "refer to question 3 in book").
6. Choice counts 2–4 (3 preferred), stems positive, answers in any position?
7. Block arc intact → completion → independent present where a lab exists?
8. Model blocks have stepwise `viz`? Design blocks have `eipe`/`choose-better`?
9. ≥2 interleaved checks with valid `from_chapter`? Cards atomic with why/when mix?
10. Lab runs mentally under the declared toolchain (pilot example flags:
   `-Wall -std=c99`)? Hints general → specific? No destructive commands?
11. Language ≠ C? Runner `run` authored per docs/SRS.md §4.9 (check/exec JSON,
    exit-0 rule, sandbox prohibitions), `toolchain:` carries `runner`,
    `version_cmd`, `smoke`; C book? No runner file emitted.
12. Line lengths sane (prose ≤120, code ≤80)?

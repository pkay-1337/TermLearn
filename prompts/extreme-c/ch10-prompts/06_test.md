# =============================================================================
# INSTRUCTIONS FOR AI AGENT / CHAT: CHAPTER MASTERY TEST GATES
# TARGET OUTPUT FILE: packs/extreme-c/ch10/test.yaml
#
# [SOURCE ASSET LOCATIONS — WHERE TO FIND CHAPTER DATA]
# 1. Extracted Chapter Text: books/extreme-c/raw_chapters/ch10.txt
#    (The full extracted text is also appended at the bottom of this prompt)
# 2. Book Table of Contents & Metadata: books/extreme-c/meta.json
# 3. Book Toolchain & Course Pack Config: packs/extreme-c/book.yaml
#
# [DIRECTIVES FOR test.yaml]
# 1. Define mastery gate criteria referencing prerequisite concept blocks and minimum quiz accuracy.
# 2. OUTPUT FORMAT:
#    test:
#      gates:
#        - needs: [b1, b2, b3]
#          min_quiz: 80
#      final_checks: []
# =============================================================================


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
chapter course pack for the `termlearn` terminal course. The learner will study
ONLY from your YAML — never from the book. Teach, don't summarize.

### Source paths you are working with (MUST respect)

- `docs/SRS.md` — the normative spec. Its §4.8 (pack schema) and §4.9
  (runner protocol) excerpts are appended to this prompt; treat them as
  binding. All other `docs/SRS.md` references below name their section.
- `prompts/ASK_USER.md` — interrogate the user per that file first.
- `books/<slug>/raw_chapters/<id>.txt` — SOURCE CHAPTER TEXT: The raw, extracted
  chapter text lives here on disk (created via `python main.py extract --book <slug>`).
  The full text is also appended directly at the bottom of this prompt.
- `books/<slug>/meta.json` — BOOK METADATA: Table of contents, chapter titles, spine order.
- `packs/<slug>/book.yaml` — COURSE CONFIGURATION: Language toolchain and runner declarations.
- `packs/<slug>/<id>/` — RECOMMENDED MODULAR TARGET DIRECTORY:
  For highest pedagogical depth and to prevent token truncation, author focused
  modular YAML files inside this directory:
  - `meta.yaml` — metadata, prerequisites, and 1–6 falsifiable objectives.
  - `study.yaml` — 6–15 concept blocks, Notional Machine state transitions, and scaffolded checks.
  - `quiz.yaml` — 30–50 dedicated synthesis questions across difficulty levels.
  - `labs.yaml` — 1–4 practical coding workspaces with blank starters and test runners.
  - `cards.yaml` — 15–25 atomic SM-2 spaced repetition flashcards.
  - `test.yaml` — mastery gates and passing thresholds.
- `packs/<slug>/<id>.yaml` — LEGACY MONOLITHIC TARGET FILE: Single unified YAML pack.
- `packs/<slug>/runner/run` — runner script (only when authoring a runner, §5).

## 0. Output destination & protocol (MUST)

- **Target Output**:
  - **Modular Pack (Recommended)**: Create directory `packs/<slug>/<id>/` and write the
    mode files (`meta.yaml`, `study.yaml`, `quiz.yaml`, `labs.yaml`, `cards.yaml`, `test.yaml`).
  - **Monolithic Pack (Legacy)**: Single file `packs/<slug>/<id>.yaml` (e.g. `packs/extreme-c/ch09.yaml`).
  - **Autonomous Agents with Tools**: Write files directly, then validate via:
    `python main.py validate --book <slug> --chapter <id> --strict`
  - **Chat-Only Models**: Output inside single `yaml`-fenced code blocks and state the
    save destination for each file.
- First interrogate the user per ASK_USER.md. MUST NOT emit final YAML until
  the user answers or says `use defaults`.
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

### 0.2 Put All Your Might — Go Plus Ultra (Never Half-Ass) (MUST)

- **The Plus Ultra Standard**: Treat the authoring of this chapter pack as a
  masterwork of pedagogical engineering. The learner studies SOLELY from your
  YAML, without the original book open. Every sentence of explanation and every
  check must carry maximal clarity, depth, and instructional power.
- **Zero Half-Assing & No Placeholders**:
  - NEVER emit placeholders (`TODO`, `...`, `/* rest of code here */`, `etc.`).
  - NEVER write lazy, hand-waving, or dismissive explanations (e.g. "This sets x to 5",
    "Self-explanatory boilerplate", "Standard syntax").
  - NEVER skip code boxes, exercises, diagrams, or tricky corner cases.
  - Dedicate full cognitive and pedagogical might to every single block, code
    example, visualizer, diagnostic check, distractor rationale, and remediation.

### 0.3 Never Worry About Length — Multi-Turn / Multi-Step Protocol (MUST)

- **Length Independence**: Do NOT worry about the length or character count of
  the YAML file! Thoroughness, depth, and pedagogical completeness strictly
  override brevity. A chapter with 8–15 richly explained blocks, deep code breakdowns,
  and 30+ diagnostic checks is vastly superior to a rushed 3-block summary.
- **Never Truncate to Save Tokens**: Never rush, combine distinct concepts, or
  cut code examples to fit into a single response context.
- **Multi-Turn Generation Protocol**:
  - **Autonomous AI Agents (with file-creation / terminal tools)**: If a chapter
    is large or concept-dense, do NOT attempt to rush everything into one tool call.
    Write the initial skeleton and first batch of blocks (e.g. `meta`, `objectives`,
    blocks `b1`–`b4`) to `packs/<slug>/<id>.yaml`. In subsequent turns or tool
    calls, append/insert blocks `b5`–`b8`, `b9`–`b12`, `cards`, `lab`, and `test`.
    Finally run `python main.py validate --book <slug> --chapter <id> --strict`.
  - **Chat-Only Models (no file tools)**: If the chapter is too large to emit in
    one message without hitting token limits, notify the user:
    *"This chapter is being generated in sequential parts to ensure exhaustive,
    untruncated depth."* Emit Part 1 (Meta + Blocks 1–4), then Part 2 (Blocks 5–8),
    then Part 3 (remaining blocks, cards, lab, test). Direct the user to assemble
    them into `packs/<slug>/<id>.yaml`.

### 0.4 Evidence-Based Learning Science & Cognitive Architecture (MUST)

Every instructional decision in this course pack is grounded in peer-reviewed
learning science, cognitive psychology, and computing education research (CER):

1. **Cognitive Load Theory (CLT) & Working Memory Limits** (Sweller 1988, 2011;
   van Merriënboer & Sweller 2005):
   - Novice working memory is strictly limited to 3–4 novel interacting elements.
   - *Intrinsic Load*: The inherent complexity of technical logic (e.g. pointer indirection,
     concurrency, stack layout). Managed by breaking the chapter into single-concept blocks.
   - *Extraneous Load*: Mental waste caused by poor presentation, split attention,
     and jargon without grounding. Minimized by keeping code and explanation spatially
     contiguous, self-contained, and crystal clear.
   - *Germane Load*: Productive mental effort devoted to schema acquisition.
     Maximized through deliberate retrieval practice, contrasting cases, and prediction.

2. **The Notional Machine** (du Boulay 1986; Sorva 2013; Fincher et al.):
   - A Notional Machine is the explicit, conceptual model of the underlying computer
     that executes the code: the call stack, stack frames, heap memory, registers,
     instruction pointer, pointers/addresses, and variable lifetimes.
   - *Novice Failure Mode*: Beginners fail not because of syntax, but because they hold
     vague, magical, or anthropomorphic mental models of execution.
   - *Rule*: Every block MUST make the Notional Machine explicit. Whenever code is
     introduced, explain the physical/virtual state transitions taking place inside
     the machine.

3. **The Block Model for Program Comprehension** (Schulte 2008):
   - Novices comprehend programs across three orthogonal dimensions:
     (a) **Text Surface**: Language syntax, tokens, and grammar.
     (b) **Execution Semantics**: Dynamic runtime operations, state changes, memory mutation.
     (c) **Purpose / Subgoal**: What functional goal this code accomplishes and why it was chosen.
   - Explanations MUST systematically address all three dimensions, never stopping at
     mere surface syntax.

4. **Concrete-Representational-Abstract (CRA) & Dual Coding** (Paivio 1986; Mayer 2009):
   - Connect abstract syntax to visual memory step-throughs (`viz`) and intuitive,
     physical mental models before formalizing abstract syntax and mathematical constraints.

5. **Desirable Difficulties & Retrieval Practice** (Bjork & Bjork 1992; Karpicke & Blunt 2011, Science):
   - Active retrieval practice produces 200%–300% higher long-term retention and conceptual
     transfer than passive reading or highlighting.
   - Interleaving (`from_chapter`) forces discriminative contrast between similar concepts
     (e.g., `*p++` vs `(*p)++`, pass-by-value vs pass-by-reference).
   - Generation effect: filling a blank or ordering scrambled code builds stronger,
     more durable neural schemas than passively observing a solution.

6. **Subgoal Learning & Schema Acquisition** (Catrambone 1998; Margulieux et al. 2016):
   - Novices organize memory around functional goal labels ("Acquire dynamic buffer via address"),
     not mechanical operations ("Call malloc"). Block titles and explanation headers MUST
     be functional subgoal labels.

7. **Spatial Contiguity & Avoiding Split Attention** (Mayer & Moreno 2003):
   - Explanations of code must be immediately adjacent to or integrated with the code,
     so the learner never has to jump back and forth across distant paragraphs.

### 0.5 Comprehensive Code Block Explanations & Notional Machine Walkthroughs (MUST)

- **No Code Without Deep Explanation**: Every single code snippet in `example`,
  `explain_md`, `checks`, or `lab` MUST be accompanied by an exhaustive, intuitive breakdown.
- **Mandatory Explanation Components for Every Code Block**:
  1. **Line-by-Line / Construct Walkthrough**: What each line, keyword, type declaration,
     or expression does in human terms.
  2. **Notional Machine State Transitions**: What happens in memory (stack frames, heap,
     pointers, CPU registers) when this code runs.
  3. **The "Why" Behind the Design**: Why this specific implementation was chosen
     over plausible alternatives (e.g., why pass by address vs by value; why `#define`
     vs `const`; why NULL check before dereference).
  4. **Boundary Conditions & Failure Traps**: What happens if a line is removed, reordered,
     or executed with boundary values (NULL, 0, -1, uninitialized memory, buffer boundaries).

### 0.6 Intuition-First Comprehensibility (MUST)

- **Teach for True Comprehension**: Write with crystal clarity, warmth, and intellectual
  rigor for an ambitious learner studying alone in a terminal.
- **Bridge Jargon with Intuition First**: Introduce difficult concepts (e.g., pointer indirection,
  memory alignment, race conditions, vtables, recursion) by first establishing an intuitive,
  physical mental model (e.g., mailboxes, address books, shared whiteboards) BEFORE
  introducing the formal keywords and syntax.
- **Never Hand-Wave**: Ban phrases like "it is obvious that...", "simply...", or "clearly...".
  If a step is subtle or tricky, slow down and unpack it step-by-step.
- **Address Misconceptions Head-On**: Explicitly name and dismantle the classic
  misconceptions that trip up learners (e.g. confusing the address of a pointer with the address
  it points to).

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
- Block shape: `id, type, title, explain_md, example?, viz?, checks[>=1], common_bugs?`.
  - `explain_md`: Typically 10–25 lines of crystal-clear, comprehensible Markdown (≤120 cols).
    MUST thoroughly unpack the concept, bridge technical jargon with intuitive mental models,
    and walk through the example code and Notional Machine state changes. Never abbreviate or
    cut short to save space; depth and conceptual clarity are paramount.
  - `example`: Verified code snippet (≤35 lines, ≤80 cols), runnable where applicable.
    Every code example MUST have an accompanying breakdown of its lines, memory mutations,
    and design rationale in `explain_md` or check `why`.
    - `subgoals` (OPTIONAL but HIGHLY RECOMMENDED for complex multi-step examples):
      Break code into purposeful functional steps:
      ```yaml
      subgoals:
        - label: "Acquire & Guard Invariant"
          lines: [1, 2]
        - label: "Mutate State"
          lines: [3, 4]
      ```
      [Research: Margulieux & Catrambone 2016 — grouping code lines into functional subgoals
      boosts learner problem-solving transfer by up to 40% and reduces cognitive split-attention.]
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
- **Answer Position Randomization (MUST)**: NEVER default all questions or multiple questions in sequence to `answer: 0`. The correct answer MUST be varied and distributed across all valid choice positions (0, 1, 2, and 3) uniformly throughout the chapter blocks. Any pack where 100% or the vast majority of choice checks have `answer: 0` is defective and will be rejected.
- **Self-Contained Questions & Zero External References (CRITICAL MUST)**:
  Every question stem (`q:`) in block checks and main quiz questions MUST be 100% self-contained.
  STRICTLY PROHIBITED in BOTH question stems (`q:`) AND explanations (`why:`): NEVER reference external book examples, code boxes, listings, or figures (e.g. NEVER write "in Example 7.2...", "in Code Box 7-6...", "in Listing 3...", "as seen in Example 1.17...", "in Figure 4...").
  Learners in a terminal DO NOT have the physical book open in front of them!
  If a question tests code, behavior, state changes, return value, output, or syntax (e.g. `engine_turn_off`, `player_shoot`, constructors), you MUST EMBED the relevant code snippet directly into the check via `code: |` with `lang: c`, or spell out the complete concrete scenario and type declarations in `q:`. Never expect the student to remember an unseen function's internal constants, default values, or implementation details from memory!
  Explanations (`why:`) MUST explain the core technical principle, memory mechanics, or language rule directly (e.g. quoting the specific line of code or guard check shown in the question), rather than citing "per Example X.Y" or "in Code Box X-Y".
- Stems MUST be positively worded. Prefer `why`/`why-fails`
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
- **Pool Scrambling (MUST)**: In all `order` checks, `lines` MUST NOT be in sequential execution order, and `answer_order` MUST NOT be `[0, 1, 2, ...]`. The lines MUST be author-scrambled so the learner performs deliberate sequencing.
- Provide `hint` that orients without giving order ("find the line that
  creates storage first"). The block's `why` MUST explain the ordering
  principle (data flow / execution order), so the learner gains a sequencing
  schema, not one puzzle solution.
- Order tasks MUST follow a worked `example` of the same pattern earlier in
  the block (fade: study intact → assemble scrambled → write in lab).
- **Faded Parsons (`faded: true`)**:
  [Research: Fromont et al. 2023 — Faded Parsons problems require learners to arrange
  lines AND fill in missing critical tokens, providing an optimal intermediate fade
  before authoring code from scratch.]
  ```yaml
  - kind: order
    faded: true
    q: "Order the lines and fill in the missing allocation size argument:"
    lines:
      - "car->speed = 0;"
      - "car_t* car = (car_t*)malloc(_____);"
      - "return car;"
      - "if (!car) return NULL;"
      - "free(car);"
    answer_order: [1, 3, 0, 2]
    distractor_why:
      "free(car);": "Premature deallocation destroys the object during construction."
    blanks:
      - line_idx: 1
        token: "_____"
        answer_text: "sizeof(car_t)"
        accepted: ["sizeof(car_t)", "sizeof(*car)"]
    why: "car_malloc must allocate the byte size of car_t, verify non-null, initialize attributes, and return the instance."
  ```

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

### 3.10 `trace` — stepped Notional Machine memory & state tables (MUST for model/algorithm)

- [Research: Sorva 2013; Lister et al. 2004 — novice programmers fail because they lack
  an accurate mental model of the Notional Machine (invisible memory state, stack frames,
  and pointers). Step-by-step state tracing is the single strongest predictor of programming
  competence.]
- Every `trace` check presents an executable code snippet and a structured table matrix
  tracking variable and memory states across execution lines.
- Schema:
  ```yaml
  - kind: trace
    q: "Trace pointer mutations across execution steps. What is the value at address 0x7ffd01 after Step 3?"
    code: |
      int a = 10;
      int *p = &a;
      *p = 25;
    trace:
      headers: ["Step", "Line", "Variable / Target", "Address", "Value"]
      rows:
        - step: 1
          line: 1
          cells: ["1", "1", "a", "0x7ffd01", "10"]
        - step: 2
          line: 2
          cells: ["2", "2", "p", "0x7ffd08", "0x7ffd01"]
        - step: 3
          line: 3
          cells: ["3", "3", "*p (a)", "0x7ffd01", "???"]
    target: {row: 2, col: 4}
    answer_text: "25"                         # text input mode OR
    choices: ["10", "25", "0x7ffd01", "NULL"] # choice mode
    answer: 1
    why: "Dereferencing *p accesses the memory at &a (0x7ffd01) and mutates the integer stored there from 10 to 25."
    concept: "pointer-deref-state"
  ```

### 3.11 `spot-bug` — authentic diagnostic debugging (MUST for boundary failure modes)

- [Research: Kalyuga et al. — authentic troubleshooting schemata require reading diagnostic
  signals (compiler errors, AddressSanitizer output, stack traces) and mapping them to source lines.]
- Schema:
  ```yaml
  - kind: spot-bug
    q: "Analyze the code and AddressSanitizer report. Which line triggers the heap-use-after-free, and why?"
    code: |
      car_t* c = car_malloc();
      car_free(c);
      c->speed = 100;
    diagnostic_log: |
      ==12345==ERROR: AddressSanitizer: heap-use-after-free on address 0x602000000010
      WRITE of size 4 at 0x602000000010 thread T0
    target_line: 3
    choices:
      - "Line 1: Allocation size was insufficient"
      - "Line 2: car_free called on uninitialized pointer"
      - "Line 3: Mutating field through dangling pointer after memory was freed"
    answer: 2
    why: "AddressSanitizer detects memory write to 0x602000000010 after that address was returned to the heap allocator in line 2."
    concept: "use-after-free"
  ```

### 3.12 `why` + interleaving on every check (MUST)

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

### 3.13 Main Chapter Quiz (`quiz:`) vs. Block Checks (`checks:`) (MUST)

- **Two Distinct Question Arenas**:
  1. `blocks[].checks`: 5–10 immediate, scaffolded checks per block (calibrated according to the topic's depth and complexity) progressively reinforcing the single concept just taught through diverse angles (syntax, state transitions, edge cases, bug traps).
  2. `quiz:` (Top-level chapter list): Dedicated 30 to 50 comprehensive quiz questions spanning the entire chapter.
- **Rules for `quiz:`**:
  - **Count**: 30 to 50 questions per chapter pack.
  - **Levels**: Include questions across three difficulty levels via `level: intro | core | advanced`.
  - **Ordering**: Arrange in NO specific order (mixed difficulty, concept-interleaved) to simulate authentic testing conditions.
  - **Independence**: Quiz questions MUST be distinct from the block checks — test chapter-wide synthesis, edge cases, combined concepts, and diagnostic discrimination.
  - **Code Boxes**: Questions can and should include `code:` blocks where relevant (e.g. predicting output, identifying bugs, analyzing stack/heap behavior) with the question prompt directly referencing the snippet.
  - **Supported Kinds**: Use any valid check kind (`mcq`, `predict`, `why-fails`, `fillblank`, `order`, `eipe`, `choose-better`, `trace`, `spot-bug`).
  - **Feedback**: Every quiz question MUST have an elaborated `why:` explanation citing the underlying principle and diagnosing distractors.

## 4. Multi-Lab Workspaces + test gates (SHOULD; verifiable)

### 4.1 Labs are Practical Tests — Student Action Required (NO Pre-Solved Code; Files Can Be Blank)
- **Pedagogical Purpose**: A lab is an interactive practical exam / problem-solving challenge. The student MUST do the work!
- **Strict Anti-Pattern: NEVER Provide 100% Pre-Solved Solutions**:
  If the student opens the lab and the code is already completely implemented and passes immediately out of the box, there is zero learning value and no challenge for the student.
- **Starter Files Can Be Blank or Scaffolded**:
  - Files that the student is tasked with writing or implementing **MAY BE COMPLETELY BLANK** (e.g. empty string `content: ""`), or scaffolded with function stubs (e.g. `return -1;`, `return NULL;`), struct footprints, and `/* TODO: ... */` tasks.
  - Supporting framework files (such as headers `.h` / interface definitions, interactive driver harnesses `main.c`, and unit test runners `test_runner.c`) define the contract and deterministic assertions so the student's solution can be compiled, tested, and verified.
- **Verification Lifecycle**:
  - When the student first executes `t` (Test) or `r` (Run) on the initial starter files, the tests SHOULD FAIL (displaying compiler errors, failed assertions, or output diffs in the console).
  - Once the student implements the code in the editor, all assertions and test cases pass 100%.

### 4.2 Multi-Lab Workspace Schema & Rules
- Chapters with code SHOULD include a `labs: [...]` array (1 to 4 practical, multi-file
  labs per ISO/IEC/IEEE 29148:2018). Each lab provisions an isolated workspace directory
  at `labs/<book>/<chapter>/<lab_id>/` and MUST provide:
  - `id`: unique identifier (`lab1`, `lab2`, etc.)
  - `title`: descriptive pedagogical title
  - `instruction_md`: complete, self-contained markdown requirements detailing what the student must implement/fix
  - `files`: array of starter files (`path` and `content`), e.g. headers (`.h`), implementations (`.c`), drivers (`main.c`), and unit tests (`test_runner.c`)
  - `commands`: language-agnostic compile/run commands executed in `cwd = workspace_dir`:
    - `run`: interactive build & run command (e.g. `gcc -Wall -Wextra -std=c99 component.c main.c -o app && ./app`)
    - `test`: test runner command executing unit test assertions (e.g. `gcc -Wall -Wextra -std=c99 component.c test_runner.c -o test_runner && ./test_runner`)
  - `test_cases`: input vs. expected output correctness verification array (`name`, `stdin`, `expect`, `expect_exit`). The system executes each test case in the workspace and performs automated unified diffing on mismatch.
  - `hints`: 1–3 progressive hints (general -> specific).
- Prohibited in commands (validator scans for these, NFR-SEC-002): destructive commands
  (`rm -rf`, `curl`, `wget`, `ssh`, `mkfs`, fork bombs), unbounded waits, or escaping the workspace.
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
13. Dedicated top-level `quiz:` stanza authored with 30–50 standalone questions across levels (intro/core/advanced) in no specific order, including code boxes where relevant, distinct from block checks?

## 8. Post-Generation Testing & Verification Protocol (MUST execute after writing YAMLs)

After authoring the YAML files (whether modular under `packs/<slug>/<id>/` or monolithic), the AI agent MUST rigorously verify and test the generated files against this inspection checklist:

### 1. Block Checks & Questions (1.1–1.10)
- **1.1 Positively-worded stem**: `q:` is clearly and positively stated without confusing negative phrasing.
- **1.2 Choice count**: 2–4 options per check (3 preferred).
- **1.3 Answer bounds**: `answer:` is a valid 0-based index (0..len(choices)-1).
- **1.4 Answer randomization**: Correct answers are uniformly distributed across 0, 1, 2, and 3 (never all 0).
- **1.5 100% self-contained**: Code is embedded directly via `code: |`; ZERO external references to book examples/listings/figures (e.g. NEVER write "in Example 7.2" or "in Listing 3").
- **1.6 Elaborated why**: Provides the core principle + explicit misconception diagnosis for every distractor.
- **1.7 Exact vocabularies**: `kind:` is exactly in (`mcq`, `predict`, `why-fails`, `fillblank`, `order`, `trace`, `spot-bug`, `eipe`, `choose-better`).
- **1.8 Scrambled Parsons (`order`)**: Lines scrambled in `lines:`, paired distractors excluded from `answer_order:`, non-sequential order.
- **1.9 Program completion (`fillblank`)**: Single load-bearing token, program visible in `code:`, answer not reserved `?` or `help`.
- **1.10 Line formatting**: Code width ≤80 columns, prose ≤120 columns.

### 2. Quiz Stanza (if `quiz:` present / `quiz.yaml`)
- **Count**: 30–50 dedicated questions.
- **Levels**: `intro`, `core`, and `advanced` all present and balanced.
- **No duplicates**: No question stem (`q:`) identical to any block-check `q:`.
- **Mixed**: Shuffled / interleaved — not grouped monolithically by level or concept.
- **Concept coverage**: Distinct concepts span the chapter's core themes (e.g. for OOP: composition, aggregation, ownership, diagnostics).
- **Checklist conformance**: Each individual item satisfies items 1.1–1.10 above.

### 3. Labs (if `labs:` present / `labs.yaml`)
- **Contract**: Each lab provides `id`, `title`, `instruction_md`, non-empty safe `files`, `commands.run` and `commands.test`, `test_cases[].expect`, and progressive hints.
- **Blank starters**: Implementation file(s) content: `""` or `/* TODO: stub */`; headers, drivers, and test-runners complete and compilable.
- **Fail-first**: Running `commands.test` on the untouched starter files MUST FAIL (missing symbols, undefined references, or assertion compile error).
- **Safe commands**: No denylisted patterns (`rm -rf`, `curl`, `wget`, `ssh`, `mkfs`, fork bombs); strictly no network.
- **Hints ordered**: Progressive hints ordered general → specific → concrete operation.
- **Code width**: All starter and harness code lines ≤80 columns.

### 4. Runnable Code (All Packs / `study.yaml`)
- **Compilation**: Every `blocks[].example.code` compiles cleanly under `book.yaml: toolchain:`.
- **Expected Output**: If `run_expected` is declared, it matches actual stdout byte-for-byte for a correct execution.
- **Pedagogical Archetypes**: Model blocks have `viz`; design blocks have `eipe` or `choose-better`; syntax/algorithm blocks have `order`.

### 5. Cannot Be Fully Automated (Need a Solution Trace)
- **Reference Solution Verification**: `commands.run` output byte-matches `test_cases[].expect` for a reference solution.
- **Fail → Pass Lifecycle**: The fail-then-pass lifecycle is verified with a real reference implementation tested against `commands.test`.

### 6. Automated Validation Command
Execute the strict validator:
```bash
python main.py validate --book <slug> --chapter <id> --strict
```
Ensure exit code 0 with zero errors before concluding.



---

# ASK_USER.md — interrogation template (SRS FR-ASK-001..003)
# The AI MUST ask these BEFORE emitting YAML. MUST NOT emit final YAML until
# the user answers or says `use defaults`.
#
# 1. 100% SELF-CONTAINED QUESTIONS & EXPLANATIONS: NEVER refer to external book examples, code boxes, listings, figures, or exercises in questions OR explanations
#    (e.g. NEVER write "In Example 7.2...", "In Code Box 7-6...", "In Listing 3...", "Refer to question 4 in book").
#    The student is studying in a terminal and does not have the book. Always embed the complete code
#    snippet directly in `code: |` with `lang: c` or write out the entire concrete scenario in `q:`.
#    If a question tests what a function does or its return value, SHOW THE FUNCTION CODE directly in the question.
#    Explanations (`why:`) must explain the underlying mechanics directly, never saying "In Code Box X-Y...".
# 2. NEVER worry about YAML length — multi-turn generation across sequential steps is supported.
# 3. Always include thorough, line-by-line explanations for every code block and reveal the Notional Machine.
# 4. Put all your might and go Plus Ultra — zero half-assing, no placeholders.
# 5. Author 5–10 scaffolded checks per block according to topic, plus 30–50 dedicated questions under top-level 'quiz:' spanning mixed difficulty levels in no specific order, separate from immediate block checks, including code boxes where relevant.

Ask (compact, one message, numbered):

1. **Level** — novice / comfortable-in-C / experienced? (affects depth of
   `explain_md` and whether `model` blocks get extra `viz` steps.)
   Default: comfortable-in-C.
2. **Depth vs speed** — deep (more blocks, 5–10 checks each according to topic) or fast (fewer
   blocks, 3–5 checks each) or balanced (2 blocks per major concept)? Default: deep.
   *(Note: YAML length is unlimited — multi-turn / multi-step generation is fully supported
   so no concepts or code explanations are ever rushed or cut short).*
3. **Prioritize / skip** — which sections/examples of this chapter matter most?
   Any to skip (e.g. Windows-only notes, C++ tangents)? Default: keep all,
   skip platform tangents.
4. **Lab difficulty + toolchain** — easy (fill 3-5 lines) / medium (write a
   function) / hard (multi-file)? Which language + runner (pilot default: C
   with `gcc -Wall -std=c99`, 2 s timeout — state yours, e.g. `python3`,
   `node`, `go run`)? No executable code in this chapter? Say so — labs are
   omitted then. Default: easy-medium, declared toolchain.
5. **Explanation language** — English default; other allowed for prose only
   (keys stay English per CR-GEN-003).
6. **Interleaved review** — how much from prior chapters (0 / 2 / 4 checks)?
   Default: 2.

Record the answers as `gen_notes.md` next to the pack (RECOMMENDED): the human
operator pastes answers there for reproducibility. Then emit the YAML per
GENERATE.md.


---

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
    checks:                    # REQUIRED, >=1 per block (SHOULD: 5-10 according to topic)
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
quiz:                          # SHOULD, 30-50 questions across levels (intro/core/advanced) in no specific order
  - kind: mcq                  # same shape as checks; supports code: "...", level: core|intro|advanced
    level: core
    q: "..."
    code: "..."                # OPTIONAL code snippet for question
    choices: [...]
    answer: 0
    why: "..."
    concept: "..."
labs:                          # SHOULD when chapter has code; 1-4 multi-file labs per ISO/IEC/IEEE 29148:2018
  - id: lab1                   # unique lab id (e.g. lab1, lab2)
    title: "..."               # descriptive pedagogical title
    instruction_md: "..."      # complete, self-contained markdown requirements
    files:                     # starter files in workspace labs/<book>/<chapter>/<lab_id>/
      - path: "component.h"
        content: "..."
      - path: "component.c"
        content: "..."
      - path: "main.c"
        content: "..."
      - path: "test_runner.c"
        content: "..."
    commands:                  # language-agnostic commands executed in cwd = workspace_dir
      run: "gcc -Wall -Wextra -std=c99 component.c main.c -o app && ./app"
      test: "gcc -Wall -Wextra -std=c99 component.c test_runner.c -o test_runner && ./test_runner"
    test_cases:                # automated input vs expected output assertions with unified diffing
      - name: "Interactive execution trace"
        stdin: ""
        expect: "...\n"
        expect_exit: 0
    hints: ["..."]             # progressive hints (general -> specific)
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

# =============================================================================
# CHAPTER CONTENT: ch10 OF extreme-c (3 part(s))
# SOURCE FILE ON DISK: books/extreme-c/raw_chapters/ch10.txt
# MODE TARGET: TEST
# =============================================================================


## part 1/3

# Chapter 07

<!-- source: Text/composition_and_aggregation.xhtml | spine-id: composition_and_aggregation.xhtml | chapter: ch10 -->

# Chapter 07

# Composition and Aggregation

In the previous chapter, we talked about encapsulation and information hiding. In this chapter, we continue with object orientation in C and we'll discuss the various relationships that can exist between two classes. Eventually, this will allow us to expand our object model and express the relations between objects as part of the upcoming chapters.

As part of this chapter, we discuss:

- Types of relations that can exist between two objects and their corresponding classes: We will talk about to-have and to-be relationships, but our focus will be on to-have relations in this chapter.
- Composition as our first to-have relation: An example will be given to demonstrate a real composition relationship between two classes. Using the given example, we explore the memory structure which we usually have in case of composition.
- Aggregation as the second to-have relation: It is similar to composition since both of them address a to-have relationship. But they are different. We will give a separate complete example to cover an aggregation case. The difference among aggregation and composition will shine over the memory layout associated with these relationships.

This is the second of the four chapters covering OOP in C. The to-be relationship, which is also called inheritance, will be covered in the next chapter.

# Relations between classes

An object model is a set of related objects. The number of relations can be many, but there are a few relationship types that can exist between two objects. Generally, there are two categories of relationships found between objects (or their corresponding classes): to-have relationships and to-be relationships.

We'll explore to-have relationships in depth in this chapter, and we'll cover to-be relationships in the next chapter. In addition, we will also see how the relationships between various objects can lead to relationships between their corresponding classes. Before dealing with that, we need to be able to distinguish between a class and an object.

# Object versus class

If you remember from the previous chapter, we have two approaches for constructing objects. One approach is prototype-based and the other is class-based.

In the prototype-based approach, we construct an object either empty (without any attribute or behavior), or we clone it from an existing object. In this context, instance and object mean the same thing. So, the prototype-based approach can be read as the object-based approach; an approach that begins from empty objects instead of classes.

In the class-based approach, we cannot construct an object without having a blueprint that is often called a class. So, we should start from a class. And then, we can instantiate an object from it. In the previous chapter, we explained the implicit encapsulation technique that defines a class as a set of declarations put in a header file. We also gave some examples showing how this works in C.

Now, as part of this section, we want to talk more about the differences between a class and an object. While the differences seem to be trivial, we want to dive deeper and study them carefully. We begin by giving an example.

Suppose that we define a class, `Person`. It has the following attributes: `name`, `surname`, and `age`. We won't talk about the behaviors because the differences usually come from the attributes, and not the behaviors.

In C, we can write the `Person` class with public attributes as follows:

typedef struct {

char name[32];

char surname[32];

unsigned int age;

} person_t;

Code Box 7-1: The Person attribute structure in C

And in C++:

class Person {

public:

std::string name;

std::string family;

uint32_t age;

};

Code Box 7-2: The Person class's class in C++

The preceding code boxes are identical. In fact, the current discussion can be applied to both C and C++, and even other OOP languages such as Java. A class (or an object template) is a blueprint that only determines the attributes required to be present in every object, and not the values that these attributes might have in one specific object. In fact, each object has its own specific set of values for the same attributes that exist in other objects instantiated from the same class.

When an object is created based on a class, its memory is allocated first. This allocated memory will be a placeholder for the attribute values. After that, we need to initialize the attribute values with some values. This is an important step, otherwise, the object might have an invalid state after being created. As you've already seen, this step is called construction.

There is usually a dedicated function that performs the construction step, which is called the constructor. The functions `list_init` and `car_construct` in the examples, found in the previous chapter, were constructor functions. It is quite possible that as part of constructing an object, we need to allocate even more memory for resources such as other objects, buffers, arrays, streams, and so on required by that object. The resources owned by the object must have been released before having the owner object freed.

We also have another function, similar to the constructor, which is responsible for freeing any allocated resources. It is called the destructor. Similarly, the functions `list_destroy` and `car_destruct` in the examples found in the previous chapter were destructors. After destructing an object, its allocated memory is freed, but before that, all the owned resources and their corresponding memories must be freed.

Before moving on, let's sum up what we've explained so far:

- A class is a blueprint that is used as a map for creating objects.
- Many objects can be made from the same class.
- A class determines which attributes should be present in every future object created based on that class. It doesn't say anything about the possible values they can have.
- A class itself does not consume any memory (except in some programming languages other than C and C++) and only exists at the source level and at compile time. But objects exist at runtime and consume memory.
- When creating an object, memory allocation happens first. In addition, memory deallocation is the last operation for an object.
- When creating an object, it should be constructed right after memory allocation. It should be also destructed right before deallocation.
- An object might be owning some resources such as streams, buffers, arrays, and so on, that must be released before having the object destroyed.

Now that you know the differences between a class and an object, we can move on and explain the different relationships that can exist between two objects and their corresponding classes. We'll start with composition.

# Composition

As the term "composition" implies, when an object contains or possesses another object – in other words, it is composed of another object – we say that there is a composition relationship between them.

As an example, a car has an engine; a car is an object that contains an engine object. Therefore, the car and engine objects have a composition relationship. There is an important condition that a composition relationship must have: the lifetime of the contained object is bound to the lifetime of the container object.

As long as the container object exists, the contained object must exist. But when the container object is about to get destroyed, the contained object must have been destructed first. This condition implies that the contained object is often internal and private to the container.

Some parts of the contained object may be still accessible through the public interface (or behavior functions) of the container class, but the lifetime of the contained object must be managed internally by the container object. If a piece of code can destruct the contained object without destructing the container object, it is a breach of the composition relationship and the relationship is no longer a composition.

The following example, example 7.1, demonstrates the composition relationship between a car object and an engine object.

It is composed of five files: two header files, which declare the public interfaces of the `Car` and `Engine` classes; two source files, which contain the implementation of the `Car` and `Engine` classes; and finally, a source file, which contains the `main` function and executes a simple scenario using a car and its engine object.

Note that, in some domains, we can have engine objects outside of the car objects; for example, in mechanical engineering CAD software. So, the type of relationships between the various objects is determined by the problem domain. For the sake of our example, imagine a domain in which engine objects could not exist outside of car objects.

The following code box shows the header file for the `Car` class:

#ifndef EXTREME_C_EXAMPLES_CHAPTER_7_1_CAR_H

#define EXTREME_C_EXAMPLES_CHAPTER_7_1_CAR_H

struct car_t;

// Memory allocator

struct car_t* car_new();

// Constructor

void car_ctor(struct car_t*);

// Destructor

void car_dtor(struct car_t*);

// Behavior functions

void car_start(struct car_t*);

void car_stop(struct car_t*);

double car_get_engine_temperature(struct car_t*);

#endif

Code Box 7-3 [ExtremeC_examples_chapter7_1_car.h]: The public interface of the Car class

As you see, the preceding declarations have been made in a similar way to what we did for the `List` class in the last example of the previous chapter, example 6.3. One of the differences is that we have chosen a new suffix for the constructor function; `car_new` instead of `car_construct`. The other difference is that we have only declared the attribute structure `car_t`. We have not defined its fields, and this is called a forward declaration. The definition for the structure `car_t` will be in the source file which comes in the code box 7-5. Note that in the preceding header file, the type `car_t` is considered an incomplete type which is not defined yet.

The following code box contains the header file for the `Engine` class:

#ifndef EXTREME_C_EXAMPLES_CHAPTER_7_1_ENGINE_H

#define EXTREME_C_EXAMPLES_CHAPTER_7_1_ENGINE_H

struct engine_t;

// Memory allocator

struct engine_t* engine_new();

// Constructor

void engine_ctor(struct engine_t*);

// Destructor

void engine_dtor(struct engine_t*);

// Behavior functions

void engine_turn_on(struct engine_t*);

void engine_turn_off(struct engine_t*);

double engine_get_temperature(struct engine_t*);

#endif

Code Box 7-4 [ExtremeC_examples_chapter7_1_engine.h]: The public interface of the Engine class

The following code boxes contains the implementations done for the `Car` and `Engine` classes. We begin with the `Car` class:

#include <stdlib.h>

// Car is only able to work with the public interface of Engine

#include "ExtremeC_examples_chapter7_1_engine.h"

typedef struct {

// Composition happens because of this attribute

struct engine_t* engine;

} car_t;

car_t* car_new() {

return (car_t*)malloc(sizeof(car_t));

}

void car_ctor(car_t* car) {

// Allocate memory for the engine object

car->engine = engine_new();

// Construct the engine object

engine_ctor(car->engine);

}

void car_dtor(car_t* car) {

// Destruct the engine object

engine_dtor(car->engine);

// Free the memory allocated for the engine object

free(car->engine);

}

void car_start(car_t* car) {

engine_turn_on(car->engine);

}

void car_stop(car_t* car) {

engine_turn_off(car->engine);

}

double car_get_engine_temperature(car_t* car) {

return engine_get_temperature(car->engine);

}

Code Box 7-5 [ExtremeC_examples_chapter7_1_car.c]: The definition of the Car class

The preceding code box shows how the car has contained the engine. As you see, we have a new attribute as part of the `car_t` attribute structure, and 


## part 2/3

the engine object

free(car->engine);

}

void car_start(car_t* car) {

engine_turn_on(car->engine);

}

void car_stop(car_t* car) {

engine_turn_off(car->engine);

}

double car_get_engine_temperature(car_t* car) {

return engine_get_temperature(car->engine);

}

Code Box 7-5 [ExtremeC_examples_chapter7_1_car.c]: The definition of the Car class

The preceding code box shows how the car has contained the engine. As you see, we have a new attribute as part of the `car_t` attribute structure, and it is of the `struct engine_t*` type. Composition happens because of this attribute.

Though the type `struct engine_t*` is still incomplete inside this source file, it can point to an object from a complete `engine_t` type at runtime. This attribute will point to an object that is going to be constructed as part of the `Car` class's constructor, and it will be freed inside the destructor. At both places, the car object exists, and this means that the engine's lifetime is included in the car's lifetime.

The `engine` pointer is private, and no pointer is leaking from the implementation. That's an important note. When you are implementing a composition relationship, no pointer should be leaked out otherwise it causes external code to be able to change the state of the contained object. Just like encapsulation, no pointer should be leaked out when it gives direct access to the private parts of an object. Private parts should always be accessed indirectly via behavior functions.

The `car_get_engine_temperature` function in the code box gives access to the `temperature` attribute of the engine. However, there is an important note regarding this function. It uses the public interface of the engine. If you pay attention, you'll see that the car's private implementation is consuming the engine's public interface.

This means that the car itself doesn't know anything about the implementation details of the engine. This is the way that it should be.

Two objects that are not of the same type, in most cases, must not know about each other's implementation details. This is what information hiding dictates. Remember that the car's behaviors are considered external to the engine.

This way, we can replace the implementation of the engine with an alternative one, and it should work, as long as the new implementation provides definitions for the same public functions declared in the engine's header file.

Now, let's look at the implementation of the `Engine` class:

#include <stdlib.h>

typedef enum {

ON,

OFF

} state_t;

typedef struct {

state_t state;

double temperature;

} engine_t;

// Memory allocator

engine_t* engine_new() {

return (engine_t*)malloc(sizeof(engine_t));

}

// Constructor

void engine_ctor(engine_t* engine) {

engine->state = OFF;

engine->temperature = 15;

}

// Destructor

void engine_dtor(engine_t* engine) {

// Nothing to do

}

// Behavior functions

void engine_turn_on(engine_t* engine) {

if (engine->state == ON) {

return;

}

engine->state = ON;

engine->temperature = 75;

}

void engine_turn_off(engine_t* engine) {

if (engine->state == OFF) {

return;

}

engine->state = OFF;

engine->temperature = 15;

}

double engine_get_temperature(engine_t* engine) {

return engine->temperature;

}

Code Box 7-6 [ExtremeC_examples_chapter7_1_engine.c]: The definition of the Engine class

The preceding code is just using the implicit encapsulation approach for its private implementation, and it is very similar to previous examples. But there is one thing to note about this. As you see, the `engine` object doesn't know that an external object is going to contain it in a composition relationship. This is like the real world. When a company is building engines, it is not clear which engine will go into which car. Of course, we could have kept a pointer to the container `car` object, but in this example, we didn't need to.

The following code box demonstrates the scenario in which we create a `car` object and invoke some of its public API to extract information about the car's engine:

#include <stdio.h>

#include <stdlib.h>

#include "ExtremeC_examples_chapter7_1_car.h"

int main(int argc, char** argv) {

// Allocate memory for the car object

struct car_t *car = car_new();

// Construct the car object

car_ctor(car);

printf("Engine temperature before starting the car: %f\n",

car_get_engine_temperature(car));

car_start(car);

printf("Engine temperature after starting the car: %f\n",

car_get_engine_temperature(car));

car_stop(car);

printf("Engine temperature after stopping the car: %f\n",

car_get_engine_temperature(car));

// Destruct the car object

car_dtor(car);

// Free the memory allocated for the car object

free(car);

return 0;

}

Code Box 7-7 [ExtremeC_examples_chapter7_1_main.c]: The main function of example 7.1

To build the preceding example, firstly we need to compile the previous three source files. Then, we need to link them together to generate the final executable object file. Note that the main source file (the source file that contains the `main` function) only depends on the car's public interface. So, when linking, it only needs the private implementation of the `car` object. However, the private implementation of the `car` object relies on the public interface of the engine interface; then, while linking, we need to provide the private implementation of the `engine` object. Therefore, we need to link all three object files in order to have the final executable.

The following commands show how to build the example and run the final executable:

$ gcc -c ExtremeC_examples_chapter7_1_engine.c -o engine.o

$ gcc -c ExtremeC_examples_chapter7_1_car.c -o car.o

$ gcc -c ExtremeC_examples_chapter7_1_main.c -o main.o

$ gcc engine.o car.o main.o -o ex7_1.out

$ ./ex7_1.out

Engine temperature before starting the car: 15.000000

Engine temperature after starting the car: 75.000000

Engine temperature after stopping the car: 15.000000

$

Shell Box 7-1: The compilation, linking, and execution of example 7.1

In this section, we explained one type of relationship that can exist between two objects. In the next section, we'll talk about the next relationship. It shares a similar concept to the composition relationship, but there are some significant differences.

# Aggregation

Aggregation also involves a container object that contains another object. The main difference is that in aggregation, the lifetime of the contained object is independent of the lifetime of the container object.

In aggregation, the contained object could be constructed even before the container object is constructed. This is opposite to composition, in which the contained object should have a lifetime shorter than or equal to the container object.

The following example, example 7.2, demonstrates an aggregation relationship. It describes a very simple game scenario in which a player picks up a gun, fires multiple times, and drops the gun.

The `player` object would be a container object for a while, and the `gun` object would be a contained object as long as the player object holds it. The lifetime of the gun object is independent of the lifetime of the player object.

The following code box shows the header file of the `Gun` class:

#ifndef EXTREME_C_EXAMPLES_CHAPTER_7_2_GUN_H

#define EXTREME_C_EXAMPLES_CHAPTER_7_2_GUN_H

typedef int bool_t;

// Type forward declarations

struct gun_t;

// Memory allocator

struct gun_t* gun_new();

// Constructor

void gun_ctor(struct gun_t*, int);

// Destructor

void gun_dtor(struct gun_t*);

// Behavior functions

bool_t gun_has_bullets(struct gun_t*);

void gun_trigger(struct gun_t*);

void gun_refill(struct gun_t*);

#endif

Code Box 7-8 [ExtremeC_examples_chapter7_2_gun.h]: The public interface of the Gun class

As you see, we have only declared the `gun_t` attribute structure as we have not defined its fields. As we have explained before, this is called a forward declaration and it results in an incomplete type which cannot be instantiated.

The following code box shows the header file of the `Player` class:

#ifndef EXTREME_C_EXAMPLES_CHAPTER_7_2_PLAYER_H

#define EXTREME_C_EXAMPLES_CHAPTER_7_2_PLAYER_H

// Type forward declarations

struct player_t;

struct gun_t;

// Memory allocator

struct player_t* player_new();

// Constructor

void player_ctor(struct player_t*, const char*);

// Destructor

void player_dtor(struct player_t*);

// Behavior functions

void player_pickup_gun(struct player_t*, struct gun_t*);

void player_shoot(struct player_t*);

void player_drop_gun(struct player_t*);

#endif

Code Box 7-9 [ExtremeC_examples_chapter7_2_player.h]: The public interface of the Player class

The preceding code box defines the public interface of all player objects. In other words, it defines the public interface of the `Player` class.

Again, we have to forward the declaration of the `gun_t` and `player_t` structures. We need to have the `gun_t` type declared since some behavior functions of the `Player` class have arguments of this type.

The implementation of the `Player` class is as follows:

#include <stdlib.h>

#include <string.h>

#include <stdio.h>

#include "ExtremeC_examples_chapter7_2_gun.h"

// Attribute structure

typedef struct {

char* name;

struct gun_t* gun;

} player_t;

// Memory allocator

player_t* player_new() {

return (player_t*)malloc(sizeof(player_t));

}

// Constructor

void player_ctor(player_t* player, const char* name) {

player->name =

(char*)malloc((strlen(name) + 1) * sizeof(char));

strcpy(player->name, name);

// This is important. We need to nullify aggregation pointers

// if they are not meant to be set in constructor.

player->gun = NULL;

}

// Destructor

void player_dtor(player_t* player) {

free(player->name);

}

// Behavior functions

void player_pickup_gun(player_t* player, struct gun_t* gun) {

// After the following line the aggregation relation begins.

player->gun = gun;

}

void player_shoot(player_t* player) {

// We need to check if the player has picked up the gun

// otherwise, shooting is meaningless

if (player->gun) {

gun_trigger(player->gun);

} else {

printf("Player wants to shoot but he doesn't have a gun!");

exit(1);

}

}

void player_drop_gun(player_t* player) {

// After the following line the aggregation relation

// ends between two objects. Note that the object gun

// should not be freed since this object is not its

// owner like composition.

player->gun = NULL;

}

Code Box 7-10 [ExtremeC_examples_chapter7_2_player.c]: The definition of the Player class

Inside the `player_t` structure, we declare the pointer attribute `gun` that is going to point to a `gun` object soon. We need to nullify this in the constructor because unlike composition, this attribute is not meant to be set as part of the constructor.

If an aggregation pointer is required to be set upon construction, the address of the target object should be passed as an argument to the constructor. Then, this situation is called a mandatory aggregation.

If the aggregation pointer can be left as null in the constructor, then it is an optional aggregation, as in the preceding code. It is important to nullify the optional aggregation pointers in the constructor.

In the function `player_pickup_gun`, the aggregation relationship begins, and it ends in the function `player_drop_gun` when the player drops the gun.

Note that we need to nullify the pointer `gun` after dropping the aggregation relationship. Unlike in composition, the container object is not the owner of the contained object. So, it has no control over its lifetime. Therefore, we should not free the gun object in any place inside the player's implementation code.

In optional aggregation relations, we may not have set the contained object at some point in the program. Therefore, we should be careful while using the aggregation pointer since any access to a pointer that is not set, or a pointer that is `null`, can lead to a segmentation fault.


## part 3/3

composition, the container object is not the owner of the contained object. So, it has no control over its lifetime. Therefore, we should not free the gun object in any place inside the player's implementation code.

In optional aggregation relations, we may not have set the contained object at some point in the program. Therefore, we should be careful while using the aggregation pointer since any access to a pointer that is not set, or a pointer that is `null`, can lead to a segmentation fault. That's basically why in the function `player_shoot`, we check the `gun` pointer is valid. If the aggregation pointer is null, it means that the code using the player object is misusing it. If that's the case, we abort the execution by returning 1 as the exit code of the process.

The following code is the implementation of the `Gun` class:

#include <stdlib.h>

typedef int bool_t;

// Attribute structure

typedef struct {

int bullets;

} gun_t;

// Memory allocator

gun_t* gun_new() {

return (gun_t*)malloc(sizeof(gun_t));

}

// Constructor

void gun_ctor(gun_t* gun, int initial_bullets) {

gun->bullets = 0;

if (initial_bullets > 0) {

gun->bullets = initial_bullets;

}

}

// Destructor

void gun_dtor(gun_t* gun) {

// Nothing to do

}

// Behavior functions

bool_t gun_has_bullets(gun_t* gun) {

return (gun->bullets > 0);

}

void gun_trigger(gun_t* gun) {

gun->bullets--;

}

void gun_refill(gun_t* gun) {

gun->bullets = 7;

}

Code Box 7-11 [ExtremeC_examples_chapter7_2_gun.c]: The definition of the Gun class

The preceding code is straightforward, and it is written in a way that a gun object doesn't know that it will be contained in any object.

Finally, the following code box demonstrates a short scenario that creates a `player` object and a `gun` object. Then, the player picks up the gun and fires with it until no ammo is left. After that, the player refills the gun and does the same. Finally, they drop the gun:

#include <stdio.h>

#include <stdlib.h>

#include "ExtremeC_examples_chapter7_2_player.h"

#include "ExtremeC_examples_chapter7_2_gun.h"

int main(int argc, char** argv) {

// Create and constructor the gun object

struct gun_t* gun = gun_new();

gun_ctor(gun, 3);

// Create and construct the player object

struct player_t* player = player_new();

player_ctor(player, "Billy");

// Begin the aggregation relation.

player_pickup_gun(player, gun);

// Shoot until no bullet is left.

while (gun_has_bullets(gun)) {

player_shoot(player);

}

// Refill the gun

gun_refill(gun);

// Shoot until no bullet is left.

while (gun_has_bullets(gun)) {

player_shoot(player);

}

// End the aggregation relation.

player_drop_gun(player);

// Destruct and free the player object

player_dtor(player);

free(player);

// Destruct and free the gun object

gun_dtor(gun);

free(gun);

return 0;

}

Code Box 7-12 [ExtremeC_examples_chapter7_2_main.c]: The main function of example 7.2

As you see here, the `gun` and `player` objects are independent of each other. The responsible logic for creating and destroying these objects is the `main` function. At some point in the execution, they form an aggregation relationship and perform their roles, then at another point, they become separated. The important thing in aggregation is that the container object shouldn't alter the lifetime of the contained object, and as long as this rule is followed, no memory issues should arise.

The following shell box shows how to build the example and run the resulting executable file. As you see, the `main` function in Code Box 7-12 doesn't produce any output:

$ gcc -c ExtremeC_examples_chapter7_2_gun.c -o gun.o $ gcc -c ExtremeC_examples_chapter7_2_player.c -o player.o $ gcc -c ExtremeC_examples_chapter7_2_main.c -o main.o $ gcc gun.o player.o main.o -o ex7_2.out $ ./ex7_2.out $

Shell Box 7-2: The compilation, linking, and execution of example 7.2

In an object model created for a real project, the amount of aggregation relationships is usually greater than the number of composition relationships. Also, aggregation relationships are more visible externally because, in order to make an aggregation relationship, some dedicated behavior functions are required, at least in the public interface of the container object, to set and reset the contained object.

As you see in the preceding example, the `gun` and `player` objects are separated from the start. They become related for a short period of time, and then they become separated again. This means that the aggregation relationship is temporary, unlike the composition relationship, which is permanent. This shows that composition is a stronger form of possession (to-have) relationship between objects, while aggregation exhibits a weaker relationship.

Now, a question comes to mind. If an aggregation relationship is temporary between two objects, is it temporary between their corresponding classes? The answer is no. The aggregation relationship is permanent between the types. If there is a small chance that in the future, two objects from two different types become related based on an aggregation relationship, their types should be in the aggregation relationship permanently. This holds for composition as well.

Even a low chance of there being an aggregation relationship should cause us to declare some pointers in the attribute structure of the container object, and this means that the attribute structure is changed permanently. Of course, this is only true for class-based programming languages.

Composition and aggregation both describe the possession of some objects. In other words, these relationships describe a "to-have" or "has-a" situation; a player has a gun, or a car has an engine. Every time you feel that an object possesses another one, it means there should either be a composition relationship or an aggregation relationship between them (and their corresponding classes).

In the next chapter, we'll continue our discussion regarding relationship types by looking at the inheritance or extension relationship.

# Summary

In this chapter, the following topics have been discussed:

- The possible relationship types between classes and objects.
- The differences and similarities between a class, an object, an instance, and a reference.
- Composition, which entails that a contained object is totally dependent on its container object.
- Aggregation, in which the contained object can live freely without any dependency on its container object.
- The fact that aggregation can be temporary between objects, but it is defined permanently between their types (or classes).

In the next chapter, we continue to explore OOP, primarily addressing the two further pillars upon which it is based: inheritance and polymorphism.


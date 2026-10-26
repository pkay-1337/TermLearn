# =============================================================================
# INSTRUCTIONS FOR AI AGENT / CHAT: CHAPTER QUIZ QUESTIONS
# TARGET OUTPUT FILE: packs/extreme-c/ch11/quiz.yaml
#
# [SOURCE ASSET LOCATIONS — WHERE TO FIND CHAPTER DATA]
# 1. Extracted Chapter Text: books/extreme-c/raw_chapters/ch11.txt
#    (The full extracted text is also appended at the bottom of this prompt)
# 2. Book Table of Contents & Metadata: books/extreme-c/meta.json
# 3. Book Toolchain & Course Pack Config: packs/extreme-c/book.yaml
#
# [DIRECTIVES FOR quiz.yaml]
# 1. Read the chapter from `books/extreme-c/raw_chapters/ch11.txt`.
# 2. Author 30 to 50 dedicated, standalone diagnostic questions testing cumulative synthesis.
# 3. Distribute questions across three difficulty levels: 'level: intro | core | advanced'.
# 4. Mix question kinds: 'mcq', 'predict', 'why-fails', 'fillblank', 'order', 'trace', 'spot-bug'.
# 5. SELF-CONTAINED CODE: Whenever testing code behavior or bugs, embed the code snippet directly
#    in the question via 'code: |'. Never reference external book exercise numbers or listings.
# 6. ANSWER RANDOMIZATION: Uniformly distribute correct answer positions across 0, 1, 2, and 3.
# 7. ELABORATED WHY: Every question MUST provide a comprehensive 'why:' explaining the core rule
#    and naming the exact misconception each wrong distractor traps.
# 8. OUTPUT FORMAT: Single YAML document with top-level 'quiz: [...]'.
#
# [POST-GENERATION VERIFICATION FOR quiz.yaml]
# - Count: 30–50 questions.
# - Levels: intro + core + advanced all present.
# - No duplicates: no q string identical to any block-check q.
# - Mixed: not grouped by level or concept.
# - Concept coverage: distinct concepts span core chapter topics (e.g. composition, aggregation, ownership, diagnostics).
# - Each item carries 1.1–1.10 (positively worded, 2-4 choices, answer in bounds, randomized answer index,
#   self-contained with embedded code, elaborated why, exact kinds, scrambled order, load-bearing fillblank, prose width <=120 cols).
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
  - `study.yaml` — as many concept blocks as the chapter's idea units demand (one single-concept block per unit; no set count), Notional Machine state transitions, and scaffolded checks.
  - `quiz.yaml` — 30–50 dedicated synthesis questions across difficulty levels.
  - `labs.yaml` — 1–4 practical coding workspaces with blank starters and test runners.
  - `cards.yaml` — as many atomic SM-2 spaced repetition flashcards as the chapter's facts demand (no set count).
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
  override brevity. A chapter wielding as many richly explained blocks as its idea units demand, deep code breakdowns,
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
  - `example`: Verified code snippet; no line-count or column caps — include exactly as much code as the concept needs, runnable where applicable.
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
12. Line lengths sane (prose ≤120; code lines carry no cap)?
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
- **1.10 Line formatting**: Prose ≤120 columns; code lines carry no width cap.

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
- **Code length**: No line-count or column caps on starter and harness code — include as much as the lab needs.

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
`FR-PACK-005`: Prose lines **SHOULD** be ≤120 chars for terminal readability; code blocks (`example.code`) and lab starters/harness code carry **no** line-count or column caps.
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
# CHAPTER CONTENT: ch11 OF extreme-c (5 part(s))
# SOURCE FILE ON DISK: books/extreme-c/raw_chapters/ch11.txt
# MODE TARGET: QUIZ
# =============================================================================


## part 1/5

# Chapter 0 8

<!-- source: Text/inheritance_and_polymorphism.xhtml | spine-id: inheritance_and_polymorphism.xhtml | chapter: ch11 -->

# Chapter 0 8

# Inheritance and Polymorphism

This chapter is a continuation of the previous two chapters, where we introduced how you can do OOP in C and reached the concepts of composition and aggregation. This chapter mainly continues the discussion regarding relationships between objects and their corresponding classes and covers inheritance and polymorphism. As part of this chapter, we conclude this topic and we continue with Abstraction in the following chapter.

This chapter is heavily dependent on the theory explained in the previous two chapters, where we were discussing the possible relationships between classes. We explained composition and aggregation relationships, and now we are going to talk about the extension or inheritance relationship in this chapter, along with a few other topics.

The following are the topics that will be explained throughout this chapter:

- As explained earlier, the inheritance relationship is the first topic that we discuss. The methods for implementing the inheritance relationship in C will be covered, and we will conduct a comparison between them.
- The next big topic is polymorphism. Polymorphism allows us to have different versions of the same behavior in the child classes, in the case of having an inheritance relationship between those classes. We will discuss the methods for having a polymorphic function in C; this will be the first step in our understanding of how C++ offers polymorphism.

Let's start our discussion with the inheritance relationship.

# Inheritance

We closed the previous chapter by talking about to-have relationships, which eventually led us to composition and aggregation relationships. In this section, we are going to talk about to-be or is-a relationships. The inheritance relationship is a to-be relationship.

An inheritance relationship can also be called an extension relationship because it only adds extra attributes and behaviors to an existing object or class. In the following sections, we'll explain what inheritance means and how it can be implemented in C.

There are situations when an object needs to have the same attributes that exist in another object. In other words, the new object is an extension to the other object.

For example, a student has all the attributes of a person, but may also have extra attributes. See Code Box 8-1:

typedef struct {

char first_name[32];

char last_name[32];

unsigned int birth_year;

} person_t;

typedef struct {

char first_name[32];

char last_name[32];

unsigned int birth_year;

char student_number[16]; // Extra attribute

unsigned int passed_credits; // Extra attribute

} student_t;

Code Box 8-1: The attribute structures of the Person class and the Student class

This example clearly shows how `student_t` extends the attributes of `person_t` with new attributes, `student_number` and `passed_credits`, which are student-specific attributes.

As we have pointed out before, inheritance (or extension) is a to-be relationship, unlike composition and aggregation, which are to-have relationships. Therefore, for the preceding example, we can say that "a student is a person," which seems to be correct in the domain of educational software. Whenever a to-be relationship exists in a domain, it is probably an inheritance relationship. In the preceding example, `person_t` is usually called the supertype, or the base type, or simply the parent type, and `student_t` is usually called the child type or the inherited subtype.

## The nature of inheritance

If you were to dig deeper and see what an inheritance relationship really is, you would find out that it is really a composition relationship in its nature. For example, we can say that a student has a person's nature inside of them. In other words, we can suppose that there is a private person object inside the `Student` class's attribute structure. That is, an inheritance relationship can be equivalent to a one-to-one composition relationship.

So, the structures in Code Box 8-1 can be written as:

typedef struct {

char first_name[32];

char last_name[32];

unsigned int birth_year;

} person_t;

typedef struct {

person_t person;

char student_number[16]; // Extra attribute

unsigned int passed_credits; // Extra attribute

} student_t;

Code Box 8-2: The attribute structures of the Person and Student classes but nested this time

This syntax is totally valid in C, and in fact nesting structures by using structure variables (not pointers) is a powerful setup. It allows you to have a structure variable inside your new structure that is really an extension to the former.

With the preceding setup, necessarily having a field of type `person_t` as the first field, a `student_t` pointer can be easily cast to a `person_t` pointer, and both of them can point to the same address in memory.

This is called upcasting. In other words, casting a pointer of the type of the child's attribute structure to the type of the parent's attribute structure is upcasting. Note that with structure variables, you cannot have this feature.

Example 8.1 demonstrates this as follows:

#include <stdio.h>

typedef struct {

char first_name[32];

char last_name[32];

unsigned int birth_year;

} person_t;

typedef struct {

person_t person;

char student_number[16]; // Extra attribute

unsigned int passed_credits; // Extra attribute

} student_t;

int main(int argc, char** argv) {

student_t s;

student_t* s_ptr = &s;

person_t* p_ptr = (person_t*)&s;

printf("Student pointer points to %p\n", (void*)s_ptr);

printf("Person pointer points to %p\n", (void*)p_ptr);

return 0;

}

Code Box 8-3 [ExtremeC_examples_chapter8_1.c]: Example 8.1, showing upcasting between Student and Person object pointers

As you can see, we expect that the `s_ptr` and `p_ptr` pointers are pointing to the same address in memory. The following is the output after building and running example 8.1:

$ gcc ExtremeC_examples_chapter8_1.c -o ex8_1.out

$ ./ex8_1.out

Student pointer points to 0x7ffeecd41810

Person pointer points to 0x7ffeecd41810

$

Shell Box 8-1: The output of example 8.1

And yes, they are pointing to the same address. Note that the shown addresses can be different in each run, but the point is that the pointers are referring to the same address. This means that a structure variable of the type `student_t` is really inheriting the `person_t` structure in its memory layout. This implies that we can use the function behaviors of the `Person` class with a pointer that is pointing to a `student` object. In other words, the `Person` class's behavior functions can be reused for the `student` objects, which is a great achievement.

Note that the following is wrong, and the code won't compile:

struct person_t;

typedef struct {

struct person_t person; // Generates an error!

char student_number[16]; // Extra attribute

unsigned int passed_credits; // Extra attribute

} student_t;

Code Box 8-4: Establishing an inheritance relationship which doesn't compile!

The line declaring the `person` field generates an error because you cannot create a variable from an incomplete type. You should remember that the forward declaration of a structure (similar to the first line in Code Box 8-4) results in the declaration of an incomplete type. You can have only pointers of incomplete types, not variables. As you've seen before, you cannot even allocate Heap memory for an incomplete type.

So, what does this mean? It means that if you're going to use nested structure variables in order to implement inheritance, the `student_t` structure should see the actual definition of `person_t`, which, based on what we learned about encapsulation, should be private and not visible to any other class.

Therefore, you have two approaches for implementing the inheritance relationship:

- Make it so that the child class has access to the private implementation (actual definition) of the base class.
- Make it so that the child class only has access to the public interface of the base class.

### The first approach for having inheritance in C

We'll demonstrate the first approach in the following example, example 8.2, and the second approach in example 8.3, which will come up in the next section. Both of them represent the same classes, `Student` and `Person`, with some behavior functions, having some objects playing in a simple scenario in the `main` function.

We'll start with example 8.2, in which the `Student` class needs to have access to the actual private definition of the `Person` class's attribute structure. The following code boxes present the headers and the sources for the `Student` and `Person` classes together with the `main` function. Let's start with the header file declaring the `Person` class:

#ifndef EXTREME_C_EXAMPLES_CHAPTER_8_2_PERSON_H

#define EXTREME_C_EXAMPLES_CHAPTER_8_2_PERSON_H

// Forward declaration

struct person_t;

// Memory allocator

struct person_t* person_new();

// Constructor

void person_ctor(struct person_t*,

const char* /* first name */,

const char* /* last name */,

unsigned int /* birth year */);

// Destructor

void person_dtor(struct person_t*);

// Behavior functions

void person_get_first_name(struct person_t*, char*);

void person_get_last_name(struct person_t*, char*);

unsigned int person_get_birth_year(struct person_t*);

#endif

Code Box 8-5 [ExtremeC_examples_chapter8_2_person.h]: Example 8.2, the public interface of the Person class

Look at the constructor function in Code Box 8-5. It accepts all the values required for creating a `person` object: `first_name`, `second_name`, and `birth_year`. As you see, the attribute structure `person_t` is incomplete, hence the `Student` class cannot use the preceding header file for establishing an inheritance relationship, similar to what we demonstrated in the previous section.

On the other hand, the preceding header file must not contain the actual definition of the attribute structure `person_t`, since the preceding header file is going to be used by other parts of the code which should not know anything about the `Person` internals. So, what should we do? We want a certain part of the logic to know about a structure definition that other parts of the code must not know about. That's where private header files jump in.

A private header file is an ordinary header file that is supposed to be included and used by a certain part of code or a certain class that actually needs it. Regarding example 8.2, the actual definition of `person_t` should be part of a private header. In the following code box, you will see an example of a private header file:

#ifndef EXTREME_C_EXAMPLES_CHAPTER_8_2_PERSON_P_H

#define EXTREME_C_EXAMPLES_CHAPTER_8_2_PERSON_P_H

// Private definition

typedef struct {

char first_name[32];

char last_name[32];

unsigned int birth_year;

} person_t;

#endif

Code Box 8-6 [ExtremeC_examples_chapter8_2_person_p.h]: The private header file which contains the actual definition of person_t

As you see, it only contains the definition of the `person_t` structure and nothing more than that. This is the part of the `Person` class which should stay private, but it needs to become public to the `Student` class. We are going to need this definition for defining the `student_t` attribute structure. The next code box demonstrates the private implementation of the `Person` class:

#include <stdlib.h>

#include <string.h>

// person_t is defined in the following header file.

#include "ExtremeC_examples_chapter8_2_person_p.h"

// Memory allocator

person_t* person_new() {

return (person_t*)malloc(sizeof(person_t));

}

// Constructor

void person_ctor(person_t* person,

const char* first_name,

const char* last_name,

unsigned int birth_year) {

strcpy(person->first_name, first_name);

strcpy(person->last_name, last_name);

person->birth_year = birth_year;

}

// D


## part 2/5

lass:

#include <stdlib.h>

#include <string.h>

// person_t is defined in the following header file.

#include "ExtremeC_examples_chapter8_2_person_p.h"

// Memory allocator

person_t* person_new() {

return (person_t*)malloc(sizeof(person_t));

}

// Constructor

void person_ctor(person_t* person,

const char* first_name,

const char* last_name,

unsigned int birth_year) {

strcpy(person->first_name, first_name);

strcpy(person->last_name, last_name);

person->birth_year = birth_year;

}

// Destructor

void person_dtor(person_t* person) {

// Nothing to do

}

// Behavior functions

void person_get_first_name(person_t* person, char* buffer) {

strcpy(buffer, person->first_name);

}

void person_get_last_name(person_t* person, char* buffer) {

strcpy(buffer, person->last_name);

}

unsigned int person_get_birth_year(person_t* person) {

return person->birth_year;

}

Code Box 8-7 [ExtremeC_examples_chapter8_2_person.c]: The definition of the Person class

There is nothing special about the definition of the `Person` class and it is like all previous examples. The following code box shows the public interface of the `Student` class:

#ifndef EXTREME_C_EXAMPLES_CHAPTER_8_2_STUDENT_H

#define EXTREME_C_EXAMPLES_CHAPTER_8_2_STUDENT_H

//Forward declaration

struct student_t;

// Memory allocator

struct student_t* student_new();

// Constructor

void student_ctor(struct student_t*,

const char* /* first name */,

const char* /* last name */,

unsigned int /* birth year */,

const char* /* student number */,

unsigned int /* passed credits */);

// Destructor

void student_dtor(struct student_t*);

// Behavior functions

void student_get_student_number(struct student_t*, char*);

unsigned int student_get_passed_credits(struct student_t*);

#endif

Code Box 8-8 [ExtremeC_examples_chapter8_2_student.h]: The public interface of the Student class

As you can see, the constructor of the class accepts similar arguments to the `Person` class's constructor. That's because a `student` object actually contains a `person` object and it needs those values for populating its composed `person` object.

This implies that the `student` constructor needs to set the attributes for the `person` part of the `student`.

Note that we have only two additional behavior functions as part of the `Student` class, and that's because we can use the `Person` class's behavior functions for `student` objects as well.

The next code box contains the private implementation of the `Student` class:

#include <stdlib.h>

#include <string.h>

#include "ExtremeC_examples_chapter8_2_person.h"

// person_t is defined in the following header

// file and we need it here.

#include "ExtremeC_examples_chapter8_2_person_p.h"

//Forward declaration

typedef struct {

// Here, we inherit all attributes from the person class and

// also we can use all of its behavior functions because of

// this nesting.

person_t person;

char* student_number;

unsigned int passed_credits;

} student_t;

// Memory allocator

student_t* student_new() {

return (student_t*)malloc(sizeof(student_t));

}

// Constructor

void student_ctor(student_t* student,

const char* first_name,

const char* last_name,

unsigned int birth_year,

const char* student_number,

unsigned int passed_credits) {

// Call the constructor of the parent class

person_ctor((struct person_t*)student,

first_name, last_name, birth_year);

student->student_number = (char*)malloc(16 * sizeof(char));

strcpy(student->student_number, student_number);

student->passed_credits = passed_credits;

}

// Destructor

void student_dtor(student_t* student) {

// We need to destruct the child object first.

free(student->student_number);

// Then, we need to call the destructor function

// of the parent class

person_dtor((struct person_t*)student);

}

// Behavior functions

void student_get_student_number(student_t* student,

char* buffer) {

strcpy(buffer, student->student_number);

}

unsigned int student_get_passed_credits(student_t* student) {

return student->passed_credits;

}

Code Box 8-9 [ExtremeC_examples_chapter8_2_student.c]: The private definition of the Student class

The preceding code box contains the most important code regarding the inheritance relationship. Firstly, we needed to include the private header of the `Person` class because as part of defining `student_t`, we want to have the first field from the `person_t` type. And, since that field is an actual variable and not a pointer, it requires that we have `person_t` already defined. Note that this variable must be the first field in the structure. Otherwise, we lose the possibility of using the `Person` class's behavior functions.

Again, in the preceding code box, as part of the `Student` class's constructor, we call the parent's constructor to initialize the attributes of the parent (composed) object. Look at how we cast the `student_t` pointer to a `person_t` pointer when passing it to the `person_ctor` function. This is possible just because the `person` field is the first member of `student_t`.

Similarly, as part of the `Student` class's destructor, we called the parent's destructor. This destruction should happen first at the child level and then the parent level, in the opposite order of construction. The next code box contains example 8.2's main scenario, which is going to use the `Student` class and create an object of type `Student`:

#include <stdio.h>

#include <stdlib.h>

#include "ExtremeC_examples_chapter8_2_person.h"

#include "ExtremeC_examples_chapter8_2_student.h"

int main(int argc, char** argv) {

// Create and construct the student object

struct student_t* student = student_new();

student_ctor(student, "John", "Doe",

1987, "TA5667", 134);

// Now, we use person's behavior functions to

// read person's attributes from the student object

char buffer[32];

// Upcasting to a pointer of parent type

struct person_t* person_ptr = (struct person_t*)student;

person_get_first_name(person_ptr, buffer);

printf("First name: %s\n", buffer);

person_get_last_name(person_ptr, buffer);

printf("Last name: %s\n", buffer);

printf("Birth year: %d\n", person_get_birth_year(person_ptr));

// Now, we read the attributes specific to the student object.

student_get_student_number(student, buffer);

printf("Student number: %s\n", buffer);

printf("Passed credits: %d\n",

student_get_passed_credits(student));

// Destruct and free the student object

student_dtor(student);

free(student);

return 0;

}

Code Box 8-10 [ExtremeC_examples_chapter8_2_main.c]: The main scenario of example 8.2

As you see in the main scenario, we have included the public interfaces of both the `Person` and `Student` classes (not the private header file), but we have only created one `student` object. As you can see, the `student` object has inherited all attributes from its internal `person` object, and they can be read via the `Person` class's behavior functions.

The following shell box shows how to compile and run example 8.2:

$ gcc -c ExtremeC_examples_chapter8_2_person.c -o person.o

$ gcc -c ExtremeC_examples_chapter8_2_student.c -o student.o

$ gcc -c ExtremeC_examples_chapter8_2_main.c -o main.o

$ gcc person.o student.o main.o -o ex8_2.out

$ ./ex8_2.out

First name: John

Last name: Doe

Birth year: 1987

Student number: TA5667

Passed credits: 134

$

Shell Box 8-2: Building and running example 8.2

The following example, example 8.3, will address the second approach to implementing inheritance relationships in C. The output should be very similar to example 8.2.

### The second approach to inheritance in C

Using the first approach, we kept a structure variable as the first field in the child's attribute structure. Now, using the second approach, we'll keep a pointer to the parent's structure variable. This way, the child class can be independent of the implementation of the parent class, which is a good thing, considering information-hiding concerns.

We gain some advantages, and we lose some by choosing the second approach. After demonstrating example 8.3 we will conduct a comparison between the two approaches, and you will see the advantages and disadvantages of using each of these techniques.

Example 8.3, below, is remarkably similar to example 8.2, especially in terms of the output and the final results. However, the main difference is that as part of this example, the `Student` class only relies on the public interface of the `Person` class, and not its private definition. This is great because it decouples the classes and allows us to easily change the implementation of the parent class without altering the implementation of the child class.

In the preceding example, the `Student` class didn't strictly violate information-hiding principles, but it could have done that because it had access to the actual definition of `person_t` and its fields. As a result, it could read or modify the fields without using `Person`'s behavior functions.

As noted, example 8.3 is remarkably similar to example 8.2, but it has some fundamental differences. The `Person` class has the same public interface as part of the new example. But this is not true regarding the `Student` class and its public interface has to be changed. The following code box shows the `Student` class's new public interface:

#ifndef EXTREME_C_EXAMPLES_CHAPTER_8_3_STUDENT_H

#define EXTREME_C_EXAMPLES_CHAPTER_8_3_STUDENT_H

//Forward declaration

struct student_t;

// Memory allocator

struct student_t* student_new();

// Constructor

void student_ctor(struct student_t*,

const char* /* first name */,

const char* /* last name */,

unsigned int /* birth year */,

const char* /* student number */,

unsigned int /* passed credits */);

// Destructor

void student_dtor(struct student_t*);

// Behavior functions

void student_get_first_name(struct student_t*, char*);

void student_get_last_name(struct student_t*, char*);

unsigned int student_get_birth_year(struct student_t*);

void student_get_student_number(struct student_t*, char*);

unsigned int student_get_passed_credits(struct student_t*);

#endif

Code Box 8-11 [ExtremeC_examples_chapter8_3_student.h]: The new public interface of the Student class

For reasons you will realize shortly, the `Student` class has to repeat all the behavior functions declared as part of the `Person` class. That's because of the fact that we can no longer cast a `student_t` pointer to a `person_t` pointer. In other words, upcasting doesn't work anymore regarding `Student` and `Person` pointers.

While the public interface of the `Person` class is not changed from example 8.2, its implementation has changed. The following code box demonstrates the implementation of the `Person` class as part of example 8.3:

#include <stdlib.h>

#include <string.h>

// Private definition

typedef struct {

char first_name[32];

char last_name[32];

unsigned int birth_year;

} person_t;

// Memory allocator

person_t* person_new() {

return (person_t*)malloc(sizeof(person_t));

}

// Constructor

void person_ctor(person_t* person,

const char* first_name,

const char* last_name,

unsigned int birth_year) {

strcpy(person->first_name, first_name);

strcpy(person->last_name, last_name);

person->birth_year = birth_year;

}

// Destructor

void person_dtor(person_t* person) {

// Nothing to do

}

// Behavior functions

void person_get_first_name(person_t* person, char* buffer) {

strcpy(buffer, person->first_name);

}

void person_get_last_name(person_t* person, char* buffer) {

strcpy(buffer, person->last_name);

}

unsigned int person_get_birth_year(person_t* person) {

return person->birth_year;

}

Code Box 8-12 [ExtremeC_examples_chapter8_3_person.c]: The new implementation of the Person class

As you see, the private definition of `person_t` is placed inside the source file and we are not using a private header anymore. This means that we are not going to share the definition with other classes such as the `Student` class at all.


## part 3/5

person_t* person, char* buffer) {

strcpy(buffer, person->last_name);

}

unsigned int person_get_birth_year(person_t* person) {

return person->birth_year;

}

Code Box 8-12 [ExtremeC_examples_chapter8_3_person.c]: The new implementation of the Person class

As you see, the private definition of `person_t` is placed inside the source file and we are not using a private header anymore. This means that we are not going to share the definition with other classes such as the `Student` class at all. We want to conduct a complete encapsulation of the `Person` class and hide all its implementation details.

The following is the private implementation of the `Student` class:

#include <stdlib.h>

#include <string.h>

// Public interface of the person class

#include "ExtremeC_examples_chapter8_3_person.h"

//Forward declaration

typedef struct {

char* student_number;

unsigned int passed_credits;

// We have to have a pointer here since the type

// person_t is incomplete.

struct person_t* person;

} student_t;

// Memory allocator

student_t* student_new() {

return (student_t*)malloc(sizeof(student_t));

}

// Constructor

void student_ctor(student_t* student,

const char* first_name,

const char* last_name,

unsigned int birth_year,

const char* student_number,

unsigned int passed_credits) {

// Allocate memory for the parent object

student->person = person_new();

person_ctor(student->person, first_name,

last_name, birth_year);

student->student_number = (char*)malloc(16 * sizeof(char));

strcpy(student->student_number, student_number);

student->passed_credits = passed_credits;

}

// Destructor

void student_dtor(student_t* student) {

// We need to destruct the child object first.

free(student->student_number);

// Then, we need to call the destructor function

// of the parent class

person_dtor(student->person);

// And we need to free the parent object's allocated memory

free(student->person);

}

// Behavior functions

void student_get_first_name(student_t* student, char* buffer) {

// We have to use person's behavior function

person_get_first_name(student->person, buffer);

}

void student_get_last_name(student_t* student, char* buffer) {

// We have to use person's behavior function

person_get_last_name(student->person, buffer);

}

unsigned int student_get_birth_year(student_t* student) {

// We have to use person's behavior function

return person_get_birth_year(student->person);

}

void student_get_student_number(student_t* student,

char* buffer) {

strcpy(buffer, student->student_number);

}

unsigned int student_get_passed_credits(student_t* student) {

return student->passed_credits;

}

Code Box 8-13 [ExtremeC_examples_chapter8_3_student.c]: The new implementation of the Student class

As demonstrated in the preceding code box, we've used the `Person` class's public interface by including its header file. In addition, as part of the definition of `student_t`, we've added a pointer field, which points to the parent `Person` object. This should remind you of the implementation of a composition relationship done as part of the previous chapter.

Note that there is no need for this pointer field to be the first item in the attribute structure. This is in contrast to what we saw in the first approach. The pointers of the types `student_t` and `person_t` are no longer interchangeable, and they are pointing to different addresses in the memory that are not necessarily adjacent. This is again in contrast to what we did in the previous approach.

Note that, as part of the `Student` class's constructor, we instantiate the parent object. Then, we construct it by calling the `Person` class's constructor and passing the required parameters. That's the same for destructors as well and we destruct the parent object lastly in the `Student` class's destructor.

Since we cannot use the behaviors of the `Person` class to read the inherited attributes, the `Student` class is required to offer its set of behavior functions to expose those inherited and private attributes.

In other words, the `Student` class has to provide some wrapper functions to expose the private attributes of its inner parent `person` object. Note that the `Student` object itself doesn't know anything about the private attributes of the `Person` object, and this is in contrast with what we saw in the first approach.

The main scenario is also very similar to how it was as part of example 8.2. The following code box demonstrates that:

#include <stdio.h>

#include <stdlib.h>

#include "ExtremeC_examples_chapter8_3_student.h"

int main(int argc, char** argv) {

// Create and construct the student object

struct student_t* student = student_new();

student_ctor(student, "John", "Doe",

1987, "TA5667", 134);

// We have to use student's behavior functions because the

// student pointer is not a person pointer and we cannot

// access to private parent pointer in the student object.

char buffer[32];

student_get_first_name(student, buffer);

printf("First name: %s\n", buffer);

student_get_last_name(student, buffer);

printf("Last name: %s\n", buffer);

printf("Birth year: %d\n", student_get_birth_year(student));

student_get_student_number(student, buffer);

printf("Student number: %s\n", buffer);

printf("Passed credits: %d\n",

student_get_passed_credits(student));

// Destruct and free the student object

student_dtor(student);

free(student);

return 0;

}

Code Box 8-14 [ExtremeC_examples_chapter8_3_main.c]: The main scenario of example 8.3

In comparison to the main function in example 8.2, we have not included the public interface of the `Person` class. We have also needed to use the `Student` class's behavior functions because the `student_t` and `person_t` pointers are not interchangeable anymore.

The following shell box demonstrates how to compile and run example 8.3. As you might have guessed, the outputs are identical:

$ gcc -c ExtremeC_examples_chapter8_3_person.c -o person.o

$ gcc -c ExtremeC_examples_chapter8_3_student.c -o student.o

$ gcc -c ExtremeC_examples_chapter8_3_main.c -o main.o

$ gcc person.o student.o main.o -o ex8_3.out

$ ./ex8_3.out

First name: John

Last name: Doe

Birth year: 1987

Student number: TA5667

Passed credits: 134

$

Shell Box 8-3: Building and running example 8.3

In the following section, we're going to compare the aforementioned approaches to implement an inheritance relationship in C.

### Comparison of two approaches

Now that you've seen two different approaches that we can take to implement inheritance in C, we can compare them. The following bullet points outline the similarities and differences between the two approaches:

- Both approaches intrinsically show composition relationships.
- The first approach keeps a structure variable in the child's attribute structure and relies on having access to the private implementation of the parent class. However, the second approach keeps a structure pointer from the incomplete type of the parent's attribute structure, and hence, it doesn't rely on the private implementation of the parent class.
- In the first approach, the parent and child types are strongly dependent. In the second approach, the classes are independent of each other, and everything inside the parent implementation is hidden from the child.
- In the first approach, you can have only one parent. In other words, it is a way to implement single inheritance in C. However, in the second approach, you can have as many parents as you like, thereby demonstrating the concept of multiple inheritance.
- In the first approach, the parent's structure variable must be the first field in the attribute structure of the child class, but in the second approach, the pointers to parent objects can be put anywhere in the structure.
- In the first approach, there were no two separate parent and child objects. The parent object was included in the child object, and a pointer to the child object was actually a pointer to the parent object.
- In the first approach, we could use the behavior functions of the parent class, but in the second approach, we needed to forward the parent's behavior functions through new behavior functions in the child class.

So far, we have only talked about inheritance itself and we haven't gone through its usages. One of the most important usages of inheritance is to have polymorphism in your object model. In the following section, we're going to talk about polymorphism and how it can be implemented in C.

# Polymorphism

Polymorphism is not really a relationship between two classes. It is mostly a technique for keeping the same code while having different behaviors. It allows us to extend code or add functionalities without having to recompile the whole code base.

In this section, we try to cover what polymorphism is and how we can have it in C. This also gives us a better view of how modern programming languages such as C++ implement polymorphism. We'll start by defining polymorphism.

## What is polymorphism?

Polymorphism simply means to have different behaviors by just using the same public interface (or set of behavior functions).

Suppose that we have two classes, `Cat` and `Duck`, and they each have a behavior function, `sound`, which makes them print their specific sound. Explaining polymorphism is not an easy task to do and we'll try to take a top-down approach in explaining it. First, we'll try to give you an idea of how polymorphic code looks and how it behaves, and then we'll dive into implementing it in C. Once you get the idea, it will be easier to move into the implementation. In the following code boxes, we first create some objects, and then we see how we would expect a polymorphic function to behave if polymorphism was in place. First, let's create three objects. We have already assumed that both the `Cat` and `Duck` classes are children of the `Animal` class:

struct animal_t* animal = animal_malloc();

animal_ctor(animal);

struct cat_t* cat = cat_malloc();

cat_ctor(cat);

struct duck_t* duck = duck_malloc();

duck_ctor(duck);

Code Box 8-15: Creating three objects of types Animal, Cat, and Duck

Without polymorphism, we would have called the `sound` behavior function for each object as follows:

// This is not a polymorphism

animal_sound(animal);

cat_sound(cat);

duck_sound(duck);

Code Box 8-16: Calling the sound behavior function on the created objects

And the output would be as follows:

Animal: Beeeep

Cat: Meow

Duck: Quack

Shell Box 8-4: The output of the function calls

The preceding code box is not demonstrating polymorphism because it uses different functions, `cat_sound` and `duck_sound`, to call specific behaviors from the `Cat` and `Duck` objects. However, the following code box shows how we expect a polymorphic function to behave. The following code box contains a perfect example of polymorphism:

// This is a polymorphism

animal_sound(animal);

animal_sound((struct animal_t*)cat);

animal_sound((struct animal_t*)duck);

Code Box 8-17: Calling the same sound behavior function on all three objects

Despite calling the same function three times, we expect to see different behaviors. It seems that passing different object pointers changes the actual behavior behind `animal_sound`. The following shell box would be the output of Code Box 8-17 if `animal_sound` was polymorphic:

Animal: Beeeep

Cat: Meow

Duck: Quake

Shell Box 8-5: The output of the function calls

As you see in Code Box 8-17, we have used the same function, `animal_sound`, but with different pointers, and as a result, different functions have been invoked behind the scenes.

CAUTION:

Please don't move forward if you're having trouble understanding the preceding code; if you are, please recap the previous section.

The preceding polymorphic code implies that there should be an inheritance relationship between the `Cat` and `Duck` classes with a third class, `Animal`, because we want to be able to cast the `duck_t` and `cat_t


## part 4/5

used the same function, `animal_sound`, but with different pointers, and as a result, different functions have been invoked behind the scenes.

CAUTION:

Please don't move forward if you're having trouble understanding the preceding code; if you are, please recap the previous section.

The preceding polymorphic code implies that there should be an inheritance relationship between the `Cat` and `Duck` classes with a third class, `Animal`, because we want to be able to cast the `duck_t` and `cat_t` pointers to an `animal_t` pointer. This also implies something else: we have to use the first approach of implementing inheritance in C in order to benefit from the polymorphism mechanism we introduced before.

You may recall that in the first approach to implementing inheritance, the child class had access to the private implementation of the parent class, and here a structure variable from the `animal_t` type should have been put as the first field in the definitions of the `duck_t` and `cat_t` attribute structures. The following code shows the relationship between these three classes:

typedef struct {

...} animal_t;

typedef struct {

animal_t animal;

...

} cat_t;

typedef struct {

animal_t animal;

...

} duck_t;

Code Box 8-18: The definitions of the attribute structures of classes Animal, Cat, and Duck

With this setup, we can cast the `duck_t` and `cat_t` pointers to the `animal_t` pointers, and then we can use the same behavior functions for both child classes.

So far, we have shown how a polymorphic function is expected to behave and how an inheritance relationship should be defined between the classes. What we haven't shown is how this polymorphic behavior is fulfilled. In other words, we haven't talked about the actual mechanism behind the polymorphism.

Suppose that the behavior function `animal_sound` is defined as it can be seen in code box 8-19. No matter the pointer you send inside as the argument, we will have always one behavior and the function calls won't be polymorphic without the underlying mechanism. The mechanism will be explained as part of example 8.4 which you will see shortly:

void animal_sound(animal_t* ptr) {

printf("Animal: Beeeep");

}

// This could be a polymorphism, but it is NOT!

animal_sound(animal);

animal_sound((struct animal_t*)cat);

animal_sound((struct animal_t*)duck);

Code Box 8-19: The function animal_sound is not polymorphic yet!

As you see next, calling the behavior function `animal_sound` with various pointers won't change the logic of the behavior function; in other words, it is not polymorphic. We will make this function polymorphic as part of the next example, example 8.4:

Animal: Beeeep

Animal: Beeeep

Animal: Beeeep

Shell Box 8-6: The output of the functional calls in Code Box 8-19

So, what is the underlying mechanism that enables polymorphic behavior functions? We answer that question in the upcoming sections, but before that we need to know why we want to have polymorphism in the first place.

## Why do we need polymorphism?

Before talking further about the way in which we're going to implement polymorphism in C, we should spend some time talking about the reasons behind the need for polymorphism. The main reason why polymorphism is needed is that we want to keep a piece of code "as is," even when using it with various subtypes of a base type. You are going to see some demonstration of this shortly in the examples.

We don't want to modify the current logic very often when we add new subtypes to the system, or when the behavior of one subtype is being changed. It's just not realistic to have zero changes when a new feature is added – there will always be some changes – but using polymorphism, we can significantly reduce the number of changes that are needed.

Another motivation for having polymorphism is due to the concept of abstraction. When we have abstract types (or classes), they usually have some vague or unimplemented behavior functions that need to be overridden in child classes and polymorphism is the key way to do this.

Since we want to use abstract types to write our logic, we need a way to call the proper implementation when dealing with pointers of very abstract types. This is another place where polymorphism comes in. No matter what the language is, we need a way to have polymorphic behaviors, otherwise the cost of maintaining a big project can grow quickly, for instance when we are going to add a new subtype to our code.

Now that we've established the importance of polymorphism, it's time to explain how we can have it in C.

## How to have polymorphic behavior in C

If we want to have polymorphism in C, we need to use the first approach we explored to implementing inheritance in C. To achieve polymorphic behavior, we can utilize function pointers. However, this time, these function pointers need to be kept as some fields in the attribute structure. Let's implement the animal sound example to illustrate this.

We have three classes, `Animal`, `Cat`, and `Duck`, and `Cat` and `Duck` are subtypes of `Animal`. Each class has one header and one source. The `Animal` class has an extra private header file that contains the actual definition of its attribute structure. This private header is required since we are taking the first approach to implement inheritance. The private header is going to be used by the `Cat` and `Duck` classes.

The following code box shows the public interface of the `Animal` class:

#ifndef EXTREME_C_EXAMPLES_CHAPTER_8_4_ANIMAL_H

#define EXTREME_C_EXAMPLES_CHAPTER_8_4_ANIMAL_H

// Forward declaration

struct animal_t;

// Memory allocator

struct animal_t* animal_new();

// Constructor

void animal_ctor(struct animal_t*);

// Destructor

void animal_dtor(struct animal_t*);

// Behavior functions

void animal_get_name(struct animal_t*, char*);

void animal_sound(struct animal_t*);

#endif

Code Box 8-20 [ExtremeC_examples_chapter8_4_animal.h]: The public interface of the Animal class

The `Animal` class has two behavior functions. The `animal_sound` function is supposed to be polymorphic and can be overridden by the child classes, while the other behavior function, `animal_get_name`, is not polymorphic, and children cannot override it.

The following is the private definition of the `animal_t` attribute structure:

#ifndef EXTREME_C_EXAMPLES_CHAPTER_8_4_ANIMAL_P_H

#define EXTREME_C_EXAMPLES_CHAPTER_8_4_ANIMAL_P_H

// The function pointer type needed to point to

// different morphs of animal_sound

typedef void (*sound_func_t)(void*);

// Forward declaration

typedef struct {

char* name;

// This member is a pointer to the function which

// performs the actual sound behavior

sound_func_t sound_func;

} animal_t;

#endif

Code Box 8-21 [ExtremeC_examples_chapter8_4_animal_p.h]: The private header of the Animal class

In polymorphism, every child class can provide its own version of the `animal_sound` function. In other words, every child class can override the function inherited from its parent class. Therefore, we need to have a different function for each child class that wants to override it. This means, if the child class has overridden the `animal_sound`, its own overridden function should be called.

That's why we are using function pointers here. Each instance of `animal_t` will have a function pointer dedicated to the behavior `animal_sound`, and that pointer is pointing to the actual definition of the polymorphic function inside the class.

For each polymorphic behavior function, we have a dedicated function pointer. Here, you will see how we use this function pointer to do the correct function call in each subclass. In other words, we show how the polymorphism actually works.

The following code box shows the definition of the `Animal` class:

#include <stdlib.h>

#include <string.h>

#include <stdio.h>

#include "ExtremeC_examples_chapter8_4_animal_p.h"

// Default definition of the animal_sound at the parent level

void __animal_sound(void* this_ptr) {

animal_t* animal = (animal_t*)this_ptr;

printf("%s: Beeeep\n", animal->name);

}

// Memory allocator

animal_t* animal_new() {

return (animal_t*)malloc(sizeof(animal_t));

}

// Constructor

void animal_ctor(animal_t* animal) {

animal->name = (char*)malloc(10 * sizeof(char));

strcpy(animal->name, "Animal");

// Set the function pointer to point to the default definition

animal->sound_func = __animal_sound;

}

// Destructor

void animal_dtor(animal_t* animal) {

free(animal->name);

}

// Behavior functions

void animal_get_name(animal_t* animal, char* buffer) {

strcpy(buffer, animal->name);

}

void animal_sound(animal_t* animal) {

// Call the function which is pointed by the function pointer.

animal->sound_func(animal);

}

Code Box 8-22 [ExtremeC_examples_chapter8_4_animal.c]: The definition of the Animal class

The actual polymorphic behavior is happening in Code Box 8-22, inside the function `animal_sound`. The private function `__animal_sound` is supposed to be the default behavior of the `animal_sound` function when the subclasses decide not to override it. You will see in the next chapter that polymorphic behavior functions have a default definition which will get inherited and used if the subclass doesn't provide the overridden version.

Moving on, inside the constructor `animal_ctor`, we store the address of `__animal_sound` into the `sound_func` field of the `animal` object. Remember that `sound_func` is a function pointer. In this setup, every child object inherits this function pointer, which points to the default definition `__animal_sound`.

And the final step, inside the behavior function `animal_sound`, we just call the function that is being pointed to by the `sound_func` field. Again, `sound_func` is the function pointer field pointing to the actual definition of the sound behavior which in the preceding case is `__animal_sound`. Note that the `animal_sound` function behaves more like a relay to the actual behavior function.

Using this setup, if the `sound_func` field was pointing to another function, then that function would have been called if `animal_sound` was invoked. That's the trick we are going to use in the `Cat` and `Duck` classes to override the default definition of the `sound` behavior.

Now, it's time to show the `Cat` and `Duck` classes. The following code boxes will show the `Cat` class's public interface and private implementation. First, we show the `Cat` class's public interface:

#ifndef EXTREME_C_EXAMPLES_CHAPTER_8_4_CAT_H

#define EXTREME_C_EXAMPLES_CHAPTER_8_4_CAT_H

// Forward declaration

struct cat_t;

// Memory allocator

struct cat_t* cat_new();

// Constructor

void cat_ctor(struct cat_t*);

// Destructor

void cat_dtor(struct cat_t*);

// All behavior functions are inherited from the animal class.

#endif

Code Box 8-23 [ExtremeC_examples_chapter8_4_cat.h]: The public interface of the Cat class

As you will see shortly, it will inherit the `sound` behavior from its parent class, the `Animal` class.

The following code box shows the definition of the `Cat` class:

#include <stdio.h>

#include <stdlib.h>

#include <string.h>

#include "ExtremeC_examples_chapter8_4_animal.h"

#include "ExtremeC_examples_chapter8_4_animal_p.h"

typedef struct {

animal_t animal;

} cat_t;

// Define a new behavior for the cat's sound

void __cat_sound(void* ptr) {

animal_t* animal = (animal_t*)ptr;

printf("%s: Meow\n", animal->name);

}

// Memory allocator

cat_t* cat_new() {

return (cat_t*)malloc(sizeof(cat_t));

}

// Constructor

void cat_ctor(cat_t* cat) {

animal_ctor((struct animal_t*)cat);

strcpy(cat->animal.name, "Cat");

// Point to the new behavior function. Overriding

// is actually happening here.

cat->animal.sound_func = __cat_sound;

}

// Destructor

void cat_dtor(cat_t* cat) {

animal_dtor((struct animal_t*)cat);

}

Code Box 8-24 [ExtremeC_examples_chapter8_4_cat.c]: The private implementation of the Cat class

As you see in the previous code box, 


## part 5/5

eturn (cat_t*)malloc(sizeof(cat_t));

}

// Constructor

void cat_ctor(cat_t* cat) {

animal_ctor((struct animal_t*)cat);

strcpy(cat->animal.name, "Cat");

// Point to the new behavior function. Overriding

// is actually happening here.

cat->animal.sound_func = __cat_sound;

}

// Destructor

void cat_dtor(cat_t* cat) {

animal_dtor((struct animal_t*)cat);

}

Code Box 8-24 [ExtremeC_examples_chapter8_4_cat.c]: The private implementation of the Cat class

As you see in the previous code box, we have defined a new function for the cat's sound, `__cat_sound`. Then inside the constructor, we make the `sound_func` pointer point to this function.

Now, overriding is happening, and from now on, all `cat` objects will actually call `__cat_sound` instead of `__animal_sound`. The same technique is used for the `Duck` class.

The following code box shows the public interface of the `Duck` class:

#ifndef EXTREME_C_EXAMPLES_CHAPTER_8_4_DUCK_H

#define EXTREME_C_EXAMPLES_CHAPTER_8_4_DUCK_H

// Forward declaration

struct duck_t;

// Memory allocator

struct duck_t* duck_new();

// Constructor

void duck_ctor(struct duck_t*);

// Destructor

void duck_dtor(struct duck_t*);

// All behavior functions are inherited from the animal class.

#endif

Code Box 8-25 [ExtremeC_examples_chapter8_4_duck.h]: The public interface of the Duck class

As you see, that's quite similar to the `Cat` class. Let's bring up the private definition of the `Duck` class:

#include <stdio.h>

#include <stdlib.h>

#include <string.h>

#include "ExtremeC_examples_chapter8_4_animal.h"

#include "ExtremeC_examples_chapter8_4_animal_p.h"

typedef struct {

animal_t animal;

} duck_t;

// Define a new behavior for the duck's sound

void __duck_sound(void* ptr) {

animal_t* animal = (animal_t*)ptr;

printf("%s: Quacks\n", animal->name);

}

// Memory allocator

duck_t* duck_new() {

return (duck_t*)malloc(sizeof(duck_t));

}

// Constructor

void duck_ctor(duck_t* duck) {

animal_ctor((struct animal_t*)duck);

strcpy(duck->animal.name, "Duck");

// Point to the new behavior function. Overriding

// is actually happening here.

duck->animal.sound_func = __duck_sound;

}

// Destructor

void duck_dtor(duck_t* duck) {

animal_dtor((struct animal_t*)duck);

}

Code Box 8-26 [ExtremeC_examples_chapter8_4_duck.c]: The private implementation of the Duck class

As you can see, the technique has been used to override the default definition of the `sound` behavior. A new private behavior function, `__duck_sound`, has been defined that does the duck-specific sound, and the `sound_func` pointer is updated to point to this function. This is basically the way that polymorphism is introduced to C++. We will talk more about this in the next chapter.

Finally, the following code box demonstrates the main scenario of example 8.4:

#include <stdio.h>

#include <stdlib.h>

#include <string.h>

// Only public interfaces

#include "ExtremeC_examples_chapter8_4_animal.h"

#include "ExtremeC_examples_chapter8_4_cat.h"

#include "ExtremeC_examples_chapter8_4_duck.h"

int main(int argc, char** argv) {

struct animal_t* animal = animal_new();

struct cat_t* cat = cat_new();

struct duck_t* duck = duck_new();

animal_ctor(animal);

cat_ctor(cat);

duck_ctor(duck);

animal_sound(animal);

animal_sound((struct animal_t*)cat);

animal_sound((struct animal_t*)duck);

animal_dtor(animal);

cat_dtor(cat);

duck_dtor(duck);

free(duck);

free(cat);

free(animal);

return 0;

}

Code Box 8-27 [ExtremeC_examples_chapter8_4_main.c]: The main scenario of example 8.4

As you see in the preceding code box, we are only using the public interfaces of the `Animal`, `Cat`, and `Duck` classes. So, the `main` function doesn't know anything about the internal implementation of the classes. Calling the `animal_sound` function with passing different pointers demonstrates how a polymorphic behavior should work. Let's look at the output of the example.

The following shell box shows how to compile and run example 8.4:

$ gcc -c ExtremeC_examples_chapter8_4_animal.c -o animal.o

$ gcc -c ExtremeC_examples_chapter8_4_cat.c -o cat.o

$ gcc -c ExtremeC_examples_chapter8_4_duck.c -o duck.o

$ gcc -c ExtremeC_examples_chapter8_4_main.c -o main.o

$ gcc animal.o cat.o duck.o main.o -o ex8_4.out

$ ./ex8_4.out

Animal: Beeeep

Cat: Meow

Duck: Quake

$

Shell Box 8-7: The compilation, execution, and output of example 8.4

As you can see in example 8.4, in class-based programming languages the behavior functions which we want to be polymorphic need special care and should be treated differently. Otherwise, a simple behavior function without the underlying mechanism that we discussed as part of example 8.4 cannot be polymorphic. That's why we have a special name for these behavior functions, and why we use specific keywords to denote a function to be polymorphic in a language such as C++. These functions are called virtual functions. Virtual functions are behavior functions that can be overridden by child classes. Virtual functions need to be tracked by the compiler, and proper pointers should be placed in the corresponding objects to point to the actual definitions when overridden. These pointers are used at runtime to execute the right version of the function.

In the next chapter, we'll see how C++ handles object-oriented relationships between classes. Also, we will find out how C++ implements polymorphism. We will also discuss Abstraction which is a direct result of polymorphism.

# Summary

In this chapter, we continued our exploration of topics in OOP, picking up from where we left off in the previous chapter. The following topics were discussed in this chapter:

- We explained how inheritance works and looked at the two approaches that we can use to implement inheritance in C.
- The first approach allows direct access to all the private attributes of the parent class, but the second approach has a more conservative approach, hiding the private attributes of the parent class.
- We compared these approaches, and we saw that each of them can be suitable in some use cases.
- Polymorphism was the next topic that we explored. To put it simply, it allows us to have different versions of the same behavior and invoke the correct behavior using the public API of an abstract supertype.
- We saw how to write polymorphic code in C and saw how function pointers contribute to choosing the correct version of a particular behavior at runtime.

The next chapter will be our final chapter about object orientation. As part of it, we'll explore how C++ handles encapsulation, inheritance, and polymorphism. More than that, we will discuss the topic of abstraction and how it leads to a bizarre type of class which is called an abstract class. We cannot create objects from these classes!


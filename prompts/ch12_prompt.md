# =============================================================================
# INSTRUCTIONS FOR AI AGENTS & CODING ASSISTANTS:
# TARGET OUTPUT FILE: packs/extreme-c/ch12.yaml
#
# [MANDATORY DIRECTIVES — READ CAREFULLY BEFORE WRITING A SINGLE LINE]
# 1. PUT ALL YOUR MIGHT & GO PLUS ULTRA (NO HALF-ASSING):
#    The learner studies ONLY from your generated YAML, never from the book.
#    Produce a masterwork of pedagogical engineering grounded in cognitive science.
#    Zero placeholders (NO 'TODO', NO '/* rest of code */', NO lazy hand-waving).
# 2. DO NOT WORRY ABOUT LENGTH — DEPTH AND CLARITY OVERRIDE BREVITY:
#    Never rush, compress, or omit blocks to save tokens. An exhaustive, deeply explained
#    pack with 8–15 blocks and 30+ checks is vastly superior to a short summary.
# 3. MULTI-TURN / MULTI-STEP GENERATION SUPPORTED & ENCOURAGED:
#    If the chapter is concept-dense or has many blocks, DO NOT attempt to crush everything
#    into one rushed output. Write the file incrementally using your file tools (e.g.
#    create skeleton + blocks 1–4, then append blocks 5–8, blocks 9–12, cards, lab, and test),
#    or in sequential parts if in chat. Take as many turns/steps as needed to do it justice.
# 4. COMPREHENSIVE CODE EXPLANATIONS & NOTIONAL MACHINE:
#    Every single code snippet MUST be accompanied by an exhaustive, intuitive breakdown:
#    line-by-line syntax, Notional Machine state transitions (stack, heap, pointers, registers),
#    the architectural 'why' behind the design, and boundary failure traps.
# 5. INTUITION-FIRST COMPREHENSIBILITY:
#    Bridge technical jargon with intuitive mental models and physical analogies before
#    introducing formal syntax. Make every concept deeply understandable for self-study.
# 6. INTERACTIVE LEARNING INNOVATIONS (v0.8+):
#    Elevate interactivity beyond basic MCQ: author `trace` checks for tricky pointer/state
#    mutations, `faded: true` Parsons checks for scaffolded syntax construction, `spot-bug`
#    checks for reading compiler/sanitizer diagnostics, and `subgoals` on complex code blocks.
# 7. EXECUTION & VALIDATION PROTOCOL:
#    - Autonomous Agents with Tools: Write/edit directly to `packs/extreme-c/ch12.yaml`.
#      Then execute: python main.py validate --book extreme-c --chapter ch12 --strict
#    - Chat-Only Interfaces: Output in ```yaml``` fenced blocks (or sequential parts) and
#      direct the user to save to `packs/extreme-c/ch12.yaml`.
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
chapter YAML file for the `termlearn` terminal course. The learner will study
ONLY from your YAML — never from the book. Teach, don't summarize.

### Source paths you are working with (MUST respect)

- `docs/SRS.md` — the normative spec. Its §4.8 (pack schema) and §4.9
  (runner protocol) excerpts are appended to this prompt; treat them as
  binding. All other `docs/SRS.md` references below name their section.
- `prompts/ASK_USER.md` — interrogate the user per that file first.
- `books/<slug>/raw_chapters/<id>.txt` — the pasted chapter source.
- `packs/<slug>/<id>.yaml` — TARGET OUTPUT FILE.
  - If you are an AI coding agent with file-creation tools: write the completed
    YAML pack directly to `packs/<slug>/<id>.yaml`, then execute
    `python main.py validate --book <slug> --chapter <id> --strict` to verify it.
  - If you are in a chat-only environment: output inside a single `yaml`-fenced
    code block and state `packs/<slug>/<id>.yaml` as the save destination.
- `packs/<slug>/runner/run` — runner script (only when authoring a runner, §5).

## 0. Output destination & protocol (MUST)

- **Target File**: `packs/<slug>/<id>.yaml` (e.g. `packs/extreme-c/ch09.yaml`).
  - **Autonomous Agents with Tools**: Write the generated file directly to
    `packs/<slug>/<id>.yaml` using your file creation tool, then validate it
    via `python main.py validate --book <slug> --chapter <id> --strict`.
  - **Chat-Only Models**: Output exactly ONE `yaml`-fenced block with the full
    chapter file and direct the user to save it to `packs/<slug>/<id>.yaml`.
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
- **Faded Parsons (`faded: true`)**:
  [Research: Fromont et al. 2023 — Faded Parsons problems require learners to arrange
  lines AND fill in missing critical tokens, providing an optimal intermediate fade
  before authoring code from scratch.]
  ```yaml
  - kind: order
    faded: true
    q: "Order the lines and fill in the missing allocation size argument:"
    lines:
      - "car_t* car = (car_t*)malloc(_____);"
      - "if (!car) return NULL;"
      - "car->speed = 0;"
      - "return car;"
    answer_order: [0, 1, 2, 3]
    blanks:
      - line_idx: 0
        token: "_____"
        answer_text: "sizeof(car_t)"
        accepted: ["sizeof(car_t)", "sizeof(*car)"]
    why: "car_malloc must allocate the byte size of car_t before initializing attributes."
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


---

# ASK_USER.md — interrogation template (SRS FR-ASK-001..003)
# The AI MUST ask these BEFORE emitting YAML. MUST NOT emit final YAML until
# the user answers or says `use defaults`.
#
# IMPORTANT: When authoring quizzes, checks, and questions:
# 1. NEVER refer to questions or exercises in the book (e.g. never say "refer to question 3 in book").
#    Always put the whole question with complete, self-contained context and code.
# 2. NEVER worry about YAML length — multi-turn generation across sequential steps is supported.
# 3. Always include thorough, line-by-line explanations for every code block and reveal the Notional Machine.
# 4. Put all your might and go Plus Ultra — zero half-assing, no placeholders.

Ask (compact, one message, numbered):

1. **Level** — novice / comfortable-in-C / experienced? (affects depth of
   `explain_md` and whether `model` blocks get extra `viz` steps.)
   Default: comfortable-in-C.
2. **Depth vs speed** — deep (more blocks, ≥3 checks each) or fast (fewer
   blocks, 1-2 checks each) or balanced (2 blocks per major concept)? Default: deep.
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

# CHAPTER ch12 OF extreme-c (3 part(s))
# TARGET FILE DESTINATION: packs/extreme-c/ch12.yaml
# Process: answer ASK_USER questions first, then emit/write YAML to `packs/extreme-c/ch12.yaml`.


## part 1/3

# Chapter 0 9

<!-- source: Text/abstraction_and_oop_in_cplusplus.xhtml | spine-id: abstraction_and_oop_in_cplusplus.xhtml | chapter: ch12 -->

# Chapter 0 9

# Abstraction and OOP in C++

This is the final chapter on OOP in C. In this chapter, we are going to cover the remaining topics and introduce you to a new programming paradigm. In addition, we explore C++ and look at how it implements object-oriented concepts behind the scenes.

As part of this chapter, we will cover the following topics:

- Firstly, we discuss the Abstraction. This continues our discussion regarding inheritance and polymorphism and will be the last topic that we cover as part of OOP in C. We show how abstraction helps us in designing object models that have the maximum extendibility and the minimum dependencies between its various components.
- We talk about how object-oriented concepts have been implemented in a famous C++ compiler, `g++` in this case. As part of this, we see that how close the approaches that we have discussed so far are in accordance with the approaches that `g++` has taken to provide the same concepts.

Let's start the chapter by talking about abstraction.

# Abstraction

Abstraction can have a very general meaning in various fields of science and engineering. But in programming, and especially in OOP, abstraction essentially deals with abstract data types. In class-based object orientation, abstract data types are the same as abstract classes. Abstract classes are special classes that we cannot create an object from; they are not ready or complete enough to be used for object creation. So, why do we need to have such classes or data types? This is because when we work with abstract and general data types, we avoid creating strong dependencies between various parts of code.

As an example, we can have the following relationships between the Human and Apple classes:

An object of the Human class eats an object of the Apple class.

An object of the Human class eats an object of the Orange class.

If the classes that an object from the Human class can eat were expanded to more than just Apple and Orange, we would need to add more relations to the Human class. Instead, though, we could create an abstract class called Fruit that is the parent of both Apple and Orange classes, and we could set the relation to be between Human and Fruit only. Therefore, we can turn our preceding two statements into one:

An object of the Human class eats an object from a subtype of the Fruit class.

The Fruit class is abstract because it lacks information about shape, taste, smell, color, and many more attributes of a specific fruit. Only when we have an apple or an orange do we know the exact values of the different attributes. The Apple and Orange classes are said to be concrete types.

We can even add more abstraction. The Human class can eat Salad or Chocolate as well. So, we can say:

An object of the Human type eats an object from a subtype of the Eatable class.

As you can see, the abstraction level of Eatable is even higher than that of Fruit. Abstraction is a great technique for designing an object model that has minimal dependency on concrete types and allows the maximum future extension to the object model when more concrete types are introduced to the system.

Regarding the preceding example, we could also add further abstraction by using the fact that Human is an Eater. Then, we could make our statement even more abstract:

An object from a subtype of the Eater class eats an object from a subtype of the Eatable class.

We can continue to abstract everything in an object model and find abstract data types that are more abstract than the level we need to solve our problem. This is usually called over-abstraction. It happens when you try to create abstract data types that have no real application, either for your current or your future needs. This should be avoided at all costs because abstraction can cause problems, despite all the benefits it provides.

A general guide regarding the amount of abstraction that we need can be found as part of the abstraction principle. I got the following quote from its Wikipedia page, https://en.wikipedia.org/wiki/Abstraction_principle_(computer_programming). It simply states:

Each significant piece of functionality in a program should be implemented in just one place in the source code. Where similar functions are carried out by distinct pieces of code, it is generally beneficial to combine them into one by abstracting out the varying parts.

While at first glance you may not see any sign of object orientation or inheritance in this statement, by giving some further thought to it you will notice that what we did with inheritance was based on this principle. Therefore, as a general rule, whenever you don't expect to have variations in a specific logic, there is no need to introduce abstraction at that point.

In a programming language, inheritance and polymorphism are two capabilities that are required in order to create abstraction. An abstract class such as Eatable is a supertype in relation to its concrete classes, such as Apple, and this is accomplished by inheritance.

Polymorphism also plays an important role. There are behaviors in an abstract type that cannot have default implementation at that abstraction level. For example, taste as an attribute implemented using a behavior function such as `eatable_get_taste` as part of the Eatable class cannot have an exact value when we are talking about an Eatable object. In other words, we cannot create an object directly from the Eatable class if we don't know how to define the `eatable_get_taste` behavior function.

The preceding function can only be defined when the child class is concrete enough. For example, we know that Apple objects should return sweet for their taste (we've assumed here that all apples are sweet). This is where polymorphism helps. It allows a child class to override its parent's behaviors and return the proper taste, for example.

If you remember from the previous chapter, the behavior functions that can be overridden by child classes are called virtual functions. Note that it is possible that a virtual function doesn't have any definition at all. Of course, this makes the owner class abstract.

By adding more and more abstraction, at a certain level, we reach classes that have no attributes and contain only virtual functions with no default definitions. These classes are called interfaces. In other words, they expose functionalities but they don't offer any implementation at all, and they are usually used to create dependencies between various components in a software project. As an example, in our preceding examples, the Eater and Eatable classes are interfaces. Note that, just like abstract classes, you must not create an object from an interface. The following code shows why this cannot be done in a C code.

The following code box is the equivalent code written for the preceding interface Eatable in C using the techniques we introduced in the previous chapter to implement inheritance and polymorphism:

typedef enum {SWEET, SOUR} taste_t;

// Function pointer type

typedef taste_t (*get_taste_func_t)(void*);

typedef struct {

// Pointer to the definition of the virtual function

get_taste_func_t get_taste_func;

} eatable_t;

eatable_t* eatable_new() { ... }

void eatable_ctor(eatable_t* eatable) {

// We don't have any default definition for the virtual function

eatable->get_taste_func = NULL;

}

// Virtual behavior function

taste_t eatable_get_taste(eatable_t* eatable) {

return eatable->get_taste_func(eatable);

}

Code Box 9-1: The Eatable interface in C

As you can see, in the constructor function we have set the `get_taste_func` pointer to `NULL`. So, calling the `eatable_get_taste` virtual function can lead to a segmentation fault. From the coding perspective, that's basically why that we must not create an object from the Eatable interface other than the reasons we know from the definition of the interface and the design point of view.

The following code box demonstrates how creating an object from the Eatable interface, which is totally possible and allowed from a C point of view, can lead to a crash and must not be done:

eatable_t *eatable = eatable_new();

eatable_ctor(eatable);

taste_t taste = eatable_get_taste(eatable); // Segmentation fault!

free(eatable);

Code Box 9-2: Segmentation fault when creating an object from the Eatable interface and calling a pure virtual function from it

To prevent ourselves from creating an object from an abstract type, we can remove the allocator function from the class's public interface. If you remember the approaches that we took in the previous chapter to implement inheritance in C, by removing the allocator function, only child classes are able to create objects from the parent's attribute structure.

External codes are then no longer able to do so. For instance, in the preceding example, we do not want any external code to be able to create any object from the structure `eatable_t`. In order to do that, we need to have the attribute structure forward declared and make it an incomplete type. Then, we need to remove the public memory allocator `eatable_new` from the class.

To summarize what we need to do to have an abstract class in C, you need to nullify the virtual function pointers that are not meant to have a default definition at that abstraction level. At an extremely high level of abstraction, we have an interface whose all function pointers are null. To prevent any external code from creating objects from abstract types, we should remove the allocator function from the public interface.

In the following section, we are going to compare similar object-oriented features in C and C++. This gives us an idea how C++ has been developed from pure C.

# Object-oriented constructs in C++

In this section, we are going to compare what we did in C and the underlying mechanisms employed in a famous C++ compiler, `g++` in this case, for supporting encapsulation, inheritance, polymorphism, and abstraction.

We want to show that there is a close accordance between the methods by which object-oriented concepts are implemented in C and C++. Note that, from now on, whenever we refer to C++, we are actually referring to the implementation of `g++` as one of the C++ compilers, and not the C++ standard. Of course, the underlying implementations can be different for various compilers, but we don't expect to see a lot of differences. We will also be using `g++` in a 64-bit Linux setup.

We are going to use the previously discussed techniques to write an object-oriented code in C, and then we write the same program in C++, before jumping to the final conclusion.

## Encapsulation

It is difficult to go deep into a C++ compiler and see how it uses the techniques that we've been exploring so far to produce the final executable, but there is one clever trick that we can use to actually see this. The way to do this is to compare the assembly instructions generated for two similar C and C++ programs.

This is exactly what we are going to do to demonstrate that the C++ compiler ends up generating the same assembly instructions as a C program that uses the OOP techniques that we've been discussing in the previous chapters.

Example 9.1 is about two C and C++ programs addressing the same simple object-oriented logic. There is a `Rectangle` class in this example, which has a behavior function for calculating its area. We want to see and compare the generated assembly codes for the same behavior function in both programs. The following code box demonstrates the C version:

#include <stdio.h>

typedef struct {

int width;

int length;

} rect_t;

int rect_area(rect_t* rect) {

return rect->width * rect->length;

}

int main(int argc, char** argv) {

rect_t r;

r.width = 10;

r.length = 25;

int area = rect_area(&r);

printf("Area: %d\n", area);



## part 2/3

s example, which has a behavior function for calculating its area. We want to see and compare the generated assembly codes for the same behavior function in both programs. The following code box demonstrates the C version:

#include <stdio.h>

typedef struct {

int width;

int length;

} rect_t;

int rect_area(rect_t* rect) {

return rect->width * rect->length;

}

int main(int argc, char** argv) {

rect_t r;

r.width = 10;

r.length = 25;

int area = rect_area(&r);

printf("Area: %d\n", area);

return 0;

}

Code Box 9-3 [ExtremeC_examples_chapter9_1.c]: Encapsulation example in C

And the following code box shows the C++ version of the preceding program:

#include <iostream>

class Rect {

public:

int Area() {

return width * length;

}

int width;

int length;

};

int main(int argc, char** argv) {

Rect r;

r.width = 10;

r.length = 25;

int area = r.Area();

std::cout << "Area: " << area << std::endl;

return 0;

}

Code Box 9-4 [ExtremeC_examples_chapter9_1.cpp]: Encapsulation example in C++

So, let's generate the assembly codes for the preceding C and C++ programs:

$ gcc -S ExtremeC_examples_chapter9_1.c -o ex9_1_c.s

$ g++ -S ExtremeC_examples_chapter9_1.cpp -o ex9_1_cpp.s

$

Shell Box 9-1: Generating the assembly outputs for the C and C++ codes

Now, let's dump the `ex9_1_c.s` and `ex9_1_cpp.s` files and look for the definition of the behavior functions. In `ex9_1_c.s`, we should look for the `rect_area` symbol, and in `ex9_1_cpp.s`, we should look for the `_ZN4Rect4AreaEv` symbol. Note that C++ mangles the symbol names, and that's why you need to search for this strange symbol. Name mangling in C++ has been discussed in Chapter 2, Compilation and Linking.

For the C program, the following is the generated assembly for the `rect_area` function:

$ cat ex9_1_c.s

...

rect_area:

.LFB0:

.cfi_startproc

pushq %rbp

.cfi_def_cfa_offset 16

.cfi_offset 6, -16

movq %rsp, %rbp

.cfi_def_cfa_register 6

movq %rdi, -8(%rbp)

movq -8(%rbp), %rax

movl (%rax), %edx

movq -8(%rbp), %rax

movl 4(%rax), %eax

imull %edx, %eax

popq %rbp

.cfi_def_cfa 7, 8

Ret

.cfi_endproc

...

$

Shell Box 9-2: The generated assembly code of the rect_area function

The following is the generated assembly instructions for the `Rect::Area` function:

$ cat ex9_1_cpp.s

...

_ZN4Rect4AreaEv:

.LFB1493:

.cfi_startproc

pushq %rbp

.cfi_def_cfa_offset 16

.cfi_offset 6, -16

movq %rsp, %rbp

.cfi_def_cfa_register 6

movq %rdi, -8(%rbp)

movq -8(%rbp), %rax

movl (%rax), %edx

movq -8(%rbp), %rax

movl 4(%rax), %eax

imull %edx, %eax

popq %rbp

.cfi_def_cfa 7, 8

Ret

.cfi_endproc

...

$

Shell Box 9-3: The generated assembly code of the Rect::Area function

Unbelievably, they are exactly the same! I'm not sure how the C++ code turns into the preceding assembly code, but I'm sure that the assembly code generated for the preceding C function is almost, to high degree of accuracy, equivalent to the assembly code generated for the C++ function.

We can conclude from this that the C++ compiler has used a similar approach to that which we used in C, introduced as implicit encapsulation as part of Chapter 6, OOP and Encapsulation, to implement the encapsulation. Like what we did with implicit encapsulation, you can see in Code Box 9-3 that a pointer to the attribute structure is passed to the `rect_area` function as the first argument.

As part of the boldened assembly instructions in both shell boxes, the `width` and `length` variables are being read by adding to the memory address passed as the first argument. The first pointer argument can be found in the `%rdi` register according to System V ABI. So, we can infer that C++ has changed the `Area` function to accept a pointer argument as its first argument, which points to the object itself.

As a final word on encapsulation, we saw how C and C++ are closely related regarding encapsulation, at least in this simple example. Let's see if the same is true regarding inheritance as well.

## Inheritance

Investigating inheritance is easier than encapsulation. In C++, the pointers from a child class can be assigned to the pointers from the parent class. Also, the child class should have access to the private definition of the parent class.

Both of these behaviors imply that C++ is using our first approach to implementing inheritance, which was discussed in the previous chapter, Chapter 8, Inheritance and Polymorphism, along with the second approach. Please refer back to the previous chapter if you need to remind yourself of the two approaches.

However, C++ inheritance seems more complex because C++ supports multiple inheritances that we can't support in our first approach. In this section, we will check the memory layouts of two objects instantiated from two similar classes in C and C++, as demonstrated in example 9.2.

Example 9.2 is about a simple class inheriting from another simple class, both of which have no behavior functions. The C version is as follows:

#include <string.h>

typedef struct {

char c;

char d;

} a_t;

typedef struct {

a_t parent;

char str[5];

} b_t;

int main(int argc, char** argv) {

b_t b;

b.parent.c = 'A';

b.parent.d = 'B';

strcpy(b.str, "1234");

// We need to set a break point at this line to see the memory layout.

return 0;

}

Code Box 9-5 [ExtremeC_examples_chapter9_2.c]: Inheritance example in C

And the C++ version comes within the following code box:

#include <string.h>

class A {

public:

char c;

char d;

};

class B : public A {

public:

char str[5];

};

int main(int argc, char** argv) {

B b;

b.c = 'A';

b.d = 'B';

strcpy(b.str, "1234");

// We need to set a break point at this line to see the memory layout.

return 0;

}

Code Box 9-6 [ExtremeC_examples_chapter9_2.cpp]: Inheritance example in C++

Firstly, we need to compile the C program and use `gdb` to set a breakpoint on the last line of the `main` function. When the execution pauses, we can examine the memory layout as well as the existing values:

$ gcc -g ExtremeC_examples_chapter9_2.c -o ex9_2_c.out

$ gdb ./ex9_2_c.out

...

(gdb) b ExtremeC_examples_chapter9_2.c:19

Breakpoint 1 at 0x69e: file ExtremeC_examples_chapter9_2.c, line 19.

(gdb) r

Starting program: .../ex9_2_c.out

Breakpoint 1, main (argc=1, argv=0x7fffffffe358) at ExtremeC_examples_chapter9_2.c:20

20 return 0;

(gdb) x/7c &b

0x7fffffffe261: 65 'A' 66 'B' 49 '1' 50 '2' 51 '3' 52 '4' 0 '\000'

(qdb) c

[Inferior 1 (process 3759) exited normally]

(qdb) q

$

Shell Box 9-4: Running the C version of example 9.2 in gdb

As you can see, we have printed seven characters, starting from the address of `b` object, which are as follows: `'A'`, `'B'`, `'1'`, `'2'`, `'3'`, `'4'`, `'\0'`. Let's do the same for the C++ code:

$ g++ -g ExtremeC_examples_chapter9_2.cpp -o ex9_2_cpp.out

$ gdb ./ex9_2_cpp.out

...

(gdb) b ExtremeC_examples_chapter9_2.cpp:20

Breakpoint 1 at 0x69b: file ExtremeC_examples_chapter9_2.cpp, line 20.

(gdb) r

Starting program: .../ex9_2_cpp.out

Breakpoint 1, main (argc=1, argv=0x7fffffffe358) at ExtremeC_examples_chapter9_2.cpp:21

21 return 0;

(gdb) x/7c &b

0x7fffffffe251: 65 'A' 66 'B' 49 '1' 50 '2' 51 '3' 52 '4' 0 '\000'

(qdb) c

[Inferior 1 (process 3804) exited normally]

(qdb) q

$

Shell Box 9-5: Running the C++ version of example 9.2 in gdb

As you can see in the preceding two shell boxes, the memory layout and the values stored in the attributes are the same. You shouldn't get confused by having the behavior functions and attributes together in a class in C++; they are going to be treated separately from the class. In C++, the attributes, no matter where you put them in a class, are always collected within the same memory block regarding a specific object, and functions will always be independent of the attributes, just as we saw when looking at implicit encapsulation as part of Chapter 6, OOP and Encapsulation.

The previous example demonstrates single inheritance. So, what about multiple inheritance? In the previous chapter, we explained why our first approach to implementing inheritance in C could not support multiple inheritance. We again demonstrate the reason in the following code box:

typedef struct { ... } a_t;

typedef struct { ... } b_t;

typedef struct {

a_t a;

b_t b;

...

} c_t;

c_t c_obj;

a_t* a_ptr = (a_ptr*)&c_obj;

b_t* b_ptr = (b_ptr*)&c_obj;

c_t* c_ptr = &c_obj;

Code Box 9-7: Demonstration of why multiple inheritance cannot work with our proposed first approach for implementing inheritance in C

In the preceding code box, the `c_t` class desires to inherit both `a_t` and `b_t` classes. After declaring the classes, we create the `c_obj` object. In the following lines of preceding code, we create different pointers.

An important note here is that all of these pointers must be pointing to the same address. The `a_ptr` and `c_ptr` pointers can be used safely with any behavior function from the `a_t` and `c_t` classes, but the `b_ptr` pointer is dangerous to use because it is pointing to the a field in the `c_t` class, which is an `a_t` object. Trying to access the fields inside `b_t` through `b_ptr` results in an undefined behavior.

The following code is the correct version of the preceding code, where all pointers can be used safely:

c_t c_obj;

a_t* a_ptr = (a_ptr*)&c_obj;

b_t* b_ptr = (b_ptr*)(&c_obj + sizeof(a_t));

c_t* c_ptr = &c_obj;

Code Box 9-8: Demonstration of how casts should be updated to point to the correct fields

As you can see on the third line in Code Box 9-8, we have added the size of an `a_t` object to the address of `c_obj`; this eventually results in a pointer pointing to the `b` field in `c_t`. Note that casting in C does not do any magic; it is there to convert types and it doesn't modify the transferring value, the memory address in the preceding case. Eventually, after the assignment, the address from the right-hand side would be copied to the left-hand side.

For now, let's see the same example in C++ with a look at example 9.3. Suppose that we have a `D` class that inherits from three different classes, `A`, `B`, and `C`. The following is the code written for example 9.3:

#include <string.h>

class A {

public:

char a;

char b[4];

};

class B {

public:

char c;

char d;

};

class C {

public:

char e;

char f;

};

class D : public A, public B, public C {

public:

char str[5];

};

int main(int argc, char** argv) {

D d;

d.a = 'A';

strcpy(d.b, "BBB");

d.c = 'C';

d.d = 'D';

d.e = 'E';

d.f = 'F';

strcpy(d.str, "1234");

A* ap = &d;

B* bp = &d;

C* cp = &d;

D* dp = &d;

// We need to set a break point at this line.

return 0;

}

Code Box 9-9 [ExtremeC_examples_chapter9_3.cpp]: Multiple inheritance in C++

Let's compile the example and run it with `gdb`:

$ g++ -g ExtremeC_examples_chapter9_3.cpp -o ex9_3.out

$ gdb ./ex9_3.out

...

(gdb) b ExtremeC_examples_chapter9_3.cpp:40

Breakpoint 1 at 0x100000f78: file ExtremeC_examples_chapter9_3.cpp, line 40.

(gdb) r

Starting program: .../ex9_3.out

Breakpoint 1, main (argc=1, argv=0x7fffffffe358) at ExtremeC_examples_chapter9_3.cpp:41

41 return 0;

(gdb) x/14c &d

0x7fffffffe25a: 65 'A' 66 'B' 66 'B' 66 'B' 0 '\000' 67 'C' 68 'D' 69 'E'

0x7fffffffe262: 70 'F' 49 '1' 50 '2' 51 '3' 52 '4' 0 '\000'

(gdb)

$

Shell Box 9-6: Compiling and running example 9.3 in gdb

As you can see, the attributes are placed adjacent to each other. This shows that multiple objects of the parent classes are being kept inside the same memory layout of the `d` object. What about the `ap`, `bp`, `cp`, and `dp` pointers? As you can see, in C++, we can cast implicitly when assigning a child pointer to a parent pointer (upcasting).

Let's examine the values of these pointers in the current execution:

(gdb) print ap

$1 = (A *) 0x7fffffffe25a

(gdb) print bp

$2 = (B *) 0x7fffffffe25f

(gdb) print cp

$3 = (C *) 0x7fffffffe261

(gdb) print dp

$4 = (D *) 0x7fffffffe25a

(gdb)

Shell Box 9-7: Printing the addresses stored in the pointers as part of exa


## part 3/3

`d` object. What about the `ap`, `bp`, `cp`, and `dp` pointers? As you can see, in C++, we can cast implicitly when assigning a child pointer to a parent pointer (upcasting).

Let's examine the values of these pointers in the current execution:

(gdb) print ap

$1 = (A *) 0x7fffffffe25a

(gdb) print bp

$2 = (B *) 0x7fffffffe25f

(gdb) print cp

$3 = (C *) 0x7fffffffe261

(gdb) print dp

$4 = (D *) 0x7fffffffe25a

(gdb)

Shell Box 9-7: Printing the addresses stored in the pointers as part of example 9.3

The preceding shell box shows that the starting address of the d object, shown as `$4`, is the same as the address being pointed to by ap, shown as `$1`. So, this clearly shows that C++ puts an object of the type A as the first field in the corresponding attribute structure of the D class. Based on the addresses in the pointers and the result we got from the `x` command, an object of the B type and then an object of the C type, are put into the same memory layout belonging to object `d`.

In addition, the preceding addresses show that the cast in C++ is not a passive operation, and it can perform some pointer arithmetic on the transferring address while converting the types. For example, in Code Box 9-9, while assigning the `bp` pointer in the `main` function, five bytes or `sizeof(A)`, are added to the address of `d`. This is done in order to overcome the problem we found in implementing multiple inheritance in C. Now, these pointers can easily be used in all behavior functions without needing to do the arithmetic yourself. As an important note, C casts and C++ casts are different, and you may see different behavior if you assume that C++ casts are as passive as C casts.

Now it's time to look at the similarities between C and C++ in the case of polymorphism.

## Polymorphism

Comparing the underlying techniques for having polymorphism in C and C++ is not an easy task. In the previous chapter, we came up with a simple method for having a polymorphic behavior function in C, but C++ uses a much more sophisticated mechanism to bring about polymorphism, though the basic underlying idea is still the same. If we want to generalize our approach for implementing polymorphism in C, we can do it as the pseudo-code that can be seen in the following code box:

// Typedefing function pointer types

typedef void* (*func_1_t)(void*, ...);

typedef void* (*func_2_t)(void*, ...);

...

typedef void* (*func_n_t)(void*, ...);

// Attribute structure of the parent class

typedef struct {

// Attributes

...

// Pointers to functions

func_1_t func_1;

func_2_t func_2;

...

func_n_t func_t;

} parent_t;

// Default private definitions for the

// virtual behavior functions

void* __default_func_1(void* parent, ...) { // Default definition }

void* __default_func_2(void* parent, ...) { // Default definition }

...

void* __default_func_n(void* parent, ...) { // Default definition }

// Constructor

void parent_ctor(parent_t *parent) {

// Initializing attributes

...

// Setting default definitions for virtual

// behavior functions

parent->func_1 = __default_func_1;

parent->func_2 = __default_func_2;

...

parent->func_n = __default_func_n;

}

// Public and non-virtual behavior functions

void* parent_non_virt_func_1(parent_t* parent, ...) { // Code }

void* parent_non_virt_func_2(parent_t* parent, ...) { // Code }

...

void* parent_non_virt_func_m(parent_t* parent, ...) { // Code }

// Actual public virtual behavior functions

void* parent_func_1(parent_t* parent, ...) {

return parent->func_1(parent, ...);

}

void* parent_func_2(parent_t* parent, ...) {

return parent->func_2(parent, ...);

}

...

void* parent_func_n(parent_t* parent, ...) {

return parent->func_n(parent, ...);

}

Code Box 9-10: Pseudo-code demonstrating how virtual functions can be declared and defined in a C code

As you can see in the preceding pseudo-code, the parent class has to maintain a list of function pointers in its attribute structure. These function pointers (in the parent class) either point to the default definitions for the virtual functions, or they are null. The pseudo-class defined as part of Code Box 9-10 has `m` non-virtual behavior functions and `n` virtual behavior functions.

Note:

Not all behavior functions are polymorphic. Polymorphic behavior functions are called virtual behavior functions or simply virtual functions. In some languages, such as Java, they are called virtual methods.

Non-virtual functions are not polymorphic, and you never get various behaviors by calling them. In other words, a call to a non-virtual function is a simple function call and it just performs the logic inside the definition and doesn't relay the call to another function. However, virtual functions need to redirect the call to a proper function, set by either the parent or the child constructor. If a child class wants to override some of the inherited virtual functions, it should update the virtual function pointers.

Note:

The `void*` type for the output variables can be replaced by any other pointer type. I used a generic pointer to show that anything can be returned from the functions in the pseudo-code.

The following pseudo-code shows how a child class overrides a few of the virtual functions found in Code Box 9-10:

Include everything related to parent class ...

typedef struct {

parent_t parent;

// Child attributes

...

} child_t;

void* __child_func_4(void* parent, ...) { // Overriding definition }

void* __child_func_7(void* parent, ...) { // Overriding definition }

void child_ctor(child_t* child) {

parent_ctor((parent_t*)child);

// Initialize child attributes

...

// Update pointers to functions

child->parent.func_4 = __child_func_4;

child->parent.func_7 = __child_func_7;

}

// Child's behavior functions

...

Code Box 9-11: Pseudo-code in C demonstrating how a child class can override some virtual functions inherited from the parent class

As you can see in Code Box 9-11, the child class needs only to update a few pointers in the parent's attribute structure. C++ takes a similar approach. When you declare a behavior function as virtual (using the `virtual` keyword), C++ creates an array of function pointers, pretty similar to the way we did in Code Box 9-10.

As you can see, we added one function pointer attribute for each virtual function, but C++ has a smarter way of keeping these pointers. It just uses an array called a virtual table or vtable. The virtual table is created when an object is about to be created. It is first populated while calling the constructor of the base class, and then as part of the constructor of the child class, just as we've shown in Code Boxes 9-10 and 9-11.

Since the virtual table is only populated in the constructors, calling a polymorphic method in a constructor, either in the parent or in the child class, should be avoided, as its pointer may have not been updated yet and it might be pointing to an incorrect definition.

As our last discussion regarding the underlying mechanisms used for having various object-oriented concepts in C and C++, we are going to talk about abstraction.

## Abstract classes

Abstraction in C++ is possible using pure virtual functions. In C++ if you define a member function as a virtual function and set it to zero, you have declared a pure virtual function. Look at the following example:

enum class Taste { Sweet, Sour };

// This is an interface

class Eatable {

public:

virtual Taste GetTaste() = 0;

};

Code Box 9-12: The Eatable interface in C++

Inside the class `Eatable`, we have a `GetTaste` virtual function that is set to zero. `GetTaste` is a pure virtual function and makes the whole class abstract. You can no longer create objects from the Eatable type, and C++ doesn't allow this. In addition, Eatable is an interface, because all of its member functions are purely virtual. This function can be overridden in a child class.

The following shows a class that is overriding the `GetTaste` function:

enum class Taste { Sweet, Sour };

// This is an interface

class Eatable {

public:

virtual Taste GetTaste() = 0;

};

class Apple : public Eatable {

public:

Taste GetTaste() override {

return Taste::Sweet;

}

};

Code Box 9-13: Two child classes implementing the Eatable interface

Pure virtual functions are remarkably similar to virtual functions. The addresses to the actual definitions are being kept in the virtual table in the same way as virtual functions, but with one difference. The initial values for the pointers of pure virtual functions are null, unlike the pointers of normal virtual functions, which need to point to a default definition while the construction is in progress.

Unlike a C compiler, which doesn't know anything about abstract types, a C++ compiler is aware of abstract types and generates a compilation error if you try to create an object from an abstract type.

In this section, we took various object-oriented concepts and compared them in C, using the techniques introduced in the past three chapters, and in C++, using the `g++` compiler. We showed that, in most cases, the approaches we employed are in accordance with the techniques that a compiler like `g++` uses.

# Summary

In this chapter, we concluded our exploration of topics in OOP, picking up from abstraction and moving on by showing the similarities between C and C++ regarding object-oriented concepts.

The following topics were discussed as part of this chapter:

- Abstract classes and interfaces were initially discussed. Using them, we can have an interface or a partially abstract class, which could be used to create concrete child classes with polymorphic and different behaviors.
- We then compared the output of the techniques we used in C to bring in some OOP features, with the output of what `g++` produces. This was to demonstrate how similar the results are. We concluded that the techniques that we employed can be very similar in their outcomes.
- We discussed virtual tables in greater depth.
- We showed how pure virtual functions (which is a C++ concept but does have a C counterpart) can be used to declare virtual behaviors that have no default definition.

The next chapter is about Unix and its correspondence to C. It will review the history of Unix and the invention of C. It will also explain the layered architecture of a Unix system.


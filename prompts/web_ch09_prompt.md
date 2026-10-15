# =============================================================================
# INSTRUCTIONS FOR AI AGENTS & CODING ASSISTANTS:
# TARGET OUTPUT DIRECTORY: web_pack/extreme-c/ch09/
# REQUIRED FILES TO CREATE IN DIRECTORY:
#   1. web_pack/extreme-c/ch09/index.html  (Semantic HTML5 shell with all micro-step cards & SVG viewports)
#   2. web_pack/extreme-c/ch09/style.css   (Brilliant design system, $44px touch targets, dark palette)
#   3. web_pack/extreme-c/ch09/app.js      (Reactive state engine, scrubbers, sandboxes, validation)
#   4. web_pack/extreme-c/ch09/server.py   (Self-contained chapter HTTP server with auto-port & browser launch)
#   5. web_pack/extreme-c/ch09/meta.json   (Manifest of chapter concepts, steps, and widgets)
#
# [MANDATORY DIRECTIVES — READ CAREFULLY BEFORE WRITING A SINGLE LINE]
# 1. PUT ALL YOUR MIGHT & GO PLUS ULTRA (NO HALF-ASSING):
#    The learner studies SOLELY from your generated interactive web app — never from the book.
#    Produce a masterwork of pedagogical engineering grounded in cognitive science.
#    Zero placeholders (NO 'TODO', NO '/* implement later */', NO lazy hand-waving).
# 2. STANDALONE ZERO-BUILD ARCHITECTURE:
#    Use vanilla HTML5, CSS3, ES2022+ JavaScript, and responsive inline SVG.
#    Require zero npm packages, zero bundlers, and zero build steps. The app must run
#    immediately by opening `index.html` or executing `python server.py`.
# 3. THE 5-STAGE MICRO-STEPPING MODEL:
#    Decompose every core concept into 3–7 atomized cards following:
#    Stage 1: Intuitive Puzzle (direct manipulation, 0 jargon)
#    Stage 2: Pattern Induction (scrubbers, observe invariants)
#    Stage 3: Productive Failure (boundary case stress-test breaking naive model)
#    Stage 4: Subgoal Naming (functional concept label & spatial bridge)
#    Stage 5: Formal Abbreviation (mathematical formula / C code implementation)
# 4. INTERACTION ARCHETYPES (MINIMUM 2 PER CHAPTER):
#    Incorporate real interactive scrubbers (drag-to-resize geometry/parameters),
#    constrained memory sandboxes (pointers, stack frames, heap leak detectors),
#    algorithmic steppers (synchronized code cursor + memory graph), or bug spotters.
# 5. INLINE VARIABLE COLOR-CODING & COGNITIVE ERGONOMICS:
#    Every prose mention of a variable or pointer MUST share the exact hex color of its
#    counterpart on the SVG canvas. Maximum 50 words per card before an interaction.
# 6. MULTI-TURN / MULTI-STEP GENERATION PROTOCOL:
#    Do not rush or compress the output. Write the files methodically across turns or tool calls:
#    First scaffold directory + meta.json + server.py + style.css, then write index.html, then app.js.
# =============================================================================


# GENERATE_WEB.md — Normative AI Instructions for Web-Native Chapter Studies
# (Implements docs/RESEARCH_WEB_MULTIMODAL_LEARNING.md and docs/SRS.md.
#  Read with prompts/ASK_USER_WEB.md. Excerpts from RESEARCH_WEB_MULTIMODAL_LEARNING.md
#  are appended to this prompt text.)
#
# LANGUAGE POLICY (MUST): this system is language-agnostic. It teaches ANY
# technical book — C, Python, Rust, algorithms, systems, networking, math, hardware.
# Whenever these instructions reference C, pointers, or `gcc`, that is ONE worked
# example of the general contract, never the product scope. Adapt the language,
# toolchain, and Notional Machine to the specific book in front of you.
#
# Every per-mode rule below is grounded in peer-reviewed learning science.
# Rules marked MUST/SHOULD follow RFC 2119. Do not soften them.

You turn ONE pasted book chapter (plain text, code kept verbatim) into ONE
complete, self-contained interactive web study application inside:
`web_pack/<book_slug>/<chapter_id>/`

The learner will study ONLY from your generated web app — never from the book.
Teach, don't summarize. Engage through tactile direct manipulation, not passive reading.

---

### Source Paths You Are Working With (MUST respect)

- `docs/RESEARCH_WEB_MULTIMODAL_LEARNING.md` — the normative pedagogical and technical spec.
- `prompts/ASK_USER_WEB.md` — interrogate the user per that file first.
- `books/<slug>/raw_chapters/<id>.txt` — the pasted chapter source.
- `web_pack/<slug>/<id>/` — TARGET OUTPUT DIRECTORY.
  - `web_pack/<slug>/<id>/index.html` — the interactive application shell & step cards.
  - `web_pack/<slug>/<id>/style.css` — the Brilliant design system & micro-interactions.
  - `web_pack/<slug>/<id>/app.js` — reactive state engine, scrubbers, sandboxes, & validation.
  - `web_pack/<slug>/<id>/server.py` — dedicated chapter HTTP server with auto-port & browser launch.
  - `web_pack/<slug>/<id>/meta.json` — structured manifest of concepts, steps, & widgets.

---

## 0. Output Destination & Protocol (MUST)

### 0.1 Directory Structure & Files
Every chapter MUST be generated as a self-contained web application located at:
`web_pack/<book_slug>/<chapter_id>/`

It MUST contain:
1. **`index.html`**: Complete semantic HTML5 markup containing all micro-step cards, SVG viewports, control handles, and feedback containers. Standalone and functional in modern browsers.
2. **`style.css`**: The Brilliant Dark Theme design system tokens, typography, responsive flex/grid layouts, $44\text{px}$ touch targets, pulse halos, and spring transition animations.
3. **`app.js`**: Pure vanilla JavaScript (ES2022+) reactive state machine controlling card progression (Card 1..N), pointer drag tracking (`setPointerCapture`), dynamic SVG node mutation, KaTeX math string binding, real-time invariant checking, and progressive hint ladders.
4. **`server.py`**: A zero-dependency local Python HTTP server script using `http.server`, `socketserver`, and `webbrowser`. Running `python server.py` automatically binds an open port (default 8080+), opens the default browser, sets proper MIME types (`.wasm`, `.js`, `.mjs`, `.css`, `.svg`, `.json`), and provides an optional `/api/compile` or `/api/run` endpoint for live code validation.
5. **`meta.json`**: Structured metadata file with `book`, `chapter_id`, `title`, `steps` list, and `widgets` manifest.

### 0.2 Agent Execution Protocol
- **Autonomous Agents with File Tools**:
  - Write files directly to `web_pack/<slug>/<id>/index.html`, `style.css`, `app.js`, `server.py`, and `meta.json`.
  - Validate by testing local file syntax and running the chapter server check.
- **Chat-Only Models**:
  - Emit each file inside clear fenced code blocks labeled with their destination paths:
    ```html
    <!-- FILE: web_pack/<slug>/<id>/index.html -->
    ...
    ```
    ```css
    /* FILE: web_pack/<slug>/<id>/style.css */
    ...
    ```
    ```javascript
    // FILE: web_pack/<slug>/<id>/app.js
    ...
    ```
    ```python
    # FILE: web_pack/<slug>/<id>/server.py
    ...
    ```
    ```json
    // FILE: web_pack/<slug>/<id>/meta.json
    ...
    ```

---

## 1. Pedagogical Architecture: The Brilliant.org Standard (MUST)

Every chapter web study MUST be organized into **micro-stepping concept units** (each composed of 3 to 7 atomized interactive cards) following the 5-stage progression:

```
┌────────────────────────────────────────────────────────────────────────┐
│ 5-Stage Micro-Stepping Progression                                     │
├───────┬──────────────────────┬─────────────────────────────────────────┤
│ Stage │ Pedagogical Name     │ User Activity                           │
├───────┼──────────────────────┼─────────────────────────────────────────┤
│ 1     │ Intuitive Puzzle     │ Direct manipulation of sandbox (no math)│
│ 2     │ Pattern Induction    │ Observe invariants across variations    │
│ 3     │ Productive Failure   │ Confront boundary case breaking model   │
│ 4     │ Subgoal Naming       │ Introduce functional concept label      │
│ 5     │ Formal Abbreviation  │ Formalize mathematical / code equation  │
└───────┴──────────────────────┴─────────────────────────────────────────┘
```

### 1.1 The 5 Stages Explained
1. **Stage 1 (Intuitive Puzzle — Zero Jargon)**:
   - Present a physical/visual manipulation task before any syntax or formula is revealed.
   - Example (Special Relativity): Drag a light clock on a train and click "Tick" to observe light traveling diagonally.
   - Example (Pointers): Click memory boxes to route wires from labels to boxes before discussing addresses or asterisks.
2. **Stage 2 (Pattern Induction)**:
   - The user manipulates continuous scrubbers or parameters and observes what remains invariant.
   - The pattern is discovered *empirically* through touch and observation.
3. **Stage 3 (Productive Failure — Kapur 2012)**:
   - The learner encounters an obstacle or boundary condition where their naive mental model breaks (e.g. speed of light limit, pointer aliasing mutation bug, memory leak, off-by-one).
   - This struggle primes working memory to attend to deep structural mechanics.
4. **Stage 4 (Subgoal Naming — Catrambone 1998)**:
   - Introduce the functional subgoal label (e.g. "Sentinel Node", "Dereference", "Stack Frame Base Pointer").
   - Connect the visual geometry/sandbox directly to the functional concept.
5. **Stage 5 (Formal Abbreviation)**:
   - Reveal the formal syntax, C/Rust code snippet, or mathematical formula.
   - The formula or code is introduced **as an abbreviation of the visual experience the learner just lived**, not as an arbitrary rule to memorize.

### 1.2 Cognitive Load Management Rules (Sweller 2011; Mayer 2021)
- **Strict Text Budgeting**: No card may exceed **50 words** before requiring an interaction. Prose is concise, active, and conversational.
- **Inline Variable Color-Coding**: Whenever text refers to a variable, memory address, or state element, wrap it in a `<span class="var-color" style="color: #hex">` that matches the exact color of that element on the SVG canvas.
  Example: *"As <span style="color: #38bdf8">ptr_a</span> is redirected to <span style="color: #f59e0b">node_2</span>, the refcount on <span style="color: #ef4444">node_1</span> drops to zero."*
- **Clamped Degrees of Freedom**: Only ONE variable or handle is interactive at a time; lock all other variables to isolate causal relationships.
- **Progressive Disclosure**: Detailed secondary derivations or deep standard library notes must be placed inside collapsible accordion elements (`<details><summary>Deep Dive: Memory Alignment</summary>...</details>`).

---

## 2. Taxonomy of Visual Aids & Interactive Archetypes (MUST)

Every chapter web study MUST incorporate at least **two** of the following interactive archetypes:

### Archetype 1: Direct Manipulation & Continuous Scrubbers
- **Mechanism**: Draggable SVG coordinate handles (`<circle>` with `setPointerCapture`), continuous range sliders, or scrubbable inline numbers.
- **Visuals**: Updates SVG geometry at 60 FPS. Shows tangent lines, dynamic bounds, real-time rates of change.
- **Cognitive Goal**: Replaces abstract algebraic evaluation with visceral physical intuition.

### Archetype 2: Constrained Memory & Structural Sandboxes
- **Mechanism**: Fixed coordinate or slot-based workspace where learners manipulate nodes, route pointers, allocate stack/heap blocks, or rewire logic circuits.
- **Visuals**: Distinct Stack pane (frames, local variables, pointers) and Heap pane (dynamically allocated structs, byte addresses).
- **Diagnostics**: Real-time automated leak detection (e.g. highlighting unreferenced blocks in `#ef4444` dashed red with warning badges: `🚨 UNREFERENCED (LEAKED)`).

### Archetype 3: Algorithmic State Steppers & Notional Machine Tracers
- **Mechanism**: A code snippet with an execution cursor (`line-highlight`) synchronized with an interactive memory visualizer and dynamic variables table.
- **Controls**: "Step Forward", "Step Backward", "Reset", or scrubber bar.
- **Cognitive Goal**: Demystifies the Notional Machine (Sorva 2013). Shows how each line of code mutates CPU registers, stack frames, and heap addresses.

### Archetype 4: Synchronized Multi-Representations
- **Mechanism**: Three co-linked panes updating simultaneously in real time:
  - **Pane A**: Interactive SVG Geometry / Memory Diagram.
  - **Pane B**: Synchronized Algebraic Equation / KaTeX Card.
  - **Pane C**: Evaluated Numeric / Assembly / C-Code State.
- **Cognitive Goal**: Eliminates the "representation translation deficit."

### Archetype 5: Interactive Bug Spotters & Diagnostic Dissectors
- **Mechanism**: Present flawed systems code or broken memory layouts. The user probes memory cells or toggles compiler flags (`-Wall`, `-fsanitize=address`) to expose undefined behavior (UB), use-after-free, or buffer overflows.
- **Diagnostics**: Render authentic compiler/sanitizer diagnostic outputs with clickable line bridges.

### Archetype 6: Topological Morphing & Spatial Transformations
- **Mechanism**: Animated SVG path transitions showing equivalence (e.g., transforming a contiguous array into an indexed hash table, or unrolling a recursive call tree into an iterative stack).

---

## 3. Visual Ergonomics & Brilliant Design System (MUST)

Every web study MUST adhere to the Brilliant UI/UX design tokens:

### 3.1 Color Palette
```css
:root {
  /* Canvas & Surfaces */
  --bg-canvas: #0f172a;        /* Deep slate background */
  --bg-card: #1e293b;          /* Card surface */
  --bg-subtle: #334155;        /* Borders & subtle dividers */
  
  /* Text */
  --text-primary: #f8fafc;     /* Crisp white text */
  --text-muted: #94a3b8;       /* Muted secondary labels */
  --text-dim: #64748b;         /* Footnotes & metadata */

  /* Interactive Elements */
  --interactive-blue: #38bdf8; /* Draggable handles & primary accents */
  --interactive-active: #0284c7; /* Active dragging state */
  
  /* Semantic & Validation */
  --status-success: #22c55e;   /* Emerald green (Correct / Valid) */
  --status-danger: #ef4444;    /* Coral red (Leak / Bug / Error) */
  --status-warning: #f59e0b;   /* Amber (Warning / Boundary) */
  
  /* Co-Linked Variable Tokens */
  --var-blue: #38bdf8;
  --var-amber: #f59e0b;
  --var-emerald: #10b981;
  --var-purple: #c084fc;
}
```

### 3.2 Touch & Pointer Ergonomics
- **44px Hit Targets**: Every draggable SVG handle or clickable button MUST have an invisible hit-target area of at least **$44\text{px} \times 44\text{px}$** (`<circle r="22" fill="transparent"/>`), even if the visible handle is only $8\text{px}$–$12\text{px}$.
- **Pointer Capture**: Draggable handles MUST attach `onpointerdown`, `onpointermove`, and `onpointerup` listeners using `e.target.setPointerCapture(e.pointerId)` to prevent dragging from dropping when the cursor leaves the element or SVG boundaries.
- **No Text Selection During Drag**: Apply `user-select: none; touch-action: none;` on draggable canvases.

### 3.3 Physics & Feedback
- **Tactile 0ms Feedback**: Canvas transforms and values update synchronously during pointer movement.
- **Delayed Evaluative Feedback**: When clicking "Check" or "Submit", provide smooth spring transitions (`transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);`), followed by in-place explanation expansion.

---

## 4. Standalone Zero-Build Architecture (MUST)

Every generated chapter MUST be self-contained and run directly in standard browsers with **zero build step**:
- Use modern, standards-compliant vanilla HTML5, CSS3, and JavaScript (ES Modules).
- KaTeX (if formulas are used) should be linked via high-speed CDN:
  `<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">`
  `<script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>`
- No npm install, no Webpack, no Vite build requirement. A user can open `index.html` directly or launch `python server.py`.

---

## 5. Chapter Server Specification (`server.py`) (MUST)

Every chapter directory MUST contain a runnable `server.py` file with the following capabilities:
1. **Zero External Dependencies**: Uses only standard library modules (`http.server`, `socketserver`, `webbrowser`, `urllib`, `subprocess`, `argparse`, `os`, `sys`).
2. **Dynamic Port Discovery**: Defaults to port 8080 (or custom CLI argument `--port`), automatically finding the next available port if 8080 is occupied.
3. **MIME Type Accuracy**: Explicitly registers `.js`, `.mjs`, `.css`, `.svg`, `.json`, and `.wasm` MIME types so modern browser features work flawlessly.
4. **Auto-Browser Launch**: Automatically opens the system's default browser to `http://localhost:<port>/` unless `--no-browser` is passed.
5. **Optional Code Compilation Hook**: If the chapter involves systems code (C, C++, etc.), the server can handle `POST /api/compile` or `POST /api/run` to execute host compiler checks with safe timeouts (2.0s) and return compiler stderr/stdout as JSON.

---

## 6. The "Plus Ultra" Directives (Never Half-Ass) (MUST)

- **The Masterwork Standard**: You are engineering a premier, world-class interactive educational experience. The user will study the subject through this application. Make it visually stunning, cognitively transformative, and technically flawless.
- **Zero Placeholders**: NEVER output `<!-- TODO: add other steps -->`, `// implement later`, `/* rest of code */`, or filler text. Every card, every state variable, every SVG node, and every validation rule must be completely written and operational.
- **Depth Over Brevity**: Author full, comprehensive chapters. A typical chapter will contain 4 to 8 micro-step units covering every core idea unit from the source text.
- **Multi-Turn Generation Protocol**:
  If generating in a chat or multi-step agent environment:
  - Turn 1: Scaffold directory, `meta.json`, `server.py`, and `style.css`.
  - Turn 2: Author `index.html` with full micro-step cards.
  - Turn 3: Author `app.js` with all reactive state, drag handlers, and validation rules.
  - Turn 4: Verify and test.
  Take as many turns as needed to deliver uncompromising perfection.


---

# ASK_USER_WEB.md — interrogation template for Web-Native Chapter Studies
# The AI MUST ask these questions BEFORE generating HTML/Web study packs.
# MUST NOT emit final chapter files until the user answers or says `use defaults`.
#
# MANDATORY DIRECTIVES:
# 1. The learner studies SOLELY from the generated interactive web chapter — never from the book.
# 2. Never refer to exercises or problem numbers in the book; make every scenario self-contained.
# 3. Put all your might and go Plus Ultra — zero half-assing, no placeholders.
# 4. Standalone zero-build architecture: pure HTML5 + SVG + CSS + JS + dedicated `server.py`.

Ask (compact, one message, numbered):

1. **Target Audience & Prior Knowledge**:
   - Novice / Comfortable-in-language / Experienced systems engineer?
   - Default: *Comfortable-in-language* (requires deep Notional Machine breakdowns without trivial hand-waving).

2. **Interactive Archetypes to Prioritize** (select 1–3 to emphasize):
   - A. **Direct Manipulation Scrubbers**: Drag-to-resize geometry, angle sweepers, continuous mathematical sliders.
   - B. **Constrained Memory Sandboxes**: Drag-and-drop pointer connections, stack/heap frame allocators, leak detectors.
   - C. **Algorithmic State Steppers**: Code execution cursor synchronized with memory tables and pointer transitions.
   - D. **Interactive Bug Spotters**: Hands-on inspection of compiler diagnostics, sanitizer warnings, and memory leaks.
   - Default: *Balanced multi-archetype progression* matching the chapter's conceptual domain.

3. **Execution & Simulation Fidelity**:
   - Pure client-side simulation (self-contained reactive state machine in JS/SVG; zero install).
   - Local runner integration via chapter `server.py` (live compilation/execution through host toolchain like `gcc`/`python3`).
   - Default: *Pure client-side simulation with optional server.py runner hook*.

4. **Curriculum Scope & Prioritized Sections**:
   - Which specific sections or mental models of this chapter matter most?
   - Any platform-specific quirks (e.g. Windows/macOS tangents) to skip?
   - Default: *Cover all core conceptual units; skip platform-specific tangents*.

5. **Visual Theme & Typography**:
   - Brilliant Dark Mode (`#0f172a` canvas, `#38bdf8` sky blue handles, `#22c55e` emerald success) or High-Contrast Light Mode?
   - Default: *Brilliant Dark Mode*.

6. **Interleaved Prior Concepts**:
   - How many review/contrasting checks from prior chapters to weave in (0, 2, or 4)?
   - Default: *2 contrasting review challenges*.

Record the answers as `web_gen_notes.md` inside `web_pack/<book>/<chapter>/` (RECOMMENDED) for reproducibility. Then emit the web study pack per `GENERATE_WEB.md`.


---

# NORMATIVE PEDAGOGICAL & TECHNICAL RESEARCH EXCERPTS (from docs/RESEARCH_WEB_MULTIMODAL_LEARNING.md):

## 2. Empirical Cognitive Research & Learning Retention Data

```
┌────────────────────────────────────────────────────────────────────────┐
│ Empirical Effect Sizes in Multimodal & Interactive Learning            │
├───────────────────────────────┬──────────────┬─────────────────────────┤
│ Phenomenon / Principle        │ Effect Size  │ Primary Citation        │
├───────────────────────────────┼──────────────┼─────────────────────────┤
│ Multimedia Principle          │ d = 1.39     │ Mayer (2001, 2021)      │
│ Spatial Contiguity Principle  │ d = 1.09     │ Mayer & Moreno (2003)   │
│ Split-Attention Elimination   │ d = 0.72–0.85│ Ginns (2006) Meta-Anal. │
│ Active Engagement (AV)        │ d = 0.60–0.90│ Hundhausen et al.(2002) │
│ Modality Principle            │ d = 1.02     │ Mayer (2021)            │
│ Signaling / Visual Cueing     │ d = 0.52     │ Schneider et al. (2018) │
│ Visual Program Tracing (PV)   │ d = 0.65     │ Sorva (2013); Guo(2013) │
└───────────────────────────────┴──────────────┴─────────────────────────┘
*Cohen's d: 0.2 = Small, 0.5 = Medium, 0.8+ = Large, 1.0+ = Transformative
```

### 2.1 Dual Coding Theory & Mayer’s Cognitive Theory of Multimedia Learning (CTML)
Human working memory is split into two distinct, capacity-constrained processing subsystems (Paivio, 1986; Baddeley, 1992):
- The **Auditory/Verbal Channel**: Processes spoken words, written text, code tokens, and symbolic syntax.
- The **Visual/Pictorial Channel**: Processes spatial orientations, geometric shapes, colors, spatial layouts, and motion vectors.

```
                   ┌───────────────────────────────────────────────┐
                   │ Cognitive Theory of Multimedia Learning (CTML)│
                   └───────────────────────────────────────────────┘

  MULTIMEDIA                     WORKING MEMORY                      LONG-TERM MEMORY
  PRESENTATION   SENSORY MEMORY  (Limited: ~3-4 elements)
 ┌────────────┐   ┌─────────┐     ┌──────────────────────┐            ┌──────────────┐
 │ Words/Code │──▶│  Ears/  │────▶│ Verbal Mental Model  │──┐         │              │
 │            │   │  Eyes   │     │ (Syntactic semantics)│  │         │              │
 └────────────┘   └─────────┘     └──────────────────────┘  │         │ Integrated   │
                                                            ├──Integr─▶  Cognitive    │
 ┌────────────┐   ┌─────────┐     ┌──────────────────────┐  │  -ation │  Schema      │
 │ SVG Memory │──▶│  Eyes   │────▶│ Pictorial Model      │──┘         │              │
 │ Graph/Viz  │   │         │     │ (Spatial heap/stack) │            │              │
 └────────────┘   └─────────┘     └──────────────────────┘            └──────────────┘
```

- **The Multimedia Principle ($d = 1.39$)**: Mayer's experimental research proves that presenting text together with visual representations produces an average $89\%$ gain in problem-solving transfer over text alone. Terminal text overloads the verbal channel while leaving the spatial channel completely dormant.
- **The Spatial Contiguity Principle ($d = 1.09$)**: Physical proximity between corresponding labels, math variables, and visual elements drastically reduces split-attention cognitive waste (Ginns, 2006).

### 2.2 The Notional Machine & Program Visualization (Sorva, 2013; Guo, 2013)
The primary obstacle in learning programming is the **Notional Machine** (du Boulay, 1986)—the hidden reality of stack frames, memory addresses, pointer dereferences, and heap structures. In Philip Guo’s *Online Python Tutor* (SIGCSE 2013), evaluated across over 10 million students, rendering dynamic pointer graphs and memory state tables enabled learners to identify pointer bugs and recursion failures **over twice as fast** as terminal printouts or standard debuggers.

### 2.3 The Engagement Taxonomy (Hundhausen, 2002; Naps et al., 2002)
Hundhausen and Naps showed that passive visual observation has minimal educational effect ($d \approx 0.15$). Only active engagement—where learners **change parameters** ($d \approx 0.74$) or **construct data structures directly** ($d \approx 0.92$)—produces dramatic retention gains.

---

## 3. Brilliant.org Deep Teardown: Phase 1 — Pedagogical & Cognitive Architecture

Brilliant.org is not an ebook with quizzes attached; it is an **active cognitive simulator**. Every lesson is engineered using strict instructional design and cognitive science frameworks.

```
┌────────────────────────────────────────────────────────────────────────┐
│ Brilliant.org 5-Stage Micro-Stepping Progression                       │
├───────┬──────────────────────┬─────────────────────────────────────────┤
│ Stage │ Pedagogical Name     │ User Activity                           │
├───────┼──────────────────────┼─────────────────────────────────────────┤
│ 1     │ Intuitive Puzzle     │ Direct manipulation of sandbox (no math)│
│ 2     │ Pattern Induction    │ Observe invariants across variations    │
│ 3     │ Productive Failure   │ Confront boundary case breaking model   │
│ 4     │ Subgoal Naming       │ Introduce functional concept label      │
│ 5     │ Formal Abbreviation  │ Formalize mathematical / code equation  │
└───────┴──────────────────────┴─────────────────────────────────────────┘
```

### 3.1 Concept Scaffolding & Micro-Stepping
Brilliant avoids the "Cognitive Cliff" by never presenting a complete theorem or algorithm all at once. Every major concept is decomposed into **3 to 7 atomized interactive cards**:
1. **Screen 1 (Intuitive Puzzle — No Jargon)**: The user is presented with a physical manipulation task. *Example:* In Special Relativity, instead of presenting Lorentz transformations ($\gamma = \frac{1}{\sqrt{1 - v^2/c^2}}$), the user drags a light clock on a train and clicks "Tick" to watch light travel along a diagonal path.
2. **Screen 2 (Pattern Induction)**: The user manipulates the velocity slider. They observe that as speed increases, the diagonal path lengthens. The user discovers the pattern *empirically* before any formula is mentioned.
3. **Screen 3 (Boundary & Edge-Case Stress Testing)**: The user slides the velocity to $c$ (the speed of light). The path becomes infinite. The interface naturally blocks exceeding $c$.
4. **Screen 4 (Subgoal Labeling & Geometric Bridge)**: The interface reveals a right-angled triangle formed by the vertical path ($c \Delta t_0$), horizontal distance ($v \Delta t$), and diagonal path ($c \Delta t$).
5. **Screen 5 (Formal Abbreviation)**: The Pythagorean theorem is applied to derive the equation. **The equation is introduced not as a rule to memorize, but as an abbreviation of the visual experience the user just lived.**

### 3.2 Productive Failure & Active Recall (Kapur, 2012)
Brilliant systematically places questions and manipulation tasks **before** explanations.
- *Mechanism:* Traditional education presents theory $\rightarrow$ worked example $\rightarrow$ exercise. Brilliant presents **challenge puzzle $\rightarrow$ struggle/failure $\rightarrow$ target concept revelation**.
- *Cognitive Impact:* Manu Kapur’s (2012) research on "Productive Failure" proves that attempting to solve a problem prior to instruction activates relevant prior knowledge and primes working memory to attend to deep structural features rather than surface syntax.

### 3.3 Immediate Tactile Feedback vs. Delayed Evaluative Feedback
Brilliant strictly bifurcates feedback into two distinct loops:
1. **Continuous Tactile Feedback (0ms latency)**:
   - When the user drags a vertex, rotates a gear, or routes a logic wire, the SVG canvas updates at 60 FPS.
   - Spring physics give elements mass and tactile resistance.
   - Audio clicks and subtle haptic vibrations (on mobile) provide confirmation of state transitions.
2. **Delayed Evaluative Feedback (On "Submit")**:
   - The user decides when their hypothesis is ready.
   - Clicking "Check" locks inputs and initiates a multi-stage validation animation (e.g. green pulse for success, subtle shake for error).
   - **Explanations are dynamically revealed in place** directly below the widget, maintaining spatial contiguity without opening disruptive modal dialogues.

### 3.4 Cognitive Load Management & Visual Ergonomics
Brilliant applies Sweller’s Cognitive Load Theory through four strict visual conventions:
1. **Strict Text Budgeting**: No card ever exceeds 2 to 3 sentences before requiring an interaction. Prose is limited to $\le 50$ words per card.
2. **Inline Variable Color-Coding**: When text refers to a variable, that variable is rendered in the exact hex color of the visual element on the canvas:
   $$\text{"As the radius } \textcolor{#3b82f6}{r} \text{ increases, the angular velocity } \textcolor{#eab308}{\omega} \text{ drops."}$$
   The circle on the canvas has a `#3b82f6` blue radius line and a `#eab308` yellow rotation arc. This completely eliminates visual search time ($d = 0.52$).
3. **Progressive Disclosure**: Detailed mathematical proofs or secondary derivations are hidden behind accordion toggles labeled *"Show derivation"* or unlocked only after solving the primary interaction.
4. **Constrained Degrees of Freedom**: If a problem teaches the effect of changing variable $A$, variables $B$ and $C$ are locked or automated so the learner can only isolate and observe the single independent variable.

---

## 4. Phase 2: Exhaustive Taxonomy of Visual Aids & Interactive Mechanics

```
                   ┌────────────────────────────────────────────────────────┐
                   │ Taxonomy of Brilliant.org Interactive Archetypes       │
                   └────────────────────────────────────────────────────────┘
                                            │
        ┌───────────────────┬───────────────┴───────────────┬────────────────────┐
        ▼                   ▼                               ▼                    ▼
┌──────────────┐    ┌──────────────┐                ┌──────────────┐     ┌──────────────┐
│ Direct       │    │ Constrained  │                │ Algorithmic  │     │ Synchronized │
│ Manipulation │    │ Sandboxes    │                │ State Machine│     │ Multi-Rep    │
│ & Scrubbers  │    │ (Circuits,   │                │ (Execution   │     │ (Geo ↔ Chart │
│ (Movable pts)│    │  Logic, Maze)│                │  Pointers)   │     │  ↔ Formula)  │
└──────────────┘    └──────────────┘                └──────────────┘     └──────────────┘
```

### 4.1 Archetype 1: Direct Manipulation & Continuous Scrubbers
- **UX Mechanic**: Sliders, scrubbable numbers in text, and draggable geometric handles (`<circle>` nodes with `setPointerCapture`).
- **Cognitive Purpose**: Replaces mental mathematical evaluation with tactile perceptual exploration. Learners observe continuous rate-of-change and derivatives organically.
- **Example**: Dragging the focal point of an elliptical mirror; light rays continuously reflect off the perimeter and converge at the second focus.

### 4.2 Archetype 2: Constrained Sandboxes
- **UX Mechanic**: Fixed-grid or slot-based micro-environments (e.g., balance scales comparing unknown weights; digital logic breadboards with AND/OR gates; optical benches with lenses).
- **Cognitive Purpose**: Engages Level 5 (Constructing) of the Naps Engagement Taxonomy. The user tests hypotheses against a rigid rule-engine that guarantees zero arbitrary failures.
- **Example**: Balance scales with bags of gold and discrete 1kg weights to teach algebraic equations ($2x + 1 = 7$) before introducing algebraic manipulation rules.

### 4.3 Archetype 3: Algorithmic & State Machine Visualizers
- **UX Mechanic**: Interactive execution graphs for data structures and algorithms. Step-through playback pointers, draggable array elements for sorting passes, tree node rotators for AVL rebalancing.
- **Cognitive Purpose**: Unveils the Notional Machine. Transforms temporal, sequential algorithm steps into persistent spatial arrangements.
- **Example**: Breadth-First Search (BFS) vs. Depth-First Search (DFS) maze solver where the user clicks a step button to watch frontier queue/stack frames expand in synchronized memory lists.

### 4.4 Archetype 4: Synchronized Multi-Representations (Co-Linked Views)
- **UX Mechanic**: Simultaneous updating of geometric, Cartesian, and algebraic representations. Dragging a point $(x, y)$ on a unit circle dynamically updates the triangle's adjacent side, draws the point on the $\sin(\theta)$ wave curve, and live-evaluates $\sin(45^\circ) = 0.707$ in the formula card.
- **Cognitive Purpose**: Overcomes the "representation translation deficit." Novices struggle to connect symbolic equations with geometric meaning; linking them in real time binds the neural pathways between both representations.

### 4.5 Archetype 5: Spatial & 3D Projections
- **UX Mechanic**: Rotatable WebGL/Three.js 3D models with orbit controls, customizable slicing planes, and vector field streamlines.
- **Cognitive Purpose**: Enables spatial perception in multivariable calculus, magnetic fields, and structural mechanics where 2D planar projections induce spatial distortion.
- **Example**: Cutting a 3D double cone with an adjustable slicing plane to morph circles into ellipses, parabolas, and hyperbolas.

### 4.6 Archetype 6: Micro-Animations & Topological Metaphors
- **UX Mechanic**: Semi-interactive SVG/Lottie state morphing.
- **Cognitive Purpose**: Anchor abstract invariants to physical conservation laws (e.g. conservation of area, volume, mass, or energy).
- **Example**: Proving the area of a circle by unwrapping concentric rings into an isosceles triangle of base $2\pi r$ and height $r$, deriving $\frac{1}{2} (2\pi r)(r) = \pi r^2$.

---

## 5. Phase 3: Technical Reverse-Engineering & Implementation Stack

```
┌────────────────────────────────────────────────────────────────────────┐
│ The Modern Interactive Web-Learning Technology Stack                   │
├─────────────────────┬────────────────────────────────┬─────────────────┤
│ Layer               │ Production Technology          │ Role            │
├─────────────────────┼────────────────────────────────┼─────────────────┤
│ Application Shell   │ React 19 / Next.js / Svelte 5  │ Layout, UI state│
│ 2D Geometry & Math  │ Mafs / JSXGraph / D3.js        │ Interactive SVG │
│ Physics & Dynamics  │ Matter.js / Rapier2D (Wasm)    │ Rigid bodies    │
│ 3D Spatial Canvas   │ Three.js / MathBox             │ WebGL 3D math   │
│ Animation & Drag    │ Framer Motion / GSAP MorphSVG  │ Spring physics  │
│ State Machine       │ XState v5                      │ Lesson gating   │
│ Formula Rendering   │ KaTeX + Dynamic CSS bindings   │ LaTeX rendering │
│ Systems Runtime     │ clang.wasm / Pyodide / WASI    │ Client compiler │
└─────────────────────┴────────────────────────────────┴─────────────────┘
```

### 5.1 Rendering Technology Matrix: When to Use What
- **SVG (DOM-based)**: Use for $\le 200$ nodes, coordinate graphs, geometric shapes, pointer arrows, and node graphs. **Critical advantage**: Native DOM events (`onPointerDown`), crisp Retina scaling, and native accessibility.
- **HTML5 Canvas 2D**: Use for high-frequency physics simulations, $\ge 500$ moving particles, cellular automata, or continuous pixel manipulation where React/DOM reconciliation causes frame drops.
- **WebGL (Three.js / MathBox)**: Use exclusively for 3D vector calculus, electromagnetic flux surfaces, and rotational mechanics.
- **KaTeX vs. MathJax**: **KaTeX** is preferred over MathJax for interactive applications because it renders synchronously to raw HTML/CSS strings at $10\times$ the speed of MathJax, allowing dynamic formula updates at 60 FPS without layout thrashing.

### 5.2 Data-Driven Lesson Architecture (JSON / TypeScript Schema)

To build a scalable platform, lesson content must be decoupled from the rendering components. Below is the normative schema for an interactive lesson card:

```typescript
// LessonCardSchema.ts - Standardized Schema for Interactive Lesson Modules

export type VisualLayerType = 
  | 'geometric_scrubber'
  | 'algorithm_sandbox'
  | 'physics_simulation'
  | 'logic_circuit'
  | 'memory_graph';

export interface InlineColorBinding {
  variable: string;     // e.g. "theta", "p_ptr", "fuel"
  color: string;        // e.g. "#3b82f6"
  label: string;        // e.g. "Angle of Rotation"
}

export interface InteractiveStateVar {
  id: string;
  type: 'number' | 'boolean' | 'point' | 'array';
  initial: any;
  min?: number;
  max?: number;
  step?: number;
  snap_points?: number[];
}

export interface ValidationRule {
  condition: string;    // e.g. "abs(angle - 45) < 0.5 && length > 2.0"
  feedback_message: string;
  is_correct: boolean;
}

export interface InteractiveLessonCard {
  id: string;
  chapter_id: string;
  step_index: number;
  title: string;
  
  // Cognitive Load Controlled Content
  prompt_markdown: string;              // Max 50 words
  color_bindings: InlineColorBinding[]; // For automatic inline text highlighting
  
  // State Machine & Interaction Definition
  state_schema: Record<string, InteractiveStateVar>;
  visual_layer: {
    type: VisualLayerType;
    view_box: [number, number, number, number]; // [minX, minY, width, height]
    config: Record<string, any>;
  };
  
  // Evaluative Feedback Loops
  validation: {
    rules: ValidationRule[];
    explanation_markdown: string;       // Revealed post-check
    hint_ladder: string[];              // Progressive hints
  };
}
```

---

## 6. Phase 4: The Builder’s Blueprint & Production-Ready Prototypes

### 6.1 The Brilliant Design System Specification

#### 1. Color Semantics
- **Canvas Base**: `#0f172a` (Dark mode) / `#ffffff` (Light mode)
- **Grid Lines / Subtle Boundaries**: `#334155` (Dark) / `#f1f5f9` (Light)
- **Static Content**: `#94a3b8` (Muted text), `#f8fafc` (Primary text)
- **Interactive Control Elements (Draggable Handles)**:
  - Default: `#38bdf8` (Vibrant Sky Blue)
  - Active Dragging: `#0284c7` (Deep Blue) with 4px pulse halo
- **Evaluation States**:
  - Success: `#22c55e` (Emerald Green)
  - Incorrect / Boundary Blocked: `#ef4444` (Coral Red)
  - Dynamic Variable A: `#3b82f6` (Blue)
  - Dynamic Variable B: `#f59e0b` (Amber)
  - Dynamic Variable C: `#a855f7` (Purple)

#### 2. Touch & Pointer Ergonomics
- **Minimum Hit Target**: Invisible touch target around handles must be **$44\text{px} \times 44\text{px}$** (`<circle r="22" opacity="0"/>`), even if the visual handle is only $10\text{px}$ in diameter.
- **Pointer Capture**: Must invoke `e.target.setPointerCapture(e.pointerId)` on `pointerdown` to ensure smooth dragging even if the mouse/finger slips outside the SVG boundaries.

#### 3. Spring Physics & Easing
- **Drag Transitions**: Linear / Instantaneous for direct manipulation.
- **Snapping / Return to Invariant**: Spring curve with `stiffness: 300, damping: 25` (zero oscillations, settles in $<200\text{ms}$).

---

### 6.2 Production Prototype 1: Synchronized Geometric-to-Equation Scrubber

Below is a self-contained, dependency-free React/SVG component demonstrating **Archetype 4 (Synchronized Multi-Representation)**. A right triangle allows dragging vertex $A$. Dragging live-updates the triangle, the geometric square visualizer, and the color-bound Pythagorean equation simultaneously:

```tsx
// SynchronizedPythagorasScrubber.tsx
import React, { useState, useRef, useCallback } from 'react';

export const SynchronizedPythagorasScrubber: React.FC = () => {
  // State: Triangle base (a) and height (b)
  const [a, setA] = useState<number>(4);
  const [b, setB] = useState<number>(3);
  const svgRef = useRef<SVGSVGElement>(null);

  // Computed Values
  const c = Math.sqrt(a * a + b * b);
  const scale = 28; // Pixels per unit
  const originX = 140;
  const originY = 220;

  // Dragging vertex B (height controller)
  const handlePointerMoveB = useCallback((e: React.PointerEvent) => {
    if (!svgRef.current || e.buttons !== 1) return;
    const rect = svgRef.current.getBoundingClientRect();
    const rawY = (originY - (e.clientY - rect.top)) / scale;
    const clampedY = Math.max(1, Math.min(6, Math.round(rawY * 10) / 10));
    setB(clampedY);
  }, [scale]);

  // Dragging vertex C (base controller)
  const handlePointerMoveC = useCallback((e: React.PointerEvent) => {
    if (!svgRef.current || e.buttons !== 1) return;
    const rect = svgRef.current.getBoundingClientRect();
    const rawX = (e.clientX - rect.left - originX) / scale;
    const clampedX = Math.max(1, Math.min(7, Math.round(rawX * 10) / 10));
    setA(clampedX);
  }, [scale]);

  return (
    <div style={{
      fontFamily: 'system-ui, -apple-system, sans-serif',
      background: '#0f172a',
      color: '#f8fafc',
      padding: '24px',
      borderRadius: '16px',
      maxWidth: '520px',
      boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.5)'
    }}>
      {/* Micro-Stepping Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
        <span style={{ fontSize: '12px', fontWeight: 700, color: '#38bdf8', letterSpacing: '1px' }}>
          STEP 2 OF 4: EXPLORE INVARIANTS
        </span>
        <span style={{ fontSize: '12px', color: '#94a3b8' }}>Pythagorean Theorem</span>
      </div>

      {/* Cognitive-Load Controlled Prompt with Inline Color Highlights */}
      <h3 style={{ fontSize: '18px', fontWeight: 600, margin: '0 0 16px 0', lineHeight: 1.4 }}>
        Drag the handles to alter base <span style={{ color: '#3b82f6', fontWeight: 700 }}>a</span> and height <span style={{ color: '#f59e0b', fontWeight: 700 }}>b</span>. Notice how hypotenuse <span style={{ color: '#10b981', fontWeight: 700 }}>c</span> balances the squares:
      </h3>

      {/* Interactive SVG Canvas */}
      <svg
        ref={svgRef}
        viewBox="0 0 460 280"
        style={{ width: '100%', height: 'auto', background: '#1e293b', borderRadius: '12px', touchAction: 'none' }}
      >
        {/* Coordinate Grid Lines */}
        <defs>
          <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
            <path d="M 28 0 L 0 0 0 28" fill="none" stroke="#334155" strokeWidth="0.5" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />

        {/* Triangle Geometry */}
        <polygon
          points={`
            ${originX},${originY} 
            ${originX + a * scale},${originY} 
            ${originX},${originY - b * scale}
          `}
          fill="rgba(56, 189, 248, 0.15)"
          stroke="#38bdf8"
          strokeWidth="2"
        />

        {/* Base Side (a) Highlight */}
        <line
          x1={originX} y1={originY}
          x2={originX + a * scale} y2={originY}
          stroke="#3b82f6" strokeWidth="4"
        />

        {/* Height Side (b) Highlight */}
        <line
          x1={originX} y1={originY}
          x2={originX} y2={originY - b * scale}
          stroke="#f59e0b" strokeWidth="4"
        />

        {/* Hypotenuse Side (c) Highlight */}
        <line
          x1={originX + a * scale} y1={originY}
          x2={originX} y2={originY - b * scale}
          stroke="#10b981" strokeWidth="4" strokeDasharray="6 3"
        />

        {/* Handle C (Controls Base a) */}
        <g 
          transform={`translate(${originX + a * scale}, ${originY})`} 
          style={{ cursor: 'ew-resize' }}
          onPointerDown={(e) => e.currentTarget.setPointerCapture(e.pointerId)}
          onPointerMove={handlePointerMoveC}
        >
          <circle r="20" fill="transparent" /> {/* 44px hit-target */}
          <circle r="7" fill="#3b82f6" stroke="#ffffff" strokeWidth="2" />
          <text y="24" textAnchor="middle" fill="#3b82f6" fontSize="12" fontWeight="bold">a = {a}</text>
        </g>

        {/* Handle B (Controls Height b) */}
        <g 
          transform={`translate(${originX}, ${originY - b * scale})`} 
          style={{ cursor: 'ns-resize' }}
          onPointerDown={(e) => e.currentTarget.setPointerCapture(e.pointerId)}
          onPointerMove={handlePointerMoveB}
        >
          <circle r="20" fill="transparent" /> {/* 44px hit-target */}
          <circle r="7" fill="#f59e0b" stroke="#ffffff" strokeWidth="2" />
          <text x="-16" y="4" textAnchor="end" fill="#f59e0b" fontSize="12" fontWeight="bold">b = {b}</text>
        </g>

        {/* Hypotenuse Label */}
        <text 
          x={originX + (a * scale) / 2 + 10} 
          y={originY - (b * scale) / 2 - 10} 
          fill="#10b981" 
          fontSize="13" 
          fontWeight="bold"
        >
          c = {c.toFixed(2)}
        </text>
      </svg>

      {/* Synchronized Live Algebraic Equation Card */}
      <div style={{
        marginTop: '16px',
        padding: '14px 18px',
        background: '#1e293b',
        borderRadius: '10px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        border: '1px solid #334155'
      }}>
        <div style={{ fontSize: '15px', letterSpacing: '0.5px' }}>
          <span style={{ color: '#3b82f6', fontWeight: 700 }}>a²</span> +{' '}
          <span style={{ color: '#f59e0b', fontWeight: 700 }}>b²</span> ={' '}
          <span style={{ color: '#10b981', fontWeight: 700 }}>c²</span>
        </div>
        <div style={{ fontSize: '14px', fontFamily: 'monospace', color: '#94a3b8' }}>
          <span style={{ color: '#3b82f6' }}>{Math.round(a * a * 100) / 100}</span> +{' '}
          <span style={{ color: '#f59e0b' }}>{Math.round(b * b * 100) / 100}</span> ={' '}
          <span style={{ color: '#10b981', fontWeight: 'bold' }}>{Math.round((a*a + b*b) * 100) / 100}</span>
        </div>
      </div>
    </div>
  );
};
```

---

### 6.3 Production Prototype 2: Constrained CS Memory & Pointer Sandbox

Below is a complete, production-grade visualizer demonstrating **Archetype 3 (Algorithmic & State Machine Visualizer)** for pointer aliasing, heap allocation, and automated memory leak detection:

```tsx
// MemoryPointerSandbox.tsx
import React, { useState } from 'react';

interface Node {
  id: string;
  name: string;
  address: string;
  val: number;
}

interface Pointer {
  name: string;
  targetId: string | null; // Points to Node id or null
}

export const MemoryPointerSandbox: React.FC = () => {
  // Heap Nodes
  const [nodes, setNodes] = useState<Node[]>([
    { id: 'node_1', name: 'car_1', address: '0x6020', val: 100 },
    { id: 'node_2', name: 'car_2', address: '0x6040', val: 200 },
  ]);

  // Stack Pointers
  const [p1Target, setP1Target] = useState<string | null>('node_1');
  const [p2Target, setP2Target] = useState<string | null>('node_1'); // Aliased to node_1!

  // Diagnostics
  const isAliased = p1Target !== null && p1Target === p2Target;
  const isLeaked = nodes.some(n => n.id !== p1Target && n.id !== p2Target);

  return (
    <div style={{
      fontFamily: 'system-ui, sans-serif',
      background: '#0f172a',
      color: '#f8fafc',
      padding: '24px',
      borderRadius: '16px',
      maxWidth: '560px',
      boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.5)'
    }}>
      <div style={{ fontSize: '12px', fontWeight: 700, color: '#38bdf8', letterSpacing: '1px' }}>
        SYSTEMS SANDBOX: POINTER ALIASING
      </div>
      <h3 style={{ fontSize: '18px', fontWeight: 600, margin: '6px 0 16px 0' }}>
        Manipulate stack pointers. Observe aliasing and memory leaks:
      </h3>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
        {/* Stack Pane */}
        <div style={{ background: '#1e293b', padding: '14px', borderRadius: '10px', border: '1px solid #334155' }}>
          <h4 style={{ margin: '0 0 10px 0', fontSize: '13px', color: '#94a3b8', textTransform: 'uppercase' }}>
            Stack Frame (Pointers)
          </h4>
          
          {/* Pointer 1 Controls */}
          <div style={{ marginBottom: '12px' }}>
            <span style={{ fontSize: '13px', fontWeight: 'bold', color: '#38bdf8' }}>car_t* ptr_a ➔ </span>
            <select 
              value={p1Target || ''} 
              onChange={(e) => setP1Target(e.target.value || null)}
              style={{ background: '#0f172a', color: '#f8fafc', border: '1px solid #475569', borderRadius: '4px', padding: '4px' }}
            >
              <option value="node_1">car_1 (0x6020)</option>
              <option value="node_2">car_2 (0x6040)</option>
              <option value="">NULL (0x0)</option>
            </select>
          </div>

          {/* Pointer 2 Controls */}
          <div>
            <span style={{ fontSize: '13px', fontWeight: 'bold', color: '#a855f7' }}>car_t* ptr_b ➔ </span>
            <select 
              value={p2Target || ''} 
              onChange={(e) => setP2Target(e.target.value || null)}
              style={{ background: '#0f172a', color: '#f8fafc', border: '1px solid #475569', borderRadius: '4px', padding: '4px' }}
            >
              <option value="node_1">car_1 (0x6020)</option>
              <option value="node_2">car_2 (0x6040)</option>
              <option value="">NULL (0x0)</option>
            </select>
          </div>
        </div>

        {/* Heap Pane */}
        <div style={{ background: '#1e293b', padding: '14px', borderRadius: '10px', border: '1px solid #334155' }}>
          <h4 style={{ margin: '0 0 10px 0', fontSize: '13px', color: '#94a3b8', textTransform: 'uppercase' }}>
            Heap Allocations (RAM)
          </h4>
          {nodes.map(node => {
            const isTargeted = p1Target === node.id || p2Target === node.id;
            return (
              <div key={node.id} style={{
                padding: '8px',
                marginBottom: '8px',
                borderRadius: '6px',
                background: isTargeted ? '#0f172a' : 'rgba(239, 68, 68, 0.15)',
                border: isTargeted ? '1px solid #38bdf8' : '1px dashed #ef4444',
                fontSize: '12px'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 'bold' }}>
                  <span>{node.name}</span>
                  <span style={{ color: '#94a3b8' }}>{node.address}</span>
                </div>
                <div style={{ color: '#94a3b8' }}>speed: {node.val} km/h</div>
                {!isTargeted && (
                  <div style={{ color: '#ef4444', fontSize: '11px', marginTop: '4px', fontWeight: 'bold' }}>
                    ⚠️ UNREFERENCED (LEAKED)
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Real-Time Diagnostic Feed */}
      <div style={{
        padding: '12px 16px',
        borderRadius: '8px',
        background: isLeaked ? 'rgba(239, 68, 68, 0.15)' : isAliased ? 'rgba(56, 189, 248, 0.1)' : 'rgba(34, 197, 94, 0.1)',
        border: `1px solid ${isLeaked ? '#ef4444' : isAliased ? '#38bdf8' : '#22c55e'}`,
        fontSize: '13px',
        lineHeight: 1.4
      }}>
        {isLeaked ? (
          <span style={{ color: '#ef4444', fontWeight: 600 }}>
            🚨 <strong>Memory Leak Detected:</strong> A heap block has zero incoming pointers. Its address is lost, making <code>free()</code> impossible!
          </span>
        ) : isAliased ? (
          <span style={{ color: '#38bdf8', fontWeight: 600 }}>
            🔗 <strong>Pointer Aliasing Active:</strong> <code>ptr_a</code> and <code>ptr_b</code> reference identical memory at address <code>{nodes.find(n => n.id === p1Target)?.address}</code>. Mutating through <code>ptr_a</code> instantly alters reads via <code>ptr_b</code>!
          </span>
        ) : (
          <span style={{ color: '#22c55e', fontWeight: 600 }}>
            ✅ <strong>Clean Isolation:</strong> Every allocated block is referenced by exactly one owner pointer.
          </span>
        )}
      </div>
    </div>
  );
};
```

---


---

# STANDALONE CHAPTER SERVER TEMPLATE (web_pack/extreme-c/ch09/server.py):

```python
#!/usr/bin/env python3
"""Dedicated Local Chapter Server for extreme-c - ch09
Zero-dependency static file server with auto-port discovery, browser launch,
and optional /api/compile or /api/run sandbox endpoints.
"""
import argparse
import http.server
import json
import mimetypes
import os
import socket
import socketserver
import subprocess
import sys
import tempfile
import webbrowser
from pathlib import Path

DIRECTORY = Path(__file__).resolve().parent

# Ensure modern web MIME types are properly recognized
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("application/javascript", ".mjs")
mimetypes.add_type("application/wasm", ".wasm")
mimetypes.add_type("image/svg+xml", ".svg")
mimetypes.add_type("application/json", ".json")
mimetypes.add_type("text/css", ".css")


def find_free_port(start_port: int = 8080, max_attempts: int = 100) -> int:
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return start_port


class ChapterRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

    def end_headers(self):
        # Enable CORS and disable aggressive caching for local interactive development
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_POST(self):
        """Handle optional local code compilation or execution requests."""
        if self.path in ("/api/compile", "/api/run"):
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body) if body else {}
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON body")
                return

            code = data.get("code", "")
            lang = data.get("lang", "c")

            if not code.strip():
                self._send_json({"success": False, "error": "Empty code payload"})
                return

            # Execute host compiler/runner safely
            result = self._execute_code(code, lang, run_exec=(self.path == "/api/run"))
            self._send_json(result)
        else:
            self.send_error(404, "Endpoint not found")

    def _send_json(self, data: dict, status: int = 200):
        response_bytes = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

    def _execute_code(self, code: str, lang: str, run_exec: bool = False) -> dict:
        """Compile and optionally run code in a temporary sandbox with timeout."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            if lang in ("c", "c99"):
                src = tmppath / "main.c"
                binary = tmppath / "main.out"
                src.write_text(code, encoding="utf-8")
                
                cmd = ["gcc", "-Wall", "-Wextra", "-std=c99", str(src), "-o", str(binary)]
                try:
                    comp = subprocess.run(cmd, capture_output=True, text=True, timeout=5.0)
                    if comp.returncode != 0:
                        return {
                            "success": False,
                            "phase": "compile",
                            "stdout": comp.stdout,
                            "stderr": comp.stderr,
                            "returncode": comp.returncode,
                        }
                    if not run_exec:
                        return {
                            "success": True,
                            "phase": "compile",
                            "stdout": comp.stdout,
                            "stderr": comp.stderr,
                            "returncode": 0,
                        }

                    # Run binary with strict timeout
                    run = subprocess.run([str(binary)], capture_output=True, text=True, timeout=2.0)
                    return {
                        "success": run.returncode == 0,
                        "phase": "run",
                        "stdout": run.stdout,
                        "stderr": run.stderr,
                        "returncode": run.returncode,
                    }
                except subprocess.TimeoutExpired:
                    return {"success": False, "error": "Execution timed out (2.0s limit)"}
                except FileNotFoundError:
                    return {"success": False, "error": "Host compiler 'gcc' not found"}
            elif lang == "python":
                src = tmppath / "main.py"
                src.write_text(code, encoding="utf-8")
                try:
                    run = subprocess.run([sys.executable, str(src)], capture_output=True, text=True, timeout=2.0)
                    return {
                        "success": run.returncode == 0,
                        "phase": "run",
                        "stdout": run.stdout,
                        "stderr": run.stderr,
                        "returncode": run.returncode,
                    }
                except subprocess.TimeoutExpired:
                    return {"success": False, "error": "Execution timed out (2.0s limit)"}
            else:
                return {"success": False, "error": f"Unsupported language: {lang}"}


def run_server(port: int = 8080, open_browser: bool = True):
    free_port = find_free_port(port)
    url = f"http://localhost:{free_port}/"
    
    # Custom TCPServer allowing port reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", free_port), ChapterRequestHandler) as httpd:
        print(f"============================================================")
        print(f"  termlearn web study: extreme-c / ch09")
        print(f"  Serving at: {url}")
        print(f"  Directory:  {DIRECTORY}")
        print(f"  Press Ctrl+C to stop.")
        print(f"============================================================")
        if open_browser:
            webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"Serve extreme-c ch09 interactive web study")
    parser.add_argument("--port", type=int, default=8080, help="Preferred port (default: 8080)")
    parser.add_argument("--no-browser", action="store_true", help="Do not open browser automatically")
    args = parser.parse_args()
    run_server(port=args.port, open_browser=not args.no_browser)

```


---

# CHAPTER ch09 OF extreme-c (7 part(s))
# TARGET DIRECTORY DESTINATION: web_pack/extreme-c/ch09/
# Process: Answer ASK_USER_WEB questions first, then create files in `web_pack/extreme-c/ch09/`.


## part 1/7

# Chapter 06

<!-- source: Text/oop_and_encapsulation.xhtml | spine-id: oop_and_encapsulation.xhtml | chapter: ch09 -->

# Chapter 06

# OOP and Encapsulation

There are many great books and articles on the subject of object-oriented programming or OOP. But I don't think that many of them address the same topic using a non-OOP language such as C! How is that even possible? Are we even able to write object-oriented programs with a programming language that has no support for it? To be precise, is it possible to write an object-oriented program using C?

The short answer to the above question is yes, but before explaining how, we need to explain why. We need to break the question down and see what OOP really means. Why is it possible to write an object-oriented program using a language that has no claim for object-orientation support? This seems like a paradox, but it's not, and our effort in this chapter is to explain why that's possible and how it should be done.

Another question that may puzzle you is that what's the point of having such discussions and knowing about OOP when you are going to use C as your primary programming language? Almost all existing mature C code bases such as open source kernels, implementation of services like HTTPD, Postfix, nfsd, ftpd, and many other C libraries such as OpenSSL and OpenCV, are all written in an object-oriented fashion. This doesn't mean that C is object-oriented; instead, the approach these projects have taken to organize their internal structure comes from an object-oriented mindset.

I highly recommend reading this chapter together with the next three chapters and getting to know more about OOP because firstly, it will enable you to think and design like the engineers who have designed the libraries mentioned before, and secondly, it would be highly beneficial when reading the sources of such libraries.

C does not support object-oriented concepts such as classes, inheritance, and virtual functions in its syntax. However, it does support object-oriented concepts – in an indirect way. In fact, nearly all the computer languages through history have supported OOP intrinsically – way before the days of Smalltalk, C++, and Java. That's because there must be a way in every general-purpose programming language to extend its data types and it is the first step towards OOP.

C cannot and should not support object-oriented features in its syntax; not because of its age, but because of very good reasons that we're going to talk about in this chapter. Simply put, you can still write an object-oriented program using C, but it takes a bit of extra effort to get around the complexity.

There are a few books and articles regarding OOP in C, and they usually try to create a type system for writing classes, implementing inheritance, polymorphism, and more, using C. These books look at adding OOP support as a set of functions, macros, and a preprocessor, all of which can be used together to write object-oriented programs with C. This won't be the approach we take in this chapter. We are not going to create a new C++ out of C; instead, we want to speculate how C has the potential to be used for OOP.

It is usually said that OOP is another programming paradigm together with procedural and functional paradigms. But OOP is more than that. OOP is more like a way of thinking about and analyzing a problem. It is an attitude towards the universe and the hierarchy of objects within it. It is part of our ancient, intrinsic, and inherited method for comprehending and analyzing the physical and abstract entities around us. It is so fundamental to our understanding of nature.

We've always thought about every problem from an object-oriented point of view. OOP is just about applying the same point of view that humans have always adopted, but this time using a programming language to solve a computational problem. All this explains why OOP is the most common programming paradigm used for writing software.

This chapter, together with the following three chapters, are going to show that any concept within OOP can be implemented in C – even though it might be complex to do. We know we can have OOP with C because some people have already done it, especially when they created C++ on top of C, and since they have built many complex and successful programs in C in an object-oriented fashion.

What these chapters are not going to suggest is a certain library or set of macros that you should use for declaring a class or establishing an inheritance relation or working with other OOP concepts. In addition, we won't impose any methodology or discipline such as specific naming conventions. We will simply use raw C to implement OOP concepts.

The reason why we're dedicating four whole chapters to OOP with C is because of the heavy theory behind object orientation and the various examples that are necessary to be explored in order to demonstrate all of it. Most of the essential theory behind OOP is going to be explained in this chapter, while the more practical topics will be dealt with in the following chapters. With all that said, we need to discuss the theory because the OOP concepts are usually new to most skilled C programmers, even those with many years of experience.

The upcoming four chapters together cover almost anything that you might come across in OOP. In this chapter, we are going to discuss the following:

- First of all, we'll give definitions for the most fundamental terms used in OOP literature. We'll define classes, objects, attributes, behaviors, methods, domains, and more. These terms will be used heavily throughout these four chapters. They are also vital to your understanding of other OOP-related resources because they are a staple part of the accepted language of OOP.
- The first part of this chapter is not wholly about terminology; we'll also heavily discuss the roots of object orientation and the philosophy behind it, exploring the nature of object-oriented thinking.
- The second section of this chapter is dedicated to C and why it is not, and cannot, be object-oriented. This is an important question that should be asked and properly answered. This topic will be further discussed in Chapter 10, Unix – History and Architecture, where we will be exploring Unix and its close relationship to C.
- The third section of this chapter talks about encapsulation, which is one of the most fundamental concepts of OOP. Put simply, it's what allows you to create objects and use them. The fact that you can put variables and methods inside an object comes directly from encapsulation. This is discussed thoroughly in the third section, and several examples are given.
- The chapter then moves on to information-hiding, which is something of a side effect (though a very important one) of having encapsulation. Without information-hiding, we wouldn't be able to isolate and decouple software modules, and we'd effectively be unable to provide implementation-independent APIs to clients. This is the last thing we discuss as part of this chapter.

As mentioned, the whole topic will cover four chapters, with the following chapters picking up from the composition relationship. From there, the upcoming chapters will cover aggregation, inheritance, polymorphism, abstraction.

In this chapter, though, we'll start with the theory behind OOP and look at how we can extract an object model from our thought process regarding a software component.

# Object-oriented thinking

As we said in the chapter introduction, object-oriented thinking is the way in which we break down and analyze what surrounds us. When you're looking at a vase on a table, you're able to understand that the vase and the table are separate objects without any heavy analysis.

Unconsciously, you are aware that there is a border between them that separates them. You know that you could change the color of the vase, and the color of the table would remain unchanged.

These observations show us that we view our environment from an object-oriented perspective. In other words, we are just creating a reflection of the surrounding object-oriented reality in our minds. We also see this a lot in computer games, 3D modeling software, and engineering software, all of which can entail many objects interacting with each other.

OOP is about bringing object-oriented thinking to software design and development. Object-oriented thinking is our default way of processing our surroundings, and that's why OOP has become the most commonly used paradigm for writing software.

Of course, there are problems that would be hard to solve if you go with the object-oriented approach, and they would have been analyzed and resolved easier if you chose another paradigm, but these problems can be considered relatively rare.

In the following sections, we are going to find out more about the translation of object-oriented thinking into writing object-oriented code.

## Mental concepts

You'd be hard-pressed to find a program that completely lacks at least some traces of object-oriented thinking, even if it had been written using C or some other non-OOP language. If a human writes a program, it will be naturally object-oriented. This will be evident even just in the variable names. Look at the following example. It declares the variables required to keep the information of 10 students:

char* student_first_names[10];

char* student_surnames[10];

int student_ages[10];

double student_marks[10];

Code Box 6-1: Four arrays related by having the student_ prefix, according to a naming convention, supposed to keep the information of 10 students

The declarations found in Code Box 6-1 show how we use variable names to group some variables under the same concept, which in this case is the student. We have to do this; else we would get confused by ad hoc names that don't make any sense to our object-oriented minds. Suppose that we had something such as this instead:

char* aaa[10];

char* bbb[10];

int ccc[10];

double ddd[10];

Code Box 6-2: Four arrays with ad hoc names supposed to keep the information of 10 students!

Using such variable names as seen in Code Box 6-2, however much experience in programming you have, you must admit that you'd have a lot of trouble dealing with this when writing an algorithm. Variable naming is – and has always been – important, because the names remind us of the concepts in our mind and the relationships between data and those concepts. By using this kind of ad hoc naming, we lose those concepts and their relationships in the code. This may not pose an issue for the computer, but it complicates the analysis and troubleshooting for us programmers and increases the likelihood of us making mistakes.

Let's clarify more about what we mean by a concept in our current context. A concept is a mental or abstract image that exists in the mind as a thought or an idea. A concept could be formed by the perception of a real-world entity or could simply be entirely imaginary and abstract. When you look at a tree or when you think about a car, their corresponding images come to mind as two different concepts.

Note that sometimes we use the term concept in a different context, such as in "object-oriented concepts," which obviously doesn't use the word concept in the same way as the definition we just gave. The word concept, used in relation to technology-related topics, simply refers to the principles to understand regarding a topic. For now, we'll use this technology-related definition.

Concepts are important to object-oriented thinking because if you cannot form and maintain an understanding of objects in your mind, you cannot extract details about what they represent and relate to, and you cannot understand their interrelations.

So, object-oriented thinking is about thinking in terms of concepts and their relationships. It follows, then, that if you want to write a proper object-oriented program, you need to have a proper underst


## part 2/7

e'll use this technology-related definition.

Concepts are important to object-oriented thinking because if you cannot form and maintain an understanding of objects in your mind, you cannot extract details about what they represent and relate to, and you cannot understand their interrelations.

So, object-oriented thinking is about thinking in terms of concepts and their relationships. It follows, then, that if you want to write a proper object-oriented program, you need to have a proper understanding of all the relevant objects, their corresponding concepts, and also their relationships, in your mind.

An object-oriented map formed in your mind, which consists of many concepts and their mutual interrelations, cannot be easily communicated to others, for instance when approaching a task as a team. More than that, such mental concepts are volatile and elusive, and they can get forgotten very easily. This also puts an extra emphasis on the fact that you will need models and other tools for representation, in order to translate your mind map into communicable ideas.

## Mind maps and object models

In this section, we look at an example to understand further what we've been discussing so far. Suppose that we have a written description of a scene. The purpose of describing something is to communicate the related specific concepts to the audience. Think of it this way: the one who is describing has a map in their mind that lays out various concepts and how they all link together; their aim is to communicate that mind map to the audience. You might say that this is more or less the goal of all artistic expression; it is actually what's happening when you look at a painting, listen to a piece of music, or read a novel.

Now we are going to look at a written description. It describes a classroom. Relax your mind and try to imagine what you are reading about. Everything you see in your mind is a concept communicated by the following description:

Our classroom is an old room with two big windows. When you enter the room, you can see the windows on the opposite wall. There are a number of brown wooden chairs in the middle of the room. There are five students sitting on the chairs, and two of them are boys. There is a green, wooden blackboard on the wall to your right, and the teacher is talking to the students. He is an old man wearing a blue shirt.

Now, let's see what concepts have formed in our minds. Before we do that though, bear in mind that your imagination can run away without you noticing. So, let's do our best to limit ourselves to the boundaries of the description. For example, I could imagine more and say that the girls are blonde. But that is not mentioned in the description, so we won't take that into account. In the next paragraph, I explain what has been shaped in my mind, and before continuing, you should also try to do that for yourself.

In my mind, there are five concepts (or mental images, or objects), one for each student in the class. There are also another five concepts for the chairs. There is another concept for the wood and another one for the glass. And I know that every chair is made from wood. This is a relationship, between the concept of wood and the concepts of the chairs. In addition, I know that every student is sitting on a chair. As such, there are five relationships – between chairs and students. We could continue to identify more concepts and relate them. In no time, we'd have a huge and complex graph describing the relationships of hundreds of concepts.

Now, pause for a moment and see how differently you were extracting the concepts and their relationships. That's a lesson that everyone can do this in a different way. This procedure also happens when you want to solve a particular problem. You need to create a mind map before attacking the problem. This is the phase that we call the understanding phase.

You solve a problem using an approach that is based on the concepts of the problem and the relationships you find between them. You explain your solution in terms of those concepts, and if someone wants to understand your solution, they should understand the concepts and their relationships first.

You'd be surprised if I told you this is what exactly happens when you try to solve a problem using a computer, but that is exactly the case. You break the problem into objects (same as the concepts in a mental context) and the relationships between them, and then you try to write a program, based on those objects, that eventually resolves the problem.

The program that you write simulates the concepts and their relations as you have them in your mind. The computer runs the solution, and you can verify whether it works. You are still the person who solves the problem, but now a computer is your colleague, since it can execute your solution, which is now described as a series of machine-level instructions translated from your mind map, much faster and more accurately.

An object-oriented program simulates concepts in terms of objects, and while we create a mind map for a problem in our minds, the program creates an object model in its memory. In other words, the terms concept, mind, and mind map are equivalent to object, memory, and object model respectively, if we are going to compare a human with an object-oriented program. This is the most important correlation we offer in this section, which relates the way we think to an object-oriented program.

But why are we using computers to simulate our mind maps? Because computers are good when it comes to speed and precision. This is a very classic answer to such questions, but it is still a relevant answer to our question. Creating and maintaining a big mind map and the corresponding object model is a complex task and is one that computers can do very well. As another advantage, the object model created by a program can be stored on a disk and used later.

A mind map can be forgotten or altered by emotions, but computers are emotionless, and object models are far more robust than human thoughts. That's why we should write object-oriented programs: to be able to transfer the concepts of our minds to effective programs and software.

Note:

So far, nothing has been invented that can download and store a mind map from someone's mind – but perhaps in the future!

## Objects are not in code

If you look at the memory of a running object-oriented program, you'll find it full of objects, all of which are interrelated. That's the same for humans. If you consider a human as a machine, you could say that they are always up and running until they die. Now, that's an important analogy. Objects can only exist in a running program, just as concepts can only exist in a living mind. That means you have objects only when you have a running program.

This may look like a paradox because when you are writing a program (an object-oriented one), the program doesn't yet exist and so cannot be running! So, how can we write object-oriented code when there is no running program and no objects?

Note:

When you are writing object-oriented code, no object exists. The objects are created once you build the code into an executable program and run it.

OOP is not actually about creating objects. It is about creating a set of instructions that will lead to a fully dynamic object model when the program is run. So, the object-oriented code should be able to create, modify, relate, and even delete objects, once compiled and run.

As such, writing object-oriented code is a tricky task. You need to imagine the objects and their relations before they exist. This is exactly the reason why OOP can be complex and why we need a programming language that supports object-orientation. The art of imagining something which is not yet created and describing or engineering its various details is usually called design. That's why this process is usually called object-oriented design (OOD) in object-oriented programming.

In object-oriented code, we only plan to create objects. OOP leads to a set of instructions for when and how an object should be created. Of course, it is not only about creation. All the operations regarding an object can be detailed using a programming language. An OOP language is a language that has a set of instructions (and grammar rules) that allow you to write and plan different object-related operations.

So far, we've seen that there is a clear correspondence between concepts in the human mind and objects in a program's memory. So, there should be a correspondence between the operations that can be performed on concepts and objects.

Every object has a dedicated life cycle. This is also true for concepts in the mind. At some point, an idea comes to mind and creates a mental image as a concept, and at some other point, it fades away. The same is true for objects. An object is constructed at one point and is destructed at another time.

As a final note, some mental concepts are very firm and constant (as opposed to volatile and transient concepts which come and go). It seems that these concepts are independent of any mind and have been in existence even when there were no minds to comprehend them. They are mostly mathematical concepts. The number 2 is an example. We have only one number 2 in the whole universe! That's amazing. It means that you and I have the very same concept in our minds of the number 2; if we tried to change it, it would no longer be the number 2. This is exactly where we leave the object-oriented realm, and we step into another realm, full of immutable objects, that is described under the title of the functional programming paradigm.

## Object attributes

Each concept in any mind has some attributes associated with it. If you remember, in our classroom description, we had a chair, named chair1, that was brown. In other words, every chair object has an attribute called color and it was brown for the chair1 object. We know that there were four other chairs in the classroom, and they had their color attributes which could have different values. In our description, all of them were brown, but it could be that in another description, one or two of them were yellow.

An object can have more than one attribute or a set of attributes. We call the values assigned to these attributes, collectively, the state of an object. The state can be thought of simply as a list of values, each one belonging to a certain attribute, attached to an object. An object can be modified during its lifetime. Such an object is said to be mutable. This simply means that the state can be changed during its lifetime. Objects can also be stateless, which means that they don't carry any state (or any attributes).

An object can be immutable as well, exactly like the concept (or object) corresponding to the number 2, which cannot be altered — being immutable means that the state is determined upon construction and cannot be modified after that.

Note:

A stateless object can be thought of as an immutable object because its state cannot be changed throughout its lifetime. In fact, it has no state to be changed.

As a final note, immutable objects are especially important. The fact that their state cannot be altered is an advantage, especially when they are shared in a multithreaded environment.

## Domain

Every program written to solve a particular problem, even an exceedingly small one, has a well-defined domain. Domain is another big term that is used widely in the literature of software engineering. The domain defines the boundaries in which software exhibits its functionality. It also defines the requirements that software should address.

A domain uses a specific and predetermined terminology (glossary) to deliver its mission and have engineers stay within its boundaries. Everyone participating in a software project should be aware of the domain in which their project is defined.

As an example, banking software is usually built for a


## part 3/7

used widely in the literature of software engineering. The domain defines the boundaries in which software exhibits its functionality. It also defines the requirements that software should address.

A domain uses a specific and predetermined terminology (glossary) to deliver its mission and have engineers stay within its boundaries. Everyone participating in a software project should be aware of the domain in which their project is defined.

As an example, banking software is usually built for a very well-defined domain. It has a set of well-known terms as its glossary which includes account, credit, balance, transfer, loan, interest, and so on.

The definition of a domain is made clear by the terms found in its glossary; you wouldn't find the terms patient, medicine, and dosage in the banking domain, for instance.

If a programming language doesn't provide facilities for working with the concepts specific to a given domain (such as the concepts of patients and medicines in the healthcare domain), it would be difficult to write the software for that domain using that programming language – not impossible, but certainly complex. Moreover, the bigger the software is, the harder it becomes to develop and maintain.

## Relations among objects

Objects can be inter-related; they can refer to each other to denote relationships. For example, as part of our classroom description, the object student4 (the fourth student) might be related to the object chair3 (the third chair) in regard to a relationship named sitting on. In other words, student4 sits on chair3. This way, all objects within a system refer to each other and form a network of objects called an object model. As we've said before, an object model is the correspondent of the mind map that we form in our minds.

When two objects are related, a change in the state of one might affect the state of the other. Let's explain this by giving an example. Suppose that we have two unrelated objects, `p1` and `p2`, representing pixels.

Object `p1` has a set of attributes as follows: `{x: 53, y: 345, red: 120, green: 45, blue: 178}`. Object `p2` has the attributes `{x: 53, y: 346, red: 79, green: 162, blue: 23}`.

Note:

The notation we used is almost but not quite the same as JavaScript Object Notation or JSON. In this notation, the attributes of an individual object are embraced within two curly braces, and the attributes are separated by commas. Each attribute has a corresponding value separated from the attribute by a colon.

Now, in order to make them related, they need to have an extra attribute to denote the relationship between themselves. The state of object `p1` would change to `{x: 53, y: 345, red: 120, green: 45, blue: 178, adjacent_down_pixel: p2}`, and that of `p2` would change to `{x: 53, y: 346, red: 79, green: 162, blue: 23, adjacent_up_pixel: p1}`.

The `adjacent_down_pixel` and `adjacent_up_pixel` attributes denote the fact that these pixel objects are adjacent; their `y` attributes differ only by 1 unit. Using such extra attributes, the objects realize that they are in a relationship with other objects. For instance, `p1` knows that its `adjacent_down_pixel` is `p2`, and `p2` knows that its `adjacent_up_pixel` is `p1`.

So, as we can see, if a relationship is formed between two objects, the states of those objects (or the lists of the values corresponding to their attributes) are changed. So, the relationship among objects is created by adding new attributes to them and because of that, the relationship becomes part of the objects' states. This, of course, has ramifications for the mutability or immutability of these objects.

Note that the subset of the attributes which define the state and immutability of an object can be changed from a domain to another, and it doesn't necessarily encompass all the attributes. In one domain, we might use only non-referring attributes (`x`, `y`, `red`, `green`, and `blue`, in the preceding example) as the state and in another domain, we might combine them all together with referring attributes (`adjacent_up_pixel` and`adjacent_down_pixel` in the preceding example).

## Object-oriented operations

An OOP language allows us to plan the object construction, object destruction, and altering the states of an object in a soon-to-be-running program. So, let's start by looking at the object construction.

Note:

The term construction has been chosen carefully. We could use creation or building, but these terms are not accepted as part of the standard terminology in OOP literature. Creation refers to the memory allocation for an object, while construction means the initialization of its attributes.

There are two ways to plan the construction of an object:

- The first approach involves either constructing an empty object – one without any attributes in its state – or, more commonly, an object with a set of minimum attributes.
- More attributes will be determined and added as the code is being run. Using this method, the same object can have different attributes in two different executions of the same program, in accordance with the changes found in the surrounding environment.
- Each object is treated as a separate entity, and any two objects, even if they seem to belong to the same group (or class), by having a list of common attributes, may get different attributes in their states as the program continues.
- As an example, the already mentioned pixel objects `p1` and `p2` are both pixels (or they both belong to the same class named `pixel`) because they have the same attributes – `x`, `y`, `red`, `green`, and `blue`. After forming a relationship, they would have different states because they then have new and different attributes: `p1` has the `adjacent_down_pixel` attribute, and `p2` has the `adjacent_up_pixel` attribute.
- This approach is used in programming languages such as JavaScript, Ruby, Python, Perl, and PHP. Most of them are interpreted programming languages, and the attributes are kept as a map (or a hash) in their internal data structures that can be easily changed at runtime. This technique is usually called prototype-based OOP.
- The second approach involves constructing an object whose attributes are predetermined and won't change in the middle of execution. No more attributes are allowed to be added to such an object at runtime, and the object will retain its structure. Only the values of the attributes are allowed to change, and that's possible only when the object is mutable.
- To apply this approach, a programmer should create a predesigned object template or class that keeps track of all the attributes that need to be present in the object at runtime. Then, this template should be compiled and fed into the object-oriented language at runtime.
- In many programming languages, this object template is called a class. Programming languages such as Java, C++, and Python use this term to denote their object templates. This technique is usually known as class-based OOP. Note that Python supports both prototype-based and class-based OOP.

Note:

A class only determines the list of attributes present in an object but not the actual values assigned to them at runtime.

Note that an object and an instance are the same thing, and they can be used interchangeably. However, in some texts, there might be some slight differences between them. There is also another term, reference, which is worth mentioning and explaining. The term object or instance is used to refer to the actual place allocated in the memory for the values of that object, while a reference is like a pointer that refers to that object. So, we can have many references referring to the same object. Generally speaking, an object usually has no name, but a reference does have a name.

Note:

In C, we have pointers as the corresponding syntax for references. We also have both Stack objects and Heap objects. A Heap object does not have a name and we use pointers to refer to it. In contrast, a Stack object is actually a variable and hence has a name.

While it is possible to use both approaches, C and especially C++ are officially designed in a way to support the class-based approach. Therefore, when a programmer wants to create an object in C or C++, they need to have a class first. We will talk more about the class and its role in OOP in future sections.

The following discussion might seem a bit unrelated, but, in fact, it isn't. There are two schools of thought regarding how humans grow through life, and they match quite accurately the object construction approaches that we've talked about. One of these philosophies says that the human is empty at birth and has no essence (or state).

By living and experiencing different good and bad events in life, their essence starts to grow and evolves into something that has an independent and mature character. Existentialism is a philosophical tradition that promotes this idea.

Its famous precept is "Existence precedes essence". This simply means that the human first comes to existence and then gains their essence through life experience. This idea is awfully close to our prototype-based approach to object construction, in which the object is constructed empty and then evolves at runtime.

The other philosophy is older and is promoted mostly by religions. In this, the human is created based on an image (or an essence), and this image has been determined before the human comes to exist. This is most similar to the way in which we plan to construct an object based on a template or class. As the object creators, we prepare a class, and then a program starts to create objects according to that class.

Note:

There has been a great correspondence between the approaches that people in novels or stories, including both literature and history sources, take to overcome a certain difficulty and the algorithms we have designed in computer science to solve similar problems. I deeply believe that the way humans live and the reality they experience are in great harmony with what we understand about algorithms and data structures as part of computer science. The preceding discussion was a great example of such harmony between OOP and Philosophy.

Like object construction, object destruction happens at runtime; we have only the power to plan it in code. All resources allocated by an object throughout its lifetime should be released when it is destroyed. When an object is being destructed, all other related objects should be changed so that they no longer refer to the destroyed object. An object shouldn't have an attribute that refers to a non-existent object, otherwise we lose the referential integrity in our object model. It can lead to runtime errors such as memory corruption or segmentation fault, as well as logical errors such as miscalculations.

Modifying an object (or altering the state of an object) can happen in two different ways. It could simply be either a change in the value of an existing attribute or it could be the addition or removal of an attribute to/from the set of attributes in that object. The latter can only happen if we have chosen the prototype-based approach to object construction. Remember that altering the state of an object that is immutable is forbidden and usually, it is not permitted by an object-oriented language.

## Objects have behaviors

Every object, together with its attributes, has a certain list of functionalities that it can perform. For instance, a car object is able to speed up, slow down, turn, and so on. In OOP, these functionalities are always in accordance with the domain requirements. For example, in a banking object model, a client can order a new account but cannot eat. Of course, the client is a person and can eat, but as long as eating functionality is not related to the banking domain, we don't consider it as a necessary functionality for a client object.

Every functionality is able to change the state of an object by altering the va


## part 4/7

ject is able to speed up, slow down, turn, and so on. In OOP, these functionalities are always in accordance with the domain requirements. For example, in a banking object model, a client can order a new account but cannot eat. Of course, the client is a person and can eat, but as long as eating functionality is not related to the banking domain, we don't consider it as a necessary functionality for a client object.

Every functionality is able to change the state of an object by altering the values of its attributes. As a simple example, a car object can accelerate. Acceleration is a functionality of the car object, and by accelerating, the speed of the car, which is one of its attributes, changes.

In summary, an object is simply a group of attributes and functionalities. In the later sections, we'll talk more about how to put these things together in an object.

So far, we have explained the fundamental terminology needed to study and understand OOP. The next step is to explain the fundamental concept of encapsulation. But, as a break, let's read about why C cannot be an OOP language.

# C is not object-oriented, but why?

C is not object-oriented, but not because of its age. If age was a reason, we could have found a way to make it object-oriented by now. But, as you will see in Chapter 12, The Most Recent C, the latest standard of the C programming language, C18, doesn't try to make C an object-oriented language.

On the other hand, we have C++, which is the result of all efforts to have an OOP language based on C. If the fate of C was for it to be replaced by an object-oriented language, then there wouldn't be any demand for C today, mainly because of C++ – but the current demand for C engineers shows that this is not the case.

A human thinks in an object-oriented way, but a CPU executes machine-level instructions which are procedural. A CPU just executes a set of instructions one by one, and from time to time, it has to jump, fetch, and execute other instructions from a different address in memory; quite similar to function calls in a program written using a procedural programming language like C.

C cannot be object-oriented because it is located on the barrier between object orientation and procedural programming. Object orientation is the human understanding of a problem and procedural execution is what a CPU can do. Therefore, we need something to be in this position and make this barrier. Otherwise high-level programs, which are usually written in an object-oriented way, cannot be translated directly into procedural instructions to be fed into the CPU.

If you look at high-level programming languages like Java, JavaScript, Python, Ruby, and so on, they have a component or layer within their architecture which bridges between their environment and the actual C library found inside the operating system (the Standard C Library in Unix-like systems and Win32 API in Windows systems). For instance, Java Virtual Machine (JVM) does that in a Java platform. While not all these environments are necessarily object-oriented (for example JavaScript or Python can be both procedural and object-oriented), they need this layer to translate their high-level logic to low-level procedural instructions.

# Encapsulation

In the previous sections, we saw that each object has a set of attributes and a set of functionalities attached to it. Here, we are going to talk about putting those attributes and functionalities into an entity called an object. We do this through a process called encapsulation.

Encapsulation simply means putting related things together into a capsule that represents an object. It happens first in your mind, and then it should be transferred to the code. The moment that you feel an object needs to have some attributes and functionalities, you are doing encapsulation in your mind; that encapsulation then needs to be transferred to the code level.

It is crucial to be able to encapsulate things in a programming language, otherwise keeping related variables together becomes an untenable struggle (we mentioned using naming conventions to accomplish this).

An object is made from a set of attributes and a set of functionalities. Both of these should be encapsulated into the object capsule. Let's first talk about attribute encapsulation.

## Attribute encapsulation

As we saw before, we can always use variable names to do encapsulation and tie different variables together and group them under the same object. Following is an example:

int pixel_p1_x = 56;

int pixel_p1_y = 34;

int pixel_p1_red = 123;

int pixel_p1_green = 37;

int pixel_p1_blue = 127;

int pixel_p2_x = 212;

int pixel_p2_y = 994;

int pixel_p2_red = 127;

int pixel_p2_green = 127;

int pixel_p2_blue = 0;

Code Box 6-3: Some variables representing two pixels grouped by their names

This example clearly shows how variable names are used to group variables under `p1` and `p2`, which somehow are implicit objects. By implicit, we mean that the programmer is the only one who is aware of the existence of such objects; the programming language doesn't know anything about them.

The programming language only sees 10 variables that seem to be independent of each other. This would be a very low level of encapsulation, to such an extent that it would not be officially considered as encapsulation. Encapsulation by variable names exists in all programming languages (because you can name variables), even in an assembly language.

What we need are approaches offering explicit encapsulation. By explicit, we mean that both the programmer and the programming language are aware of the encapsulation and the capsules (or objects) that exist. Programming languages that do not offer explicit attribute encapsulation are very hard to use.

Fortunately, C does offer explicit encapsulation, and that's one of the reasons behind why we are able to write so many intrinsically object-oriented programs with it more or less easily. On the other hand, as we see shortly in the next section, C doesn't offer explicit behavior encapsulation, and we have to come up with an implicit discipline to support this.

Note that having an explicit feature such as encapsulation in a programming language is always desired. Here, we only spoke about encapsulation, but this can be extended to many other object-oriented features, such as inheritance and polymorphism. Such explicit features allow a programming language to catch relevant errors at compile time instead of runtime.

Resolving errors at runtime is a nightmare, and so we should always try to catch errors at compile time. This is the main advantage of having an object-oriented language, which is completely aware of the object-oriented way of our thinking. An object-oriented language can find and report errors and violations in our design at compile time and keep us from having to resolve many severe bugs at runtime. Indeed, this is the reason why we are seeing more complex programming languages every day – to make everything explicit to the language.

Unfortunately, not all object-oriented features are explicit in C. That's basically why it is hard to write an object-oriented program with C. But there are more explicit features in C++ and, indeed, that's why it is called an object-oriented programming language.

In C, structures offer encapsulation. Let's change the code inside Code Box 6-3, and rewrite it using structures:

typedef struct {

int x, y;

int red, green, blue;

} pixel_t;

pixel_t p1, p2;

p1.x = 56;

p1.y = 34;

p1.red = 123;

p1.green = 37;

p1.blue = 127;

p2.x = 212;

p2.y = 994;

p2.red = 127;

p2.green = 127;

p2.blue = 0;

Code Box 6-4: The pixel_t structure and declaring two pixel_t variables

There are some important things to note regarding Code Box 6-4:

- The attribute encapsulation happens when we put the `x`, `y`, `red`, `green`, and `blue` attributes into a new type, `pixel_t`.
- Encapsulation always creates a new type; attribute encapsulation does this particularly in C. This is very important to note. In fact, this is the way that we make encapsulation explicit. Please note the `_t` suffix at the end of the `pixel_t`. It is very common in C to add the `_t` suffix to the end of the name of new types, but it is not mandatory. We use this convention throughout this book.
- `p1` and `p2` will be our explicit objects when this code is executed. Both of them are of the `pixel_t` type, and they have only the attributes dictated by the structure. In C, and especially C++, types dictate the attributes to their objects.
- The new type, `pixel_t`, is only the attributes of a class (or the object template). The word "class," remember, refers to a template of objects containing both attributes and functionalities. Since a C structure only keeps attributes, it cannot be a counterpart for a class. Unfortunately, we have no counterpart concept for a class in C; attributes and functionalities exist separately, and we implicitly relate them to each other in the code. Every class is implicit to C and it refers to a single structure together with a list of C functions. You'll see more of this in the upcoming examples, as part of this chapter and the future chapters.
- As you see, we are constructing objects based on a template (here, the structure of `pixel_t`), and the template has the predetermined attributes that an object should have at birth. Like we said before, the structure only stores attributes and not the functionalities.
- Object construction is very similar to the declaration of a new variable. The type comes first, then the variable name (here the object name) after that. While declaring an object, two things happen almost at the same time: first the memory is allocated for the object (creation), and then, the attributes are initialized (construction) using the default values. In the preceding example, since all attributes are integers, the default integer value in C is going to be used which is 0.
- In C and many other programming languages, we use a dot (`.`) to access an attribute inside an object, or an arrow (`->`) while accessing the attributes of a structure indirectly through its address stored in a pointer. The statement `p1.x` (or `p1->x` if `p1` is a pointer) should be read as the x attribute in the p1 object.

As you know by now, attributes are certainly not the only things that can be encapsulated into objects. Now it is time to see how functionalities are encapsulated.

## Behavior encapsulation

An object is simply a capsule of attributes and methods. The method is another standard term that we usually use to denote a piece of logic or functionality being kept in an object. It can be considered as a C function that has a name, a list of arguments, and a return type. Attributes convey values and methods convey behaviors. Therefore, an object has a list of values and can perform certain behaviors in a system.

In class-based object-oriented languages such as C++, it is very easy to group a number of attributes and methods together in a class. In prototype-based languages such as JavaScript, we usually start with an empty object (ex nihilo, or "from nothing") or clone from an existing object. To have behaviors in the object, we need to add methods. Look at the following example, which helps you gain an insight into how prototype-based programming languages work. It is written in JavaScript:

// Construct an empty object

var clientObj = {};

// Set the attributes

clientObj.name = "John";

clientObj.surname = "Doe";

// Add a method for ordering a bank account

clientObj.orderBankAccount = function () {

...

}

...

// Call the method

clientObj.orderBankAccount();

Code Box 6-5: Constructing a client object in JavaScript

As you see in this example, on the 2nd line, we create an empty object. In the following two lines, we add two new attributes, `name` and `surname`, to our object. And on the following line, we add a new method, `orderBankAccount`, w


## part 5/7



clientObj.name = "John";

clientObj.surname = "Doe";

// Add a method for ordering a bank account

clientObj.orderBankAccount = function () {

...

}

...

// Call the method

clientObj.orderBankAccount();

Code Box 6-5: Constructing a client object in JavaScript

As you see in this example, on the 2nd line, we create an empty object. In the following two lines, we add two new attributes, `name` and `surname`, to our object. And on the following line, we add a new method, `orderBankAccount`, which points to a function definition. This line is an assignment actually. On the right-hand side is an anonymous function, which does not have a name and is assigned to the `orderBankAccount` attribute of the object, on the left-hand side. In other words, we store a function into the `orderBankAccount` attribute. On the last line, the object's method `orderBankAccount` is called. This example is a great demonstration of prototype-based programming languages, which only rely on having an empty object at first and nothing more.

The preceding example would be different in a class-based programming language. In these languages, we start by writing a class because without having a class, we can't have any object. The following code box contains the previous example but written in C++:

class Client {

public:

void orderBankAccount() {

...

}

std::string name;

std::string surname:

};

...

Client clientObj;

clientObj.name = "John";

clientObj.surname = "Doe";

...

clientObj.orderBankAccount ();

Code Box 6-6: Constructing the client object in C++

As you see, we started by declaring a new class, `Client`. On the 1st line, we declared a class, which immediately became a new C++ type. It resembles a capsule and is surrounded by braces. After declaring the class, we constructed the object `clientObj` from the `Client` type.

On the following lines, we set the attributes, and finally, we called the `orderBankAccount` method on the `clientObj` object.

Note:

In C++, methods are usually called member functions and attributes are called data members.

If you look at the techniques employed by open source and well-known C projects in order to encapsulate some items, you notice that there is a common theme among them. In the rest of this section, we are going to propose a behavior encapsulation technique which is based on the similar techniques observed in such projects.

Since we'll be referring back to this technique often, I'm going to give it a name. We call this technique implicit encapsulation. It's implicit because it doesn't offer an explicit behavior encapsulation that C knows about. Based on what we've got so far in the ANSI C standard, it is not possible to let C know about classes. So, all techniques that try to address object orientation in C have to be implicit.

The implicit encapsulation technique suggests the following:

- Using C structures to keep the attributes of an object (explicit attribute encapsulation). These structures are called attribute structures.
- For behavior encapsulation, C functions are used. These functions are called behavior functions. As you might know, we cannot have functions in structures in C. So, these functions have to exist outside the attribute structure (implicit behavior encapsulation).
- Behavior functions must accept a structure pointer as one of their arguments (usually the first argument or the last one). This pointer points to the attribute structure of the object. That's because the behavior functions might need to read or modify the object's attributes, which is very common.
- Behavior functions should have proper names to indicate that they are related to the same class of objects. That's why sticking to a consistent naming convention is very important when using this technique. This is one of the two naming conventions that we try to stick to in these chapters in order to have a clear encapsulation. The other one is using `_t` suffix in the names of the attribute structures. However, of course, we don't force them and you can use your own custom naming conventions.
- The declaration statements corresponding to the behavior functions are usually put in the same header file that is used for keeping the declaration of the attribute structure. This header is called the declaration header.
- The definitions of the behavior functions are usually put in one or various separate source files which include the declaration header.

Note that with implicit encapsulation, classes do exist, but they are implicit and known only to the programmer. The following example, example 6.1, shows how to use this technique in a real C program. It is about a car object that accelerates until it runs out of fuel and stops.

The following header file, as part of example 6.1, contains the declaration of the new type, `car_t`, which is the attribute structure of the `Car` class. The header also contains the declarations required for the behavior functions of the `Car` class. We use the phrase "the `Car` class" to refer to the implicit class that is missing from the C code and it encompasses collectively the attribute structure and the behavior functions:

#ifndef EXTREME_C_EXAMPLES_CHAPTER_6_1_H

#define EXTREME_C_EXAMPLES_CHAPTER_6_1_H

// This structure keeps all the attributes

// related to a car object

typedef struct {

char name[32];

double speed;

double fuel;

} car_t;

// These function declarations are

// the behaviors of a car object

void car_construct(car_t*, const char*);

void car_destruct(car_t*);

void car_accelerate(car_t*);

void car_brake(car_t*);

void car_refuel(car_t*, double);

#endif

Code Box 6-7 [ExtremeC_examples_chapter6_1.h]: The declarations of the attribute structure and the behavior functions of the Car class

As you see, the attribute structure `car_t` has three fields – `name`, `speed`, and `fuel` – which are the attributes of the car object. Note that `car_t` is now a new type in C, and we can now declare variables of this type. The behavior functions are also usually declared in the same header file, as you can see in the preceding code box. They start with the `car_` prefix to put emphasis on the fact that all of them belong to the same class.

Something very important regarding the implicit encapsulation technique: each object has its own unique attribute structure variable, but all objects share the same behavior functions. In other words, we have to create a dedicated variable from the attribute structure type for each object, but we only write behavior functions once and we call them for different objects.

Note that the `car_t` attribute structure is not a class itself. It only contains the attributes of the `Car` class. The declarations all together make the implicit `Car` class. You'll see more examples of this as we go on.

There are many famous open source projects that use the preceding technique to write semi-object-oriented code. One example is `libcurl`. If you have a look at its source code, you will see a lot of structures and functions starting with `curl_`. You can find the list of such functions here: https://curl.haxx.se/libcurl/c/allfuncs.html.

The following source file contains the definitions of the behavior functions as part of example 6.1:

#include <string.h>

#include "ExtremeC_examples_chapter6_1.h"

// Definitions of the above functions

void car_construct(car_t* car, const char* name) {

strcpy(car->name, name);

car->speed = 0.0;

car->fuel = 0.0;

}

void car_destruct(car_t* car) {

// Nothing to do here!

}

void car_accelerate(car_t* car) {

car->speed += 0.05;

car->fuel -= 1.0;

if (car->fuel < 0.0) {

car->fuel = 0.0;

}

}

void car_brake(car_t* car) {

car->speed -= 0.07;

if (car->speed < 0.0) {

car->speed = 0.0;

}

car->fuel -= 2.0;

if (car->fuel < 0.0) {

car->fuel = 0.0;

}

}

void car_refuel(car_t* car, double amount) {

car->fuel = amount;

}

Code Box 6-8 [ExtremeC_examples_chapter6_1.c]: The definitions of the behavior functions as part of the Car class

The `Car`'s behavior functions are defined in Code Box 6-8. As you can see, all the functions accept a `car_t` pointer as their first argument. This allows the function to read and modify the attributes of an object. If a function is not receiving a pointer to an attribute structure, then it can be considered as an ordinary C function that does not represent an object's behavior.

Note that the declarations of behavior functions are usually found next to the declarations of their corresponding attribute structure. That's because the programmer is the sole person in charge of maintaining the correspondence of the attribute structure and the behavior functions, and the maintenance should be easy enough. That's why keeping these two sets close together, usually in the same header file, helps in maintaining the overall structure of the class, and eases the pain for future efforts.

In the following code box, you'll find the source file that contains the `main` function and performs the main logic. All the behavior functions will be used here:

#include <stdio.h>

#include "ExtremeC_examples_chapter6_1.h"

// Main function

int main(int argc, char** argv) {

// Create the object variable

car_t car;

// Construct the object

car_construct(&car, "Renault");

// Main algorithm

car_refuel(&car, 100.0);

printf("Car is refueled, the correct fuel level is %f\n",

car.fuel);

while (car.fuel > 0) {

printf("Car fuel level: %f\n", car.fuel);

if (car.speed < 80) {

car_accelerate(&car);

printf("Car has been accelerated to the speed: %f\n",

car.speed);

} else {

car_brake(&car);

printf("Car has been slowed down to the speed: %f\n",

car.speed);

}

}

printf("Car ran out of the fuel! Slowing down ...\n");

while (car.speed > 0) {

car_brake(&car);

printf("Car has been slowed down to the speed: %f\n",

car.speed);

}

// Destruct the object

car_destruct(&car);

return 0;

}

Code Box 6-9 [ExtremeC_examples_chapter6_1_main.c]: The main function of example 6.1

As the first instruction in the `main` function, we've declared the `car` variable from the `car_t` type. The variable `car` is our first `car` object. On this line, we have allocated the memory for the object's attributes. On the following line, we constructed the object. Now on this line, we have initialized the attributes. You can initialize an object only when there is memory allocated for its attributes. In the code, the constructor accepts a second argument as the car's name. You may have noticed that we are passing the address of the `car` object to all `car_*` behavior functions.

Following that in the `while` loop, the `main` function reads the `fuel` attribute and checks whether its value is greater than zero. The fact that the `main` function, which is not a behavior function, is able to access (read and write) the `car`'s attributes is an important thing. The `fuel` and `speed` attributes, for instance, are examples of public attributes, which functions (external code) other than the behavior functions can access. We will come back to this point in the next section.

Before leaving the `main` function and ending the program, we've destructed the `car` object. This simply means that resources allocated by the object have been released at this phase. Regarding the `car` object in this example, there is nothing to be done for its destruction, but it is not always the case and destruction might have steps to be followed. We will see more of this in the upcoming examples. The destruction phase is mandatory and prevents memory leaks in the case of Heap allocations.

It would be good to see how we could write the preceding example in C++. This would help you to get an insight into how an OOP language understands classes and objects and how it reduces the overhead of writing proper object-oriented code.

The following code box, as part of example 6.2, shows the header file containing the `Car` class in C++:

#ifndef EXTREME_C_EXAMPLES_CHAPTER_6_2_H

#define EXTRE


## part 6/7

s. The destruction phase is mandatory and prevents memory leaks in the case of Heap allocations.

It would be good to see how we could write the preceding example in C++. This would help you to get an insight into how an OOP language understands classes and objects and how it reduces the overhead of writing proper object-oriented code.

The following code box, as part of example 6.2, shows the header file containing the `Car` class in C++:

#ifndef EXTREME_C_EXAMPLES_CHAPTER_6_2_H

#define EXTREME_C_EXAMPLES_CHAPTER_6_2_H

class Car {

public:

// Constructor

Car(const char*);

// Destructor

~Car();

void Accelerate();

void Brake();

void Refuel(double);

// Data Members (Attributes in C)

char name[32];

double speed;

double fuel;

};

#endif

Code Box 6-10 [ExtremeC_examples_chapter6_2.h]: The declaration of the Car class in C++

The main feature of the preceding code is the fact that C++ knows about classes. Therefore, the preceding code demonstrates an explicit encapsulation; both attribute and behavior encapsulations. More than that, C++ supports more object-oriented concepts such as constructors and destructors.

In the C++ code, all the declarations, both attributes and behaviors, are encapsulated in the class definition. This is the explicit encapsulation. Look at the two first functions that we have declared as the constructor and the destructor of the class. C doesn't know about the constructors and destructors; but C++ has a specific notation for them. For instance, the destructor starts with ~ and it has the same name as the class does.

In addition, as you can see, the behavior functions are missing the first pointer argument. That's because they all have access to the attributes inside the class. The next code box shows the content of the source file that contains the definition of the declared behavior functions:

#include <string.h>

#include "ExtremeC_examples_chapter6_2.h"

Car::Car(const char* name) {

strcpy(this->name, name);

this->speed = 0.0;

this->fuel = 0.0;

}

Car::~Car() {

// Nothing to do

}

void Car::Accelerate() {

this->speed += 0.05;

this->fuel -= 1.0;

if (this->fuel < 0.0) {

this->fuel = 0.0;

}

}

void Car::Brake() {

this->speed -= 0.07;

if (this->speed < 0.0) {

this->speed = 0.0;

}

this->fuel -= 2.0;

if (this->fuel < 0.0) {

this->fuel = 0.0;

}

}

void Car::Refuel(double amount) {

this->fuel = amount;

}

Code Box 6-11 [ExtremeC_examples_chapter6_2.cpp]: The definition of the Car class in C++

If you look carefully, you'll see that the `car` pointer in the C code has been replaced by a `this` pointer, which is a keyword in C++. The keyword `this` simply means the current object. I'm not going to explain it any further here, but it is a smart workaround to eliminate the pointer argument in C and make behavior functions simpler.

And finally, the following code box contains the `main` function that uses the preceding class:

// File name: ExtremeC_examples_chapter6_2_main.cpp

// Description: Main function

#include <iostream>

#include "ExtremeC_examples_chapter6_2.h"

// Main function

int main(int argc, char** argv) {

// Create the object variable and call the constructor

Car car("Renault");

// Main algorithm

car.Refuel(100.0);

std::cout << "Car is refueled, the correct fuel level is "

<< car.fuel << std::endl;

while (car.fuel > 0) {

std::cout << "Car fuel level: " << car.fuel << std::endl;

if (car.speed < 80) {

car.Accelerate();

std::cout << "Car has been accelerated to the speed: "

<< car.speed << std::endl;

} else {

car.Brake();

std::cout << "Car has been slowed down to the speed: "

<< car.speed << std::endl;

}

}

std::cout << "Car ran out of the fuel! Slowing down ..."

<< std::endl;

while (car.speed > 0) {

car.Brake();

std::cout << "Car has been slowed down to the speed: "

<< car.speed << std::endl;

}

std::cout << "Car is stopped!" << std::endl;

// When leaving the function, the object 'car' gets

// destructed automatically.

return 0;

}

Code Box 6-12 [ExtremeC_examples_chapter6_2_main.cpp]: The main function of example 6.2

The `main` function written for C++ is very similar to the one we wrote for C, except that it allocates the memory for a class variable instead of a structure variable.

In C, we can't put attributes and behavior functions in a bundle that is known to C. Instead, we have to use files to group them. But in C++, we have a syntax for this bundle, which is the class definition. It allows us to put data members (or attributes) and member functions (or behavior functions) in the same place.

Since C++ knows about the encapsulation, it is redundant to pass the pointer argument to the behavior functions, and as you can see, in C++, we don't have any first pointer arguments in member function declarations like those we see in the C version of the `Car` class.

So, what happened? We wrote an object-oriented program in both C, which is a procedural programming language, and in C++, which is an object-oriented one. The biggest change was using `car.Accelerate()` instead of `car_accelerate(&car)`, or using `car.Refuel(1000.0)` instead of `car_refuel(&car, 1000.0)`.

In other words, if we are doing a call such as `func(obj, a, b, c, ...)` in a procedural programming language, we can do it as `obj.func(a, b, c, ...)` in an object-oriented language. They are equivalent but coming from different programming paradigms. Like we said before, there are numerous examples of C projects that use this technique.

Note:

In Chapter 9, Abstraction and OOP in C++, you will see that C++ uses exactly the same preceding technique in order to translate high-level C++ function calls to low-level C function calls.

As a final note, there is an important difference between C and C++ regarding object destruction. In C++, the destructor function is invoked automatically whenever an object is allocated on top of the Stack and it is going out of scope, like any other Stack variable. This is a great achievement in C++ memory management, because in C, you may easily forget to call the destructor function and eventually experience a memory leak.

Now it is time to talk about other aspects of encapsulation. In the next section, we will talk about a consequence of encapsulation: information-hiding.

## Information hiding

So far, we've explained how encapsulation bundles attributes (which represent values) and functionalities (which represent behaviors) together to form objects. But it doesn't end there.

Encapsulation has another important purpose or consequence, which is information-hiding. Information-hiding is the act of protecting (or hiding) some attributes and behaviors that should not be visible to the outer world. By the outer world, we mean all parts of the code that do not belong to the behaviors of an object. By this definition, no other code, or simply no other C function, can access a private attribute or a private behavior of an object if that attribute or behavior is not part of the public interface of the class.

Note that the behaviors of two objects from the same type, such as `car1` and `car2` from the `Car` class, can access the attributes of any object from the same type. That's because of the fact that we write behavior functions once for all objects in a class.

In example 6.1, we saw that the `main` function was easily accessing the `speed` and `fuel` attributes in the `car_t` attribute structure. This means that all attributes in the `car_t` type were public. Having a public attribute or behavior can be a bad thing because it might have some long-lasting and dangerous.

As a consequence, the implementation details could leak out. Suppose that you are going to use a car object. Usually, it is only important to you that it has a behavior that accelerates the car; and you are not curious about how it is done. There may be even more internal attributes in the object that contribute to the acceleration process, but there is no valid reason that they should be visible to the consumer logic.

For instance, the amount of the electrical current being delivered to the engine starter could be an attribute, but it should be just private to the object itself. This also holds for certain behaviors that are internal to the object. For example, injecting the fuel into the combustion chamber is an internal behavior that should not be visible and accessible to you, otherwise, you could interfere with that and interrupt the normal process of the engine.

From another point of view, the implementation details (how the car works) vary from one car manufacturer to another but being able to accelerate a car is a behavior that is provided by all car manufacturers. We usually say that being able to accelerate a car is part of the public API or the public interface of the `Car` class.

Generally, the code using an object becomes dependent on the public attributes and behaviors of that object. This is a serious concern. Leaking out an internal attribute by declaring it public at first and then making it private can effectively break the build of the dependent code. It is expected that other parts of the code that are using that attribute as a public thing won't get compiled after the change.

This would mean you've broken the backward compatibility. That's why we choose a conservative approach and make every single attribute private by default until we find sound reasoning for making it public.

To put it simply, exposing private code from a class effectively means that rather than being dependent on a light public interface, we have been dependent on a thick implementation. These consequences are serious and have the potential to cause a lot of rework in a project. So, it is important to keep attributes and behaviors as private as they can be.

The following code box, as part of example 6.3, will demonstrate how we can have private attributes and behaviors in C. The example is about a `List` class that is supposed to store some integer values:

#ifndef EXTREME_C_EXAMPLES_CHAPTER_6_3_H

#define EXTREME_C_EXAMPLES_CHAPTER_6_3_H

#include <unistd.h>

// The attribute structure with no disclosed attribute

struct list_t;

// Allocation function

struct list_t* list_malloc();

// Constructor and destructor functions

void list_init(struct list_t*);

void list_destroy(struct list_t*);

// Public behavior functions

int list_add(struct list_t*, int);

int list_get(struct list_t*, int, int*);

void list_clear(struct list_t*);

size_t list_size(struct list_t*);

void list_print(struct list_t*);

#endif

Code Box 6-13 [ExtremeC_examples_chapter6_3.h]: The public interface of the List class

What you see in the preceding code box is the way that we make the attributes private. If another source file, such as the one that contains the `main` function, includes the preceding header, it'll have no access to the attributes inside the `list_t` type. The reason is simple. The `list_t` is just a declaration without a definition, and with just a structure declaration, you cannot access the fields of the structure. You cannot even declare a variable out of it. This way, we guarantee the information-hiding. This is actually a great achievement.

Once again, before creating and publishing a header file, it is mandatory to double-check whether we need to expose something as public or not. By exposing a public behavior or a public attribute, you'll create dependencies whose breaking would cost you time, development effort, and eventually money.

The following code box demonstrates the actual definition of the `list_t` attribute structure. Note that it is defined inside a source file and not a header file:

#include <stdio.h>

#include <stdlib.h>

#define MAX_SIZE 10

// Define the alias type bool_t

typedef int bool_t;

// Define the type list_t

typedef struct {

size_t size;

int* items;

} list_t;

// A private behavior which checks if the list is full

bool_t __list_is_full(list_t* list) {

return (list->size == MAX_SIZE);


## part 7/7

y money.

The following code box demonstrates the actual definition of the `list_t` attribute structure. Note that it is defined inside a source file and not a header file:

#include <stdio.h>

#include <stdlib.h>

#define MAX_SIZE 10

// Define the alias type bool_t

typedef int bool_t;

// Define the type list_t

typedef struct {

size_t size;

int* items;

} list_t;

// A private behavior which checks if the list is full

bool_t __list_is_full(list_t* list) {

return (list->size == MAX_SIZE);

}

// Another private behavior which checks the index

bool_t __check_index(list_t* list, const int index) {

return (index >= 0 && index <= list->size);

}

// Allocates memory for a list object

list_t* list_malloc() {

return (list_t*)malloc(sizeof(list_t));

}

// Constructor of a list object

void list_init(list_t* list) {

list->size = 0;

// Allocates from the heap memory

list->items = (int*)malloc(MAX_SIZE * sizeof(int));

}

// Destructor of a list object

void list_destroy(list_t* list) {

// Deallocates the allocated memory

free(list->items);

}

int list_add(list_t* list, const int item) {

// The usage of the private behavior

if (__list_is_full(list)) {

return -1;

}

list->items[list->size++] = item;

return 0;

}

int list_get(list_t* list, const int index, int* result) {

if (__check_index(list, index)) {

*result = list->items[index];

return 0;

}

return -1;

}

void list_clear(list_t* list) {

list->size = 0;

}

size_t list_size(list_t* list) {

return list->size;

}

void list_print(list_t* list) {

printf("[");

for (size_t i = 0; i < list->size; i++) {

printf("%d ", list->items[i]);

}

printf("]\n");

}

Code Box 6-14 [ExtremeC_examples_chapter6_3.c]: The definition of the List class

All the definitions that you see in the preceding code box are private. The external logic that is going to use a `list_t` object does not know anything about the preceding implementations, and the header file is the only piece of code that the external code will be dependent on.

Note that the preceding file has not even included the header file! As long as the definitions and function signatures match the declarations in the header file, that's all that's needed. However, it is recommended to do so because it guarantees the compatibility between the declarations and their corresponding definitions. As you've seen in Chapter 2, Compilation and Linking, the source files are compiled separately and finally linked together.

In fact, the linker brings private definitions to the public declarations and makes a working program out of them.

Note:

We can use a different notation for private behavior functions. We use the prefix `__` in their names. As an example, the `__check_index` function is a private function. Note that a private function does not have any corresponding declaration in the header file.

The following code box contains example 6.3's `main` function that creates two list objects, populates the first one, and uses the second list to store the reverse of the first list. Finally, it prints them out:

#include <stdlib.h>

#include "ExtremeC_examples_chapter6_3.h"

int reverse(struct list_t* source, struct list_t* dest) {

list_clear(dest);

for (size_t i = list_size(source) - 1; i >= 0; i--) {

int item;

if(list_get(source, i, &item)) {

return -1;

}

list_add(dest, item);

}

return 0;

}

int main(int argc, char** argv) {

struct list_t* list1 = list_malloc();

struct list_t* list2 = list_malloc();

// Construction

list_init(list1);

list_init(list2);

list_add(list1, 4);

list_add(list1, 6);

list_add(list1, 1);

list_add(list1, 5);

list_add(list2, 9);

reverse(list1, list2);

list_print(list1);

list_print(list2);

// Destruction

list_destroy(list1);

list_destroy(list2);

free(list1);

free(list2);

return 0;

}

Code Box 6-15 [ExtremeC_examples_chapter6_3_main.c]: The main function of example 6.3

As you can see in the preceding code box, we wrote the `main` and `reverse` functions only based on the things declared in the header file. In other words, these functions are using only the public API (or public interface) of the `List` class; the declarations of the attribute structure `list_t` and its behavior functions. This example is a nice demonstration of how to break the dependencies and hide the implementation details from other parts of the code.

Note:

Using the public API, you can write a program that compiles, but it cannot turn into a real working program unless you provide the corresponding object files of the private part and link them together.

There are some points related to the preceding code that we explore in more detail here. We needed to have a `list_malloc` function in order to allocate memory for a `list_t` object. Then, we can use the function `free` to release the allocated memory when we're done with the object.

You cannot use `malloc` directly in the preceding example. That's because if you are going to use `malloc` inside the `main` function, you have to pass `sizeof(list_t)` as the required number of bytes that should be allocated. However, you cannot use `sizeof` for an incomplete type.

The `list_t` type included from the header file is an incomplete type because it is just a declaration that doesn't give any information regarding its internal fields, and we don't know its size while compiling it. The real size will be determined only at link time when we know the implementation details. As a solution, we had to have the `list_malloc` function defined and have `malloc` used in a place where `sizeof(list_t)` is determined.

In order to build example 6.3, we need to compile the sources first. The following commands produce the necessary object files before the linking phase:

$ gcc -c ExtremeC_examples_chapter6_3.c -o private.o

$ gcc -c ExtremeC_examples_chapter6_3_main.c -o main.o

Shell Box 6-1: Compiling example 6.3

As you see, we have compiled the private part into `private.o` and the main part into `main.o`. Remember that we don't compile header files. The public declarations in the header are included as part of the `main.o` object file.

Now we need to link the preceding object files together, otherwise `main.o` alone cannot turn into an executable program. If you try to create an executable file using only `main.o`, you will see the following errors:

$ gcc main.o -o ex6_3.out

main.o: In function 'reverse':

ExtremeC_examples_chapter6_3_main.c:(.text+0x27): undefined reference to 'list_clear'

...

main.o: In function 'main':

ExtremeC_examples_chapter6_3_main.c:(.text+0xa5): undefined reference to 'list_malloc'

... collect2: error: ld returned 1 exit status

$

Shell Box 6-2: Trying to link example 6.3 by just providing main.o

You see that the linker cannot find the definitions of the functions declared in the header file. The proper way to link the example is as follows:

$ gcc main.o private.o -o ex6_3.out

$ ./ex6_3.out

[4 6 1 5 ]

[5 1 6 4 ]

$

Shell Box 6-3: Linking and running example 6.3

What happens if you change the implementation behind the `List` class?

Say, instead of using an array, you use a linked list. It seems that we don't need to generate the `main.o` again, because it is nicely independent of the implementation details of the list it uses. So, we need only to compile and generate a new object file for the new implementation; for example, `private2.o`. Then, we just need to relink the object files and get the new executable:

$ gcc main.o private2.o -o ex6_3.out

$ ./ex6_3.out

[4 6 1 5 ]

[5 1 6 4 ]

$

Shell Box 6-4: Linking and running example 6.3 with a different implementation of the List class

As you see, from the user's point of view, nothing has changed, but the underlying implementation has been replaced. That is a great achievement and this approach is being used heavily in C projects.

What if we wanted to not repeat the linking phase in case of a new list implementation? In that case, we could use a shared library (or `.so` file) to contain the private object file. Then, we could load it dynamically at runtime, removing the need to relink the executable again. We have discussed shared libraries as part of Chapter 3, Object Files.

Here, we bring the current chapter to an end and we will continue our discussion in the following chapter. The next two chapters will be about the possible relationships which can exist between two classes.

# Summary

In this chapter, the following topics have been discussed:

- We gave a thorough explanation of object-orientation philosophy and how you can extract an object model from your mind map.
- We also introduced the concept of the domain and how it should be used to filter the mind map to just keep relevant concepts and ideas.
- We also introduced the attributes and behaviors of a single object and how they should be extracted from either the mind map or the requirements given in the description of a domain.
- We explained why C cannot be an OOP language and explored its role in the translation of OOP programs into low-level assembly instructions that eventually will be run on a CPU.
- Encapsulation, as the first principle in OOP, was discussed. We use encapsulation to create capsules (or objects) that contain a set of attributes (placeholders for values) and a set of behaviors (placeholders for logic).
- Information-hiding was also discussed, including how it can lead to interfaces (or APIs) that can be used without having to become dependent on the underlying implementation.
- While discussing information-hiding, we demonstrated how to make attributes or methods private in C code.

The next chapter will be the opening to the discussion regarding possible relations between classes. We start Chapter 7, Composition, and Aggregation, with talking about composition relationship and then, we continue with inheritance and polymorphism as part of Chapter 8, Inheritance and Polymorphism.


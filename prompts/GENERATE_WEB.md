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

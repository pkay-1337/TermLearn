# termlearn TUI Redesign Specification
**"Elegance in the Terminal" — Modern, Responsive, Theme-Driven Textual Architecture**

- **Document Version**: 1.0.0
- **Applies to**: `termlearn` v0.7.0+
- **Status**: Draft / Proposed Specification
- **Engine**: Textual 0.50+ / 1.0+ on Python 3.11+
- **Standards & Baselines**: RFC 2119, IEEE Std 29148-2018, `docs/SRS.md` (§6.2 `IF-TUI-001..006`, §7.3 `NFR-USE-001..004`)
- **Location**: `~/Apps/termlearn/docs/TUI_REDESIGN_SPEC.md`

---

## 1. Executive Summary & Design Vision

The initial v0.6.0 Textual implementation proved the architectural premise: Textual can drive native interactive loops over shared `lib/` scoring, persistence, and toolchains without touching the underlying YAML packs or SQLite schemas. However, visually and ergonomically, the v0.6.0 TUI is a barebones, unstyled functional wireframe. It suffers from:

1. **Zero Styling**: No custom CSS/TCSS exists; it relies on drab default browser-fallback widgets.
2. **Flat Layouts**: Monolithic single-column scrolling containers dump raw strings into unpadded screens.
3. **Absence of Visual Metaphors**: Flashcards look like plain debug text (`Q: ... / A: ...`); labs look like unformatted text dumps rather than an integrated coding workspace; the chapter menu is an uninspiring 8-item list.
4. **Poor Spatial Hierarchy**: No card framing, no status badges, no progress bars, and no visual depth.

### The Vision
Transform `termlearn` into a **world-class terminal product** that rivals modern developer tools like *lazygit*, *btop*, *k9s*, and *glow*. The experience must feel snappy, focused, beautiful, and tactile—turning technical learning into a high-satisfaction terminal experience.

---

## 2. Art Direction & Theme System

### 2.1 The "Catppuccin Mocha Aurora" Palette

The UI is anchored by a curated, APCA-contrast-tested modern dark palette.

```
┌────────────────────────────────────────────────────────────────────────┐
│ Catppuccin Mocha Aurora Palette                                        │
├──────────────────┬───────────┬─────────────────────────────────────────┤
│ Role             │ Hex Value │ Description / Usage                     │
├──────────────────┼───────────┼─────────────────────────────────────────┤
│ $crust           │ #11111b   │ Deep background / Window canvas         │
│ $mantle          │ #181825   │ Sidebar / Navigation background         │
│ $base            │ #1e1e2e   │ Standard card / Panel background        │
│ $surface-0       │ #313244   │ Borders, inactive dividers              │
│ $surface-1       │ #45475a   │ Inactive button / Elevated container    │
│ $surface-2       │ #585b70   │ Active selection / Hovered border       │
│ $accent-primary  │ #89b4fa   │ Sapphire Blue: Primary focus / Titles   │
│ $accent-secondary│ #cba6f7   │ Mauve: Chapter badges / Concept tags    │
│ $accent-cyan     │ #89dceb   │ Sky: Interactive prompts & hotkeys      │
│ $status-success  │ #a6e3a1   │ Emerald: Correct, PASS, Mastered (>=80%)│
│ $status-warning  │ #f9e2af   │ Amber: Review due, Hints, Warning (50%) │
│ $status-danger   │ #f38ba8   │ Coral: Wrong, FAIL, Errors, Low mastery │
│ $text-primary    │ #cdd6f4   │ High-contrast foreground text           │
│ $text-muted      │ #6c7086   │ Captions, hotkey explanations           │
└──────────────────┴───────────┴─────────────────────────────────────────┘
```

### 2.2 Depth & Border Hierarchy
* **Level 0 (Canvas)**: Background `$crust`, no border.
* **Level 1 (Panels & Cards)**: Background `$base`, border `round $surface-0`.
* **Level 2 (Focused / Active Item)**: Background `$base`, border `heavy $accent-primary` or `$accent-cyan`, subtle header badge highlight.
* **Level 3 (Modal Overlays)**: Background `$surface-1`, border `double $accent-secondary`, shadowed backdrop (`background: rgba(17, 17, 27, 0.7)`).

### 2.3 Accessibility & Terminal Fallback Rules
* Conforms strictly to **`IF-CLI-007`** and **`IF-TUI-006`**:
  * If `NO_COLOR` is set or terminal lacks truecolor, the stylesheet collapses gracefully into standard 16-color ANSI with zero loss of contrast.
  * Meaning is **never conveyed by color alone**: every success/failure, grade, or status incorporates explicit text and Unicode signifiers (`✔ PASS`, `✖ FAIL`, `● DUE`, `★ MASTERED`).

---

## 3. Structural Layout Architecture

### 3.1 Global Application Shell

```
┌────────────────────────────────────────────────────────────────────────┐
│  termlearn ── Fluent C  ›  Ch.04 Pointers  ›  Study         [?] Help   │ ← AppHeader
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│                                                                        │
│                       SCREEN WORKSPACE VIEWPORT                        │
│                                                                        │
│                                                                        │
├────────────────────────────────────────────────────────────────────────┤
│  [n] Next   [p] Prev   [r] Run   [?] Help   [q] Back      termlearn v0.7│ ← AppFooter
└────────────────────────────────────────────────────────────────────────┘
```

* **AppHeader**:
  * Left: Styled branding (`termlearn` in bold cyan), followed by a dynamic breadcrumb trail showing current book and chapter.
  * Right: Context badge (e.g. `[Review Due: 3]` or `[Score: 4/5]`) and quick `[?] Help` indicator.
* **AppFooter**:
  * Shows contextual hotkeys formatted as visual "key pills" (`[r] Run`, `[f] Flip`, `[1-4] Grade`).
  * Right: Compact version label.

---

## 4. Comprehensive Screen Specifications

### 4.1 Home Screen: The Library Dashboard

Replace the single vertical `OptionList` with a **Dual-Pane Master-Detail Dashboard**.

```
┌──────────────────────────────────┬─────────────────────────────────────┐
│ 📚 YOUR LIBRARY                  │ 📖 BOOK DETAILS                     │
├──────────────────────────────────┼─────────────────────────────────────┤
│  ▶ fluent-c                      │  Fluent C                           │
│    By: Dan Saks                  │  Author: Dan Saks                   │
│    [4/4 Chapters]  [██████░░] 75%│  Source: books/fluent-c/source.epub │
│                                  │  Toolchain: gcc (C99)               │
│    extreme-c                     ├─────────────────────────────────────┤
│    By: Kamran Amini              │  Mastery: 75% (3 of 4 Mastered)     │
│    [6/12 Chapters] [███░░░░░] 33%│  SRS Due: 5 Cards Due Today         │
│                                  │                                     │
│    network-programming           │  Chapters:                          │
│    By: Lewis Van Winkle          │  • ch01: Intro to C                 │
│    [0/8 Chapters]  [NEW BOOK]    │  • ch02: Data Types                 │
│                                  │  • ch03: Pointers & Addresses  [★]  │
│                                  │  • ch04: Memory Management     [★]  │
│                                  ├─────────────────────────────────────┤
│                                  │  [ Enter ] Open Chapter Browser     │
└──────────────────────────────────┴─────────────────────────────────────┘
```

* **Left Pane (`#book-list`)**:
  * Preserves `#book-list` ID for automated test compatibility (`VR-009`).
  * Custom option rendering with clean metadata cards: slug, truncated author list, pack completeness pill badge, and a visual ASCII mastery gauge.
* **Right Pane (`#book-details`)**:
  * Reactively updates on selection change.
  * Displays full metadata, toolchain prerequisites, chapter breakdown, and quick stats.

---

### 4.2 Chapters Screen: The Curriculum Roadmap

```
┌──────────────────────────────────┬─────────────────────────────────────┐
│ 🗺️ CHAPTERS: fluent-c            │ 📑 CHAPTER OVERVIEW                 │
├──────────────────────────────────┼─────────────────────────────────────┤
│  ● ch01: Introduction      [PASS]│  Chapter 04: Pointers & Addresses   │
│  │                               │  Source: Ch.4 pp. 45–72             │
│  ● ch02: Arrays & Memory   [PASS]│  Level: Core                        │
│  │                               ├─────────────────────────────────────┤
│  ▶ ch03: Pointer Basics    [STUDY│  Learning Objectives:               │
│  │  ↳ Due: 3  ·  Lab: PASS       │  ✔ Understand pointer arithmetic    │
│  │                               │  ✔ Distinguish stack vs heap addr   │
│  ○ ch04: Dynamic Alloc     [NEW] │  ✔ Diagnose dangling pointer bugs   │
│                                  ├─────────────────────────────────────┤
│                                  │  Status: STUDYING                   │
│                                  │  SRS Cards Due: 3                   │
│                                  │  Lab Status: PASS (Snapshot #4f2a)  │
│                                  ├─────────────────────────────────────┤
│                                  │  [ Enter ] Open Chapter Action Menu │
└──────────────────────────────────┴─────────────────────────────────────┘
```

* **Visual Roadmap Tree**: Visual connected node markers (`●` completed, `▶` current, `○` upcoming) showing learning progression.
* **Status Badges**:
  * `[MASTERED]` in bold green (`$status-success`).
  * `[STUDYING]` in vibrant cyan (`$accent-cyan`).
  * `[NEW]` in muted purple (`$accent-secondary`).
  * `[NO PACK]` in dimmed grey with a tooltip: *"Run gen-prompt first"*.

---

### 4.3 Chapter Menu: The Mission Command Deck

Instead of a plain 8-line list, organize modes into a **Categorized Action Grid**.

```
┌────────────────────────────────────────────────────────────────────────┐
│ 🎯 CHAPTER 04: POINTERS & ADDRESSES                                    │
│ Pick an activity to begin:                                             │
├────────────────────────────────────────────────────────────────────────┤
│  [1] 📖 STUDY (Walkthrough)         │  [2] 📝 REVISE (Summary Notes)   │
│  Step-by-step concepts with inline  │  Condensed review notes, code     │
│  formative checks & memory steppers │  examples & common bugs list.     │
│  Status: 4 of 5 blocks completed    │  No scoring or evaluation.        │
├─────────────────────────────────────┼──────────────────────────────────┤
│  [3] ⚡ QUIZ & CHECKS               │  [4] 🧩 PARSONS PROBLEMS          │
│  Conceptual checks, output traces   │  Scrambled code puzzle exercises  │
│  and bug diagnostic questions.      │  with distractor elimination.     │
│  Best Score: 85%                    │  Mastery: 3 / 3 Solved            │
├─────────────────────────────────────┼──────────────────────────────────┤
│  [5] 💻 CODE LAB                    │  [6] 🏆 CHAPTER TEST (Gate)       │
│  Interactive coding challenge with  │  Prove chapter mastery against    │
│  compiler runs & hidden test suite. │  strict quiz & lab gate criteria. │
│  Current Lab: PASS                  │  Status: READY TO ATTEMPT         │
├─────────────────────────────────────┼──────────────────────────────────┤
│  [7] 🗂️ FLASHCARDS (SRS)            │  [8] 📊 CHAPTER ANALYTICS         │
│  Spaced repetition card deck for    │  Accuracy rates, concept mastery  │
│  long-term memory retention.        │  breakdown & weakest areas.       │
│  Queue: 3 Cards Due Today           │  Weakest Concept: Address-Of (&)  │
└────────────────────────────────────────────────────────────────────────┘
```

* Hotkeys `1-8` immediately activate the tile.
* Tiles feature subtle hover glow and border transitions.
* Displays live progress stats right inside each tile.

---

### 4.4 Study Mode: The Distraction-Free Focus Reader

```
┌────────────────────────────────────────────────────────────────────────┐
│ 📖 STUDY: Fluent C › Ch.04 › Block 2 of 5: Pointer Arithmetic           │
│ Progress: [██████████████░░░░░░░░░░░░░░] 40%                           │
├────────────────────────────────────────────────────────────────────────┤
│ 💡 Mental Model & Exposition                                           │
│                                                                        │
│ Pointers advance by increments of `sizeof(*ptr)` bytes rather than raw │
│ single bytes. Adding 1 to an `int*` on a 64-bit architecture advances  │
│ the memory address by 4 bytes.                                         │
│                                                                        │
│ ┌─ Example (C99) ────────────────────────────────── [r: Run Code] ───┐ │
│ │ 1 │ int arr[3] = {10, 20, 30};                                     │ │
│ │ 2 │ int *p = arr;                                                  │ │
│ │ 3 │ printf("p=%p, p+1=%p (diff=%ld)\n",                            │ │
│ │ 4 │        (void*)p, (void*)(p+1), (char*)(p+1) - (char*)p);       │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ┌─ Memory Stepper (Step 1/2) ────────────────────────── [n: Next] ───┐ │
│ │  arr: [ 0x1000: 10 ]  [ 0x1004: 20 ]  [ 0x1008: 30 ]               │ │
│ │  p:   ^ points to 0x1000                                           │ │
│ └────────────────────────────────────────────────────────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│  [n] Next Step / Advance     [p] Prev Block     [r] Run Code     [q] Back
└────────────────────────────────────────────────────────────────────────┘
```

* **Component Structure**:
  * **Exposition Box**: Markdown rendered with elegant typographics.
  * **Code Container**: Dedicated border, line numbers, syntax highlighting (Monokai / Catppuccin), and a top-right action badge `[r: Run Code]`.
  * **Visualizer Box (`ascii-viz`)**: Distinct dashed/round border, step indicator dots (`● ○ ○`), and clear memory diagram presentation.
  * **Inline Question Transition**: When advancing to checks, the question mounts smoothly inside the card frame with zero layout snapping.

---

### 4.5 Quiz & Question Widgets: Tactile Assessment

#### Multiple Choice / Predict / Why-Fails
```
┌────────────────────────────────────────────────────────────────────────┐
│ ⚡ QUESTION 3 / 8                                  [concept: ptr-arith] │
├────────────────────────────────────────────────────────────────────────┤
│ What is printed by line 4?                                             │
│                                                                        │
│ ┌─ Snippet ──────────────────────────────────────────────────────────┐ │
│ │ int a[2] = {5, 9};                                                 │ │
│ │ int *p = a;                                                        │ │
│ │ printf("%d\n", *(p + 1));                                          │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ Select an option:                                                      │
│                                                                        │
│   (1) 5                                                                │
│   (2) 9                                                                │
│   (3) The memory address of a[1]                                       │
│   (4) Undefined behavior                                               │
│                                                                        │
├────────────────────────────────────────────────────────────────────────┤
│ ✔ CORRECT!                                                             │
│ Why: `p + 1` evaluates to the address of `a[1]`. Dereferencing with    │
│ `*` yields the value stored at that address, which is 9.               │
│                                                                        │
│ [ Next Question (n) ]                                                  │
└────────────────────────────────────────────────────────────────────────┘
```

* **Option Cards**:
  * Instead of standard full-width plain grey buttons, options are styled as clean, selectable cards with clear number chips `(1)`, `(2)`.
  * Keyboard numbers `1-4` or mouse click trigger the selection.
* **Feedback Banner**:
  * Success: Deep green card (`$status-success`) with a clear `✔ CORRECT` badge and formatted `why` text.
  * Error: Crimson card (`$status-danger`) with an `✖ NOT QUITE` badge, stating what went wrong and highlighting misconceptions.
  * Focus immediately transitions to the `[ Next Question (n) ]` button so pressing `n` or Enter effortlessly advances.

---

### 4.6 Cards Screen: The Skeuomorphic Flashcard Deck

```
┌────────────────────────────────────────────────────────────────────────┐
│ 🗂️ SPACED REPETITION DECK — Fluent C             Card 3 of 8 Due Today  │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│           ╭───────────────────────────────────────────────╮            │
│           │ 🏷️ CONCEPT: stack-vs-heap                     │            │
│           │                                               │            │
│           │  What happens to a stack-allocated variable   │            │
│           │  when its enclosing function returns?         │            │
│           │                                               │            │
│           │                                               │            │
│           │                                               │            │
│           │                        [f] Flip Card to Reveal│            │
│           ╰───────────────────────────────────────────────╯            │
│                                                                        │
├────────────────────────────────────────────────────────────────────────┤
│  [f] Flip Card            [e] Edit Card Text            [q] Back / Quit
└────────────────────────────────────────────────────────────────────────┘
```

#### Flipped State (Answer Revealed & Grading Deck)
```
┌────────────────────────────────────────────────────────────────────────┐
│ 🗂️ SPACED REPETITION DECK — Fluent C             Card 3 of 8 Due Today  │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│           ╭───────────────────────────────────────────────╮            │
│           │ 💡 ANSWER                                     │            │
│           │                                               │            │
│           │  Its storage duration ends; its stack frame   │            │
│           │  is reclaimed. Accessing it thereafter is     │            │
│           │  undefined behavior (dangling pointer).       │            │
│           │                                               │            │
│           │                                               │            │
│           ╰───────────────────────────────────────────────╯            │
│                                                                        │
│ Rate your recall:                                                      │
│                                                                        │
│  [1] Again (<10m)    [2] Hard (1d)    [3] Good (3d)    [4] Easy (6d)   │
│     (Coral Red)        (Amber)          (Sapphire)       (Emerald)     │
│                                                                        │
├────────────────────────────────────────────────────────────────────────┤
│  [1-4] Grade Card         [e] Edit Card Text            [q] Back / Quit
└────────────────────────────────────────────────────────────────────────┘
```

* **Physical Card Feel**: Fixed width (`64 cols`), fixed height (`14 lines`), centered horizontally and vertically within the canvas.
* **4-Tier Color-Coded Recall Buttons**:
  * `[1] Again`: Coral Red (`#f38ba8`)
  * `[2] Hard`: Warm Amber (`#f9e2af`)
  * `[3] Good`: Sapphire Blue (`#89b4fa`)
  * `[4] Easy`: Emerald Green (`#a6e3a1`)
* Shows the next calculated SM-2 interval right on the button labels.

---

### 4.7 Lab Screen: The Terminal Mini-IDE

Replace the vertical stack of inputs and buttons with a **Dual-Pane Integrated Developer Environment**.

```
┌──────────────────────────────────┬─────────────────────────────────────┐
│ 📝 LAB: Dynamic Vector           │ 💻 CODE EDITOR (starter.c)          │
├──────────────────────────────────┤                                     │
│ Prompt:                          │ 1 │ #include <stdio.h>              │
│ Implement `vector_push` to       │ 2 │ #include <stdlib.h>             │
│ double capacity when `len == cap`│ 3 │                                 │
│                                  │ 4 │ void vector_push(Vec *v, int x)│
│ Expected:                        │ 5 │ {                               │
│ Output: "vec[3]=40 cap=4"        │ 6 │     /* TODO: implement */       │
│                                  │ 7 │ }                               │
│ ┌─ Hints (1 of 3) [h: Next] ───┐ │                                     │
│ │ Use realloc(v->data, ...);   │ │                                     │
│ └──────────────────────────────┘ │                                     │
├──────────────────────────────────┴─────────────────────────────────────┤
│ 🖥️ CONSOLE OUTPUT                                                      │
│ [▶ Run Output]   [🧪 Hidden Test Suite]                                │
├────────────────────────────────────────────────────────────────────────┤
│ Status: ✔ Compiled in 34ms | Exit: 0                                   │
│ vec[0]=10 cap=2                                                        │
│ vec[1]=20 cap=2                                                        │
│ vec[2]=30 cap=4                                                        │
│ vec[3]=40 cap=4                                                        │
├────────────────────────────────────────────────────────────────────────┤
│  [r] Run Code   [t] Submit to Hidden Tests   [h] Hint   [q] Back
└────────────────────────────────────────────────────────────────────────┘
```

* **Top Left**: Task instruction panel, prompt details, and expandable hints widget.
* **Top Right**: Syntax-highlighted `TextArea` code editor with line numbers and active cursor line highlighting.
* **Bottom Panel**: Terminal execution console displaying stdout, stderr, compile diagnostics, and hidden test pass/fail results with instant diff visualization.
* **Toolbar Actions**: Sleek key-pill buttons for Run, Test, and Hint.

---

### 4.8 Stats Screen: Learning Analytics Dashboard

```
┌────────────────────────────────────────────────────────────────────────┐
│ 📊 LEARNING ANALYTICS — Fluent C                                       │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ OVERALL MASTERY ─┐ ┌─ SRS CARDS DUE ─┐ ┌─ CURRENT STREAK ─┐ ┌─ ACCURACY ──┐ │
│ │       78%         │ │     5 Cards     │ │     3 Days       │ │     86%     │ │
│ │  3 of 4 Chapters  │ │  Ready to review│ │  Keep it going!  │ │ 42/49 checks│ │
│ └───────────────────┘ └─────────────────┘ └──────────────────┘ └─────────────┘ │
│                                                                        │
│ 📋 Chapter Mastery Breakdown                                           │
│ ┌────────────────────────────────────────────────────────────────────┐ │
│ │ Chapter              │ Blocks │ Accuracy │ Progress       │ Status │ │
│ ├──────────────────────┼────────┼──────────┼────────────────┼────────┤ │
│ │ ch01: Introduction   │ 4 / 4  │ 92%      │ [██████████]   │ MASTER │ │
│ │ ch02: Arrays         │ 5 / 5  │ 88%      │ [█████████░]   │ MASTER │ │
│ │ ch03: Pointers       │ 6 / 6  │ 74%      │ [███████░░░]   │ STUDY  │ │
│ │ ch04: Memory Mgmt    │ 2 / 5  │ 60%      │ [██████░░░░]   │ STUDY  │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ⚠️ Concept Weak Spots (Accuracy < 75%)                                  │
│ • pointer-arithmetic  (Accuracy: 50%  —  2/4 hits)  ›  Review in ch03  │
│ • stack-allocation    (Accuracy: 60%  —  3/5 hits)  ›  Review in ch04  │
├────────────────────────────────────────────────────────────────────────┤
│  [r] Reset Progress        [?] Help        [q] Back to Chapter Menu    │
└────────────────────────────────────────────────────────────────────────┘
```

* **Metric KPI Cards**: Prominent 4-card KPI summary header.
* **Progress Bar Tables**: Unicode progress bars inside the DataTable (`[████████░░]`).
* **Weak Concept Highlighting**: Direct actionable pointers indicating which chapter and block to revisit to fix weaknesses.

---

## 5. TCSS Architecture & Stylesheet Specification

To implement this design, a dedicated stylesheet `tui/style.tcss` is introduced and linked into `LearnApp.CSS_PATH`.

### 5.1 CSS Hierarchy & Class Tokens

```css
/* ==========================================================================
   termlearn — Master TCSS Stylesheet
   Theme: Catppuccin Mocha Aurora
   ========================================================================== */

/* Color Tokens */
$crust: #11111b;
$mantle: #181825;
$base: #1e1e2e;
$surface-0: #313244;
$surface-1: #45475a;
$surface-2: #585b70;

$accent-primary: #89b4fa;
$accent-secondary: #cba6f7;
$accent-cyan: #89dceb;

$status-success: #a6e3a1;
$status-warning: #f9e2af;
$status-danger: #f38ba8;

$text-primary: #cdd6f4;
$text-muted: #6c7086;

/* Screen Layout Base */
Screen {
    background: $crust;
    color: $text-primary;
}

/* Master Header & Footer */
Header {
    dock: top;
    height: 1;
    background: $mantle;
    color: $accent-cyan;
    text-style: bold;
}

Footer {
    dock: bottom;
    height: 1;
    background: $mantle;
    color: $text-muted;
}

/* Base Panel & Card Containers */
.card-panel {
    background: $base;
    border: round $surface-0;
    padding: 1 2;
    margin: 1;
}

.card-panel:focus-within {
    border: round $accent-primary;
}

/* Split Pane Layouts */
.master-detail-container {
    layout: horizontal;
    height: 1fr;
}

.sidebar-pane {
    width: 38%;
    background: $mantle;
    border-right: vline $surface-0;
    padding: 1;
}

.content-pane {
    width: 62%;
    background: $base;
    padding: 1 2;
}

/* Action Grid (Chapter Menu) */
.menu-grid {
    layout: grid;
    grid-size: 2 4;
    grid-gutter: 1;
    padding: 1;
}

.menu-tile {
    background: $base;
    border: round $surface-0;
    padding: 1 2;
    height: 100%;
}

.menu-tile:hover, .menu-tile:focus {
    border: round $accent-cyan;
    background: $surface-0;
}

/* Flashcard SRS */
.flashcard-outer {
    align: center middle;
    height: 1fr;
}

.flashcard-box {
    width: 68;
    height: 16;
    background: $base;
    border: heavy $accent-primary;
    padding: 1 3;
}

.flashcard-flipped {
    border: heavy $accent-secondary;
}

/* Grading Deck */
.grade-bar {
    layout: horizontal;
    align: center middle;
    margin-top: 1;
    height: 3;
}

.btn-again {
    background: $status-danger;
    color: $crust;
    text-style: bold;
    margin-right: 1;
}

.btn-hard {
    background: $status-warning;
    color: $crust;
    text-style: bold;
    margin-right: 1;
}

.btn-good {
    background: $accent-primary;
    color: $crust;
    text-style: bold;
    margin-right: 1;
}

.btn-easy {
    background: $status-success;
    color: $crust;
    text-style: bold;
}

/* Lab Split Workspace */
.lab-split-top {
    layout: horizontal;
    height: 60%;
}

.lab-split-bottom {
    height: 40%;
    background: $mantle;
    border-top: hline $surface-0;
    padding: 1;
}

.lab-prompt {
    width: 40%;
    border-right: vline $surface-0;
    padding: 1;
}

.lab-editor {
    width: 60%;
}

/* Feedback Callouts */
.feedback-box {
    padding: 1 2;
    margin: 1 0;
    border: round $surface-0;
}

.feedback-success {
    background: #1e3a29;
    border: round $status-success;
    color: $status-success;
}

.feedback-error {
    background: #3e2025;
    border: round $status-danger;
    color: $status-danger;
}
```

---

## 6. Technical Invariants & Verification Contract

### 6.1 Strict Invariant Preservation
To guarantee that existing automated tests in `tests/test_tui.py` (and test requirements `VR-009`) continue to pass without regression:

1. **DOM ID Preservation**:
   * `#book-list` remains an `OptionList` widget on `HomeScreen`.
   * `#ch-list` remains an `OptionList` widget on `ChaptersScreen`.
   * `#mode-list` remains an `OptionList` widget on `ChapterMenu`.
   * `#body` remains a `Vertical` container on `StudyScreen`, `QuizScreen`, and `CardsScreen`.
   * `#order-in`, `#fill-in`, and `#micro-in` remain the IDs of the `Input` controls in `QuestionWidget`.
   * `#feedback` remains a `Static` widget inside `QuestionWidget`.
   * `#lab-out` remains a `Static` widget in `LabScreen`.
2. **Keyboard Mapping & Binding Invariants**:
   * All single-letter shortcuts (`r`, `e`, `h`, `s`, `n`, `p`, `f`, `1-4`, `q`, `?`) continue to trigger identical underlying actions.
   * `?` continues to open `HelpModal`; `Esc` or `q` continues to dismiss it.
3. **Data Independence**:
   * The TUI remains strictly read-only with respect to pack files (`packs/**/*.yaml`).
   * SQLite operations continue to route strictly through `lib/progress.py` and `lib/srs.py`.

---

## 7. Phased Implementation Roadmap

* **Phase 1: Foundation & Theming**
  * Create `tui/style.tcss` with the complete Catppuccin Mocha Aurora color variables, layout rules, and component styles.
  * Integrate `style.tcss` into `LearnApp` in `tui/app.py`.
* **Phase 2: Master-Detail Dashboards (Home, Chapters, ChapterMenu)**
  * Update `HomeScreen` with two-column layout (`#book-list` + details preview).
  * Update `ChaptersScreen` with roadmap progress badges.
  * Update `ChapterMenu` with categorized tiles while retaining `#mode-list`.
* **Phase 3: Core Interactive Learning (Study, Quiz, Cards)**
  * Redesign `QuestionWidget` option cards and feedback callout banners.
  * Implement the physical centered card container and 4-color recall deck on `CardsScreen`.
  * Style code syntax blocks and memory stepper frames in `StudyScreen`.
* **Phase 4: Workspace & Analytics (Lab, Stats, Test)**
  * Build the dual-pane Lab layout (Task & hints on left, Code editor on right, Console below).
  * Build the 4-card KPI summary header and styled progress tables in `StatsScreen`.
* **Phase 5: Verification & Polish**
  * Execute `pytest` ensuring 100% green tests on `tests/test_tui.py` (`VR-009`).
  * Run interactive pilot testing across all modes.

---

*Authored for the `termlearn` project.*

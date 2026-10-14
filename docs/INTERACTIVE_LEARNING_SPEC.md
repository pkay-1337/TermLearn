# Language-Agnostic Interactive Learning & Pluggable Runner Specification
**Document ID:** SPEC-PED-001 / SPEC-RUNNER-002  
**Target Subsystems:** `docs/SRS.md`, `lib/pack.py`, `lib/lab.py`, `lib/ai_prompt.py`, `tui/widgets.py`, `tui/practice.py`, `tui/screens.py`, `tui/style.tcss`  
**Status:** APPROVED  
**Applies to:** `termlearn` v0.8.0+  
**Standards & Baselines:** RFC 2119, IEEE Std 29148-2018, `docs/SRS.md` (§4.6–§4.9, §5.1, §6.2)  
**Date:** October 2026  

---

## 1. Executive Summary & Educational Rationale

### 1.1 The Limitations of Static Text in Systems Education
`termlearn`'s foundation incorporates proven cognitive science principles: active recall, spaced repetition (SM-2), and Parsons ordering problems. However, in low-level systems programming, software architecture, and tooling, learners repeatedly confront conceptual bottlenecks that static Markdown text and simple multiple-choice questions cannot resolve:

1. **The "Notional Machine" Visibility Deficit (Sorva, 2013; Lister, 2004)**:
   - When learning pointers, memory allocation, variable lifetimes, or register passing, learners struggle because the underlying machine state is completely invisible.
   - Predicting final output (`stdout`) fails to assess whether the learner possessed an accurate intermediate mental model of memory mutations.
2. **The "Blank Slate" Cognitive Cliff (Sweller, 1988; Renkl, 2002)**:
   - Jumping from 4-line multiple choice or ordering questions directly to authoring full C/Rust/Python modules in an editor induces excessive extraneous cognitive load.
   - Learners need **faded scaffolding** (Ericson, 2022) that bridges ordering pre-written logic with active code synthesis.
3. **The Diagnostic Debugging Gap (Kalyuga et al.)**:
   - Real-world programming requires diagnosing compiler warnings, sanitizer errors (`AddressSanitizer`), core dumps, and stack traces. Standard tutorials rarely train this skill formatively.
4. **Cognitive Chunking in Complex Code (Margulieux & Catrambone, 2016)**:
   - Novices perceive multi-line code examples as monolithic walls of syntax. Subgoal labels explicitly chunk code into purposeful functional steps, improving problem-solving transfer by up to 40%.
5. **Authentic Toolchain Immersion (Collins et al., Cognitive Apprenticeship)**:
   - The terminal is a live runtime environment with access to symbols, disassembly, and static analysis. Learners should be able to inspect the machine's perspective on their code on demand.

### 1.2 The Language-Agnostic Imperative
`termlearn` is designed for any programming language, shell, or systems tool (C, Rust, Python, Go, Zig, SQL, Docker). Therefore, interactive features **MUST NOT** be hardcoded to any single compiler or toolchain:
- **Declarative Interactions (P1–P4)**: Driven entirely by portable YAML schemas in the course packs. Zero host compiler required; runs seamlessly on mobile devices (Termux) and minimal environments.
- **Dynamic Inspections (P5)**: Driven by the **Pluggable Runner Protocol**, where the AI authors a per-book runner script defining standardized execution verbs.

---

## 2. Pluggable Runner Protocol (Normative Extension to SRS §4.9)

### 2.1 The Extended Protocol Verbs
In addition to the mandatory `RUNNER-CHECK` (`run check <src>`) and `RUNNER-EXEC` (`run exec <src> --expect <file>`), generated runners at `packs/<slug>/<toolchain.runner>` **MAY** implement the following standardized verbs:

```
┌────────────────────────────────────────────────────────────────────────┐
│ Pluggable Runner Verbs                                                 │
├─────────────────┬──────────────────────────────────┬───────────────────┤
│ Verb            │ Invocation                       │ Status            │
├─────────────────┼──────────────────────────────────┼───────────────────┤
│ RUNNER-VERBS    │ run verbs                        │ RECOMMENDED       │
│ RUNNER-CHECK    │ run check <src>                  │ REQUIRED          │
│ RUNNER-EXEC     │ run exec <src> --expect <f> ...  │ REQUIRED          │
│ RUNNER-INSPECT  │ run inspect <src> --mode <m>     │ OPTIONAL          │
│ RUNNER-LINT     │ run lint <src>                   │ OPTIONAL          │
└─────────────────┴──────────────────────────────────┴───────────────────┘
```

1. `RUNNER-VERBS`:
   - Invocation: `run verbs`
   - Output: Exactly one JSON object to stdout:
     ```json
     {"verbs": ["check", "exec", "inspect", "lint"]}
     ```
   - Behavior: If `verbs` is not implemented or exits non-zero, the app defaults to assuming only `["check", "exec"]` are available.

2. `RUNNER-INSPECT`:
   - Invocation: `run inspect <source-file> --mode <symbols|disasm|sections|ast>`
   - Output: Exactly one JSON object to stdout:
     ```json
     {
       "ok": true,
       "mode": "disasm",
       "format": "asm",
       "content": "0000000000001149 <car_accelerate>:\n  1149: 55    push rbp\n..."
     }
     ```
   - On error: `{"ok": false, "diagnostics": "objdump failed: ..."}`.
   - Language Agnosticism:
     - For C: `symbols` runs `nm -C`; `disasm` runs `objdump -d -M intel`; `sections` runs `readelf -S`.
     - For Python: `ast` runs `python3 -m ast`; `disasm` runs `python3 -m dis`.
     - For Rust: `symbols` runs `cargo nm`; `disasm` runs `cargo objdump -- -d`.
     - For SQL/Docker: `inspect` can return parsed query plans (`EXPLAIN`) or container layer metadata.

3. `RUNNER-LINT`:
   - Invocation: `run lint <source-file>`
   - Output: Exactly one JSON object to stdout:
     ```json
     {
       "ok": true,
       "diagnostics": [
         {"line": 12, "col": 5, "severity": "warning", "message": "variable 'x' set but not used"}
       ]
     }
     ```

### 2.2 Built-in Pilot Fallback
When a pack does not declare a `toolchain.runner` and `example.lang == 'c'`, the system provides a built-in fallback for `RUNNER-INSPECT` using host `gcc`, `nm`, `objdump`, and `readelf`. If these utilities are absent, the UI gracefully informs the user without throwing exceptions.

---

## 3. The 5 Interactive Learning Innovations

### 3.1 P1: Memory & State Trace Checks (`kind: trace`)

#### 3.1.1 Purpose
Forces the learner to mentally trace intermediate runtime state (variables, memory addresses, pointer dereferences, stack frames, or register contents) step-by-step through execution rather than only guessing final stdout.

#### 3.1.2 YAML Schema
```yaml
- kind: trace
  q: "Trace the pointer mutations across execution steps. What is the value at address 0x7ffd01 after Step 3?"
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
  target:
    row: 2       # 0-based index of row containing the challenge
    col: 4       # 0-based index of column to predict
  answer_text: "25"                         # Text entry mode OR
  choices: ["10", "25", "0x7ffd01", "NULL"] # Choice mode (when choices provided)
  answer: 1                                 # Index in choices
  why: "Dereferencing *p accesses the memory at &a (0x7ffd01) and mutates the integer stored there from 10 to 25."
  concept: "pointer-deref-state"
```

#### 3.1.3 TUI Interaction & Responsive Behavior
1. **Interactive Stepper**: The learner uses `n` (next step) and `p` (prev step) to step through execution.
2. **Code Synchronization**: As the step index advances, the corresponding line in the code view is highlighted with `→ Line X`.
3. **State Table Reveal**: Rows up to the active step are displayed in an APCA-high-contrast ASCII/Unicode grid.
4. **Target Challenge**: The target cell (`target.row`, `target.col`) displays `[ ??? ]` highlighted in yellow.
5. **Answering**:
   - If `choices` are present: keys `1-N` select the choice.
   - If `answer_text` is present: learner types the value into an inline text box and presses `Enter`.
6. **Mobile/Termux (< 80 cols)**: If terminal width is constrained, the table renders in stacked record format (`Step 1: a = 10; Step 2: p = &a`).

---

### 3.2 P2: Faded Parsons Problems (`kind: order` with `faded: true`)

#### 3.2.1 Purpose
Transitions the learner from passive line-ordering to active authoring by requiring them to order code blocks while simultaneously filling in missing syntactic tokens (`_____`).

#### 3.2.2 YAML Schema
```yaml
- kind: order
  faded: true
  q: "Order the lines to implement the opaque constructor and fill in the missing sizeof argument:"
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
      accepted: ["sizeof(car_t)", "sizeof(*car)", "sizeof(struct car_t)"]
  why: "car_malloc must allocate the byte size of car_t on the heap before initialization."
  concept: "opaque-constructor"
```

#### 3.2.3 TUI Interaction
1. **Line Permutation**: Learner uses `j`/`k` to select lines, `J`/`K` (or `d`/`u` / Space) to swap and arrange order.
2. **Blank Focus**: Pressing `Tab` focuses the editable blank field within any faded line.
3. **Validation**: Both line sequence (`answer_order`) and token text (`accepted` or `answer_text`) must be satisfied to pass.
4. **Backwards Compatibility**: When `faded: true` is omitted, `kind: order` behaves as standard pure-ordering.

---

### 3.3 P3: Interactive Bug Spotter (`kind: spot-bug`)

#### 3.3.1 Purpose
Builds authentic diagnostic intuition by confronting the learner with genuine compiler warnings, AddressSanitizer crashes, or runtime stack traces, requiring them to locate the buggy line and pick the corrective patch.

#### 3.3.2 YAML Schema
```yaml
- kind: spot-bug
  q: "Analyze the code and AddressSanitizer report. Which line causes the heap-use-after-free, and why?"
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
    - "Line 3: Struct member 'speed' is private"
  answer: 2
  fix_code: "// Move car_free(c) to the end of the object lifecycle"
  why: "AddressSanitizer detects memory write to 0x602000000010 after that address was returned to the heap allocator in line 2."
  concept: "use-after-free"
```

#### 3.3.3 TUI Interaction
1. **Dual-Pane Diagnostic Layout**:
   - Left Pane: Line-numbered code snippet.
   - Right Pane: Red/amber styled diagnostic error log.
2. **Line Cursor**: Learner can move a pointer cursor (`j`/`k`) over the code lines.
3. **Diagnostic Choices**: Answering via `1-N` choices matches the line and conceptual diagnosis.

---

### 3.4 P4: Subgoal Labeled Worked Examples (`subgoals`)

#### 3.4.1 Purpose
Reduces cognitive load by segmenting complex code blocks into meaningful functional subgoals (e.g. `[Invariant Guard]`, `[Resource Allocation]`, `[State Mutation]`).

#### 3.4.2 YAML Schema
Added optionally to `example:` blocks in concept units:
```yaml
blocks:
  - id: b6
    type: design
    title: "Encapsulate behavior using struct-pointer functions"
    explain_md: "..."
    example:
      lang: c
      code: |
        int list_add(list_t* list, int item) {
            if (!list || list->size >= list->capacity) return 0;
            list->items[list->size++] = item;
            return 1;
        }
      subgoals:
        - label: "Parameter & Capacity Invariant Guard"
          lines: [2]
        - label: "State Mutation"
          lines: [3]
        - label: "Status Return"
          lines: [4]
```

#### 3.4.3 TUI Presentation
In `StudyScreen`, when `subgoals` are defined:
- Code is rendered with styled Catppuccin headers above each line cluster:
  ```
  ┌─ Subgoal: Parameter & Capacity Invariant Guard ────────────────────┐
  │   2 │   if (!list || list->size >= list->capacity) return 0;       │
  └────────────────────────────────────────────────────────────────────┘
  ┌─ Subgoal: State Mutation ──────────────────────────────────────────┐
  │   3 │   list->items[list->size++] = item;                          │
  └────────────────────────────────────────────────────────────────────┘
  ```
- Terminal degradation: In narrow viewports, renders clean comment annotations: `// [Subgoal: Parameter Invariant Guard]`.

---

### 3.5 P5: Live Toolchain Inspector Tab (`RUNNER-INSPECT`)

#### 3.5.1 Purpose
Empowers learners to inspect real machine artifacts (symbols, disassembly, AST, sections) for any runnable example or lab code directly from the terminal without leaving `termlearn`.

#### 3.5.2 TUI Interaction (`InspectModal` / `InspectScreen`)
- **Hotkey**: Pressing `i` in `StudyScreen` (on a block with code) or in `LabScreen` (on current buffer).
- **Tabbed Interface**:
  - `[1] Symbols (nm)`: List of exported (`T`/`D`) vs internal (`t`/`b`) symbols. Demonstrates opaque encapsulation and `static` visibility.
  - `[2] Disassembly (objdump / dis)`: Annotated assembly showing register usage (e.g. `rdi` for `this`, `rax` for return values).
  - `[3] Sections (readelf)`: Memory sections (`.text`, `.data`, `.rodata`, `.bss`).
  - `[4] AST / High-Level`: Abstract syntax tree or bytecode representation.
- **Vim Navigation**: `j`/`k` to scroll output, `1-4` to switch tabs, `q`/`Esc` to close.

---

## 4. Schema & Validation Specifications (`lib/pack.py`)

### 4.1 Check Kinds Vocabulary Update
```python
CHECK_KINDS = {
    "predict", "why-fails", "mcq", "fillblank", "order",
    "eipe", "choose-better", "micro-lab",
    "trace", "spot-bug"  # NEW ADDITIONS
}

CHOICE_KINDS = {
    "predict", "why-fails", "mcq", "eipe", "choose-better",
    "spot-bug"  # Added to choice kinds when choices present
}
```

### 4.2 Validation Rules & Error Codes
1. **Trace Checks**:
   - `ERR TRACE-SHAPE`: `kind: trace` **MUST** include `trace.headers` (list of strings, $\ge 2$) and `trace.rows` (list of dicts, $\ge 1$).
   - `ERR TRACE-TARGET`: `target.row` and `target.col` **MUST** be valid integers pointing within `trace.rows`.
   - `ERR TRACE-ANSWER`: `kind: trace` **MUST** declare either `answer_text` OR (`choices` and `answer`).
2. **Faded Parsons Checks**:
   - `ERR FADED-BLANK`: If `kind: order` has `faded: true`, `blanks` **MUST** be a non-empty list of mappings containing `line_idx` ($0 \le \text{idx} < \text{len(lines)}$) and `answer_text` (or `accepted`).
3. **Bug Spotter Checks**:
   - `ERR BUG-TARGET`: `kind: spot-bug` **MUST** include `code`, `diagnostic_log`, `choices` (2–5 items), `answer` (valid index), and `why`.
4. **Subgoals**:
   - `ERR SUBGOAL-SPAN`: If `subgoals` appears in `example`, each item **MUST** contain `label` (string) and `lines` (list of positive integers within the code line count).

---

## 5. Verification & Acceptance Criteria

1. **Backwards Compatibility**:
   - `python main.py validate --book extreme-c --chapter ch04 --strict` exits 0.
   - `python main.py validate --book extreme-c --chapter ch09 --strict` exits 0.
2. **Schema & Runner Tests**:
   - Validation unit tests verify detection of valid and malformed `trace`, `faded-parsons`, `spot-bug`, and `subgoals`.
   - Protocol tests verify `RUNNER-VERBS`, `RUNNER-INSPECT`, and fallback behavior.
3. **TUI Tests**:
   - `tests/test_interactive_modes.py` exercises stepping through a trace table, solving a faded blank, and viewing the inspector.
4. **Regression**:
   - 100% of existing test suite (94 tests) continues to pass without errors.

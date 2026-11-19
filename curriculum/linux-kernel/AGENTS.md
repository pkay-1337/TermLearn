# AGENTS.md — Authoring Directives for Study Blocks & Chapter Packs

> **CRITICAL DIRECTIVE FOR AI AUTHORS:**  
> The learner is **NOT** reading external textbooks. Your generated study blocks, visualizations, code examples, and labs **ARE their primary textbooks**.  
> You must teach from first principles, directly grounded in the **actual pinned Linux kernel source code** and **empirical tool evidence**. Never handwave, never summarize textbooks from memory, and never write generic blog-style prose.

---

## 1. Primary Source of Truth

Every claim, code walkthrough, diagram, and check must trace directly to one of two sources:

1. **The Pinned Kernel Source Trees (`sources/`):**
   - **Phase A (0.01 / 0.11 / 0.12):** `sources/early-history.git` (pristine) and `sources/Linux-0.11-fork` (runnable harness).
   - **Phase B (0.95 → 1.2):** `sources/early-history.git` at tagged releases (`v0.95`, `v1.0`, `v1.2`).
   - **Phase C (2.0 → 2.6.12):** `sources/early-history.git` (2.6.12-rc2 is the git root).
   - **Phase D & Modern LTS:** `sources/linux-6.18.*` and `sources/linux-7.3.*`.
2. **Captured Empirical Evidence (`evidence/<chapter>/`):**
   - For tooling chapters (T0a–T8), every command, output column, and failure message must be copied verbatim from `evidence/<chapter>/transcript.md` and reference an evidence ID (`E-T0A-01`...).

**Fail Closed Rule:** If you do not have the exact source code range or captured command transcript, **stop and verify**. Never invent function signatures, line numbers, struct fields, or register names to make a nicer story.

---

## 2. Pedagogical Architecture: The 5-Job `explain_md` Contract

Because the learner does not have a textbook open, every block's `explain_md` must perform five deliberate pedagogical jobs in order:

```text
+-------------------------------------------------------------------------+
| Job 1: Frame the Problem                                                |
|   What hardware constraint, concurrency bug, or design problem forced    |
|   the kernel developers to invent this mechanism?                       |
+-------------------------------------------------------------------------+
                                   │
                                   ▼
+-------------------------------------------------------------------------+
| Job 2: The Notional Machine                                             |
|   What objects exist? Who owns them? Where do they live in memory?       |
|   What are the state transitions and immutable invariants?              |
+-------------------------------------------------------------------------+
                                   │
                                   ▼
+-------------------------------------------------------------------------+
| Job 3: The Source-Grounded Walkthrough                                  |
|   Walk the exact pinned source code line-by-line.                       |
|   Explain every pointer dereference, bitmask, register, and handoff.    |
+-------------------------------------------------------------------------+
                                   │
                                   ▼
+-------------------------------------------------------------------------+
| Job 4: The Failure Mode & Boundary                                      |
|   What happens when this breaks? Trace a race condition, a page fault,  |
|   a memory leak, an interrupt storm, or an OOM crash.                   |
+-------------------------------------------------------------------------+
                                   │
                                   ▼
+-------------------------------------------------------------------------+
| Job 5: The Compressed Mental Axiom                                      |
|   One crisp, memorable operating systems principle to retain forever.   |
+-------------------------------------------------------------------------+
```

---

## 3. Voice & Tone: Human, Grounded, and Anti-Robotic

Your writing must read like a **senior kernel maintainer and mentor** sitting right next to the learner at a dual-monitor terminal with a fresh cup of coffee. It must feel alive, conversational, and direct—never like a translated corporate policy manual, textbook regurgitation, or clinical academic paper.

### 3.1 Banned AI Clichés & Robotic Tropes
Never use these hollow filler phrases:
- ❌ *"In this section, we will delve into..."*
- ❌ *"It is crucial / paramount to note that..."*
- ❌ *"A testament to the elegance / sophistication of..."*
- ❌ *"Furthermore, it is important to observe..."*
- ❌ *"In conclusion, this mechanism serves as a vital component..."*
- ❌ *"Let us embark on a journey through..."*

### 3.2 Human Systems Voice Rules
1. **Active & Direct:** Write *"When the timer fires, IRQ0 kicks the CPU into `timer_interrupt`"* rather than *"The facilitation of task preemption is executed via the occurrence of an interrupt."*
2. **Talk to the Developer:** Use natural conversational imperatives: *"Look at line 42"*, *"Notice what `eax` holds right before the jump"*, *"Why doesn't this crash immediately? Because..."*.
3. **Acknowledge the Pain Points:** Call out the real traps, developer surprises, and historical quirks: *"In 1991, Linus didn't have modern ELF linkers, so he wrote a custom 200-line C hack (`tools/build.c`) to stitch floppy sectors together."* or *"If you forget this single semicolon, GCC's parser loses its mind and vomits 80 cascading errors on line 12."*
4. **Vivid Mental Analogies:** Make invisible hardware mechanisms tangible: *"Think of the Task State Segment (TSS) like an automatic hardware bookmark"* or *"The `.bss` section is an IOU for memory—it promises zeroed RAM at runtime without paying for bytes on your hard disk."*
5. **Varied Sentence Cadence:** Mix short, punchy technical observations with rigorous technical traces. Avoid walls of uniform 30-word sentences.

---

## 4. Block Structure & Schema Rules (`study.yaml`)

Every block in `study.yaml` must adhere to the termlearn pack specification:

### 4.1 Block Types
- `model`: Explains an invisible hardware or operating system mechanism (e.g. two-level paging, CPU context switching). Must feature prediction and state visualization.
- `syntax`: Deconstructs a specific syntax, command shape, or binary output (e.g. `pahole` struct layout, GCC flags, Kconfig grammar). Must feature an ordering or fill-in-the-blank check.
- `algorithm`: Walks a step-by-step procedural path through code (e.g. `sys_fork` dispatch, `bread` buffer lookup, page fault handler). Must feature a trace or bug-spotting check.
- `design`: Evaluates engineering trade-offs, limitations, and architectural decisions (e.g. why $O(N)$ scheduling arrays cannot scale, why VFS replaced hardcoded Minix). Must feature comparative evaluation (`choose-better` or `eipe`).

### 4.2 Diagrams & Visualizations (`diagram:` and `viz:`)
**Strong Visual Preference:** The learner understands systems concepts best when co-presented with clean visual diagrams. Always prefer rich, visual terminal diagrams over purely text-heavy explanations. Every block **must** include either a `diagram:` (relational structure / flowchart / ASCII art), a `viz:` (stepped memory / register state), or **both** co-presented together.

#### Which Visual Engine to Choose:
1. **Flowcharts (`diagram: kind: flow`) — PREFER FOR CONTROL & DATA FLOW:**
   - Use whenever teaching pipelines, call graphs, syscall dispatching, decision trees, or lifecycle progressions.
   - Declare structured `nodes:` (shapes: `box`, `round`, `decision`, `io`), `edges:` with optional labels, and stepped focus reveal (`steps: [{focus: [...], note: "..."}]`).
   - Termlearn renders these using automatic topological layout with heavy Unicode borders (`┏━┓ ┃ ┗━┛`) and arrows (`▼`, `▶`).
2. **ASCII Architecture Art (`diagram: kind: art`) — PREFER FOR HARDWARE & FORMATS:**
   - Use for verbatim physical layouts: floppy/disk sector maps, packet header structures, hardware registers, and CPU bit fields.
   - Keep width aligned to $\le 70$ columns; clean box drawings using `+`, `-`, and `|`.
3. **Memory State Machines (`viz: kind: ascii-memory`) — PREFER FOR MEMORY & REGISTERS:**
   - Use for stepwise pointer mutations, stack/heap allocations, page directory/table lookups, and register state transitions over time.
   - **CRITICAL FORMAT RULE:** Every entry in `steps:` **MUST be a clean, human-readable string** (per SRS §4.4: `steps: ["...", "..."]`), **NEVER a YAML dictionary mapping** (`{label: ..., registers: ...}`). Termlearn prints `str(step)` with `▶ ` prefixed to the active step; if you supply a YAML dictionary, the learner will see ugly Python debug syntax (`{'label': '...', 'registers': {...}}`).
   - Format each step as a concise, elegant state progression line:
     ```yaml
     viz:
       kind: ascii-memory
       steps:
         - "[Step 1: Child Spawn] PID: 4120 in /home/user/workload · FD1 -> stdout · Status: ACTIVE"
         - "[Step 2: Exit & Harvest] PID: 4120 dead · stdout: '5\\n' · Shell waitpid() records $?=0"
     ```
   - Provide 2–5 sequential steps revealing state changes as the user presses `n`.


### 4.3 Code Examples in Blocks (`example:`)
- **Kernel Code Excerpts:** When presenting raw kernel source or assembly excerpts, **always set `lang: text` or `lang: asm`**. Never use `lang: c` for kernel excerpts, because `main.py validate` compile-probes C snippets with host `gcc`, which will fail on kernel headers.
- **Standalone Userspace Code:** Only set `lang: c` when the code is a 100% self-contained, valid C99 userspace program with `main()` that compiles cleanly with `gcc -Wall -Wextra`.
- **Exact Expected Output:** When `run_expected:` is declared, it must match the actual stdout output byte-for-byte.

---

## 5. Assessment Construction Standards (Checks & Quizzes)

Each block must contain **5 to 8 scaffolded checks** covering multiple cognitive levels.

### 5.1 Check Rules
1. **Self-Contained:** Every check must embed all necessary code snippets, transcripts, or scenarios directly in the stem (`q:`). The learner must never need to switch tabs or remember an external book listing.
2. **Allowed Kinds Only:** Use only valid kinds: `predict`, `why-fails`, `fillblank`, `order`, `spot-bug`, `trace`, `mcq`, `choose-better`, `eipe`.
3. **Plausible Distractors:** Distractors must represent real systems misconceptions (e.g., confusing virtual with physical addresses, confusing exit status with stdout, or assuming a read-only buffer can be modified).
4. **Exhaustive Explanations (`why:`):**
   - State clearly why the correct option is correct.
   - **Explicitly name the misconception behind every incorrect distractor.** (e.g. *"Option A is incorrect because .bss allocates zeroed RAM at runtime, not on disk."*).
5. **No Self-Referential Interleaving in the First Chapter:** For Chapter `T0A`, do not use `from_chapter: T0A`. Interleaving across chapters begins only in chapter 2 onward.

---

## 6. Lab Design & The "Algorithm Synthesis" Family (`labs.yaml`)

Each chapter must provide practical, interactive labs. In addition to standard experiment labs (`knob`, `break-it`, `instrument`), implement **Algorithm Synthesis Labs** wherever specified in `PLAN.md`:

### 6.1 What an Algorithm Synthesis Lab Must Provide
When instructing the learner to extract and implement a kernel algorithm (e.g., `list_head`, `kfifo`, LRU buffer cache, buddy allocator, LPM trie):
1. **Clear Functional Specification:**
   - Define the exact C struct definitions.
   - Define the function prototypes (e.g. `void list_add(struct list_head *new, struct list_head *head);`).
   - State the invariant that must hold true after every operation.
2. **Complete Test Harness:**
   - Provide starter template files with `# TODO` markers.
   - Provide an automated test script (`check.sh` or `verify.c`) that exercises edge cases: empty structures, wraparounds, full buffers, and out-of-order operations.
   - The lab `test_cases:` must verify that the learner's synthesized C implementation compiles cleanly with `-Wall -Wextra` and exits 0 with `ALL TESTS PASSED`.

---

## 7. Verification Checklist Before Saving Any Pack

Before concluding the generation of any chapter pack, run this verification checklist:

- [ ] All 6 YAML files exist in `packs/linux-kernel/<chapter_id>/`:
  - `meta.yaml`
  - `study.yaml`
  - `labs.yaml`
  - `quiz.yaml`
  - `cards.yaml`
  - `test.yaml`
- [ ] Every block in `study.yaml` has:
  - `id: b1`... (monotonically numbered).
  - An `explain_md` covering the 5 pedagogical jobs.
  - A rich `diagram:` (`kind: flow` or `kind: art`) or `ascii-memory` visualization (`viz:`) with multi-step state transitions.
  - 5–8 diverse, self-contained checks with comprehensive `why:` explanations.
- [ ] Kernel code excerpts use `lang: text` or `lang: asm`.
- [ ] Every fact, macro, and struct maps to the pinned source tree for that phase.
- [ ] All lab files include deterministic `test_cases:` with `expect:` and `expect_exit: 0`.
- [ ] The chapter is registered in `packs/linux-kernel/book.yaml` and `books/linux-kernel/meta.json`.
- [ ] The strict validator passes:
  ```bash
  python main.py validate --book linux-kernel --chapter <id> --strict
  ```

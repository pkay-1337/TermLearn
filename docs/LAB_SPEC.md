# ISO/IEC/IEEE 29148:2018 Specification: Multi-Lab Workspace & Correctness Verification System

**Document Identifier**: `SPEC-TERMLEARN-LAB-2026-V1`  
**Standard Compliance**: ISO/IEC/IEEE 29148:2018 (Systems and software engineering — Life cycle processes — Requirements engineering)  
**Requirements Normative Language**: RFC 2119 (Key words for use in RFCs to Indicate Requirement Levels)  
**Status**: APPROVED BASELINE SPECIFICATION  
**Date**: 2026-10-18  

---

## 1. Introduction

### 1.1 Purpose
This specification defines the functional, structural, and behavioral requirements for the next-generation **Multi-Lab, Multi-File Workspace, and Input/Output Correctness Verification System** within TermLearn. It supersedes the legacy single-file, single-lab architecture with an authentic, project-scale engineering environment.

### 1.2 Scope
This document covers:
1. The declarative pack schema for multiple labs per chapter (`labs:` array).
2. The filesystem layout and automated provisioning under `labs/<book_slug>/<chapter_id>/<lab_id>/`.
3. The language-agnostic execution engine supporting arbitrary build/run commands.
4. The automated correctness verification engine comparing execution input (`stdin`, `args`) against expected output (`stdout`, `stderr`, exit codes) with unified diff generation.
5. The Terminal User Interface (TUI) lab interaction model (multi-file viewer, external `$EDITOR` integration, multi-lab navigation, and real-time execution feedback).
6. Security boundaries and execution sandboxing.

### 1.3 Conformance (RFC 2119)
The key words **"MUST"**, **"MUST NOT"**, **"REQUIRED"**, **"SHALL"**, **"SHALL NOT"**, **"SHOULD"**, **"SHOULD NOT"**, **"RECOMMENDED"**, **"MAY"**, and **"OPTIONAL"** in this document are to be interpreted as described in RFC 2119.

---

## 2. References & Context

- **ISO/IEC/IEEE 29148:2018**: Requirements engineering process model and requirement structure.
- **RFC 2119**: Key words for requirement levels.
- **TermLearn System Requirements**: `docs/SRS.md` (§4.8 Pack Schema, §4.9 Runner Protocol, §5 Feature List).

---

## 3. Specific Requirements

### 3.1 Workspace & Directory Hierarchy

- `REQ-LAB-DIR-001`: The system **SHALL** maintain a dedicated physical workspace directory for every lab in every chapter on disk, adhering strictly to the topology:
  ```text
  labs/<book_slug>/<chapter_id>/<lab_id>/
  ```
  Where `<book_slug>` is the unique book identifier, `<chapter_id>` is the chapter identifier (e.g., `ch10`), and `<lab_id>` is the specific lab identifier (e.g., `lab1`, `lab2`).

- `REQ-LAB-DIR-002`: When a lab is invoked via the TUI or CLI, the system **SHALL** automatically verify the presence of the corresponding lab directory. If the directory does not exist, the system **SHALL** create it along with any missing parent directories.

- `REQ-LAB-DIR-003`: The system **SHALL** provision all initial files declared in the lab definition into the lab directory upon initial workspace creation.

- `REQ-LAB-DIR-004`: Once a lab workspace is provisioned, the system **MUST NOT** overwrite, delete, or revert any file modified by the student during routine runs, test executions, or navigation.

- `REQ-LAB-DIR-005`: The system **SHALL** provide an explicit reset capability (via UI shortcut `R` or CLI flag `--reset`) that restores the workspace to the pristine initial files declared in the pack, only after requesting explicit confirmation from the user.

---

### 3.2 Pack Schema (`labs: [...]`)

- `REQ-LAB-SCH-001`: In the chapter pack YAML specification, the chapter definition **MAY** contain a top-level `labs` array holding 1 to `N` lab objects. The legacy top-level `lab` mapping **SHALL NOT** be required (no backward compatibility).

- `REQ-LAB-SCH-002`: Each lab object within `labs` **MUST** specify the following mandatory attributes:
  1. `id` (`string`): Unique ASCII identifier within the chapter (e.g., `lab1`, `lab2`).
  2. `title` (`string`): Human-readable descriptive title.
  3. `instruction_md` (`string`): Comprehensive Markdown instructions detailing the problem context, tasks, invariants, and expected outcomes.
  4. `files` (`array` of objects): List of files participating in the lab.
  5. `commands` (`object`): Language-agnostic execution commands containing at least `run` and/or `test`.

- `REQ-LAB-SCH-003`: Each file entry in `files` **MUST** declare:
  1. `path` (`string`): Path relative to the lab directory (e.g., `engine.h`, `src/utils.c`).
  2. `content` (`string`): Initial starter code, template, or test fixture.

- `REQ-LAB-SCH-004`: A lab definition **MAY** specify an optional `test_cases` array for input-versus-expected-output evaluation, where each item defines:
  1. `name` (`string`): Descriptive case label.
  2. `command` (`string`, optional): Specific binary or script to execute (defaults to the lab's primary target).
  3. `args` (`array` of strings, optional): Command-line arguments.
  4. `stdin` (`string`, optional): Standard input stream piped into the process.
  5. `expect` (`string`): Exact expected standard output (`stdout`).
  6. `expect_exit` (`integer`, optional): Expected process exit code (default: `0`).

- `REQ-LAB-SCH-005`: A lab definition **MAY** specify an optional `hints` array containing progressive textual hints revealed sequentially.

---

### 3.3 Execution & Input/Output Correctness Verification

- `REQ-LAB-EXE-001`: All execution commands (`commands.run`, `commands.test`, and `test_cases[].command`) **MUST** execute with the working directory (`cwd`) set to the specific lab workspace (`labs/<book_slug>/<chapter_id>/<lab_id>/`).

- `REQ-LAB-EXE-002`: The execution engine **SHALL** be completely language-agnostic, executing shell commands via the operating system process spawner without enforcing C-specific toolchains or flags.

- `REQ-LAB-EXE-003`: When the student triggers a **Run** action, the system **SHALL** execute `commands.run`, capture standard output and standard error, and display the stream in the TUI console panel with process execution timing (`elapsed_ms`) and termination status.

- `REQ-LAB-EXE-004`: When the student triggers a **Test** action, the system **SHALL** execute the verification suite:
  1. If `commands.test` is defined, the system **SHALL** execute `commands.test` in the lab workspace. A non-zero exit code **SHALL** constitute a test failure.
  2. If `test_cases` are defined, the system **SHALL** execute each test case in order, feeding `stdin` and checking `stdout` against `expect`.

- `REQ-LAB-EXE-005`: In input-versus-expected-output verification (`test_cases`), the system **SHALL** compare actual output against expected output:
  1. If `actual_stdout != expected_stdout`, the test case **SHALL** fail.
  2. The system **SHALL** generate a unified diff between expected output and actual output, formatted as:
     ```diff
     --- expected
     +++ actual
     @@ -1,3 +1,3 @@
      Initializing Engine...
     -Temperature: 15.0
     +Temperature: 0.0
     ```
  3. If `actual_exit_code != expected_exit_code`, the test case **SHALL** fail, reporting the exit status disparity and capturing the tail of `stderr`.

- `REQ-LAB-EXE-006`: The system **SHALL** enforce a strict execution timeout (specified by `commands.timeout_s`, defaulting to 5 seconds). Any process exceeding this duration **SHALL** be terminated via `SIGKILL` and flagged as `TIMEOUT`.

- `REQ-LAB-EXE-007`: The system **SHALL** sanitize all commands against a dangerous command denylist (including `rm -rf /`, `curl`, `wget`, `ssh`, `:(){ :|:& };:`) before launching processes.

---

### 3.4 Terminal User Interface (TUI) Interaction Model

- `REQ-LAB-UI-001`: The system **SHALL** provide a responsive, multi-pane TUI screen (`LabScreen`) within Textual.

- `REQ-LAB-UI-002`: The TUI **SHALL** render a multi-lab navigation header displaying the current lab index and title (e.g., `Lab 1/3: Encapsulating the Engine Component`), providing keybindings (`[` / `]` and `p` / `n`) to switch between labs.

- `REQ-LAB-UI-003`: The TUI **SHALL** provide a **File Selector Bar** listing all files present in the lab workspace. Selecting a file tab **SHALL** display the file's current disk content in a syntax-highlighted viewer.

- `REQ-LAB-UI-004`: The TUI **SHALL** support opening files in the student's external `$EDITOR` (or fallback to `nano`/`vim`):
  1. Upon pressing `e` (or clicking **Edit**), the system **SHALL** invoke `self.app.suspend()`.
  2. The external editor **SHALL** be launched targeting the active file or the lab workspace directory.
  3. When the editor process terminates, the TUI **SHALL** resume and immediately reload file contents from disk.

- `REQ-LAB-UI-005`: The TUI **SHALL** display real-time pass/fail status badges:
  - `UNTESTED` (dim gray) before testing.
  - `PASSING ✔` (emerald green) when all test suites and test cases pass.
  - `FAILING ✖` (crimson red) when a compilation error, assertion failure, or diff mismatch occurs.

- `REQ-LAB-UI-006`: The TUI **SHALL** provide a dedicated console output drawer displaying compiler output, test execution logs, unified diffs, and execution timing.

- `REQ-LAB-UI-007`: The TUI **SHALL** support progressive hints via `h`: each press reveals the next available hint in `hints` without scrolling or disrupting workspace layout.

---

### 3.5 Progress Persistence & Telemetry

- `REQ-LAB-PRG-001`: The system **SHALL** record all lab test outcomes in the local SQLite progress database under a table `lab_runs`:
  ```sql
  CREATE TABLE IF NOT EXISTS lab_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts INTEGER NOT NULL,
    book TEXT NOT NULL,
    chapter TEXT NOT NULL,
    lab_id TEXT NOT NULL,
    passed INTEGER NOT NULL,
    output TEXT DEFAULT '',
    elapsed_ms INTEGER DEFAULT 0
  );
  ```

- `REQ-LAB-PRG-002`: When all test suites and test cases for a lab pass successfully (`passed == 1`), the system **SHALL** register the lab as mastered, updating chapter completion progress and satisfying lab gate requirements in chapter tests.

---

### 3.6 AI Prompt & Generation Standard

- `REQ-LAB-GEN-001`: AI chapter generation prompts (`prompts/GENERATE.md`, `lib/ai_prompt.py`) **SHALL** require the AI model to author 1 to 3 scaffolded labs per chapter whenever the chapter involves executable code or algorithms.

- `REQ-LAB-GEN-002`: The AI **MUST** structure labs with escalating pedagogical complexity:
  - **Lab 1 (Foundational)**: Single/dual-file implementation or bug repair focusing on core chapter syntax/invariants.
  - **Lab 2 (Architectural)**: Multi-file component decomposition, interface isolation, or delegation.
  - **Lab 3 (Advanced/Capstone, where applicable)**: Robustness, defensive checks, lifecycle edge cases, or full end-to-end integration.

- `REQ-LAB-GEN-003`: For every authored lab, the AI **MUST** author:
  1. Complete, compilable header/interface files and supportive framework.
  2. Starter implementation files which **MAY** be blank (`content: ""`) or scaffolded with function stubs and `/* TODO: ... */` tasks.
  3. Comprehensive test harnesses (`test_runner` or `test_cases`) with deterministic assertions and/or concrete input/output pairs.
  4. Language-agnostic, portable build and test command strings.

- `REQ-LAB-GEN-004`: Starter implementation files **SHALL NOT** provide 100% pre-solved solutions (tests must fail or report missing symbols initially). The student **MUST** actively write or complete the implementation.

---

## 4. Verification & Validation (V&V) Matrix

| Requirement ID | Description | Method | Pass Criteria |
| :--- | :--- | :--- | :--- |
| `REQ-LAB-DIR-001` | Workspace directory topology | Test | `labs/<book>/<chapter>/<lab_id>/` exists upon provisioning. |
| `REQ-LAB-DIR-004` | Non-destructive student edits | Test | Modifying a file, re-opening lab, and running retains modifications. |
| `REQ-LAB-SCH-002` | Mandatory attributes validation | Inspection | `main.py validate --strict` verifies `id`, `title`, `instruction_md`, `files`, `commands`. |
| `REQ-LAB-EXE-001` | Subprocess working directory | Test | Subprocess prints `cwd` matching lab workspace path. |
| `REQ-LAB-EXE-004` | Test execution & verdict | Test | Returncode 0 yields pass; non-zero yields failure with diagnostics. |
| `REQ-LAB-EXE-005` | Input/Output diff verification | Test | Mismatched stdout produces clean unified diff with `-` and `+` markers. |
| `REQ-LAB-EXE-006` | Process timeout safety | Test | Infinite loop process terminates within 5 seconds with `TIMEOUT`. |
| `REQ-LAB-UI-002` | Multi-lab switcher | Demonstration | Pressing `n` and `p` switches active lab and loads corresponding files. |
| `REQ-LAB-UI-004` | External `$EDITOR` suspend | Demonstration | Pressing `e` suspends TUI, opens editor, and reloads file upon return. |
| `REQ-LAB-PRG-001` | Persistence in SQLite | Test | `lab_runs` row inserted with timestamp and correct pass status. |

---

## 5. Traceability to Existing System

- **Supersedes**: `docs/SRS.md` `FR-AI-006`, `FR-LAB-001`, `FR-LAB-002`, `FR-LAB-003`, `FR-LAB-004`.
- **Replaces**: `lab: {starter_c: ...}` in `packs/<slug>/<id>.yaml` with `labs: [...]`.
- **Coexists With**: SRS flashcards, conceptual quizzes, Parsons order checks, and study blocks.

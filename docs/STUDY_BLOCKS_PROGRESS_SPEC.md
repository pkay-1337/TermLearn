# Chapter Study Block List & Completion Tracking Specification
**Document ID:** SPEC-TUI-003  
**Target Subsystem:** `lib/progress.py`, `tui/screens.py`, `tui/practice.py`, `tui/style.tcss`, `tests/test_tui.py`  
**Status:** APPROVED  
**Author:** AI Pair Programmer  
**Date:** October 2026  

---

## 1. Executive Summary & Problem Statement

### 1.1 The Blind Entry Problem in Study Mode
In `termlearn`, each course chapter is structured into pedagogical concept units termed **blocks** (`b1`, `b2`, `b3`, etc.). Each block consists of:
1. Conceptual explanation (`explain_md`)
2. Runnable example code (`example`)
3. Optional memory visualizer step-through (`viz`)
4. Targeted micro-checks / diagnostic questions (`checks`)

Currently, when a user selects **Study** from `ChapterMenu`, the application pushes `StudyScreen` starting rigidly at block 0 (`bi = 0`). The user experiences several usability limitations:
- **No Progress Awareness**: There is no screen or badge showing how many blocks exist in the chapter, which blocks have been completed, which are partially attempted, or which remain untouched.
- **No Direct Access / Bookmarking**: If a chapter has 8 blocks and the user previously completed blocks 1 through 3, returning to Study starts at block 1 again. The user must manually press `n` dozens of times to skip forward to block 4.
- **Inability to Review Specific Concepts**: A learner wanting to review a specific tricky block (e.g., `b3: pointer arithmetic and void*`) cannot pick it directly; they must traverse sequentially.

### 1.2 User Requirement
The user requested:
> *"the chapters studies have blocks right? can we get a list of blocks with indicator if if we have completed it or not? and open that first when clicking on a study"*  
> *"plan and create an spec for it keeping in mind everything, movement, not breaking anyother feature"*

This requires:
1. **Upfront Block List Screen**: Selecting "Study" in `ChapterMenu` opens `StudyBlockListScreen` first instead of jumping directly into block 1.
2. **Completion Indicators**: Visual status badges for every block:
   - `[✔ COMPLETED]` (all checks completed / marked done)
   - `[◐ IN PROGRESS]` (some checks attempted, e.g., 2/4 checks)
   - `[○ NOT STARTED]` (no checks attempted, unread)
3. **Block Selection & Launch**: Selecting any block launches `StudyScreen` positioned directly at that block (`start_block=bi`).
4. **Fluid Vim Movement**: Full Vim navigation (`j`/`k`, `Enter`/`l`, `g`/`G`, `d`/`u`, `q`/`h`, `Tab`), dual-pane dossier preview, and responsive support for small/mobile viewports (Termux).
5. **No Regressions**: Zero disruption to other `ChapterMenu` modes (Revise, Quiz, Parsons, Lab, Test, Cards, Stats) or existing test suites.

---

## 2. Block Completion Definition & Data Model

### 2.1 Completion Semantics
Each chapter YAML defines `blocks: list[dict]`. Let $N = \text{len}(b.\text{checks})$.

| Scenario | Condition | Status | Badge Display |
| :--- | :--- | :--- | :--- |
| **Completed (Checks)** | $N > 0$ and user has answered all $N$ checks, OR explicitly recorded in `block_progress` | `completed` | `[bold green]✔ DONE[/]` or `[bold green]✔ COMPLETED[/]` |
| **Completed (No Checks)** | $N = 0$ and user stepped through block to completion in `StudyScreen` (recorded in `block_progress`) | `completed` | `[bold green]✔ READ[/]` or `[bold green]✔ DONE[/]` |
| **In Progress** | $N > 0$ and user has attempted at least 1 check, but $< N$ checks | `in_progress` | `[bold yellow]◐ k/N CHECKS[/]` |
| **Not Started** | 0 checks attempted and not marked completed in `block_progress` | `not_started` | `[dim]○ TODO[/]` |

### 2.2 Database Schema Migration (`lib/progress.py`)
To track block completions explicitly (especially for blocks without checks or to remember full block completion even when individual checks are retried), `init_db()` in `lib/progress.py` creates a lightweight table:

```sql
CREATE TABLE IF NOT EXISTS block_progress(
  id INTEGER PRIMARY KEY,
  ts INTEGER,
  book TEXT,
  chapter TEXT,
  block TEXT,
  completed INTEGER DEFAULT 1,
  UNIQUE(book, chapter, block)
);
```

### 2.3 Progress API (`lib/progress.py`)
We introduce three focused helper functions:

```python
def mark_block_completed(book: str, chapter: str, block: str) -> None:
    """Record that a study block was completed by the user."""
    con = init_db()
    try:
        con.execute(
            "INSERT INTO block_progress(ts, book, chapter, block, completed) "
            "VALUES(?, ?, ?, ?, 1) "
            "ON CONFLICT(book, chapter, block) DO UPDATE SET ts=excluded.ts, completed=1",
            (int(time.time()), book, chapter, block),
        )
        con.commit()
    finally:
        con.close()

def block_status(book: str, chapter: str, block_id: str, n_checks: int) -> dict:
    """Returns detailed completion status for a specific block."""
    con = _db_or_none()
    if con is None:
        return {"status": "not_started", "completed": False, "attempted": 0, "correct": 0, "total": n_checks}
    try:
        # Check explicit completion flag
        bp = con.execute(
            "SELECT completed FROM block_progress WHERE book=? AND chapter=? AND block=?",
            (book, chapter, block_id)
        ).fetchone()
        is_done = bool(bp and bp[0])

        # Check answers table
        rows = con.execute(
            "SELECT check_idx, correct FROM answers WHERE book=? AND chapter=? AND block=?",
            (book, chapter, block_id)
        ).fetchall()
        attempted_indices = {r[0] for r in rows}
        correct_count = sum(1 for r in rows if r[1] == 1)

        if n_checks > 0:
            if is_done or len(attempted_indices) >= n_checks:
                status = "completed"
                completed = True
            elif len(attempted_indices) > 0:
                status = "in_progress"
                completed = False
            else:
                status = "not_started"
                completed = False
        else:
            status = "completed" if is_done else "not_started"
            completed = is_done

        return {
            "status": status,
            "completed": completed,
            "attempted": len(attempted_indices),
            "correct": correct_count,
            "total": n_checks,
        }
    finally:
        con.close()

def chapter_blocks_progress(book: str, chapter: str, blocks: list[dict]) -> list[dict]:
    """Batch-fetches progress status for all blocks in a chapter."""
    out = []
    for b in blocks:
        bid = b.get("id", "?")
        n_ck = len(b.get("checks", []) or [])
        st = block_status(book, chapter, bid, n_ck)
        st["id"] = bid
        st["title"] = b.get("title", bid)
        out.append(st)
    return out
```

---

## 3. UI/UX Architecture & Screen Flow

### 3.1 Screen Navigation Hierarchy
```
HomeScreen (Book Selection)
   │
   ▼ [Enter]
ChaptersScreen (Chapter Selection)
   │
   ▼ [Enter]
ChapterMenu (Mode Selection: 1. Study, 2. Revise, 3. Quiz, ...)
   │
   ├─► [1] Study: StudyBlockListScreen (NEW)
   │        │
   │        ├─► [Enter / l / 1-9]: StudyScreen(start_block=bi)
   │        │        │
   │        │        └─► [q / h / End of Chapter]: pops back to StudyBlockListScreen (auto-refreshed)
   │        │
   │        └─► [q / h]: pops back to ChapterMenu
   │
   ├─► [2] Revise: ReviseScreen
   ├─► [3] Quiz: QuizScreen
   └─► ...
```

### 3.2 Dual-Pane Dossier Layout (`StudyBlockListScreen`)

#### Desktop / Wide Terminal ($\ge 80$ cols):
```
+--------------------------------------------------------------------------------------------------------+
| 📖  STUDY BLOCKS — extreme-c / ch04: Essential Features                   [Completed: 2/4 blocks · 50%]|
+----------------------------------------------------+---------------------------------------------------+
|  BLOCK SELECTION (j/k: nav · Enter/l: open)        |  BLOCK PREVIEW (l/Tab: focus · d/u: scroll)       |
|                                                    |                                                   |
| > [1]  ✔ DONE      b1: Macros: #define & expansion |  ## b1: Macros: #define and expansion             |
|   [2]  ◐ 2/3       b2: Pointer dereferencing       |                                                   |
|   [3]  ○ TODO      b3: Function call stack         |  - **Type:** Syntax                               |
|   [4]  ○ TODO      b4: Struct memory layout        |  - **Status:** ✔ COMPLETED (3/3 checks answered)  |
|                                                    |  - **Concepts:** macro-expansion, macro-design    |
|                                                    |                                                   |
|                                                    |  ### Summary                                      |
|                                                    |  Directives starting with `#` are for the         |
|                                                    |  preprocessor, never the compiler...              |
|                                                    |                                                   |
|                                                    |  ```c                                             |
|                                                    |  #define ABC 5                                    |
|                                                    |  int main() { ... }                               |
|                                                    |  ```                                              |
|                                                    |                                                   |
|                                                    |  👉 Press [bold cyan]Enter[/] or [bold cyan]l[/]  |
|                                                    |     to launch Study mode at this block.           |
+----------------------------------------------------+---------------------------------------------------+
| [1-4] Jump to Block  ·  j/k Navigate  ·  Enter/l Open  ·  Tab Toggle Pane  ·  q/h Back  ·  ? Help      |
+--------------------------------------------------------------------------------------------------------+
```

#### Narrow Terminal / Mobile / Termux ($< 80$ cols):
- Dynamically hides the right pane on narrow viewports (`pane-hidden`), displaying the full-width block list.
- Pressing `l` or `Tab` toggles to the full-width block dossier; pressing `h` or `Tab` toggles back to the block list.
- Fully compatible with mobile and small split panes.

### 3.3 Vim Movement & Keybindings

| Keybinding | Action | Target / Context |
| :--- | :--- | :--- |
| `j` / `Down` | Move cursor down 1 item | `#block-list` (OptionList) or scroll relative y=+2 in dossier |
| `k` / `Up` | Move cursor up 1 item | `#block-list` (OptionList) or scroll relative y=-2 in dossier |
| `g` / `Home` | Jump to first block | `#block-list` or scroll home in dossier |
| `G` / `End` | Jump to last block | `#block-list` or scroll end in dossier |
| `d` / `u` | Half-page scroll down / up | Active pane |
| `Enter` / `l` | Launch Study Mode at highlighted block | Opens `StudyScreen(book, chapter, start_block=bi)` |
| `Tab` | Switch focus between list and preview dossier | Dual-pane navigation |
| `1`-`9` | Quick jump to block 1–9 | Directly highlights and opens or selects block |
| `q` / `h` | Return to `ChapterMenu` | Screen pop |
| `?` | Open Help modal | Lists all bindings and navigation controls |

---

## 4. `StudyScreen` Integration

### 4.1 Parameterization
`StudyScreen.__init__` is updated with `start_block: int = 0`:
```python
class StudyScreen(VimScrollMixin, _Base):
    def __init__(self, book: str, chapter: str, start_block: int = 0) -> None:
        super().__init__()
        self.book = book
        self.chapter = chapter
        self.bi = max(0, start_block)
        self.stage = "explain"
        self.vi = 0
```
- In `compose()`, ensures `self.bi` is clamped to `min(self.bi, len(self.blocks) - 1)`.

### 4.2 Auto-Marking Block Completion
In `StudyScreen`:
- When user reaches `stage == "done"` or calls `_advance_block()`:
  ```python
  from lib.progress import mark_block_completed
  b = self._block()
  mark_block_completed(self.book, self.chapter, b.get("id", "?"))
  ```
- This guarantees that finishing a block immediately records completion in the database.

### 4.3 Returning to `StudyBlockListScreen`
- When the user completes the final block of the chapter or presses `q` or `h`:
  `self.app.pop_screen()` returns to `StudyBlockListScreen`.
- In `StudyBlockListScreen.on_screen_resume()`:
  The screen automatically re-fetches block progress from the database and refreshes the list items and preview dossier. The learner immediately sees the updated `[✔ COMPLETED]` badge!

---

## 5. TCSS Styling Specifications (`tui/style.tcss`)

```tcss
/* Study Block Selection Screen */
.block-split-container {
    width: 100%;
    height: 1fr;
    layout: horizontal;
}

.block-list-pane {
    width: 1fr;
    height: 100%;
    border-right: heavy $panel-darken-2;
    padding: 0 1;
}

.block-details-pane {
    width: 1fr;
    height: 100%;
    padding: 1 2;
    overflow-y: auto;
    background: $surface;
}

.block-status-banner {
    width: 100%;
    height: 3;
    content-align: center middle;
    background: $primary-darken-3;
    color: $text;
    text-style: bold;
    border-bottom: heavy $primary;
}

.badge-done {
    color: $success;
    text-style: bold;
}

.badge-prog {
    color: $warning;
    text-style: bold;
}

.badge-todo {
    color: $text-muted;
}
```

---

## 6. Verification & Automated Test Strategy

1. **Unit & Database Tests**:
   - Verify `mark_block_completed` inserts and updates `block_progress`.
   - Verify `block_status` accurately computes `completed`, `in_progress`, and `not_started` across blocks with checks and blocks without checks.
   - Verify `chapter_blocks_progress` returns proper batch metrics.

2. **TUI Navigation Tests (`tests/test_tui.py`)**:
   - `test_chapter_menu_opens_study_block_list`: Pressing `1` from `ChapterMenu` opens `StudyBlockListScreen`.
   - `test_study_block_list_renders_indicators`: Verify `[✔ DONE]`, `[◐ ...]`, and `[○ TODO]` indicators render correctly according to recorded progress.
   - `test_study_block_list_select_block_opens_study`: Selecting a block launches `StudyScreen` with `bi == selected_index`.
   - `test_study_screen_completion_updates_list`: Stepping through a block marks it completed and pops back with updated badge.
   - Update `test_nav_home_to_study_and_help` to account for the block list step before `StudyScreen`.

3. **Regression Safety**:
   - Run all existing 91 tests (`pytest`) ensuring 100% pass rate.
   - Manual verification in narrow viewport simulation (Termux 80x24).

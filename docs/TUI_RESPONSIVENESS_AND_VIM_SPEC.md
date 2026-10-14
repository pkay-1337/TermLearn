# TUI Responsiveness and Vim Navigation Specification
**Document ID:** SPEC-TUI-002  
**Target Subsystem:** `tui/` (`tui/style.tcss`, `tui/widgets.py`, `tui/practice.py`, `tui/screens.py`, `tui/app.py`)  
**Status:** DRAFT (Awaiting User Review)  
**Author:** AI Pair Programmer  
**Date:** October 2026  

---

## 1. Executive Summary & Problem Statement

### 1.1 The Multiple-Choice & Content Overflow Problem
In `termlearn`, technical questions frequently contain detailed contextual prompts, code snippets, and lengthy multi-line answer options (e.g., in deep C memory semantics, pointer arithmetic, and concurrency). In the current Textual implementation:
1. **Button Truncation**: Multiple-choice options are constructed using Textual's default `Button` widget (`classes="question-opt-btn"`). Textual buttons enforce single-line text constraints. When an option exceeds ~40-60 terminal columns, it is aggressively truncated with ellipsis (`...`), hiding critical nuances of the question choices.
2. **Viewport Vertical Overflow**: In `QuizScreen` and `StudyScreen`, the question prompt, syntax-highlighted code block, and 4 choice options often occupy more vertical rows than standard terminal heights (24-40 rows). When an answer is submitted, `#feedback` and `#next-btn` are mounted at the bottom of the widget below the visible fold. Because the screen container does not auto-scroll to the newly revealed feedback, the user is left stranded wondering if an action occurred.
3. **Rigid Viewport Layouts**: In `CardsScreen` (SRS flashcards), `.flashcard-frame` has rigid fixed dimensions (`width: 72; max-height: 20;`). On small terminal windows (e.g., 70-80 columns or split tmux panes), it overflows and clips. On larger terminals with detailed explanations, answers exceed 20 lines and clip.
4. **Master-Detail Keyboard Inaccessibility**: In `HomeScreen` and `ChaptersScreen`, long dossiers (e.g., 28 chapters or detailed objectives) render in the right pane (`#book-details-md`, `#ch-details-md`). Focus is permanently trapped in the left `OptionList`, making it impossible for keyboard-only users to scroll and read the complete curriculum roadmap.

### 1.2 The Vim Movement Ergonomics Requirement
Terminal power users expect ubiquitous Vim keybindings (`j`/`k`, `h`/`l`, `d`/`u`, `g`/`G`) for seamless navigation without reaching for arrow keys or a mouse. However:
- Text navigation must be contextual: typing inside `Input` fields (Parsons `#order-in`, fill-in-the-blank `#fill-in`, card editor) or `TextArea` (code lab `#lab-code`) must never trigger Vim motion commands.
- Dual-pane views (`HomeScreen`, `ChaptersScreen`) need intuitive pane switching (`l` to enter dossier pane, `h` to return to list).
- Option navigation should support both rapid single-key shortcuts (`1`-`4`, `n`, `q`) and fluid `j`/`k` roving cursor selection.

---

## 2. Root-Cause Analysis of Current TUI Viewports

| Component | Current Implementation | Root Cause of Defect | Impact |
| :--- | :--- | :--- | :--- |
| **MCQ Options** (`QuestionWidget`) | `Button(f"({i}) {opt}")` | Textual `Button` has fixed single-line height, no automatic word wrap (`text-wrap: wrap` ignored or clipped by button chrome). | Long options are cut off (`...`), making conceptual choices unreadable. |
| **Code Examples** (`QuestionWidget` & `StudyScreen`) | `Syntax(ck["code"])` | No vertical bounding (`max-height`). Large 30-line code examples consume the entire terminal screen. | Options and feedback are pushed far offscreen. |
| **Answer Feedback** (`QuestionWidget`) | Mounts `Button("#next-btn")` below `#feedback` | Container does not issue `scroll_visible` or programmatic scroll anchor on update. | User sees nothing happen after pressing an answer key; feedback is hidden below fold. |
| **Master-Detail Dossier** (`HomeScreen`, `ChaptersScreen`) | Left: `OptionList`; Right: `Vertical(classes="content-pane")` | Focus is trapped on `OptionList`. Right pane has `overflow-y: auto` but no `can_focus = True` or key handlers. | Long chapter lists (e.g. 28 chapters) cannot be scrolled with keyboard. |
| **SRS Deck** (`CardsScreen`) | `.flashcard-frame` (`width: 72; min-height: 14; max-height: 20;`) | Hardcoded character dimensions rather than viewport percentages. | Overflows on <80 col screens; clips long card explanations on tall screens. |
| **Scroll Navigation** (All screens) | Relying solely on default `ScrollableContainer` mouse wheel / arrow keys | No bindings for `j`/`k`, `d`/`u`, `g`/`G`. | Terminal users accustomed to `less`/Vim are forced to use arrow keys or mouse. |

---

## 3. Viewport Responsiveness Architecture

### 3.1 The `ChoiceCard` Custom Widget
To replace rigid `Button` widgets, we introduce `ChoiceCard(Static)` in `tui/widgets.py`:
- **Structure**:
  ```
  +-----------------------------------------------------------------------+
  | (1)  This is a detailed multi-line option that wraps cleanly across   |
  |      several lines of text without truncation or ellipses clipping... |
  +-----------------------------------------------------------------------+
  ```
- **Attributes**:
  - `can_focus = True`: Allows keyboard focus traversal via `Tab`/`Shift+Tab` and `j`/`k`.
  - TCSS styling:
    ```tcss
    ChoiceCard {
        width: 100%;
        height: auto;
        min-height: 3;
        padding: 0 1;
        margin-bottom: 1;
        background: $surface-0;
        color: $text-primary;
        border: round $surface-1;
    }
    ChoiceCard:hover {
        background: $surface-1;
        border: round $accent-cyan;
    }
    ChoiceCard:focus {
        background: $surface-1;
        border: round $accent-primary;
        text-style: bold;
    }
    ChoiceCard.choice-card-selected {
        background: $accent-primary;
        color: $crust;
    }
    ```
- **Behavior**:
  - Clicking on a `ChoiceCard` fires selection.
  - Pressing `Enter` or `Space` while focused selects that option.
  - Preserves direct hotkeys: pressing `1`, `2`, `3`, `4` on the parent screen immediately triggers the corresponding card.

### 3.2 Auto-Scroll on Answer Submission
When an answer is submitted in `QuestionWidget`:
1. The feedback label `#feedback` is updated with outcome and explanation (`why`).
2. If in `QuizScreen` or `StudyScreen`, `#next-btn` is mounted.
3. Immediately after mounting/updating, `call_after_refresh` triggers:
   ```python
   def _scroll_to_feedback(self) -> None:
       try:
           self.query_one("#feedback").scroll_visible(animate=True, top=False)
       except Exception:
           pass
   ```
This guarantees that regardless of question prompt length or code size, the terminal viewport smoothly scrolls down to display the result and next action.

### 3.3 Syntax Container Height Bounds
In `tui/style.tcss`, all syntax/code blocks embedded inside study and quiz views are given intelligent bounds:
```tcss
QuestionWidget Syntax, .study-example-box Syntax {
    max-height: 14;
    overflow-y: auto;
    overflow-x: auto;
    border: round $surface-1;
}
```
If a code snippet has 8 lines, it renders cleanly at height 8. If it has 40 lines, it caps at 14 rows with an internal scrollbar, preventing vertical blowout of the question layout.

### 3.4 Fluid Layouts for Small and Large Displays
- Replace fixed pixel/column widths with responsive percentages (`width: 90%; max-width: 86; min-width: 28;`).
- Master-detail views (`.master-detail-row`):
  - On terminals >= 100 columns: Sidebar 40%, Content 60%.
  - On terminals between 70 and 99 columns: Sidebar 45%, Content 55%.
  - On narrow/mobile terminals (< 70 columns): Automatically collapse to single-pane full-width view with toggle (`l`/`h` or `Tab`/`Shift+Tab`).
  - Content containers use `overflow-y: auto` with auto-wrapping markdown.

### 3.5 Termux & Mobile Environment Optimization
Mobile terminal emulators (Termux on Android, iSH on iOS) have distinct ergonomic constraints that `termlearn` actively accommodates:
1. **Narrow Portrait Viewports (36–55 columns)**:
   - On a phone held in portrait mode, widths frequently range between 38 and 50 columns.
   - Fixed character widths (such as the legacy `width: 72` in `.flashcard-frame`) cause severe horizontal overflow. All components are bound by responsive percentage widths (`width: 95%`) with small minimum bounds (`min-width: 28`), guaranteeing zero horizontal overflow.
   - Master-detail views (`HomeScreen`, `ChaptersScreen`) adaptively collapse when `terminal_width < 70`: the list and dossier panes become full-width (100%), and pressing `l` or `Tab` toggles to the dossier view while `h` or `Shift+Tab` toggles back to the list.
2. **Touch-Target Ergonomics**:
   - Termux translates touch taps into ANSI mouse events.
   - `ChoiceCard` enforces `min-height: 3` and `margin-bottom: 1`, providing ample thumb-friendly tap targets without misclicks.
3. **Termux Extra-Keys Bar Workflow**:
   - Mobile users frequently configure the Termux extra-keys bar (`ESC`, `TAB`, `CTRL`, `ALT`, `j`, `k`, `1`, `2`, `3`, `4`, `q`).
   - Because all core learning workflows are single-key (`1`–`4` for MCQ/cards, `j`/`k` for scrolling, `f`/`Space` for flip, `n` for next, `q` for back), users can complete entire study and quiz sessions with the software keyboard dismissed, reclaiming 100% of the screen height for book content.
4. **2x2 Responsive Grade Deck**:
   - In `CardsScreen`, the 4 grading buttons (`[1] Again`, `[2] Hard`, `[3] Good`, `[4] Easy`) cannot fit side-by-side on a 40-column phone screen.
   - Under narrow viewports (`width < 70`), the grade deck dynamically wraps into a 2x2 grid, keeping all 4 buttons large, legible, and comfortably tappable.
5. **Virtual Keyboard Overhead**:
   - When an on-screen keyboard is open (e.g., during Parsons line ordering or fill-in-the-blank), effective vertical height drops to ~12–15 lines.
   - Auto-scrolling to `#feedback` and input anchors ensures the active focus area is never concealed behind the keyboard.

---

## 4. Comprehensive TUI Screen Audit & Responsive Design Matrix

| Screen / Widget | Current Viewport Weakness | Responsiveness Fix | Vim Keybindings Added |
| :--- | :--- | :--- | :--- |
| **`HomeScreen`** | Fixed 42/58 split; right dossier cannot be scrolled with keyboard. | Fluid pane widths; right pane `#book-details` receives keyboard scroll focus. | `j`/`k`: navigate book list.<br>`l` or `Tab`: focus dossier pane.<br>`h` or `Shift+Tab`: return focus to book list.<br>`g`/`G`: first/last book.<br>In dossier: `j`/`k` (scroll), `d`/`u` (half page), `g`/`G` (top/bottom). |
| **`ChaptersScreen`** | Long lists of 28 chapters; dossier cannot be scrolled with keyboard. | Fluid pane widths; `#ch-details` scrollable via keyboard. | `j`/`k`: navigate chapters.<br>`l` or `Tab`: focus dossier pane.<br>`h` or `Shift+Tab`: return to chapter list.<br>`g`/`G`: first/last chapter.<br>In dossier: `j`/`k`, `d`/`u`, `g`/`G`. |
| **`ChapterMenu`** | Rigid 8-mode list box. | Fluid centering with max width 70 cols. | `j`/`k`: move selection.<br>`g`/`G`: top/bottom mode.<br>`l` or `Enter`: launch mode.<br>`h` or `q`: back to chapters. |
| **`StudyScreen`** | Long markdown blocks and code snippets push next action offscreen. | Constrain `Syntax` max-height to 14 rows; auto-scroll to feedback on check completion. | `j`/`k`: scroll content 2 lines.<br>`d`/`u`: scroll half page.<br>`g`/`G`: scroll top/bottom.<br>`n`/`p`: next/previous block (preserved). |
| **`QuizScreen`** | **CRITICAL**: MCQ buttons truncate long options; feedback renders below fold. | Replace `Button` with multi-line `ChoiceCard`; auto-scroll to `#feedback` on answer. | `j`/`k`: scroll question or move choice focus.<br>`1`-`4`: direct answer.<br>`Enter`/`Space`: answer focused card.<br>`d`/`u`: half-page scroll.<br>`g`/`G`: top/bottom scroll.<br>`n`: next question. |
| **`QuestionWidget`** | Button truncation; Distractor lines in Parsons order wrap awkwardly. | `ChoiceCard` with `text-wrap: wrap`; code blocks bounded; auto-scroll anchor. | Supports focus traversal across choices; keyboard selection with `Enter`/`Space`. |
| **`CardsScreen`** | Rigid 72x20 card frame overflows on small terminals and clips on large cards. | Fluid `.flashcard-frame`: `width: 90%; max-width: 82; max-height: 65vh; overflow-y: auto;`. | `Space` or `l` or `f`: flip card.<br>`j`/`k`: scroll card if long text.<br>`1`-`4` or `h`/`j`/`k`/`l` when flipped to grade.<br>`e`: edit card. |
| **`LabScreen`** | Fixed 38/62 split crushes instructions on narrow screens; console output clips. | Minimum pane widths; scrollable info and console panes. | When `#lab-code` (TextArea) is unfocused:<br>`j`/`k`: scroll instructions/console.<br>`Ctrl+W` or `Tab`: cycle focus between instructions, editor, and console. |
| **`ReviseScreen`** | Long document with 15+ block cards; hard to navigate with arrows. | Full-width scrollable container with card separators. | `j`/`k`: scroll 2 lines down/up.<br>`d`/`u`: scroll half page down/up.<br>`g`/`G`: jump to top/bottom.<br>`q`/`h`: back. |
| **`StatsScreen`** | KPI cards and two DataTables require scrolling. | Responsive KPI row wrap; keyboard focus between DataTables. | `j`/`k`: scroll analytics or move table row.<br>`d`/`u`: half page scroll.<br>`g`/`G`: top/bottom.<br>`Tab`: switch between Accuracy and Concepts table. |
| **`TestScreen`** | Fixed details card. | Fluid card width `width: 90%; max-width: 80;`. | `j`/`k`: scroll test report.<br>`q`/`h`: back. |

---

## 5. Vim Ergonomics & Keymap Specification

### 5.1 General Navigation Philosophy
1. **Modal Awareness**: When an `Input` (Parsons line order, fill-in-the-blank, edit card modal) or `TextArea` (code lab editor) is focused, alphanumeric keys MUST type text directly. Vim navigation is only active when non-text widgets are focused, or via explicit container bindings.
2. **Standard Mappings**:
   - `j`: Move down 1 item (lists) or scroll down 2 rows (containers).
   - `k`: Move up 1 item (lists) or scroll up 2 rows (containers).
   - `d` or `Ctrl+d`: Scroll down half-page (~12 rows).
   - `u` or `Ctrl+u`: Scroll up half-page (~12 rows).
   - `g`: Jump to top / first item.
   - `G`: Jump to bottom / last item.
   - `h`: Navigate back / focus left pane.
   - `l`: Enter / focus right pane / flip card.
3. **Preservation of TermLearn Direct Hotkeys (`VR-009`)**:
   - Number keys `1`-`4` in Quiz: instantly pick answer choice.
   - Number keys `1`-`8` in ChapterMenu: instantly open mode.
   - Number keys `1`-`4` in Cards: instantly grade card (Again/Hard/Good/Easy).
   - Single letters: `n` (next), `p` (prev), `r` (run), `t` (test), `f` (flip), `e` (edit), `q` (back/quit), `?` (help).

### 5.2 The `VimScrollMixin`
To ensure clean, DRY implementation without code duplication, we define `VimScrollMixin` in `tui/widgets.py`:
```python
class VimScrollMixin:
    """Provides standard Vim scrolling bindings for ScrollableContainer screens."""
    
    def action_vim_down(self) -> None:
        target = self.get_scroll_target()
        if target:
            target.scroll_relative(y=2, animate=False)

    def action_vim_up(self) -> None:
        target = self.get_scroll_target()
        if target:
            target.scroll_relative(y=-2, animate=False)

    def action_vim_pagedown(self) -> None:
        target = self.get_scroll_target()
        if target:
            step = max(4, target.size.height // 2)
            target.scroll_relative(y=step, animate=False)

    def action_vim_pageup(self) -> None:
        target = self.get_scroll_target()
        if target:
            step = max(4, target.size.height // 2)
            target.scroll_relative(y=-step, animate=False)

    def action_vim_top(self) -> None:
        target = self.get_scroll_target()
        if target:
            target.scroll_home(animate=False)

    def action_vim_bottom(self) -> None:
        target = self.get_scroll_target()
        if target:
            target.scroll_end(animate=False)
```

### 5.3 OptionList Vim Integration
For `HomeScreen` (`#book-list`), `ChaptersScreen` (`#ch-list`), and `ChapterMenu` (`#mode-list`):
- Textual's `OptionList` natively handles Up/Down.
- We add bindings to the enclosing screen:
  - `j` -> `action_cursor_down`
  - `k` -> `action_cursor_up`
  - `g` -> `action_cursor_first`
  - `G` -> `action_cursor_last`
- In master-detail screens (`HomeScreen`, `ChaptersScreen`):
  - `l` or `Tab`: Focus right dossier pane (`#book-details` or `#ch-details`).
  - `h` or `Shift+Tab`: Focus left list pane (`#book-list` or `#ch-list`).

---

## 6. Detailed Component Specifications

### 6.1 `ChoiceCard` Widget Implementation
File: `tui/widgets.py`
```python
class ChoiceCard(Static):
    """A focusable, multi-line choice card for multiple-choice questions."""
    can_focus = True

    class Selected(Message):
        """Posted when the card is selected by click, Enter, or Space."""
        def __init__(self, index: int) -> None:
            super().__init__()
            self.index = index

    def __init__(self, index: int, text: str, id: str | None = None) -> None:
        super().__init__(id=id, classes="choice-card")
        self.index = index
        self.raw_text = text

    def compose(self) -> ComposeResult:
        yield Label(f"({self.index})  {self.raw_text}", classes="choice-card-text")

    def on_click(self) -> None:
        self.post_message(self.Selected(self.index - 1))

    def on_key(self, event: events.Key) -> None:
        if event.key in ("enter", "space"):
            event.stop()
            self.post_message(self.Selected(self.index - 1))
```

### 6.2 Master-Detail Dual-Pane Focus Switching
File: `tui/screens.py` (`HomeScreen` & `ChaptersScreen`)
- Make the right dossier container focusable:
  ```python
  class DossierPane(Vertical):
      can_focus = True
      BINDINGS = [
          Binding("j", "scroll_down", "Down", show=False),
          Binding("k", "scroll_up", "Up", show=False),
          Binding("d", "page_down", "Half Page Down", show=False),
          Binding("u", "page_up", "Half Page Up", show=False),
          Binding("g", "scroll_top", "Top", show=False),
          Binding("G", "scroll_bottom", "Bottom", show=False),
      ]
  ```
- In `HomeScreen` / `ChaptersScreen`:
  - `action_switch_pane_right`: switches focus from list to dossier.
  - `action_switch_pane_left`: switches focus from dossier back to list.
  - Bound to `l` / `h` and `tab` / `shift+tab`.

### 6.3 Flashcard Frame Responsiveness
File: `tui/style.tcss`
```tcss
.cards-outer {
    align: center middle;
    height: 1fr;
    padding: 1;
    overflow-y: auto;
}

.flashcard-frame {
    width: 90%;
    max-width: 82;
    min-height: 12;
    height: auto;
    max-height: 65vh;
    background: $base;
    border: heavy $accent-primary;
    padding: 1 2;
    margin-bottom: 1;
    overflow-y: auto;
}
```

---

## 7. Verification and Compatibility Requirements

### 7.1 Preservation of Existing DOM IDs (`VR-009`)
All DOM IDs relied upon by `tests/test_tui.py` MUST be strictly preserved:
- `#book-list` (OptionList)
- `#ch-list` (OptionList)
- `#mode-list` (OptionList)
- `#body` (Vertical container in Study, Quiz, Cards)
- `#order-in`, `#fill-in`, `#micro-in` (Inputs in QuestionWidget)
- `#feedback` (Static feedback display)
- `#next-btn` (Button for next question)
- `#lab-code`, `#lab-out` (TextArea and output in Lab)

### 7.2 Existing Test Suite Integrity
- All existing tests in `tests/test_tui.py` MUST continue to pass.
- Decouple hardcoded counts in tests so adding future chapter packs does not cause brittle assertion failures.
- New automated tests will be added:
  1. `test_choice_card_multi_line_wrapping`: verify options with >100 characters render without truncation.
  2. `test_vim_scrolling_in_screens`: verify `j`/`k`, `d`/`u`, `g`/`G` scroll containers in `StudyScreen`, `QuizScreen`, and `ReviseScreen`.
  3. `test_master_detail_pane_switching`: verify `l` and `h` switch focus between `#book-list`/`#ch-list` and the dossier pane.
  4. `test_quiz_feedback_auto_scroll`: verify feedback scroll anchor activates upon answering.

---

## 8. Implementation Steps

1. **Step 1: CSS Overhaul (`tui/style.tcss`)**:
   - Add `.choice-card` styles (multi-line, hover, focus, selected).
   - Add responsive fluid limits to `.flashcard-frame` and `.content-pane`.
   - Add `max-height: 14; overflow-y: auto;` to `Syntax` blocks inside questions.
2. **Step 2: `ChoiceCard` & Auto-Scroll (`tui/widgets.py`)**:
   - Implement `ChoiceCard` with `can_focus = True` and text wrap.
   - Update `QuestionWidget` to compose `ChoiceCard` instead of `Button`.
   - Implement smooth auto-scroll to `#feedback` upon answer submission.
3. **Step 3: Vim Keymaps & Mixins (`tui/widgets.py`, `tui/practice.py`, `tui/screens.py`)**:
   - Implement `VimScrollMixin` and attach to `StudyScreen`, `QuizScreen`, `ReviseScreen`, `StatsScreen`, `TestScreen`.
   - Add `j`/`k`/`g`/`G` bindings and `h`/`l` pane switching to `HomeScreen`, `ChaptersScreen`, and `ChapterMenu`.
   - Add card-flip Vim bindings (`Space`/`l`/`f` to flip, `h`/`j`/`k`/`l` for grades) to `CardsScreen`.
4. **Step 4: Automated Testing & Verification**:
   - Run `pytest` across entire suite.
   - Add unit tests for `ChoiceCard` and Vim keybindings in `tests/test_tui.py`.

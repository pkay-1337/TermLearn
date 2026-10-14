"""Textual TUI for termlearn. Same packs, same lib data/persistence layer as the
Rich CLI (SRS IF-TUI-001..006); only the presentation is new.

- Packs are read, never rewritten, by this package.
- Every interactive screen keeps the CLI keybindings as aliases (IF-TUI-002).
- The Footer on each screen is the persistent hint bar (IF-TUI-003);
  `?` opens the key overlay anywhere (IF-TUI-003).
- The Rich CLI remains the `--plain` linear mode (IF-TUI-006).
"""

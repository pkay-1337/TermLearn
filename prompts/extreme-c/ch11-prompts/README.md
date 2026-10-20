# AI Generation Prompts for extreme-c / ch11

### Source Asset Locations (Where to Find Chapter Data):
- **Raw Extracted Chapter Text**: `books/extreme-c/raw_chapters/ch11.txt`
- **Book Metadata & TOC**: `books/extreme-c/meta.json`
- **Book Toolchain & Config**: `packs/extreme-c/book.yaml`
- **Target Chapter Output Directory**: `packs/extreme-c/ch11/`

### Available Prompts in this Bundle:
1. **`01_meta.md`** → generates `packs/extreme-c/ch11/meta.yaml`
2. **`02_study.md`** → generates `packs/extreme-c/ch11/study.yaml`
3. **`03_quiz.md`** → generates `packs/extreme-c/ch11/quiz.yaml`
4. **`04_labs.md`** → generates `packs/extreme-c/ch11/labs.yaml`
5. **`05_cards.md`** → generates `packs/extreme-c/ch11/cards.yaml`
6. **`06_test.md`** → generates `packs/extreme-c/ch11/test.yaml`

### For Autonomous Coding Agents (Claude Code, Antigravity, Cursor, Codex):
Feed **`master_prompt.md`** directly to the agent. It reads `books/extreme-c/raw_chapters/ch11.txt`,
creates `packs/extreme-c/ch11/`, and sequentially authors and validates all 6 mode files.

### Verification:
```bash
python main.py validate --book extreme-c --chapter ch11 --strict
```

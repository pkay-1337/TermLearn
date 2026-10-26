# AI Generation Prompts for bgnet / ch03

### Source Asset Locations (Where to Find Chapter Data):
- **Raw Extracted Chapter Text**: `books/bgnet/raw_chapters/ch03.txt`
- **Verbatim copy in this bundle**: `chapter.txt`
- **Book Metadata & TOC**: `books/bgnet/meta.json`
- **Book Toolchain & Config**: `packs/bgnet/book.yaml`
- **Target Chapter Output Directory**: `packs/bgnet/ch03/`

### Available Prompts in this Bundle:
1. **`01_meta.md`** → generates `packs/bgnet/ch03/meta.yaml`
2. **`02_study.md`** → generates `packs/bgnet/ch03/study.yaml`
3. **`03_quiz.md`** → generates `packs/bgnet/ch03/quiz.yaml`
4. **`04_labs.md`** → generates `packs/bgnet/ch03/labs.yaml`
5. **`05_cards.md`** → generates `packs/bgnet/ch03/cards.yaml`
6. **`06_test.md`** → generates `packs/bgnet/ch03/test.yaml`

### For Autonomous Coding Agents (Claude Code, Antigravity, Cursor, Codex):
Feed **`master_prompt.md`** directly to the agent. It reads `books/bgnet/raw_chapters/ch03.txt`,
creates `packs/bgnet/ch03/`, and sequentially authors and validates all 6 mode files.

### Verification:
```bash
python main.py validate --book bgnet --chapter ch03 --strict
```

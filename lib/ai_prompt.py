"""gen-prompt emitter: GENERATE.md + ASK_USER.md + chapter text, chunked,
plus normative docs/SRS.md excerpts (FR-GEN-001: self-contained prompt).

Supports modular mode generation (--mode meta|study|quiz|labs|cards|test|master|all|legacy)
and prompt bundle export to prompts/<book>/<chapter>-prompts/.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUDGET = 12000
OVERLAP = 500

VALID_MODES = ("meta", "study", "quiz", "labs", "cards", "test", "master", "all", "legacy")


def chunk(text: str, budget: int = BUDGET, overlap: int = OVERLAP) -> list[str]:
    if len(text) <= budget:
        return [text]
    parts, i = [], 0
    while i < len(text):
        parts.append(text[i:i + budget])
        i += budget - overlap
    return parts


def extract_marked(path: Path, begin: str, end: str) -> str:
    """Slice lines between marker comments (prefix match). Raises KeyError
    if markers are missing or misordered — a loud failure, never silent."""
    lines = path.read_text(encoding="utf-8").splitlines()
    bi = next((i for i, l in enumerate(lines) if begin in l), None)
    ei = next((i for i, l in enumerate(lines) if end in l), None)
    if bi is None or ei is None or ei <= bi:
        raise KeyError(f"markers {begin!r}..{end!r} missing/misordered in {path}")
    return "\n".join(lines[bi:ei + 1])


def normative_excerpts() -> str:
    srs = ROOT / "docs" / "SRS.md"
    schema = extract_marked(srs, "SCHEMA-BEGIN", "SCHEMA-END")
    proto = extract_marked(srs, "RUNNER-PROTOCOL-BEGIN", "RUNNER-PROTOCOL-END")
    return schema + "\n\n" + proto


def _src_info(book: str, chapter: str) -> str:
    dir_path = f"packs/{book}/{chapter}"
    source_file = f"books/{book}/raw_chapters/{chapter}.txt"
    book_meta = f"books/{book}/meta.json"
    book_config = f"packs/{book}/book.yaml"
    return (
        f"# [SOURCE ASSET LOCATIONS — WHERE TO FIND CHAPTER DATA]\n"
        f"# 1. Extracted Chapter Text: {source_file}\n"
        f"#    (This is the single source of truth; the full chapter text is NOT embedded\n"
        f"#     in this prompt — read it from the raw file above, or from chapter.txt in\n"
        f"#     the prompt bundle directory.)\n"
        f"# 2. Book Table of Contents & Metadata: {book_meta}\n"
        f"# 3. Book Toolchain & Course Pack Config: {book_config}\n"
        f"#\n"
    )


def _get_mode_header(book: str, chapter: str, mode: str) -> str:
    """Mode-specific header only (target file + directives + verification tail).
    No GENERATE.md, no ASK_USER.md, no SRS excerpts, no chapter text — those
    live in master_prompt.md."""
    dir_path = f"packs/{book}/{chapter}"
    source_file = f"books/{book}/raw_chapters/{chapter}.txt"
    book_config = f"packs/{book}/book.yaml"

    if mode == "meta":
        return (
            f"# =============================================================================\n"
            f"# INSTRUCTIONS FOR AI AGENT / CHAT: CHAPTER METADATA & OBJECTIVES\n"
            f"# TARGET OUTPUT FILE: {dir_path}/meta.yaml\n"
            f"#\n"
            f"# [DIRECTIVES FOR meta.yaml]\n"
            f"# 1. Read the full chapter text from `{source_file}` (see master_prompt.md).\n"
            f"# 2. Enumerate all core idea units in the chapter (concepts, mechanics, procedures).\n"
            f"# 3. Identify prerequisites from previous chapters (or [] if none).\n"
            f"# 4. Formulate 1 to 6 falsifiable, measurable learning objectives.\n"
            f"# 5. OUTPUT FORMAT (exact YAML mapping inside a single yaml code fence):\n"
            f"#    meta:\n"
            f"#      book: {book}\n"
            f"#      chapter_id: {chapter}\n"
            f"#      title: \"Descriptive Chapter Title\"\n"
            f"#      source_ref: \"Ch.X pp.Y-Z\"\n"
            f"#      level: intro | core | advanced\n"
            f"#      prereqs: []\n"
            f"#    objectives:\n"
            f"#      - \"Observable skill/mastery 1\"\n"
            f"#      - \"Observable skill/mastery 2\"\n"
        )
    elif mode == "study":
        return (
            f"# =============================================================================\n"
            f"# INSTRUCTIONS FOR AI AGENT / CHAT: CONCEPT BLOCKS & STUDY CONTENT\n"
            f"# TARGET OUTPUT FILE: {dir_path}/study.yaml\n"
            f"#\n"
            f"# [DIRECTIVES FOR study.yaml]\n"
            f"# 1. Read the chapter from `{source_file}` (see master_prompt.md).\n"
            f"# 2. Dedicate your full cognitive might to deep, pedagogical explanations.\n"
            f"# 3. Break the chapter into as many single-concept blocks as needed ('blocks: [...]'); no set count — one block per concept.\n"
            f"# 4. For each block:\n"
            f"#    - 'id': unique block id ('b1', 'b2', ...)\n"
            f"#    - 'type': 'model' | 'syntax' | 'design' | 'algorithm'\n"
            f"#    - 'title': functional, action-oriented concept title\n"
            f"#    - 'explain_md': rich, intuitive Markdown explanation (5–20 lines) breaking down\n"
            f"#      syntax, Notional Machine state transitions, and memory lifecycle.\n"
            f"#    - 'example': runnable code snippet with 'run_expected' stdout; non-trivial code MUST also\n"
            f"#      carry 'explain_md' (2–6 lines of Markdown rendered right under the code); optional 'subgoals'\n"
            f"#    - 'diagram': OPTIONAL block-level structure picture for model/design blocks with non-memory\n"
            f"#      structure (call graph, data flow, layering) — kind: flow (nodes/edges, ids unique, refs\n"
            f"#      resolvable, ≤14 nodes) or kind: art (verbatim ASCII, no ANSI); optional caption + steps ≤6\n"
            f"#    - 'viz': stepped ASCII memory diagrams for every 'model' block (2–6 steps).\n"
            f"#    - 'checks': 5 to 10 scaffolded micro-checks per block ('predict', 'why-fails',\n"
            f"#      'mcq', 'fillblank', 'order' with 'faded: true', 'eipe', 'choose-better', 'trace', 'spot-bug').\n"
            f"#      Every check MUST have an elaborated 'why:' explaining the principle and diagnosing distractors.\n"
            f"# 5. OUTPUT FORMAT: Single YAML document with top-level 'blocks: [...]'.\n"
            f"#\n"
            f"# [POST-GENERATION VERIFICATION FOR study.yaml]\n"
            f"# - Runnable code: every blocks[].example.code compiles under {book_config}: toolchain.\n"
            f"# - If run_expected is declared, it matches actual output for a correct solution.\n"
            f"# - Model blocks have viz; design blocks have eipe/choose-better; syntax/algorithm blocks have order.\n"
            f"# - Every non-trivial example.code has explain_md; diagram stanzas (if any) use exact vocabularies.\n"
            f"# - Each check carries rules 1.1–1.10 (positively-worded, randomized answers, embedded code, elaborated why).\n"
        )
    elif mode == "quiz":
        return (
            f"# =============================================================================\n"
            f"# INSTRUCTIONS FOR AI AGENT / CHAT: CHAPTER QUIZ QUESTIONS\n"
            f"# TARGET OUTPUT FILE: {dir_path}/quiz.yaml\n"
            f"#\n"
            f"# [DIRECTIVES FOR quiz.yaml]\n"
            f"# 1. Read the chapter from `{source_file}` (see master_prompt.md).\n"
            f"# 2. Author 30 to 50 dedicated, standalone diagnostic questions testing cumulative synthesis.\n"
            f"# 3. Distribute questions across three difficulty levels: 'level: intro | core | advanced'.\n"
            f"# 4. Mix question kinds: 'mcq', 'predict', 'why-fails', 'fillblank', 'order', 'trace', 'spot-bug'.\n"
            f"# 5. SELF-CONTAINED CODE: Whenever testing code behavior or bugs, embed the code snippet directly\n"
            f"#    in the question via 'code: |'. Never reference external book exercise numbers or listings.\n"
            f"# 6. ANSWER RANDOMIZATION: Uniformly distribute correct answer positions across 0, 1, 2, and 3.\n"
            f"# 7. ELABORATED WHY: Every question MUST provide a comprehensive 'why:' explaining the core rule\n"
            f"#    and naming the exact misconception each wrong distractor traps.\n"
            f"# 8. OUTPUT FORMAT: Single YAML document with top-level 'quiz: [...]'.\n"
            f"#\n"
            f"# [POST-GENERATION VERIFICATION FOR quiz.yaml]\n"
            f"# - Count: 30–50 questions.\n"
            f"# - Levels: intro + core + advanced all present.\n"
            f"# - No duplicates: no q string identical to any block-check q.\n"
            f"# - Mixed: not grouped by level or concept.\n"
            f"# - Concept coverage: distinct concepts span core chapter topics (e.g. composition, aggregation, ownership, diagnostics).\n"
            f"# - Each item carries 1.1–1.10 (positively worded, 2-4 choices, answer in bounds, randomized answer index,\n"
            f"#   self-contained with embedded code, elaborated why, exact kinds, scrambled order, load-bearing fillblank, prose width <=120 cols).\n"
        )
    elif mode == "labs":
        return (
            f"# =============================================================================\n"
            f"# INSTRUCTIONS FOR AI AGENT / CHAT: PRACTICAL LAB WORKSPACES\n"
            f"# TARGET OUTPUT FILE: {dir_path}/labs.yaml\n"
            f"#\n"
            f"# [DIRECTIVES FOR labs.yaml]\n"
            f"# 1. Read the chapter from `{source_file}` (see master_prompt.md).\n"
            f"# 2. Author 1 to 4 practical, multi-file coding challenges.\n"
            f"# 3. STUDENT ACTION REQUIRED — NEVER EMIT PRE-SOLVED SOLUTIONS:\n"
            f"#    - Student implementation files MUST BE SCAFFOLDED OR BLANK (empty string, stubs, '/* TODO */').\n"
            f"#    - Supporting framework files (headers '.h', interactive drivers 'main.c', and unit test runners\n"
            f"#      'test_runner.c') provide the deterministic assertions.\n"
            f"# 4. Initial verification test MUST fail on unedited starter files, and pass once implemented.\n"
            f"# 5. Provide language-agnostic commands ('run' and 'test'), automated 'test_cases' with unified diffs,\n"
            f"#    and 1–3 progressive hints (general -> specific).\n"
            f"# 6. OUTPUT FORMAT: Single YAML document with top-level 'labs: [...]'.\n"
            f"#\n"
            f"# [POST-GENERATION VERIFICATION FOR labs.yaml]\n"
            f"# - Contract: each lab has id, title, instruction_md, non-empty safe files, commands.run/test, test_cases[].expect, progressive hints.\n"
            f"# - Blank starters: implementation file(s) content: \"\" or TODO-stubbed; headers/drivers/test-runners complete.\n"
            f"# - Fail-first: running commands.test on the untouched starter must FAIL (missing symbols/compile error).\n"
            f"# - Safe commands: no denylisted patterns (rm -rf, curl, wget, ssh, mkfs, fork bombs); no network.\n"
            f"# - Hints ordered: general -> specific -> operation.\n"
            f"# - Code lines: no line-count or column caps — include as much as the lab needs.\n"
            f"# - Cannot be fully automated (need a solution trace):\n"
            f"#   * commands.run output byte-matches test_cases[].expect for a reference solution.\n"
            f"#   * Fail->pass lifecycle verified with a real reference implementation.\n"
        )
    elif mode == "cards":
        return (
            f"# =============================================================================\n"
            f"# INSTRUCTIONS FOR AI AGENT / CHAT: SPACED REPETITION FLASHCARDS (SM-2)\n"
            f"# TARGET OUTPUT FILE: {dir_path}/cards.yaml\n"
            f"#\n"
            f"# [DIRECTIVES FOR cards.yaml]\n"
            f"# 1. Read the chapter from `{source_file}` (see master_prompt.md).\n"
            f"# 2. Author as many atomic flashcards as needed for durable concepts, rules, syntax, and memory models (no set count).\n"
            f"# 3. Each card must be answerable in <10s: front = concise prompt; back = answer + 1-line 'why'.\n"
            f"# 4. Include 'why/when' conceptual cards ('When must X be used?') alongside 'what' cards.\n"
            f"# 5. Assign a descriptive 'concept:' tag to each card for telemetry tracking.\n"
            f"# 6. OUTPUT FORMAT: Single YAML document with top-level 'cards: [...]'.\n"
        )
    elif mode == "test":
        return (
            f"# =============================================================================\n"
            f"# INSTRUCTIONS FOR AI AGENT / CHAT: CHAPTER MASTERY TEST GATES\n"
            f"# TARGET OUTPUT FILE: {dir_path}/test.yaml\n"
            f"#\n"
            f"# [DIRECTIVES FOR test.yaml]\n"
            f"# 1. Define mastery gate criteria referencing prerequisite concept blocks and minimum quiz accuracy.\n"
            f"# 2. OUTPUT FORMAT:\n"
            f"#    test:\n"
            f"#      gates:\n"
            f"#        - needs: [b1, b2, b3]\n"
            f"#          min_quiz: 80\n"
            f"#      final_checks: []\n"
        )
    elif mode == "master":
        return (
            f"# =============================================================================\n"
            f"# INSTRUCTIONS FOR AUTONOMOUS AI AGENTS & CODING ASSISTANTS:\n"
            f"# TARGET DIRECTORY: {dir_path}/\n"
            f"#\n"
            f"{_src_info(book, chapter)}"
            f"# [MANDATORY DIRECTIVES FOR MODULAR CHAPTER GENERATION]\n"
            f"# DO NOT write a single monolithic chNN.yaml file!\n"
            f"# Instead, create directory '{dir_path}/' and author focused, modular YAML files:\n"
            f"#\n"
            f"# Step 1: Write '{dir_path}/meta.yaml' (metadata, prerequisites, 1–6 objectives)\n"
            f"# Step 2: Write '{dir_path}/study.yaml' (as many concept blocks as needed, Notional Machine viz, micro-checks)\n"
            f"# Step 3: Write '{dir_path}/quiz.yaml' (30–50 standalone diagnostic questions across difficulty levels)\n"
            f"# Step 4: Write '{dir_path}/labs.yaml' (1–4 multi-file coding projects with stubs & test harnesses)\n"
            f"# Step 5: Write '{dir_path}/cards.yaml' (as many atomic SM-2 flashcards as needed)\n"
            f"# Step 6: Write '{dir_path}/test.yaml' (mastery gates and certification criteria)\n"
            f"#\n"
            f"# [POST-GENERATION TESTING PROTOCOL (MUST TEST AFTER CREATING YAMLS)]\n"
            f"# 1. Block checks & questions: each item carries 1.1–1.10.\n"
            f"# 2. Quiz stanza (if quiz: present / quiz.yaml):\n"
            f"#    - Count 30–50.\n"
            f"#    - Levels intro + core + advanced all present.\n"
            f"#    - No duplicates — no q string identical to any block-check q.\n"
            f"#    - Mixed — not grouped by level or concept.\n"
            f"#    - Concept coverage — distinct concepts span core chapter topics (e.g. composition, aggregation, ownership, diagnostics).\n"
            f"#    - Each item carries 1.1–1.10.\n"
            f"# 3. Labs (if labs: present / labs.yaml):\n"
            f"#    - Contract — each lab has id, title, instruction_md, non-empty safe files, commands.run/test, test_cases[].expect, progressive hints.\n"
            f"#    - Blank starters — implementation file(s) content: \"\" or TODO-stubbed; headers/drivers/test-runners complete.\n"
            f"#    - Fail-first — running commands.test on the untouched starter must FAIL (missing symbols/compile error).\n"
            f"#    - Safe commands — no denylisted patterns (rm -rf, curl, wget, ssh, mkfs, fork bombs); no network.\n"
            f"#    - Hints ordered general -> specific -> operation.\n"
            f"#    - Code lines: no line-count or column caps — include as much as the lab needs.\n"
            f"# 4. Runnable code (all packs / study.yaml):\n"
            f"#    - Every blocks[].example.code compiles under {book_config}: toolchain.\n"
            f"#    - If run_expected is declared, it matches actual output for a correct solution.\n"
            f"#    - Every non-trivial example.code has explain_md (2–6 lines rendered under the code).\n"
            f"#    - diagram stanzas (if any) valid: kind flow|art; refs resolvable; steps ≤6; art ANSI-free.\n"
            f"#    - Model blocks have viz; design blocks have eipe/choose-better; syntax/algorithm blocks have order.\n"
            f"# 5. Cannot be fully automated (need a solution trace):\n"
            f"#    - commands.run output byte-matches test_cases[].expect for a reference solution.\n"
            f"#    - Fail->pass lifecycle verified with a real reference implementation.\n"
            f"# 6. Automated Validation Command:\n"
            f"#    python main.py validate --book {book} --chapter {chapter} --strict\n"
        )
    else:  # legacy monolithic
        return (
            f"# =============================================================================\n"
            f"# INSTRUCTIONS FOR AI AGENTS: MONOLITHIC PACK\n"
            f"# TARGET OUTPUT FILE: packs/{book}/{chapter}.yaml\n"
            f"#\n"
            f"{_src_info(book, chapter)}"
            f"# [POST-GENERATION TESTING PROTOCOL (MUST TEST AFTER CREATING YAML)]\n"
            f"# 1. Block checks & questions: each item carries 1.1–1.10.\n"
            f"# 2. Quiz stanza: Count 30–50; intro+core+advanced; no duplicates; mixed; concept coverage.\n"
            f"# 3. Labs: Contract; blank starters; fail-first; safe commands; hints general->specific->operation; no code-length caps.\n"
            f"# 4. Runnable code: compiles under toolchain; run_expected matches stdout; non-trivial examples carry explain_md; diagram stanzas valid; model has viz, design has eipe, syntax has order.\n"
            f"# 5. Cannot be fully automated: commands.run matches test_cases[].expect; fail->pass verified with reference solution.\n"
            f"# 6. Run: python main.py validate --book {book} --chapter {chapter} --strict\n"
        )


def _common_block(book: str, chapter: str) -> str:
    """Shared normative content: GENERATE.md + ASK_USER.md + SRS excerpts +
    chapter-content pointer. Lives only in master_prompt.md."""
    gen = (ROOT / "prompts" / "GENERATE.md").read_text(encoding="utf-8")
    ask = (ROOT / "prompts" / "ASK_USER.md").read_text(encoding="utf-8")
    source_rel = f"books/{book}/raw_chapters/{chapter}.txt"
    raw = ROOT / source_rel
    if not raw.exists():
        raise FileNotFoundError(f"no extracted text: {raw} — run extract first")
    return (
        f"{gen}\n---\n{ask}\n---\n"
        f"{normative_excerpts()}\n---\n"
        f"# =============================================================================\n"
        f"# CHAPTER CONTENT: {chapter} OF {book}\n"
        f"# The full chapter text is NOT embedded in this prompt.\n"
        f"# Read it from: {source_rel}\n"
        f"# (A verbatim copy ships in the prompt bundle as chapter.txt)\n"
        f"# MODE TARGET: {chapter.upper() if False else 'MASTER'}\n"
        f"# =============================================================================\n"
    )


def _mode_pointer(book: str, chapter: str) -> str:
    """Pointer from a mode-specific file to master_prompt.md for common rules."""
    source_rel = f"books/{book}/raw_chapters/{chapter}.txt"
    return (
        f"#\n"
        f"# COMMON RULES: see master_prompt.md for GENERATE.md, ASK_USER.md,\n"
        f"# the SRS §4.8 / §4.9 excerpts, and the chapter source assets.\n"
        f"# Chapter text: {source_rel}\n"
        f"# (A verbatim copy ships in this prompt bundle as chapter.txt)\n"
    )


def build_prompt(book: str, chapter: str, mode: str = "master") -> str:
    header = _get_mode_header(book, chapter, mode)
    if mode == "master":
        return header + _common_block(book, chapter)
    return header + _mode_pointer(book, chapter) + f"# MODE TARGET: {mode.upper()}\n# =============================================================================\n"


def emit_prompt_bundle(book: str, chapter: str, dest_dir: Path | str | None = None) -> Path:
    """Generate all individual mode prompts + master prompt into a dedicated bundle folder.
    
    Target location: prompts/<book>/<chapter>-prompts/
    """
    if dest_dir:
        base = Path(dest_dir)
    else:
        base = ROOT / "prompts" / book / f"{chapter}-prompts"
    base.mkdir(parents=True, exist_ok=True)

    # Copy the raw chapter text into the bundle as the single source of truth.
    raw = ROOT / "books" / book / "raw_chapters" / f"{chapter}.txt"
    if raw.exists():
        (base / "chapter.txt").write_text(raw.read_text(encoding="utf-8"), encoding="utf-8")

    mode_files = [
        ("01_meta.md", "meta"),
        ("02_study.md", "study"),
        ("03_quiz.md", "quiz"),
        ("04_labs.md", "labs"),
        ("05_cards.md", "cards"),
        ("06_test.md", "test"),
        ("master_prompt.md", "master"),
    ]

    for fname, mode in mode_files:
        content = build_prompt(book, chapter, mode=mode)
        (base / fname).write_text(content, encoding="utf-8")

    readme = (
        f"# AI Generation Prompts for {book} / {chapter}\n\n"
        f"### Source Asset Locations (Where to Find Chapter Data):\n"
        f"- **Raw Extracted Chapter Text**: `books/{book}/raw_chapters/{chapter}.txt`\n"
        f"- **Verbatim copy in this bundle**: `chapter.txt`\n"
        f"- **Book Metadata & TOC**: `books/{book}/meta.json`\n"
        f"- **Book Toolchain & Config**: `packs/{book}/book.yaml`\n"
        f"- **Target Chapter Output Directory**: `packs/{book}/{chapter}/`\n\n"
        f"### Available Prompts in this Bundle:\n"
        f"1. **`01_meta.md`** → generates `packs/{book}/{chapter}/meta.yaml`\n"
        f"2. **`02_study.md`** → generates `packs/{book}/{chapter}/study.yaml`\n"
        f"3. **`03_quiz.md`** → generates `packs/{book}/{chapter}/quiz.yaml`\n"
        f"4. **`04_labs.md`** → generates `packs/{book}/{chapter}/labs.yaml`\n"
        f"5. **`05_cards.md`** → generates `packs/{book}/{chapter}/cards.yaml`\n"
        f"6. **`06_test.md`** → generates `packs/{book}/{chapter}/test.yaml`\n\n"
        f"### For Autonomous Coding Agents (Claude Code, Antigravity, Cursor, Codex):\n"
        f"Feed **`master_prompt.md`** directly to the agent. It reads `books/{book}/raw_chapters/{chapter}.txt`,\n"
        f"creates `packs/{book}/{chapter}/`, and sequentially authors and validates all 6 mode files.\n\n"
        f"### Verification:\n"
        f"```bash\n"
        f"python main.py validate --book {book} --chapter {chapter} --strict\n"
        f"```\n"
    )
    (base / "README.md").write_text(readme, encoding="utf-8")
    return base


def emit(book: str, chapter: str, mode: str = "master", out: str | None = None):
    mode = mode.lower()
    if mode not in VALID_MODES:
        raise ValueError(f"unknown mode {mode!r}, choose from {VALID_MODES}")

    if mode == "all":
        dest = emit_prompt_bundle(book, chapter, dest_dir=out)
        print(f"Generated all prompt files in {dest}")
        return

    prompt = build_prompt(book, chapter, mode=mode)
    if out:
        p = Path(out)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(prompt, encoding="utf-8")
        # place a verbatim chapter copy next to the emitted prompt
        raw = ROOT / "books" / book / "raw_chapters" / f"{chapter}.txt"
        if raw.exists():
            (p.parent / "chapter.txt").write_text(raw.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"wrote {out} ({len(prompt)} chars, mode={mode})")
    else:
        print(prompt)

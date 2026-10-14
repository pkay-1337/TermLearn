"""gen-prompt emitter: GENERATE.md + ASK_USER.md + chapter text, chunked,
plus normative docs/SRS.md excerpts (FR-GEN-001: self-contained prompt)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUDGET = 12000
OVERLAP = 500


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


def build_prompt(book: str, chapter: str) -> str:
    gen = (ROOT / "prompts" / "GENERATE.md").read_text(encoding="utf-8")
    ask = (ROOT / "prompts" / "ASK_USER.md").read_text(encoding="utf-8")
    raw = ROOT / "books" / book / "raw_chapters" / f"{chapter}.txt"
    if not raw.exists():
        raise FileNotFoundError(f"no extracted text: {raw} — run extract first")
    text = raw.read_text(encoding="utf-8")
    parts = chunk(text)
    target_path = f"packs/{book}/{chapter}.yaml"
    agent_header = (
        f"# =============================================================================\n"
        f"# INSTRUCTIONS FOR AI AGENTS & CODING ASSISTANTS:\n"
        f"# TARGET OUTPUT FILE: {target_path}\n"
        f"#\n"
        f"# [MANDATORY DIRECTIVES — READ CAREFULLY BEFORE WRITING A SINGLE LINE]\n"
        f"# 1. PUT ALL YOUR MIGHT & GO PLUS ULTRA (NO HALF-ASSING):\n"
        f"#    The learner studies ONLY from your generated YAML, never from the book.\n"
        f"#    Produce a masterwork of pedagogical engineering grounded in cognitive science.\n"
        f"#    Zero placeholders (NO 'TODO', NO '/* rest of code */', NO lazy hand-waving).\n"
        f"# 2. DO NOT WORRY ABOUT LENGTH — DEPTH AND CLARITY OVERRIDE BREVITY:\n"
        f"#    Never rush, compress, or omit blocks to save tokens. An exhaustive, deeply explained\n"
        f"#    pack with 8–15 blocks and 30+ checks is vastly superior to a short summary.\n"
        f"# 3. MULTI-TURN / MULTI-STEP GENERATION SUPPORTED & ENCOURAGED:\n"
        f"#    If the chapter is concept-dense or has many blocks, DO NOT attempt to crush everything\n"
        f"#    into one rushed output. Write the file incrementally using your file tools (e.g.\n"
        f"#    create skeleton + blocks 1–4, then append blocks 5–8, blocks 9–12, cards, lab, and test),\n"
        f"#    or in sequential parts if in chat. Take as many turns/steps as needed to do it justice.\n"
        f"# 4. COMPREHENSIVE CODE EXPLANATIONS & NOTIONAL MACHINE:\n"
        f"#    Every single code snippet MUST be accompanied by an exhaustive, intuitive breakdown:\n"
        f"#    line-by-line syntax, Notional Machine state transitions (stack, heap, pointers, registers),\n"
        f"#    the architectural 'why' behind the design, and boundary failure traps.\n"
        f"# 5. INTUITION-FIRST COMPREHENSIBILITY:\n"
        f"#    Bridge technical jargon with intuitive mental models and physical analogies before\n"
        f"#    introducing formal syntax. Make every concept deeply understandable for self-study.\n"
        f"# 6. EXECUTION & VALIDATION PROTOCOL:\n"
        f"#    - Autonomous Agents with Tools: Write/edit directly to `{target_path}`.\n"
        f"#      Then execute: python main.py validate --book {book} --chapter {chapter} --strict\n"
        f"#    - Chat-Only Interfaces: Output in ```yaml``` fenced blocks (or sequential parts) and\n"
        f"#      direct the user to save to `{target_path}`.\n"
        f"# =============================================================================\n\n"
    )
    out = [agent_header,
           gen, "\n---\n", ask, "\n---\n",
           normative_excerpts(), "\n---\n",
           f"# CHAPTER {chapter} OF {book} ({len(parts)} part(s))",
           f"# TARGET FILE DESTINATION: {target_path}",
           f"# Process: answer ASK_USER questions first, then emit/write YAML to `{target_path}`.\n"]
    for n, p in enumerate(parts, 1):
        out.append(f"\n## part {n}/{len(parts)}\n\n{p}\n")
    return "\n".join(out)


def emit(book: str, chapter: str, out: str | None = None):
    prompt = build_prompt(book, chapter)
    if out:
        Path(out).write_text(prompt, encoding="utf-8")
        print(f"wrote {out} ({len(prompt)} chars)")
    else:
        print(prompt)

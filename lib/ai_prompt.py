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
        f"# - If you have tools to create/write files (e.g. write_to_file, bash, fs tools):\n"
        f"#   CREATE and write the generated YAML pack directly to `{target_path}`.\n"
        f"#   Then run: python main.py validate --book {book} --chapter {chapter} --strict\n"
        f"# - If you are in a chat-only interface without file-writing tools:\n"
        f"#   Output the YAML in exactly ONE ```yaml``` block and direct the user to save it to `{target_path}`.\n"
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

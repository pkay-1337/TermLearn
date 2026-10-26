"""EPUB -> raw_chapters/*.txt + meta.json. (SRS FR-EXT-001..006)

Runnable standalone:
    python -m lib.epub_extract books/<slug>/source.epub --out books/<slug> [--force]
Or via:
    python main.py extract --book <slug> [--force]
"""
import argparse
import datetime
import json
import re
import shutil
import unicodedata
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).resolve().parents[1]
CHAR_BUDGET_NOTE = 12000  # gen-prompt chunks here; extractor itself is lossless


def _clean(s: str) -> str:
    # strip zero-width chars (Extreme C title has U+200B), normalize spaces
    s = unicodedata.normalize("NFKC", s or "")
    s = s.replace("\u200b", "").replace("\u200c", "").replace("\ufeff", "")
    s = re.sub(r"[ \t]+", " ", s)
    return s.strip()


# Metadata-only: drop parentheticals that are empty or a bare connector word
# left over from publisher templates like "Title (for <brand>)" with a blank
# brand (FR-EXT-001). Real parentheticals with extra words are kept.
_EMPTY_PAREN = re.compile(r"\s*\(\s*(?:for|by|with|from)?\s*\)", re.IGNORECASE)


def _tidy(s: str) -> str:
    return _clean(_EMPTY_PAREN.sub("", _clean(s)))


def _inline_text(el) -> str:
    """Render inline element: code -> `x`, em/strong kept as text, links keep text."""
    parts = []
    for node in el.descendants if hasattr(el, "descendants") else [el]:
        if isinstance(node, NavigableString):
            parent = node.parent
            if parent is not None and parent.name == "code":
                continue  # handled at code tag level
            parts.append(str(node))
        elif getattr(node, "name", None) == "code":
            txt = _clean(node.get_text())
            parts.append(f"`{txt}`" if txt else "")
        elif getattr(node, "name", None) == "br":
            parts.append("\n")
    # fallback for plain tags
    if not parts:
        return _clean(el.get_text(" ") if hasattr(el, "get_text") else str(el))
    text = "".join(parts)
    # collapse whitespace but keep single newlines from <br>
    lines = [_clean(l) for l in text.split("\n")]
    return "\n".join(l for l in lines if l)


def _table_to_md(table) -> str:
    rows = []
    for tr in table.find_all("tr"):
        cells = [_clean(c.get_text(" ")) for c in tr.find_all(["th", "td"])]
        if cells:
            rows.append(cells)
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    out = ["| " + " | ".join(rows[0]) + " |",
           "| " + " | ".join("---" for _ in rows[0]) + " |"]
    out += ["| " + " | ".join(r) + " |" for r in rows[1:]]
    return "\n".join(out)


def html_to_markdown(content: bytes) -> tuple[str, list[str]]:
    """Convert one spine item's HTML to markdown-ish text. Returns (text, notes)."""
    soup = BeautifulSoup(content, "html.parser")
    body = soup.find("body") or soup
    notes: list[str] = []
    lines: list[str] = []
    # collect footnote-ish anchors for [Note] appendix (FR-EXT-006)
    for a in body.find_all("a"):
        href = a.get("href", "")
        cls = " ".join(a.get("class", []))
        if "note" in cls.lower() or "footnote" in cls.lower() or href.startswith("#ftn"):
            t = _clean(a.get_text(" "))
            if t:
                notes.append(t)

    for el in body.find_all(["h1", "h2", "h3", "h4", "h5", "h6",
                             "p", "pre", "ul", "ol", "table", "blockquote",
                             "img", "hr"], recursive=True):
        # skip nested-inside-table/list double handling for block containers
        if el.find_parent(["table", "pre"]) in (None,):
            pass
        tag = el.name
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag[1])
            t = _clean(el.get_text(" "))
            if t:
                lines.append("")
                lines.append("#" * min(level, 4) + " " + t)
                lines.append("")
        elif tag == "p":
            # skip paragraphs that are just inside a list item already handled? keep simple
            if el.find_parent("li") is not None:
                continue
            t = _inline_text(el)
            if t:
                lines.append(t)
                lines.append("")
        elif tag == "pre":
            code = _clean(el.get_text("\n"))
            if code:
                lang = ""
                for c in (el.get("class", []) or []):
                    m = re.search(r"language-(\w+)", c)
                    if m:
                        lang = m.group(1)
                        break
                lines.append(f"```{lang if lang in ('c', 'cpp', 'sh', 'bash', 'python') else 'c'}")
                lines.append(el.get_text("\n").strip("\n"))
                lines.append("```")
                lines.append("")
        elif tag in ("ul", "ol"):
            if el.find_parent("li") is not None:
                continue
            for i, li in enumerate(el.find_all("li", recursive=False), 1):
                t = _inline_text(li)
                bullet = f"{i}." if tag == "ol" else "-"
                if t:
                    lines.append(f"{bullet} {t}")
            lines.append("")
        elif tag == "table":
            md = _table_to_md(el)
            if md:
                lines.append(md)
                lines.append("")
        elif tag == "blockquote":
            t = _clean(el.get_text(" "))
            if t:
                lines.append("> " + t)
                lines.append("")
        elif tag == "img":
            alt = _clean(el.get("alt", "") or el.get("title", "") or "figure")
            src = el.get("src", "")
            lines.append(f"![{alt}]({src})")
            lines.append("")
        elif tag == "hr":
            lines.append("---")
            lines.append("")
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip() + "\n"
    return text, notes


def _chapter_title(soup_text: str, fallback: str) -> str:
    h1s: list[str] = []
    for line in soup_text.splitlines():
        s = line.strip()
        if s.startswith("# "):
            t = _clean(s[2:])
            if t and len(t) < 120:
                h1s.append(t)
                if len(h1s) >= 4:
                    break
        elif s.startswith("## ") and len(h1s) == 1:
            t = _clean(s[3:])
            if t and len(t) < 120:
                h1s.append(t)
                break
    if len(h1s) >= 2:
        c1 = h1s[0]
        c1_norm = re.sub(r"(?i)(chapter\s+\d)\s+(\d)", r"\1\2", c1)
        if re.match(r"(?i)^(chapter|part)\s+\d+$", c1_norm.strip()):
            for c2 in h1s[1:]:
                if c2.lower() != c1.lower() and not re.match(r"(?i)^(chapter|part)\s+\d+$", c2):
                    return f"{c1_norm} — {c2}"
    if h1s:
        return h1s[0]
    return fallback


def extract_epub(epub_path: Path, out_dir: Path, force: bool = False) -> dict:
    """Core extraction. Returns meta dict and writes files. (FR-EXT-001..003,005,006)"""
    import ebooklib.epub as E
    from ebooklib.epub import EpubHtml, EpubNav, EpubNcx

    if not epub_path.exists():
        raise FileNotFoundError(f"EPUB not found: {epub_path}")
    out_dir.mkdir(parents=True, exist_ok=True)
    raw = out_dir / "raw_chapters"

    if raw.exists() and any(raw.iterdir()) and not force:
        raise FileExistsError(
            f"{raw} already has content. Re-run with --force (backs up first). Refusing silent overwrite (FR-EXT-005).")
    if force and raw.exists() and any(raw.iterdir()):
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        bak = out_dir / f"raw_chapters.bak.{stamp}"
        shutil.move(str(raw), str(bak))
    raw.mkdir(parents=True, exist_ok=True)

    book = E.read_epub(str(epub_path))

    def _md(key: str) -> str:
        vals = book.get_metadata("DC", key)
        return _clean(vals[0][0]) if vals else ""

    title = _tidy(_md("title")) or epub_path.stem
    authors = [_tidy(_clean(v[0])) for v in book.get_metadata("DC", "creator")]
    language = _md("language") or "en"

    spine_ids = [sid for sid, _ in book.spine]
    warnings: list[str] = []
    chapters: list[dict] = []
    counter = 0
    for sid in spine_ids:
        try:
            item = book.get_item_with_id(sid)
        except KeyError:
            warnings.append(f"spine id missing from manifest: {sid}")
            continue
        if item is None:
            warnings.append(f"spine id resolved to None: {sid}")
            continue
        if isinstance(item, (EpubNav, EpubNcx)):
            continue
        if not isinstance(item, EpubHtml):
            warnings.append(f"non-HTML spine item skipped (listed, not dropped silently): {sid} ({type(item).__name__})")
            continue
        try:
            text, notes = html_to_markdown(item.get_content())
        except Exception as e:  # FR-EXT-003: record, don't silently drop
            warnings.append(f"unparseable spine item {sid} ({item.get_name()}): {e}")
            continue
        if notes:
            text += "\n[Notes]\n" + "\n".join(f"- [Note] {n}" for n in notes) + "\n"
        if len(text.strip()) < 50:
            warnings.append(f"near-empty chapter text (kept anyway): {sid} ({item.get_name()})")
        counter += 1
        ch_id = f"ch{counter:02d}"
        fname = item.get_name() or sid
        chap_title = _chapter_title(text, _clean(sid.replace("_", " ").replace(".xhtml", "")))
        dest = raw / f"{ch_id}.txt"
        header = (f"# {chap_title}\n\n<!-- source: {fname} | spine-id: {sid} | chapter: {ch_id} -->\n\n")
        dest.write_text(header + text, encoding="utf-8")
        chapters.append({"id": ch_id, "spine_id": sid, "file": fname,
                         "title": chap_title, "chars": len(text)})

    meta = {"slug": out_dir.name, "title": title, "authors": authors,
            "language": language, "source_file": epub_path.name,
            "spine_count": len(spine_ids), "chapters": chapters, "warnings": warnings,
            "extracted_at": datetime.datetime.now().isoformat(timespec="seconds")}
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return meta


def extract_book(slug: str, force: bool = False) -> dict:
    book_dir = ROOT / "books" / slug
    epub = book_dir / "source.epub"
    meta = extract_epub(epub, book_dir, force=force)
    from rich.console import Console
    c = Console()
    c.print(f"[green]extracted {len(meta['chapters'])} chapters -> {book_dir / 'raw_chapters'}[/green]")
    if meta["warnings"]:
        c.print(f"[yellow]{len(meta['warnings'])} warning(s):[/yellow]")
        for w in meta["warnings"][:10]:
            c.print(f"  - {w}")
    return meta


def main(argv=None):
    ap = argparse.ArgumentParser(description="Extract EPUB chapters (SRS FR-EXT-001..006)")
    ap.add_argument("epub", help="path to source.epub")
    ap.add_argument("--out", required=True, help="output book dir (books/<slug>)")
    ap.add_argument("--force", action="store_true", help="allow overwrite (backs up existing)")
    a = ap.parse_args(argv)
    meta = extract_epub(Path(a.epub), Path(a.out), force=a.force)
    print(f"chapters={len(meta['chapters'])} warnings={len(meta['warnings'])}")


if __name__ == "__main__":
    main()

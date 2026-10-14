"""Book/chapter discovery. (SRS FR-BOOK-001..005, FR-CHAP-001..004)"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read_json(p: Path) -> dict | None:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def discover_books() -> list[dict]:
    """Merge books/*/meta.json with packs/*/book.yaml. (FR-BOOK-001)"""
    out: dict[str, dict] = {}
    bdir = ROOT / "books"
    if bdir.exists():
        for d in sorted(bdir.iterdir()):
            if not d.is_dir():
                continue
            if (d / ".ignore").exists():
                continue  # FR-BOOK-005
            meta = _read_json(d / "meta.json")
            has_epub = (d / "source.epub").exists()
            if meta is None and not has_epub:
                continue
            out[d.name] = {"slug": d.name,
                           "title": (meta or {}).get("title", d.name),
                           "authors": (meta or {}).get("authors", []),
                           "n_chapters": len((meta or {}).get("chapters", [])),
                           "has_epub": has_epub,
                           "pack_chapters": 0}
    pdir = ROOT / "packs"
    if pdir.exists():
        for d in sorted(pdir.iterdir()):
            if not d.is_dir():
                continue
            n = len(list(d.glob("ch*.yaml")))
            if d.name in out:
                out[d.name]["pack_chapters"] = n
            else:
                out[d.name] = {"slug": d.name, "title": d.name, "authors": [],
                               "n_chapters": 0, "has_epub": False, "pack_chapters": n}
    return list(out.values())


def _slugify(title: str) -> str:
    import re
    s = title.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "book"


def discover_chapters(slug: str) -> list[dict]:
    """Author order: packs/<slug>/book.yaml wins, else books/<slug>/meta.json. (FR-CHAP-002)"""
    import yaml
    book_yaml = ROOT / "packs" / slug / "book.yaml"
    if book_yaml.exists():
        try:
            data = yaml.safe_load(book_yaml.read_text(encoding="utf-8")) or {}
            order = data.get("order", [])
            chap_meta = {c.get("id"): c for c in data.get("chapters", [])}
            result = []
            for cid in order:
                title = chap_meta.get(cid, {}).get("title", cid)
                pack_file = ROOT / "packs" / slug / f"{cid}.yaml"
                has_pack = pack_file.exists()
                if has_pack:
                    try:
                        pdata = yaml.safe_load(pack_file.read_text(encoding="utf-8")) or {}
                        pack_title = pdata.get("meta", {}).get("title")
                        if pack_title and len(pack_title) > len(title):
                            title = pack_title
                    except Exception:
                        pass
                result.append({"id": cid,
                               "title": title,
                               "has_pack": has_pack,
                               "has_lab": _pack_has_lab(slug, cid)})
            return result
        except Exception:
            pass
    meta = _read_json(ROOT / "books" / slug / "meta.json")
    if meta:
        result = []
        for c in meta.get("chapters", []):
            cid = c["id"]
            title = c.get("title", cid)
            pack_file = ROOT / "packs" / slug / f"{cid}.yaml"
            has_pack = pack_file.exists()
            if has_pack:
                try:
                    pdata = yaml.safe_load(pack_file.read_text(encoding="utf-8")) or {}
                    pack_title = pdata.get("meta", {}).get("title")
                    if pack_title and len(pack_title) > len(title):
                        title = pack_title
                except Exception:
                    pass
            result.append({"id": cid,
                           "title": title,
                           "has_pack": has_pack,
                           "has_lab": _pack_has_lab(slug, cid)})
        return result
    return []


def _pack_has_lab(slug: str, cid: str) -> bool:
    try:
        import yaml
        p = ROOT / "packs" / slug / f"{cid}.yaml"
        if not p.exists():
            return False
        return bool((yaml.safe_load(p.read_text(encoding="utf-8")) or {}).get("lab"))
    except Exception:
        return False


def list_books():
    from rich.console import Console
    from rich.table import Table
    c = Console()
    rows = discover_books()
    if not rows:
        c.print("[yellow]No books yet. Drop an EPUB at books/<slug>/source.epub[/yellow]")
        return
    t = Table(title="books")
    t.add_column("slug"); t.add_column("title"); t.add_column("author")
    t.add_column("chapters"); t.add_column("pack"); t.add_column("mastery")
    for r in rows:
        from lib import progress as _p
        authors = ", ".join(r["authors"][:2]) if r["authors"] else "—"
        t.add_row(r["slug"], str(r["title"])[:40], authors[:24],
                  str(r["n_chapters"]), str(r["pack_chapters"]),
                  _p.book_mastery(r["slug"], r["pack_chapters"]))
    c.print(t)


def list_chapters(book: str):
    from rich.console import Console
    from rich.table import Table
    c = Console()
    rows = discover_chapters(book)
    if not rows:
        # FR-BOOK-004: guide, don't crash
        c.print(f"[yellow]No chapters for '{book}'. Next: python main.py extract --book {book}, "
                f"then gen-prompt + validate.[/yellow]")
        return
    t = Table(title=f"chapters — {book}")
    t.add_column("id"); t.add_column("title"); t.add_column("pack")
    t.add_column("status"); t.add_column("due"); t.add_column("lab")
    for r in rows:
        from lib import progress as _p
        t.add_row(r["id"], str(r["title"]),
                  "yes" if r["has_pack"] else "no",
                  _p.chapter_status(book, r["id"]) if r["has_pack"] else "—",
                  str(_p.chapter_due_count(book, r["id"])) if r["has_pack"] else "—",
                  _p.chapter_lab_state(book, r["id"], r.get("has_lab", False)))
    c.print(t)

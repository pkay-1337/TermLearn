"""Pack load + schema validation. (SRS FR-PACK-001..006, FR-VAL-001..004, NFR-SEC-002)"""
from pathlib import Path
import os
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]

BOOK_REQUIRED_TOP = {"book", "order", "chapters"}
CHAPTER_REQUIRED_TOP = {"meta", "objectives", "blocks"}
CHAPTER_KNOWN_TOP = {"meta", "objectives", "blocks", "cards", "lab", "test", "draft"}
BLOCK_TYPES = {"model", "syntax", "design", "algorithm"}
CHECK_KINDS = {"predict", "why-fails", "mcq", "fillblank", "order",
               "eipe", "choose-better", "micro-lab",
               "trace", "spot-bug"}
CHOICE_KINDS = {"predict", "why-fails", "mcq", "eipe", "choose-better", "spot-bug"}
DENYLIST = ["rm -rf", "curl", "wget", "ssh", "mkfs", ":(){", "dd if=", "chmod 777"]

#: Network-capable constructs (FR-TEST-004, D-18). Regexes, case-sensitive;
#: kept blunt on purpose — a hit means human review, and strict FAILS.
NET_PATTERNS = [r"\bsocket\b", r"\burllib\b", r"http\.client",
                r"\brequests\b", r"/dev/tcp", r"(^|\s)nc\s",
                r"\bcurl\s+[^\s]*http", r"\bwget\s+[^\s]*http",
                r"\bpip\s+install\b"]
#: GUI imports need a display the terminal may lack — WARN-only by design.
GUI_PATTERNS = [r"\btkinter\b", r"\bPyQt[45]?\b", r"\bpygame\b", r"\bSDL\b"]


def scan_network(text: str) -> list[str]:
    """Return names of matched network-capable patterns (FR-TEST-004)."""
    hits = []
    for pat in NET_PATTERNS:
        m = re.search(pat, text or "")
        if m:
            hits.append(m.group(0).strip())
    return hits


def scan_gui(text: str) -> list[str]:
    """Return names of matched GUI imports (WARN-only notes)."""
    hits = []
    for pat in GUI_PATTERNS:
        m = re.search(pat, text or "")
        if m:
            hits.append(m.group(0).strip())
    return hits


def suggest_fixes(data: dict) -> list[str]:
    """Per-error repair suggestions with full context (FR-VAL-004, D-15).
    Advisory only — never changes any verdict. Each hint names the location
    and the exact legal shape."""
    hints: list[str] = []
    if not isinstance(data, dict):
        return ["HINT: top level must be a mapping with meta/objectives/blocks"]
    for key in ("meta", "objectives", "blocks"):
        if key not in data:
            hints.append(f"HINT: add top-level '{key}:' (see docs/SRS.md §4.8)")
    for k in ("book", "chapter_id", "title", "source_ref", "level", "prereqs"):
        if isinstance(data.get("meta"), dict) and k not in data["meta"]:
            hints.append(f"HINT: add 'meta.{k}:'")
    for bi, b in enumerate(data.get("blocks", []) or []):
        if not isinstance(b, dict):
            continue
        loc = f"blocks[{bi}]"
        for k in ("id", "type", "title", "explain_md", "checks"):
            if k not in b:
                hints.append(f"HINT: {loc}: add '{k}:'")
        if b.get("type") not in BLOCK_TYPES and "type" in b:
            hints.append(f"HINT: {loc}: type {b.get('type')!r} invalid — "
                         f"use one of {sorted(BLOCK_TYPES)}")
        for ci, ck in enumerate(b.get("checks", []) or []):
            if not isinstance(ck, dict):
                continue
            cloc = f"{loc}:checks[{ci}]"
            if ck.get("kind") not in CHECK_KINDS:
                hints.append(f"HINT: {cloc}: kind {ck.get('kind')!r} invalid — "
                             f"use one of {sorted(CHECK_KINDS)}")
                continue
            if "why" not in ck or not str(ck.get("why", "")).strip():
                hints.append(f"HINT: {cloc}: add 'why:' with the principle + "
                             f"trapped misconceptions")
            if ck["kind"] in CHOICE_KINDS:
                chs = ck.get("choices", [])
                ans = ck.get("answer")
                if isinstance(chs, list) and not (isinstance(ans, int)
                                                 and 0 <= ans < len(chs)):
                    opts = "; ".join(f"{i}. {o}" for i, o in enumerate(chs)) or "(no choices listed)"
                    hints.append(f"HINT: {cloc}: set answer to 0..{len(chs) - 1}; "
                                 f"choices are {opts}")
            if ck["kind"] == "order":
                lines = ck.get("lines", [])
                ao = ck.get("answer_order", [])
                if isinstance(lines, list) and isinstance(ao, list):
                    n = len(lines)
                    dupes = sorted({i for i in ao if ao.count(i) > 1})
                    bad = [i for i in ao if not isinstance(i, int) or not 0 <= i < n]
                    if dupes or bad or len(ao) < 2:
                        hints.append(f"HINT: {cloc}: answer_order must hold >=2 unique "
                                     f"indices into 0..{n - 1}"
                                     + (f"; duplicated {dupes}" if dupes else "")
                                     + (f"; out of range {bad}" if bad else ""))
            if ck["kind"] == "fillblank" and not str(ck.get("answer_text", "")).strip():
                hints.append(f"HINT: {cloc}: add 'answer_text:' with the exact token")
            if ck["kind"] == "order" and ck.get("faded") is True and not ck.get("blanks"):
                hints.append(f"HINT: {cloc}: faded order check needs 'blanks:' with line_idx and answer_text")
            if ck["kind"] == "trace":
                if "trace" not in ck or not isinstance(ck.get("trace"), dict):
                    hints.append(f"HINT: {cloc}: trace check needs 'trace:' with headers and rows")
                if "target" not in ck:
                    hints.append(f"HINT: {cloc}: trace check needs 'target:' with row and col")
            if ck["kind"] == "spot-bug":
                if "diagnostic_log" not in ck:
                    hints.append(f"HINT: {cloc}: spot-bug check needs 'diagnostic_log:' with compiler/sanitizer report")
                if "code" not in ck:
                    hints.append(f"HINT: {cloc}: spot-bug check needs 'code:' snippet")
    return hints


def _err(code: str, msg: str) -> str:
    return f"{code}: {msg}"


def _gcc_available() -> bool:
    try:
        r = subprocess.run(["gcc", "--version"], capture_output=True, timeout=5)
        return r.returncode == 0
    except Exception:
        return False


def _compiles_c(code: str) -> tuple[bool, str]:
    """Compile-only probe (-c). Returns (ok, stderr_tail)."""
    if not _gcc_available():
        return True, "gcc absent — skipped"
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "probe.c"
        src.write_text(code, encoding="utf-8")
        try:
            r = subprocess.run(["gcc", "-Wall", "-std=c99", "-O0", "-c",
                                str(src), "-o", str(Path(td) / "probe.o")],
                               capture_output=True, text=True, timeout=15)
        except subprocess.TimeoutExpired:
            return False, "gcc timeout"
        if r.returncode != 0:
            tail = (r.stderr or "")[-800:]
            return False, tail
        return True, ""


def _rich_renders(md: str) -> bool:
    try:
        from rich.markdown import Markdown
        from rich.console import Console
        Console(width=80, record=True).print(Markdown(md or ""))
        return True
    except Exception:
        return False


def validate_book_data(book: dict, fname: str = "book.yaml") -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    if not isinstance(book, dict):
        return [_err("BOOK-SHAPE", f"{fname}: top level must be mapping")], []
    for k in BOOK_REQUIRED_TOP:
        if k not in book:
            errors.append(_err("BOOK-MISSING", f"{fname}: missing required key '{k}'"))
    if errors:
        return errors, warnings
    order = book["order"]
    chapters = book["chapters"]
    if not isinstance(order, list) or not order:
        errors.append(_err("BOOK-ORDER", f"{fname}: 'order' must be non-empty list"))
    if not isinstance(chapters, list) or not chapters:
        errors.append(_err("BOOK-CHAPTERS", f"{fname}: 'chapters' must be non-empty list"))
        return errors, warnings
    ids = [c.get("id") for c in chapters if isinstance(c, dict)]
    if len(set(ids)) != len(ids):
        errors.append(_err("BOOK-DUP", f"{fname}: duplicate chapter ids"))
    if isinstance(order, list) and set(order) != set(ids):
        errors.append(_err("BOOK-ORDER-MISMATCH", f"{fname}: order {order} != chapter ids {ids}"))
    for c in chapters:
        if not isinstance(c, dict) or "id" not in c or "title" not in c or "source_ref" not in c:
            errors.append(_err("BOOK-CHAPTER-SHAPE", f"{fname}: each chapter needs id/title/source_ref, got {c}"))
        c.setdefault("prereqs", [])
        for p in c.get("prereqs", []):
            if p not in ids:
                errors.append(_err("BOOK-PREREQ", f"{fname}: chapter {c.get('id')} prereq '{p}' unknown"))
    return errors, warnings


def validate_chapter_data(ch: dict, fname: str = "chXX.yaml", strict: bool = False,
                          known_chapters: set | None = None,
                          chapter_blocks: dict[str, set | None] | None = None) -> tuple[list[str], list[str]]:
    """chapter_blocks maps chapter id -> set of block ids (None = unloadable:
    refs to it stay chapter-level). When None entirely, block-level refs stay
    advisory (unit-test use)."""
    errors, warnings = [], []
    if not isinstance(ch, dict):
        return [_err("CH-SHAPE", f"{fname}: top level must be mapping")], []
    for k in ch:
        if k not in CHAPTER_KNOWN_TOP:
            warnings.append(_err("CH-UNKNOWN-KEY", f"{fname}: unknown top-level key '{k}'"))
    if ch.get("draft") is True:
        # FR-GEN-003/D-01: drafts never gate advancement — strict promotes this.
        warnings.append(_err("DRAFT", f"{fname}: marked draft:true — review before trusting scores"))
    for k in CHAPTER_REQUIRED_TOP:
        if k not in ch:
            errors.append(_err("CH-MISSING", f"{fname}: missing required key '{k}'"))
    if errors:
        return errors, warnings

    meta = ch["meta"]
    for k in ("book", "chapter_id", "title", "source_ref", "level", "prereqs"):
        if k not in meta:
            errors.append(_err("META-MISSING", f"{fname}: meta missing '{k}'"))
    if meta.get("level") not in ("intro", "core", "advanced"):
        errors.append(_err("META-LEVEL", f"{fname}: level must be intro|core|advanced"))
    if known_chapters is not None:
        for p in meta.get("prereqs", []):
            if p not in known_chapters:
                errors.append(_err("META-PREREQ", f"{fname}: prereq '{p}' not in book order"))

    if not isinstance(ch["objectives"], list) or not (1 <= len(ch["objectives"]) <= 6):
        errors.append(_err("OBJ-SHAPE", f"{fname}: objectives must be list of 1..6"))

    blocks = ch["blocks"]
    if not isinstance(blocks, list) or not blocks:
        errors.append(_err("BLOCK-EMPTY", f"{fname}: blocks must be non-empty list"))
        return errors, warnings
    block_ids = [b.get("id") for b in blocks if isinstance(b, dict)]
    if len(set(block_ids)) != len(block_ids):
        errors.append(_err("BLOCK-DUP", f"{fname}: duplicate block ids"))

    why_total = 0
    why_conceptual = 0  # predict/why-fails/mcq counted; conceptual = why-fails kinds
    for bi, b in enumerate(blocks):
        loc = f"{fname}:blocks[{bi}]"
        if not isinstance(b, dict):
            errors.append(_err("BLOCK-SHAPE", f"{loc} must be mapping"))
            continue
        for k in ("id", "type", "title", "explain_md", "checks"):
            if k not in b:
                errors.append(_err("BLOCK-MISSING", f"{loc} missing '{k}'"))
        if b.get("type") not in BLOCK_TYPES:
            errors.append(_err("BLOCK-TYPE", f"{loc} unknown type {b.get('type')!r}, want {sorted(BLOCK_TYPES)}"))
            continue
        if not isinstance(b.get("checks", None), list) or not b.get("checks"):
            errors.append(_err("BLOCK-CHECKS", f"{loc} checks must be non-empty list"))
            continue
        ex = b.get("example")
        if isinstance(ex, dict):
            if ex.get("code") and len(str(ex["code"]).splitlines()) > 80:
                warnings.append(_err("EX-LONG", f"{loc} example >80 lines; keep terminal-readable (FR-PACK-005)"))
            if "subgoals" in ex:
                sgs = ex.get("subgoals")
                if not isinstance(sgs, list) or not sgs:
                    errors.append(_err("SUBGOAL-SHAPE", f"{loc} example subgoals must be non-empty list"))
                else:
                    code_len = len(str(ex.get("code", "")).splitlines())
                    for sgi, sg in enumerate(sgs):
                        if not isinstance(sg, dict) or not sg.get("label") or not isinstance(sg.get("lines"), list):
                            errors.append(_err("SUBGOAL-SHAPE", f"{loc} example subgoals[{sgi}] needs label and lines list"))
                        elif code_len > 0 and any(not isinstance(ln, int) or ln < 1 or ln > code_len for ln in sg.get("lines", [])):
                            errors.append(_err("SUBGOAL-SPAN", f"{loc} example subgoals[{sgi}] lines out of bounds (1..{code_len})"))
        if b.get("type") == "model" and "viz" not in b:
            warnings.append(_err("MODEL-NOVIZ", f"{loc} model block without viz; SHOULD add ascii-memory (MAP-001)"))
        for ci, ck in enumerate(b["checks"]):
            cloc = f"{loc}:checks[{ci}]"
            if not isinstance(ck, dict) or "kind" not in ck or "q" not in ck:
                errors.append(_err("CHECK-SHAPE", f"{cloc} needs kind+q"))
                continue
            kind = ck["kind"]
            if kind not in CHECK_KINDS:
                errors.append(_err("CHECK-KIND", f"{cloc} unknown kind {kind!r}"))
                continue
            if "why" not in ck or not str(ck["why"]).strip():
                errors.append(_err("CHECK-WHY", f"{cloc} missing required 'why' explanation"))
            else:
                why_total += 1
                if kind in ("predict", "why-fails", "eipe", "choose-better", "trace", "spot-bug"):
                    why_conceptual += 1
            if kind in CHOICE_KINDS:
                chs = ck.get("choices")
                ans = ck.get("answer")
                if not isinstance(chs, list) or not (2 <= len(chs) <= 5):
                    errors.append(_err("CHECK-CHOICES", f"{cloc} choices must be list of 2..5"))
                elif not isinstance(ans, int) or not (0 <= ans < len(chs)):
                    errors.append(_err("CHECK-ANSWER", f"{cloc} answer index {ans!r} out of bounds 0..{len(chs)-1}"))
            if kind == "order":
                lines = ck.get("lines")
                ao = ck.get("answer_order")
                if not isinstance(lines, list) or len(lines) < 2:
                    errors.append(_err("ORDER-LINES", f"{cloc} lines must be list of >=2"))
                elif (not isinstance(ao, list) or len(ao) < 2 or len(ao) > len(lines)
                      or len(set(ao)) != len(ao)
                      or not all(isinstance(i, int) and 0 <= i < len(lines) for i in ao)):
                    errors.append(_err("ORDER-PERM", f"{cloc} answer_order {ao!r} must list >=2 unique valid indices into lines (distractor lines are simply omitted)"))
                if ck.get("faded") is True:
                    blanks = ck.get("blanks")
                    if not isinstance(blanks, list) or not blanks:
                        errors.append(_err("FADED-BLANK", f"{cloc} faded order check requires non-empty 'blanks' list"))
                    else:
                        for bi, blk in enumerate(blanks):
                            if not isinstance(blk, dict) or "line_idx" not in blk:
                                errors.append(_err("FADED-BLANK", f"{cloc} blanks[{bi}] requires line_idx"))
                            elif not isinstance(blk["line_idx"], int) or not (0 <= blk["line_idx"] < len(lines or [])):
                                errors.append(_err("FADED-BLANK", f"{cloc} blanks[{bi}] line_idx out of bounds"))
                            elif not blk.get("answer_text") and not blk.get("accepted"):
                                errors.append(_err("FADED-BLANK", f"{cloc} blanks[{bi}] requires answer_text or accepted list"))
            if kind == "fillblank":
                if "answer_text" not in ck or not str(ck["answer_text"]).strip():
                    errors.append(_err("FILL-ANSWER", f"{cloc} fillblank needs answer_text"))
            if kind == "trace":
                tr = ck.get("trace")
                if not isinstance(tr, dict) or not isinstance(tr.get("headers"), list) or len(tr["headers"]) < 2:
                    errors.append(_err("TRACE-SHAPE", f"{cloc} trace check requires 'trace.headers' list of >=2"))
                elif not isinstance(tr.get("rows"), list) or len(tr["rows"]) < 1:
                    errors.append(_err("TRACE-SHAPE", f"{cloc} trace check requires 'trace.rows' list of >=1"))
                else:
                    tgt = ck.get("target")
                    if not isinstance(tgt, dict) or "row" not in tgt or "col" not in tgt:
                        errors.append(_err("TRACE-TARGET", f"{cloc} trace check requires 'target' with row and col"))
                    elif (not isinstance(tgt["row"], int) or not (0 <= tgt["row"] < len(tr["rows"]))
                          or not isinstance(tgt["col"], int) or not (0 <= tgt["col"] < len(tr["headers"]))):
                        errors.append(_err("TRACE-TARGET", f"{cloc} trace target row/col out of bounds"))
                    has_txt = bool(str(ck.get("answer_text", "")).strip())
                    chs = ck.get("choices")
                    ans = ck.get("answer")
                    has_choices = isinstance(chs, list) and len(chs) >= 2 and isinstance(ans, int) and (0 <= ans < len(chs))
                    if not has_txt and not has_choices:
                        errors.append(_err("TRACE-ANSWER", f"{cloc} trace check requires answer_text or choices+answer"))
            if kind == "spot-bug":
                if not str(ck.get("code", "")).strip():
                    errors.append(_err("BUG-CODE", f"{cloc} spot-bug check requires 'code' snippet"))
                if not str(ck.get("diagnostic_log", "")).strip():
                    errors.append(_err("BUG-LOG", f"{cloc} spot-bug check requires 'diagnostic_log' report"))
            for ref in ("from_chapter", "from_block"):
                pass
            if "from_chapter" in ck and known_chapters is not None:
                if ck["from_chapter"] not in known_chapters:
                    errors.append(_err("INTERLEAVE-REF", f"{cloc} from_chapter {ck['from_chapter']!r} unknown"))
                elif ("from_block" in ck and chapter_blocks is not None
                      and chapter_blocks.get(ck["from_chapter"]) is not None
                      and ck["from_block"] not in chapter_blocks[ck["from_chapter"]]):
                    errors.append(_err("INTERLEAVE-BLOCK", f"{cloc} from_block {ck['from_block']!r} not in {ck['from_chapter']}"))

    # MAP-005 / FR-AI-005 quality gates -> warnings (errors in --strict)
    interleaved = sum(1 for b in blocks if isinstance(b, dict)
                      for ck in (b.get("checks") or []) if isinstance(ck, dict) and "from_chapter" in ck)
    if interleaved < 2:
        warnings.append(_err("INTERLEAVE-COUNT", f"{fname}: only {interleaved} interleaved checks; SHOULD have >=2 (MAP-005)"))
    if why_total and why_conceptual < (why_total + 1) // 2:
        warnings.append(_err("WHY-RATIO", f"{fname}: only {why_conceptual}/{why_total} conceptual (predict/why-fails/eipe/choose-better); SHOULD be >=half (FR-AI-005)"))

    # lab checks (language-aware: only C has a local probe in this version)
    lab = ch.get("lab")
    if isinstance(lab, dict):
        starter = lab.get("starter_c", "")
        lang = (lab.get("lang", "c") or "c").lower()
        if starter and lang == "c":
            if len(starter.splitlines()) > 80:
                warnings.append(_err("LAB-LONG", f"{fname}:lab starter_c >80 lines"))
            ok, tail = _compiles_c(starter)
            if not ok:
                errors.append(_err("LAB-COMPILE", f"{fname}:lab starter_c does not compile: {tail[:300]}"))
        elif starter:
            warnings.append(_err("LANG-NOPROBE", f"{fname}:lab lang '{lang}' has no local compile probe — skipped; toolchain declares it"))
        tests_sh = lab.get("tests_sh", "")
        if tests_sh:
            for bad in scan_denylist(tests_sh):
                msg = _err("LAB-DENY", f"{fname}:lab tests_sh contains denylisted {bad!r}")
                (errors if strict else warnings).append(msg)
            for hit in scan_network(tests_sh):
                msg = _err("NET-RISKY", f"{fname}:lab tests_sh looks network-capable ({hit!r})")
                (errors if strict else warnings).append(msg)
            for hit in scan_gui(tests_sh):
                warnings.append(_err("GUI-NOTE", f"{fname}:lab tests_sh imports GUI ({hit!r}) — headless hosts may fail"))
    # test gates reference check
    test = ch.get("test")
    if isinstance(test, dict):
        for g in test.get("gates", []):
            for need in g.get("needs", []):
                if need not in block_ids:
                    errors.append(_err("TEST-GATE", f"{fname}:test gate needs unknown block {need!r}"))

    # render smoke: Markdown fields must not crash Rich
    for bi, b in enumerate(blocks):
        if isinstance(b, dict) and not _rich_renders(str(b.get("explain_md", ""))):
            errors.append(_err("RENDER", f"{fname}:blocks[{bi}] explain_md crashes Rich renderer"))

    if strict:
        # Informational notes MUST NOT fail strict validation: LANG-NOPROBE
        # (no local probe exists) and GUI-NOTE (hosts vary by design).
        keep_prefixes = ("LANG-NOPROBE", "GUI-NOTE")
        keep = [w for w in warnings if w.startswith(keep_prefixes)]
        errors.extend(w for w in warnings if not w.startswith(keep_prefixes))
        warnings = keep
    return errors, warnings


def _has_runnable(data: dict) -> bool:
    """True if the chapter has anything needing a toolchain (lab, run_expected,
    micro-lab code). Language-agnostic."""
    if isinstance(data.get("lab"), dict):
        return True
    for b in data.get("blocks", []) or []:
        ex = (b or {}).get("example") or {}
        if ex.get("run_expected"):
            return True
        for ck in (b or {}).get("checks", []) or []:
            if (ck or {}).get("kind") == "micro-lab" and (ck or {}).get("code"):
                return True
    return False


def toolchain_gate(has_toolchain: bool, data: dict) -> str | None:
    """Return a TOOLCHAIN-MISSING message if runnable content exists without a
    declared `book.yaml: toolchain:` stanza, else None. Caller decides
    warn-vs-fail by strictness."""
    if _has_runnable(data) and not has_toolchain:
        return _err("TOOLCHAIN-MISSING", "book.yaml: pack has runnable content but no 'toolchain' stanza (e.g. {lang: c, compile: [...], run: [...]})")
    return None


def _load_yaml(p: Path):
    import yaml
    try:
        return yaml.safe_load(p.read_text(encoding="utf-8")), None
    except Exception as e:
        return None, _err("YAML-SYNTAX", f"{p}: {e}")


def validate_book(book: str, chapter: str | None = None, strict: bool = False,
                  packs_root: Path | None = None, fix_hints: bool = False) -> bool:
    from rich.console import Console
    c = Console()
    base = (packs_root or (ROOT / "packs")) / book
    if not base.exists():
        c.print(f"[red]no pack dir: {base} — run gen-prompt first[/red]")
        return False
    bfile = base / "book.yaml"
    bdata, yerr = _load_yaml(bfile)
    if yerr:
        c.print(f"[red]{yerr}[/red]")
        return False
    berrs, bwarns = validate_book_data(bdata, "book.yaml")
    for w in bwarns:
        c.print(f"[yellow]WARN {w}[/yellow]")
    for e in berrs:
        c.print(f"[red]ERR {e}[/red]")
    if berrs:
        return False
    # FR-EXT-003/D-22: surface extraction warnings (informational, all modes).
    meta = base.parent.parent / "books" / book / "meta.json"
    try:
        import json as _j
        for w in (_j.loads(meta.read_text(encoding="utf-8")) or {}).get("warnings", []):
            c.print(f"[yellow]WARN EXT-SOURCE: {w}[/yellow]")
    except (FileNotFoundError, ValueError):
        pass
    order = bdata.get("order", [])
    known = set(order)
    if "toolchain" in bdata and not isinstance(bdata["toolchain"], dict):
        berrs.append(_err("BOOK-TOOLCHAIN", "book.yaml: 'toolchain' must be a mapping, e.g. {lang: c, compile: [...], run: [...]}"))
    # best-effort block-id map for INTERLEAVE-BLOCK checks (D-05); load
    # failures are reported in the main per-chapter pass, not here.
    # Unloadable chapters map to None: their refs stay chapter-level only.
    blockmap: dict[str, set | None] = {}
    for _cid in order:
        _f = base / f"{_cid}.yaml"
        try:
            import yaml as _y
            _d = _y.safe_load(_f.read_text(encoding="utf-8")) or {}
            blockmap[_cid] = {b.get("id") for b in _d.get("blocks", [])
                              if isinstance(b, dict)}
        except Exception:
            blockmap[_cid] = None
    targets = [chapter] if chapter else list(order)
    ok = True
    for cid in targets:
        f = base / f"{cid}.yaml"
        if not f.exists():
            c.print(f"[red]ERR CH-MISSING: {f} not found (FR-CHAP-003)[/red]")
            ok = False
            continue
        data, yerr = _load_yaml(f)
        if yerr:
            c.print(f"[red]{yerr}[/red]")
            ok = False
            continue
        errs, warns = validate_chapter_data(data, f"{cid}.yaml", strict=strict, known_chapters=known,
                                            chapter_blocks=blockmap)
        for w in warns:
            c.print(f"[yellow]WARN {w}[/yellow]")
        for e in errs:
            c.print(f"[red]ERR {e}[/red]")
        if fix_hints and isinstance(data, dict):
            for h in suggest_fixes(data):
                c.print(f"[cyan]{h}[/cyan]")
        if errs:
            ok = False
            ch_ok = False
        else:
            ch_ok = True
            # runnable probes (FR-VAL-001): compile C examples; other
            # languages are skipped with a note (LANG-NOPROBE).
            for b in data.get("blocks", []):
                ex = (b or {}).get("example") or {}
                if not ex.get("code"):
                    continue
                exlang = (ex.get("lang", "c") or "c").lower()
                if exlang != "c":
                    c.print(f"[dim]note: no compile probe for lang '{ex.get('lang')}' ({cid}/{b.get('id')})[/dim]")
                    continue
                good, tail = _compiles_c(str(ex["code"]))
                if not good:
                    c.print(f"[red]ERR EX-COMPILE: {cid}/{b.get('id')} example does not compile: {tail[:300]}[/red]")
                    ch_ok = False
            msg = toolchain_gate("toolchain" in bdata, data)
            if msg:
                if strict:
                    c.print(f"[red]ERR {msg}[/red]")
                    ch_ok = False
                else:
                    c.print(f"[yellow]WARN {msg}[/yellow]")
            ok = ok and ch_ok
            if ch_ok:
                c.print(f"[green]OK {cid}.yaml[/green]")
    rok, rmsgs = check_generated_runner(book, strict=strict,
                                          packs_root=packs_root or (ROOT / "packs"))
    for m in rmsgs:
        if m.startswith("WARN"):
            c.print(f"[yellow]{m}[/yellow]")
        elif m.startswith("ERR") or m.startswith("RUNNER-"):
            c.print(f"[red]ERR {m}[/red]")
        else:
            c.print(f"[dim]{m}[/dim]")
    ok = ok and rok
    return ok


def require_chapter(book: str, chapter: str, packs_root: Path | None = None) -> Path:
    p = (packs_root or (ROOT / "packs")) / book / f"{chapter}.yaml"
    if not p.exists():
        raise FileNotFoundError(f"missing pack: {p} — run gen-prompt + validate first (FR-CHAP-003)")
    return p


def _read_toolchain(packs_root: Path, book: str) -> dict:
    import yaml
    p = packs_root / book / "book.yaml"
    if not p.exists():
        raise FileNotFoundError(f"no pack dir for book {book!r}")
    return (yaml.safe_load(p.read_text(encoding="utf-8")) or {}).get("toolchain") or {}


def load_book_toolchain(book: str, packs_root: Path | None = None) -> dict:
    """Toolchain stanza from packs/<book>/book.yaml ({} if absent)."""
    return _read_toolchain(packs_root or (ROOT / "packs"), book)


def scan_denylist(text: str) -> list[str]:
    """NFR-SEC-002 denylist scan shared by tests_sh and runner sources."""
    return [b for b in DENYLIST if b in (text or "")]


def check_generated_runner(book: str, strict: bool = False,
                           packs_root: Path | None = None) -> tuple[bool, list[str]]:
    """RUNNER-SMOKE + version probe + denylist scan for toolchain.runner.
    Returns (ok, messages). Informational notes are *returned*, never printed
    here — the caller decides presentation."""
    from lib import lab as _lab
    msgs: list[str] = []
    ok = True
    try:
        tc = _read_toolchain(packs_root or (ROOT / "packs"), book)
    except FileNotFoundError as e:
        return False, [_err("RUNNER-NOBOOK", str(e))]
    rel = tc.get("runner", "")
    if not rel:
        return True, []
    base = (packs_root or (ROOT / "packs")) / book
    rpath = base / rel
    if not (rpath.exists() and os.access(str(rpath), os.X_OK)):
        return False, [_err("RUNNER-MISSING",
                            f"toolchain.runner {rel!r} missing or not executable")]
    src = rpath.read_text(encoding="utf-8", errors="replace")
    bad = scan_denylist(src)
    if bad:
        msg = _err("RUNNER-DENY", f"runner source contains denylisted {bad}")
        if strict:
            return False, [msg]
        msgs.append("WARN " + msg)
    net = scan_network(src)
    if net:
        msg = _err("RUNNER-NET", f"runner source looks network-capable {net}")
        if strict:
            return False, [msg]
        msgs.append("WARN " + msg)
    gui = scan_gui(src)
    if gui:
        msgs.append("WARN " + _err("GUI-NOTE", f"runner source imports GUI {gui}"))
    vc = tc.get("version_cmd") or []
    if vc:
        try:
            pr = subprocess.run([str(x) for x in vc], capture_output=True,
                                text=True, timeout=15)
            msgs.append("toolchain version: " + (pr.stdout or pr.stderr or "?")[:120].strip())
        except Exception as e:
            msgs.append(f"note: version_cmd failed (non-fatal): {e}")
    smoke = tc.get("smoke") or {}
    if not smoke:
        msgs.append("WARN " + _err("RUNNER-NOSMOKE",
                                   "generated runner has no toolchain.smoke vectors — smoke test skipped"))
        return ok, msgs
    ext = str(smoke.get("ext", "src"))
    with tempfile.TemporaryDirectory(prefix="termlearn-smoke-") as td:
        hello = Path(td) / f"hello.{ext}"
        hello.write_text(str(smoke.get("src", "")), encoding="utf-8")
        good, diag, rerr = _lab.check_runner(rpath, hello)
        if rerr or not good:
            return False, [_err("RUNNER-SMOKE",
                                f"check verb failed: {rerr or diag[:300]}")]
        r = _lab.exec_runner(rpath, hello, str(smoke.get("expect", "")),
                             int(tc.get("timeout_s", 2) or 2))
        if r.get("runner_error") or r.get("timed_out") or not r["tests_passed"]:
            return False, [_err("RUNNER-SMOKE",
                                f"exec verb failed: {r.get('runner_error') or r.get('diff', '')[:300]}")]
    msgs.append("runner smoke: OK")
    return ok, msgs


def load_chapter(book: str, chapter: str) -> dict:
    import yaml
    p = require_chapter(book, chapter)
    return yaml.safe_load(p.read_text(encoding="utf-8"))

"""Quiz runner: mcq/predict/why-fails/fillblank/eipe/choose-better/order/micro-lab.
(SRS FR-QUIZ-001..003)"""
import random
import time

CHOICE_KINDS = {"predict", "why-fails", "mcq", "eipe", "choose-better", "spot-bug"}


def collect_checks(data: dict) -> list[tuple[str, int, dict]]:
    out = []
    for b in data.get("blocks", []):
        for i, ck in enumerate(b.get("checks", [])):
            out.append((b.get("id", "?"), i, ck))
    return out


def collect_quiz_questions(data: dict) -> list[tuple[str, int, dict]]:
    """Collect questions for the chapter-level quiz.
    Uses top-level `quiz` stanza if present and non-empty (dedicated 30-50 questions).
    Falls back to collect_checks(data) for backward compatibility with older packs.
    """
    quiz_items = data.get("quiz")
    if isinstance(quiz_items, list) and quiz_items:
        return [("quiz", i, ck) for i, ck in enumerate(quiz_items) if isinstance(ck, dict)]
    return collect_checks(data)


def filter_checks(checks: list[tuple[str, int, dict]],
                  concept: str | None = None) -> list[tuple[str, int, dict]]:
    """Exact concept-tag match (D-02). None/empty returns all."""
    if not concept:
        return list(checks)
    return [(b, i, ck) for b, i, ck in checks
            if str(ck.get("concept", "")) == concept]


def tally(results: list[tuple[str, bool]]) -> dict[str, list[int]]:
    """concept -> [hits, total] for end-of-run breakdown (D-03)."""
    t: dict[str, list[int]] = {}
    for concept, ok in results:
        h, n = t.get(concept or "—", [0, 0])
        t[concept or "—"] = [h + (1 if ok else 0), n + 1]
    return t


def _shuffled_choices(ck: dict, rng: random.Random | None) -> tuple[list, int]:
    chs = list(ck["choices"])
    ans = int(ck["answer"])
    if rng is None:
        return chs, ans
    order = list(range(len(chs)))
    rng.shuffle(order)
    return [chs[i] for i in order], order.index(ans)


def ask_choice(console, ck: dict, rng=None) -> bool:
    from lib import keys as _k
    chs, ans = _shuffled_choices(ck, rng)
    if ck.get("code"):
        from rich.syntax import Syntax
        console.print(Syntax(ck["code"], ck.get("lang", "c"), theme="monokai"))
    if ck.get("diagnostic_log"):
        console.print(f"[bold red]Diagnostic Log:[/bold red]\n{ck['diagnostic_log']}")
    for i, opt in enumerate(chs, 1):
        console.print(f"  {i}. {opt}")
    raw = _k.ask(console, f"answer [1-{len(chs)}] · ? help · q quit: ", "quiz").lower()
    if raw == "q":
        raise KeyboardInterrupt
    try:
        pick = int(raw) - 1
    except ValueError:
        pick = -1
    ok = (pick == ans)
    console.print("[green]correct[/green]" if ok else f"[red]not quite — answer was {ans + 1}[/red]")
    console.print(f"[dim]why: {ck.get('why', '')}[/dim]")
    return ok


def ask_fillblank(console, ck: dict) -> bool:
    from lib import keys as _k
    if ck.get("code"):
        from rich.syntax import Syntax
        console.print(Syntax(ck["code"], ck.get("lang", "c"), theme="monokai"))
    raw = _k.ask(console, "fill in the blank · ? help · q quit: ", "quiz")
    if raw.lower() == "q":
        raise KeyboardInterrupt
    ok = (raw == str(ck.get("answer_text", "")).strip())
    console.print("[green]correct[/green]" if ok else f"[red]expected: {ck.get('answer_text')}[/red]")
    console.print(f"[dim]why: {ck.get('why', '')}[/dim]")
    return ok


def ask_microlab(console, ck: dict, book: str | None = None) -> bool:
    from lib import lab as _lab
    from lib import keys as _k
    code = ck.get("code", "")
    expect = ck.get("expect", "")
    if code:
        from rich.syntax import Syntax
        console.print(Syntax(code, ck.get("lang", "c"), theme="monokai"))
    console.print("[dim]predict-then-verify: type expected output, r=run it:[/dim]")
    raw = _k.ask(console, "expected output (r runs the code) · ? help: ", "quiz").strip()
    if raw.lower() == "q":
        raise KeyboardInterrupt
    if raw.lower() == "r" and code:
        r = _lab.run_code(code, ck.get("lang", "c"), timeout=2, book=book)
        if r.get("unsupported"):
            console.print(f"[yellow]no local runner for '{r['lang']}' — answer from the trace.[/yellow]")
        else:
            console.print(r["output"][:2000] if r["compiled"] else f"[red]{r['stderr'][:1000]}[/red]")
        raw = _k.ask(console, "now type the output: ", "quiz")
    ok = (raw == expect) if expect else True
    console.print("[green]correct[/green]" if ok else f"[red]expected: {expect!r}[/red]")
    console.print(f"[dim]why: {ck.get('why', '')}[/dim]")
    return ok


def run_check(console, block_id: str, idx: int, ck: dict, rng=None,
              book: str | None = None) -> tuple[bool, int]:
    kind = ck.get("kind")
    level_tag = f" · {ck['level'].upper()}" if ck.get("level") else ""
    console.print(f"\n[bold][{kind}{level_tag}][/bold] {ck.get('q', '')}")
    t0 = time.time()
    try:
        if kind in CHOICE_KINDS or ck.get("choices"):
            ok = ask_choice(console, ck, rng)
        elif kind == "fillblank":
            ok = ask_fillblank(console, ck)
        elif kind == "order":
            from lib import parsons as _p
            ok = _p.ask_order(console, ck, rng)
        elif kind == "micro-lab":
            ok = ask_microlab(console, ck, book)
        else:
            console.print(f"[red]unsupported kind {kind!r} — skipped[/red]")
            return False, 0
    except KeyboardInterrupt:
        console.print("[dim]quit.[/dim]")
        raise
    ms = int((time.time() - t0) * 1000)
    return ok, ms


def run(book: str, chapter: str, sample=None, seed=None, concept=None):
    """Interactive quiz over chapter checks or dedicated quiz questions, shuffled. Persists answers + run score."""
    import yaml
    from rich.console import Console
    from rich.table import Table
    from lib.pack import require_chapter
    from lib.srs import init_db, log_answer
    from lib.progress import record_quiz
    console = Console()
    try:
        data = yaml.safe_load(require_chapter(book, chapter).read_text(encoding="utf-8"))
    except FileNotFoundError:
        console.print(f"[yellow]No pack for {book}/{chapter} yet: run gen-prompt, paste YAML to packs/{book}/{chapter}.yaml, then validate.[/yellow]")
        return
    checks = filter_checks(collect_quiz_questions(data), concept)
    rng = random.Random(seed) if seed else None
    if rng:
        rng.shuffle(checks)
    if sample:
        checks = checks[:sample]
    if not checks:
        console.print("[yellow]No checks in this pack"
                      + (f" for concept {concept!r}" if concept else "") + ".[/yellow]")
        return
    con = init_db()
    score = 0
    done = 0
    results: list[tuple[str, bool]] = []
    try:
        for block_id, idx, ck in checks:
            try:
                ok, ms = run_check(console, block_id, idx, ck, rng, book)
            except KeyboardInterrupt:
                break
            log_answer(con, book, chapter, block_id, idx, ok, ms,
                       concept=str(ck.get("concept", "")))
            done += 1
            score += ok
            results.append((str(ck.get("concept", "")), bool(ok)))
    finally:
        con.close()
    console.print(f"\n[bold]score: {score}/{done}[/bold]")
    if done:
        record_quiz(book, chapter, score, done, seed,
                    items=[f"{b}:{i}" for b, i, _ in checks[:done]])
        by = tally(results)
        t = Table(title="by concept")
        t.add_column("concept"); t.add_column("hits"); t.add_column("total"); t.add_column("pct")
        for c, (h, n) in sorted(by.items()):
            t.add_row(c, str(h), str(n), f"{100.0 * h / n:.0f}%")
        console.print(t)
        weak = sorted(((c, h / n) for c, (h, n) in by.items() if h < n),
                      key=lambda r: r[1])
        console.print("[bold]weakest:[/bold] " + ", ".join(c for c, _ in weak[:3])
                      if weak else "[green]no weak concepts — all 100%[/green]")


def score_chapter(book: str, chapter: str) -> dict:
    """Non-interactive evidence for the test gate: last recorded quiz run. (FR-TEST-002)"""
    from lib.progress import get_last_quiz
    return get_last_quiz(book, chapter) or {"score": 0, "total": 0}

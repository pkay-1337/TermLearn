#!/bin/python3
"""Entry point — CLI routing only. Domain logic MUST live in lib/. (SRS CR-DES-001, IF-CLI-001..005)"""
import typer

from lib import books as books_mod

app = typer.Typer(help="termlearn — learn technical books in the terminal. See docs/SRS.md")


@app.command()
def books():
    """List discovered books with pack coverage + mastery. (FR-BOOK-001..002)"""
    books_mod.list_books()


@app.command()
def chapters(book: str = typer.Option(..., "--book", help="Book slug, e.g. extreme-c")):
    """List chapters in author order with status. (FR-CHAP-001..002)"""
    books_mod.list_chapters(book)


@app.command()
def extract(
    book: str = typer.Option(..., "--book", help="Book slug"),
    force: bool = typer.Option(False, "--force", help="Overwrite raw_chapters (backs up first)"),
):
    """Extract EPUB -> raw_chapters/*.txt + meta.json. (FR-EXT-001..006)"""
    from lib import epub_extract
    epub_extract.extract_book(book, force=force)


@app.command()
def gen_prompt(
    book: str = typer.Option(..., "--book"),
    chapter: str = typer.Option(..., "--chapter", help="Chapter id, e.g. ch01"),
    mode: str = typer.Option("master", "--mode", help="Prompt mode: meta, study, quiz, labs, cards, test, master, all, or legacy"),
    out: str = typer.Option("", "--out", help="Optional output file or directory"),
):
    """Emit AI generation prompt(s) for a chapter. (FR-GEN-001..003)"""
    from lib import ai_prompt
    ai_prompt.emit(book, chapter, mode=mode, out=out or None)


@app.command()
def split(
    book: str = typer.Option(..., "--book", help="Book slug"),
    chapter: str = typer.Option(..., "--chapter", help="Chapter id, e.g. ch01"),
    backup: bool = typer.Option(True, "--backup/--no-backup", help="Keep original monolithic file as .yaml.bak"),
):
    """Split a monolithic chapter YAML into a modular directory pack."""
    from lib import pack
    pack.split_chapter_to_modular(book, chapter, backup=backup)



@app.command()
def validate(
    book: str = typer.Option(..., "--book"),
    chapter: str = typer.Option("", "--chapter", help="Empty = all chapters"),
    strict: bool = typer.Option(False, "--strict", help="Warnings become errors"),
    fix_hints: bool = typer.Option(False, "--fix-hints", help="Print repair suggestions (advisory, changes nothing)"),
):
    """Validate packs/<slug> YAML + refs + gcc probes. (FR-VAL-001..004)"""
    from lib import pack
    ok = pack.validate_book(book, chapter or None, strict=strict, fix_hints=fix_hints)
    raise typer.Exit(0 if ok else 1)


@app.command()
def study(book: str = typer.Option(..., "--book"), chapter: str = typer.Option(..., "--chapter")):
    """Learn-first traversal of concept blocks. (FR-STUDY-001..006)"""
    from lib import study as m
    m.run(book, chapter)


@app.command()
def revise(book: str = typer.Option(..., "--book"), chapter: str = typer.Option(..., "--chapter")):
    """Passive notes + concepts, no scoring. (FR-REV-001..002)"""
    from lib import revise as m
    m.run(book, chapter)


@app.command()
def quiz(
    book: str = typer.Option(..., "--book"),
    chapter: str = typer.Option(..., "--chapter"),
    sample: int = typer.Option(0, "--sample", help="0 = all"),
    seed: int = typer.Option(0, "--seed"),
    concept: str = typer.Option("", "--concept", help="Only checks with this concept tag"),
):
    """Run chapter checks shuffled. (FR-QUIZ-001..003)"""
    from lib import quiz as m
    m.run(book, chapter, sample=sample or None, seed=seed or None,
          concept=concept or None)


@app.command()
def parsons(book: str = typer.Option(..., "--book"), chapter: str = typer.Option(..., "--chapter")):
    """Parsons ordering interaction. (FR-PAR-001..003)"""
    from lib import parsons as m
    m.run(book, chapter)


@app.command()
def lab(
    book: str = typer.Option(..., "--book"),
    chapter: str = typer.Option(..., "--chapter"),
    no_save_solution: bool = typer.Option(False, "--no-save-solution", help="Log verdict only, do not retain code"),
):
    """Editable compile-and-run lab with hidden tests. (FR-LAB-001..003)"""
    from lib import lab as m
    m.run(book, chapter, save_solution_on_test=not no_save_solution)


@app.command()
def test(book: str = typer.Option(..., "--book"), chapter: str = typer.Option(..., "--chapter"), force: bool = typer.Option(False, "--force")):
    """Chapter mastery gate, deterministic. (FR-TEST-001..004)"""
    from lib import lab as _lab  # test reuses quiz+lab runners
    from lib import quiz as _quiz
    from lib import pack as _pack
    from lib import progress as _prog
    # thin orchestration; scoring lives in lib modules (CR-DES-001)
    _pack.require_chapter(book, chapter)
    q = _quiz.score_chapter(book, chapter)
    l = _lab.check_lab(book, chapter, non_interactive=True)
    ok = _prog.record_test(book, chapter, q, l, force=force)
    raise typer.Exit(0 if ok else 1)


@app.command()
def srs(book: str = typer.Option("", "--book", help="Empty = all books")):
    """Cross-chapter due queue, SM-2. (FR-SRS-001..004)"""
    from lib import srs as m
    m.run(book or None)


@app.command()
def stats(
    book: str = typer.Option(..., "--book"),
    reset: bool = typer.Option(False, "--reset", help="Wipe progress after confirmation"),
    chapter: str = typer.Option("", "--chapter", help="With --reset: limit wipe to chapter"),
):
    """Mastery, per-concept accuracy, due counts, weak spots. (FR-STAT-001..003)"""
    from lib import stats as m
    if reset:
        m.reset_progress(book, chapter or None)
    else:
        m.run(book)


@app.command()
def export(
    book: str = typer.Option(..., "--book"),
    chapter: str = typer.Option("", "--chapter"),
    format: str = typer.Option("md", "--format"),
    out: str = typer.Option("", "--out", help="Write to file instead of stdout"),
):
    """Export notes to Markdown. (FR-EXP-001..002)"""
    from lib import export_md as m
    m.run(book, chapter or None, format, out or None)


@app.command()
def tui(
    book: str = typer.Option("", "--book", help="Start at a book's chapters"),
    chapter: str = typer.Option("", "--chapter", help="With --book: open the chapter menu directly"),
):
    """Launch the Textual TUI (same packs as the CLI)."""
    from tui.app import run
    run(book=book, chapter=chapter)


if __name__ == "__main__":
    app()

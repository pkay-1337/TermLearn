# termlearn — terminal interactive learning from technical books

See `docs/SRS.md` (IEEE 29148 + RFC 2119, normative).

## Quickstart (v0.1, Rich CLI)

```bash
pip install -r requirements.txt
python main.py --help
python main.py books                  # list books (FR-BOOK)
python main.py chapters --book extreme-c
python main.py extract --book extreme-c
python main.py gen-prompt --book extreme-c --chapter ch01
python main.py validate --book extreme-c [--chapter ch01] [--strict]
python main.py study --book extreme-c --chapter ch01
python main.py revise --book extreme-c --chapter ch01
python main.py quiz --book extreme-c --chapter ch01
python main.py parsons --book extreme-c --chapter ch01
python main.py lab --book extreme-c --chapter ch01
python main.py test --book extreme-c --chapter ch01
python main.py srs --book extreme-c
python main.py stats --book extreme-c
python main.py export --book extreme-c --format md
```

## Layout (SRS §2.5)

- `main.py` — CLI routing only (CR-DES-001)
- `lib/` — domain logic (one module per mode)
- `books/<slug>/source.epub` — source truth; `raw_chapters/*.txt` + `meta.json` generated
- `packs/<slug>/book.yaml` + `chNN.yaml` — AI-generated teaching packs (sole runtime source)
- `prompts/GENERATE.md`, `ASK_USER.md` — normative AI contract
- `tests/` + `tests/fixtures/` — synthetic fixtures first (VR-001..003), pilot book for e2e (VR-004/006)

Pilot book: `books/extreme-c/source.epub` (Extreme C).

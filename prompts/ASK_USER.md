# ASK_USER.md — interrogation template (SRS FR-ASK-001..003)
# The AI MUST ask these BEFORE emitting YAML. MUST NOT emit final YAML until
# the user answers or says `use defaults`.

Ask (compact, one message, numbered):

1. **Level** — novice / comfortable-in-C / experienced? (affects depth of
   `explain_md` and whether `model` blocks get extra `viz` steps.)
   Default: comfortable-in-C.
2. **Depth vs speed** — deep (more blocks, ≥3 checks each) or fast (fewer
   blocks, 1-2 checks each) or balanced (2 blocks per major concept)? Default: deep.
3. **Prioritize / skip** — which sections/examples of this chapter matter most?
   Any to skip (e.g. Windows-only notes, C++ tangents)? Default: keep all,
   skip platform tangents.
4. **Lab difficulty + toolchain** — easy (fill 3-5 lines) / medium (write a
   function) / hard (multi-file)? Which language + runner (pilot default: C
   with `gcc -Wall -std=c99`, 2 s timeout — state yours, e.g. `python3`,
   `node`, `go run`)? No executable code in this chapter? Say so — labs are
   omitted then. Default: easy-medium, declared toolchain.
5. **Explanation language** — English default; other allowed for prose only
   (keys stay English per CR-GEN-003).
6. **Interleaved review** — how much from prior chapters (0 / 2 / 4 checks)?
   Default: 2.

Record the answers as `gen_notes.md` next to the pack (RECOMMENDED): the human
operator pastes answers there for reproducibility. Then emit the YAML per
GENERATE.md.

# ASK_USER.md — interrogation template (SRS FR-ASK-001..003)
# The AI MUST ask these BEFORE emitting YAML. MUST NOT emit final YAML until
# the user answers or says `use defaults`.
#
# 1. 100% SELF-CONTAINED QUESTIONS & EXPLANATIONS: NEVER refer to external book examples, code boxes, listings, figures, or exercises in questions OR explanations
#    (e.g. NEVER write "In Example 7.2...", "In Code Box 7-6...", "In Listing 3...", "Refer to question 4 in book").
#    The student is studying in a terminal and does not have the book. Always embed the complete code
#    snippet directly in `code: |` with `lang: c` or write out the entire concrete scenario in `q:`.
#    If a question tests what a function does or its return value, SHOW THE FUNCTION CODE directly in the question.
#    Explanations (`why:`) must explain the underlying mechanics directly, never saying "In Code Box X-Y...".
# 2. NEVER worry about YAML length — multi-turn generation across sequential steps is supported.
# 3. Always include thorough, line-by-line explanations for every code block and reveal the Notional Machine.
# 4. Put all your might and go Plus Ultra — zero half-assing, no placeholders.
# 5. Author 5–10 scaffolded checks per block according to topic, plus 30–50 dedicated questions under top-level 'quiz:' spanning mixed difficulty levels in no specific order, separate from immediate block checks, including code boxes where relevant.

Ask (compact, one message, numbered):

1. **Level** — novice / comfortable-in-C / experienced? (affects depth of
   `explain_md` and whether `model` blocks get extra `viz` steps.)
   Default: comfortable-in-C.
2. **Depth vs speed** — deep (more blocks, 5–10 checks each according to topic) or fast (fewer
   blocks, 3–5 checks each) or balanced (2 blocks per major concept)? Default: deep.
   *(Note: YAML length is unlimited — multi-turn / multi-step generation is fully supported
   so no concepts or code explanations are ever rushed or cut short).*
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

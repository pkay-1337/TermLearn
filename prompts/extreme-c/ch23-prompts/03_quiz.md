# =============================================================================
# INSTRUCTIONS FOR AI AGENT / CHAT: CHAPTER QUIZ QUESTIONS
# TARGET OUTPUT FILE: packs/extreme-c/ch23/quiz.yaml
#
# [DIRECTIVES FOR quiz.yaml]
# 1. Read the chapter from `books/extreme-c/raw_chapters/ch23.txt` (see master_prompt.md).
# 2. Author 30 to 50 dedicated, standalone diagnostic questions testing cumulative synthesis.
# 3. Distribute questions across three difficulty levels: 'level: intro | core | advanced'.
# 4. Mix question kinds: 'mcq', 'predict', 'why-fails', 'fillblank', 'order', 'trace', 'spot-bug'.
# 5. SELF-CONTAINED CODE: Whenever testing code behavior or bugs, embed the code snippet directly
#    in the question via 'code: |'. Never reference external book exercise numbers or listings.
# 6. ANSWER RANDOMIZATION: Uniformly distribute correct answer positions across 0, 1, 2, and 3.
# 7. ELABORATED WHY: Every question MUST provide a comprehensive 'why:' explaining the core rule
#    and naming the exact misconception each wrong distractor traps.
# 8. OUTPUT FORMAT: Single YAML document with top-level 'quiz: [...]'.
#
# [POST-GENERATION VERIFICATION FOR quiz.yaml]
# - Count: 30–50 questions.
# - Levels: intro + core + advanced all present.
# - No duplicates: no q string identical to any block-check q.
# - Mixed: not grouped by level or concept.
# - Concept coverage: distinct concepts span core chapter topics (e.g. composition, aggregation, ownership, diagnostics).
# - Each item carries 1.1–1.10 (positively worded, 2-4 choices, answer in bounds, randomized answer index,
#   self-contained with embedded code, elaborated why, exact kinds, scrambled order, load-bearing fillblank, width <=80/120 cols).
#
# COMMON RULES: see master_prompt.md for GENERATE.md, ASK_USER.md,
# the SRS §4.8 / §4.9 excerpts, and the chapter source assets.
# Chapter text: books/extreme-c/raw_chapters/ch23.txt
# (A verbatim copy ships in this prompt bundle as chapter.txt)
# MODE TARGET: QUIZ
# =============================================================================

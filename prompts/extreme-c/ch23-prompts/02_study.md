# =============================================================================
# INSTRUCTIONS FOR AI AGENT / CHAT: CONCEPT BLOCKS & STUDY CONTENT
# TARGET OUTPUT FILE: packs/extreme-c/ch23/study.yaml
#
# [DIRECTIVES FOR study.yaml]
# 1. Read the chapter from `books/extreme-c/raw_chapters/ch23.txt` (see master_prompt.md).
# 2. Dedicate your full cognitive might to deep, pedagogical explanations.
# 3. Break the chapter into as many single-concept blocks as needed ('blocks: [...]'); no set count — one block per concept.
# 4. For each block:
#    - 'id': unique block id ('b1', 'b2', ...)
#    - 'type': 'model' | 'syntax' | 'design' | 'algorithm'
#    - 'title': functional, action-oriented concept title
#    - 'explain_md': rich, intuitive Markdown explanation (5–20 lines) breaking down
#      syntax, Notional Machine state transitions, and memory lifecycle.
#    - 'example': runnable code snippet with 'run_expected' stdout; non-trivial code MUST also
#      carry 'explain_md' (2–6 lines of Markdown rendered right under the code); optional 'subgoals'
#    - 'diagram': OPTIONAL block-level structure picture for model/design blocks with non-memory
#      structure (call graph, data flow, layering) — kind: flow (nodes/edges, ids unique, refs
#      resolvable, ≤14 nodes) or kind: art (verbatim ASCII, no ANSI); optional caption + steps ≤6
#    - 'viz': stepped ASCII memory diagrams for every 'model' block (2–6 steps).
#    - 'checks': 5 to 10 scaffolded micro-checks per block ('predict', 'why-fails',
#      'mcq', 'fillblank', 'order' with 'faded: true', 'eipe', 'choose-better', 'trace', 'spot-bug').
#      Every check MUST have an elaborated 'why:' explaining the principle and diagnosing distractors.
#    - fillblank answers MUST be one word/token; if a multi-word expression or a line is unavoidable,
#      the stem MUST state the exact answer format (e.g. 'Answer format: `res->field`').
#    - order stems MUST state how many correct lines to place, or say all displayed lines are used;
#      when a distractor is present, say so (e.g. 'Order the 5 correct lines; one line is a distractor').
#    - All choices in one set MUST be uniform in length and grammatical form; the correct answer must
#      not be identifiable by being the longest or shortest (aim for max/min ratio <=1.3).
# 5. OUTPUT FORMAT: Single YAML document with top-level 'blocks: [...]'.
#
# [POST-GENERATION VERIFICATION FOR study.yaml]
# - Runnable code: every blocks[].example.code compiles under packs/extreme-c/book.yaml: toolchain.
# - If run_expected is declared, it matches actual output for a correct solution.
# - Model blocks have viz; design blocks have eipe/choose-better; syntax/algorithm blocks have order.
# - Every non-trivial example.code has explain_md; diagram stanzas (if any) use exact vocabularies.
# - Each check carries rules 1.1–1.10 (positively-worded, randomized answers, embedded code, elaborated why).
#
# COMMON RULES: see master_prompt.md for GENERATE.md, ASK_USER.md,
# the SRS §4.8 / §4.9 excerpts, and the chapter source assets.
# Chapter text: books/extreme-c/raw_chapters/ch23.txt
# (A verbatim copy ships in this prompt bundle as chapter.txt)
# MODE TARGET: STUDY
# =============================================================================

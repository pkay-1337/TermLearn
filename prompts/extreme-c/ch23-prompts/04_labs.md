# =============================================================================
# INSTRUCTIONS FOR AI AGENT / CHAT: PRACTICAL LAB WORKSPACES
# TARGET OUTPUT FILE: packs/extreme-c/ch23/labs.yaml
#
# [DIRECTIVES FOR labs.yaml]
# 1. Read the chapter from `books/extreme-c/raw_chapters/ch23.txt` (see master_prompt.md).
# 2. Author 1 to 4 practical, multi-file coding challenges.
# 3. STUDENT ACTION REQUIRED — NEVER EMIT PRE-SOLVED SOLUTIONS:
#    - Student implementation files MUST BE SCAFFOLDED OR BLANK (empty string, stubs, '/* TODO */').
#    - Supporting framework files (headers '.h', interactive drivers 'main.c', and unit test runners
#      'test_runner.c') provide the deterministic assertions.
# 4. Initial verification test MUST fail on unedited starter files, and pass once implemented.
# 5. Provide language-agnostic commands ('run' and 'test'), automated 'test_cases' with unified diffs,
#    and 1–3 progressive hints (general -> specific).
# 6. LAB INSTRUCTION QUALITY (MUST):
#    - Begin every instruction_md with a short, plain-language '### What You Are Building' section
#      that explains the object/behavior the student will build and how it behaves, without jargon.
#    - After that intro, make the requirements an unambiguous contract: name exact APIs, constants,
#      struct fields, return values, and error codes; define vague terms; avoid ambiguous pronouns.
#    - Specify validation precedence when several errors can apply, plus empty/full/zero/maximum,
#      invalid/closed, and lifecycle cases. Include a worked example or exact expected 'run' output.
#    - The instruction must stand alone: do not leave required behavior inferable only from headers,
#      hints, tests, or the reference solution. Resolve any 'could two implementations differ?' gap.
# 7. OUTPUT FORMAT: Single YAML document with top-level 'labs: [...]'.
#
# [POST-GENERATION VERIFICATION FOR labs.yaml]
# - Contract: each lab has id, title, instruction_md, non-empty safe files, commands.run/test, test_cases[].expect, progressive hints.
# - Instruction intro: every instruction_md starts with a plain-language 'What You Are Building' section.
# - Unambiguous contract: exact APIs/fields/returns, error precedence, boundary and lifecycle cases, and a worked example; no behavior only inferable from tests or hints.
# - Blank starters: implementation file(s) content: "" or TODO-stubbed; headers/drivers/test-runners complete.
# - Fail-first: running commands.test on the untouched starter must FAIL (missing symbols/compile error).
# - Safe commands: no denylisted patterns (rm -rf, curl, wget, ssh, mkfs, fork bombs); no network.
# - Hints ordered: general -> specific -> operation.
# - Code lines: no line-count or column caps — include as much as the lab needs.
# - Cannot be fully automated (need a solution trace):
#   * commands.run output byte-matches test_cases[].expect for a reference solution.
#   * Fail->pass lifecycle verified with a real reference implementation.
#
# COMMON RULES: see master_prompt.md for GENERATE.md, ASK_USER.md,
# the SRS §4.8 / §4.9 excerpts, and the chapter source assets.
# Chapter text: books/extreme-c/raw_chapters/ch23.txt
# (A verbatim copy ships in this prompt bundle as chapter.txt)
# MODE TARGET: LABS
# =============================================================================

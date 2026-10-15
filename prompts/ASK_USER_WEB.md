# ASK_USER_WEB.md — interrogation template for Web-Native Chapter Studies
# The AI MUST ask these questions BEFORE generating HTML/Web study packs.
# MUST NOT emit final chapter files until the user answers or says `use defaults`.
#
# MANDATORY DIRECTIVES:
# 1. The learner studies SOLELY from the generated interactive web chapter — never from the book.
# 2. Never refer to exercises or problem numbers in the book; make every scenario self-contained.
# 3. Put all your might and go Plus Ultra — zero half-assing, no placeholders.
# 4. Standalone zero-build architecture: pure HTML5 + SVG + CSS + JS + dedicated `server.py`.

Ask (compact, one message, numbered):

1. **Target Audience & Prior Knowledge**:
   - Novice / Comfortable-in-language / Experienced systems engineer?
   - Default: *Comfortable-in-language* (requires deep Notional Machine breakdowns without trivial hand-waving).

2. **Interactive Archetypes to Prioritize** (select 1–3 to emphasize):
   - A. **Direct Manipulation Scrubbers**: Drag-to-resize geometry, angle sweepers, continuous mathematical sliders.
   - B. **Constrained Memory Sandboxes**: Drag-and-drop pointer connections, stack/heap frame allocators, leak detectors.
   - C. **Algorithmic State Steppers**: Code execution cursor synchronized with memory tables and pointer transitions.
   - D. **Interactive Bug Spotters**: Hands-on inspection of compiler diagnostics, sanitizer warnings, and memory leaks.
   - Default: *Balanced multi-archetype progression* matching the chapter's conceptual domain.

3. **Execution & Simulation Fidelity**:
   - Pure client-side simulation (self-contained reactive state machine in JS/SVG; zero install).
   - Local runner integration via chapter `server.py` (live compilation/execution through host toolchain like `gcc`/`python3`).
   - Default: *Pure client-side simulation with optional server.py runner hook*.

4. **Curriculum Scope & Prioritized Sections**:
   - Which specific sections or mental models of this chapter matter most?
   - Any platform-specific quirks (e.g. Windows/macOS tangents) to skip?
   - Default: *Cover all core conceptual units; skip platform-specific tangents*.

5. **Visual Theme & Typography**:
   - Brilliant Dark Mode (`#0f172a` canvas, `#38bdf8` sky blue handles, `#22c55e` emerald success) or High-Contrast Light Mode?
   - Default: *Brilliant Dark Mode*.

6. **Interleaved Prior Concepts**:
   - How many review/contrasting checks from prior chapters to weave in (0, 2, or 4)?
   - Default: *2 contrasting review challenges*.

Record the answers as `web_gen_notes.md` inside `web_pack/<book>/<chapter>/` (RECOMMENDED) for reproducibility. Then emit the web study pack per `GENERATE_WEB.md`.

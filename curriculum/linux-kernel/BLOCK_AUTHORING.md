# Block Authoring Method

This is the local pedagogy contract for `linux-kernel` chapter packs. It says how to turn evidence into blocks that actually teach. It does not replace the normative schema: use `docs/SRS.md` §4.8 for the pack contract, `prompts/GENERATE.md` for global generation rules, `prompts/checks_after_chapter_creation.md` for post-creation verification, and `PLAN.md` for the evidence-first gate.

If this document conflicts with `docs/SRS.md`, the SRS wins. If it conflicts with a vague memory of a textbook, this document wins.

## 1. What a block is for

A block is not a section of notes. A block is one deliberately designed learning event that changes what the learner can do.

A block is complete only when the learner can, without notes:

1. state the invisible mechanism in their own words;
2. predict what happens in a new but nearby case;
3. interpret a second signal that confirms or contradicts the first;
4. explain where the model stops working or what failure mode it creates.

If the learner can only repeat a definition, the block is a fact dump and MUST be rewritten.

## 2. Non-negotiable design rules

- **One skill per block.** The objective must name one observable performance. If two mental models, two diagrams, or two unrelated evidence artifacts are needed, split the block.
- **Evidence before prose.** Every factual claim must trace to an evidence ID in `curriculum/linux-kernel/evidence/<chapter>/`.
- **One notional machine.** Each block must make explicit what the learner should believe is happening underneath the visible syntax, command, or source line.
- **Teach causally.** Explain what changes state, what observes the state, what can go wrong, and why the observed evidence has that shape.
- **No fact dump.** A list of terms, flags, structs, line numbers, or command outputs is not instruction.
- **Checks are part of the lesson.** Checks target the exact misconception the block is meant to remove; they are not an afterthought.
- **Fading is required.** Move from worked example to completion to prediction to diagnosis to transfer.
- **Second signal required where possible.** Pair source with runtime, one tool with another, a prediction with an observed trace, or a counter with a packet capture.
- **Interleave prior knowledge.** Each chapter MUST include at least two checks that force discrimination against earlier blocks or chapters.
- **Fail closed.** If evidence is missing, record an open question. Do not invent output, flags, line numbers, register values, packet paths, or behavior.

## 3. Evidence-to-block pipeline

Use this sequence for every block.

### 3.1 Build the evidence inventory

For the chapter bundle, list each evidence ID and what it can prove.

```text
E-T0A-05: gcc diagnostic for bad.c; proves compiler error shape and file/line location.
E-T0A-06: corrected build transcript; proves effect of one minimal fix.
E-A1-04: boot/gdb transcript; proves eip reached main at init/main.c:107.
```

An evidence item that proves nothing specific is not useful. Rewrite the capture or drop it.

### 3.2 Extract idea units

From the evidence, enumerate every checkable idea unit: concept, state transition, procedure, boundary case, warning, command shape, output column, or design trade-off.

Example idea units:

```text
- A compiler diagnostic names file, line, and error class before runtime begins.
- `gcc -g` changes debug metadata, not generated program semantics.
- gdb can stop before `main` and inspect registers from the remote target.
- `main` receives control after boot/setup/head setup, not at reset.
```

### 3.3 Name the misconception

For each idea unit, write the wrong model the learner is likely to bring.

```text
Idea unit: gdb starts only after libc initialization.
Misconception: a debugger can only inspect source after `main`.
Evidence that refutes it: E-T1A-05/E-A1-08 breakpoint before or at `main`.
```

A block without a named misconception usually becomes a definition list.

### 3.4 Write one falsifiable objective

Use this shape:

> Given `<evidence-backed situation>`, the learner can `<observable action>` so that `<checkable result>`.

Good:

> Given the captured `gcc` diagnostic and matching source, the learner can identify the first failing file/line and choose the minimal fix that makes the next build succeed.

Bad:

> Understand compiler errors.

Bad objectives contain words like `understand`, `know`, `learn`, or `appreciate` without an observable action.

### 3.5 Storyboard the teaching arc

Every block follows this arc unless the block type requires a justified variant:

1. **Elicit** — ask for a prediction before revealing the mechanism.
2. **Model** — show the notional machine: objects, state, transitions, owner, and boundary.
3. **Work** — walk one concrete worked example from evidence.
4. **Fade** — remove support and make the learner complete, predict, or diagnose.
5. **Contrast** — show a near miss, failure mode, or alternative design.
6. **Retrieve** — require answer from memory, then explain why.
7. **Transfer** — apply the same skill to a new case or earlier chapter.

### 3.6 Draft from evidence

Write `explain_md` from the captured source/output only. Put the block-to-evidence map in `gen_notes.md`, and set chapter `meta.source_ref` to the evidence bundle path plus IDs used by the chapter.

Recommended audit line:

```text
b4 <- E-T0A-05, E-T0A-06; claim: diagnostic -> fix -> successful rebuild.
```

Do not put raw evidence IDs in learner-facing question text unless they are part of the fiction of a diagnostic artifact.

### 3.7 Verify mechanically

Before declaring the block ready:

- re-run the command or trace in a clean workspace;
- compare exact source snippets against the pinned commit/tag;
- confirm expected output is captured output after normalizing volatile fields;
- run the `tinker` command before writing it into a lab;
- run `python main.py validate --book linux-kernel --chapter <id> --strict`.

## 4. Block types in this curriculum

| Type | Teaches | Best evidence | Required checks | Best artifact |
|------|---------|---------------|-----------------|---------------|
| `model` | Invisible mechanism or state transition | source path, trace, register/memory/packet state | `predict` or `why-fails`, plus `trace`/`viz`/`diagram` where spatial | state transition diagram or stepped trace |
| `syntax` | Surface form, command shape, output shape, API idiom | exact command, transcript, diagnostic | `fillblank`/`order`, plus `why-fails` | annotated command/output |
| `algorithm` | Procedure over states | source path, call sequence, trace table | `predict` + `order` or `micro-lab` | numbered trace table |
| `design` | Judgment under constraints | diff, failed build, trade-off evidence | `eipe` or `choose-better` | decision note with rejected alternative |

Do not choose a `type` because it is easy. Choose it by what the learner must do.

## 5. The explanation recipe

A good `explain_md` is 5–15 lines and does five jobs.

1. **Frame the question.** Start with the problem the mechanism answers.
2. **Name the notional machine.** State what exists, who owns it, and what state matters.
3. **Walk one worked case.** Trace the exact evidence artifact; do not generalize before the learner sees a concrete case.
4. **Expose the boundary.** State the failure mode, misleading output, or condition where the simple model breaks.
5. **Compress the rule.** End with a compact generalization that can be retrieved later.

Example pattern:

```text
The question is not "what flag do I type?" but "what does this tool observe?"

The notional machine here is: the compiler reads translation units, builds symbol
and type information, then reports the first structural failure it cannot repair.

Look at E-T0A-05: the diagnostic names bad.c:6 before any program output exists.
That means this failure belongs to translation, not execution.

The boundary is that a diagnostic is evidence about one failed path, not a list of
every bug. Fixing the first error can expose a later error.

Rule: read the diagnostic as a state report from the compiler, then change one
thing and rerun the observation.
```

Anti-patterns:

- "This flag enables debugging." — names no state change.
- "The kernel does X." — names no file, transition, or evidence.
- "As shown above." — blocks are studied standalone.
- "This is standard/self-explanatory." — the block has not taught anything.
- A bullet list of every field/flag before one worked case — high extraneous load.

## 6. Worked examples and fading

Novices need worked examples; expertise comes from gradually removing support. Use four levels.

| Level | Author action | Learner action | Good check kinds |
|-------|---------------|----------------|------------------|
| F0 Worked | Fully annotated source/output/trace | Follow and self-explain | `eipe`, short `mcq` |
| F1 Completion | One field, line, column, or transition omitted | Fill the missing piece | `fillblank`, `order` |
| F2 Prediction | Mechanism shown, result hidden | Predict result before reveal | `predict`, `trace` |
| F3 Diagnosis | Wrong result or broken artifact shown | Identify cause and repair | `why-fails`, `spot-bug` |
| F4 Transfer | New nearby case | Apply skill without cue | interleaved check, `choose-better` |

Rules:

- Every worked example MUST come from evidence or be marked `adapted: true` with a reason.
- Annotate the state before, the state-changing step, and the state after.
- Do not explain every trivial token. Spend explanation on load-bearing transitions.
- Ask at least one self-explanation question: "Why this and not the near miss?"
- For a tool, the worked example must include what the tool cannot observe.
- For a kernel source path, the worked example must include the handoff into the next subsystem or function.

## 7. Check authoring

### 7.1 Check ladder for 5–10 checks

A block with 5–10 checks should cover several cognitive actions:

1. **Recognition** — identify the object, meaning, or output shape.
2. **Prediction** — simulate the mechanism.
3. **Ordering** — reconstruct a procedure or call sequence.
4. **Diagnosis** — explain a failure or misleading output.
5. **Discrimination** — choose between two close models.
6. **Transfer/interleaving** — apply the skill to a prior or adjacent case.

Do not write ten variants of "what does this flag stand for?"

### 7.2 Check quality rules

- The stem is positively worded and self-contained.
- The full code, transcript, or concrete scenario is embedded.
- Choices are 2–4, parallel in grammar and roughly similar in length.
- Each distractor encodes a real misconception, not a random error.
- The correct answer is not always the longest option or position `0`.
- `why:` states the principle and names the misconception trapped by each distractor.
- `predict` checks name a tracing strategy and ask for state, not a vibe.
- `trace` checks use a real state table with one load-bearing mutation.
- `spot-bug` checks use an authentic diagnostic or failure transcript.
- `eipe` and `choose-better` checks compare relationships or trade-offs, not trivia.
- No references to "above", "the example", "listing", "page", "earlier exercise", or unseen material.
- At least two chapter checks MUST be interleaved from earlier chapters with valid `from_chapter` and `from_block`.

### 7.3 Distractor design

Write distractors from observed failure modes:

- wrong tool for the symptom;
- right tool, wrong scope;
- source line from a different version;
- treating compile-time evidence as runtime evidence;
- treating a counter as a packet payload;
- assuming reset state when the trace starts at `main`;
- confusing current state with a previous state;
- choosing a fix that hides the diagnostic instead of fixing the cause.

A distractor that no learner would actually choose wastes a check slot.

## 8. Tool blocks

Tool chapters use the same block rules plus the tool mastery protocol in `STUDY_METHOD.md`.

Every tool block MUST answer:

1. What does this tool observe?
2. What can it not observe?
3. What is the smallest workload where the output is interpretable?
4. What do the important columns/fields mean?
5. What filter removes noise without hiding the signal?
6. What controlled failure changes the output?
7. What second tool confirms the claim?
8. What symptom would make the learner choose this tool later?

A lab that only says "run this command and paste the output" is not a lab. It must include a prediction, one change, one observed difference, one failure-mode question, and a teach-back prompt.

## 9. Kernel source blocks

Kernel blocks must keep source evidence and runtime evidence distinct.

- Use exact `commit:path:line` references from the pinned tree.
- Cite `sources/early-history.git@0.11` for pristine 0.11 source claims.
- Cite `sources/Linux-0.11-fork@<commit>` only for build/boot/gdb harness claims.
- Do not read modern source into old-kernel explanations except as an explicitly marked contrast.
- For a code path, teach the handoff: entry → function → state mutation → callee/return → observable effect.
- For a structure, teach owner, lifetime, key fields, invariant, and failure if invariant breaks.
- For a boot/assembly block, name the current execution context and what state is or is not available yet.
- Kernel excerpts use `lang: text` or `lang: asm`, never `lang: c`, as required by `PLAN.md`.

## 10. Interleaving and spacing

Interleaving should feel slightly harder than blocked practice because the learner must first decide which model applies.

Use it in three places:

1. **Within a chapter** — mix check kinds and concepts after the initial teaching sequence.
2. **Across chapters** — include at least two checks from earlier chapters.
3. **In the quiz and final checks** — ask synthesis questions that require a current and a prior model together.

Spacing is achieved by reusing older blocks in new contexts, not by telling the learner to reread notes.

## 11. Metacognition and teach-back

The learner must practice judging their own understanding.

Add one of these to each chapter:

- "Predict before reveal, then rate confidence 1–3."
- "Which evidence would falsify your explanation?"
- "What did this tool not show you?"
- "Name the part of your model that changed after the experiment."
- "Write a three-line mini-manual: when to use, how to read one field, one pitfall."

Checks and labs should expose overconfidence rather than reward familiarity.

## 12. Research basis

These findings justify the rules above. They do not replace evidence from the chapter bundle.

| Finding | Use here |
|---------|----------|
| Retrieval practice improves meaningful learning more than repeated elaborative study; learners often underuse it (Karpicke & Blunt, *Science*, 2011, DOI `10.1126/science.1199327`). | Prediction, `trace`, cards, no-note explain-back. |
| Practice testing, distributed practice, and interleaving have strong or moderate utility; highlighting and rereading are weak (Dunlosky et al., *PSPI*, 2013, DOI `10.1177/1529100612453266`). | 5–10 checks per block, spaced reuse, interleaved prior checks. |
| Cognitive load theory: instruction should manage extraneous load and adapt guidance to learner expertise (Sweller, Ayres, & Kalyuga, *Cognitive Load Theory*, 2011, DOI `10.1007/978-1-4419-8126-4`). | One skill per block, one notional machine, worked examples then fading. |
| A notional machine should be an explicit learning objective, and different levels may be needed (Sorva, *ACM TOCE*, 2013, DOI `10.1145/2483710.2483713`). | State notional machine in every block; avoid vague "the kernel does X". |
| Self-explanations help learners refine conditions/actions and monitor understanding (Chi et al., *Cognitive Science*, 1989, DOI `10.1207/s15516709cog1302_1`). | `why:` explanations, self-explanation prompts, teach-back. |
| Worked examples are effective for initial acquisition, but guidance must fade (Renkl, *Cognitive Science*, 2014, DOI `10.1111/cogs.12086`). | F0–F4 fading ladder. |
| Explaining why confusing facts make sense improves memory (Pressley et al., *JEP*, 1988, DOI `10.1037/0022-0663.80.3.384`). | `why-fails`, `eipe`, causal explanations. |
| Interleaving can reduce practice performance while improving later retention and discrimination (Taylor & Rohrer, *Applied Cognitive Psychology*, 2010, DOI `10.1002/acp.1598`). | Mixed checks and cross-chapter transfer. |

## 13. Authoring worksheet

Copy this into `gen_notes.md` for each block before writing YAML.

```text
Block:
Type:
Evidence IDs:
Source of truth:
Objective:
Prior knowledge required:
Notional machine:
Misconception targeted:
Worked example:
Boundary or failure mode:
Second signal:
Check ladder:
  1.
  2.
  3.
  4.
  5.
Interleaved target:
Lab/tinker change:
Teach-back prompt:
Open questions:
```

## 14. Final quality gate

Before a chapter is declared complete:

- [ ] Every block has one falsifiable objective and one notional machine.
- [ ] Every block maps to evidence IDs in `gen_notes.md`.
- [ ] Every factual claim is traceable to source, transcript, or observed artifact.
- [ ] Every `model` block has prediction/diagnosis and a state or structure artifact.
- [ ] Every `syntax` block has order/fillblank plus a failure mode.
- [ ] Every `algorithm` block has trace/order/micro-lab.
- [ ] Every `design` block has `eipe` or `choose-better`.
- [ ] Explanation follows the five-job recipe and is not a fact list.
- [ ] Worked example is evidence-backed and faded into prediction/diagnosis.
- [ ] Checks are 5–10 per block and cover multiple cognitive actions.
- [ ] Distractors encode real misconceptions.
- [ ] At least two checks interleave prior chapters.
- [ ] Tool blocks teach mental model, output, filters, failure modes, composition, diagnosis, and teach-back.
- [ ] Kernel blocks distinguish canonical source from runtime harness evidence.
- [ ] No invented outputs, flags, line numbers, register values, or behavior.
- [ ] `python main.py validate --book linux-kernel --chapter <id> --strict` passes.

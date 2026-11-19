# Study Method

The method is designed for retention and transfer: read a small slice, trace it,
change it, and explain it. The artifact is a dossier, not a highlight reel.

## Weekly loop

| Day | Work |
|-----|------|
| 1 | Read the chapter's source map; write questions; predict the trace |
| 2 | Trace the path with gdb/ftrace/printk; capture raw evidence |
| 3 | Run the knob experiment; record counters and output |
| 4 | Run the modify/rebuild experiment; keep the diff |
| 5 | Explain-back: draw the diagram and write the journal entry |
| 6 | Spaced review: re-answer the chapter checks without notes |
| 7 | Rest or read ahead without taking notes |

A kernel chapter is 1–2 weeks. Short tool chapters are 2–4 days. Networking
modules are 1–2 weeks. Overlap between tracks is deliberate; phase gates prevent
skipping. Do not start the next chapter with an open question from the previous
one unless you write it down as a deliberate carry-over.

## Chapter protocol

1. **Map** — list the files and functions in the reading slice. Do not read
   them all yet.
2. **Question** — write 3–5 questions the slice should answer.
3. **Trace** — follow one path end to end. Mark every handoff.
4. **Experiment** — run one knob, one break-it or instrument, and one ablation.
5. **Diff** — compare the version you studied with a later version for one
   function or structure.
6. **Explain** — produce a diagram and a short written explanation.
7. **Test** — answer the termlearn checks and quiz without looking.
8. **Review** — add cards for the structures and invariants you missed.

## Tool mastery protocol

Tool chapters (T0a–T8 in `TOOLING.md`) use a different loop. C reading and
basic socket API vocabulary are assumed. T0a/T0b are tool on-ramps: use a tiny
userspace program and toy repository before the kernel tree.

1. **Question** — name a kernel question the tool can answer. In T0a/T0b,
   start with a question about a tiny userspace program.
2. **Mental model** — write what the tool observes and what it cannot observe.
3. **Guided tour** — run it on a known workload and read every column.
4. **Filter** — start noisy, add one filter at a time, explain each removal.
5. **Break-it** — cause a controlled failure and find it.
6. **Compose** — confirm the result with a second tool.
7. **Diagnose** — solve a symptom prompt without being told the command.
8. **Teach-back** — write the mini-manual: three invocations, one pitfall, one
   confusing column, one limitation.

A tool chapter is done when you can choose the tool from a symptom, read its
output without a cheat sheet, and explain what it cannot tell you. Core labs are
required; stretch labs are optional depth. There is no fixed lab cap.

## The dossier

Each chapter gets `notes/chNN-<slug>.md`:

```markdown
# Chapter N — Title

## Version and source
Kernel version:
Commit/tag:
Files read:

## Questions
1.
2.
3.

## Path
Userspace entry:
Kernel entry:
Key handoffs:
Return path:

## Data structures
| Structure | Owner | Lifetime | Key fields |
|-----------|-------|----------|------------|

## Experiment
Question:
Prediction:
Change:
Commands:
Observation:
Surprise:
Explanation:

## Diff vs later kernel
Function/structure:
What changed:
Why it matters:

## Diagram
(ASCII or mermaid)

## Open questions
-

## Review cards
-
```

## Tools by job

| Job | Tool |
|-----|------|
| Find a symbol | `git grep`, cscope, clangd |
| Find when a line changed | `git log -S`, `git blame` |
| Boot or debug a kernel | QEMU, gdb, kgdb, crash, drgn |
| Follow a call path | gdb breakpoints, ftrace `function_graph` |
| See syscalls | strace |
| See packet flow | `ip -s`, `ss -ti`, `nstat`, tcpdump |
| See scheduling | `perf sched`, `trace-cmd`, `/proc/sched_debug` |
| See memory | `/proc/meminfo`, `/proc/vmstat`, `slabtop`, `vmstat` |
| See kernel events | ftrace, perf, bpftrace |
| Inspect a binary | `objdump`, `readelf`, `nm`, `pahole` |
| Check a patch | `checkpatch.pl`, sparse, smatch, coccinelle |
| Test and fuzz | kselftests, KUnit, syzkaller, virtme-ng |
| Send upstream | `b4`, `get_maintainer.pl`, lore.kernel.org |
| Compare versions | `git diff vX vY -- path/`, `git log -p` |

## Reading rules

- Read the data structure before the function that uses it.
- Read the caller before the callee when the callee is large.
- Read the error path; it often explains the design.
- Read the comments that state invariants, not the comments that restate code.
- If a function is too large, find the branch that matters for your path and
  ignore the rest.
- Do not read modern code while studying an old kernel. Note the difference and
  move on.

## Retention

- Explain without notes: open a blank file and draw the path from memory.
- Compare with the source; mark every missing handoff.
- Make one card per invariant or ownership rule, not per line of code.
- Re-run one old experiment at the start of each new phase.
- Keep a "surprises" list; it is the best source of review material.

## When stuck

1. Write the smallest question you cannot answer.
2. Find the function that must answer it.
3. Add a trace or breakpoint; do not guess.
4. If the trace is too noisy, narrow the path or use a filter.
5. If the source is too large, switch to an older version where the same
   mechanism is smaller.
6. If the experiment is unsafe, move it into a namespace or QEMU.
7. If you are still stuck after 30 minutes, write the blocker in the journal and
   continue; return with fresh eyes.

## Phase review

At the end of each phase:

- Re-run one experiment from the first chapter.
- Draw the phase's main path from memory.
- List the three most important structures and their lifetimes.
- Compare one function across the phase's first and last version.
- Complete the phase exit gate in `PROGRESS.md`.
- Choose the next phase's first question.

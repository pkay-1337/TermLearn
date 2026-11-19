# Linux Kernel Curriculum

Status: **planning only**. This directory contains the plan, method, source map,
environment notes, templates, and helper scripts. It intentionally does **not**
contain chapter packs or book files yet.

## What this is

A tinkering-first path through Linux history:

1. **Tooling** (T0a–T8, split into focused chapters): tool on-ramp,
   git/build/inspection, QEMU/gdb, post-mortem debugging, strace, ftrace,
   perf, bpftrace, network tools, testing/fuzzing, and upstream workflow.
2. **Early kernels** (0.01, 0.11, 0.12): small enough to read and run.
3. **Middle kernels** (0.95 → 2.6.12): watch the modern shape emerge.
4. **Modern kernels** (6.18 LTS / 7.3): learn the real networking stack.
5. **One deep dive** chosen after the networking track.

The goal is not to read every line. It is to build a correct mental model by
reading bounded slices, changing one thing, observing the effect, and explaining
the result. Tools are taught as full chapters: a lab must teach the tool's
mental model, output, filters, failure modes, and composition, not just run it.
There is no lab cap; a chapter gets as many labs and lab families as it needs.
Baseline: C reading and basic socket API vocabulary are assumed; kernel tooling
is not. T0a starts with a tiny userspace program and tool habits, not the kernel
tree. Use [BLOCK_AUTHORING.md](BLOCK_AUTHORING.md) when drafting packs; it turns
evidence into teaching blocks instead of fact lists.

## Start here

| File | Purpose |
|------|---------|
| `PLAN.md` | Full curriculum, phases, tooling, networking modules, milestones, evidence-first authoring gate |
| `TOOLING.md` | T0a–T8 tool chapters, learner baseline, lab families, modern kernel developer stack |
| `TINKERING.md` | The experiment method and lab families |
| `SOURCES.md` | Version history, git topology, fetch commands |
| `ENVIRONMENT.md` | Host tools, kernel modules, QEMU/Docker, safety |
| `STUDY_METHOD.md` | Weekly loop, chapter protocol, note template |
| `PROOF_OF_WORK.md` | Online blog, LinkedIn proof-of-work blueprints, and public portfolio strategy |
| [BLOCK_AUTHORING.md](BLOCK_AUTHORING.md) | Evidence-backed method for writing teaching blocks, checks, and labs |
| `AGENTS.md` | Directives for AI authors generating self-contained, source-grounded study packs |
| `PROGRESS.md` | Milestones and checklists |
| `notes/README.md` | How to keep chapter notes |
| `templates/` | Experiment/tool lab YAML, instruction, tinker, and check templates |
| `scripts/` | Fetch, graft, build, boot, and network-namespace helpers |

## Termlearn integration

Chapter packs will be created later under `books/linux-kernel/` and
`packs/linux-kernel/`, and only after the evidence-first authoring gate in
`PLAN.md`: actual tool runs for tooling chapters and pinned source plus observed
runtime behavior for kernel chapters. Each experiment lab can declare:

```yaml
commands:
  run: "sh probe.sh"
  test: "sh check.sh"
  tinker: "sh"
```

In the lab screen press `x` (or click **Tinker**). Termlearn opens a separate
terminal when available (alacritty, tmux, or `TERMLEARN_TINKER_TERMINAL`);
otherwise it suspends and runs the command in the current terminal.

## Non-goals

- No attempt to read all of `net/` or `drivers/net/` line by line.
- No VXLAN-only curriculum. VXLAN is one module in a broad tunnel/overlay lab.
- No tool demo labs. A lab that only runs a command does not count.
- No chapter packs until the plan is reviewed and the evidence-first pilot is approved.
- No assumed prior knowledge of the terminal, git, kernel builds, gdb, or tracing.

# Tinkering Method

The kernel is learned by changing it and watching what happens, not by reading
it passively. Every chapter must produce at least one experiment with a
prediction, a change, an observation, and an explanation.

## The loop

1. **Question** — write one sentence, e.g. "What happens to a packet after
   `dev_queue_xmit` on loopback?"
2. **Predict** — write the expected trace, counter, or output before running.
3. **Change one thing** — a sysctl, a qdisc, a route, a few lines of code, or a
   build option.
4. **Run** — capture the command and the output.
5. **Observe** — use at least two signals when possible (e.g. `ip -s link` and
   ftrace; `ss -ti` and `nstat`).
6. **Explain** — reconcile prediction and observation in the journal.
7. **Generalize** — state what this means for a different interface, protocol,
   or kernel version.

If the result matches the prediction, the experiment still needs an explanation.
If it does not, the surprise is the lesson.

## Lab families

### 1. Knob

Change a value and observe a counter or behavior.

Examples:

- `net.core.somaxconn`, `net.ipv4.tcp_congestion_control`, `net.core.rmem_max`.
- `tc qdisc add dev lo root netem delay 50ms`.
- `ip link set dev veth0 mtu 1400`.
- Kernel config: disable a feature and rebuild.

### 2. Break-it

Introduce a small, reversible fault.

Examples:

- Add a one-line bug in a copy of a function and watch the trace change.
- Delete a route and observe the error path.
- Set a queue limit to 1 and watch drops.
- Corrupt a checksum in a test harness.

### 3. Instrument

Add visibility, then remove it.

Examples:

- Add `printk` or a tracepoint to a kernel function.
- Use ftrace `function_graph` on `netif_receive_skb`.
- Attach a bpftrace probe to `tcp_retransmit_skb`.
- Use `perf record -g` on a packet-heavy workload.

### 4. Ablation

Remove a mechanism and compare.

Examples:

- Compare CUBIC and BBR.
- Compare `noqueue` and `fq_codel` on the same link.
- Compare a bridge with and without VLAN filtering.
- Compare a kernel with and without a feature compiled in.

### 5. Rebuild

Change source and rebuild.

Examples:

- Rebuild 0.11 with a changed time slice.
- Rebuild 2.6.12 with a different scheduler option.
- Rebuild a modern kernel with a small patch to a tracepoint.

### 6. Predict

Write the expected result before running.

Examples:

- Predict the encapsulation overhead of VXLAN vs GRE.
- Predict which counter increments when a UDP receive buffer is full.
- Predict the route selected for a given destination and policy rule.

## Tool-teaching lab families

Tools are not demos. Use these families (see `TOOLING.md` for the full map) to
teach the tool itself:

### 7. Guided tour

Run the tool on a known workload and read the output line by line. Name each
column, the default filter, and what the tool cannot see.

### 8. Filter

Start noisy. Add one filter at a time (`strace -e`, ftrace `set_ftrace_filter`,
perf `-e`, bpftrace predicates). Explain what each filter removed.

### 9. Compose

Use two tools on the same question: `strace` + `ss`, `perf` + `ftrace`,
`bpftrace` + `tcpdump`, `gdb` + QEMU. Reconcile the two views.

### 10. Diagnose

Give a symptom, not a command. The learner chooses the tool, forms a hypothesis,
and gathers evidence.

### 11. Challenge

An open-ended, reproducible question. The learner produces a trace, a
measurement, or a patch and explains it.

### 12. Teach-back

Write a mini-manual: three invocations to remember, one pitfall, one confusing
output column, and one question the tool cannot answer.

### 13. Algorithm synthesis (Analyze and Implement)

Extract a kernel algorithm or data structure directly from source, strip out
architectural boilerplate or driver glue, and implement a clean, standalone,
test-driven equivalent in userspace C.

Examples:

- Inspect `include/linux/list.h` and implement `struct list_head` + `container_of()`.
- Inspect `fs/buffer.c` and implement a fixed-size hash table + circular LRU buffer cache.
- Inspect `drivers/char/` / `kfifo` and implement a power-of-2 lockless circular ring buffer.
- Inspect `mm/page_alloc.c` and implement an order-0 to order-10 binary buddy allocator.
- Inspect `net/ipv4/fib_trie.c` and implement a bitwise CIDR longest-prefix-match (LPM) trie.
- Inspect `net/sched/sch_tbf.c` and implement a token-bucket rate limiter.

## Rules

1. **One variable per run.** If you change two things, you learn nothing.
2. **Record the exact command.** A result without a command is a rumor.
3. **Use a namespace or QEMU for network changes.** Never experiment on the
   host's default namespace unless the change is trivial and reversible.
4. **Snapshot before editing kernel source.** Use git or a copied tree.
5. **Remove instrumentation after the experiment.** Keep the diff, not the
   debug print.
6. **Compare at least two signals.** One counter can lie; two can be reconciled.
7. **Write the explanation the same day.** Memory decays faster than logs.
8. **No lab cap.** Use as many labs and lab families as the chapter needs.
9. **Core or stretch.** Mark every lab. Core is required; stretch is optional
   depth. There is no fixed cap.
10. **State run conditions.** Record privilege needs, tool versions, and how
    nondeterministic output is normalized.
11. **No tool demo without a question.** Every tool lab starts from a question.
12. **No tool lab without a second signal.** Confirm the tool's view with
    another tool or counter.
13. **Teach the failure.** Show what a missing symbol, filter, or permission
    looks like.
14. **Teach the composition.** The real skill is combining tools, not memorizing
    flags.
15. **Evidence before authoring.** Observe every command, output, source range,
    and failure before writing the lab. No evidence means no lab. See the
    evidence-first authoring section in `PLAN.md`.

## Experiment lab anatomy

A termlearn experiment lab has three commands:

```yaml
commands:
  run: "sh probe.sh"
  test: "sh check.sh"
  tinker: "sh"
  timeout_s: 10
```

- `run` is captured. It should print a small, deterministic observation.
- `test` is captured and diffed. It should check the observation or a file.
- `tinker` is interactive. It should open the environment where the learner can
  explore: a shell, gdb, QEMU, `ip netns exec`, or a tracing tool.

`tinker` runs with the lab workspace as `cwd` and inherits stdin/stdout/stderr.
It has no timeout by default. In the TUI press `x`; in CLI `lab` mode type `x`.

Tool labs add more than the three commands: guided commands, what to notice,
one filter change, a second signal, a diagnose prompt, and a teach-back. A tool
chapter may have many such labs; do not cap them. See
`templates/tool-lab.yaml` for a multi-lab example.

Separate-terminal order:

1. `TERMLEARN_TINKER_TERMINAL` if set (e.g. `alacritty -e`).
2. `tmux new-window` if inside tmux.
3. `alacritty -e` if alacritty and a display are available.
4. Otherwise suspend the TUI and run in the current terminal.

## Experiment instruction template

Use `templates/experiment-instruction.md`. Every instruction must contain:

- **What this tool answers** in one plain-language sentence (tool labs).
- **Mental model** — what the tool observes and what it cannot observe.
- **Guided commands** with a known workload and expected output.
- **What to notice** — the columns, events, or counters that matter.
- **Predict** before running.
- **Setup** with exact commands.
- **Change** with one variable (filter, fault, workload, or kernel change).
- **Observe** with exact commands and the counters/output to capture.
- **Second signal** — another tool that confirms or contradicts the first.
- **Diagnose** — a symptom prompt, not a command prompt.
- **Explain** questions that force a mechanism-level answer.
- **Teach-back** — the three invocations, one pitfall, one confusing column.
- **Evidence IDs** — every output claim and source reference cites a captured
  artifact; unverified claims are omitted.
- **Cleanup** so the next experiment starts clean.

## Journal template

Copy this into `notes/` for each experiment:

```markdown
## YYYY-MM-DD — Chapter / Experiment

Question:
Prediction:
Environment (kernel version, config, namespace, tools):
Commands:
Observation:
Surprise:
Explanation:
Next question:
Artifacts (trace, diff, graph, log path):
```

## Safety

- Use `unshare -n` or `ip netns` for interface, route, qdisc, and netfilter
  experiments.
- Use QEMU for old kernels; do not try to boot 0.11 on the host.
- Do not run `iptables -F`, `nft flush ruleset`, or route changes in the host
  namespace.
- Do not run untrusted code with `sudo`.
- Keep a terminal open with `ip netns list` and a known-good shell.
- Prefer `ip -n <ns>` and `ip netns exec <ns>` over `sudo` where possible.

## Determinism and privileges

Before authoring a lab, write down:

- exact privilege or capability needed, plus the namespace/QEMU fallback;
- tool versions that change the output format;
- which fields are normalized before `test` runs: timestamps, durations, CPU
  IDs, addresses, counters that depend on host load;
- the filtering command that makes the observation small enough to read;
- the cleanup command.

Captured `run`/`test` output must be deterministic or use tolerant matching.
Never require an exact full trace from ftrace, perf, tcpdump, or bpftrace.

## What "done" looks like

A chapter is done when you can:

1. Draw the path from userspace to the kernel function and back.
2. Name the key data structure and the function that owns it.
3. Reproduce the experiment from your notes.
4. Explain one surprise without looking at the answer.
5. State one thing that changed between the version you studied and modern code.

A tool chapter is done when you can:

1. Choose the tool from a symptom, not from a memorized command.
2. Read its output without a cheat sheet and name the important columns.
3. Filter noise and explain what each filter removed.
4. Confirm its view with a second tool or counter.
5. State one thing the tool cannot observe.
6. Teach the tool back in a five-minute mini-manual.

# Tooling Track

Tools are part of the curriculum, not a side note. Each tool gets its own
chapter (T0a–T8), its own labs, and its own exit criteria. A lab must teach the
tool: what problem it solves, how to read its output, how to filter it, how it
fails, and how to combine it with another tool.

The labs are not capped. A tool chapter should include as many labs and lab
families as it needs. More small labs are better than one large demo.

## Tool chapters

| Chapter | Tool or workflow | Primary use |
|---------|------------------|-------------|
| T0a | First contact: terminal, files, processes, C compiler, make, git basics | Run, compile, inspect, and commit |
| T0b | Source navigation: grep/rg, cscope/clangd, git history | Find definitions, callers, and commits |
| T0c | Build and patch: Kconfig/Kbuild, modules, checkpatch, get_maintainer | Build, modify, and prepare a patch |
| T0d | Binary and type inspection: nm, readelf, objdump, size, pahole | Inspect symbols, sections, layout, and types |
| T0e | Static analysis: sparse, smatch, coccinelle | Find and fix static issues |
| T0f | T0 capstone: integrate navigation, history, patch, build, inspection | Go from symptom to patch |
| T1a | QEMU, gdb, architecture vocabulary | Boot, break, inspect userspace and kernel |
| T1b | kgdb, crash, drgn, lockdep | Post-mortem, live introspection, and lock validation |
| T2 | strace | See syscalls and userspace/kernel boundaries |
| T3 | ftrace, trace-cmd | Trace kernel functions and events |
| T4 | perf | Measure CPU, scheduling, memory, and events |
| T5 | bpftrace, bpftool, BTF, eBPF, XDP | Programmable kernel tracing and data-path acceleration |
| T6a | ip, ss, ip netns, ip -s | Address, link, route, socket, namespace state |
| T6b | tc, nft, conntrack, nstat | Queueing, filtering, connection and counter state |
| T6c | tcpdump, ethtool, iperf3, socat, traceroute | Capture, link details, traffic generation, path probes |
| T7a | kselftests, KUnit, virtme-ng, lockdep/KCSAN | Run and write repeatable tests with concurrency verification |
| T7b | syzkaller, stress-ng, fio, reproducer minimization | Fuzz, load, and reproduce |
| T8 | b4, lore, get_maintainer, checkpatch, syzbot | Upstream kernel workflow |

These are chapters, not appendices. They can be studied in order or pulled in
when a phase needs them.

## Learner baseline and on-ramp

Assume C reading and basic socket API vocabulary:

- C structs, pointers, macros, and simple compiler errors are already readable.
  T0a uses a 10-line C program as a workload, not as a syntax lesson.
- `socket()`, file descriptors, `bind()`, `connect()`, `send()`, and `recv()`
  are being learned; their kernel implementation is not assumed.
- Architecture vocabulary — registers, stack, calling convention, privilege
  levels, paging — is introduced in T1a and A1.
- The terminal, git, kernel builds, gdb, ftrace, perf, and eBPF are new. T0a
  starts there. Every new tool term is defined before use.

T0a/T0b are the tool on-ramp. Do not begin with kernel source, `sparse`, or
`coccinelle`. Build confidence with a tiny program, a tiny repository, and
readable output first. T0c–T0f then move the same habits onto the kernel tree.

## Evidence requirements for tool chapters

A tool chapter is written only after the creator has actually used the tool in
the pinned environment. `TOOLING.md` describes what should be taught; it is not
permission to describe behavior from memory. The source of truth is the observed
run.

For every intended lab, capture before drafting:

- exact command and working directory;
- workload files and their contents;
- tool version and relevant environment (`uname -a`, distro, config where
  applicable);
- privilege mode and fallback, if any;
- raw stdout/stderr and exit code;
- a second signal that confirms or contradicts the first observation;
- the failure case or noisy output before filtering;
- the exact cleanup command.

Store these in `evidence/<chapter>/` with stable IDs such as `E-T2-04`. The lab
instruction may state only what those artifacts show. Mappings are mandatory:

| Instruction section | Evidence required |
|---------------------|-------------------|
| What this tool answers | observed command and output that answer the question |
| Mental model | observed output plus version-pinned docs or source from the same environment |
| Guided commands | executed commands with recorded exit codes |
| What to notice | specific columns, events, errors, or counters visible in the transcript |
| Change one thing | before/after transcripts for the changed filter, fault, or workload |
| Second signal | transcript from the independent tool used to reconcile the view |
| Explain-back | mechanism claims traceable to source/docs and the observed transcript |
| Cleanup | executed cleanup with confirmation that state was removed |

Rules:

- Do not invent flags, columns, error strings, counters, or plausible output.
- Do not copy output from another machine, kernel version, or tool version.
- If two tool versions format output differently, pin the version or provide a
  separate evidence item for each format.
- Execute the `tinker` command before writing it into a lab.
- If a privileged tool cannot be observed safely, use QEMU or a namespace, or
  mark it unverified and skip the lab. Never author from assumed permission.
- "What the tool cannot observe" must be checked against its documented scope
  and demonstrated by a negative observation where practical.
- An evidence gap becomes an open question in the plan, not prose in the pack.

The same rules apply to tool labs embedded in kernel, networking, or deep-dive
chapters. The creator uses the tool to answer a real question before writing the
lab.

## Tool lab families

Every tool chapter should mix several of these. Use as many as the tool needs.


### 1. Guided tour

Run the tool on a known workload. Read the output line by line. Answer:
what is this column, what is the default filter, what is missing?

### 2. Predict

Show the command and workload. Ask for the expected output, counter, or event
before running. Compare.

### 3. Filter

Start with noisy output. Add one filter at a time (`-e`, `-p`, `-f`, ftrace
`set_ftrace_filter`, perf `-e`, bpftrace predicates). Explain what each filter
removed.

### 4. Break-it

Cause a controlled failure (drop a packet, fill a queue, add a delay, trigger a
retransmit, fault a syscall). Find it with the tool. Prove it with a second
signal.

### 5. Compose

Use two tools together: `strace` + `ss`, `perf` + `ftrace`, `bpftrace` +
`tcpdump`, `gdb` + QEMU, `ip -s` + `nstat`. Reconcile the two views.

### 6. Diagnose

Give a symptom, not a command: "the connection stalls", "the syscall is slow",
"the packet is dropped", "the kernel panics at boot". The learner chooses the
tool, forms a hypothesis, and gathers evidence.

### 7. Challenge

An open-ended question with a reproducible environment. The learner must
produce a trace, a measurement, or a patch, and explain it.

### 8. Teach-back

Write a mini-manual: the three invocations you will remember, one pitfall, one
output column that confused you, and one question the tool cannot answer.

## Tool lab contract

Every tool lab instruction must contain:

1. **What this tool answers** in one plain-language sentence.
2. **Mental model** — what the tool observes and what it cannot observe.
3. **Guided commands** — exact commands with a known workload.
4. **What to notice** — the columns, events, or counters that matter.
5. **One change** — a filter, a fault, a workload change, or a kernel change.
6. **A second signal** — another tool that confirms or contradicts the first.
7. **Explain-back** — questions that force a mechanism-level answer.
8. **Cleanup** — exact commands to remove namespaces, processes, or modules.
9. **Beginner check** — define every new term, show expected output, name the
   most common error, and use a userspace warm-up before kernel code.
10. **No tool-name dumping** — introduce the tool only when the lab has a
    question it answers.
11. **Priority label** — mark the lab **core** or **stretch**. Core is required;
    stretch is optional depth.
12. **Run conditions** — state privilege needs, tool versions that affect
    output, and how nondeterministic fields are normalized.
13. **Evidence reference** — every claim, expected output, and "what to notice"
    item cites an evidence ID captured before drafting.
14. **Fail closed** — no evidence, no lab. Unverified privileged behavior is
    skipped, not guessed.

Example lab skeleton:

```yaml
labs:
  - id: lab-strace-filter
    title: "Find the syscall behind a slow open"
    instruction_md: |
      ## What this tool answers
      `strace` shows the syscalls a process makes and where it blocks.

      ## Mental model
      It observes the userspace/kernel boundary, not kernel internals.

      ## Guided commands
      ...
      ## What to notice
      ...
      ## Change one thing
      ...
      ## Second signal
      ...
      ## Explain
      ...
      ## Cleanup
      ...
    files:
      - path: "workload.sh"
        content: |
          ...
    commands:
      run: "sh workload.sh"
      test: "sh check.sh"
      tinker: "strace -f -tt -T -o trace.log ./workload"
      timeout_s: 10
    test_cases:
      - name: "trace contains openat"
        stdin: ""
        expect: "openat"
        expect_exit: 0
    hints:
      - "..."
```

## T0a — First contact

**Why:** you cannot debug a kernel if you are still fighting the terminal.

**Learn:**

- Files, directories, permissions, `PATH`, stdin/stdout/stderr, exit status.
- Processes: `ps`, `kill`, foreground/background, `Ctrl-C`.
- Compile C: `gcc -Wall -Wextra -g`, warnings versus errors.
- `make` basics; build a tiny multi-file project.
- Git basics: `init`, `status`, `add`, `commit`, `log`, `diff`.
- Read an error message: find the file and line, fix one thing, rerun.

**Labs:** run a 10-line program; break it and read the compiler error; compile
with `-g`; build with `make`; initialize a toy repository; make a commit;
change a file and inspect the diff.

**Exit:** compile, run, modify, and commit a tiny program without help.

## T0b — Source navigation

**Why:** the kernel is too big to read linearly; you need to jump to the right
line.

**Learn:**

- `grep`/`rg` first: `-n`, `-C`, `-w`, file globs.
- `cscope`: find symbol, callers, and callees.
- `clangd`: `compile_commands.json`, go-to-definition, find references.
- `git log`, `git log -S`, `git log -L`, `git blame`, `git worktree`,
  `git bisect`.
- Source tree map: `arch/`, `kernel/`, `mm/`, `fs/`, `net/`, `drivers/`.

**Labs:** find a symbol with `rg`; open its callers in cscope; go to definition
in clangd; find the commit that added a string with `git log -S`; blame a line;
bisect a toy regression.

**Exit:** given a symbol, find its definition, callers, and introducing commit.

## T0c — Build and patch

**Why:** building and patching are daily kernel work, not special events.

**Learn:**

- Kconfig: `make menuconfig`, `.config`, `CONFIG_*`, `make olddefconfig`.
- Kbuild: `make -j`, `make M=...`, `make modules_install`.
- Module metadata: `modinfo`, `insmod`, `rmmod`, `dmesg`.
- `scripts/checkpatch.pl`, `scripts/get_maintainer.pl`.
- Patch format: `git diff`, `git format-patch`, `git apply`.

**Labs:** build and load a hello-world module; change one config option; add a
checkpatch warning and fix it; find the maintainers for a file; produce a patch
and apply it to a clean tree.

**Exit:** build a module, fix a checkpatch warning, and produce a readable
patch.

## T0d — Binary and type inspection

**Why:** the source is not the whole story; the compiled artifact shows what
the machine actually sees.

**Learn:**

- `nm`: symbols, undefined symbols, local versus global.
- `readelf`: headers, sections, symbols, relocations.
- `objdump`: disassembly, source interleave, relocations.
- `size`: text/data/bss.
- `pahole`: struct layout, padding, holes, BTF.
- Debug info versus BTF; why `-g` and `CONFIG_DEBUG_INFO_BTF` matter.

**Labs:** list symbols with `nm`; find a section with `readelf`; disassemble one
function with `objdump`; compare `size` before and after a change; inspect a
struct with `pahole`; correlate a symbol with its source line.

**Exit:** given a symbol or struct, find it in both the source and the binary.

## T0e — Static analysis

**Why:** some bugs are visible before the program runs.

**Learn:**

- `sparse`: type mismatches, address-space annotations, endianness.
- `smatch`: flow-sensitive warnings.
- `coccinelle`: semantic patches for repeated transformations.
- When each tool is the right choice, and when none of them can help.

**Labs:** introduce a sparse warning and fix it; run `smatch` on a small
module; write a `coccinelle` rule for a repeated pattern; compare what each
tool found and missed.

**Exit:** run all three on one module and explain which finding came from which
tool.

## T0f — T0 capstone

**Why:** real work is a workflow, not a pile of commands.

**Learn:**

- Symptom → symbol → callers → introducing commit → patch → build → check.
- Keep a reproducible command log and a clean diff.

**Labs:** given a symptom, find the symbol; find its callers and the commit
that introduced it; make a small patch; run checkpatch and sparse; build and
boot the result; write the artifact trail.

**Exit:** a reproducible artifact trail from symptom to verified patch.

`b4`, `lore.kernel.org`, and `syzbot` belong in T8, not T0a–T0f.

## T1a — QEMU and gdb

**Why:** you cannot debug a kernel on the host without risking the host, and
you should learn gdb before pointing it at a kernel.

**Learn:**

- gdb on a userspace program: `break`, `run`, `list`, `print`, `next`, `step`,
  `finish`, `bt`, `frame`, `watch`, conditional breakpoints.
- Architecture vocabulary introduced by debugging: registers, stack frame,
  calling convention, instruction pointer, breakpoint trap.
- QEMU boot: `-kernel`, `-append`, `-initrd`, `-drive`, `-nographic`.
- QEMU debug: `-s -S`, `target remote :1234`, `hbreak start_kernel`, snapshots.
- Symbols: `-g`, `vmlinux`, source line mapping, and why optimized code lies.

**Labs:** debug the 10-line T0a program; stop at a named function and read its
arguments; watch a variable change; QEMU-boot a kernel; break at `start_kernel`
and step once; explain the stack/register state at the breakpoint.

**Exit:** debug a userspace program and a QEMU kernel boot, then explain what
the debugger is actually observing.

## T1b — Post-mortem and live introspection

**Why:** after a panic the process is gone; you need artifacts and structure
walkers, not just breakpoints.

**Learn:**

- kgdb over serial for stop-and-inspect kernel debugging.
- `crash` on a vmcore: `bt`, `log`, `ps`, `files`, `struct`, `kmem`.
- `drgn` for live and post-mortem structure walking with typed C expressions.
- Lockdep (`CONFIG_PROVE_LOCKING`): decoding lockdep splats in `dmesg`, circular lock dependency detection ($A \to B$ vs $B \to A$), and atomic-context sleep violations (`BUG: scheduling while atomic`).
- `lockstat` (`/proc/lock_stat`): measuring spinlock and mutex contention time, hold time, and acquisition bottlenecks.
- Debuginfo, `vmlinux`, BTF, and matching kernel builds.
- Reproducing a panic in QEMU and capturing a repeatable artifact.

**Labs:** trigger a controlled panic in QEMU; capture the log and vmcore;
inspect the backtrace in `crash`; walk one kernel structure with `drgn`;
inject a circular lock dependency in a dummy module, capture the lockdep splat,
and map the lock inversion graph; compare a live view with the post-mortem artifact.

**Exit:** given a crash artifact, explain the faulty state without editing the
source.

## T2 — strace

**Why:** most "kernel" questions start at the syscall boundary.

**Learn:**

- Basic: `strace ./prog`, `-f`, `-p`, `-o`, `-s`, `-v`, `-tt`, `-T`.
- Filters: `-e trace=`, `-e signal=`, `-e read=`, `-e write=`, `-P path`.
- Decoding: `-y`, `-yy`, `-k` (if built with stack unwinding).
- Summary: `-c`, `-C`, `-w`.
- Injection: `-e inject=` for controlled failures (use with care).
- Attach to a running process and to a process in a container/namespace.

**Labs:** trace `ip link add`; find the `openat` behind a config read; compare
`-c` summaries; inject `ENOENT` and observe the error path; trace a process
inside a netns.

**Exit:** given a slow or failing userspace operation, produce a filtered trace
that names the syscall and the blocking point.

## T3 — ftrace and trace-cmd

**Why:** ftrace is built into the kernel and is often the fastest way to see
what the kernel is doing.

**Learn:**

- `/sys/kernel/tracing`: `available_tracers`, `current_tracer`, `trace`,
  `trace_pipe`, `set_ftrace_filter`, `set_graph_function`.
- `function`, `function_graph`, `nop`, `wakeup`, `irqsoff`.
- Events: `available_events`, `events/*/enable`, `events/*/filter`.
- Instances: `instances/`, per-instance buffers.
- Snapshots: `snapshot`, `trace_marker`, `trace_clock`.
- `trace-cmd record`, `trace-cmd report`, `trace-cmd stream`.
- Boot-time tracing via `trace_event=` and `trace_buf_size=`.

**Labs:** trace `netif_receive_skb` on loopback; filter to one PID; measure
function duration; compare `function` and `function_graph`; use an instance to
separate two experiments; capture a boot trace.

**Exit:** answer "which function ran, in what order, for how long, and on which
CPU?" with a trace you can rerun.

## T4 — perf

**Why:** perf is the standard for CPU, scheduling, memory, and hardware-event
measurement.

**Learn:**

- `perf stat`, `perf record`, `perf report`, `perf annotate`.
- `perf sched`, `perf lock`, `perf mem`, `perf trace`, `perf probe`.
- `perf c2c` for cache-line contention.
- Symbols, call graphs, `--call-graph dwarf`, flame graphs.
- `perf list`, event modifiers, `-e`, `-p`, `-t`, `-C`.

**Labs:** measure context switches; record a packet workload; find the hottest
function; compare CUBIC and BBR; measure a qdisc backlog; inspect a lock
contention trace.

**Exit:** produce a measurement with a clear baseline, a change, and an
explanation of the delta.

## T5 — bpftrace, bpftool, BTF, eBPF

**Why:** modern kernel developers use eBPF for low-overhead, programmable
tracing and for data-path work.

**Learn:**

- bpftrace probes: `kprobe`, `kretprobe`, `tracepoint`, `uprobe`, `USDT`,
  `profile`, `interval`, `software`, `hardware`.
- Actions: `printf`, `hist`, `lhist`, `count`, `sum`, `avg`, `min`, `max`,
  `delete`, `clear`.
- Maps, filters, `BEGIN`/`END`, `join`, `str`, `ksym`, `kstack`, `ustack`.
- `bpftool prog`, `bpftool map`, `bpftool btf`, `bpftool feature`.
- BTF, CO-RE, `vmlinux.h`, and why BTF matters.
- XDP and tc eBPF: write, compile with clang/LLVM, and load a minimal 15-line native XDP program (`XDP_DROP` / `XDP_PASS`) that drops or redirects packets directly in the driver RX ring before `sk_buff` allocation.

**Labs:** count syscalls by process; histogram TCP retransmit latency; trace
`tcp_retransmit_skb` with a filter; count packets per interface; inspect BTF for
a struct; load a minimal 15-line XDP drop program on a veth pair, benchmark packet throughput
against Netfilter/iptables, and verify zero `sk_buff` allocations.

**Exit:** write a bpftrace one-liner and a small bpftool-loaded program, then
explain the overhead and the safety limits.

## T6a — Address, link, route, and namespace state

**Why:** first answer "what objects exist and what state are they in?"

**Learn:**

- `ip -d link`, `ip addr`, `ip route`, `ip neigh`, `ip netns`, `ip -s`.
- `ss -lntup`, `ss -ti`, `ss -m`, `ss -e`.
- Link types: loopback, dummy, veth, bridge, VLAN.
- Namespaces: `ip netns add/exec/del`, `ip -n <ns>`, veth peer movement.

**Labs:** inspect loopback; create a dummy interface; move a veth into a netns;
compare `ip -d link` with `ss -lntup`; explain one `ip link add` operation.

**Exit:** given a namespace and interface, describe state and the object model
without changing the host namespace.

## T6b — Queueing, firewalling, and counters

**Why:** packets disappear because queues, filters, or conntrack dropped them.

**Learn:**

- `tc qdisc`, `tc class`, `tc filter`, `tc -s`, `netem`, `fq_codel`.
- `nft list ruleset`, `nft monitor trace`, `conntrack -L`.
- `nstat`, `netstat -s` (legacy), `/proc/net/snmp`.
- Counter semantics: where a counter increments, and what it cannot prove.

**Labs:** add delay with netem; fill a tiny queue and observe drops; add an nft
drop rule in a namespace; watch conntrack entries; reconcile `tc -s` with
`nstat`.

**Exit:** given a drop symptom, identify the queue/filter/counter responsible
and prove it with a second signal.

## T6c — Capture, link details, and traffic generation

**Why:** sometimes you must see the bytes or generate controlled load.

**Learn:**

- `tcpdump -i`, `-n`, `-e`, `-w`, `-r`, BPF filters.
- `ethtool`, `ethtool -S`, `ethtool -k`, `ethtool -i`.
- `iperf3`, `socat`, `mtr`/`traceroute`.
- Capture hygiene: select one interface, filter tightly, and stop cleanly.

**Labs:** capture loopback; read an Ethernet/IP/UDP header; capture VXLAN or
GENEVE encapsulation; generate TCP load with `iperf3`; compare `tcpdump` with
`ip -s`.

**Exit:** capture a specific packet, explain each header field you need, and
reconcile the capture with a kernel counter.

## T7a — Repeatable tests

**Why:** a kernel change without a test is a guess.

**Learn:**

- `tools/testing/selftests/`, especially `selftests/net`.
- KUnit for in-kernel unit tests; assertions and expected failures.
- `virtme-ng` for fast kernel testing without a full VM image.
- Avoiding flakes: deterministic setup, cleanup, and version pins.
- Concurrency verification: running test workloads under `CONFIG_PROVE_LOCKING` (Lockdep) and `CONFIG_KCSAN` (Kernel Concurrency Sanitizer) to catch data races and lock inversions.

**Labs:** run an existing selftest; read its pass/fail contract; write a small
KUnit test; boot a test kernel with virtme-ng; make a failing test pass after a
one-line change.

**Exit:** add a runnable test that would catch a known regression.

## T7b — Fuzzing, load, and reproduction

**Why:** some bugs only appear under volume, race, or strange inputs.

**Learn:**

- syzkaller concepts and syzbot reproducer format.
- `stress-ng`, `fio`, and `iperf3` for controlled load.
- Minimize, isolate, script, and record the environment.
- Reproduce in QEMU before trying the host.

**Labs:** run a syzkaller-style reproducer in QEMU; stress a qdisc; load a
filesystem or socket path with `fio`/`iperf3`; minimize a reproducer; record
kernel config and tool versions.

**Exit:** produce a minimal, repeatable reproducer and state exactly which
conditions are necessary.

## T8 — Upstream workflow

**Why:** "real kernel developer" includes the review and patch process.

**Learn:**

- `git format-patch`, `git send-email`, `b4 prep`, `b4 send`.
- `scripts/get_maintainer.pl`, `scripts/checkpatch.pl`.
- lore.kernel.org, patchwork, Reviewed-by/Acked-by tags.
- `syzbot` reports and `Fixes:` tags.
- Stable backports and `Cc: stable`.

**Labs:** format a patch; run checkpatch; find the maintainers; simulate a
review reply; write a Fixes tag for a synthetic bug.

**Exit:** a patch series that passes checkpatch, targets the right maintainers,
and has a clear commit message.

## Tooling by phase

| Phase | Tool chapters |
|-------|---------------|
| Before A | T0a, T0b |
| A | T0c–T0f, T1a, T2 |
| B | T2, T3 |
| C | T1b (lockdep/lockstat), T3, T4, T6a, T6b |
| D | T1b, T4, T5, T6b, T6c, T7a, T7b, T8 |
| Networking | T6a throughout; T6b for qdisc/firewall; T6c for capture/counters; T3/T4/T5 for deep evidence |

## Modern kernel developer stack

Beyond the tool chapters, the plan assumes familiarity with:

- `git` and `b4` for history and patches.
- `checkpatch`, `sparse`, `smatch`, `coccinelle` for static checks.
- `KASAN`, `KCSAN`, `lockdep`, `lockstat`, `kmemleak`, `debugobjects` for dynamic checks.
- `XDP`, `tc-bpf`, `bpftrace`, `bpftool`, `drgn`, `crash` for diagnosis and data-path acceleration.
- `ftrace`, `perf` for function, event, and hardware performance profiling.
- `QEMU`, `virtme-ng`, `kselftests`, `KUnit`, `syzkaller` for testing.
- `ip`, `ss`, `tc`, `nft`, `tcpdump`, `ethtool`, `conntrack`, `nstat` for
  networking.
- `pahole`, `objdump`, `readelf`, `nm`, `gdb` for binaries and structures.

## Rules

1. **No tool demo without a question.** Every lab starts from a question.
2. **No tool lab without a second signal.** One counter can lie.
3. **No lab cap.** Use as many labs as the chapter needs.
4. **Teach the output.** Naming the command is not teaching the tool.
5. **Teach the failure.** Show what a missing symbol, filter, or permission
   looks like.
6. **Teach the composition.** The real skill is combining tools.
7. **Record the version.** Tool behavior changes between releases.
8. **Clean up.** Namespaces, processes, modules, and QEMU guests.
9. **Tool-on-ramp only.** C reading and socket API vocabulary are assumed.
   Define tool terms; show expected output and common errors; use tiny
   userspace examples first.
10. **No tool-name dumping.** Introduce a tool only when the learner has a
    question it answers.
11. **Core or stretch.** Mark every lab. Core is required; stretch is optional
    depth. No hard lab cap.
12. **State run conditions.** Record privilege needs, tool versions, and how
    nondeterministic output is normalized.

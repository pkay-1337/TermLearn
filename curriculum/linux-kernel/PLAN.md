# Linux Kernel Curriculum Plan

Status: **plan only**. No chapter packs or book files have been created.
Review this plan first; chapters will be generated phase by phase afterwards.

## 1. Goal

Build a working, source-grounded mental model of Linux from the earliest public
kernel to a modern LTS, then go deep on one networking subsystem.

The finish line is not "I read the kernel." It is:

- I can trace a packet or syscall through the source and explain each handoff.
- I can change a kernel knob or a few lines, rebuild, and predict what happens.
- I can use `ip`, `ss`, `tc`, `nft`, `strace`, `gdb`, ftrace, perf, and bpftrace
  to answer questions without guessing.
- I can read an unfamiliar function in `net/` and place it in the stack.

### Learner baseline

This plan assumes:

- You can read C: structs, pointers, function pointers, macros, and simple
  build errors are familiar. There is no C syntax on-ramp.
- You are currently learning socket APIs: descriptors, `socket()`, `bind()`,
  `connect()`, `send()`, and `recv()` are known at the API level.
- The kernel side of sockets is new: syscalls, `net_device`, `sk_buff`,
  rtnetlink, and packet paths are not assumed.
- The terminal, git, kernel builds, gdb, ftrace, perf, and eBPF are new. T0a
  starts there.
- Architecture basics — x86 registers, stack, calling convention, privilege
  levels, and paging — are introduced just-in-time in T1a and A1, not assumed.

## 2. Principles

1. **Spiral, not exhaustive.** Visit the same subsystems at 0.11, 1.2, 2.6,
   and modern. Each pass adds one layer of realism.
2. **Bounded slices.** A chapter studies one path, one data structure, or one
   mechanism. It does not study "networking" in one sitting.
3. **Tinkering-first.** Every chapter has at least one experiment where the
   learner changes one thing, runs it, and explains the result.
4. **Source at the version being studied.** Do not read modern code while
   studying 0.11. Use the tag or tarball for that phase.
5. **Evidence over vibes.** Each chapter ends with a trace, a diff, a graph, or
   a measurement, not just highlighted text.
6. **Networking is a vertical track, not the whole curriculum.** Boot, memory,
   scheduling, VFS, and drivers still matter.
7. **VXLAN is one module, not the spine.** The tunnel module covers VXLAN,
   GENEVE, GRE, IPIP, bridges, VLANs, veth, and namespaces together.
8. **Tools are taught, not just invoked.** `strace`, `gdb`, QEMU, ftrace,
   perf, bpftrace, and the rest get their own chapters and labs. A lab that
   only runs a tool has failed; it must teach the mental model, the output,
   the filters, the failure modes, and the composition.
9. **No lab cap.** A chapter gets as many labs and lab families as it needs.
   More small, focused labs beat one large demo.
10. **No chapter packs yet.** The plan, templates, and scripts come first.
11. **Tool on-ramp, not C on-ramp.** C reading and basic socket vocabulary are
    given. Terminal, git, builds, gdb, tracing, and eBPF are not. Define tool
    terms before use, show expected output, and start with tiny userspace
    examples before kernel examples. Do not dump tool names; introduce a tool
    when the learner has a question it answers.
12. **Evidence before prose.** A chapter is authored only after its claims have
    been observed. For tooling, the creator uses the actual tools on a known
    workload and records the output. For kernel chapters, the creator reads the
    pinned source and uses build/boot/debug/trace tools when the chapter claims
    runtime behavior. The plan, docs, and templates are contracts, not evidence.
13. **Algorithm synthesis (Analyze and implement).** To deeply understand an internal
    mechanism and prepare for systems-level DSA, read and analyze the kernel's real data
    structure or algorithm in source, strip away extraneous locking or hardware boilerplate,
    and implement a clean, standalone, test-driven equivalent in C.

## 3. Curriculum architecture

```
Tooling  T0a–T0f, T1a/T1b, T2–T8   tool on-ramp, debug, trace, observe, test
Phase A  0.01 / 0.11 / 0.12        read the whole thing, run it
Phase B  0.95 → 1.2                 watch structure appear
Phase C  2.0 → 2.6.12 (C1 → C9)      learn the modern skeleton
Phase D  6.18 LTS / 7.3             work in the real stack
Track N  networking M0 → M7         broad, hands-on, source-backed
Deep dive one subsystem             chosen after M7
```

Each chapter follows the same contract:

- a short source reading map with exact files and functions;
- one primary path or mechanism to trace;
- one **knob** experiment (change a value or config);
- one **modify** experiment (change a few lines and rebuild);
- one **observe** experiment (ftrace, gdb, `ss`, `ip -s`, perf, bpftrace);
- one **explain-back** artifact (diagram, trace, or journal entry);
- as many termlearn labs as the chapter needs, with `run`, `test`, and
  (where useful) `tinker`. There is no upper bound.
- for tool chapters: labs that teach the tool, not labs that merely run it.
  See `TOOLING.md` for the T0a–T8 chapters and the eight tool lab families.
- labs are labelled **core** or **stretch**. Core labs are required; stretch
  labs are optional depth. There is still no fixed lab cap.
- every factual claim, source reference, and expected output is backed by an
  evidence bundle captured before drafting. See "Evidence-first authoring".
- a tool chapter's evidence comes from actually running the tool; a kernel
  chapter's evidence comes from the pinned source tree plus observed runtime
  behavior where the chapter makes a runtime claim.

### Phase exit gate

Do not move to the next phase until you have:

- one path diagram drawn from memory;
- one rebuild or patch plus the exact diff;
- one two-tool evidence note with commands and raw output;
- one explain-back or teach-back artifact;
- updated `PROGRESS.md` with open questions listed.

A finished phase is evidenced, not just read.

### Block plans

Blocks follow the termlearn vocabulary: `model` for an invisible mechanism,
`syntax` for a surface form or output shape, `algorithm` for a procedure, and
`design` for a judgment under constraints. There is no fixed block cap. The
rule is **one new falsifiable skill per block**. If a block needs two mental
models, two diagrams, or unrelated evidence artifacts, split it.

Use [BLOCK_AUTHORING.md](BLOCK_AUTHORING.md) for the local teaching-design
method: evidence mapping, notional machines, worked-example fading, check
ladders, interleaving, and the final quality gate. The SRS remains the normative
pack schema.

Each block must cite evidence IDs from the chapter bundle. Checks follow the
content-type mapping: `model` gets `predict`/`why-fails` plus a diagram or viz;
`syntax` gets `order`/`fillblank` plus `why-fails`; `algorithm` gets
`trace`/`order`/micro-lab; `design` gets `eipe`/`choose-better`. Every chapter
gets at least two interleaved checks from earlier chapters.

#### T0a — First contact

1. `model` Shell command loop — predict cwd, argv, command lookup.
2. `model` stdin/stdout/stderr and exit status.
3. `syntax` `gcc` command shape, `-Wall`, `-Wextra`, `-g`.
4. `algorithm` Read compiler diagnostic → file/line → one fix → rerun.
5. `model` `make` dependency graph.
6. `algorithm` Change one file and predict rebuild target.
7. `model` Git working tree/index/commit model.
8. `syntax` `status`, `add`, `commit`, `log`, `diff` output.
9. `algorithm` Make a clean commit and inspect its diff.
10. `design` Choose next command from failure text.

#### T0b — Source navigation

1. `model` Source as graph: distinguish declarations (`include/`), definitions (`.c`), call sites, and macro expansions (`SYSCALL_DEFINE`, `DEFINE_PER_CPU`).
2. `syntax` `rg` patterns: word boundaries (`-w`), path filtering (`-g '*.c'`), case sensitivity, and file-type flags.
3. `syntax` `rg` context and output: `-C 3`, line numbers (`-n`), search traps in macro-wrapped identifiers (e.g., `SYSCALL_DEFINE[0-6]\(read\b`).
4. `algorithm` Definition search: jump from symbol call site to canonical definition without getting trapped in header prototypes.
5. `algorithm` Caller enumeration: locate true callers across subsystems while filtering false positives from shared struct member names.
6. `model` Git history DAG: commit objects, trees, parent links, merge topologies, and why code history survives renames.
7. `syntax` Git forensic inspection: `git log -S <symbol>` (pickaxe), `git log -G <regex>`, `git log -L :<func>:<file>` (function range), and `git blame -w -M`.
8. `algorithm` Historical archaeology: trace a symbol from current implementation back to the originating commit, commit message, and rationale.
9. `design` Navigation trade-offs: choose raw text search (`rg`) vs semantic indexing (`cscope`/`clangd`) vs history (`git log -S`).
10. `design` Epistemic limits: articulate what static navigation cannot prove (indirect function pointers in `file_operations`, runtime callbacks, dynamic dispatch).

#### T0c — Build and patch

1. `model` Kconfig configuration pipeline: `Kconfig` files → `.config` → `include/generated/autoconf.h` macro definitions (`#define CONFIG_... 1`).
2. `syntax` Kconfig grammar: `bool`, `tristate` (`y`, `m`, `n`), `depends on`, `select`, `default`, and menu hierarchies.
3. `algorithm` Configuration toggling: modify `.config` (via `scripts/config` or `menuconfig`), run `make olddefconfig`, and verify generated header macro updates.
4. `model` Kbuild object flow: recursive Make execution, `obj-y` (built into `vmlinux`) vs `obj-m` (loadable `.ko` modules) vs composite objects.
5. `syntax` Module Makefile structure: canonical `obj-m += mymod.o` and two-phase invocation (`make -C /lib/modules/$(uname -r)/build M=$(PWD) modules`).
6. `algorithm` Out-of-tree module build: compile a standalone C source file into a `.ko`, inspecting intermediate `.mod.c` and `.o` artifacts.
7. `algorithm` Module lifecycle and safety: load with `insmod`/`modprobe`, verify active state via `lsmod` and `dmesg`, and safely unload with `rmmod`.
8. `model` Unified patch model: patch as an atomic, reviewable context diff against an exact upstream tree commit.
9. `syntax` Gatekeeper tooling output: parse `checkpatch.pl --strict` warnings (formatting, 80/100 columns, CamelCase, whitespace) and `get_maintainer.pl` recipient lists.
10. `algorithm` Patch authoring and hygiene: generate an upstream-ready patch with `git format-patch -1`, imperative subject line, 72-column wrapped body, and `Signed-off-by:`.
11. `design` Patch principles: ensure every patch is minimal, atomic, bisectable (no broken intermediate states), and attributable.

#### T0d — Binary and type inspection

1. `model` Translation lifecycle: relocatable object (`.o`) vs statically linked executable/kernel (`vmlinux`) vs runtime memory-mapped image.
2. `model` ELF section anatomy: `.text` (executable instructions), `.data` (initialized data), `.rodata` (constants), `.bss` (zero-alloc), and kernel-specific `.init.text` (discarded after boot via `free_initmem`).
3. `syntax` `nm` symbol type codes: decode `T`/`t` (text), `D`/`d` (data), `B`/`b` (bss), `R`/`r` (read-only), `U` (undefined external), and exported symbol tables (`__ksymtab`).
4. `algorithm` Symbol address resolution: locate static vs global symbol addresses and sizes in object files using `nm -v` and `nm -S`.
5. `syntax` `readelf` section inspection: parse ELF header architecture flags (`readelf -h`) and section allocation/permission flags (`readelf -S`).
6. `syntax` `objdump` disassembly: inspect compiled machine code with `objdump -d -S` (source-interleaved) and syntax flavors (`-M intel` vs `-M att`).
7. `algorithm` Instruction path mapping: trace a C function from source statement to disassembled assembly, stack frame setup, and register allocation.
8. `model` Struct layout and hardware alignment: natural alignment rules (4-byte int, 8-byte pointer), compiler padding bytes, and 64-byte CPU cacheline boundaries.
9. `syntax` `pahole` and BTF output: interpret struct memory footprints, holes, member offsets, and cacheline boundaries (`/* size: 128, cachelines: 2, members: 7 */`).
10. `algorithm` Struct layout optimization: identify padding holes in a struct with `pahole` and reorder members to minimize size and prevent cacheline splits.
11. `design` Tool matrix selection: choose `nm`, `readelf`, `objdump`, `size`, or `pahole` based on whether the question concerns symbols, sections, instructions, or type layouts.

#### T0e — Static analysis

1. `model` Static analysis fundamentals: AST traversal, data-flow analysis, soundness, completeness, false positives vs false negatives.
2. `syntax` Sparse diagnostic shapes: parse `warning: incorrect type in assignment`, address space mismatch (`__user` vs `__kernel`), and endianness violations.
3. `algorithm` User-pointer defense: reproduce a direct `__user` pointer dereference in toy C, run Sparse, and repair with `copy_from_user` / `get_user`.
4. `model` Kernel type annotation vocabulary: role of `__user`, `__kernel`, `__iomem`, `__rcu`, `__percpu`, and endian types (`__le32`, `__be32`).
5. `algorithm` Kernel Sparse execution: run `make C=1` on a target compilation unit and filter diagnostic findings.
6. `model` Semantic patching concept: program transformation via Abstract Syntax Tree (AST) pattern matching rather than text substitution.
7. `syntax` Coccinelle SmPL grammar: declare meta-variables, matching patterns, and transformation diff blocks (`-` and `+`) in `.cocci` rules.
8. `algorithm` Applying semantic patches: run `spatch --sp-file` against a source file to perform an automated API migration or defect fix.
9. `algorithm` Smatch flow analysis: execute Smatch to detect cross-function logic defects (uninitialized variables, missing unlock paths, buffer bounds).
10. `design` Diagnostic triage: distinguish genuine defects from benign analyzer quirks, and apply documented annotations to silence false positives.

#### T0f — Tooling capstone

1. `model` Empirical debugging loop: Symptom observation → Hypothesis formulation → Evidence collection → Minimal patch → Dual verification.
2. `algorithm` Clean reproduction harness: set up an isolated test branch and script a deterministic failing test case.
3. `algorithm` Root-cause localization: combine `rg`, `git log -S`, and `git blame` to isolate the commit and function introducing the defect.
4. `algorithm` Minimal patch authoring: apply targeted source modifications and build incrementally.
5. `algorithm` Dual-signal verification: confirm the fix using one dynamic test run and one binary inspection tool (`pahole` or `nm`).
6. `model` Patch series hygiene: order commits logically with zero intermediate build breaks to preserve `git bisect` integrity.
7. `design` Two-tool evidence dossier: author a structured report reconciling independent command outputs, exit codes, and diffs.
8. `design` Tooling limitation review: produce a comprehensive matrix cataloging the blindspots of every tool in the T0 suite.

#### T1a — QEMU and gdb

1. `model` Debugger execution model: `ptrace` control in userspace vs GDB Remote Serial Protocol (RSP) stub in QEMU.
2. `syntax` GDB fundamental controls: `break`, `run`, `list`, `print /x`, `display`, and register inspection (`info registers`).
3. `syntax` Stack and execution flow: `step` (into), `next` (over), `finish`, `backtrace`, `frame`, and `info frame`.
4. `algorithm` Userspace debug cycle: attach GDB to a small C application, step through execution, inspect local variables, and evaluate stack frames.
5. `model` x86_64 register and ABI conventions: argument registers (`rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9`), scratch registers, stack pointer (`rsp`), base pointer (`rbp`), instruction pointer (`rip`).
6. `syntax` Data watchpoints: `watch` (write), `rwatch` (read), `awatch` (access), and conditional breakpoints (`break file:line if cond`).
7. `algorithm` Memory corruption detection: catch unexpected variable modifications using hardware watchpoints.
8. `model` QEMU virtualization boundary: host vs guest execution context, virtual CPU states, guest physical memory mapping, and the `-gdb tcp::1234` RSP socket.
9. `syntax` QEMU boot flags: `-kernel`, `-append "console=ttyS0"`, `-initrd`, `-drive`, `-nographic`, `-s` (gdb stub port 1234), and `-S` (freeze vCPU at reset).
10. `algorithm` Remote kernel attachment: launch QEMU halted with `-s -S`, attach GDB with `target remote :1234`, and load symbol tables with `file vmlinux`.
11. `model` Optimization realities: compiler inlining, register variables marked `<optimized out>`, code motion, and why early boot requires hardware breakpoints (`hbreak`).
12. `algorithm` Kernel entry breakpoint: set hardware breakpoint at `start_kernel`, step through early bootstrap, and inspect control registers (`cr0`, `cr3`, `cr4`).
13. `design` Observation strategy: choose between software breakpoints, hardware breakpoints, watchpoints, or printk/ftrace based on execution frequency and timing constraints.

#### T2 — strace

1. `model` System call interface boundary: user mode (Ring 3) to kernel mode (Ring 0) transition, register argument conventions, and return value/errno mapping.
2. `syntax` `strace` invocation grammar: launch program directly (`strace <cmd>`), attach to PID (`-p PID`), and log output to file (`-o trace.log`).
3. `syntax` Trace line field anatomy: system call identifier, decoded argument structures, return values, and symbolic error names (`ENOENT`, `EAGAIN`, `EFAULT`).
4. `algorithm` Stream filtering: isolate specific system calls (`-e trace=openat,read,write`), syscall classes (`-e trace=network`, `-e trace=file`), or error results (`-z`, `-Z`).
5. `algorithm` Return code and error triage: identify failing syscall sequences and correlate errno values with userspace error messages.
6. `model` File descriptor lifecycle: process-local descriptor table (`task_struct->files`), standard streams (`0`, `1`, `2`), sockets, pipes, and resource leakage.
7. `syntax` Forensic telemetry flags: `-f` (follow forks/threads), `-tt` (microsecond timestamps), `-T` (syscall duration), `-c` (aggregate profiling table), and `-yy` (decode socket endpoints, pipe inodes, and file paths).
8. `algorithm` Latency root-cause analysis: use `strace -c` and `-T` to determine whether application latency originates in userspace CPU loops or blocking kernel syscalls (e.g. `futex`, `epoll_wait`).
9. `algorithm` Missing-dependency diagnosis: trace a failing application to locate missing shared libraries (`.so`) or unreadable configuration files via `openat`.
10. `design` Epistemic boundaries: articulate what `strace` cannot observe (page faults, context switches, interrupt handling, and kernel-space thread execution).

#### A1 — Boot and first C

1. `model` Source tree anatomy & the 100-file operating system: navigate `sources/early-history.git` at pinned tag `0.11` (commit `b65b60f4`) vs `sources/Linux-0.11-fork` (runnable harness); deconstruct the 8 core directories (`boot/`, `init/`, `kernel/`, `mm/`, `fs/`, `include/`, `lib/`, `tools/`) and the 100-file / 13,839-line complete Unix mental model.
2. `model` The A1 mission & the 4-stage bootstrap pipeline: map the custody chain from cold power-on reset to C entry (`bootsect.s` sector 1 → `setup.s` sectors 2–5 → `head.s` sector 6+ → `init/main.c`); articulate why assembly must build the world C assumes.
3. `model` 80386 hardware reset state: real-mode execution, 1MB addressing ceiling, CS:IP reset vector at `0xFFFF0`, and segmented memory translation (`Base * 16 + Offset`).
4. `model` 0.11 boot media layout: raw floppy disk sectors partitioned into `bootsect.s` (sector 1, 512 bytes) → `setup.s` (sectors 2–5, 2048 bytes) → `system` (kernel image starting at sector 6).
5. `algorithm` `bootsect.s` handoff: BIOS loads bootsect to `0x7C00`; bootsect relocates itself to `0x90000`, loads `setup.s` to `0x90200`, and streams `system` to `0x10000` via BIOS INT 13h.
6. `algorithm` `setup.s` protected-mode transition: query BIOS memory size into `0x90002`, move `system` down to `0x00000`, enable A20 gate, load temporary GDT/IDT with `lgdt`/`lidt`, set PE bit in `CR0`, and far-jump `jmpi 0,8` to 32-bit segment 8.
7. `algorithm` `head.s` to `main()` entry: load 32-bit data segments (`ds=0x10`), populate initial 256 IDT interrupt gates with dummy handlers, build page directory at `0x0000` and first 4 page tables at `0x1000`–`0x4000` (identity-mapping 16MB), load `CR3`, set `CR0.PG`, and `ret` into `init/main.c:main()`.
8. `syntax` Early C idioms and inline assembly: port I/O macros (`inb`, `outb`), control register access (`mov to/from cr0`), and interrupt flags (`cli`, `sti`).
9. `model` 0.11 physical memory layout: memory zones: `0–640KB` (kernel, page tables, buffer cache), `640KB–1MB` (video RAM, BIOS ROM), `1MB–...` (buffer cache continuation, optional ramdisk, main memory for user pages).
10. `algorithm` QEMU boot execution: boot 0.11 disk image in QEMU with serial console output and capture full boot banner.
11. `algorithm` GDB breakpoint at `main()`: attach GDB to QEMU stub (`target remote :1234`), set hardware breakpoint at `main`, and confirm arrival.
12. `algorithm` Machine state verification: inspect general registers, segment registers (`cs`, `ds`), control registers (`cr0`, `cr3`), and stack pointer at `main()` entry.
13. `design` Pristine vs runnable fork: analyze why 1991 assembly syntax and GCC 1.40 assumptions fail under modern toolchains and justify runnable fork modifications.
14. `design` Annotated boot-trace artifact: construct a chronological map detailing register states, memory moves, and privilege switches from BIOS to `main()`.

#### A2 — Processes and scheduling

1. `model` Process control block: `struct task_struct` fields (state, counter, priority, pid, uid, signals), and the `task_union` 4KB layout (struct at bottom, kernel stack growing downward).
2. `model` Process state lifecycle: `task[NR_TASKS]` array (fixed 64 slots), state transitions (`TASK_RUNNING`, `TASK_INTERRUPTIBLE`, `TASK_UNINTERRUPTIBLE`, `TASK_ZOMBIE`, `TASK_STOPPED`).
3. `syntax` Task management macros: `FIRST_TASK`, `LAST_TASK`, `current` pointer, and `switch_to(n)` TSS selector invocation.
4. `algorithm` `sys_fork` dispatch: trap via `int 0x80` to `sys_fork`, allocate unused PID, search `task[]` for an open slot, and call `copy_process`.
5. `algorithm` `copy_process` mechanics: allocate physical page for child `task_union`, clone parent `task_struct`, duplicate page tables (marking pages read-only for Copy-On-Write), configure TSS registers, set child return value `eax = 0`, and register child in `task[]`.
6. `model` Timer interrupt trigger: Programmable Interval Timer (PIT) IRQ0 firing at 100Hz (10ms tick), triggering assembly entry `timer_interrupt`.
7. `algorithm` `do_timer` accounting: decrement `current->counter`. When counter reaches 0, set `need_resched` flag and invoke `schedule()`.
8. `algorithm` `schedule()` algorithm: execute $O(N)$ scan over `task[]` for runnable task with maximum `counter`. When all runnable counters are 0, recompute counters globally via `counter = (counter >> 1) + priority`.
9. `model` Hardware TSS context switch: execute `ljmp *(tss_selector)` causing 386 CPU to hardware-save outgoing registers into outgoing TSS and restore incoming registers from incoming TSS.
10. `algorithm` Time-slice modification experiment: alter default priority and counter values in `sched.h`, rebuild, and measure CPU time distribution.
11. `algorithm` Process competition observation: execute two CPU-bound loops and trace scheduling handoffs using GDB watchpoints on `current`.
12. `design` Scheduler timeline artifact: construct an exact timeline diagram mapping PIT ticks, counter decrements, and task context switches.
13. `design` 0.11 scheduler scalability limits: explain why global $O(N)$ scanning, fixed-size task arrays, periodic recalculation, and hardware TSS cannot scale to multiprocessor (SMP) or modern server workloads.

#### A3 — Memory

1. `model` 0.11 physical memory architecture: low memory mapping, buffer cache boundary, and high memory page frames managed by `mem_map[]`.
2. `model` Two-level paging architecture: `CR3` register pointing to Page Directory, Page Directory Entry (PDE), Page Table Entry (PTE), control bits (Present, Read/Write, User/Supervisor), and 4KB page frames.
3. `syntax` Page manipulation macros: `PAGE_DIR`, `PAGE_SIZE (4096)`, `PAGE_ALIGN`, and bit-shift operators decomposing 32-bit linear addresses into directory/table/offset indices.
4. `algorithm` Address translation walk: manually trace a virtual address through PDE lookup, PTE lookup, and offset addition to derive physical RAM addresses.
5. `algorithm` Page-fault entry (`mm/page.s`): hardware traps on `INT 14`, pushes error code (protection violation vs not-present), reads faulting linear address from `CR2`, and routes to C handlers.
6. `algorithm` Demand paging (`do_no_page`): allocate a clean physical page with `get_free_page()`, resolve executable disk block from inode, read 4KB block into page frame via buffer cache, and map PTE.
7. `algorithm` Copy-on-Write (`do_wp_page`): detect write fault on shared page (`mem_map[page] > 1`), allocate fresh physical page, copy 4KB contents from source page, decrement source page count, and remap PTE as writable.
8. `model` Physical page frame tracker: `mem_map[]` reference counting byte array tracking page usage above 1MB (`0` = free, `1` = exclusive, `>1` = shared).
9. `algorithm` Page-fault instrumentation: attach GDB to `do_no_page()` and `do_wp_page()`, log faulting `CR2` addresses, and verify `mem_map[]` state changes.
10. `algorithm` Memory exhaustion observation: write a workload exhausting physical RAM, observing allocation failure and process termination.
11. `design` Probe interference in low-level handlers: explain why adding printk or allocating memory inside page fault handlers triggers recursive faults and system crashes.
12. `design` Page-fault trace artifact: draw an exact causal sequence diagram showing instruction write fault → `INT 14` → `CR2` capture → `do_wp_page` → PTE update.

#### A4 — Filesystem and syscalls

1. `model` File abstraction hierarchy: process file descriptor table (`current->filp[fd]`) → global file table (`file_table[64]`) → in-core inode table (`inode_table[32]`) → buffer cache hash table (`hash_table[307]`).
2. `syntax` 0.11 filesystem data structures: `struct m_inode` (mode, uid, size, block zones `i_zone[9]`) and `struct buffer_head` (`b_data`, `b_blocknr`, `b_dev`, `b_uptodate`, `b_dirt`, `b_count`).
3. `model` Buffer cache engine: dual-linked structure combining hash buckets for $O(1)$ block lookup (`hash(dev, block)`) with a circular LRU doubly linked list for buffer reclamation.
4. `algorithm` Block read path (`bread`): query hash table for `(dev, block)`. On hit, increment `b_count`; on miss, extract oldest clean buffer from LRU, dispatch block I/O request to disk driver, sleep on `b_wait`, and return populated buffer.
5. `algorithm` Path resolution (`namei.c`): parse path strings (e.g., `/usr/bin/sh`) by traversing directory inodes, scanning directory entries (`struct dir_entry`), matching filename strings, and fetching target inode numbers.
6. `algorithm` `sys_open` lifecycle: allocate unused fd in `current->filp[]`, resolve inode via `open_namei()`, allocate and link `struct file`, set file offset to 0, and return fd index.
7. `algorithm` `sys_read` and `sys_write` data flow: convert logical file byte offset `f_pos` to physical disk block number via inode `i_zone` table, fetch block via `bread()`, and transfer bytes to userspace using `put_fs_byte()`.
8. `model` Syscall trap architecture: `int 0x80` software interrupt vector mapped to assembly dispatcher `_system_call` in `system_call.s`.
9. `syntax` Syscall dispatch table: register stack frame saving, validation check (`eax < NR_syscalls`), indirect jump via `sys_call_table[%eax]`, signal checking, and `iret` return.
10. `algorithm` Custom syscall implementation: declare a new syscall in `include/unistd.h`, register its handler in `include/linux/sys.h`, implement in `kernel/`, rebuild, and invoke from userspace C.
11. `design` Syscall end-to-end trace artifact: construct a complete sequence diagram tracing userspace libc wrapper → `int 0x80` → `sys_read` → `bread` → disk driver → return to Ring 3.
12. `design` Pre-VFS architecture evaluation: explain how hardcoding the Minix disk format directly into filesystem routines prevented multi-filesystem support and motivated the Virtual Filesystem Switch (VFS) in Phase B.

#### A5 — Build, run, and trace

1. `model` 0.11 build toolchain requirements: Minix environment, GCC 1.40, GNU `as86`/`ld86` for 16-bit real-mode code, and `a.out` binary layout.
2. `syntax` 0.11 Makefiles: recursive directory targets (`boot`, `fs`, `kernel`, `mm`), compiler/assembler flags, and explicit binary dependency chains.
3. `model` Disk image generation: `tools/build.c` utility stitching `bootsect` (512B) + `setup` (2048B) + `system` (raw kernel executable) into bootable floppy `Image`, and patching root device bytes at offset 508.
4. `algorithm` Clean rebuild execution: execute clean compilation using `scripts/build-0.11.sh` and verify generated `Image` size and checksum.
5. `algorithm` Assembly and toolchain diagnostic repair: identify and repair gas assembly dialect mismatches and linker script alignment issues under modern toolchains.
6. `model` QEMU PC hardware emulation: configure virtual machine parameters: `-m 16M`, `-boot a`, `-fda Image`, hard drive `-hda hdc-0.11.img`, and serial console redirection.
7. `algorithm` Kernel boot verification: boot the rebuilt `Image` in QEMU, observe sector load dots, and confirm shell prompt accessibility.
8. `algorithm` GDB multi-stage attachment: connect GDB to QEMU stub (`target remote :1234`), load symbols from `tools/system`, and break at `0x7C00` (bootsector), `0x90200` (setup), and `main()`.
9. `algorithm` Build and boot transcript capture: record reproducible terminal transcripts documenting compilation, image generation, QEMU boot, and initial command execution.
10. `design` Evidence manifest compilation: compile complete evidence manifest documenting command lines, tool versions, Git tree hashes, and exit codes for Phase A.
11. `design` Historical source vs runnable fork: document the technical rationale for preserving pristine historical source in `sources/early-history.git` while executing builds in `sources/Linux-0.11-fork`.

#### C9 — Concurrency, Locking & Lockdep

1. `model` Single-core 0.11 `cli`/`sti` vs Modern SMP: why global interrupt disabling cannot scale, and the multi-decade architectural battle to kill the Big Kernel Lock (BKL).
2. `model` Fundamental execution context boundary: Atomic Context (interrupt handlers, softirqs, spinlock critical sections) vs Sleeping Context (process context, kthreads, mutexes). The ironclad maintainer rule: *Never sleep in atomic context*.
3. `syntax` Mutual exclusion primitives: `spinlock_t` (`spin_lock`, `spin_unlock`, `spin_lock_irqsave`, `spin_unlock_irqrestore`), `raw_spinlock_t`, and sleeping `struct mutex` (`mutex_lock`, `mutex_unlock`).
4. `algorithm` Bottom halves and deferred work: the latency hierarchy from hardware IRQ top halves → softirq execution (`NET_RX`, `NET_TX`, `TIMER_SOFTIRQ`) → `tasklets` → process-context `workqueues` (`schedule_work`).
5. `model` Read-Copy-Update (RCU) architecture: lockless read fast paths, `rcu_read_lock()` / `rcu_read_unlock()`, atomic pointer publishing with `rcu_assign_pointer()` and `rcu_dereference()`, and deferred reclamation via grace periods (`synchronize_rcu()`, `call_rcu()`).
6. `algorithm` Lockdep proof engine (`CONFIG_PROVE_LOCKING`): lock classes, acquisition order tracking, directed acyclic graphs (DAGs) of lock transitions, and circular dependency validation ($A \to B$ vs $B \to A$).
7. `design` Lockdep splat triage: decode a `[ BUG: possible circular locking dependency detected ]` stack trace from `dmesg`, extract the conflicting lock acquisition chains, and repair the lock inversion.

## 4. Phase A — Early kernels (0.01, 0.11, 0.12)

Purpose: see the whole system at a size where one person can hold it.

| Chapter | Focus | Source slice | Experiment | Exit artifact |
|---------|-------|--------------|------------|---------------|
| A1 | Boot and first C | `boot/`, `init/`, `kernel/` entry | Boot 0.11 in QEMU; break at `main` in gdb | Annotated boot trace |
| A2 | Processes and scheduling | `kernel/sched.c`, `kernel/fork.c` | Change a time slice; observe two busy loops | Scheduler timeline |
| A3 | Memory | `mm/memory.c`, `mm/page.s` | Touch pages; watch page faults and free-list changes | Page-fault trace |
| A4 | Filesystem and syscalls | `fs/`, `include/linux/fs.h` | Add or trace a tiny syscall path | Syscall path diagram |
| A5 | Build, run, and trace | 0.11 toolchain, QEMU, gdb | Rebuild from source; attach gdb | Reproducible build notes |

0.01 is read-only: it is tiny and instructive, but it does not build or boot on
modern hardware. 0.11/0.12 are the runnable anchors.

Tool chapters: **T0a/T0b** are the tool on-ramp before Phase A. **T0c–T0f**,
**T1a**, and **T2** are full chapters, not side notes. T1a starts with userspace
gdb on a 10-line C program, then moves to a QEMU/kernel breakpoint. Architecture
vocabulary is introduced during those labs. `kgdb`, `crash`, and `drgn` are
post-mortem tools and belong to **T1b** in Phase D.

### Integrated Study Order: Phase A & Companion Tooling

To avoid studying kernel internals blindly without the diagnostic tools needed to observe them, follow this staged sequence. Never enter a kernel subsystem without the tool required to verify it:

```text
[Stage 1: On-Ramp & Emulation Setup]
  T0a (Terminal, Make, C, Git)
      │
      ▼
  T0b (ripgrep, cscope, git blame/bisect)
      │
      ▼
  T1a (QEMU & GDB: Userspace → Kernel Remote Stub)
      │
[Stage 2: Bootstrap & Binary Layout]
      ▼
  A1  (Boot and First C: bootsect.s → setup.s → head.s → main)
      │
      ▼
  T0d (Binary Inspection: nm, readelf, objdump, pahole)
      │
[Stage 3: CPU & Memory Engines]
      ▼
  A2  (Processes & Scheduling + 0.11 Scheduler Synthesis Lab)
      │
      ▼
  A3  (Paging & Page Faults + mem_map Allocator Synthesis Lab)
      │
[Stage 4: Syscall & I/O Boundary]
      ▼
  T2  (strace: Userspace Syscall Boundary & Decoding)
      │
      ▼
  A4  (Syscalls, Inodes, & Buffer Cache + LRU Cache Synthesis Lab)
      │
[Stage 5: Toolchain Synthesis]
      ▼
  A5  (Build, Run, & Trace: tools/build.c & 0.11 Disk Images)
      │
[Stage 6: Code Hygiene & Milestone P1 Capstone]
      ▼
  T0c (Kconfig, Kbuild, checkpatch, get_maintainer)
      │
      ▼
  T0e (Static Analysis: sparse, smatch, coccinelle)
      │
      ▼
  T0f (Tooling Capstone: Symptom → Commit → Patch → Dual Verify)
```

| Step | Chapter | Track | Focus & Role in Curriculum | Prerequisite / Key Lab |
|:---:|:---:|:---:|:---|:---|
| 1 | **T0a** | Tooling | First contact: terminal, C compiler (`gcc`), `make`, git basics | Workspace hygiene, compile toy C, inspect exit codes |
| 2 | **T0b** | Tooling | Tree navigation: `rg`, `cscope`/`clangd`, `git blame`/`bisect` | Navigating definitions and call graphs in Linux 0.11 source |
| 3 | **T1a** | Tooling | QEMU & GDB (userspace debug → remote kernel stub `:1234`) | **Direct prerequisite for A1** (remote GDB attachment to QEMU) |
| 4 | **A1** | Kernel | Boot & first C (`bootsect.s` → `setup.s` → `head.s` → `main()`) | Boot 0.11 in QEMU; break at `main()` in GDB; inspect CR0/CR3 |
| 5 | **T0d** | Tooling | Binary inspection: `nm`, `readelf`, `objdump`, `size`, `pahole` | Inspect 0.11 `system` binary symbols, sections, and struct alignment |
| 6 | **A2** | Kernel | Processes & scheduling (PIT IRQ0, priority decay, TSS switch) | **Algorithm Synthesis Lab:** Simulate 0.11 scheduler decay in C |
| 7 | **A3** | Kernel | Memory (two-level paging, `mem_map[]`, demand paging, COW) | **Algorithm Synthesis Lab:** Implement 4KB page frame allocator in C |
| 8 | **T2** | Tooling | `strace` (userspace syscall boundary, arguments, return codes) | **Direct prerequisite for A4** (observing syscalls from userspace) |
| 9 | **A4** | Kernel | Filesystem & syscalls (`int 0x80`, inodes, buffer cache LRU) | **Algorithm Synthesis Lab:** Implement LRU buffer cache in C |
| 10 | **A5** | Kernel | Build, run, and trace (`tools/build.c`, floppy sector stitching) | Rebuild 0.11 from source; verify Image checksums and serial boot |
| 11 | **T0c** | Tooling | Modern build & patch hygiene (Kconfig/Kbuild, `checkpatch.pl`) | Bridges 0.11 primitive Makefile to modern Phase B build systems |
| 12 | **T0e** | Tooling | Static analysis (`sparse`, `smatch`, `coccinelle`) | Address space typing (`__user`) and AST semantic transformations |
| 13 | **T0f** | Tooling | Tooling capstone (symptom → commit → patch → dual verify) | **Milestone P1 Exit Gate:** Full maintainer bug hunt and verification |


## 5. Phase B — The shape appears (0.95 → 1.2)

Purpose: watch modules, `file_operations`, `sk_buff`, and the first real
networking stack appear.

| Chapter | Focus | Source slice | Experiment |
|---------|-------|--------------|------------|
| B1 | Init, modules, architecture | `init/`, `kernel/module.c`, arch boot | Load/unload a trivial module |
| B2 | Scheduler and signals | `kernel/sched.c`, `kernel/signal.c` | Compare scheduling with A2 |
| B3 | Virtual memory | `mm/` | Map, fault, and unmap a page |
| B4 | VFS and the block layer | `fs/`, `drivers/block/` | Trace `open`/`read`/`write` |
| B5 | First networking stack | `net/`, `net/inet/` | Send a UDP datagram over loopback |
| B6 | Character and misc devices | `drivers/char/`, `drivers/char/misc.c` | Implement a miscdevice with `file_operations` and `copy_to_user` |

Keep 1.0 and 1.2 as comparison points. If a path is too different, compare the
same concept rather than the same line. Chapter B6 establishes the foundational
userspace-to-kernel driver contract: `struct file_operations` (`open`, `read`,
`write`, `ioctl`, `release`), device numbers (`dev_t`, major/minor), the modern
`miscdevice` registration wrapper (`misc_register`), and safe userspace memory
isolation boundaries via `copy_to_user()` / `copy_from_user()`.

Tool chapters: **T2** (strace) and **T3** (ftrace/trace-cmd). The labs move from
"run the command" to "filter the output, predict the event, and confirm it with
a second signal".

## 6. Phase C — The modern skeleton (2.0 → 2.6.12)

Purpose: learn the structures and layers that modern kernels still use.

| Chapter | Focus | Source slice | Experiment |
|---------|-------|--------------|------------|
| C1 | Build, config, and boot | `Makefile`, `init/`, `arch/x86/` | Build a 2.6.12 kernel and boot it |
| C2 | Scheduler and preemption | `kernel/sched.c` | Change a scheduling parameter |
| C3 | Memory management | `mm/` | Watch reclaim or slab behavior |
| C4 | VFS and page cache | `fs/`, `mm/filemap.c` | Trace a read through the page cache |
| C5 | Block and I/O | `block/`, `drivers/block/` | Compare I/O schedulers |
| C6 | Networking core | `net/core/`, `net/ipv4/` | Follow an skb from `dev_queue_xmit` to loopback |
| C7 | Netfilter and qdisc | `net/netfilter/`, `net/sched/` | Filter and shape loopback traffic |
| C8 | Unified Device Model & sysfs | `drivers/base/`, `fs/sysfs/` | Register a platform driver; bind/unbind via sysfs |
| C9 | Concurrency, Locking & Lockdep | `kernel/locking/`, `include/linux/spinlock.h`, `include/linux/mutex.h`, `include/linux/rcupdate.h` | Inject a circular lock dependency in QEMU; decode the lockdep splat |

2.6.12-rc2 is the first commit in `torvalds/linux`. The pre-2005 history is
reachable through the graft described in `SOURCES.md`.

Chapter C8 studies the birth of the Linux 2.6 Unified Device Model: `struct bus_type`,
`struct device`, and `struct device_driver`. It traces how buses discover and bind
drivers (`driver->probe` and `driver->remove`), how `kobject` hierarchies automatically
generate the `/sys/bus/`, `/sys/class/`, and `/sys/devices/` filesystem topologies,
and how driver controls are exposed using `DEVICE_ATTR_RW`.

Chapter C9 confronts the single hardest architectural reality of the 2.6 multiprocessor transition: the death of the Big Kernel Lock (BKL) and the emergence of fine-grained locking and lockless data structures. In 0.11, concurrency was trivial (`cli()` and `sti()` on a single 386 core). In 2.6 and modern Linux, concurrency defines the entire kernel:
- Context boundaries: Atomic context (hardware IRQs, `softirq`, spinlocks) vs. sleeping context (process context, mutexes). Violating this produces `BUG: scheduling while atomic`.
- Spinlocks vs Mutexes: Busy-waiting on a CPU cacheline vs descheduling the thread into a wait queue.
- Bottom halves: Why hardware IRQs must defer packet and block processing to `softirq` (`NET_RX`/`NET_TX`) and `workqueues`.
- Read-Copy-Update (RCU): The foundational mechanism underpinning modern Linux networking and routing tables, allowing unlimited concurrent readers to traverse linked structures without locks, atomic operations, or memory barriers on the read side.
- Lockdep (`CONFIG_PROVE_LOCKING`): The static/dynamic lock validation engine that proves whether any two locks can deadlock before a deadlock ever occurs in production. Upstream maintainers immediately reject any patch introducing a lockdep splat.

Tool chapters: **T3** (ftrace/trace-cmd), **T4** (perf), and **T6a/T6b**
(address/link/routing plus qdisc/firewall observability). Tool labs should use
the kernel path you are studying, not a synthetic workload.

## 7. Phase D — Modern kernels (6.18 LTS / 7.3)

Purpose: work in the real stack with modern tooling, then choose a deep dive.

| Chapter | Focus | Source slice | Experiment |
|---------|-------|--------------|------------|
| D1 | Build, boot, and config | `init/`, `kernel/`, `arch/x86/` | Build and boot a minimal kernel |
| D2 | Scheduler and namespaces | `kernel/sched/`, `kernel/nsproxy.c` | Run workloads in net/pid namespaces |
| D3 | Memory | `mm/` | Observe page allocation and reclaim |
| D4 | VFS, block, and filesystems | `fs/`, `block/` | Trace a file read end to end |
| D5 | Networking core | `net/core/`, `net/ipv4/`, `net/ipv6/` | Trace loopback RX/TX |
| D6 | PCIe drivers and virtio | `drivers/pci/`, `drivers/net/virtio_net.c` | Trace PCIe probe/remove, MSI-X, and virtio RX/TX |
| D7 | Tooling capstone | ftrace, perf, bpftrace, bpftool, drgn | Answer a live question with two independent tools |
| D8 | Security and isolation | namespaces, cgroups, netfilter | Build a small isolated network lab |

Chapter D6 bridges virtual interfaces (`veth`, `bridge`, `dummy`) with real PCIe
hardware architecture: PCI vendor/device ID tables (`struct pci_device_id`), Base
Address Registers (BARs), MMIO register mapping (`pci_iomap`), interrupt allocation
(legacy IRQ vs MSI/MSI-X multi-queue), DMA bus mastering (`pci_set_master`), and the
modern `virtio-net` virtualization standard over split/packed virtqueues.

Tool chapters: **T1b** (kgdb/crash/drgn), **T4** (perf), **T5** (bpftrace/eBPF),
**T6b/T6c** (qdisc/firewall plus capture/counters), **T7a/T7b** (testing plus
fuzzing/reproduction), and **T8** (upstream workflow). D7 is the capstone: use
two independent tools to answer one live question. It is not a repeat of the
tool tours.

Modern scale matters. In the local 7.x tree:

| Area | LOC | Files |
|------|-----|-------|
| `net/` | 1,306,469 | 1,733 |
| `drivers/net/` | 210,101 | 6,307 |
| `net/core/` | 94,237 | — |
| `net/ipv4/` | 117,128 | — |
| `net/ipv6/` | 78,917 | — |
| `net/netfilter/` | 136,253 | — |
| `net/sched/` | 64,617 | — |

`net/` plus `drivers/net/` is about 1.5 million lines. This is why the plan is
spiral and slice-based.

## 8. Tooling track (T0a → T8)

Purpose: make the tools a first-class part of the curriculum. The full chapter
map, lab families, and exit criteria live in `TOOLING.md`.

### Tool baseline

T0a assumes no prior exposure to the terminal, git, build systems, gdb, or
tracing, but C reading is already present. It starts with a 10-line userspace
program and a toy repository, not the kernel tree. Every new tool term is
defined before it is used; every lab shows what success looks like and the most
common failure. Tools are introduced only when the learner has a question they
answer. `sparse`, `smatch`, `coccinelle`, and `pahole` appear in T0d/T0e, after
there is code and a binary to inspect.

| Chapter | Focus | Primary use |
|---------|-------|-------------|
| T0a | First contact: terminal, files, processes, C compiler, make, git basics | Run, compile, inspect, commit |
| T0b | Source navigation: grep/rg, cscope/clangd, git history | Find definitions, callers, and commits |
| T0c | Build and patch: Kconfig/Kbuild, modules, checkpatch, get_maintainer | Build, modify, and prepare a patch |
| T0d | Binary and type inspection: nm, readelf, objdump, size, pahole | Inspect symbols, sections, layout, and types |
| T0e | Static analysis: sparse, smatch, coccinelle | Find and fix static issues |
| T0f | T0 capstone: integrate navigation, history, patch, build, inspection | Go from symptom to patch |
| T1a | QEMU, gdb, architecture vocabulary | Boot, break, inspect userspace and kernel |
| T1b | kgdb, crash, drgn, lockdep | Post-mortem, live introspection, and lock validation |
| T2 | strace | Syscall boundary and userspace/kernel handoff |
| T3 | ftrace, trace-cmd | Function and event tracing |
| T4 | perf | CPU, scheduling, memory, and hardware events |
| T5 | bpftrace, bpftool, BTF, eBPF, XDP | Programmable tracing and kernel/driver data-path acceleration |
| T6a | ip, ss, ip netns, ip -s | Address, link, route, socket, namespace state |
| T6b | tc, nft, conntrack, nstat | Queueing, filtering, connection and counter state |
| T6c | tcpdump, ethtool, iperf3, socat, traceroute | Capture, driver ring/offload inspection, traffic generation, path probes |
| T7a | kselftests, KUnit, virtme-ng | Run and write repeatable tests |
| T7b | syzkaller, stress-ng, fio, reproducer minimization | Fuzz, load, and reproduce |
| T8 | b4, lore, get_maintainer, checkpatch, syzbot | Upstream workflow |

Rules:

- T0a/T0b are prerequisites for T0c–T0f. Do not start with the kernel source.
- Each tool chapter has labs that teach the tool, not labs that only run it.
- T6c explicitly teaches `ethtool` as the primary driver observability tool: inspecting hardware RX/TX ring descriptor limits (`ethtool -g`), querying and toggling hardware offloads like TSO, GSO, and checksums (`ethtool -k`), and reading driver ASIC error counters directly from `struct ethtool_ops` (`ethtool -S`).
- Define every term before using it. Show expected output and common errors.
- Start T0a/T0b labs with tiny userspace examples before kernel examples.
- Use the eight tool lab families from `TOOLING.md`: guided tour, predict,
  filter, break-it, compose, diagnose, challenge, teach-back.
- No lab cap. A tool chapter gets as many labs as it needs.
- Mark every lab **core** or **stretch**. Core labs are required; stretch labs
  are optional depth. This controls effort, not creativity.
- Every lab that needs privilege states the exact requirement and a fallback:
  namespace, QEMU guest, or skip with a recorded reason.
- Captured `run`/`test` output must be deterministic or use tolerant matching.
  Normalize timestamps, counters, and CPU IDs before diffing.
- Every tool lab uses a real kernel question and a second confirming signal.
  T0a/T0b may use a userspace warm-up before the kernel question.

## 9. Networking track (M0 → M7)

This track runs alongside Phases B–D. It is broad on purpose: interface types,
tunnels, routing, transport, and observability are all first-class.

Baseline: you are already learning the socket API. M0 starts at the handoff
from a descriptor to a `net_device`; it does not reteach "what is a socket".

### M0 — `ip`, rtnetlink, and the object model

- Userspace: `ip link`, `ip addr`, `ip route`, `ip neigh`, `ip netns`.
- Kernel: `net/core/rtnetlink.c`, `net/core/dev.c`, `net/core/neighbour.c`.
- Experiment: create a dummy interface and watch netlink messages with `strace`
  or `ip -d link show`.
- Exit: explain how `ip link add` becomes a `net_device`.

### M1 — Loopback and the packet path

- Source: `drivers/net/loopback.c`, `net/core/dev.c`, `net/core/skbuff.c`, `include/linux/skbuff.h`, `net/ipv4/ip_input.c`,
  `net/ipv4/ip_output.c`.
- Hardware NIC vs Synthetic Drivers: Contrast software loopback with real hardware
  execution (`drivers/net/ethernet/intel/e1000/` or `virtio_net.c` in QEMU):
  * Coherent DMA rings (`dma_alloc_coherent`) vs streaming payload buffers (`dma_map_single`).
  * The NAPI interrupt mitigation loop: hardware IRQ → `napi_schedule()` → driver `poll()`
    routine draining ring in budget chunks (budget = 64) → `napi_complete_done()` → IRQ re-enable.
  * The MMIO doorbell register write (`writel`) notifying hardware of ready TX descriptors.
- `sk_buff` Lifetime, Anatomy, and Freeing Semantics:
  * Linear buffer bounds: `head`, `data`, `tail`, `end` pointers; dynamic header reservation and adjustment via `skb_reserve()`, `skb_put()`, `skb_push()`, and `skb_pull()`.
  * Cloning vs Copying: Shallow copies sharing linear data buffers (`skb_clone()`, `skb->cloned`, `dataref`) vs deep payload allocations (`skb_copy()`) vs fragmented clones (`pskb_copy()`).
  * Non-linear paged fragments: `skb_shinfo()`, `skb_frag_t`, `frags[]`, and how multi-page Jumbo frames or zerocopy packets avoid contiguous physical memory allocation.
  * Ownership and freeing semantics: `kfree_skb()` (drop/error path; triggers drop-monitor tracepoints) vs `consume_skb()` (normal successful consumption) vs `dev_kfree_skb_any()` (irq-safe freeing in drivers).
- Experiment: ping loopback; trace `netif_rx` / `netif_receive_skb` with ftrace; contrast
  with a trace of `e1000_intr()` and `e1000_clean_rx_irq()` under QEMU; trace `skb_clone` vs `skb_copy` memory overhead, inspecting `skb->users` and `skb_shinfo(skb)->dataref` reference counters via GDB/bpftrace.
- Exit: draw the exact TX → loopback → RX path, including skb ownership and headroom transitions, and contrast it
  with a hardware DMA ring + NAPI polling cycle.

### M2 — Interface zoo and the XDP Data Path

- Source: `drivers/net/dummy.c`, `veth.c`, `tun.c`, `tap.c`, `ifb.c`,
  `net/8021q/`, `drivers/net/macvlan.c`, `ipvlan/`, `net/bridge/`, `net/core/filter.c`.
- The Dual Data Path Architecture:
  * Traditional Kernel Stack: Driver RX ring → `napi_gro_receive()` → `__netif_receive_skb()` → `sk_buff` allocation → Netfilter PREROUTING → FIB routing lookup → socket receive queue.
  * Programmable Fast Path (XDP): In-driver execution (`bpf_prog_run_xdp()`) executing directly on the raw DMA buffer frame before `sk_buff` allocation. Possible driver verdicts: `XDP_DROP` (immediate wire drop), `XDP_TX` (bounce back out same NIC), `XDP_REDIRECT` (bypass host stack to veth/AF_XDP socket), `XDP_PASS` (allocate `sk_buff` and pass to standard kernel stack).
- Experiment: build a topology with veth + bridge + VLAN + dummy; compare
  `ip -d link`, `bridge link`, and `ip -s link`; attach a 15-line XDP program (`XDP_DROP`) to a veth pair, blast UDP packets using `iperf3`/`trafgen`, and measure the throughput and CPU difference between driver-level XDP drop (no `sk_buff` allocated) and Netfilter/iptables `-j DROP`.
- Exit: choose the right interface type for a stated problem and articulate when a packet should be handled by an in-driver XDP program versus the standard Linux networking stack.

### M3 — IPv4/IPv6, routing, ARP/ND

- Source: `net/ipv4/devinet.c`, `route.c`, `fib_trie.c`, `arp.c`,
  `net/ipv6/route.c`, `ndisc.c`.
- Experiment: add/delete routes; watch FIB lookup and neighbor resolution.
- Exit: explain a route lookup and an ARP/ND resolution from packet to cache.

### M4 — UDP and sockets

- Source: `net/ipv4/udp.c`, `net/ipv4/udp_tunnel_core.c`, `net/socket.c`,
  `net/core/sock.c`, `net/ipv4/af_inet.c`.
- Socket Buffer Memory Accounting:
  * Per-socket memory tracking: `sk_wmem_alloc` (transmit buffer bytes queued) and `sk_rmem_alloc` (receive buffer bytes queued).
  * Socket buffer sizing: `SO_SNDBUF` / `SO_RCVBUF` limits vs kernel auto-tuning.
  * Memory exhaustion & drop paths: What happens when `sk_rmem_alloc` exceeds `sk_rcvbuf` (`sock_queue_rcv_skb` fails, drops counted in `/proc/net/snmp` `UdpRcvbufErrors` and `ss -u -m`).
- Experiment: send datagrams, fill a receive buffer, watch drops in `ss -u -a -m`
  and `/proc/net/snmp` (`UdpRcvbufErrors`), and inspect `sk_rmem_alloc` saturation.
- Exit: explain UDP encapsulation, checksums, socket memory accounting, and receive queue limits.

### M5 — TCP

- Source: `net/ipv4/tcp.c`, `tcp_input.c`, `tcp_output.c`, `tcp_timer.c`,
  `tcp_cong.c`, `tcp_cubic.c`, `tcp_bbr.c`.
- TCP Memory Pressure and Auto-tuning:
  * Memory limits: `/proc/sys/net/ipv4/tcp_rmem` (min, default, max) and `tcp_wmem`.
  * Global system memory pressure: `/proc/sys/net/ipv4/tcp_mem` (min, pressure, max in 4KB page units).
  * Auto-tuning engine: Dynamic receive buffer scaling based on Bandwidth-Delay Product (BDP) vs memory pressure throttling (`tcp_memory_pressure`, `sk_stream_wait_memory`).
- Experiment: compare CUBIC and BBR on a lossy link; trace retransmits and
  congestion-window changes; lower `/proc/sys/net/ipv4/tcp_mem` thresholds to force simulated memory pressure, observe TCP window clamping, socket memory throttling in `ss -ti -m`, and memory allocation stall traces.
- Exit: explain handshake, slow start, loss recovery, socket memory accounting, and one congestion
  control choice with evidence.

### M6 — Tunnels and overlays (VXLAN is one module)

- Source: `net/ipv4/ip_tunnel.c`, `ip_tunnel_core.c`, `udp_tunnel_core.c`,
  `drivers/net/vxlan/`, `geneve.c`, `net/bridge/`, `net/8021q/`.
- Experiment: build VXLAN, GENEVE, and GRE overlays over a veth/bridge
  underlay; compare encapsulation, FDB behavior, and MTU.
- Exit: explain encapsulation overhead, underlay vs overlay, and when to use
  VXLAN vs GENEVE vs GRE vs a plain bridge/VLAN.

### M7 — Observability and testing

- Tools: T6a/T6b/T6c (`ip -s`, `ss`, `nstat`, `tc -s`, `nft`, `tcpdump`,
  `ethtool`) plus ftrace, perf, and bpftrace.
- Source: `net/core/net-procfs.c`, `net/ipv4/inet_diag.c`, `net/core/flow_dissector.c`.
- Dual Data-Path Tracing:
  * Kernel Traditional Stack: `napi_gro_receive` → `__netif_receive_skb` → `sk_buff` traversal → netfilter hooks → qdisc queues.
  * eBPF / XDP Fast Path: `bpf_prog_run_xdp` → `xdp_redirect_map` → `tracepoint:xdp:xdp_exception`.
- Experiment: answer one live question (drops, retransmits, qdisc backlog, or XDP vs stack CPU overhead) with
  two independent tools and reconcile them.
- Exit: a reproducible measurement note that another person can rerun.

## 10. Deep-dive options (choose after M7)

Pick one, then study it at modern LTS depth:

- TCP congestion control and loss recovery
- Routing and FIB performance
- Netfilter/conntrack/NAT
- qdisc, fq_codel, netem, and traffic shaping
- eBPF/XDP and the data path
- Network driver, PCIe lifecycle, and NAPI
- Platform device driver and Device Tree (`.dts`/`.dtb`)
- Namespaces, veth, and container networking
- Tunnels and overlay control planes
- kTLS, MPTCP, or WireGuard
- Wireless and mac80211

Selection rule: choose the subsystem you already had to touch twice during M0–M7.

A deep dive is done when you can produce:

- a version-pinned reading map with the five most important functions;
- a path diagram from entry point to return path;
- two experiments, each with a prediction, a change, and raw output;
- one patch, config change, or probe that changes what you observe;
- a two-tool evidence note reconciling independent views;
- a five-minute teach-back that states what the subsystem does not do.

## 11. Termlearn integration

Chapter packs will be generated later. They will use the existing pack schema:

```yaml
labs:
  - id: lab1
    title: "Trace loopback"
    instruction_md: |
      ...
    files:
      - path: probe.sh
        content: |
          ...
    commands:
      run: "sh probe.sh"
      test: "sh check.sh"
      tinker: "sh"
      timeout_s: 10
    test_cases:
      - name: "probe prints lo"
        stdin: ""
        expect: "lo\n"
        expect_exit: 0
    hints:
      - "..."
```

- `run` and `test` are captured and diffed as usual.
- `tinker` is interactive and inherits the terminal.
- In the TUI press `x`; in CLI `lab` mode type `x`.
- Separate-terminal order: `TERMLEARN_TINKER_TERMINAL`, tmux, alacritty, then
  suspend/resume.
- Kernel excerpts must use `lang: text` or `asm`, never `lang: c`, because
  `validate` compile-probes C examples.
- There is no lab cap. A chapter gets as many labs and lab families as it needs.
- Tool chapters use tool-teaching labs, not demos. See `TOOLING.md`.

Lab families for this curriculum:

1. **Knob** — change a sysctl, qdisc, or build option.
2. **Break-it** — introduce a small bug or misconfiguration.
3. **Instrument** — add a tracepoint or `printk`, rebuild, observe.
4. **Ablation** — remove a feature or path and compare behavior.
5. **Rebuild** — rebuild an old kernel with a modern toolchain.
6. **Predict** — write the expected trace before running the experiment.
7. **Guided tour** — read a tool's output on a known workload.
8. **Filter** — remove noise one filter at a time and explain each removal.
9. **Compose** — confirm one tool's view with a second tool.
10. **Diagnose** — start from a symptom, choose the tool, gather evidence.
11. **Challenge** — open-ended, reproducible question with an artifact.
12. **Teach-back** — write the tool's mini-manual and limitations.
13. **Algorithm synthesis** — analyze a core kernel data structure or algorithm directly
    in source, isolate its invariants and edge cases, and implement a clean, standalone,
    test-driven equivalent in C.

### Algorithm Synthesis Labs (Kernel DSA Extraction)

These labs bridge kernel source analysis and systems-level algorithmic mastery. The learner
inspects the kernel source file, identifies the core data structure invariant, and implements
a test-driven userspace C equivalent:

| Chapter | Subsystem / Algorithm | Source Target | Synthesis Lab Task |
|---------|-----------------------|---------------|-------------------|
| A2 | 0.11 Dynamic Priority Scheduler | `kernel/sched.c` | Implement an interactive task scheduler simulating counter decay `(counter >> 1) + priority` |
| A3 | Physical Page Frame Allocator | `mm/memory.c` | Implement a 4KB chunk memory pool allocator using `mem_map[]` reference counting |
| A4 | LRU Buffer Cache | `fs/buffer.c` | Implement a fixed-capacity buffer cache with hash buckets (`hash(dev, block)`) and circular LRU eviction |
| B1 | Intrusive Doubly-Linked List | `include/linux/list.h` | Implement `struct list_head`, `list_add`, `list_del`, and the `container_of` macro in C |
| B6 | Lockless Ring Buffer / FIFO | `drivers/char/` / `kfifo` | Implement a power-of-2 circular FIFO ring buffer with head/tail modulo wrapping for single-producer single-consumer |
| C3 | Binary Buddy Allocator | `mm/page_alloc.c` | Implement an order-0 to order-10 binary buddy allocator with block splitting and buddy coalescing |
| C4 | Radix Tree Page Index | `lib/radix-tree.c` | Implement a trie/radix tree mapping 32-bit linear page offsets to memory pointers |
| C9 | RCU Grace Period & Pointer Publishing | `include/linux/rcupdate.h` | Implement a lockless single-writer multi-reader linked list in C with RCU read side, atomic pointer swapping, and grace-period reclamation |
| M1 | DMA Descriptor Ring | `drivers/net/ethernet/intel/e1000/` | Implement a mock circular DMA ring buffer with hardware ownership flags and doorbell update |
| M1 | `sk_buff` Buffer & Headroom Manager | `net/core/skbuff.c` | Implement an intrusive packet buffer in C with `skb_reserve`, `skb_push`, `skb_put`, and reference-counted `skb_clone` |
| M2 | Minimal Driver-Level XDP Packet Filter | `net/core/filter.c` / `samples/bpf/` | Implement a standalone packet parsing engine in C matching MAC/IP headers and executing drop/forward actions in linear buffers |
| M3 | Longest Prefix Match (LPM) Trie | `net/ipv4/fib_trie.c` | Implement a bitwise routing trie for IPv4 CIDR subnet lookup (`192.168.1.0/24`) |
| M5 | TCP Congestion State Machine | `net/ipv4/tcp_cubic.c` | Implement the window growth/reduction math simulating TCP slow start, congestion avoidance, and fast recovery |
| T6b | Token Bucket Rate Limiter | `net/sched/sch_tbf.c` | Implement a token bucket traffic shaper calculating token replenishment over microsecond intervals |

### Evidence-first authoring

Chapter packs are generated one vertical slice at a time, and only from
observed evidence. The authoring AI must **use** the thing it is writing about;
it must not reconstruct behavior from memory, blog posts, or plausible-looking
output.

#### Source of truth

| Chapter type | Source of truth | Not evidence |
|--------------|-----------------|--------------|
| Tooling (T0a–T8) | Actual runs in the pinned environment: commands, workload files, versions, raw stdout/stderr, exit codes, and second-signal comparisons | `TOOLING.md` prose, man-page memory, guessed flags, output copied from another machine |
| Kernel phase (A1–D7) | Pinned kernel tag/commit, exact source ranges from that tree, config, and captured build/boot/trace output | Modern source read while studying old code, remembered function names, line numbers from another version |
| Networking (M0–M7) | Pinned kernel source plus observed namespace/interface/socket/counter behavior from a clean environment | Generic networking tutorials, assumed defaults, unverified `ip`/`ss` output |

#### Evidence bundle

Before drafting, capture a bundle for each chapter:

```text
evidence/<chapter>/
  manifest.json          command, cwd, env, exit code, artifact paths, evidence IDs
  transcript.md          raw stdout/stderr with command boundaries
  source/                exact source ranges with commit:path:line and file hashes
  artifacts/             logs, traces, diffs, screenshots or serial captures
  environment.json       uname, distro, kernel version, tool versions, config
```

Each evidence item gets an ID such as `E-T0A-03` or `E-A1-02`. Every factual
claim in the chapter refers to one or more IDs.

#### Authoring steps

1. **Pin the environment.** Record kernel version/commit/tag, tree hash, kernel
   config, architecture, distro, and tool versions. For old kernels, state
   whether the source is the pristine tarball or the runnable fork.
2. **Capture evidence before prose.**
   - Tooling: run each intended command on a known workload; capture success,
     failure, filter changes, and a second signal. Execute the `tinker` command
     before writing it into a lab.
   - Kernel: extract exact source ranges with `git show <tag>:<path>` or
     `git blame`; capture build, boot, gdb, ftrace, perf, or namespace output
     whenever the chapter claims runtime behavior.
3. **Build the evidence manifest.** Store command, working directory, exit
   code, raw artifact paths, source hash, tool versions, and privilege mode.
4. **Draft from evidence only.** Expected output comes from captured output;
   source references come from extracted source; "what to notice" items come
   from observed columns or events. If something is not in the bundle, it is an
   open question, not a sentence in the chapter.
5. **Verify mechanically.** Re-run `run`, `test`, and `tinker` in a clean
   workspace. Normalize volatile fields such as timestamps, counters, CPU IDs,
   and addresses. Verify every source snippet and line range against the pinned
   commit. Run `main.py validate --book linux-kernel --chapter <id> --strict`.
6. **Fail closed.** No evidence means no lab. A privileged tool that was not
   observed in QEMU, a namespace, or an allowed host context is skipped or
   marked unavailable; its output is never invented. A missing symbol or source
   line is reported as missing, not guessed.
7. **Pilot in termlearn.** The pack is approved only after all labs pass in a
   clean workspace and the evidence IDs trace to raw artifacts.
8. **Only then generate the next slice.**

The first pilot slice is **T0a + T1a userspace gdb + A1**. For that slice the
evidence capture comes first: compile/run/git output for T0a; real gdb
transcripts for T1a; and pinned 0.11 source plus boot/gdb output for A1. Do not
generate all chapter packs at once.

## 12. Milestones and rough time

| Milestone | Scope | Estimate |
|-----------|-------|----------|
| P0 | Plan docs, sources fetched, T0a–T0b, 0.11 boots | 2–3 weeks |
| P1 | Phase A + T0c–T0f + T1a/T2 tool labs | 7–9 weeks |
| P2 | Phase B + T2/T3 tool labs | 6–8 weeks |
| P3 | Phase C + T3/T4/T6a/T6b tool labs | 8–10 weeks |
| P4 | Modern build/boot, D1–D4, T1b/T4 | 7–9 weeks |
| P5 | Networking M0–M3 + T6a | 5–7 weeks |
| P6 | Networking M4–M5 + T5/T6b/T6c | 6–8 weeks |
| P7 | Networking M6–M7 + T1b/T5/T7a/T7b | 6–8 weeks |
| P8 | Deep dive + T8 | 8–12 weeks |
| P9 | Capstone write-up | 2 weeks |

Total: roughly 12–17 months at a sustainable pace. This assumes deliberate
overlap: short tool chapters run alongside kernel phases, and only core labs
are mandatory. C reading and socket API vocabulary are already present, so no
C-syntax or networking-101 track is included. If old-kernel builds require
container work, add a 15–20% buffer.

## 13. First two weeks

1. Read this plan and `TOOLING.md`; install the missing tools from
   `ENVIRONMENT.md`.
2. Do T0a: compile, run, and modify a 10-line C program; initialize a toy git
   repository and make a commit. No C syntax lesson is needed.
3. Do T0b: find a symbol in the toy repo with `rg`, then use `git log -S` and
   `git blame`. Repeat once in the kernel tree.
4. Read `SOURCES.md`; fetch the tarballs and graft the git history.
5. Boot 0.11 in QEMU; save the exact command and output.
6. Do the first T1a lab: debug the 10-line program with gdb — breakpoint,
   `list`, `print`, `next`, `bt`. Then break at `start_kernel` once under QEMU.
7. Do the first T2 lab: trace one `ip` command with `strace -f -tt -T`.
8. Read `TINKERING.md`; run one knob experiment and one instrument experiment.
9. Write the first journal entry in `notes/`, review this plan, capture the
   pilot evidence bundles, and only then generate the pilot packs: T0a, T1a
   userspace gdb, and A1.

## 14. Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Old kernels do not build with modern gcc | Use Docker images from the era, `-m32`, or the runnable 0.11 fork |
| Modern tree is too large | Keep slices small; use cscope/clangd and `git log -S` |
| Experiments mutate the host network | Use network namespaces, veth, and QEMU; never edit host routes casually |
| Reading without retention | Require an explain-back artifact per chapter |
| Tool tourism ("I ran the command") | Each tool lab needs a question, a second signal, and a teach-back |
| Tool overload | T1/T6/T7 split into focused chapters; one new tool per lab |
| Beginner tool overload | T0a/T0b start with tiny userspace examples; define terms before use |
| C/socket baseline drift | No C-syntax or networking-101 track; labs ask kernel questions, not grammar |
| Nondeterministic output | Normalize timestamps/counters/CPU IDs; use tolerant `expect` matching |
| Privilege or tool permission failure | State exact capability and namespace/QEMU fallback per lab |
| Scope/time underestimate | Only core labs required; overlap stated; 15–20% buffer for build setup |
| Too many shallow labs | No lab cap, but every lab must teach one skill; no filler labs |
| Tool gaps (tcpdump, perf, bpftrace) | Install per `ENVIRONMENT.md`; use `ss`, `nstat`, ftrace as fallbacks |
| VXLAN tunnel vision | Networking M6 explicitly compares VXLAN, GENEVE, GRE, bridge, and VLAN |
| Chapter generation drifts from reality | Evidence-first authoring; every claim traced to a raw artifact; fail closed on missing evidence |

## 15. What is intentionally not here yet

- No `books/linux-kernel/meta.json`.
- No `evidence/<chapter>/` bundles.
- No `packs/linux-kernel/` chapter YAML.
- No T0a–T8 tool chapter packs yet.
- No generated study blocks, quizzes, or labs.
- No deep-dive choice.

Those come after the plan review and the first source-fetch/boot session.

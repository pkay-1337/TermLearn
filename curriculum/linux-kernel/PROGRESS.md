# Progress

Update this file after each experiment or study session. Keep dates in ISO
format. A checked box means there is an artifact in `notes/` or `sources/`.
Baseline: C reading and basic socket API vocabulary are assumed; kernel tooling
is not.

## Milestones

- [ ] P0 — Plan reviewed; sources fetched; T0a–T0b basics; 0.11 boots in QEMU
- [ ] P1 — Phase A complete (0.01/0.11/0.12) + T0c–T0f + T1a/T2 tool labs
- [ ] P2 — Phase B complete (0.95 → 1.2) + T2/T3 tool labs
- [ ] P3 — Phase C complete (2.0 → 2.6.12) + T3/T4/T6a/T6b tool labs
- [ ] P4 — Modern build/boot and D1–D4 + T1b/T4
- [ ] P5 — Networking M0–M3 + T6a
- [ ] P6 — Networking M4–M5 + T5/T6b/T6c
- [ ] P7 — Networking M6–M7 + T1b/T5/T7a/T7b
- [ ] P8 — Deep dive + T8
- [ ] P9 — Capstone write-up

## Tooling track

T0a/T0b assume no prior tool experience; C reading and socket API vocabulary
are already present. Use a tiny program and toy repo first.

- [ ] T0a terminal, files, processes, C compiler, make, git basics
- [ ] T0b grep/rg, cscope/clangd, git log/blame/bisect
- [ ] T0c Kconfig/Kbuild, modules, checkpatch, get_maintainer
- [ ] T0d nm, readelf, objdump, size, pahole
- [ ] T0e sparse, smatch, coccinelle
- [ ] T0f capstone: symptom → symbol → commit → patch → build → check
- [ ] T1a QEMU, gdb, architecture vocabulary (userspace first, then kernel)
- [ ] T1b kgdb, crash, drgn (post-mortem, Phase D)
- [ ] T2 strace
- [ ] T3 ftrace, trace-cmd
- [ ] T4 perf
- [ ] T5 bpftrace, bpftool, BTF, eBPF
- [ ] T6a ip, ss, ip netns, ip -s
- [ ] T6b tc, nft, conntrack, nstat
- [ ] T6c tcpdump, ethtool, iperf3, socat, traceroute
- [ ] T7a kselftests, KUnit, virtme-ng
- [ ] T7b syzkaller, stress-ng, fio, reproducer minimization
- [ ] T8 b4, lore, get_maintainer, checkpatch, syzbot

For each tool chapter, check the lab families that have artifacts:

- [ ] guided tour
- [ ] predict
- [ ] filter
- [ ] break-it
- [ ] compose
- [ ] diagnose
- [ ] challenge
- [ ] teach-back

## Phase exit gates

Check these before moving to the next phase:

- [ ] path diagram drawn from memory
- [ ] rebuild or patch plus exact diff
- [ ] two-tool evidence note with commands and raw output
- [ ] explain-back or teach-back artifact
- [ ] evidence bundle reviewed; no unverified claims remain
- [ ] open questions recorded below
- [ ] `PLAN.md` updated if a prerequisite was missing

## Phase A — Early kernels

- [ ] A1 boot and first C
- [ ] A2 processes and scheduling
- [ ] A3 memory
- [ ] A4 filesystem and syscalls
- [ ] A5 build, run, and trace

## Phase B — 0.95 → 1.2

- [ ] B1 init, modules, architecture
- [ ] B2 scheduler and signals
- [ ] B3 virtual memory
- [ ] B4 VFS and block layer
- [ ] B5 first networking stack
- [ ] B6 character and misc devices

## Phase C — 2.0 → 2.6.12

- [ ] C1 build, config, boot
- [ ] C2 scheduler and preemption
- [ ] C3 memory management
- [ ] C4 VFS and page cache
- [ ] C5 block and I/O
- [ ] C6 networking core
- [ ] C7 netfilter and qdisc
- [ ] C8 Unified Device Model and sysfs
- [ ] C9 concurrency, locking, and lockdep

## Phase D — Modern

- [ ] D1 build, boot, config
- [ ] D2 scheduler and namespaces
- [ ] D3 memory
- [ ] D4 VFS, block, filesystems
- [ ] D5 networking core
- [ ] D6 PCIe drivers, virtio, and virtual interfaces
- [ ] D7 tooling capstone (two independent tools, one live question)
- [ ] D8 security and isolation

## Networking track

- [ ] M0 `ip`, rtnetlink, object model
- [ ] M1 loopback and packet path
- [ ] M2 interface zoo
- [ ] M3 IPv4/IPv6, routing, ARP/ND
- [ ] M4 UDP and sockets
- [ ] M5 TCP
- [ ] M6 tunnels and overlays (VXLAN, GENEVE, GRE, bridge, VLAN)
- [ ] M7 observability and testing

## Deep dive

Chosen subsystem:

- [ ] Choice recorded with a reason
- [ ] Reading map written with five key functions
- [ ] Path diagram from entry point to return path
- [ ] Two experiments complete, each with prediction/change/raw output
- [ ] One patch, config change, or probe changes what you observe
- [ ] Two-tool evidence note reconciles independent views
- [ ] Five-minute teach-back written
- [ ] Capstone note written

## Journal index

| Date | Chapter / experiment | Artifact | Status |
|------|----------------------|----------|--------|
| | | | |

## Environment log

Record tool and kernel versions when they change:

| Date | Kernel | gcc | iproute2 | QEMU | Notes |
|------|--------|-----|----------|------|-------|
| | | | | | |

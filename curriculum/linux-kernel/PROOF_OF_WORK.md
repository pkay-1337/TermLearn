# Engineering Portfolio & Proof-of-Work Guide

> **Purpose:** Transform your curriculum milestones and termlearn evidence dossiers into high-signal public artifacts (technical blog posts, GitHub evidence repositories, and LinkedIn technical write-ups) that catch the attention of kernel maintainers, systems hiring managers, and hardware/silicon recruiters.

---

## 1. The "Anti-Fluff" Systems Portfolio Strategy

Most public tech posts are ignored by senior engineering leads because they are generic: *"Day 14 of 100 Days of Code! I read about memory!"* Senior systems engineers and hiring managers at companies like Qualcomm, NVIDIA, Apple, Google, and Red Hat cringe at certificates and superficial summaries.

### What Actually Makes a Principal Engineer Stop and Message You?
1. **Specific, Pinned Grounding:** You cite exact files, line numbers, and commits (`sources/early-history.git@v0.11:kernel/sched.c#L125` or `linux-6.18/drivers/pci/`).
2. **Empirical Evidence over Text:** You include real terminal transcripts, GDB register dumps, `pahole` struct layouts, ftrace graphs, or Wireshark captures.
3. **The "Tinker" Delta:** You explain what happened when you changed one variable or introduced a deliberate bug: *"I doubled the time slice from 15 to 30 ticks; here is the Gantt chart of how process CPU time shifted."*
4. **Synthesized Algorithms:** You link to a standalone, unit-tested C implementation of a kernel data structure (e.g., your extracted `list_head` or lockless ring buffer).

---

## 2. The 5-Part Post Blueprint

Every blog post or LinkedIn technical write-up should follow this structured format:

```markdown
### [Hook / Problem]
A concrete technical question or common misconception.
(e.g., "Why does `size app` report 4MB of .bss, but `ls -l` shows the binary is only 16KB?")

### [The Kernel Mechanism]
The exact architecture, struct, or state machine from the pinned source.
(Include 5–10 lines of actual kernel source or C implementation).

### [The Experiment & What Broke]
What you tested, what parameter you changed, or what bug you introduced.
(Include command, flags, and the observed surprise).

### [The Visual / Evidence Artifact]
An ASCII memory diagram, an annotated GDB register dump, a `pahole` struct comparison,
or an ftrace function graph showing the exact hardware/kernel behavior.

### [The Production Takeaway & Code Link]
Why this matters in high-performance computing, drivers, or cloud environments.
Link to your GitHub repo evidence dossier / termlearn lab run.
```

---

## 3. Chapter-by-Chapter Proof-of-Work Menu

*(Skipping preliminary shell/git basics T0a and T0b; start publishing from T0c onward).*

### Tooling Chapters (T0c → T2)

#### Chapter T0c — Build & Patch
* **Post Title:** *Deconstructing Kbuild: How a Single Kconfig Flag Propagates to C Machine Code*
* **What to Document:**
  - Trace a flag (`CONFIG_FOO=y` vs `CONFIG_FOO=m`) from `Kconfig` → `.config` → `include/generated/autoconf.h` macro definition.
  - Show the Kbuild object compilation pipeline (`obj-y` built into `vmlinux` vs `obj-m` loadable `.ko`).
  - **Evidence Artifact:** A side-by-side diff of `autoconf.h` and the resulting binary symbols in `nm`.
  - **Key Takeaway:** How the Linux kernel achieves modularity without runtime overhead.

#### Chapter T0d — Binary & Type Inspection
* **Post Title:** *Finding Hidden Memory Holes: How `pahole` and Cacheline Alignment Optimize C Structs*
* **What to Document:**
  - Explain CPU natural alignment (4-byte int, 8-byte pointer) and compiler padding.
  - Dissect an unoptimized struct with `pahole` showing wasted bytes and cacheline boundary crossings (`/* size: 128, cachelines: 2 */`).
  - Reorder members to eliminate holes and shrink the struct into a single 64-byte cacheline.
  - **Evidence Artifact:** Raw `pahole` before-and-after output showing bytes saved and cacheline efficiency.
  - **Key Takeaway:** Why memory layout matters for network packet headers (`sk_buff`) and multicore performance.

#### Chapter T0e — Static Analysis
* **Post Title:** *Why GCC Won't Save You from Kernel Crashes: Trapping `__user` Pointer Bugs with Sparse*
* **What to Document:**
  - Explain why direct dereferences of userspace pointers inside Ring 0 cause critical security vulnerabilities or page faults.
  - Introduce kernel address space tags (`__user`, `__kernel`, `__iomem`, `__rcu`).
  - Show Sparse detecting an illegal assignment that GCC compiled without any warnings.
  - **Evidence Artifact:** The Sparse diagnostic output compared with the silent GCC compiler pass.
  - **Key Takeaway:** How the kernel enforces address-space safety across the user/kernel privilege boundary.

#### Chapter T0f — Tooling Capstone
* **Post Title:** *From Crash Symptom to Upstream Patch: An Empirical Debugging Walkthrough*
* **What to Document:**
  - The step-by-step triage loop: Symptom observation → Navigation (`rg`, `git log -S`) → Minimal patch → Verification.
  - Running `checkpatch.pl --strict` and `get_maintainer.pl`.
  - **Evidence Artifact:** The formatted patch (`git format-patch -1`) accompanied by dual-signal verification notes (`nm` + functional test).

#### Chapter T1a — QEMU & GDB
* **Post Title:** *Why Optimized C Code Lies in GDB: Tracing `start_kernel` with Hardware Breakpoints in QEMU*
* **What to Document:**
  - Contrast userspace `ptrace` with QEMU Remote Serial Protocol (RSP) stub debugging (`-s -S`).
  - Explain why software breakpoints (`int3`) fail in early boot before paging is initialized, and why hardware breakpoints (`hbreak`) are mandatory.
  - Show compiler optimizations (`-O2`): inlining, dead code elimination, and variables marked `<optimized out>`.
  - **Evidence Artifact:** Annotated GDB session stepping through early assembly and inspecting `CR0` and `CR3` registers.

#### Chapter T2 — strace
* **Post Title:** *Beyond Basic `strace`: Profiling Syscall Latency and Decoding Sockets with `-yy` and `-T`*
* **What to Document:**
  - Explain the system call context switch boundary (Ring 3 to Ring 0).
  - Use `-yy` to decode file descriptors directly into peer IP addresses, ports, and file paths.
  - Use `-c` and `-T` to isolate whether an application slowdown is caused by userspace CPU loops or blocked kernel calls.
  - **Evidence Artifact:** An annotated `strace -c` latency summary table isolating a blocking syscall.

---

### Phase A: Early Kernels — Linux 0.11 (A1 → A5)

#### Chapter A1 — Boot & First C
* **Post Title:** *From BIOS Reset to `main()`: The 20 Assembly Instructions That Booted Linux 0.11*
* **What to Document:**
  - The exact 3-stage handoff: `bootsect.s` (0x7C00 → 0x90000) → `setup.s` (A20 gate, setting `CR0.PE`, far jump `jmpi 0,8`) → `head.s` (GDT/IDT, 16MB identity paging at 0x0000–0x4000, setting `CR0.PG`).
  - The moment the CPU transitions from 16-bit Real Mode to 32-bit Protected Mode with Paging.
  - **Evidence Artifact:** A step-by-step memory relocation diagram and GDB register dump at the entry of `main()`.
  - **Algorithm Extraction:** None (hardware architecture focus).

#### Chapter A2 — Processes & Scheduling
* **Post Title:** *How Linux Scheduled Tasks Before CFS: Dissecting the 0.11 $O(N)$ Priority Decay Algorithm*
* **What to Document:**
  - The 4KB `task_union` structure (process control block at the bottom, stack growing downward).
  - The 100Hz PIT timer interrupt (IRQ0) decrementing `current->counter`.
  - The $O(N)$ selection loop: finding the maximum counter, and the global refresh formula `counter = (counter >> 1) + priority`.
  - Hardware TSS context switching via `ljmp`.
  - **Evidence Artifact:** A timeline chart showing timer ticks, counter decrements, and task preemption.
  - **Algorithm Extraction Link:** Share your GitHub repo implementing the interactive userspace C simulation of the 0.11 priority scheduler.

#### Chapter A3 — Virtual Memory & Paging
* **Post Title:** *Watching Copy-On-Write Happen Live: Two-Level Paging, `INT 14`, and `CR2` in Linux 0.11*
* **What to Document:**
  - The x86 32-bit two-level paging walk: Directory (10 bits) → Table (10 bits) → Offset (12 bits).
  - How `sys_fork()` marks child page tables read-only for Copy-On-Write.
  - Step-by-step handling of a page fault (`INT 14`): reading the faulting linear address from `CR2`, checking error code, allocating a fresh physical page, and remapping PTE as writable.
  - **Evidence Artifact:** GDB breakpoint logs on `do_wp_page()` capturing `CR2` and tracking `mem_map[]` reference counts incrementing and decrementing.
  - **Algorithm Extraction Link:** Share your 4KB chunk memory pool allocator built in userspace C.

#### Chapter A4 — Filesystem & Buffer Cache
* **Post Title:** *From `int 0x80` to Disk Blocks: The Pointer Chain Behind the Linux Buffer Cache*
* **What to Document:**
  - The 4-level pointer chain: `filp[fd]` → `file_table[64]` → `inode_table[32]` → Buffer Cache `hash_table[307]`.
  - Path traversal in `namei.c`: converting `/usr/bin/sh` to disk inode numbers.
  - How the buffer cache combines hash buckets for $O(1)$ block lookup with a circular doubly linked LRU list for buffer recycling.
  - **Evidence Artifact:** An architectural diagram tracing `sys_read()` down to `bread()` and device request queues.
  - **Algorithm Extraction Link:** Share your fixed-capacity LRU buffer cache implemented in standalone C.

#### Chapter A5 — Build, Run & Trace Capstone
* **Post Title:** *Rebuilding a 1991 Operating System on Modern Hardware: `tools/build.c` and Floppy Sector Geometry*
* **What to Document:**
  - Deconstructing `tools/build.c`: stitching `bootsect`, `setup`, and `system` into a bootable raw disk image and patching root device bytes at offset 508.
  - Why 1991 GCC 1.40 assembly idioms fail on modern ELF toolchains, and how the runnable fork resolves them.
  - **Evidence Artifact:** A complete terminal transcript showing the clean build, disk image generation, and QEMU serial boot.

---

### Phase B: Middle Kernels — 1.2 (B1 → B6)

#### Chapter B1 — Modules & The Intrusive Linked List
* **Post Title:** *The Genius of Linux's `list_head` and the Pointer Math Behind `container_of()`*
* **What to Document:**
  - Why traditional computer-science linked lists (with dedicated node pointers) cause memory fragmentation in operating systems.
  - How Linux embeds `struct list_head` directly inside data structures.
  - The exact pointer arithmetic in `container_of()`: `(type *)((char *)ptr - offsetof(type, member))`.
  - **Evidence Artifact:** A memory diagram of three distinct structs linked together on a single list.
  - **Algorithm Extraction Link:** Share your clean, unit-tested userspace C implementation of generic intrusive linked lists.

#### Chapter B6 — Character Drivers & Device Boundary
* **Post Title:** *Writing a Linux Character Device Driver in 100 Lines of C: `file_operations` and the User Boundary*
* **What to Document:**
  - The fundamental driver contract: `struct file_operations` mapping `open`, `read`, `write`, `release`.
  - Demultiplexing major/minor numbers and the modern `misc_register()` wrapper.
  - The security boundary: why dereferencing user pointers crashes the kernel, and how `copy_to_user()` / `copy_from_user()` validate page tables.
  - **Evidence Artifact:** Code snippet of the driver and terminal transcript of `echo "hello" > /dev/ringbuf` and `cat /dev/ringbuf`.
  - **Algorithm Extraction Link:** Share your lockless single-producer single-consumer circular FIFO ring buffer with power-of-2 wrapping.

---

### Phase C: Modern Skeleton — 2.6.12 (C1 → C9)

#### Chapter C3 — The Binary Buddy Allocator
* **Post Title:** *How the Linux Kernel Prevents Memory Fragmentation: The Binary Buddy Allocator*
* **What to Document:**
  - Why naive dynamic memory allocators fragment physical RAM over time.
  - How Linux manages physical page frames using power-of-2 order lists (Order-0: 4KB to Order-10: 4MB).
  - The buddy address invariant: `buddy_pfn = pfn ^ (1 << order)`.
  - Block splitting on allocation and buddy coalescing on free.
  - **Evidence Artifact:** ASCII state diagram showing a 64KB block splitting down to 4KB and coalescing back up.
  - **Algorithm Extraction Link:** Share your binary buddy memory allocator written in pure C with unit tests.

#### Chapter C8 — The Unified Device Model & `sysfs`
* **Post Title:** *Why Linux Invented `/sys`: The Unified Device Model, `kobject`, and Driver Binding*
* **What to Document:**
  - The chaos of pre-2.6 device management and why `/proc` was abandoned for hardware devices.
  - The core triad: `struct bus_type`, `struct device`, and `struct device_driver`.
  - The driver matching lifecycle: bus scanning, `driver->probe()`, and `driver->remove()`.
  - How `kobject` trees automatically generate `/sys/bus/`, `/sys/class/`, and `/sys/devices/`.
  - **Evidence Artifact:** Code showing a custom platform driver creating attributes via `DEVICE_ATTR_RW` and reading them from userspace via `cat /sys/...`.

#### Chapter C9 — Concurrency, Locking & Lockdep
* **Post Title:** *Why Linux Doesn't Deadlock on 128 Cores: Spinlocks, RCU, and Decoding Lockdep Splats*
* **What to Document:**
  - The golden maintainer rule: why you can never sleep in atomic context (and what happens when you do: `BUG: scheduling while atomic`).
  - Spinlocks vs Mutexes: CPU cacheline spinning vs thread descheduling.
  - Read-Copy-Update (RCU): How modern Linux networking achieves lockless, wait-free reads via atomic pointer swaps (`rcu_assign_pointer`) and grace periods (`synchronize_rcu`).
  - Lockdep (`CONFIG_PROVE_LOCKING`): How the kernel validates lock acquisition order graphs and catches circular dependencies ($A \to B$ vs $B \to A$) before deadlocks occur.
  - **Evidence Artifact:** Transcript of a deliberate circular lock dependency injected into QEMU, decoding the resulting lockdep splat in `dmesg`.
  - **Algorithm Extraction Link:** Share your lockless single-writer multi-reader linked list in C implementing RCU grace periods and atomic pointer publishing.

---

### Phase D & Networking: Modern Linux (D1 → D6, M0 → M7)

#### Chapter D6 — PCIe Drivers, MMIO & Virtio
* **Post Title:** *How Linux Talks to PCIe Devices: Probing, BAR Mapping, and MSI-X in QEMU*
* **What to Document:**
  - The anatomy of a PCIe driver: `struct pci_driver`, vendor/device ID tables (`struct pci_device_id`).
  - Base Address Registers (BARs) and mapping hardware registers into kernel virtual memory via `pci_iomap()`.
  - Interrupt architectures: Legacy line IRQs vs Message Signaled Interrupts (`MSI`/`MSI-X` multi-queue).
  - Enabling bus mastering for DMA transfers (`pci_set_master()`).
  - **Evidence Artifact:** QEMU session loading a custom PCI device driver, reading its BAR registers, and logging interrupt arrival.

#### Chapter M1 — Loopback vs. Hardware NICs (NAPI, DMA & sk_buff Lifetime)
* **Post Title:** *Why High-Speed Linux Networking Doesn't Use Interrupts: DMA Rings, NAPI, and sk_buff Ownership*
* **What to Document:**
  - The "interrupt storm" problem: why handling one hardware interrupt per packet livelocks the CPU at 10Gbps+.
  - The NAPI solution: hardware IRQ fires → driver disables IRQ → schedules `softirq` → polls RX ring descriptors in batches (budget = 64) → re-enables IRQ.
  - DMA ring buffers: Coherent descriptor rings (`dma_alloc_coherent`) vs streaming payload mapping (`dma_map_single`).
  - Anatomy and lifetime of `struct sk_buff`: headroom reservation (`skb_reserve`), push/put/pull operations, linear vs fragmented buffers (`skb_shinfo`), and `skb_clone` vs `skb_copy` reference counting.
  - Ownership semantics: `kfree_skb()` (drop/error path) vs `consume_skb()`.
  - **Evidence Artifact:** ftrace call graph showing `napi_schedule()` → driver `poll()` → `napi_gro_receive()`, and bpftrace trace of `skb->users` reference counts.
  - **Algorithm Extraction Link:** Share your mock circular DMA ring buffer with hardware ownership flags and an intrusive packet buffer in C with headroom reservation.

#### Chapter M2 — The Interface Zoo & The XDP Fast Path
* **Post Title:** *Bypassing the Linux Kernel Networking Stack: 10 Million Packets/Sec with 15 Lines of XDP*
* **What to Document:**
  - Synthetic network interfaces: when to use `veth`, `bridge`, `dummy`, and `macvlan`.
  - The latency cost of the standard kernel stack: `sk_buff` allocation, Netfilter traversal, and socket queues.
  - In-driver eXpress Data Path (XDP): executing eBPF directly in the driver RX ring on raw DMA frames before `sk_buff` allocation.
  - Benchmark comparison: Throughput and CPU saturation of `XDP_DROP` vs `iptables -j DROP`.
  - **Evidence Artifact:** Graph and benchmark data comparing XDP early drop vs iptables packet drop rates under synthetic load.
  - **Algorithm Extraction Link:** Share your standalone packet parser and filter in C operating on raw linear packet buffers.

#### Chapter M3 — Routing & The FIB Trie
* **Post Title:** *How the Linux Kernel Routes Millions of Packets per Second: The Longest-Prefix-Match (LPM) Trie*
* **What to Document:**
  - Why routing table lookup cannot use standard hash maps (CIDR subnet masks like `/24` require prefix matching).
  - The structure of `net/ipv4/fib_trie.c`: bitwise trie traversal.
  - Route caching and neighbor table resolution (ARP/ND).
  - **Evidence Artifact:** An annotated `fib_trie` dump from `/proc/net/fib_triestat` comparing table depth vs lookup speed.
  - **Algorithm Extraction Link:** Share your bitwise IPv4 CIDR routing trie implemented in C.

#### Chapter M5 — TCP Congestion Control
* **Post Title:** *BBR vs CUBIC on a Lossy Link: Tracing Congestion Window Collapse with ftrace*
* **What to Document:**
  - The TCP state machine: slow start, congestion avoidance, fast retransmit, and recovery.
  - Loss-based congestion control (CUBIC) vs bottleneck-bandwidth-round-trip control (BBR).
  - Setting up a lossy network namespace using `tc qdisc add dev veth0 root netem loss 5%`.
  - **Evidence Artifact:** An annotated graph or ftrace plot showing `snd_cwnd` (congestion window) collapses under CUBIC vs steady throughput under BBR.

#### Chapter T6c — Driver Observability with `ethtool`
* **Post Title:** *The Secret Knobs Inside Your Network Driver: Tuning Ring Buffers and Offloads with `ethtool`*
* **What to Document:**
  - What `ip` and `ss` cannot see: driver descriptor rings and ASIC counters.
  - Inspecting and adjusting hardware ring sizes: `ethtool -g eth0`.
  - Verifying hardware offloads: `ethtool -k eth0` (TSO, GSO, checksum offload).
  - Reading raw ASIC drop counters directly from `struct ethtool_ops`: `ethtool -S eth0`.
  - **Evidence Artifact:** Terminal transcript demonstrating an overflow in driver FIFO buffers resolved by tuning ring descriptors.

---

## 4. How to Structure Your Public GitHub Portfolio

Create a dedicated public repository (e.g., `github.com/<yourname>/linux-kernel-journey`):

```text
├── README.md                  # High-level index with links to all blog posts & evidence
├── evidence/                  # Raw termlearn evidence dossiers
│   ├── T0A/                   # Captured transcripts, environment.json, manifest.json
│   ├── A1/
│   ├── A2/
│   └── ...
├── algorithms/                # Standalone, unit-tested C extraction implementations
│   ├── 01_intrusive_list/     # struct list_head + container_of() + tests + Makefile
│   ├── 02_lockless_ringbuf/   # Power-of-2 circular buffer + tests + Makefile
│   ├── 03_lru_cache/          # Buffer cache hash + circular LRU
│   ├── 04_buddy_allocator/    # Binary buddy allocator
│   └── 05_lpm_trie/           # IPv4 CIDR longest-prefix-match trie
└── writeups/                  # Markdown source files for your blog / LinkedIn posts
    ├── 2027-01-00-boot-0.11.md
    ├── 2027-02-00-sched-decay.md
    └── ...
```

---

## 5. Summary Checklist Before Publishing Any Post

Before you hit publish on LinkedIn, Substack, or Hashnode, verify:

- [ ] Does the post start with a specific technical hook instead of personal diary prose?
- [ ] Is there an exact pinned kernel source file or commit cited?
- [ ] Is there a visual or empirical artifact (diagram, GDB transcript, ftrace graph, `pahole` output)?
- [ ] Does the post describe what happened when you changed a parameter or introduced a bug?
- [ ] If applicable, is there a link to a clean, runnable, unit-tested C implementation on GitHub?
- [ ] Are relevant technical keywords tagged naturally (`#LinuxKernel`, `#SystemsProgramming`, `#DeviceDrivers`, `#C`, `#PCIe`, `#Debugging`)?

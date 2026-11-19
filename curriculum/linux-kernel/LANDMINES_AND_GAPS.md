# Kernel Curriculum Maintainer Directives: Landmines & Plan Gaps

## 1. Pedagogical Landmines to Avoid

### Landmine A: The 0.11 Toolchain / Environment Sinkhole
Linux 0.11 was written for an 80386 on a Minix host with GCC 1.40 and a.out binaries. If you try to build pristine 0.11 with a modern GCC 13+ ELF toolchain, inline assembly will break, register constraints will misbehave, and section layouts will corrupt.

* **The Trap:** Spending three weeks debugging 1991 gas syntax errors instead of studying operating systems.
* **Maintainer Rule:** You have `sources/Linux-0.11-fork` in your tree—stick to it. 0.11 is a pedagogical vehicle for understanding the x86 real-to-protected mode transition (`setup.s` → `head.s`), TSS-based task switching, and primitive paging. The moment build fiddling takes more than an hour, fall back to the runnable fork or QEMU disk image.

### Landmine B: Modern Build Iteration Latency (Phase D)
Building modern Linux (`x86_64_defconfig` or distro config) builds ~4,000 files, takes 20–40 minutes, and consumes 50GB of disk.

* **The Trap:** If your compile-boot-test loop takes 15 minutes, you will not tinker. You will hesitate to add printks or change sysctls.
* **Maintainer Rule:** Your modern build/boot cycle must be under 30 seconds.
  1. Use a stripped-down `tinyconfig` or `defconfig` with `make localmodconfig` (or a dedicated QEMU micro-config with `CONFIG_NET=y`, `CONFIG_INET=y`, `CONFIG_VETH=y`, virtio drivers, and no extraneous drivers).
  2. Use `virtme-ng` (listed in `T7a`) or QEMU with a Direct Kernel Boot (`-kernel arch/x86/boot/bzImage -append "console=ttyS0 root=/dev/root"`) mounting your host filesystem via 9p/virtiofs. Do not build full disk images for daily debugging.

### Landmine C: Loopback & Veth Illusion in the Networking Track
In M0 through M2, you trace loopback and veth. That is great because it requires zero hardware and zero root privilege if run inside network namespaces.

* **The Trap:** Loopback and veth bypass the real world. They execute in process context or immediate softirq without real DMA, hardware rings, interrupt moderation, or true NAPI polling loops. Learners often think `netif_rx()` is how modern NICs work.
* **Maintainer Rule:** Make sure M1/M2 explicitly contrasts synthetic software interfaces with real hardware driver flows. Spin up a virtual `e1000` or `virtio-net` in QEMU and trace `napi_gro_receive()` and the DMA buffer ring (`rx_ring` / `tx_ring`).

---

## 2. Critical Gaps to Patch in the Plan

### Gap 1: Concurrency, Locking, and Lockdep are Under-Represented
In 0.11, concurrency was trivial: `cli()` and `sti()` (disabling interrupts on a single-core 386 CPU). In 2.6 and modern Linux, concurrency is the kernel.

* Modern `net/` is almost entirely lockless on the fast path, held together by RCU (`rcu_read_lock`, `rcu_dereference`), per-CPU stats, and atomic operations.
* **Action:** In Phase C or D, add a dedicated block on concurrency primitives:
  * Spinlocks vs. mutexes (atomic context vs. sleeping context).
  * Bottom halves (`softirq`, `tasklets`, `workqueues`).
  * Lockdep (`CONFIG_PROVE_LOCKING`): Upstream maintainers will reject any patch that introduces a lockdep splat. Add lockdep inspection to `TOOLING.md`.

### Gap 2: Memory Accounting in Networking (sk_buff Lifetime)
You mention tracing an `sk_buff` through loopback, but the single hardest thing for developers touching `net/` is: *who owns the skb and where is it freed?*

* Cloning vs. copying (`skb_clone` vs `skb_copy`).
* Linear data vs. paged fragments (`skb_shinfo`, `skb_frag_t`).
* Socket buffer memory accounting: `sk_wmem_alloc`, `sk_rmem_alloc`, and TCP memory pressure thresholds.
* **Action:** In M1 or M4, add an explicit experiment on skb allocation, headroom reservation (`skb_reserve`), expansion (`skb_put` / `skb_push`), and freeing (`kfree_skb` vs `dev_kfree_skb_any`).

### Gap 3: BPF / XDP as an Alternative Data Path
In modern networking (Phase D / M7), Netfilter and traditional TC are increasingly supplemented or replaced by XDP (eXpress Data Path) and tc-bpf.

* Having T5 (`bpftrace` / eBPF) is great, but don't just use BPF for observability; introduce a 15-line XDP program in M2 or M7 that drops or redirects packets directly at the driver RX ring before an `sk_buff` is even allocated. It cements why `sk_buff` allocation overhead matters.

# Chapter A1 Generation Notes: Boot & First C (Linux 0.11)

## 1. Pinned Source & Empirical Evidence Mapping
Every block, lab, and quiz item traces directly to captured evidence artifacts:
- **E-A1-01**: Pinned git tag `0.11` at commit `b65b60f4acd7efbbccd3d2411e9e5bca520a7574` in `sources/early-history.git`. Confirms exactly 100 source files across 8 directories (boot, fs, include, init, kernel, lib, mm, tools).
- **E-A1-02**: Load constants and relocation assembly in `boot/bootsect.s` (`BOOTSEG=0x07c0`, `INITSEG=0x9000`, `SETUPSEG=0x9020`, `SYSSEG=0x1000`). Traces `rep movw` copying 256 words and `jmpi go, INITSEG`.
- **E-A1-03**: BIOS parameters, system relocation to `0x00000`, A20 gate keyboard controller commands (`0xD1` to port `0x64`, `0xDF` to port `0x60`), 8259 PIC remapping to `0x20-0x2F`, descriptor tables, and protected-mode transition (`lmsw ax; jmpi 0, 8`).
- **E-A1-04**: 32-bit segment reloading, 16MB identity paging (`pg_dir` at 0x0, 4 page tables at 0x1000-0x4000), `CR3=0x0`, `CR0.PG=1`, and `pushl $_main; ret` handoff.
- **E-A1-05**: C initialization in `init/main.c`: memory sizing (`memory_end = (1<<20) + (EXT_MEM_K<<10)`), buffer cache partitioning, driver initialization, `sti()`, `move_to_user_mode()`, and forking task 1 (`init`).
- **E-A1-06**: Unmodified GCC 16 build failure demonstrating `-Wimplicit-int` and prototype strictness.
- **E-A1-07**: Successful build under GCC 16 with `-std=gnu89 -m32 -fno-builtin -fno-stack-protector -fomit-frame-pointer`.
- **E-A1-08**: Artifact verification of DOS/MBR boot floppy `Image` and ELF kernel `tools/system`.
- **E-A1-09**: Live hypervisor GDB breakpoint trace at `init/main.c:107`, verifying `eip = 0x6771`, `esp = 0x27f70`, `eax = 0x80000013`, `cr0 = 0x80000013`, `cr3 = 0x00000000`.

## 2. Pedagogical Architecture
- **5-Job explain_md**: Every block covers 1. Frame Problem, 2. Notional Machine, 3. Source Walkthrough, 4. Failure Mode, 5. Mental Axiom.
- **Visuals**: Flowcharts for custody handoffs and pipelines; ASCII art for floppy sector geometry, real-mode math, and memory maps; ASCII memory step progressions for register states.
- **5 Labs**: Spanning repository auditing (`audit_tree.sh`), real-mode segmented address math (`real_mode_calc.c`), MBR sector validation (`validate_bootsector.c`), QEMU/GDB trapping (`trap_main.sh`), and page table walking (`page_walk.c`).
- **Balance**: Quiz items rigorously balanced across options {0: 11, 1: 11, 2: 11}.

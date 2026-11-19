# Authoring Notes for Chapter T1A

**Chapter ID:** T1A  
**Title:** T1a — QEMU, gdb, and architecture vocabulary  
**Target Audience:** Senior Kernel Maintainer pedagogical standard; terminal-native learners.  
**Source Ref:** `curriculum/linux-kernel/evidence/T1A/transcript.md; E-T1A-01..E-T1A-07`

## 1. Evidence-to-Block Mapping

| Evidence ID | Description | Primary Study Block | Quiz / Lab Use |
|-------------|-------------|---------------------|----------------|
| `E-T1A-01`  | `gdb 18.1` environment and installation verification | `b1` | General verification |
| `E-T1A-02`  | Debug build with `-std=c99 -Wall -Wextra -g -O0 debugme.c` | `b2` | Lab 1 compile contract |
| `E-T1A-03`  | Breakpoint on `socket_probe`, `bt`, `info locals`, `next`, `print doubled` ($1=14) | `b2`, `b3`, `b4`, `b5` | Lab 1 test case; Q14 |
| `E-T1A-04`  | Hardware watchpoint on `fd`: triggers on write (`old=0 -> new=7`), deleted on exit | `b6`, `b7` | Lab 2 contract; Q8, Q15 |
| `E-T1A-05`  | Stepping and stack navigation: `next`, `step`, `bt`, `finish` (value returned $1=14) | `b3` | Q2, Q20 |
| `E-T1A-06`  | Workload hash pinning (`debugme.c` sha256 `be53530d...`) | All blocks | Artifact integrity |
| `E-T1A-07`  | QEMU `-s -S` + GDB remote attachment to Linux 0.11 `main` (`eip=0x6771`, `eax=0x80000013`) | `b1`, `b8`, `b9`, `b10`, `b11`, `b12` | Lab 3; Q1, Q3, Q4, Q10 |

## 2. Idea Units Accounted For
- `b1`: Debugger execution model: ptrace syscall vs QEMU RSP stub over TCP. (Taught & Checked)
- `b2`: Fundamental controls: break, run, print /x, info registers, disassembly x/8i. (Taught & Checked)
- `b3`: Stack and flow: step (into), next (over), finish, backtrace, frame switching. (Taught & Checked)
- `b4`: Stepwise debug cycle: pre-condition check, doorstep pause, mutation, post-condition check. (Taught & Checked)
- `b5`: Architecture vocabulary: x86_64 ABI argument registers (RDI, RSI, RDX, RCX, R8, R9) vs 32-bit stack. (Taught & Checked)
- `b6`: Hardware data watchpoints: DR0-DR3 registers, watch, rwatch, awatch, scope deletion. (Taught & Checked)
- `b7`: Memory corruption diagnosis: buffer overrun trapping and backtrace attribution. (Taught & Checked)
- `b8`: Virtualization boundary: host userspace process vs virtual silicon vs guest OS. (Taught & Checked)
- `b9`: QEMU boot flags: -m 16M, -boot a, -fda, -hda, -display none, -s (1234), -S (freeze). (Taught & Checked)
- `b10`: Remote kernel attachment: loading symbols with file tools/system, target remote :1234, continue. (Taught & Checked)
- `b11`: Optimization realities: inlining, <optimized out>, software breakpoint (0xCC) vs hardware breakpoint (hbreak). (Taught & Checked)
- `b12`: Kernel entry milestone: main() entry disassembly, CR0 register bit decoding (0x80000013: PG, ET, MP, PE). (Taught & Checked)
- `b13`: Systems observation strategy: halting debuggers vs non-halting tracing (ftrace) under timing constraints. (Taught & Checked)

## 3. Code-Box and Source Disposition
- All kernel and GDB session excerpts are tagged `lang: text` or `lang: asm`.
- Userspace C examples are valid C99 with `main()` compiling cleanly with `gcc -Wall -Wextra`.
- No modern Linux source is read into 0.11 explanations except where explicitly marked as ABI contrast.

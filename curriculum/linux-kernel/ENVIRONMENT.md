# Environment

This is the working baseline for the curriculum. Re-check it before Phase A and
again before the networking track; kernels and tools change.

## Host baseline (checked November 2026)

| Item | State |
|------|-------|
| Working tree | `/home/pk/Apps/termlearn` |
| Kernel source snapshot | `/home/pk/linux-master` (about 1.8 GB) |
| Free disk | about 144 GB |
| Terminal | alacritty |
| `ip` | 7.3.0 |
| Present | `ss`, `tc`, `nft`, `iptables`, `bridge`, `unshare`, `strace`, `gdb`, `docker`, `python3`, `gcc`, `make` |
| Missing | `tcpdump`, `iperf3`, `ethtool`, `conntrack`, `bpftrace`, `perf`, `traceroute`, `socat` |
| QEMU | present: `qemu-system-i386` and `qemu-system-x86_64` 11.1.3 |
| Toolchain extras | present: `sparse`, `smatch`, `spatch` (Coccinelle 1.3.3), `pahole`, `cscope`, `clangd`; later check `b4`, `bpftool`, `drgn`, `crash`, `virtme-ng`, `syzkaller` |

Install the missing tools before the networking track. Package names vary:

```sh
# Debian/Ubuntu
sudo apt install tcpdump iperf3 ethtool conntrack traceroute socat \
  linux-tools-common linux-tools-generic bpftrace

# Arch
sudo pacman -S tcpdump iperf3 ethtool conntrack-tools traceroute socat \
  perf bpftrace
```

Also useful:

```sh
sudo apt install qemu-system-x86 qemu-system-arm bc bison flex libssl-dev \
  libelf-dev dwarves pahole bpftool trace-cmd cscope clangd

sudo apt install b4 sparse smatch coccinelle crash drgn virtme-ng
```

## Tool learning matrix

Tools are taught in T0a–T8 (`TOOLING.md`), not just installed. Each row is a
chapter with multiple labs. C reading and basic socket API vocabulary are
assumed; terminal, build, debug, and tracing tools are not.

| Chapter | Tools | What you must be able to do |
|---------|-------|-----------------------------|
| T0a | terminal, files, processes, gcc, make, git basics | Run, compile, inspect, and commit |
| T0b | grep/rg, cscope/clangd, git history | Find definitions, callers, and commits |
| T0c | Kconfig/Kbuild, modules, checkpatch, get_maintainer | Build, modify, and prepare a patch |
| T0d | nm, readelf, objdump, size, pahole | Inspect symbols, sections, layout, and types |
| T0e | sparse, smatch, coccinelle | Find and fix static issues |
| T0f | capstone workflow | Go from symptom to verified patch |
| T1a | QEMU, gdb, architecture vocabulary | Boot, break, inspect userspace and kernel |
| T1b | kgdb, crash, drgn | Post-mortem and live kernel introspection |
| T2 | strace | Trace, filter, and explain syscalls |
| T3 | ftrace, trace-cmd | Trace functions and events, filter, measure duration |
| T4 | perf | Measure CPU, scheduling, memory, and hardware events |
| T5 | bpftrace, bpftool, BTF, eBPF | Write probes, read maps, inspect BTF |
| T6a | ip, ss, ip netns, ip -s | Inspect address/link/route/namespace state |
| T6b | tc, nft, conntrack, nstat | Inspect qdisc, firewall, and counters |
| T6c | tcpdump, ethtool, iperf3, socat, traceroute | Capture, generate load, inspect link/path |
| T7a | kselftests, KUnit, virtme-ng | Run and write repeatable tests |
| T7b | syzkaller, stress-ng, fio, reproducer minimization | Fuzz, load, and reproduce |
| T8 | b4, lore, get_maintainer, checkpatch, syzbot | Prepare and review upstream patches |

A tool is not "learned" when the command runs. It is learned when you can
choose it from a symptom, read its output without a cheat sheet, and state what
it cannot observe.

## Privileges and deterministic output

Record the run conditions before each tool lab:

```sh
id
capsh --print 2>/dev/null || true
cat /proc/sys/kernel/perf_event_paranoid 2>/dev/null || true
ls -ld /sys/kernel/tracing /sys/kernel/debug 2>/dev/null || true
```

Expected requirements:

| Tool group | Requirement | Fallback |
|------------|-------------|----------|
| T2 strace | ptrace permission | Userspace-only trace; same-user process |
| T3 ftrace | root or tracing group | QEMU guest with tracing enabled |
| T4 perf | `perf_event_paranoid` and symbols | `perf stat` software events; ftrace |
| T5 bpftrace | CAP_BPF/CAP_PERFMON/root plus BTF | `bpftool feature`; skip with recorded reason |
| T6a netns | `CAP_NET_ADMIN` in a new user namespace | QEMU guest |
| T1b crash/drgn | matching `vmlinux` and debuginfo | QEMU panic artifact with saved `vmlinux` |

Output rules:

- Normalize timestamps, durations, CPU IDs, and addresses before diffing.
- Prefer `contains`/regex expectations over full-trace equality.
- Filter a tool to one PID, interface, event, or function before capturing.
- Record tool versions beside raw output; ftrace/perf/bpftrace formats change.
- Every lab states cleanup explicitly.

## Evidence capture environment

Evidence bundles must record the environment that produced them. Capture this
once per authoring session and again when a tool or kernel version changes:

```sh
uname -a
cat /etc/os-release
git --version
gcc --version
make --version
gdb --version
strace --version 2>/dev/null || strace -V
qemu-system-i386 --version
ip -V
```

For kernel chapters also record the exact commit or tag, tree hash, config, and
whether the source is pristine or a runnable fork. For privileged labs record
the capability mode and fallback used. Store the result in
`evidence/<chapter>/environment.json` and reference it from the chapter's
evidence manifest.

## Kernel modules and namespaces

The running kernel exposes the modules needed for the networking track:

| Feature | State |
|---------|-------|
| `NET_NS` | built in (`y`) |
| `VETH` | module (`m`) |
| `DUMMY` | module (`m`) |
| `TUN` | module (`m`) |
| `VXLAN` | module (`m`) |
| `GENEVE` | module (`m`) |
| `BRIDGE` | module (`m`) |
| `VLAN_8021Q` | module (`m`) |
| `MACVLAN` | module (`m`) |
| `IPVLAN` | module (`m`) |
| unprivileged user namespaces | enabled |

Check:

```sh
grep -E 'CONFIG_(NET_NS|VETH|DUMMY|TUN|VXLAN|GENEVE|BRIDGE|VLAN_8021Q|MACVLAN|IPVLAN)=' /boot/config-$(uname -r)
sysctl kernel.unprivileged_userns_clone 2>/dev/null || true
ip netns list
```

Do not load modules blindly. Prefer network namespaces and existing modules.
If a module is missing, note it and use a QEMU guest or a different interface
type for that experiment.

## Old-kernel toolchains

Modern gcc often fails on 0.11–2.4 code. Options, in order of preference:

1. Use the runnable 0.11 fork for boot labs.
2. Use a Docker image from the era (`gcc:4.9`, `debian:stretch`,
   `debian:buster`) with `-m32` and the required 32-bit libs.
3. Use `qemu-system-i386` with a prebuilt image.
4. Only patch the build system when the alternative is not studying the kernel.

Do not spend a week making 0.11 compile with gcc 14. The lesson is the code, not
the build system.

## QEMU

Recommended guest settings:

```sh
qemu-system-x86_64 -m 2G -smp 2 -kernel arch/x86/boot/bzImage \
  -append "console=ttyS0 root=/dev/sda rw" \
  -drive file=rootfs.img,format=raw \
  -nographic -no-reboot
```

For 0.11:

```sh
qemu-system-i386 -m 16M -boot a -fda Image -hda hdc-0.11.img
```

For debugging, add `-s -S` and connect gdb:

```sh
gdb vmlinux
(gdb) target remote :1234
(gdb) hbreak start_kernel
(gdb) continue
```

## Network lab safety

- Use `ip netns` or `unshare -n` for interface, route, qdisc, and netfilter
  experiments.
- Never flush the host's rules or routes as a first step.
- Keep one shell outside the namespace and one inside.
- Use `ip -n <ns>` rather than `sudo` where possible.
- Clean up with `ip netns del <ns>`; veth peers disappear with the namespace.
- For VXLAN/GENEVE/GRE, run both endpoints in namespaces connected by veth.

The helper `scripts/netlab.sh` creates a small namespace:

```sh
scripts/netlab.sh up
ip netns exec tl sh
scripts/netlab.sh down
```

## Terminal handoff for tinker commands

Termlearn can open interactive commands in a separate terminal:

```sh
export TERMLEARN_TINKER_TERMINAL="alacritty -e"
```

Detection order:

1. `TERMLEARN_TINKER_TERMINAL`
2. `tmux new-window` when `TMUX` is set
3. `alacritty -e` when alacritty and a display are available
4. suspend the TUI and run in the current terminal

Useful variants:

```sh
export TERMLEARN_TINKER_TERMINAL="alacritty -e"
export TERMLEARN_TINKER_TERMINAL="kitty"
export TERMLEARN_TINKER_TERMINAL="xterm -e"
export TERMLEARN_TINKER_TERMINAL="tmux new-window"
```

## Verification checklist

Run before starting a phase:

```sh
uname -a
gcc --version | head -1
ip -V
ss -V
tc -V
qemu-system-x86_64 --version | head -1
docker --version
python3 --version
```

Record the output in the phase journal. When a tool is missing, write the
fallback you will use instead of silently skipping the observation.

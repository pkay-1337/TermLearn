# Sources and Version Map

This file records where each kernel version comes from and how to get a
continuous history from 0.10 to today.

## Version timeline

| Version | Date | Why it matters | Source |
|---------|------|----------------|--------|
| 0.01 | Sep 1991 | The original; readable, not runnable | Historic tarball |
| 0.10 | 1991 | First tag in the pre-git history | `history/history.git` |
| 0.11 | Dec 1991 | Small, bootable with a modern fork | Tarball + runnable fork |
| 0.12 | Jan 1992 | Slightly more complete | Tarball |
| 0.95–0.99 | 1992 | The shape of 1.0 appears | `history/history.git` |
| 1.0 | Mar 1994 | First stable-ish release | Tag/tarball |
| 1.2 | Mar 1995 | Modules, more drivers, early net | Tag/tarball |
| 2.0 | Jun 1996 | SMP, modern driver model | Tag/tarball |
| 2.2 | Jan 1999 | Better networking and VM | Tag/tarball |
| 2.4 | Jan 2001 | Long-lived enterprise kernel | Tag/tarball |
| 2.6 | Dec 2003 | The modern skeleton | Tag/tarball |
| 2.6.12 | Jun 2005 | First commit in `torvalds/linux` | Git |
| 6.18 | 2025–2026 | Current LTS line | Git/tarball |
| 7.3 | 2026 | Current stable line | Git/tarball |

As of November 2026: mainline is `7.4-rc3`, stable is `7.3.5`, and LTS lines
include `6.18.64` and `6.12.118`. Treat these as moving targets; pin the exact
version in your notes.

## Evidence for kernel chapters

For kernel chapters, the source of truth is the **pinned tree plus observed
behavior**, not memory, blog posts, or modern source read while studying an old
version. The creator must actually open the source at the version being taught.
When the chapter claims runtime behavior, the creator must also run the relevant
build, boot, trace, debug, or namespace experiment before drafting.

Each kernel chapter records:

- exact version, tag, or commit and the tree hash;
- exact file paths and line ranges read from that tree;
- extracted source snippets with `commit:path:line-range`;
- file hashes for tarballs or forks used instead of git;
- kernel config and tool versions for runtime observations;
- raw build/boot/gdb/ftrace/perf/`ip`/`ss` output with command boundaries;
- a clear separation between pristine source and runnable forks such as the
  modernized 0.11 tree.

Capture source evidence with commands like:

```sh
git rev-parse <tag>^{commit} <tag>^{tree}
git show <tag>:init/main.c | nl -ba | sed -n '480,540p'
git blame -L 480,540 <tag> -- init/main.c
sha256sum sources/linux-0.11.tar.gz
uname -a
cat /etc/os-release
gcc --version
qemu-system-i386 --version
```

Store the output in `evidence/<chapter>/source/` and
`evidence/<chapter>/environment.json`. Give each item an ID such as `E-A1-02`
and cite it from the chapter draft.

Rules:

- Never invent a function name, line number, struct field, or config symbol.
- If a symbol is not present in the pinned tree, say so and record the search
  command.
- Do not use a modern tree to explain an early-kernel chapter. If a modern
  comparison is useful, mark it as a separate, explicitly versioned evidence
  item.
- Man pages and `Documentation/` are supporting context, not proof of what the
  pinned source does.
- If runtime behavior cannot be reproduced, the lab is not authored until the
  environment is fixed or the claim is removed.

## Git topology

- `torvalds/linux` begins at commit `1da177e4c3f41524e886b7f1b8a0c1fc7321cac2`
  ("Linux-2.6.12-rc2", 2005-04-16). It has no parent in that repository.
- `tglx/history` ends at `e7e173af42dbf37b1d946f9ee00219cb3b2bea6a`, whose tree
  is `0bba044c4ce775e45a88a51686b5d9f90697ea9d`.
- `1da177e4` has the same tree, so grafting `e7e173af` as its parent produces a
  continuous history.
- `history/history.git` contains tags from `0.10` onward, including `0.11`,
  `0.12`, and the `0.95`–`0.99` line.

Sanity check after grafting:

```sh
git rev-parse 1da177e4c3f41524e886b7f1b8a0c1fc7321cac2^{tree}
git rev-parse e7e173af42dbf37b1d946f9ee00219cb3b2bea6a^{tree}
```

Both must print `0bba044c4ce775e45a88a51686b5d9f90697ea9d`.

## Fetch everything

The helper `scripts/fetch-sources.sh` downloads the tarballs. The helper
`scripts/graft-history.sh` clones the git repositories and creates the graft.

Manual equivalent:

```sh
mkdir -p sources && cd sources

git clone --filter=blob:none https://github.com/torvalds/linux.git linux.git
cd linux.git
git remote add tglx https://git.kernel.org/pub/scm/linux/kernel/git/tglx/history.git
git fetch --filter=blob:none tglx
git replace --graft 1da177e4c3f41524e886b7f1b8a0c1fc7321cac2 e7e173af42dbf37b1d946f9ee00219cb3b2bea6a
git log --oneline --reverse | head
```

To get the earliest tags in a separate clone:

```sh
git clone --filter=blob:none https://git.kernel.org/pub/scm/linux/kernel/git/history/history.git early-history.git
cd early-history.git
git tag | sort -V | head -30
git checkout 0.11
```

Notes:

- `git replace` is local; it is not pushed. Use `git --no-replace-objects` if
  you need the original view.
- A blobless clone is much smaller than a full clone but still downloads blobs
  on demand. Budget several GB for a full history.
- The graft is a convenience, not a rewrite. It does not change commit hashes.

## Tarballs

Historic kernels:

```sh
https://mirrors.edge.kernel.org/pub/linux/kernel/Historic/linux-0.01.tar.gz
https://mirrors.edge.kernel.org/pub/linux/kernel/Historic/old-versions/linux-0.11.tar.gz
https://mirrors.edge.kernel.org/pub/linux/kernel/Historic/old-versions/linux-0.12.tar.gz
https://mirrors.edge.kernel.org/pub/linux/kernel/Historic/old-versions/linux-0.95.tar.gz
https://mirrors.edge.kernel.org/pub/linux/kernel/Historic/old-versions/linux-0.95a.tar.gz
https://mirrors.edge.kernel.org/pub/linux/kernel/Historic/old-versions/linux-0.96a.tar.gz
https://mirrors.edge.kernel.org/pub/linux/kernel/Historic/old-versions/linux-0.96b.tar.gz
https://mirrors.edge.kernel.org/pub/linux/kernel/Historic/old-versions/linux-0.96c.tar.gz
https://mirrors.edge.kernel.org/pub/linux/kernel/Historic/old-versions/old/linux-0.97.tar.gz
https://mirrors.edge.kernel.org/pub/linux/kernel/Historic/old-versions/tytso/linux-0.10.tar.gz
```

Use `history/history.git` for tags beyond the available tarballs.
Modern tarballs:

```sh
https://mirrors.edge.kernel.org/pub/linux/kernel/v2.6/linux-2.6.12.tar.gz
https://mirrors.edge.kernel.org/pub/linux/kernel/v6.x/linux-6.18.64.tar.xz
https://mirrors.edge.kernel.org/pub/linux/kernel/v7.x/linux-7.3.5.tar.xz
```

Verify against `sha256sums.asc` in the same directory. Do not trust a mirror
without a checksum or signature.

## Runnable 0.11

Pristine 0.11 does not build with a modern toolchain. For boot labs, use a
modernized fork such as:

```sh
https://github.com/yuan-xy/Linux-0.11
```

This fork exists to build and boot under QEMU. Read the pristine tarball when
you are studying the original code; use the fork when you need a running
system. Record which one you used in the journal.

Typical boot command after building the fork:

```sh
qemu-system-i386 -m 16M -boot a -fda Image -hda hdc-0.11.img
```

## Space and time

| Item | Approximate size |
|------|------------------|
| `linux-master` snapshot | 1.8 GB |
| Blobless `torvalds/linux` clone | 1–2 GB |
| Full history with blobs | 5+ GB |
| Old tarballs (0.01–0.99) | tens of MB |
| Modern tarball | ~150–250 MB compressed |
| Built kernel tree | 2–10 GB depending on config |

Keep `sources/` and `build/` out of git; keep notes and diffs in git.

## Source-reading shortcuts

```sh
git log --oneline -S 'function_name' -- path/
git log -p --follow path/file.c
git blame -L start,end path/file.c
git show v6.18:net/core/dev.c | less
git grep -n 'symbol' v6.18 -- net/
```

For the local modern tree, `cscope` or `clangd` with `compile_commands.json`
beats `grep` once you are past the early phases.

## Tool documentation

Use the docs that ship with the version you are studying:

| Tool | Where to read |
|------|---------------|
| strace | `man strace`, `strace -h`, upstream `strace` README |
| gdb | `man gdb`, `info gdb`, GDB manual |
| QEMU | `qemu-system-x86_64 -help`, QEMU documentation |
| ftrace | `Documentation/trace/` in the kernel tree |
| perf | `tools/perf/Documentation/`, `perf help` |
| bpftrace | `man bpftrace`, `bpftrace -l`, bpftrace reference guide |
| bpftool | `tools/bpf/bpftool/Documentation/`, `bpftool help` |
| network tools | `man ip`, `man ss`, `man tc`, `man nft`, `man tcpdump` |
| testing | `tools/testing/selftests/`, `Documentation/dev-tools/` |
| upstream | `Documentation/process/`, `b4 --help`, lore.kernel.org |

The local `linux-master/Documentation/` tree is often more current than a blog
post. Read the version that matches the kernel you are running.

#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
src=${1:-"$root/sources/linux.git"}

if [ ! -d "$src" ]; then
  printf 'no source dir: %s\n' "$src" >&2
  printf 'run scripts/graft-history.sh or fetch a modern tarball first\n' >&2
  exit 1
fi

make -C "$src" defconfig
make -C "$src" -j"$(nproc)"
printf 'built %s\n' "$src"

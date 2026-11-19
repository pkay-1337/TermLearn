#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
src="$root/sources/linux-0.11-runnable"

if [ ! -f "$src/Image" ]; then
  printf 'no %s/Image; run scripts/build-0.11.sh first\n' "$src" >&2
  exit 1
fi

cd "$src"
exec qemu-system-i386 -m 16M -boot a -fda Image -hda hdc-0.11.img "$@"

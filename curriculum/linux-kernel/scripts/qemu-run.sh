#!/bin/sh
set -eu
if [ $# -lt 1 ]; then
  printf 'usage: %s <bzImage> [qemu args...]\n' "$0" >&2
  exit 2
fi

bzimage=$1
shift

exec qemu-system-x86_64 \
  -m "${MEM:-1G}" \
  -kernel "$bzimage" \
  -append "console=ttyS0 ${CMDLINE:-}" \
  -nographic \
  -no-reboot \
  "$@"

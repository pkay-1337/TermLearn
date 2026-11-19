#!/bin/sh
set -eu
if [ $# -lt 1 ]; then
  printf 'usage: %s <source-dir> [docker-image]\n' "$0" >&2
  exit 2
fi

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
src=$1
case "$src" in
  /*) ;;
  *) src="$root/sources/$src" ;;
esac
image=${2:-${IMAGE:-debian:bookworm}}

if [ ! -d "$src" ]; then
  printf 'no source dir: %s\n' "$src" >&2
  exit 1
fi

docker run --rm -v "$src:/src" -w /src "$image" sh -c '
  apt-get update
  apt-get install -y build-essential bc bison flex libssl-dev libelf-dev
  make defconfig
  make -j"$(nproc)"
'

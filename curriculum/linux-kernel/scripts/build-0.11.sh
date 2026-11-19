#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
src="$root/sources/linux-0.11-runnable"
mkdir -p "$root/sources"

if [ ! -d "$src/.git" ]; then
  git clone --depth 1 https://github.com/yuan-xy/Linux-0.11.git "$src"
fi

cd "$src"
make
printf 'built %s\n' "$src"

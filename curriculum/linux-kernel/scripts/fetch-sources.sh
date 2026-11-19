#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
src="$root/sources"
mkdir -p "$src"
cd "$src"

fetch() {
  url=$1
  out=$2
  if [ -f "$out" ]; then
    printf 'have %s\n' "$out"
    return 0
  fi
  printf 'fetching %s\n' "$out"
  if command -v curl >/dev/null 2>&1; then
    curl -fL --retry 3 -o "$out" "$url"
  else
    wget -O "$out" "$url"
  fi
}

base=https://mirrors.edge.kernel.org/pub/linux/kernel/Historic
old=$base/old-versions

fetch "$base/linux-0.01.tar.gz" "linux-0.01.tar.gz"
for v in 0.11 0.12 0.95 0.95a 0.96a 0.96b 0.96c; do
  fetch "$old/linux-$v.tar.gz" "linux-$v.tar.gz"
done
fetch "$old/old/linux-0.97.tar.gz" "linux-0.97.tar.gz"
fetch "$old/tytso/linux-0.10.tar.gz" "linux-0.10.tar.gz"

fetch "https://mirrors.edge.kernel.org/pub/linux/kernel/v2.6/linux-2.6.12.tar.gz" "linux-2.6.12.tar.gz"
fetch "https://mirrors.edge.kernel.org/pub/linux/kernel/v6.x/linux-6.18.64.tar.xz" "linux-6.18.64.tar.xz"
fetch "https://mirrors.edge.kernel.org/pub/linux/kernel/v7.x/linux-7.3.5.tar.xz" "linux-7.3.5.tar.xz"

printf 'sources in %s\n' "$src"

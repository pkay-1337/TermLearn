#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
src="$root/sources"
mkdir -p "$src"
cd "$src"

if [ ! -d linux.git ]; then
  git clone --filter=blob:none https://github.com/torvalds/linux.git linux.git
fi

cd linux.git
if ! git remote | grep -qx tglx; then
  git remote add tglx https://git.kernel.org/pub/scm/linux/kernel/git/tglx/history.git
fi
git fetch --filter=blob:none tglx

first=1da177e4c3f41524e886b7f1b8a0c1fc7321cac2
parent=e7e173af42dbf37b1d946f9ee00219cb3b2bea6a
if ! git replace -l | grep -q "$first"; then
  git replace --graft "$first" "$parent"
fi

printf 'first tree:  '
git rev-parse "$first^{tree}"
printf 'parent tree: '
git rev-parse "$parent^{tree}"
git log --oneline --reverse | head

cd "$src"
if [ ! -d early-history.git ]; then
  git clone --filter=blob:none https://git.kernel.org/pub/scm/linux/kernel/git/history/history.git early-history.git
fi
cd early-history.git
git tag | sort -V | head -30

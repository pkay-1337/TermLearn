#!/bin/sh
set -eu
ns=${NS:-tl-tinker-$$}
cleanup() {
  ip netns del "$ns" 2>/dev/null || true
}
trap cleanup EXIT INT TERM
ip netns add "$ns"
ip -n "$ns" link set lo up
printf 'namespace: %s\n' "$ns"
printf 'try: ip -n %s link show\n' "$ns"
printf 'try: ip netns exec %s sh\n' "$ns"
ip netns exec "$ns" sh

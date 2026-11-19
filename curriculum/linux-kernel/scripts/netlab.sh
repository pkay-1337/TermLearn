#!/bin/sh
set -eu
ns=${NS:-tl}
cmd=${1:-up}

case "$cmd" in
  up)
    ip netns add "$ns" 2>/dev/null || true
    ip -n "$ns" link set lo up
    printf 'namespace %s ready\n' "$ns"
    printf 'enter: ip netns exec %s sh\n' "$ns"
    ;;
  down)
    ip netns del "$ns" 2>/dev/null || true
    printf 'namespace %s removed\n' "$ns"
    ;;
  status)
    ip netns list
    ;;
  *)
    printf 'usage: %s [up|down|status]\n' "$0" >&2
    exit 2
    ;;
esac

#!/bin/sh
set -eu
test -f observed.txt
grep -q "expected observation" observed.txt
printf 'ok\n'

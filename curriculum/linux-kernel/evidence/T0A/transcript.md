# T0A evidence transcript

Captured 2026-11-19. Raw stdout/stderr and exit codes below.

## Environment

```text
$ uname -a
Linux pkay 6.18.63-2-lts #1 SMP PREEMPT_DYNAMIC Wed, 11 Nov 2026 19:03:11 +0000 x86_64 GNU/Linux
$ cat /etc/os-release
NAME="Arch Linux"
PRETTY_NAME="Arch Linux"
ID=arch
BUILD_ID=rolling
ANSI_COLOR="38;2;23;147;209"
HOME_URL="https://archlinux.org/"
DOCUMENTATION_URL="https://wiki.archlinux.org/"
SUPPORT_URL="https://bbs.archlinux.org/"
BUG_REPORT_URL="https://gitlab.archlinux.org/groups/archlinux/-/issues"
PRIVACY_POLICY_URL="https://terms.archlinux.org/docs/privacy-policy/"
LOGO=archlinux-logo
$ git --version
git version 2.56.1
$ id -u && id -un
1000
pk
```

## Build workload

cwd: `/home/pk/Apps/termlearn/curriculum/linux-kernel/evidence/T0A/artifacts/workload`

```text
$ pwd
/home/pk/Apps/termlearn/curriculum/linux-kernel/evidence/T0A/artifacts/workload
$ gcc --version
gcc (GCC) 16.2.1 20260810
Copyright (C) 2026 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

$ make --version
GNU Make 4.4.1
Built for x86_64-pc-linux-gnu
Copyright (C) 1988-2023 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
$ gcc -std=c99 -Wall -Wextra -g main.c -o app
[exit=0]
$ ./app
5
[exit=0]
$ gcc -std=c99 -Wall -Wextra -g bad.c -o bad
bad.c: In function ‘main’:
bad.c:6:5: error: expected ‘,’ or ‘;’ before ‘printf’
    6 |     printf("%d\n", x)
      |     ^~~~~~
bad.c:8:1: error: expected declaration or statement at end of input
    8 | }
      | ^
bad.c:5:9: warning: unused variable ‘x’ [-Wunused-variable]
    5 |     int x = 1
      |         ^
[exit=1]
$ make clean
rm -f app
[exit=0]
$ make
gcc -std=c99 -Wall -Wextra -g main.c -o app
[exit=0]
$ size app
   text	   data	    bss	    dec	    hex	filename
   1502	    584	      8	   2094	    82e	app
[exit=0]
```

## Workload hashes

```text
$ sha256sum evidence/T0A/artifacts/workload/main.c evidence/T0A/artifacts/workload/Makefile evidence/T0A/artifacts/workload/bad.c
4609b9dc684c628dd18eda949aa5295672565e5654f42fd5d8dc311f3d0088ed  evidence/T0A/artifacts/workload/main.c
5310797b9d5c4fe17bf02cf68a0717fe3c4dd71428ab8e152364df38d022c11a  evidence/T0A/artifacts/workload/Makefile
afe9f17e0dbf57160a7cb46565cf72c6746189c7affccb96e70dca246e1bb077  evidence/T0A/artifacts/workload/bad.c
```

## Git workload

cwd: `/tmp/opencode/t0a-git`

```text
$ pwd
/tmp/opencode/t0a-git
$ git init -q
[exit=0]
$ git status --short
?? hello.c
[exit=0]
$ git add hello.c
[exit=0]
$ git status --short
A  hello.c
[exit=0]
$ git -c user.name=Evidence -c user.email=evidence@example.invalid commit -m "add hello"
[master (root-commit) f71d88d] add hello
 1 file changed, 4 insertions(+)
 create mode 100644 hello.c
[exit=0]
$ git log --oneline
f71d88d add hello
[exit=0]
$ git status --short
[exit=0]
$ git status --short
 M hello.c
[exit=0]
$ git diff
diff --git a/hello.c b/hello.c
index 58fe692..2cecef0 100644
--- a/hello.c
+++ b/hello.c
@@ -1,4 +1,4 @@
 int main(void)
 {
-    return 0;
+    return 1;
 }
[exit=0]
$ git diff --stat
 hello.c | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
[exit=0]
```

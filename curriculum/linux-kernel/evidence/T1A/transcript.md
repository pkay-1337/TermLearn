# T1A evidence transcript

Captured 2026-11-19. Raw stdout/stderr and exit codes below.
Addresses, process IDs and BuildID values are volatile.

## Environment

```text
$ gdb --version
GNU gdb (GDB) 18.1
Copyright (C) 2026 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
$ id -u && id -un
1000
pk
```

## Userspace workload

cwd: `/home/pk/Apps/termlearn/curriculum/linux-kernel/evidence/T1A/artifacts/workload`

```text
$ pwd
/home/pk/Apps/termlearn/curriculum/linux-kernel/evidence/T1A/artifacts/workload
$ gcc -std=c99 -Wall -Wextra -g -O0 debugme.c -o debugme
[exit=0]
$ file debugme
debugme: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=bb3bae3fe9c91fc26baa467ed36412794448f9f5, for GNU/Linux 4.4.0, with debug_info, not stripped
[exit=0]
```

## Breakpoint, backtrace, locals, next, continue

```text
$ gdb -q -batch -ex "set debuginfod enabled off" -ex "set pagination off" -ex "break socket_probe" -ex "run" -ex "bt" -ex "frame 0" -ex "info locals" -ex "print fd" -ex "print doubled" -ex "next" -ex "print doubled" -ex "continue" ./debugme
Breakpoint 1 at 0x1144: file debugme.c, line 5.
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/libthread_db.so.1".

Breakpoint 1, socket_probe (fd=7) at debugme.c:5
5	    int doubled = fd * 2;
#0  socket_probe (fd=7) at debugme.c:5
#1  0x0000555555555186 in main () at debugme.c:13
#0  socket_probe (fd=7) at debugme.c:5
5	    int doubled = fd * 2;
doubled = 0
$1 = 7
$2 = 0
6	    printf("probe fd=%d doubled=%d\n", fd, doubled);
$3 = 14
probe fd=7 doubled=14
result=14
[Inferior 1 (process 151076) exited normally]
[exit=0]
```

## Hardware watchpoint

```text
$ gdb -q -batch -ex "set debuginfod enabled off" -ex "set pagination off" -ex "break main" -ex "run" -ex "watch fd" -ex "continue" -ex "info locals" -ex "print fd" -ex "continue" ./debugme
Breakpoint 1 at 0x1175: file debugme.c, line 12.
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/libthread_db.so.1".

Breakpoint 1, main () at debugme.c:12
12	    int fd = 7;
Hardware watchpoint 2: fd

Hardware watchpoint 2: fd

Old value = 0
New value = 7
main () at debugme.c:13
13	    int result = socket_probe(fd);
fd = 7
result = 0
$1 = 7

Watchpoint 2 deleted because the program has left the block in
which its expression is valid.
0x00007ffff7c27781 in ?? () from /usr/lib/libc.so.6
[exit=0]
```

## List, step, finish

```text
$ gdb -q -batch -ex "set debuginfod enabled off" -ex "set pagination off" -ex "break main" -ex "run" -ex "list" -ex "next" -ex "next" -ex "step" -ex "bt" -ex "finish" -ex "print result" ./debugme
Breakpoint 1 at 0x1175: file debugme.c, line 12.
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/libthread_db.so.1".

Breakpoint 1, main () at debugme.c:12
12	    int fd = 7;
7	    return doubled;
8	}
9	
10	int main(void)
11	{
12	    int fd = 7;
13	    int result = socket_probe(fd);
14	    printf("result=%d\n", result);
15	    return 0;
16	}
13	    int result = socket_probe(fd);
14	    printf("result=%d\n", result);
15	    return 0;
#0  main () at debugme.c:15
$1 = 14
"finish" not meaningful in the outermost frame.
[exit=0]

$ gdb -q -batch -ex "set debuginfod enabled off" -ex "set pagination off" -ex "break main" -ex "run" -ex "next" -ex "step" -ex "bt" -ex "finish" -ex "print result" ./debugme
Breakpoint 1 at 0x1175: file debugme.c, line 12.
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/libthread_db.so.1".

Breakpoint 1, main () at debugme.c:12
12	    int fd = 7;
13	    int result = socket_probe(fd);
socket_probe (fd=7) at debugme.c:5
5	    int doubled = fd * 2;
#0  socket_probe (fd=7) at debugme.c:5
#1  0x0000555555555186 in main () at debugme.c:13
0x0000555555555186 in main () at debugme.c:13
13	    int result = socket_probe(fd);
Value returned is $1 = 14
$2 = 0
[exit=0]
```

## Workload hash

```text
$ sha256sum evidence/T1A/artifacts/workload/debugme.c
be53530d168d4d24b145c3c8b6d854f2f80adc56f50fb49b181f2566c24aeedb  evidence/T1A/artifacts/workload/debugme.c
```

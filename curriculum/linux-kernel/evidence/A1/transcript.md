# A1 evidence transcript

Captured 2026-11-19. Raw stdout/stderr and exit codes below.
Source claims use `early-history.git@0.11`; runtime uses `Linux-0.11-fork@c2e45a7f`.

## Environment

```text
$ uname -a
Linux pkay 6.18.63-2-lts #1 SMP PREEMPT_DYNAMIC Wed, 11 Nov 2026 19:03:11 +0000 x86_64 GNU/Linux
$ id -u && id -un
1000
pk
$ qemu-system-i386 --version
QEMU emulator version 11.1.3
Copyright (c) 2003-2026 Fabrice Bellard and the QEMU Project developers
$ gdb --version
GNU gdb (GDB) 18.1
Copyright (C) 2026 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
```

## Pinned source

cwd: `/home/pk/Apps/termlearn/curriculum/linux-kernel/sources/early-history.git`

```text
$ git rev-parse 0.11
b65b60f4acd7efbbccd3d2411e9e5bca520a7574
$ git rev-parse 0.11^{tree}
d4303c76a830525f6aa6152569b3e3ee83b8c47d
$ git ls-tree -r --name-only 0.11 -- boot init | sort
boot/bootsect.s
boot/head.s
boot/setup.s
init/main.c
$ sha256sum ../linux-0.11.tar.gz
660997a6b1f03ee5aadce0ac806ffa653dedf1dea6d82c6731f9c9ddf0092673  ../linux-0.11.tar.gz
$ git show 0.11:boot/bootsect.s | sha256sum
b7b307f1fb5c982c15d842b2470616e73d1675a1907958dc0f018cad9eb9c769  -
$ git show 0.11:boot/setup.s | sha256sum
1856453ce77a05f1008dc6e4e918920da8941dc614eaacafad13f553a399d4ab  -
$ git show 0.11:boot/head.s | sha256sum
31c86b26f2741a2c0a1d71722a340679f74089d1ae62d5c7bde51ccd694eafd1  -
$ git show 0.11:init/main.c | sha256sum
4afd642cc5d57b2101b1bffb975335182cc30a1cbcb503cf3b890000343daa92  -
```

Exact line ranges are stored in `source/`.

## Runtime harness identity and help

cwd: `/home/pk/Apps/termlearn/curriculum/linux-kernel/sources/Linux-0.11-fork`

```text
$ git rev-parse HEAD
c2e45a7f55ba61029be3b74cd7e72f23bbd068d6
$ git status --short --branch
## master...origin/master
$ make help
<<<<This is the basic help info of linux-0.11>>>

Usage:
     make --generate a kernel floppy Image with a fs on hda1
     make start -- start the kernel in qemu
     make debug -- debug the kernel in qemu & gdb at port 1234
     make disk  -- generate a kernel Image & copy it to floppy
     make cscope -- genereate the cscope index databases
     make tags -- generate the tag file
     make cg -- generate callgraph of the system architecture
     make clean -- clean the object files
     make distclean -- only keep the source code files

Note!:
     * You need to install the following basic tools:
          ubuntu|debian, qemu|bochs, ctags, cscope, calltree, graphviz 
          vim-full, build-essential, hex, dd, gcc 4.3.2...
     * Becarefull to change the compiling options, which will heavily
     influence the compiling procedure and running result.

Author:
     * 1991, linus write and release the original linux 0.95(linux 0.11).
     * 2005, jiong.zhao<gohigh@sh163.net> release a new version 
     which can be used in RedHat 9 along with the book 'Explaining 
     Linux-0.11 Completly', and he build a site http://www.oldlinux.org
     * 2008, falcon<wuzhangjin@gmail.com> release a new version which can be
     used in ubuntu|debian 32bit|64bit with gcc 4.3.2, and give some new 
     features for experimenting. such as this help info, boot/bootsect.s and
     boot/setup.s with AT&T rewritting, porting to gcc 4.3.2 :-)

<<<Be Happy To Play With It :-)>>>
[exit=0]
```

## Default build attempt

```text
$ make -j1
make[1]: Entering directory '/home/pk/Apps/termlearn/curriculum/linux-kernel/sources/Linux-0.11-fork/boot'
make[1]: Leaving directory '/home/pk/Apps/termlearn/curriculum/linux-kernel/sources/Linux-0.11-fork/boot'
make[1]: Entering directory '/home/pk/Apps/termlearn/curriculum/linux-kernel/sources/Linux-0.11-fork/boot'
make[1]: Leaving directory '/home/pk/Apps/termlearn/curriculum/linux-kernel/sources/Linux-0.11-fork/boot'
make[1]: Entering directory '/home/pk/Apps/termlearn/curriculum/linux-kernel/sources/Linux-0.11-fork/boot'
make[1]: Leaving directory '/home/pk/Apps/termlearn/curriculum/linux-kernel/sources/Linux-0.11-fork/boot'
init/main.c:23:15: error: type defaults to ‘int’ in declaration of ‘fork’ [-Wimplicit-int]
   23 | static inline fork(void) __attribute__((always_inline));
      |               ^~~~
init/main.c:24:15: error: type defaults to ‘int’ in declaration of ‘pause’ [-Wimplicit-int]
   24 | static inline pause(void) __attribute__((always_inline));
      |               ^~~~~
init/main.c: In function ‘printf’:
init/main.c:160:28: error: too many arguments to function ‘vsprintf’; expected 0, have 3
  160 |         write(1,printbuf,i=vsprintf(printbuf, fmt, args));
      |                            ^~~~~~~~ ~~~~~~~~
init/main.c:46:12: note: declared here
   46 | extern int vsprintf();
      |            ^~~~~~~~
make: *** [Makefile:43: init/main.o] Error 1
[exit=2]
```

## Successful build attempt

```text
$ make -j1 CFLAGS="-g -m32 -fno-builtin -fno-stack-protector -fomit-frame-pointer -std=gnu89 -Iinclude -I../include -I../../include"
make[1]: Entering directory '/home/pk/Apps/termlearn/curriculum/linux-kernel/sources/Linux-0.11-fork/kernel'
make[1]: Leaving directory '/home/pk/Apps/termlearn/curriculum/linux-kernel/sources/Linux-0.11-fork/kernel'
make[1]: Entering directory '/home/pk/Apps/termlearn/curriculum/linux-kernel/sources/Linux-0.11-fork/mm'
make[1]: Leaving directory '/home/pk/Apps/termlearn/curriculum/linux-kernel/sources/Linux-0.11-fork/mm'
make[1]: Entering directory '/home/pk/Apps/termlearn/curriculum/linux-kernel/sources/Linux-0.11-fork/fs'
exec.c: In function ‘do_execve’:
exec.c:239:25: warning: assignment to ‘char *’ from ‘int’ makes pointer from integer without a cast [-Wint-conversion]
  239 |                 if ((cp = strchr(buf, '\n'))) {
                         ^
make[1]: Leaving directory '/home/pk/Apps/termlearn/curriculum/linux-kernel/sources/Linux-0.11-fork/fs'
make[1]: Entering directory '/home/pk/Apps/termlearn/curriculum/linux-kernel/sources/Linux-0.11-fork/kernel/blk_drv'
make[1]: Leaving directory '/home/pk/Apps/termlearn/curriculum/linux-kernel/sources/Linux-0.11-fork/kernel/blk_drv'
make[1]: Entering directory '/home/pk/Apps/termlearn/curriculum/linux-kernel/sources/Linux-0.11-fork/kernel/chr_drv'
sync
make[1]: Leaving directory '/home/pk/Apps/termlearn/curriculum/linux-kernel/sources/Linux-0.11-fork/kernel/chr_drv'
make[1]: Entering directory '/home/pk/Apps/termlearn/curriculum/linux-kernel/sources/Linux-0.11-fork/kernel/math'
make[1]: Leaving directory '/home/pk/Apps/termlearn/curriculum/linux-kernel/sources/Linux-0.11-fork/kernel/math'
make[1]: Entering directory '/home/pk/Apps/termlearn/curriculum/linux-kernel/sources/Linux-0.11-fork/lib'
make[1]: Leaving directory '/home/pk/Apps/termlearn/curriculum/linux-kernel/sources/Linux-0.11-fork/lib'
1+0 records in
1+0 records out
512 bytes copied, 2.2944e-05 s, 22.3 MB/s
4+0 records in
4+0 records out
2048 bytes (2.0 kB, 2.0 KiB) copied, 1.7174e-05 s, 119 MB/s
309+1 records in
309+1 records out
158465 bytes (158 kB, 155 KiB) copied, 0.00044083 s, 359 MB/s
2+0 records in
2+0 records out
2 bytes copied, 2.5066e-05 s, 79.8 kB/s
[exit=0]
```

## Build artifacts

```text
$ ls -l Image tools/system System.map hdc-0.11.img
-rw-r--r-- 1 pk pk 62447616 Nov 19 13:44 hdc-0.11.img
-rw-r--r-- 1 pk pk   161025 Nov 19 13:51 Image
-rw-r--r-- 1 pk pk    12820 Nov 19 13:51 System.map
-rwxr-xr-x 1 pk pk  343220 Nov 19 13:51 tools/system
$ file Image tools/system
Image:        DOS/MBR boot sector
tools/system: ELF 32-bit LSB executable, Intel i386, version 1 (SYSV), statically linked, with debug_info, not stripped
$ sha256sum Image tools/system System.map
972474892d39c3be7506ee707f5bd7d396c7960485c9fa3c512f77e0b33b2375  Image
7ce373fb398357ffa03d938c76698ade4778b8fdddcc81d84f7ed0c32bcb4c68  tools/system
675d18164eb71052d0c878e21a17de8dda6811fd1970f2f004f75607af21d070  System.map
```

## QEMU + gdb at main

```text
$ qemu-system-i386 -m 16M -boot a -fda Image -hda hdc-0.11.img -s -S -display none &
WARNING: Image format was not specified for 'Image' and probing guessed raw.
         Automatically detecting the format is dangerous for raw images, write operations on block 0 will be restricted.
         Specify the 'raw' format explicitly to remove the restrictions.
WARNING: Image format was not specified for 'hdc-0.11.img' and probing guessed raw.
         Automatically detecting the format is dangerous for raw images, write operations on block 0 will be restricted.
         Specify the 'raw' format explicitly to remove the restrictions.
$ gdb -q -batch -ex "set debuginfod enabled off" -ex "set pagination off" -ex "file tools/system" -ex "target remote :1234" -ex "break main" -ex "continue" -ex "bt" -ex "info registers eip esp eax" -ex "x/8i \$eip" -ex "info breakpoints"
0x0000fff0 in do_execve (eip=0x0 <startup_32>, tmp=0, filename=0x0 <startup_32>, argv=0x0 <startup_32>, envp=0x0 <startup_32>) at exec.c:199
199		if (!(inode=namei(filename)))		/* get executables inode */
Breakpoint 1 at 0x6771: file init/main.c, line 107.

Breakpoint 1, main () at init/main.c:107
107	{			/* The startup routine assumes (well, ...) this */
#0  main () at init/main.c:107
eip            0x6771              0x6771 <main>
esp            0x27f70             0x27f70 <user_stack+4080>
eax            0x80000013          -2147483629
=> 0x6771 <main>:	lea    0x4(%esp),%ecx
   0x6775 <main+4>:	and    $0xfffffff0,%esp
   0x6778 <main+7>:	push   -0x4(%ecx)
   0x677b <main+10>:	push   %ebp
   0x677c <main+11>:	mov    %esp,%ebp
   0x677e <main+13>:	push   %ebx
   0x677f <main+14>:	push   %ecx
   0x6780 <main+15>:	sub    $0x10,%esp
Num     Type           Disp Enb Address    What
1       breakpoint     keep y   0x00006771 in main at init/main.c:107
	breakpoint already hit 1 time
[Inferior 1 (process 1) detached]
[gdb exit=0]
qemu-system-i386: terminating on signal 15 from pid 151534 (/usr/bin/bash)
[qemu stopped]
```

# T0B Evidence Transcript: Source Navigation

Captured 2026-11-19. Raw commands, stdout/stderr, and exit codes.

## Environment & Versions

cwd: `curriculum/linux-kernel/evidence/T0B/artifacts/workload`

```text
$ uname -a
Linux sandbox 6.18.63-2-lts #1 SMP PREEMPT_DYNAMIC Wed, 11 Nov 2026 19:03:11 +0000 x86_64 GNU/Linux
[exit=0]
$ git --version
git version 2.56.1
[exit=0]
$ rg --version | head -n 1
ripgrep 15.2.0
[exit=0]
$ cscope --version
cscope: version 15.9
[exit=0]
```

## Evidence Transcripts

### E-T0B-01: Environment Verification
```text
$ rg --version | head -n 1 && git --version
ripgrep 15.2.0
git version 2.56.1
[exit=0]
```

### E-T0B-02: Header vs C vs Call Site
```text
$ rg -n "sensor_init" .
./src/main.c
11:    int rc = sensor_init(&dev, 42);

./src/sensor.c
11:int sensor_init(struct sensor_device *dev, int id)

./include/sensor_dev.h
12:int sensor_init(struct sensor_device *dev, int id);
[exit=0]
```

### E-T0B-03: Word Boundary Filtering (-w)
```text
$ rg -n "poll" .
./src/main.c
4:int bus_dispatch_poll(struct sensor_device *dev);
16:    int val = bus_dispatch_poll(&dev);
17:    printf("sensor_poll returned %d (registered: %s)\n", val, sensor_temp_primary.name);

./src/bus.c
8:int bus_dispatch_poll(struct sensor_device *dev)
10:    /* True caller of sensor_poll */
11:    return sensor_poll(dev);

./src/sensor.c
25:int sensor_poll(struct sensor_device *dev)

./include/sensor_dev.h
13:int sensor_poll(struct sensor_device *dev);
[exit=0]

$ rg -n -w "sensor_poll" .
./src/main.c
17:    printf("sensor_poll returned %d (registered: %s)\n", val, sensor_temp_primary.name);

./src/bus.c
10:    /* True caller of sensor_poll */
11:    return sensor_poll(dev);

./src/sensor.c
25:int sensor_poll(struct sensor_device *dev)

./include/sensor_dev.h
13:int sensor_poll(struct sensor_device *dev);
[exit=0]
```

### E-T0B-04: Path Filtering (-g)
```text
$ rg -n -g "*.h" "struct sensor_device" .
./include/sensor_dev.h
4:struct sensor_device {
12:int sensor_init(struct sensor_device *dev, int id);
13:int sensor_poll(struct sensor_device *dev);
17:    static struct sensor_device sensor_##name_sym = { \
[exit=0]

$ rg -n -g "src/*.c" "sensor_init" .
./src/main.c
11:    int rc = sensor_init(&dev, 42);

./src/sensor.c
11:int sensor_init(struct sensor_device *dev, int id)
[exit=0]
```

### E-T0B-05: Context Lines (-C)
```text
$ rg -n -C 2 "sanitize_sensor_id" src/sensor.c
1-#include "../include/sensor_dev.h"
2-
3:static int sanitize_sensor_id(int id)
4-{
5-    if (id < 0 || id > 1024) {
--
14-        return -1;
15-    }
16:    int valid = sanitize_sensor_id(id);
17-    if (valid < 0) {
18-        return -1;
[exit=0]
```

### E-T0B-06: Macro Search Traps and Token Pasting
```text
$ rg -n "temp_primary" .
./src/main.c
6:REGISTER_SENSOR(temp_primary, 101);
17:    printf("sensor_poll returned %d (registered: %s)\n", val, sensor_temp_primary.name);
[exit=0]

$ rg -n "sensor_temp_primary" .
./src/main.c
17:    printf("sensor_poll returned %d (registered: %s)\n", val, sensor_temp_primary.name);
[exit=0]
```

### E-T0B-07: Definition Search Strategy
```text
$ rg -n "^int sensor_init\(" .
./src/sensor.c
11:int sensor_init(struct sensor_device *dev, int id)

./include/sensor_dev.h
12:int sensor_init(struct sensor_device *dev, int id);
[exit=0]
```

### E-T0B-08: Caller Enumeration
```text
$ rg -n "sensor_poll\(" src/
src/bus.c
11:    return sensor_poll(dev);

src/sensor.c
25:int sensor_poll(struct sensor_device *dev)
[exit=0]
```

### E-T0B-09: Member vs Variable Disambiguation (-- or -e)
```text
$ rg -n -e "->id" src/
src/sensor.c
20:    dev->id = valid;
[exit=0]

$ rg -n -e "\.id" .
./include/sensor_dev.h
18:        .id = (id_val), \
[exit=0]
```

### E-T0B-10: Git Commit Object & Tree Topology
```text
$ git log --oneline --graph -n 5
* 2689035 (HEAD -> master) Refactor sensor ID validation into sanitize_sensor_id helper
* bf07b1e Add main entry point invoking sensor and bus dispatch
* 192567d Add bus dispatch caller for sensor poll
* e35c772 Implement core sensor initialization and polling
* 386a521 Initial sensor driver interface and Makefile
[exit=0]

$ git cat-file -p HEAD
tree 7c34487d17f2abd615f25a2e969847c5372aaa55
parent bf07b1ec97d8cefbb11c8ea795d5c693fd0cff17
author Kernel Learner <learner@kernel.org> 1795095569 +0530
committer Kernel Learner <learner@kernel.org> 1795095569 +0530

Refactor sensor ID validation into sanitize_sensor_id helper
[exit=0]
```

### E-T0B-11: Git Pickaxe (git log -S)
```text
$ git log -S "sanitize_sensor_id" --oneline
2689035 (HEAD -> master) Refactor sensor ID validation into sanitize_sensor_id helper
[exit=0]
```

### E-T0B-12: Git Function Evolution (git log -L)
```text
$ git log -L :sensor_init:src/sensor.c --oneline
2689035 (HEAD -> master) Refactor sensor ID validation into sanitize_sensor_id helper
diff --git a/src/sensor.c b/src/sensor.c
--- a/src/sensor.c
+++ b/src/sensor.c
@@ -3,10 +11,14 @@
 int sensor_init(struct sensor_device *dev, int id)
 {
-    if (!dev || id < 0) {
+    if (!dev) {
+        return -1;
+    }
+    int valid = sanitize_sensor_id(id);
+    if (valid < 0) {
         return -1;
     }
-    dev->id = id;
+    dev->id = valid;
     dev->status = 1;
     return 0;
 }
 
e35c772 Implement core sensor initialization and polling
diff --git a/src/sensor.c b/src/sensor.c
--- /dev/null
+++ b/src/sensor.c
@@ -0,0 +3,10 @@
+int sensor_init(struct sensor_device *dev, int id)
+{
+    if (!dev || id < 0) {
+        return -1;
+    }
+    dev->id = id;
+    dev->status = 1;
+    return 0;
+}
[exit=0]
```

### E-T0B-13: Git Line-by-Line Attribution (git blame)
```text
$ git blame -n -L 12,24 src/sensor.c
e35c772  4 (Kernel Learner 2026-11-19 19:09:29 +0530 12) {
2689035 13 (Kernel Learner 2026-11-19 19:09:29 +0530 13)     if (!dev) {
2689035 14 (Kernel Learner 2026-11-19 19:09:29 +0530 14)         return -1;
2689035 15 (Kernel Learner 2026-11-19 19:09:29 +0530 15)     }
2689035 16 (Kernel Learner 2026-11-19 19:09:29 +0530 16)     int valid = sanitize_sensor_id(id);
2689035 17 (Kernel Learner 2026-11-19 19:09:29 +0530 17)     if (valid < 0) {
e35c772  6 (Kernel Learner 2026-11-19 19:09:29 +0530 18)         return -1;
e35c772  7 (Kernel Learner 2026-11-19 19:09:29 +0530 19)     }
2689035 20 (Kernel Learner 2026-11-19 19:09:29 +0530 20)     dev->id = valid;
e35c772  9 (Kernel Learner 2026-11-19 19:09:29 +0530 21)     dev->status = 1;
e35c772 10 (Kernel Learner 2026-11-19 19:09:29 +0530 22)     return 0;
e35c772 11 (Kernel Learner 2026-11-19 19:09:29 +0530 23) }
e35c772 12 (Kernel Learner 2026-11-19 19:09:29 +0530 24) 
[exit=0]
```

### E-T0B-14: Kernel Historical Archaeology on Linux 0.11
```text
$ git -C sources/early-history.git log -S "PAGE_SIZE" --oneline 0.11
b65b60f4acd (tag: 0.11) Linux-0.11 (December 8, 1991)
fa1ec1000cf (tag: 0.10) Linux 0.10 (November 11, 1991 ???)
bb441db1a90 Linux-0.01 (September 17, 1991)
[exit=0]
```

### E-T0B-15: Semantic Index Generation (cscope)
```text
$ cscope -b -R
[exit=0]
$ ls -la cscope.out
-rw-rw-rw- 1 pk pk 103666 Nov 19 19:09 cscope.out
[exit=0]
```

### E-T0B-16: Function Pointer Epistemic Boundary
```text
$ rg -n "read_sample" .
./include/sensor_dev.h
8:    int (*read_sample)(void *buf);
21:        .read_sample = 0 \
[exit=0]
```

# Chapter Generation Notes: extreme-c / ch09

- **Chapter**: Chapter 06 — OOP and Encapsulation
- **Source**: Text/oop_and_encapsulation.xhtml
- **Target Pack**: packs/extreme-c/ch09.yaml

## User Interrogation Responses (ASK_USER.md)

1. **Level**: comfortable-in-C
2. **Depth vs speed**: deep (exhaustive blocks, >=3 checks each, zero placeholders, complete code breakdowns)
3. **Prioritize / skip**: keep all concepts and examples
4. **Lab difficulty + toolchain**: best accordingly (medium/hard C opaque pointer/encapsulation pattern, C with gcc -Wall -std=c99 -O0, 2s timeout)
5. **Explanation language**: English
6. **Interleaved review**: 2 checks from prior chapters (ch04)

---

# Chapter Generation Notes: extreme-c / ch10

- **Chapter**: Chapter 07 — Composition and Aggregation
- **Source**: Text/composition_and_aggregation.xhtml
- **Target Pack**: packs/extreme-c/ch10.yaml
- **Generated**: fresh regeneration from prompts/extreme-c/ch10_prompt.md

## User Interrogation Responses (ASK_USER.md)

1. **Level**: comfortable-in-C (default)
2. **Depth vs speed**: deep (default, exhaustive blocks, 5-7 checks each, zero placeholders)
3. **Prioritize / skip**: keep all, skip platform tangents (default)
4. **Lab difficulty + toolchain**: medium, C with gcc -Wall -Wextra -std=c99, 2s timeout (default)
5. **Explanation language**: English (default)
6. **Interleaved review**: 2 checks (to satisfy strict validator gate MAP-005, referencing ch04 and ch09)

## Pack Statistics

- 11 blocks (model / syntax / design / algorithm), 66 scaffolded block checks
- 20 atomic SM-2 spaced repetition flashcards
- 40-question dedicated chapter quiz (intro/core/advanced, mixed, zero duplicates with block checks)
- 3 multi-file labs with scaffolded blank starter files (engine.c, car.c, player.c) and unit test assertions
- 5 final mastery checks; gate needs all 11 blocks at min_quiz 80
- Strict validation: PASS (`python main.py validate --book extreme-c --chapter ch10 --strict`)

---

# Chapter Generation Notes: extreme-c / ch11

- **Chapter**: Chapter 08 — Inheritance and Polymorphism
- **Source**: Text/inheritance_and_polymorphism.xhtml
- **Target Pack**: packs/extreme-c/ch11/ (modular: meta/study/quiz/labs/cards/test)

## User Interrogation Responses (ASK_USER.md)

1. **Level**: comfortable-in-C
2. **Depth vs speed**: deep (exhaustive blocks, 5-6 checks each, zero placeholders)
3. **Prioritize / skip**: keep all, skip platform tangents
4. **Lab difficulty + toolchain**: according to chapter — medium multi-file C labs,
   gcc -Wall -Wextra -std=c99, 2s timeout
5. **Explanation language**: English
6. **Interleaved review**: 2 checks (ch10, ch09)

## Pack Statistics

- 12 blocks (model / syntax / design / algorithm), 61 scaffolded block checks
- 20 atomic SM-2 spaced repetition flashcards
- 40-question dedicated chapter quiz (intro/core/advanced, mixed, zero duplicates with block checks)
- 3 multi-file labs with blank starter files (student.c, cat.c, duck.c) and unit test assertions
- 5 final mastery checks; gate needs all 12 blocks at min_quiz 80
- Answer positions balanced across 0/1/2/3 (22/22/21/19)
- Strict validation: PASS (`python main.py validate --book extreme-c --chapter ch11 --strict`)
- Lab lifecycle verified: untouched starters fail to link; reference solutions pass; run output
  byte-matches `test_cases[].expect` for all 3 labs

---

# Chapter Generation Notes: extreme-c / ch12

- **Chapter**: Chapter 09 — Abstraction and OOP in C++
- **Source**: Text/abstraction_and_oop_in_cplusplus.xhtml
- **Target Pack**: packs/extreme-c/ch12.yaml

## User Interrogation Responses (ASK_USER.md)

1. **Level**: comfortable-in-C (default)
2. **Depth vs speed**: deep (exhaustive blocks, high check volume, comprehensive culmination of entire OOP series)
3. **Prioritize / skip**: keep all core C abstraction, interfaces, pure virtual mechanics, g++ assembly, GDB layouts
4. **Lab difficulty + toolchain**: medium, C with gcc -Wall -std=c99 -O0, 2s timeout (default)
5. **Explanation language**: English (default)
6. **Interleaved review**: 3+ checks spanning last 3 chapters (ch09, ch10, ch11)

---

# Chapter Generation Notes: extreme-c / ch23

- **Chapter**: Chapter 20 — Socket Programming
- **Source**: Text/socket_programming.xhtml
- **Target Pack**: packs/extreme-c/ch23/ (modular: meta/study/quiz/labs/cards/test)

## User Interrogation Responses (ASK_USER.md)

1. **Level**: comfortable-in-C (default)
2. **Depth vs speed**: deep (exhaustive blocks, 5-7 checks each, zero placeholders, complete code breakdowns)
3. **Prioritize / skip**: keep all core socket concepts, protocol serialization, UDS stream/datagram, TCP/UDP, and multi-threaded calculator architecture; skip platform-specific tangents (Windows-only notes)
4. **Lab difficulty + toolchain**: medium multi-file C labs, gcc -Wall -Wextra -std=c99, 2s timeout
5. **Explanation language**: English
6. **Interleaved review**: 2 checks (ch10, ch11)

## Pack Statistics

- 11 blocks (model / syntax / design / algorithm), 66 scaffolded block checks
- 20 atomic SM-2 spaced repetition flashcards
- 40-question dedicated chapter quiz (intro/core/advanced, mixed, zero duplicates with block checks)
- 5 practical multi-file labs with scaffolded starter files, fail-first verification, and unit test assertions:
  1. lab1: Application Protocol Framing and Deserialization (calc_frame.c)
  2. lab2: Unix Domain Socket Stream Server and Client Lifecycle (uds_socket.c)
  3. lab3: Network Byte Order Binary Packet Marshaler (net_calc.c)
  4. lab4: Stream Accumulator Deserializer with Observer Callbacks (stream_deserializer.c)
  5. lab5: Reliable Stream Transmission and Delimited Frame Reception (reliable_stream_io.c)
- 5 final mastery checks; gate needs all 11 blocks at min_quiz 80
- Strict validation: PASS (`python main.py validate --book extreme-c --chapter ch23 --strict`)


# Chapter Generation Notes: extreme-c / ch22

- **Chapter**: Chapter 19 — Single-Host IPC and Sockets
- **Source**: Text/single-host_ipc_and_sockets.xhtml
- **Target Pack**: packs/extreme-c/ch22/ (modular: meta/study/quiz/labs/cards/test)

## User Interrogation Responses (ASK_USER.md)

1. **Level**: comfortable-in-C
2. **Depth vs speed**: deep (more blocks, 5–10 checks each, zero placeholders)
3. **Prioritize / skip**: keep all topics (signals → pipes → message queues → UDS → five network layers → sockets → listener/connector)
4. **Lab difficulty + toolchain**: hard multi-file labs, gcc -Wall -Wextra -std=c99, 2s timeout
5. **Explanation language**: English
6. **Interleaved review**: exactly 2 checks (compromise confirmed by user for strict validation)

## Post-Interrogation Overrides (user-directed, govern the genus)

- **Block count**: "use as many blocks as needed" — authoring was NOT capped at 15;
  20 single-concept blocks shipped (b1–b20).
- **Card count**: "don't trim cards" — 41 atomic cards shipped, outside (above) the
  bundle's 15–25 guidance; kept at user instruction after the range conflict was raised.

## Pack Statistics

- 20 blocks: 12 model / 3 algorithm / 2 design / 3 syntax; 126 scaffolded block
  checks (76 conceptual = why-fails/predict/eipe/choose-better/trace/spot-bug)
- Check kind mix: mcq 25, fillblank 18, trace 16, predict 15, why-fails 21,
  eipe 10, choose-better 9, order 7, spot-bug 5
- 18 visualization stanzas; model blocks all carry viz
- Book code: Code Box 19-1 (signals), 19-2 (pipe), 19-3 (mq) taught verbatim as
  b9/b10/b13 examples (adapted: false); the six Shell Boxes are rendered as
  stats/transcripts inside explanation prose; b14–b20 carry no pseudo examples
- 41 atomic SM-2 flashcards (post-interrogation override above)
- 46-question dedicated quiz (10 intro / 22 core / 14 advanced; mixed kinds;
  zero duplicate stems with block checks; answer slots spread 0–3)
- 3 practical multi-file labs (progressive hints, fail-first verified with the
  real lab_workspace engine, then byte-exact reference passes):
  1. lab1: Length-Prefix Framing over a Pushed Byte Channel (framing.c)
  2. lab2: Engine Room of a POSIX-Style Message Queue (imq.c)
  3. lab3: Listener-Connector Sequences on a Simulated Kernel (listener.c, connector.c)
- 2 interleaved review checks: b1 → ch21 (pull-based sync), b10 → ch20
  (fork descriptor inheritance)
- 5 final mastery checks; gate needs all 20 blocks at min_quiz 80
- Strict validation: PASS (`python main.py validate --book extreme-c --chapter ch22 --strict`, exit 0)

## Idea-Unit Audit Trail (chapter heading → block)

- Techniques taxonomy / pull vs push → b1; serialization/deserialization → b2;
  content types + Base64/compression → b3; variable-length partitioning
  (delimiter, length prefix, FSM) → b4; sequentiality sync/async → b5;
  fixed- vs variable-length design → b6
- File descriptors → b7; signals semantics → b8; signal/kill/raise syntax (+Code
  Box 19-1) → b9; pipe wiring algorithm (+Code Box 19-2) → b10; unrelated-
  process sharing (fd transfer vs mkfifo) → b11; queues vs pipes model → b12;
  mq_* API (+Code Box 19-3) → b13; UDS model → b14
- Physical+link layers → b15; network layer/IP → b16; transport layer
  (ports, stream vs datagram, TCP/UDP) → b17; application layer + IPS → b18;
  socket attributes + descriptor split → b19; listener-connector sequences → b20

## Code-Box Dispositions (all 9 boxes)

- Code Box 19-1 → b9 example (verbatim, compiles clean, no run_expected —
  busy-loop + external kills are interactive)
- Code Box 19-2 → b10 example (verbatim, fork-based child/parent timing shown
  in shell transcript; run_expected omitted for the same nondeterminism reason)
- Code Box 19-3 → b13 example (verbatim; macOS note and -lrt build facts kept)
- Shell Boxes 19-1..19-4 → embedded in b9/b13 explain/check facts as transcripts
- Chapter link/notes (QNX MQM reference) → enrichment provenance only

## Verification Notes

- All 3 examples compile under the hero probe (gcc -Wall -std=c99 -O0 -c) and
  every no-code block omits example.code (compile-probe discipline)
- Labs: stubs are empty student files (framing.c, imq.c, listener.c, connector.c)
  → fail-first via undefined references (exit 1); verified reference solutions
  in /tmp/opencode/ch22-dev/lab{1,2,3}/*_ref.c pass commands.test (exit 0, unit
  harnesses "FRAMING/IMQ/SOCKSIM TESTS PASSED") and byte-match
  test_cases[].expect against commands.run stdout
- Quiz trace items: target at check level (per validator), answer_text at check
  level; quiz WHY-RATIO maintained ≥ half via 4 mcq→conceptual conversions

# ch23 study.yaml Rewrite (2026-10-26)

Scope: full replacement of `packs/extreme-c/ch23/study.yaml` (was authored with
invented runnable examples, ch10/ch11 interleaved refs, swapped TCP/UDP ports,
and a wrong htons distractor). Structural counts unchanged elsewhere: quiz
(50), cards, labs (3), test.yaml untouched - its `needs: [b1..b11]` gate still
resolves because ids b1..b11 are kept, three blocks appended (b12-b14).

## What Changed

- 14 blocks (was 11) following the book's own order: review recap (b1),
  project hierarchy + build/run Shell Boxes 20-1..20-4 (b2), calculator
  protocol verbatim Code Box 20-1 example (b3), serializer API + ring-buffer
  machine (b4), stateful service with CALC_SVC_OK/-1 doctrine (b5), UDS
  stream server lifecycle + unlink + sun_path 103/107 + abstract sockets
  (b6), accept_forever/client_handler/stream_write_resp verbatim mechanics,
  ctor 256 / read 128 / ret<buf.len fatal (b7), stream client with reader
  thread + SHUT_RD + 128 ctor + exit order (b8), UDS datagram server with
  per-datagram objects + req_found FALSE -> -1/ERROR_INVALID_RESPONSE(201)/0
  (b9), datagram client self-bind dependency (calc_cli.sock, connect, sendto)
  (b10), TCP main-only deltas with htons(6666) + h_addr copy (b11), byte
  order block (htons trap 6666->2586 arithmetic fixed; the old "27162" was
  wrong) (b12), UDP with htons(9999) and auto-bound clients (b13), one-code
  base-four-skins consolidation (b14).
- Examples policy: ONLY book code boxes. b3 carries Code Box 20-1 verbatim
  (adapted: false, compiles clean under gcc -Wall -Wextra -std=c99); all
  other blocks no-code (check-level snippets carry the teaching), matching
  the ch22 precedent.
- Interleaved checks: exactly 2, now anchored to the real prerequisite -
  b3 -> ch22/b4 (partitioning methods drive the #/$ delimiter choice) and
  b6 -> ch22/b20 (stream listener sequence; bind exclusivity rule). The old
  ch10/ch11 composition/vtable refs were irrelevant and removed.
- 90 checks (6-7/block, ids b1..b10 5 then 7 each, b11 6, b12 7, b13 6,
  b14 5); conceptual WHY share 57/90 = 63.3% (validator needs >= half);
  kinds mix predict/trace/spot-bug/why-fails/eipe/choose-better +
  fillblank/order/mcq sparsely.
- All 14 blocks carry ascii-memory viz; every check carries level + concept
  (90 unique slugs); no stem collides with quiz items (Jaccard <= 0.75) or
  within study.
- trace targets verified on ??? cells; spot-bug target_line verified on the
  defective lines after repair (b7 teardown-order bug now coherently shows
  svc created-then-torn-down-before-loop; b9 uses buf.len = socklen as the
  bug at line 18 per Code Box 20-25's buf.len = read_nr_bytes).

## Verification Notes

- Strict: python3 main.py validate --book extreme-c --chapter ch23 --strict
  -> OK ch23/ (exit 0); only benign EXT-SOURCE cover-page advisory remains
- Quiz/cards/labs/test diffs: none; block ids b1..b11 retained so test.yaml
  gates stay valid

# Generation notes: bgnet ch06 (System Calls or Bust)

## Scope

Source chapter: `books/bgnet/raw_chapters/ch06.txt` (1830 lines). This chapter
covers `getaddrinfo`, `socket`, `bind`, `connect`, `listen`, `accept`,
`send`/`recv`, `sendto`/`recvfrom`, `close`/`shutdown`, `getpeername`, and
`gethostname`, plus the `showip.c` walkthrough and the old-style
`sockaddr_in` setup.

Target pack: `packs/bgnet/ch06/` in modular mode (`meta.yaml`, `study.yaml`,
`quiz.yaml`, `labs.yaml`, `cards.yaml`, `test.yaml`).

## ASK_USER decisions (defaults applied)

No blocking questions were asked. Defaults used:

- Quiz size: 44 questions, above the 30 minimum, with 12 intro, 14 core, and
  18 advanced items.
- Labs: 3 labs, each multi-file with a fail-first stub and a deterministic
  unit runner.
- Prerequisite: `ch05`, because this chapter assumes file descriptors, process
  I/O, and basic C build habits.
- Level: `core`.
- Cards: one atomic SM-2 card per fact/concept, 47 total.
- Interleaving: 3 checks cite prior-chapter block ids (`ch04/b6`,
  `ch04/b7`, `ch04/b9`) and test transfer, not recall of the source text.

## Idea units

Every substantive unit in the chapter is mapped to a study block and at least
one check.

| # | Idea unit | Where covered |
|---|-----------|---------------|
| 1 | `gethostbyname` is IPv4-only and forces hand-built `sockaddr_in` | b1 |
| 2 | `getaddrinfo` signature and four parameters | b1, b2 |
| 3 | `hints` fields: `ai_family`, `ai_socktype`, `ai_protocol`, `ai_flags` | b1, b2 |
| 4 | `AF_UNSPEC` asks for either family | b1, b2 |
| 5 | `AI_PASSIVE` marks a server wildcard request | b1, b2 |
| 6 | Result list traversal with `ai_next` | b1, b2 |
| 7 | `ai_addr`/`ai_addrlen` are family-dependent | b1, b3 |
| 8 | Result ownership and `freeaddrinfo` | b2 |
| 9 | Error reporting with `gai_strerror` | b2 |
| 10 | Server hints example: NULL node, service, `AI_PASSIVE` | b1, b2 |
| 11 | Client hints example: node + service, no `AI_PASSIVE` | b1, b2, b7 |
| 12 | Looping over candidates and calling `connect` | b7 |
| 13 | `showip.c` formats addresses from the result list | b3 |
| 14 | `inet_ntop` and the family switch | b3 |
| 15 | Numeric host strings and `AI_NUMERICHOST` | b3 |
| 16 | Service names versus numeric port strings | b1, b3 |
| 17 | `sockaddr_storage` holds either address family | b3, b13 |
| 18 | `socket()` signature: domain, type, protocol | b4 |
| 19 | Socket descriptor return and `-1` failure | b4 |
| 20 | `PF_INET`/`AF_INET` equivalence in practice | b4 |
| 21 | `SOCK_STREAM` versus `SOCK_DGRAM` | b4 |
| 22 | `bind()` signature and `sockaddr` cast | b5 |
| 23 | Choosing the bind port and address | b5 |
| 24 | `INADDR_ANY` wildcard binding | b5 |
| 25 | Old-style `sockaddr_in`: zeroing, `sin_family`, `sin_port`, `sin_addr` | b5 |
| 26 | Network byte order for the port field | b5, b6 |
| 27 | `SO_REUSEADDR` and `setsockopt` | b6 |
| 28 | Handling `bind` errors | b5, b6 |
| 29 | `connect()` signature and `sockaddr` cast | b7 |
| 30 | `connect` returns `0`/`-1` and sends no application data | b7 |
| 31 | Clients normally skip `bind` and get an ephemeral port | b7 |
| 32 | `listen()` signature and backlog | b8 |
| 33 | Server call sequence: socket, bind, listen, accept | b8 |
| 34 | `accept()` returns a new descriptor | b9 |
| 35 | `accept` fills peer address and treats `addrlen` as in/out | b9 |
| 36 | The listening socket remains open after `accept` | b9 |
| 37 | `send()` signature and flags such as `MSG_OOB` | b10 |
| 38 | Partial sends and the send-all loop | b10 |
| 39 | `recv()` return `0` means peer closed | b10 |
| 40 | Partial receives and buffer sizing | b10 |
| 41 | `sendto()` adds a destination address for datagrams | b11 |
| 42 | `recvfrom()` reports the sender and treats `addrlen` as in/out | b11 |
| 43 | Connectionless datagram workflow | b11 |
| 44 | `close()` releases the descriptor | b12 |
| 45 | `shutdown()` directions: `SHUT_RD`, `SHUT_WR`, `SHUT_RDWR` | b12 |
| 46 | `shutdown` half-close versus `close` full release | b12 |
| 47 | `getpeername()` retrieves the connected peer | b13 |
| 48 | `gethostname()` retrieves the local host name | b13 |
| 49 | Resolver may return multiple candidates | b1, b2, b7 |
| 50 | Per-call error handling (`gai_strerror`, `perror`) | b2, b5, b6, b7 |
| 51 | IPv4 versus IPv6 address sizes | b3, b13 |
| 52 | Windows startup/cleanup differs from POSIX | b12 (mention only) |
| 53 | Blocking behavior of `connect` and `accept` | b7, b8, b9 |
| 54 | `accept` blocks until a connection arrives | b9 |
| 55 | `connect` blocks through the TCP handshake | b7 |
| 56 | `hints` must be zeroed before use | b1, b2 |
| 57 | `service` is required for a useful lookup | b1, b2 |
| 58 | `AI_PASSIVE` with a NULL node yields wildcard addresses | b1, b2 |
| 59 | `addrlen` must be initialized before `accept`/`recvfrom` | b9, b11 |
| 60 | The `sockaddr` cast is safe only when the family matches | b3, b9, b11, b13 |

## Code boxes

There are 26 code-bearing boxes/transcripts in the source chapter. All are
either taught, checked, or explicitly deferred; none are ignored silently.

| # | Source box | Disposition |
|---|------------|-------------|
| 1 | `getaddrinfo` signature | Taught and checked in b1/b2 |
| 2 | Server `getaddrinfo` sample | Taught in b1, checked in b2 |
| 3 | Client `getaddrinfo` sample | Taught in b7, checked in b7 |
| 4 | `showip.c` | Adapted as b3 example and checks |
| 5 | Sample `showip` shell run | Mapped to b3 expected output/checks |
| 6 | `socket` signature | Taught in b4, checked in b4 |
| 7 | `socket` call using `res` | Taught in b4, checked in b4 |
| 8 | `bind` signature | Taught in b5, checked in b5 |
| 9 | `bind` example | Taught and checked in b5 |
| 10 | Old-style `sockaddr_in` bind | Taught and checked in b5/b6 |
| 11 | `setsockopt(SO_REUSEADDR)` | Taught and checked in b6 |
| 12 | `connect` signature | Taught in b7, checked in b7 |
| 13 | `connect` example | Taught and checked in b7 |
| 14 | `listen` signature | Taught in b8, checked in b8 |
| 15 | Server call-sequence pseudocode | Taught in b8, ordered in b8 |
| 16 | `accept` signature | Taught in b9, checked in b9 |
| 17 | `accept` example | Taught and checked in b9 |
| 18 | `send` signature | Taught in b10, checked in b10 |
| 19 | `send` example | Taught and checked in b10 |
| 20 | `recv` signature | Taught in b10, checked in b10 |
| 21 | `sendto` signature | Taught in b11, checked in b11 |
| 22 | `recvfrom` signature | Taught in b11, checked in b11 |
| 23 | `close` call | Taught in b12, checked in b12 |
| 24 | `shutdown` signature | Taught in b12, checked in b12 |
| 25 | `getpeername` signature | Taught in b13, checked in b13 |
| 26 | `gethostname` signature | Taught in b13, checked in b13 |

All 13 runnable study examples are marked `adapted: true` with a per-block
`note` that records the simplification (fixed inputs, compact error handling,
or deterministic printed output). The call shapes and system-call semantics
are unchanged.

Deferred on purpose: Windows-specific `WSAStartup`/`closesocket` code is
mentioned as a portability note but not exercised, because every example,
test, and lab targets POSIX and compiles with
`_POSIX_C_SOURCE 200112L`. No networking is performed by any lab.

## Block and check inventory

| Block | Type | Checks | Focus |
|-------|------|--------|-------|
| b1 | model | 7 | getaddrinfo request model, hints, AI_PASSIVE |
| b2 | syntax | 7 | getaddrinfo call shape, ownership, errors |
| b3 | model | 8 | result-list walk, address formatting, sockaddr_storage |
| b4 | syntax | 8 | socket creation and descriptor handling |
| b5 | syntax | 8 | bind and old-style sockaddr_in setup |
| b6 | design | 7 | address reuse and socket options |
| b7 | syntax | 8 | connect and client candidate loop |
| b8 | syntax | 7 | listen and server call order |
| b9 | model | 8 | accept, new descriptor, peer address |
| b10 | algorithm | 9 | stream send/recv, partial I/O, close detection |
| b11 | syntax | 9 | datagram sendto/recvfrom |
| b12 | design | 8 | close, shutdown, half-close decisions |
| b13 | syntax | 8 | getpeername, gethostname, peer storage |

Totals: 13 blocks, 102 checks, all conceptual (`recall` count: 0), with
7-9 checks per block. Interleaved checks: 3 (from `ch04/b6`, `ch04/b7`,
`ch04/b9`). Model blocks have `viz`; design blocks have `eipe` and
`choose-better`; syntax/algorithm blocks have `order`.

## Quiz, cards, labs, test

- Quiz: 44 questions, levels interleaved round-robin (intro/core/advanced),
  no duplicate stems against study checks, answer indices distributed across
  0-3.
- Cards: 47 atomic cards, each with a single fact, a stable `concept`, and a
  one-line rationale or a WHY/WHEN prompt.
- Labs: `lab1` (hints), `lab2` (address walk), `lab3` (stream I/O). Each has
  complete headers, `main`, test runner, fail-first stub, reference-pass
  behavior, and one reference `run` case.
- Test: 3 gates (`b1-b4` at 70, `b1-b9` at 80, all at 85) plus 5 final checks
  referencing real block ids.

## Answer-shape invariants

- All 16 `fillblank` items (12 block checks, 4 quiz questions) accept a
  single word/token; no multi-word or line-length answers remain.
- Every `order` stem states the number of correct lines to place and notes
  that one displayed line is a distractor.
- Choice sets were rewritten into parallel phrasing. The maximum
  max/min character ratio across all 116 choice sets is 1.30, and the correct
  option is never more than 20% longer than the longest distractor.

## Verification log

- `python main.py validate --book bgnet --chapter ch06 --strict` -> `OK ch06/`,
  exit 0, zero errors and zero warnings.
- All 11 study examples with `run_expected` compile under
  `gcc -Wall -std=c99 -O0` and match their expected stdout.
- All 3 labs fail first with the untouched stub (`test` exit 1).
- All 3 labs pass with the reference implementation (`test` exit 0), and each
  `run` output exactly matches its `test_cases[0].expect`.
- No question, explanation, hint, or card references a book chapter, code
  box, listing, figure, exercise, or problem number. Prior-chapter citations
  exist only in internal `from_chapter` metadata for interleaved checks.

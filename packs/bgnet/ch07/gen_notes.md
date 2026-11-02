# Generation notes: bgnet ch07 (Client-Server Background)

## Scope

Source chapter: `books/bgnet/raw_chapters/ch07.txt` (2331 lines). It covers the
client-server model, a fork-per-connection stream server, SIGCHLD reaping, peer
address formatting, a stream client, datagram listener/talker programs, family
matching, and connected datagram sockets.

Target pack: `packs/bgnet/ch07/` in modular mode (`meta.yaml`, `study.yaml`,
`quiz.yaml`, `labs.yaml`, `cards.yaml`, `test.yaml`).

## Decisions

No blocking questions were asked. Defaults used:

- Quiz size: 38 questions, with 13 intro, 12 core, and 13 advanced items.
- Labs: 3 deterministic C labs with fail-first stubs and unit runners.
- Prerequisite: `ch06`, because the chapter assumes getaddrinfo, socket,
  bind, listen, accept, and send/recv.
- Level: `core`.
- Cards: 42 atomic cards, one per fact or contrast.
- Interleaving: 2 checks cite prior block ids (`ch06/b8` for listen ordering
  and `ch06/b9` for listener lifetime) and test transfer rather than recall.

## Idea units

Count: **35 idea units**, all mapped below.

| # | Idea unit | Where covered |
|---|-----------|---------------|
| 1 | Client initiates; server waits and answers | b1 |
| 2 | telnet/telnetd, ftp/ftpd, browser/web-server pairs | b1 |
| 3 | Both sides must agree on the socket type | b1 |
| 4 | One server handles many clients with fork | b1, b3 |
| 5 | Server loop: wait, accept, fork, return to accept | b1, b3 |
| 6 | Server sends a fixed greeting on the accepted stream | b3, b6, lab1 |
| 7 | Server hints use AF_UNSPEC, SOCK_STREAM, AI_PASSIVE | b2 |
| 8 | Candidate loop tries each addrinfo record | b2 |
| 9 | SO_REUSEADDR allows rebinding a lingering port | b2 |
| 10 | bind failure closes the socket and tries the next candidate | b2 |
| 11 | listen marks the bound socket ready and sets backlog | b2 |
| 12 | accept returns a new descriptor | b3 |
| 13 | accept addrlen is an in/out value | b3 |
| 14 | Parent closes new_fd after fork | b3 |
| 15 | Child closes its copy of the listening socket | b3 |
| 16 | fork copies the descriptor table; closes are per process | b3 |
| 17 | SIGCHLD signals child state changes | b4 |
| 18 | waitpid(-1, NULL, WNOHANG) drains ready zombies | b4 |
| 19 | Reaping loop stops on 0 or -1 | b4 |
| 20 | Handler saves and restores errno | b4 |
| 21 | get_in_addr selects sin_addr or sin6_addr by family | b5 |
| 22 | inet_ntop formats an address; INET6_ADDRSTRLEN is safe | b5 |
| 23 | sockaddr_storage must be cast only after the family check | b5 |
| 24 | Stream client resolves, connects, receives, closes | b6 |
| 25 | Client skips bind and gets an ephemeral port | b6 |
| 26 | Stream has no message boundaries; null-terminate text | b6 |
| 27 | Datagram listener uses SOCK_DGRAM, bind, recvfrom | b7 |
| 28 | Datagram listener does not listen or accept | b7 |
| 29 | recvfrom reports the sender address | b7 |
| 30 | Datagram talker uses sendto with an explicit destination | b8 |
| 31 | UDP is best effort; sendto success is local only | b8 |
| 32 | Forcing AF_INET6 avoids a silent family mismatch | b8, b9 |
| 33 | Connected datagram socket records one default peer | b9 |
| 34 | Connected UDP filters other senders | b9 |
| 35 | UDP connect is not a handshake and adds no reliability | b9 |

## Code boxes

The source has 5 fenced boxes: one shell `telnet` command and four full C
programs (`server.c`, `client.c`, `listener.c`, `talker.c`). All are either
taught, checked, or adapted; none are ignored.

| # | Source box | Disposition |
|---|------------|-------------|
| 1 | `telnet remotehostname 3490` | Taught as the stream server test method in b1/b6 |
| 2 | `server.c` | Adapted into b1-b5 examples and checks |
| 3 | `client.c` | Adapted into b6 example and checks |
| 4 | `listener.c` | Adapted into b7 example and checks |
| 5 | `talker.c` | Adapted into b8/b9 examples and checks |

All 9 runnable examples are marked `adapted: true` with a per-block note. The
adaptations replace live network peers with pipes, socketpairs, or loopback
sockets, shorten error exits, and print deterministic state. The call shapes
and system-call semantics are unchanged.

Deferred on purpose: no Windows startup/cleanup code is exercised, because
every example and lab targets POSIX and compiles with `_POSIX_C_SOURCE`. No lab
performs external network I/O.

## Block and check inventory

| Block | Type | Checks | Focus |
|-------|------|--------|-------|
| b1 | model | 7 | client-server roles, fork-per-connection loop |
| b2 | syntax | 9 | server hints, candidate loop, bind, listen |
| b3 | model | 9 | accept, fork, descriptor ownership |
| b4 | algorithm | 7 | SIGCHLD, waitpid, WNOHANG, errno |
| b5 | syntax | 7 | get_in_addr, inet_ntop, family cast |
| b6 | syntax | 9 | stream client connect/recv/close |
| b7 | syntax | 8 | datagram listener bind/recvfrom |
| b8 | syntax | 8 | datagram talker sendto and family match |
| b9 | design | 8 | connected datagram sockets and filtering |

Totals: 9 blocks, 72 checks, 8-9 checks per block where depth warrants it.
Interleaved checks: 2. Model blocks have `viz`; design block b9 has
`choose-better`; syntax/algorithm blocks include `order`, `trace`, or
`spot-bug` where appropriate.

## Quiz, cards, labs, test

- Quiz: 38 questions, levels interleaved round-robin (intro/core/advanced), no
  duplicate stems against study checks, answer indices distributed across
  0-2.
- Cards: 42 atomic cards with stable `concept` tags and one-line rationales.
- Labs: `lab1` (serve one accepted connection), `lab2` (reap ready children),
  `lab3` (build an IPv6 datagram destination). Each has complete headers,
  drivers, test runners, fail-first stubs, reference-pass behavior, and one
  reference `run` case.
- Test: 3 gates (`b1-b4` at 70, `b1-b6` at 80, all at 85) plus 5 final checks
  referencing real block ids.

## Answer-shape invariants

- All 14 `fillblank` items (9 block checks, 5 quiz questions) accept a single
  word/token; no multi-word or line-length answers remain.
- Every `order` stem states the number of correct lines to place and notes
  when a displayed line is a distractor.
- All 86 choice sets use parallel phrasing. The maximum max/min character
  ratio is 1.29, and the correct option is never more than 20% longer than the
  longest distractor (max 1.167).
- Answer positions are distributed: study checks 23/18/14 across 0/1/2; quiz
  13/11/7 across 0/1/2.

## Verification log

- `python main.py validate --book bgnet --chapter ch07 --strict` -> `OK ch07/`,
  exit 0, zero errors and zero warnings.
- All 9 study examples with `run_expected` compile under
  `gcc -Wall -std=c99 -O0` and match their expected stdout.
- All 3 labs fail first with the untouched stub (`test` exit 1).
- All 3 labs pass with the reference implementation (`test` exit 0), and each
  `run` output exactly matches its `test_cases[0].expect`.
- No question, explanation, hint, or card references a book chapter, code
  box, listing, figure, exercise, or problem number. Prior-chapter citations
  exist only in internal `from_chapter` metadata for interleaved checks.

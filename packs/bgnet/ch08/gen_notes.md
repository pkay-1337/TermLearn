# ch08 Generation Notes

## Source and scope

- Source: `books/bgnet/raw_chapters/ch08.txt`, titled **Slightly Advanced Techniques**.
- Prerequisite: `ch07`; level: `advanced`.
- Coverage: blocking/non-blocking sockets, `poll()`, `select()`, partial sends, serialization,
  length-prefixed encapsulation, and IPv4 UDP broadcast.
- Deferred: full production chat-server listings and the complete `pack()`/`unpack()` implementation.
  Their mechanisms are taught and checked; the listings are not required for mastery.

## Idea units

Count: **40 idea units**, all taught, checked, or explicitly deferred below.

| Area | Units |
|------|-------|
| Blocking | blocking means sleep; `fcntl` sets `O_NONBLOCK`; `EAGAIN`/`EWOULDBLOCK`; busy-wait cost |
| `poll()` | `pollfd` fields; `POLLIN`/`POLLOUT`/`POLLHUP`; millisecond timeout; return count; scanning `revents`; listener readiness; dynamic array growth; removal by compaction or negative `fd` |
| `select()` | three sets; `FD_ZERO`/`FD_SET`/`FD_CLR`/`FD_ISSET`; highest fd plus one; `timeval` units; zero vs `NULL` timeout; master/read_fds copy; close detected by `recv` returning 0; non-blocking workaround |
| Partial send | short `send` return; sendall loop; error on 0/-1; receiver sees a byte stream |
| Serialization | text/raw/portable choices; `htonl`/`ntohl`; raw struct hazards; IEEE-754; `pack754`; packing struct fields independently; untrusted-length validation |
| Encapsulation | length-prefixed packet; fixed name field; total length includes length byte; partial receive; two-packet work buffer |
| Broadcast | UDP only; `SO_BROADCAST`; subnet address; `INADDR_BROADCAST`; router scope; cost to every host |

## Code-box disposition

The source contains **26 fenced code boxes**. Disposition:

- **Adapted into runnable examples:** blocking `fcntl`, `poll` prototype/`pollfd`, simple `poll`,
  `poll` chat loop, `select` prototype/`fd_set`/`timeval`, simple `select`, `select` chat loop,
  `sendall`, integer serialization, struct field packing, and `SO_BROADCAST` setup.
- **Taught and checked without a full listing:** the large `poll` and `select` chat servers, naive
  float packing, `pack754`, and the `pack()`/`unpack()` demonstration.
- **Deferred:** the complete variable-argument `pack()`/`unpack()` implementation and full server
  listings. The packet layout and framing rules are covered by `b8` and the lab.

Every adapted example is marked `adapted: true` with a note explaining the local substitution
(pipe or socketpair instead of a live network peer).

## Answer-shape invariants

- `fillblank` answers are one token: `EWOULDBLOCK`, `milliseconds`, `1`, `bytes`, `htonl`, `754`,
  `INADDR_BROADCAST`.
- `order` stems state the number of correct lines and whether a distractor is present.
- Choice sets are written to comparable length; the strict validator's ratio audit is the final gate.
- Correct-answer positions are distributed across the choice sets.

## Verification

- Strict validation must pass with zero errors and warnings.
- Every example must compile under the book toolchain and match `run_expected`.
- Every lab must fail on the untouched stub and pass with a reference implementation.

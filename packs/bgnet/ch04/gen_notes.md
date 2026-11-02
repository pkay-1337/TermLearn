# bgnet / ch04 generation notes (audit trail)

## ASK_USER interrogation — answered by operator directive ("read the prompts and get to work, just do what the prompt says")

1. Level: comfortable-in-C (default).
2. Depth: deep — 5–10 scaffolded checks per block (default).
3. Prioritize/skip: keep all chapter idea units; skip platform tangents.
   The author explicitly postpones IPv6 flow information and scope ID, so
   they are taught as "present but not yet explained" under b9. The IPv6-to-
   IPv4 NAT gateway is outside the chapter's scope and is deferred under b12.
   Standard 64-bit byte-order functions and floating-point serialization are
   named but deferred by the author to the htons() reference/serialization
   chapter; cards record the 64-bit limitation. Raw sockets and historical
   `inet_addr`/`inet_aton`/`inet_ntoa` details stay as warnings, not labs.
4. Lab difficulty + toolchain: easy-medium; C with the declared toolchain
   `gcc -Wall -Wextra -std=c99`, matching `packs/bgnet/book.yaml`.
5. Explanation language: English.
6. Interleaved review: 2 checks pulling from ch03 — b6 revisits transport
   layers/ports (ch03 b4), b12 revisits the layered model (ch03 b8). Both are
   self-contained questions, not external references.

## Idea-unit enumeration (Karpicke & Blunt 2011 idea-unit method; every unit
## is taught, practiced, or explicitly deferred)

### IPv4 / IPv6 addresses (b1–b2)
1.  IPv4 addresses are four bytes ("octets"), written in dotted-quad form
    → b1 explain, viz, predict/mcq.
2.  Dotted text is presentation; the machine stores four byte values
    → b1 explain + eipe; b10–b11 conversion.
3.  IPv4 is 32 bits, about 4.3 billion distinct values → b1 checks.
4.  Virtually every site used IPv4; demand grew to every person and device
    → b1 explain.
5.  Early huge allocations to large organizations accelerated exhaustion
    → b1 mcq/why.
6.  Stopgap measures delayed exhaustion; IPv6 is the long-term answer
    → b1 explain.
7.  IPv6 is 128 bits, about 340 trillion trillion trillion values, roughly
    79 million billion trillion times IPv4 → b1 checks.
8.  The 96-bit difference is an exponent change, not 96 extra addresses
    → b1 why-fails.
9.  IPv6 text uses eight two-byte hexadecimal groups separated by colons
    → b2 explain, order/fillblank.
10. Leading zeros inside a group may be dropped → b2 checks.
11. A run of all-zero groups compresses to exactly one `::` → b2 checks.
12. Multiple spellings can name the same 16-byte value → b2 eipe/checks.
13. `::1` is IPv6 loopback; `127.0.0.1` is IPv4 loopback → b2 mcq, card.
14. `::ffff:192.0.2.33` is the IPv4-mapped spelling → b2 fillblank, card.
15. IPv6 reserves large blocks for special use, but capacity remains vast
    → b1/b2 explain (non-checkable aside, no check needed).

### Subnets, netmasks, CIDR (b3)
16. An address has a network portion and a host portion → b3 explain.
17. Zeroing the host portion names the network → b3 predict.
18. Historical classes A/B/C fixed the split at 1/2/3 network bytes
    → b3 explain + card.
19. A netmask has 1-bits for network and 0-bits for host → b3 checks.
20. Bitwise-AND of address and mask yields the network number
    → b3 predict/eipe.
21. `192.0.2.12 AND 255.255.255.0 = 192.0.2.0` → b3 worked example.
22. Modern masks may use any prefix length, not only 8/16/24 → b3 checks.
23. `255.255.255.252` is 30 network bits and 2 host bits (four addresses)
    → b3 mcq/trace.
24. A valid netmask is a contiguous run of 1-bits then 0-bits → b3 why-fails.
25. CIDR slash notation writes the network-bit count (`/30`) → b3 checks.
26. IPv6 CIDR examples include `2001:db8::/32` and
    `2001:db8:5413:4028::9db9/64` → b3 fillblank/lab.

### Ports and layering (b4)
27. A port is a 16-bit number used by TCP and, coincidentally, UDP
    → b4 checks, card.
28. IP gets bytes to the host; the port selects the service → b4 eipe/why.
29. Hotel analogy: IP is the street address, port is the room number
    → b4 explain + card.
30. One IP can serve mail and web simultaneously because ports differ
    → b4 checks.
31. Well-known ports: HTTP 80, telnet 23, SMTP 25, DOOM 666; IANA list and
    `/etc/services` are the references → b4 mcq, card.
32. Ports below 1024 are special and usually require OS privileges
    → b4 mcq, card.
33. The pair (IP, port) names an endpoint, not just a host → b4 checks.

### Byte order (b5–b6)
34. A multi-byte value is a byte sequence; `b34f` is the running example
    → b5 explain/trace.
35. Big-endian stores the most significant byte first (`b3 4f`)
    → b5 checks.
36. Little-endian stores the least significant byte first (`4f b3`)
    → b5 checks.
37. Intel 80x86 is little-endian; Motorola 68k is big-endian; PowerPC may be
    either → b5 mcq, card.
38. Network Byte Order is big-endian → b5 checks.
39. Host Byte Order is whatever the local machine uses → b5 checks.
40. Assume Host Byte Order is wrong and always convert → b5 eipe/why.
41. Conversions exist for short (2 bytes) and long (4 bytes), including
    unsigned variants → b6 checks, card.
42. Names read h/n + s/l: htons, htonl, ntohs, ntohl → b6 eipe, card.
43. Convert to network order outbound and to host order inbound
    → b6 checks.
44. There is no `stolh()`-style width conversion → b6 why-fails.
45. No standard 64-bit variants in the sockets API; floating point needs
    serialization → DEFERRED by the author (cards record the limitation).
46. Assume numbers in the chapter are Host Byte Order unless stated
    → b5/b6 explain.

### structs and lookups (b7–b9)
47. A socket descriptor is a plain `int` → card; DEFERRED for new checking
    because ch03 already taught and checked descriptor creation/use, and
    ch04 repeats the `int` only as a bridge into the structs.
48. `struct addrinfo` prepares socket address structures and supports host
    and service lookups; it is often the first call → b7 explain/checks.
49. `ai_flags` holds options such as AI_PASSIVE/AI_CANONNAME → b7 explain.
50. `ai_family` selects AF_INET, AF_INET6, or AF_UNSPEC → b7 checks.
51. `ai_socktype` selects SOCK_STREAM or SOCK_DGRAM; `ai_protocol` uses 0
    for "any" → b7 checks.
52. `ai_addrlen` is the byte size of `ai_addr` → b7 checks.
53. `ai_addr` points to a generic sockaddr (really sockaddr_in/_in6)
    → b7 eipe/checks.
54. `ai_canonname` holds the canonical hostname → b7 mcq.
55. `ai_next` links candidates; getaddrinfo returns a heap-allocated chain
    → b7 checks.
56. AF_UNSPEC makes lookup code IP-version-agnostic → b7 choose-better.
57. Use the first lookup result that works → b7 explain.
58. `struct sockaddr` exposes `sa_family` and `sa_data[14]` → b8 checks.
59. Packing sa_data by hand is unwieldy, so sockaddr_in is the parallel
    IPv4 layout → b8 explain/eipe.
60. A sockaddr_in pointer may be cast to sockaddr* and vice versa because
    the family field agrees at the front → b8 eipe/checks.
61. sockaddr_in fields: sin_family, sin_port, sin_addr, sin_zero[8]
    → b8 checks.
62. sin_family must be AF_INET; sin_port must be Network Byte Order
    → b8 checks.
63. sin_zero must be zeroed with memset → b8 why-fails.
64. `struct in_addr` holds a uint32_t `s_addr` in network order; it was
    historically a union but `s_addr` still works → b8 checks.
65. `struct sockaddr_in6` holds sin6_family, sin6_port, sin6_flowinfo,
    sin6_addr, sin6_scope_id → b9 checks.
66. `struct in6_addr` is a 16-byte `s6_addr` array → b9 checks.
67. IPv6 flowinfo and scope ID are deliberately postponed by the author
    → b9 explain note (deferred by source).
68. `struct sockaddr_storage` is large enough for either family; read
    `ss_family`, then cast → b9 checks.
69. sockaddr_storage's pad/align fields are implementation-specific and
    must be ignored → b9 explain, card.
70. recvfrom-style calls of unknown family need storage, not sockaddr_in
    → b9 choose-better.

### Text/binary conversion (b10–b11)
71. `inet_pton` converts presentation text to network binary (in_addr or
    in6_addr) → b10 checks, lab3.
72. Arguments are family, text, and destination → b10 checks.
73. Return >0 on success, 0 on malformed text, -1 on system error
    → b10 checks, quiz.
74. Check >0 before using the destination → b10 why-fails, lab3.
75. inet_addr/inet_aton are obsolete and IPv4-only → b10 checks.
76. inet_pton does numeric conversion only; it performs no DNS → b10 checks.
77. `inet_ntop` converts network binary to presentation text → b11 checks,
    lab3.
78. Arguments are family, address, output buffer, and buffer length
    → b11 checks.
79. INET_ADDRSTRLEN and INET6_ADDRSTRLEN size the output buffers
    → b11 checks, lab3.
80. Check the returned pointer before printing → b11 why-fails, lab3.
81. inet_ntoa is obsolete and IPv4-only → b11 checks.
82. inet_ntop does numeric formatting only; no DNS → b11 why-fails.

### Private networks / NAT (b12)
83. A firewall may translate internal addresses to external addresses with
    NAT → b12 explain/checks.
84. NAT is transparent; a beginner client does not implement it → b12 eipe.
85. Private IPv4 ranges: 10.x.x.x, 192.168.x.x, 172.16–31.x.x (RFC 1918)
    → b12 checks, card.
86. Networks behind NAT need not use reserved ranges but commonly do
    → b12 explain.
87. `192.0.2.x` is the documentation range, not a public assignment
    → b12 checks.
88. IPv6 private-style prefixes start `fdXX:` (or `fcXX:` in future) per
    RFC 4193 → b12 mcq, card.
89. NAT and IPv6 generally do not mix; the v6-to-v4 gateway is out of scope
    → DEFERRED under b12 with the author's own reason.
90. A remote host may see the firewall's public address while the local host
    sees a private address; NAT tracks flows to translate replies
    → b12 checks/explain.
91. Two hosts cannot directly share one public address without translation
    state → b12 why-fails/explain.

## Code boxes in the chapter: 11

1. IPv6 address example → quoted/taught in b2; checked by b2.
2. IPv6 compression-equivalence pairs → taught in b2; checked by b2.
3. `int` socket descriptor → DEFERRED for new checking: already taught and
   checked in ch03 (b1/b2), recorded on a ch04 card as a bridge.
4. `struct addrinfo` → taught in b7; checked by b7.
5. `struct sockaddr` → taught in b8; checked by b8.
6. `struct sockaddr_in` → taught in b8; checked by b8.
7. `struct in_addr` → taught in b8; checked by b8.
8. `struct sockaddr_in6` + `struct in6_addr` → taught in b9; checked by b9.
9. `struct sockaddr_storage` → taught in b9; checked by b9.
10. `inet_pton` IPv4/IPv6 calls → taught in b10; checked by b10 and lab3.
11. `inet_ntop` IPv4/IPv6 calls → taught in b11; checked by b11 and lab3.

No book-verbatim code is cut into an `example.code` stanza; every example is
an authored teaching construct built from the chapter APIs, so no
`adapted: true` declarations are needed.

## Check-kind coverage

- 102 block checks across 12 blocks (7–9 per block): 52/102 conceptual
  (predict/why-fails/eipe/choose-better/trace/spot-bug), above the half
  requirement.
- 2 interleaved checks with `from_chapter: ch03` (b6 from b4; b12 from b8).
- Correct-answer indices rotated per choice count: 3-choice 17/17/17,
  4-choice 9/9/8/8. No duplicate block-check stems and no duplicate
  concepts.
- `spot-bug` checks always carry an authentic compiler/ASan/tcpdump-style
  diagnostic log.

## Quiz: 43 standalone questions (11 intro / 20 core / 12 advanced),
## interleaved order, no stem duplicates any block-check q. Answer indices
## 11/9/9/8 across 0–3.

## Cards: 64 atomic SM-2 cards covering the idea units, including the
## socket-descriptor type, 64-bit conversion limitation, and deferred
## flowinfo/scope fields.

## Labs: 3 — subnet/netmask arithmetic (easy), byte-order conversion with
## wire bytes (medium), checked inet_pton/inet_ntop round trips (medium).
## All three verified fail-first on untouched stubs and pass with a reference
## solution on this host; every `test_cases[].expect` string matches exactly,
## and the interactive `run` output matches the documented expected text.

## Validation

`python main.py validate --book bgnet --chapter ch04 --strict` → `OK ch04/`

## Self-containedness audit (2026-10-27)

Applied after a learner-facing review of quiz/check wording. Replaced external
chapter/book pointers in all block-check stems and whys, quiz stems and whys,
test final checks, cards, lab descriptions, and block explanations with direct
wording or internal block ids (`(bN)`). Interleaved checks no longer mention
`Ch.2`; only their `from_chapter` metadata remains. `meta.yaml` retains the
bibliographic `source_ref`, which is not learner-facing.

Post-edit scan: zero `chapter`/`Ch.N` hits in `study.yaml` checks and explains,
`quiz.yaml`, `test.yaml`, `cards.yaml`, or `labs.yaml` (outside metadata/docs).
Re-ran `python main.py validate --book bgnet --chapter ch04 --strict` → `OK ch04/`.

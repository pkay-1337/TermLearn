# bgnet / ch03 generation notes (audit trail)

## ASK_USER interrogation — answered by operator directive ("read the prompts and get to work, just do what the prompt says")

1. Level: comfortable-in-C (default).
2. Depth: deep — 5–10 scaffolded checks per block (default).
3. Prioritize/skip: keep all; skip platform tangents. The telnot/telnet
   protocol aside is kept as an explain note under b4 (not a checkable
   fact); routing is deliberately out of scope per the author's own text,
   recorded as a deferred note under b8.
4. Lab difficulty + toolchain: easy-medium; C with the declared toolchain
   `gcc -Wall -std=c99 -O0`, 2 s timeout (packs/bgnet/book.yaml).
5. Explanation language: English.
6. Interleaved review: 2 checks pulling from ch02 (Intro — the client/server
   division). Content is fully self-contained (ch02 has no pack yet).

## Idea-unit enumeration (Karpicke & Blunt 2011 idea-unit method; every unit
## is taught, practiced, or explicitly deferred)

1.  Sockets = speaking to other programs via standard Unix file
    descriptors → b1 (explain, mcq, eipe)
2.  fd = an integer associated with an open "file" — network connection,
    FIFO, pipe, terminal, real on-the-disk file → b1 (explain, viz, mcqs,
    fillblank)
3.  socket() returns the socket descriptor; you communicate through it with
    send()/recv() → b2 (example, checks)
4.  read()/write() also work on sockets; send()/recv() offer greater control
    over data transmission → b2 (mcq + explain)
5.  Socket kinds: DARPA Internet addresses, Unix sockets (path names on a
    local node), CCITT X.25 (safely ignorable); guide covers Internet only
    → b3 (explain + scope mcq)
6.  Raw sockets exist and are powerful; deliberately out of scope → b3
    explain (deferred by the author's own text)
7.  SOCK_STREAM / SOCK_DGRAM vocabulary; datagram = "connectionless" (though
    they can be connect()'d if you really want) → b3 (fillblank, mcqs)
8.  Stream = reliable two-way connected communication; "1, 2" goes in, "1, 2"
    arrives; error-free → b3 (diagram, mcq) + b4
9.  Stream users: telnet, ssh (typed characters must arrive in order), web
    browsers over HTTP → b4 (mcq)
10. telnet to port 80, "GET / HTTP/1.0", RETURN twice → the HTML comes back
    → b4 explain + why-fails check
11. telnot aside: telnet is a spec'd networking protocol; the guide's telnot
    is telnet-like and does not implement that protocol → b4 explain note
    (platform/tooling aside per "skip platform tangents")
12. Stream sockets ride TCP (RFC 793): data arrives sequentially and
    error-free → b4 (fillblank, mcq, trace)
13. "TCP/IP": IP (RFC 791) deals with Internet routing and is not generally
    responsible for data integrity → b4 (mcq, why-fails)
14. Datagram facts: it may arrive; it may arrive out of order; if it arrives,
    the data within the packet is error-free → b3 (mcq) + b5 (example,
    predict, why-fails)
15. Datagram sockets use IP but not TCP — they use UDP (RFC 768); connectionless:
    build a packet, slap an IP header with destination info on it, send; no
    open connection maintained → b5 (explain, mcq, fillblank)
16. Datagram users: tftp, dhcpcd, multiplayer games, streaming audio, video
    conferencing → b5 (mcq)
17. tftp-style reliability: each packet must be ACKed by the recipient; no
    reply within ~5 s → retransmit until ACKed; essential when implementing
    reliable SOCK_DGRAM applications → b6 (example, diagram, checks)
18. Unreliable applications (games, audio, video) ignore drops or compensate
    cleverly (accursed lag) → b5 (explain)
19. Why an unreliable underlying protocol: speed and speed — fire-and-forget
    beats arrival bookkeeping; chat → TCP, 40 positional updates/s → UDP
    → b5 (mcq)
20. Data encapsulation: packet born → wrapped by TFTP → UDP → IP → Ethernet
    (hardware/physical layer) → b7 (art diagram, predict, fillblank)
21. Receiver strips in reverse: hardware strips the Ethernet header; kernel
    strips IP and UDP headers; the TFTP program strips the TFTP header →
    b7 (mcqs, why-fails)
22. Layered Network Model (ISO/OSI), 7 layers: Application, Presentation,
    Session, Transport, Network, Data Link, Physical → b8 explain + order
    check
23. Unix-consistent 4-layer model: Application (telnet, ftp), Host-to-Host
    Transport (TCP, UDP), Internet (IP and routing), Network Access
    (Ethernet, wi-fi) → b8 (diagram, fillblank)
24. The layers correspond to the encapsulation structure → b7 + b8
25. Socket programmer's view: you send() (stream) or sendto() (datagram);
    the kernel builds the Transport and Internet layers; the hardware does
    the Network Access layer; hardware/topology are transparent → b8
    (example, eipe, mcq)
26. Routing: the author explicitly declines to teach it (router strips the
    packet to the IP header, consults its routing table) → DEFERRED under
    b8 with reason "the author omits routing from ch.2 by design".

## Code boxes in the chapter: 0 (zero verbatim code boxes — the chapter is
## prose plus API names: socket(), send(), recv(), read(), write(),
## sendto(), SOCK_STREAM, SOCK_DGRAM). Every example.code stanza below is an
## authored teaching construct built strictly from those chapter APIs, so no
## `adapted: true` declarations are needed (nothing book-verbatim was cut).

## Check-kind coverage
- 54 block checks across 8 blocks (5–10 per block): every kind in the
  vocabulary appears where its research grounding fits (predict on model
  blocks, order/faded Parsons on syntax/algorithm, eipe/choose-better on
  design, trace for Notional-Machine state, spot-bug for kernel-issued
  handle traps).
- 2 interleaved checks with from_chapter: ch02 (b3, b8).
- Correct-answer indices rotated across 0–3 (verified by script post-gen).

## Quiz: 36 standalone questions (10 intro / 16 core / 10 advanced),
## interleaved order, no stem duplicates any block-check q.

## Labs: 2 (lab1 easy socket-probe, lab2 medium two-flavor probe) — verified
## fail-first on stubs and pass with a reference solution on this host.

# bgnet / ch05 generation notes (audit trail)

## ASK_USER interrogation — answered by operator directive ("read the prompts and get to work, just do what the prompt says")

1. Level: comfortable-in-C (default).
2. Depth: deep — 5–10 scaffolded checks per block (default). This is a
   70-line recap chapter, so eight small blocks carry the full checklist
   without inventing material.
3. Prioritize/skip: keep every one of the twelve migration steps and both
   code boxes. Skip no substantive idea. Full `getaddrinfo()` /
   `getnameinfo()` signatures, `freeaddrinfo()`, and multicast group
   selection belong to later chapters and are explicitly deferred.
4. Lab difficulty + toolchain: easy-medium, C with the declared toolchain
   `gcc -Wall -Wextra -std=c99`, matching `packs/bgnet/book.yaml`.
5. Explanation language: English.
6. Interleaved review: 2 checks from ch04 — b2 revisits `sin6_port` byte
   order (ch04 b8), b4 revisits `INET6_ADDRSTRLEN` (ch04 b11).

## Idea-unit enumeration (Karpicke & Blunt 2011 idea-unit method; every unit
## is taught, practiced, or explicitly deferred)

### Framing and the shortcut (b5, b8)
1.  The chapter is the short "for the impatient" version; almost everything
    was covered earlier → b5/b8 explain.
2.  First migration step: use `getaddrinfo()` to get all `struct sockaddr`
    information instead of packing structures by hand → b5 checks, cards.
3.  A lookup-driven design keeps the program IP-version-agnostic → b5
    eipe/choose-better, card.
4.  `getaddrinfo()` eliminates many of the subsequent hand-packing steps
    → b5 checks, b8 mcq.
5.  Any hard-coded IP-version choice should be wrapped in a helper function
    → b6 checks.
6.  A helper must actually honor its family input; otherwise it hides the
    IPv4 assumption → b6 why-fails.

### Family constants (b1)
7.  Change `AF_INET` to `AF_INET6` → b1 checks, card.
8.  Change `PF_INET` to `PF_INET6` → b1 checks, card.
9.  A family tag selects the address layout the kernel interprets → b1
    explain/viz.
10. Missing one family decision creates a mixed-family program → b1
    why-fails/choose-better.

### IPv6 wildcard (b2)
11. `INADDR_ANY` assignments become `in6addr_any` assignments → b2 checks.
12. `sa.sin_addr.s_addr = INADDR_ANY` marks "use my IPv4 address" → b2
    explain/checks.
13. `sa6.sin6_addr = in6addr_any` marks "use my IPv6 address" → b2 checks,
    lab1.
14. `IN6ADDR_ANY_INIT` can initialize a declared `struct in6_addr` → b2
    fillblank, card.
15. `in6addr_any` is an all-zero 16-byte object; assignment copies all 16
    bytes → b2 explain/viz/trace.
16. `IN6ADDR_ANY_INIT` is only an initializer; `in6addr_any` is the object
    used for later assignment → b2 choose-better, quiz, card.
17. Assigning the whole `sin6_addr` is legal; assigning its `s6_addr` array
    is not → b2 why-fails, b8/quiz.
18. The IPv6 wildcard means any local address → b2 explain/card.
19. `memset` still clears the surrounding structure before filling it
    → b2 trace/explain, b3.

### Structures and fields (b3)
20. Replace `struct sockaddr_in` with `struct sockaddr_in6` → b3 checks,
    card.
21. Add "6" to the fields as appropriate (`sin_family` → `sin6_family`,
    `sin_port` → `sin6_port`, `sin_addr` → `sin6_addr`) → b3 checks, lab1.
22. There is no `sin6_zero` field; do not rename `sin_zero` → b3 mcq/order,
    test final check.
23. Replace `struct in_addr` with `struct in6_addr` → b3 checks.
24. `in_addr.s_addr` becomes `in6_addr.s6_addr`, a 16-byte array → b3
    checks, cards.
25. The IPv6 structure is wider and holds a 16-byte address → b3
    predict/viz.
26. The family-specific layout means a struct/field mismatch is a real bug,
    not cosmetic → b3 eipe/spot-bug.
27. Ports remain 16-bit and still need network byte order → b2 interleaved,
    test final check, card.

### Converters (b4)
28. Replace `inet_aton()` / `inet_addr()` with `inet_pton()` → b4 checks,
    card.
29. Replace `inet_ntoa()` with `inet_ntop()` → b4 checks, card.
30. `inet_pton` returns 1 success, 0 malformed text, -1 system error → b4
    why-fails/predict, quiz.
31. Only a return of 1 makes the binary destination trustworthy → b4
    why-fails, lab2.
32. `inet_ntop` returns the destination pointer or NULL → b4 explain, lab2.
33. The family argument selects the text grammar and binary width → b4
    spot-bug, lab2, quiz.
34. `INET6_ADDRSTRLEN` sizes the IPv6 output buffer → b4 interleaved,
    lab1/lab2.
35. The old converters are IPv4-only, so they cannot stay after the family
    change → b4 choose-better, card.

### Lookups (b5, b6)
36. Replace `gethostbyname()` with the superior `getaddrinfo()` → b5 checks,
    card.
37. Replace `gethostbyaddr()` with the superior `getnameinfo()` → b5 checks,
    card.
38. Caveat: `gethostbyaddr()` can still work with IPv6, but new code should
    use `getnameinfo()` → b5 mcq/choose-better, card.
39. `getaddrinfo()` returns prepared sockaddr candidates; follow them
    instead of rebuilding bytes → b5 eipe/choose-better, b8.
40. Filtering results to one family defeats the version-agnostic benefit
    → b5 why-fails, quiz.
41. Helpers quarantine family-specific decisions for audit and tests → b6
    checks, card.
42. Dependency-ordered migration lets the compiler expose one coherent
    layer of errors at a time → b8 checks, card.

### Broadcast (b7)
43. `INADDR_BROADCAST` no longer works → b7 checks, card.
44. Use IPv6 multicast instead → b7 checks, card, test gate concept.
45. `INADDR_BROADCAST` is a 32-bit IPv4 value and cannot fill a 16-byte
    `in6_addr` → b7 why-fails/spot-bug, card.
46. Multicast delivers to a group of interested receivers; broadcast is not
    an IPv6 address form → b7 explain/eipe.
47. A cast only silences the compiler; it does not create a valid IPv6
    group address → b7 choose-better.

### Code boxes
48. Code box 1 (the `sa`/`sa6` wildcard pair) → reconstructed and checked in
    b2; its two assignments are the b2 fillblanks and lab1 behavior.
49. Code box 2 (`struct in6_addr ia6 = IN6ADDR_ANY_INIT;`) → b2 fillblank,
    card, and quiz.
50. The shortened second code box is not executed as a standalone example
    because it has no output; its declaration form is checked instead.

## Deferred items (explicit)

- Full `getaddrinfo()` / `getnameinfo()` argument lists, hints, result
  traversal, and `freeaddrinfo()`: forward reference to the next chapter on
  system calls. ch05 only teaches which lookup replaces which and why.
- Choosing and joining a specific IPv6 multicast group, plus routing scope:
  the chapter only says "use IPv6 multicast"; group semantics are out of
  scope here.
- The chapter's "Et voilà" closing has no technical content.
- `gethostbyaddr()`'s residual IPv6 capability is taught as a caveat, not
  explored as a preferred path.

## Check-kind coverage

- 61 block checks across 8 blocks (7–9 per block): 34/61 conceptual
  (predict/why-fails/eipe/choose-better/trace/spot-bug), above the half
  requirement.
- 2 interleaved checks with `from_chapter: ch04` (b2 from b8; b4 from b11).
- Answer indices balanced per choice count: 3-choice 6/6/6; 4-choice
  8/8/8/8. No duplicate block-check stems and no duplicate concepts.
- All `order` pools are scrambled and none uses a sequential
  `answer_order`; each includes a paired distractor with `distractor_why`.
- `spot-bug` checks carry authentic compiler or runtime diagnostic logs.

## Quiz: 32 standalone questions (9 intro / 14 core / 9 advanced),
## interleaved, no stem duplicates any block-check q. Answer indices
## 10/10/9 across 0–2. Full coverage: family switch, wildcard forms,
## struct/field migration, converters, lookups, broadcast, and order.

## Cards: 37 atomic SM-2 cards, including why/when cards for the wildcard
## form choice, helper encapsulation, unchecked `inet_pton` returns, and
## the unchanged port rules.

## Labs: 2 — IPv6 wildcard endpoint construction (easy-medium) and checked
## `inet_pton`/`inet_ntop` round trips that build an endpoint (medium).
## Both verified on this host:
##   - untouched starter: `commands.test` fails with exit code 1;
##   - reference implementation: `commands.test` and both `test_cases`
##     pass with byte-identical expected stdout and exit code 0.
## No network access is used in either lab.

## Validation

`python main.py validate --book bgnet --chapter ch05 --strict` → `OK ch05/`

## Self-containedness audit

- Block-check stems, quiz stems, explanations, answer choices, and cards now
  contain zero references to "the chapter", "Ch.4", the book, listings,
  figures, examples, "above", or "below". Source pointers in `why` are
  internal block ids such as `(b2)`.
- Every code-dependent check embeds its code or its complete scenario. Code
  lines that rely on a type are paired with the relevant declaration or a
  comment stating the rule being tested (for example, `ai_family` controls
  the lookup's returned family in the hint-migration spot-bug).
- The two interleaved checks remain self-contained: they state the port or
  buffer rule entirely in the question and `why`, while `from_chapter` is
  metadata only.
- `getaddrinfo()` / `getnameinfo()` are taught at the decision level, with
  the hints family field explained so the lookup questions can be answered
  without a later chapter. Their full argument contract remains deferred.
- Re-ran `python main.py validate --book bgnet --chapter ch05 --strict`
  after the audit: `OK ch05/`.

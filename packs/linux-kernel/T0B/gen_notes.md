# Authoring Notes & Evidence Provenance: T0B

Chapter: T0B — Source navigation: definitions, callers, and commits
Captured: 2026-11-19
Status: Complete & Verified

## Evidence-to-Block Mapping

| Evidence ID | Claim / Telemetry | Used in Blocks | Used in Labs / Quiz |
|---|---|---|---|
| `E-T0B-01` | Toolchain versions (rg 15.2.0, git 2.56.1, cscope 15.9) | b1, b2, b9 | meta.yaml |
| `E-T0B-02` | Header vs C definition vs call site (`sensor_init`) | b1 | lab1, b1-c1 |
| `E-T0B-03` | Word boundary filtering (`poll` vs `sensor_poll`) | b2 | lab1, b2-c1 |
| `E-T0B-04` | Path filtering with globs (`-g '*.h'`, `-g 'src/*.c'`) | b2 | lab1, b2-c2 |
| `E-T0B-05` | Surrounding context lines (`-C 2`) | b3 | b3-c2 |
| `E-T0B-06` | Macro token concatenation search trap (`temp_primary`) | b3 | b3-c1, quiz |
| `E-T0B-07` | Definition search anchored to column 0 (`^int sensor_init\(`) | b4 | lab1, b4-c1 |
| `E-T0B-08` | Caller enumeration with parenthesis (`sensor_poll\(`) | b5 | lab2, b5-c2 |
| `E-T0B-09` | Member vs variable disambiguation and leading dash (`->id`) | b5 | lab2, b5-c1 |
| `E-T0B-10` | Git commit object DAG anatomy (`git cat-file -p HEAD`) | b6 | b6-c1 |
| `E-T0B-11` | Git pickaxe symbol diff traversal (`git log -S`) | b7 | lab3, b7-c1 |
| `E-T0B-12` | Git function-range evolution (`git log -L`) | b7 | b7-c3 |
| `E-T0B-13` | Line-by-line author attribution (`git blame -n -L`) | b7 | b7-c2 |
| `E-T0B-14` | Historical kernel archaeology in `early-history.git` | b8 | b8-c1 |
| `E-T0B-15` | Semantic index database generation (`cscope -b -R`) | b9 | b9-c1 |
| `E-T0B-16` | Epistemic boundary of static search on function pointers | b10 | b10-c1 |

## Idea Unit Coverage
- Taught: 10/10 planned blocks in PLAN.md
- Checked: 50 block checks + 30 quiz questions + 4 final checks + 20 cards
- Deferred: None

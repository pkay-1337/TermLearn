# Notes

One file per chapter or experiment. Use the dossier template from
`../STUDY_METHOD.md`. Baseline: C reading and socket API vocabulary are already
present; kernel tools are learned here.

Naming:

```
chNN-slug.md            chapter dossier
tool-Tn-slug.md         tool chapter dossier (T0a–T8 incl. split chapters)
YYYY-MM-DD-slug.md      standalone experiment or surprise
phase-a-review.md       phase review
deep-dive-choice.md     decision record
```

Tool dossiers should include the mini-manual from the teach-back lab: three
invocations, one pitfall, one confusing column, and one limitation.

Rules:

- Write the question and prediction before the observation.
- Paste exact commands, not paraphrases.
- Keep raw logs in `notes/artifacts/`; link them from the note.
- Record the kernel version, commit, and config for every experiment.
- Mark uncertainty explicitly; do not smooth over a surprise.
- Link the source file and function for every claim.

Artifacts:

```
notes/artifacts/
  ftrace-2026-11-19-loopback.txt
  gdb-2026-11-20-schedule.log
  diff-veth-mtu.patch
  qemu-0.11-boot.log
```

Keep notes in git. Keep large build trees, tarballs, and QEMU images out of git.

---
description: "Show the full curriculum with completion flags. Optional arg: a track (foundations|core|workflow|plugins|domains) to filter to one module."
argument-hint: "[track]"
allowed-tools: ["Bash(python3:*)"]
---

The optional filter is: **$ARGUMENTS**

If `$ARGUMENTS` is empty, print the full curriculum:

```bash
python3 .claude/bin/state.py syllabus
```

If `$ARGUMENTS` is non-empty, filter to that track:

```bash
python3 .claude/bin/state.py syllabus --track "$ARGUMENTS"
```

After the output:

- **No filter:** briefly explain the five tracks (one line each), then remind the student they can jump anywhere with `/lesson <id>` — the canonical order is the recommended path.
- **Track filter:** explain in one sentence what that track teaches and what comes after it. Offer `/lesson <first-uncompleted>` if appropriate.

If the script exits non-zero with "unknown track", show the list of valid tracks and ask the student to pick one.

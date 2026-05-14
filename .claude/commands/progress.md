---
description: "Show the student's training progress. Optional arg: a track (foundations|core|workflow|plugins|domains) to filter the view."
argument-hint: "[track]"
allowed-tools: ["Bash(python3:*)"]
---

The optional filter is: **$ARGUMENTS**

If `$ARGUMENTS` is empty, show the full progress:

```bash
python3 .claude/bin/state.py show
```

If `$ARGUMENTS` is non-empty, treat it as a track name or alias and filter:

```bash
python3 .claude/bin/state.py show --track "$ARGUMENTS"
```

After the output, add a one-line summary of where the student is and what `/next` will take them to. Do not auto-advance — just inform.

If a track filter was used and that track is finished, congratulate them and offer the next track in the canonical order (foundations → core → workflow → plugins → domains).

If the script exits non-zero with "unknown track", relay the list of valid tracks back to the student.

---
description: "Show the student's training progress."
allowed-tools: ["Bash(python3:*)"]
---

Run the state script and show its output verbatim:

```bash
python3 .claude/bin/state.py show
```

Then, in plain language, add a one-line summary of where they are and what `/next` will take them to. Do **not** auto-advance — just inform.

If there are uncompleted lessons within the current track, point that out and offer to resume. If the current track is finished, offer the next track in the canonical order.

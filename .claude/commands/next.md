---
description: "Resume from where the student left off."
allowed-tools: ["Bash(python3:*)"]
---

Read the suggested next command:

```bash
python3 .claude/bin/state.py next
```

The output is a single slash command (e.g. `/lesson init-walkthrough`). Confirm with the student:

> "Riprendiamo da `<command>`? Sì / no — o vuoi altro?"

If yes, invoke the corresponding skill. If they want something else, ask what and route accordingly.

If the script returns `/syllabus` (no current pointer), greet them and run `/syllabus` so they can choose.

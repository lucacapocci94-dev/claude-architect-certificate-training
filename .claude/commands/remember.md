---
description: "Persist a note the student wants you to remember."
argument-hint: "<free text>"
allowed-tools: ["Bash(python3:*)"]
---

Persist the note:

```bash
python3 .claude/bin/state.py add-note "$ARGUMENTS"
```

Confirm briefly:

> "Annotato in `.claude/state/notes.md`. Lo rileggerò all'inizio di ogni sessione."

Use this for: project context, goals, blockers, naming conventions the student uses, anything they want you to recall in future sessions.

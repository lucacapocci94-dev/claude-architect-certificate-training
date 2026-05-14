---
description: "Reset training progress. Use --hard to also wipe profile and notes."
argument-hint: "[--hard]"
allowed-tools: ["Bash(python3:*)"]
---

Before doing anything, **confirm with the student**:

- Plain reset wipes lesson completions but keeps name, level, and notes.
- `--hard` wipes everything, including the profile.

Once confirmed:

```bash
python3 .claude/bin/state.py reset $ARGUMENTS
```

Then suggest `/start` if it was a hard reset, or `/syllabus` otherwise.

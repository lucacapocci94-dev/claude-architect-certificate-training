---
description: "Show the full curriculum with completion flags."
allowed-tools: ["Bash(python3:*)"]
---

Print the curriculum:

```bash
python3 .claude/bin/state.py syllabus
```

After the output, briefly explain the five tracks (one line each) and remind the student they can jump anywhere with `/lesson <id>` — but the canonical order is the recommended path.

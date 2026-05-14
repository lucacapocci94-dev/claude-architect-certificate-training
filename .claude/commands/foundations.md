---
description: "Start (or resume) the Foundations Zero track — from chat-only to Claude Code."
allowed-tools: ["Bash(python3:*)"]
---

Set the current track and route to the first uncompleted lesson of `foundations`:

```bash
python3 .claude/bin/state.py set-current --track foundations
python3 .claude/bin/state.py next
```

Use the second command's output to know which `/lesson <id>` to suggest. Briefly explain to the student what Foundations Zero covers (five micro-lessons: intro → install → first session → `/init` → CLAUDE.md) and confirm before launching the first lesson.

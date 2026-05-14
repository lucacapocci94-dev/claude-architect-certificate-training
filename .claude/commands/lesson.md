---
description: "Run a specific micro-lesson by id."
argument-hint: "<lesson-id>"
allowed-tools: ["Bash(python3:*)", "Read"]
---

The student wants to run lesson: **$ARGUMENTS**

Steps:

1. If `$ARGUMENTS` is empty, show `python3 .claude/bin/state.py next` and ask them to pick one.
2. Locate the matching skill at `.claude/skills/<lesson-id>/SKILL.md`. If it does not exist, list the valid ids from `python3 .claude/bin/state.py syllabus` and ask the student to pick.
3. Update the current pointer so resume works if the session is interrupted:

   ```bash
   python3 .claude/bin/state.py set-current --module "<lesson-id>"
   ```

4. Read the skill file and **deliver the lesson** following its instructions.
5. At the very end, after the student demonstrates understanding (a check question answered correctly, or an explicit "ok, capito"), call:

   ```bash
   python3 .claude/bin/state.py complete "<lesson-id>"
   ```

6. Suggest the next command but **do not auto-run** it. The student decides when to continue.

**Never** call `complete` without an explicit confirmation from the student. The progress file is sacred.

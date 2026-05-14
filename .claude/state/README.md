# State directory

This directory holds the student's local training state. Files here are git-ignored — each student has their own.

## Files

| File | Purpose |
|---|---|
| `profile.json` | Student profile: name, level, started_at, last_active |
| `progress.json` | Completed lessons, current module, next suggested step |
| `notes.md` | Free-form notes the student asked to remember (project context, goals, blockers) |
| `schema/profile.template.json` | Template for `profile.json` — committed |
| `schema/progress.template.json` | Template for `progress.json` — committed |

## How it works

1. **SessionStart hook** reads `profile.json` and `progress.json` and injects them into the model's context so Claude greets the student by name and knows where they left off.
2. **Lesson skills** instruct Claude to append a completion entry to `progress.json` via the `update-progress.sh` helper when a micro-lesson finishes.
3. **PreCompact hook** snapshots state to disk so nothing is lost when the context window is compacted.

If you ever want to start over, delete the three top files (`profile.json`, `progress.json`, `notes.md`) or run `/reset-progress` from inside Claude Code.

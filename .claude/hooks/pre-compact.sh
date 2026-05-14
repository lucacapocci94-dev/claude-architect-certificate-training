#!/usr/bin/env bash
# PreCompact hook — runs before the conversation is compacted.
# Emits a short manifest of training state so the post-compact context
# still knows where the student is. The state files themselves already
# persist between sessions; this is a belt-and-suspenders reminder.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
if ! command -v python3 >/dev/null 2>&1; then
  exit 0
fi
echo "<pre-compact-training-snapshot>"
python3 "$ROOT/bin/state.py" session-start 2>/dev/null || true
echo "</pre-compact-training-snapshot>"
echo ""
echo "Important: training progress is persisted in .claude/state/. After compaction, re-read .claude/state/progress.json and .claude/state/profile.json if you need full detail. Never invent progress that is not in those files."

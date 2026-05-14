#!/usr/bin/env bash
# SessionStart hook — runs at session startup, resume, clear, and compact.
# Output to stdout becomes additional context for the model.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
if ! command -v python3 >/dev/null 2>&1; then
  echo "<training-state-error>python3 not found — state hook disabled</training-state-error>"
  exit 0
fi
python3 "$ROOT/bin/state.py" session-start || {
  echo "<training-state-error>state.py session-start failed</training-state-error>"
  exit 0
}

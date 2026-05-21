#!/usr/bin/env bash
# Stop hook — runs when Claude finishes responding (end of turn).
# Shows the student a short "where you are" snapshot so they don't lose
# track between sessions: name, current track, % complete, next suggested
# lesson. Encourages them to commit one concrete action before closing.
#
# Output to stdout is shown to the model (which then surfaces it to the
# student); keep it short and on-topic.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  exit 0
fi

# Only nag at the end of a real teaching turn — not after every tool call.
# We approximate this by checking that .claude/state/profile.json has a name set.
PROFILE="$ROOT/state/profile.json"
if [ ! -f "$PROFILE" ]; then
  exit 0
fi

NAME="$(python3 -c "import json,sys; p=json.load(open('$PROFILE')); print(p.get('name') or '')" 2>/dev/null || echo "")"
if [ -z "$NAME" ]; then
  exit 0
fi

echo "<end-of-turn-reminder>"
python3 "$ROOT/bin/state.py" show 2>/dev/null | head -20 || true
echo ""
echo "Prima di chiudere: prova a fare UNA cosa concreta nel tuo progetto Angular"
echo "(es. far generare un componente, far scrivere un test, far spiegare un file)."
echo "Il tuo avanzamento è salvato in .claude/state/ e ti aspetta alla prossima sessione."
echo "</end-of-turn-reminder>"

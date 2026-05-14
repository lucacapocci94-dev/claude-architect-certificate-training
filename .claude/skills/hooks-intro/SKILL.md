---
description: "Core 4/9 — Hooks: the seven hook events (SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Notification, Stop, PreCompact), how to wire them in settings.json, how exit codes affect behavior (0 = ok, 2 = block), output-to-stdout-as-context pattern. Use when the student asks what a hook is, how to add a hook, the difference between SDK hooks and Claude Code hooks, or invokes /lesson hooks-intro."
command: "lesson hooks-intro"
track: "core-concepts"
duration_min: 9
---

# Core 4/9 — Hooks

**Lesson id:** `hooks-intro`
**Mark complete with:** `python3 .claude/bin/state.py complete hooks-intro`

---

## 1. What a hook is

A hook is a **shell command** the Claude Code harness runs automatically at specific moments — without asking the model. Two big consequences:

1. **Deterministic.** The model can't skip them. If you wire a hook to run tests before every commit, tests *always* run.
2. **Programmatic.** They can read files, post to APIs, decide to block an action — anything a shell command can do.

This is the difference between "asking Claude nicely to run tests" (probabilistic) and "the harness runs them every time" (deterministic). The certification exam loves this distinction.

## 2. The events you care about

| Event | Fires when | Typical use |
|---|---|---|
| `SessionStart` | A session starts, resumes, clears, or is created post-compact | Inject context (this very program injects training state) |
| `UserPromptSubmit` | The user hits enter | Pre-process the prompt, add reminders |
| `PreToolUse` | Before a tool runs | **Block** dangerous actions (exit 2) |
| `PostToolUse` | After a tool runs | Log, validate output, format files |
| `Stop` | The model is about to end its turn | Run lint/tests, require something before stopping |
| `Notification` | A notification fires | Forward to Slack/desktop |
| `PreCompact` | Right before compaction | Snapshot important state |

## 3. Wiring them in `settings.json`

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "npx prettier --write $CLAUDE_TOOL_INPUT_path" }
        ]
      }
    ]
  }
}
```

This auto-formats every file Claude edits. The `matcher` filters which tools trigger this hook.

## 4. Exit codes are the language

- **0** — success, business as usual.
- **2** — **block** the operation that triggered the hook. The model sees the hook's stderr as feedback and can react.
- Other non-zero — error, but doesn't block.

So a `PreToolUse` hook that does:

```bash
#!/usr/bin/env bash
if grep -q "rm -rf /" <<< "$CLAUDE_TOOL_INPUT_command"; then
  echo "Refusing: 'rm -rf /' is forbidden." >&2
  exit 2
fi
exit 0
```

…will block any `Bash` tool call containing `rm -rf /` and tell the model why.

## 5. Output → context

Anything a hook writes to **stdout** is appended to the model's context. This is how SessionStart hooks pre-load state. Look at this very repo's hook:

```bash
cat .claude/hooks/session-start.sh
```

It calls `state.py session-start`, which prints a `<training-state>` block. The next thing the model sees in the session is that block.

## 6. SDK hooks vs Claude Code hooks (exam trap)

The Agent SDK exposes hooks in code (Python/TypeScript callbacks). Claude Code hooks are shell commands in `settings.json`. **They are different mechanisms** with the same conceptual purpose. The exam will ask which to use when:

- Building a custom app on the SDK → SDK hooks (Python callbacks).
- Customising Claude Code behavior locally → settings.json hooks (shell).

## 7. Hands-on

Add a `Stop` hook that reminds the student to commit if there are uncommitted changes:

```bash
mkdir -p .claude/hooks
cat > .claude/hooks/remind-commit.sh <<'EOF'
#!/usr/bin/env bash
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
  echo "Hai modifiche non commitate. Vuoi che lo faccia io?"
fi
EOF
chmod +x .claude/hooks/remind-commit.sh
```

Then add to `.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      { "matcher": "", "hooks": [{ "type": "command", "command": "bash .claude/hooks/remind-commit.sh" }] }
    ]
  }
}
```

Restart `claude`. The reminder appears every time Claude ends a turn with uncommitted work.

## 8. Anti-patterns

- **Hooks that take 30 seconds.** They run on every event — keep them fast.
- **`PreToolUse` blocking everything.** Used to "secure" but breaks the agent. Block only what's truly forbidden.
- **Writing to the wrong stream.** Context-injection goes to **stdout**; failure reasons go to **stderr**.
- **No `set -e` in bash hooks.** Silent failures.

## 9. Check question

> "Vuoi che Claude **non possa mai** eseguire `rm -rf` su nessuna directory, indipendentemente da quello che decide il modello. Quale meccanismo usi?
> A. Lo scrivo in CLAUDE.md ('non usare mai rm -rf').
> B. Un `PreToolUse` hook che esamina il comando proposto ed esce con 2 se contiene `rm -rf`.
> C. Un `PostToolUse` hook che esamina il risultato.
> D. Una skill chiamata 'no-rm-rf'."

Correct: **B**. CLAUDE.md and skills are instructions the model *can* ignore. Hooks are deterministic enforcement.

## 10. Wrap up

> "Hai gli hook. La prossima cosa: il sistema che ti fa approvare/negare ogni azione — le **permission**. `/lesson permissions-intro`."

```bash
python3 .claude/bin/state.py complete hooks-intro
```

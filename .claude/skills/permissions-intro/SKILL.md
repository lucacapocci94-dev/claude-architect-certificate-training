---
description: "Core 5/9 — Permissions: allow / deny / ask, allowedTools and disallowedTools, scoping with patterns (Bash(git:*)), the relationship to hooks, and settings.json layering. Use when the student asks about permissions, allowed-tools, why Claude keeps asking before each command, or invokes /lesson permissions-intro."
command: "lesson permissions-intro"
track: "core-concepts"
duration_min: 7
---

# Core 5/9 — Permissions

**Lesson id:** `permissions-intro`
**Mark complete with:** `python3 .claude/bin/state.py complete permissions-intro`

---

## 1. The three states

Every tool call has one of three outcomes:

| State | What happens |
|---|---|
| **allow** | Tool runs without prompting |
| **ask** | The user gets a Y/N prompt (the default for risky tools) |
| **deny** | Tool refuses, the model sees the refusal and can replan |

Tuning this is how you go from "annoying — Claude asks 30 times per session" to "smooth — Claude only asks for the truly destructive stuff."

## 2. Patterns, not just names

Permissions support patterns:

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Edit",
      "Bash(git status)",
      "Bash(git diff:*)",
      "Bash(npm test:*)",
      "Bash(npm run lint:*)"
    ],
    "ask": ["Bash(npm install:*)"],
    "deny": [
      "Bash(rm -rf:*)",
      "Bash(curl:*)",
      "WebFetch"
    ]
  }
}
```

`Bash(git diff:*)` means "any `git diff` invocation with any args." `Bash(rm -rf:*)` means "always refuse `rm -rf <anything>`."

## 3. Where it lives

Like CLAUDE.md, permissions stack across layers:

| File | Scope |
|---|---|
| `~/.claude/settings.json` | All your projects |
| `<repo>/.claude/settings.json` | This project, all teammates |
| `<repo>/.claude/settings.local.json` | This project, only you (git-ignore it) |

Order of precedence on conflict: **local > project > user**. More specific wins.

## 4. The "allow once" / "allow always" prompt

When Claude wants to run something not in your allow list, the prompt offers:

- **Allow once** — run this exact call, ask again next time.
- **Allow always** — append a matching pattern to `settings.local.json` automatically. Watch out: this is per-user-per-project and persists.
- **Deny** — refuse. Model sees the refusal.

The exam tests: knowing that "allow always" writes to **local** (your personal file), not project. If you want it team-wide, you must edit `settings.json` by hand and commit it.

## 5. Permissions vs hooks (exam favourite)

Both can stop a tool call. They are not interchangeable:

- **Permissions** = static config. Easy to read, easy to share, no logic.
- **PreToolUse hooks** = arbitrary code. Use when you need to inspect *what's being done* (the actual command args) and decide.

Rule of thumb: if you can express the rule as a pattern, use **permissions**. If it requires inspecting the content (e.g. "block if the SQL contains DROP TABLE"), use a **hook**.

## 6. Hands-on

Have the student look at the current permissions for this very training repo:

```bash
cat .claude/settings.json
```

Then add a personal layer in `settings.local.json`:

```bash
cat > .claude/settings.local.json <<'EOF'
{
  "permissions": {
    "allow": ["Bash(python3 .claude/bin/state.py:*)"]
  }
}
```

…so the training program's `state.py` calls don't prompt anymore. Restart `claude`. Notice the difference.

(Make sure `.claude/settings.local.json` is git-ignored — it should be by default.)

## 7. Anti-patterns

- **Blanket `Bash(*)` in allow.** Defeats safety.
- **Personal allows in project file.** They leak to teammates. Use `.local.json`.
- **No deny list.** Even with all the asking, an accidental "allow always" on `rm -rf` is one click away. Deny it explicitly.
- **Forgetting WebFetch.** Default-deny WebFetch in any repo handling private code unless you trust the destination.

## 8. Check question

> "Lavori in un repo dove il team ha già un `.claude/settings.json` committato. Vuoi che `npm run dev` non ti chieda mai conferma, ma solo per te. Dove lo metti?
> A. Modifico `~/.claude/settings.json`.
> B. Aggiungo a `.claude/settings.json` e committo.
> C. Aggiungo a `.claude/settings.local.json` (git-ignored).
> D. Cambio nella CLAUDE.md."

Correct: **C**. Local settings = personal, not shared.

## 9. Wrap up

> "Permission sotto controllo. Prossimo: come delegare lavoro a un altro Claude — i **subagent**. `/lesson subagents-intro`."

```bash
python3 .claude/bin/state.py complete permissions-intro
```

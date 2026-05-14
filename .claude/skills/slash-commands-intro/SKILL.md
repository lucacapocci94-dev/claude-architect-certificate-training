---
description: "Core 2/9 — Custom slash commands: when to use, how to write one with frontmatter (description, argument-hint, allowed-tools), the difference between commands and skills. Use when the student asks how to make a slash command, what /foo does, the syntax for .claude/commands/*.md, or invokes /lesson slash-commands-intro."
command: "lesson slash-commands-intro"
track: "core-concepts"
duration_min: 7
---

# Core 2/9 — Custom slash commands

**Lesson id:** `slash-commands-intro`
**Mark complete with:** `python3 .claude/bin/state.py complete slash-commands-intro`

---

## 1. What a slash command actually is

A slash command is just a **markdown file** that Claude reads and treats as a prompt. When the student types `/foo`, Claude looks for `.claude/commands/foo.md` (project) or `~/.claude/commands/foo.md` (user) and uses the file's content as the next user message — with `$ARGUMENTS` expanded.

No magic. It's a prompt template you reuse.

## 2. Why bother

Three reasons:

1. **Encode repeated workflows.** "Review the diff, suggest tests, run them." → write it once as `/review`, reuse forever.
2. **Standardize across the team.** Everyone gets the same review prompt, not whatever each person remembers to ask.
3. **Reduce keystrokes.** `/ship` is shorter than typing the whole release procedure.

## 3. The frontmatter

A minimal command:

```markdown
---
description: "Run all tests and lint, then summarize failures."
allowed-tools: ["Bash(npm:*)", "Read"]
---

Run `npm test` and `npm run lint`. If anything fails, list each failure as a bullet point with the file path and the one-line reason. Do not propose fixes — that's a separate command.
```

Frontmatter fields:

| Field | Purpose |
|---|---|
| `description` | Shown in the `/` menu so the student picks the right one |
| `argument-hint` | A hint shown in the menu, e.g. `<PR-number>` |
| `allowed-tools` | Pre-allowed tools so the user isn't prompted (use carefully) |
| `model` | Override model for this command (e.g. `haiku` for cheap commands) |

## 4. `$ARGUMENTS`

If the student runs `/lesson rules-and-memory`, then inside `lesson.md` you can write:

```markdown
The student wants to run lesson: **$ARGUMENTS**
```

…and `$ARGUMENTS` becomes `rules-and-memory`. Simple string substitution.

## 5. Commands vs skills — the right distinction

This trips everyone up. Quick cheat-sheet:

| | Slash command | Skill |
|---|---|---|
| File | `.claude/commands/foo.md` | `.claude/skills/foo/SKILL.md` |
| Trigger | Student types `/foo` | Claude auto-invokes when description matches the user's intent |
| Visibility to model at startup | Loaded only when invoked | Description is always visible in the skill catalog |
| Use for | Explicit, named workflows the student initiates | Background knowledge / playbooks Claude pulls in when relevant |

A common pattern (this very training program uses it): write a skill for the **content**, write a slash command for the **entrypoint**. The command is two lines that says "do the skill at `.claude/skills/foo/SKILL.md`".

## 6. Hands-on

Have the student create a `/log` command in their project that summarises recent git activity:

```bash
mkdir -p .claude/commands
cat > .claude/commands/log.md <<'EOF'
---
description: "Summarise the last 10 commits in plain English."
allowed-tools: ["Bash(git log:*)"]
---

Run `git log -10 --oneline` and summarise the last 10 commits in 2-3 sentences. Group by theme if you can spot one (features, fixes, refactor).
EOF
```

Then in `claude`, type `/` — `/log` should appear in the menu. Run it.

## 7. Anti-patterns

- **Allowing `Bash(*)` blanket.** Defeats the permission system. Allow specific subcommands only: `Bash(git log:*)`, `Bash(npm test)`.
- **One huge command that does ten things.** Split. Compose with `/cmd-a then /cmd-b`.
- **Putting personal commands in project `.claude/commands/`.** Put them in `~/.claude/commands/`.

## 8. Check question

> "Vuoi un comando team-wide che apra il template di code review e lo applichi al diff attuale. Dove lo metti?
> A. `.claude/commands/review.md`, committato nel repo.
> B. `~/.claude/commands/review.md`, solo sulla tua macchina.
> C. In CLAUDE.md alla radice del repo.
> D. In una rule sotto `.claude/rules/review.md`."

Correct: **A**. Team-wide = project level, committed. (B is for your personal commands. D is for instructions that activate by file path, not by user invocation.)

## 9. Wrap up

> "Hai capito i command. La prossima leva è più potente: le **skill**. `/lesson skills-intro`."

```bash
python3 .claude/bin/state.py complete slash-commands-intro
```

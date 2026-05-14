---
description: "Core 3/9 — Skills: how SKILL.md files become auto-activated playbooks, frontmatter (description, allowed-tools, context), when to use a skill vs a slash command, skill discovery via description. Use when the student asks what a skill is, how to make one, where to put SKILL.md, or invokes /lesson skills-intro."
command: "lesson skills-intro"
track: "core-concepts"
duration_min: 8
---

# Core 3/9 — Skills

**Lesson id:** `skills-intro`
**Mark complete with:** `python3 .claude/bin/state.py complete skills-intro`

---

## 1. The mental model

A **skill** is a playbook Claude can pick up *on its own* when it spots the right situation. The student does not type `/skill-name`. They describe what they want; Claude reads the skill catalog, matches the description, and follows the SKILL.md.

Slash command = the student summons it.
Skill = Claude summons it.

## 2. Anatomy

A skill is a directory under `.claude/skills/` (project) or `~/.claude/skills/` (user) containing a `SKILL.md` file:

```
.claude/skills/
  database-migration/
    SKILL.md
    examples/
      add-column.sql
      drop-index.sql
```

The `SKILL.md` has frontmatter and a body:

```markdown
---
description: "Use when the user wants to write or review a database migration. Covers adding/dropping columns safely under load, backfill patterns, and rollback. Triggered by phrases like 'write a migration', 'add a column', 'is this migration safe'."
allowed-tools: ["Read", "Edit", "Bash(psql:*)"]
---

# Database migration playbook

Step 1: Check the table size with `SELECT count(*) FROM <table>`.
Step 2: If > 1M rows, propose a phased migration (add nullable, backfill, set NOT NULL).
...
```

## 3. The `description` is everything

The description is how Claude **decides** to use the skill. A bad description is invisible; a good one is specific about triggers.

**Bad:** `"Database stuff."`

**Good:** `"Use when the user wants to write or review a database migration. Covers safely adding columns under load, backfill patterns, and rollback. Triggered by phrases like 'add a column', 'write a migration', 'is this migration safe to apply'."`

Notice: includes **what** the skill covers and **example trigger phrases**. This pattern is what gets the skill matched reliably.

## 4. When to use a skill (vs CLAUDE.md or a command)

| Situation | Choice |
|---|---|
| A rule that applies everywhere | CLAUDE.md |
| A rule that applies to certain files | `.claude/rules/foo.md` with globs |
| A long playbook only relevant in specific tasks | **Skill** |
| A workflow the user explicitly invokes | Slash command |

The big win of skills over CLAUDE.md: skills are **not loaded into context unless triggered**. CLAUDE.md is always in context. A 500-line skill costs nothing on a session where its topic doesn't come up.

## 5. Hands-on

Have the student create a small skill in their project:

```bash
mkdir -p .claude/skills/changelog-entry
cat > .claude/skills/changelog-entry/SKILL.md <<'EOF'
---
description: "Use when the user is about to commit and wants to add an entry to CHANGELOG.md. Follows Keep a Changelog format. Triggered by 'update the changelog', 'add a changelog entry', 'document this change'."
allowed-tools: ["Read", "Edit"]
---

# Changelog entry playbook

1. Open `CHANGELOG.md`.
2. Find the `[Unreleased]` section.
3. Add the entry under the matching category: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.
4. Phrase it past tense, user-facing: "Fixed login redirect loop when 2FA was enabled."
EOF
```

Now in `claude`, ask: "ho appena aggiunto il rate limiting al login — aggiorna il changelog." Watch Claude pull in the skill description and follow it.

## 6. Skills you didn't write

Skills can come from three places:

1. **Yours** — what you author for your team
2. **Anthropic's built-ins** — shipped with Claude Code
3. **Plugins** — third-party packages of skills (covered in the Plugins track)

The certification exam tests recognising **when to author a custom skill** vs **when to use an existing one**. Default to use; build only when nothing fits.

## 7. Anti-patterns

- **Vague description.** Skill never gets matched. Pre-mortem: re-read the description as a stranger — would they know when to use it?
- **Skill that duplicates CLAUDE.md.** If it's always relevant, it belongs in memory, not in a skill.
- **Skills with side effects baked in.** Skills should explain *how* — they should not auto-execute destructive operations without prompting.

## 8. Check question

> "Hai una procedura di 4 step per gestire le rotazioni di credenziali. Vuoi che Claude la segua **solo quando** l'utente parla di credenziali o di rotazione segreti, non sempre. Cosa scegli?
> A. La metto in CLAUDE.md alla radice.
> B. La metto in `~/.claude/CLAUDE.md`.
> C. La scrivo come skill in `.claude/skills/credential-rotation/SKILL.md` con una description che elenca i trigger.
> D. Apro un issue su GitHub di Anthropic per richiederla."

Correct: **C**. Skills load on demand; CLAUDE.md would force them into every session.

## 9. Wrap up

> "Capito skill e command. Adesso il meccanismo che fa partire codice in automatico: gli **hook**. `/lesson hooks-intro`."

```bash
python3 .claude/bin/state.py complete skills-intro
```

---
description: "Foundations 5/5 — CLAUDE.md hierarchy: user / project / directory levels, @imports, and which file wins. Use when the student wants to learn about CLAUDE.md hierarchy, memory layers, @imports, ~/.claude/CLAUDE.md vs project CLAUDE.md, or invokes /lesson claude-md-hierarchy."
command: "lesson claude-md-hierarchy"
track: "foundations"
duration_min: 8
---

# Foundations 5/5 — The CLAUDE.md hierarchy

**Lesson id:** `claude-md-hierarchy`
**Mark complete with:** `python3 .claude/bin/state.py complete claude-md-hierarchy`

---

## 1. The three layers

There is not one CLAUDE.md — there are three layers, **all loaded automatically at session start**, in this order of priority (lower beats higher when they conflict):

| Layer | Location | Scope | Example contents |
|---|---|---|---|
| **User** | `~/.claude/CLAUDE.md` | Every project, every machine of yours | "Always answer in Italian", "I prefer pnpm", personal coding style |
| **Project** | `<repo>/CLAUDE.md` | This repo, every team member | Build commands, test commands, repo layout, domain language |
| **Directory** | `<repo>/<subdir>/CLAUDE.md` | Only files inside that subdir | Per-package conventions in a monorepo |

Critical point: **all three are read every time**. They don't replace each other — they **stack**.

## 2. When to put what where

This is where most students get it wrong. Make them practice the assignment:

| Instruction | Where it goes |
|---|---|
| "Use 2-space indent in this repo" | Project |
| "Always reply in Italian unless I switch to English" | User |
| "The `packages/api/` subdir uses class-based controllers; the rest uses functions" | Directory (`packages/api/CLAUDE.md`) |
| "Never commit without running `npm run lint`" | Project |
| "I work at Accenture; prefer Azure when suggesting clouds" | User |
| "This monorepo's `apps/web/` uses React 19 and Server Components" | Directory |

Wrong assignments are how you end up with conflicting instructions across the team. Project CLAUDE.md should never contain personal preferences.

## 3. `@imports` — keeping CLAUDE.md small

A CLAUDE.md can pull in other files with `@path/to/file.md`. This is how you keep the main file small and split detail into reference docs:

```markdown
## Build

@docs/build.md

## Testing

@docs/testing.md
```

When Claude reads CLAUDE.md, it follows `@imports` and inlines the content. Common pattern:

```
CLAUDE.md             <- short, ~50 lines
docs/
  build.md            <- expand on build
  testing.md          <- expand on testing
  conventions.md      <- naming, error handling, …
```

This keeps the main CLAUDE.md scannable and lets you @ specific docs only when needed.

## 4. `.claude/rules/` — the next level

Once a project has many concerns, even split docs get heavy. The pattern is:

```
.claude/rules/
  testing.md
  error-handling.md
  security.md
```

You reference them from CLAUDE.md with @import, OR — and this is the modern pattern — you mark them with **glob frontmatter** so they only activate for specific files. We cover that in `/lesson rules-and-memory` (Core Concepts 1/9).

## 5. Hands-on (3 minutes)

Have the student:

1. Open / create `~/.claude/CLAUDE.md` (their **user** memory).
2. Add a line like:

   ```
   - Reply in Italian unless I switch to English.
   - Prefer pnpm over npm.
   ```

3. Quit and re-launch `claude` in any project. Ask anything. Confirm the reply is in Italian.

That's it — they've now configured both **personal** (user) and **per-project** (project) memory.

## 6. The conflict rule

When user and project disagree, **project wins** for that repo. Why: the project is shared with the team, and the team's conventions trump the individual's preferences. Example:

- User: "Use pnpm everywhere."
- Project: "This repo uses npm for legacy reasons."
- Result inside this repo: npm. Outside: pnpm.

## 7. Check question

> "Lavori su un monorepo dove `packages/api/` usa controller a classi e `packages/web/` usa solo funzioni. Dove metti la regola 'usa controller a classi'?
> A. `~/.claude/CLAUDE.md`
> B. `<repo>/CLAUDE.md` (radice)
> C. `<repo>/packages/api/CLAUDE.md`
> D. Nel codice, come commento all'inizio di ogni file."

Correct: **C**. Directory-level CLAUDE.md scopes the rule to exactly where it applies. Putting it in B leaks it to `packages/web/`.

## 8. Wrap up — Foundations complete!

This closes the Foundations Zero track. They can now:

- Install and run Claude Code
- Have their first session and survive the permission prompts
- Generate, edit, and trust a CLAUDE.md
- Split memory across user / project / directory layers

Suggest:

> "Foundations completata. Adesso entriamo nel cuore: le **Core Concepts**. Si parte da `rules-and-memory` che approfondisce quello che hai appena visto, e va fino agli hook e all'MCP. `/core` per cominciare."

```bash
python3 .claude/bin/state.py complete claude-md-hierarchy
python3 .claude/bin/state.py set-current --track core-concepts --module rules-and-memory --next "/lesson rules-and-memory"
```

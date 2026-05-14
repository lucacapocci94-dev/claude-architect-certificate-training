---
description: "Core 1/9 — Rules and memory: how CLAUDE.md, @imports, .claude/rules/ with glob frontmatter, and ~/.claude work together to shape Claude's behavior. Use when the student asks about rules, memory layers, path-specific rules, glob frontmatter on rules, or invokes /lesson rules-and-memory."
command: "lesson rules-and-memory"
track: "core-concepts"
duration_min: 8
---

# Core 1/9 — Rules & memory: making Claude behave

**Lesson id:** `rules-and-memory`
**Mark complete with:** `python3 .claude/bin/state.py complete rules-and-memory`

---

## 1. Recap and extend

In Foundations 5 we saw the three CLAUDE.md layers (user / project / directory). Now we go one level deeper: **rules**, which are instructions that activate only when relevant.

The problem: dumping every rule into CLAUDE.md makes it bloat. By month 3 of a real project, you have rules about testing, error handling, logging, security, naming, commit messages, performance, … 80 rules and 600 lines. Claude reads it all every session — token cost climbs and the signal-to-noise ratio drops.

The fix: **path-specific rules**.

## 2. The `.claude/rules/` pattern

Move rules out of CLAUDE.md and into focused files under `.claude/rules/`:

```
.claude/
  rules/
    testing.md
    error-handling.md
    security.md
    react-components.md
```

CLAUDE.md keeps only the high-level overview and either:
- `@imports` rules unconditionally, or
- Lets each rule activate based on the **files being edited**, via glob frontmatter.

## 3. Glob frontmatter — the magic

A rule file with frontmatter:

```markdown
---
description: "React component conventions"
globs: ["src/components/**/*.tsx", "src/pages/**/*.tsx"]
---

- Use function components, never classes.
- Co-locate tests as `*.test.tsx`.
- Props must be a typed interface, not inline.
```

When Claude is about to edit `src/components/Button.tsx`, this rule is **automatically pulled into context**. When editing `server/api.ts`, it stays out. Per-task token spend drops dramatically.

This is one of the things the certification exam tests — **proportionate context loading**.

## 4. When to use which mechanism

| You want… | Use… |
|---|---|
| Behavior that applies everywhere, always | Project CLAUDE.md body |
| A block of detail referenced from CLAUDE.md | `@docs/foo.md` import |
| Behavior that only matters when editing certain files | `.claude/rules/foo.md` with `globs:` |
| Personal preference across all projects | `~/.claude/CLAUDE.md` |

## 5. Hands-on (5 minutes)

Have the student create one path-specific rule in their project:

```bash
mkdir -p .claude/rules
cat > .claude/rules/testing.md <<'EOF'
---
description: "Testing conventions"
globs: ["**/*.test.ts", "**/*.spec.ts"]
---

- Use Vitest, not Jest.
- One assertion per test where possible.
- No snapshot tests for anything non-trivial.
EOF
```

Then in `claude`, ask "scrivi un test per la funzione foo" and watch — the rule appears in context only when test files are involved.

## 6. Anti-patterns to flag (exam-relevant)

1. **A single 900-line CLAUDE.md.** Token waste, instructions blur into each other.
2. **Vague rules** ("write clean code"). Useless. Rules must be checkable.
3. **Contradictory layers.** User says "always TypeScript", project is JS-only. Project wins, but the friction means the user-level rule is in the wrong place.
4. **Rules in code comments.** They rot and Claude won't see them unless it happens to read that file.

## 7. Check question

> "Il tuo monorepo ha un sottosistema in Python (microservizio) e uno in TypeScript (frontend). Vuoi una regola 'usa `ruff` invece di `black`' che si attivi solo quando si modifica codice Python. Dove la metti?
> A. In CLAUDE.md alla radice del repo.
> B. In `~/.claude/CLAUDE.md`.
> C. In `.claude/rules/python.md` con `globs: ['**/*.py']`.
> D. In un commento all'inizio di ogni file `.py`."

Correct: **C**. Path-specific, automatic activation, no token cost when editing TS files.

## 8. Wrap up

> "Hai messo a posto la memoria. Adesso vediamo l'altra leva per estendere Claude Code: gli slash command custom. `/lesson slash-commands-intro`."

```bash
python3 .claude/bin/state.py complete rules-and-memory
```

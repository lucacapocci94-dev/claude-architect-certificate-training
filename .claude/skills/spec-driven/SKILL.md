---
description: "Workflow 2/5 — Spec-driven development: turning a brainstorm into a written spec, the spec format (goal, non-goals, constraints, acceptance criteria), why specs survive /clear, and using specs as the source of truth for code. Use when the student asks what a spec is, how to write one, why write a spec before code, or invokes /lesson spec-driven."
command: "lesson spec-driven"
track: "workflow"
duration_min: 8
---

# Workflow 2/5 — Spec-driven development

**Lesson id:** `spec-driven`
**Mark complete with:** `python3 .claude/bin/state.py complete spec-driven`

---

## 1. What a spec actually is

A spec is a short markdown file that captures **what** to build, **why**, and **how we'll know it's done** — *before* any code. Not a design doc. Not a PRD. A working artifact, 1-3 pages.

Three reasons it matters with Claude Code:

1. **Survives `/clear`.** Brainstorm context dies on clear; the spec on disk doesn't.
2. **Reviewable.** You read the spec for 2 minutes. You read 800 lines of code for 30.
3. **Multi-session.** Day 1 you write the spec. Day 2 someone else (or another Claude) implements it.

## 2. The spec template

```markdown
# Spec: <one-line title>

## Goal
What we are building. Two sentences max.

## Why
The problem this solves. One short paragraph.

## Non-goals
What this explicitly does NOT solve, even though it's nearby. Critical for scope.

## Constraints
- Performance: e.g. "<200ms p95"
- Compatibility: e.g. "must work with current Postgres 13"
- Security: e.g. "no PII in logs"

## Approach
Bullet points of the high-level design. Not code yet.

## Acceptance criteria
A checklist a reviewer can run through.
- [ ] Endpoint /foo returns 200 for ...
- [ ] Tests cover the rate-limited case
- [ ] No breaking changes to /bar
```

Keep each section short. If the spec exceeds 2-3 pages, you're really writing a design doc — split it.

## 3. The brainstorm → spec pipeline

After the brainstorming lesson, the natural next prompt is:

> "Basato su queste risposte, scrivimi uno spec in `docs/specs/<name>.md` seguendo il template: Goal, Why, Non-goals, Constraints, Approach, Acceptance Criteria. Tienilo corto."

Claude writes the file. You read it. You correct. You commit it. **Now** you `/clear` and start implementing — from the spec, not from the conversation.

## 4. Specs as the contract

Once the spec exists, every implementation prompt becomes:

> "Implementa lo step 1 della spec in `docs/specs/csv-export.md`. Niente fuori scope."

The spec is the *contract*. Whatever isn't in the spec doesn't get built. This single rule eliminates 80% of scope creep that comes from chatting with an LLM.

## 5. Specs in `.claude/`

Some teams put specs under `docs/specs/`; others use `.claude/specs/`. Either works. The win is that the spec is **findable by future Claude sessions** — they're text files on disk in the repo. Claude can grep them when picking up work.

## 6. Specs vs plan mode

These are not the same:

| | Spec | Plan mode |
|---|---|---|
| Lifetime | Long-lived markdown file | One turn inside one session |
| Audience | Humans and future sessions | Right now |
| Detail | Goal, scope, acceptance | Files to touch, in what order |

A typical flow uses both: write a spec, then in plan mode propose a concrete plan to deliver one slice of the spec, then approve and execute.

## 7. Hands-on

Pick a real task in the student's project. Have them:

1. Brainstorm (lesson 1).
2. Ask Claude to write `docs/specs/<task>.md` using the template above.
3. Edit it — kill anything they don't actually want.
4. Commit the spec.
5. `/clear`.
6. New session: "Leggi `docs/specs/<task>.md`. Proponi un piano per implementare la sezione Approach, una slice alla volta."
7. Approve, build, repeat.

## 8. Anti-patterns

- **Spec written after the code.** Useless; that's just documentation, not a contract.
- **A 12-page spec.** Means you're hiding from doing the work. Cut it.
- **Spec without acceptance criteria.** "Done" becomes opinion.
- **Spec ignored after writing.** If the implementation drifts, update the spec or the code — never let them disagree.

## 9. Check question

> "Hai brainstormato con Claude per 20 minuti, c'è un design buono in testa, il contesto della sessione è grande. Cosa fai prima di scrivere codice?
> A. Vado dritto a codare nella stessa sessione, così non perdo il contesto.
> B. Faccio scrivere a Claude lo spec in `docs/specs/<task>.md`, committo, `/clear`, ricomincio dal file.
> C. Mi salvo gli appunti in un file txt locale e basta.
> D. `/compact` e via."

Correct: **B**. Spec on disk = persistent context, reviewable artifact, no token cost on the next session.

## 10. Wrap up

> "Spec scritta. Ora pianifichiamo l'implementazione con il **plan mode** più in profondità. `/lesson plan-deep`."

```bash
python3 .claude/bin/state.py complete spec-driven
```

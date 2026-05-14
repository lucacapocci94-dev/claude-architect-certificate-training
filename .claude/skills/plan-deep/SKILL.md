---
description: "Workflow 3/5 — Plan mode in depth: writing actually-good plans, splitting plans into reviewable slices, plan ↔ spec relationship, approving partial plans, when to plan inside plan mode vs in markdown. Use when the student wants to go deeper on planning, asks how to make Claude plan well, how big a plan should be, or invokes /lesson plan-deep."
command: "lesson plan-deep"
track: "workflow"
duration_min: 7
---

# Workflow 3/5 — Planning in depth

**Lesson id:** `plan-deep`
**Mark complete with:** `python3 .claude/bin/state.py complete plan-deep`

---

## 1. Recap: plan mode

Core Concepts 7/9 covered the **mechanics** of plan mode: Shift+Tab toggles it, Claude proposes a plan via `ExitPlanMode`, you approve or reject.

This lesson is about **writing good plans** — a craft, not a feature.

## 2. What a "good plan" looks like

A good plan from Claude has these properties:

1. **File-level concrete.** It says "edit `src/middleware/rateLimit.ts`", not "modify the middleware layer."
2. **Ordered.** Steps are sequenced; dependencies are explicit.
3. **Sliceable.** It can be cut after step 3 and still produce a working state.
4. **Acceptance-linked.** Each step ties back to a line in the spec.
5. **Free of vague verbs.** No "improve", "refactor", "clean up" without specifics.

Plans that fail these tests will fail in execution. Reject and ask for a better plan — that's free.

## 3. The plan-shrinking prompt

When Claude proposes a 12-step plan, the right move is usually:

> "Troppi step. Dammi una versione che fa solo la prima feature end-to-end (slice 1). Le altre dopo."

This is the **vertical slice** principle: ship a thin slice that works, then add another. Beats "build all the foundations, then connect them" almost every time, because you find the problems early.

## 4. Plans on disk

Plan mode lives in one turn. But for larger work, the better pattern is:

1. Use plan mode to get the first sketch.
2. Ask Claude to write it to `docs/plans/<task>.md`.
3. Edit it, slice it.
4. Implement slice by slice, one session per slice if needed.

This pairs perfectly with the spec from the previous lesson. Spec answers "what." Plan answers "in what order."

## 5. The "first commit" rule

A plan is healthy if it produces a deployable state at the end of step 1. If step 1 alone leaves the code broken, the plan is too coarse — split it.

Apply this even to refactors: "step 1: introduce the new function alongside the old one, all tests pass." Not: "step 1: change every call site simultaneously."

## 6. Hands-on

Pick the spec they wrote in the previous lesson. Inside `claude`:

1. Enter plan mode (Shift+Tab twice).
2. Say: "Leggi `docs/specs/<task>.md`. Proponi un piano per la prima slice end-to-end."
3. When Claude proposes — apply the five tests above. If anything's vague, push back.
4. Once happy, **before approving**, ask: "scrivi questo piano in `docs/plans/<task>.md` e poi fermati."
5. Approve. Claude writes the file. Exit plan mode.
6. New session (`/clear` first): "Implementa la slice 1 del piano in `docs/plans/<task>.md`. Niente fuori scope."

## 7. Anti-patterns

- **Approving a 15-step plan.** You won't remember step 4 by step 12. Slice.
- **Plans that are also code.** Plans are prose. The first code line should come *after* the plan is approved.
- **Re-planning every session.** If a plan exists on disk, read it; don't redo it.
- **Plans without rollback.** For any risky step, the plan should say how to undo it.

## 8. Check question

> "Stai per rifare il sistema di autenticazione. Lo spec è scritto. Claude propone un piano di 18 step che fa tutto in un colpo. Cosa fai?
> A. Approvo, è chiaro e dettagliato.
> B. Rigetto e chiedo solo la prima slice end-to-end, lasciando il resto per dopo.
> C. Cambio modello a Opus per piani più lunghi.
> D. Faccio io a mano per non rischiare.'"

Correct: **B**. 18 step monolithic plan = high risk, low reviewability, no early feedback. Vertical slice.

## 9. Wrap up

> "Sai pianificare. Ora il loop tra te e Claude: come **iterare** bene. `/lesson iterative-refinement`."

```bash
python3 .claude/bin/state.py complete plan-deep
```

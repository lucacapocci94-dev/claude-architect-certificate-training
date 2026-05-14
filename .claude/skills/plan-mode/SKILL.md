---
description: "Core 7/9 — Plan mode: ExitPlanMode, when to plan vs execute, how shift+tab toggles it, why planning first saves time on non-trivial tasks. Use when the student asks about plan mode, ExitPlanMode, how to plan before code, or invokes /lesson plan-mode."
command: "lesson plan-mode"
track: "core-concepts"
duration_min: 6
---

# Core 7/9 — Plan mode

**Lesson id:** `plan-mode`
**Mark complete with:** `python3 .claude/bin/state.py complete plan-mode`

---

## 1. What plan mode does

In plan mode, Claude **cannot** edit files, write files, or run side-effecting commands. It can only read, search, and think. At the end of its analysis it presents a plan and asks for approval via `ExitPlanMode`.

This is the "measure twice, cut once" lever for non-trivial work.

## 2. How to enter / exit

- Inside `claude`, press **Shift+Tab** twice to toggle plan mode on.
- The footer shows "plan mode" while active.
- When Claude is ready, it calls `ExitPlanMode` with its proposed plan. You see the plan, approve or reject.
- Approving leaves plan mode and executes; rejecting keeps you in planning.

## 3. When to use it

Use plan mode when:

- The task touches **multiple files** or **multiple subsystems**.
- The change is **hard to reverse** (DB migration, public API change, infrastructure).
- You're **unsure** if Claude will go where you actually want.
- The task is **expensive** to redo (slow tests, slow builds).

Skip it for:

- Tiny edits ("rename this variable").
- Pure exploration ("explain what this file does").
- One-shot tasks where the "plan" is the same as the "execution."

## 4. The bigger lesson

Plan mode embodies a workflow you should adopt **even outside plan mode**: separate the "decide what to do" turn from the "do it" turn. When you don't, you get changes you didn't expect and have to revert.

In practice, even without plan mode, you can do:

> "Non scrivere ancora. Prima dimmi cosa cambieresti, in 5 bullet."

Same effect, more control.

## 5. Plan mode vs `/init` (clarification)

`/init` walks the repo and **writes** a CLAUDE.md. Not plan mode — it's a single command with a single side effect.

Plan mode is for *any* task: it's the default-off mode you toggle for risky work.

## 6. Hands-on

In their repo, have them:

1. Toggle plan mode (Shift+Tab twice).
2. Say something non-trivial: "Voglio sostituire il logger custom con `pino` ovunque."
3. Watch Claude grep, read, and propose a phased plan with files to touch.
4. They review. If it looks wrong, they say "no, prima rispetta i wrapper esistenti" — Claude replans.
5. When happy, they approve via the ExitPlanMode prompt. Claude executes.

## 7. Anti-patterns

- **Approving the first plan without reading it.** The whole point is the human in the loop.
- **Using plan mode for trivial work.** Wastes your time on bureaucracy.
- **Forgetting you're in plan mode and being confused that Claude won't edit.** The footer tells you.
- **Pre-planning every coding session.** Plan mode is a tool, not a religion.

## 8. Check question

> "Devi rinominare `getUser` in `getUserById` ovunque (12 file). Quale approccio?
> A. Plan mode: troppo rischioso non pianificare.
> B. Diretto, senza plan mode: è una rename meccanica, Claude può grep-e-replace.
> C. Faccio io a mano, troppo rischioso lasciar fare a Claude.
> D. Spawno cinque subagent in parallelo, uno per ogni gruppo di file."

Correct: **B**. Plan mode adds value when the *strategy* is uncertain. For a meccanical rename, just do it.

## 9. Wrap up

> "Hai capito quando pianificare. Adesso la cosa che ti farà risparmiare più soldi: gestire il **contesto**. `/lesson context-window`."

```bash
python3 .claude/bin/state.py complete plan-mode
```

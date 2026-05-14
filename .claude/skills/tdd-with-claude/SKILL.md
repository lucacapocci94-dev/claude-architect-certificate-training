---
description: "Workflow 5/5 — TDD with Claude Code: red-green-refactor loop, getting Claude to write failing tests first, locking behavior with tests before refactor, how tests act as guardrails against hallucination. Use when the student asks about TDD, test-driven, how to lock behavior, why tests are useful with LLMs, or invokes /lesson tdd-with-claude."
command: "lesson tdd-with-claude"
track: "workflow"
duration_min: 8
---

# Workflow 5/5 — TDD with Claude

**Lesson id:** `tdd-with-claude`
**Mark complete with:** `python3 .claude/bin/state.py complete tdd-with-claude`

---

## 1. Why TDD specifically matters with LLMs

LLMs hallucinate. They produce code that **looks** right. Reading it does not always catch the wrong assumption. **Running tests does.**

TDD with Claude isn't religion — it's the cheapest source of ground truth in the loop. Write the test, run it, watch it fail or pass. The signal is binary and immediate.

## 2. The red-green-refactor with Claude

### Red
> "Non implementare. Scrivi un test in `tests/bar.test.ts` per: il caso A, il caso B, e l'edge case C. Eseguilo e verifica che fallisca con l'errore atteso."

Claude writes the test and runs it. You see "FAIL." This is the *spec, executable*. If the test passes immediately, the test is wrong or the feature already exists.

### Green
> "Ora implementa `bar` in `src/bar.ts` finché tutti e tre i test passano. Nient'altro."

Claude implements, runs, iterates until green. The constraint "niente di più" prevents bonus features.

### Refactor
> "Tutti verdi. Rifattorizza per leggibilità. I test devono restare verdi."

The tests are now a **safety net** for refactoring. No regression goes undetected.

## 3. Tests as the spec

In the workflow track we've built up: brainstorm → spec → plan → tests → code. The tests are the *executable* version of the spec. If the test passes, the spec section is satisfied.

For tricky behavior (rate limiting, idempotency, retry policy), tests beat prose every time.

## 4. Locking behavior before refactor

Before any non-trivial refactor:

> "Prima di toccare `src/auth.ts`, scrivi test che catturano il suo comportamento attuale. Coprilo come una mummia. Solo dopo, rifattorizziamo."

This is a powerful Claude Code move: **characterisation tests** before refactor. Often these expose behavior nobody knew existed — bugs that have been quietly working.

## 5. Hooks make TDD enforceable

Recall hooks (Core 4/9). A `Stop` hook that runs the test suite before the model can end its turn turns TDD from "we agreed to do it" to "the harness will not let us not do it":

```json
{
  "hooks": {
    "Stop": [
      { "matcher": "", "hooks": [{ "type": "command", "command": "npm test" }] }
    ]
  }
}
```

If tests fail, the hook exits 2; Claude sees the failure and continues until they pass. This is the certification's "deterministic over probabilistic" principle in action.

## 6. Hands-on

Pick a small function in the student's repo. Have them:

1. Delete its body (or rename it to `_old`).
2. Ask Claude to write tests that cover its old behavior.
3. Implement until green.
4. Notice: the new implementation can differ from the old one, but if tests pass, behavior is equivalent.

If they're brave: add the Stop hook above and watch the next few sessions become more disciplined.

## 7. Anti-patterns

- **Letting Claude write tests **after** code.** The tests will be tautologies. Always tests-first.
- **One mega-test.** Three focused tests beat one "does everything" test.
- **Mocking everything.** Mocks lie. Prefer integration tests where they're cheap.
- **TDD on the wrong thing.** Don't TDD UI styling. TDD logic, math, business rules.

## 8. Check question

> "Devi cambiare un algoritmo di pricing che è in produzione da 2 anni. Cosa fai prima di toccare il codice?
> A. Vado direttamente, conosco il dominio.
> B. Faccio scrivere a Claude test che caratterizzano il comportamento attuale (anche bug-included), li faccio passare, poi rifattorizzo.
> C. Riscrivo da zero per pulizia.
> D. Chiedo a Claude di mostrare la differenza prima e dopo a parole."

Correct: **B**. Characterisation tests + green-before-refactor = safe change.

## 9. Wrap up — Workflow complete!

That closes the Workflow track. The student now has the production loop:

- Brainstorm before code
- Spec on disk
- Plan in slices
- Iterate with specific feedback
- TDD as ground truth

Suggest:

> "Workflow chiuso. Ultima sezione prima dei domini d'esame: i **plugin** di Claude Code (incluso `superpowers`). `/plugins`."

```bash
python3 .claude/bin/state.py complete tdd-with-claude
python3 .claude/bin/state.py set-current --track plugins --module plugins-intro --next "/lesson plugins-intro"
```

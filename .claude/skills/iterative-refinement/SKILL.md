---
description: "Workflow 4/5 — Iterative refinement: providing examples, the test-driven prompt, the interview pattern for ambiguity, how to give effective feedback on wrong output. Use when the student asks how to fix Claude's output, why Claude keeps doing the wrong thing, how to iterate quickly, or invokes /lesson iterative-refinement."
command: "lesson iterative-refinement"
track: "workflow"
duration_min: 7
---

# Workflow 4/5 — Iterative refinement

**Lesson id:** `iterative-refinement`
**Mark complete with:** `python3 .claude/bin/state.py complete iterative-refinement`

---

## 1. The reality

Claude rarely gets a non-trivial task perfect on the first try. The skill is *how you iterate*. Two students with identical Claude Code installs differ massively in productivity because of this single skill.

## 2. Three techniques that change the curve

### a) Show, don't tell
When the output is close-but-wrong in style, give one **concrete example** of what right looks like:

> "Non così. Voglio così:
>
> ```ts
> // BAD
> const x = items.filter(i => i.active).map(i => i.id);
>
> // GOOD
> const activeIds = items
>   .filter(i => i.active)
>   .map(i => i.id);
> ```
>
> Riapplica al codice che hai scritto."

One example moves Claude from probabilistic to nearly deterministic on style decisions. This is the **few-shot** pattern from the certification exam — it works here too.

### b) Test-first
Instead of "implement X", flip to "write the tests for X first, run them, see them fail, then implement until they pass."

> "Non scrivere ancora l'implementazione. Scrivi prima i test in `tests/foo.test.ts` per il caso A, il caso B, il caso edge. Eseguili (ovviamente falliscono). Solo dopo, implementa."

The tests become the spec. Claude can't drift from them.

### c) The interview pattern (when stuck)
When Claude keeps producing wrong output, **stop pushing on the output and ask why**:

> "Fermati. Spiegami in 3 frasi perché hai fatto questa scelta. Voglio capire il modello mentale."

You'll find the wrong assumption in one turn instead of fighting the symptoms for ten.

## 3. Effective feedback vs ineffective feedback

| Ineffective | Effective |
|---|---|
| "Sbagliato, riprova" | "Sbagliato perché il valore Y non viene letto. Verifica con `console.log` prima di scrivere il fix." |
| "Più pulito" | "Estrai questa funzione `validate` in `lib/validate.ts` e importala." |
| "Non così" | "Vedi `src/util/format.ts` — segui quello stile, non quello che hai scritto." |
| "Hai dimenticato i test" | "Aggiungi test in `foo.test.ts` per: empty input, single item, 1000 items." |

The pattern: **specific**, **actionable**, **with a reference** to either a file or an example.

## 4. The 80/20 of feedback prompts

Memorize these three:

1. "Cosa hai assunto qui che potrebbe essere sbagliato?"
2. "Scrivi prima il test che catturerebbe questo bug."
3. "Mostrami il tuo ragionamento prima del codice."

## 5. When to give up on the current path

If after 3 turns the code is still wrong, the issue isn't the iteration — it's the starting point. Try:

- `/clear` and restart with a tighter spec.
- A different decomposition (smaller chunks).
- Plan mode (Workflow 3) to think before doing.

Don't burn 20 turns refining the wrong path.

## 6. Hands-on

Pick a small task in their repo. Have them:

1. Ask Claude to implement it.
2. When Claude produces output, give **bad** feedback ("not like this"). Notice the second output isn't much better.
3. Undo. Restart. Give **good** feedback (specific, file-referenced, example). Notice the second output is materially better.

This is the muscle. Repeat it in real work until it's automatic.

## 7. Anti-patterns

- **Vague "make it better."** Defines a doom loop.
- **Letting tiny issues accumulate.** Fix them as they appear, one feedback prompt each.
- **Re-explaining the entire context in each turn.** Reference files, not history.
- **Refusing to step back.** When stuck for 3 turns, change the approach, not the prompt.

## 8. Check question

> "Claude scrive una funzione con uno stile che non ti piace. Quale feedback è migliore?
> A. 'Più pulito.'
> B. 'Ridefiniscila in modo idiomatico.'
> C. 'Guarda `src/util/format.ts` — segui quello stile (chaining su più righe, niente arrow inline). Riapplica.'
> D. 'Non così.'"

Correct: **C**. Reference + concrete style rule = ~deterministic result.

## 9. Wrap up

> "Iterazione presa. L'ultimo del workflow: scrivere con Claude in **TDD**. `/lesson tdd-with-claude`."

```bash
python3 .claude/bin/state.py complete iterative-refinement
```

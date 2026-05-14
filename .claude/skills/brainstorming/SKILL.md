---
description: "Workflow 1/5 — Brainstorming with Claude: forcing Claude to ask questions before generating, the 'before you write, what do you NOT know' prompt, building shared understanding. Use when the student asks how to brainstorm with Claude, why Claude jumps to code too fast, how to make Claude ask questions, or invokes /lesson brainstorming."
command: "lesson brainstorming"
track: "workflow"
duration_min: 7
---

# Workflow 1/5 — Brainstorming first

**Lesson id:** `brainstorming`
**Mark complete with:** `python3 .claude/bin/state.py complete brainstorming`

---

## 1. The problem

Default Claude jumps to producing code. Tell it "build a rate limiter" and it picks an approach (probably wrong for your case) and writes 200 lines. You revert, retry, revert. Hours lost.

The fix: **force a brainstorming turn first.** Make Claude interview you before it does anything.

## 2. The brainstorming prompt

Here is the verbatim prompt that works. Memorize it:

> "Non scrivere ancora codice. Prima fammi tutte le domande che ti servono per essere sicuro di capire cosa voglio. Pensa ai casi limite, ai vincoli non detti, alle decisioni che presumeresti senza chiederlo. Falle una alla volta, dalle più importanti alle meno."

In English:

> "Don't write code yet. First, ask me every question you need to be sure you understand. Think about edge cases, unstated constraints, decisions you'd quietly assume. One question at a time, most important first."

## 3. Why this works

- **Surfaces assumptions** the model would otherwise bake silently into the code.
- **Catches scope errors** ("you didn't mention rate limit per user vs per IP — which?").
- **Aligns the mental model** before any keystrokes.
- **Costs almost nothing** in tokens compared to the alternative (write → revert → rewrite).

A rate limiter built after 10 minutes of Q&A is usually correct on the first try. Without Q&A, you usually get 3-4 iterations.

## 4. The interview pattern

Once Claude starts asking, two rules:

1. **Don't pre-answer questions it hasn't asked.** Let it lead. If you front-load 8 facts, it stops thinking and goes to code.
2. **Be honest about "I don't know."** "I don't know if we have multi-tenancy yet" is a valid answer — it forces Claude to either propose both options or to research.

After enough questions, Claude will say "I think I have what I need. Want me to summarise the design before I write?" Yes — say yes. **Always.**

## 5. The pre-mortem add-on

After the design summary, push one more turn:

> "Prima di scrivere — quali sono i tre modi in cui questo design può fallire in produzione? Quali ipotesi ho fatto che potrebbero essere sbagliate?"

Pre-mortem is cheap. Bugs caught here cost a sentence; the same bugs caught in production cost a weekend.

## 6. Hands-on

In their project, have them pick a real small task ("aggiungi un export CSV alle prenotazioni"). They run:

```
claude
```

And open with the brainstorming prompt. Watch Claude ask 5-10 questions. They answer. Then ask for the design summary. Then run the pre-mortem.

**Only after all that** do they say "ok, scrivilo."

Compare: how does the result feel vs the usual "just write the export"?

## 7. Anti-patterns

- **One giant prompt** dumping all context and asking for code. Claude will obey and you'll get average output.
- **Skipping questions because you "already know."** You don't know what Claude doesn't know. Let it ask.
- **Answering bigger than asked.** Stick to the question; over-answering kills the flow.
- **Doing brainstorm-then-code-in-one-session.** Brainstorm to a written spec, then `/clear`, then code from the spec. Massively cheaper.

## 8. Check question

> "Devi aggiungere un campo `archived_at` a una tabella `orders` in produzione (5M righe). Qual è il primo prompt che invii a Claude?
> A. 'Aggiungi una migration con archived_at TIMESTAMP nullable.'
> B. 'Aggiungi archived_at e fai il deploy.'
> C. 'Non scrivere ancora. Prima fammi le domande che ti servono per essere sicuro: capacità di scrittura, blocchi, backfill, downtime accettabile.'
> D. 'Fai tu come pensi sia meglio.'"

Correct: **C**. Interview-first turns a risky change into a designed change.

## 9. Wrap up

> "Hai imparato a far parlare Claude prima che scriva. Adesso trasformiamo quel dialogo in un artefatto: lo **spec**. `/lesson spec-driven`."

```bash
python3 .claude/bin/state.py complete brainstorming
```

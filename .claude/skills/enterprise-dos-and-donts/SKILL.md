---
description: "Plugins 5/5 (closing lesson) — Enterprise do's & don'ts when using Claude Code at Accenture: what to delegate, what to keep in your own hands, sensitive data discipline, how to present AI-assisted work to managers, and the failure modes that will get you in trouble. Use when the student is wrapping up the canonical 1-week path, asks 'what should I be careful about?', 'is it safe to use Claude on client code?', 'how do I talk about this with my manager?', or invokes /lesson enterprise-dos-and-donts."
command: "lesson enterprise-dos-and-donts"
track: "plugins"
duration_min: 15
---

# Plugins 5/5 — Enterprise do's & don'ts at Accenture

**Lesson id:** `enterprise-dos-and-donts`
**Mark complete with:** `python3 .claude/bin/state.py complete enterprise-dos-and-donts`

This is the closing lesson of the canonical 1-week path. Up to here you have learnt **what Claude Code can do**. This lesson is about **what you should and should not let it do**, specifically in an Accenture / client-services context.

---

## 1. The mental model

Frame it for the student:

> "Claude Code è uno stagista geniale, instancabile e a volte un po' troppo sicuro di sé. Tu sei il senior. Sai delegare, sai rivedere, sai dove non ti puoi permettere errori. **La produttività vera arriva quando capisci quando NON usarlo.**"

Three categories of work:

| Category | Example | Approach |
|---|---|---|
| **Green** (delegate freely) | Boilerplate, tests for existing code, refactors with tests as guardrails, exploring an unfamiliar repo | Let Claude run. Review the diff. |
| **Yellow** (delegate but verify line-by-line) | Business logic, new features touching domain rules, security-adjacent code (auth, permissions, SQL queries) | Pair-mode. Read every line. Tests required. |
| **Red** (do not delegate, or delegate only the *first draft* and rewrite) | Cryptography, compliance-driven code (GDPR, financial), production migrations, anything you cannot afford a hallucination on | Use Claude as a sounding board. Write the final version yourself. |

## 2. The five do's

1. **Always work in a project under version control.** Even if you're not pushing anywhere, `git init` + commit before letting Claude work. A 5-second `git diff` after a Claude session is the cheapest safety net you'll ever buy.
2. **Use plan mode for anything non-trivial.** Plan mode (shift+tab) costs you 30 seconds and saves you the wrong implementation. Lesson `plan-mode` already covered this — now make it a habit.
3. **Lock behaviour with tests before refactor.** If Claude is about to touch existing code, ask it first to write tests that capture the *current* behaviour, then refactor. The tests catch silent regressions. (See `tdd-with-claude`.)
4. **Keep a project `CLAUDE.md` that encodes your team's rules.** "We use Angular 17 standalone components, never NgModules", "all HTTP calls go through `*.service.ts`", "tests use Jasmine, not Jest". This is how you stop fighting the same battle in every session.
5. **Tell your manager what you delegated.** Not because they will police you — because **they want to know which engineers know how to leverage AI**. Make it visible. "I shipped this in half a day using Claude Code for the boilerplate and writing the auth layer by hand." That's the sentence that gets you promoted.

## 3. The five don'ts (the ones that bite)

1. **Don't paste client secrets, credentials, or PII into the chat.** Same rule as Slack, same rule as Stack Overflow. Claude Code reads files from disk — that's fine. *You* typing `DB_PASSWORD=xyz` into the prompt is not.
2. **Don't trust generated code on infra you can't roll back.** Database migrations, IAM policies, production deploy scripts. Claude will write them confidently. Roll-back-ability is your only defence — never accept an irreversible action without reading every character.
3. **Don't accept tests Claude wrote on code Claude wrote without manually thinking about edge cases.** Both sides came from the same model. If Claude missed a case in the impl, it almost certainly missed it in the test. Add at least one edge case yourself before merging.
4. **Don't let Claude touch sensitive folders without a permission deny rule.** In `.claude/settings.json` add `"permissions": { "deny": ["Read(secrets/**)", "Read(.env*)"] }`. Belt and braces — even if the model "decides" to read them, it can't.
5. **Don't pretend you didn't use it.** The opposite of #5 in the do's. If a reviewer asks "did Claude write this?", say yes and walk them through what you reviewed. Hiding it once is enough to lose trust.

## 4. Hands-on: the "manager impression" exercise

Have the student run, **in their own Angular project** (or in `extra_materials/sample-angular-project/`):

```
claude
> "Aggiungi una funzionalità 'filtra prodotti per categoria' al componente products-list,
   con un select sopra la lista. Prima fammi vedere il piano in plan mode,
   poi scrivimi i test, poi l'implementazione."
```

After it ships, get them to write — on paper or in a note — the **3 sentences they would tell their manager** about this change:

1. What you built.
2. Which parts you delegated to Claude vs. wrote yourself.
3. Where you actively reviewed because it was yellow or red.

This is the artefact they should be able to produce on demand. It's the difference between "I use AI" and "I use AI **well**" — and the latter is what gets noticed.

## 5. Check question

> "Stai per modificare il file `auth.service.ts` di un cliente — gestisce login e JWT.
> Quale di queste è la mossa migliore?
> A. Chiedi a Claude di riscriverlo da zero in plan mode, accetti il piano, lo lasci lavorare e poi committi.
> B. Apri il file, ti fai spiegare da Claude cosa fa riga per riga, poi modifichi tu a mano la parte che ti serve cambiare e usi Claude solo per scrivere i test.
> C. Cancelli il file e chiedi a Claude di ricrearlo basandosi sui test esistenti.
> D. Lasci che Claude faccia tutto in modalità auto-accept per risparmiare tempo."

Correct: **B**. Auth is **red** territory. Claude can explain, can write tests around it, can suggest — but the production diff is yours.

## 6. Wrap up & mark complete

> "Hai finito il percorso da 1 settimana. Sai installare, configurare, brainstormare, pianificare, testare, e — fondamentale — sai cosa NON delegare. Adesso il programma di certificazione è opzionale: se vuoi prepararti per l'esame, esegui `/syllabus domains` e iniziamo i 5 domini."

```bash
python3 .claude/bin/state.py complete enterprise-dos-and-donts
```

Then offer:

- `/syllabus domains` → optional certification track
- `/remember "le mie regole personali su quando NON usare Claude"` → save their own version of this lesson
- Just close the session and start using Claude Code on real work. The course is done.

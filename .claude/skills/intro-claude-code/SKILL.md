---
description: "Foundations 1/5 — What Claude Code actually is, and why it is *not* the same as using Claude in a chat window. Use when the student is at the very start of Foundations, asks 'what is Claude Code', 'how is this different from ChatGPT', 'why not just use claude.ai', or invokes the /lesson intro-claude-code command."
command: "lesson intro-claude-code"
track: "foundations"
duration_min: 5
---

# Foundations 1/5 — What is Claude Code?

**Lesson id:** `intro-claude-code`
**Mark complete with:** `python3 .claude/bin/state.py complete intro-claude-code`

---

## 1. Open with a question (assess)

Ask the student, in their language:

> "Fino ad oggi, come hai usato Claude o ChatGPT? Hai mai incollato un pezzo di codice in una chat e chiesto di sistemarlo? Hai mai usato uno strumento che leggesse l'intero repo per te?"

You are listening for the mental model: do they think of an LLM as **a chat window** (paste in → paste out), or as **an agent that operates on their machine**? This shapes everything.

## 2. The core idea

Explain — slowly, no jargon — the difference between three things they might already know:

| Tool | What it sees | What it can do |
|---|---|---|
| **claude.ai** in browser | Whatever you paste into the chat | Reply with text you can copy back |
| **Copilot** in your IDE | The file you have open + nearby files | Suggest the next few lines while you type |
| **Claude Code** in your terminal | **Your entire repository**, plus the ability to run shell commands, edit files, run tests | Do the whole task end-to-end: read, plan, edit, test, commit |

Make it concrete. Use this exact example:

> "Immagina di voler aggiungere il rate-limiting a un endpoint in un'app Python. In chat: incolli la funzione, ricevi un suggerimento, lo incolli indietro, scopri che hai dimenticato di aggiornare i test, copi quelli, e così via — sette giri di copia-incolla. Con Claude Code: apri il terminale nel repo, dici 'aggiungi rate-limiting all'endpoint /login con limite di 10 al minuto', e lui legge il codice, scrive la modifica, aggiunge i test, li esegue, e ti mostra il diff. Tre minuti invece di trenta."

## 3. What Claude Code is *technically*

In one short paragraph:

> "Claude Code è un'applicazione da terminale. Quando la lanci con `claude` in una cartella, fa partire un loop: tu scrivi un messaggio, il modello decide se rispondere o usare uno **strumento** (leggere un file, eseguire un comando, scrivere codice), esegue lo strumento, vede il risultato, e continua finché il compito non è finito. Tu sei nel ciclo: puoi interromperlo, vedere ogni azione, approvarla o negarla."

The two ideas that matter for the rest of the course:

1. **It is agentic** — the model decides which tool to use, not you.
2. **You stay in the loop** — by default it asks before touching anything risky (the "permission system", lesson 10).

## 4. What it is **not**

Address the common misconceptions head-on:

- It is **not** an IDE plugin. It runs in the terminal. (There are IDE integrations, but the core product is the CLI.)
- It is **not** a search box. It works iteratively, often making 5–20 tool calls before finishing.
- It is **not** unsafe by default. Every destructive action prompts you unless you've explicitly allowed it.

## 5. Hands-on (no install yet)

Tell them:

> "Per ora non installare niente. Apri il sito https://claude.com/product/claude-code e leggi i primi due paragrafi. Poi torna qui."

Wait for them. Ask:

> "Cosa ti ha colpito di più rispetto a come usavi Claude in chat?"

Let them answer. Mirror back the key insight: **the model has hands**.

## 6. Check question (must answer correctly to proceed)

Pose this question. One correct answer.

> "Qual è la differenza fondamentale tra usare Claude in chat e usare Claude Code?
> A. Claude Code usa un modello diverso e più potente.
> B. Claude Code può eseguire strumenti (leggere file, scrivere file, lanciare comandi) sul tuo computer, mentre la chat può solo restituire testo.
> C. Claude Code è gratis mentre la chat è a pagamento.
> D. Claude Code funziona offline."

Correct: **B**. If they pick A, C, or D, gently correct and re-explain the agentic-loop idea before moving on.

## 7. Wrap up & mark complete

When they answer B (or you've corrected them), say:

> "Perfetto. Adesso lo installiamo. Prossima lezione: `/lesson install-claude-code`."

Then mark complete:

```bash
python3 .claude/bin/state.py complete intro-claude-code --notes "Got the agentic-loop concept"
```

End the turn. Let them type `/lesson install-claude-code` when ready.

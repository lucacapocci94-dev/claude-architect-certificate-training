---
description: "Foundations 3/5 — First real Claude Code session in the student's own project. Covers running claude, basic interaction patterns, /help, /exit, interrupting, and the permission prompts. Use when the student is ready for their first hands-on session or invokes /lesson first-session."
command: "lesson first-session"
track: "foundations"
duration_min: 10
---

# Foundations 3/5 — Your first real session

**Lesson id:** `first-session`
**Mark complete with:** `python3 .claude/bin/state.py complete first-session`

---

## 1. Choose a project (not this one)

This is important: tell the student to **open a second terminal** and `cd` into one of *their* projects — preferably one with some code in it, ideally under git. Personal repos are fine, work repos are fine (subject to their security policy).

If they say "I don't have a project", suggest cloning a small public one as a sandbox:

```bash
git clone https://github.com/anthropics/courses ~/claude-sandbox
cd ~/claude-sandbox
```

Make sure they actually have a terminal open in a real project before continuing. Wait.

## 2. Launch

```bash
claude
```

A REPL opens. The first time, it asks them whether to trust this directory — they answer yes for their own code.

Tell them:

> "Da adesso, tutto quello che scrivi è un messaggio per l'agente. Lui legge, decide se serve uno strumento, lo esegue, e ti risponde. Niente più copia-incolla."

## 3. Try four things, in order

### a) Ask, don't command
Have them type:

> "Cosa fa questo repo? Spiegamelo come se fossi un nuovo membro del team."

Watch Claude do **Glob** + **Read** calls. Point that out: each line that starts with `⏺ Read(...)` or `⏺ Bash(...)` is a tool call. This is the agentic loop in action.

### b) Permission prompts
Now have them ask something that needs a shell command:

> "Conta quante righe di codice ci sono in totale."

Claude will propose running `find` / `wc -l` and **ask for permission** before executing. Three buttons: allow once, allow always, deny. Tell them:

> "Le prime sessioni: rispondi 'allow once'. Dopo qualche giorno saprai quali comandi sono sempre sicuri e potrai allowed-list-arli in `.claude/settings.json` (lesson 10)."

### c) Interrupt
Have them ask for something they don't actually want (e.g. "ora cancella tutti i file"). When Claude proposes a destructive command, they hit **Esc** to interrupt. Demonstrate that **they control the loop**.

### d) `/help` and `/exit`
Inside the prompt, they type `/help` to see all built-in slash commands. Important ones to point out:

- `/help` — list commands
- `/clear` — wipe the conversation (lesson 13 explains why this matters for tokens)
- `/compact` — summarise old turns to free context
- `/init` — generate a CLAUDE.md (next lesson!)
- `/exit` — quit

To exit: `/exit` or `Ctrl+D` twice.

## 4. Three principles to land

After the demo, summarise in three lines:

1. **You stay in the loop.** Every dangerous action asks first. Esc cancels.
2. **The model is the orchestrator.** You give intent. It figures out the steps.
3. **Tokens cost money.** Don't keep one giant conversation — `/clear` between unrelated tasks. (We will train this habit in lesson 13.)

## 5. Check question

> "Sei nel mezzo di un'azione e Claude Code propone di eseguire un comando shell che NON vuoi che esegua. Cosa fai?
> A. Chiudo il terminale di forza.
> B. Premo Esc per interrompere; il loop si ferma in attesa di un nuovo messaggio.
> C. Cancello il comando dal terminale.
> D. Riavvio il computer."

Correct: **B**. Esc is the universal interrupt — they should commit it to muscle memory.

## 6. Wrap up & mark complete

> "Hai fatto la tua prima sessione vera. Adesso facciamo capire a Claude *cosa* è questo repo, in modo permanente: si chiama `/init`. `/lesson init-walkthrough`."

```bash
python3 .claude/bin/state.py complete first-session
```

If the student looks tired or the context is getting big, suggest `/compact-now` before continuing.

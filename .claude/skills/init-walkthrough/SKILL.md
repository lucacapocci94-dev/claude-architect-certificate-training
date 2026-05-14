---
description: "Foundations 4/5 — The /init command: what it does, what it generates, and how to fix a bad CLAUDE.md. Use when the student is ready to run /init on their project, asks about /init, asks 'what should I put in CLAUDE.md', or invokes /lesson init-walkthrough."
command: "lesson init-walkthrough"
track: "foundations"
duration_min: 8
---

# Foundations 4/5 — `/init` and your project's first CLAUDE.md

**Lesson id:** `init-walkthrough`
**Mark complete with:** `python3 .claude/bin/state.py complete init-walkthrough`

---

## 1. What `/init` actually does

In one sentence:

> "`/init` è un comando incorporato che fa esplorare il repo a Claude e genera un file `CLAUDE.md` che riassume cos'è il progetto, come si compila, come si testa, e quali convenzioni segue."

That file becomes the **project memory** for every future session — Claude reads it automatically at startup. You read it once, fix it, and from that moment every prompt costs fewer tokens because Claude doesn't have to re-discover the basics each time.

Analogy:

> "Pensa a CLAUDE.md come al README per un nuovo collega. Solo che il collega lo legge davvero, ogni volta."

## 2. Run it (hands-on)

Have them, in their project terminal:

```bash
claude
```

Then at the prompt:

```
/init
```

Claude will:
1. Glob the repo to understand its shape.
2. Read package.json / pyproject.toml / Cargo.toml / go.mod / Makefile / similar.
3. Read README and any existing docs.
4. Propose a CLAUDE.md.
5. Ask permission to write it.

This takes 30–90 seconds. Watch each tool call go by.

## 3. Open the generated file and read it together

Have them open the new `CLAUDE.md` in their editor. A good one has at minimum:

- **Project overview** (1–2 lines: what is this thing)
- **How to build** (`npm run build`, `make`, `cargo build`, …)
- **How to test** (`npm test`, `pytest`, `go test ./...`)
- **How to lint / format** (`npm run lint`, `ruff`, `gofmt`)
- **Repo layout** (where the important folders are)
- **Conventions** (naming, branch strategy, commit format if any)

If anything is wrong (paths, commands, framework), **fix it now**. This is the single highest-leverage edit they will make all course — every future session reads this file.

## 4. The non-obvious things to add by hand

The default `/init` output is bare. Tell them these are common additions:

- **What NOT to touch** — generated files, vendored deps. "Never edit `dist/`, `node_modules/`, `*.generated.ts`."
- **Domain language** — "In this codebase, 'transaction' always means a DB transaction, never a financial one."
- **Done = ?** — "A change is done when tests pass AND `npm run lint` passes."
- **Security boundaries** — "Never log anything from `request.body`; we have PII filters."

Add 2–3 of these to their CLAUDE.md as a live exercise.

## 5. Verify it works

Quit `claude` (`/exit`) and re-launch:

```bash
claude
```

Then ask:

```
Come si lanciano i test in questo progetto?
```

Claude should answer **without reading any file** — it already knows from CLAUDE.md. That's the win.

## 6. Common mistakes to flag

- **Pasting in everything.** CLAUDE.md should be ~100 lines tops. It's instructions, not docs.
- **Forgetting to commit it.** It belongs in git so the whole team gets the same instructions.
- **Letting it rot.** When commands change, CLAUDE.md must change. Treat it like code.
- **Mixing personal preferences in.** Personal stuff (your editor, your shell aliases) goes in `~/.claude/CLAUDE.md` (user level), not project CLAUDE.md. That's the next lesson.

## 7. Check question

> "Hai lanciato `/init` in un monorepo. Il CLAUDE.md generato dice di lanciare i test con `npm test` ma in realtà nel tuo repo si fa `pnpm -C packages/api test`. Cosa fai?
> A. Niente — Claude lo capirà da solo la prossima volta.
> B. Apro CLAUDE.md, correggo il comando, lo committo. Ogni futura sessione partirà giusta.
> C. Aggiungo una nota nella mia chat ogni volta.
> D. Apro un issue su GitHub di anthropic-ai/claude-code."

Correct: **B**. CLAUDE.md is *the* place to teach Claude about your project. Edit it like code.

## 8. Wrap up & mark complete

> "Bene. Adesso vediamo la gerarchia: dove altro vivono i CLAUDE.md e come si combinano. `/lesson claude-md-hierarchy`."

```bash
python3 .claude/bin/state.py complete init-walkthrough
```

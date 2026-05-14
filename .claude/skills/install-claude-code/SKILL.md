---
description: "Foundations 2/5 — Install Claude Code, authenticate, and verify. Use when the student is ready to install Claude Code, asks 'how do I install Claude Code', 'how do I run claude', or invokes /lesson install-claude-code."
command: "lesson install-claude-code"
track: "foundations"
duration_min: 7
---

# Foundations 2/5 — Install Claude Code

**Lesson id:** `install-claude-code`
**Mark complete with:** `python3 .claude/bin/state.py complete install-claude-code`

---

## 1. Pre-flight check (60 seconds)

Ask the student to confirm they have **Node.js 18 or newer** installed. They run this in a terminal:

```bash
node --version
```

If `node` is missing or `< v18`, point them to https://nodejs.org and ask them to install the LTS version, then come back.

## 2. Install

The official install is one command. Tell them, verbatim:

```bash
npm install -g @anthropic-ai/claude-code
```

**Why `-g`?** It installs `claude` as a global command in their PATH so they can run it from any directory.

If they get a permission error on macOS/Linux, the cleanest fix is **not** `sudo` — it's switching npm's prefix to a user-writable directory. Suggest:

```bash
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.zshrc   # or ~/.bashrc
source ~/.zshrc
npm install -g @anthropic-ai/claude-code
```

## 3. Verify the binary

```bash
claude --version
```

They should see a version number. If "command not found", their PATH is missing the npm-global bin — re-source the shell rc file.

## 4. Authenticate

The first `claude` run will prompt for authentication. Two options:

- **Pro / Max subscription** (recommended for individuals) — sign in with Claude account.
- **API key** (for orgs without a subscription) — get one at https://console.anthropic.com, set `ANTHROPIC_API_KEY` in their shell rc:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**At Accenture:** check internal docs first — there may be a corporate workspace they should join, which avoids personal subscriptions.

## 5. Smoke test

Have them create a throwaway directory and try it:

```bash
mkdir ~/claude-smoke-test && cd ~/claude-smoke-test
echo "console.log('hello')" > hello.js
claude
```

Inside the interactive prompt, they type:

> "Leggi hello.js e dimmi cosa fa."

They should see Claude **read the file** (a Read tool call) and reply. Their reaction here is the moment they understand "the model has hands" from lesson 1.

To exit: `/exit` or `Ctrl+D` twice.

## 6. Common gotchas

- **PATH not updated** → close and reopen the terminal, or `exec $SHELL`.
- **Corporate proxy** → set `HTTPS_PROXY` env var before running `claude`.
- **No internet on the runner** → Claude Code needs an internet connection to talk to the API.
- **Running as root** → don't. Use a normal user.

## 7. Check question

> "Hai installato Claude Code, e quando provi a lanciare `claude` ricevi 'command not found'. Hai già controllato che `node --version` funzioni. Qual è il primo passo da provare?
> A. Reinstallare Node.js.
> B. Eseguire `sudo claude`.
> C. Aggiungere il bin di npm al PATH (es. `~/.npm-global/bin`) e riaprire il terminale.
> D. Cambiare modello da Sonnet a Opus."

Correct: **C**. The binary is installed but not findable.

## 8. Wrap up & mark complete

> "Installato. La prossima lezione: aprire `claude` dentro un repo vero e fare il primo giro. `/lesson first-session`."

```bash
python3 .claude/bin/state.py complete install-claude-code
```

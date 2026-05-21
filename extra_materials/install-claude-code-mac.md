# Install Claude Code on macOS — Quick Reference

Easy-to-consult, easy-to-test commands. Each block is copy-pasteable; a verify command follows every install step.

> **Requirements:** macOS 12+, an internet connection. Node.js is only required for the npm install method (Option C).

---

## Pick an install method

| Option | Needs Node/npm? | Best for |
|---|---|---|
| **A. Native installer (curl)** | No | Quickest path, official Anthropic installer |
| **B. Homebrew cask** | No | You already use `brew` for everything |
| **C. npm global** | Yes | You're already a Node developer |

---

## Option A — Native installer (no npm)

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Verify:

```bash
claude --version
```

The script drops a native binary (typically under `~/.local/bin/claude`) and patches your shell rc to add it to `PATH`. If `command not found` after install, reopen the terminal or run `exec $SHELL`.

---

## Option B — Homebrew cask (no npm)

```bash
brew install --cask claude-code
```

Verify:

```bash
claude --version
```

If you don't have Homebrew yet:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew --version
```

---

## Option C — npm global (requires Node.js ≥ 18)

### C.1 Check Node.js

```bash
node --version
```

Expected: `v18.x` or newer. If missing or too old:

```bash
brew install node
node --version
```

### C.2 Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

Verify:

```bash
claude --version
```

### Permission error (`EACCES`)?

Do **not** use `sudo`. Switch npm's global prefix to a user-writable directory:

```bash
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.zshrc
source ~/.zshrc
npm install -g @anthropic-ai/claude-code
```

Verify:

```bash
which claude
claude --version
```

---

## Authenticate

The first time you run `claude`, you'll be prompted.

**Option A — Pro/Max subscription (recommended for individuals)**

Just run `claude` and log in via the browser flow.

**Option B — API key (for orgs without a subscription)**

Get a key at https://console.anthropic.com, then:

```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.zshrc
source ~/.zshrc
```

Verify:

```bash
echo $ANTHROPIC_API_KEY | head -c 10   # should print "sk-ant-..."
```

> **At Accenture:** check internal docs first — there may be a corporate workspace to join.

---

## Smoke test (30 seconds)

```bash
mkdir ~/claude-smoke-test && cd ~/claude-smoke-test
echo "console.log('hello')" > hello.js
claude
```

Inside the interactive prompt:

> Read hello.js and tell me what it does.

You should see Claude make a **Read** tool call, then reply. Exit with `/exit` or `Ctrl+D` twice.

---

## Common gotchas

| Symptom | Fix |
|---|---|
| `command not found: claude` | Close and reopen the terminal, or run `exec $SHELL`. Check `echo $PATH` includes `~/.npm-global/bin`. |
| `EACCES` on `npm install -g` | Use the `~/.npm-global` prefix trick above. Never `sudo`. |
| Corporate proxy blocks API | `export HTTPS_PROXY="http://proxy.corp:port"` before running `claude`. |
| Apple Silicon vs Intel | No difference — the npm package is universal. |
| Old Node from `nvm` | Run `nvm use --lts`, then reinstall: `npm install -g @anthropic-ai/claude-code`. |

---

## One-shot verification

Works for any install method:

```bash
echo "claude:  $(claude --version)" \
  && echo "PATH OK: $(which claude)"
```

If both lines print a value, you're ready. Next stop: `/lesson first-session`.

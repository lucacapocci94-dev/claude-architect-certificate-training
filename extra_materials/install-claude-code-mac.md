# Install Claude Code on macOS — Quick Reference

Easy-to-consult, easy-to-test commands. Each block is copy-pasteable; a verify command follows every install step.

> **Requirements:** macOS 12+, Node.js ≥ 18, an internet connection.

---

## 1. Check Node.js

```bash
node --version
```

Expected: `v18.x` or newer. If missing or too old, install via Homebrew:

```bash
brew install node
```

Verify:

```bash
node --version
```

No Homebrew yet? Install it first:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Verify:

```bash
brew --version
```

---

## 2. Install Claude Code

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

## 3. Authenticate

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

## 4. Smoke test (30 seconds)

```bash
mkdir ~/claude-smoke-test && cd ~/claude-smoke-test
echo "console.log('hello')" > hello.js
claude
```

Inside the interactive prompt:

> Read hello.js and tell me what it does.

You should see Claude make a **Read** tool call, then reply. Exit with `/exit` or `Ctrl+D` twice.

---

## 5. Common gotchas

| Symptom | Fix |
|---|---|
| `command not found: claude` | Close and reopen the terminal, or run `exec $SHELL`. Check `echo $PATH` includes `~/.npm-global/bin`. |
| `EACCES` on `npm install -g` | Use the `~/.npm-global` prefix trick above. Never `sudo`. |
| Corporate proxy blocks API | `export HTTPS_PROXY="http://proxy.corp:port"` before running `claude`. |
| Apple Silicon vs Intel | No difference — the npm package is universal. |
| Old Node from `nvm` | Run `nvm use --lts`, then reinstall: `npm install -g @anthropic-ai/claude-code`. |

---

## 6. One-shot verification script

Paste this whole block — it confirms every step is green:

```bash
echo "Node:    $(node --version)" \
  && echo "npm:     $(npm --version)" \
  && echo "claude:  $(claude --version)" \
  && echo "PATH OK: $(which claude)"
```

If all four lines print a value, you're ready. Next stop: `/lesson first-session`.

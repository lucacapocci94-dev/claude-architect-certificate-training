---
description: "Plugins 1/4 — What a Claude Code plugin is: a bundle of skills, commands, hooks, and agents distributed as a single unit. How plugins differ from MCP servers (skills/instructions vs tools/data). Use when the student asks 'what is a plugin', 'is a plugin like a Chrome extension', the difference between a plugin and an MCP server, or invokes /lesson plugins-intro."
command: "lesson plugins-intro"
track: "plugins"
duration_min: 6
---

# Plugins 1/4 — What a Claude Code plugin actually is

**Lesson id:** `plugins-intro`
**Mark complete with:** `python3 .claude/bin/state.py complete plugins-intro`

---

## 1. The simple definition

A Claude Code **plugin** is just a packaged folder of the things you already know:

- **skills** (`SKILL.md` files)
- **slash commands** (`commands/*.md`)
- **hooks** (`settings.json` entries)
- **agents** (subagent definitions)

Distributed as one unit — usually a git repo someone else maintains. You install it; Claude Code reads it the same way it reads your local `.claude/` directory.

> "Un plugin è semplicemente la cartella `.claude/` di qualcun altro, che adesso vive sulla tua macchina e influenza Claude come se l'avessi scritta tu."

That's literally all it is. No magic.

## 2. What plugins are *not*

Two confusions to clear up:

- **Plugins are not MCP servers.** MCP servers add **tools** (functions Claude can call: `github.create_issue`, `postgres.query`). Plugins add **instructions, playbooks, and workflows**. Different layers; they coexist.
- **Plugins are not browser extensions.** They don't intercept anything. They're declarative markdown + a tiny bit of JSON.

| Layer | What it adds | Example |
|---|---|---|
| **MCP server** | Tools, resources, prompt templates | GitHub MCP exposes `list_issues` |
| **Plugin** | Skills, commands, hooks, agents | `superpowers` plugin adds a brainstorming skill |
| **Built-ins** | Read, Write, Bash, Grep, Glob | Ship with Claude Code |

A plugin **can** include an MCP server config — but the concept is broader.

## 3. Why use plugins

1. **Don't reinvent.** Someone solved your workflow; install theirs.
2. **Team scale.** Ship a plugin internally; every dev gets the same setup with one install.
3. **Discovery.** Plugins expose patterns you wouldn't have written yourself.

## 4. Trust, briefly

A plugin runs on your machine with your permissions. Read the source before installing — at minimum, check what hooks it defines (they execute shell commands automatically) and what tools it allow-lists.

Rule of thumb: install plugins from sources you'd `git clone && npm install` from. Same trust bar.

## 5. The marketplace

Today, plugins live on GitHub. There's no central registry yet — discovery is via search, blog posts, and word of mouth. Anthropic's docs link to a few official ones.

Two plugins worth knowing:

- **`superpowers`** — brainstorming → spec → plan → build workflow as skills. Covered in the next lesson.
- **`claude-code-guide`** — meta-plugin that helps with Claude Code itself.

## 6. Hands-on (no install yet)

Have the student browse one or two plugin repos to see the shape:

```bash
# Just browse, don't install yet
xdg-open https://github.com/topics/claude-code-plugin   # or open in browser
```

Notice the structure: it really is just a `.claude/` directory with `skills/`, `commands/`, etc. They could write one themselves. (They will, in lesson 4 of this track.)

## 7. Check question

> "Cosa aggiunge un plugin a Claude Code?
> A. Nuovi modelli linguistici.
> B. Strumenti (functions) come `github.create_issue`.
> C. Skill, slash command, hook e agent custom — istruzioni e workflow, non strumenti.
> D. Una GUI."

Correct: **C**. MCP adds strumenti; i plugin aggiungono il *come* (skill/playbook/workflow).

## 8. Wrap up

> "Sai cosa è un plugin. Adesso installiamone uno. `/lesson plugins-install`."

```bash
python3 .claude/bin/state.py complete plugins-intro
```

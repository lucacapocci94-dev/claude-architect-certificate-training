---
description: "Plugins 2/4 — How to install a Claude Code plugin: the /plugin marketplace flow, manual install by clone, scope (user vs project), and how to verify it loaded. Use when the student wants to install a plugin, asks 'how do I install a Claude Code plugin', '/plugin marketplace', or invokes /lesson plugins-install."
command: "lesson plugins-install"
track: "plugins"
duration_min: 6
---

# Plugins 2/4 — Installing a plugin

**Lesson id:** `plugins-install`
**Mark complete with:** `python3 .claude/bin/state.py complete plugins-install`

---

## 1. Two install paths

### Path A — `/plugin marketplace` (recommended)

Inside `claude`, type:

```
/plugin marketplace
```

You get a browseable list of plugins. Pick one, hit install. Claude Code clones it into the right place and you're done.

### Path B — Manual install (when you want exact control)

A plugin is a folder. To install one manually:

```bash
# User-level (all your projects)
mkdir -p ~/.claude/plugins
git clone https://github.com/<org>/<plugin>.git ~/.claude/plugins/<plugin>

# Project-level (just this repo)
mkdir -p .claude/plugins
git clone https://github.com/<org>/<plugin>.git .claude/plugins/<plugin>
```

Then restart `claude`. The plugin's skills, commands, hooks, and agents load just like your own.

## 2. User vs project (when to choose what)

| Goal | Where to install |
|---|---|
| Personal workflow you want everywhere | `~/.claude/plugins/` |
| Team workflow for this repo | `.claude/plugins/` (and commit it!) |
| Try it without polluting anything | A scratch project's `.claude/plugins/` |

For team projects, **committing** the plugin (or vendoring it) is the only way to guarantee every teammate has the same setup. The alternative is documentation that everyone ignores.

## 3. Verifying

After install + restart, run `/help` in `claude`. The new commands should appear in the list. Run `/<plugin-command>` to confirm it works.

If a plugin defines hooks, they fire automatically — check `cat .claude/settings.json` if you installed at project level, or `~/.claude/settings.json` for user level. The plugin's hooks are merged in.

## 4. Uninstalling

Just delete the folder:

```bash
rm -rf ~/.claude/plugins/<plugin>
# or
rm -rf .claude/plugins/<plugin>
```

Restart `claude`. Gone.

If the plugin added entries to your `settings.json` automatically, you may need to remove those by hand — check the diff.

## 5. Hands-on — install `superpowers`

This is the plugin you'll use in lesson 3 of this track. Install it now:

```bash
mkdir -p ~/.claude/plugins
git clone https://github.com/obra/superpowers.git ~/.claude/plugins/superpowers
```

(If that URL has moved, check the README in the plugin's marketplace listing — the install path is the only thing that changes.)

Restart `claude` in any project. Type `/help`. New skills should appear: brainstorming, spec, plan, etc.

## 6. Anti-patterns

- **Installing 10 plugins at once.** Conflicts and noise. Add one, use it for a week, then add another.
- **Installing a plugin and never reading what it does.** Plugins run hooks on your machine. Read at least the `settings.json` and the README before trusting one.
- **Installing user-level a plugin only used in one project.** Then it loads on every session everywhere.

## 7. Check question

> "Hai trovato un plugin che vorresti che tutto il team usi su un repo specifico. Cosa fai?
> A. Lo installo in `~/.claude/plugins/` e dico a tutti di fare uguale.
> B. Lo clono in `.claude/plugins/<plugin>` del repo, lo committo (o vendor-izzo), tutti lo ricevono al pull.
> C. Lo metto solo nel mio CLAUDE.md.
> D. Apro una PR su Anthropic."

Correct: **B**. Project-level, committed, deterministic for the team.

## 8. Wrap up

> "Hai installato `superpowers`. Adesso impariamo a usarlo per davvero. `/lesson superpowers-plugin`."

```bash
python3 .claude/bin/state.py complete plugins-install
```

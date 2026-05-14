---
description: "Plugins 4/4 — Authoring your own plugin: directory layout, manifest, packaging your skills+commands+hooks as a distributable unit, versioning, sharing inside Accenture. Use when the student wants to create a plugin, asks how to package skills for the team, plugin manifest format, or invokes /lesson plugins-create."
command: "lesson plugins-create"
track: "plugins"
duration_min: 10
---

# Plugins 4/4 — Author your own plugin

**Lesson id:** `plugins-create`
**Mark complete with:** `python3 .claude/bin/state.py complete plugins-create`

---

## 1. When to author a plugin

Author a plugin when **at least two** of these are true:

- You have a workflow you keep reapplying in different projects.
- A teammate has asked you "how do you do that?" more than once.
- You're tired of copying the same `.claude/skills/foo/` folder between repos.

If only one is true, leave it as a per-project setup. Premature plugin = maintenance burden.

## 2. The layout

A plugin is just a folder with the standard `.claude` shape, plus a manifest:

```
my-plugin/
  plugin.json              # manifest (name, version, description)
  README.md                # how to install + what it does
  skills/
    my-skill/
      SKILL.md
  commands/
    my-command.md
  hooks/
    my-hook.sh
  agents/
    my-agent.md
  settings.json            # optional: hooks wiring
```

`plugin.json` example:

```json
{
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "What this plugin does in one sentence.",
  "author": "you@accenture.com",
  "homepage": "https://github.com/you/my-plugin"
}
```

(The exact schema is evolving; check the plugin docs for the current required fields. The folder structure itself is the contract.)

## 3. Authoring loop

Use **this training repo** as the template. It already has everything a plugin needs:

```
.claude/
  skills/<lesson-id>/SKILL.md      ← skills examples
  commands/*.md                    ← slash command examples
  hooks/*.sh                       ← hook examples
  bin/state.py                     ← helper script pattern
  settings.json                    ← hooks wiring
```

Copy the structure, replace the content, you have a plugin.

The authoring loop:

1. Identify the workflow (write it down).
2. Build it as a regular `.claude/` setup in one project.
3. Use it for a week. Iterate.
4. Extract to a new repo as a plugin (with `plugin.json` + README).
5. Test by installing it in a fresh project.
6. Share.

## 4. Skill descriptions are the key

This bears repeating from Core 3/9: the **description** is how Claude discovers your skill. A plugin with vague descriptions has dead skills nobody triggers. Be specific. List trigger phrases.

Look at `.claude/skills/intro-claude-code/SKILL.md` in this repo for the pattern:

```
description: "Foundations 1/5 — What Claude Code actually is, and why it is *not* the same as using Claude in a chat window. Use when ... or invokes /lesson intro-claude-code."
```

Notice: it says **what it covers**, **when to use it**, and **trigger phrases**. Copy that pattern.

## 5. Internal Accenture plugins

For sharing inside Accenture:

- Use the internal Git server.
- Tag versions (`v0.1.0`, `v0.2.0`).
- Document install in the README.
- Maintain a `CHANGELOG.md`.
- Decide on a stability promise (semver or "I'll break it as I learn").

Plugins are code — treat them like a small library. PRs, code review, the lot.

## 6. Hands-on — build a tiny plugin

Have the student build a **two-skill plugin** for their team. Suggestions:

- `commit-message` — a skill that, given a diff, writes a conventional-commit message in the team's house style.
- `pr-template` — fills in the team's PR template given the diff.
- `runbook-incident` — opens an incident runbook template when the user says "we have an incident".

Steps:

```bash
mkdir -p ~/my-plugin/{skills,commands}
cd ~/my-plugin
git init
# create plugin.json, README.md, skills/<x>/SKILL.md, commands/<x>.md
```

Then install it in another project:

```bash
mkdir -p .claude/plugins
ln -s ~/my-plugin .claude/plugins/my-plugin
```

(Symlink while iterating — easier than git pull every time.)

Restart `claude`. Trigger the skill. Iterate.

## 7. Anti-patterns

- **Plugins that do many things.** One plugin = one coherent purpose.
- **Hooks that do work the user didn't ask for.** Surprising users with their own machine is bad UX.
- **No README.** People won't read your SKILL.md — they'll skim the README and bounce.
- **Skipping versioning.** Six months in, two teams on different versions, bug reports unreproducible.

## 8. Check question

> "Vuoi distribuire una skill 'fix-flaky-test' a tutto il dipartimento Cloud&Tech di Accenture. Cosa fai?
> A. La metto nel mio `~/.claude/skills/` e mando un'email con le istruzioni di copia.
> B. Creo un repo plugin con `plugin.json`, README, `skills/fix-flaky-test/SKILL.md`, tag `v0.1.0`. Tutti fanno `git clone` in `~/.claude/plugins/`.
> C. La incollo in uno Slack post.
> D. La metto in CLAUDE.md di ogni repo del dipartimento."

Correct: **B**. Packaged, versioned, installable, updatable.

## 9. Wrap up — Plugins track complete!

That closes the Plugins track. The student now:

- Knows what a plugin is (and isn't)
- Can install and uninstall plugins
- Has used `superpowers` on a real feature
- Can author and share their own plugin

This also marks **the end of the practical curriculum**. Next: the certification domains.

Suggest:

> "Pratica chiusa. Da qui in poi è prep esame: 5 domini, peso 27/18/20/20/15. Si parte da Domain 1 (il più pesante). `/domain1`."

```bash
python3 .claude/bin/state.py complete plugins-create
python3 .claude/bin/state.py set-current --track domains --module domain1 --next "/domain1"
```

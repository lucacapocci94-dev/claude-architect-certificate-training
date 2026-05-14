---
description: "First-time onboarding: collect the student's name, level, and goals."
allowed-tools: ["Bash(python3:*)"]
---

Begin the onboarding flow. Follow these steps **strictly in order**, asking one question at a time and waiting for the answer before moving on.

## Step 1 — Welcome and name

Greet the student warmly in their language. Ask:

> "Come ti posso chiamare durante il corso?" (or, in English: "What should I call you during the course?")

When they answer, store it immediately:

```bash
python3 .claude/bin/state.py set-profile --name "<their name>"
```

## Step 2 — Experience level

Ask which best describes them. Present these four options verbatim:

1. **Absolute beginner** — I have never used Claude or any LLM seriously
2. **Used chat only** — I have used Claude / ChatGPT in a chat window, pasting code snippets, but never an agentic coding tool on a real repo
3. **Tried Claude Code** — I have run `claude` a few times but I do not feel productive yet
4. **Regular user** — I use Claude Code regularly and I want exam-focused prep

Map the answer to one of: `absolute_beginner`, `used_chat_only`, `tried_claude_code`, `regular_user`. Then store it:

```bash
python3 .claude/bin/state.py set-profile --level <mapped-value>
```

## Step 3 — Goals

Ask what they want to get out of this program — pick all that apply:

- Pass the Claude Architect certification
- Become productive in Claude Code day-to-day
- Build a specific agent / tool at work
- Just curious

Save each one:

```bash
python3 .claude/bin/state.py set-profile --goal "<goal-1>" --goal "<goal-2>"
```

## Step 4 — Project context (optional)

Ask if they have a project (work or personal) they intend to use Claude Code with during the course. If yes, capture a one-sentence description:

```bash
python3 .claude/bin/state.py add-note "Project: <short description>"
```

Reassure them that anything they ask you to remember later (`/remember`) will be persisted in `.claude/state/notes.md`.

## Step 5 — Route them

Based on the level, suggest the right starting point and **set the resume pointer** so `/next` works correctly:

- `absolute_beginner` / `used_chat_only`:
  ```bash
  python3 .claude/bin/state.py set-current --track foundations --module intro-claude-code --next "/lesson intro-claude-code"
  ```
  Tell them: "Cominciamo da zero. La prima micro-lezione è `/lesson intro-claude-code` — circa 5 minuti."

- `tried_claude_code`:
  ```bash
  python3 .claude/bin/state.py set-current --track core-concepts --module rules-and-memory --next "/lesson rules-and-memory"
  ```
  Tell them: "Saltiamo l'installazione. Cominciamo dai concetti chiave."

- `regular_user`:
  ```bash
  python3 .claude/bin/state.py set-current --track domains --module domain1 --next "/domain1"
  ```
  Tell them: "Andiamo diretti sulla certificazione. `/domain1` per iniziare."

End by showing them the four orchestrator commands they will use most: `/next`, `/progress`, `/syllabus`, `/remember <something>`.

**Do not start the first lesson in this same response.** End cleanly so they can type the next command themselves — it builds the muscle.

---
description: "Core 6/9 — Subagents: the Task tool, parallel exploration, context isolation between parent and subagent, the Explore subagent vs general-purpose, when to use which, the no-shared-memory rule. Use when the student asks about subagents, the Task tool, parallel work, the Explore agent, or invokes /lesson subagents-intro."
command: "lesson subagents-intro"
track: "core-concepts"
duration_min: 9
---

# Core 6/9 — Subagents

**Lesson id:** `subagents-intro`
**Mark complete with:** `python3 .claude/bin/state.py complete subagents-intro`

---

## 1. The idea in one sentence

A subagent is a **second Claude** that the main session spawns to do a focused job, with its own fresh context, returning only a summary to the parent.

## 2. Why this is huge

1. **Context isolation.** Subagent reads 50 files; parent's context grows by one paragraph.
2. **Parallelism.** Three subagents searching three areas at once = 3× faster.
3. **Specialisation.** Each subagent has its own system prompt and toolset.

## 3. The `Task` tool

The mechanism is the built-in `Task` tool. The parent calls it with:

- `subagent_type` — which agent template to use (`Explore`, `general-purpose`, or a custom agent you defined)
- `description` — short label
- `prompt` — the full briefing for the subagent (it doesn't see the parent's history!)

**Critical:** subagents start cold. They have **none** of the parent's conversation. Everything they need must be in the prompt.

This is the most-missed exam point: students assume subagents inherit context. They don't.

## 4. Two built-in subagents to know

| Agent | Use for |
|---|---|
| `Explore` | Read-only search — "find where X is defined", "which files use Y". Cheap, fast. |
| `general-purpose` | Open-ended work — research, writing code, executing multi-step tasks |

The Explore subagent is the right answer when the parent just needs to **locate** something without burning context reading lots of files.

## 5. Custom subagents — `.claude/agents/`

You can define your own:

```
.claude/agents/code-reviewer.md
```

```markdown
---
description: "Reviews code for security and correctness, returns a punch list."
allowed-tools: ["Read", "Grep"]
---

You are a senior code reviewer. Focus on: SQL injection, XSS, missing input validation, unsafe defaults. Return a short bulleted list. Do not propose fixes — that's a different agent's job.
```

The parent invokes it via `Task(subagent_type="code-reviewer", prompt="...")`.

## 6. The hub-and-spoke pattern

For exam: the canonical multi-agent topology is **hub-and-spoke**:

```
                ┌─→ Subagent A (web research)
Coordinator ────┼─→ Subagent B (doc analysis)
                └─→ Subagent C (synthesis)
```

All communication routes through the coordinator. Subagents **never** talk to each other directly. The coordinator is responsible for: decomposing the task, dispatching, collecting, deduplicating, retrying.

## 7. Hands-on

In the student's repo, have them try the Explore subagent. Inside `claude`:

> "Esplora il repo e trova tutti i posti dove leggiamo da `process.env`. Voglio sapere quali variabili d'ambiente servono."

Watch Claude spawn an Explore subagent. Notice the parent context grows by just a few lines (the summary), not by every file read.

## 8. Anti-patterns

- **Delegating to a subagent and assuming it knows your project.** Brief it like a contractor: paths, conventions, what to ignore.
- **Sequential when parallel works.** If the three subagents have no dependencies, fire them in a **single response** with multiple `Task` calls.
- **Subagent doing critical writes.** Subagents are good for reads and reports; let the parent do the destructive work where the human can see it.
- **No retry / no synthesis.** If a subagent fails, the coordinator must handle it. Don't just propagate the error.

## 9. Check question

> "Devi capire quali file del repo usano una vecchia libreria deprecata. Il repo è grande, vuoi tenere il contesto della sessione corrente leggero. Cosa fai?
> A. Leggo ogni file uno per uno con Read.
> B. Spawn-o un subagent `Explore` con il prompt 'cerca tutti gli import di vecchia-lib e elencali con file:riga'.
> C. Chiedo a Claude di indovinare quali file potrebbero usarla.
> D. Apro l'IDE e cerco a mano."

Correct: **B**. Explore is the cheap, isolated, focused option.

## 10. Wrap up

> "Subagent fatto. Adesso una modalità che cambia tutto: il **plan mode**. `/lesson plan-mode`."

```bash
python3 .claude/bin/state.py complete subagents-intro
```

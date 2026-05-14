---
description: "Core 8/9 — Context window management: tokens, the lost-in-the-middle effect, /clear vs /compact, when to delegate to subagents to keep context light, scratchpad files, and what the SessionStart hook injects. Use when the student asks about context, /compact, /clear, lost-in-the-middle, why Claude forgets, or invokes /lesson context-window."
command: "lesson context-window"
track: "core-concepts"
duration_min: 8
---

# Core 8/9 — Context window management

**Lesson id:** `context-window`
**Mark complete with:** `python3 .claude/bin/state.py complete context-window`

---

## 1. The constraint

Claude has a fixed context window (today: 200k tokens for Sonnet, 1M for some Opus configs). Every message, every tool call, every file read goes into this window. When you run out, the harness compacts (summarises old turns) or you have to clear.

Two costs:

1. **Money.** Tokens are billed.
2. **Quality.** Models suffer from **lost-in-the-middle**: information buried in long context is recalled worse than information near the start or end.

So a 30-turn session full of tool outputs from yesterday's task isn't just expensive — it makes today's task **harder** because the relevant info is drowned.

## 2. The three levers

| Action | When | What it does |
|---|---|---|
| `/clear` | Between unrelated tasks | Hard reset of the conversation. Cheap, fast. |
| `/compact` | Mid-task, context getting heavy | Summarises old turns into a paragraph, keeps recent ones. |
| Delegate to subagent | Reading lots of files | Subagent's context grows; yours doesn't. |

This program enforces lever 3 by design: the orchestrator is supposed to remind you to `/compact-now` after every 2–3 lessons.

## 3. Persistent state across `/clear`

When you `/clear`, the conversation dies. **What survives:**

- CLAUDE.md (re-read on next session)
- `.claude/rules/`, `.claude/skills/`, `.claude/agents/`
- The `SessionStart` hook — runs again, can inject context
- Files on disk (obviously)

The pattern: **write important state to disk** (a scratchpad file, an updated CLAUDE.md note, a `state.py add-note`), then `/clear` freely. This very training program does exactly that.

## 4. Scratchpad files

For longer tasks, drop intermediate findings into a scratchpad:

```bash
# (Claude does this)
cat > .claude/scratch/2026-05-14-rate-limiter-design.md <<'EOF'
- Looked at express-rate-limit, koa-ratelimit, custom.
- Decision: custom with Redis Sorted Set; reasons: ...
- Next: write the implementation in src/middleware/rateLimit.ts.
EOF
```

After a `/clear`, Claude can re-read the scratchpad to continue without re-doing exploration.

## 5. Lost-in-the-middle in the exam

Domain 5 tests this. Three points to remember:

- **Persistent case facts** — for support-style sessions, snapshot the critical facts in a structured block near the top and end, not just buried mid-conversation.
- **Tool result trimming** — long tool outputs should be summarised, not pasted in full.
- **Move recent decisions to the bottom** — recency boost compensates for middle decay.

## 6. Hands-on

Right now in this session, the student can:

1. Run `python3 .claude/bin/state.py show` to see what's persisted on disk.
2. Note that even if you `/clear` this very session, the next one resumes from disk via the SessionStart hook.
3. (Optional) Try `/compact` to feel the difference.

## 7. Anti-patterns

- **One eternal session.** People do this. Two weeks in, the context is 80% noise and quality plummets.
- **Pasting whole files when you only need 20 lines.** Use Read with offset/limit, or grep.
- **Forgetting that compaction loses detail.** If a number is crucial, write it to disk before compacting.
- **Trusting the model to "remember" what you said 50 turns ago.** Re-state critical facts or put them on disk.

## 8. Check question

> "Stai facendo refactoring di un repo grande e sei a 60% di context dopo 2 ore. Ti restano due tipi di azione: scrivere codice (mirate) e capire dipendenze (grosse esplorazioni). Cosa fai?
> A. Continuo finché crasha.
> B. `/clear` e ricomincio da zero senza appoggio.
> C. Scrivo le decisioni prese fino ad ora in uno scratchpad o in CLAUDE.md, poi `/compact` o `/clear`; le esplorazioni successive le delego a un subagent Explore così il context principale resta leggero.
> D. Aumento il modello a Opus."

Correct: **C**. Combine persistence + compaction + delegation. D doesn't solve the *information* problem.

## 9. Wrap up

> "Hai capito come tenere leggero il contesto. Ultima del cuore: l'**MCP**. `/lesson mcp-intro`."

```bash
python3 .claude/bin/state.py complete context-window
```

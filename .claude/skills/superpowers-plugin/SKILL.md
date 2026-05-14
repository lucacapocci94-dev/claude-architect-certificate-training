---
description: "Plugins 3/4 — The superpowers plugin: walk through its brainstorming, spec, plan, and build skills end-to-end on a small feature. Shows how the workflow track concepts (brainstorm → spec → plan → TDD) get encoded as reusable skills. Use when the student wants to try superpowers, asks what superpowers does, the difference between a plugin and a workflow they could write themselves, or invokes /lesson superpowers-plugin."
command: "lesson superpowers-plugin"
track: "plugins"
duration_min: 12
---

# Plugins 3/4 — Using the `superpowers` plugin end-to-end

**Lesson id:** `superpowers-plugin`
**Mark complete with:** `python3 .claude/bin/state.py complete superpowers-plugin`

---

## 1. What `superpowers` is

`superpowers` is a community plugin that encodes — as skills — the exact workflow the certification rewards: brainstorm → spec → plan → build with TDD. Same ideas as the Workflow track of this course, packaged so the **right skill auto-activates** at each stage.

In other words: you said "voglio aggiungere X". `superpowers` notices you're starting fresh, pulls in its brainstorming skill, asks you the right questions, helps you write the spec, plans the slices, runs the TDD loop.

It's not magic. It's our Workflow track, but ready-to-use.

> "Pensa a `superpowers` come a un istruttore tascabile che ti tiene onesto: ti costringe a brainstormare prima di scrivere, a scrivere lo spec prima del piano, il piano prima del codice. Lo stesso loop che abbiamo visto, ma fatto rispettare in automatico."

## 2. Confirm install

Make sure they did `/lesson plugins-install`. Then in `claude`:

```
/help
```

They should see `superpowers`-related commands and skills. If not, restart `claude` or recheck the install.

## 3. End-to-end walkthrough — small real feature

Pick a small, real feature in their project. Example: "add a CSV export to the bookings list."

### Step 1 — Trigger the brainstorming
The student types something like:

> "Voglio aggiungere un export CSV alla lista prenotazioni. Voglio fare le cose bene — usiamo `superpowers`."

`superpowers` activates its **brainstorming skill**. It will ask:

- Which fields go in the CSV?
- What encoding (UTF-8 BOM for Excel)?
- Filters applied at export time?
- Permissions — anyone can export, or admins only?
- Max row count? Streaming for big exports?
- Filename format?

The student answers. **One question at a time**, no front-loading.

### Step 2 — The spec
After enough Q&A, `superpowers` proposes writing a spec — usually to `docs/specs/` or `.claude/specs/`. The student reviews, edits, commits.

### Step 3 — The plan
Now in plan mode (or via the plugin's plan skill), it splits the spec into vertical slices: "slice 1: backend endpoint + minimal CSV"; "slice 2: frontend button"; "slice 3: filters."

### Step 4 — TDD build
For each slice: tests first, then implementation. The plugin enforces this rhythm so the student doesn't slip back into "code first, hope second."

### Step 5 — Done
At the end, the spec, the plan, the tests, and the code all agree. Reviewer reads the spec in 2 minutes, skims the code in 5.

## 4. Compare to doing it yourself

The Workflow track of this course teaches you to do this **by typing the prompts manually**. The plugin does it for you. The trade-offs:

| | Manual workflow | `superpowers` plugin |
|---|---|---|
| Up-front discipline | Required every time | Encoded once |
| Customisability | Total | Limited to plugin design |
| Team-wide consistency | Hard (depends on memory) | Easy (install plugin) |
| Token cost | Lower (focused prompts) | Slightly higher (skill files loaded) |

For solo work where you already practice the discipline, the manual workflow is fine. For teams, plugins win.

## 5. Hands-on

The student does the full end-to-end with a real (small) feature in their repo. Do not rush — this is the longest lesson (12 min) and the most valuable hands-on exercise. By the end they should have:

- A spec under `docs/specs/`
- A plan in `docs/plans/` or in their head
- Tests + minimal implementation of one slice

## 6. Anti-patterns

- **Skipping the brainstorming questions because "you know the answer."** You don't. Let the skill ask.
- **Editing the spec to remove the parts that scare you.** Those are the parts that need to stay in.
- **Implementing all slices in one go.** Defeats the slicing.
- **Using `superpowers` for trivial work.** A rename doesn't need brainstorming.

## 7. Check question

> "Stai per aggiungere una nuova route a un'API in produzione. Hai 30 minuti. Usi `superpowers` o no?
> A. No, troppo overhead.
> B. Sì: in 30 minuti farò brainstorm + spec + slice 1 con test — meglio mezza feature corretta che una intera fragile.
> C. No, in 30 minuti faccio comunque tutto a mano.
> D. Solo se Claude lo decide."

Correct: **B**. The plugin's value is *forcing the discipline* exactly when you don't have time.

## 8. Wrap up

> "Hai usato `superpowers`. Ultima lezione del track: scrivere il tuo plugin. `/lesson plugins-create`."

```bash
python3 .claude/bin/state.py complete superpowers-plugin
```

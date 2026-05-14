---
description: "Alias italiano di /syllabus — mostra il programma del corso, opzionalmente filtrato per modulo."
argument-hint: "[modulo]"
allowed-tools: ["Bash(python3:*)"]
---

Italian alias of `/syllabus`. Same behavior — accepts an optional track filter.

The optional filter is: **$ARGUMENTS**

If `$ARGUMENTS` is empty, print the full curriculum:

```bash
python3 .claude/bin/state.py syllabus
```

If `$ARGUMENTS` is non-empty, filter to that track:

```bash
python3 .claude/bin/state.py syllabus --track "$ARGUMENTS"
```

After the output, in **Italian**: spiega brevemente cosa copre quel modulo (o, senza filtro, una riga per ognuno dei cinque track) e offri il prossimo passo (`/next` o `/lesson <id>`).

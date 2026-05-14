---
description: "Alias italiano di /progress — mostra il tuo avanzamento, opzionalmente filtrato per modulo."
argument-hint: "[modulo]"
allowed-tools: ["Bash(python3:*)"]
---

Italian alias of `/progress`. Same behavior — accepts an optional track filter.

The optional filter is: **$ARGUMENTS**

If `$ARGUMENTS` is empty:

```bash
python3 .claude/bin/state.py show
```

If `$ARGUMENTS` is non-empty:

```bash
python3 .claude/bin/state.py show --track "$ARGUMENTS"
```

Poi, in **italiano**: riassumi in una riga dove si trova lo studente e cosa propone `/next`. Non avanzare automaticamente.

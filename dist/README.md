# Downloadable artifacts

Pre-built, self-contained packages of the training program. Pick the format you prefer and follow the instructions in `INSTALL.md` inside the archive.

| File | Use for |
|---|---|
| `claude-architect-training.zip` | Windows, macOS, anyone who prefers double-clickable archives |
| `claude-architect-training.tar.gz` | Linux / macOS terminal users (`tar -xzf ...`) |

## What's inside each archive

```
claude-architect-training/
  INSTALL.md          ← start here
  CLAUDE.md           ← orchestrator protocol + instructor persona
  .gitignore
  .claude/
    bin/state.py
    commands/         16 slash commands
    hooks/            SessionStart, PreCompact, PostToolUse
    settings.json
    skills/           28 micro-lessons
    state/
      schema/         templates only; per-student state stays local
      README.md
```

No git history, no per-student state files, no PDF reference material — just the bits you need to drop into a project and start learning.

## How to download

### From GitHub web UI
1. Open the file in the GitHub repo: `dist/claude-architect-training.zip`
2. Click **Download raw file** (the down-arrow icon, top right of the file view).

### From the command line
```bash
# Replace <branch> with the branch this lives on (currently claude/formazione-learning-program-RG3Ad)
curl -L -o claude-architect-training.zip \
  "https://raw.githubusercontent.com/lucacapocci94-dev/claude-architect-certificate-training/<branch>/dist/claude-architect-training.zip"
```

### Verify (optional)
```bash
unzip -l claude-architect-training.zip | tail -3
# Should report 92 files.
```

## Refreshing the artifacts

If you change the source `.claude/` or `CLAUDE.md`, rebuild:

```bash
./dist/build.sh   # see below — TODO: add this script if you maintain the program
```

Until that script exists, the build commands are:

```bash
STAGE=/tmp/claude-architect-training
rm -rf "$STAGE" && mkdir -p "$STAGE"
cp -r .claude "$STAGE/"
cp CLAUDE.md .gitignore "$STAGE/"
rm -f "$STAGE/.claude/state/profile.json" \
      "$STAGE/.claude/state/progress.json" \
      "$STAGE/.claude/state/notes.md"
chmod +x "$STAGE/.claude/hooks/"*.sh "$STAGE/.claude/bin/state.py"
( cd /tmp && zip -qr claude-architect-training.zip claude-architect-training \
              && tar -czf claude-architect-training.tar.gz claude-architect-training )
mv /tmp/claude-architect-training.zip /tmp/claude-architect-training.tar.gz dist/
```

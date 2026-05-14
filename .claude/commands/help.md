---
description: "List every command in the training program with a one-line explanation."
allowed-tools: ["Bash(python3:*)"]
---

Print the help screen verbatim, then offer to run any of the listed commands.

```
HELP — Claude Architect Foundations training program
=====================================================

ORCHESTRATOR (where you live day-to-day)
  /start                  First-time onboarding. Collects name, level, goals,
                          and sets your resume pointer. Run this once.
  /next                   Resume from where you left off. Reads
                          progress.json and routes you to the next lesson.
  /progress [track]       Show what you've completed. With no arg, shows
                          everything; with a track name (foundations | core |
                          workflow | plugins | domains), shows just that
                          module's lessons.
  /syllabus [track]       Show the full curriculum. With no arg, shows all
                          28 lessons across 5 tracks; with a track, shows
                          just that track.
  /help                   This screen.

TRACK ENTRYPOINTS (jump into a module)
  /foundations            Foundations Zero — for students who have never
                          used Claude Code. 5 lessons.
  /core                   Core Concepts — rules, commands, skills, hooks,
                          permissions, subagents, plan mode, context, MCP.
                          9 lessons.
  /workflow               Workflow — brainstorming, spec-driven dev, plan
                          mode in depth, iterative refinement, TDD.
                          5 lessons.
  /plugins                Plugins — what they are, how to install,
                          superpowers walkthrough, authoring your own.
                          4 lessons.
  /domain1 ... /domain5   Certification domains (exam-focused). 5 lessons.

LESSONS (granular control)
  /lesson <id>            Run a specific micro-lesson by id, e.g.
                          /lesson init-walkthrough. The id is whatever
                          appears in /syllabus.

STATE & MEMORY (your data, persisted to .claude/state/)
  /remember <text>        Persist a free-form note (project context, goals,
                          blockers). Appended to .claude/state/notes.md and
                          re-read every session.
  /reset-progress         Wipe progress. Add --hard to also wipe profile
                          and notes. Confirms before doing anything.

CONTEXT DISCIPLINE (save tokens, save quality)
  /compact-now            Reminder to free context with the built-in
                          /compact or /clear — your progress is safe on
                          disk so nothing is lost.

ITALIAN ALIASES (same as above, mirroring the student's language)
  /programma [track]      Alias of /syllabus.
  /avanzamento [track]    Alias of /progress.
  /aiuto                  Alias of /help.

BUILT-IN CLAUDE CODE COMMANDS (these are part of Claude Code itself,
not of this training program — but you will use them every day)
  /help                   Claude Code's own help — when typed inside
                          claude, lists all built-in commands too.
  /init                   Walk the repo and generate a CLAUDE.md.
                          Covered in /lesson init-walkthrough.
  /compact                Summarise old turns to free context.
  /clear                  Hard-reset the conversation. Your training
                          progress on disk is unaffected.
  /exit                   Quit claude.
  /mcp                    List connected MCP servers and their tools.
                          Covered in /lesson mcp-intro.
  /plugin marketplace     Browse and install plugins. Covered in
                          /lesson plugins-install.

TYPICAL FLOWS

  First time ever:
    /start                                  -> onboarding
    /next                                   -> first lesson
    (work through Foundations Zero)
    /progress foundations                   -> check the module
    /next                                   -> on to Core Concepts

  Resuming after a break:
    /next                                   -> picks up where you were
    (or: /progress to see the map first)

  Curious about a specific topic:
    /syllabus                               -> find the lesson id
    /lesson <id>                            -> run it directly

  Saving project context for later:
    /remember "I'm building a CSV export
               for the bookings dashboard"
```

After printing, ask the student which one they want to run.

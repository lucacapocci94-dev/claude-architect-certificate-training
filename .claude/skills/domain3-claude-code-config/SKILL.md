---
description: "Domain 3 — Claude Code Configuration & Workflows (20% of exam). Covers: CLAUDE.md hierarchy (user/project/directory level), @import and .claude/rules/, custom slash commands and skills (frontmatter options, context: fork, allowed-tools), path-specific rules with glob patterns, plan mode vs direct execution, the Explore subagent, iterative refinement techniques (examples, test-driven, interview pattern), and CI/CD integration (-p flag, --output-format json, session context isolation). Use when the user wants to study Domain 3 or asks about Claude Code configuration topics — e.g. 'let's start section 3', 'teach me CLAUDE.md hierarchy', 'explain plan mode', 'study domain 3', 'how does CI/CD integration work', 'what are path-specific rules'."
command: "domain3"
---

> **OPTIONAL — certification track only.** Not part of the canonical 1-week productivity path. Only teach when the student has finished Foundations + Core + Workflow + Plugins, or has stated the cert exam as their goal.

This is Domain 3: Claude Code Configuration & Workflows — accounting for **20%** of the exam.

It shows up most often in these scenarios: Code Generation with Claude Code, Developer Productivity Tools, and Claude Code for CI/CD.

This domain is heavily focused on knowing specific configurations. You need to know exactly where files belong and what each setting does — pure reasoning will not compensate for gaps here. Practical, hands-on familiarity is essential.

There are **6 task statements** in this domain. Use the teaching approach defined in CLAUDE.md. Start by gauging the student's Claude Code experience (total beginner / daily user / set it up for an entire team).

## Documentation References

| Topic | Resource | URL |
|-------|----------|-----|
| Claude Code overview (all) | Claude Code — Documentation | https://code.claude.com/docs/en/overview |
| CLAUDE.md hierarchy (3.1) | Claude Code — CLAUDE.md and Memory | https://code.claude.com/docs/en/memory |
| Skills & slash commands (3.2) | Claude Code — Skills | https://code.claude.com/docs/en/skills |
| Hooks (3.2, 3.6) | Claude Code — Hooks | https://code.claude.com/docs/en/hooks |
| Sub-agents & Explore (3.4) | Claude Code — Sub-agents | https://code.claude.com/docs/en/sub-agents |
| MCP integration (3.1) | Claude Code — MCP Integration | https://code.claude.com/docs/en/mcp |
| CI/CD with GitHub Actions (3.6) | Claude Code — GitHub Actions CI/CD | https://code.claude.com/docs/en/github-actions |
| CI/CD with GitLab (3.6) | Claude Code — GitLab CI/CD | https://code.claude.com/docs/en/gitlab-ci-cd |
| Headless / -p flag (3.6) | Claude Code — Headless | https://code.claude.com/docs/en/headless |

## TASK STATEMENT 3.1: CLAUDE.md HIERARCHY

Cover the three configuration tiers:

- **User-level (`~/.claude/CLAUDE.md`)**: scoped exclusively to the individual developer. Not tracked by version control. Not propagated through git. When a new colleague clones the repository, they will NOT inherit these settings.
- **Project-level (`.claude/CLAUDE.md` or root `CLAUDE.md`)**: shared across the entire team. Checked into version control. All collaborators receive these instructions. This is where team-wide conventions belong.
- **Directory-level (subdirectory `CLAUDE.md` files)**: activated only when Claude operates within that particular directory.

Emphasise the most frequently tested trap on the exam:

- A newly onboarded team member does not see the expected instructions
- The underlying issue: the instructions were placed in user-level configuration rather than project-level
- Students should be able to identify this root cause immediately

Cover modular file organisation:

- `@import` directives that pull in external files from within CLAUDE.md (useful for importing relevant standards on a per-package basis)
- `.claude/rules/` folder for splitting rules into topic-focused files (`testing.md`, `api-conventions.md`, `deployment.md`) instead of cramming everything into a single monolithic file

Cover the `/memory` command, which lets you inspect which memory files are currently active. This is your go-to debugging tool when Claude behaves inconsistently between sessions.

**Practice scenario:** Developer A's Claude Code consistently applies the team's API naming conventions. Developer B, who started just last week, gets unpredictable naming suggestions from Claude Code. Both developers are working in the same repository. Provide four answer choices and walk through why the instructions residing in user-level config is the actual cause.

## TASK STATEMENT 3.2: CUSTOM SLASH COMMANDS AND SKILLS

Cover the folder layout:

- `.claude/commands/` = shared at the project level, committed to version control
- `~/.claude/commands/` = private to the individual, not committed
- `.claude/skills/` containing `SKILL.md` files = invoked on demand with configurable behaviour

Cover the skill frontmatter settings:

- `context: fork`: executes the skill inside an isolated sub-agent context. Any verbose output is contained within that fork. The primary conversation remains uncluttered. Ideal for codebase exploration, brainstorming sessions, or any task that generates a lot of noise.
- `allowed-tools`: limits which tools are available during skill execution. Useful for preventing destructive operations while a skill runs.
- `argument-hint`: displays a prompt asking the developer for required input when the skill is invoked without arguments.

Cover the fundamental distinction:

- Skills = triggered on demand for specific tasks (run only when explicitly called)
- CLAUDE.md = loaded automatically and applied universally (always in effect)
- Avoid placing task-specific procedures inside CLAUDE.md. Avoid placing universal standards inside skills.

Cover personal skill customisation:

- Developers can create their own variants under `~/.claude/skills/` using different names
- This keeps personal workflow tweaks separate from the team's shared configuration

**Practice scenario:** A team needs a `/review` command accessible to all members. One particular developer also wants a personal `/brainstorm` skill that generates detailed, verbose output. Walk through which directory each goes in and what frontmatter settings each requires.

## TASK STATEMENT 3.3: PATH-SPECIFIC RULES

Cover `.claude/rules/` files that use YAML frontmatter:

```yaml
---
paths: ["terraform/**/*"]
---
```

These rules are only loaded when the files being edited match the specified glob pattern.

Cover the core advantage over directory-level CLAUDE.md:

- Glob patterns can match files scattered across the ENTIRE project tree
- `**/*.test.tsx` targets every test file no matter which folder it lives in
- A directory-level CLAUDE.md is restricted to just the files within that single directory
- When you need test conventions to apply uniformly to test files distributed across dozens of directories, path-specific rules are the right approach

Cover the token efficiency benefit:

- Path-scoped rules are injected ONLY when editing files that match the pattern
- This cuts down on irrelevant context and saves tokens compared to instructions that are always loaded

**Practice scenario:** A project stores test files alongside source files in over 50 directories. The team wants consistent testing conventions everywhere. Offer four choices: A) path-specific rules with a glob pattern, B) a separate CLAUDE.md in every directory, C) a single root CLAUDE.md, D) a skill. Walk through why option A is the best answer.

## TASK STATEMENT 3.4: PLAN MODE VS DIRECT EXECUTION

Cover the decision framework:

**Use plan mode when:**

- The task involves sweeping, large-scale modifications
- There are several viable approaches that need evaluation before committing to one
- Architectural choices must be made up front
- Changes span many files (e.g., a library migration touching 45+ files)
- Exploration and design should happen before any code is modified

**Use direct execution when:**

- The change is straightforward and narrowly scoped
- A single-file bug fix where the stack trace points to the exact problem
- Adding a simple conditional like a date validation check
- The right approach is already clear before starting

Cover the Explore subagent:

- Keeps noisy, verbose discovery output separate from the main conversation
- Feeds back concise summaries so the main context window stays clean
- Particularly valuable during multi-phase tasks to avoid exhausting the context window

Cover the combined pattern:

- Start with plan mode for investigation and high-level design
- Switch to direct execution to carry out the approved plan
- This hybrid approach is standard in real-world usage and frequently tested on the exam

**Practice scenario:** Present three assignments: (1) decompose a monolith into microservices, (2) fix a null pointer exception inside a single function, (3) swap one logging library for another across 30 files. Have the student categorise each as plan mode or direct execution and explain their reasoning.

## TASK STATEMENT 3.5: ITERATIVE REFINEMENT

Cover the technique hierarchy:

- **Concrete input/output examples (2-3 pairs showing before and after)**: consistently outperform written descriptions alone
- **Test-driven iteration**: define tests first, then share failing test output to steer Claude toward the correct implementation
- **Interview pattern**: instruct Claude to ask clarifying questions before writing code (helps surface considerations you might overlook, especially in unfamiliar domains)

Cover when to combine feedback vs deliver it sequentially:

- Bundle everything in a single message when the fixes are interdependent (adjusting one impacts the others)
- Provide feedback one issue at a time when problems are independent (resolving one has no bearing on the rest)

Cover example-driven communication:

- When natural language descriptions lead to inconsistent interpretations, switch to concrete input/output examples
- Provide 2-3 sample transformations showing what you expect
- Claude generalises more reliably from examples than from prose alone

**Practice scenario:** A developer describes a code transformation using natural language. Claude Code produces different results each time. Ask the student which technique should be tried first (concrete input/output examples) and why it works better.

## TASK STATEMENT 3.6: CI/CD INTEGRATION

Cover the `-p` flag:

- Launches Claude Code in non-interactive (print) mode
- Without this flag, the CI job will stall indefinitely waiting for user input
- This corresponds to Q10 in the sample question set. Commit it to memory.

Cover structured output for CI:

- `--output-format json` combined with `--json-schema`: generates machine-readable structured results
- Downstream automation can parse these findings and post them as inline comments on pull requests

Cover session context isolation:

- The same Claude session that wrote the code is LESS reliable at reviewing its own output
- It carries over its internal reasoning, making it less inclined to challenge its own decisions
- Always use a separate, independent instance for code review

Cover incremental review context:

- When re-running a review after additional commits, feed the previous review findings into the new session
- Tell Claude to flag ONLY new issues or previously reported issues that remain unresolved
- This avoids redundant comments that gradually undermine developer confidence in the tool

Cover CLAUDE.md for CI pipelines:

- Specify testing standards, criteria for meaningful tests, and available test fixtures
- Claude Code running in CI relies on this context to produce high-quality tests
- Without it, generated tests tend to be shallow, low-value boilerplate

**Practice scenario:** A CI pipeline executes `claude "Analyze this PR"` and hangs without ever completing. The logs reveal Claude is waiting for interactive input. Present four possible fixes. Walk through why adding the `-p` flag is the correct solution.

## DOMAIN 3 COMPLETION

Administer an 8-question practice exam:

- 2 questions covering CLAUDE.md hierarchy (3.1)
- 1 question covering commands and skills (3.2)
- 1 question covering path-specific rules (3.3)
- 2 questions covering plan mode vs direct execution (3.4)
- 1 question covering iterative refinement (3.5)
- 1 question covering CI/CD integration (3.6)

Grade the results. If the student scores 7 or higher out of 8, they are ready. Below 7, revisit the weak areas.

**Build exercise:** "Configure a project that includes a CLAUDE.md hierarchy (project-level plus directory-level), a `.claude/rules/` setup with glob patterns targeting test files and API files, a custom skill using `context: fork`, and a CI script that invokes Claude Code with the `-p` flag and produces JSON output."

## NEXT STEPS

You have finished learning Domain 3. The next recommended step is to clear the context with the `/clear` command to avoid unnecessarily wasting tokens and to prevent hallucinations, then start with the next domain by typing `/domain4`.

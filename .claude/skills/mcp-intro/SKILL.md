---
description: "Core 9/9 — MCP (Model Context Protocol): what it is, the relationship to tools and skills, how to install an MCP server, .mcp.json vs ~/.claude.json scoping, env var expansion, build-vs-use decisions. Use when the student asks what MCP is, how to add an MCP server, GitHub MCP, Postgres MCP, or invokes /lesson mcp-intro."
command: "lesson mcp-intro"
track: "core-concepts"
duration_min: 10
---

# Core 9/9 — MCP (Model Context Protocol)

**Lesson id:** `mcp-intro`
**Mark complete with:** `python3 .claude/bin/state.py complete mcp-intro`

---

## 1. What MCP actually is

**MCP = Model Context Protocol.** It is a *standard* for how an LLM client (like Claude Code) talks to an external server that exposes tools, resources, and prompts. Anthropic-designed, open, language-agnostic.

Think of it as **USB for LLM tools**. Anyone can write an MCP server. Any MCP client can use any MCP server.

So when you "install the GitHub MCP", you're not getting a Claude Code-specific plugin — you're connecting to a server that follows the protocol, and the same server works in Claude Code, in Cursor, in any other MCP-aware client.

## 2. What an MCP server exposes

Three kinds of things:

| Thing | Like… |
|---|---|
| **Tools** | Functions the model can call (`github.create_issue`, `postgres.query`) |
| **Resources** | Files the model can read (e.g. `slack://channel/general/recent`) |
| **Prompts** | Pre-baked prompt templates |

The model decides when to use them, just like with built-in tools.

## 3. Installing an MCP server in Claude Code

Two scopes:

| File | Scope |
|---|---|
| `<repo>/.mcp.json` | Project — shared with the team |
| `~/.claude.json` | User — your machine only |

Example `.mcp.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "command": "uvx",
      "args": ["mcp-server-postgres"],
      "env": {
        "POSTGRES_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

The `${...}` syntax expands environment variables at runtime — **never** commit credentials.

## 4. Verifying it works

```bash
claude
```

Then `/mcp` inside the prompt — lists connected servers and their tools. If a server fails to start, the same view shows the error.

## 5. Build vs use (exam topic)

The exam tests when to build your own MCP server vs use a community one:

| Use existing | Build your own |
|---|---|
| GitHub, Slack, Linear, Jira, Postgres | Internal APIs, proprietary systems |
| Standard protocols (HTTP, S3) | Custom auth, custom shapes |
| Active maintenance | Need versioning under your control |
| Free or already trusted | Sensitive data, must self-host |

Default: **use**. Build only when nothing fits.

## 6. MCP vs skills vs tools (clarify)

Students confuse these. Cheat-sheet:

| Layer | What it is | Lives where |
|---|---|---|
| Built-in tools | Read, Write, Bash, Grep, Glob — shipped with Claude Code | Inside the harness |
| Custom tools via MCP | Functions exposed by an MCP server | The MCP server process |
| Skills | Markdown playbooks for tasks | `.claude/skills/` |
| Slash commands | Prompt templates | `.claude/commands/` |

So GitHub-MCP **adds tools** like `github.list_issues`. A skill might *teach Claude when to use them*. Not the same layer.

## 7. Resources are underused

Most students focus on MCP tools and ignore resources. Resources are great when you want to expose **read-only data** to the model: a knowledge base, a Slack archive, a database schema.

Slack channel as a resource > Slack channel via a `get_messages` tool, because resources show up as part of context naturally.

## 8. Hands-on

Have the student install the GitHub MCP server in this very training repo:

```bash
cat > .mcp.json <<'EOF'
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
EOF
```

They need a `GITHUB_TOKEN` env var (a personal access token with `repo` scope). Then:

```bash
export GITHUB_TOKEN=ghp_...
claude
```

`/mcp` should show `github` as connected. Then ask: "elenca le mie issue aperte."

## 9. Anti-patterns

- **Committing secrets in `.mcp.json`.** Use `${ENV_VAR}` always.
- **Installing 10 MCP servers and never using 8.** Each one adds tools to context and noise — install per-project, not per-machine, unless you really use it everywhere.
- **Reaching for MCP when a slash command would do.** MCP is for systems with state; slash commands are for templated workflows.
- **Building a custom MCP for something already public.** Check the registry first: https://github.com/modelcontextprotocol/servers.

## 10. Check question

> "Vuoi che tutto il team possa interrogare il database di staging tramite Claude Code, ma le credenziali sono individuali. Cosa fai?
> A. Metto il server Postgres MCP e le credenziali in `.mcp.json`, committo.
> B. Metto il server in `.mcp.json` (committato) usando `${POSTGRES_URL}`; ogni dev imposta la sua variabile d'ambiente.
> C. Lo metto in `~/.claude.json` di ciascuno separatamente.
> D. Costruisco il mio MCP server custom."

Correct: **B**. Shared config, per-user secrets via env. C lo costringe a duplicare la configurazione 10 volte. A è una leak di credenziali.

## 11. Wrap up — Core Concepts complete!

That closes the Core Concepts track. The student now understands:

- Rules and memory layering
- Slash commands vs skills
- Hooks (deterministic enforcement)
- Permissions (static enforcement)
- Subagents and context isolation
- Plan mode
- Context window management
- MCP

Suggest:

> "Cuore completato. Ora il **workflow**: come essere davvero produttivi. Si parte da `brainstorming`. `/workflow`."

```bash
python3 .claude/bin/state.py complete mcp-intro
python3 .claude/bin/state.py set-current --track workflow --module brainstorming --next "/lesson brainstorming"
```

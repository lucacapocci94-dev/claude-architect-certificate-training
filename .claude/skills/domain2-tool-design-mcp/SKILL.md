---
description: "Domain 2 — Tool Design & MCP Integration (18% of exam). Covers: tool description quality and misrouting fixes, structured error responses (transient/validation/business/permission), tool_choice configuration (auto/any/forced), tool distribution and the 4-5 tools-per-agent guideline, MCP server scoping (.mcp.json vs ~/.claude.json), environment variable expansion, MCP resources, build-vs-use decisions for community servers, and built-in tools (Grep vs Glob, Read/Write/Edit). Use when the user wants to study Domain 2 or asks about tool design and MCP topics — e.g. 'let's start section 2', 'teach me MCP integration', 'explain tool_choice', 'study domain 2', 'how do structured errors work', 'what is tool misrouting'."
command: "domain2"
---

> **OPTIONAL — certification track only.** Not part of the canonical 1-week productivity path. Only teach when the student has finished Foundations + Core + Workflow + Plugins, or has stated the cert exam as their goal.

This is Domain 2: Tool Design & MCP Integration — worth **18%** of the exam.

It shows up mainly in: Customer Support Resolution Agent, Multi-Agent Research System, and Developer Productivity Tools scenarios.

This domain contains **5 task statements**. Follow the teaching structure from CLAUDE.md. Gauge the student's familiarity with MCP and tool design (none / have used MCP tools / have built MCP servers).

## Documentation References

| Topic | Resource | URL |
|-------|----------|-----|
| Tool design & tool_choice (2.1, 2.3) | Claude API — Tool Use | https://platform.claude.com/docs/en/build-with-claude/tool-use |
| MCP overview (2.4) | Model Context Protocol | https://modelcontextprotocol.io/ |
| MCP tools & errors (2.2, 2.4) | MCP — Tools | https://modelcontextprotocol.io/docs/concepts/tools |
| MCP resources (2.4) | MCP — Resources | https://modelcontextprotocol.io/docs/concepts/resources |
| MCP servers & scoping (2.4) | MCP — Servers | https://modelcontextprotocol.io/docs/concepts/servers |
| Built-in tools (2.5) | Claude Code — Documentation | https://code.claude.com/docs/en/overview |
| MCP in Claude Code (2.4) | Claude Code — MCP Integration | https://code.claude.com/docs/en/mcp |

## TASK STATEMENT 2.1: TOOL INTERFACE DESIGN

Emphasize that tool descriptions serve as the CORE mechanism through which LLMs choose which tool to invoke. This is not a nice-to-have — it is THE deciding factor. When descriptions are vague or sparse (e.g., "Retrieves customer information"), the model has no reliable basis for distinguishing between tools with similar purposes.

Cover the elements of an effective tool description:

- A clear statement of the tool's primary function
- Specification of expected inputs (data formats, types, constraints)
- Sample queries the tool is well-suited to handle
- Known edge cases and limitations
- Explicit differentiation: when to reach for THIS tool rather than a similar one

Cover the misrouting issue:

- When two tools share overlapping or nearly identical descriptions, the model struggles to pick the right one
- The exam's Q2 features get_customer and lookup_order with bare-bones descriptions that lead to persistent misrouting
- The correct fix: enrich the descriptions. NOT adding few-shot examples (they increase token cost without addressing the actual root cause), NOT introducing a routing classifier (over-engineered as an initial measure), NOT merging tools into one (disproportionate effort)

Cover tool decomposition:

- Break broad, multi-purpose tools into focused, single-purpose tools with well-defined input/output contracts
- Example: decompose analyze_document into extract_data_points, summarize_content, and verify_claim_against_source

Cover conflicts with the system prompt:

- Keyword-heavy instructions in system prompts can form unintended associations that steer the model away from well-crafted tool descriptions
- After modifying tool descriptions, always audit the system prompt for conflicting directives

Practice scenario: An agent sends "check the status of order #12345" to get_customer rather than lookup_order. Both tools have descriptions like "Retrieves [entity] information." Offer four candidate fixes and walk through why improving the descriptions is the right first move.

## TASK STATEMENT 2.2: STRUCTURED ERROR RESPONSES

Cover the MCP `isError` flag pattern as the standard way to signal failures back to the calling agent.

Cover the four error categories:

- Transient: timeouts, service outages. Safe to retry.
- Validation: malformed input (incorrect format, missing required field). Correct the input, then retry.
- Business: policy-level violations (e.g., refund amount exceeds the allowed limit). NOT safe to retry. Requires an alternative workflow.
- Permission: access denied. Requires escalation or a different set of credentials.

Cover structured error metadata: `errorCategory`, an `isRetryable` boolean, and a human-readable message. For business errors specifically, include retriable: false alongside a customer-friendly explanation so the agent can relay the reason clearly.

Cover the essential distinction between two failure modes:

- Access failure: the tool was unable to reach the underlying data source (timeout, authentication error). The agent must decide whether a retry is warranted.
- Valid empty result: the tool successfully queried the source and returned no matches. The agent should NOT retry — the correct answer is "no results found."
- Mixing up these two cases corrupts recovery logic. The exam specifically tests this distinction.

Cover error propagation in multi-agent architectures:

- Subagents handle transient failures locally through their own retry logic
- They only escalate errors they cannot resolve on their own
- When propagating an error, include any partial results gathered so far along with a summary of what was already attempted

Practice scenario: A tool returns an empty array following a customer lookup. The agent retries three times and then hands off to a human operator. The real problem is that the customer's account simply does not exist. Ask the student to pinpoint the issue (conflating a valid empty result with an access failure) and propose the correct fix.

## TASK STATEMENT 2.3: TOOL DISTRIBUTION AND TOOL_CHOICE

Cover the tool overload problem:

- Assigning 18 tools to a single agent undermines selection accuracy
- The sweet spot is 4-5 tools per agent, each aligned with the agent's role
- A synthesis agent should NOT carry web search tools. A web search agent should NOT carry document analysis tools.

Cover `tool_choice` configuration:

- `"auto"`: the model decides whether to invoke a tool or generate a text response. This is the default. Suitable for general-purpose operation.
- `"any"`: the model MUST invoke a tool but gets to pick which one. Useful when you need guaranteed structured output conforming to one of several schemas.
- `{"type": "tool", "name": "extract_metadata"}`: the model MUST invoke this exact tool. Useful for enforcing a mandatory initial step before any enrichment happens.

Cover scoped cross-role tools:

- For frequent, straightforward operations, provide a constrained version of a tool directly to the agent that needs it
- Example: a synthesis agent receives a scoped verify_fact tool for simple lookups, while more involved verifications still go through the coordinator
- This eliminates coordinator round-trip overhead for the roughly 85% of cases that are straightforward
- The exam's Q9 tests precisely this pattern

Cover replacing open-ended tools with constrained alternatives:

- Rather than granting a subagent fetch_url (which can retrieve anything), provide load_document, which only accepts and validates document URLs

Practice scenario: A synthesis agent keeps returning control to the coordinator for basic fact-checking, adding 2-3 extra round trips per task and inflating latency by 40%. Approximately 85% of these verifications are simple lookups. Present four possible solutions and walk through why a scoped verify_fact tool is the right answer.

## TASK STATEMENT 2.4: MCP SERVER INTEGRATION

Cover the scoping hierarchy:

- Project-level: .mcp.json stored in the project repository. Tracked in version control. Shared across the team.
- User-level: ~/.claude.json. Personal configuration. NOT version-controlled. NOT shared.
- All tools exposed by every configured server are discovered at connection time and become available simultaneously.

Cover environment variable expansion:

- .mcp.json supports the `${GITHUB_TOKEN}` syntax for injecting secrets
- This keeps credentials out of the version-controlled config file
- Individual developers configure their own tokens in their local environment

Cover MCP resources:

- Surface content catalogs (issue summaries, documentation hierarchies, database schemas) as MCP resources
- This lets agents see what data is available without needing to make exploratory tool calls
- Cuts down on unnecessary queries

Cover the build-vs-use decision:

- Prefer existing community MCP servers for common integrations (Jira, GitHub, Slack)
- Only invest in a custom server when team-specific workflows fall outside what community servers can support
- Strengthen MCP tool descriptions to prevent the agent from defaulting to built-in tools (such as Grep) when a more specialized MCP tool exists

Practice scenario: A team wants to connect to Jira. One developer suggests building a custom MCP server from scratch. Ask the student to explain why the team should first evaluate community servers, and under what conditions a custom build becomes the right call.

## TASK STATEMENT 2.5: BUILT-IN TOOLS

Cover the Grep vs Glob distinction:

- Grep: searches inside file CONTENTS for matching patterns. Good for: finding where a function is called, tracking down error messages, locating import statements.
- Glob: matches file PATHS using naming patterns. Good for: discovering files by extension (`**/*.test.tsx`), locating configuration files.
- The exam intentionally sets up scenarios where picking the wrong tool wastes time or produces no results.

Cover Read/Write/Edit:

- Edit: makes targeted modifications by matching unique text strings. Fast and precise.
- When Edit fails (because the text match is not unique): fall back to Read (load the full file) followed by Write (output the complete modified file)
- Read + Write is the dependable fallback whenever Edit cannot locate a unique anchor string

Cover incremental codebase exploration:

- Begin with Grep to identify entry points (function definitions, import statements)
- Follow up with Read to trace imports and execution flow from those entry points
- Do NOT load every file upfront — that drains the context budget fast
- To trace function usage through wrapper modules, first identify exported names, then search for each name across the codebase

Practice scenario: A developer needs to locate every file that invokes a specific deprecated function and also find the corresponding test files for each caller. Walk through the proper tool sequence: Grep for the function name (identifies the callers), Glob for test files whose names match the caller filenames.

## DOMAIN 2 COMPLETION

Administer a 7-question practice exam:

- 2 questions on tool descriptions and misrouting (2.1)
- 2 questions on error handling and error categories (2.2)
- 1 question on tool distribution and `tool_choice` (2.3)
- 1 question on MCP server configuration (2.4)
- 1 question on built-in tools (2.5)

Score the results. If the student gets 6 or more out of 7, they are ready. Below 6, revisit the weak areas.

Build exercise: "Create 3 MCP tools with one intentionally ambiguous pair. Write error responses covering all four error categories. Configure them in .mcp.json with environment variable expansion. Test `tool_choice` forced selection for the first step."

## NEXT STEPS

You have finished learning Domain 2. The next recommended step is to clear the context with the `/clear` command to avoid unnecessarily wasting tokens and to prevent hallucinations, then start with the next domain by typing `/domain3`.

---
description: "Domain 1 — Agentic Architecture & Orchestration (27% of exam). Covers: agentic loop lifecycle and stop_reason handling, hub-and-spoke multi-agent orchestration, subagent invocation with the Task tool and context passing, programmatic workflow enforcement vs prompt-based guidance, Agent SDK hooks (PostToolUse, tool call interception), fixed vs dynamic task decomposition, and session state/resumption strategies. Use when the user wants to study Domain 1 or asks about agentic architecture topics — e.g. 'let's start section 1', 'teach me agentic loops', 'explain multi-agent orchestration', 'study domain 1', 'how do SDK hooks work', 'what is hub-and-spoke'."
command: "domain1"
---

This covers Domain 1: Agentic Architecture & Orchestration, which accounts for **27%** of the exam and carries the highest weight of any domain.

It features prominently across three exam scenarios: Customer Support Resolution Agent, Multi-Agent Research System, and Developer Productivity Tools.

There are **7 task statements** in this domain. Adhere to the teaching structure defined in CLAUDE.md. Begin by gauging the student's experience with agentic systems (no experience / built a basic agent / built multi-agent systems).

## Documentation References

| Topic | Resource | URL |
|-------|----------|-----|
| Agentic loops (1.1) | Claude API — Messages | https://platform.claude.com/docs/en/api/messages |
| Tool execution (1.1) | Claude API — Tool Use | https://platform.claude.com/docs/en/build-with-claude/tool-use |
| Multi-agent orchestration (1.2, 1.3) | Claude Agent SDK — Overview | https://platform.claude.com/docs/en/agent-sdk/overview |
| Subagent invocation (1.3) | Claude Agent SDK — Subagents | https://platform.claude.com/docs/en/agent-sdk/subagents |
| Workflow enforcement & hooks (1.4, 1.5) | Claude Agent SDK — Hooks | https://platform.claude.com/docs/en/agent-sdk/hooks |
| Session state & resumption (1.7) | Claude Agent SDK — Sessions | https://platform.claude.com/docs/en/agent-sdk/sessions |

## TASK STATEMENT 1.1: AGENTIC LOOPS

Cover the full lifecycle of an agentic loop:

- Submit a request to Claude through the Messages API
- Examine the stop_reason field in the returned response
- When stop_reason equals `tool_use`: carry out the specified tool(s), add the tool outputs to the conversation history as a new message, and send the updated history back to Claude
- When stop_reason equals `end_turn`: the agent's work is complete and the final answer should be delivered to the user
- It is essential that tool outputs are appended to the conversation history so the model can incorporate new information in subsequent iterations

Cover the three anti-patterns that frequently appear on the exam:

1. **Using natural language cues to decide when to stop looping** (for instance, checking whether the assistant wrote "I'm done"). This is incorrect because natural language is inherently ambiguous and unreliable. The stop_reason field was designed precisely for this purpose.
2. **Relying on fixed iteration limits as the main termination strategy** (such as "halt after 10 cycles"). This is flawed because it either truncates productive work prematurely or permits wasteful extra iterations. The model indicates completion through stop_reason.
3. **Treating the presence of assistant text as a signal that work is finished** (like "if the response includes text, assume we're done"). This is wrong because the model may return text content alongside `tool_use` blocks in the same response.

Explain the difference between model-driven decision-making (where Claude autonomously determines which tool to invoke based on the current context) and pre-configured decision trees or hard-coded tool sequences. The exam favours model-driven approaches for their adaptability, while reserving programmatic enforcement for critical business logic (explored further in 1.4).

**Practice scenario:** Describe a situation where a developer's agent intermittently stops too early because the code checks `response.content[0].type == "text"` to determine whether the loop should end. Have the student pinpoint the defect and propose the correct fix.

## TASK STATEMENT 1.2: MULTI-AGENT ORCHESTRATION

Cover the hub-and-spoke architecture pattern:

- A central coordinator agent acts as the hub
- Specialised subagents serve as spokes, invoked by the coordinator for targeted tasks
- ALL inter-agent communication passes through the coordinator. Subagents never talk to one another directly.
- The coordinator is responsible for: breaking down the task, choosing which subagents to call, supplying them with the necessary context, combining their outputs, managing errors, and relaying information between them

Cover the critical isolation principle:

- Subagents do NOT automatically receive the coordinator's conversation history
- Subagents do NOT retain memory from one invocation to the next
- Any information a subagent requires must be explicitly provided in its prompt
- This isolation concept is the single most frequently misunderstood aspect of multi-agent systems

Cover the coordinator's key responsibilities:

- Evaluate the incoming query and dynamically decide which subagents to engage (rather than blindly running every subagent in a fixed pipeline)
- Divide the research scope among subagents to reduce overlap (assign separate subtopics or distinct source categories)
- Run iterative refinement cycles: assess the synthesised output for coverage gaps, re-delegate with more focused queries, and repeat until quality thresholds are met
- Channel all communication through the coordinator to ensure observability and uniform error handling

Cover the narrow decomposition failure:

- The exam includes a specific question (Q7 in the sample set) where a coordinator asked to explore "impact of AI on creative industries" breaks the task into only visual-arts-related subtopics, completely overlooking music, writing, and film
- The underlying cause is the coordinator's own decomposition logic, not any downstream subagent
- The exam rewards candidates who trace problems back to their true origin

**Practice scenario:** A multi-agent research system generates a report on "renewable energy technologies" that addresses only solar and wind power, leaving out geothermal, tidal, biomass, and nuclear fusion. Offer four answer choices that point to different parts of the system. The correct answer pinpoints the coordinator's task decomposition as the root cause.

## TASK STATEMENT 1.3: SUBAGENT INVOCATION AND CONTEXT PASSING

Cover the Task tool:

- It is the mechanism through which a coordinator spawns subagents
- The coordinator's `allowedTools` must list "Task"; otherwise, it has no ability to create subagents
- Every subagent is defined by an `AgentDefinition` that specifies its description, system prompt, and permitted tools

Cover context passing:

- Embed the complete results from earlier agents directly into the subagent's prompt (for example, forwarding web search findings and document analysis to a synthesis agent)
- Employ structured data formats that clearly separate content from metadata (source URLs, document titles, page numbers) so attribution is preserved across agents
- Write coordinator prompts that define research objectives and quality standards rather than prescribing step-by-step procedural instructions. This allows subagents to adapt their approach.

Cover parallel spawning:

- Issue multiple Task tool calls within a single coordinator response to launch subagents concurrently
- This yields significantly better latency compared to sequential invocation across separate turns
- The exam assesses awareness of latency trade-offs

Cover `fork_session`:

- Produces independent branches from a common analysis baseline
- Suited for investigating divergent strategies (for instance, evaluating two different testing approaches from the same codebase analysis)
- Each forked branch operates autonomously after the point of divergence

**Practice scenario:** A synthesis agent delivers a report containing multiple claims with no source attribution. Both the web search and document analysis subagents are functioning correctly on their own. Ask the student to determine the root cause (the context passed to the synthesis agent lacked structured metadata) and the remedy (mandate that subagents return structured claim-to-source mappings).

## TASK STATEMENT 1.4: WORKFLOW ENFORCEMENT AND HANDOFF

Cover the enforcement spectrum:

- **Prompt-based guidance:** embed instructions in the system prompt (e.g. "always verify the customer's identity first"). This succeeds most of the time but carries a non-zero failure rate.
- **Programmatic enforcement:** use hooks or prerequisite gates that physically prevent downstream tools from executing until required steps are completed. This guarantees compliance every time.

Cover the exam's decision rule:

- When the consequences involve financial risk, security exposure, or regulatory compliance: programmatic enforcement is required. This is directly tested in Q1 of the sample set.
- When the consequences are low-stakes (such as formatting preferences or stylistic guidelines): prompt-based guidance is sufficient.
- The exam will offer prompt-based solutions as answer choices for high-stakes situations. Always reject them.

Cover multi-concern request handling:

- Break requests that contain multiple distinct issues into separate items
- Investigate each item concurrently while sharing relevant context
- Produce a unified resolution that addresses all concerns

Cover structured handoff protocols:

- When escalating to a human agent, assemble: customer ID, conversation summary, root cause analysis, refund amount (where applicable), and recommended next steps
- The receiving human agent does NOT have access to the full conversation transcript
- Therefore the handoff summary must be completely self-contained

**Practice scenario:** Production logs reveal that in 8% of interactions, a customer support agent issues refunds without first confirming account ownership, occasionally crediting the wrong account. Present four options: A) programmatic prerequisite gate, B) improved system prompt, C) few-shot examples, D) routing classifier. Walk through why A is the right answer and why B, C, and D fall short.

## TASK STATEMENT 1.5: AGENT SDK HOOKS

Cover `PostToolUse` hooks:

- These intercept tool results after execution but before the model processes them
- Use case: standardise inconsistent data formats coming from different MCP tools (for example, converting Unix timestamps to ISO 8601 or translating numeric status codes into human-readable labels)
- The model always receives clean, uniform data regardless of which tool generated it

Cover tool call interception hooks:

- These intercept outgoing tool calls before they are executed
- Use case: block refund operations exceeding $500 and redirect them to a human escalation workflow
- Use case: enforce compliance requirements (such as requiring manager approval for certain actions)

Cover the decision framework:

- Hooks provide deterministic guarantees. Deploy them for business rules that must hold 100% of the time.
- Prompts provide probabilistic guidance. Deploy them for preferences and soft constraints.
- If even a single failure could cost the business money or create legal exposure, use hooks.

**Practice scenario:** An agent sporadically processes international transfers without performing the required compliance checks. Ask the student whether this calls for a hook or enhanced prompt instructions, and have them justify the choice.

## TASK STATEMENT 1.6: TASK DECOMPOSITION STRATEGIES

Cover the two primary patterns:

### Fixed sequential pipelines (prompt chaining):

- Divide work into a predetermined sequence of stages
- Example: review each file individually, then perform a cross-file integration analysis
- Ideal for: predictable, well-structured tasks such as code reviews or document processing
- Strength: delivers consistent, repeatable results
- Weakness: unable to adjust when unexpected findings emerge

### Dynamic adaptive decomposition:

- Create subtasks on the fly based on what each step reveals
- Example: "add tests to a legacy codebase" begins by mapping the project structure, identifying the highest-impact areas, then building a prioritised plan that evolves as new dependencies surface
- Ideal for: exploratory or open-ended investigation tasks
- Strength: responds flexibly to the actual problem
- Weakness: behaviour is less predictable

Cover the attention dilution problem:

- Analysing too many files in a single pass leads to uneven depth of coverage
- Solution: break large reviews into individual per-file analysis passes PLUS a separate cross-file integration pass
- The per-file passes ensure thorough local examination; the integration pass catches cross-file data flow issues

**Practice scenario:** A code review spanning 14 files produces thorough feedback on some files but completely misses obvious bugs in others, and flags a pattern as problematic in one file while accepting the identical pattern elsewhere. Ask the student to diagnose the issue (attention dilution from a single-pass review) and propose the fix (a multi-pass architecture).

## TASK STATEMENT 1.7: SESSION STATE AND RESUMPTION

Cover the session management options:

- `--resume <session-name>`: pick up a specific named session where it left off
- `fork_session`: spawn an independent branch from a shared analysis baseline
- Start fresh with summary injection: open a new session but seed the initial context with a structured summary of earlier findings

Cover when each approach is appropriate:

- **Resume:** the previous context remains largely valid and files have not undergone major changes
- **Fork:** you need to explore competing approaches from the same starting analysis
- **Fresh start:** tool results have gone stale, files have been modified, or context quality has deteriorated over a lengthy session

Cover the stale context problem:

- When resuming after code has been edited, tell the agent about the SPECIFIC files that changed so it can perform targeted re-analysis
- Avoid forcing the agent to re-explore the entire codebase from scratch
- Launching a fresh session with an injected summary tends to be more dependable than resuming when tool results are outdated

**Practice scenario:** A developer resumes a session after modifying 3 files. The agent then provides contradictory guidance about those files because it is still reasoning from outdated tool results. Ask the student to identify the correct strategy.

## DOMAIN 1 COMPLETION

Once all 7 task statements have been covered, administer a 10-question practice exam:

- 3 questions covering agentic loops and orchestration (1.1, 1.2)
- 2 questions covering subagent invocation and context passing (1.3)
- 2 questions covering enforcement and hooks (1.4, 1.5)
- 2 questions covering decomposition strategies (1.6)
- 1 question covering session management (1.7)

Grade the student's responses. A score of 8 or higher out of 10 indicates readiness. Below 8, pinpoint the weak task statements and revisit them with additional practice scenarios.

Conclude with a hands-on build exercise: "Build a coordinator agent with two subagents (web search and document analysis), proper context passing with structured metadata, a programmatic prerequisite gate, and a PostToolUse normalisation hook. Test with a multi-concern request."

## NEXT STEPS

You have finished learning Domain 1. The next recommended step is to clear the context with the `/clear` command to avoid unnecessarily wasting tokens and to prevent hallucinations, then start with the next domain by typing `/domain2`.

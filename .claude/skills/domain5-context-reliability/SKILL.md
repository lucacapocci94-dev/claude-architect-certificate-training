---
description: "Domain 5 — Context Management & Reliability (15% of exam). Covers: context preservation (persistent case facts, lost-in-the-middle effect, tool result trimming), escalation triggers (valid vs unreliable — sentiment and self-reported confidence), structured error propagation (silent suppression and workflow termination anti-patterns), codebase exploration strategies (scratchpad files, subagent delegation, /compact), human review calibration (stratified sampling, field-level confidence), and information provenance (claim-source mappings, conflict handling, temporal awareness). Use when the user wants to study Domain 5 or asks about context management topics — e.g. 'let's start section 5', 'teach me context management', 'explain escalation triggers', 'study domain 5', 'how does error propagation work', 'what is information provenance'."
command: "domain5"
---

This is Domain 5: Context Management & Reliability — worth **15%** of the exam.

Although it carries the lowest weight, the ideas in this domain ripple through Domains 1, 2, and 4. Mistakes here undermine your multi-agent architectures and data extraction workflows.

These concepts surface in nearly every exam scenario, especially Customer Support Resolution Agent, Multi-Agent Research System, and Structured Data Extraction.

This domain contains **6 task statements**. Adhere to the teaching structure defined in CLAUDE.md. Begin by gauging the student's familiarity with long-context applications and multi-agent systems.

## Documentation References

| Topic | Resource | URL |
|-------|----------|-----|
| Context & conversation history (5.1) | Claude API — Messages | https://platform.claude.com/docs/en/api/messages |
| Multi-agent context (5.1, 5.3, 5.4) | Claude Agent SDK — Overview | https://platform.claude.com/docs/en/agent-sdk/overview |
| Subagent delegation (5.4) | Claude Agent SDK — Subagents | https://platform.claude.com/docs/en/agent-sdk/subagents |
| Hook-based error handling (5.3) | Claude Agent SDK — Hooks | https://platform.claude.com/docs/en/agent-sdk/hooks |
| Session resumption (5.4) | Claude Agent SDK — Sessions | https://platform.claude.com/docs/en/agent-sdk/sessions |
| Codebase exploration tools (5.4) | Claude Code — Sub-agents | https://code.claude.com/docs/en/sub-agents |
| Structured errors in MCP (5.3) | MCP — Tools | https://modelcontextprotocol.io/docs/concepts/tools |
| Prompt techniques (5.5, 5.6) | Prompt Engineering Guide | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview |

## TASK STATEMENT 5.1: CONTEXT PRESERVATION

Teach the progressive summarisation pitfall:

- When you condense conversation history, hard facts like dollar amounts, dates, percentages, and customer expectations get diluted into vague generalisations
- For instance, "Customer is requesting a $247.83 refund on order #8891, placed March 3rd" might degrade to "customer is seeking a refund on a past order"
- Solution: isolate transactional facts into a dedicated "case facts" block that persists across every prompt. This block must never be summarised.

Teach the "lost in the middle" phenomenon:

- Models attend most reliably to content at the start and end of long inputs
- Important information positioned in the middle risks being overlooked
- Solution: surface critical findings in a summary at the top of the input. Use clear section headings throughout to aid navigation.

Teach tool result trimming:

- An order lookup might return 40+ fields when you actually need only 5
- Strip tool responses down to the relevant fields BEFORE inserting them into context
- This avoids draining the token budget with accumulated irrelevant information

Teach full history requirements:

- Every subsequent API call must carry the complete conversation history
- Dropping earlier messages destroys conversational continuity

Teach upstream agent optimisation:

- Redesign agents to emit structured outputs (essential facts, citations, relevance scores) rather than verbose narratives and chain-of-thought reasoning
- This is especially important when downstream agents operate under tight context limits

## TASK STATEMENT 5.2: ESCALATION AND AMBIGUITY RESOLUTION

Teach the three legitimate escalation triggers:

- The customer explicitly asks for a human agent: comply right away. Do NOT try to resolve the issue first.
- Policy exceptions or gaps: the request sits outside documented policies (e.g., a competitor price-match when your policy only covers your own website)
- Inability to advance the case: the agent has exhausted its options and cannot move the resolution forward

Teach the two unreliable triggers:

- Sentiment-driven escalation: a frustrated tone does not indicate a complex problem
- Self-assessed confidence scores: the model frequently overestimates certainty on difficult cases and underestimates it on straightforward ones

Teach the frustration distinction:

- When the problem itself is simple but the customer is upset: acknowledge their frustration and propose a solution
- Only escalate if the customer repeats their preference for a human after you have offered assistance
- However, if the customer states outright "I want to speak to a person": escalate at once without attempting further investigation

Teach ambiguous customer matching:

- Several customer records match a lookup query
- Request additional identifiers (email address, phone number, order number)
- Do NOT pick a record using heuristics like most recent activity or highest engagement

## TASK STATEMENT 5.3: ERROR PROPAGATION

Teach structured error context:

- Category of failure (transient, validation, business logic, permission)
- What the system tried to do (the specific query and parameters involved)
- Any partial results collected before the failure occurred
- Possible fallback strategies

Teach the two anti-patterns:

- Silent suppression: handing back empty results disguised as a success. This eliminates any chance of recovery.
- Workflow termination: aborting the entire pipeline because one step failed. This discards all partial progress.

Teach how to distinguish access failure from a valid empty result:

- Access failure: the tool was unable to reach the data source. A retry may be appropriate.
- Valid empty result: the tool reached the source successfully and found zero matches. Retrying is pointless. The empty result IS the correct answer.

Teach coverage annotations:

- Synthesis outputs should flag which conclusions are well-evidenced and which areas have gaps
- For example, "The geothermal energy section is sparse because journal access was unavailable" is far better than quietly leaving it out

## TASK STATEMENT 5.4: CODEBASE EXPLORATION

Teach context degradation:

- During prolonged sessions, the model begins citing "typical patterns" rather than the specific classes or files it identified earlier
- As context fills with verbose exploration output, the model gradually loses track of its own prior discoveries

Teach mitigation strategies:

- Scratchpad files: persist key findings to a file on disk and refer back to it for later questions
- Subagent delegation: spin up subagents for focused investigations while the main agent retains high-level coordination
- Summary injection: condense the results from one exploration phase before dispatching subagents for the next
- /compact: shrink context usage when it becomes bloated with verbose discovery output

Teach crash recovery:

- Every agent serialises its structured state to a predetermined file path (a manifest)
- When execution resumes, the coordinator reads the manifest and injects its contents into agent prompts

## TASK STATEMENT 5.5: HUMAN REVIEW AND CONFIDENCE CALIBRATION

Teach the aggregate metrics pitfall:

- A 97% overall accuracy figure can conceal a 40% error rate on a particular document type
- Always break down accuracy by document category AND field segment before deciding to automate

Teach stratified random sampling:

- Periodically sample even high-confidence extractions for manual verification
- This catches novel error patterns that would otherwise go undetected

Teach field-level confidence calibration:

- The model emits a confidence score for each extracted field
- Set thresholds using labelled validation datasets (ground truth)
- Route fields below the threshold to human reviewers
- Focus scarce reviewer bandwidth on the highest-uncertainty items

## TASK STATEMENT 5.6: INFORMATION PROVENANCE

Teach structured claim-source mappings:

- Every finding should carry: claim + source URL + document title + relevant excerpt + publication date
- Downstream agents must preserve and merge these mappings throughout the synthesis process
- Without this discipline, attribution is destroyed during summarisation

Teach conflict handling:

- Two reputable sources cite different statistics
- Do NOT arbitrarily choose one over the other
- Annotate the output with both values along with their respective source attributions
- Leave the final judgement to the consumer

Teach temporal awareness:

- Always capture publication and data collection dates in structured outputs
- Differing dates often explain differing numbers (they are not contradictions)

Teach content-appropriate rendering:

- Financial data belongs in tables
- News items work best as prose
- Technical findings suit structured lists
- Avoid collapsing everything into a single uniform format

## DOMAIN 5 COMPLETION

6-question practice exam. Score. 5+/6 to pass. Build exercise: "Construct a coordinator backed by two subagents. Implement a persistent case facts block. Simulate a timeout with structured error propagation. Test against conflicting sources and confirm the synthesis retains proper attribution."

## NEXT STEPS

You have finished learning all 5 domains. The next recommended step is to clear the context with the `/clear` command to avoid unnecessarily wasting tokens and to prevent hallucinations, then review any weak areas or take a full practice exam.

---
description: "Domain 4 — Prompt Engineering & Structured Output (20% of exam). Covers: explicit categorical criteria vs vague instructions, false positive trust management, few-shot prompting for consistency and hallucination reduction, structured output via tool_use with JSON schemas (optional/nullable fields, enums), validation-retry loops and their effectiveness boundary, Message Batches API (50% cost, 24h window, custom_id), synchronous vs batch API selection, and multi-instance review with independent sessions. Use when the user wants to study Domain 4 or asks about prompt engineering topics — e.g. 'let's start section 4', 'teach me few-shot prompting', 'explain validation-retry loops', 'study domain 4', 'how does the Batches API work', 'what is structured output with tool_use'."
command: "domain4"
---

This is Domain 4: Prompt Engineering & Structured Output — worth **20%** of the exam.

It shows up mainly in: Claude Code for CI/CD and Structured Data Extraction scenarios.

This domain is deceptively tricky. The incorrect options often sound like solid engineering practice. Choosing the right answer demands knowing exactly which technique solves which particular problem.

This domain contains **6 task statements**. Follow the teaching structure from CLAUDE.md. Gauge the student's prompt engineering background (novice prompting / familiar with few-shot / has built extraction pipelines).

## Documentation References

| Topic | Resource | URL |
|-------|----------|-----|
| Prompt techniques (4.1, 4.2) | Prompt Engineering Guide | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview |
| Structured output & tool_choice (4.3) | Claude API — Tool Use | https://platform.claude.com/docs/en/build-with-claude/tool-use |
| Batch processing (4.5) | Claude API — Message Batches | https://platform.claude.com/docs/en/build-with-claude/message-batches |
| Extended thinking (4.4) | Extended Thinking | https://platform.claude.com/docs/en/build-with-claude/extended-thinking |
| Code examples (4.2, 4.4) | Anthropic Cookbook | https://github.com/anthropics/anthropic-cookbook |

## TASK STATEMENT 4.1: EXPLICIT CRITERIA

Present the foundational principle: precise, categorical criteria vastly outperform vague confidence-based guidance.

- **Wrong approach:** "Be conservative." "Only surface high-confidence findings."
- **Right approach:** "Flag comments exclusively when the described behaviour conflicts with actual code behaviour. Surface bugs and security vulnerabilities. Ignore minor style nitpicks and local coding conventions."

Cover the false positive trust dynamic:

- An elevated false positive rate in a single category erodes user trust across ALL categories
- Solution: temporarily turn off categories with high false-positive rates while you refine the prompts for those categories
- This rebuilds trust while giving you room to iterate

Cover severity calibration:

- Establish explicit severity tiers accompanied by concrete CODE EXAMPLES at each level
- Avoid vague prose descriptions of severity. Provide actual code snippets that illustrate what qualifies as "critical" versus "minor."

## TASK STATEMENT 4.2: FEW-SHOT PROMPTING

Emphasize that few-shot examples are the single most powerful lever for achieving consistency. Not additional instructions. Not confidence thresholds.

Cover when to use them:

- Thorough instructions on their own still yield inconsistent formatting
- The model makes uneven judgment calls when encountering ambiguous situations
- Extraction tasks return empty or null fields for data that is clearly present in the source document

Cover how to build effective examples:

- Include 2-4 carefully chosen examples targeting ambiguous edge cases
- Each example should demonstrate the REASONING behind selecting one course of action over other plausible alternatives
- This teaches the model to generalise to new patterns rather than simply memorising pre-defined cases

Cover the hallucination reduction benefit:

- Providing few-shot examples that demonstrate proper handling of diverse document layouts (inline citations versus bibliographies, narrative text versus structured tables) leads to substantially better extraction accuracy

## TASK STATEMENT 4.3: STRUCTURED OUTPUT WITH TOOL_USE

Present the reliability spectrum:

- tool_use with JSON schemas = completely eliminates JSON syntax errors
- Prompt-based JSON = the model can generate malformed JSON

Clarify what tool_use does NOT guard against:

- Semantic mistakes: individual line items that fail to add up to the stated total
- Misplaced values: data landing in the wrong fields
- Fabrication: the model invents values for required fields when the source material lacks that information

Cover tool_choice options:

- `"auto"`: the default setting. The model may respond with plain text instead of a tool call.
- `"any"`: the model MUST invoke a tool but picks which one. Ideal for guaranteeing structured output when the document type is unknown.
- `{"type": "tool", "name": "..."}`: the model MUST invoke the specified tool. Useful for enforcing a mandatory initial step.

Cover schema design principles:

- Use optional/nullable fields when the source may not contain the relevant data. THIS PREVENTS FABRICATION.
- Include an `"unclear"` enum value for ambiguous situations
- Include an `"other"` option paired with a freeform detail string for open-ended categorisation
- Embed format normalisation rules in the prompt alongside strict schema definitions

## TASK STATEMENT 4.4: VALIDATION-RETRY LOOPS

Cover retry-with-error-feedback:

- Pass back: the original document + the failed extraction attempt + the specific validation error message
- The model leverages the error details to correct itself

Cover the retry effectiveness boundary:

- **EFFECTIVE** for: format discrepancies, structural output errors, values placed in wrong fields
- **INEFFECTIVE** for: data that genuinely does not exist in the source document
- The exam tests both situations. The student needs to determine which type of failure can be fixed by retrying.

Cover detected_pattern fields:

- Attach these to structured findings to record which code construct triggered each finding
- Enables systematic analysis of dismissal trends when developers reject findings
- Feeds into prompt improvement over time based on collected data

Cover self-correction mechanisms:

- Extract `calculated_total` alongside `stated_total` so discrepancies can be flagged automatically
- Include `conflict_detected` boolean fields for cases where source data is internally inconsistent

## TASK STATEMENT 4.5: BATCH PROCESSING

Cover the Message Batches API characteristics:

- Delivers 50% cost reduction
- Processing window of up to 24 hours
- No guaranteed latency SLA
- Does NOT support multi-turn tool calling within a single request
- Relies on `custom_id` to match requests with their corresponding responses

Cover the selection guideline:

- **Synchronous API:** workflows that block other work (pre-merge checks, anything a developer sits and waits for)
- **Batch API:** workflows tolerant of latency (overnight reporting, weekly audits, nightly test generation)
- In the exam's Q11, a manager suggests using batch processing for everything. The correct answer preserves synchronous handling for blocking workflows.

Cover batch failure handling:

- Pinpoint failed documents using their `custom_id`
- Resubmit only the failures with adjustments (e.g., splitting oversized documents into chunks)
- Test and refine prompts on a representative sample BEFORE running the full batch to maximise first-pass success rates

## TASK STATEMENT 4.6: MULTI-INSTANCE REVIEW

Cover the self-review pitfall:

- When a model reviews its own output within the same session, it retains its original reasoning context
- This makes it less inclined to challenge its own earlier decisions
- A separate instance without access to prior context is more effective at catching subtle errors

Cover multi-pass architecture:

- Individual per-file analysis passes: ensures uniform depth of review for each file
- A separate cross-file integration pass: identifies data flow problems that span multiple files
- This approach prevents attention dilution and eliminates contradictory findings

Cover confidence-based routing:

- The model assigns a confidence score to each individual finding
- Findings with low confidence are routed to a human reviewer
- Calibrate the confidence thresholds using labelled validation datasets

## DOMAIN 4 COMPLETION

8-question practice exam. Score. 7+/8 to pass. Build exercise: "Create an extraction tool with JSON schema (required, optional, nullable fields, enums with 'other'). Implement validation-retry. Process 10 documents, add few-shot examples for varied formats, compare before/after extraction quality."

## NEXT STEPS

You have finished learning Domain 4. The next recommended step is to clear the context with the `/clear` command to avoid unnecessarily wasting tokens and to prevent hallucinations, then start with the next domain by typing `/domain5`.

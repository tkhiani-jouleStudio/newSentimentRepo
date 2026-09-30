# Specification: feedback-sentiment-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [ ] Read the project input (`product-requirements-document.md` and `intent.md` at the solution root)
- [ ] Bootstrap agent code in `assets/feedback-sentiment-agent/` using instructions from the `sap-agent-bootstrap` section (invoke from inside `assets/feedback-sentiment-agent/`, use copy commands — do NOT create files manually)
- [ ] Install dependencies, validate the agent starts and responds at `/.well-known/agent.json`

---

## Runtime Skills

Based on the PRD: the sentiment analysis task is well-contained (classify + summarize feedback). No complex multi-step workflows or conditional decision trees are required. Runtime skills are **not needed** — the system prompt is sufficient.

---

## Project-Specific Tasks

### System Prompt & Agent Behaviour

- [ ] Open `assets/feedback-sentiment-agent/app/agent.py` and update the `@prompt_section` body (`get_system_prompt`) with the following instructions:
  - The agent's purpose: analyze customer feedback text, classify each item as positive, negative, or neutral, and produce a concise summary of the overall feedback.
  - Classification rules: return exactly one label per feedback item — `positive`, `negative`, or `neutral`.
  - Summary rules: after classifying all items, generate a concise summary highlighting key themes, overall sentiment trend, and any notable patterns.
  - Output format: return a structured response containing (1) a list of per-item classifications and (2) an overall summary.
  - Accuracy commitment: strive for consistent, context-aware classification. When uncertain, lean toward `neutral`.
  - Do NOT fabricate or invent data. Process only the feedback text provided.
  - If input is empty or invalid, return an informative error message.

### Input Handling (REQ-01)

- [ ] Implement input parsing in the agent's `stream()` method:
  - Accept a single feedback text or a list of multiple feedback texts as user input.
  - Parse the input to extract individual feedback items before classification.
  - Validate input is non-empty; return a structured error message if empty.

### Sentiment Classification (REQ-02)

- [ ] Implement classification logic via LLM tool call:
  - For each feedback item, prompt the LLM to classify sentiment as exactly one of: `positive`, `negative`, or `neutral`.
  - Include classification context in the prompt to improve consistency and reach the 96% accuracy target.
  - Return a list of `{ "feedback": "<text>", "sentiment": "<label>" }` objects.

### Summary Generation (REQ-03)

- [ ] Implement summary generation via LLM:
  - After all items are classified, prompt the LLM to generate a concise summary.
  - Summary must include: overall sentiment trend, key themes, and any notable patterns.
  - Summary should be 2–5 sentences.

### Structured Result Delivery (REQ-04)

- [ ] Ensure the agent returns a structured output object with:
  - `classifications`: list of per-item results `[{ "feedback": "...", "sentiment": "positive|negative|neutral" }]`
  - `summary`: string containing the overall feedback summary
  - `item_count`: total number of feedback items processed

---

## Business Instrumentation

- [ ] Implement business step instrumentation for each milestone using structured logging (`[MILESTONE_ID].[achieved|missed]: [description]`) and OpenTelemetry spans. Extract business logic into plain async helpers (NOT inside `stream()` generator) to avoid `GeneratorExit` issues:

  | Milestone | Log on achievement | Log on miss |
  |-----------|-------------------|-------------|
  | M1: Feedback Ingestion | `M1.achieved: feedback ingestion complete — N items received` | `M1.missed: feedback ingestion failed — input was empty or unparseable` |
  | M2: Sentiment Classification | `M2.achieved: sentiment classification complete — N items classified` | `M2.missed: classification step did not complete for one or more items` |
  | M3: Summary Generation | `M3.achieved: summary generated successfully` | `M3.missed: summary generation returned empty or failed` |
  | M4: Result Delivery | `M4.achieved: structured results delivered to requester` | `M4.missed: result delivery failed — output could not be returned` |
  | M5: Accuracy Validation | `M5.achieved: accuracy target met — classification accuracy >= 96%` | `M5.missed: accuracy target not met — review model and prompt configuration` |

- [ ] Verify `bootstrap(app)` is called after `app = server.build()` in `main.py`

---

## MCP Tool Integration

No SAP API integrations are required for this agent (pure AI-to-LLM). Skip MCP translation, setup-solution for MCP assets, and mock generation.

- [ ] Confirm no `requires` entries are needed in `asset.yaml` beyond what the bootstrap generates

---

## Testing

- [ ] `conftest.py` sets only `IBD_TESTING=true`
- [ ] Write unit tests in `assets/feedback-sentiment-agent/tests/`:
  - `test_input_parsing.py` — tests valid single item, valid list, empty input (error case)
  - `test_classification.py` — tests positive, negative, neutral classification with mocked LLM responses
  - `test_summary.py` — tests summary generation with mocked LLM response
  - `test_structured_output.py` — tests that output contains `classifications`, `summary`, and `item_count`
- [ ] Write one integration test in `assets/feedback-sentiment-agent/tests/test_integration.py`:
  - Submit a list of 3 feedback items (one positive, one negative, one neutral)
  - Assert all three are classified correctly (mocked LLM)
  - Assert summary is non-empty
  - Assert structured output format is correct
- [ ] Run `pytest` from `assets/feedback-sentiment-agent/` (no args) — coverage must be ≥ 70%
- [ ] Verify `assets/feedback-sentiment-agent/app/agent.py` has exactly 9 decorated functions: run `grep -c "^@agent_model\|^@agent_config\|^@prompt_section" assets/feedback-sentiment-agent/app/agent.py` — must return 9
- [ ] Run `pytest` again (no args) to generate final `test_report.json`
- [ ] Verify `test_report.json` exists in `assets/feedback-sentiment-agent/`

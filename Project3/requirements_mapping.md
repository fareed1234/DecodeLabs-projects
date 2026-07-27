# Requirement-to-Implementation Mapping

| Project 3 Requirement | Implementation |
|---|---|
| Restrict the LLM to only use the provided reference text | `<context>` tag lock + Rule 1 (explicit parametric-memory ban) in `prompts/system_prompt.md` |
| Implement strict Negative Constraints | Rule 2 — exact fallback phrase `"Information Not Found"`, no conversational filler allowed |
| Require exact paragraph citations for claims | Rule 3 — `[Para X]` format enforced per sentence/claim |
| Prevent AI hallucination | Rules 1 + 4 combined (no blending outside facts, no guessing) |
| Robustness against distractors / injection | Tests C & D in `tests/test_cases.md`; XML delimiters isolate instructions from data |

## Key Concepts Referenced (from course material)

- **Open-Book vs. Closed-Book paradigm** — this system implements the Closed-Book model: verified corpus only, zero-tolerance hallucination threshold, evaluated like an SAT reading-comprehension test rather than creative writing.
- **The Gatekeeper Mandate** — three pillars: Context Locking, Deflection Protocols, Source Attribution — all implemented in the system prompt.
- **RAG Failure Triage** — awareness of retrieval errors (missing content, missed top-ranked chunks, context truncation) and generation errors (wrong format, incomplete answering) informs why citations and strict formatting rules exist.

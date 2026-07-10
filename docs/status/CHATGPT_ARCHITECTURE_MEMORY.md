# ChatGPT Architecture Memory

**Last Updated:** 2026-06-25

## Immutable Governance Directives
1. **Never mutate Engine Math:** If an integration is failing, check the data flow and payload structure first. Do not rewrite core algorithms. 
2. **Deterministic Data Lineage:** `lifetime_projection` is exclusively owned by `MasterProbabilityEngine`. `top_opportunities` is exclusively owned by `QuestionEngine`. The serialization layers (Extractors) and coordinators (`PipelineRunner`) must never silently drop this data.
3. **Canonical Data Truth:** Always test against actual canonical fixtures (e.g., Raju's chart) rather than purely mocked dictionaries, as the system relies on deep astrological interdependencies.

## Phase 16B Post-Mortem
* **Bug:** `PipelineRunner.answer_question()` explicitly clobbered the `lifetime_projection` array when regenerating the `final_probability` dict for domain-specific queries.
* **Fix:** Explicit preservation of the `lifetime_projection` array during dictionary reconstruction was implemented.
* **Lesson:** When overriding or extending dictionary states in Python, strictly copy or preserve fields that are outside the immediate domain logic to avoid breaking downstream consumers like `QuestionEngine.compose_response()`.

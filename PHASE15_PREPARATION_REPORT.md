# PHASE 15 PREPARATION REPORT

## Architecture Post-Decoupling
Once the Mandali Decoupling Refactor is executed, the Question Engine will be mathematically isolated and highly performant. It will answer all timing queries using only the `NatalPromiseEngine` and `DashaEngine`.

## The Mandali Module (Phase 15)
Phase 15 will focus entirely on building the **Layer 4 Independent Advisory Module** as defined in `ASTROLOGICAL_PREDICTION_GOVERNANCE_v1`.

### Core Responsibilities of Phase 15:
1.  **Independent JSON Generation:** Build a standalone `MandaliEngine` that does not interact with `evaluator.py`. It will simply take a birth chart and output a JSON array of current/future transits.
2.  **Double-Transit Scoring:** Implement the rules of Jupiter and Saturn transits over natal houses, scored independently as "Favorable Climate", "Neutral", or "Challenging".
3.  **LLM Synthesizer Update:** Update the Answer Composer system prompt. It will receive two separate JSON blocks:
    *   Block A: The frozen mathematical conclusion from the Question Engine (e.g., "Marriage Timing is ACTIVE via Jupiter Antardasha").
    *   Block B: The Mandali commentary (e.g., "Saturn is transiting the 7th house, causing delays").
    *   The LLM will be instructed to weave Block B into Block A as *nuance* ("You are currently in a highly favorable period for marriage, though you may experience temporary frustrating delays due to Saturn's transit").
4.  **No Probability Overrides:** Ensure the `MandaliEngine` cannot change the "FAVORABLE" / "MIXED" / "UNFAVORABLE" boolean state passed down by the Question Engine.

### Summary
Phase 15 transitions Mandali from a *Mathematical Constraint* (which crashes formulas if missing) into an *Interpretive Overlay* (which enriches the final natural language answer).

# GOVERNANCE CONSISTENCY REVIEW

## Structural Conflict Detected

**STATUS: FATAL ARCHITECTURAL CONFLICT**

There is a direct and fatal conflict between the newly proposed `ASTROLOGICAL_PREDICTION_GOVERNANCE_v1.md` (which isolates Mandali) and the actual source code currently running in `registry_data.py` and `evaluator.py` (which tightly couples Mandali).

### The Conflict

1. **The New Rule:** "Mandali is STRICTLY EXCLUDED from Formula Evaluator Logic and Formula Family Scoring."
2. **The Current Code:** `registry_data.py` contains 6 Formula Variants that *require* Transit conditions (e.g., `transit_jupiter_aspect_5th_9th`) to pass the boolean gate in the Evaluator. `evaluator.py` actively checks for `"transit" in layer.lower()`. 

If the Governance Rule is accepted and frozen today, the existing Python codebase is immediately rendered non-compliant and functionally broken for all Timing queries.

### Why This Matters

A Formula like `AST_PROP_TIMING` (Property Purchase Timing) currently has 3 required layers:
1. `dasha_activates_4th`
2. `2nd_11th_lord_activation`
3. `transit_jupiter_saturn_activate_4th`

If the Question Engine is isolated from Transit calculations, layer 3 can never be evaluated, meaning the formula will never achieve 100% fulfillment, meaning Property Timing will *always* evaluate as UNFAVORABLE or MIXED, resulting in incorrect astrological predictions.

---

## Recommended Resolution

Before freezing the Governance document, the codebase must undergo a **Mandali Decoupling Refactor**.

**Action Plan:**
1. Eradicate all `TransitEngine` and `transit_...` flags from `registry_data.py`.
2. Delete the `future_gochara_required` parameter from the Python Schema object and the `question_registry.json`.
3. Update `evaluator.py` to remove Transit checks.

**Alternative Option:**
Reverse the Governance change and allow the Question Engine to ingest Mandali math. However, as noted in the previous architectural review, this creates performance bottlenecks and violates the separation of Promise vs. Transit.

**Recommendation:**
**STOP** and approve the Mandali Decoupling Refactor. The code must be cleaned to match the governance before moving forward.

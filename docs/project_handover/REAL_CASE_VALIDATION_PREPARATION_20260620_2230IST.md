# REAL CASE VALIDATION PREPARATION

**SNAPSHOT DATE:** 2026-06-20
**SNAPSHOT TIME:** 22:30 IST

## Validation Tiers

### 20 Case Validation (Alpha)
*   **Scope:** 20 verified celebrity/historical charts with known life events.
*   **Objective:** Confirm basic accuracy of Promise detection (e.g. "Did this person marry late?").

### 50 Case Validation (Beta)
*   **Scope:** 50 diverse charts including edge cases (Neecha Bhanga, severe combustion).
*   **Objective:** Test Dasha activation accuracy (e.g. "Did marriage occur during this specific AD?").

### 100 Case Validation (Release Candidate)
*   **Scope:** 100 double-blind charts.
*   **Objective:** Statistical validation of system accuracy across all 11 domains.

## Validation Workflow
1.  Ingest real-world JSON chart payload.
2.  Route 5 specific questions through the pipeline.
3.  Compare JSON probability/timing output against historical fact.
4.  Log pass/fail metrics.

## Pass Criteria
*   The Question Engine correctly flags `FAVORABLE` / `STRONG` promise matching reality.
*   The Dasha Engine identifies the actual period of manifestation within its array of activated layers.

## Failure Criteria
*   False Positives (Engine predicts marriage, native is lifelong celibate).
*   False Negatives (Engine denies wealth, native is billionaire).
*   Timing Misses (Event occurred outside generated Dasha windows).

## Formula Refinement Loop
If failure occurs, developers must mathematically refine the `registry_data.py` required signals for that variant, rather than injecting hardcoded exceptions.

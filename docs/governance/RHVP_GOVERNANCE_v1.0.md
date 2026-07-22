# Real Horoscope Validation Program (RHVP)
## Governance Framework Version 1.0

### Executive Summary
The Real Horoscope Validation Program (RHVP) is the official framework for scientifically validating the astrological quality of the Samartha Vedic AI System (Version 1.0). The purpose of this program is **NOT software development**, but the rigorous empirical validation of the frozen Golden Master engine against real-world consultation cases.

---

### 1. Validation Workflow
The validation workflow follows a strict, sequential process designed to accumulate statistical evidence rather than isolated anecdotes:
1. **Case Ingestion:** Ingest a real-world horoscope via the standard consultation mechanism.
2. **Deterministic Output:** Run the horoscope through the frozen Version 1.0 engine to generate deterministic baseline readings.
3. **Astrological Assessment:** Compare the engine's output against the known, real-world realities of the native's life.
4. **Observation Generation:** Log any discrepancies, accuracies, or notable engine behaviors into the Validation Register as a **Validation Backlog (VB)** item.
5. **Pattern Analysis:** Aggregate multiple VB items over time to detect statistical patterns across similar planetary placements or formulas.
6. **Domain Review:** Present aggregated, statistically significant patterns to the Domain Authority (Project Owner) for formal review.

---

### 2. Observation Recording Process
Every finding must be meticulously recorded. When an observation is made, the validator must document:
- **Consultation ID:** The anonymous identifier of the chart.
- **Engine Output:** The exact calculation or interpretation produced by the engine.
- **Real-World Reality:** The actual life event or characteristic observed in the native.
- **Delta:** The variance between the engine output and reality.
- **Related Formulas/Factors:** The specific engine components (e.g., `Marriage Prospects`, `Wealth Timing`) involved in the discrepancy.

---

### 3. Observation Categories (Classification)
Every finding must initially be recorded **ONLY** as:
- **VB (Validation Backlog):** An unverified observation pending aggregation and review.

No observation may be converted into actionable engineering/calibration backlogs until explicitly reviewed and approved by the Domain Authority. The actionable categories are:
- **CB (Calibration Backlog):** Approved adjustments to formula weights or threshold constants in the JSON config.
- **EB (Enhancement Backlog):** Approved architectural additions for future engine releases (Version 1.1+).
- **BB (Bug Backlog):** Approved software defects where the code diverges from mathematical astrological rules.

---

### 4. Evidence Requirements
To elevate a Validation Backlog (VB) into a recommendation, the following evidence must be satisfied:
- **Reproducibility:** The behavior must be consistently reproducible on the current Golden Master Version 1.0 architecture.
- **Traceability:** The exact formula path (via the Knowledge Graph) leading to the conclusion must be documented.
- **Multi-Case Corroboration:** The observation must be corroborated across multiple independent horoscopes. **Never recommend software changes directly from a single horoscope.**
- **Statistical Significance:** A discernible pattern must emerge across aggregated data points.

---

### 5. Validation Confidence Levels
Observations are assigned a confidence level based on their evidence accumulation:
- **Level 1 (Isolated):** Observed in a single chart. Action: *Monitor.*
- **Level 2 (Recurring):** Observed in 2-4 charts with similar planetary configurations. Action: *Investigate formula mechanics.*
- **Level 3 (Pattern Established):** Observed in 5+ charts. Action: *Prepare for Domain Authority Review.*
- **Level 4 (Statistically Significant):** High-frequency variance explicitly tied to a specific engine threshold. Action: *Recommend Calibration (CB).*

---

### 6. Rules for Accepting Observations
An observation is accepted into the Validation Register (as a VB) if:
- It is based on a real, verified astrological case study.
- It clearly contrasts the engine's deterministic output against a known historical fact of the native's life.
- It is logged objectively, without speculative engineering assumptions.

---

### 7. Rules for Rejecting Observations
An observation will be immediately rejected if:
- It relies on hypothetical, unverified, or fabricated horoscopes.
- It proposes an immediate software code change based on a single chart anomaly.
- It attempts to bypass the VB classification and act as a direct Bug (BB) or Calibration (CB) request without Project Owner review.

---

### 8. Validation Register Structure
The Validation Register is the central tracking document for all RHVP activity. It must be maintained as a tabular markdown or CSV file containing:
- **VB-ID:** Unique identifier (e.g., `VB-001`).
- **Date Logged:** Date of the consultation.
- **Domain/Formula:** The specific astrological domain (e.g., Career, Marriage).
- **Observation Summary:** Brief description of the variance.
- **Confidence Level:** L1 through L4.
- **Corroborating Cases:** Number of charts exhibiting this pattern.
- **Status:** `OPEN`, `REVIEW_PENDING`, `APPROVED`, `REJECTED`.

---

### 9. Consultation Workflow
During active consultation evaluation, the AI or validator will:
1. Load the chart via standard pipeline methods.
2. Formulate explicit queries using the Question Engine.
3. Extract the `top_opportunities` and `explainability_graph`.
4. Validate the synthesized response against the native's known history.
5. Log any resulting `VB` items in the Validation Register without making immediate system changes.

---

### 10. Monthly Validation Review Process
To ensure disciplined governance, observations are reviewed in batches:
1. **Aggregation:** At the end of the validation cycle, all Level 3 and Level 4 VB items are compiled into a Review Report.
2. **Domain Authority Review:** The Project Owner reviews the statistical patterns and traceability evidence.
3. **Verdict:** The Domain Authority issues a verdict on each proposed pattern:
   - *Approve for Calibration (CB)*
   - *Approve for Enhancement (EB)*
   - *Approve for Bug Fix (BB)*
   - *Reject / Require More Evidence*
4. **Implementation:** Only upon approval do items enter the active engineering queue, adhering to the *Parameter-Driven Evolution* doctrine.

---
**AUTHORIZATION:** RHVP Framework Finalized. Golden Master Version 1.0 Engineering Remains Closed.

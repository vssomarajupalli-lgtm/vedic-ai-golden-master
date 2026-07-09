# FORMULA REPOSITORY RISK REGISTER v1

## 1. Overview
This register tracks structural risks, missing protections, and future implementation hazards identified during the Phase 12C Governance Audit. It serves as a mitigation checklist for the upcoming implementation phases.

---

## 2. Structural & Governance Risks

| Risk ID | Hazard Description | Severity | Mitigation Strategy |
|---|---|---|---|
| **RISK-FR-01** | **Threshold Ambiguity in Confidence Layers** <br> The logic states a template triggers when a "majority" of layers are fulfilled. If 2 layers are positive, 1 is negative, and 1 is neutral, "majority" becomes ambiguous in code. | HIGH | Implementation must define strict logical matrices (e.g., `if True >= 60%`) rather than relying on abstract subjective counting. |
| **RISK-FR-02** | **Context Window Bloat** <br> A complex formula could theoretically request 10 planets, 5 houses, and 4 dashas. This could overwhelm the LLM's context window, leading to hallucination. | MED | Implement a volume validator in the `FormulaValidator` to reject formulas that exceed a maximum threshold of `required_signals`. |
| **RISK-FR-03** | **Graceful Degradation Failure** <br> If a formula demands `TransitEngine` but the server fails to calculate the transit array, the entire query fails. | HIGH | Define a strict fallback protocol. If an engine fails, the formula should downgrade to the `neutral_template` and append an error notification to the response, rather than crashing. |
| **RISK-FR-04** | **Circular Dependencies** <br> Future extensions of the data model might attempt to chain formulas (e.g., Formula B requires Formula A's output). | LOW | Explicitly ban formula chaining in the loader logic. Formulas must only consume raw Engine outputs, never other formulas. |
| **RISK-FR-05** | **Null Payload Hallucination** <br> If the formula requests the 7th house, but the 7th house payload is entirely empty or malformed from the Engine, the Answer Composer might invent data to fill the void. | MED | The `FormulaRepositoryLoader` must perform a strict null-check on the extracted payload before passing it to the LLM, aborting the generation if requested data is missing. |

---

## 3. Future Implementation Hazards (Gochara)

| Risk ID | Hazard Description | Mitigation Strategy |
|---|---|---|
| **HAZ-GO-01** | **Reference Frame Bleed** <br> When `future_gochara_required` activates Moon-centered transits, there is a risk that this setting persists globally and breaks subsequent Lagna-centered queries for the same user session. | The `PipelineRunner` must treat reference-frame shifts as strictly localized, ephemeral state variations that are wiped immediately after the formula resolves. |

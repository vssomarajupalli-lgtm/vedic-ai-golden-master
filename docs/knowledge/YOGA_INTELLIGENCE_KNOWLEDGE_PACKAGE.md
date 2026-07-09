# YOGA INTELLIGENCE KNOWLEDGE PACKAGE

## 1. Executive Summary
The Yoga Engine is a pure detection and classification layer within the Golden Master pipeline. It is responsible for identifying 23 distinct classical astrological yogas (planetary combinations) across 7 major categories (Universal, Pancha Mahapurusha, Wealth, Career, Education, Marriage, Children, Spiritual). Unlike other engines, it assigns no numerical scores, probabilities, or mathematical weights—its output is strictly boolean logic wrapped in an explainability trace.

## 2. Purpose
The purpose of the Yoga Engine is to detect the presence or absence of specific astrological rules and provide an execution trace ("Passed" / "Failed") detailing exactly which conditions were met or missed. This data is intended to be consumed by the Master Probability Synthesis (Future Phase 10E) and the Question Engine to modulate the final domain probabilities.

## 3. Responsibilities
- Receives the normalized JSON chart data (specifically house and planet placements).
- Executes hardcoded Python boolean checks to verify astrological rules (e.g., "Is Jupiter in a Kendra from the Moon?").
- Evaluates dignity requirements for specific yogas.
- Generates a `yoga_traces` object containing an array of rules and their pass/fail status.
- Classifies yogas into `universal_yogas` or house-specific arrays (e.g., `house_2_yogas`).

## 4. Architecture
The architecture is currently highly coupled and imperative. Each yoga is implemented as a dedicated hardcoded python method (e.g., `_detect_gaja_kesari_yoga`). It evaluates data statically and sequentially.

## 5. Inputs
- `chart_data`: The normalized payload output from the JSON normalizer containing planets, houses, and dignity values.
- `planet_results`: (Stubbed) Base structural scores, though currently unused in logic.
- `house_results`: (Stubbed) Base house scores, though currently unused in logic.

## 6. Outputs
- `universal_yogas` (list): Names of yogas that apply globally to the chart.
- `house_X_yogas` (list): Arrays grouping yogas to their primary domain of impact.
- `yoga_traces` (dict): Detailed rule-by-rule execution trace for all 23 evaluated yogas.
  - `status` ("PASSED" or "FAILED")
  - `rules` (list of dicts containing the rule string and boolean result)
  - `failure_reason` (string explaining which exact rule failed)

## 7. Data Contracts
- Outputs adhere to an explainability contract where every failure must return a human-readable `failure_reason` intended for the UI Verification Console.

## 8. Engine Dependencies
- **Upstream:** None mathematically (it relies only on the raw parsed chart data).
- **Downstream:** Consumed by the `PipelineRunner` and passed to the `NatalPromiseEngine` (though currently unused in the 4-pillar formula). Intended for the `QuestionEngine`.

## 9. Formula Dependencies
- **Implicit Dependency:** `YOGA_REGISTRY` from `app.config.yoga_registry`. However, the logic itself is entirely hardcoded in Python methods.

## 10. Business Rules
- **Pure Detection:** The engine applies zero mathematical weighting. It strictly returns boolean states.
- **Dignity Requirements:** Many yogas (e.g., Saraswati Yoga, Lakshmi Yoga) strictly require specific dignities (Own Sign, Exalted) to trigger a `PASSED` status.

## 11. Deterministic Rules
Implements 23 deterministic boolean combinations, including:
- **Gaja Kesari:** Jupiter in Kendra from Moon.
- **Neecha Bhanga Raja:** Dispositor of a debilitated planet positioned in a Kendra.
- **Ruchaka/Bhadra/Hamsa/Malavya/Sasa:** Planet in Kendra + Strong Dignity.
- **Dhana:** 2nd and 11th Lords conjunct.

## 12. Execution Flow
1. Receives normalized chart data.
2. Initializes output dictionaries.
3. Sequentially calls all 23 `_detect_...` methods.
4. If a method returns `PASSED`, the `add_trace()` helper appends the yoga to the appropriate `universal` or `house_X_yogas` array.
5. Returns the fully populated trace payload.

## 13. Implementation Files
- `backend/app/engines/yoga_engine.py`

## 14. Documentation Files
- No external architectural documentation exists solely for the Yoga Engine.

## 15. Governance References
- `docs/architecture/FORMULA_MASTER_INDEX_PLAN.md` (Designates `YOG-001` through `YOG-023`)

## 16. Technical Debt
- **Hardcoded Logic:** 23 complex business rules are embedded as Python code instead of being loaded from the central Formula Registry.
- **Pipeline Disconnection:** The Yoga results are generated but are largely ignored by the current `NatalPromiseEngine` and `HouseStrengthEngine`, meaning yogas currently have no mathematical impact on the final Master Probability score.

## 17. Missing Documentation
- Documentation defining exactly how a `PASSED` yoga should mathematically modify the Master Probability score (e.g., +15% per Phase 10E proposal).

## 18. Recommendations
- **Refactor to Registry (Phase 10A):** Delete the 23 Python methods and replace them with a dynamic evaluator that reads `YOG_` formulas from `registry_data.py`.
- **Integrate Mathematics:** Update the Master Probability formula to mathematically reward charts that possess passing yogas, as outlined in the Phase 10E implementation plan.

## 19. Formula Integration (Yoga Data Model)
*Migrated from `docs/architecture/FORMULA_REPOSITORY_DATA_MODEL_v1.md` (CON-004 Resolution)*
- **Yoga Support Confidence Layer**: Within the broader formula data model, Yogas function as a specific confidence layer. Their structural role is to define named mathematical combinations that amplify or rescue a base astrological assessment.
- **Data Structure**: Yogas are not calculated within the formula. The formula merely checks if the Yoga Engine trace output contains a `PASSED` status for the specific required Yoga.

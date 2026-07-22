# Validation Execution Checklist
*Strict operational sequence for executing a validation run.*

**Case ID:** `CASE-###`

## Execution Sequence
1. [ ] **Load Version 1.0:** Ensure the environment is strictly running Golden Master v1.0.
2. [ ] **Run deterministic pipeline:** Feed the centralized `canonical_content.json` (referenced in `CASE_METADATA.md`) into the engine.
3. [ ] **Generate consultation report:** Extract the `top_opportunities` and complete deterministic output.
4. [ ] **Compare with Ground Truth:** Cross-reference the engine's output against the verified `ground_truth.md`.
5. [ ] **Record observations:** Document all findings (successes and variances) in `validation_notes.md` and the Validation Register.
6. [ ] **Create VB entries if necessary:** Log new anomalies as `VB-###` in the Observation Register.
7. [ ] **Update Evidence Register:** If a VB correlates with an existing pattern, append the case to the respective `EVD-###` file.
8. [ ] **Close case:** Mark the case as fully processed in the local RHVP tracking system.

*CRITICAL RULE: No software modifications are permitted during execution.*

# Observation Register Template
*(This register aggregates all active Validation Backlog (VB) items across the system)*

| VB-ID | Initial Logging Date | Domain / Formula | Description of Variance | Initial Source Case | Confidence Level | Current Status | EVD Reference |
|-------|----------------------|------------------|-------------------------|---------------------|------------------|----------------|---------------|
| `VB-###` | YYYY-MM-DD | e.g. Marriage Timing | Formula triggered late marriage due to Saturn, but native married early | `CASE-###` | L1 | OPEN | `EVD-###` |
| | | | | | | | |
| | | | | | | | |

## Status Enumeration
- **OPEN:** Validation Backlog is tracking new cases.
- **LOCKED:** Sufficient evidence collected. Pending Domain Authority review.
- **ELEVATED:** Promoted to Calibration Candidate (`CC-###`).
- **REJECTED:** Observation deemed invalid or not statistically reproducible.

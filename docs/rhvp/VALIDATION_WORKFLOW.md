# Real Horoscope Validation Program (RHVP)
## Operational Infrastructure & Workflow

### 1. Folder Structure
The RHVP infrastructure resides in `docs/rhvp/` and is strictly isolated from core engineering documentation.
```
docs/rhvp/
├── templates/
│   ├── VALIDATION_REGISTER_TEMPLATE.md
│   ├── OBSERVATION_REGISTER_TEMPLATE.md
│   ├── EVIDENCE_REGISTER_TEMPLATE.md
│   └── MONTHLY_VALIDATION_REVIEW_TEMPLATE.md
├── registers/
│   ├── validation/        (Holds individual validation records per horoscope)
│   ├── observation/       (Holds aggregated observations across horoscopes)
│   └── evidence/          (Holds corroborating statistical evidence)
├── reviews/               (Holds Monthly Validation Reviews)
├── CALIBRATION_CANDIDATE_REGISTER.md  (Empty queue for Domain Authority review)
└── VALIDATION_WORKFLOW.md
```

### 2. Naming Conventions & Numbering Scheme
- **Horoscope Identifiers (Cases):** `CASE-YYYYMMDD-###` (e.g., `CASE-20260801-001`)
- **Validation Backlog Items:** `VB-###` (e.g., `VB-042`)
- **Evidence Files:** `EVD-###` (e.g., `EVD-042` maps to `VB-042`)
- **Calibration Candidates:** `CC-###` (e.g., `CC-007`)
- **Monthly Reviews:** `MVR-YYYY-MM` (e.g., `MVR-2026-08.md`)

### 3. Lifecycle of a Validation Observation
1. **Case Validation:** A horoscope (`CASE-***`) is tested against the deterministic engine. Results are logged in a Validation Register.
2. **Observation Capture:** Any discrepancy or variance is logged as a Validation Backlog (`VB-###`) in the Observation Register.
3. **Evidence Accumulation:** As multiple charts exhibit the same variance, the findings are aggregated in an Evidence Register (`EVD-###`), raising the Confidence Level from L1 (Isolated) up to L4 (Statistically Significant).
4. **Candidate Elevation:** Once a `VB-###` reaches L3 or L4, it is moved to the `CALIBRATION_CANDIDATE_REGISTER.md` as a Candidate (`CC-###`).
5. **Monthly Review (Approval Workflow):** During the monthly cycle, the Project Owner reviews all `CC` items. Approved candidates transition to Engineering via a formal Calibration Backlog (CB), Enhancement Backlog (EB), or Bug Backlog (BB).

### 4. Review Checkpoints
- **Checkpoint 1 (Intake):** Ensure the `CASE` relies on factual, historical data, not theoretical placement assumptions.
- **Checkpoint 2 (Aggregation):** Ensure the `EVD` actually maps to the exact same formula threshold before raising the Confidence Level.
- **Checkpoint 3 (Candidate Gate):** Ensure a `VB` is not elevated to `CC` without a minimum of 5 corroborating cases (L3+).
- **Checkpoint 4 (Domain Authority Gate):** The Project Owner reviews the `MVR` before any `CB` is authorized for software development.

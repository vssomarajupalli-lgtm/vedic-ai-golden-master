# ARCHITECTURE DECISION LOG
**Version:** 1.0

This log acts as the central index for all formal Architecture Decision Records (ADRs) within the Golden Master repository.

## Phase A: Repository Structure & Governance

| ADR ID | Title | Domain | Original Phase | Canonical Owner | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [ADR-001](docs/architecture/decisions/ADR-001.md) | YAML as the Canonical Formula Storage Format | Repository Structure | Phase 10 | Formula Repository | Accepted |
| [ADR-002](docs/architecture/decisions/ADR-002.md) | Single JSON Array Format for Question Registry | Repository Structure | Phase 11 | Question Registry | Accepted |
| [ADR-003](docs/architecture/decisions/ADR-003.md) | Prohibition of Hardcoded Astrological Rules | Governance | Phase 9 | Engine Architecture | Accepted |

---
## Phase B: Engine Architecture

| ADR ID | Title | Domain | Original Phase | Canonical Owner | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [ADR-004](docs/architecture/decisions/ADR-004.md) | Prohibition of Aggregating Promise, Dasha, and Transit Scores | Engine Architecture | Phase 15 | Engine Architecture | Accepted |
| [ADR-005](docs/architecture/decisions/ADR-005.md) | Prohibition of LLM-Driven Astrological Decision Making | Engine Architecture | Phase 14 | Engine Architecture | Accepted |
| [ADR-006](docs/architecture/decisions/ADR-006.md) | Mandali as an Interpretive Overlay (Decoupled from Core Math) | Engine Architecture | Phase 15 | Engine Architecture | Accepted |
| [ADR-007](docs/architecture/decisions/ADR-007.md) | The 24 Master Node to 200+ Question Expansion Blueprint | Engine Architecture | Phase 9 | Question Registry | Accepted |
| [ADR-008](docs/architecture/decisions/ADR-008.md) | Evaluate Once, Consume Many (Single Source of Truth) | Engine Architecture | Phase 12 | Formula Evaluator | Accepted |
| [ADR-009](docs/architecture/decisions/ADR-009.md) | Deterministic Mapping Matrix (Replacement of NLP Routing) | Engine Architecture | Phase 9 | Question Registry | Accepted |

---
## Phase C: Formula Architecture & Data Model

| ADR ID | Title | Domain | Original Phase | Canonical Owner | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [ADR-010](docs/architecture/decisions/ADR-010.md) | Formula Scaling via Many-to-One Convergence Rule | Formula Architecture | Phase 14 | Formula Repository | Accepted |
| [ADR-011](docs/architecture/decisions/ADR-011.md) | Exclusion of the Moon from the Biological Progeny Promise | Data Model | Phase 14 | Formula Repository | Accepted |
| [ADR-012](docs/architecture/decisions/ADR-012.md) | Non-Numeric Confidence Model (Boolean Layering) | Data Model | Phase 12 | Formula Evaluator | Accepted |

---
*(Later phases will be appended here as they are recovered and approved)*

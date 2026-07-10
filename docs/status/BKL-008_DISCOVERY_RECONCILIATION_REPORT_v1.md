# BKL-008 Discovery Reconciliation Report v1

**Date:** 2026-07-09
**Program:** GM-005 Repository Refinement
**Phase:** BKL-008 Discovery Reconciliation

---

## 1. Is ARP-002 Actually Incomplete?

**Conclusion: WITHDRAWN (ARP-002 is Complete)**

The previous discovery report erroneously concluded that ARP-002 (Root Directory Clutter Relocation) was incomplete due to the presence of `BKL-*` and `PHASE14F-*` files in the root directory. 

**Repository Evidence:** A review of `docs/status/BKL-007_CONSTITUTIONAL_VALIDATION_REVIEW_v1.md` confirms that ARP-002 targeted the relocation of 135 legacy markdown files. A structural assessment confirms these files were successfully relocated. The remaining files in the root directory are strictly related to the active GM-005 Refinement program or recent Phase 14F completion.

Therefore, I explicitly **withdraw** the previous finding. ARP-002 was successfully completed during BKL-007.

## 2. Root Directory Assessment

Based on the rule prohibiting the relocation of active milestone artifacts during GM-005, the root directory is classified as follows:

| File | Classification | Recommendation |
| :--- | :--- | :--- |
| `.gitignore` | Permanent Root File | Retain in root |
| `docker-compose.yml` | Permanent Root File | Retain in root |
| `pytest.ini` | Permanent Root File | Retain in root |
| `docs/governance/BKL-006_CHIEF_ARCHITECT_DECISION_REGISTER.md` | Active Milestone Artifact | Retain in root for GM-005 duration |
| `docs/status/BKL-007_ARCHITECTURAL_REFINEMENT_PLAN_v1.md` | Active Milestone Artifact | Retain in root for GM-005 duration |
| `docs/status/BKL-007_ARCHITECTURE_EVIDENCE_REPORT_v1.md` | Active Milestone Artifact | Retain in root for GM-005 duration |
| `docs/status/BKL-007_CONSTITUTIONAL_VALIDATION_REVIEW_v1.md` | Active Milestone Artifact | Retain in root for GM-005 duration |
| `docs/status/BKL-007_REPOSITORY_DISCOVERY_REPORT_v1.md` | Active Milestone Artifact | Retain in root for GM-005 duration |
| `docs/status/BKL-008_REPOSITORY_DISCOVERY_REPORT_v1.md` | Active Milestone Artifact | Retain in root for GM-005 duration |
| `docs/archive/PHASE14F_QUESTION_REGISTRY_DIFF.txt` | Active Milestone Artifact | Retain in root for GM-005 duration |
| `docs/archive/PHASE14F_REGISTRY_DATA_DIFF.txt` | Active Milestone Artifact | Retain in root for GM-005 duration |
| `REPOSITORY_TREE_BKL008.txt` | Temporary Working Artifact | Can be safely deleted at phase end |

## 3. Documentation Architecture Assessment

The `docs/` hierarchy exhibits severe semantic overlap and structural fragmentation across 10 identified domains.

| Directory | Purpose | Owner | Overlap | Recommendation | Merge Required? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `archive` (94 files) | Deprecated artifacts | Architecture | Overlaps with handover/project_handover | Consolidate all deprecated materials here | Yes |
| `handover` (14 files) | Legacy project transitions | Architecture | Overlaps with archive | Deprecate and move to archive | Yes |
| `project_handover` (11 files) | Legacy project transitions | Architecture | Overlaps with archive | Deprecate and move to archive | Yes |
| `current` (4 files) | Active project state | Governance/Architecture | Overlaps with status/current_status | Merge into status | Yes |
| `current_status` (13 files) | Active project state | Governance/Architecture | Overlaps with status/current | Merge into status | Yes |
| `status` (66 files) | Active project state | Governance/Architecture | Overlaps with current/current_status | Establish as single source of truth for state | Yes |
| `knowledge` (18 files) | Technical context | Engineering | Overlaps with reference | Establish as single source of truth for context | Yes |
| `reference` (9 files) | Technical context | Engineering | Overlaps with knowledge | Merge into knowledge | Yes |
| `implementation` (8 files) | Active building specs | Engineering | Overlaps with validation | Consolidate under engineering/ | Yes |
| `validation` (6 files) | Testing specs | Engineering | Overlaps with implementation | Consolidate under engineering/ | Yes |

## 4. Legacy Pipeline Assessment

**Target:** `backend/archive_legacy_pdf_pipeline`

**Repository Evidence:** A programmatic `grep` search for `archive_legacy_pdf_pipeline`, `pdf_text_extractor`, and `index_reader` confirms that absolutely zero files within the active backend (`app/`, `main.py`, `run.py`) import or reference this module. The module is fully isolated and only referenced by its own internal tests.

**Recommendation:** **Remove**
As this is verified dead code that is actively polluting the operational backend namespace, it should be deleted. (If archival is constitutionally demanded, it may be zipped and placed in `docs/archive`, but deletion is preferred for source trees).

## 5. Frontend Engineering Assessment

**Target:** `frontend/package.json`

**Repository Evidence:** Inspection of the `package.json` confirms the absence of any testing libraries (Vitest, Jest) or testing execution scripts. Testing is genuinely absent.

**Classification:** **Future GM Milestone**
This is an engineering and CI/CD implementation requirement. It is out of scope for a *Repository Refinement* phase (GM-005) and should be deferred to a future functional milestone.

## 6. Backlog Reconciliation

Based on the evidence, the previously proposed BKL-008 backlog items are reconciled as follows:

| Previous Item | Reconciled Status | Repository Evidence / Justification |
| :--- | :--- | :--- |
| **BKL-008-1:** Execute Root Relocation (ARP-002) | **Invalid** | ARP-002 was completed. Remaining files are active milestone artifacts; moving them violates the GM-005 active artifact rule. |
| **BKL-008-2:** Initialize Frontend Testing | **Future GM Milestone** | Identified as an engineering task, not a structural repository refinement task. |
| **BKL-008-3:** Remove Legacy PDF Pipeline | **Valid** | Confirmed as dead code in the operational backend namespace. |
| **BKL-008-4:** Consolidate Documentation Taxonomy | **Valid** | Severe semantic overlap exists across `archive`, `status`, `knowledge`, and `handover` domains. |

## 7. Final Recommendation

Based on the reconciled repository evidence, the TRUE architectural objective for BKL-008 must be strictly focused on structural consolidation and legacy eradication.

**Recommended Objective for BKL-008:**
*Execute a comprehensive documentation taxonomy consolidation to merge overlapping domains (`archive`, `status`, `knowledge`), and eradicate isolated dead code (`backend/archive_legacy_pdf_pipeline`) to establish a unified, low-noise structural baseline for the Golden Master.*

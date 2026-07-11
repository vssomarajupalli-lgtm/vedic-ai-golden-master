# ENGINE KNOWLEDGE OWNERSHIP MAPPING

## SECTION 1: Document Information

* **Date**: 2026-06-29
* **Repository**: D:\vedic-ai-golden-master
* **Project**: SVAI-GM
* **Program**: Program B
* **Milestone**: GM-005
* **Knowledge Domain**: Engine Knowledge
* **Version**: v1.0
* **Status**: DRAFT
* **Author**: Coding Engine

---

## SECTION 2: Purpose

The Golden Master repository must maintain absolute architectural clarity. This document establishes the permanent ownership of every deterministic engine knowledge asset. 

Every engine shall have exactly:
* **One Canonical Knowledge Owner** (the single package that dictates its domain rules)
* **One Architectural Definition** (its boundaries and data contracts)
* **One Primary Knowledge Package**

Supporting references may reference the engine but shall never redefine its logic, constraints, or ownership boundaries.

---

## SECTION 3: Engine Knowledge Ownership Registry

| Engine | Canonical Knowledge Owner | Supporting References | Knowledge Consumers | Dependent Engines | Dependent Documents | Repository Classification | Current Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Planet Engine** | `PLANET_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | `ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` | Core Astrological Architecture | House, Yoga, Varga, Dosha | Formula catalogs | Canonical | Active |
| **House Engine** | `HOUSE_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | `ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` | Core Astrological Architecture | Yoga, Dosha, Varga | Formula catalogs | Canonical | Active |
| **Dasha Engine** | `DASHA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | `ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` | Master Probability | None | Formula catalogs | Canonical | Active |
| **Yoga Engine** | `YOGA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | `ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` | **Information Layer Only** (Reporting, Explanation, Question Engine context, Frontend UI) | **None** — Yoga does not contribute to any deterministic engine | `FORMULA_REPOSITORY_DATA_MODEL_v1.md` | Canonical | Active |
| **Dosha Engine** | `DOSHA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | `ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` | Master Probability | None | Formula catalogs | Canonical | Active |
| **Varga Engine** | `VARGA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | `ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` | Dasha Engine | None | Phase 9 Varga Governance | Canonical | Active |
| **Functional Nature Engine** | `FUNCTIONAL_NATURE_ENGINE_KNOWLEDGE_PACKAGE.md` | `ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` | Master Probability | None | None | Canonical | Active |
| **Master Probability Engine** | `MASTER_PROBABILITY_KNOWLEDGE_PACKAGE.md` | `ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` | Question Engine | None | Pipeline configuration | Canonical | Active |
| **Question Engine** | `QUESTION_ENGINE_KNOWLEDGE_PACKAGE.md` | `QUESTION_REGISTRY_MASTER_v1.md` | API Layer, Frontend | None | `QUESTION_REGISTRY_BACKEND_CONTRACT_v1.md` | Canonical | Active |
| **Quality Metrics Engine** | `QUALITY_METRICS_ENGINE_KNOWLEDGE_PACKAGE.md` | `DEPLOYMENT_VALIDATION_REPORT.md` | Validation Systems | None | Pipeline integration reports | Canonical | Active |
| **Mandali Generator** | `MANDALI_GENERATOR_KNOWLEDGE_PACKAGE.md` | `PHASE15_MANDALI_DECOUPLING_DECISION_RECORD.md` | Transit Engine | Transit Engine | Phase 15 reports | Canonical | Active |
| **Transit Engine** | `TRANSIT_ENGINE_KNOWLEDGE_PACKAGE.md` | None | None (Legacy context) | None | Phase 7/8 Transit logic | Legacy | Legacy Reference |
| **Pipeline Runner** | *Conflict (See Section 4)* | `DEPENDENCY_AUDIT_REPORT.md` | Question Engine | Master Probability, Question Engine | Phase 13 Pipeline Reports | Temporary | Conflicted |
| **Validation Framework** | `VALIDATION_FRAMEWORK_KNOWLEDGE_PACKAGE.md` | `DEPLOYMENT_VALIDATION_REPORT.md` | QA Systems | None | Phase 13G Validation Report | Canonical | Active |
| **Calibration Framework** | `CALIBRATION_FRAMEWORK_KNOWLEDGE_PACKAGE.md` | None | Master Probability | None | Phase 9 Profile Fixes | Canonical | Active |

---

## SECTION 4: Ownership Constraints & Conflicts

The analysis identifies the following strict conditions and existing conflicts within the Engine Knowledge domain:

### Ownership Conflicts
* **Pipeline Runner**: Shared ownership conflict between `QUESTION_ENGINE_KNOWLEDGE_PACKAGE.md` and `MASTER_PROBABILITY_KNOWLEDGE_PACKAGE.md`. Both packages attempt to define the execution sequence.
* **Question Engine Calculations**: Conflict between Question Engine's canonical definition and legacy hardcoded 60/40 probability split logic buried in its documentation.

### Shared Ownership
* Shared ownership of Engine rules is **STRICTLY PROHIBITED**. The conflicts listed above represent architectural violations that must be eliminated.

### Historical Ownership
* **Transit Engine**: The Transit Engine acts as a legacy reference. It owns historical spatial logic but exercises no active ownership over Version 2 architecture.
* **Phase 8-16 Readouts**: These documents contain historical engine definitions that are now superseded by the `*_KNOWLEDGE_PACKAGE.md` files.

### Missing Ownership
* **Pipeline Runner**: Lacks a dedicated canonical Knowledge Package.

### Future GM-005 Consolidation Candidates
* Extract Pipeline Runner logic into a dedicated Canonical Package.
* Archive legacy Phase 8-16 implementation readouts to eliminate duplicate/historical engine descriptions.
* Strip probability synthesis mathematics from the Question Engine package.

*(Note: No conflicts are resolved by this document.)*

---

## SECTION 5: Canonical Constitutional Rules

To preserve the deterministic architecture, the following constitutional rules must be enforced during future refinement:

* **One Engine**: Each functional domain represents a single module.
* **One Knowledge Owner**: Only the specific Engine Knowledge Package may define the rules for that domain.
* **One Canonical Definition**: No engine definitions may be scattered across Phase readouts or catalogs.
* **Question Engine owns no deterministic calculations**: It is an Orchestrator-Only component. It routes inputs and outputs; it does not synthesize or calculate probabilities.
* **Mandali Generator remains Canonical**: It is the definitive source for spatial grid arithmetic.
* **Transit Engine remains Legacy Reference**: It is preserved for deterministic historical tracing only.
* **Knowledge Preservation Before Consolidation**: Before deleting any historical engine documentation, its unique context must be verified against the canonical Knowledge Package.

---

## SECTION 6: Out of Scope

This document explicitly does **NOT**:

* Modify engine logic
* Modify architecture
* Merge documents
* Delete documents
* Rename documents
* Resolve conflicts

---

## SECTION 7: Summary

The Engine Knowledge Ownership Mapping identifies the singular, definitive owner for every deterministic engine within the Golden Master repository. By categorizing consumers, dependent documents, and exposing orchestration conflicts (like the Pipeline Runner), this document serves as the constitutional baseline.

Future repository refinement decisions must strictly uphold this one-to-one ownership model to guarantee architectural integrity.
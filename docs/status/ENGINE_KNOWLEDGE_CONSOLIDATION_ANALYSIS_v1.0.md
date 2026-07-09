# ENGINE KNOWLEDGE CONSOLIDATION ANALYSIS

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

## SECTION 2: Engine Knowledge Philosophy

The integrity of the Golden Master repository rests upon the absolute isolation of its deterministic engines. To prevent architectural drift, the following philosophy applies strictly to Engine Knowledge:

* **One Engine**: Each functional domain exists as a single, isolated module.
* **One Canonical Knowledge Source**: The domain rules, responsibilities, and logic of an engine are defined in exactly one Knowledge Package.
* **One Architectural Owner**: A single entity is responsible for the engine's implementation and output contracts.
* **Many Consumers**: Other systems may consume the engine's outputs, but they may never redefine the engine's purpose or logic.
* **Knowledge Preservation Before Consolidation**: Historical context surrounding an engine's creation must be safely preserved in its canonical source before legacy reports are archived.

---

## SECTION 3: Engine Knowledge Registry

| Engine | Canonical Knowledge Source | Supporting Documents | Consumers | Repository Classification | Current Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Planet Engine** | `docs/knowledge/PLANET_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | `ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` | House, Yoga, Varga, Dosha | Canonical | Active |
| **House Engine** | `docs/knowledge/HOUSE_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | `ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` | Yoga, Dosha, Varga | Canonical | Active |
| **Dasha Engine** | `docs/knowledge/DASHA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | `ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` | Master Probability | Canonical | Active |
| **Yoga Engine** | `docs/knowledge/YOGA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | `ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` | Master Probability | Canonical | Active |
| **Dosha Engine** | `docs/knowledge/DOSHA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | `ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` | Master Probability | Canonical | Active |
| **Varga Engine** | `docs/knowledge/VARGA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | `ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` | Dasha | Canonical | Active |
| **Functional Nature Engine** | `docs/knowledge/FUNCTIONAL_NATURE_ENGINE_KNOWLEDGE_PACKAGE.md` | `ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` | Master Probability | Canonical | Active |
| **Master Probability Engine** | `docs/knowledge/MASTER_PROBABILITY_KNOWLEDGE_PACKAGE.md` | `ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` | Question Engine | Canonical | Active |
| **Question Engine** | `docs/knowledge/QUESTION_ENGINE_KNOWLEDGE_PACKAGE.md` | `QUESTION_REGISTRY_MASTER_v1.md` | API Layer | Canonical | Active |
| **Quality Metrics Engine** | `docs/knowledge/QUALITY_METRICS_ENGINE_KNOWLEDGE_PACKAGE.md` | `docs/status/DEPLOYMENT_VALIDATION_REPORT.md` | Pipeline Runner | Canonical | Active |
| **Mandali Generator** | `docs/knowledge/MANDALI_GENERATOR_KNOWLEDGE_PACKAGE.md` | `PHASE15_MANDALI_DECOUPLING_DECISION_RECORD.md` | Transit Engine | Canonical | Active |
| **Transit Engine** | `docs/knowledge/TRANSIT_ENGINE_KNOWLEDGE_PACKAGE.md` | None | None | Legacy | Legacy Reference |
| **Validation Framework** | `docs/knowledge/VALIDATION_FRAMEWORK_KNOWLEDGE_PACKAGE.md` | `docs/status/DEPLOYMENT_VALIDATION_REPORT.md` | QA Systems | Canonical | Active |
| **Calibration Framework** | `docs/knowledge/CALIBRATION_FRAMEWORK_KNOWLEDGE_PACKAGE.md` | None | Master Probability | Canonical | Active |
| **Pipeline Runner** | None (Orchestration logic is fragmented) | `docs/status/DEPENDENCY_AUDIT_REPORT.md` | Question Engine | Temporary / Needs Consolidation | Conflicted |

---

## SECTION 4: Knowledge Dependency Mapping

* **Planet / House Engines**:
  * *Knowledge Owner*: Core Astrological Architecture
  * *Dependent Engines*: Yoga, Dosha, Varga, Functional Nature
  * *Dependent Documents*: Formula catalogs
  * *Knowledge Consumers*: Master Probability
* **Yoga / Dosha Engines**:
  * *Knowledge Owner*: Intelligence Framework
  * *Dependent Engines*: Master Probability
  * *Dependent Documents*: `docs/architecture/FORMULA_REPOSITORY_DATA_MODEL_v1.md`
  * *Knowledge Consumers*: Question Engine
* **Master Probability Engine**:
  * *Knowledge Owner*: Synthesis Architecture
  * *Dependent Engines*: Question Engine
  * *Dependent Documents*: `docs/knowledge/QUESTION_ENGINE_KNOWLEDGE_PACKAGE.md`
  * *Knowledge Consumers*: API Layer
* **Question Engine**:
  * *Knowledge Owner*: Orchestration Architecture
  * *Dependent Engines*: None (Terminal Node)
  * *Dependent Documents*: API Contracts, UI Blueprints
  * *Knowledge Consumers*: Frontend
* **Mandali Generator**:
  * *Knowledge Owner*: Spatial Transit Architecture
  * *Dependent Engines*: Transit Engine
  * *Dependent Documents*: Phase 15 ADR
  * *Knowledge Consumers*: Legacy Transit modules

---

## SECTION 5: Knowledge Duplication Analysis

Based on repository evidence, the following Engine Knowledge redundancies exist:

* **Duplicate engine descriptions**: Almost all Phase 8-16 implementation readouts contain historical descriptions of the engines that overlap with the canonical `*_KNOWLEDGE_PACKAGE.md` files. (*Classification: Historical Reference*)
* **Duplicate responsibilities**: Both `docs/knowledge/QUESTION_ENGINE_KNOWLEDGE_PACKAGE.md` and `docs/knowledge/MASTER_PROBABILITY_KNOWLEDGE_PACKAGE.md` describe Pipeline execution sequence. (*Classification: Requires Future Consolidation*)
* **Duplicate architectural explanations**: Found across `docs/governance/ASTROLOGICAL_PREDICTION_GOVERNANCE_v1.md` and `GOLDEN_MASTER_MANIFEST.md`. (*Classification: Requires Future Consolidation*)
* **Duplicate ownership**: The `docs/architecture/FORMULA_REPOSITORY_DATA_MODEL_v1.md` re-defines Yoga boundaries. (*Classification: True Duplicate*)
* **Cross-referenced knowledge**: `ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` correctly catalogs the I/O boundaries of all engines. (*Classification: Supporting Reference*)

---

## SECTION 6: Knowledge Ownership Conflicts

The following conflicts degrade the architectural integrity of the Engine Knowledge domain:

* **Engine**: Pipeline Runner
  * **Conflicting Documents**: `docs/knowledge/QUESTION_ENGINE_KNOWLEDGE_PACKAGE.md` vs `docs/knowledge/MASTER_PROBABILITY_KNOWLEDGE_PACKAGE.md`
  * **Evidence**: Both documents dictate how the sequence of engines should execute.
  * **Architectural Risk**: Circular dependencies and orchestration drift.
  * **Future Consolidation Recommendation**: Extract execution DAG logic into a new, canonical `docs/knowledge/PIPELINE_RUNNER_KNOWLEDGE_PACKAGE.md`.

* **Engine**: Question Engine
  * **Conflicting Documents**: `docs/knowledge/QUESTION_ENGINE_KNOWLEDGE_PACKAGE.md` vs System Architecture
  * **Evidence**: The Question Engine knowledge package still contains hardcoded references to probability weighting (the 60/40 split), violating its status as an Orchestrator-Only.
  * **Architectural Risk**: Logic bleed. The Question Engine is secretly operating as a math engine.
  * **Future Consolidation Recommendation**: Delete all synthesis math from the Question Engine documentation.

*(Note: No conflicts are resolved by this document.)*

---

## SECTION 7: Canonical Engine Knowledge Rules

To maintain an uncorrupted Golden Master, the following rules govern Engine Knowledge:

* **One Canonical Engine Description**: An engine is defined purely by its Knowledge Package.
* **One Engine Owner**: No two engines may produce the same output metric.
* **No Duplicate Responsibilities**: Orchestration and Calculation are strictly decoupled.
* **Question Engine remains Orchestrator Only**: It routes; it does not synthesize.
* **Mandali Generator remains Canonical**: It is the definitive source for spatial grid arithmetic.
* **Transit Engine remains Legacy Reference**: It provides historical context but is not active V2 architecture.
* **Knowledge Preservation Before Consolidation**: Any historical rationale stripped during deduplication must be preserved in an ADR or Canonical Package.

---

## SECTION 8: Repository Risk Assessment

Failure to consolidate Engine Knowledge presents significant systemic risks:

* **Architecture Drift**: Developers may build integrations based on the obsolete logic found in legacy Phase reports.
* **Duplicate Engine Documentation**: Fragments of true intent are scattered, making onboarding and audits practically impossible.
* **Ownership Ambiguity**: When multiple engines (like Question and Probability) claim orchestration rights, data contracts will inevitably clash.
* **Conflicting Responsibilities**: Engines that calculate *and* orchestrate violate Single Responsibility Principles, preventing modular testing.
* **Knowledge Fragmentation**: A failure to centralize domain logic makes the creation of future AI-assisted validation tools impossible.
* **Repository Inconsistency**: The root directory remains cluttered with contradictory implementation plans.

---

## SECTION 9: Out of Scope

This document explicitly does **NOT**:

* Modify engine logic
* Modify architecture
* Merge documents
* Delete documents
* Rename documents
* Resolve conflicts
* Implement repository refinement

---

## SECTION 10: Summary

The Engine Knowledge Consolidation Analysis establishes a clear, evidence-based map of the repository's deterministic engines. While the core engines are structurally sound and documented within their respective Knowledge Packages, critical orchestration conflicts and legacy duplication threaten architectural clarity. 

Future Engine Knowledge Consolidation must execute the recommendations outlined herein, strictly preserving canonical ownership and architectural integrity while purging contradictory historical fragmentation.

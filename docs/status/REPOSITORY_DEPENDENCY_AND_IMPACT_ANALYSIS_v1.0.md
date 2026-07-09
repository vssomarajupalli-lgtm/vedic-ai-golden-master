# REPOSITORY DEPENDENCY AND IMPACT ANALYSIS

## SECTION 1: Document Information

* **Date**: 2026-06-29
* **Repository**: D:\vedic-ai-golden-master
* **Project**: SVAI-GM
* **Program**: Program B
* **Milestone**: GM-005
* **Version**: v1.0
* **Status**: DRAFT
* **Author**: Coding Engine

---

## SECTION 2: Purpose

Repository refinement is an inherently risky process; deleting, merging, or relocating a single file can break architectural lineage or obscure critical domain knowledge. Therefore, comprehensive dependency analysis must precede any refinement execution.

No repository asset may be modified, archived, or deleted without explicitly understanding every dependency that relies upon it. This document maps the critical dependencies across the Golden Master repository, serving as the primary impact assessment reference for the Repository Refinement Decision Register.

---

## SECTION 3: Dependency Classification Model

To accurately assess the impact of repository modifications, dependencies are classified into the following strict categories:

* **Direct Dependency**: A hard link where one component cannot function or be understood without the other (e.g., Code importing a module, or a markdown file directly linking to another).
* **Indirect Dependency**: A relationship established through an intermediary component (e.g., Engine A relies on Orchestrator B, which relies on Engine C).
* **Knowledge Dependency**: A conceptual reliance where one document provides the theoretical or domain context required to interpret another.
* **Architectural Dependency**: A systemic requirement where the loss of an asset fundamentally alters the Golden Master design.
* **Governance Dependency**: A reliance on a rule-set or checklist that dictates compliance and approval procedures.
* **Formula Dependency**: Mathematical lineage where a derived calculation relies on a foundational formula.
* **Validation Dependency**: A testing requirement where regression suites depend on predefined canonical profiles or test cases.
* **Calibration Dependency**: Tuning mechanisms that rely on validation metrics and statistical output schemas.
* **Documentation Dependency**: The reliance of an index, catalog, or readme on the existence of its targeted files.
* **Historical Dependency**: Audit trails reliant on legacy phase reports to explain *why* a decision was made.
* **Reference Dependency**: Pointers and citations used across ADRs and compliance checklists.

---

## SECTION 4: Repository Dependency Analysis

The repository's ecosystem relies on highly interconnected assets:

* **Architecture & Governance documents**: Form the bedrock. Every Knowledge Package and engine implementation holds a strict *Governance Dependency* on the `docs/status/ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` and `docs/governance/GOVERNANCE_COMPLIANCE_CHECKLIST_v1.0.md`.
* **Knowledge Packages**: Serve as the central hub. They maintain *Knowledge Dependencies* on the root architecture documents, while Engine source code maintains a *Direct Dependency* on them.
* **Formula & Engine documentation**: Hold a *Formula Dependency* on the `docs/status/FORMULA_CATEGORY_CATALOG_v1.md`.
* **Validation & Calibration assets**: Hold a *Validation Dependency* on the outputs defined in the Engine Data Contracts.
* **API & Frontend documentation**: Hold an *Indirect Dependency* on the Question Engine and Master Probability Engine schemas.
* **Reports (Phase 8-16)**: Hold a *Historical Dependency* on the original Version 1 implementations.
* **Decision Registers & Completion Reports**: Hold a *Documentation Dependency* on the files they officially catalog and approve.

---

## SECTION 5: Engine Dependency Impact

The core deterministic engines maintain specific dependency profiles:

* **Planet Engine / House Engine**:
  * *Dependencies*: Ephemeris Data, Time/Location logic.
  * *Consumers*: Varga, Yoga, Dosha, Dasha, Functional Nature.
  * *Criticality*: Highest. Modifications break the entire mathematical downstream.
* **Yoga / Dosha Engines**:
  * *Dependencies*: Planet Strength, House Strength.
  * *Consumers*: Master Probability Engine.
  * *Criticality*: High. Modifications alter final probabilistic synthesis.
* **Question Engine**:
  * *Dependencies*: NLP Intents, Pipeline Runner outputs.
  * *Consumers*: API Layer, Frontend.
  * *Criticality*: High. Structural changes break user routing and response composition.
* **Pipeline Runner**:
  * *Dependencies*: All core engines (Orchestration).
  * *Consumers*: Question Engine.
  * *Criticality*: Absolute. Modifications risk cross-engine execution violations.

---

## SECTION 6: Repository Impact Assessment

Evaluating the consequences of refinement actions on major repository components:

* **Impact if modified**: Risk of architectural drift or breaking validation test suites (especially for JSON Contracts or Formulas).
* **Impact if renamed**: Broken markdown links across ADRs, Indexes, and Knowledge Packages (*Documentation Dependency* failure).
* **Impact if merged**: Potential dilution of strict "Single Responsibility" ownership principles. Loss of domain boundaries.
* **Impact if archived**: Removal from immediate developer visibility. If an active Canonical asset is archived by mistake, it breaks *Architectural Dependency*.
* **Impact if relocated**: Breaks hardcoded path references in scripts (e.g., `pytest`, `docker-compose`) and markdown references.
* **Impact if removed**: Permanent loss of deterministic logic or historical context. Severely prohibited for Knowledge and Governance assets.
* **Knowledge preservation requirements**: Before any asset is altered, its knowledge must be explicitly verified as existing in a superseding Canonical document.

---

## SECTION 7: High Risk Dependency Chains

The following dependency chains represent the most sensitive structures in the repository. They require extreme care during refinement:

* **Architecture → Governance → Engine**: Altering overarching architecture documents can silently invalidate Engine Governance, which in turn makes active Engine code non-compliant.
* **Knowledge Package → Formula → Engine**: The mathematical lineage. If a Knowledge Package is poorly merged, the theoretical basis for a coded Formula is lost, rendering the Engine a "black box".
* **Calibration → Probability → Question Engine**: Tweaking calibration documentation can obscure the weights used by the Probability engine, which breaks the consistency of the final Question Engine output.
* **Pipeline → Engine Outputs → Reports**: The Pipeline dictates execution order. Modifying this affects the state of outputs fed into validation reports.
* **Decision Register → Repository Refinement**: The absolute highest risk. If the Decision Register process is bypassed, the entire repository refinement becomes untraceable.

---

## SECTION 8: Single Points of Failure

The loss, accidental deletion, or unauthorized merging of the following assets would catastrophically impact the Golden Master integrity:

* **Core architecture documents**: e.g., `docs/governance/ASTROLOGICAL_PREDICTION_GOVERNANCE_v1.md`. Loss breaks overarching systemic rules.
* **Knowledge Packages**: e.g., `docs/knowledge/PLANET_INTELLIGENCE_KNOWLEDGE_PACKAGE.md`. Loss turns deterministic math into undocumented legacy code.
* **Canonical formula definitions**: Loss prevents any future auditing or correction of astrological mathematics.
* **Engine governance**: e.g., `docs/status/ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md`. Loss re-introduces ambiguous ownership and overlapping authority.
* **Decision Registers**: e.g., `docs/governance/REPOSITORY_REFINEMENT_DECISION_REGISTER_v1.0.md`. Loss destroys the audit trail of why the repository looks the way it does.

---

## SECTION 9: Refinement Risk Assessment

Repository refinement carries the following systemic risks:

* **Knowledge loss**: Accidentally deleting a "duplicate" file that actually contained unique caveats or historical context.
* **Broken references**: Widespread 404 errors in markdown files due to renamed or relocated targets.
* **Governance inconsistency**: Consolidating documents in a way that accidentally omits a constitutional restriction.
* **Documentation fragmentation**: Moving files into sub-directories without updating the central Indexes, making them virtually invisible.
* **Formula inconsistency**: Severing the link between the documented formula catalog and the actual implemented Python logic.
* **Validation inconsistency**: Archiving a test-case JSON file that a regression suite relies upon.
* **Historical information loss**: Erasing the Phase 8-16 reports without capturing their architectural justifications in an ADR.

---

## SECTION 10: Out of Scope

This document is strictly an analysis tool. It explicitly does **NOT**:

* Rename files
* Delete files
* Merge documents
* Move files
* Modify formulas
* Modify architecture
* Approve repository changes
* Implement repository refinement

---

## SECTION 11: Summary

The Golden Master repository is not merely a collection of files; it is a highly interdependent web of Governance, Knowledge, Formula, and Architectural dependencies. The loss or blind modification of a single Canonical asset can trigger cascading failures across validation suites, engine compliance, and historical traceability.

Future refinement decisions processed through the Repository Refinement Decision Register must be rigorously evaluated against this dependency analysis before any approval is granted.

# FORMULA OWNERSHIP MAPPING

## SECTION 1: Document Information

* **Date**: 2026-06-29
* **Repository**: D:\vedic-ai-golden-master
* **Project**: SVAI-GM
* **Program**: Program B
* **Milestone**: GM-005
* **Knowledge Domain**: Formula Knowledge
* **Version**: v1.0
* **Status**: DRAFT
* **Author**: Coding Engine

---

## SECTION 2: Formula Ownership Philosophy

The Golden Master repository strictly enforces the following formula ownership philosophy to prevent architectural drift and mathematical inconsistency:

* **One Formula**: Every deterministic calculation exists as a single logical entity.
* **One Owner**: A single canonical Engine holds absolute authority over that calculation.
* **One Canonical Definition**: The formula's mathematics are defined in exactly one Knowledge Package.
* **Many Consumers**: Other engines may request the formula's output, but never recreate the math.
* **Knowledge Preservation Before Consolidation**: Before any duplicate formula documentation is archived or merged, its historical context must be safely preserved in the canonical source.

---

## SECTION 3: Formula Ownership Registry

| Formula | Canonical Owner | Supporting Documents | Consumers | Knowledge Package | Repository Classification | Current Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Planet Strength** | Planet Engine | `FORMULA_CATEGORY_CATALOG_v1.md` | House, Yoga, Varga, Dosha | `PLANET_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | Canonical | Active |
| **House Strength** | House Engine | `FORMULA_CATEGORY_CATALOG_v1.md` | Yoga, Dosha, Varga | `HOUSE_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | Canonical | Active |
| **Yoga Detection** | Yoga Engine | `docs/architecture/FORMULA_MASTER_INDEX_PLAN.md` | **Information Layer Only** (Question Engine context, Frontend UI, Reporting) | `YOGA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | Canonical | Active |
| **Dosha Detection** | Dosha Engine | `FORMULA_CATEGORY_CATALOG_v1.md` | Master Probability | `DOSHA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | Canonical | Active |
| **Varga Refinement** | Varga Engine | None | Dasha | `VARGA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | Canonical | Active |
| **Dasha Activation** | Dasha Engine | `docs/architecture/FORMULA_MASTER_INDEX_PLAN.md` | Master Probability | `DASHA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | Canonical | Active |
| **Master Probability** | Master Probability Engine | None | Question Engine | `MASTER_PROBABILITY_KNOWLEDGE_PACKAGE.md` | Canonical | Active |
| **Question Routing Formula** | Question Engine | `QUESTION_COVERAGE_MATRIX_v1.md` | API Layer, Frontend | `QUESTION_ENGINE_KNOWLEDGE_PACKAGE.md` | Canonical | Active |
| **Calibration Formula** | Calibration Framework | None | Master Probability | `CALIBRATION_FRAMEWORK_KNOWLEDGE_PACKAGE.md` | Canonical | Active |
| **Quality Metrics** | Quality Metrics Engine | `DEPLOYMENT_VALIDATION_REPORT.md` | Pipeline Runner | `QUALITY_METRICS_ENGINE_KNOWLEDGE_PACKAGE.md` | Canonical | Active |
| **Mandali Rules** | Mandali Generator | `PHASE15_MANDALI_DECOUPLING_DECISION_RECORD.md` | Transit Engine | `MANDALI_GENERATOR_KNOWLEDGE_PACKAGE.md` | Canonical | Active |
| **Transit Reference Logic** | Transit Engine | None | None (Legacy reference) | `TRANSIT_ENGINE_KNOWLEDGE_PACKAGE.md` | Legacy | Legacy reference only |

---

--- Ownership Dependency Matrix ---

The flow of mathematical authority dictates strict boundary rules:

* **Planet Strength**: Owned by Planet Engine. Consumed by House/Yoga/Dosha/Varga. Referenced by Master Index. Must never be modified by Consumers.
* **House Strength**: Owned by House Engine. Consumed by Yoga/Dosha/Varga. Referenced by Master Index. Must never be modified by Yoga Engine.
* **Yoga Detection**: Owned by Yoga Engine. Consumed by **Information Layer Only** (Question Engine context, Frontend UI, Reporting). Referenced by Question Router. Must never be modified by Probability Framework.
* **Dosha Detection**: Owned by Dosha Engine. Consumed by Master Probability. Referenced by Question Router. Must never be modified by Probability Framework.
* **Master Probability**: Owned by Master Probability Engine. Consumed by Question Engine. Referenced by API Layer. Must never be modified by Question Engine.
* **Calibration Formula**: Owned by Calibration Framework. Consumed by Master Probability. Referenced by Pipeline Runner. Must never be modified by Astrology Engines (Planet, House, Yoga, etc.).
* **Mandali Rules**: Owned by Mandali Generator. Consumed by Transit Engine. Referenced by Phase 15 ADR. Must never be modified by legacy Transit logic.

---

## SECTION 5: Ownership Conflicts

The following conflicts, identified during the Formula Governance Consolidation Analysis, threaten formula ownership integrity. 

*(Note: These conflicts are recorded for evidence only and are not resolved by this document).*

* **Conflict**: Probability weight hardcoding in the Question Engine.
  * **Evidence**: `QUESTION_ENGINE_KNOWLEDGE_PACKAGE.md` contains a 60/40 synthesis split.
  * **Risk**: The Question Engine illegally claims ownership of a Master Probability formula.
  * **Future GM-007 action**: Excise the math from the Question Engine; enforce Master Probability as the sole owner.

* **Conflict**: Yoga Data Model duplication.
  * **Evidence**: `FORMULA_REPOSITORY_DATA_MODEL_v1.md` redefines Yoga detection parameters outside of the Yoga Engine.
  * **Risk**: Dual ownership of Yoga rules; risk of drift.
  * **Future GM-007 action**: Consolidate model into `YOGA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md`.

* **Conflict**: Question Routing definitions.
  * **Evidence**: Phase 11 readouts contain hardcoded routing logic conflicting with `QUESTION_REGISTRY_MASTER_v1.md`.
  * **Risk**: Conflicting definitions for Question Engine routing formulas.
  * **Future GM-007 action**: Archive Phase 11 reports; enforce `QUESTION_REGISTRY_MASTER_v1.md` as canonical.

---

## SECTION 6: Canonical Ownership Rules

To ensure astrological purity, the following architectural ownership rules apply:

* **One owner per formula**: No formula logic may ever exist in two engines.
* **Consumers do not own formulas**: An engine requesting data must use the output exactly as provided, without applying proprietary modifications.
* **Question Engine owns no deterministic formulas**: As an Orchestrator-Only, it strictly routes inputs and outputs.
* **Master Probability owns synthesis only**: It cannot redefine the base strength metrics provided by Planet or House engines.
* **Calibration never owns astrology formulas**: Statistical weighting must remain strictly decoupled from pure astrological math.

---

## SECTION 7: Out of Scope

This document explicitly does **NOT**:

* Modify formulas
* Rewrite formulas
* Merge documents
* Change ownership
* Delete documents
* Modify architecture

---

## SECTION 8: Summary

The Formula Ownership Mapping explicitly defines the single authoritative owner for every deterministic calculation in the system. By strictly enforcing "One Formula, One Owner", the Golden Master protects its astrological purity and creates a clear separation of concerns.

Future execution of the Formula Consolidation milestone (GM-007) shall strictly preserve the canonical ownership identified in this document.
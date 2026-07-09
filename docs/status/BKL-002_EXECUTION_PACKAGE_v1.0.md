# BKL-002 EXECUTION PACKAGE

## SECTION 1: Document Information

* **Date**: 2026-06-29
* **Repository**: D:\vedic-ai-golden-master
* **Project**: SVAI-GM
* **Program**: Program B
* **Milestone**: GM-005
* **Backlog Item**: BKL-002
* **Version**: v1.0
* **Status**: DRAFT
* **Author**: Coding Engine

---

## SECTION 2: Backlog Item Summary

* **Backlog ID**: BKL-002
* **Title**: Remove hardcoded probability synthesis math (the 60/40 split) from Question Engine documentation to restore Orchestrator-Only purity.
* **Knowledge Domain**: Engine Knowledge
* **Evidence Source**: Formula Ownership Mapping
* **Priority**: Critical
* **Architectural Risk**: High

---

## SECTION 3: Architectural Evidence

The necessity of BKL-002 is mandated by the following GM-005 analyses:

* **Formula Ownership Mapping**: Explicitly identifies the Question Engine's hardcoded 60/40 split as an illegal claim of ownership over Master Probability synthesis math.
* **Formula Governance Consolidation Analysis**: Highlights that deterministic formulas must be single-sourced. Probability math embedded in an orchestrator violates this rule.
* **Question Engine Knowledge Package**: Contains the documented violation: `(domain_score * 0.60) + (dasha_score * 0.40)` calculation inside the QuestionEngine, overtly overriding the MasterProbabilityEngine.
* **Master Probability Knowledge Package**: Establishes that the Master Probability Engine is the absolute canonical owner of all probability synthesis and weighting calculations.
* **Canonical Source Mapping**: Defines the constitutional rule of "One Formula, One Owner".
* **Conflict Resolution Plan**: Mandates the removal of overlapping responsibilities.

**Why the Question Engine violates the "Orchestrator Only" constitutional rule:**
The Question Engine is structurally defined as an "Orchestrator Only" component that routes queries and formats responses. By embedding a `60% Natal Promise / 40% Dasha` mathematical calculation within its own documentation, it ceases to be a pure orchestrator and illegally becomes a mathematical synthesis engine. This creates overlapping formula authority with the Master Probability Engine, ensuring conflicting calculations and architectural drift.

---

## SECTION 4: Scope

### In Scope
* Extraction of all mathematical probability synthesis logic (specifically the 60/40 split formula) from the `docs/knowledge/QUESTION_ENGINE_KNOWLEDGE_PACKAGE.md`.
* Replacing the removed formula with references indicating that probability math is owned strictly by the Master Probability Engine.

### Out of Scope
* Modifying actual `.py`, `.json`, or `.tsx` code files.
* Deleting or moving the Question Engine or Master Probability Engine knowledge packages.
* Updating the `docs/knowledge/MASTER_PROBABILITY_KNOWLEDGE_PACKAGE.md` with new weights (unless evaluating the canonical strategy dictates a cross-reference).
* Re-architecting the 60/40 math itself (the goal is boundary correction, not mathematical adjustment).
* Predetermining the exact architectural solution for the math's relocation before architectural review.

---

## SECTION 5: Impact Assessment

* **Repository Impact**: Direct modification of `docs/knowledge/QUESTION_ENGINE_KNOWLEDGE_PACKAGE.md` to remove the mathematical violation.
* **Knowledge Impact**: Centralizes all probability math strictly into the Master Probability domain. 
* **Architecture Impact**: Restores the structural purity of the Question Engine as an Orchestrator-Only node. Eliminates dual-ownership of synthesis logic.
* **Governance Impact**: Strongly enforces the "One Formula, One Owner" constitutional rule.
* **API Impact**: Zero. This is a documentation refinement enforcing backend boundaries.
* **Formula Ownership Impact**: Confirms the Master Probability Engine as the absolute sole owner of probability synthesis.

---

## SECTION 6: Validation Requirements

To validate completion, a static analysis must confirm that:
1. `docs/knowledge/QUESTION_ENGINE_KNOWLEDGE_PACKAGE.md` contains absolutely zero mathematical formulas, weighting ratios (e.g., 60/40), or calculations for generating probability scores.
2. The document clearly delegates probability synthesis to the Master Probability Engine.

---

## SECTION 7: Success Criteria

* **Orchestrator-Only Purity**: The Question Engine documentation describes an engine that performs zero astrological calculations and zero probability synthesis.
* **Formula Ownership Defended**: The Master Probability Engine retains sole architectural authority over the weighting of astrological inputs.
* **Single Responsibility Enforced**: The 60/40 math violation is successfully excised from the Question Engine's canonical scope without assuming the final implementation of how the Master Engine calculates it.

---

## SECTION 8: Approval Checklist

* [ ] Architecture Review
* [ ] Evidence Verified
* [ ] Formula Ownership Verified
* [ ] Knowledge Preserved
* [ ] Decision Register Updated
* [ ] Repository Validation Complete

---

## SECTION 9: Summary

This document constitutes the formal Execution Package for BKL-002. By excising the rogue 60/40 synthesis calculation from the Question Engine, the Golden Master restores strict adherence to the "Orchestrator Only" boundary constraint. 

Physical implementation of this refinement cannot begin until this Execution Package is explicitly approved.

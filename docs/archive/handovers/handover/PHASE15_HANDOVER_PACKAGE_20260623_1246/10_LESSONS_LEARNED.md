---
Generated Date & Time: 2026-06-23T12:46:10+05:30
Current Project Phase: Phase 15 (Promise Engine Validation)
Latest Git Commit Hash: d8a09355ae980b69be448fe4dfeaf0f23e7f3bea
Current Branch: main
Current Runtime Status: Validation Stable
---

# 10_LESSONS_LEARNED

## Old vs New Canonical Dataset Confusion
* **Lesson:** Keeping legacy and new canonical JSON files in the same directory without clear tags caused significant confusion. The runtime was loading old configurations (`canonical_content.json`) while tests were checking new files (`raju_canonical_content.json`).
* **Resolution:** Hardcoded the production dataset into `run.py` to ensure reality validation consistently queries the Raju case.

## Dasha Timeline Missing Issue
* **Lesson:** The Dasha synthesis block was completely dropping timeline items due to loose filtering logic.
* **Resolution:** Enforced rigid Dasha Timeline continuity contracts.

## Double Penalty Discussions
* **Lesson:** The original additive heuristic engine double-penalized planets. For example, Saturn in the 7th House penalized the `HouseStrength` score, but then `NatalPromiseEngine` independently deducted an *additional* 15 points using heuristic flags. This resulted in mathematically broken, artificially suppressed domain scores (e.g., Marriage returning 20/100 for a married native).
* **Resolution:** Implemented the strict No Double Penalty rule. All afflictions are computed *only once* inside the lower-level Planet and House engines.

## Formula Redesign Decisions
* **Lesson:** Magic numbers and unconstrained addition/subtraction lead to unpredictable scoring distributions.
* **Resolution:** Re-architected all systems into bounded `[0, 100]` components weighted by deterministic percentages. This ensures the output is always mathematically reasonable and easily explainable to the end-user.

## Architecture Governance Lessons
* **Lesson:** Moving fast and patching code without referring to an overarching architectural document (like `PROMISE_ENGINE_FORMULA_v1.md`) leads to technical debt.
* **Resolution:** All changes must follow Mandali Governance—first documenting the formula, gaining approval, then writing the code to match.

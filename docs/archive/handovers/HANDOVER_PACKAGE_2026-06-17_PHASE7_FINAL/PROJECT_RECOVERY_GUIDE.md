---
archive_title: "FINAL PROJECT RECOVERY GUIDE"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\handovers"
archive_reason: "Superseded by current documentation architecture"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# FINAL PROJECT RECOVERY GUIDE
**Document State:** Final (Phase 7 Lockdown)
**Date:** 2026-06-17

## Purpose
This document is designed to allow a new ChatGPT, Gemini, or other AI coding agent session to recover total project context quickly upon instantiation. If you are an AI reading this, you are working on a mathematically locked, deterministic Vedic Astrology Engine. Do not hallucinate math.

## Required Reading Order
Before proposing any code modifications or debugging, you MUST read the following documents in this exact order:

1. `docs/archive/SYSTEM_ARCHITECTURE.md` (Contains the foundational D1 rules and pipeline DAG)
2. `docs/archive/PROJECT_STATUS_MASTER.md` (Contains critical historical bugs, like the 48-score fallback)
3. `docs/archive/CHATGPT_IMPLEMENTATION_MEMORY.md` (Contains "Zero Magic Numbers" rules)
4. `docs/governance/CONTRACT_REGISTRY.md` (Contains strict JSON payload definitions)
5. `docs/governance/CODING_AGENT_PRECAUTIONS.md` (Contains rules for interacting with this repository)
6. `docs/status/PROJECT_HANDOVER_2026-06-17_1305.md` (Contains the Phase 7 release handoff details)

## Release Information
* **Release Tag:** `v0.7.1-phase7-final`
* **Test Status:** 613 Passed, 0 Failed, 0 Errors.
* **Current Completion State:** All calculation engines (Phase 1 through Phase 7) are 100% complete, integrated, and mathematically verified.

## Rollback Procedure
If tests fall below 613 passing, or if mathematical determinism is broken by a bad generation, execute an immediate rollback.
1. Run `git status` to identify modified files.
2. Run `git restore <file>` to revert modifications.
3. If necessary, revert to the nearest `v0.7.1-phase7-final` commit.
4. **Never rewrite engine math to force a test to pass.**

## Current Architecture
The system operates as a Unidirectional Directed Acyclic Graph (DAG) orchestrated by the `PipelineRunner`. Data flows sequentially:
`JSON Normalization` → `Functional Nature` → `Planet/House Strength` → `Rasi/Ashtakavarga` → `Varga` → `Dasha/Transit` → `Yoga/Natal Promise` → `Master Probability`.
Engines are isolated and never invoke each other directly.

## Known Contracts
The system enforces strict JSON payload schemas. Key contracts include:
* `canonical_content.json` input standard.
* Dasha `timeline[]` array contract.
* Varga nested `{"D9": {"planets": ...}}` wrapper.
Refer strictly to the `CONTRACT_REGISTRY.md`.

## Governance Locks
The project is strictly governed by architectural locks. You may not modify:
* **D1 Immutability:** Natal base positions cannot be overwritten.
* **Functional Nature:** Deterministic ascendant-based rules are sealed.
* **Mandali Boundaries:** Transits trigger on Mandali bounds, not Rasi signs.
* **Dosha Routing:** Dosha evaluates separately from standard dignity scaling.
* **Zero Magic Numbers:** All weighting variables live in `astrology_constants.py`.

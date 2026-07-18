---
archive_title: "PROJECT HANDOVER"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\handovers"
archive_reason: "Superseded by current documentation architecture"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# PROJECT HANDOVER
**Date:** 2026-06-17 13:05 IST

## A. Project Goal
Deliver a fully deterministic, mathematically stable Vedic Astrology processing pipeline that consumes raw JSON input (`canonical_content.json`) and produces heavily synthesized probability scores mapped to human domains. 

## B. Current Architecture
FastAPI backend processing static deterministic engine evaluations.
React/Vite frontend digesting the output payload.
No AI models process the mathematical calculations.

## C. Engine Dependency Chain
1. `JsonNormalizer`
2. `Functional Nature Engine`
3. `Planet/House/Rasi Strength Engines`
4. `Varga Engine`
5. `Ashtakavarga Engine`
6. `Dasha Engine`
7. `Transit Engine` (Mandali integration)
8. `Yoga Engine`
9. `Natal Promise Engine`
10. `Master Probability Engine`

## D. Governance Rules
- No code rewrites without exact audits.
- No modifications to probability mathematics.
- 100% test coverage stability required.

## E. Mandali Rules
- 1 Mandali = 9 Padas.
- Moon Pada = Center.
- 12 Mandalis = 108 Padas mapped absolutely.

## F. Dosha Rules
Strict preservation passthrough. Extract existing values; do not alter or dynamically recalculate doshas.

## G. Dasha Rules
Outputs explicitly formalized to a sequential `timeline[]` schema array of objects.

## H. Testing Status
- 613/613 Pytest validations PASS.
- Architecture is locked.

## I. Git Status Expectations
A clean repository tree, strictly tracked. Any future modifications require explicit impact analysis via diff output.

## J. Future Work
- Final system packaging and release.
- Infrastructure automation.

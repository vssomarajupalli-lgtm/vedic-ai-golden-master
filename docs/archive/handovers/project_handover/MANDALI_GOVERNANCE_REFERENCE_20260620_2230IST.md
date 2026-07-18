---
archive_title: "MANDALI GOVERNANCE REFERENCE"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\handovers"
archive_reason: "Superseded by current documentation architecture"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# MANDALI GOVERNANCE REFERENCE

**SNAPSHOT DATE:** 2026-06-20
**SNAPSHOT TIME:** 22:30 IST

## Original Concept
Mandali was originally conceived as a core timing probability trigger (Double-Transit Theory) operating within the Question Engine to greenlight boolean flags for events like Marriage or Childbirth based on Jupiter/Saturn transits.

## Moon-Centered Mandali
Future scopes explored "Moon-Centered Mandali" (Gochara from Natal Moon) for evaluating daily/monthly planetary weather.

## Reason for Decoupling
Calculating real-time ephemeris transit data inside a deterministic Promise/Dasha matrix broke Parashari principles (Transits do not override Dasha). It created massive computational overhead and generated test failures when mock payloads omitted transit nodes. 

## Current Governance
Mandali is mathematically banished from the Question Engine.
`Question Engine = Natal Promise + Dasha Activation`.

## Future Advisory Role
Mandali (Phase 15) is designated as Layer 4: An independent JSON advisory overlay. It will calculate current planetary transits independently and supply "weather commentary" to the LLM Answer Composer.

## Restrictions
Mandali shall not:
*   Modify Question Probability.
*   Prevent a Dasha activation.
*   Interact with `evaluator.py`.

## Future Phase 15 Boundaries
When Phase 15 begins, the developer must build the `MandaliEngine` as a standalone python module that outputs its JSON schema completely parallel to the `QuestionEngine` output.

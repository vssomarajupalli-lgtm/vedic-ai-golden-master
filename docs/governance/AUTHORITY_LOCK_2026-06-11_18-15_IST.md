# HEADER

Project: Samartha Astro AI 2.0 / VEDIC-AI

Status: APPROVED

Version: 1.0

Created: 2026-06-11 18:15 IST

Authority Level: Project Lock Document

Effective From: 2026-06-11 18:15 IST

Approved By: Domain Expert

---

# SECTION 1 — AUTHORITY HIERARCHY

Define the official authority order:

1. Domain Expert Clarifications
2. Authority Lock Documents
3. Approved Decision Register
4. Approved Master Roadmap
5. VEDIC_AI_SOURCE_OF_TRUTH.md
6. ARCHITECTURE_RULES.md
7. PROJECT_HANDOVER_MASTER
8. GOCHARA_MANDALI_GOVERNANCE_v1.md
9. Reference Documents
10. Historical Audit Files

Rule: If conflict exists, higher authority always prevails.

---

# SECTION 2 — LOCKED DECISIONS

## DR-001
MD / AD / PD calculations already exist within canonical source data.
Do NOT redesign.
Do NOT recreate Vimshottari calculations.
Dasha Engine is: Extraction + Activation + Interpretation Only.

## DR-002
The largest remaining astrology subsystem is: Samartha Gochara Engine.

## DR-003
Extraction First Rule.
Before implementing any calculation, verify whether the data already exists in:
* canonical_content.json
* machine_index.json
* source extraction output
Extraction is preferred over recalculation.

## DR-004
When ambiguity exists: STOP.
Create clarification request.
Ask Domain Expert.
Do not assume.

## DR-005
Architecture conflicts must never be resolved through AI assumptions.
Only Domain Expert clarification is authoritative.

## DR-007
Engine Isolation Rule.
No engine may directly instantiate or call another engine.
All communication must occur through:
* PipelineRunner
* Aggregated payloads
* Result dictionaries

---

# SECTION 3 — DOSHA CLARIFICATION LOCK

Previous assumption: "Dosha Engine Missing" is no longer accepted as a final conclusion.

Domain Expert clarification:
Kuja Dosha is already declared within source horoscope data.
Planet placements already exist.

Before implementing any dosha calculation, verify:
* What already exists in canonical data
* What already exists in source PDF
* What requires extraction only
* What requires interpretation only

Follow DR-003. Do not recreate Kuja Dosha mathematics unless explicitly instructed.

---

# SECTION 4 — GOCHARA AUTHORITY LOCK

`GOCHARA_MANDALI_GOVERNANCE_v1.md` is the authoritative transit specification.
For transit-related architecture:
`GOCHARA_MANDALI_GOVERNANCE_v1.md` prevails over older transit assumptions.

Locked Decision:
Samartha Gochara is a Moon Nakshatra Pada Based System.
It is NOT a simple Rasi Transit Engine.

---

# SECTION 5 — GOCHARA IMPLEMENTATION LOCK

Accepted implementation flow:
Birth Profile
→ Natal Moon
→ Moon Pada Anchor
→ Pada Belt Mapping
→ Zone Detection
→ Zone Scoring
→ Elinati Shani Builder
→ Dasha Overlap
→ Domain Trigger Layer
→ Final Gochara Output

Current Transit Engine:
May be extended.
Do not assume complete replacement is required.

---

# SECTION 6 — GOCHARA AUDIT FINDINGS LOCK

Accepted findings:

**Existing:**
* Classical Transit Layer
* BAV Validation
* Dasha Synchronization
* Domain Mapping

**Missing:**
* Moon Pada Anchor Layer
* Pada Belt Mapping
* Zone Detection Layer
* Zone Scoring Layer
* Elinati Shani Builder
* Proprietary Samartha Trigger Logic

---

# SECTION 7 — CANONICAL DATA INVENTORY LOCK

Accepted Inventory:

**Present:**
* Dasha Data
* Ashtakavarga Data
* Bhava Data

**Partial:**
* Planet Strength Data
* Varga Data

**Missing / Not Yet Extracted:**
* Structured Dosha Payload
* Structured Yoga Payload
* Structured Gochara Payload

Future implementation must follow extraction-first methodology.

---

# SECTION 8 — CURRENT IMPLEMENTATION PRIORITY

Approved priority order:

1. QuestionEngine DR-007 Fix
2. Functional Nature Engine
3. Extraction Layer Completion
   * Shadbala
   * Bhava Bala
   * Remaining Vargas
   * Dosha Extraction
4. Samartha Gochara Engine
5. Remaining Integration
6. Remedy Engine

---

# SECTION 9 — SUPERSEDED ASSUMPTIONS

Mark the following assumptions as superseded:
* Dasha mathematics must be recalculated.
* Dosha engine requires complete Kuja recomputation.
* Transit engine is only a classical Rasi transit calculator.
* Gochara is equivalent to standard Parashari transit logic.
* Engines may directly call other engines.

---

# SECTION 10 — FUTURE CHANGE RULE

If a newer authority lock document is created:
Newest timestamp wins.

Example:
`AUTHORITY_LOCK_2026-06-11_18-15_IST.md`
is superseded by
`AUTHORITY_LOCK_YYYY-MM-DD_HH-MM_IST.md`
when officially approved.

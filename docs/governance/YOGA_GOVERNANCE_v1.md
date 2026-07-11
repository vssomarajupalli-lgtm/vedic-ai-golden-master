# YOGA_GOVERNANCE_v1

## Status

**Approved Architecture — Final Chief Architect Decision**

## Purpose

This document defines the final governance rules for Yoga implementation within Vedic AI. It establishes Yoga as a detection and reporting layer, strictly isolating it from all deterministic scoring mechanics.

**This decision is FINAL. Do not reopen previous discussions.**

---

# FINAL CHIEF ARCHITECT DECISION

**Yoga SHALL NOT participate in deterministic strength calculations.**

Yoga SHALL NOT contribute to:

- Planet Strength
- Bhava Strength  
- House Strength
- Rasi Strength
- Dasha
- Gochara
- Ashtakavarga
- Natal Promise
- Master Probability
- Formula Evaluation
- Question Probability

or any deterministic scoring engine.

Yoga SHALL NOT require:

- weights
- percentages
- calibration
- parameter configuration
- future Parameter-Driven Evolution
- or engineering tuning.

---

## NEW ROLE OF YOGA

**Yoga becomes an INFORMATION LAYER ONLY.**

Yoga exists **to inform**, not **to calculate**.

---

## DISPLAY GOVERNANCE

Display ONLY the Yogas that actually exist inside the canonical JSON.

**Example**

Canonical JSON contains:
- Gaja Kesari Yoga
- Neecha Bhanga Raja Yoga

Display:
```
Detected Yogas:
- Gaja Kesari Yoga
- Neecha Bhanga Raja Yoga
```

Do NOT display:
- hundreds of absent Yogas
- False
- No
- Not Present
- Empty
- Cross marks
- Long checklists

If no Yoga exists, display:
```
No classical Yoga detected.
```

Nothing more.

---

## PARAMETER-DRIVEN EVOLUTION

The following deterministic subsystems remain part of the Parameter-Driven Evolution philosophy:

✓ Planet Strength
✓ Bhava Strength
✓ House Strength
✓ Rasi Strength
✓ Gochara
✓ Dasha
✓ Ashtakavarga
✓ Natal Promise
✓ Master Probability
✓ Formula Calibration
✓ Question Engine

**Yoga is intentionally excluded. Yoga is NOT part of Parameter-Driven Evolution.**

---

## CONFIGURATION OWNERSHIP PRINCIPLE

Deterministic Python engines own calculations.

Configuration files own parameters.

**Configuration SHALL NEVER contain business logic.**

Yoga owns neither deterministic calculations nor configurable parameters.

Yoga remains a descriptive information layer.

---

## ARCHITECTURE RULES

### 1. Yoga = Detection Layer

The Yoga Engine is fundamentally a detection and classification system. It analyzes planetary and house combinations to identify the presence of classical yogas. It does not calculate probabilities, strengths, or weights.

### 2. No Yoga Scoring

Yogas shall not output numeric scores. The result of a yoga evaluation is binary: **Present** or **Absent**.

### 3. No Yoga Bonuses

Yogas shall not apply mathematical bonuses to any engine.

### 4. No Yoga Penalties

Yogas shall not apply mathematical penalties to any engine.

### 5. Multi-Bhava Tagging Allowed

A single yoga can be mapped to multiple houses if the classical definition involves combinations across multiple bhavas.

### 6. Universal Yoga Category Allowed

Yogas that affect the entire chart (e.g., Gaja Kesari Yoga) can be tagged as "universal" rather than tied to a specific house.

### 7. Yoga Usage Scope

Yoga Engine outputs shall only be utilized by:

- Reporting and Explanation Layers
- Question Engine (for contextual information only)
- Frontend UI

Yoga outputs shall **NEVER** be consumed by the NatalPromiseEngine or used to alter the Four Pillar Promise calculation.

---

## PERMANENT ENGINEERING STATEMENT

> **Yoga is a descriptive astrological observation, not a deterministic scoring component.**
> 
> The system reports ONLY the Yogas present in the canonical source.
> 
> Yoga does not contribute to deterministic calculations, probabilities, strengths, calibration, weighting or Parameter-Driven Evolution.

---

## IMPLEMENTATION STATUS

- ✅ Yoga Engine implemented as detection-only (`backend/app/engines/yoga_engine.py`)
- ✅ Outputs binary Present/Absent status per yoga
- ✅ No numeric scores in yoga evaluation
- ✅ No yoga bonuses/penalties applied to other engines
- ✅ Yoga results available to QuestionEngine and UI only
- ✅ Question Registry `required_yogas` field used for contextual routing only

---

## REPOSITORY CONSISTENCY

All engineering documents have been synchronized to reflect this final governance decision:

- `docs/knowledge/VEDIC_AI_MASTER_DEVELOPMENT_ROADMAP.md` — Updated with Yoga Governance section
- `docs/status/PROJECT_STATUS_MASTER.md` — Updated with Yoga Governance section
- `Reports/GM-006/2026-07-11_MASTER_ENGINEERING_HANDOVER.md` — Updated with Engineering Decision #13
- This document (`docs/governance/YOGA_GOVERNANCE_v1.md`) — Final authority

---

## CONFLICT RESOLUTION

Any document, code comment, or design artifact that implies:

- Yoga scoring
- Yoga weighting  
- Yoga calibration
- Yoga parameterization
- Yoga contribution to deterministic engines

**is outdated and contradicts this governance.**

The final Chief Architect decision supersedes all previous discussions, proposals, and draft architectures.

**Do not reopen. Do not evaluate alternatives. Do not propose modifications.**

This decision is FINAL.
# ASTROLOGICAL RATIONALE: HEALTH FORMULAS

## 1. Core Methodology Overview
The current implementation of `HLT_VITALITY_BASE` evaluates the Lagna (physical body), Lagna Lord (ruler of self), Sun (natural karaka for vitality/Atma), the 6th House (diseases), and 6th Lord.

**Reviewer Assessment:** WEAK AND INCOMPLETE. The current implementation violates several core Parashari principles regarding medical astrology and longevity calculation.

## 2. Answers to Specific Review Questions

### Why is the Moon absent?
**Current State:** The Moon was excluded to simplify the payload.
**Astrological Critique:** This is a fatal flaw. In Jyotish, the Lagna represents the physical body, the Sun represents the soul/vitality, and the Moon represents the mind and physical fluids. The Moon is the primary indicator of Balarishta (infant mortality and early childhood health). Without the Moon, the evaluation of a person's psychosomatic health or early life vitality is impossible.

### Why is the 8th House/Lord absent?
**Current State:** The 8th house was excluded to focus purely on the 6th house (disease).
**Astrological Critique:** Incorrect methodology. The 6th house represents curable, acute diseases, daily health routines, and recovery. The 8th house represents chronic, incurable, hidden, and terminal diseases. It is also the house of Ayu (Longevity). Excluding the 8th house makes it impossible to predict chronic illnesses or life-threatening conditions.

### Why is the 12th House/Lord absent?
**Current State:** Excluded for payload minimization.
**Astrological Critique:** The 12th house represents hospitalization, confinement, and the loss of physical vitality (Vyaya). Without the 12th house, the system cannot answer questions like "Will I be hospitalized?" or "Will I require surgery?"

### Why is longevity merged into vitality?
**Current State:** Question 6.2 ("Will I have a long life?") maps to `HLT_GENERAL_VITALITY`.
**Astrological Critique:** This is fundamentally incorrect in classical astrology. Vitality (Lagna/Sun) and Longevity (8th house/Saturn) are distinct calculations (Ayurdaya). A person with a weak Lagna can have a very long life filled with sickness (strong 8th house). A person with a strong Lagna can die young in an accident (Alpayu).

## 3. Exclusion Analysis

| Excluded Signal | Why Considered | Why Rejected | Future Formula Ownership |
|-----------------|----------------|--------------|--------------------------|
| **Moon** | Karaka for mind/fluids. | Simplification of core payload. | Must be re-added to `HLT_VITALITY_BASE`. |
| **8th House/Lord** | Chronic illness / Longevity. | Assumed 6th house was sufficient for general health. | Must be split into a new Base Family: `HLT_LONGEVITY_BASE`. |
| **12th House/Lord** | Hospitalization. | Deemed too specific for general illness. | Belongs in a new `HLT_HOSPITALIZATION_RISK` variant. |
| **Saturn** | Ayushkaraka (Karaka for longevity). | Focus was on vitality (Sun). | Must be added to `HLT_LONGEVITY_BASE`. |

## 4. Methodology Breakdown

### Core House Logic (Proposed Revision)
- **1st House:** Physical body, general resilience.
- **6th House:** Acute illnesses, immune system, daily health.
- **8th House:** Chronic, incurable, or terminal illnesses. Longevity.
- **12th House:** Hospitalization, bed rest, surgical recovery.

### Core Karaka Logic (Proposed Revision)
- **Sun:** Natural vitality, bones, spine, heart.
- **Moon:** Mental health, psychosomatic illness, fluids.
- **Saturn:** Chronic pain, aging, longevity (Ayushkaraka).

### Core Dasha Logic
- Dashas of 6th, 8th, or 12th lords, or planets sitting in these houses, trigger illness.
- Dashas of Maraka lords (2nd and 7th) trigger death or severe health crises.

### Core Transit Logic
- Saturn transiting over the 6th/8th/12th or over natal Moon (Sade Sati) triggers chronic health events.
- Jupiter transiting the Lagna or aspecting the 6th promotes healing and recovery.

### Future Mandali Impact
- The Moon-centered Mandali is critical for health transits. Evaluating transits from the Moon (Gochara) provides the mental/emotional experience of the illness and the physical manifestation of fluid-based/circulatory diseases.

## 5. FINAL RECOMMENDATION
**DO NOT USE CURRENT MODEL.**
1. Split Longevity out into `HLT_LONGEVITY_BASE` containing 8th House, 8th Lord, and Saturn.
2. Add the Moon to `HLT_VITALITY_BASE`.
3. Add the 8th and 12th houses to `HLT_ILLNESS_RISK` to correctly identify chronic vs. acute conditions.

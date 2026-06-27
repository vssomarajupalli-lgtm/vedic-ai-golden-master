# GOCHARA_MANDALI_GOVERNANCE_v1.md

# 1. PURPOSE

This document is the single authoritative Gochara specification for the Samartha Astro-AI system.

It supersedes all previous Gochara drafts, experimental transit models, and legacy transit boundary definitions.

All future Gochara implementations must follow this document.

---

# 2. CORE GOCHARA PHILOSOPHY

The system shall not use classical fixed Rasi boundaries as the primary transit evaluation framework.

The system shall use:

Moon-Centered Rasi Mandalis

for all transit evaluation logic.

Only the location framework changes.

Transit interpretation rules remain unchanged.

---

# 3. MANDALI FOUNDATION

## Zodiac Structure

Total Nakshatra Padas = 108

Total Mandalis = 12

Mandali Size = 9 Padas

Therefore:

108 ÷ 12 = 9 Padas per Mandali

---

# 4. NATAL MOON REFERENCE

The native's Moon Nakshatra Pada becomes the central reference point.

Example:

Natal Moon = Dhanishta Pada 2

This Pada becomes the center of the Makara Mandali.

---

# 5. MANDALI CONSTRUCTION RULE

Each Mandali contains:

4 Padas before center

1 Center Pada

4 Padas after center

Total = 9 Padas

Example:

Makara Mandali

Shravana Pada 2

Shravana Pada 3

Shravana Pada 4

Dhanishta Pada 1

Dhanishta Pada 2 (Center)

Dhanishta Pada 3

Dhanishta Pada 4

Shatabhisha Pada 1

Shatabhisha Pada 2

The Mandali retains the classical Rasi name.

Only its boundaries differ.

---

# 6. RASI TO MANDALI REPLACEMENT

Throughout the transit engine:

Replace

Planet in Rasi

with

Planet in Mandali

Examples:

Makara Rasi → Makara Mandali

Kumbha Rasi → Kumbha Mandali

Mesha Rasi → Mesha Mandali

etc.

---

# 7. PLANET MAPPING RULE

All transit planets must be mapped to Mandalis.

Including:

Sun

Moon

Mars

Mercury

Jupiter

Venus

Saturn

Rahu

Ketu

No exceptions.

---

# 8. PROHIBITED LOGIC

The engine shall NOT perform runtime calculations such as:

+4 Pada

-4 Pada

+13 Pada

-13 Pada

Dynamic influence radius calculations

Forward influence belts

Backward influence belts

These concepts are already represented through Mandali construction.

---

# 9. RETROGRADE RULE

Retrograde behavior remains unchanged.

Direct motion remains unchanged.

Planetary longitude calculations remain unchanged.

Astronomical calculations remain unchanged.

Only location determination changes:

Classical Rasi

↓

Mandali

---

# 10. SATURN GOCHARA RULES

## Sade Sati

If Natal Moon belongs to Mandali M:

Sade Sati activates when Saturn occupies:

Previous Mandali

Current Mandali

Next Mandali

Activation begins immediately upon entry.

Activation ends immediately upon exit.

No gradual reduction logic is used.

---

## Elinati Shani

The engine must calculate:

Start Date

End Date

Duration

Current Status

The calculation must use Mandali-based transit positioning.

---

## Ashtama Shani

The traditional rule remains unchanged.

Only the location framework changes from Rasi to Mandali.

---

# 11. OTHER PLANETARY GOCHARAS

The following remain supported:

Guru Gochara

Kuja Gochara

Budha Gochara

Shukra Gochara

Surya Gochara

Rahu Gochara

Ketu Gochara

Only the location framework changes.

Interpretation logic remains unchanged.

---

# 12. DASHA INTEGRATION

The Gochara engine must support:

Mahadasha

Antardasha

Pratyantardasha

The engine must display:

Active MD

Active AD

Active PD

Dasha-linked transit overlaps

Current transit influence during MD/AD/PD

Future transit influence during MD/AD/PD

Past transit validation windows

---

# 13. PLANET STRENGTH MODEL

The engine must support:

Shadbala derived strength

Exaltation

Own Sign

Moolatrikona

Uchchabala

Swarashi Bala

Optional:

Friend Sign

Neutral Sign

Enemy Sign

Output shall be percentage based.

Range:

0–100

---

# 14. BHAVA STRENGTH MODEL

The engine must support:

Bhava Bala

House Strength

Lord Strength

Directional Strength

Aspect Strength

Output shall be percentage based.

Range:

0–100

---

# 15. QUESTION SCORING MODEL

Current approved formula:

Final Question Score

= (0.40 × Lord Strength)

* (0.30 × Karaka Strength)

* (0.15 × D9 Strength)

* (0.10 × Supporting Varga Strength)

* (0.05 × Fixed Support Score)

* Bonus

Maximum score = 100

If Vargottama:

Add +5 bonus

Cap final score at 100.

---

# 16. REQUIRED GOCHARA OUTPUTS

The engine must generate:

Current Transit Snapshot

Planetary Transit Positions

Sade Sati Status

Elinati Shani Status

Ashtama Shani Status

Dasha Overlap Results

Transit Timeline Windows

Question-Specific Transit Results

Future Transit Events

Past Transit Validation Events

---

# 17. JSON OUTPUT CONTRACT

The engine must return JSON-ready objects.

Required sections:

Birth Profile

Natal Summary

Transit Snapshot

Planet Strengths

Bhava Strengths

Dasha Status

Gochara Status

Timeline Windows

Question Results

Metadata

PWA Rendering Data

---

# 18. REPORT OUTPUT CONTRACT

Supported outputs:

PWA

Web

Split PDF

Master PDF

---

# 19. BIRTH PAGE RULE

Every report must begin with:

Native Name

Date of Birth

Time of Birth

Place of Birth

Latitude

Longitude

Runtime Timestamp

---

# 20. DATE FORMAT RULE

All visible dates:

DD.MM.YYYY

Examples:

14.06.2026

21.04.1972

Machine dates must not appear in user-facing reports.

---

# 21. BRANDING RULE

All reports shall reserve a branding area for:

Samartha Astro-AI

Samartha Vastu

Branding must remain lightweight and suitable for local rendering.

---

# 22. SUPPRESSED MODULES

The following shall never appear in active output:

Avakahada Chakra

Ghata Chakra

Panchadha Maitri Chakra

Jaimini Karakas

Jaimini Arudhas

---

# 23. VALIDATION TESTS

The engine must verify:

Moon Pada based Mandali generation

Mandali transit mapping

Sade Sati activation

Elinati Shani periods

MD/AD/PD overlap logic

Planet strength calculations

Bhava strength calculations

Vargottama bonus

JSON compatibility

PWA compatibility

Split PDF compatibility

Master PDF compatibility

---

# 24. IMPLEMENTATION ROADMAP

Phase 1
Birth Profile Ingestion

Phase 2
Natal Moon Extraction

Phase 3
Mandali Generator

Phase 4
Transit Planet Resolver

Phase 5
Saturn Transit Engine

Phase 6
Sade Sati Engine

Phase 7
Elinati Shani Engine

Phase 8
Dasha Overlap Engine

Phase 9
Question Engine Integration

Phase 10
JSON Builder

Phase 11
PWA Integration

Phase 12
PDF Output Engine

---

# 25. GOVERNANCE FREEZE

This document is the authoritative transit specification.

The following are frozen:

1. Moon-Centered Mandali Architecture

2. 12 Mandalis

3. 9 Padas per Mandali

4. Natal Moon Center Reference

5. Rasi → Mandali Replacement

6. No Runtime ±4 / ±13 Pada Logic

7. Immediate Transit Activation On Mandali Entry

8. Existing Transit Interpretation Rules Preserved

Any future enhancements must extend this framework and shall not bypass it.

# VEDIC_AI_MASTER_DEVELOPMENT_ROADMAP.md

# 1. PROJECT VISION

## 1.1 Objective

Build a deterministic Vedic Astrology Intelligence System.

The system must not depend on generative prediction logic.

The system must operate through:

* Structured horoscope data
* Deterministic calculations
* Domain-specific evaluation
* Dasha activation
* Transit triggering
* Probability scoring
* Grade generation

---

## 1.2 Source Of Truth

### 1.2.1 Primary Sources

machine_index.json

canonical_content.json

### 1.2.2 Supporting Sources

canonical_sections.json

canonical_page_map.json

### 1.2.3 Human Verification Sources

cleaned.pdf

canonical.pdf

---

## 1.3 Output Philosophy

Every engine outputs:

Score (%)

Grade

Supporting Factors

No free-form prediction generation.

No AI storytelling.

---

# 2. DATA INGESTION LAYER

## 2.1 Horoscope Source Loader

### 2.1.1 Load Navigation Data

machine_index.json

### 2.1.2 Load Knowledge Data

canonical_content.json

### 2.1.3 Validation Layer

File integrity

Schema validation

Missing field validation

---

## 2.2 Astrology Data Extraction

### 2.2.1 Birth Data

### 2.2.2 Planetary Positions

### 2.2.3 Bhava Positions

### 2.2.4 Planetary States

Retrogression

Combustion

Avasthas

Friendships

Panchadha Maitri

### 2.2.5 Shadbala

### 2.2.6 Ishta Phala

### 2.2.7 Kashta Phala

### 2.2.8 Bhava Bala

### 2.2.9 Ashtakavarga

BAV

SAV

### 2.2.10 Shodasavarga

D1

D2

D3

D4

D7

D9

D10

D12

D16

D20

D24

D27

D30

D40

D45

D60

### 2.2.11 Dasha Tables

MD

AD

PD

Sookshma

### 2.2.12 Dosha Data

Kuja Dosha

Kala Sarpa

Future Doshas

### 2.2.13 Yoga Data

Existing

Future

---

# 3. ASCENDANT CONFIGURATION LAYER

## 3.1 Lagna Initialization

### 3.1.1 Ascendant Detection

### 3.1.2 House Ownership Matrix

---

## 3.2 Functional Nature Engine

### 3.2.1 Functional Benefic

### 3.2.2 Functional Malefic

### 3.2.3 Neutral

### 3.2.4 Mixed

### 3.2.5 Yogakaraka

---

## 3.3 Planet Intent Matrix

Purpose:

Separate:

Planet Strength

from

Planet Nature

---

# 4. PLANET STRENGTH ENGINE

## 4.1 Core Strength Layer

### 4.1.1 Shadbala

### 4.1.2 Ishta Phala

### 4.1.3 Kashta Phala

---

## 4.2 Positional Dignity

### 4.2.1 Exaltation

### 4.2.2 Debilitation

### 4.2.3 Own Sign

### 4.2.4 Moolatrikona

### 4.2.5 Friendly Sign

### 4.2.6 Enemy Sign

---

## 4.3 State Modifiers

### 4.3.1 Retrogression

### 4.3.2 Combustion

### 4.3.3 Avastha

### 4.3.4 Planetary War

Future

---

## 4.4 Relationship Modifiers

### 4.4.1 Natural Friendship

### 4.4.2 Temporary Friendship

### 4.4.3 Panchadha Maitri

---

## 4.5 Final Planet Strength

Output:

Planet Score %

Planet Grade

---

# 5. RASI STRENGTH ENGINE

## 5.1 Sign Environment

### 5.1.1 Sign Lord Strength

### 5.1.2 Occupants

### 5.1.3 Benefic Occupants

### 5.1.4 Malefic Occupants

---

## 5.2 Ashtakavarga Support

### 5.2.1 SAV

### 5.2.2 BAV

---

## 5.3 Aspect Support

### 5.3.1 Benefic

### 5.3.2 Malefic

---

## 5.4 Final Rasi Strength

Output:

Rasi Score %

Rasi Grade

---

# 6. HOUSE STRENGTH ENGINE

## 6.1 House Lord Evaluation

## 6.2 House Occupants

## 6.3 Benefic Influence

## 6.4 Malefic Influence

## 6.5 Bhava Bala

## 6.6 Bhavat Bhavam

## 6.7 Ashtakavarga Influence

---

## 6.8 Final House Strength

Output:

House Score %

House Grade

---

# 7. DOSHA ENGINE

## 7.1 Kuja Dosha

### 7.1.1 Lagna Reference

### 7.1.2 Moon Reference

### 7.1.3 Venus Reference

---

## 7.2 Kala Sarpa

---

## 7.3 Future Doshas

Pitru

Naga

Others

---

## 7.4 Dosha Impact Scoring

Output:

Dosha Severity %

Dosha Grade

---

# 8. YOGA ENGINE

## 8.1 Raja Yoga

## 8.2 Dhana Yoga

## 8.3 Gaja Kesari

## 8.4 Neechabhanga Raja Yoga

## 8.5 Vipareeta Raja Yoga

## 8.6 Future Yogas

---

## 8.7 Yoga Strength

Output:

Yoga Score %

Yoga Grade

---

# 9. SHODASAVARGA ENGINE

## 9.1 D2 Hora

Finance

## 9.2 D4 Chaturthamsa

Property

## 9.3 D7 Saptamsa

Children

## 9.4 D9 Navamsa

Marriage

## 9.5 D10 Dasamsa

Career

## 9.6 D20 Vimsamsa

Spiritual

## 9.7 D24 Education

## 9.8 D30 Trimsamsa

Difficulties

---

## 9.9 Vargottama Detection

## 9.10 Neechabhanga Validation

---

## 9.11 Final Varga Score

Output:

Varga Score %

Varga Grade

---

# 10. NATAL PROMISE ENGINE

## 10.1 Domain Mapping Framework

Marriage

Career

Finance

Property

Children

Health

Foreign Travel

Litigation

Business

Education

Spiritual

Longevity

Mental State

---

## 10.2 Domain Evaluation Rules

Planet Rules

House Rules

Varga Rules

Dosha Rules

Yoga Rules

---

## 10.3 Natal Promise Gate

Output:

Absent

Weak

Moderate

Strong

Excellent

---

# 11. DASHA EXTRACTION & ACTIVATION ENGINE

## 11.1 Canonical Extraction Layer
* Extract pre-calculated MD/AD/PD values from `canonical_content.json` (Treat as authoritative, do NOT recalculate).

## 11.2 Mahadasha Layer
## 11.3 Antardasha Layer
## 11.4 Pratyantardasha Layer
## 11.5 Sookshma Layer

---

## 11.5 MD-AD Relationships

1-1

5-9

7-7

6-8

2-12

Others

---

## 11.6 Activation Scoring

Output:

Activation %

Activation Grade

---

# 12. TRANSIT ENGINE

## 12.1 Saturn Transit

## 12.2 Jupiter Transit

## 12.3 Rahu Transit

## 12.4 Ketu Transit

## 12.5 Other Planets

Future

---

## 12.6 Lagna View

## 12.7 Chandra Lagna View

---

## 12.8 Transit Support Score

Output:

Transit %

Transit Grade

---

# 13. DOMAIN EVALUATION ENGINE

## 13.1 Marriage

## 13.2 Career

## 13.3 Finance

## 13.4 Property

## 13.5 Children

## 13.6 Health

## 13.7 Foreign Travel

## 13.8 Litigation

## 13.9 Business

## 13.10 Education

## 13.11 Spiritual

## 13.12 Longevity

## 13.13 Mental State

---

# 14. EVENT PROBABILITY ENGINE

## 14.1 Natal Promise Contribution

## 14.2 Planet Contribution

## 14.3 Rasi Contribution

## 14.4 House Contribution

## 14.5 Dosha Contribution

## 14.6 Yoga Contribution

## 14.7 Varga Contribution

## 14.8 Dasha Contribution

## 14.9 Transit Contribution

---

## 14.10 Final Probability

Output:

Probability %

Grade

---

# 15. QUESTION ENGINE

## 15.1 User Query Detection

Marriage

Career

Property

Children

Finance

Health

etc.

---

## 15.2 Domain Routing

Activate only required engines.

---

## 15.3 Result Compilation

Collect all scores.

---

# 16. MASTER SYNTHESIS ENGINE

## 16.1 Collect Outputs

Planet

Rasi

House

Dosha

Yoga

Varga

Natal Promise

Dasha

Transit

---

## 16.2 Final Evaluation

Weighted scoring

Priority validation

Conflict resolution

---

## 16.3 Final Output

Overall %

Overall Grade

Supporting Factors

Positive Factors

Negative Factors

Risk Factors

Opportunity Factors

---

# 17. REMEDY ENGINE (PHASE 3)

## 17.1 Weak Planet Remedies

## 17.2 Dosha Remedies

## 17.3 Domain Remedies

Marriage

Career

Health

Finance

---

# 18. FUTURE EXPANSION LAYER

## 18.1 Additional Doshas

## 18.2 Additional Yogas

## 18.3 Additional Vargas

## 18.4 Advanced Timing

## 18.5 Advanced Research Modules

---

# FINAL DEVELOPMENT ORDER

Phase 1

Data Layer
Ascendant Layer
Planet Strength

Phase 2

Rasi
House
Dosha
Yoga

Phase 3

Varga
Natal Promise

Phase 4

Dasha (Extraction Only - No Recalculation)

Phase 5

Transit (Gochara Engine - Largest Remaining Module)
Domain Evaluation
Probability
Question Engine
Master Synthesis

Phase 6

Remedies
Future Research

END OF MASTER ROADMAP

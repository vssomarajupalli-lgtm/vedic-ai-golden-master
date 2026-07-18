---
archive_title: "PROJECT REQUIREMENTS"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive"
archive_reason: "Superseded by current documentation architecture"
original_version: "Unknown (historical)"
replacement_document: "docs/knowledge/PROJECT_REQUIREMENTS.md"
---

# PROJECT REQUIREMENTS
# Deterministic Vedic Astrology Calculation Platform

---

# 1. PROJECT PURPOSE

The purpose of this software is to develop a deterministic Vedic astrology calculation platform capable of:

- extracting astrology data from horoscope PDFs
- generating normalized structured JSON
- calculating Graha (planetary) strengths
- calculating Bhava/Rasi (house) strengths
- generating deterministic explainable outputs

The software must preserve classical astrology principles while providing structured computational analysis.

The software should NOT generate random astrology predictions.

The software should:
- remain deterministic
- remain modular
- remain explainable
- separate calculations from interpretation
- preserve D1 foundational logic

---

# 2. CURRENT IMPLEMENTATION PRIORITY

The CURRENT implementation phase focuses ONLY on:

1. PDF extraction
2. JSON normalization
3. Graha strength calculations
4. House strength calculations
5. deterministic outputs
6. deterministic testing

The current project is NOT yet focused on:
- autonomous prediction systems
- continuous transit monitoring
- AI-generated astrology
- large probabilistic synthesis systems

---

# 3. SOFTWARE IDENTITY

Current project identity:

DETERMINISTIC ASTROLOGY CALCULATION PLATFORM

The software currently focuses on:
- extraction
- normalization
- deterministic scoring
- explainable outputs

Future expansion phases may later include:
- Dasha systems
- Transit systems
- Event-domain abstractions
- Probability synthesis
- AI-assisted interpretation

These remain FUTURE roadmap phases and are NOT current implementation priorities.

---

# 4. CORE DEVELOPMENT PRINCIPLES

Rule 1:
Keep calculations deterministic.

Rule 2:
Keep modules independent.

Rule 3:
Avoid overengineering.

Rule 4:
One engine at a time.

Rule 5:
Separate calculations from interpretation.

Rule 6:
Keep D1 foundational and immutable.

Rule 7:
AI must NEVER generate astrology math.

---

# 5. MAIN SOFTWARE WORKFLOW

CURRENT IMPLEMENTATION FLOW:

PDF/Input JSON
↓
Extraction
↓
Normalized JSON
↓
Planet Strength Engine
↓
House Strength Engine
↓
Varga Refinement
↓
Deterministic Output Reports

---

# 6. MAIN SOFTWARE MODULES

## 6.1 PDF Extraction Engine

Purpose:
- extract text
- extract tables
- identify headings
- generate structured JSON

Responsibilities:
- PDF reading
- section identification
- table extraction
- structured data preparation

---

## 6.2 JSON Normalization Engine

Purpose:
- normalize extracted data
- enforce schema consistency
- provide safe defaults
- prepare deterministic engine inputs

Responsibilities:
- schema validation
- missing field handling
- type normalization
- standardized payload generation

---

## 6.3 Planet Strength Engine

Purpose:
calculate deterministic Graha strength percentages.

Inputs may include:
- Graha Bala
- Shadbala
- dignity
- conjunctions
- aspects
- positional strength

Output:
0–100 deterministic planetary strength score.

---

## 6.4 House Strength Engine

Purpose:
calculate deterministic House/Bhava strength percentages.

Inputs may include:
- Bhava Bala
- house lord strength
- karaka support
- aspects
- occupants

Output:
0–100 deterministic house strength score.

---

## 6.5 Varga Refinement Engine

Purpose:
provide structural refinement support without overriding D1.

Important:
Vargas refine interpretation.
They must NOT overwrite D1 foundation.

Current implementation focus:
- D9
- D10

Additional Vargas remain future expansion phases.

---

# 7. FUTURE ROADMAP MODULES

The following systems are FUTURE implementation phases and are NOT current development priorities:

- Dasha Engine
- Transit Engine
- Event-domain systems
- Probability synthesis systems
- AI interpretation layer
- conversational astrology assistant

---

# 8. D1 FOUNDATION PRINCIPLE

The D1 chart represents foundational karma.

All future systems must treat D1 as:
- foundational
- deterministic
- immutable
- explainable

Future layers may refine interpretation but must NOT overwrite D1.

---

# 9. DETERMINISTIC CALCULATION PRINCIPLE

All astrology calculations must remain:

- deterministic
- explainable
- reproducible
- auditable

Every score modification should be traceable.

The system should avoid:
- hidden calculations
- random outputs
- AI-generated scoring
- unexplained modifiers

---

# 10. AI USAGE POLICY

AI may later assist with:
- explanation
- formatting
- report enhancement
- readable summaries

AI must NEVER:
- generate astrology math
- override deterministic scores
- invent probabilities
- mutate engine calculations

AI remains optional and secondary to deterministic calculations.

---

# 11. OUTPUT GOALS

Current output goals:

- normalized JSON outputs
- Graha strength reports
- House strength reports
- deterministic explainable outputs

Outputs should remain:
- readable
- explainable
- structured
- deterministic

---

# 12. TESTING PHILOSOPHY

Testing should remain:

- deterministic
- isolated
- reproducible
- schema-validated

Tests should focus on:
- extraction stability
- normalization correctness
- score consistency
- D1 immutability
- deterministic outputs

---

# 13. CURRENT PRACTICAL GOAL

Current practical goal:

Create a stable deterministic astrology calculation platform capable of:

- extracting astrology PDFs
- generating normalized JSON
- calculating explainable Graha strengths
- calculating explainable House strengths
- producing deterministic reports

Current implementation priority remains:

DETERMINISTIC CALCULATION CORRECTNESS
AND
EXTRACTION STABILITY

---

# 14. FUTURE EXPANSION POLICY

Future systems should be added only after:

- extraction stabilization
- contract stabilization
- deterministic testing stabilization
- core engine correctness

Avoid premature expansion into:
- massive synthesis systems
- excessive architecture abstraction
- unnecessary framework complexity

The software should evolve gradually and remain maintainable.

---

# 15. TECHNOLOGY DIRECTION

Current technology direction:

- Python
- Local desktop execution
- JSON-based workflow
- deterministic modular engines

Current project does NOT require:
- cloud infrastructure
- databases
- distributed systems
- always-running services

The software should remain lightweight, modular, and locally executable.
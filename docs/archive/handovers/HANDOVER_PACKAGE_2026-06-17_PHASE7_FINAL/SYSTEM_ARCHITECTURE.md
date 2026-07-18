---
archive_title: "SYSTEM ARCHITECTURE"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\handovers"
archive_reason: "Superseded by current documentation architecture"
original_version: "Unknown (historical)"
replacement_document: "docs/SYSTEM_ARCHITECTURE.md"
---

# SYSTEM ARCHITECTURE
# Deterministic Vedic Astrology Calculation Platform

---

# 1. SYSTEM OVERVIEW

The software is a local desktop-based deterministic Vedic astrology calculation platform.

The software is designed to:

- extract horoscope PDF data
- normalize extracted data into structured JSON
- calculate Graha (planetary) strengths
- calculate Bhava/Rasi (house) strengths
- generate deterministic explainable outputs

The software prioritizes:
- deterministic calculations
- modular architecture
- explainable outputs
- lightweight execution
- maintainable structure

---

# 2. CURRENT SOFTWARE WORKFLOW

CURRENT IMPLEMENTATION FLOW:

PDF/Input JSON
↓
JSON Normalization Engine (Dosha Passthrough)
↓
Functional Nature Engine (Governance Locked)
↓
Planet & House Strength Engines
↓
Rasi & Ashtakavarga Engines
↓
Varga Refinement Engine
↓
Dasha Timeline & Transit (Mandali Gochara) Engines
↓
Yoga Engine & Natal Promise Engine
↓
Master Probability Synthesis Engine
↓
Deterministic Output Reports

---

# 3. FUTURE ROADMAP WORKFLOW

The following systems are future roadmap phases:

- AI interpretation systems
- Natural language interface layers

Future roadmap systems should begin only after:
- extraction stabilization
- normalization stabilization
- deterministic testing stabilization
- core engine correctness validation

---

# 4. MAIN PROJECT STRUCTURE

vedic-ai-system/
│
├── backend/
├── docs/
├── extracted_json/
├── outputs/
├── sample_reports/
├── source_pdfs/
└── temp/

---

# 5. BACKEND STRUCTURE

backend/
│
├── app/
├── requirements.txt
└── run.py

---

# 6. APP STRUCTURE

app/
│
├── engines/
├── parsers/
├── utils/
├── tests/
└── config/

---

# 7. PARSERS MODULE

Purpose:
extract and structure astrology PDF data.

Current parser responsibilities:

- PDF text extraction
- table extraction
- heading identification
- section identification
- structured JSON generation

Current parser files may include:

- pdf_extractor.py
- table_parser.py
- heading_parser.py
- json_builder.py

---

# 8. JSON NORMALIZATION LAYER

Purpose:
normalize extracted astrology data into deterministic structured contracts.

Responsibilities:

- schema validation
- safe defaults
- type normalization
- payload consistency
- engine-ready structured inputs

Important:
All engines should consume normalized JSON only.

Engines must NOT depend directly on:
- PDFs
- OCR systems
- raw extraction logic

---

# 9. PLANET STRENGTH ENGINE

Purpose:
calculate deterministic Graha strength percentages.

Possible inputs include:

- Graha Bala
- Shadbala
- dignity
- conjunctions
- aspects
- positional strength

Output:
0–100 deterministic planetary strength score.

Important:
All calculations must remain:
- deterministic
- explainable
- reproducible

---

# 10. HOUSE STRENGTH ENGINE

Purpose:
calculate deterministic House/Bhava strength percentages.

Possible inputs include:

- Bhava Bala
- house lord strength
- karaka support
- aspects
- occupants

Output:
0–100 deterministic house strength score.

Important:
All calculations must remain:
- deterministic
- explainable
- reproducible

---

# 11. VARGA REFINEMENT ENGINE

Purpose:
provide structural refinement support for D1 interpretation.

Current implementation focus:
- D9
- D10

Vargas should:
- refine interpretation
- support D1 analysis
- provide structural context

Vargas must NOT:
- overwrite D1
- dominate foundational calculations
- mutate D1 core logic

Additional Vargas remain future expansion phases.

---

# 12. PIPELINE RUNNER

Purpose:
orchestrate deterministic execution flow.

Responsibilities:

- manage execution sequence
- pass normalized payloads
- coordinate engines
- preserve deterministic flow

Important:
Engines must NEVER directly call each other.

PipelineRunner remains the central orchestrator.

---

# 13. DETERMINISTIC ARCHITECTURE RULES

Core architecture rules:

Rule 1:
Keep calculations deterministic.

Rule 2:
Keep engines stateless.

Rule 3:
Keep modules independent.

Rule 4:
Avoid overengineering.

Rule 5:
Separate calculations from interpretation.

Rule 6:
Preserve D1 immutability.

Rule 7:
AI must NEVER generate astrology math.

---

# 14. D1 FOUNDATION PRINCIPLE

The D1 chart represents foundational astrology structure.

D1 must remain:

- foundational
- deterministic
- immutable
- explainable

Future refinement systems may support interpretation but must NOT overwrite D1 foundation logic.

---

# 15. OUTPUT FLOW

PDF/Input JSON
↓
Normalized JSON
↓
Deterministic Engine Outputs
↓
Structured Reports

Current outputs include:

- normalized JSON
- Graha strength reports
- House strength reports
- deterministic explainable outputs

---

# 16. TESTING ARCHITECTURE

Testing should remain:

- deterministic
- isolated
- reproducible
- schema-validated

Testing focus areas:

- extraction stability
- normalization correctness
- deterministic score consistency
- D1 immutability
- output reproducibility

---

# 17. CURRENT IMPLEMENTATION STATUS

Currently implemented and stabilized:

- project structure
- parser separation
- JSON normalization foundation (Dosha routed)
- Functional Nature Engine (Governance Locked)
- Planet Strength Engine
- House Strength Engine
- Varga Engine
- Ashtakavarga Engine
- Dasha Engine (Timeline contract)
- Transit Engine (Mandali Gochara)
- Yoga Engine
- Natal Promise Engine
- Master Probability Synthesis
- Pipeline Runner
- deterministic testing structure (613/613 Passed)

Not yet implemented:
- AI interpretation systems

---

# 18. TECHNOLOGY STACK

Current technology stack:

- Python
- VS Code
- local desktop execution
- JSON-based workflow

The current software does NOT require:

- cloud infrastructure
- distributed systems
- databases
- always-running services

The software should remain lightweight and modular.

---

# 19. FUTURE EXPANSION POLICY

Future systems should be added gradually and only after stabilization of:

- extraction
- normalization
- deterministic testing
- core engine correctness

Avoid premature expansion into:
- excessive framework abstraction
- unnecessary orchestration complexity
- oversized synthesis systems

The software should evolve carefully and remain maintainable.
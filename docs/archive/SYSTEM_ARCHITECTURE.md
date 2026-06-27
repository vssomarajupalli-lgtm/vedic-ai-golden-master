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

Current inputs strictly implemented:

- SAV (Sarvashtakavarga)
- Occupants
- Benefic Aspects
- Malefic Aspects
- House Type (Kendra/Trikona/Dusthana)
- House Yogas

Output:
0–100 deterministic house strength score.

Important:
Bhava Bala override logic has been permanently REMOVED. 
The House Strength formula explicitly adheres to foundational deterministic rules without bypasses.

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

Varga Neutral Fallback Contract:
- The engine enforces a strict neutral fallback score of `50.0` when requested Varga data is missing or incomplete, guaranteeing pipeline stability.

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

Rule 8:
No Double Penalty Rule. A planetary condition or affliction must be evaluated exactly once at its root (e.g., House or Planet Engine) and shall not be re-applied or compounded downstream.

Rule 9:
Engine Dependency Hierarchy is permanently FROZEN as a strict Directed Acyclic Graph (DAG). Lower engines must never depend on higher engines.

Rule 10:
Engine Output Contracts are permanently FROZEN. All mathematical logic changes must retain the standard JSON contract structure (`final_score`, `raw_score`, `breakdown`, `modifiers`, `confidence_flags`, `metadata`).


---

# 14. FOUR PILLAR PROMISE ARCHITECTURE

The Natal Promise Engine evaluates life domains using a strict, unalterable four-pillar formula to prevent double counting and preserve explainability:

- Bhava Strength (Field of manifestation): 35%
- Bhavadhipati Strength (Lord of the house): 30%
- Karaka Strength (Natural significator): 20%
- Varga Validation (Divisional chart): 15%

Support Houses are designated as a Deferred Status / Dead Configuration and are intentionally excluded from the Promise Engine mathematical flow.

---

# 15. YOGA GOVERNANCE

The Yoga Engine is governed by strict rules enforcing determinism and preserving core probability scoring:

- Detection, Classification, and Explanation ONLY.
- No scoring.
- No probability modification. 
- Yoga must never modify the Promise Score, Activation Score, Planet Score, or House Score.

---

# 16. D1 FOUNDATION PRINCIPLE

The D1 chart represents foundational astrology structure.

D1 must remain:

- foundational
- deterministic
- immutable
- explainable

Future refinement systems may support interpretation but must NOT overwrite D1 foundation logic.

---

# 17. OUTPUT FLOW

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

# 18. TESTING ARCHITECTURE

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

# 19. CURRENT IMPLEMENTATION STATUS

Currently implemented and stabilized:

- project structure
- parser separation
- JSON normalization foundation (Dosha routed)
- Functional Nature Engine (Governance Locked)
- Planet Strength Engine
- House Strength Engine
- Varga Engine (Fallback 50.0)
- Ashtakavarga Engine
- Dasha Engine (Timeline contract)
- Transit Engine (Moon-Centered Nine-Pada Mandali Gochara - FROZEN)
- Yoga Engine (Detection Only)
- Natal Promise Engine (Four Pillar locked)
- Master Probability Synthesis
- Pipeline Runner
- deterministic testing structure (Passed)
- Verification Console (Phase 15 Transparency)
- Phase 16A Architecture Constitution (Approved)
- Ownership Matrix & Formula Ownership Register (Finalized)
- Calibration Version Governance & Migration Strategy (Frozen)

Not yet implemented:
- AI interpretation systems

---

# 20. TECHNOLOGY STACK

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

# 21. FUTURE EXPANSION POLICY

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

---

# 22. CALIBRATION ARCHITECTURE

Documenting the mathematical Calibration Layer implemented in Phase 16A.3:

*   **CalibrationManager**: The singleton provider of configuration. Safely deserializes JSON tuning values into Python types (including restoring integer and tuple keys).
*   **Calibration Profiles**: 100% of the mathematical weights, matrices, and scores reside externally in JSON profiles.
*   **Dependency Injection**: Engines are initialized dynamically (`__init__(self, calibration=None)`) replacing hardcoded constant imports.
*   **One Active Profile Rule**: Only one uniform calibration profile can be loaded per pipeline execution to ensure consistent calculations.
*   **Immutable Runtime**: The `CalibrationManager` provides read-only fragments. No engine can mutate calibration math.
*   **Engine Independence**: Engines do not communicate mathematical changes to each other; they strictly query the central profile.
*   **Numerical Parity Principle**: The baseline implementation was mandated to achieve 100% parity against legacy hardcoded math before unlocking any tuning capabilities.
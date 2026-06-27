# PROJECT CONTEXT
# Deterministic Vedic Astrology Calculation Platform

---

# 1. PROJECT OVERVIEW

This project is a deterministic Vedic astrology calculation platform designed to:

- extract astrology data from horoscope PDFs
- normalize extracted data into structured JSON
- calculate Graha (planetary) strengths
- calculate Bhava/Rasi (house) strengths
- generate deterministic explainable outputs

The software focuses on calculation correctness, modularity, and deterministic architecture.

The project is currently in a foundational engine development phase.

---

# 2. CURRENT PROJECT FOCUS

Current implementation focus:

1. PDF extraction stability
2. JSON normalization
3. deterministic Graha strength calculations
4. deterministic House strength calculations
5. deterministic testing
6. explainable outputs

The project is currently focused on building a stable core calculation engine.

---

# 3. CURRENT SOFTWARE IDENTITY

Current software identity:

DETERMINISTIC ASTROLOGY CALCULATION PLATFORM

The current software is NOT yet:

- a full autonomous astrology intelligence ecosystem
- a continuous prediction engine
- a large probabilistic synthesis platform
- a conversational astrology AI system

Those remain possible future roadmap directions only.

---

# 4. CURRENT IMPLEMENTED COMPONENTS

The following core components are currently implemented or partially stabilized:

## Implemented

- project structure stabilization
- parser/engine separation
- JSON normalization foundation
- Planet Strength Engine
- House Strength Engine
- Pipeline Runner
- deterministic testing structure

## Partially Implemented

- PDF extraction stabilization
- Varga refinement support
- schema refinement
- extraction validation

## Not Yet Implemented

- Dasha engine
- Transit engine
- Probability synthesis systems
- Event-domain systems
- AI interpretation layer

---

# 5. CORE SOFTWARE WORKFLOW

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

# 6. PDF EXTRACTION CONTEXT

The software is designed to process astrology PDF reports containing:

- birth details
- D1 chart data
- Vargas
- Graha Bala
- Shadbala
- Bhava Bala
- Ashtakavarga
- Dasha tables
- transit sections
- phalita sections

The extraction process should remain staged:

Stage 1:
raw extraction

Stage 2:
table extraction

Stage 3:
heading identification

Stage 4:
structured JSON conversion

Stage 5:
validation and normalization

Current implementation priority remains extraction stability and structured JSON correctness.

---

# 7. DETERMINISTIC ENGINE CONTEXT

All engines must remain:

- deterministic
- modular
- stateless
- explainable
- independently testable

Engines must NEVER:
- generate random outputs
- mutate upstream payloads
- directly call other engines
- rely on AI-generated calculations

The PipelineRunner remains the only orchestrator.

---

# 8. D1 FOUNDATION PRINCIPLE

The D1 chart represents the foundational astrology layer.

All future refinement systems must treat D1 as:

- foundational
- deterministic
- immutable
- explainable

Future refinement systems may support interpretation but must NOT overwrite D1 foundation logic.

---

# 9. VARGA CONTEXT

Vargas provide structural refinement support.

Current implementation focus:
- D9
- D10

Vargas should:
- refine interpretation
- provide structural context
- support D1 analysis

Vargas should NOT:
- replace D1
- overwrite D1 scores
- dominate foundational calculations

Additional Vargas remain future expansion phases.

---

# 10. AI USAGE CONTEXT

AI may later assist with:

- report explanation
- formatting
- readable summaries
- interpretation enhancement

AI must NEVER:
- generate astrology calculations
- modify deterministic scores
- invent probabilities
- override deterministic engine outputs

Deterministic calculation engines remain primary.

---

# 11. FUTURE ROADMAP CONTEXT

The following systems are future roadmap phases and are NOT current implementation priorities:

- Dasha systems
- Transit systems
- Event-domain abstractions
- Probability synthesis
- AI interpretation systems
- conversational astrology assistants

These systems should only begin after:

- extraction stabilization
- deterministic engine stabilization
- schema stabilization
- testing stabilization

---

# 12. CURRENT DEVELOPMENT STRATEGY

Current strategy:

1. stabilize extraction
2. stabilize normalization
3. validate deterministic calculations
4. strengthen testing
5. improve explainability
6. expand carefully

The project should avoid premature expansion into:
- large synthesis systems
- excessive architecture abstraction
- unnecessary framework complexity

The software should evolve gradually and remain maintainable.

---

# 13. TESTING CONTEXT

Testing should remain:

- deterministic
- reproducible
- isolated
- schema-validated

Testing focus areas:

- extraction stability
- JSON normalization correctness
- Graha strength consistency
- House strength consistency
- D1 immutability
- deterministic outputs

---

# 14. CURRENT PRACTICAL GOAL

The current practical goal is:

Build a stable deterministic astrology calculation engine capable of:

- processing astrology PDFs
- generating normalized JSON
- calculating explainable Graha strengths
- calculating explainable House strengths
- producing deterministic outputs

The current phase prioritizes correctness and stability over feature expansion.

---

# 15. LONG-TERM DIRECTION

Future expansion may later include:

- Dasha timing systems
- Transit evaluation
- question-based prediction support
- AI-assisted interpretation
- enhanced reporting

However, all future systems must remain:

- deterministic
- modular
- explainable
- maintainable
- secondary to core calculation correctness
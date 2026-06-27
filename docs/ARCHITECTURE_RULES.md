# ARCHITECTURE RULES
# Deterministic Vedic Astrology Calculation Platform

---

# PURPOSE OF THIS FILE

This document defines the active architectural rules for the current implementation phase of the software.

Its purpose is to:

- preserve deterministic design
- maintain modular architecture
- prevent coding confusion
- prevent unnecessary overengineering
- maintain implementation discipline

This document should reflect CURRENT implementation discipline.

Future roadmap systems should remain secondary to current deterministic engine stabilization.

---

# 1. CORE ARCHITECTURE PRINCIPLE

The software must remain:

- deterministic
- modular
- explainable
- maintainable
- lightweight

The current software is primarily a:

DETERMINISTIC ASTROLOGY CALCULATION PLATFORM

The current implementation focus is:

- extraction
- normalization
- Graha strength calculations
- House strength calculations
- deterministic outputs

---

# 2. DETERMINISTIC CALCULATION RULE

All astrology calculations must remain:

- deterministic
- reproducible
- explainable
- auditable

The software must avoid:

- hidden calculations
- random scoring
- AI-generated math
- unpredictable outputs

Every score modification should be traceable.

---

# 3. D1 IMMUTABILITY RULE

The D1 chart represents the foundational astrology layer.

D1 must remain:

- foundational
- deterministic
- immutable
- explainable

Future refinement systems may support interpretation but must NOT overwrite D1 foundation logic.

---

# 4. ENGINE ISOLATION RULE

Each engine must remain independent.

Engines must:

- accept normalized payloads
- calculate deterministically
- return structured outputs
- remain stateless

Engines must NEVER:

- directly call other engines
- mutate upstream payloads
- retain runtime memory/state
- perform orchestration logic

---

# 5. PIPELINE RUNNER RULE

The PipelineRunner remains the central orchestrator.

Responsibilities:

- execution sequencing
- payload handoff
- deterministic flow control
- engine coordination

Important:
engines must NEVER orchestrate each other.

---

# 6. JSON NORMALIZATION RULE

All engines must consume normalized JSON only.

Engines must NEVER directly depend on:

- PDFs
- OCR systems
- extraction internals
- raw extraction text

Normalization layer responsibilities:

- schema consistency
- type normalization
- safe defaults
- payload stabilization

---

# 7. MODULARITY RULE

The software should remain modular.

Modules should remain separated:

- parsers
- normalization
- engines
- utilities
- configuration
- testing

Avoid:
- tightly coupled logic
- giant monolithic modules
- unnecessary dependencies

---

# 8. OVERENGINEERING PREVENTION RULE

Current implementation phase prioritizes:

- correctness
- stability
- maintainability
- testing
- extraction quality

Avoid premature expansion into:

- excessive framework abstraction
- oversized synthesis systems
- unnecessary orchestration complexity
- speculative architecture systems

The project should evolve gradually.

---

# 9. EXPLAINABILITY RULE

All deterministic outputs should remain explainable.

Outputs should support:

- readable score reasoning
- breakdown visibility
- traceable modifiers
- reproducible results

The software should avoid:
- black-box calculations
- unexplained adjustments
- hidden modifiers

---

# 10. AI USAGE RULE

AI may later assist with:

- summaries
- formatting
- readable reports
- explanation enhancement

AI must NEVER:

- generate astrology math
- override deterministic scores
- invent probabilities
- mutate engine outputs

Deterministic engines remain primary.

---

# 11. TESTING RULE

Testing should remain:

- deterministic
- isolated
- reproducible
- schema-validated

Testing focus areas:

- extraction stability
- normalization correctness
- Graha score consistency
- House score consistency
- D1 immutability
- output reproducibility

---

# 12. VARGA RULE

Vargas provide structural refinement support.

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

# 13. CURRENT IMPLEMENTATION BOUNDARY

Current implementation boundaries include:

- PDF extraction
- JSON normalization
- Graha strength calculations
- House strength calculations
- deterministic reporting

The following remain FUTURE roadmap phases:

- Dasha systems
- Transit systems
- Event-domain systems
- Probability synthesis systems
- AI interpretation systems

These are NOT current implementation priorities.

---

# 14. TECHNOLOGY RULE

Current software direction:

- Python
- local desktop execution
- JSON-based workflow
- lightweight modular structure

Current software does NOT require:

- databases
- distributed systems
- cloud orchestration
- always-running services

The software should remain lightweight and maintainable.

---

# 15. DEVELOPMENT DISCIPLINE RULE

Before adding new systems:

first stabilize:
- extraction
- normalization
- deterministic scoring
- testing
- output consistency

New architecture layers should only be added after:
- current modules stabilize
- deterministic correctness is validated
- testing coverage improves

Correctness is more important than rapid feature expansion.

---

# 16. FUTURE ROADMAP RULE

Future systems may later include:

- Dasha timing systems
- Transit evaluation
- question-based future prediction
- AI-assisted interpretation
- enhanced reporting

Future roadmap systems must remain:

- modular
- deterministic
- explainable
- secondary to core calculation correctness

The project should expand carefully and remain maintainable.
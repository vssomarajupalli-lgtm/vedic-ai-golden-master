# JSON CONTRACT MASTER
# Deterministic Vedic Astrology Calculation Platform

---

# PURPOSE OF THIS FILE

This document defines the active JSON contract philosophy and current normalized payload structure for the software.

Its purpose is to:

- maintain schema consistency
- stabilize deterministic engine inputs
- prevent payload confusion
- support modular engine design
- simplify future testing and validation

This file reflects CURRENT implementation contracts.

Future roadmap contracts should remain clearly separated from current active schemas.

---

# 1. CURRENT CONTRACT PHILOSOPHY

Current implementation contracts primarily support:

- PDF extraction normalization
- deterministic Graha calculations
- deterministic House calculations
- Varga refinement support
- deterministic output generation

The current implementation does NOT yet require:

- event-domain contracts
- probability synthesis contracts
- AI interpretation contracts
- large temporal orchestration payloads

Those remain future roadmap phases.

---

# 2. NORMALIZATION PRINCIPLE

All engines must consume:

NORMALIZED JSON ONLY

Engines must NEVER directly depend on:

- PDFs
- OCR systems
- raw extraction text
- parser-specific formats

The normalization layer is responsible for:

- schema consistency
- safe defaults
- type normalization
- missing field handling
- payload stabilization

---

# 3. CURRENT HIGH-LEVEL JSON FLOW

PDF/Input JSON
↓
Raw Extraction JSON
↓
Cleaned JSON
↓
Normalized JSON
↓
Engine Inputs
↓
Deterministic Outputs

---

# 4. CURRENT ACTIVE CONTRACT STRUCTURE

Current active normalized payload structure:

```json
{
  "birth_details": {},
  "d1_chart": {},
  "vargas": {},
  "planet_strength_inputs": {},
  "house_strength_inputs": {},
  "metadata": {}
}
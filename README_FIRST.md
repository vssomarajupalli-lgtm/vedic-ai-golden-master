# README_FIRST.md

---

This document is intentionally concise.

Its purpose is to provide startup guidance only.

Detailed architecture, governance, calibration, roadmap, project status and implementation specifications are maintained in their respective authoritative documents.

This document must not duplicate those documents.

---

# VEDIC-AI GOLDEN MASTER — STARTUP GUIDE

## Project Purpose

Build a deterministic Vedic Astrology Intelligence System that:
- Loads canonical horoscope JSON from HoroscopeCleaner_Final
- Validates and normalizes astrology data
- Calculates deterministic Planet/House/Varga/Ashtakavarga/Dasha/Transit/Yoga/Natal Promise/Master Probability
- Evaluates 83 questions across 13 domains using 43 calibrated formulas
- Produces deterministic API, HTML, PDF, and question answers

---

# AUTHORITY HIERARCHY

If any document conflicts, higher priority wins.

| Priority | Document | Purpose |
|----------|----------|---------|
| 1 | Source Code | Implementation truth |
| 2 | `VEDIC_AI_SOURCE_OF_TRUTH.md` | Official source assets, data ownership, contracts, boundaries |
| 3 | `SYSTEM_ARCHITECTURE.md` | Architecture constraints, engine definitions, rules |
| 4 | `PROJECT_STATUS_MASTER.md` | Current project status, completed/pending work, priorities |
| 5 | `VEDIC_AI_MASTER_DEVELOPMENT_ROADMAP.md` | Feature roadmap, milestones, long-term planning |

**Design References** (read when needed): `docs/GOCHARA_MANDALI_GOVERNANCE_v1.md`, `docs/ARCHITECTURE_RULES.md`, `docs/knowledge/PROJECT_REQUIREMENTS.md`, `docs/knowledge/VEDIC_AI_MASTER_ARCHITECTURE.md`, `docs/knowledge/VEDIC_AI_PROBABILITY_ENGINE_ARCHITECTURE.md`

---

# STARTUP RULES

Before implementing anything:

1. Read this README_FIRST.md completely
2. Verify project status in `docs/status/PROJECT_STATUS_MASTER.md`
3. Verify roadmap in `docs/knowledge/VEDIC_AI_MASTER_DEVELOPMENT_ROADMAP.md`
4. Verify architecture in `docs/SYSTEM_ARCHITECTURE.md`
5. Implement only approved backlog items from `docs/knowledge/VEDIC_AI_MASTER_DEVELOPMENT_ROADMAP.md`
6. Never use archived documents
7. Never bypass deterministic engines
8. Never modify frozen architecture without Architecture Review Board approval

---

# PERMANENT ENGINEERING PRINCIPLES

**Deterministic Engine** — All calculations deterministic, explainable, reproducible.

**D1 Immutability** — D1 chart is foundational, deterministic, immutable, explainable. Future refinements support interpretation only.

**Engine Independence** — Engines NEVER directly call each other. PipelineRunner is the central orchestrator.

**Parameter-Driven Evolution** — Deterministic engine stable after Feature Complete. Future refinement via centralized parameter/configuration files.

**Single Source of Truth** — Engines own calculations; configs own parameters; configs NEVER contain business logic; Yoga is descriptive only.

**Formula Governance** — Formula Registry (WHAT) → Formula Calibration (HOW MUCH) → Engine Calibration (HOW) → Master Probability.

**Calibration Governance** — CalibrationManager provides config; Profiles (v1.0_default IMMUTABLE, v1.0_current mutable, v1.0_frozen production); One Active Profile Rule; Immutable Runtime; Engine Independence; Numerical Parity Principle (100% parity vs legacy before tuning).

**Architecture Freeze** — 5 layers frozen; NO CHANGES without Architecture Review Board approval.

**Explainability** — All calculations transparent, auditable, traceable.

**No Hidden Calculations** — No AI-generated astrology math, no heuristic overrides of extracted truth.

---

# DEVELOPMENT PHILOSOPHY

1. Extract Truth → 2. Normalize Truth → 3. Consume Truth → 4. Derive Logic → 5. Present Results

Never: Invent astrology data, recalculate extracted values, override extracted truth with heuristics.

Always: Prefer extracted source data, prefer deterministic calculations, prefer transparent formulas, maintain auditability.

---

# DOCUMENT NAVIGATION

| Need | Go To |
|------|-------|
| What this project is | This file |
| Source assets & contracts | `VEDIC_AI_SOURCE_OF_TRUTH.md` |
| Engine definitions, rules, DAG | `SYSTEM_ARCHITECTURE.md` |
| Current status & priorities | `PROJECT_STATUS_MASTER.md` |
| Backlogs, milestones, Definition of Done | `VEDIC_AI_MASTER_DEVELOPMENT_ROADMAP.md` |
| Source assets & canonical JSON | `VEDIC_AI_SOURCE_OF_TRUTH.md` |
| Engine definitions, DAG, rules | `SYSTEM_ARCHITECTURE.md` |
| Calibration architecture | `SYSTEM_ARCHITECTURE.md` §22 |
| Yoga governance | `SYSTEM_ARCHITECTURE.md` §15 |
| Architecture freeze details | `SYSTEM_ARCHITECTURE.md` §21 |
| Current backlogs & milestones | `VEDIC_AI_MASTER_DEVELOPMENT_ROADMAP.md` |
| Completed/pending work | `PROJECT_STATUS_MASTER.md` |

---

# STARTUP CHECKLIST

Before implementing anything:

1. Read this README_FIRST.md completely
2. Verify project status in `docs/status/PROJECT_STATUS_MASTER.md`
3. Verify roadmap in `docs/knowledge/VEDIC_AI_MASTER_DEVELOPMENT_ROADMAP.md`
4. Verify architecture in `docs/SYSTEM_ARCHITECTURE.md`
5. Implement only approved backlog items from `docs/knowledge/VEDIC_AI_MASTER_DEVELOPMENT_ROADMAP.md`
6. Never use archived documents
7. Never bypass deterministic engines
8. Never modify frozen architecture without Architecture Review Board approval

---

# DOCUMENT MAINTENANCE RULE

README_FIRST.md shall contain only:

- Startup guidance
- Navigation
- Authority hierarchy
- Permanent engineering principles

It shall NEVER become:

- Architecture documentation
- Roadmap
- Status report
- Implementation guide
- Backlog tracker
- Calibration specification

---

**README_FIRST.md is now a stable startup document suitable for long-term use.**
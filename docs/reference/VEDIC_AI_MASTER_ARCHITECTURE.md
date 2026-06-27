# VEDIC_AI_MASTER_ARCHITECTURE.md

## Project Vision
Vedic-AI is a deterministic Vedic Astrology Intelligence System. It executes mathematical rules on parsed data without AI hallucination.

## Core Engines (Fully Implemented)

### 1. Planet Strength Engine
Calculates classical dignity, placement, aspects, and state modifiers. Output: 0-100%

### 2. House Strength Engine
Calculates Bhava Bala, lord contribution, occupants, and aspects. Output: 0-100%

### 3. Rasi Strength Engine
Calculates strength of the 12 signs using SAV Bindus and Rasi Lord strength. Output: 0-100%

### 4. Ashtakavarga Engine
Integrates SAV and BAV bindu counts to evaluate support.

### 5. Dasha Activation Engine
Calculates Vimshottari Mahadasha and Antardasha temporal mapping. Output: 0-100%

### 6. Varga Engine
Validates planetary dignity across divisional charts (D9, D10).

### 7. Yoga Engine
Detects and mathematically scores major classical Parashari Yogas (Raja, Dhana, Arishta, Gaja Kesari, Pancha Mahapurusha, Neecha Bhanga). 

### 8. Transit Engine
Integrates live Gochara using Swiss Ephemeris (`swisseph`) for dynamic activation timing. Includes a synthetic orbit fallback for offline/development environments.

### 9. Natal Promise Engine
Synthesizes planetary, house, and yoga strengths into core Life Domains (Wealth, Career, Health, Marriage, Education, Spirituality).

### 10. Master Probability Engine
Aggregates all pipelines into a final deterministic probability score, generating a definitive Master Grade (e.g., EXCELLENT, WEAK).

### 11. Question Engine
Uses the Master Probability engine outputs to ground Natural Language Queries, safely prompting LLMs for domain-specific readings.

---

## Technical Architecture Layers (Phase 4 Complete)

### 1. Extraction Pipeline (HoroscopeCleaner_Final)
Responsible for producing the mandatory `machine_index.json` and `canonical_content.json`.

### 2. Deterministic Calculation Core (Python)
The pure math layer containing the 11 engines. Completely stateless and strictly tested (619 assertions).

### 3. REST API (FastAPI)
Exposes the calculation core via stateless endpoints (`/process-chart`, `/ask-question`, `/generate-report`). Enforces strict `Pydantic` schema validation.

### 4. Report Generation
Consumes API output to build professional, deterministic templates in JSON, HTML (`Jinja2`), and PDF (`WeasyPrint`).

### 5. Frontend UI (React + Vite PWA)
A mobile-first, installable Progressive Web App. Uses `Zustand` for stateless in-memory storage of the calculation payload, enabling instant navigation between Dashboard, Results, Question Engine, and Export components.

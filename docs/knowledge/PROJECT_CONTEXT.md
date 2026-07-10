# PROJECT_CONTEXT.md

## What is Vedic-AI?
Vedic-AI is a deterministic Vedic Astrology engine designed to intake normalized JSON data (originally scraped from massive astrology PDFs) and output highly accurate, mathematically rigorous life predictions. 

## Current Implementation Phase
We have successfully completed **Phase 4: Frontend & API Integration**.
The V1 architecture is formally frozen.

## Tech Stack
- **Backend Core**: Python 3.14
- **Math Libraries**: `pyswisseph` (Swiss Ephemeris for planetary calculations)
- **API Framework**: FastAPI, Pydantic
- **Testing**: Pytest (619 tests passing)
- **Report Generation**: Jinja2 (HTML), WeasyPrint (PDF)
- **Frontend**: React 18, TypeScript, Vite (PWA), Tailwind CSS, Zustand, React Router DOM, Axios.

## Core Directives
- **Zero Hallucination**: AI is strictly relegated to the final `QuestionEngine` layer, where it acts as a translator for the underlying rigid math.
- **Modularity**: Every astrology concept (Yogas, Transits, House Strength, Dashas) is isolated into its own mathematical engine class.

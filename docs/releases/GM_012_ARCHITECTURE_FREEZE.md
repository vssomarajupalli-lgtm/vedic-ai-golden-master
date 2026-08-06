# GM-012 Architecture Freeze

## Current Runtime Architecture — Frozen Baseline

**Date:** 2026-08-06  
**Commit SHA:** `53e82d6`  
**Tag:** `gm-012-complete`

This document freezes the runtime architecture at the GM-012 milestone.
No architectural changes are permitted without a new release review.

---

## Frozen Data Flow

```
JsonNormalizer
      ↓
PipelineRunner
      ↓
MandaliTransitAdapter
      ↓
UniversalMandaliEngine
      ↓
MandaliPlacementFactory
      ↓
Builders
      ↓
ReportBuilder
```

---

## Layer Responsibilities

### 1. JsonNormalizer
`backend/app/parsers/json_normalizer.py`
- Transforms raw HoroscopeCleaner `raw_*` JSON into normalized engine schema
- Type coercion, key normalization, safe defaults
- **Owns:** normalization only. No astrology, no orchestration.

### 2. PipelineRunner
`backend/app/pipeline_runner.py`
- The sole orchestrator of the calculation pipeline
- Resolves `target_date_utc` (Single Source of Truth)
- Calls engines sequentially, threads dependencies
- Builds runtime `canonical_json` for Mandali from normalized natal + ephemeris
- Instantiates and drives MandaliPlacementFactory and builders
- **Owns:** orchestration, dependency injection, DTO assembly

### 3. MandaliTransitAdapter
`backend/app/engines/mandali_transit_adapter.py`
- Pure mapping layer: EphemerisService snapshot → Mandali `current_transit` schema
- Reuses existing resolver/logic; no duplicated astronomy
- **Owns:** format translation only

### 4. UniversalMandaliEngine
`backend/app/engines/universal_mandali_engine.py`
- Capability 7.7 composition engine
- Produces `MandaliAdvisory` (calculation data only)
- **Owns:** mandali grid, transit resolutions, lifecycle projections, advisory composition
- **Does NOT own:** placement DTOs, presentation, formatting, anonymous objects

### 5. MandaliPlacementFactory
`backend/app/builders/mandali_placement_factory.py`
- Builds `NatalPlanetPlacement` / `CurrentTransitPlanetPlacement` DTOs
- Zero calculations; pure DTO construction
- **Owns:** placement DTO creation

### 6. Builders
- `MandaliChartLayoutBuilder` — grid cell layout from placements
- `TransitionSummaryBuilder` — transition summary rows (next mandali, entry date, days remaining)
- **Owns:** presentation/layout composition only

### 7. ReportBuilder
`backend/app/reports/builder.py`
- Assembles the final user-facing report JSON
- Serializes fully populated `MandaliResponseDTO` (incl. `mandali_analysis`)
- **Owns:** report assembly only

---

## Architectural Principles (Enforced)

| Principle | Status |
|-----------|--------|
| Engine Isolation | UniversalMandaliEngine = calculation only |
| PipelineRunner Orchestrator | Single orchestrator, no engines orchestrate others |
| One Formula One Owner | Each formula/builder owned in exactly one place |
| Separation of Concerns | Normalize → Orchestrate → Calculate → Map → Layout → Report |
| DTO-driven | Typed dataclasses between layers |
| No anonymous objects | Removed; factory produces typed DTOs |
| Canonical JSON immutability | Runtime canonical_json built fresh per request; never mutated |
| No duplicate logic | Adapter reuses resolver/house logic |

---

## Frozen Endpoints

- `POST /api/v1/process-chart`
- `POST /api/v1/generate-report`
- `POST /api/v1/ask-question`
- `POST /api/v1/ask-structured-question`
- Knowledge graph endpoints (`/knowledge/state`, `/knowledge/seed`, …)
- Health endpoints

---

## Change Policy

Any modification to the frozen architecture requires:
1. A new release ticket (e.g., GM-013)
2. Architecture review
3. Validation against this freeze document
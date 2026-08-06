# GM-012 Release Notes

## Vedic AI — Mandali Runtime Integration

**Date:** 2026-08-06  
**Commit SHA:** `53e82d6`  
**Tag:** `gm-012-complete`

---

## 1. Executive Summary

GM-012 delivers complete Mandali Runtime Integration. The Universal Mandali Engine is now fully wired into the deterministic astrology pipeline. Runtime transit data flows from the Swiss Ephemeris fallback through a dedicated adapter, placement DTOs are built by a dedicated factory, and MandaliResponseDTO is fully populated end-to-end (natal chart, current chart, and transition summary). This milestone closes the prior gap where `mandali_analysis` was structurally present but contained zero populated data.

---

## 2. Objectives Achieved

- ✓ Runtime transit pipeline integrated (EphemerisService → adapter → Mandali engine)
- ✓ MandaliPlacementFactory created for DTO construction
- ✓ MandaliResponseDTO fully populated (natal/chart/transition)
- ✓ ReportBuilder consumes complete Mandali analysis
- ✓ Engine Isolation Principle preserved
- ✓ PipelineRunner orchestrator principle preserved
- ✓ Anonymous runtime objects removed
- ✓ Backend starts, Process Chart and Generate Report pass

---

## 3. Architecture Changes

Data flow established:

```
JsonNormalizer
      ↓
PipelineRunner
      ↓
MandaliTransitAdapter  (EphemerisService → current_transit)
      ↓
UniversalMandaliEngine → MandaliAdvisory
      ↓
MandaliPlacementFactory → Natal/Current Placement DTOs
      ↓
MandaliChartLayoutBuilder / TransitionSummaryBuilder
      ↓
MandaliResponseDTO
      ↓
ReportBuilder
```

Key change: placement DTO creation moved from the calculation engine up into
the orchestration layer (PipelineRunner + MandaliPlacementFactory), restoring
strict Separation of Concerns.

---

## 4. New Components

- **MandaliPlacementFactory** (`backend/app/builders/mandali_placement_factory.py`)
  - Builds `NatalPlanetPlacement` and `CurrentTransitPlanetPlacement` DTOs
  - Pure mapping layer; no calculations
- **MandaliTransitAdapter** (`backend/app/engines/mandali_transit_adapter.py`)
  - Transforms EphemerisService snapshot into Mandali `current_transit` schema
  - Reuses NakshatraPadaResolver logic and existing house-from-Moon calculation
- **Builder migration**: `mandali_chart_layout_builder.py` and
  `transition_summary_builder.py` moved into `builders/` package

---

## 5. Modified Components

- **PipelineRunner** — orchestrates Ephemeris → adapter → Mandali → factory → builders
- **UniversalMandaliEngine** — returns calculation data only; removed anonymous placement objects
- **ReportBuilder** — serializes fully populated MandaliResponseDTO
- **QuestionEngine** — import fix for `Optional`/`datetime` startup blocker
- **JsonNormalizer** — sign normalization for registry-compatible rasi names
- **TransitEngine** — consumes transit payload house numbers
- **EphemerisService** — standard rasi naming for reference registry

---

## 6. Validation Results

| Area | Status |
|------|--------|
| Backend Start | PASS |
| Swagger | PASS |
| Health API | PASS |
| Knowledge APIs | PASS |
| Process Chart | PASS |
| Generate Report | PASS |
| Mandali (natal/current/transition) | PASS |
| Question API | PASS |
| Frontend | Not re-executed this cycle |

---

## 7. Repository Changes

**Files Added (commit `53e82d6`):** 12 new
- builders (`mandali_placement_factory.py`, `mandali_chart_layout_builder.py`, `transition_summary_builder.py`, `__init__.py`)
- engines (`mandali_transit_adapter.py`)
- schemas (`current_chart.py`, `mandali_chart_cell.py`, `mandali_response.py`, `natal_chart.py`, `report.py`, `transition_summary.py`)
- services (`question_service.py`)

**Files Modified:** 9 (queries, reports, question_engine, transit_engine, universal_mandali_engine, json_normalizer, pipeline_runner, report/builder, ephemeris_service)

**Files Removed (cleanup):** duplicate builder copies, accidental frontend files in backend/, temp artifacts

---

## 8. Known Deferred Work

- Repository cleanup pending (remaining uncommitted source)
- Remaining schema review (uncommitted schema files)
- Frontend review (uncommitted components/hooks/services)
- Future backlog references (GM-013 planning)
- Explanation Engine commit pending (`8b59822` pre-roll)

---

## 9. Git Information

- **Commit SHA:** `53e82d6`
- **Tag:** `gm-012-complete`
- **Date:** 2026-08-06
- **Branch:** `main`
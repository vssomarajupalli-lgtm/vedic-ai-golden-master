# System Architecture

**Last Updated:** 2026-06-25 (Phase 16B Completion)

## Core Philosophy
The Vedic AI System operates as a strictly deterministic pipeline. There are NO generative AI components computing astrological math. Generative AI is exclusively reserved for linguistic mapping on the periphery, translating structured data payload into readable answers.

## The PipelineRunner Architecture
The `PipelineRunner` acts as the master coordinator. Its execution flow:
1. Normalizes incoming raw chart JSON via `JsonNormalizer`.
2. Executes structural engines (`PlanetStrengthEngine`, `HouseStrengthEngine`, `VargaEngine`).
3. Executes timing engines (`DashaEngine`, `AshtakavargaEngine`, `TransitEngine`).
4. Executes synthesis engines (`NatalPromiseEngine`, `MasterProbabilityEngine`).

## Master Probability & Timeline Generation
The `MasterProbabilityEngine` computes the `lifetime_projection`—a deterministic timeline mapping Vimshottari Dasha (MD-AD-PD) periods against combined astrological strength rules to produce activation percentages and final probability scores. This structure is preserved intact across the serialization boundary.

## Question Engine Integration
The API (`api/v1/endpoints/reports.py`) injects dynamic queries into the pipeline:
1. Routes questions to standard domains (e.g., "Career").
2. Queries the `QuestionEngine` via `PipelineRunner.answer_question()`.
3. The runner recalculates specific domain contributions while strictly **preserving** the non-domain specific `lifetime_projection`.
4. Extracted `top_opportunities` (future windows) are returned natively.

## Report Generation Flow
The `ReportBuilder` invokes localized extractors (e.g., `MasterProbabilitySection`) to convert the complex `PipelineRunner` nested dicts into a flat `FinalReportSchema`. This schema is directly consumed and rendered by the Jinja2 `base.html` template.

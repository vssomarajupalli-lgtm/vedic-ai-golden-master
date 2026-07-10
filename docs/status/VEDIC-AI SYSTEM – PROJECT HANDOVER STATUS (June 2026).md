# VEDIC-AI SYSTEM – PROJECT HANDOVER STATUS (June 2026)

## PROJECT GOAL

Build a deterministic Vedic Astrology platform that:

1. Accepts HoroscopeCleaner_Final output.
2. Processes horoscope data through:

   * Planet Strength Engine
   * House Strength Engine
   * Rasi Strength Engine
   * Ashtakavarga Engine
   * Dasha Engine
   * Transit Engine
   * Natal Promise Engine
   * Yoga Engine
   * Master Probability Engine
3. Produces:

   * Life Domain Scores
   * Yoga Analysis
   * Dasha Analysis
   * Transit (Gochara) Analysis
   * Question Engine Answers
   * PDF/HTML Reports
4. Uses deterministic calculations first and LLM explanation second.

---

# CURRENT PROJECT STATUS

## Backend

Status: RUNNING

API Documentation:

http://127.0.0.1:8000/docs

Main endpoints:

GET /api/v1/health/

POST /api/v1/process-chart

POST /api/v1/generate-report

POST /api/v1/ask-question

---

## Frontend

Status: RUNNING

Implemented pages:

Dashboard.tsx

Upload.tsx

Results.tsx

QuestionEngine.tsx

ExportReport.tsx

Frontend routing fixed.

"Coming Soon" placeholders removed.

Frontend builds successfully.

---

# MAJOR ISSUES FIXED

## Issue 1 – Placeholder Screens

Problem:

App.tsx was using dummy pages.

Fix:

Replaced placeholders with actual page imports.

Status:

FIXED

---

## Issue 2 – Pydantic 422 Validation

Problem:

Backend expected Dict.

Frontend sometimes sent arrays.

Fix:

Schema relaxed.

Status:

FIXED

---

## Issue 3 – process-chart Crash

Problem:

charts.py expected:

master_synthesis

Pipeline returned:

master_probability

Fix:

Updated endpoint.

Status:

FIXED

---

## Issue 4 – ReportBuilder Crash

Problem:

machine_index handled as dict.

Actual structure was list.

Fix:

Safe handling added.

Status:

FIXED

---

## Issue 5 – Report Extraction Paths

Problem:

Reports expected:

root.yogas
root.natal_promises

Actual output:

engine_outputs.yogas
engine_outputs.natal_promise

Fix:

Updated extractors.

Status:

FIXED

---

## Issue 6 – UNKNOWN Grades

Problem:

Extractor used:

details.get("grade")

NatalPromiseEngine outputs:

details["promise"]

Fix:

Changed extractor to:

details.get("promise", "UNKNOWN")

Result:

UNKNOWN → WEAK

Status:

FIXED

---

# CURRENT CRITICAL PROBLEM

## Symptoms

Results page shows:

Marriage = 48

Career = 48

Wealth = 48

Education = 48

Children = 48

Property = 48

Health = 48

Spirituality = 48

All grades:

WEAK

Yoga output:

Missing or incomplete

Question Engine:

Not producing meaningful output

Transit / Gochara:

Not visible

---

# WHAT HAS BEEN PROVEN

Frontend receives report.

Frontend renders report.

Grades now render correctly.

The remaining issue is upstream.

---

# JSON STRUCTURE VERIFIED

canonical_content.json contains:

birth_data

planets

houses

vargas

dashas

ashtakavarga

machine_index.json contains:

report metadata

section mappings

page mappings

native_info

---

# MACHINE INDEX INVESTIGATION

Result:

machine_index is NOT used by astrology calculations.

Used only for:

Report metadata

Client information

Navigation

PDF structure

Conclusion:

Astrology calculations depend on canonical_content.json only.

---

# JSON NORMALIZER STATUS

Current code on disk:

Supports:

raw_planets OR planets

raw_houses OR houses

raw_vargas OR vargas

raw_dashas OR dashas

raw_ashtakavarga OR ashtakavarga

birth_data

Example:

raw_data.get("raw_planets")
or raw_data.get("planets", {})

This patch IS PRESENT in source code.

Verified manually.

---

# PLANET NAME MAPPING VERIFIED

Surya -> sun

Chandra -> moon

Kuja -> mars

Budha -> mercury

Guru -> jupiter

Shukra -> venus

Shani -> saturn

Rahu -> rahu

Ketu -> ketu

No mapping failures found.

---

# MAJOR CONTRADICTION DISCOVERED

Audit reports claimed:

Normalized planets = 0

Normalized houses = 0

However:

Current JsonNormalizer source code supports actual file structure.

Planet mappings are valid.

Therefore root cause remains UNPROVEN.

Runtime evidence still missing.

---

# FILES MODIFIED DURING DEBUGGING

backend/app/api/v1/endpoints/charts.py

backend/app/api/v1/endpoints/reports.py

backend/app/parsers/json_normalizer.py

backend/app/reports/builder.py

backend/app/reports/sections/extractors.py

backend/app/engines/natal_promise_engine.py

backend/app/pipeline_runner.py

frontend/src/App.tsx

frontend/src/pages/Upload.tsx

frontend/src/api/backend.ts

---

# TEST STATUS

Pytest:

619 / 619 tests passing

No known test failures.

---

# WHAT IS NOT WORKING

1. Life Domain scores remain fixed at 48.

2. Real horoscope data not proven to reach NatalPromiseEngine.

3. Yoga analysis incomplete.

4. Question Engine output not validated.

5. Transit / Gochara integration not validated.

6. Final predictive report not achieved.

---

# NEXT ACTION PLAN (MANDATORY)

DO NOT:

Rewrite project.

Rewrite rules MD.

Rewrite architecture.

Rewrite engines.

Add more speculative fixes.

---

## PHASE 1 – RUNTIME PROOF

Create:

test_real_chart.py

Purpose:

Run without:

Frontend

FastAPI

ReportBuilder

Question Engine

Load:

canonical_content.json

Execute:

JsonNormalizer

PipelineRunner

Print:

Normalized planet count

Normalized house count

Marriage score

Career score

Wealth score

Yoga count

Master score

Goal:

Prove whether 48 originates inside core engine or later.

---

## PHASE 2

If test_real_chart.py outputs:

48 / 48 / 48

Root cause is inside:

JsonNormalizer

PipelineRunner

NatalPromiseEngine

---

## PHASE 3

If test_real_chart.py outputs:

19 / 62 / 57 etc.

Root cause is inside:

FastAPI

ReportBuilder

Frontend

---

## PHASE 4

Only after real scores appear:

Validate:

Yoga Engine

Question Engine

Transit Engine

Gochara

PDF Reports

---

# FINAL ASSESSMENT

Architecture Status:
~80%

User-Facing Astrology Output:
~20%

Project is NOT complete.

Core unresolved issue:

Real horoscope data is not yet proven to flow correctly through the complete pipeline.

The next session must begin with runtime proof, not further theory.


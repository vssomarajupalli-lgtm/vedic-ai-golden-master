# REPORT SYSTEM KNOWLEDGE PACKAGE

## 1. Executive Summary
The Report System is responsible for formatting, generating, and delivering the astrological evaluations. It converts the deeply nested, deterministic JSON outputs produced by the `PipelineRunner` and Master Probability engine into structured HTML, PDF, or specialized JSON schemas for consumption by the user or client applications.

## 2. Purpose
To abstract presentation logic away from calculation logic. The astrological engines should only return math and metadata. The Report System takes that metadata and applies layout, branding, and human-readable templating.

## 3. Responsibilities
- Receives the raw computational output (`breakdown`, `final_score`).
- Formats the data according to predefined schemas.
- Uses HTML/PDF generators to build static, downloadable reports.
- Isolates text generation from the core analytical math.

## 4. Architecture
Located under `backend/app/reports/`. It utilizes a builder pattern (`builder.py`) to assemble various sections (`sections/`) of a report based on `templates/`.
- `builder.py`: Orchestrates the assembly of the report.
- `html_generator.py`: Converts raw data schemas into HTML strings.
- `pdf_generator.py`: Compiles HTML and CSS into a binary PDF payload.
- `schemas.py`: Defines Pydantic models enforcing the shape of the report data payload.

## 5. Inputs
- `engine_outputs` (The raw output dictionary from the `PipelineRunner`).
- Report configuration (e.g., format requested: HTML vs PDF).

## 6. Outputs
- Formatted documents (PDF binaries or HTML strings).
- Structured JSON conforming to `schemas.py`.

## 7. Data Contracts
- The report system strictly enforces the shape of the presentation payload using Pydantic schemas, ensuring the frontend always receives predictable shapes regardless of how the underlying calculation math evolves.

## 8. Engine Dependencies
- **Upstream:** `PipelineRunner` and all core engines.
- **Downstream:** Delivered via the API Layer (`app.api.v1.endpoints.reports`).

## 9. Implementation Files
- `backend/app/reports/builder.py`
- `backend/app/reports/html_generator.py`
- `backend/app/reports/pdf_generator.py`
- `backend/app/reports/schemas.py`
- `backend/app/reports/sections/`
- `backend/app/reports/templates/`

## 10. Technical Debt & Recommendations
- **Coupling of Text Generation:** Ensure no "astrological logic" leaks into the report layer. All decisions (e.g., determining if a yoga is "excellent" vs "good") must be done in the engine layer and passed as a string flag to the report layer.

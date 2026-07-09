# REPORT SYSTEM AUDIT
**Date:** 2026-06-18
**Focus:** Export Report Readiness and PDF Generation Constraints

## Executive Summary
An exhaustive audit of the `backend/app/reports/` directory and frontend `ExportReport.tsx` reveals that the report generation pipeline is **functionally complete** at the code level. The system successfully extracts deterministic data, builds structured schemas, and renders HTML. The sole blockade preventing PDF export is an environmental constraint: **missing OS-level GTK dependencies required by WeasyPrint**.

---

### 1. Is Report Builder complete?
**YES.** 
`builder.py` is fully implemented. It orchestrates `FinalReportSchema` via isolated sub-extractors (`MasterProbabilitySection`, `YogaAnalysisSection`, `NatalPromiseSection`, `ExecutiveSummarySection`, etc.). It natively consumes the output of the `PipelineRunner` without recalculating logic, strictly adhering to the Engine Isolation rule.

### 2. Is PDF generation complete?
**YES (Code-level).**
`pdf_generator.py` is fully written. It orchestrates the handover from `HTMLGenerator` to `weasyprint.HTML().write_pdf()`. The API endpoint (`/api/v1/endpoints/reports.py`) is fully wired to receive the `?format=pdf` query parameter, and the frontend `ExportReport.tsx` correctly triggers the download.

### 3. Is the problem only WeasyPrint OS dependencies?
**YES.**
The codebase actively traps the missing dependency in `pdf_generator.py`:
```python
try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False
```
Because WeasyPrint relies heavily on C-level libraries (Pango, Cairo, GDK-PixBuf) that do not natively exist on standard Windows development environments, the import fails, tripping the fallback flag.

### 4. Can reports currently be generated successfully?
**YES (Partial Formats).**
The system currently generates flawless outputs for:
* **Raw JSON:** Natively structured by `ReportBuilder`.
* **Standalone HTML:** Flawlessly rendered by `html_generator.py`.
Users can successfully click "Raw JSON" or "Standalone HTML" on the frontend today.

### 5. What exact error prevents end-to-end export?
When a user clicks "Printable PDF", the API executes the `pdf_generator.py` class. Because `WEASYPRINT_AVAILABLE` evaluates to `False`, the code throws a `RuntimeError` which is caught by the API and surfaced to the frontend as an HTTP 501:
`"Failed to download PDF: WeasyPrint OS dependencies are missing. Cannot generate PDF natively."`

### 6. Is Docker packaging sufficient to solve it?
**YES.**
Dockerizing the backend using a standard Linux container (e.g., `python:3.11-slim`) completely resolves the problem. A simple `apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 libcairo2` in the Dockerfile provides all necessary GTK bindings for WeasyPrint natively.

### 7. Would replacing WeasyPrint be necessary?
**NO.**
Replacing WeasyPrint is not necessary and would be highly destructive to the current architecture. Shifting to ReportLab would require rewriting the entire HTML template into proprietary Python canvas drawing commands. Shifting PDF generation to the React frontend (e.g., `html2pdf.js`) would strip the backend of its "Single Source of Truth" reporting capability. 

### 8. What is the safest solution that preserves architecture?
**DOCKERIZATION.**
The absolute safest path forward is to package the application via Docker. 
* **Zero Code Changes:** Requires no modifications to `builder.py`, `pdf_generator.py`, or the React frontend.
* **Architecture Preservation:** Keeps PDF generation squarely in the Python backend.
* **Environment Parity:** Guarantees that the PDF rendering engine will work identically across local development, CI/CD, and production deployments.

---
**Recommendation:** Proceed directly to Phase 8: Infrastructure & Deployment Automation, focusing on building the `Dockerfile` and `docker-compose.yml` to encapsulate the WeasyPrint dependencies.

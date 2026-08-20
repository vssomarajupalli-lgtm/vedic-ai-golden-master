from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse, Response
from typing import Any
import traceback

from app.schemas.report import ReportGenerationRequest
from app.pipeline_runner import PipelineRunner
from app.reports.builder import ReportBuilder
from app.reports.html_generator import HTMLGenerator
from app.reports.pdf_generator import PDFGenerator
from app.reports.south_indian_chart_data import build_south_indian_chart_data
from app.core.logging import log

router = APIRouter()
pipeline = PipelineRunner()
report_builder = ReportBuilder()
html_generator = HTMLGenerator()
pdf_generator = PDFGenerator()

# Presentation-only section filter (GM-017.6).
# Maps Print & Export Framework section ids to the top-level report keys they
# require. Used solely to select which blocks the HTML/PDF document renders;
# the JSON report and all calculations are never filtered or altered.
SECTION_TO_REPORT_KEYS = {
    "horoscope-summary": ["client_profile", "executive_summary", "lifetime_intelligence"],
    "questions": ["question_responses"],
    "activation-timeline": ["lifetime_intelligence"],
    "gochara": ["gochara_report", "mandali_analysis", "mandali_gochar_report",
                "important_advisory", "upcoming_mandali_events", "current_mandali",
                "saturn_lifetime_cycles", "formula_verification",
                "south_indian_chart_data"],
    "appendix": ["formula_verification"],
}
# Keys always retained so the document shell never loses required layout data.
ALWAYS_KEEP_KEYS = {"metadata", "master_summary"}


def _filter_report_sections(report: dict, sections: list | None) -> dict:
    """
    Returns a copy of the report containing only the top-level keys required by
    the selected sections. With no sections (the default) the complete report is
    returned unchanged.
    """
    if not sections:
        return report
    allowed = set(ALWAYS_KEEP_KEYS)
    for section in sections:
        allowed.update(SECTION_TO_REPORT_KEYS.get(section, ()))
    return {key: value for key, value in report.items() if key in allowed}

@router.post("/generate-report")
def generate_report(
    request: ReportGenerationRequest,
    format: str = Query("json", description="Export format: json, html, pdf"),
    sections: list[str] | None = Query(None, description="Presentation-only sections to include (e.g. gochara, questions). Default: all sections."),
    report_type: str = Query("main", description="Report type: main (default) or question-companion (additive JSON data layer).")
) -> Any:
    """
    Stateless endpoint that accepts raw scraped JSON, runs the astrology engine,
    and formats the output via the ReportBuilder instead of returning raw arrays.
    """
    try:
        log.info(f"Generating report in format: {format}, report_type: {report_type}")
        
        # 1. Execute engine (Identical to process-chart)
        raw_data = request.canonical_content
        raw_data["_machine_index"] = request.machine_index
        outputs = pipeline.process(raw_data)

        # 1b. Question Engine companion (P1 - additive JSON data layer).
        # Opt-in via report_type=question-companion. Reuses the SAME pipeline
        # output and the same existing question_service/ReportBuilder code — no
        # new routing, formulas, or identity sources. HTML/PDF rendering is
        # intentionally not part of P1 (requests render a 501, not a degraded
        # document). The default main-report path below is untouched.
        if report_type == "question-companion":
            from app.reports.companion_builder import companion_builder
            if format.lower() != "json":
                raise HTTPException(
                    status_code=501,
                    detail="Question Engine companion is available in JSON only (HTML/PDF are scoped separately)."
                )
            return companion_builder.build(outputs, request.machine_index)
        
        # 2. Answer questions using the centralized service
        from app.services.question_service import question_service
        q_responses = []
        # Use provided question_ids or fallback to a default set
        question_ids_to_process = request.question_ids or ["10.1", "2.1", "7.1"]
        
        for q_id in question_ids_to_process:
            try:
                # The service expects the full pipeline output
                structured_answer = question_service.answer_structured_question(
                    question_id=q_id,
                    pipeline_output=outputs
                )
                q_responses.append(structured_answer)
            except Exception as e:
                log.warning(f"Failed to generate structured report for question {q_id}: {str(e)}")
        
        # 3. Build the final report structure
        report = report_builder.build_json_report(outputs, request.machine_index, questions=q_responses)
        
        # 3b. Attach the report-level South-Indian chart presentation snapshot.
        # Pure passthrough of already-existing canonical natal data (no astrology
        # calculation) so the HTML/PDF templates can render the three verified
        # South-Indian charts. The JSON report and all calculations are untouched.
        sic_data = build_south_indian_chart_data(request.canonical_content, report)
        if sic_data is not None:
            report["south_indian_chart_data"] = sic_data
        
        # 4. Handle export formats
        if format.lower() == "json":
            return report
        elif format.lower() == "html":
            html_content = html_generator.generate(_filter_report_sections(report, sections))
            return HTMLResponse(content=html_content)
        elif format.lower() == "pdf":
            try:
                pdf_bytes = pdf_generator.generate(_filter_report_sections(report, sections))
                return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=vedic_ai_report.pdf"})
            except RuntimeError as re:
                raise HTTPException(status_code=501, detail=str(re))
        else:
            raise HTTPException(status_code=400, detail="Invalid format requested. Supported: json, html, pdf.")
            
    except HTTPException:
        # Preserve intentional HTTP status codes (e.g. the 501 PDF-unavailable
        # signal) instead of collapsing them into a generic 500.
        raise
    except Exception as e:
        log.error(f"Error generating report: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Report Generation failed: {str(e)}")

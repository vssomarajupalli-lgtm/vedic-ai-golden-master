from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse, Response
from typing import Any, Optional, Dict
from datetime import datetime
import traceback

from app.schemas.chart import ChartProcessRequest
from app.pipeline_runner import PipelineRunner
from app.reports.builder import ReportBuilder
from app.reports.html_generator import HTMLGenerator
from app.reports.pdf_generator import PDFGenerator
from app.core.logging import log

router = APIRouter()
pipeline = PipelineRunner()
report_builder = ReportBuilder()
html_generator = HTMLGenerator()
pdf_generator = PDFGenerator()

@router.post("/generate-report")
def generate_report(
    request: ChartProcessRequest, 
    format: str = Query("json", description="Export format: json, html, pdf")
) -> Any:
    """
    Stateless endpoint that accepts raw scraped JSON, runs the astrology engine,
    and formats the output via the ReportBuilder instead of returning raw arrays.
    """
    try:
        log.info(f"Generating report in format: {format}")
        
        # 1. Execute engine (Identical to process-chart)
        raw_data = request.canonical_content
        raw_data["_machine_index"] = request.machine_index
        outputs = pipeline.process(raw_data)
        
        # 1.5. Execute Question Engine to generate structured opportunity windows
        from app.core.question_router import QuestionRouter
        from app.formulas.loader import FormulaRepositoryLoader
        from app.formulas.signal_translator import SignalTranslator
        from app.formulas.evaluator import FormulaEvaluator
        from app.formatters.display_formatter import DisplayFormatter
        
        router_instance = QuestionRouter()
        default_q_ids = ["10.1", "2.1", "7.1"]
        q_responses = []
        
        for q_id in default_q_ids:
            try:
                route_result = router_instance.route_question(q_id)
                f = FormulaRepositoryLoader().get_formula(route_result["formula_key"])
                domain = route_result["registry_record"]["domain_name"].lower()
                title = route_result["metadata"].get("question_name", "Astrological Query")
                
                engine_outputs_dict = outputs.get("engine_outputs", outputs)
                isolated_signals = SignalTranslator.translate(f.required_signals, engine_outputs_dict)
                eval_res = FormulaEvaluator.evaluate(f, engine_outputs_dict, isolated_signals)
                
                # Extract canonical target_date_utc written by process() — no clock dependency.
                _tdi = outputs.get("target_date_utc")
                _tdu = datetime.fromisoformat(_tdi) if _tdi else None
                
                fmt = DisplayFormatter.format_question_result(
                    question_title=title,
                    domain=domain,
                    natal_promise=engine_outputs_dict.get("natal_promise", {}),
                    dasha_activation=engine_outputs_dict.get("dashas", {}),
                    lifetime_projection=outputs.get("master_probability", {}).get("lifetime_projection", []),
                    final_state=eval_res.final_state,
                    isolated_signals=eval_res.isolated_signals,
                    client_metadata=request.machine_index.get("native_info", {}) if isinstance(request.machine_index, dict) else {},
                    target_date_utc=_tdu
                )
                q_responses.append(fmt.dict())
            except Exception as e:
                log.warning(f"Failed to generate structured report for {q_id}: {str(e)}")
        
        # 2. Extract into final schema
        report = report_builder.build_json_report(outputs, request.machine_index, questions=q_responses)
        
        # 3. Handle export formats
        if format.lower() == "json":
            return report
        elif format.lower() == "html":
            html_content = html_generator.generate(report)
            return HTMLResponse(content=html_content)
        elif format.lower() == "pdf":
            try:
                pdf_bytes = pdf_generator.generate(report)
                return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=vedic_ai_report.pdf"})
            except RuntimeError as re:
                raise HTTPException(status_code=501, detail=str(re))
        else:
            raise HTTPException(status_code=400, detail="Invalid format requested. Supported: json, html, pdf.")
            
    except Exception as e:
        log.error(f"Error generating report: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Report Generation failed: {str(e)}")

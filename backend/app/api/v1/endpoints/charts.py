from fastapi import APIRouter, HTTPException
from typing import Any, Optional
import traceback

from app.schemas.chart import ChartProcessRequest, ChartProcessResponse
from app.pipeline_runner import PipelineRunner
from app.core.logging import log

router = APIRouter()

# Instantiate the stateless frozen pipeline once
pipeline = PipelineRunner()

@router.post("/process-chart", response_model=ChartProcessResponse)
def process_chart(request: ChartProcessRequest) -> Any:
    """
    Stateless endpoint that accepts the raw scraped JSON from HoroscopeCleaner_Final
    and runs the entire deterministic Vedic-AI pipeline.
    """
    try:
        log.info("Processing new chart computation request.")
        
        # The pipeline expects the full request structure with canonical_content key
        raw_input = {
            "canonical_content": request.canonical_content,
            "canonical_json": request.canonical_content.get("canonical_json") if isinstance(request.canonical_content, dict) else None,
            "_machine_index": request.machine_index
        }
        
        # DEBUG: Log the consultation_date
        log.info(f"Consultation date in request: {request.canonical_content.get('raw_metadata', {}).get('consultation_date')}")
        
        # Execute the frozen astrological engine
        outputs = pipeline.process(raw_input)
        
        # Extract master synthesis block
        master_synth = outputs.get("master_probability", {})
        if not master_synth:
            raise ValueError("Pipeline did not produce master_probability block")
            
        yogas = outputs.get("engine_outputs", {}).get("yogas", {}).get("active_yogas", [])
        
        log.info(f"Chart processed successfully. Score: {master_synth.get('final_score')}")
        
        response_obj = ChartProcessResponse(
            final_score=master_synth.get("final_score", 0.0),
            probability_grade=master_synth.get("grade", "UNKNOWN"),
            breakdown=outputs,
            yogas=yogas,
            master_probability=master_synth,
            engine_outputs=outputs.get("engine_outputs", {}),
            target_date_utc=outputs.get("target_date_utc"),
            metadata=outputs.get("metadata")
        )
        return response_obj
        
    except Exception as e:
        log.error(f"Error during chart processing: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Astrological computation failed: {str(e)}"
        )

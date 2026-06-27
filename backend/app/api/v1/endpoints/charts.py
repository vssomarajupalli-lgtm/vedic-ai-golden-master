from fastapi import APIRouter, HTTPException
from typing import Any
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
    and runs the entire mathematical Vedic-AI pipeline.
    """
    try:
        log.info("Processing new chart computation request.")
        
        # Merge canonical content and machine index as expected by PipelineRunner
        raw_data = request.canonical_content
        raw_data["_machine_index"] = request.machine_index
        
        # Execute the frozen astrological engine
        outputs = pipeline.process(raw_data)
        
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
            yogas=yogas
        )
        print("API Response /process-chart Final Score:", response_obj.final_score)
        print("API Response /process-chart Yogas Count:", len(response_obj.yogas))
        print("====== DEBUG END ======")
        return response_obj
        
    except Exception as e:
        log.error(f"Error during chart processing: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Astrological computation failed: {str(e)}"
        )

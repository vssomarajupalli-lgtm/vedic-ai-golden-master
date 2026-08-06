from fastapi import APIRouter, HTTPException
from typing import Any
import traceback

from app.schemas.question import QuestionRequest, QuestionResponse
from app.pipeline_runner import PipelineRunner
from app.core.logging import log
from app.core.question_router import QuestionRouter
from app.core.preferences_manager import PreferencesManager

router = APIRouter()

# Instantiate the stateless modules
pipeline_runner = PipelineRunner()
question_router = QuestionRouter()
preferences_manager = PreferencesManager()

@router.post("/ask-question", response_model=QuestionResponse)
def ask_question(request: QuestionRequest) -> Any:
    """
    Stateless endpoint to answer an astrological question using an LLM,
    grounded by the deterministic math provided in the payload.
    """
    try:
        log.info("Processing question request...")
        
        # 1. Validation: Must have either text or ID
        if not request.question_text and not request.question_id:
            raise HTTPException(status_code=400, detail="Must provide either question_text or question_id")
        
        # Extract actual internal payload if wrapped inside a ChartProcessResponse
        # The question engine expects the full pipeline output structure
        internal_payload = request.engine_outputs
        if isinstance(internal_payload, dict) and "engine_outputs" in internal_payload:
            # Already has the full structure
            pass
        else:
            # Wrap in the expected pipeline output structure
            internal_payload = {
                "engine_outputs": internal_payload,
                "master_probability": request.master_probability,
                "metadata": request.metadata,
                "target_date_utc": request.target_date_utc
            }
        
        # Pass target_date_utc through to pipeline_runner (Single Source of Truth)
        if request.target_date_utc:
            internal_payload["target_date_utc"] = request.target_date_utc
        
        resolved_question_id = None
        question_text_to_process = request.question_text
        
        # 2. Question Router flow
        if request.question_id:
            route_result = question_router.route_question(request.question_id)
            if route_result["status"] == "error":
                # If error is a configuration error, 500, otherwise 422 for client errors
                status_code = 500 if route_result["error_type"] == "registry_configuration_error" else 422
                raise HTTPException(status_code=status_code, detail=route_result["message"])
                
            resolved_question_id = request.question_id
            metadata = route_result["metadata"]
            
            # Since the LLM still needs a natural language question text to base its answer on,
            # we inject the deterministic question_name if user left text blank
            if not question_text_to_process:
                question_text_to_process = metadata.get("question_name", "Astrological Query")
        
# 3. Use PipelineRunner as the orchestrator to answer the question
        # (Preserves legacy pipeline compatibility until phase 11D)
        
        # Contract enforcement: target_date_utc is required for deterministic execution
        if not internal_payload.get("target_date_utc"):
            raise HTTPException(
                status_code=422,
                detail="target_date_utc is required for ask-question. Pass the canonical target_date_utc returned by the Process Chart endpoint."
            )
        
        result = pipeline_runner.answer_question(
            question_or_id=question_text_to_process,
            pipeline_output=internal_payload
        )
        
        answer = result.get("answer_text", "")
        # Deterministic engine currently doesn't track used yogas in response
        used_yogas = []
        
        # 4. Auto-append to recents if valid question_id
        if resolved_question_id:
            try:
                preferences_manager.add_recent(resolved_question_id)
            except Exception as e:
                log.error(f"Failed to add question to recents: {str(e)}")
        
        log.info("Question answered successfully.")
        
        return QuestionResponse(
            answer_text=answer,
            referenced_yogas=used_yogas,
            resolved_question_id=resolved_question_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error during question generation: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Question Engine failed: {str(e)}"
        )

from app.schemas.question import StructuredQuestionResponse
from app.services.question_service import question_service

@router.post("/ask-structured-question", response_model=StructuredQuestionResponse)
def ask_structured_question(request: QuestionRequest) -> Any:
    """
    Stateless endpoint to answer an astrological question using the new Phase 14H.1 
    structured display format, bypassing LLM generation.
    """
    try:
        log.info("Processing structured question request...")
        
        if not request.question_id:
            raise HTTPException(status_code=400, detail="Must provide question_id for structured response")
            
        # The service expects the full pipeline output structure.
        # We need to reconstruct it from the QuestionRequest.
        pipeline_output = {
            "engine_outputs": request.engine_outputs,
            "master_probability": request.master_probability,
            "metadata": request.metadata,
            "target_date_utc": request.target_date_utc
        }
        
        formatted_result = question_service.answer_structured_question(
            question_id=request.question_id,
            pipeline_output=pipeline_output
        )
        
        try:
            preferences_manager.add_recent(request.question_id)
        except Exception as e:
            log.error(f"Failed to add question to recents: {str(e)}")
            
        return StructuredQuestionResponse(
            question_id=request.question_id,
            results=[formatted_result]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error during structured question generation: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Question Engine failed: {str(e)}"
        )

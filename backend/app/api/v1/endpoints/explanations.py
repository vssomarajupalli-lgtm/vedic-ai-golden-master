"""
GM-012D.5 — AI Explanation Generation API Endpoint

Endpoint for generating AI explanations based on deterministic pipeline outputs.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


router = APIRouter(prefix="/explanations", tags=["explanations"])


class ExplanationRequest(BaseModel):
    """Request to generate an AI explanation"""
    question_id: Optional[str] = Field(None, description="Question ID from Question Registry")
    question_text: Optional[str] = Field(None, description="Free-text question (used if question_id not provided)")
    pipeline_output: Optional[dict] = Field(None, description="Full pipeline output from /process-chart")
    target_date_utc: Optional[str] = Field(None, description="ISO8601 UTC timestamp for transit/dasha calculations")
    engine_outputs: Optional[dict] = Field(None, description="Pre-computed engine outputs (optional)")
    master_probability: Optional[dict] = Field(None, description="Master probability breakdown")
    metadata: Optional[dict] = Field(None, description="Additional metadata")


class ExplanationResponse(BaseModel):
    """AI-generated explanation response"""
    question: str
    domain: str
    routed: bool
    explanation: str
    citations: List[dict] = []
    evidence_summary: dict = {}
    confidence: str
    metadata: dict = {}
    processing_time_ms: int = 0


# Dependency to get the AI Explanation Service
async def get_ai_explanation_service():
    from app.services.ai_explanation_service import get_ai_explanation_service
    return get_ai_explanation_service()


@router.post("/generate", response_model=dict)
async def generate_explanation(
    request: ExplanationRequest,
    ai_service = Depends(get_ai_explanation_service),
) -> dict:
    """
    Generate an AI explanation for a question based on deterministic pipeline outputs.
    
    This endpoint:
    1. Builds a GroundingPackage from pipeline outputs
    2. Uses PromptBuilder to create a PromptPackage
    3. Invokes the configured AI provider
    4. Validates and returns the structured explanation
    
    Request body:
    {
        "question_id": "7.1",  // optional if question_text provided
        "question_text": "Will I get married?",  // optional if question_id provided
        "pipeline_output": {...},  // full pipeline output from /process-chart
        "target_date_utc": "2026-07-29T10:00:00Z"  // optional
    }
    """
    try:
        # Validate request
        if not request.question_id and not request.question_text:
            raise HTTPException(
                status_code=400,
                detail="Must provide either question_id or question_text"
            )
        
        if not request.pipeline_output:
            raise HTTPException(
                status_code=400,
                detail="pipeline_output is required"
            )
        
        # Generate explanation using the service
        result = await ai_service.generate_explanation(
            question_id=request.question_id,
            question_text=request.question_text,
            pipeline_output=request.pipeline_output,
            target_date_utc=request.target_date_utc,
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Explanation generation failed: {str(e)}"
        )


@router.get("/health", response_model=dict)
async def health_check(
    ai_service = Depends(get_ai_explanation_service),
) -> dict:
    """Health check for explanations endpoint"""
    try:
        health = await ai_service.health_check()
        return health
    except Exception as e:
        return {
            "status": "degraded",
            "endpoint": "/api/v1/explanations",
            "error": str(e)
        }
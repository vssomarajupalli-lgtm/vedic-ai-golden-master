from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class FormulaSchema(BaseModel):
    formula_key: str = Field(..., description="Unique string identifier (e.g., MAR_TIMING_001)")
    formula_name: str = Field(..., description="Human-readable name")
    formula_category: str = Field(..., description="High-level classification (e.g., Timing Assessment)")
    parent_formula_key: Optional[str] = Field(None, description="Key of the Base Family this variant inherits from")
    
    required_engines: List[str] = Field(default_factory=list, description="Engines that MUST execute for this formula")
    required_signals: List[str] = Field(default_factory=list, description="Specific astrological variables to be plucked from the engines")
    required_dasha_layers: List[str] = Field(default_factory=list, description="Depth of time-tracking required (e.g., Mahadasha)")
    required_vargas: List[str] = Field(default_factory=list, description="Divisional charts required for synthesis")
    required_confidence_layers: List[str] = Field(default_factory=list, description="Checklist of astrological conditions to evaluate")
    
    future_gochara_required: bool = Field(default=False, description="Flag for Moon-centered Mandali (transit forecasting)")
    answer_template_key: str = Field(default="timing_assessment_v1", description="Pointer to the linguistic boundary for the Answer Composer")

class FormulaRegistry(BaseModel):
    formulas: List[FormulaSchema]

class FormulaEvaluationResult(BaseModel):
    final_state: str = Field(..., description="FAVORABLE, MIXED, or UNFAVORABLE")
    isolated_signals: Dict[str, Any] = Field(..., description="Minimized payload of only the requested signals")
    answer_template_key: str = Field(..., description="Template to use in the Answer Composer")
    system_warnings: List[str] = Field(default_factory=list, description="Warnings like engine degradation")
    factor_fulfillment: Dict[str, bool] = Field(default_factory=dict, description="Which factors were fulfilled")
    factor_weights: Dict[str, float] = Field(default_factory=dict, description="Calibrated weights per factor")
    fulfilled_layers: int = Field(default=0, description="Number of fulfilled confidence layers")
    total_layers: int = Field(default=0, description="Total confidence layers")
    promise_score: float = Field(default=50.0, description="Natal promise score for the domain")

class ComposerPromptPackage(BaseModel):
    prompt_template_id: str = Field(..., description="The ID of the template loaded (e.g., timing_assessment_v1_favorable)")
    system_prompt: str = Field(..., description="The strict instructions for the LLM to format the response")
    user_prompt: Optional[str] = Field(None, description="Deferred to API layer")
    evidence_block: str = Field(..., description="Deterministically formatted string of astrological evidence")
    system_warnings: List[str] = Field(default_factory=list, description="Warnings to be strictly appended")
    final_state: str = Field(..., description="The final deterministic state")

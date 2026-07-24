from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class MatchStatus(str, Enum):
    MATCH = "MATCH"
    PARTIAL = "PARTIAL MATCH"
    MISMATCH = "MISMATCH"
    NA = "NOT APPLICABLE"

class ModuleResult(BaseModel):
    expected: Any = None
    actual: Any = None
    status: MatchStatus = MatchStatus.NA
    comments: str = ""

class ComparisonRecord(BaseModel):
    planet_strength: ModuleResult = Field(default_factory=ModuleResult)
    house_strength: ModuleResult = Field(default_factory=ModuleResult)
    varga: ModuleResult = Field(default_factory=ModuleResult)
    ashtakavarga: ModuleResult = Field(default_factory=ModuleResult)
    functional_nature: ModuleResult = Field(default_factory=ModuleResult)
    yogas: ModuleResult = Field(default_factory=ModuleResult)
    dasha: ModuleResult = Field(default_factory=ModuleResult)
    gochara: ModuleResult = Field(default_factory=ModuleResult)
    mandali: ModuleResult = Field(default_factory=ModuleResult)
    natal_promise: ModuleResult = Field(default_factory=ModuleResult)
    master_probability: ModuleResult = Field(default_factory=ModuleResult)
    question_engine: ModuleResult = Field(default_factory=ModuleResult)

class ValidationCase(BaseModel):
    case_id: str
    native_name: str
    birth_details: Dict[str, str] = Field(default_factory=dict)
    canonical_json_path: str
    validation_status: str = "PENDING"
    validation_date: Optional[str] = None
    reviewer: str = ""
    notes: str = ""
    expected_results: Dict[str, Any] = Field(default_factory=dict)
    actual_engine_results: Dict[str, Any] = Field(default_factory=dict)
    comparison: ComparisonRecord = Field(default_factory=ComparisonRecord)
    calibration_notes: str = ""
    reviewer_notes: str = ""
    final_decision: str = ""

class AccuracyMetrics(BaseModel):
    total_matches: int = 0
    total_partial: int = 0
    total_mismatches: int = 0
    total_applicable: int = 0
    planet_strength_accuracy: float = 0.0
    house_strength_accuracy: float = 0.0
    yoga_accuracy: float = 0.0
    question_accuracy: float = 0.0
    master_probability_accuracy: float = 0.0
    overall_accuracy: float = 0.0

class RegressionAnalysis(BaseModel):
    improved_cases: List[str] = Field(default_factory=list)
    unchanged_cases: List[str] = Field(default_factory=list)
    regressed_cases: List[str] = Field(default_factory=list)

class CalibrationRecommendation(BaseModel):
    parameter_name: str
    old_value: Any
    new_value: Any
    reason: str
    supporting_cases: List[str] = Field(default_factory=list)
    regression_check: RegressionAnalysis = Field(default_factory=RegressionAnalysis)
    approval_status: str = "PENDING"

class CalibrationHistoryRecord(BaseModel):
    calibration_version: str
    date: str
    parameter: str
    old_value: Any
    new_value: Any
    reason: str
    affected_cases: List[str] = Field(default_factory=list)
    approval: str
    rollback_information: str = ""

class ValidationWorkspaceData(BaseModel):
    cases: Dict[str, ValidationCase] = Field(default_factory=dict)
    recommendations: List[CalibrationRecommendation] = Field(default_factory=list)
    history: List[CalibrationHistoryRecord] = Field(default_factory=list)

"""
Calibration Schema — Pydantic models for calibration profile validation.

This module provides validation schemas for the calibration profile system.
Supports business-oriented grouping with full parameter metadata.
"""

from typing import Any, Dict, List, Optional, ClassVar
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from enum import Enum


class ParameterStatus(str, Enum):
    """Parameter protection status."""
    PROTECTED = "protected"      # Repository default - cannot be deleted
    CUSTOM = "custom"            # User-added - can be deleted


class ParameterSchema(BaseModel):
    """Single calibration parameter with full metadata."""
    name: str
    description: str = ""
    purpose: str = ""
    default_value: Any
    current_value: Any
    recommended_range: Optional[List[Any]] = None
    editable: bool = True
    protected: bool = False
    weight_pct: Optional[float] = None  # For section weight validation

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Parameter name cannot be empty")
        return v.strip()


class AdditionalFactorSchema(BaseModel):
    """Additional factor slot for Version 2 enhancements."""
    name: str = ""
    description: str = ""
    weight_pct: float = 0.0
    editable: bool = True
    removable: bool = True


class FormulaFactorSchema(BaseModel):
    """Single formula factor with full metadata."""
    name: str
    description: str = ""
    purpose: str = ""
    default_value: float = 0.0
    current_value: float = 0.0
    recommended_range: Optional[List[float]] = None
    editable: bool = True
    protected: bool = True
    weight_pct: float = 0.0
    enabled: bool = True
    engine_required: str = ""

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Factor name cannot be empty")
        return v.strip()


class FormulaCalibrationSection(BaseModel):
    """Calibration section for a single formula."""
    formula_key: str
    formula_name: str = ""
    description: str = ""
    total_weight_pct: float = 100.0
    enabled: bool = True
    factors: Dict[str, FormulaFactorSchema] = Field(default_factory=dict)


class SectionSchema(BaseModel):
    """Calibration section with business-oriented grouping."""
    name: str
    description: str = ""
    total_weight_pct: float = 100.0
    parameters: Dict[str, ParameterSchema] = Field(default_factory=dict)
    additional_factor_1: Optional[AdditionalFactorSchema] = None
    additional_factor_2: Optional[AdditionalFactorSchema] = None

    model_config = ConfigDict(extra='allow')

    @field_validator('total_weight_pct')
    @classmethod
    def validate_weight(cls, v: float) -> float:
        if v < 0 or v > 100:
            raise ValueError("Section weight must be between 0 and 100")
        return v

    @model_validator(mode='after')
    def validate_section_weights(self) -> 'SectionSchema':
        """Ensure section weights sum to 100% (approximately)."""
        # This is validated at profile level
        return self


class ProfileMetadata(BaseModel):
    """Profile metadata."""
    profile_id: str
    version: str = "1.0.0"
    status: str = "ACTIVE"
    based_on: Optional[str] = None
    last_modified: Optional[str] = None
    modified_by: Optional[str] = None
    validation_horoscopes_completed: int = 0


class ProfileSnapshot(BaseModel):
    """Calibration history snapshot."""
    snapshot_id: str
    timestamp: str
    horoscope_id: str
    reason: str
    changes_made: List[Dict[str, Any]] = Field(default_factory=list)
    validation_score: Optional[float] = None
    engineer: str = ""


class CalibrationProfile(BaseModel):
    """Complete calibration profile with business-oriented sections."""
    metadata: ProfileMetadata
    sections: Dict[str, SectionSchema] = Field(default_factory=dict)
    formula_calibration: Dict[str, FormulaCalibrationSection] = Field(default_factory=dict)
    history: List[ProfileSnapshot] = Field(default_factory=list)

    # Required sections for v1.0
    REQUIRED_SECTIONS: ClassVar[List[str]] = [
        "planet_strength",
        "house_strength",
        "rasi_strength",
        "natal_promise",
        "probability",
        "dasha",
        "question_engine",
        "transit",
        "ashtakavarga"
    ]

    @model_validator(mode='after')
    def validate_profile(self) -> 'CalibrationProfile':
        """Validate complete profile."""
        # Check if this is a legacy format profile (flat keys without sections)
        # If sections exist and have content, validate normally
        if self.sections and any(self.sections.values()):
            # Check required sections exist
            missing = [s for s in self.REQUIRED_SECTIONS if s not in self.sections]
            if missing:
                raise ValueError(f"Missing required sections: {missing}")

            # Validate each section weights sum to ~100%
            for section_name, section in self.sections.items():
                param_weights = [p.weight_pct for p in section.parameters.values() if p.weight_pct is not None]
                if param_weights and abs(sum(param_weights) - 100.0) > 0.01:
                    raise ValueError(f"Section '{section_name}' parameter weights sum to {sum(param_weights)}%, expected 100%")

            # Check for duplicate parameter names within each section
            for section_name, section in self.sections.items():
                param_names = list(section.parameters.keys())
                if len(param_names) != len(set(param_names)):
                    raise ValueError(f"Duplicate parameter names found in section '{section_name}'")

        # Validate formula_calibration if present
        if self.formula_calibration:
            for formula_key, formula_section in self.formula_calibration.items():
                if formula_section.factors:
                    factor_weights = [f.weight_pct for f in formula_section.factors.values() if f.weight_pct is not None and f.enabled]
                    if factor_weights and abs(sum(factor_weights) - 100.0) > 0.01:
                        raise ValueError(f"Formula '{formula_key}' enabled factor weights sum to {sum(factor_weights)}%, expected 100%")

                    # Check for duplicate factor names
                    factor_names = list(formula_section.factors.keys())
                    if len(factor_names) != len(set(factor_names)):
                        raise ValueError(f"Duplicate factor names found in formula '{formula_key}'")

                    # Validate engine_required engines exist (basic check - just ensure not empty string)
                    for factor_name, factor in formula_section.factors.items():
                        if factor.engine_required and not factor.engine_required.strip():
                            raise ValueError(f"Formula '{formula_key}' factor '{factor_name}' has empty engine_required")

        return self

    def get_section_weight_total(self) -> float:
        """Get total weight of all sections (should be ~100%)."""
        return sum(s.total_weight_pct for s in self.sections.values())

    def is_ready_for_prediction(self) -> bool:
        """Check if profile is valid and ready for prediction."""
        try:
            self.validate_profile()
            return True
        except ValueError:
            return False


class ValidationResult(BaseModel):
    """Result of profile validation."""
    valid: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    profile_status: str = "INVALID"
    section_status: Dict[str, str] = Field(default_factory=dict)
    current_total: float = 0.0
    protected_factors: int = 0
    custom_factors: int = 0
    ready_for_prediction: bool = False


# JSON Schema generation for override files
def generate_calibration_schema() -> Dict[str, Any]:
    """Generate JSON Schema for calibration profile validation."""
    return CalibrationProfile.model_json_schema()


def generate_override_schema() -> Dict[str, Any]:
    """Generate JSON Schema for override files."""
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "title": "Calibration Override Schema",
        "properties": {
            "metadata": {
                "type": "object",
                "properties": {
                    "base_profile": {"type": "string", "const": "v1.0_default"},
                    "created": {"type": "string", "format": "date-time"},
                    "author": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["base_profile"]
            },
            "overrides": {
                "type": "object",
                "patternProperties": {
                    "^[a-z_]+\\.(.+)$": {
                        "type": "object",
                        "properties": {
                            "value": {},
                            "description": {"type": "string"},
                            "timestamp": {"type": "string", "format": "date-time"}
                        },
                        "required": ["value"]
                    }
                }
            }
        },
        "required": ["metadata", "overrides"]
    }
    return schema
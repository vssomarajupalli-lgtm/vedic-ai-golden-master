"""
Calibration Manager — Single unified calibration interface for Golden Master v1.0.

This module provides the single calibration subsystem for the single-user desktop application.
Combines data layer (profile loading/validation) and control plane (editing/validation/history).

Design Principles:
- Single class, single responsibility per method
- Zero enterprise features (no locking, no hot reload, no events, no concurrency)
- Backward compatible with existing engine property accessors
- Safe failure: never crashes, auto-restores previous valid profile
- Single-user desktop: no locking, no events, no hot reload
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from copy import deepcopy

from .calibration_registry import CalibrationRegistry
from .calibration_types import CalibrationProfile
from .calibration_schema import (
    CalibrationProfile as SchemaCalibrationProfile,
    ValidationResult,
    CalibrationProfile as ProfileSchema,
    SectionSchema,
    ParameterSchema,
    AdditionalFactorSchema,
    ProfileMetadata,
    ProfileSnapshot,
    FormulaFactorSchema,
    FormulaCalibrationSection,
    generate_override_schema,
)


class ValidationResult:
    """Result of a validation operation."""
    def __init__(self, success: bool, data: Any = None, errors: List[str] = None, warnings: List[str] = None):
        self.success = success
        self.data = data
        self.errors = errors or []
        self.warnings = warnings or []

    @classmethod
    def ok(cls, data: Any = None, warnings: List[str] = None):
        return cls(True, data, [], warnings or [])

    @classmethod
    def fail(cls, errors: List[str], warnings: List[str] = None):
        return cls(False, None, errors, warnings or [])


class CalibrationManager:
    """
    Single calibration interface: data layer + control plane.

    Combines:
    - Profile loading & validation (data layer)
    - Parameter editing & management (control plane)
    - Profile history & factory reset (management)

    No enterprise features: no locking, no hot reload, no events, no concurrency.
    """

    # Required sections for v1.0
    REQUIRED_SECTIONS = [
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

    def __init__(self, profile_id: str = "v1.0_current", registry: CalibrationRegistry = None):
        self.registry = registry or CalibrationRegistry()
        self.profile_dir = Path(__file__).parent / "profiles"
        self.history_dir = Path(__file__).parent / "calibration_history"

        # Load and validate profile
        self._last_valid_profile = None
        self.active_profile = self._load_and_validate_profile(profile_id)
        self.profile_id = profile_id

    # =====================================================================
    # PROFILE LOADING & VALIDATION (Data Layer)
    # =====================================================================

    def _load_and_validate_profile(self, profile_id: str) -> Dict[str, Any]:
        """Load profile with validation and safe fallback."""
        try:
            profile_path = self.profile_dir / f"{profile_id}.json"
            if not profile_path.exists():
                # Fallback to default if current doesn't exist
                if profile_id == "v1.0_current":
                    profile_path = self.profile_dir / "v1.0_default.json"
                else:
                    raise FileNotFoundError(f"Profile not found: {profile_id}")

            with open(profile_path, 'r', encoding='utf-8') as f:
                raw_profile = json.load(f)

            # For legacy profiles (v1.0.0_base), skip validation and return raw profile
            # Legacy profiles have flat format without 'sections' key
            if "sections" not in raw_profile:
                return raw_profile

            # Validate against schema
            validated = self._validate_profile_dict(raw_profile)

            # Store as last valid for fallback
            self._last_valid_profile = deepcopy(validated)
            return validated

        except Exception as e:
            # Safe fallback: restore last valid profile
            if self._last_valid_profile:
                print(f"[CalibrationManager] Profile load failed, restoring last valid: {e}")
                return deepcopy(self._last_valid_profile)
            # Ultimate fallback: load default
            print(f"[CalibrationManager] Loading factory default: {e}")
            return self._load_factory_default()

    def _load_factory_default(self) -> Dict[str, Any]:
        """Load the immutable factory default profile."""
        default_path = self.profile_dir / "v1.0_default.json"
        with open(default_path, 'r', encoding='utf-8') as f:
            raw = json.load(f)
        validated = self._validate_profile_dict(raw)
        self._last_valid_profile = deepcopy(validated)
        return validated

    def _validate_profile_dict(self, profile_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Validate profile dictionary against schema."""
        try:
            # Use Pydantic schema for validation
            profile = SchemaCalibrationProfile.model_validate(profile_dict)
            return profile.model_dump()
        except Exception as e:
            raise ValueError(f"Profile validation failed: {e}")

    def _ensure_current_profile(self) -> None:
        """Ensure v1.0_current.json exists (copy from default if needed)."""
        current_path = self.profile_dir / "v1.0_current.json"
        if not current_path.exists():
            default_path = self.profile_dir / "v1.0_default.json"
            shutil.copy2(default_path, current_path)

    # =====================================================================
    # ENGINE READ API (Backward Compatible - Zero Breaking Changes)
    # =====================================================================

    def _extract_section_values(self, section_name: str) -> Dict[str, Any]:
        """Extract current_values from a section's parameters.

        Handles both new sections format and legacy flat format.
        """
        # Try new sections format first
        section = self.active_profile.get("sections", {}).get(section_name, {})
        params = section.get("parameters", {})
        if params:
            result = {}
            for k, v in params.items():
                if isinstance(v, dict) and "current_value" in v:
                    result[k] = v.get("current_value", v.get("default_value"))
                else:
                    result[k] = v
            return result

        # Fallback to legacy flat format
        legacy_data = self.active_profile.get(section_name, {})
        return legacy_data

    def _get_specialized_property(self, section_name: str, mapping: Dict[str, str],
                                   special_handlers: Dict[str, callable] = None) -> Dict[str, Any]:
        """Extract specialized property with UPPER_CASE key mapping for engines.

        Handles both new sections format and legacy flat format.
        """
        # Try new sections format first
        section = self.active_profile.get("sections", {}).get(section_name, {})
        params = section.get("parameters", {})
        if params:
            result = {}
            for k, v in params.items():
                if isinstance(v, dict) and "current_value" in v:
                    val = v.get("current_value", v.get("default_value"))
                    engine_key = mapping.get(k, k.upper())
                    # Apply special handlers if provided
                    if special_handlers and k in special_handlers:
                        val = special_handlers[k](val)
                    result[engine_key] = val
            return result

        # Fallback to legacy flat format
        legacy_data = self.active_profile.get(section_name, {})
        # Apply mapping to legacy keys
        result = {}
        for k, v in legacy_data.items():
            engine_key = mapping.get(k, k.upper())
            result[engine_key] = v
        return result

    @property
    def ashtakavarga(self) -> Dict[str, Any]:
        """Return ashtakavarga calibration values in engine-expected format (UPPER_CASE keys).

        Handles both new sections format and legacy flat format.
        """
        # Try new sections format first
        section = self.active_profile.get("sections", {}).get("ashtakavarga", {})
        params = section.get("parameters", {})
        if params:
            mapping = {
                "bav_grade_thresholds": "BAV_GRADE_THRESHOLDS",
                "planet_modifier": "BAV_PLANET_MODIFIER",
                "sav_thresholds": "SAV_BINDU_SCALE",  # engine expects SAV_BINDU_SCALE
                "dasha_bav_confidence": "DASHA_BAV_CONFIDENCE",
                "dasha_bav_weights": "DASHA_BAV_WEIGHTS",
                "excluded_planets": "BAV_EXCLUDED_PLANETS",
                "bav_planets": "BAV_PLANETS",
            }
            params = section.get("parameters", {})
            result = {}
            for k, v in params.items():
                if isinstance(v, dict) and "current_value" in v:
                    val = v.get("current_value", v.get("default_value"))
                    # Map to engine-expected key
                    engine_key = mapping.get(k, k.upper())
                    result[engine_key] = val
                # Handle SAV thresholds separately (they're nested)
                if k == "sav_thresholds" and isinstance(v, dict) and "current_value" in v:
                    sav_val = v.get("current_value", v.get("default_value"))
                    result["SAV_FAVORABLE_THRESHOLD"] = sav_val.get("favorable", 28)
                    result["SAV_STRONG_THRESHOLD"] = sav_val.get("strong", 30)
                    result["SAV_WEAK_THRESHOLD"] = sav_val.get("weak", 22)
                    # Also create SAV_BINDU_SCALE for engine compatibility
                    result["SAV_BINDU_SCALE"] = [
                        (0, 0),
                        (sav_val.get("favorable", 28), 30),
                        (sav_val.get("strong", 30), 50),
                        (30, 70),  # default middle anchors
                        (35, 85),
                        (40, 100),
                        (56, 100)
                    ]
            # Add classical constants that are always needed
            from app.config.astrology_constants import BAV_EXCLUDED_PLANETS, BAV_PLANETS
            result["BAV_EXCLUDED_PLANETS"] = list(BAV_EXCLUDED_PLANETS)
            result["BAV_PLANETS"] = list(BAV_PLANETS)
            # Convert BAV_GRADE_THRESHOLDS from dict {grade: threshold} to list of tuples [(threshold, grade), ...]
            if "BAV_GRADE_THRESHOLDS" in result and isinstance(result["BAV_GRADE_THRESHOLDS"], dict):
                # Sort by threshold descending (EXCELLENT=7, STRONG=6, etc.)
                grade_map = result["BAV_GRADE_THRESHOLDS"]
                result["BAV_GRADE_THRESHOLDS"] = [(v, k) for k, v in sorted(grade_map.items(), key=lambda x: -x[1])]
            return result

        # Fallback to legacy flat format
        legacy_data = self.active_profile.get("ashtakavarga", {})
        if legacy_data:
            # Legacy already has UPPER_CASE keys
            result = dict(legacy_data)
            # Ensure required keys exist
            from app.config.astrology_constants import BAV_EXCLUDED_PLANETS, BAV_PLANETS
            if "BAV_EXCLUDED_PLANETS" not in result:
                result["BAV_EXCLUDED_PLANETS"] = list(BAV_EXCLUDED_PLANETS)
            if "BAV_PLANETS" not in result:
                result["BAV_PLANETS"] = list(BAV_PLANETS)
            # Create SAV_BINDU_SCALE from individual thresholds for engine compatibility
            if "SAV_BINDU_SCALE" not in result:
                favorable = result.get("SAV_FAVORABLE_THRESHOLD", 28)
                strong = result.get("SAV_STRONG_THRESHOLD", 30)
                weak = result.get("SAV_WEAK_THRESHOLD", 22)
                result["SAV_BINDU_SCALE"] = [
                    (0, 0),
                    (favorable, 30),
                    (strong, 50),
                    (30, 70),  # default middle anchors
                    (35, 85),
                    (40, 100),
                    (56, 100)
                ]
            return result

        # Ultimate fallback
        from app.config.astrology_constants import BAV_EXCLUDED_PLANETS, BAV_PLANETS
        return {
            "BAV_EXCLUDED_PLANETS": list(BAV_EXCLUDED_PLANETS),
            "BAV_PLANETS": list(BAV_PLANETS),
        }

    @property
    def transit(self) -> Dict[str, Any]:
        """Return transit calibration values in engine-expected format (UPPER_CASE keys).

        Handles both new sections format and legacy flat format.
        """
        # Try new sections format first
        section = self.active_profile.get("sections", {}).get("transit", {})
        params = section.get("parameters", {})
        if params:
            mapping = {
                "weights": "TRANSIT_WEIGHTS",
                "house_quality": "TRANSIT_HOUSE_QUALITY",
                "conjunction_matrix": "TRANSIT_CONJUNCTION_MATRIX",
                "aspect_weights": "TRANSIT_ASPECT_WEIGHTS",
                "special_aspects": "TRANSIT_SPECIAL_ASPECTS",
                "special_aspect_weight": "TRANSIT_SPECIAL_ASPECT_WEIGHT",
                "vedha_pairs": "VEDHA_PAIRS",
                "vedha_cap": "TRANSIT_VEDHA_CAP",
                "dasha_sync_bonuses": "TRANSIT_DASHA_SYNC_BONUSES",
            }
            params = section.get("parameters", {})
            result = {}
            for k, v in params.items():
                if isinstance(v, dict) and "current_value" in v:
                    val = v.get("current_value", v.get("default_value"))
                    # Map to engine-expected key
                    engine_key = mapping.get(k, k.upper())
                    # Convert string keys to integers for house quality maps
                    if engine_key == "TRANSIT_HOUSE_QUALITY" and isinstance(val, dict):
                        converted = {}
                        for planet, houses in val.items():
                            if isinstance(houses, dict):
                                converted[planet] = {int(h): q for h, q in houses.items()}
                            else:
                                converted[planet] = houses
                        val = converted
                    # Convert VEDHA_PAIRS string keys to integers
                    if engine_key == "VEDHA_PAIRS" and isinstance(val, dict):
                        val = {int(h): v for h, v in val.items()}
                    result[engine_key] = val
            return result

        # Fallback to legacy flat format
        legacy_data = self.active_profile.get("transit", {})
        mapping = {
            "weights": "TRANSIT_WEIGHTS",
            "house_quality": "TRANSIT_HOUSE_QUALITY",
            "conjunction_matrix": "TRANSIT_CONJUNCTION_MATRIX",
            "aspect_weights": "TRANSIT_ASPECT_WEIGHTS",
            "special_aspects": "TRANSIT_SPECIAL_ASPECTS",
            "special_aspect_weight": "TRANSIT_SPECIAL_ASPECT_WEIGHT",
            "vedha_pairs": "VEDHA_PAIRS",
            "vedha_cap": "TRANSIT_VEDHA_CAP",
            "dasha_sync_bonuses": "TRANSIT_DASHA_SYNC_BONUSES",
        }
        result = {}
        for k, v in legacy_data.items():
            engine_key = mapping.get(k, k.upper())
            val = legacy_data[k]
            if engine_key == "TRANSIT_HOUSE_QUALITY" and isinstance(val, dict):
                converted = {}
                for planet, houses in val.items():
                    if isinstance(houses, dict):
                        converted[planet] = {int(h): q for h, q in houses.items()}
                    else:
                        converted[planet] = houses
                    val = converted
            if engine_key == "VEDHA_PAIRS" and isinstance(val, dict):
                val = {int(h): v for h, v in val.items()}
            result[engine_key] = val
        return result

    @property
    def question_engine(self) -> Dict[str, Any]:
        return self._extract_section_values("question_engine")

    @property
    def planet_strength(self) -> Dict[str, Any]:
        """Return planet strength calibration in engine-expected format (PLANET_SCORING_MATRIX).

        Handles both new sections format and legacy flat format.
        """
        # Try new sections format first - return dict with PLANET_SCORING_MATRIX from constants
        try:
            from app.config.astrology_constants import PLANET_SCORING_MATRIX, NATURAL_BENEFICS, NATURAL_MALEFICS
            return {
                "PLANET_SCORING_MATRIX": PLANET_SCORING_MATRIX,
                "NATURAL_BENEFICS": NATURAL_BENEFICS,
                "NATURAL_MALEFICS": NATURAL_MALEFICS
            }
        except ImportError:
            pass

        # Fallback to legacy flat format
        legacy_data = self.active_profile.get("planet_strength", {})
        return legacy_data

    @property
    def house_strength(self) -> Dict[str, Any]:
        """Return house strength calibration in engine-expected format (HOUSE_SCORING_MATRIX).

        Handles both new sections format and legacy flat format.
        """
        # Try new sections format first - return dict with HOUSE_SCORING_MATRIX from constants
        try:
            from app.config.astrology_constants import HOUSE_SCORING_MATRIX
            return {
                "HOUSE_SCORING_MATRIX": HOUSE_SCORING_MATRIX
            }
        except ImportError:
            pass

        # Fallback to legacy flat format
        legacy_data = self.active_profile.get("house_strength", {})
        return legacy_data

    @property
    def rasi_strength(self) -> Dict[str, Any]:
        """Return rasi strength calibration section in engine-expected format."""
        rasi_cal = self.active_profile.get("sections", {}).get("rasi_strength", {})
        # Return the full rasi_strength section so engines can extract RASI_SCORING_MATRIX
        return rasi_cal

    @property
    def varga(self) -> Dict[str, Any]:
        return self._extract_section_values("varga")

    @property
    def dasha(self) -> Dict[str, Any]:
        return self._extract_section_values("dasha")

    @property
    def master_probability(self) -> Dict[str, Any]:
        return self._extract_section_values("probability")

    @property
    def natal_promise(self) -> Dict[str, Any]:
        return self._extract_section_values("natal_promise")

    @property
    def formula_calibration(self) -> Dict[str, Any]:
        """Return formula calibration in engine-expected format."""
        formula_cal = self.active_profile.get("formula_calibration", {})
        result = {}
        for formula_key, formula_section in formula_cal.items():
            if not formula_section.get("enabled", True):
                continue
            factors = formula_section.get("factors", {})
            result[formula_key] = {
                "enabled": formula_section.get("enabled", True),
                "total_weight_pct": formula_section.get("total_weight_pct", 100.0),
                "factors": {}
            }
            # Only include enabled factors, normalize weights
            enabled_factors = {k: v for k, v in factors.items() if v.get("enabled", True)}
            if enabled_factors:
                total_weight = sum(f.get("weight_pct", 0) for f in enabled_factors.values())
                if total_weight > 0:
                    for fname, fdata in enabled_factors.items():
                        weight = fdata.get("weight_pct", 0)
                        normalized_weight = (weight / total_weight) * 100 if total_weight != 100 else weight
                        result[formula_key]["factors"][fname] = {
                            "weight": normalized_weight,
                            "enabled": True,
                            "engine_required": fdata.get("engine_required", ""),
                            "description": fdata.get("description", ""),
                            "purpose": fdata.get("purpose", "")
                        }
        return result

    # =====================================================================
    # CONTROL PLANE: PARAMETER INSPECTION
    # =====================================================================

    def get_value(self, path: str) -> ValidationResult:
        """
        Get parameter with full metadata.

        Path format: "section.parameter" or "section.additional_factor_1"
        Returns: ValidationResult with {value, description, purpose, recommended_range,
             default_value, current_value, editable, protected}
        """
        try:
            parts = path.split('.')
            if len(parts) != 2:
                return ValidationResult.fail([f"Invalid path format: {path}. Use 'section.parameter'"])

            section_name, param_name = parts
            sections = self.active_profile.get("sections", {})

            if section_name not in sections:
                return ValidationResult.fail([f"Section not found: {section_name}"])

            section = sections[section_name]

            # Check parameters
            if param_name in section.get("parameters", {}):
                param = section["parameters"][param_name]
                return ValidationResult.ok({
                    "path": path,
                    "name": param.get("name", param_name),
                    "description": param.get("description", ""),
                    "purpose": param.get("purpose", ""),
                    "recommended_range": param.get("recommended_range"),
                    "default_value": param.get("default_value"),
                    "current_value": param.get("current_value"),
                    "editable": param.get("editable", True),
                    "protected": param.get("protected", False),
                    "weight_pct": param.get("weight_pct"),
                })

            # Check additional factors
            if param_name in ("additional_factor_1", "additional_factor_2"):
                factor = section.get(param_name)
                if factor:
                    return ValidationResult.ok({
                        "path": path,
                        "name": factor.get("name", ""),
                        "description": factor.get("description", ""),
                        "weight_pct": factor.get("weight_pct", 0.0),
                        "editable": factor.get("editable", True),
                        "protected": False,
                    })
                return ValidationResult.ok({
                    "path": path,
                    "name": "",
                    "description": factor.get("description", "") if factor else "",
                    "weight_pct": 0.0,
                    "editable": True,
                    "protected": False,
                })

            return ValidationResult.fail([f"Parameter not found: {path}"])

        except Exception as e:
            return ValidationResult.fail([f"Error getting value: {e}"])

    def get_section(self, section_name: str) -> ValidationResult:
        """Get entire section with all parameters."""
        try:
            sections = self.active_profile.get("sections", {})
            if section_name not in sections:
                return ValidationResult.fail([f"Section not found: {section_name}"])
            return ValidationResult.ok(sections[section_name])
        except Exception as e:
            return ValidationResult.fail([f"Error getting section: {e}"])

    def get_all_sections(self) -> ValidationResult:
        """Get all sections summary."""
        try:
            sections = self.active_profile.get("sections", {})
            summary = {}
            for name, section in sections.items():
                param_count = len(section.get("parameters", {}))
                additional_factors = sum(1 for f in ["additional_factor_1", "additional_factor_2"] if section.get(f))
                summary[name] = {
                    "description": section.get("description", ""),
                    "total_weight_pct": section.get("total_weight_pct", 100.0),
                    "parameter_count": param_count,
                    "additional_factors": additional_factors,
                    "protected_factors": sum(1 for p in section.get("parameters", {}).values() if p.get("protected", False)),
                    "custom_factors": sum(1 for p in section.get("parameters", {}).values() if not p.get("protected", False)),
                }
            return ValidationResult.ok(summary)
        except Exception as e:
            return ValidationResult.fail([f"Error getting sections: {e}"])

    # =====================================================================
    # CONTROL PLANE: PARAMETER EDITING
    # =====================================================================

    def _validate_section_weights(self, section_name: str) -> ValidationResult:
        """Validate that section parameter weights sum to 100%."""
        try:
            sections = self.active_profile.get("sections", {})
            if section_name not in sections:
                return ValidationResult.fail([f"Section not found: {section_name}"])

            section = sections[section_name]
            params = section.get("parameters", {})

            total = sum(p.get("weight_pct", 0) for p in params.values() if p.get("weight_pct") is not None)

            if abs(total - 100.0) > 0.01:
                return ValidationResult.fail([f"Section '{section_name}' weights sum to {total}%, expected 100%"])

            return ValidationResult.ok({"total_weight": total})
        except Exception as e:
            return ValidationResult.fail([f"Error validating section weights: {e}"])

    def _validate_full_profile(self) -> ValidationResult:
        """Validate entire profile using schema."""
        try:
            SchemaCalibrationProfile.model_validate(self.active_profile)
            return ValidationResult.ok({"validated": True})
        except Exception as e:
            return ValidationResult.fail([f"Profile validation failed: {e}"])

    def modify_weight(self, section_name: str, param_name: str, new_weight: float) -> ValidationResult:
        """Modify parameter weight within a section."""
        try:
            if not (0 <= new_weight <= 100):
                return ValidationResult.fail(["Weight must be between 0 and 100"])

            sections = self.active_profile.get("sections", {})
            if section_name not in sections:
                return ValidationResult.fail([f"Section not found: {section_name}"])

            section = sections[section_name]
            if param_name not in section.get("parameters", {}):
                return ValidationResult.fail([f"Parameter not found: {param_name}"])

            param = section["parameters"][param_name]
            if not param.get("editable", True):
                return ValidationResult.fail([f"Parameter is not editable: {param_name}"])

            if "weight_pct" not in param or param["weight_pct"] is None:
                return ValidationResult.fail([f"Parameter has no weight: {param_name}"])

            old_weight = param.get("weight_pct", 0)
            param["weight_pct"] = new_weight
            param["current_value"] = new_weight

            # Validate section weights still sum to 100%
            validation = self._validate_section_weights(section_name)
            if not validation.success:
                # Rollback
                param["weight_pct"] = old_weight
                param["current_value"] = old_weight
                return validation

            return ValidationResult.ok({"old_weight": old_weight, "new_weight": new_weight})

        except Exception as e:
            return ValidationResult.fail([f"Error modifying weight: {e}"])

    def modify_percentage(self, section_name: str, param_name: str, new_pct: float) -> ValidationResult:
        """Modify a percentage value (alias for modify_weight for clarity)."""
        return self.modify_weight(section_name, param_name, new_pct)

    def set_value(self, section_name: str, param_name: str, new_value: Any) -> ValidationResult:
        """Set any parameter value with validation."""
        try:
            sections = self.active_profile.get("sections", {})
            if section_name not in sections:
                return ValidationResult.fail([f"Section not found: {section_name}"])

            section = sections[section_name]
            if param_name not in section.get("parameters", {}):
                return ValidationResult.fail([f"Parameter not found: {param_name}"])

            param = section["parameters"][param_name]
            if not param.get("editable", True):
                return ValidationResult.fail([f"Parameter is not editable: {param_name}"])

            # Range validation
            if "recommended_range" in param and param["recommended_range"]:
                r = param["recommended_range"]
                if len(r) == 2:
                    if not (r[0] <= new_value <= r[1]):
                        return ValidationResult.fail([f"Value {new_value} outside recommended range [{r[0]}, {r[1]}]"])

            old_value = param.get("current_value")
            param["current_value"] = new_value

            # Validate full profile
            validation = self._validate_full_profile()
            if not validation.success:
                param["current_value"] = old_value
                return validation

            return ValidationResult.ok({"old_value": old_value, "new_value": new_value})

        except Exception as e:
            return ValidationResult.fail([f"Error setting value: {e}"])

    def add_factor(self, section_name: str, factor_name: str, weight: float, description: str = "") -> ValidationResult:
        """Add a custom factor to a section."""
        try:
            sections = self.active_profile.get("sections", {})
            if section_name not in sections:
                return ValidationResult.fail([f"Section not found: {section_name}"])

            section = sections[section_name]

            # Find first available additional factor slot
            factor_slot = None
            for slot in ["additional_factor_1", "additional_factor_2"]:
                factor = section.get(slot)
                if not factor or not factor.get("name"):
                    factor_slot = slot
                    break

            if not factor_slot:
                return ValidationResult.fail([f"No available factor slots in {section_name}"])

            if weight < 0 or weight > 100:
                return ValidationResult.fail(["Weight must be between 0 and 100"])

            # Validate total weights
            current_total = sum(p.get("weight_pct", 0) for p in section.get("parameters", {}).values() if p.get("weight_pct"))
            if current_total + weight > 100:
                return ValidationResult.fail([f"Adding weight {weight} would exceed 100% (current: {current_total}%)"])

            # Add the factor
            section[factor_slot] = {
                "name": factor_name,
                "description": description,
                "weight_pct": weight,
                "editable": True,
                "removable": True
            }

            # Validate section
            validation = self._validate_section_weights(section_name)
            if not validation.success:
                section[factor_slot] = {"name": "", "description": "", "weight_pct": 0.0, "editable": True, "removable": True}
                return validation

            return ValidationResult.ok({"slot": factor_slot, "name": factor_name, "weight": weight})

        except Exception as e:
            return ValidationResult.fail([f"Error adding factor: {e}"])

    def delete_factor(self, section_name: str, param_name: str) -> ValidationResult:
        """Delete a custom factor (protected factors cannot be deleted)."""
        try:
            sections = self.active_profile.get("sections", {})
            if section_name not in sections:
                return ValidationResult.fail([f"Section not found: {section_name}"])

            section = sections[section_name]

            # Check parameters
            if param_name in section.get("parameters", {}):
                param = section["parameters"][param_name]
                if param.get("protected", False):
                    return ValidationResult.fail([f"Cannot delete protected parameter: {param_name}"])
                del section["parameters"][param_name]
            # Check additional factors
            elif param_name in ("additional_factor_1", "additional_factor_2"):
                factor = section.get(param_name)
                if factor and factor.get("removable", True):
                    section[param_name] = {"name": "", "description": "", "weight_pct": 0.0, "editable": True, "removable": True}
                else:
                    return ValidationResult.fail([f"Factor cannot be removed: {param_name}"])
            else:
                return ValidationResult.fail([f"Parameter not found: {param_name}"])

            # Validate section
            validation = self._validate_section_weights(section_name)
            if not validation.success:
                return validation

            return ValidationResult.ok({"deleted": param_name})

        except Exception as e:
            return ValidationResult.fail([f"Error deleting factor: {e}"])

    def rename_factor(self, section_name: str, old_name: str, new_name: str) -> ValidationResult:
        """Rename a parameter or custom factor."""
        try:
            if not new_name or not new_name.strip():
                return ValidationResult.fail(["New name cannot be empty"])

            new_name = new_name.strip()
            if not new_name.replace('_', '').isalnum():
                return ValidationResult.fail(["Name must be alphanumeric with underscores only"])

            sections = self.active_profile.get("sections", {})
            if section_name not in sections:
                return ValidationResult.fail([f"Section not found: {section_name}"])

            section = sections[section_name]

            # Check parameters
            if old_name in section.get("parameters", {}):
                if new_name in section["parameters"]:
                    return ValidationResult.fail([f"Parameter already exists: {new_name}"])
                param = section["parameters"].pop(old_name)
                param["name"] = new_name
                section["parameters"][new_name] = param
                return ValidationResult.ok({"renamed": f"{old_name} -> {new_name}"})

            # Check additional factors
            for slot in ["additional_factor_1", "additional_factor_2"]:
                factor = section.get(slot)
                if factor and factor.get("name") == old_name:
                    if new_name in section.get("parameters", {}):
                        return ValidationResult.fail([f"Name already exists: {new_name}"])
                    factor["name"] = new_name
                    return ValidationResult.ok({"renamed": f"{old_name} -> {new_name}"})

            return ValidationResult.fail([f"Parameter not found: {old_name}"])

        except Exception as e:
            return ValidationResult.fail([f"Error renaming factor: {e}"])

    def reorder_factors(self, section_name: str, ordered_names: List[str]) -> ValidationResult:
        """Reorder parameters within a section."""
        try:
            sections = self.active_profile.get("sections", {})
            if section_name not in sections:
                return ValidationResult.fail([f"Section not found: {section_name}"])

            section = sections[section_name]
            params = section.get("parameters", {})

            if set(ordered_names) != set(params.keys()):
                return ValidationResult.fail(["Ordered names must match existing parameter names exactly"])

            # Reorder
            reordered = {name: params[name] for name in ordered_names}
            section["parameters"] = reordered

            return ValidationResult.ok({"reordered": ordered_names})

        except Exception as e:
            return ValidationResult.fail([f"Error reordering factors: {e}"])

    # =====================================================================
    # PROFILE MANAGEMENT
    # =====================================================================

    def save_current(self) -> ValidationResult:
        """Persist v1.0_current.json atomically."""
        try:
            self._ensure_current_profile()

            # Validate before saving
            validation = self._validate_full_profile()
            if not validation.success:
                return validation

            current_path = self.profile_dir / "v1.0_current.json"
            temp_path = self.profile_dir / "v1.0_current.json.tmp"

            # Prepare output with proper structure
            output = {
                "metadata": self.active_profile.get("metadata", {}),
                "sections": self.active_profile.get("sections", {}),
                "formula_calibration": self.active_profile.get("formula_calibration", {})
            }
            output["metadata"]["last_modified"] = datetime.now().isoformat()
            output["metadata"]["modified_by"] = "Calibration Manager"

            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)

            # Atomic rename
            temp_path.replace(current_path)

            # Update last valid
            self._last_valid_profile = deepcopy(self.active_profile)

            return ValidationResult.ok({"saved": str(current_path)})

        except Exception as e:
            return ValidationResult.fail([f"Error saving profile: {e}"])

    def factory_reset(self) -> ValidationResult:
        """Reset v1.0_current.json to factory defaults."""
        try:
            self.active_profile = self._load_factory_default()
            return self.save_current()
        except Exception as e:
            return ValidationResult.fail([f"Error during factory reset: {e}"])

    def export_frozen(self) -> ValidationResult:
        """Create immutable v1.0_frozen.json from current profile."""
        try:
            validation = self._validate_full_profile()
            if not validation.success:
                return validation

            frozen_path = self.profile_dir / "v1.0_frozen.json"
            temp_path = self.profile_dir / "v1.0_frozen.json.tmp"

            output = {
                "metadata": {
                    **self.active_profile.get("metadata", {}),
                    "profile_id": "v1.0_frozen",
                    "status": "FROZEN",
                    "last_modified": datetime.now().isoformat(),
                    "based_on": "v1.0_current",
                },
                "sections": self.active_profile.get("sections", {}),
                "formula_calibration": self.active_profile.get("formula_calibration", {})
            }

            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)

            temp_path.replace(frozen_path)

            return ValidationResult.ok({"frozen": str(frozen_path)})

        except Exception as e:
            return ValidationResult.fail([f"Error exporting frozen profile: {e}"])

    def save_snapshot(self, horoscope_id: str, notes: str = "", engineer: str = "Engineer") -> ValidationResult:
        """Save calibration snapshot for validation history."""
        try:
            # Ensure history directory exists
            self.history_dir.mkdir(parents=True, exist_ok=True)

            # Find next snapshot number
            existing = list(self.history_dir.glob("calibration_*.json"))
            nums = [int(f.stem.split('_')[1]) for f in existing if f.stem.split('_')[1].isdigit()]
            next_num = max(nums) + 1 if nums else 1

            if next_num > 20:
                return ValidationResult.fail(["Maximum 20 validation snapshots reached"])

            snapshot_id = f"calibration_{next_num:03d}"
            timestamp = datetime.now().isoformat()

            # Compute diff from last snapshot
            changes = self._compute_changes()

            snapshot = {
                "snapshot_id": snapshot_id,
                "timestamp": timestamp,
                "horoscope_id": horoscope_id,
                "reason": notes,
                "changes_made": changes,
                "validation_score": None,  # To be filled by engineer
                "engineer": engineer,
                "profile": deepcopy(self.active_profile)
            }

            snapshot_path = self.history_dir / f"{snapshot_id}.json"
            with open(snapshot_path, 'w', encoding='utf-8') as f:
                json.dump(snapshot, f, indent=2, ensure_ascii=False)

            return ValidationResult.ok({"snapshot": snapshot_id, "path": str(snapshot_path)})

        except Exception as e:
            return ValidationResult.fail([f"Error saving snapshot: {e}"])

    def promote_to_frozen(self) -> ValidationResult:
        """Promote v1.0_current.json to v1.0_frozen.json (final production profile)."""
        return self.export_frozen()

    def get_history(self) -> ValidationResult:
        """Get list of calibration history snapshots."""
        try:
            snapshots = []
            for f in sorted(self.history_dir.glob("calibration_*.json")):
                with open(f, 'r', encoding='utf-8') as fp:
                    data = json.load(fp)
                snapshots.append({
                    "snapshot_id": data.get("snapshot_id"),
                    "timestamp": data.get("timestamp"),
                    "horoscope_id": data.get("horoscope_id"),
                    "reason": data.get("reason"),
                    "validation_score": data.get("validation_score"),
                    "engineer": data.get("engineer"),
                    "changes_count": len(data.get("changes_made", []))
                })
            return ValidationResult.ok({"snapshots": snapshots, "count": len(snapshots)})
        except Exception as e:
            return ValidationResult.fail([f"Error getting history: {e}"])

    # =====================================================================
    # VALIDATION (Internal)
    # =====================================================================

    def _validate_full_profile(self) -> ValidationResult:
        """Validate entire profile using schema."""
        try:
            SchemaCalibrationProfile.model_validate(self.active_profile)
            return ValidationResult.ok({"validated": True})
        except Exception as e:
            return ValidationResult.fail([f"Profile validation failed: {e}"])

    def _validate_section_weights(self, section_name: str) -> ValidationResult:
        """Validate that section parameter weights sum to 100%."""
        try:
            sections = self.active_profile.get("sections", {})
            if section_name not in sections:
                return ValidationResult.fail([f"Section not found: {section_name}"])

            section = sections[section_name]
            params = section.get("parameters", {})

            total = sum(p.get("weight_pct", 0) for p in params.values() if p.get("weight_pct") is not None)

            if abs(total - 100.0) > 0.01:
                return ValidationResult.fail([f"Section '{section_name}' weights sum to {total}%, expected 100%"])

            return ValidationResult.ok({"total_weight": total})
        except Exception as e:
            return ValidationResult.fail([f"Error validating section weights: {e}"])

    def _compute_changes(self) -> List[Dict[str, Any]]:
        """Compute changes from last snapshot or default."""
        # Simplified: return empty list for now
        # In production, would compare against last snapshot
        return []

    def _validate_profile(self) -> ValidationResult:
        """Validate current profile and return status."""
        try:
            SchemaCalibrationProfile.model_validate(self.active_profile)

            # Compute status
            sections = self.active_profile.get("sections", {})
            section_status = {}
            for name, section in sections.items():
                total = sum(p.get("weight_pct", 0) for p in section.get("parameters", {}).values() if p.get("weight_pct"))
                protected = sum(1 for p in section.get("parameters", {}).values() if p.get("protected"))
                custom = sum(1 for p in section.get("parameters", {}).values() if not p.get("protected"))
                additional = sum(1 for f in ["additional_factor_1", "additional_factor_2"] if section.get(f, {}).get("name"))

                section_status[name] = {
                    "current_total": total,
                    "protected_factors": protected,
                    "custom_factors": custom,
                    "additional_factors": additional,
                    "valid": abs(total - 100.0) < 0.01
                }

            metadata = self.active_profile.get("metadata", {})
            return ValidationResult.ok({
                "valid": True,
                "profile_status": "VALID",
                "section_status": section_status,
                "current_total": sum(s.get("total_weight_pct", 100) for s in sections.values()),
                "protected_factors": sum(s["protected_factors"] for s in section_status.values()),
                "custom_factors": sum(s["custom_factors"] for s in section_status.values()),
                "ready_for_prediction": all(s["valid"] for s in section_status.values()),
                "validation_horoscopes_completed": metadata.get("validation_horoscopes_completed", 0),
                "profile_id": metadata.get("profile_id", "unknown"),
            })
        except Exception as e:
            return ValidationResult.ok({
                "valid": False,
                "profile_status": "INVALID",
                "errors": [str(e)],
                "ready_for_prediction": False,
            })

    # =====================================================================
    # PROFILE STATUS
    # =====================================================================

    def get_profile_status(self) -> ValidationResult:
        """Get comprehensive profile health status."""
        return self._validate_profile()

    def validate_profile(self) -> ValidationResult:
        """Explicit validation call."""
        return self._validate_profile()


__all__ = ['CalibrationManager', 'ValidationResult']
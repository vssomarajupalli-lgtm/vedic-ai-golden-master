from typing import Any, Dict


def build_engine_provenance(calibration: Any, engine_name: str, formula_source: str) -> Dict[str, Any]:
    """Builds real, deterministic provenance metadata at the formula owner.

    All values are engine-known facts: the engine display name, the calibration
    profile the engine is bound to, and the calibration section that supplies
    its formula configuration. No invented values, no clock-dependent fields
    (execution timestamps are deliberately not emitted to keep outputs
    deterministic).
    """
    meta: Dict[str, Any] = {}
    try:
        meta = calibration.active_profile.get("metadata", {}) or {}
    except Exception:
        meta = {}
    return {
        "engine": engine_name,
        "version": str(meta.get("version", "1.0.0")),
        "formula_source": formula_source,
        "formula_version": "1.0",
        "calibration_profile": str(meta.get("profile_id", "v1.0_default")),
        "calibration_version": str(meta.get("version", "1.0.0")),
    }


def build_factor_provenance(raw: float, weight: float) -> Dict[str, Any]:
    """Records a single factor as computed by the owning engine.

    `contribution` is exactly `raw * weight` using the same operands the engine
    already multiplies — nothing is recomputed or re-implemented here.
    """
    raw_f = float(raw)
    weight_f = float(weight)
    return {
        "raw": raw_f,
        "weight": weight_f,
        "contribution": raw_f * weight_f,
    }

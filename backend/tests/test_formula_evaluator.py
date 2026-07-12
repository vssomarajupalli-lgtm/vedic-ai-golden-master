import pytest
from app.formulas.schema import FormulaSchema, FormulaEvaluationResult
from app.formulas.evaluator import FormulaEvaluator
from app.formulas.loader import formula_repository_loader

@pytest.fixture
def dummy_formula():
    return FormulaSchema(
        formula_key="TEST_EVAL",
        formula_name="Test Evaluator",
        formula_category="Timing Assessment",
        required_engines=["NatalPromiseEngine", "TransitEngine", "DashaEngine"],
        required_signals=["7th_house", "venus"],
        required_confidence_layers=["transit_saturn_7th", "dasha_venus"],
        answer_template_key="test_template"
    )

def test_engine_degradation(dummy_formula):
    payload = {
        "natal_promise": {"data": "ok"},
        "dasha": {"data": "ok"}
        # Missing transit
    }
    
    warnings = FormulaEvaluator.check_engine_degradation(dummy_formula, payload)
    assert len(warnings) == 1
    assert "TransitEngine output is missing" in warnings[0]

def test_missing_payload_handling(dummy_formula):
    payload = {
        "natal_promise": {},
        "transit": {},
        "dasha": {}
        # Missing "7th_house" and "venus" signals
    }
    
    # Build isolated_signals (empty - signals not found)
    isolated_signals = {}
    formula_calibration = {}
    
    result = FormulaEvaluator.evaluate(dummy_formula, payload, isolated_signals, formula_calibration)
    assert result.final_state == "MIXED"  # Degrades to mixed due to missing signals/warnings
    warnings_str = " ".join(result.system_warnings)
    assert "Missing Payload" in warnings_str
    assert "7th_house" in warnings_str

def test_favorable_resolution(dummy_formula):
    payload = {
        "natal_promise": {"7th_house": "good", "venus": "good"},
        "transit": {"ok": True},
        "dasha": {"ok": True}
    }
    
    # Build isolated_signals with required signals
    isolated_signals = {"7th_house": "good", "venus": "good"}
    formula_calibration = {}
    
    result = FormulaEvaluator.evaluate(dummy_formula, payload, isolated_signals, formula_calibration)
    assert result.final_state == "FAVORABLE"
    assert len(result.system_warnings) == 0

def test_degraded_to_mixed(dummy_formula):
    payload = {
        "natal_promise": {"7th_house": "good", "venus": "good"},
        "dasha": {"ok": True}
        # Transit missing
    }
    
    isolated_signals = {"7th_house": "good", "venus": "good"}
    formula_calibration = {}
    
    result = FormulaEvaluator.evaluate(dummy_formula, payload, isolated_signals, formula_calibration)
    assert result.final_state == "MIXED"
    assert len(result.system_warnings) > 0
    assert "TransitEngine output is missing" in result.system_warnings[0]

def test_calibration_weights_applied(dummy_formula):
    """Test that formula calibration weights are properly applied."""
    payload = {
        "natal_promise": {"marriage": {"score": 80}},
        "transit": {"ok": True},
        "dasha": {"ok": True}
    }
    
    isolated_signals = {"7th_house": "good", "venus": "good"}
    formula_calibration = {
        "enabled": True,
        "factors": {
            "7th_house": {"weight_pct": 40.0, "enabled": True},
            "venus": {"weight_pct": 60.0, "enabled": True}
        }
    }
    
    result = FormulaEvaluator.evaluate(dummy_formula, payload, isolated_signals, formula_calibration)
    assert result.factor_weights.get("7th_house") == 40.0
    assert result.factor_weights.get("venus") == 60.0
    assert result.factor_fulfillment.get("7th_house") is True
    assert result.factor_fulfillment.get("venus") is True

def test_calibration_normalization(dummy_formula):
    """Test that calibration weights auto-normalize to 100%."""
    payload = {"natal_promise": {"marriage": {"score": 80}}, "transit": {"ok": True}, "dasha": {"ok": True}}
    isolated_signals = {"7th_house": "good", "venus": "good"}
    # Weights don't sum to 100
    formula_calibration = {
        "enabled": True,
        "factors": {
            "7th_house": {"weight_pct": 30.0, "enabled": True},
            "venus": {"weight_pct": 30.0, "enabled": True}
        }
    }
    
    result = FormulaEvaluator.evaluate(dummy_formula, payload, isolated_signals, formula_calibration)
    # Should normalize to 50/50
    assert result.factor_weights.get("7th_house") == 50.0
    assert result.factor_weights.get("venus") == 50.0
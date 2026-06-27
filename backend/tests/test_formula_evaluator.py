import pytest
from app.formulas.schema import FormulaSchema, FormulaEvaluationResult
from app.formulas.evaluator import FormulaEvaluator

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

def test_extract_signals():
    payload = {
        "natal_promise": {
            "houses": {
                "7th_house": {"lord": "venus", "bindus": 28}
            },
            "planets": {
                "venus": {"dignity": "exalted"}
            }
        },
        "transit": {
            "some_transit": "value"
        }
    }
    
    signals = FormulaEvaluator.extract_signals(payload, ["7th_house", "venus"])
    assert "7th_house" in signals
    assert signals["7th_house"]["lord"] == "venus"
    assert "venus" in signals
    assert signals["venus"]["dignity"] == "exalted"
    assert "some_transit" not in signals

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
    
    result = FormulaEvaluator.evaluate(dummy_formula, payload)
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
    
    result = FormulaEvaluator.evaluate(dummy_formula, payload)
    assert result.final_state == "FAVORABLE"
    assert len(result.system_warnings) == 0

def test_degraded_to_mixed(dummy_formula):
    payload = {
        "natal_promise": {"7th_house": "good", "venus": "good"},
        "dasha": {"ok": True}
        # Transit missing
    }
    
    result = FormulaEvaluator.evaluate(dummy_formula, payload)
    assert result.final_state == "MIXED"
    assert len(result.system_warnings) > 0
    assert "TransitEngine output is missing" in result.system_warnings[0]

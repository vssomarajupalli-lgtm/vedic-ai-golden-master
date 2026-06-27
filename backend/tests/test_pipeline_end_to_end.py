import pytest
from typing import Dict, Any
from app.core.question_router import QuestionRouter
from app.formulas.loader import formula_repository_loader
from app.formulas.evaluator import FormulaEvaluator
from app.formulas.composer import answer_composer, TemplateNotFoundError
from app.formulas.schema import ComposerPromptPackage

@pytest.fixture
def mock_chart_payload() -> Dict[str, Any]:
    # A generic payload that has all the right engines and signals to trigger a FAVORABLE or MIXED state
    return {
        "natal_promise": {
            "7th_house": {"strength": 90, "lord": "venus"},
            "10th_house": {"strength": 85, "lord": "mars"},
            "2nd_house": {"strength": 80},
            "8th_house": {"strength": 60},
            "11th_house": {"strength": 88},
            "9th_house": {"strength": 75},
            "12th_house": {"strength": 50},
            "venus": {"dignity": "exalted"},
            "jupiter": {"dignity": "own_sign"},
            "saturn": {"dignity": "friendly"},
            "rahu": {"dignity": "neutral"},
            "lagna_lord": "mars",
            "7th_lord": "venus",
            "10th_lord": "mars"
        },
        "dasha": {
            "current_mahadasha": "venus",
            "current_antardasha": "jupiter"
        },
        "transit": {
            "jupiter_transit_7th_lagna": True,
            "transit_saturn_jupiter_activate_10th": True
        },
        "ashtakavarga": {
            "10th_house_bindus": 32
        }
    }

def run_pipeline(question_id: str, payload: Dict[str, Any]) -> ComposerPromptPackage:
    router = QuestionRouter()
    route_result = router.route_question(question_id)
    if route_result["status"] == "error":
        raise ValueError(route_result["message"])
        
    formula_key = route_result["formula_key"]
    formula = formula_repository_loader.get_formula(formula_key)
    eval_result = FormulaEvaluator.evaluate(formula, payload)
    prompt_package = answer_composer.compose(eval_result)
    return prompt_package

def test_scenario_1_marriage_timing(mock_chart_payload):
    # Scenario 1: QID 7.2 -> MAR_TIMING_001
    package = run_pipeline("7.2", mock_chart_payload)
    
    assert package is not None
    assert package.prompt_template_id == "timing_assessment_v1_favorable"
    assert "FAVORABLE" in package.system_prompt
    assert package.final_state == "FAVORABLE"
    assert "7th_house" in package.evidence_block

def test_scenario_2_career_growth(mock_chart_payload):
    # Scenario 2: QID 10.1 -> CAR_GROWTH_001
    package = run_pipeline("10.1", mock_chart_payload)
    
    assert package is not None
    assert package.prompt_template_id == "timing_assessment_v1_favorable"
    assert "10th_house" in package.evidence_block
    
def test_scenario_3_wealth_sudden(mock_chart_payload):
    # Scenario 3: QID 2.7 -> WEA_SUDDEN_001
    package = run_pipeline("2.7", mock_chart_payload)
    
    assert package is not None
    assert package.prompt_template_id == "multifactor_assessment_v1_favorable"
    assert "8th_house" in package.evidence_block

def test_negative_invalid_question_id():
    with pytest.raises(ValueError) as exc:
        run_pipeline("99.99", {})
    assert "not found in registry" in str(exc.value)

def test_negative_engine_degradation(mock_chart_payload):
    # Remove Transit Engine output
    del mock_chart_payload["transit"]
    
    # 7.2 requires TransitEngine
    package = run_pipeline("7.2", mock_chart_payload)
    
    # Missing TransitEngine should trigger degradation to MIXED
    assert package.final_state == "MIXED"
    assert package.prompt_template_id == "timing_assessment_v1_mixed"
    assert "TransitEngine output is missing" in package.evidence_block
    assert len(package.system_warnings) > 0

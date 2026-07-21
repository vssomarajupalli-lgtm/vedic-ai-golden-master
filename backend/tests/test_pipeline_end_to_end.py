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
        "planets": {
            "venus": {"final_score": 85.0},
            "jupiter": {"final_score": 80.0},
            "saturn": {"final_score": 70.0},
            "sun": {"final_score": 75.0},
            "moon": {"final_score": 70.0},
            "mars": {"final_score": 65.0},
            "mercury": {"final_score": 60.0},
            "rahu": {"final_score": 50.0},
            "ketu": {"final_score": 50.0},
        },
        "houses": {
            "7": {"final_score": 85.0, "lord_strength_score": 85.0},
            "10": {"final_score": 80.0, "lord_strength_score": 80.0},
            "11": {"final_score": 75.0, "lord_strength_score": 75.0},
            "2": {"final_score": 70.0, "lord_strength_score": 70.0},
            "5": {"final_score": 70.0, "lord_strength_score": 70.0},
            "9": {"final_score": 70.0, "lord_strength_score": 70.0},
            "8": {"final_score": 65.0, "lord_strength_score": 65.0},
            "12": {"final_score": 60.0, "lord_strength_score": 60.0},
            "6": {"final_score": 60.0, "lord_strength_score": 60.0},
            "1": {"final_score": 80.0, "lord_strength_score": 80.0},
        },
        "vargas": {
            "D9": {"planets": {"venus": {"final_score": 85.0}, "jupiter": {"final_score": 80.0}, "saturn": {"final_score": 70.0}}},
            "D10": {"planets": {"saturn": {"final_score": 75.0}, "jupiter": {"final_score": 80.0}}},
            "D2": {"planets": {"jupiter": {"final_score": 75.0}}},
            "D24": {"planets": {"mercury": {"final_score": 70.0}}},
            "D7": {"planets": {"jupiter": {"final_score": 75.0}}},
            "D4": {"planets": {"mars": {"final_score": 70.0}}},
            "D20": {"planets": {"jupiter": {"final_score": 80.0}}},
            "D6": {"planets": {"sun": {"final_score": 70.0}}},
        },
        "dashas": {
            "synthesis": {"dasha_strength": 70}
        },
        "rasis": {},
        "ashtakavarga": {},
        "natal_promise": {
            "marriage": {"score": 80, "breakdown": {"bhava": 85, "bhavadhipati": 85, "karaka": 85, "varga": 85}},
            "career": {"score": 80, "breakdown": {"bhava": 80, "bhavadhipati": 80, "karaka": 80, "varga": 80}},
            "wealth": {"score": 80, "breakdown": {"bhava": 80, "bhavadhipati": 80, "karaka": 80, "varga": 80}},
            "education": {"score": 80, "breakdown": {"bhava": 80, "bhavadhipati": 80, "karaka": 80, "varga": 80}},
            "children": {"score": 80, "breakdown": {"bhava": 80, "bhavadhipati": 80, "karaka": 80, "varga": 80}},
            "property": {"score": 80, "breakdown": {"bhava": 80, "bhavadhipati": 80, "karaka": 80, "varga": 80}},
            "health": {"score": 80, "breakdown": {"bhava": 80, "bhavadhipati": 80, "karaka": 80, "varga": 80}},
            "spirituality": {"score": 80, "breakdown": {"bhava": 80, "bhavadhipati": 80, "karaka": 80, "varga": 80}},
        },
        "transit": {
            "activation_score": 70
        },
        "yogas": {
            "marriage_yoga": {"strength": 80}
        }
    }

def build_isolated_signals(formula, engine_outputs):
    """Build isolated signals for formula evaluation."""
    isolated = {}
    payload = {
        "planets": engine_outputs.get("planets", {}),
        "houses": engine_outputs.get("houses", {}),
        "vargas": engine_outputs.get("vargas", {}),
        "dashas": engine_outputs.get("dashas", {}),
        "rasis": engine_outputs.get("rasis", {}),
        "ashtakavarga": engine_outputs.get("ashtakavarga", {}),
        "natal_promise": engine_outputs.get("natal_promise", {}),
        "transit": engine_outputs.get("transit", {}),
        "yogas": engine_outputs.get("yogas", {}),
    }
    signal_paths = {
        "7th_house": ("houses", "7", "final_score"),
        "7th_lord": ("houses", "7", "lord_strength_score"),
        "venus": ("planets", "venus", "final_score"),
        "d9": ("vargas", "D9", "planets", "venus", "final_score"),
        "yoga": ("yogas", "marriage_yoga", "strength"),
        "dasha": ("dashas", "synthesis", "dasha_strength"),
        "transit": ("transit", "activation_score"),
        "10th_house": ("houses", "10", "final_score"),
        "10th_lord": ("houses", "10", "lord_strength_score"),
        "saturn": ("planets", "saturn", "final_score"),
        "d10": ("vargas", "D10", "planets", "saturn", "final_score"),
        "11th_house": ("houses", "11", "final_score"),
        "jupiter": ("planets", "jupiter", "final_score"),
        "2nd_house": ("houses", "2", "final_score"),
        "d2": ("vargas", "D2", "planets", "jupiter", "final_score"),
        "5th_house": ("houses", "5", "final_score"),
        "9th_house": ("houses", "9", "final_score"),
        "8th_house": ("houses", "8", "final_score"),
        "rahu": ("planets", "rahu", "final_score"),
        "12th_house": ("houses", "12", "final_score"),
        "sun": ("planets", "sun", "final_score"),
        "moon": ("planets", "moon", "final_score"),
        "6th_house": ("houses", "6", "final_score"),
        "lagna": ("houses", "1", "final_score"),
        "lagna_lord": ("houses", "1", "lord_strength_score"),
        "mercury": ("planets", "mercury", "final_score"),
        "d24": ("vargas", "D24", "planets", "mercury", "final_score"),
        "d7": ("vargas", "D7", "planets", "jupiter", "final_score"),
        "d4": ("vargas", "D4", "planets", "mars", "final_score"),
        "ketu": ("planets", "ketu", "final_score"),
        "d20": ("vargas", "D20", "planets", "jupiter", "final_score"),
        "d6": ("vargas", "D6", "planets", "sun", "final_score"),
    }
    for sig in formula.required_signals:
        path = signal_paths.get(sig)
        if path:
            current = payload
            for key in path:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    current = None
                    break
            if current is not None:
                isolated[sig] = current
    return isolated

def run_pipeline(question_id: str, payload: Dict[str, Any]) -> ComposerPromptPackage:
    router = QuestionRouter()
    route_result = router.route_question(question_id)
    if route_result["status"] == "error":
        raise ValueError(route_result["message"])
        
    formula_key = route_result["formula_key"]
    formula = formula_repository_loader.get_formula(formula_key)
    
    # Get formula calibration
    formula_calibration = formula_repository_loader.get_formula_calibration(formula_key)
    
    # Build isolated signals
    isolated_signals = build_isolated_signals(formula, payload)
    
    eval_result = FormulaEvaluator.evaluate(
        formula=formula,
        engine_outputs=payload,
        isolated_signals=isolated_signals,
        formula_calibration=formula_calibration
    )
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
    
    # 7.3 -> MAR_TIMING_DELAY requires TransitEngine
    package = run_pipeline("7.3", mock_chart_payload)
    
    # Missing TransitEngine should trigger degradation to MIXED
    assert package.final_state == "MIXED"
    assert package.prompt_template_id == "timing_assessment_v1_mixed"
    assert "TransitEngine output is missing" in package.evidence_block
    assert len(package.system_warnings) > 0

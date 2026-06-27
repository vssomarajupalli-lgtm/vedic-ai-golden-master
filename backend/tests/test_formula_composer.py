import pytest
import json
from app.formulas.schema import FormulaEvaluationResult
from app.formulas.composer import AnswerComposer, TemplateNotFoundError

@pytest.fixture
def mock_favorable_result():
    return FormulaEvaluationResult(
        final_state="FAVORABLE",
        isolated_signals={"7th_house": "strong", "venus": "exalted"},
        answer_template_key="timing_assessment_v1",
        system_warnings=[]
    )

@pytest.fixture
def mock_mixed_result():
    return FormulaEvaluationResult(
        final_state="MIXED",
        isolated_signals={"7th_house": "strong", "venus": "exalted"},
        answer_template_key="timing_assessment_v1",
        system_warnings=["Engine Degradation: TransitEngine output is missing."]
    )

def test_composer_favorable_execution(mock_favorable_result):
    composer = AnswerComposer()
    package = composer.compose(mock_favorable_result)
    
    assert package.prompt_template_id == "timing_assessment_v1_favorable"
    assert package.user_prompt is None
    assert package.final_state == "FAVORABLE"
    
    # Check evidence block determinism
    assert "FINAL STATE: FAVORABLE" in package.evidence_block
    assert "SYSTEM WARNINGS:" not in package.evidence_block
    assert json.dumps(mock_favorable_result.isolated_signals, indent=2) in package.evidence_block
    
    # Check system prompt loaded
    assert "FAVORABLE" in package.system_prompt
    assert "GOVERNANCE RULES" in package.system_prompt

def test_composer_mixed_with_warnings(mock_mixed_result):
    composer = AnswerComposer()
    package = composer.compose(mock_mixed_result)
    
    assert package.prompt_template_id == "timing_assessment_v1_mixed"
    assert package.final_state == "MIXED"
    
    # Check evidence block warnings inclusion
    assert "SYSTEM WARNINGS:" in package.evidence_block
    assert "TransitEngine output is missing" in package.evidence_block
    
def test_composer_template_not_found():
    composer = AnswerComposer()
    bad_result = FormulaEvaluationResult(
        final_state="FAVORABLE",
        isolated_signals={},
        answer_template_key="does_not_exist_999",
        system_warnings=[]
    )
    with pytest.raises(TemplateNotFoundError):
        composer.compose(bad_result)

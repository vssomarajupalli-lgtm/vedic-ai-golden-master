import pytest
from app.formulas.schema import FormulaSchema
from app.formulas.loader import FormulaRepositoryLoader, FormulaNotFoundError
from app.formulas.validator import FormulaValidator, DuplicateFormulaError, InvalidFormulaError

def get_mock_valid_formulas():
    return [
        FormulaSchema(
            formula_key="TEST_001",
            formula_name="Test Formula",
            formula_category="Timing Assessment",
            required_engines=["NatalPromiseEngine"],
            required_signals=["7th_house"],
            required_vargas=[],
            required_confidence_layers=["layer_1"],
            future_gochara_required=False,
            answer_template_key="template_1"
        )
    ]

def get_mock_duplicate_formulas():
    formulas = get_mock_valid_formulas()
    formulas.append(
        FormulaSchema(
            formula_key="TEST_001",
            formula_name="Duplicate Formula",
            formula_category="Timing Assessment",
            required_engines=["NatalPromiseEngine"],
            required_signals=["7th_house"],
            required_vargas=[],
            required_confidence_layers=["layer_1"],
            future_gochara_required=False,
            answer_template_key="template_1"
        )
    )
    return formulas

def get_mock_invalid_engine_formulas():
    formulas = get_mock_valid_formulas()
    formulas[0].required_engines = ["NonExistentEngine"]
    return formulas

def get_mock_invalid_category_formulas():
    formulas = get_mock_valid_formulas()
    formulas[0].formula_category = "Random Category"
    return formulas

def test_validator_success():
    formulas = get_mock_valid_formulas()
    assert FormulaValidator.validate_all(formulas) is True

def test_validator_duplicate_key():
    formulas = get_mock_duplicate_formulas()
    with pytest.raises(DuplicateFormulaError):
        FormulaValidator.validate_all(formulas)

def test_validator_invalid_engine():
    formulas = get_mock_invalid_engine_formulas()
    with pytest.raises(InvalidFormulaError) as excinfo:
        FormulaValidator.validate_all(formulas)
    assert "Invalid engine reference" in str(excinfo.value)

def test_validator_invalid_category():
    formulas = get_mock_invalid_category_formulas()
    with pytest.raises(InvalidFormulaError) as excinfo:
        FormulaValidator.validate_all(formulas)
    assert "Invalid category" in str(excinfo.value)

def test_loader_success():
    loader = FormulaRepositoryLoader()
    # It should load the seed formulas automatically without error
    formulas = loader.list_formulas()
    assert len(formulas) >= 8 # the 8 seed formulas
    
    # Test get_formula
    formula = loader.get_formula("MAR_TIMING_NORMAL")
    assert formula.formula_key == "MAR_TIMING_NORMAL"
    assert "DashaEngine" in formula.required_engines

def test_loader_not_found():
    loader = FormulaRepositoryLoader()
    with pytest.raises(FormulaNotFoundError):
        loader.get_formula("NON_EXISTENT_999")

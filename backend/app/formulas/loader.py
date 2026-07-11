from typing import List, Dict, Optional, Any
from app.formulas.schema import FormulaSchema
from app.formulas.registry_data import get_seed_registry
from app.formulas.validator import FormulaValidator
from app.calibration.calibration_manager import CalibrationManager

class FormulaNotFoundError(Exception):
    pass

class FormulaRepositoryLoader:
    def __init__(self, calibration_manager: Optional[CalibrationManager] = None):
        self._formulas: Dict[str, FormulaSchema] = {}
        self.calibration_manager = calibration_manager or CalibrationManager()
        self._load_registry()

    def _load_registry(self):
        """
        Loads the formula definitions and validates them.
        """
        # Load the seed data
        formulas_list = get_seed_registry()
       
        # Validate all formulas (checks for duplicates, invalid engines, etc)
        FormulaValidator.validate_all(formulas_list)
       
        # Cache them internally
        for f in formulas_list:
            self._formulas[f.formula_key] = f

    def get_formula(self, formula_key: str) -> FormulaSchema:
        """
        Retrieve a formula by key. If the formula has a parent_formula_key,
        it resolves the inheritance by concatenating the array fields from the parent.
        Raises FormulaNotFoundError if the key does not exist.
        """
        formula = self._formulas.get(formula_key)
        if not formula:
            raise FormulaNotFoundError(f"Formula with key '{formula_key}' not found in repository.")
           
        if formula.parent_formula_key:
            parent_formula = self._formulas.get(formula.parent_formula_key)
            if not parent_formula:
                raise FormulaNotFoundError(f"Parent Formula '{formula.parent_formula_key}' not found.")
               
            # Create a flattened copy
            flattened = formula.model_copy()
           
            # Merge lists while preserving parent-first order
            flattened.required_engines = list(dict.fromkeys(parent_formula.required_engines + formula.required_engines))
            flattened.required_signals = list(dict.fromkeys(parent_formula.required_signals + formula.required_signals))
            flattened.required_dasha_layers = list(dict.fromkeys(parent_formula.required_dasha_layers + formula.required_dasha_layers))
            flattened.required_vargas = list(dict.fromkeys(parent_formula.required_vargas + formula.required_vargas))
            flattened.required_confidence_layers = list(dict.fromkeys(parent_formula.required_confidence_layers + formula.required_confidence_layers))
           
            # Inherit boolean/string fields if the child hasn't explicitly overridden them
            if "future_gochara_required" not in formula.model_fields_set:
                flattened.future_gochara_required = parent_formula.future_gochara_required
               
            if "answer_template_key" not in formula.model_fields_set:
                flattened.answer_template_key = parent_formula.answer_template_key
               
            return flattened

        return formula

    def get_formula_calibration(self, formula_key: str) -> Dict[str, Any]:
        """
        Returns the formula calibration data from the active calibration profile.
        Returns empty dict if formula not found in calibration.
        """
        formula_cal = self.calibration_manager.formula_calibration
        return formula_cal.get(formula_key, {})

    def list_formulas(self) -> List[FormulaSchema]:
        """
        Return all loaded formulas.
        """
        return list(self._formulas.values())

# Global instance for app usage
formula_repository_loader = FormulaRepositoryLoader()

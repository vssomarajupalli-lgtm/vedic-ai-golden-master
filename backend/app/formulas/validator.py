from typing import List, Dict
from app.formulas.schema import FormulaSchema

VALID_CATEGORIES = {
    "Natal Assessment",
    "Timing Assessment",
    "Transit Assessment",
    "Risk Assessment",
    "Strength Assessment",
    "Multi-factor Assessment",
    "Timing/Natal Assessment" # added for CAR_GROWTH_001
}

VALID_ENGINES = {
    "NatalPromiseEngine",
    "DashaEngine",
    "TransitEngine",
    "AshtakavargaEngine",
    "YogaEngine"
}

class DuplicateFormulaError(Exception):
    pass

class InvalidFormulaError(Exception):
    pass

class FormulaValidator:
    
    @staticmethod
    def validate_all(formulas: List[FormulaSchema]) -> bool:
        """
        Validates a list of formulas.
        Raises DuplicateFormulaError if keys are duplicated.
        Raises InvalidFormulaError if category or engines are invalid.
        """
        keys_seen = set()
        
        for formula in formulas:
            # 1. Duplicate Key Check
            if formula.formula_key in keys_seen:
                raise DuplicateFormulaError(f"Duplicate formula_key found: {formula.formula_key}")
            keys_seen.add(formula.formula_key)
            
            # 2. Invalid Category Check
            if formula.formula_category not in VALID_CATEGORIES:
                raise InvalidFormulaError(f"Invalid category '{formula.formula_category}' in formula: {formula.formula_key}")
            
            # 3. Invalid Engine Reference Check
            for engine in formula.required_engines:
                if engine not in VALID_ENGINES:
                    raise InvalidFormulaError(f"Invalid engine reference '{engine}' in formula: {formula.formula_key}")
                    
            # Basic field presence is handled by Pydantic FormulaSchema parsing
            
        return True

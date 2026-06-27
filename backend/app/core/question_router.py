from typing import Dict, Any, Optional
from app.core.registry_loader import QuestionRegistryLoader, RegistryValidationError

class QuestionRouter:
    """
    Question Router maps an incoming question_id to its corresponding
    Registry Entry and Formula Key, ensuring safe evaluation without crashing.
    """
    def __init__(self, loader: Optional[QuestionRegistryLoader] = None):
        self.loader = loader or QuestionRegistryLoader()
        self._registry_error = None
        
        # Pre-load registry to catch any Duplicate or Missing mappings immediately
        try:
            self.loader.load_registry()
        except Exception as e:
            # We catch the RegistryValidationError (Duplicate entries, missing fields, etc.)
            # and store it so route_question returns a safe error instead of crashing the API.
            self._registry_error = str(e)

    def route_question(self, question_id: str) -> Dict[str, Any]:
        """
        Takes a question_id and safely resolves it against the registry.
        """
        # 1. Handle Duplicate / Broken Registry State
        if self._registry_error:
            return {
                "status": "error",
                "error_type": "registry_configuration_error",
                "message": f"Registry failed to load: {self._registry_error}"
            }
            
        # 2. Handle Malformed Question ID
        if not question_id or not isinstance(question_id, str):
            return {
                "status": "error",
                "error_type": "malformed_question_id",
                "message": "Question ID must be a valid non-empty string."
            }

        # 3. Lookup
        record = self.loader.get_question(question_id)
        
        # 4. Handle Missing Registry Entry
        if not record:
            return {
                "status": "error",
                "error_type": "missing_registry_entry",
                "message": f"Question ID '{question_id}' not found in registry."
            }
            
        # 5. Success Flow
        return {
            "status": "success",
            "registry_record": record,
            "formula_key": record.get("formula_key"),
            "metadata": {
                "domain_name": record.get("domain_name"),
                "question_name": record.get("question_name"),
                "timing_required": record.get("timing_required"),
                "future_gochara_required": record.get("future_gochara_required")
            }
        }

import json
import os
from typing import List, Dict, Any

class RegistryValidationError(Exception):
    """Exception raised for validation errors in the Question Registry."""
    pass

class QuestionRegistryLoader:
    def __init__(self, file_path: str = None):
        if file_path is None:
            # Default to the config directory relative to this file
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_dir, 'config', 'question_registry.json')
        self.file_path = file_path
        self.registry_data: List[Dict[str, Any]] = []
        self._question_index: Dict[str, Dict[str, Any]] = {}
    
    def load_registry(self) -> List[Dict[str, Any]]:
        """Loads and parses the JSON registry."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Question Registry file not found at {self.file_path}")
            
        with open(self.file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise RegistryValidationError(f"Invalid JSON format in registry: {str(e)}")
                
        if not isinstance(data, list):
            raise RegistryValidationError("Registry root must be a JSON array.")
            
        self.registry_data = data
        self.validate_registry()
        
        # Build optimized lookup index
        self._question_index = {item['question_id']: item for item in self.registry_data}
        
        return self.registry_data
        
    def validate_registry(self):
        """Validates schema compliance and duplicate detections."""
        required_keys = {
            "question_id",
            "domain_id",
            "domain_name",
            "question_name",
            "formula_key",
            "timing_required",
            "future_gochara_required"
        }
        
        seen_question_ids = set()
        seen_formula_keys = set()
        
        for index, item in enumerate(self.registry_data):
            if not isinstance(item, dict):
                raise RegistryValidationError(f"Item at index {index} is not a JSON object.")
                
            missing_keys = required_keys - set(item.keys())
            if missing_keys:
                raise RegistryValidationError(f"Item at index {index} is missing required fields: {missing_keys}")
                
            q_id = item["question_id"]
            f_key = item["formula_key"]
            
            if q_id in seen_question_ids:
                raise RegistryValidationError(f"Duplicate question_id detected: {q_id}")
            seen_question_ids.add(q_id)
            
            # Type validations
            if not isinstance(item["domain_id"], int):
                raise RegistryValidationError(f"Item {q_id} has invalid domain_id (must be int)")
            if not isinstance(item["timing_required"], bool):
                raise RegistryValidationError(f"Item {q_id} has invalid timing_required (must be boolean)")
            if not isinstance(item["future_gochara_required"], bool):
                raise RegistryValidationError(f"Item {q_id} has invalid future_gochara_required (must be boolean)")
                
    def get_question(self, question_id: str) -> Dict[str, Any]:
        """Returns a question definition by its ID."""
        if not self._question_index:
            self.load_registry()
        return self._question_index.get(question_id)

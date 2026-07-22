import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.core.registry_loader import QuestionRegistryLoader

class PreferencesManagerError(Exception):
    """Exception raised for validation errors in the Preferences Manager."""
    pass

class PreferencesManager:
    """
    Manages lightweight persistence for Favorites and Recent Questions.
    Ensures safe validation against the canonical Question Registry.
    """
    def __init__(self, loader: Optional[QuestionRegistryLoader] = None, file_path: str = None):
        self.loader = loader or QuestionRegistryLoader()
        
        if file_path is None:
            # Default to a local JSON file in the database directory
            from app.core.paths import get_app_data_dir
            file_path = str(get_app_data_dir() / 'user_preferences.json')
            
        self.file_path = file_path
        
        # Ensure database directory exists
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self._load_data()

    def _load_data(self):
        if not os.path.exists(self.file_path):
            self.data = {"favorites": [], "recents": []}
            self._save_data()
        else:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                try:
                    self.data = json.load(f)
                except json.JSONDecodeError:
                    self.data = {"favorites": [], "recents": []}

    def _save_data(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)

    def _validate_question_id(self, question_id: str) -> Dict[str, Any]:
        """Validates that a question_id actually exists in the Source of Truth."""
        if not question_id or not isinstance(question_id, str):
            raise PreferencesManagerError("question_id must be a valid non-empty string.")
        
        record = self.loader.get_question(question_id)
        if not record:
            raise PreferencesManagerError(f"Invalid registry reference: question_id '{question_id}' not found.")
        return record

    # --- Favorites ---

    def add_favorite(self, question_id: str) -> dict:
        record = self._validate_question_id(question_id)
        
        # Prevent duplicates
        for fav in self.data["favorites"]:
            if fav["question_id"] == question_id:
                raise PreferencesManagerError(f"question_id '{question_id}' is already in favorites.")
                
        new_fav = {
            "question_id": question_id,
            "question_name": record.get("question_name", "Unknown Question"),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        self.data["favorites"].append(new_fav)
        self._save_data()
        return new_fav

    def remove_favorite(self, question_id: str) -> bool:
        if not question_id:
            raise PreferencesManagerError("question_id cannot be empty.")
            
        initial_len = len(self.data["favorites"])
        self.data["favorites"] = [f for f in self.data["favorites"] if f["question_id"] != question_id]
        
        if len(self.data["favorites"]) == initial_len:
            raise PreferencesManagerError(f"question_id '{question_id}' not found in favorites.")
            
        self._save_data()
        return True

    def list_favorites(self) -> List[dict]:
        return self.data["favorites"]

    # --- Recent Questions ---

    def add_recent(self, question_id: str) -> dict:
        record = self._validate_question_id(question_id)
        
        # If it already exists, remove it so it bubbles to the top
        self.data["recents"] = [r for r in self.data["recents"] if r["question_id"] != question_id]
        
        new_recent = {
            "question_id": question_id,
            "question_name": record.get("question_name", "Unknown Question"),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        # Prepend to front (newest first)
        self.data["recents"].insert(0, new_recent)
        
        # Enforce retention limit (10 items)
        self.data["recents"] = self.data["recents"][:10]
        
        self._save_data()
        return new_recent

    def list_recents(self) -> List[dict]:
        return self.data["recents"]

import json
import os
from pathlib import Path
from .calibration_types import CalibrationProfile

class CalibrationRegistry:
    """
    Loads and serves available calibration profiles.
    """
    
    def __init__(self, profiles_dir: str = None):
        if profiles_dir is None:
            # Default to the 'profiles' directory alongside this file
            profiles_dir = os.path.join(os.path.dirname(__file__), "profiles")
        self.profiles_dir = Path(profiles_dir)
        self._profiles = {}
        self._load_all_profiles()

    def _load_all_profiles(self):
        if not self.profiles_dir.exists():
            return
            
        for filepath in self.profiles_dir.glob("*.json"):
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    profile_id = data.get("metadata", {}).get("profile_id")
                    if profile_id:
                        self._profiles[profile_id] = CalibrationProfile(**data)
                except Exception as e:
                    print(f"Warning: Failed to load profile {filepath}: {e}")

    def get_profile(self, profile_id: str) -> CalibrationProfile:
        if profile_id not in self._profiles:
            raise ValueError(f"Calibration profile '{profile_id}' not found.")
        return self._profiles[profile_id]

    def list_profiles(self) -> list:
        return list(self._profiles.keys())

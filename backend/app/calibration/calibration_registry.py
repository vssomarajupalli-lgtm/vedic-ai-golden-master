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
                        # Transform new format (with sections) to CalibrationProfile format
                        profile_data = self._transform_profile_data(data)
                        self._profiles[profile_id] = CalibrationProfile(**profile_data)
                except Exception as e:
                    print(f"Warning: Failed to load profile {filepath}: {e}")
    
    def _transform_profile_data(self, data: dict) -> dict:
                    """Transform new sections-based format to CalibrationProfile format."""
                    sections = data.get("sections", {})
        
                    # Handle both old format (flat keys) and new format (sections dict)
                    if isinstance(sections, list) or not sections:
                        # Old format: sections is an empty list or missing, data has flat keys
                        # Extract directly from data
                        profile_data = {
                            "metadata": data.get("metadata", {}),
                            "sections": {},  # Empty sections for old format
                            "master_probability": data.get("master_probability", {}),
                            "planet_strength": data.get("planet_strength", {}),
                            "house_strength": data.get("house_strength", {}),
                            "rasi_strength": data.get("rasi_strength", {}),
                            "varga": data.get("varga", {}),
                            "dasha": data.get("dasha", {}),
                            "ashtakavarga": data.get("ashtakavarga", {}),
                            "natal_promise": data.get("natal_promise", {}),
                            "transit": data.get("transit", {}),
                        }
                    else:
                        # New format: sections is a dict with section details
                        profile_data = {
                            "metadata": data.get("metadata", {}),
                            "sections": sections,  # Include the full sections dict for CalibrationManager
                            "master_probability": sections.get("master_probability", {}).get("parameters", {}),
                            "planet_strength": sections.get("planet_strength", {}).get("parameters", {}),
                            "house_strength": sections.get("house_strength", {}).get("parameters", {}),
                            "rasi_strength": sections.get("rasi_strength", {}).get("parameters", {}),
                            "varga": sections.get("varga", {}).get("parameters", {}),
                            "dasha": sections.get("dasha", {}).get("parameters", {}),
                            "ashtakavarga": sections.get("ashtakavarga", {}).get("parameters", {}),
                            "natal_promise": sections.get("natal_promise", {}).get("parameters", {}),
                            "transit": sections.get("transit", {}).get("parameters", {}),
                        }
        
                    return profile_data
    
    def get_profile(self, profile_id: str) -> CalibrationProfile:
        if profile_id not in self._profiles:
            raise ValueError(f"Calibration profile '{profile_id}' not found.")
        return self._profiles[profile_id]
    
    def list_profiles(self) -> list:
        return list(self._profiles.keys())

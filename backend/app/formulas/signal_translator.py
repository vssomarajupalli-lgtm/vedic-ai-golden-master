from typing import Dict, Any, List

class SignalTranslator:
    """
    Acts as an adapter layer between the mathematical PipelineRunner structure 
    (e.g., houses["7"]) and the semantic Formula Registry strings (e.g., "7th_house").
    """
    
    PLANET_MAP = {
        "sun": "sun",
        "moon": "moon",
        "mars": "mars",
        "mercury": "mercury",
        "jupiter": "jupiter",
        "venus": "venus",
        "saturn": "saturn",
        "rahu": "rahu",
        "ketu": "ketu"
    }

    HOUSE_MAP = {
        "1st_house": "1",
        "2nd_house": "2",
        "3rd_house": "3",
        "4th_house": "4",
        "5th_house": "5",
        "6th_house": "6",
        "7th_house": "7",
        "8th_house": "8",
        "9th_house": "9",
        "10th_house": "10",
        "11th_house": "11",
        "12th_house": "12",
        "lagna": "1"
    }
    
    LORD_MAP = {
        "1st_lord": "1",
        "2nd_lord": "2",
        "3rd_lord": "3",
        "4th_lord": "4",
        "5th_lord": "5",
        "6th_lord": "6",
        "7th_lord": "7",
        "8th_lord": "8",
        "9th_lord": "9",
        "10th_lord": "10",
        "11th_lord": "11",
        "12th_lord": "12",
        "lagna_lord": "1"
    }

    @classmethod
    def translate(cls, required_signals: List[str], engine_outputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Translates structural pipeline payload into a flattened semantic dictionary.
        Returns isolated_signals directly, safely extracting rich planet/house data 
        using deterministic namespace routing.
        """
        isolated_signals = {}
        
        planets_data = engine_outputs.get("planets", {})
        houses_data = engine_outputs.get("houses", {})

        for signal in required_signals:
            # 1. Static Planet Mapping
            if signal in cls.PLANET_MAP:
                sanskrit_name = cls.PLANET_MAP[signal]
                if sanskrit_name in planets_data:
                    isolated_signals[signal] = planets_data[sanskrit_name]
                    
            # 2. Static House Mapping
            elif signal in cls.HOUSE_MAP:
                house_idx = cls.HOUSE_MAP[signal]
                if house_idx in houses_data:
                    isolated_signals[signal] = houses_data[house_idx]
                    
            # 3. Dynamic Lord Resolution
            elif signal in cls.LORD_MAP:
                house_idx = cls.LORD_MAP[signal]
                if house_idx in houses_data:
                    lord_name = houses_data[house_idx].get("metadata", {}).get("lord")
                    if lord_name and lord_name in planets_data:
                        isolated_signals[signal] = planets_data[lord_name]
                        
            # 4. Derived Signals (Stubs for future expansion)
            elif signal == "upapada_lagna":
                pass
            elif signal == "darakaraka":
                pass
                
        return isolated_signals

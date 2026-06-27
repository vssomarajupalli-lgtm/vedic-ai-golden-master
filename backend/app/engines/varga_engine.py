from typing import Dict, Any

from app.config.astrology_constants import D9_SCORES, D10_SCORES, VARGOTTAMA_BONUS
from app.engines.planet_strength_engine import PlanetStrengthEngine

class VargaEngine:
    """
    Varga Engine (Phase 5)
    Calculates structural refinements from D9 (Navamsha) and D10 (Dashamamsha).
    
    Adheres to the following Immutable Rules:
    - Stateless evaluation mapping.
    - Strict adherence to Standardized JSON Contract output.
    - Additive modifiers only (Immutable D1 Rule).
    """

    def __init__(self, calibration=None):
        if calibration is None:
            from app.calibration.calibration_manager import CalibrationManager
            calibration = CalibrationManager()
        # Load scoring constants from central config
        self.D9_SCORES = calibration.varga.get('D9_SCORES', {})
        self.D10_SCORES = calibration.varga.get('D10_SCORES', {})
        self.VARGOTTAMA_BONUS = calibration.varga.get('VARGOTTAMA_BONUS', 0)
        self.planet_engine = PlanetStrengthEngine()

    def evaluate(self, normalized_data: Dict[str, Any], dependency_scores: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluates Varga modifiers for all planets in the chart.
        Dependency scores are passed in via the PipelineRunner.
        """
        if dependency_scores is None:
            dependency_scores = {}

        results = {
            "D9": {"planets": {}},
            "D10": {"planets": {}}
        }
        planets = normalized_data.get("planets", {})
        vargas_data = normalized_data.get("vargas", {})

        for planet_name, planet_d1_data in planets.items():
            base_score = dependency_scores.get(planet_name, {}).get("final_score", 0.0)
            d1_dignity = planet_d1_data.get("dignity", "neutral").lower()

            # 1. Evaluate D9 (Navamsha)
            d9_data = vargas_data.get("D9", {}).get("planets", {}).get(planet_name, {})
            d9_dignity = d9_data.get("dignity", "neutral").lower().replace(" ", "_") if d9_data else "neutral"
            d9_score = self.D9_SCORES.get(d9_dignity, 0.0)
            
            modifiers = {}
            confidence_flags = []
            
            if d9_score != 0.0:
                modifiers["D9_dignity_modifier"] = d9_score
                confidence_flags.append(f"D9_{d9_dignity}")

            if d1_dignity == "exalted" and d9_dignity == "debilitated":
                confidence_flags.append("varga_contradicted")
            elif d1_dignity == "debilitated" and d9_dignity == "exalted":
                confidence_flags.append("neecha_bhanga_varga")

            if d9_data and d9_data.get("is_vargottama"):
                modifiers["D9_vargottama_bonus"] = self.VARGOTTAMA_BONUS
                confidence_flags.append("D9_vargottama")

            if d9_data:
                d9_strength_result = self.planet_engine.calculate_strength(d9_data, shadbala_data={})
                d9_final_score = float(d9_strength_result.get("final_score", 50.0))
                d9_breakdown = d9_strength_result.get("breakdown", {})
            else:
                d9_final_score = "Data Unavailable"
                d9_breakdown = {}

            results["D9"]["planets"][planet_name] = {
                "metadata": {
                    "entity_id": planet_name,
                    "entity_type": "planet"
                },
                "final_score": d9_final_score,
                "breakdown": d9_breakdown,
                "modifiers": modifiers,
                "temporal_activation": {},
                "confidence_flags": confidence_flags
            }

            # 2. Evaluate D10 (Dashamamsha)
            d10_data = vargas_data.get("D10", {}).get("planets", {}).get(planet_name, {})
            d10_dignity = d10_data.get("dignity", "neutral").lower().replace(" ", "_") if d10_data else "neutral"
            d10_score = self.D10_SCORES.get(d10_dignity, 0.0)
            
            modifiers = {}
            confidence_flags = []
            
            if d10_score != 0.0:
                modifiers["D10_dignity_modifier"] = d10_score
                confidence_flags.append(f"D10_{d10_dignity}")

            if d10_data:
                d10_strength_result = self.planet_engine.calculate_strength(d10_data, shadbala_data={})
                d10_final_score = float(d10_strength_result.get("final_score", 50.0))
                d10_breakdown = d10_strength_result.get("breakdown", {})
            else:
                d10_final_score = "Data Unavailable"
                d10_breakdown = {}

            results["D10"]["planets"][planet_name] = {
                "metadata": {
                    "entity_id": planet_name,
                    "entity_type": "planet"
                },
                "final_score": d10_final_score,
                "breakdown": d10_breakdown,
                "modifiers": modifiers,
                "temporal_activation": {},
                "confidence_flags": confidence_flags
            }

        return results
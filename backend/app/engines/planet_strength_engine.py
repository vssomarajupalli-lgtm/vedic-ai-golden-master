from app.config.astrology_constants import PLANET_SCORING_MATRIX
from app.utils.astrology_math import clamp_score
from app.utils.engine_provenance import build_engine_provenance, build_factor_provenance

class PlanetStrengthEngine:
    """
    Deterministic scoring engine for calculating planetary operational strength.
    Calculates a 0-100 score based on strict astrological rules.
    No AI reasoning is used in these calculations.
    """

    def __init__(self, calibration=None):
        if calibration is None:
            from app.calibration.calibration_manager import CalibrationManager
            calibration = CalibrationManager()
        # Load scoring constants from central config to improve maintainability
        self.scoring_matrix = calibration.planet_strength.get('PLANET_SCORING_MATRIX', {})
        self.calibration = calibration
        try:
            self.weights = calibration.active_profile.get("sections", {}).get("planet_strength", {}).get("parameters", {})
        except (KeyError, TypeError):
            self.weights = {}

    def _get_weight(self, param_name: str, default: float) -> float:
        return self.weights.get(param_name, {}).get("weight_pct", default * 100.0) / 100.0

    def calculate_strength(self, planet_data: dict, shadbala_data: dict = None) -> dict:
        """
        Calculates the overall strength of a planet.
        """
        breakdown = {}
        factor_provenance = {}

        # 1. Evaluate Dignity (25%)
        dignity_raw = self._evaluate_dignity(planet_data.get("dignity", "neutral"))
        dignity_weight = self._get_weight("dignity", 0.25)
        dignity_score = dignity_raw * dignity_weight
        breakdown["dignity"] = dignity_score
        factor_provenance["dignity"] = build_factor_provenance(dignity_raw, dignity_weight)

        # 2. Evaluate House Placement (20%)
        house_raw = self._evaluate_house(planet_data.get("house_type", "neutral"))
        house_weight = self._get_weight("house_placement", 0.20)
        house_score = house_raw * house_weight
        breakdown["house_placement"] = house_score
        factor_provenance["house_placement"] = build_factor_provenance(house_raw, house_weight)

        # 3. Evaluate Aspects (15%)
        aspect_raw = self._evaluate_aspects(
            planet_data.get("benefic_aspects_count", 0),
            planet_data.get("malefic_aspects_count", 0)
        )
        aspect_weight = self._get_weight("aspects", 0.15)
        aspect_score = aspect_raw * aspect_weight
        breakdown["aspects"] = aspect_score
        factor_provenance["aspects"] = build_factor_provenance(aspect_raw, aspect_weight)

        # 4. Evaluate Conjunctions (10%)
        conj_raw = self._evaluate_conjunctions(
            planet_data.get("benefic_conjunctions_count", 0),
            planet_data.get("malefic_conjunctions_count", 0)
        )
        conj_weight = self._get_weight("conjunctions", 0.10)
        conj_score = conj_raw * conj_weight
        breakdown["conjunctions"] = conj_score
        factor_provenance["conjunctions"] = build_factor_provenance(conj_raw, conj_weight)

        # 5. Evaluate Combustion (10%)
        is_combust = planet_data.get("is_combust", False)
        combust_raw = self.scoring_matrix["state_modifiers"]["combust_score"] if is_combust else 100
        combust_weight = self._get_weight("combustion", 0.10)
        combust_score = combust_raw * combust_weight
        breakdown["combustion"] = combust_score
        factor_provenance["combustion"] = build_factor_provenance(combust_raw, combust_weight)

        # 6. Evaluate Retrogression (5%)
        is_retro = planet_data.get("is_retrograde", False)
        retro_raw = self.scoring_matrix["state_modifiers"]["retrograde_score"] if is_retro else 50
        retro_weight = self._get_weight("retrogression", 0.05)
        retro_score = retro_raw * retro_weight
        breakdown["retrogression"] = retro_score
        factor_provenance["retrogression"] = build_factor_provenance(retro_raw, retro_weight)

        # 7. Evaluate Shadbala (10%)
        planet_name = planet_data.get("name", "unknown").lower()
        shadbala_info = None
        if shadbala_data and isinstance(shadbala_data, dict):
            shadbala_info = shadbala_data.get(planet_name)
        if shadbala_info and "required_percentage" in shadbala_info:
            req_pct = float(shadbala_info["required_percentage"])
            shadbala_raw = self._map_shadbala_to_score(req_pct)
        else:
            shadbala_raw = 50.0 # Neutral fallback
        shadbala_weight = self._get_weight("shadbala", 0.10)
        shadbala_score = shadbala_raw * shadbala_weight
        breakdown["shadbala"] = shadbala_score
        factor_provenance["shadbala"] = build_factor_provenance(shadbala_raw, shadbala_weight)

        # 8. Evaluate Varga Dignity (5%)
        varga_raw = 50.0 # Placeholder for D9 dignity extraction
        varga_weight = self._get_weight("varga_dignity", 0.05)
        varga_score = varga_raw * varga_weight
        breakdown["varga_dignity"] = varga_score
        factor_provenance["varga_dignity"] = build_factor_provenance(varga_raw, varga_weight)

        total_score = (dignity_score + house_score + aspect_score + conj_score + 
                       combust_score + retro_score + shadbala_score + varga_score)

        # Clamp final score between 0 and 100
        final_score = clamp_score(total_score)

        provenance = build_engine_provenance(
            self.calibration, "PlanetStrengthEngine", "calibration.planet_strength"
        )
        provenance["factors"] = factor_provenance

        return {
            "metadata": {
                "entity_id": planet_name,
                "entity_type": "planet",
                **provenance
            },
            "final_score": final_score,
            "raw_score": float(total_score),
            "breakdown": breakdown,
            "confidence_flags": self._generate_confidence_flags(total_score, final_score)
        }

    # --- Isolated Helper Methods ---

    def _evaluate_dignity(self, dignity: str) -> float:
        key = dignity.lower().replace(" ", "_")
        return float(self.scoring_matrix["dignity"].get(key, self.scoring_matrix["dignity"]["neutral"]))

    def _evaluate_house(self, house_type: str) -> float:
        key = house_type.lower().replace(" ", "_")
        return float(self.scoring_matrix["house_placement"].get(key, self.scoring_matrix["house_placement"]["neutral"]))

    def _evaluate_aspects(self, benefic_count: int, malefic_count: int) -> float:
        raw = 50.0 + (benefic_count * self.scoring_matrix["aspects"]["benefic_aspect"]) + (malefic_count * self.scoring_matrix["aspects"]["malefic_aspect"])
        return max(0.0, min(100.0, raw))

    def _evaluate_conjunctions(self, benefic_count: int, malefic_count: int) -> float:
        raw = 50.0 + (benefic_count * self.scoring_matrix.get("conjunctions", {}).get("benefic_conjunction", 25)) + (malefic_count * self.scoring_matrix.get("conjunctions", {}).get("malefic_conjunction", -25))
        return max(0.0, min(100.0, raw))

    def _map_shadbala_to_score(self, req_pct: float) -> float:
        """
        Maps Shadbala required_percentage to the [0, 100] internal probability scale.
        Anchors:
            >= 160 -> 100
            140 -> 80
            120 -> 65
            100 -> 50
            80 -> 35
            <= 40 -> 0
        """
        anchors = [
            (0, 0),
            (40, 0),
            (80, 35),
            (100, 50),
            (120, 65),
            (140, 80),
            (160, 100)
        ]
        
        if req_pct <= anchors[1][0]:
            return anchors[1][1]
        elif req_pct >= anchors[-1][0]:
            return anchors[-1][1]
            
        for i in range(len(anchors) - 1):
            lo_p, lo_s = anchors[i]
            hi_p, hi_s = anchors[i + 1]
            if lo_p <= req_pct <= hi_p:
                t = (req_pct - lo_p) / (hi_p - lo_p)
                return lo_s + t * (hi_s - lo_s)
        return 50.0

    # --- Future Extensibility Stubs ---

    def _evaluate_ashtakavarga(self, bav_points: int) -> int:
        """Stub for future Phase integration of Bhinna Ashtakavarga support."""
        pass

    def _evaluate_varga_support(self, varga_data: dict) -> int:
        """Stub for future Phase integration of D9/Varga manifestation refinement."""
        pass

    def _generate_confidence_flags(self, raw_score: float, final_score: int) -> list:
        """Generates debug and synthesis flags based on the score."""
        flags = []
        if raw_score < 0:
            flags.append("clamped_to_zero")
            flags.append("severely_afflicted")
        elif raw_score > 100:
            flags.append("clamped_to_100")
        elif raw_score > 75:
            flags.append("highly_dignified")
        return flags
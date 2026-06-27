from typing import Any, Dict, List, Union
from app.utils.astrology_math import clamp_score

_NEUTRAL = 50.0

class NatalPromiseEngine:
    """
    Deterministic natal promise scoring engine.

    Evaluates the birth chart promise for 8 life domains using a
    strict 4-pillar weighted formula per domain:

        bhava          × 0.35   (HouseStrengthEngine)
        bhavadhipati   × 0.30   (PlanetStrengthEngine lord of primary house)
        karaka         × 0.20   (PlanetStrengthEngine natural significator)
        varga          × 0.15   (VargaEngine domain-specific chart)

    Architecture Rules:
        - No Double Penalty Rule: Afflictions are evaluated strictly inside Planet/House engines.
        - Zero astrological recalculation. Consumes pre-computed scores only.
        - No AI/ML. Pure arithmetic.
    """

    def __init__(self, calibration=None):
        if calibration is None:
            from app.calibration.calibration_manager import CalibrationManager
            calibration = CalibrationManager()
        self.config   = calibration.natal_promise.get("DOMAIN_CONFIG", {})
        self.domains  = list(self.config.keys())
        self.karaka   = calibration.natal_promise.get("DOMAIN_KARAKA", {})
        self.grades   = calibration.natal_promise.get("NATAL_PROMISE_GRADES", [])
        self.bonuses  = calibration.natal_promise.get("DOMAIN_BONUSES", {})
        self.sign_lord_map = calibration.rasi_strength.get("SIGN_LORD_MAP", {})

    def evaluate(
        self,
        planet_results:    Dict[str, Any],
        house_results:     Dict[str, Any],
        rasi_results:      Dict[str, Any],
        varga_results:     Dict[str, Any],
        av_results:        Dict[str, Any],
        yoga_results:      Dict[str, Any],
        normalized_houses: Dict[str, Any],
        normalized_vargas: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Evaluates natal promise for all 8 domains.
        """
        if normalized_vargas is None:
            normalized_vargas = {}
        result = {}
        for domain in self.domains:
            result[domain] = self._score_domain(
                domain, planet_results, house_results,
                varga_results, normalized_houses, yoga_results, normalized_vargas
            )
        print("NatalPromiseEngine output sample (Marriage):", result.get("marriage", {}).get("score"))
        return result

    def _score_domain(
        self,
        domain:            str,
        planet_results:    dict,
        house_results:     dict,
        varga_results:     dict,
        normalized_houses: dict,
        yoga_results:      dict,
        normalized_vargas: dict,
    ) -> dict:
        cfg     = self.config[domain]
        weights = cfg["weights"]

        # --- Pillar 1: Bhava Strength (35%) ---
        primary_houses = cfg["primary_house"]
        f_bhava, primary_house_key = self._primary_house_score(
            primary_houses, house_results
        )

        # --- Pillar 2: Bhavadhipati Strength (30%) ---
        f_bhavadhipati = self._lord_score(
            primary_house_key, normalized_houses, planet_results
        )

        # --- Pillar 3: Karaka Strength (20%) ---
        karaka_cfg = self.karaka[domain]
        f_karaka = self._karaka_score(
            karaka_cfg["primary"], karaka_cfg.get("secondary"), planet_results, domain
        )

        # --- Pillar 4: Varga Validation (15%) ---
        varga_id = cfg["varga"]
        f_varga = self._varga_score(
            varga_id,
            varga_results,
            karaka_cfg["primary"]
        )

        # --- Weighted sum ---
        raw = (
            weights["bhava"]        * f_bhava +
            weights["bhavadhipati"] * f_bhavadhipati +
            weights["karaka"]       * f_karaka  +
            weights["varga"]        * f_varga
        )

        score   = clamp_score(round(raw))
        promise = self._promise_grade(score)

        return {
            "score":   score,
            "raw_score": round(raw, 4),
            "promise": promise,
            "breakdown": {
                "bhava":          round(f_bhava, 2),
                "bhavadhipati":   round(f_bhavadhipati, 2),
                "karaka":         round(f_karaka,  2),
                "varga":          round(f_varga,   2),
            },
            "primary_house": primary_house_key,
            "varga_chart":   varga_id,
            "karaka":        karaka_cfg["primary"],
            "afflictions":   [], # Afflictions are now handled inside the respective planet/house engines
        }

    # -------------------------------------------------------------------------
    # Factor Computations
    # -------------------------------------------------------------------------

    def _primary_house_score(
        self,
        primary_house: Union[str, List[str]],
        house_results: dict
    ):
        if isinstance(primary_house, list):
            scores = [
                house_results.get(h, {}).get("final_score", _NEUTRAL)
                for h in primary_house
            ]
            avg = sum(scores) / len(scores) if scores else _NEUTRAL
            return avg, primary_house[0]
        else:
            score = house_results.get(primary_house, {}).get("final_score", _NEUTRAL)
            return score, primary_house

    def _karaka_score(
        self,
        primary_karaka:   str,
        secondary_karaka: str,
        planet_results:   dict,
        domain:           str,
    ) -> float:
        p_score = planet_results.get(primary_karaka, {}).get("final_score", _NEUTRAL)

        if secondary_karaka is None:
            return p_score

        s_score = planet_results.get(secondary_karaka, {}).get("final_score", _NEUTRAL)

        blend = {
            "career":      max(p_score, (p_score + s_score) / 2),
            "education":   0.60 * p_score + 0.40 * s_score,
            "children":    0.70 * p_score + 0.30 * s_score,
            "property":    0.60 * p_score + 0.40 * s_score,
            "health":      0.60 * p_score + 0.40 * s_score,
        }
        return blend.get(domain, p_score)

    def _lord_score(
        self,
        primary_house_key: str,
        normalized_houses: dict,
        planet_results:    dict,
    ) -> float:
        lord = normalized_houses.get(primary_house_key, {}).get("lord", "")
        if not lord or lord not in planet_results:
            return _NEUTRAL
        return planet_results[lord].get("final_score", _NEUTRAL)

    def _varga_score(
        self,
        varga_id:      str,
        varga_results: dict,
        primary_karaka: str,
    ) -> float:
        varga_planets = varga_results.get(varga_id, {}).get("planets", {})
        karaka_data = varga_planets.get(primary_karaka, {})
        return float(karaka_data.get("final_score", _NEUTRAL))

    def _promise_grade(self, score: int) -> str:
        for threshold, label in self.grades:
            if score >= threshold:
                return label
        return "PRESENT"


from app.config.astrology_constants import (
    SAV_BINDU_SCALE,
    BAV_GRADE_THRESHOLDS,
    BAV_PLANET_MODIFIER,
    SAV_FAVORABLE_THRESHOLD,
    SAV_STRONG_THRESHOLD,
    SAV_WEAK_THRESHOLD,
    DASHA_BAV_CONFIDENCE,
    BAV_EXCLUDED_PLANETS,
    BAV_PLANETS,
    SIGNS_IN_ORDER
)
from app.utils.astrology_math import clamp_score


class AshtakavargaEngine:
    """
    Deterministic Ashtakavarga scoring engine.

    Processes extracted BAV (Bhinnashtakavarga) and SAV (Sarvashtakavarga)
    bindu data from canonical_content.json.

    Produces:
        1. BAV chart with grade per house per planet
        2. SAV chart with normalized score per house
        3. Planet BAV support modifiers (injected into PlanetStrengthEngine)
        4. Dasha lord BAV support and timing confidence multiplier
        5. SAV analytics (totals, peaks, favorable/unfavorable classification)
        6. Cross-engine modifier summary

    Architecture Rules:
        - Zero astrological recalculation. (Rule 4)
        - Reads SAV/BAV as extracted values; does NOT recompute from positions.
        - BAV consistency check raises a flag but does NOT override either value.
        - Rahu/Ketu excluded from BAV (classical Parashari standard).
        - All constants in astrology_constants.py.
    """

    def __init__(self, calibration=None):
        if calibration is None:
            from app.calibration.calibration_manager import CalibrationManager
            calibration = CalibrationManager()
        self.sav_scale         = calibration.rasi_strength.get('SAV_BINDU_SCALE', {})
        self.bav_grade_map     = calibration.ashtakavarga.get('BAV_GRADE_THRESHOLDS', {})
        self.planet_modifier   = calibration.ashtakavarga.get('BAV_PLANET_MODIFIER', {})
        self.dasha_confidence  = calibration.ashtakavarga.get('DASHA_BAV_CONFIDENCE', 0)
        self.excluded_planets  = calibration.ashtakavarga.get('BAV_EXCLUDED_PLANETS', [])
        self.bav_planets       = calibration.ashtakavarga.get('BAV_PLANETS', [])

    # -------------------------------------------------------------------------
    # Public Interface
    # -------------------------------------------------------------------------

    def evaluate(
        self,
        normalized_payload: dict,
        dependency_scores: dict = None
    ) -> dict:
        """
        Evaluates complete Ashtakavarga analysis.

        Args:
            normalized_payload (dict): Full JsonNormalizer output.
                Required keys: "ashtakavarga", "planets", "dashas", "metadata"
            dependency_scores (dict): PlanetStrengthEngine outputs.
                Keyed by planet system name → {"final_score": int}

        Returns:
            dict: Full AV analysis payload (see module docstring).
        """
        dependency_scores  = dependency_scores or {}
        av_data            = normalized_payload.get("ashtakavarga", {})
        normalized_planets = normalized_payload.get("planets", {})
        normalized_dashas  = normalized_payload.get("dashas", {})
        
        asc_sign           = normalized_payload.get("metadata", {}).get("ascendant_sign", "aries").lower()

        raw_sav = av_data.get("sav_chart",  {})
        raw_bav = av_data.get("bav_charts", {})

        # --- Core computations ---
        bav_charts_out     = self._build_bav_charts(raw_bav, asc_sign)
        sav_chart_out      = self._build_sav_chart(raw_sav, asc_sign)
        planet_bav_support = self._compute_planet_bav_support(
            normalized_planets, raw_bav, dependency_scores
        )
        dasha_bav_support  = self._compute_dasha_bav_support(
            normalized_dashas, normalized_planets, raw_bav
        )
        sav_analytics      = self._compute_sav_analytics(raw_sav, raw_bav, asc_sign)
        engine_modifiers   = self._build_engine_modifiers(
            planet_bav_support, dasha_bav_support
        )

        return {
            "bav_charts":        bav_charts_out,
            "sav_chart":         sav_chart_out,
            "planet_bav_support": planet_bav_support,
            "dasha_bav_support": dasha_bav_support,
            "sav_analytics":     sav_analytics,
            "engine_modifiers":  engine_modifiers
        }

    # -------------------------------------------------------------------------
    # Coordinate Mapping Helper
    # -------------------------------------------------------------------------
    def _sign_to_house(self, sign: str, asc_sign: str) -> int:
        """Translates a zodiac sign to a relative house based on the ascendant."""
        try:
            s_idx = SIGNS_IN_ORDER.index(sign)
            a_idx = SIGNS_IN_ORDER.index(asc_sign)
            return ((s_idx - a_idx + 12) % 12) + 1
        except ValueError:
            return 1

    # -------------------------------------------------------------------------
    # BAV Charts
    # -------------------------------------------------------------------------

    def _build_bav_charts(self, raw_bav: dict, asc_sign: str) -> dict:
        """
        Builds the annotated BAV chart for each of the 7 classical planets.
        Converts extracted sign keys to relative house numbers for downstream compatibility.
        """
        result = {}
        for planet in self.bav_planets:
            if planet not in raw_bav:
                continue
            sign_data = raw_bav[planet]
            planet_chart = {}
            # Ensure all 12 houses are represented
            for house_num in range(1, 13):
                planet_chart[str(house_num)] = {"bindus": 0, "grade": "CRITICAL"}
                
            for sign, bindus in sign_data.items():
                house = self._sign_to_house(sign, asc_sign)
                b = int(bindus)
                planet_chart[str(house)] = {
                    "bindus": b,
                    "grade":  self._bav_grade(b)
                }
            result[planet] = planet_chart
        return result

    # -------------------------------------------------------------------------
    # SAV Chart
    # -------------------------------------------------------------------------

    def _build_sav_chart(self, raw_sav: dict, asc_sign: str) -> dict:
        """
        Builds the annotated SAV chart for all 12 houses.
        Converts extracted sign keys to relative house numbers.
        """
        result = {}
        for house_num in range(1, 13):
            result[str(house_num)] = {
                "bindus": 0, "score": 0.0, "grade": "CRITICAL",
                "is_favorable": False, "is_strong": False, "is_weak": True
            }
            
        for sign, bindus_raw in raw_sav.items():
            house = self._sign_to_house(sign, asc_sign)
            bindus = int(bindus_raw)
            score = self._sav_score(bindus)
            result[str(house)] = {
                "bindus":       bindus,
                "score":        round(score, 2),
                "grade":        self._sav_grade(bindus),
                "is_favorable": bindus >= SAV_FAVORABLE_THRESHOLD,
                "is_strong":    bindus >= SAV_STRONG_THRESHOLD,
                "is_weak":      bindus < SAV_WEAK_THRESHOLD
            }
        return result

    # -------------------------------------------------------------------------
    # Planet BAV Support
    # -------------------------------------------------------------------------

    def _compute_planet_bav_support(
        self,
        normalized_planets: dict,
        raw_bav: dict,
        dependency_scores: dict
    ) -> dict:
        """
        For each of the 7 BAV planets, computes support directly from the planet's sign.
        """
        result = {}
        for planet in self.bav_planets:
            planet_data = normalized_planets.get(planet, {})
            sign        = planet_data.get("sign", "")
            house       = int(planet_data.get("house", 0))

            planet_bav  = raw_bav.get(planet, {})
            if planet_bav and sign in planet_bav:
                bindus = int(planet_bav[sign])
            elif house > 0:
                bindus = 4  # sign not found in chart
            elif house == 0:
                bindus = 4  # unknown placement
            else:
                bindus = 4  

            score    = self._bav_score(bindus)
            grade    = self._bav_grade(bindus)
            modifier = self._bav_modifier(bindus)

            result[planet] = {
                "house":    house,
                "bindus":   bindus,
                "score":    round(score, 2),
                "grade":    grade,
                "modifier": modifier
            }
        return result

    # -------------------------------------------------------------------------
    # Dasha BAV Support
    # -------------------------------------------------------------------------

    def _compute_dasha_bav_support(
        self,
        normalized_dashas: dict,
        normalized_planets: dict,
        raw_bav: dict
    ) -> dict:
        md_lord = normalized_dashas.get("mahadasha", {}).get("lord", "")
        ad_lord = normalized_dashas.get("antardasha", {}).get("lord", "")

        md_data = self._single_dasha_bav(md_lord, normalized_planets, raw_bav)
        ad_data = self._single_dasha_bav(ad_lord, normalized_planets, raw_bav)

        combined = round(0.60 * md_data["score"] + 0.40 * ad_data["score"], 2)
        combined_confidence  = self._confidence_label(combined)
        combined_multiplier  = self.dasha_confidence[combined_confidence]

        return {
            "mahadasha":                   md_data,
            "antardasha":                  ad_data,
            "combined_dasha_bav_score":    combined,
            "timing_confidence":           combined_confidence,
            "timing_confidence_multiplier": combined_multiplier
        }

    def _single_dasha_bav(
        self,
        lord: str,
        normalized_planets: dict,
        raw_bav: dict
    ) -> dict:
        if not lord or lord in self.excluded_planets:
            return {
                "lord": lord, "house": 0,
                "bindus": 4, "score": 50.0,
                "grade": "AVERAGE", "timing_confidence": "moderate"
            }

        planet_data = normalized_planets.get(lord, {})
        house       = int(planet_data.get("house", 0))
        sign        = planet_data.get("sign", "")

        planet_bav = raw_bav.get(lord, {})
        bindus     = int(planet_bav.get(sign, 4)) if (planet_bav and sign) else 4
        score      = self._bav_score(bindus)
        grade      = self._bav_grade(bindus)
        confidence = self._confidence_label(score)

        return {
            "lord":              lord,
            "house":             house,
            "bindus":            bindus,
            "score":             round(score, 2),
            "grade":             grade,
            "timing_confidence": confidence
        }

    # -------------------------------------------------------------------------
    # SAV Analytics
    # -------------------------------------------------------------------------

    def _compute_sav_analytics(self, raw_sav: dict, raw_bav: dict, asc_sign: str) -> dict:
        """
        Computes aggregate SAV statistics.
        Calculations must be mapped back to house outputs for downstream engines.
        """
        totals = {}
        for h in range(1, 13):
            totals[str(h)] = 0
            
        for sign, bindus in raw_sav.items():
            h = str(self._sign_to_house(sign, asc_sign))
            totals[h] = int(bindus)

        total_bindus   = sum(totals.values())
        avg_per_house  = round(total_bindus / 12, 2)
        peak_house     = max(totals, key=totals.get) if totals else "1"
        weakest_house  = min(totals, key=totals.get) if totals else "1"
        favorable      = [h for h, b in totals.items() if b >= SAV_FAVORABLE_THRESHOLD]
        unfavorable    = [h for h, b in totals.items() if b < SAV_WEAK_THRESHOLD]

        # BAV consistency check: sum(BAV per house for 7 planets) vs SAV
        consistency = {}
        for sign in SIGNS_IN_ORDER:
            h = str(self._sign_to_house(sign, asc_sign))
            bav_sum = sum(
                int(raw_bav.get(p, {}).get(sign, 0))
                for p in self.bav_planets
            )
            sav_val = totals[h]
            consistency[h] = {
                "bav_sum":    bav_sum,
                "sav_val":    sav_val,
                "consistent": bav_sum == sav_val
            }

        all_consistent = all(v["consistent"] for v in consistency.values())

        return {
            "total_bindus":        total_bindus,
            "average_per_house":   avg_per_house,
            "peak_house":          peak_house,
            "weakest_house":       weakest_house,
            "favorable_houses":    sorted(favorable, key=int),
            "unfavorable_houses":  sorted(unfavorable, key=int),
            "bav_consistency_check": all_consistent,
            "house_consistency":   consistency
        }

    # -------------------------------------------------------------------------
    # Engine Modifier Summary
    # -------------------------------------------------------------------------

    def _build_engine_modifiers(
        self,
        planet_bav_support: dict,
        dasha_bav_support:  dict
    ) -> dict:
        planet_adjustments = {
            planet: data["modifier"]
            for planet, data in planet_bav_support.items()
        }

        return {
            "planet_score_adjustments":      planet_adjustments,
            "dasha_bav_confidence_multiplier": dasha_bav_support.get(
                "timing_confidence_multiplier", 1.0
            )
        }

    # -------------------------------------------------------------------------
    # Scoring Helpers
    # -------------------------------------------------------------------------

    def _bav_score(self, bindus: int) -> float:
        return round((bindus / 8) * 100, 2)

    def _sav_score(self, bindus: int) -> float:
        anchors = self.sav_scale
        if bindus <= anchors[0][0]:
            return float(anchors[0][1])
        if bindus >= anchors[-1][0]:
            return float(anchors[-1][1])
        for i in range(len(anchors) - 1):
            lo_b, lo_s = anchors[i]
            hi_b, hi_s = anchors[i + 1]
            if lo_b <= bindus <= hi_b:
                t = (bindus - lo_b) / (hi_b - lo_b)
                return lo_s + t * (hi_s - lo_s)
        return 50.0

    def _bav_grade(self, bindus: int) -> str:
        for threshold, grade in self.bav_grade_map:
            if bindus >= threshold:
                return grade
        return "CRITICAL"

    def _sav_grade(self, bindus: int) -> str:
        if bindus >= SAV_STRONG_THRESHOLD:    return "STRONG"
        if bindus >= SAV_FAVORABLE_THRESHOLD: return "FAVORABLE"
        if bindus >= SAV_WEAK_THRESHOLD:      return "AVERAGE"
        if bindus > 0:                        return "WEAK"
        return "CRITICAL"

    def _bav_modifier(self, bindus: int) -> int:
        if bindus >= 5:  return self.planet_modifier["high"]
        if bindus == 4:  return self.planet_modifier["neutral"]
        return self.planet_modifier["low"]

    def _confidence_label(self, score: float) -> str:
        if score >= 62.5:  return "high"
        if score >= 50.0:  return "moderate"
        return "low"

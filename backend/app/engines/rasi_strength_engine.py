from app.config.astrology_constants import (
    SIGN_LORD_MAP,
    SIGNS_IN_ORDER,
    SAV_BINDU_SCALE,
    RASI_SCORING_MATRIX,
    PROBABILITY_GRADES,
    NATURAL_BENEFICS,
    NATURAL_MALEFICS
)
from app.utils.astrology_math import clamp_score


class RasiStrengthEngine:
    """
    Deterministic scoring engine for the strength of all 12 zodiac signs (Rasis).

    Evaluates each sign's environmental quality using six independent factors:
        A. SAV Environment     (35%) — Sarvashtakavarga bindu support
        B. Sign Lord Strength  (25%) — Pre-calculated lord planet score
        C. Occupant Quality    (20%) — Strength-weighted benefic/malefic occupants
        D. Benefic/Malefic Balance (10%) — Count-based nature impact + aspects
        E. Dignity Impact       (5%) — Exaltation/debilitation of occupant planets
        F. Varga Validation     (5%) — D9/D10 dignity of occupants

    Architecture Rules:
        - Zero astrological recalculation — consumes pre-computed dependency_scores only. (Rule 4)
        - Stateless — no runtime state retained between calls. (Rule 4)
        - Pure stdlib — no ML/AI. (Rules 2, 10)
        - All scoring constants sourced from astrology_constants.py. (Rule 7)
    """

    def __init__(self, calibration=None):
        if calibration is None:
            from app.calibration.calibration_manager import CalibrationManager
            calibration = CalibrationManager()
        self.matrix     = calibration.rasi_strength.get('RASI_SCORING_MATRIX', {})
        self.benefics   = set(calibration.planet_strength.get('NATAL_BENEFICS', []))
        self.malefics   = set(calibration.planet_strength.get('NATAL_MALEFICS', []))
        self.calibration = calibration
        try:
            self.weights = calibration.active_profile.get("sections", {}).get("rasi_strength", {}).get("parameters", {})
        except (KeyError, TypeError):
            self.weights = {}

    def _get_weight(self, param_name: str, default: float) -> float:
        return self.weights.get(param_name, {}).get("weight_pct", default * 100.0) / 100.0

    # -------------------------------------------------------------------------
    # Public Interface
    # -------------------------------------------------------------------------

    def evaluate(
        self,
        normalized_payload: dict,
        dependency_scores: dict = None,
        varga_outputs: dict = None
    ) -> dict:
        """
        Evaluates Rasi strength for all 12 signs.

        Args:
            normalized_payload (dict): Full JsonNormalizer output.
                Required keys: "planets", "houses", "metadata"
            dependency_scores (dict): Output from PlanetStrengthEngine.
                Keyed by planet system name → {"final_score": int}
            varga_outputs (dict): Output from VargaEngine.
                Keyed by varga ID ("D9", "D10") → {"planets": {...}}

        Returns:
            dict: Keyed by sign name (English lowercase). Each value is a
                  fully explainable score payload.
        """
        dependency_scores = dependency_scores or {}
        varga_outputs     = varga_outputs or {}

        normalized_planets = normalized_payload.get("planets", {})
        normalized_houses  = normalized_payload.get("houses", {})
        ascendant_sign     = normalized_payload.get("metadata", {}).get("ascendant_sign", "aries")

        # Pre-build sign→occupant map (one pass, avoids O(n²) inner loops)
        sign_occupants = self._build_sign_occupant_map(normalized_planets)

        results = {}
        for sign in SIGNS_IN_ORDER:
            occupants   = sign_occupants.get(sign, [])
            house_num   = self._sign_to_house(sign, ascendant_sign)
            house_data  = normalized_houses.get(str(house_num), {})
            sav_bindus  = house_data.get("sav_points", 0)
            lord        = SIGN_LORD_MAP[sign]

            # --- Calculate each factor independently ---
            factor_a = self._factor_sav(sav_bindus)
            factor_b = self._factor_lord(lord, dependency_scores)
            factor_c = self._factor_occupant_quality(occupants, dependency_scores)
            factor_d = self._factor_balance(occupants, normalized_planets)
            factor_e = self._factor_dignity(sign, lord, occupants, normalized_planets)
            factor_f = self._factor_varga(occupants, varga_outputs)

            # --- Composite weighted formula ---
            raw = (
                self._get_weight("sav_bindus", 0.35) * factor_a +
                self._get_weight("sign_lord", 0.25) * factor_b +
                self._get_weight("occupant_quality", 0.20) * factor_c +
                self._get_weight("occupant_balance", 0.10) * factor_d +
                self._get_weight("dignity_impact", 0.05) * factor_e +
                self._get_weight("varga_refinement", 0.05) * factor_f
            )

            final_score = clamp_score(round(raw))

            results[sign] = {
                "metadata": {
                    "entity_id":   sign,
                    "entity_type": "rasi",
                    "lord":        lord,
                    "house_num":   house_num,
                    "occupants":   [p["name"] for p in occupants]
                },
                "final_score": final_score,
                "grade":       self._grade(final_score),
                "raw_score":   round(raw, 2),
                "breakdown": {
                    "sav_bindus":     sav_bindus,
                    "sav_score":      round(factor_a, 2),
                    "lord_score":     round(factor_b, 2),
                    "occupant_score": round(factor_c, 2),
                    "balance_score":  round(factor_d, 2),
                    "dignity_score":  round(factor_e, 2),
                    "varga_score":    round(factor_f, 2)
                },
                "modifiers": {
                    "varga_refinement": 0.0  # placeholder for pipeline-level wiring
                },
                "confidence_flags": self._flags(sign, lord, dependency_scores, sav_bindus, occupants)
            }

        return results

    # -------------------------------------------------------------------------
    # Factor A — SAV Environment (35%)
    # -------------------------------------------------------------------------

    def _factor_sav(self, bindus: int) -> float:
        """
        Piecewise linear interpolation of SAV bindus → 0-100 score.
        Anchor points from VEDIC_AI_MASTER_ARCHITECTURE.md.
        """
        anchors = SAV_BINDU_SCALE

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

        return 50.0  # unreachable — safety fallback

    # -------------------------------------------------------------------------
    # Factor B — Sign Lord Strength (25%)
    # -------------------------------------------------------------------------

    def _factor_lord(self, lord: str, dependency_scores: dict) -> float:
        """
        Reads the pre-computed planet strength score for this sign's ruling lord.
        Never re-calculates — consumes PlanetStrengthEngine output directly.
        Default 50 (neutral) if lord is missing from dependency_scores.
        """
        return float(
            dependency_scores.get(lord, {}).get("final_score",
                self.matrix["default_lord_score"])
        )

    # -------------------------------------------------------------------------
    # Factor C — Occupant Quality (20%)
    # -------------------------------------------------------------------------

    def _factor_occupant_quality(self, occupants: list, dependency_scores: dict) -> float:
        """
        Strength-weighted benefic/malefic occupant score.

        Benefic planet  → contribution = planet final_score  (high strength helps sign)
        Malefic planet  → contribution = 100 - planet final_score  (high strength damages sign)

        Empty sign → 50 (neutral baseline — empty ≠ afflicted)
        """
        if not occupants:
            return float(self.matrix["empty_sign_baseline"])

        contributions = []
        for p in occupants:
            name  = p["name"]
            score = float(dependency_scores.get(name, {}).get("final_score", 50))
            if name in self.benefics:
                contributions.append(score)
            else:
                contributions.append(100.0 - score)

        return sum(contributions) / len(contributions)

    # -------------------------------------------------------------------------
    # Factor D — Benefic / Malefic Balance (10%)
    # -------------------------------------------------------------------------

    def _factor_balance(self, occupants: list, normalized_planets: dict) -> float:
        """
        Count-based nature impact from occupants and aspects into the sign.

        Each benefic occupant: +10
        Each malefic occupant: -10
        Each benefic aspector: +5  (capped at ±10 total from aspects)
        Each malefic aspector: -5  (capped at ±10 total from aspects)

        Empty sign → 50 (neutral)
        """
        if not occupants:
            return float(self.matrix["empty_sign_baseline"])

        mods = self.matrix["occupant_modifiers"]
        balance = 50.0

        # Occupant nature contribution
        for p in occupants:
            name = p["name"]
            if name in self.benefics:
                balance += mods["benefic"]
            else:
                balance += mods["malefic"]

        # Aspect contribution — collect all aspectors for planets in this sign
        aspect_mod = 0.0
        seen_aspectors = set()
        for p in occupants:
            for aspector in normalized_planets.get(p["name"], {}).get("aspected_by", []):
                if aspector not in seen_aspectors:
                    seen_aspectors.add(aspector)
                    if aspector in self.benefics:
                        aspect_mod += mods["benefic_aspect"]
                    elif aspector in self.malefics:
                        aspect_mod += mods["malefic_aspect"]

        # Cap aspect contribution
        cap = mods["aspect_cap"]
        balance += max(-cap, min(cap, aspect_mod))

        return float(clamp_score(balance))

    # -------------------------------------------------------------------------
    # Factor E — Dignity Impact (5%)
    # -------------------------------------------------------------------------

    def _factor_dignity(
        self,
        sign: str,
        lord: str,
        occupants: list,
        normalized_planets: dict
    ) -> float:
        """
        Dignity-based quality score for occupant planets in the sign.

        Each occupant's dignity produces a modifier (exalted→+30 … debilitated→-20).
        Additional +10 if the sign's ruling lord occupies its own sign.
        Empty sign → 50 (neutral).
        """
        if not occupants:
            return float(self.matrix["empty_sign_baseline"])

        dmod    = self.matrix["dignity_modifiers"]
        mods    = []

        for p in occupants:
            raw_dignity = normalized_planets.get(p["name"], {}).get("dignity", "neutral")
            mods.append(float(dmod.get(raw_dignity, 0)))

        avg = sum(mods) / len(mods)

        # Lord-in-own-sign bonus
        lord_own = any(p["name"] == lord for p in occupants)
        lord_bonus = float(dmod["lord_own_bonus"]) if lord_own else 0.0

        return float(clamp_score(50.0 + avg + lord_bonus))

    # -------------------------------------------------------------------------
    # Factor F — Varga Validation (5%)
    # -------------------------------------------------------------------------

    def _factor_varga(self, occupants: list, varga_outputs: dict) -> float:
        """
        D9 and D10 dignity refinement for all occupant planets.

        Per planet, per varga:
            Vargottama:    +15
            Exalted:       +10
            Own/Moola:     +8
            Friendly:      +4
            Neutral:        0
            Enemy:         -4
            Debilitated:   -8

        Empty sign or no varga data → 50 (neutral).
        """
        if not occupants or not varga_outputs:
            return float(self.matrix["empty_sign_baseline"])

        varga_dignity_map = {
            "exalted":      10.0,
            "own_house":     8.0,
            "moolatrikona":  8.0,
            "friendly":      4.0,
            "neutral":       0.0,
            "enemy":        -4.0,
            "debilitated":  -8.0
        }
        vargottama_bonus = 15.0

        all_mods = []
        for p in occupants:
            name = p["name"]
            for varga_id in ("D9", "D10"):
                varga_planets = varga_outputs.get(varga_id, {}).get("planets", {})
                if name not in varga_planets:
                    continue
                vd = varga_planets[name]
                mod = varga_dignity_map.get(vd.get("dignity", "neutral"), 0.0)
                if vd.get("is_vargottama", False):
                    mod += vargottama_bonus
                all_mods.append(mod)

        if not all_mods:
            return float(self.matrix["empty_sign_baseline"])

        avg = sum(all_mods) / len(all_mods)
        return float(clamp_score(50.0 + avg))

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _build_sign_occupant_map(self, normalized_planets: dict) -> dict:
        """
        Single-pass grouping of planets by their sign.
        Returns: {"aries": [planet_dict, ...], "taurus": [...], ...}
        """
        sign_map = {s: [] for s in SIGNS_IN_ORDER}
        for planet_data in normalized_planets.values():
            sign = planet_data.get("sign", "")
            if sign in sign_map:
                sign_map[sign].append(planet_data)
        return sign_map

    def _sign_to_house(self, sign: str, ascendant_sign: str) -> int:
        """
        Derives the house number of a sign given the ascendant.
        For Aries ascendant: Aries=1, Taurus=2, ..., Pisces=12.
        For Taurus ascendant: Taurus=1, Gemini=2, ..., Aries=12.
        """
        try:
            sign_idx = SIGNS_IN_ORDER.index(sign)
            asc_idx  = SIGNS_IN_ORDER.index(ascendant_sign)
        except ValueError:
            return 1  # safe fallback

        return ((sign_idx - asc_idx) % 12) + 1

    def _grade(self, score: int) -> str:
        """Looks up the grade label for a given score using PROBABILITY_GRADES."""
        for threshold, label in PROBABILITY_GRADES:
            if score >= threshold:
                return label
        return "TOO WEAK"

    def _flags(
        self,
        sign: str,
        lord: str,
        dependency_scores: dict,
        sav_bindus: int,
        occupants: list
    ) -> list:
        """Generates diagnostic confidence flags for explainability."""
        flags = []

        if sav_bindus == 0:
            flags.append("zero_sav")

        if lord not in dependency_scores:
            flags.append("lord_absent")
        elif dependency_scores[lord].get("final_score", 50) < 10:
            flags.append("lord_debilitated")

        if occupants:
            all_malefic = all(p["name"] in self.malefics for p in occupants)
            if all_malefic:
                flags.append("malefic_dominant")
        else:
            flags.append("empty_sign")

        lord_data = dependency_scores.get(lord, {})
        sav_score = self._factor_sav(sav_bindus)
        if sav_score > 80 and lord_data.get("final_score", 0) > 70:
            flags.append("strongly_supported")

        return flags

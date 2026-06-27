from app.config.astrology_constants import PROBABILITY_GRADES
from app.utils.astrology_math import clamp_score


# ---------------------------------------------------------------------------
# Master Probability Weights
# Source: VEDIC_AI_MASTER_ARCHITECTURE.md
# ---------------------------------------------------------------------------
MASTER_WEIGHTS = {
    "natal_promise":   0.40,   # Domain promise scores (8 domains)  [live]
    "planet_strength": 0.15,   # Avg BAV-adjusted planet score [live]
    "house_strength":  0.10,   # Avg SAV-adjusted house score  [live]
    "rasi_strength":   0.10,   # Avg sign environment score    [live]
    "varga_validation":0.10,   # Varga D9/D10 dignity          [live]
    "dasha_activation":0.10,   # Temporal activation score     [live]
    "transit_trigger": 0.05,   # Transit overlay               [live]
}

# Neutral score for unimplemented stubs
_STUB_SCORE = 50.0


class MasterProbabilityEngine:
    """
    Deterministic synthesis engine — the top of the scoring stack.

    Consumes all downstream engine outputs and produces a single
    weighted probability score per the master architecture formula:

        Natal Promise      = 40%  [live — avg of 8 NatalPromiseEngine domain scores]
        Planet Strength    = 15%  [live — BAV-adjusted final_score avg]
        House Strength     = 10%  [live — SAV-adjusted final_score avg]
        Rasi Strength      = 10%  [live — weighted sign score avg]
        Varga Validation   = 10%  [live — D9/D10 modifier avg]
        Dasha Activation   = 10%  [live — base × timing_multiplier]
        Transit Trigger    =  5%  [live — TransitEngine Gochara activation_score]

    Architecture Rules:
        - Zero astrological recalculation. Consumes pre-computed scores only.
        - Stubs return STUB_SCORE=50 (neutral) so they contribute as if
          absent — total probability remains correctly weighted.
        - All weights in MASTER_WEIGHTS constant above.
        - No AI/ML. Pure arithmetic weighted average.
    """

    def __init__(self, calibration=None):
        if calibration is None:
            from app.calibration.calibration_manager import CalibrationManager
            calibration = CalibrationManager()
        self.weights = calibration.master_probability.get('MASTER_WEIGHTS', {})
        self.stub    = _STUB_SCORE

    # -------------------------------------------------------------------------
    # Public Interface
    # -------------------------------------------------------------------------

    def evaluate(self, engine_outputs: dict) -> dict:
        """
        Computes the master probability score from all engine outputs.

        Args:
            engine_outputs (dict): Full pipeline output containing keys:
                "planets", "houses", "rasis", "vargas", "dashas", "ashtakavarga"

        Returns:
            dict: Master probability payload with score, grade, and full breakdown.
        """
        factors = self._compute_all_factors(engine_outputs)
        raw     = self._weighted_sum(factors)
        
        score   = clamp_score(round(raw))
        grade   = self._grade(score)

        # Mode 2: Lifetime Projection
        timeline = engine_outputs.get("dashas", {}).get("timeline", [])
        projected_timeline = []
        for record in timeline:
            temp_factors = factors.copy()
            # Substitute the specific period's Dasha Activation
            temp_factors["dasha_activation"] = record.get("dasha_activation", 50.0)
            
            temp_raw = self._weighted_sum(temp_factors)
            temp_score = clamp_score(round(temp_raw))
            temp_grade = self._grade(temp_score)
            
            projected_timeline.append({
                "start_date": record.get("start_date", "Unknown"),
                "end_date": record.get("end_date", "Unknown"),
                "md": record.get("mahadasha", "unknown"),
                "ad": record.get("antardasha", "unknown"),
                "pd": record.get("pratyantardasha", "unknown"),
                "md_planet_strength": record.get("md_planet_strength", 0.0),
                "ad_planet_strength": record.get("ad_planet_strength", 0.0),
                "pd_planet_strength": record.get("pd_planet_strength", 0.0),
                "activation_pct": record.get("dasha_activation", 50.0),
                "final_probability_pct": temp_score,
                "grade": temp_grade
            })

        return {
            "final_score":  score,
            "raw_score":    round(raw, 4),
            "grade":        grade,
            "breakdown":    factors,
            "weights":      self.weights,
            "stub_factors": [],
            "live_factors": [
                "natal_promise", "planet_strength", "house_strength", "rasi_strength",
                "varga_validation", "dasha_activation", "transit_trigger"
            ],
            "lifetime_projection": projected_timeline
        }

    # -------------------------------------------------------------------------
    # Factor Computation
    # -------------------------------------------------------------------------

    def _compute_all_factors(self, engine_outputs: dict) -> dict:
        return {
            "natal_promise":    self._natal_promise(engine_outputs.get("natal_promise", {})),
            "planet_strength":  self._planet_strength(engine_outputs.get("planets", {})),
            "house_strength":   self._house_strength(engine_outputs.get("houses", {})),
            "rasi_strength":    self._rasi_strength(engine_outputs.get("rasis", {})),
            "varga_validation": self._varga_validation(engine_outputs.get("vargas", {})),
            "dasha_activation": self._dasha_activation(engine_outputs.get("dashas", {})),
            "transit_trigger":  self._transit_trigger(engine_outputs.get("transit", {})),
        }

    def _natal_promise(self, natal_results: dict) -> float:
        """
        Aggregates NatalPromiseEngine domain scores into a single float.
        Strategy: average of all 8 domain scores.
        # Natal Promise: average of all 8 domain promise scores from NatalPromiseEngine.
        # Falls back to stub score (50, neutral) if natal_promise is absent.

        Note: In a domain-specific query (e.g. "Will I get married?"), the
        MasterProbabilityEngine should receive the SINGLE domain's natal promise
        score (e.g. natal_results["marriage"]["score"]) rather than this average.
        That routing is handled by the QuestionEngine (future phase).
        """
        if not natal_results:
            return self.stub
        scores = [
            data["score"]
            for data in natal_results.values()
            if isinstance(data, dict) and "score" in data
        ]
        return round(sum(scores) / len(scores), 2) if scores else self.stub

    def _planet_strength(self, planet_results: dict) -> float:
        """
        Aggregate planet strength score.
        Uses BAV-adjusted final_score (post Step 7.5) for all planets.
        Excludes planets with no score data.
        Returns neutral 50 if no planet data.
        """
        if not planet_results:
            return self.stub
        scores = [
            data["final_score"]
            for data in planet_results.values()
            if "final_score" in data
        ]
        return round(sum(scores) / len(scores), 2) if scores else self.stub

    def _house_strength(self, house_results: dict) -> float:
        """
        Aggregate house strength score.
        Uses SAV-adjusted final_score for all 12 houses.
        Returns neutral 50 if no house data.
        """
        if not house_results:
            return self.stub
        scores = [
            data["final_score"]
            for data in house_results.values()
            if "final_score" in data
        ]
        return round(sum(scores) / len(scores), 2) if scores else self.stub

    def _rasi_strength(self, rasi_results: dict) -> float:
        """
        Aggregate rasi strength score across all 12 signs.
        Returns neutral 50 if no rasi data.
        """
        if not rasi_results:
            return self.stub
        scores = [
            data["final_score"]
            for data in rasi_results.values()
            if "final_score" in data
        ]
        return round(sum(scores) / len(scores), 2) if scores else self.stub

    def _varga_validation(self, varga_results: dict) -> float:
        """
        Aggregate varga modifier score.

        For each planet with varga data, sums all modifier values
        (D9/D10 dignity + vargottama bonuses) and normalises to [0, 100]:
            50 = neutral baseline (no modifiers)
            >50 = net positive dignities
            <50 = net negative dignities

        Returns neutral 50 if no varga data.
        """
        if not varga_results:
            return self.stub

        per_planet = {}
        for varga_chart in varga_results.values():
            for planet, data in varga_chart.get("planets", {}).items():
                mods = data.get("modifiers", {})
                net = sum(mods.values())
                if planet not in per_planet:
                    per_planet[planet] = 0.0
                per_planet[planet] += net

        scores = []
        for planet, net in per_planet.items():
            scores.append(clamp_score(self.stub + net))

        return round(sum(scores) / len(scores), 2) if scores else self.stub

    def _dasha_activation(self, dasha_results: dict) -> float:
        """
        Aggregate dasha activation score.

        For each active dasha lord:
            activation = base_score × timing_multiplier   (clamped to [0, 100])

        Combined: 0.60 × MD_activation + 0.40 × AD_activation
        Mirrors the same MD/AD weighting used in AshtakavargaEngine.

        Returns neutral 50 if no dasha data.
        """
        if not dasha_results:
            return self.stub

        # Filter out non-dictionary entries (like "timeline" list) to prevent attribute errors
        entries = [e for e in dasha_results.values() if isinstance(e, dict)]

        # Identify MD and AD by confidence_flags
        md_data = next(
            (e for e in entries if "active_mahadasha" in e.get("confidence_flags", [])),
            entries[0] if entries else {}
        )
        ad_data = next(
            (e for e in entries if "active_antardasha" in e.get("confidence_flags", [])),
            entries[-1] if len(entries) > 1 else {}
        )

        md_score = self._single_dasha_score(md_data)
        ad_score = self._single_dasha_score(ad_data)

        combined = 0.60 * md_score + 0.40 * ad_score
        return round(clamp_score(combined), 2)

    def _single_dasha_score(self, dasha_data: dict) -> float:
        """
        Computes a single dasha lord's activation score.
        activation = base_score × timing_multiplier, clamped to [0, 100].
        """
        base       = float(dasha_data.get("final_score", self.stub))
        multiplier = dasha_data.get("temporal_activation", {}).get(
            "timing_multiplier", 1.0
        )
        return clamp_score(round(base * multiplier, 2))

    def _transit_trigger(self, transit_results: dict) -> float:
        """
        Reads the activation_score from TransitEngine output.

        Falls back to STUB_SCORE (50, neutral) if transit_results is absent or
        empty — this preserves backward compatibility when no transit_positions
        are supplied to PipelineRunner (all existing tests remain unaffected).
        """
        return float(transit_results.get("activation_score", self.stub))

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _weighted_sum(self, factors: dict) -> float:
        """Computes the weighted average of all factor scores."""
        total = 0.0
        for key, score in factors.items():
            weight = self.weights.get(key, 0.0)
            total += score * weight
        return total

    def _grade(self, score: int) -> str:
        """Looks up the probability grade label from PROBABILITY_GRADES."""
        for threshold, label in PROBABILITY_GRADES:
            if score >= threshold:
                return label
        return "TOO WEAK"

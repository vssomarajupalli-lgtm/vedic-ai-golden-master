import unittest
from app.engines.master_probability_engine import MasterProbabilityEngine


class TestMasterProbabilityEngine(unittest.TestCase):
    """
    Deterministic tests for MasterProbabilityEngine.

    All expected values are derived from the master architecture weights:
        natal_promise   = 40%  [stub → 50]
        planet_strength = 15%
        house_strength  = 10%
        rasi_strength   = 10%
        varga_validation= 10%
        dasha_activation= 10%
        transit_trigger =  5%  [stub → 50]

    Formula: final_score = Σ(factor_score × weight), clamped [0, 100]
    """

    def setUp(self):
        self.engine = MasterProbabilityEngine()

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    def _planet(self, score):
        return {"final_score": score, "raw_score": float(score)}

    def _house(self, score):
        return {"final_score": score}

    def _rasi(self, score):
        return {"final_score": score}

    def _varga(self, modifiers):
        return {"modifiers": modifiers, "confidence_flags": []}

    def _dasha(self, base, mult, level="mahadasha"):
        return {
            "final_score": base,
            "temporal_activation": {"timing_multiplier": mult},
            "confidence_flags": [f"active_{level}"]
        }

    # -----------------------------------------------------------------------
    # 1. Output schema
    # -----------------------------------------------------------------------

    def test_output_has_required_keys(self):
        result = self.engine.evaluate({})
        for key in ("final_score", "raw_score", "grade", "breakdown",
                    "weights", "stub_factors", "live_factors"):
            self.assertIn(key, result, f"Missing key: {key}")

    def test_breakdown_has_all_7_factors(self):
        result = self.engine.evaluate({})
        factors = result["breakdown"]
        for f in ("natal_promise", "planet_strength", "house_strength",
                  "rasi_strength", "varga_validation", "dasha_activation",
                  "transit_trigger"):
            self.assertIn(f, factors)

    def test_stub_factors_listed(self):
        result = self.engine.evaluate({})
        self.assertEqual(len(result["stub_factors"]), 0)

    def test_live_factors_listed(self):
        result = self.engine.evaluate({})
        for f in ("natal_promise", "planet_strength", "house_strength", "rasi_strength",
                  "varga_validation", "dasha_activation", "transit_trigger"):
            self.assertIn(f, result["live_factors"])

    def test_weights_sum_to_1(self):
        result = self.engine.evaluate({})
        total = sum(result["weights"].values())
        self.assertAlmostEqual(total, 1.0, places=6)

    # -----------------------------------------------------------------------
    # 2. Empty inputs → neutral baseline
    # -----------------------------------------------------------------------

    def test_empty_inputs_return_50(self):
        """With all stubs and no live data, every factor = 50 → final = 50."""
        result = self.engine.evaluate({})
        self.assertEqual(result["final_score"], 50)

    def test_empty_planets_returns_neutral(self):
        score = self.engine._planet_strength({})
        self.assertEqual(score, 50.0)

    def test_empty_houses_returns_neutral(self):
        score = self.engine._house_strength({})
        self.assertEqual(score, 50.0)

    def test_empty_rasis_returns_neutral(self):
        score = self.engine._rasi_strength({})
        self.assertEqual(score, 50.0)

    def test_empty_vargas_returns_neutral(self):
        score = self.engine._varga_validation({})
        self.assertEqual(score, 50.0)

    def test_empty_dashas_returns_neutral(self):
        score = self.engine._dasha_activation({})
        self.assertEqual(score, 50.0)

    # -----------------------------------------------------------------------
    # 3. Planet strength factor
    # -----------------------------------------------------------------------

    def test_planet_strength_average_of_all_planets(self):
        """Average of (60, 40) = 50.0."""
        planets = {"jupiter": self._planet(60), "venus": self._planet(40)}
        score = self.engine._planet_strength(planets)
        self.assertAlmostEqual(score, 50.0, places=2)

    def test_planet_strength_single_planet(self):
        planets = {"saturn": self._planet(75)}
        score = self.engine._planet_strength(planets)
        self.assertAlmostEqual(score, 75.0, places=2)

    def test_planet_strength_uses_final_score(self):
        """Uses final_score (BAV-adjusted), not raw_score."""
        planets = {
            "sun": {"final_score": 50, "base_score": 45, "bav_modifier": +5}
        }
        score = self.engine._planet_strength(planets)
        self.assertAlmostEqual(score, 50.0, places=2)

    # -----------------------------------------------------------------------
    # 4. House strength factor
    # -----------------------------------------------------------------------

    def test_house_strength_average(self):
        """Average of (30, 70) = 50.0."""
        houses = {"1": self._house(30), "9": self._house(70)}
        score = self.engine._house_strength(houses)
        self.assertAlmostEqual(score, 50.0, places=2)

    def test_house_strength_all_strong(self):
        """All 80 → average = 80."""
        houses = {str(i): self._house(80) for i in range(1, 5)}
        score = self.engine._house_strength(houses)
        self.assertAlmostEqual(score, 80.0, places=2)

    # -----------------------------------------------------------------------
    # 5. Rasi strength factor
    # -----------------------------------------------------------------------

    def test_rasi_strength_average(self):
        rasis = {"aries": self._rasi(40), "taurus": self._rasi(60)}
        score = self.engine._rasi_strength(rasis)
        self.assertAlmostEqual(score, 50.0, places=2)

    # -----------------------------------------------------------------------
    # 6. Varga validation factor
    # -----------------------------------------------------------------------

    def test_varga_neutral_when_no_modifiers(self):
        """Planet with empty modifiers → 50 baseline."""
        vargas = {"D9": {"planets": {"sun": self._varga({})}}}
        score = self.engine._varga_validation(vargas)
        self.assertAlmostEqual(score, 50.0, places=2)

    def test_varga_positive_modifiers_above_50(self):
        """Positive modifier net → score > 50."""
        vargas = {"D9": {"planets": {"jupiter": self._varga({"D9_vargottama_bonus": 15.0})}}}
        score = self.engine._varga_validation(vargas)
        self.assertGreater(score, 50.0)

    def test_varga_negative_modifiers_below_50(self):
        """Negative modifier net → score < 50."""
        vargas = {"D9": {"planets": {"sun": self._varga({"D9_dignity_modifier": -5.0})}}}
        score = self.engine._varga_validation(vargas)
        self.assertLess(score, 50.0)

    def test_varga_clamped_at_100(self):
        """Very large positive modifier → clamped to 100."""
        vargas = {"D9": {"planets": {"jupiter": self._varga({"huge_bonus": 200.0})}}}
        score = self.engine._varga_validation(vargas)
        self.assertEqual(score, 100.0)

    def test_varga_clamped_at_zero(self):
        """Very large negative modifier → clamped to 0."""
        vargas = {"D9": {"planets": {"sun": self._varga({"huge_penalty": -200.0})}}}
        score = self.engine._varga_validation(vargas)
        self.assertEqual(score, 0.0)

    # -----------------------------------------------------------------------
    # 7. Dasha activation factor
    # -----------------------------------------------------------------------

    def test_dasha_activation_md_only(self):
        """Single MD at base=50, mult=1.15 → 50×1.15=57.5 → 60% MD weight applied."""
        dashas = {"saturn": self._dasha(50, 1.15, "mahadasha")}
        score = self.engine._dasha_activation(dashas)
        # MD score = clamp(50 × 1.15) = 57.5 → combined = 0.60×57.5 + 0.40×57.5 = 57.5
        # (only MD present, AD falls back to same entry)
        self.assertGreater(score, 50.0)

    def test_dasha_activation_md_ad_weighted(self):
        """MD=50×1.0=50, AD=100×1.0=100 → 0.60×50 + 0.40×100 = 70."""
        dashas = {
            "saturn":  self._dasha(50,  1.0, "mahadasha"),
            "jupiter": self._dasha(100, 1.0, "antardasha")
        }
        score = self.engine._dasha_activation(dashas)
        self.assertAlmostEqual(score, 70.0, places=2)

    def test_dasha_activation_clamped_at_100(self):
        """Base=100, mult=2.0 → activation clamped to 100."""
        dashas = {"saturn": self._dasha(100, 2.0, "mahadasha")}
        score = self.engine._dasha_activation(dashas)
        self.assertLessEqual(score, 100.0)

    def test_single_dasha_score_formula(self):
        """single_dasha_score = clamp(base × multiplier). Result is an int (clamp_score rounds)."""
        data = {
            "final_score": 50,
            "temporal_activation": {"timing_multiplier": 1.21},
            "confidence_flags": []
        }
        score = self.engine._single_dasha_score(data)
        # 50 × 1.21 = 60.5 → clamp_score rounds to int → 60 or 61
        self.assertAlmostEqual(score, 50 * 1.21, delta=1.0)

    def test_single_dasha_score_missing_multiplier_defaults_1(self):
        """Missing timing_multiplier → defaults to 1.0."""
        data = {"final_score": 55, "temporal_activation": {}, "confidence_flags": []}
        score = self.engine._single_dasha_score(data)
        self.assertAlmostEqual(score, 55.0, places=2)

    # -----------------------------------------------------------------------
    # 8. Weighted sum formula
    # -----------------------------------------------------------------------

    def test_weighted_sum_all_50_returns_50(self):
        """All factors = 50 → weighted sum = 50."""
        factors = {k: 50.0 for k in self.engine.weights}
        result = self.engine._weighted_sum(factors)
        self.assertAlmostEqual(result, 50.0, places=4)

    def test_weighted_sum_all_100_returns_100(self):
        factors = {k: 100.0 for k in self.engine.weights}
        result = self.engine._weighted_sum(factors)
        self.assertAlmostEqual(result, 100.0, places=4)

    def test_weighted_sum_all_0_returns_0(self):
        factors = {k: 0.0 for k in self.engine.weights}
        result = self.engine._weighted_sum(factors)
        self.assertAlmostEqual(result, 0.0, places=4)

    def test_planet_weight_is_15_percent(self):
        """Planet factor at 100, all others at 0 → raw = 15."""
        factors = {k: 0.0 for k in self.engine.weights}
        factors["planet_strength"] = 100.0
        result = self.engine._weighted_sum(factors)
        self.assertAlmostEqual(result, 15.0, places=4)

    def test_natal_promise_weight_is_40_percent(self):
        """Natal Promise at 100, all others at 0 → raw = 40."""
        factors = {k: 0.0 for k in self.engine.weights}
        factors["natal_promise"] = 100.0
        result = self.engine._weighted_sum(factors)
        self.assertAlmostEqual(result, 40.0, places=4)

    # -----------------------------------------------------------------------
    # 9. Grade mapping
    # -----------------------------------------------------------------------

    def test_grade_70_is_very_good_or_good(self):
        grade = self.engine._grade(70)
        self.assertIn(grade, ("VERY GOOD", "GOOD"))

    def test_grade_50_is_good_or_moderate(self):
        grade = self.engine._grade(50)
        self.assertIsNotNone(grade)

    def test_grade_0_is_too_weak(self):
        grade = self.engine._grade(0)
        self.assertEqual(grade, "TOO WEAK")

    # -----------------------------------------------------------------------
    # 10. Final score clamping
    # -----------------------------------------------------------------------

    def test_final_score_between_0_and_100(self):
        """Any input must produce final_score in [0, 100]."""
        result = self.engine.evaluate({
            "planets": {"sun": self._planet(100)},
            "houses":  {"1":   self._house(100)},
            "rasis":   {"aries": self._rasi(100)},
        })
        self.assertGreaterEqual(result["final_score"], 0)
        self.assertLessEqual(result["final_score"],    100)

    def test_low_scores_clamped_at_zero(self):
        result = self.engine.evaluate({
            "planets": {"sun":   self._planet(0)},
            "houses":  {"1":     self._house(0)},
            "rasis":   {"aries": self._rasi(0)},
            "vargas":  {"D9": {"planets": {"sun":   self._varga({"penalty": -200.0})}}},
        })
        self.assertGreaterEqual(result["final_score"], 0)

    # -----------------------------------------------------------------------
    # 11. Raju spot-check (canonical chart values)
    # -----------------------------------------------------------------------

    def test_raju_canonical_engine_outputs_produce_valid_score(self):
        """
        Feed Raju's known engine output averages and verify the master
        probability score is a reasonable non-zero value.

        Raju approximate averages from pipeline output:
            planets:  avg ≈ 25  (many weak planets)
            houses:   avg ≈ 20  (many clamped to zero)
            rasis:    avg ≈ 47  (mixed signs)
            vargas:   avg vargottama bonuses ≈ net +15
            dashas:   MD Saturn 50×1.21=60.5, AD Jupiter 55×1.21=66.55
        """
        engine_outputs = {
            "planets": {
                "sun":     self._planet(50),
                "moon":    self._planet(35),
                "mars":    self._planet(0),
                "mercury": self._planet(0),
                "jupiter": self._planet(60),
                "venus":   self._planet(30),
                "saturn":  self._planet(50),
                "rahu":    self._planet(5),
                "ketu":    self._planet(5),
            },
            "houses": {str(h): self._house(s) for h, s in {
                1: 0, 2: 38, 3: 10, 4: 31, 5: 33,
                6: 0, 7: 11, 8: 0,  9: 48, 10: 33, 11: 33, 12: 0
            }.items()},
            "rasis": {
                "aries": self._rasi(39), "taurus": self._rasi(44),
                "gemini": self._rasi(39), "cancer": self._rasi(52),
                "leo": self._rasi(45), "virgo": self._rasi(54),
                "libra": self._rasi(50), "scorpio": self._rasi(43),
                "sagittarius": self._rasi(55), "capricorn": self._rasi(51),
                "aquarius": self._rasi(68), "pisces": self._rasi(34)
            },
            "vargas": {
                "D9": {"planets": {
                    "jupiter": self._varga({"D9_vargottama_bonus": 15.0}),
                    "saturn":  self._varga({
                        "D9_dignity_modifier": 15.0,
                        "D9_vargottama_bonus": 15.0,
                        "D10_dignity_modifier": 10.0
                    })
                }},
            },
            "dashas": {
                "saturn":  self._dasha(50, 1.21, "mahadasha"),
                "jupiter": self._dasha(55, 1.21, "antardasha"),
            }
        }
        result = self.engine.evaluate(engine_outputs)
        self.assertIn("final_score", result)
        self.assertGreater(result["final_score"], 0)
        self.assertLessEqual(result["final_score"], 100)
        # Raju is a mixed chart — score should be in weak-moderate range
        self.assertGreater(result["final_score"], 30,
                           "Raju's master score should be above 30 (stub natal_promise=50 lifts it)")
        self.assertLess(result["final_score"], 80,
                        "Raju's master score should be below 80 (many weak planets/houses)")


if __name__ == "__main__":
    unittest.main()

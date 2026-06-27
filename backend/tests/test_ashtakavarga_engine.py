import unittest
from app.engines.ashtakavarga_engine import AshtakavargaEngine
from app.config.astrology_constants import BAV_PLANETS

# ---------------------------------------------------------------------------
# Shared fixtures (Raju's chart — Mesha Lagna)
# ---------------------------------------------------------------------------

RAW_BAV = {
    "sun":     {"aries": 5, "taurus": 4, "gemini": 3, "cancer": 6, "leo": 3, "virgo": 5, "libra": 4, "scorpio": 3, "sagittarius": 5, "capricorn": 4, "aquarius": 6, "pisces": 1},
    "moon":    {"aries": 4, "taurus": 5, "gemini": 4, "cancer": 5, "leo": 2, "virgo": 4, "libra": 5, "scorpio": 3, "sagittarius": 4, "capricorn": 5, "aquarius": 5, "pisces": 1},
    "mars":    {"aries": 3, "taurus": 3, "gemini": 3, "cancer": 4, "leo": 2, "virgo": 4, "libra": 3, "scorpio": 3, "sagittarius": 3, "capricorn": 3, "aquarius": 4, "pisces": 1},
    "mercury": {"aries": 5, "taurus": 4, "gemini": 4, "cancer": 5, "leo": 3, "virgo": 5, "libra": 4, "scorpio": 3, "sagittarius": 4, "capricorn": 4, "aquarius": 6, "pisces": 2},
    "jupiter": {"aries": 5, "taurus": 5, "gemini": 5, "cancer": 6, "leo": 5, "virgo": 7, "libra": 5, "scorpio": 4, "sagittarius": 5, "capricorn": 5, "aquarius": 7, "pisces": 2},
    "venus":   {"aries": 3, "taurus": 4, "gemini": 3, "cancer": 4, "leo": 3, "virgo": 5, "libra": 3, "scorpio": 3, "sagittarius": 3, "capricorn": 3, "aquarius": 5, "pisces": 2},
    "saturn":  {"aries": 1, "taurus": 0, "gemini": 4, "cancer": 0, "leo": 4, "virgo": 2, "libra": 4, "scorpio": 3, "sagittarius": 1, "capricorn": 2, "aquarius": 7, "pisces": 1}
}

RAW_SAV = {
    "aries": 26, "taurus": 25, "gemini": 26, "cancer": 30,
    "leo": 22, "virgo": 32, "libra": 28, "scorpio": 22,
    "sagittarius": 25, "capricorn": 26, "aquarius": 40, "pisces": 0
}

RAJU_PLANETS = {
    "sun":     {"house": 1,  "sign": "aries"},
    "moon":    {"house": 2,  "sign": "taurus"},
    "mars":    {"house": 8,  "sign": "scorpio"},
    "mercury": {"house": 12, "sign": "pisces"},
    "jupiter": {"house": 9,  "sign": "sagittarius"},
    "venus":   {"house": 12, "sign": "pisces"},
    "saturn":  {"house": 7,  "sign": "libra"},
    "rahu":    {"house": 6,  "sign": "virgo"},
    "ketu":    {"house": 12, "sign": "pisces"}
}

RAJU_DASHAS = {
    "mahadasha":    {"lord": "saturn"},
    "antardasha":   {"lord": "jupiter"},
    "pratyantardasha": {"lord": "mars"}
}

RAJU_PLANET_SCORES = {
    "sun":     {"final_score": 45},
    "moon":    {"final_score": 30},
    "mars":    {"final_score": 0},
    "mercury": {"final_score": 0},
    "jupiter": {"final_score": 55},
    "venus":   {"final_score": 35},
    "saturn":  {"final_score": 50},
    "rahu":    {"final_score": 5},
    "ketu":    {"final_score": 5}
}

RAJU_PAYLOAD = {
    "metadata": {
        "ascendant_sign": "aries"
    },
    "ashtakavarga": {
        "sav_chart":  RAW_SAV,
        "bav_charts": RAW_BAV
    },
    "planets": RAJU_PLANETS,
    "dashas":  RAJU_DASHAS
}



class TestAshtakavargaEngine(unittest.TestCase):

    def setUp(self):
        self.engine = AshtakavargaEngine()

    # -----------------------------------------------------------------------
    # 1. BAV Bindu → Score (linear)
    # -----------------------------------------------------------------------

    def test_bav_score_all_anchor_values(self):
        """Linear BAV score: 0→0, 4→50, 8→100."""
        self.assertEqual(self.engine._bav_score(0), 0.0)
        self.assertEqual(self.engine._bav_score(4), 50.0)
        self.assertEqual(self.engine._bav_score(8), 100.0)

    def test_bav_score_intermediate_values(self):
        """5 bindus → 62.5, 3 bindus → 37.5."""
        self.assertAlmostEqual(self.engine._bav_score(5), 62.5, places=2)
        self.assertAlmostEqual(self.engine._bav_score(3), 37.5, places=2)

    def test_bav_score_7_bindus(self):
        """7 bindus → 87.5."""
        self.assertAlmostEqual(self.engine._bav_score(7), 87.5, places=2)

    def test_bav_score_1_bindu(self):
        """1 bindu → 12.5."""
        self.assertAlmostEqual(self.engine._bav_score(1), 12.5, places=2)

    # -----------------------------------------------------------------------
    # 2. BAV Grade Classification
    # -----------------------------------------------------------------------

    def test_bav_grade_0_critical(self):
        self.assertEqual(self.engine._bav_grade(0), "CRITICAL")

    def test_bav_grade_1_critical(self):
        self.assertEqual(self.engine._bav_grade(1), "CRITICAL")

    def test_bav_grade_2_weak(self):
        self.assertEqual(self.engine._bav_grade(2), "WEAK")

    def test_bav_grade_3_below_avg(self):
        self.assertEqual(self.engine._bav_grade(3), "BELOW_AVG")

    def test_bav_grade_4_average(self):
        self.assertEqual(self.engine._bav_grade(4), "AVERAGE")

    def test_bav_grade_5_good(self):
        self.assertEqual(self.engine._bav_grade(5), "GOOD")

    def test_bav_grade_6_strong(self):
        self.assertEqual(self.engine._bav_grade(6), "STRONG")

    def test_bav_grade_7_excellent(self):
        self.assertEqual(self.engine._bav_grade(7), "EXCELLENT")

    def test_bav_grade_8_excellent(self):
        self.assertEqual(self.engine._bav_grade(8), "EXCELLENT")

    # -----------------------------------------------------------------------
    # 3. SAV Piecewise Normalization
    # -----------------------------------------------------------------------

    def test_sav_anchor_points_exact(self):
        """Official anchor points normalize exactly."""
        self.assertEqual(self.engine._sav_score(0),  0.0)
        self.assertEqual(self.engine._sav_score(20), 30.0)
        self.assertEqual(self.engine._sav_score(25), 50.0)
        self.assertEqual(self.engine._sav_score(30), 70.0)
        self.assertEqual(self.engine._sav_score(35), 85.0)
        self.assertEqual(self.engine._sav_score(40), 100.0)

    def test_sav_interpolation_28_bindus(self):
        """28 bindus interpolated between 25→50 and 30→70."""
        score = self.engine._sav_score(28)
        self.assertAlmostEqual(score, 62.0, places=1)

    def test_sav_zero_bindus_scores_zero(self):
        self.assertEqual(self.engine._sav_score(0), 0.0)

    def test_sav_above_max_clamped_100(self):
        self.assertEqual(self.engine._sav_score(56), 100.0)

    # -----------------------------------------------------------------------
    # 4. Planet BAV Support Extraction
    # -----------------------------------------------------------------------

    def test_planet_bav_support_jupiter_h9(self):
        """Jupiter in H9: BAV = 5 bindus → GOOD → modifier +5."""
        result = self.engine._compute_planet_bav_support(
            RAJU_PLANETS, RAW_BAV, RAJU_PLANET_SCORES
        )
        jup = result["jupiter"]
        self.assertEqual(jup["house"],    9)
        self.assertEqual(jup["bindus"],   5)
        self.assertEqual(jup["grade"],    "GOOD")
        self.assertEqual(jup["modifier"], +5)

    def test_planet_bav_support_saturn_h7(self):
        """Saturn in H7: BAV = 4 bindus → AVERAGE → modifier 0."""
        result = self.engine._compute_planet_bav_support(
            RAJU_PLANETS, RAW_BAV, RAJU_PLANET_SCORES
        )
        sat = result["saturn"]
        self.assertEqual(sat["house"],    7)
        self.assertEqual(sat["bindus"],   4)
        self.assertEqual(sat["grade"],    "AVERAGE")
        self.assertEqual(sat["modifier"], 0)

    def test_planet_bav_support_mercury_h12(self):
        """Mercury in H12: BAV = 2 bindus → WEAK → modifier -5."""
        result = self.engine._compute_planet_bav_support(
            RAJU_PLANETS, RAW_BAV, RAJU_PLANET_SCORES
        )
        mer = result["mercury"]
        self.assertEqual(mer["house"],    12)
        self.assertEqual(mer["bindus"],   2)
        self.assertEqual(mer["grade"],    "WEAK")
        self.assertEqual(mer["modifier"], -5)

    def test_planet_bav_support_sun_h1(self):
        """Sun in H1: BAV = 5 bindus → GOOD → modifier +5."""
        result = self.engine._compute_planet_bav_support(
            RAJU_PLANETS, RAW_BAV, RAJU_PLANET_SCORES
        )
        sun = result["sun"]
        self.assertEqual(sun["bindus"],   5)
        self.assertEqual(sun["modifier"], +5)

    def test_planet_bav_support_missing_bav_defaults_to_neutral(self):
        """Planet with no BAV chart defaults to 4 bindus (AVERAGE, modifier 0)."""
        result = self.engine._compute_planet_bav_support(
            RAJU_PLANETS, {}, RAJU_PLANET_SCORES  # empty BAV
        )
        self.assertEqual(result["jupiter"]["bindus"],   4)
        self.assertEqual(result["jupiter"]["modifier"],  0)

    def test_planet_bav_support_all_7_planets_present(self):
        """All 7 BAV planets appear in planet_bav_support output."""
        result = self.engine._compute_planet_bav_support(
            RAJU_PLANETS, RAW_BAV, RAJU_PLANET_SCORES
        )
        for planet in BAV_PLANETS:
            self.assertIn(planet, result, f"Missing {planet} in planet_bav_support")

    # -----------------------------------------------------------------------
    # 5. Planet BAV Modifier Derivation
    # -----------------------------------------------------------------------

    def test_modifier_high_bindus_5_returns_plus5(self):
        self.assertEqual(self.engine._bav_modifier(5), +5)

    def test_modifier_high_bindus_6_returns_plus5(self):
        self.assertEqual(self.engine._bav_modifier(6), +5)

    def test_modifier_high_bindus_7_returns_plus5(self):
        self.assertEqual(self.engine._bav_modifier(7), +5)

    def test_modifier_neutral_bindus_4_returns_0(self):
        self.assertEqual(self.engine._bav_modifier(4), 0)

    def test_modifier_low_bindus_3_returns_minus5(self):
        self.assertEqual(self.engine._bav_modifier(3), -5)

    def test_modifier_low_bindus_2_returns_minus5(self):
        self.assertEqual(self.engine._bav_modifier(2), -5)

    def test_modifier_low_bindus_0_returns_minus5(self):
        self.assertEqual(self.engine._bav_modifier(0), -5)

    # -----------------------------------------------------------------------
    # 6. Dasha BAV Support
    # -----------------------------------------------------------------------

    def test_dasha_bav_saturn_md_h7(self):
        """Saturn (MD) in H7: BAV = 4 bindus → AVERAGE → moderate confidence."""
        result = self.engine._compute_dasha_bav_support(
            RAJU_DASHAS, RAJU_PLANETS, RAW_BAV
        )
        md = result["mahadasha"]
        self.assertEqual(md["lord"],   "saturn")
        self.assertEqual(md["house"],  7)
        self.assertEqual(md["bindus"], 4)
        self.assertEqual(md["grade"],  "AVERAGE")
        self.assertEqual(md["timing_confidence"], "moderate")

    def test_dasha_bav_jupiter_ad_h9(self):
        """Jupiter (AD) in H9: BAV = 5 bindus → GOOD → high confidence."""
        result = self.engine._compute_dasha_bav_support(
            RAJU_DASHAS, RAJU_PLANETS, RAW_BAV
        )
        ad = result["antardasha"]
        self.assertEqual(ad["lord"],   "jupiter")
        self.assertEqual(ad["house"],  9)
        self.assertEqual(ad["bindus"], 5)
        self.assertEqual(ad["grade"],  "GOOD")
        # 5 bindus → score 62.5 → _confidence_label(62.5) → 'high' (>= 62.5)
        self.assertEqual(ad["timing_confidence"], "high")

    def test_dasha_bav_combined_score_formula(self):
        """Combined = 0.60 × MD_score + 0.40 × AD_score."""
        result = self.engine._compute_dasha_bav_support(
            RAJU_DASHAS, RAJU_PLANETS, RAW_BAV
        )
        # Saturn H7 = 4 bindus → 50.0; Jupiter H9 = 5 bindus → 62.5
        expected = round(0.60 * 50.0 + 0.40 * 62.5, 2)  # = 55.0
        self.assertAlmostEqual(result["combined_dasha_bav_score"], expected, places=0)

    def test_dasha_bav_combined_confidence_moderate(self):
        """Combined score 55 (between 50 and 62.5) → moderate confidence."""
        result = self.engine._compute_dasha_bav_support(
            RAJU_DASHAS, RAJU_PLANETS, RAW_BAV
        )
        self.assertEqual(result["timing_confidence"], "moderate")

    def test_dasha_bav_combined_multiplier_moderate(self):
        """Moderate confidence → multiplier 1.05."""
        result = self.engine._compute_dasha_bav_support(
            RAJU_DASHAS, RAJU_PLANETS, RAW_BAV
        )
        self.assertAlmostEqual(result["timing_confidence_multiplier"], 1.05)

    # -----------------------------------------------------------------------
    # 7. Timing Confidence Multiplier
    # -----------------------------------------------------------------------

    def test_confidence_high_score_62_5(self):
        self.assertEqual(self.engine._confidence_label(62.5), "high")

    def test_confidence_high_score_100(self):
        self.assertEqual(self.engine._confidence_label(100.0), "high")

    def test_confidence_moderate_score_50(self):
        self.assertEqual(self.engine._confidence_label(50.0), "moderate")

    def test_confidence_moderate_score_60(self):
        self.assertEqual(self.engine._confidence_label(60.0), "moderate")

    def test_confidence_low_score_37_5(self):
        self.assertEqual(self.engine._confidence_label(37.5), "low")

    def test_confidence_low_score_0(self):
        self.assertEqual(self.engine._confidence_label(0.0), "low")

    # -----------------------------------------------------------------------
    # 8. SAV Favorable Classification
    # -----------------------------------------------------------------------

    def test_sav_h11_40_bindus_favorable(self):
        """H11 SAV=40 is favorable and strong."""
        result = self.engine._build_sav_chart(RAW_SAV, "aries")
        h11 = result["11"]
        self.assertEqual(h11["bindus"],       40)
        self.assertTrue(h11["is_favorable"])
        self.assertTrue(h11["is_strong"])
        self.assertFalse(h11["is_weak"])

    def test_sav_h12_0_bindus_unfavorable(self):
        """H12 SAV=0 is unfavorable, not strong, is weak, grade CRITICAL."""
        result = self.engine._build_sav_chart(RAW_SAV, "aries")
        h12 = result["12"]
        self.assertEqual(h12["bindus"],       0)
        self.assertFalse(h12["is_favorable"])
        self.assertFalse(h12["is_strong"])
        self.assertTrue(h12["is_weak"])
        self.assertEqual(h12["grade"],        "CRITICAL")

    def test_sav_h7_28_bindus_exactly_favorable(self):
        """H7 SAV=28 (exactly at threshold) → is_favorable=True."""
        result = self.engine._build_sav_chart(RAW_SAV, "aries")
        h7 = result["7"]
        self.assertEqual(h7["bindus"], 28)
        self.assertTrue(h7["is_favorable"])

    def test_sav_h5_22_bindus_is_weak(self):
        """H5 SAV=22 (below weak threshold 22) → is_weak=True? No — 22 < 22 is False."""
        result = self.engine._build_sav_chart(RAW_SAV, "aries")
        h5 = result["5"]
        self.assertEqual(h5["bindus"], 22)
        # 22 is NOT < 22, so is_weak should be False (boundary case)
        self.assertFalse(h5["is_weak"])

    def test_sav_chart_has_all_12_houses(self):
        """SAV chart always contains all 12 houses."""
        result = self.engine._build_sav_chart(RAW_SAV, "aries")
        self.assertEqual(len(result), 12)
        for h in range(1, 13):
            self.assertIn(str(h), result)

    # -----------------------------------------------------------------------
    # 9. BAV Consistency Check
    # -----------------------------------------------------------------------

    def test_bav_consistency_h11_correct(self):
        """H11: 6+5+4+6+7+5+7 = 40 = SAV → consistent."""
        result = self.engine._compute_sav_analytics(RAW_SAV, RAW_BAV, "aries")
        h11 = result["house_consistency"]["11"]
        self.assertEqual(h11["bav_sum"], 40)
        self.assertEqual(h11["sav_val"], 40)
        self.assertTrue(h11["consistent"])

    def test_bav_consistency_h12_inconsistent(self):
        """H12: 1+1+1+2+2+2+1=10 ≠ 0 (SAV) → inconsistent → flag raised."""
        result = self.engine._compute_sav_analytics(RAW_SAV, RAW_BAV, "aries")
        h12 = result["house_consistency"]["12"]
        self.assertEqual(h12["bav_sum"], 10)
        self.assertEqual(h12["sav_val"], 0)
        self.assertFalse(h12["consistent"])

    def test_bav_consistency_flag_false_when_any_mismatch(self):
        """bav_consistency_check is False if any house is inconsistent."""
        result = self.engine._compute_sav_analytics(RAW_SAV, RAW_BAV, "aries")
        # H12 is inconsistent → overall flag must be False
        self.assertFalse(result["bav_consistency_check"])

    def test_bav_consistency_all_true_when_consistent(self):
        """When SAV exactly equals BAV sums, bav_consistency_check is True."""
        bav = {"sun": {"aries": 3}, "moon": {"aries": 3}, "mars": {"aries": 2},
               "mercury": {"aries": 2}, "jupiter": {"aries": 2}, "venus": {"aries": 2},
               "saturn": {"aries": 2}}
        sav = {"aries": 16}  # 3+3+2+2+2+2+2 = 16
        result = self.engine._compute_sav_analytics(sav, bav, "aries")
        self.assertTrue(result["house_consistency"]["1"]["consistent"])

    # -----------------------------------------------------------------------
    # 10. SAV Analytics Totals
    # -----------------------------------------------------------------------

    def test_sav_analytics_total_bindus(self):
        """Total bindus = sum of all 12 SAV house values."""
        result = self.engine._compute_sav_analytics(RAW_SAV, RAW_BAV, "aries")
        expected = sum(RAW_SAV.values())
        self.assertEqual(result["total_bindus"], expected)

    def test_sav_analytics_peak_house(self):
        """Peak house for Raju is H11 (SAV=40)."""
        result = self.engine._compute_sav_analytics(RAW_SAV, RAW_BAV, "aries")
        self.assertEqual(result["peak_house"], "11")

    def test_sav_analytics_weakest_house(self):
        """Weakest house for Raju is H12 (SAV=0)."""
        result = self.engine._compute_sav_analytics(RAW_SAV, RAW_BAV, "aries")
        self.assertEqual(result["weakest_house"], "12")

    def test_sav_analytics_favorable_houses(self):
        """Favorable houses (SAV >= 28) correctly identified."""
        result = self.engine._compute_sav_analytics(RAW_SAV, RAW_BAV, "aries")
        favorable = result["favorable_houses"]
        # H4=30, H6=32, H7=28, H11=40 should all be favorable
        for h in ["4", "6", "7", "11"]:
            self.assertIn(h, favorable)

    def test_sav_analytics_unfavorable_houses(self):
        """Unfavorable houses (SAV < 22) correctly identified."""
        result = self.engine._compute_sav_analytics(RAW_SAV, RAW_BAV, "aries")
        unfavorable = result["unfavorable_houses"]
        # H12=0 is the only house below 22 (H5=22 is exactly 22, not < 22)
        self.assertIn("12", unfavorable)
        self.assertNotIn("5",  unfavorable)  # 22 is not < 22

    # -----------------------------------------------------------------------
    # 11. Output Schema Completeness
    # -----------------------------------------------------------------------

    def test_output_has_all_top_level_keys(self):
        """evaluate() output has all 6 required top-level keys."""
        result = self.engine.evaluate(RAJU_PAYLOAD, dependency_scores=RAJU_PLANET_SCORES)
        required = ["bav_charts", "sav_chart", "planet_bav_support",
                    "dasha_bav_support", "sav_analytics", "engine_modifiers"]
        for key in required:
            self.assertIn(key, result)

    def test_bav_charts_has_7_planets(self):
        """bav_charts output contains all 7 BAV planets."""
        result = self.engine.evaluate(RAJU_PAYLOAD, dependency_scores=RAJU_PLANET_SCORES)
        for planet in BAV_PLANETS:
            self.assertIn(planet, result["bav_charts"])

    def test_bav_charts_each_planet_has_12_houses(self):
        """Each planet's BAV chart has entries for all 12 houses."""
        result = self.engine.evaluate(RAJU_PAYLOAD, dependency_scores=RAJU_PLANET_SCORES)
        for planet in BAV_PLANETS:
            planet_chart = result["bav_charts"][planet]
            self.assertEqual(len(planet_chart), 12)
            for h in range(1, 13):
                self.assertIn(str(h), planet_chart)

    def test_bav_chart_entry_has_bindus_and_grade(self):
        """Each BAV house entry contains 'bindus' and 'grade' keys."""
        result = self.engine.evaluate(RAJU_PAYLOAD, dependency_scores=RAJU_PLANET_SCORES)
        entry = result["bav_charts"]["jupiter"]["9"]
        self.assertIn("bindus", entry)
        self.assertIn("grade",  entry)

    def test_sav_chart_has_all_12_houses(self):
        """sav_chart output has all 12 houses."""
        result = self.engine.evaluate(RAJU_PAYLOAD, dependency_scores=RAJU_PLANET_SCORES)
        self.assertEqual(len(result["sav_chart"]), 12)

    def test_sav_chart_entry_has_all_keys(self):
        """Each SAV chart entry has all required keys."""
        result = self.engine.evaluate(RAJU_PAYLOAD, dependency_scores=RAJU_PLANET_SCORES)
        entry  = result["sav_chart"]["11"]
        for key in ["bindus", "score", "grade", "is_favorable", "is_strong", "is_weak"]:
            self.assertIn(key, entry)

    def test_engine_modifiers_has_7_planets(self):
        """planet_score_adjustments covers all 7 BAV planets."""
        result = self.engine.evaluate(RAJU_PAYLOAD, dependency_scores=RAJU_PLANET_SCORES)
        adj = result["engine_modifiers"]["planet_score_adjustments"]
        for planet in BAV_PLANETS:
            self.assertIn(planet, adj)

    # -----------------------------------------------------------------------
    # 12. Missing / Empty Data Handling
    # -----------------------------------------------------------------------

    def test_empty_payload_no_crash(self):
        """evaluate() with empty payload returns safe empty output without crashing."""
        result = self.engine.evaluate({})
        self.assertIn("bav_charts", result)
        self.assertIn("sav_chart",  result)

    def test_missing_bav_chart_defaults_to_neutral(self):
        """Missing BAV chart for a planet results in 4-bindu neutral defaults."""
        payload = {
            "ashtakavarga": {"sav_chart": RAW_SAV, "bav_charts": {}},
            "planets":       RAJU_PLANETS,
            "dashas":        RAJU_DASHAS
        }
        result = self.engine.evaluate(payload, dependency_scores=RAJU_PLANET_SCORES)
        # All planets should default to 4 bindus (neutral) since BAV charts empty
        support = result["planet_bav_support"]
        for planet in BAV_PLANETS:
            self.assertEqual(support[planet]["bindus"],   4)
            self.assertEqual(support[planet]["modifier"],  0)

    def test_rahu_ketu_excluded_from_bav_charts(self):
        """Rahu and Ketu never appear in bav_charts output."""
        result = self.engine.evaluate(RAJU_PAYLOAD, dependency_scores=RAJU_PLANET_SCORES)
        self.assertNotIn("rahu", result["bav_charts"])
        self.assertNotIn("ketu", result["bav_charts"])

    # -----------------------------------------------------------------------
    # 13. Full Integration (Raju Spot-Checks)
    # -----------------------------------------------------------------------

    def test_raju_full_evaluate_spot_checks(self):
        """Full evaluate() with Raju data passes all key spot-checks."""
        result = self.engine.evaluate(RAJU_PAYLOAD, dependency_scores=RAJU_PLANET_SCORES)

        # Jupiter H9: BAV=5 → GOOD → modifier +5
        jup_support = result["planet_bav_support"]["jupiter"]
        self.assertEqual(jup_support["bindus"],   5)
        self.assertEqual(jup_support["grade"],    "GOOD")
        self.assertEqual(jup_support["modifier"], +5)

        # Saturn H7: BAV=4 → AVERAGE → modifier 0
        sat_support = result["planet_bav_support"]["saturn"]
        self.assertEqual(sat_support["bindus"],   4)
        self.assertEqual(sat_support["modifier"],  0)

        # Mercury H12: BAV=2 → WEAK → modifier -5
        mer_support = result["planet_bav_support"]["mercury"]
        self.assertEqual(mer_support["bindus"],   2)
        self.assertEqual(mer_support["modifier"], -5)

        # H11 SAV=40 → score 100, is_favorable True
        h11 = result["sav_chart"]["11"]
        self.assertEqual(h11["bindus"], 40)
        self.assertEqual(h11["score"],  100.0)
        self.assertTrue(h11["is_favorable"])

        # H12 SAV=0 → CRITICAL
        h12 = result["sav_chart"]["12"]
        self.assertEqual(h12["grade"], "CRITICAL")


if __name__ == "__main__":
    unittest.main()

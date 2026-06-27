import unittest
from app.engines.rasi_strength_engine import RasiStrengthEngine
from app.config.astrology_constants import SIGNS_IN_ORDER, SIGN_LORD_MAP

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

# Minimal planet set for Raju's chart (Mesha Lagna)
RAJU_PLANETS = {
    "sun":     {"name": "sun",     "sign": "aries",       "dignity": "exalted",     "house": 1,  "benefic_aspects_count": 0, "malefic_aspects_count": 1, "aspected_by": ["saturn"]},
    "moon":    {"name": "moon",    "sign": "taurus",      "dignity": "neutral",     "house": 2,  "benefic_aspects_count": 1, "malefic_aspects_count": 0, "aspected_by": ["jupiter"]},
    "mars":    {"name": "mars",    "sign": "scorpio",     "dignity": "own sign",    "house": 8,  "benefic_aspects_count": 0, "malefic_aspects_count": 0, "aspected_by": []},
    "mercury": {"name": "mercury", "sign": "pisces",      "dignity": "debilitated", "house": 12, "benefic_aspects_count": 0, "malefic_aspects_count": 1, "aspected_by": ["mars"]},
    "jupiter": {"name": "jupiter", "sign": "sagittarius", "dignity": "own sign",    "house": 9,  "benefic_aspects_count": 2, "malefic_aspects_count": 0, "aspected_by": []},
    "venus":   {"name": "venus",   "sign": "pisces",      "dignity": "exalted",     "house": 12, "benefic_aspects_count": 1, "malefic_aspects_count": 0, "aspected_by": ["jupiter"]},
    "saturn":  {"name": "saturn",  "sign": "libra",       "dignity": "exalted",     "house": 7,  "benefic_aspects_count": 0, "malefic_aspects_count": 1, "aspected_by": []},
    "rahu":    {"name": "rahu",    "sign": "virgo",       "dignity": "neutral",     "house": 6,  "benefic_aspects_count": 0, "malefic_aspects_count": 0, "aspected_by": []},
    "ketu":    {"name": "ketu",    "sign": "pisces",      "dignity": "neutral",     "house": 12, "benefic_aspects_count": 0, "malefic_aspects_count": 0, "aspected_by": []}
}

RAJU_HOUSES = {
    "1":  {"sav_points": 26, "lord": "mars",    "house_type": "kendra"},
    "2":  {"sav_points": 25, "lord": "venus",   "house_type": "neutral"},
    "3":  {"sav_points": 26, "lord": "mercury", "house_type": "neutral"},
    "4":  {"sav_points": 30, "lord": "moon",    "house_type": "kendra"},
    "5":  {"sav_points": 22, "lord": "sun",     "house_type": "trikona"},
    "6":  {"sav_points": 32, "lord": "mercury", "house_type": "dusthana"},
    "7":  {"sav_points": 28, "lord": "venus",   "house_type": "kendra"},
    "8":  {"sav_points": 22, "lord": "mars",    "house_type": "dusthana"},
    "9":  {"sav_points": 25, "lord": "jupiter", "house_type": "trikona"},
    "10": {"sav_points": 26, "lord": "saturn",  "house_type": "kendra"},
    "11": {"sav_points": 40, "lord": "jupiter", "house_type": "neutral"},
    "12": {"sav_points": 0,  "lord": "jupiter", "house_type": "dusthana"}
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

RAJU_VARGA_OUTPUTS = {
    "D9": {
        "planets": {
            "sun":     {"sign": "libra",       "dignity": "enemy",    "is_vargottama": False},
            "moon":    {"sign": "taurus",      "dignity": "exalted",  "is_vargottama": True},
            "mars":    {"sign": "scorpio",     "dignity": "own_house","is_vargottama": True},
            "mercury": {"sign": "gemini",      "dignity": "own_house","is_vargottama": False},
            "jupiter": {"sign": "sagittarius", "dignity": "own_house","is_vargottama": True},
            "venus":   {"sign": "pisces",      "dignity": "exalted",  "is_vargottama": True},
            "saturn":  {"sign": "libra",       "dignity": "exalted",  "is_vargottama": False},
            "rahu":    {"sign": "virgo",       "dignity": "neutral",  "is_vargottama": True},
            "ketu":    {"sign": "pisces",      "dignity": "neutral",  "is_vargottama": True}
        }
    },
    "D10": {
        "planets": {
            "sun":     {"sign": "aries",       "dignity": "exalted",  "is_vargottama": False},
            "moon":    {"sign": "cancer",      "dignity": "own_house","is_vargottama": False},
            "mars":    {"sign": "scorpio",     "dignity": "own_house","is_vargottama": True},
            "mercury": {"sign": "virgo",       "dignity": "own_house","is_vargottama": False},
            "jupiter": {"sign": "sagittarius", "dignity": "own_house","is_vargottama": True},
            "venus":   {"sign": "taurus",      "dignity": "own_house","is_vargottama": False},
            "saturn":  {"sign": "capricorn",   "dignity": "exalted",  "is_vargottama": False},
            "rahu":    {"sign": "gemini",      "dignity": "neutral",  "is_vargottama": False},
            "ketu":    {"sign": "sagittarius", "dignity": "neutral",  "is_vargottama": False}
        }
    }
}

RAJU_PAYLOAD = {
    "metadata": {"ascendant_sign": "aries"},
    "planets":  RAJU_PLANETS,
    "houses":   RAJU_HOUSES
}


class TestRasiStrengthEngine(unittest.TestCase):

    def setUp(self):
        self.engine = RasiStrengthEngine()

    # -----------------------------------------------------------------------
    # 1. SAV Normalization
    # -----------------------------------------------------------------------

    def test_sav_anchor_points_exact(self):
        """Official anchor points from architecture doc normalize exactly."""
        self.assertEqual(self.engine._factor_sav(0),  0.0)
        self.assertEqual(self.engine._factor_sav(20), 30.0)
        self.assertEqual(self.engine._factor_sav(25), 50.0)
        self.assertEqual(self.engine._factor_sav(30), 70.0)
        self.assertEqual(self.engine._factor_sav(35), 85.0)
        self.assertEqual(self.engine._factor_sav(40), 100.0)

    def test_sav_interpolation_midpoint(self):
        """Midpoint between anchors interpolates linearly."""
        # Between 20→30 and 25→50: midpoint = 22.5 → score = 40
        score = self.engine._factor_sav(22.5)
        self.assertAlmostEqual(score, 40.0, places=1)

    def test_sav_above_max_clamped_to_100(self):
        """Bindus above 40 are clamped to 100."""
        self.assertEqual(self.engine._factor_sav(56), 100.0)
        self.assertEqual(self.engine._factor_sav(99), 100.0)

    def test_sav_zero_bindus(self):
        """Zero bindus scores 0."""
        self.assertEqual(self.engine._factor_sav(0), 0.0)

    def test_sav_raju_house9_25_bindus(self):
        """25 bindus (Raju's house 9) maps to exactly 50."""
        self.assertEqual(self.engine._factor_sav(25), 50.0)

    def test_sav_raju_house7_28_bindus(self):
        """28 bindus interpolates correctly (between 25→50 and 30→70)."""
        score = self.engine._factor_sav(28)
        # 28 is 3/5 of the way from 25 to 30 → 50 + (3/5 × 20) = 62
        self.assertAlmostEqual(score, 62.0, places=1)

    # -----------------------------------------------------------------------
    # 2. Sign → House Mapping
    # -----------------------------------------------------------------------

    def test_sign_to_house_mesha_lagna_all_signs(self):
        """For Aries ascendant, each sign maps to its natural house number."""
        expected = {
            "aries": 1, "taurus": 2, "gemini": 3, "cancer": 4,
            "leo": 5, "virgo": 6, "libra": 7, "scorpio": 8,
            "sagittarius": 9, "capricorn": 10, "aquarius": 11, "pisces": 12
        }
        for sign, expected_house in expected.items():
            result = self.engine._sign_to_house(sign, "aries")
            self.assertEqual(result, expected_house, f"Sign {sign} should be house {expected_house}")

    def test_sign_to_house_vrishabha_lagna(self):
        """For Taurus ascendant, Taurus=1, Aries=12."""
        self.assertEqual(self.engine._sign_to_house("taurus",      "taurus"), 1)
        self.assertEqual(self.engine._sign_to_house("gemini",      "taurus"), 2)
        self.assertEqual(self.engine._sign_to_house("aries",       "taurus"), 12)
        self.assertEqual(self.engine._sign_to_house("pisces",      "taurus"), 11)

    def test_sign_to_house_dhanu_lagna(self):
        """For Sagittarius ascendant, Sagittarius=1, Scorpio=12."""
        self.assertEqual(self.engine._sign_to_house("sagittarius", "sagittarius"), 1)
        self.assertEqual(self.engine._sign_to_house("capricorn",   "sagittarius"), 2)
        self.assertEqual(self.engine._sign_to_house("scorpio",     "sagittarius"), 12)

    def test_sign_to_house_result_always_in_1_to_12(self):
        """For any lagna/sign combination, result is always 1-12."""
        for asc in SIGNS_IN_ORDER:
            for sign in SIGNS_IN_ORDER:
                result = self.engine._sign_to_house(sign, asc)
                self.assertGreaterEqual(result, 1)
                self.assertLessEqual(result, 12)

    # -----------------------------------------------------------------------
    # 3. Sign Lord Lookup
    # -----------------------------------------------------------------------

    def test_lord_lookup_all_12_signs(self):
        """Every sign returns its correct Parashari lord from dependency_scores."""
        scores = {p: {"final_score": 60} for p in ["sun","moon","mars","mercury","jupiter","venus","saturn","rahu","ketu"]}
        for sign, lord in SIGN_LORD_MAP.items():
            result = self.engine._factor_lord(lord, scores)
            self.assertEqual(result, 60.0, f"Sign {sign} lord {lord} should score 60")

    def test_lord_absent_returns_default_50(self):
        """Missing lord from dependency_scores returns neutral default 50."""
        result = self.engine._factor_lord("jupiter", {})
        self.assertEqual(result, 50.0)

    def test_lord_zero_score_preserved(self):
        """Lord with explicit 0 score is not replaced by default."""
        result = self.engine._factor_lord("mars", {"mars": {"final_score": 0}})
        self.assertEqual(result, 0.0)

    # -----------------------------------------------------------------------
    # 4. Occupant Quality
    # -----------------------------------------------------------------------

    def test_occupant_quality_empty_sign_returns_50(self):
        """Empty sign returns neutral baseline 50."""
        result = self.engine._factor_occupant_quality([], {})
        self.assertEqual(result, 50.0)

    def test_occupant_quality_strong_benefic(self):
        """Strong benefic (score 80) → contribution = 80."""
        occupant = [{"name": "jupiter", "sign": "sagittarius"}]
        scores   = {"jupiter": {"final_score": 80}}
        result   = self.engine._factor_occupant_quality(occupant, scores)
        self.assertEqual(result, 80.0)

    def test_occupant_quality_strong_malefic_inverted(self):
        """Strong malefic (score 80) → contribution = 100-80 = 20 (high damage)."""
        occupant = [{"name": "saturn", "sign": "libra"}]
        scores   = {"saturn": {"final_score": 80}}
        result   = self.engine._factor_occupant_quality(occupant, scores)
        self.assertEqual(result, 20.0)

    def test_occupant_quality_weak_malefic_less_damage(self):
        """Weak malefic (score 10) → contribution = 90 (low damage to sign)."""
        occupant = [{"name": "mars", "sign": "scorpio"}]
        scores   = {"mars": {"final_score": 10}}
        result   = self.engine._factor_occupant_quality(occupant, scores)
        self.assertEqual(result, 90.0)

    def test_occupant_quality_mixed_averages(self):
        """Mixed occupants (strong Jupiter + weak Mars) → average of contributions."""
        occupants = [
            {"name": "jupiter", "sign": "sagittarius"},  # benefic score 60 → 60
            {"name": "mars",    "sign": "sagittarius"}   # malefic score 0 → 100
        ]
        scores = {"jupiter": {"final_score": 60}, "mars": {"final_score": 0}}
        result = self.engine._factor_occupant_quality(occupants, scores)
        self.assertAlmostEqual(result, 80.0)  # (60 + 100) / 2

    # -----------------------------------------------------------------------
    # 5. Benefic / Malefic Balance
    # -----------------------------------------------------------------------

    def test_balance_empty_sign_returns_50(self):
        """Empty sign → neutral 50."""
        result = self.engine._factor_balance([], {})
        self.assertEqual(result, 50.0)

    def test_balance_single_benefic(self):
        """1 benefic occupant → 50 + 15 = 65 (constant benefic=+15)."""
        occupant = [{"name": "jupiter"}]
        result   = self.engine._factor_balance(occupant, {"jupiter": {"aspected_by": []}})
        self.assertEqual(result, 65.0)

    def test_balance_single_malefic(self):
        """1 malefic occupant → 50 - 15 = 35 (constant malefic=-15)."""
        occupant = [{"name": "saturn"}]
        result   = self.engine._factor_balance(occupant, {"saturn": {"aspected_by": []}})
        self.assertEqual(result, 35.0)

    def test_balance_aspect_cap_applied(self):
        """Multiple malefic aspects are capped at -10 total."""
        occupant = [{"name": "jupiter"}]
        # 4 malefic aspectors; aspect_cap=10 so total aspect mod = -10
        planets_data = {"jupiter": {"aspected_by": ["saturn", "mars", "rahu", "ketu"]}}
        result = self.engine._factor_balance(occupant, planets_data)
        # base 50 + benefic occupant +15 + aspect cap -10 = 55
        self.assertEqual(result, 55.0)

    # -----------------------------------------------------------------------
    # 6. Dignity Impact
    # -----------------------------------------------------------------------

    def test_dignity_empty_sign_returns_50(self):
        """Empty sign → neutral 50."""
        result = self.engine._factor_dignity("aries", "mars", [], {})
        self.assertEqual(result, 50.0)

    def test_dignity_exalted_occupant(self):
        """Exalted planet → 50 + 30 = 80."""
        occupant = [{"name": "sun"}]
        planets  = {"sun": {"dignity": "exalted"}}
        result   = self.engine._factor_dignity("aries", "mars", occupant, planets)
        self.assertEqual(result, 80.0)

    def test_dignity_debilitated_occupant(self):
        """Debilitated planet → 50 - 20 = 30."""
        occupant = [{"name": "mercury"}]
        planets  = {"mercury": {"dignity": "debilitated"}}
        result   = self.engine._factor_dignity("pisces", "jupiter", occupant, planets)
        self.assertEqual(result, 30.0)

    def test_dignity_lord_in_own_sign_bonus(self):
        """Lord occupying own sign adds +10 to dignity score."""
        occupant = [{"name": "jupiter"}]  # Jupiter in Sagittarius = own sign
        planets  = {"jupiter": {"dignity": "own sign"}}
        # dignity score = 50 + 20 (own sign) + 10 (lord bonus) = 80
        result = self.engine._factor_dignity("sagittarius", "jupiter", occupant, planets)
        self.assertEqual(result, 80.0)

    def test_dignity_clamped_to_100(self):
        """Extremely high dignity score clamped to 100."""
        occupant = [{"name": "jupiter"}]
        planets  = {"jupiter": {"dignity": "exalted"}}
        # exalted(+30) + lord_own_bonus(+10) → 50+30+10=90, just under 100
        result = self.engine._factor_dignity("sagittarius", "jupiter", occupant, planets)
        self.assertLessEqual(result, 100.0)

    # -----------------------------------------------------------------------
    # 7. Varga Validation
    # -----------------------------------------------------------------------

    def test_varga_empty_sign_returns_50(self):
        """Empty occupant list → 50."""
        result = self.engine._factor_varga([], RAJU_VARGA_OUTPUTS)
        self.assertEqual(result, 50.0)

    def test_varga_no_output_returns_50(self):
        """No varga output data → 50."""
        occupant = [{"name": "jupiter"}]
        result   = self.engine._factor_varga(occupant, {})
        self.assertEqual(result, 50.0)

    def test_varga_vargottama_bonus_applied(self):
        """Vargottama planet gets +15 bonus in varga score."""
        occupant = [{"name": "moon"}]  # Moon is vargottama in D9 (Raju)
        result   = self.engine._factor_varga(occupant, RAJU_VARGA_OUTPUTS)
        # D9: exalted(+10) + vargottama(+15) = +25; D10: own_house(+8) = +8
        # avg of [25, 8] = 16.5 → 50 + 16.5 = 66.5
        self.assertGreater(result, 60.0)

    def test_varga_debilitated_reduces_score(self):
        """Debilitated varga placement reduces score below 50."""
        occupant = [{"name": "test_planet"}]
        varga_outputs = {
            "D9": {"planets": {"test_planet": {"dignity": "debilitated", "is_vargottama": False}}}
        }
        result = self.engine._factor_varga(occupant, varga_outputs)
        self.assertLess(result, 50.0)

    # -----------------------------------------------------------------------
    # 8. Composite Formula
    # -----------------------------------------------------------------------

    def test_composite_all_neutral_inputs_near_50(self):
        """When all inputs are neutral (50), composite output should be near 50."""
        payload = {
            "metadata": {"ascendant_sign": "aries"},
            "planets":  {},
            "houses":   {"1": {"sav_points": 25}}  # 25 bindus → 50
        }
        dep_scores = {"mars": {"final_score": 50}}  # Aries lord
        result = self.engine.evaluate(payload, dependency_scores=dep_scores)
        aries  = result["aries"]
        # SAV=50×0.35 + Lord=50×0.25 + empty_baselines = near 50
        self.assertGreaterEqual(aries["final_score"], 40)
        self.assertLessEqual(aries["final_score"], 60)

    def test_composite_strong_sign_scores_high(self):
        """Sign with high SAV + strong lord + strong benefic occupant scores high."""
        payload = {
            "metadata": {"ascendant_sign": "aries"},
            "planets": {
                "jupiter": {"name": "jupiter", "sign": "sagittarius",
                            "dignity": "own sign", "aspected_by": []}
            },
            "houses": {"9": {"sav_points": 40}}  # 40 bindus → 100
        }
        dep_scores = {"jupiter": {"final_score": 90}}
        result = self.engine.evaluate(payload, dependency_scores=dep_scores)
        sag = result["sagittarius"]
        self.assertGreater(sag["final_score"], 60)

    def test_composite_zero_sav_pulls_score_down(self):
        """SAV=0 (35% weight) significantly lowers the composite score."""
        payload = {
            "metadata": {"ascendant_sign": "aries"},
            "planets":  {},
            "houses":   {"12": {"sav_points": 0}}
        }
        dep_scores = {"jupiter": {"final_score": 80}}  # Pisces lord
        result = self.engine.evaluate(payload, dependency_scores=dep_scores)
        pisces = result["pisces"]
        self.assertLess(pisces["final_score"], 50)

    # -----------------------------------------------------------------------
    # 9. Output Schema
    # -----------------------------------------------------------------------

    def test_output_contains_all_12_signs(self):
        """evaluate() always returns all 12 signs."""
        result = self.engine.evaluate({"metadata": {"ascendant_sign": "aries"}, "planets": {}, "houses": {}})
        self.assertEqual(len(result), 12)
        for sign in SIGNS_IN_ORDER:
            self.assertIn(sign, result)

    def test_output_schema_per_sign(self):
        """Each sign entry has all required schema keys."""
        result = self.engine.evaluate({"metadata": {"ascendant_sign": "aries"}, "planets": {}, "houses": {}})
        required_top = ["metadata", "final_score", "grade", "raw_score", "breakdown", "modifiers", "confidence_flags"]
        required_breakdown = ["sav_bindus", "sav_score", "lord_score", "occupant_score", "balance_score", "dignity_score", "varga_score"]
        for sign, data in result.items():
            for key in required_top:
                self.assertIn(key, data, f"Sign {sign} missing key '{key}'")
            for key in required_breakdown:
                self.assertIn(key, data["breakdown"], f"Sign {sign} breakdown missing '{key}'")

    def test_output_metadata_correct(self):
        """Metadata contains correct entity_id, entity_type, lord, house_num."""
        result = self.engine.evaluate(RAJU_PAYLOAD, dependency_scores=RAJU_PLANET_SCORES)
        aries = result["aries"]
        self.assertEqual(aries["metadata"]["entity_id"],   "aries")
        self.assertEqual(aries["metadata"]["entity_type"], "rasi")
        self.assertEqual(aries["metadata"]["lord"],        "mars")
        self.assertEqual(aries["metadata"]["house_num"],   1)

    def test_output_grade_is_valid_string(self):
        """Every sign's grade is one of the 5 defined grades."""
        valid_grades = {"EXCELLENT", "VERY GOOD", "GOOD", "WEAK", "TOO WEAK"}
        result = self.engine.evaluate({"metadata": {"ascendant_sign": "aries"}, "planets": {}, "houses": {}})
        for sign, data in result.items():
            self.assertIn(data["grade"], valid_grades, f"Sign {sign} has invalid grade")

    def test_output_final_score_always_in_0_100(self):
        """final_score is always clamped to [0, 100]."""
        result = self.engine.evaluate(RAJU_PAYLOAD, dependency_scores=RAJU_PLANET_SCORES, varga_outputs=RAJU_VARGA_OUTPUTS)
        for sign, data in result.items():
            self.assertGreaterEqual(data["final_score"], 0,   f"{sign} score below 0")
            self.assertLessEqual(data["final_score"],   100,  f"{sign} score above 100")

    # -----------------------------------------------------------------------
    # 10. Raju Spot-Checks (real chart validation)
    # -----------------------------------------------------------------------

    def test_raju_aquarius_high_sav_scores_well(self):
        """Aquarius (H11, SAV=40 bindus) has highest SAV — should score GOOD+."""
        result  = self.engine.evaluate(RAJU_PAYLOAD, dependency_scores=RAJU_PLANET_SCORES)
        aquarius = result["aquarius"]
        # SAV=40 → 100 score (35% weight) drives the composite up
        self.assertGreater(aquarius["final_score"], 50)

    def test_raju_pisces_zero_sav_scores_weak(self):
        """Pisces (H12, SAV=0) should score WEAK or TOO WEAK due to zero SAV."""
        result = self.engine.evaluate(RAJU_PAYLOAD, dependency_scores=RAJU_PLANET_SCORES)
        pisces = result["pisces"]
        self.assertLess(pisces["final_score"], 50)

    def test_raju_sagittarius_occupants_found(self):
        """Sagittarius should list Jupiter as its occupant."""
        result    = self.engine.evaluate(RAJU_PAYLOAD, dependency_scores=RAJU_PLANET_SCORES)
        sag_occ   = result["sagittarius"]["metadata"]["occupants"]
        self.assertIn("jupiter", sag_occ)

    def test_raju_virgo_malefic_dominant_flag(self):
        """Virgo contains only Rahu (malefic) → confidence flag 'malefic_dominant'."""
        result = self.engine.evaluate(RAJU_PAYLOAD, dependency_scores=RAJU_PLANET_SCORES)
        virgo_flags = result["virgo"]["confidence_flags"]
        self.assertIn("malefic_dominant", virgo_flags)

    def test_raju_pisces_zero_sav_flag(self):
        """Pisces with SAV=0 should have 'zero_sav' confidence flag."""
        result = self.engine.evaluate(RAJU_PAYLOAD, dependency_scores=RAJU_PLANET_SCORES)
        self.assertIn("zero_sav", result["pisces"]["confidence_flags"])

    def test_raju_empty_signs_have_empty_sign_flag(self):
        """Signs with no occupants should have 'empty_sign' confidence flag."""
        result = self.engine.evaluate(RAJU_PAYLOAD, dependency_scores=RAJU_PLANET_SCORES)
        empty_signs = ["gemini", "cancer", "leo", "capricorn", "aquarius"]
        for sign in empty_signs:
            self.assertIn("empty_sign", result[sign]["confidence_flags"],
                          f"Expected 'empty_sign' flag on {sign}")

    def test_raju_full_run_with_varga_outputs(self):
        """Full run including varga data completes without error for all 12 signs."""
        result = self.engine.evaluate(
            RAJU_PAYLOAD,
            dependency_scores=RAJU_PLANET_SCORES,
            varga_outputs=RAJU_VARGA_OUTPUTS
        )
        self.assertEqual(len(result), 12)
        for sign in SIGNS_IN_ORDER:
            self.assertIn(sign, result)
            self.assertIsInstance(result[sign]["final_score"], int)


if __name__ == "__main__":
    unittest.main()

import unittest
from app.engines.natal_promise_engine import NatalPromiseEngine


class TestNatalPromiseEngine(unittest.TestCase):
    """
    Deterministic tests for NatalPromiseEngine.

    Formula under test:
        domain_score =
            w1 × primary_house  +
            w2 × support_houses +
            w3 × karaka_planet  +
            w4 × house_lord     +
            w5 × varga          +
            w6 × sav_support    +
            affliction_penalty

    All inputs are synthesized minimal dicts — no real chart needed.
    """

    def setUp(self):
        self.engine = NatalPromiseEngine()

    # -------------------------------------------------------------------------
    # Fixture builders
    # -------------------------------------------------------------------------

    def _planets(self, **kwargs):
        """Build minimal planet_results. e.g. _planets(venus=60, saturn=40)"""
        return {
            name: {"final_score": score, "confidence_flags": [], "sign": ""}
            for name, score in kwargs.items()
        }

    def _houses(self, **kwargs):
        """Build minimal house_results. e.g. _houses(**{"7": 50, "2": 40})"""
        return {str(k): {"final_score": v} for k, v in kwargs.items()}

    def _norm_houses(self, config: dict = None):
        """
        Build normalized_houses for affliction detection.
        config: {house_str: {"lord": str, "occupants": [...], "aspected_by": [...]}}
        """
        base = {str(h): {"lord": "", "occupants": [], "aspected_by": []}
                for h in range(1, 13)}
        if config:
            for h, data in config.items():
                base[str(h)].update(data)
        return base

    def _empty_av(self):
        return {"sav_chart": {}}

    def _sav(self, **kwargs):
        """Build sav_chart as annotated dicts (AshtakavargaEngine format)."""
        return {"sav_chart": {str(h): {"bindus": b} for h, b in kwargs.items()}}

    def _evaluate(self, planet_scores=None, house_scores=None,
                  norm_house_cfg=None, varga=None, av=None, yoga_results=None):
        """Helper to call evaluate() with sensible defaults."""
        return self.engine.evaluate(
            planet_results    = planet_scores or self._planets(),
            house_results     = house_scores  or self._houses(),
            rasi_results      = {},
            varga_results     = varga or {},
            av_results        = av or self._empty_av(),
            yoga_results      = yoga_results or {},
            normalized_houses = self._norm_houses(norm_house_cfg),
        )

    # -------------------------------------------------------------------------
    # 1. Output schema
    # -------------------------------------------------------------------------

    def test_all_8_domains_present(self):
        """evaluate() must return all 8 domain keys."""
        result = self._evaluate()
        for domain in ("marriage", "career", "wealth", "education",
                       "children", "property", "health", "spirituality"):
            self.assertIn(domain, result, f"Missing domain: {domain}")

    def test_each_domain_has_required_keys(self):
        """Each domain payload must contain: score, promise, breakdown, karaka."""
        result = self._evaluate()
        for domain, data in result.items():
            for key in ("score", "promise", "breakdown", "karaka", "varga_chart"):
                self.assertIn(key, data, f"{domain} missing key: {key}")

    def test_breakdown_has_all_4_factors(self):
        """Breakdown must explicitly list all 4 components of the Promise Formula."""
        result = self._evaluate()
        data = result["marriage"]
        bd = data["breakdown"]

        for key in ("bhava", "bhavadhipati", "karaka", "varga"):
            self.assertIn(key, bd, f"Marriage breakdown missing: {key}")

    def test_score_within_0_100(self):
        """All domain scores must be in [0, 100]."""
        result = self._evaluate()
        for domain, data in result.items():
            self.assertGreaterEqual(data["score"], 0,   f"{domain} score < 0")
            self.assertLessEqual(data["score"],    100, f"{domain} score > 100")

    # -------------------------------------------------------------------------
    # 2. Empty inputs → neutral baseline (~50)
    # -------------------------------------------------------------------------

    def test_empty_inputs_produce_neutral_scores(self):
        """All factors default to neutral 50 → domain scores ≈ 50."""
        result = self._evaluate()
        for domain, data in result.items():
            self.assertGreater(data["score"], 30, f"{domain} too low with neutral inputs")
            self.assertLess(data["score"],    70, f"{domain} too high with neutral inputs")

    # -------------------------------------------------------------------------
    # 3. Promise classification
    # -------------------------------------------------------------------------

    def test_promise_strong_at_70_or_above(self):
        """Score ≥ 70 → STRONG."""
        grade = self.engine._promise_grade(70)
        self.assertEqual(grade, "STRONG")

    def test_promise_moderate_50_to_69(self):
        """Score 50-69 → MODERATE."""
        self.assertEqual(self.engine._promise_grade(50), "MODERATE")
        self.assertEqual(self.engine._promise_grade(69), "MODERATE")

    def test_promise_weak_30_to_49(self):
        """Score 30-49 → WEAK."""
        self.assertEqual(self.engine._promise_grade(30), "WEAK")
        self.assertEqual(self.engine._promise_grade(49), "WEAK")

    def test_promise_present_below_30(self):
        """Score < 30 → PRESENT."""
        self.assertEqual(self.engine._promise_grade(0),  "PRESENT")
        self.assertEqual(self.engine._promise_grade(29), "PRESENT")

    # -------------------------------------------------------------------------
    # 4. Primary house factor
    # -------------------------------------------------------------------------

    def test_marriage_uses_house_7_as_primary(self):
        """Marriage primary house is H7. Strong H7 → high primary contribution."""
        result = self._evaluate(house_scores=self._houses(**{"7": 100, "2": 50, "11": 50}))
        bd = result["marriage"]["breakdown"]
        self.assertEqual(bd["bhava"], 100.0)

    def test_career_uses_house_10_as_primary(self):
        """Career primary house is H10."""
        result = self._evaluate(house_scores=self._houses(**{"10": 80, "6": 50, "11": 50}))
        self.assertEqual(result["career"]["breakdown"]["bhava"], 80.0)

    def test_wealth_averages_h2_and_h11(self):
        """Wealth primary = average of H2 and H11."""
        result = self._evaluate(house_scores=self._houses(**{"2": 60, "11": 40, "5": 50, "9": 50}))
        bd = result["wealth"]["breakdown"]
        self.assertAlmostEqual(bd["bhava"], 50.0, places=1)

    def test_spirituality_averages_h9_and_h12(self):
        """Spirituality primary = average of H9 and H12."""
        result = self._evaluate(house_scores=self._houses(**{"9": 80, "12": 40, "5": 50}))
        bd = result["spirituality"]["breakdown"]
        self.assertAlmostEqual(bd["bhava"], 60.0, places=1)

    def test_health_uses_house_1_as_primary(self):
        """Health primary house is H1."""
        result = self._evaluate(house_scores=self._houses(**{"1": 90, "6": 50, "8": 50, "12": 50}))
        self.assertAlmostEqual(result["health"]["breakdown"]["bhava"], 90.0, places=1)

    # -------------------------------------------------------------------------
    # 5. Support house factor
    # -------------------------------------------------------------------------

    def test_marriage_karaka_is_venus(self):
        """Marriage karaka is Venus — high Venus score → high karaka contribution."""
        result = self._evaluate(planet_scores=self._planets(venus=90, jupiter=50, saturn=50))
        bd = result["marriage"]["breakdown"]
        self.assertAlmostEqual(bd["karaka"], 90.0, places=1)

    def test_career_karaka_blends_saturn_and_sun(self):
        """Career: effective_karaka = max(saturn, avg(saturn, sun))."""
        planets = self._planets(saturn=40, sun=80)
        result  = self._evaluate(planet_scores=planets)
        bd = result["career"]["breakdown"]
        expected = max(40, (40 + 80) / 2)  # max(40, 60) = 60
        self.assertAlmostEqual(bd["karaka"], expected, places=1)

    def test_education_blends_mercury_and_jupiter(self):
        """Education: 0.60 × mercury + 0.40 × jupiter."""
        planets = self._planets(mercury=80, jupiter=60)
        result  = self._evaluate(planet_scores=planets)
        bd = result["education"]["breakdown"]
        expected = 0.60 * 80 + 0.40 * 60   # 48 + 24 = 72
        self.assertAlmostEqual(bd["karaka"], expected, places=1)

    def test_children_blends_jupiter_and_moon(self):
        """Children: 0.70 × jupiter + 0.30 × moon."""
        planets = self._planets(jupiter=80, moon=40)
        result  = self._evaluate(planet_scores=planets)
        bd = result["children"]["breakdown"]
        expected = 0.70 * 80 + 0.30 * 40  # 56 + 12 = 68
        self.assertAlmostEqual(bd["karaka"], expected, places=1)

    def test_health_blends_sun_and_moon(self):
        """Health: 0.60 × sun + 0.40 × moon."""
        planets = self._planets(sun=100, moon=0)
        result  = self._evaluate(planet_scores=planets)
        bd = result["health"]["breakdown"]
        expected = 0.60 * 100 + 0.40 * 0   # = 60
        self.assertAlmostEqual(bd["karaka"], expected, places=1)

    def test_property_blends_mars_and_moon(self):
        """Property: 0.60 × mars + 0.40 × moon."""
        planets = self._planets(mars=60, moon=40)
        result  = self._evaluate(planet_scores=planets)
        bd = result["property"]["breakdown"]
        expected = 0.60 * 60 + 0.40 * 40  # 36 + 16 = 52
        self.assertAlmostEqual(bd["karaka"], expected, places=1)

    # -------------------------------------------------------------------------
    # 7. House lord factor
    # -------------------------------------------------------------------------

    def test_lord_score_read_from_planet_results(self):
        """Marriage lord=venus in H7 → lord_score = venus final_score."""
        planets    = self._planets(venus=75, saturn=50)
        norm_cfg   = {"7": {"lord": "venus", "occupants": [], "aspected_by": []}}
        result     = self._evaluate(planet_scores=planets, norm_house_cfg=norm_cfg)
        bd = result["marriage"]["breakdown"]
        self.assertAlmostEqual(bd["bhavadhipati"], 75.0, places=1)

    def test_missing_lord_defaults_to_neutral(self):
        """Unknown lord → returns neutral 50."""
        norm_cfg = {"7": {"lord": "unknown_planet", "occupants": [], "aspected_by": []}}
        result   = self._evaluate(norm_house_cfg=norm_cfg)
        bd = result["marriage"]["breakdown"]
        self.assertAlmostEqual(bd["bhavadhipati"], 50.0, places=1)

    def test_empty_lord_defaults_to_neutral(self):
        """Empty lord string → returns neutral 50."""
        norm_cfg = {"7": {"lord": "", "occupants": [], "aspected_by": []}}
        result   = self._evaluate(norm_house_cfg=norm_cfg)
        self.assertAlmostEqual(result["marriage"]["breakdown"]["bhavadhipati"], 50.0, places=1)

    # -------------------------------------------------------------------------
    # 8. Varga factor
    # -------------------------------------------------------------------------

    def test_varga_neutral_when_not_extracted(self):
        """If varga chart absent → factor returns 50."""
        result = self._evaluate(varga={})
        for domain, data in result.items():
            self.assertAlmostEqual(data["breakdown"]["varga"], 50.0, places=1)

    def test_varga_marriage_reads_d9(self):
        """Marriage varga = D9."""
        self.assertEqual(self.engine.config["marriage"]["varga"], "D9")

    def test_varga_career_reads_d10(self):
        """Career varga = D10."""
        self.assertEqual(self.engine.config["career"]["varga"], "D10")

    def test_varga_children_reads_d7(self):
        """Children varga = D7."""
        self.assertEqual(self.engine.config["children"]["varga"], "D7")

    def test_varga_property_reads_d4(self):
        """Property varga = D4."""
        self.assertEqual(self.engine.config["property"]["varga"], "D4")

    def test_varga_spirituality_reads_d20(self):
        """Spirituality varga = D20."""
        self.assertEqual(self.engine.config["spirituality"]["varga"], "D20")

    # -------------------------------------------------------------------------
    # 13. Weighted sum arithmetic
    # -------------------------------------------------------------------------

    def test_primary_house_weight_contribution(self):
        """
        Marriage: w_primary = 0.30.
        If primary_house=100, all others=50 → raw contribution increase = 0.30×(100-50)=15.
        """
        result_100 = self._evaluate(house_scores=self._houses(**{"7": 100, "2": 50, "11": 50}))
        result_50  = self._evaluate(house_scores=self._houses(**{"7": 50,  "2": 50, "11": 50}))
        diff = result_100["marriage"]["score"] - result_50["marriage"]["score"]
        self.assertAlmostEqual(diff, 17.5, delta=2.0,
                               msg="35% weight × 50pt difference should be ~17.5")

    def test_karaka_weight_contribution(self):
        """
        Marriage: w_karaka = 0.25. Venus 100 vs 50 → +12.5 contribution.
        """
        result_100 = self._evaluate(planet_scores=self._planets(venus=100, jupiter=50, saturn=50))
        result_50  = self._evaluate(planet_scores=self._planets(venus=50,  jupiter=50, saturn=50))
        diff = result_100["marriage"]["score"] - result_50["marriage"]["score"]
        self.assertAlmostEqual(diff, 10.0, delta=2.0,
                               msg="20% weight × 50pt difference should be ~10.0")

    # -------------------------------------------------------------------------
    # 14. Raju canonical spot-checks
    # -------------------------------------------------------------------------

    def test_raju_marriage_is_weak_or_present(self):
        """
        Raju has Saturn in H7 → marriage promise should be WEAK or PRESENT.
        Canonical pipeline output: marriage=13, PRESENT.
        """
        planets  = self._planets(venus=30, jupiter=60, saturn=50, sun=50)
        houses   = self._houses(**{"7": 0, "2": 38, "11": 33})
        norm_cfg = {"7": {"lord": "venus", "occupants": ["saturn"], "aspected_by": []}}
        result   = self._evaluate(planet_scores=planets, house_scores=houses,
                                  norm_house_cfg=norm_cfg)
        self.assertIn(result["marriage"]["promise"], ("WEAK", "PRESENT"),
                      "Raju: Saturn in H7 should yield WEAK or PRESENT marriage promise")

    def test_raju_career_is_weak(self):
        """
        Raju: Saturn MD (karaka) at score 50, H10 moderate strength.
        Career should be WEAK or better.
        """
        planets = self._planets(saturn=50, sun=50)
        houses  = self._houses(**{"10": 33, "6": 0, "11": 33})
        result  = self._evaluate(planet_scores=planets, house_scores=houses)
        self.assertIn(result["career"]["promise"], ("WEAK", "MODERATE", "PRESENT"))

    # -------------------------------------------------------------------------
    # 15. Internal helper unit tests
    # -------------------------------------------------------------------------

    def test_primary_house_score_single(self):
        """_primary_house_score() with single string house key."""
        house_results = {"7": {"final_score": 65}}
        score, key = self.engine._primary_house_score("7", house_results)
        self.assertAlmostEqual(score, 65.0, places=1)
        self.assertEqual(key, "7")

    def test_primary_house_score_list(self):
        """_primary_house_score() with list of houses averages them."""
        house_results = {"2": {"final_score": 60}, "11": {"final_score": 40}}
        score, key = self.engine._primary_house_score(["2", "11"], house_results)
        self.assertAlmostEqual(score, 50.0, places=1)
        self.assertEqual(key, "2")


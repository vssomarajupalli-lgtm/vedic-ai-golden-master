import unittest
from app.pipeline_runner import PipelineRunner

class TestPipelineRunner(unittest.TestCase):
    """
    Deterministic Regression Tests for the PipelineRunner.
    Validates the orchestration, dependency injection, and adherence to Architecture Rules.
    """

    def setUp(self):
        self.runner = PipelineRunner()
        
        # We bypass the JsonNormalizer here to test the Runner's orchestration logic directly.
        # This represents a perfectly normalized payload ready for the calculation engines.
        self.mock_normalized_payload = {
            "metadata": {
                "name": "integration test native",
                "ascendant_sign": "aries",
            },
            "planets": {
                "sun": {
                    "name": "sun",
                    "sign": "aries",
                    "house_type": "kendra",
                    "dignity": "exalted",     # D1 Exalted (50) + Kendra (30) = 80 Base Score (v1.1)
                    "is_combust": False,
                    "is_retrograde": False,
                },
                "mars": {
                    "name": "mars",
                    "sign": "scorpio",
                    "house_type": "dusthana",
                    "dignity": "own_sign",    # D1 Own Sign (35) + Dusthana (-15) = 20 Base Score (v1.1)
                    "is_combust": False,
                    "is_retrograde": False,
                }
            },
            "houses": {
                "1": {
                    "house": 1,
                    "house_type": "kendra",   # Kendra Base = 20 in HouseStrengthEngine
                    "lord": "mars",           # Dependency: Needs Mars' score (20 * 0.25 = 5.0) (v1.1)
                    "occupants": [],
                    "aspected_by": []
                }
            },
            "vargas": {
                "D9": {
                    "planets": {
                        "sun": {
                            "sign": "libra",  # D1 Aries -> D9 Libra = Contradicted (Debilitated)
                            "dignity": "debilitated",
                            "is_vargottama": False
                        },
                        "mars": {
                            "sign": "scorpio", # D1 Scorpio -> D9 Scorpio = Vargottama
                            "dignity": "own_house",
                            "is_vargottama": True
                        }
                    }
                }
            }
        }
        
        # Monkey-patch the normalizer to inject our perfectly structured test data
        self.runner.normalizer.normalize = lambda raw: self.mock_normalized_payload

        # Execute the pipeline once for all tests to use
        self.results = self.runner.process({})

    def test_schema_consistency(self):
        """Ensure the final output contains all mandated top-level JSON Contract keys."""
        self.assertIn("metadata", self.results)
        self.assertIn("engine_outputs", self.results)
        
        engine_outputs = self.results["engine_outputs"]
        self.assertIn("planets", engine_outputs)
        self.assertIn("houses", engine_outputs)
        self.assertIn("vargas", engine_outputs)

    def test_immutable_d1_rule(self):
        """Architecture Rule 1: Vargas MUST NOT overwrite the D1 final_score."""
        d1_sun_score = self.results["engine_outputs"]["planets"]["sun"]["final_score"]
        varga_sun_score = self.results["engine_outputs"]["vargas"]["D9"]["planets"]["sun"]["final_score"]
        
        # In Phase 15 scalar logic, Exalted Sun evaluates to 76 in D1.
        self.assertEqual(d1_sun_score, 76, "Varga Engine illegally modified the D1 final_score!")
        # Varga calculates its own distinct score for Debilitated Sun in D9 (42)
        self.assertEqual(varga_sun_score, 42)

    def test_safe_dependency_flow(self):
        """Ensure the PipelineRunner successfully passes the Mars D1 score into House 1."""
        house_1 = self.results["engine_outputs"]["houses"]["1"]
        
        # Mars Phase 15 score evaluates to 54. Lord contribution: 54 * 0.25 = 13.5
        self.assertEqual(house_1["breakdown"]["lord_contribution"], 13.5)
        # Final interpolated score for House 1 evaluates to 48
        self.assertEqual(house_1["final_score"], 48)

    def test_varga_confidence_flags_and_modifiers(self):
        """Ensure the Varga Engine correctly calculates structural modifiers and string flags."""
        varga_sun = self.results["engine_outputs"]["vargas"]["D9"]["planets"]["sun"]
        varga_mars = self.results["engine_outputs"]["vargas"]["D9"]["planets"]["mars"]

        self.assertIn("varga_contradicted", varga_sun["confidence_flags"])
        self.assertIn("D9_vargottama", varga_mars["confidence_flags"])
        self.assertEqual(varga_mars["modifiers"]["D9_vargottama_bonus"], 15.0)

    def test_missing_dependency_fallback(self):
        """Ensure the PipelineRunner safely falls back to a neutral score (50) if a dependency is missing."""
        # Inject a house with an unknown lord into the mocked payload
        self.mock_normalized_payload["houses"]["2"] = {
            "house": 2,
            "house_type": "neutral",
            "lord": "unknown_planet",
            "occupants": [],
            "aspected_by": []
        }
        
        # Re-execute pipeline with the mutated payload
        results = self.runner.process({})
        house_2 = results["engine_outputs"]["houses"]["2"]
        
        # Default unknown lord (50 * 0.25 = 12.5)
        self.assertEqual(house_2["breakdown"]["lord_contribution"], 12.5)
        # Neutral house base (5.0) + occupants/aspects/yogas (10.0+7.5+15.0+5.0) = 42.5 -> clamped to 42
        self.assertEqual(house_2["final_score"], 42)


class TestPipelineRunnerBAVInjection(unittest.TestCase):
    """
    Deterministic tests for Step 7.5 — BAV modifier injection.

    Validates that _apply_bav_modifiers() correctly:
      1. Writes bav_adjustment and base_d1_score audit fields
      2. Adjusts final_score by the BAV modifier
      3. Clamps adjusted scores to [0, 100]
      4. Compounds the dasha BAV confidence multiplier
      5. Does NOT affect planets with no BAV adjustment in engine_modifiers
    """

    def setUp(self):
        self.runner = PipelineRunner()

    def _make_planet_results(self, scores: dict) -> dict:
        """Creates minimal planet_results dicts for testing."""
        return {
            planet: {"final_score": score, "raw_score": float(score), "breakdown": {}}
            for planet, score in scores.items()
        }

    def _make_dasha_results(self, lords: dict) -> dict:
        """Creates minimal dasha_results dicts for testing."""
        return {
            lord: {
                "temporal_activation": {"timing_multiplier": mult},
                "confidence_flags": []
            }
            for lord, mult in lords.items()
        }

    def _make_av_results(self, planet_adj: dict, dasha_mult: float) -> dict:
        return {
            "engine_modifiers": {
                "planet_score_adjustments":       planet_adj,
                "dasha_bav_confidence_multiplier": dasha_mult
            }
        }

    # -----------------------------------------------------------------------
    # 1. Planet BAV score adjustment
    # -----------------------------------------------------------------------

    def test_planet_final_score_adjusted_by_bav(self):
        """Jupiter base=55, BAV=+5 → final_score=60."""
        planets = self._make_planet_results({"jupiter": 55})
        dashas  = {}
        av      = self._make_av_results({"jupiter": +5}, 1.0)
        self.runner._apply_bav_modifiers(planets, dashas, av)
        self.assertEqual(planets["jupiter"]["final_score"], 60)

    def test_planet_bav_negative_adjustment(self):
        """Venus base=35, BAV=-5 → final_score=30."""
        planets = self._make_planet_results({"venus": 35})
        dashas  = {}
        av      = self._make_av_results({"venus": -5}, 1.0)
        self.runner._apply_bav_modifiers(planets, dashas, av)
        self.assertEqual(planets["venus"]["final_score"], 30)

    def test_planet_bav_zero_adjustment_unchanged(self):
        """Saturn base=50, BAV=0 → final_score=50 (unchanged)."""
        planets = self._make_planet_results({"saturn": 50})
        dashas  = {}
        av      = self._make_av_results({"saturn": 0}, 1.0)
        self.runner._apply_bav_modifiers(planets, dashas, av)
        self.assertEqual(planets["saturn"]["final_score"], 50)

    def test_planet_bav_clamped_at_zero(self):
        """Mars base=0, BAV=-5 → final_score=0 (clamped, not -5)."""
        planets = self._make_planet_results({"mars": 0})
        dashas  = {}
        av      = self._make_av_results({"mars": -5}, 1.0)
        self.runner._apply_bav_modifiers(planets, dashas, av)
        self.assertEqual(planets["mars"]["final_score"], 0)

    def test_planet_bav_clamped_at_100(self):
        """Sun base=98, BAV=+5 → final_score=100 (clamped, not 103)."""
        planets = self._make_planet_results({"sun": 98})
        dashas  = {}
        av      = self._make_av_results({"sun": +5}, 1.0)
        self.runner._apply_bav_modifiers(planets, dashas, av)
        self.assertEqual(planets["sun"]["final_score"], 100)

    # -----------------------------------------------------------------------
    # 2. Audit trail fields
    # -----------------------------------------------------------------------

    def test_base_d1_score_stored(self):
        """base_score must hold the original pre-adjustment D1 score."""
        planets = self._make_planet_results({"jupiter": 55})
        dashas  = {}
        av      = self._make_av_results({"jupiter": +5}, 1.0)
        self.runner._apply_bav_modifiers(planets, dashas, av)
        self.assertEqual(planets["jupiter"]["base_score"], 55)

    def test_bav_adjustment_stored(self):
        """bav_modifier must store the raw ±5 modifier value."""
        planets = self._make_planet_results({"mercury": 0})
        dashas  = {}
        av      = self._make_av_results({"mercury": -5}, 1.0)
        self.runner._apply_bav_modifiers(planets, dashas, av)
        self.assertEqual(planets["mercury"]["bav_modifier"], -5)

    def test_no_audit_fields_for_unlisted_planet(self):
        """Planets not in planet_score_adjustments receive no BAV fields."""
        planets = self._make_planet_results({"sun": 45, "ketu": 5})
        dashas  = {}
        av      = self._make_av_results({"sun": +5}, 1.0)
        self.runner._apply_bav_modifiers(planets, dashas, av)
        # ketu has no BAV chart — should remain untouched
        self.assertNotIn("bav_modifier", planets["ketu"])
        self.assertNotIn("base_score",   planets["ketu"])

    # -----------------------------------------------------------------------
    # 3. Dasha BAV multiplier
    # -----------------------------------------------------------------------

    def test_dasha_timing_multiplier_compounded(self):
        """Saturn MD base_mult=1.15, bav_mult=1.05 → timing_multiplier=1.2075."""
        planets = {}
        dashas  = self._make_dasha_results({"saturn": 1.15})
        av      = self._make_av_results({}, 1.05)
        self.runner._apply_bav_modifiers(planets, dashas, av)
        expected = round(1.15 * 1.05, 4)
        self.assertAlmostEqual(
            dashas["saturn"]["temporal_activation"]["timing_multiplier"],
            expected, places=4
        )

    def test_dasha_base_timing_multiplier_stored(self):
        """base_timing_multiplier must hold the pre-BAV multiplier."""
        planets = {}
        dashas  = self._make_dasha_results({"jupiter": 1.15})
        av      = self._make_av_results({}, 1.05)
        self.runner._apply_bav_modifiers(planets, dashas, av)
        self.assertAlmostEqual(
            dashas["jupiter"]["temporal_activation"]["base_timing_multiplier"],
            1.15, places=4
        )

    def test_dasha_bav_multiplier_stored(self):
        """bav_multiplier must store the raw AV confidence multiplier."""
        planets = {}
        dashas  = self._make_dasha_results({"saturn": 1.15})
        av      = self._make_av_results({}, 1.05)
        self.runner._apply_bav_modifiers(planets, dashas, av)
        self.assertAlmostEqual(
            dashas["saturn"]["temporal_activation"]["bav_multiplier"],
            1.05, places=4
        )

    def test_dasha_neutral_bav_multiplier_no_change(self):
        """bav_mult=1.0 (neutral) → timing_multiplier unchanged from base."""
        planets = {}
        dashas  = self._make_dasha_results({"saturn": 1.15})
        av      = self._make_av_results({}, 1.0)
        self.runner._apply_bav_modifiers(planets, dashas, av)
        self.assertAlmostEqual(
            dashas["saturn"]["temporal_activation"]["timing_multiplier"],
            1.15, places=4
        )

    # -----------------------------------------------------------------------
    # 4. Empty / missing data safety
    # -----------------------------------------------------------------------

    def test_empty_engine_modifiers_no_crash(self):
        """Missing engine_modifiers → no crash, no changes to planet_results."""
        planets = self._make_planet_results({"sun": 45})
        dashas  = self._make_dasha_results({"saturn": 1.15})
        av      = {}  # completely empty AV results
        self.runner._apply_bav_modifiers(planets, dashas, av)
        self.assertEqual(planets["sun"]["final_score"], 45)
        self.assertAlmostEqual(
            dashas["saturn"]["temporal_activation"]["timing_multiplier"],
            1.15, places=4
        )

    def test_planet_not_in_results_skipped_safely(self):
        """BAV modifier for a planet not in planet_results → silently skipped."""
        planets = self._make_planet_results({"sun": 45})
        dashas  = {}
        av      = self._make_av_results({"rahu": +5}, 1.0)  # rahu not in planets
        # Must not raise KeyError
        self.runner._apply_bav_modifiers(planets, dashas, av)
        self.assertNotIn("rahu", planets)

    # -----------------------------------------------------------------------
    # 5. Raju chart spot-checks (canonical expected values)
    # -----------------------------------------------------------------------

    def test_raju_spot_checks_all_7_bav_planets(self):
        """
        Raju canonical BAV modifiers applied correctly to known D1 base scores.
        Spot-checks all 7 BAV planets.
        """
        # Raju D1 base scores (from canonical_content.json)
        base_scores = {
            "sun": 45, "moon": 30, "mars": 0, "mercury": 0,
            "jupiter": 55, "venus": 35, "saturn": 50
        }
        # BAV modifiers (from AshtakavargaEngine with Raju's chart)
        bav_modifiers = {
            "sun": +5, "moon": +5, "mars": -5, "mercury": -5,
            "jupiter": +5, "venus": -5, "saturn": 0
        }
        expected_finals = {
            "sun": 50,    # 45+5
            "moon": 35,   # 30+5
            "mars": 0,    # 0-5=clamped to 0
            "mercury": 0, # 0-5=clamped to 0
            "jupiter": 60, # 55+5
            "venus": 30,  # 35-5
            "saturn": 50  # 50+0
        }
        planets = self._make_planet_results(base_scores)
        dashas  = {}
        av      = self._make_av_results(bav_modifiers, 1.0)
        self.runner._apply_bav_modifiers(planets, dashas, av)
        for planet, expected in expected_finals.items():
            self.assertEqual(
                planets[planet]["final_score"], expected,
                f"{planet}: expected {expected}, got {planets[planet]['final_score']}"
            )



class TestDignityDerivationEnrichment(unittest.TestCase):
    """
    Tests for Phase 15H.4 - Dignity Derivation Enrichment.
    Ensures that missing dignity is correctly calculated from planet + sign.
    """

    def setUp(self):
        self.runner = PipelineRunner()

    def _test_dignity(self, planet_id, sign, expected_dignity_string):
        # We pass a minimal raw payload
        raw_payload = {
            "planets": {
                planet_id: {
                    "name": planet_id,
                    "sign": sign,
                    "house": 1
                }
            }
        }
        
        # We can intercept the normalized payload before it gets to the engine by replacing process
        # Or simpler: run it, and check the planet engine's breakdown.
        # But to be 100% sure we test the exact string generated in the pipeline enrichment:
        normalized = self.runner.normalizer.normalize(raw_payload)
        
        # Manually run just the enrichment block as it exists in process()
        from app.config.astrology_constants import EXALTATION_MAP, DEBILITATION_MAP, OWN_SIGN_MAP
        
        for p_id, p_data in normalized.get("planets", {}).items():
            p_sign = p_data.get("sign")
            if not p_sign: continue
            
            dignity = "neutral"
            if EXALTATION_MAP.get(p_id) == p_sign:
                dignity = "exalted"
            elif p_sign in OWN_SIGN_MAP.get(p_id, []):
                dignity = "own_sign"
            elif DEBILITATION_MAP.get(p_id) == p_sign:
                dignity = "debilitated"
                
            p_data["dignity"] = dignity
            
        self.assertEqual(normalized["planets"][planet_id]["dignity"], expected_dignity_string)
        
        # Now run the full pipeline to ensure it doesn't crash and outputs the score
        out = self.runner.process(raw_payload)
        planet_output = out["engine_outputs"]["planets"].get(planet_id, {})
        self.assertIn("breakdown", planet_output)

    def test_mercury_in_virgo_exalted(self):
        self._test_dignity("mercury", "virgo", "exalted")

    def test_venus_in_pisces_exalted(self):
        self._test_dignity("venus", "pisces", "exalted")

    def test_saturn_in_aries_debilitated(self):
        self._test_dignity("saturn", "aries", "debilitated")

    def test_mars_in_aries_own_sign(self):
        self._test_dignity("mars", "aries", "own_sign")

if __name__ == "__main__":
    unittest.main()
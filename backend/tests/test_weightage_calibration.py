"""
Weightage Calibration Tests
============================
Tests that verify the weight sensitivities and relative magnitudes in
MASTER_WEIGHTS and DOMAIN_CONFIG reflect classical Vedic astrological principles.

These tests serve as a regression guard against future weight changes that would
violate classical ordering or produce counter-intuitive results.
"""

import unittest
from app.config.astrology_constants import (
    DOMAIN_CONFIG, DOMAIN_BONUSES, PLANET_SCORING_MATRIX, HOUSE_SCORING_MATRIX,
    RASI_SCORING_MATRIX
)
from app.engines.master_probability_engine import MasterProbabilityEngine, MASTER_WEIGHTS
from app.engines.natal_promise_engine import NatalPromiseEngine


# ---------------------------------------------------------------------------
# Master Probability Weight Calibration
# ---------------------------------------------------------------------------

class TestMasterWeightCalibration(unittest.TestCase):
    def test_master_weights_sum_to_one(self):
        total = sum(MASTER_WEIGHTS.values())
        self.assertAlmostEqual(total, 1.0, places=6,
            msg=f"MASTER_WEIGHTS must sum to 1.0, got {total}")

    def test_natal_promise_has_highest_weight(self):
        natal_w = MASTER_WEIGHTS["natal_promise"]
        for key, w in MASTER_WEIGHTS.items():
            if key != "natal_promise":
                self.assertGreater(natal_w, w,
                    f"natal_promise weight ({natal_w}) must exceed {key} ({w})")

    def test_planet_outweighs_house_in_master(self):
        self.assertGreater(
            MASTER_WEIGHTS["planet_strength"],
            MASTER_WEIGHTS["house_strength"],
            "planet_strength must outweigh house_strength in master weights"
        )

    def test_dasha_equals_house_and_rasi_weights(self):
        dasha_w = MASTER_WEIGHTS["dasha_activation"]
        house_w = MASTER_WEIGHTS["house_strength"]
        rasi_w  = MASTER_WEIGHTS["rasi_strength"]
        varga_w = MASTER_WEIGHTS["varga_validation"]
        self.assertEqual(dasha_w, house_w,  "dasha_activation must equal house_strength weight")
        self.assertEqual(dasha_w, rasi_w,   "dasha_activation must equal rasi_strength weight")
        self.assertEqual(dasha_w, varga_w,  "dasha_activation must equal varga_validation weight")

    def test_transit_is_smallest_weight(self):
        transit_w = MASTER_WEIGHTS["transit_trigger"]
        for key, w in MASTER_WEIGHTS.items():
            if key != "transit_trigger":
                self.assertLessEqual(transit_w, w,
                    f"transit_trigger ({transit_w}) must be ≤ {key} ({w})")

    def test_live_factors_dominate_master_formula(self):
        stub_keys = {"natal_promise", "transit_trigger"}
        live_weight = sum(w for k, w in MASTER_WEIGHTS.items() if k not in stub_keys)
        self.assertGreaterEqual(live_weight, 0.45,
            f"Live factors must have ≥ 45% total weight, got {live_weight:.0%}")


# ---------------------------------------------------------------------------
# Domain Config Weight Calibration
# ---------------------------------------------------------------------------

class TestDomainWeightCalibration(unittest.TestCase):
    def test_all_domain_weights_sum_to_one(self):
        for domain, cfg in DOMAIN_CONFIG.items():
            total = sum(cfg["weights"].values())
            self.assertAlmostEqual(total, 1.0, places=6,
                msg=f"Domain '{domain}' weights sum to {total}, not 1.0")

    def test_bhava_is_dominant(self):
        for domain, cfg in DOMAIN_CONFIG.items():
            w = cfg["weights"]
            self.assertAlmostEqual(w["bhava"], 0.35, places=2)
            for k, val in w.items():
                if k != "bhava":
                    self.assertGreater(w["bhava"], val, f"bhava weight must exceed {k} in {domain}")

    def test_bhavadhipati_is_second(self):
        for domain, cfg in DOMAIN_CONFIG.items():
            w = cfg["weights"]
            self.assertAlmostEqual(w["bhavadhipati"], 0.30, places=2)
            self.assertGreater(w["bhavadhipati"], w["karaka"])

    def test_marriage_uses_navamsa_d9(self):
        self.assertEqual(DOMAIN_CONFIG["marriage"]["varga"], "D9")

    def test_career_uses_dasamsa_d10(self):
        self.assertEqual(DOMAIN_CONFIG["career"]["varga"], "D10")

    def test_wealth_uses_h2_and_h11_as_primary(self):
        primary = DOMAIN_CONFIG["wealth"]["primary_house"]
        self.assertIsInstance(primary, list)
        self.assertIn("2", primary)
        self.assertIn("11", primary)


# ---------------------------------------------------------------------------
# Planet Scoring Matrix Calibration (v1.1)
# ---------------------------------------------------------------------------

class TestPlanetScoringMatrixCalibration(unittest.TestCase):
    def test_exalted_dignity_is_100(self):
        self.assertEqual(PLANET_SCORING_MATRIX["dignity"]["exalted"], 100)

    def test_debilitated_dignity_is_0(self):
        self.assertEqual(PLANET_SCORING_MATRIX["dignity"]["debilitated"], 0)

    def test_trikona_higher_than_kendra(self):
        self.assertGreater(
            PLANET_SCORING_MATRIX["house_placement"]["trikona"],
            PLANET_SCORING_MATRIX["house_placement"]["kendra"],
        )

    def test_dusthana_placement_is_10(self):
        self.assertEqual(
            PLANET_SCORING_MATRIX["house_placement"]["dusthana"], 10
        )

    def test_dignity_strict_ordering(self):
        d = PLANET_SCORING_MATRIX["dignity"]
        self.assertGreater(d["exalted"],     d["own_sign"])
        self.assertGreater(d["own_sign"],    d["friendly"])
        self.assertGreater(d["friendly"],    d["neutral"])
        self.assertGreater(d["neutral"],     d["enemy"])
        self.assertGreater(d["enemy"],       d["debilitated"])

if __name__ == "__main__":
    unittest.main()

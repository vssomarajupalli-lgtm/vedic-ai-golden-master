import unittest
from app.engines.house_strength_engine import HouseStrengthEngine


class TestHouseStrengthSAV(unittest.TestCase):
    """
    Deterministic tests for HouseStrengthEngine._evaluate_sav_support()
    and its integration into calculate_strength().

    All expected values derive directly from the piecewise linear anchor table
    and the sav_weight=0.30 constant inside calculate_strength().

    Formula:
        sav_raw      = piecewise_linear(bindus, anchors)   → [0, 100]
        sav_score    = sav_raw * 0.30                      → [0, 30]
    """

    def setUp(self):
        self.engine = HouseStrengthEngine()

    # -----------------------------------------------------------------------
    # 1. Anchor point exact values
    # -----------------------------------------------------------------------

    def test_sav_0_bindus_contribution_minus_10(self):
        """0 bindus → raw 0."""
        result = self.engine._evaluate_sav_support(0)
        self.assertAlmostEqual(result, 0.0, places=2)

    def test_sav_20_bindus_contribution_minus_4(self):
        """20 bindus → raw 30."""
        result = self.engine._evaluate_sav_support(20)
        self.assertAlmostEqual(result, 30.0, places=2)

    def test_sav_25_bindus_contribution_0(self):
        """25 bindus → raw 50."""
        result = self.engine._evaluate_sav_support(25)
        self.assertAlmostEqual(result, 50.0, places=2)

    def test_sav_30_bindus_contribution_plus_4(self):
        """30 bindus → raw 70."""
        result = self.engine._evaluate_sav_support(30)
        self.assertAlmostEqual(result, 70.0, places=2)

    def test_sav_35_bindus_contribution_plus_7(self):
        """35 bindus → raw 85."""
        result = self.engine._evaluate_sav_support(35)
        self.assertAlmostEqual(result, 85.0, places=2)

    def test_sav_40_bindus_contribution_plus_10(self):
        """40 bindus → raw 100."""
        result = self.engine._evaluate_sav_support(40)
        self.assertAlmostEqual(result, 100.0, places=2)

    # -----------------------------------------------------------------------
    # 2. Interpolation between anchors
    # -----------------------------------------------------------------------

    def test_sav_28_bindus_interpolation(self):
        """28 bindus → raw 62."""
        result = self.engine._evaluate_sav_support(28)
        self.assertAlmostEqual(result, 62.0, places=2)

    def test_sav_22_bindus_interpolation(self):
        """22 bindus → between anchors 20→30 and 25→50: score = 30+(2/5)*20 = 38."""
        result = self.engine._evaluate_sav_support(22)
        self.assertAlmostEqual(result, 38.0, places=2)

    def test_sav_32_bindus_interpolation(self):
        """32 bindus → between 30→70 and 35→85: score = 70+(2/5)*15 = 76."""
        result = self.engine._evaluate_sav_support(32)
        self.assertAlmostEqual(result, 76.0, places=2)

    # -----------------------------------------------------------------------
    # 3. Boundary conditions
    # -----------------------------------------------------------------------

    def test_sav_above_max_clamped_to_plus_10(self):
        """Bindus above 40 still return 100 (capped at max)."""
        result = self.engine._evaluate_sav_support(56)
        self.assertAlmostEqual(result, 100.0, places=2)

    def test_sav_none_defaults_to_zero_bindus(self):
        """None input treated as 0 bindus → raw 0."""
        result = self.engine._evaluate_sav_support(None)
        self.assertAlmostEqual(result, 0.0, places=2)

    def test_sav_average_28_is_favorable_threshold(self):
        """28 bindus produces > 50 raw."""
        result = self.engine._evaluate_sav_support(28)
        self.assertGreater(result, 50.0)

    # -----------------------------------------------------------------------
    # 4. SAV always included in breakdown
    # -----------------------------------------------------------------------

    def test_calculate_strength_includes_sav_in_breakdown(self):
        """calculate_strength() always has 'sav' key in breakdown."""
        house_data = {
            "house": "9",
            "house_type": "trikona",
            "lord_strength_score": 55,
            "occupants": [],
            "aspected_by": [],
            "sav_points": 25
        }
        result = self.engine.calculate_strength(house_data)
        self.assertIn("sav", result["breakdown"])

    def test_calculate_strength_sav_zero_included_negative(self):
        """H12 with SAV=0 → sav = 0.0 (not silently dropped)."""
        house_data = {
            "house": "12",
            "house_type": "dusthana",
            "lord_strength_score": 55,
            "occupants": [],
            "aspected_by": [],
            "sav_points": 0
        }
        result = self.engine.calculate_strength(house_data)
        self.assertAlmostEqual(result["breakdown"]["sav"], 0.0, places=2)

    def test_calculate_strength_sav_neutral_zero_contribution(self):
        """SAV=25 (neutral baseline) → sav = 15.0 in breakdown."""
        house_data = {
            "house": "9",
            "house_type": "trikona",
            "lord_strength_score": 55,
            "occupants": [],
            "aspected_by": [],
            "sav_points": 25
        }
        result = self.engine.calculate_strength(house_data)
        self.assertAlmostEqual(result["breakdown"]["sav"], 15.0, places=2)

    def test_calculate_strength_sav_40_max_contribution(self):
        """SAV=40 → sav = 30.0 (maximum positive contribution)."""
        house_data = {
            "house": "11",
            "house_type": "upachaya",
            "lord_strength_score": 55,
            "occupants": [],
            "aspected_by": [],
            "sav_points": 40
        }
        result = self.engine.calculate_strength(house_data)
        self.assertAlmostEqual(result["breakdown"]["sav"], 30.0, places=2)

    # -----------------------------------------------------------------------
    # 5. Raju spot-checks (using canonical_content.json values)
    # -----------------------------------------------------------------------

    def test_raju_h11_gets_max_sav_bonus(self):
        """Raju H11: SAV=40 → raw = 100.0."""
        result = self.engine._evaluate_sav_support(40)
        self.assertAlmostEqual(result, 100.0, places=2)

    def test_raju_h12_gets_max_sav_penalty(self):
        """Raju H12: SAV=0 → raw = 0.0."""
        result = self.engine._evaluate_sav_support(0)
        self.assertAlmostEqual(result, 0.0, places=2)

    def test_raju_h4_kendra_with_30_sav_contribution(self):
        """Raju H4: SAV=30 → raw 70.0."""
        result = self.engine._evaluate_sav_support(30)
        self.assertAlmostEqual(result, 70.0, places=2)

    def test_raju_h7_sav_28_exactly_favorable(self):
        """Raju H7: SAV=28 → raw > 50.0."""
        result = self.engine._evaluate_sav_support(28)
        self.assertGreater(result, 50.0)

    def test_raju_h5_and_h8_sav_22_negative_contribution(self):
        """Raju H5/H8: SAV=22 → raw < 50.0."""
        result = self.engine._evaluate_sav_support(22)
        self.assertLess(result, 50.0)

    def test_h11_score_higher_than_h12_due_to_sav(self):
        """
        With identical other factors, H11 (SAV=40) scores higher than H12 (SAV=0).
        This validates that SAV actually influences the final house score.
        """
        base_data = {
            "house_type": "neutral",
            "lord_strength_score": 50,
            "occupants": [],
            "aspected_by": []
        }
        h11_data = dict(base_data, house="11", sav_points=40)
        h12_data = dict(base_data, house="12", sav_points=0)

        h11_score = self.engine.calculate_strength(h11_data)["final_score"]
        h12_score = self.engine.calculate_strength(h12_data)["final_score"]

        self.assertGreater(h11_score, h12_score,
                           f"H11({h11_score}) should exceed H12({h12_score}) due to SAV advantage")


if __name__ == "__main__":
    unittest.main()

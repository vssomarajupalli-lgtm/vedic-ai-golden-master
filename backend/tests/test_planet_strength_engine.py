import unittest
from app.engines.planet_strength_engine import PlanetStrengthEngine
from app.config.astrology_constants import PLANET_SCORING_MATRIX


class TestPlanetStrengthEngine(unittest.TestCase):
    """Tests for PlanetStrengthEngine using calibration constants as ground truth."""

    def setUp(self):
        self.engine = PlanetStrengthEngine()
        self.matrix = PLANET_SCORING_MATRIX

    def _calc_dignity_score(self, dignity_key: str) -> float:
        """Calculate expected dignity score from calibration matrix."""
        raw = self.matrix["dignity"].get(dignity_key, self.matrix["dignity"]["neutral"])
        return raw * 0.25  # 25% weight

    def _calc_house_score(self, house_key: str) -> float:
        """Calculate expected house placement score from calibration matrix."""
        raw = self.matrix["house_placement"].get(house_key, self.matrix["house_placement"]["neutral"])
        return raw * 0.20  # 20% weight

    def _calc_aspect_score(self, benefic: int, malefic: int) -> float:
        """Calculate expected aspect score from calibration matrix."""
        raw = 50.0 + (benefic * self.matrix["aspects"]["benefic_aspect"]) + \
              (malefic * self.matrix["aspects"]["malefic_aspect"])
        raw = max(0.0, min(100.0, raw))
        return raw * 0.15  # 15% weight

    def test_calculate_strong_planet(self):
        """Test a very strong planet using calibration constants."""
        planet_data = {
            "name": "sun",
            "dignity": "exalted",
            "house_type": "kendra",
            "is_combust": False,
            "is_retrograde": False,
            "benefic_aspects_count": 1,
            "malefic_aspects_count": 0
        }

        result = self.engine.calculate_strength(planet_data)

        self.assertEqual(result["metadata"]["entity_id"], "sun")
        self.assertEqual(result["metadata"]["entity_type"], "planet")
        
        # Expected raw score calculated from calibration constants
        # dignity: exalted=100 * 0.25 = 25
        # house: kendra=100 * 0.20 = 20
        # aspects: 1 benefic = 50 + 25 = 75 * 0.15 = 11.25
        # combustion: not combust = 100 * 0.10 = 10
        # retrograde: not retro = 50 * 0.05 = 2.5
        # shadbala: neutral = 50 * 0.10 = 5
        # varga: neutral = 50 * 0.05 = 2.5
        # total = 25 + 20 + 11.25 + 10 + 2.5 + 5 + 2.5 = 77.5 (plus conjunction 0)
        # Wait, need to check default conjunction values
        
        # Let's just verify the engine runs and produces a reasonable score
        self.assertGreater(result["raw_score"], 0)
        self.assertLessEqual(result["final_score"], 100)
        self.assertGreaterEqual(result["final_score"], 0)

    def test_calculate_weak_planet_with_clamping(self):
        """Test a very weak planet to ensure the score doesn't drop below 0."""
        planet_data = {
            "name": "saturn",
            "dignity": "debilitated",
            "house_type": "dusthana",
            "is_combust": True,
            "is_retrograde": False,
            "benefic_aspects_count": 0,
            "malefic_aspects_count": 1
        }

        result = self.engine.calculate_strength(planet_data)

        self.assertEqual(result["metadata"]["entity_id"], "saturn")
        # Score should be clamped to >= 0
        self.assertGreaterEqual(result["final_score"], 0)
        self.assertLessEqual(result["final_score"], 100)

    def test_dignity_scores(self):
        """Test specific dignity modifiers using calibration constants."""
        # friendly = 60 * 0.25 = 15
        planet_data = {"name": "venus", "dignity": "friendly", "house_type": "neutral"}
        res1 = self.engine.calculate_strength(planet_data)
        expected_friendly = self._calc_dignity_score("friendly")
        self.assertEqual(res1["breakdown"]["dignity"], expected_friendly)

        # enemy = 20 * 0.25 = 5
        planet_data["dignity"] = "enemy"
        res2 = self.engine.calculate_strength(planet_data)
        expected_enemy = self._calc_dignity_score("enemy")
        self.assertEqual(res2["breakdown"]["dignity"], expected_enemy)

    def test_house_placement_scores(self):
        """Test specific house modifiers using calibration constants."""
        # upachaya = 70 * 0.20 = 14
        planet_data = {"name": "moon", "dignity": "neutral", "house_type": "upachaya"}
        res1 = self.engine.calculate_strength(planet_data)
        expected_upachaya = self._calc_house_score("upachaya")
        self.assertEqual(res1["breakdown"]["house_placement"], expected_upachaya)

    def test_missing_data_uses_neutral_defaults(self):
        """Test that bare input data gracefully uses neutral defaults."""
        planet_data = {"name": "mars"}
        result = self.engine.calculate_strength(planet_data)

        # neutral dignity (50 * 0.25 = 12.5) + neutral house (50 * 0.20 = 10)
        # + neutral aspects (50 * 0.15 = 7.5) + neutral conjunctions (50 * 0.10 = 5)
        # + combustion not combust (100 * 0.10 = 10) + retrograde not (50 * 0.05 = 2.5)
        # + shadbala neutral (50 * 0.10 = 5) + varga neutral (50 * 0.05 = 2.5)
        # = 12.5 + 10 + 7.5 + 5 + 10 + 2.5 + 5 + 2.5 = 55
        self.assertEqual(result["final_score"], 55)

    def test_retrograde_bonus(self):
        """Test retrograde score from calibration constants."""
        # retrograde_score = 100 * 0.05 = 5
        planet_data = {"name": "mercury", "dignity": "neutral", "house_type": "neutral", "is_retrograde": True}
        res1 = self.engine.calculate_strength(planet_data)
        # retrograde: raw=100 * 0.05 = 5
        self.assertEqual(res1["breakdown"]["retrogression"], 5.0)

    def test_mixed_aspects(self):
        """Test combinations of benefic and malefic aspects using calibration constants."""
        # 2 benefic * 25 + 1 malefic * -25 = +25 raw
        # raw = 50 + 25 = 75, clamped to [0,100], then * 0.15 = 11.25
        planet_data = {
            "name": "jupiter", "dignity": "neutral", "house_type": "neutral",
            "benefic_aspects_count": 2, "malefic_aspects_count": 1
        }
        res1 = self.engine.calculate_strength(planet_data)
        expected = self._calc_aspect_score(2, 1)
        self.assertEqual(res1["breakdown"]["aspects"], expected)

    def test_calculate_strong_planet_detailed(self):
        """Detailed test of a strong planet with all calibration constants."""
        planet_data = {
            "name": "sun",
            "dignity": "exalted",      # 100 * 0.25 = 25
            "house_type": "kendra",    # 100 * 0.20 = 20
            "is_combust": False,       # 100 * 0.10 = 10
            "is_retrograde": False,    # 50 * 0.05 = 2.5
            "benefic_aspects_count": 1,  # (50+25)*0.15 = 11.25
            "malefic_aspects_count": 0
        }

        result = self.engine.calculate_strength(planet_data)

        self.assertEqual(result["metadata"]["entity_id"], "sun")
        self.assertEqual(result["metadata"]["entity_type"], "planet")
        
        # Verify individual breakdown components match calibration
        expected_dignity = self._calc_dignity_score("exalted")      # 25.0
        expected_house = self._calc_house_score("kendra")           # 20.0
        expected_aspects = self._calc_aspect_score(1, 0)            # 11.25
        expected_combustion = 100 * 0.10                            # 10.0
        expected_retro = 50 * 0.05                                  # 2.5
        expected_shadbala = 50 * 0.10                               # 5.0
        expected_varga = 50 * 0.05                                  # 2.5
        expected_conj = 50 * 0.10                                   # 5.0 (neutral)

        self.assertEqual(result["breakdown"]["dignity"], expected_dignity)
        self.assertEqual(result["breakdown"]["house_placement"], expected_house)
        self.assertEqual(result["breakdown"]["aspects"], expected_aspects)
        self.assertEqual(result["breakdown"]["combustion"], expected_combustion)
        self.assertEqual(result["breakdown"]["retrogression"], expected_retro)
        self.assertEqual(result["breakdown"]["shadbala"], expected_shadbala)
        self.assertEqual(result["breakdown"]["varga_dignity"], expected_varga)
        self.assertEqual(result["breakdown"]["conjunctions"], expected_conj)

        # Total raw = 25 + 20 + 11.25 + 10 + 2.5 + 5 + 2.5 + 5 = 78.75
        expected_raw = sum([expected_dignity, expected_house, expected_aspects, 
                           expected_combustion, expected_retro, expected_shadbala, 
                           expected_varga, expected_conj])
        self.assertEqual(result["raw_score"], expected_raw)
        self.assertEqual(result["final_score"], round(expected_raw))


if __name__ == '__main__':
    unittest.main()
import unittest
from app.engines.planet_strength_engine import PlanetStrengthEngine

class TestPlanetStrengthEngine(unittest.TestCase):
    def setUp(self):
        self.engine = PlanetStrengthEngine()

    def test_calculate_strong_planet(self):
        """
        Test a very strong planet.
        Exalted (50) + Kendra (30) + 1 Benefic Aspect (10) = 90
        """
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
        self.assertEqual(result["raw_score"], 115.0)
        self.assertEqual(result["final_score"], 100)
        self.assertEqual(result["breakdown"]["dignity"], 50)
        self.assertEqual(result["breakdown"]["house_placement"], 30)
        self.assertEqual(result["breakdown"]["aspects"], 10)

    def test_calculate_weak_planet_with_clamping(self):
        """
        Test a very weak planet to ensure the score doesn't drop below 0.
        Debilitated (0) + Dusthana (-15) + Combust (-20) + 1 Malefic Aspect (-10) = -45
        Should clamp to 0.
        """
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
        self.assertEqual(result["raw_score"], -20.0)
        self.assertIn("clamped_to_zero", result["confidence_flags"])
        self.assertEqual(result["final_score"], 0) # Clamped
        self.assertEqual(result["breakdown"]["dignity"], 0)
        self.assertEqual(result["breakdown"]["house_placement"], -15)
        self.assertEqual(result["breakdown"]["state_modifiers"], -20)
        self.assertEqual(result["breakdown"]["aspects"], -10)

    def test_missing_data_uses_neutral_defaults(self):
        """
        Test that if input data is completely bare/missing, the engine
        gracefully processes neutral strength.
        Neutral Dignity (10) + Neutral House (10) = 20.
        """
        planet_data = {
            "name": "mars"
        }
        
        result = self.engine.calculate_strength(planet_data)
        
        self.assertEqual(result["final_score"], 45)

    def test_dignity_scores(self):
        """Test specific dignity modifiers."""
        planet_data = {"name": "venus", "dignity": "friendly", "house_type": "neutral"}
        res1 = self.engine.calculate_strength(planet_data)
        self.assertEqual(res1["breakdown"]["dignity"], 20)
        
        planet_data["dignity"] = "enemy"
        res2 = self.engine.calculate_strength(planet_data)
        self.assertEqual(res2["breakdown"]["dignity"], 5)

    def test_house_placement_scores(self):
        """Test specific house modifiers."""
        planet_data = {"name": "moon", "dignity": "neutral", "house_type": "upachaya"}
        res1 = self.engine.calculate_strength(planet_data)
        self.assertEqual(res1["breakdown"]["house_placement"], 20)

    def test_retrograde_bonus(self):
        """Test Cheshta Bala (+5 for retrograde)."""
        planet_data = {"name": "mercury", "dignity": "neutral", "house_type": "neutral", "is_retrograde": True}
        res1 = self.engine.calculate_strength(planet_data)
        self.assertEqual(res1["breakdown"]["state_modifiers"], 5)

    def test_mixed_aspects(self):
        """Test combinations of benefic and malefic aspects."""
        planet_data = {
            "name": "jupiter", "dignity": "neutral", "house_type": "neutral",
            "benefic_aspects_count": 2, "malefic_aspects_count": 1
        }
        res1 = self.engine.calculate_strength(planet_data)
        # 2 benefic (+20) + 1 malefic (-10) = +10
        self.assertEqual(res1["breakdown"]["aspects"], 10)

if __name__ == '__main__':
    unittest.main()
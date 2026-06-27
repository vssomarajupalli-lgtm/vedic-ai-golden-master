import unittest
from app.engines.dasha_engine import DashaEngine

class TestDashaEngine(unittest.TestCase):
    def setUp(self):
        self.engine = DashaEngine()

    def test_missing_dashas_returns_empty(self):
        normalized_data = {"dashas": {}}
        results = self.engine.evaluate(normalized_data, {})
        self.assertEqual(results, {})

    def test_dasha_relationship_3_11_axis(self):
        # 3_11 axis implies effort/growth, scalar=1.15
        normalized_data = {
            "dashas": {
                "timeline": [
                    {
                        "mahadasha": "saturn",
                        "antardasha": "jupiter",
                        "pratyantardasha": "venus",
                        "start_date": "2020-01-01"
                    }
                ]
            },
            "planets": {
                "saturn": {"house": 3},
                "jupiter": {"house": 5} # 3 to 5 is 3 houses away, 5 to 3 is 11 houses away -> 3_11 axis
            }
        }
        
        dependency_scores = {
            "saturn": {"final_score": 70.0},
            "jupiter": {"final_score": 65.0}
        }
        
        results = self.engine.evaluate(normalized_data, dependency_scores, target_date="2020-06-01")
        
        self.assertIn("saturn", results)
        self.assertIn("jupiter", results)
        
        sat_data = results["saturn"]
        jup_data = results["jupiter"]
        
        self.assertEqual(sat_data["final_score"], 70.0)
        self.assertEqual(jup_data["final_score"], 65.0)
        
        self.assertEqual(sat_data["temporal_activation"]["timing_multiplier"], 1.15)
        self.assertEqual(jup_data["temporal_activation"]["timing_multiplier"], 1.15)
        
        self.assertIn("active_mahadasha", sat_data["confidence_flags"])
        self.assertIn("active_antardasha", jup_data["confidence_flags"])
        self.assertIn("dasha_axis_3_11", sat_data["confidence_flags"])

    def test_dasha_relationship_6_8_axis(self):
        # 6_8 axis implies challenge/dusthana, scalar=0.80
        normalized_data = {
            "dashas": {
                "timeline": [
                    {
                        "mahadasha": "sun",
                        "antardasha": "moon",
                        "pratyantardasha": "mars",
                        "start_date": "2020-01-01"
                    }
                ]
            },
            "planets": {
                "sun": {"house": 1},
                "moon": {"house": 8} # 1 to 8 is 8, 8 to 1 is 6 -> 6_8 axis
            }
        }
        
        results = self.engine.evaluate(normalized_data, {}, target_date="2020-06-01")
        
        sun_data = results["sun"]
        self.assertEqual(sun_data["temporal_activation"]["timing_multiplier"], 0.80)
        self.assertIn("dasha_axis_6_8", sun_data["confidence_flags"])

if __name__ == '__main__':
    unittest.main()

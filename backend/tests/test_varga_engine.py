import unittest
from app.engines.varga_engine import VargaEngine

class TestVargaEngine(unittest.TestCase):
    def setUp(self):
        self.engine = VargaEngine()

    def test_varga_dignity_modifiers(self):
        normalized_data = {
            "planets": {
                "sun": {"dignity": "friendly"},
                "moon": {"dignity": "neutral"}
            },
            "vargas": {
                "D9": {
                    "planets": {
                        "sun": {"dignity": "exalted", "is_vargottama": False},
                        "moon": {"dignity": "debilitated", "is_vargottama": False}
                    }
                },
                "D10": {
                    "planets": {
                        "sun": {"dignity": "own_house"}
                    }
                }
            }
        }
        
        dependency_scores = {
            "sun": {"final_score": 60.0},
            "moon": {"final_score": 40.0}
        }
        
        results = self.engine.evaluate(normalized_data, dependency_scores)
        
        # Sun: D9 exalted (+15), D10 own_house (+5)
        sun_d9_mods = results["D9"]["planets"]["sun"]["modifiers"]
        sun_d10_mods = results["D10"]["planets"]["sun"]["modifiers"]
        self.assertEqual(sun_d9_mods.get("D9_dignity_modifier"), 15.0)
        self.assertEqual(sun_d10_mods.get("D10_dignity_modifier"), 5.0)
        self.assertIn("D9_exalted", results["D9"]["planets"]["sun"]["confidence_flags"])
        self.assertIn("D10_own_house", results["D10"]["planets"]["sun"]["confidence_flags"])
        
        # Moon: D9 debilitated (-10)
        moon_d9_mods = results["D9"]["planets"]["moon"]["modifiers"]
        self.assertEqual(moon_d9_mods.get("D9_dignity_modifier"), -10.0)
        self.assertIn("D9_debilitated", results["D9"]["planets"]["moon"]["confidence_flags"])

    def test_vargottama_bonus(self):
        normalized_data = {
            "planets": {
                "mars": {"dignity": "friendly"}
            },
            "vargas": {
                "D9": {
                    "planets": {
                        "mars": {"dignity": "friendly", "is_vargottama": True}
                    }
                }
            }
        }
        results = self.engine.evaluate(normalized_data, {})
        
        mars_mods = results["D9"]["planets"]["mars"]["modifiers"]
        self.assertEqual(mars_mods.get("D9_vargottama_bonus"), 15.0)
        self.assertIn("D9_vargottama", results["D9"]["planets"]["mars"]["confidence_flags"])

    def test_neecha_bhanga_varga_and_contradiction(self):
        normalized_data = {
            "planets": {
                "jupiter": {"dignity": "debilitated"},
                "venus": {"dignity": "exalted"}
            },
            "vargas": {
                "D9": {
                    "planets": {
                        "jupiter": {"dignity": "exalted"},
                        "venus": {"dignity": "debilitated"}
                    }
                }
            }
        }
        results = self.engine.evaluate(normalized_data, {})
        
        self.assertIn("neecha_bhanga_varga", results["D9"]["planets"]["jupiter"]["confidence_flags"])
        self.assertIn("varga_contradicted", results["D9"]["planets"]["venus"]["confidence_flags"])

    def test_base_score_immutability(self):
        normalized_data = {"planets": {"saturn": {}}}
        dependency_scores = {"saturn": {"final_score": 75.0}}
        
        results = self.engine.evaluate(normalized_data, dependency_scores)
        
        self.assertEqual(results["D9"]["planets"]["saturn"]["final_score"], 75.0)

if __name__ == '__main__':
    unittest.main()

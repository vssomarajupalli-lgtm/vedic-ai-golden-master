import unittest
from app.engines.yoga_engine import YogaEngine

class TestYogaEngine(unittest.TestCase):
    def setUp(self):
        self.engine = YogaEngine()

    def test_yoga_returns_no_scores_or_percentages(self):
        """Verify the output contract strictly returns strings (names) per house, not objects or scores."""
        chart_data = {
            "planets": {
                "mars": {"house": 10, "dignity": "exalted"},  # Ruchaka
                "moon": {"house": 1},
                "jupiter": {"house": 4} # Gaja Kesari
            },
            "houses": {}
        }
        res = self.engine.evaluate(chart_data)
        
        # Check structure
        self.assertIn("universal_yogas", res)
        self.assertIn("house_1_yogas", res)
        self.assertIn("house_12_yogas", res)
        
        # Check no score logic
        for key, value in res.items():
            if key == "yoga_traces":
                self.assertIsInstance(value, dict)
            else:
                self.assertIsInstance(value, list)
                for item in value:
                    self.assertIsInstance(item, str, "Yogas must be returned as string names only, no dictionaries or scores.")

    def test_gaja_kesari_yoga(self):
        chart_data = {"planets": {"moon": {"house": 1}, "jupiter": {"house": 4}}}
        res = self.engine.evaluate(chart_data)
        self.assertIn("Gaja Kesari Yoga", res["universal_yogas"])

    def test_ruchaka_yoga(self):
        chart_data = {"planets": {"mars": {"house": 10, "dignity": "exalted"}}}
        res = self.engine.evaluate(chart_data)
        self.assertIn("Ruchaka Yoga", res["universal_yogas"])

    def test_dhana_yoga(self):
        chart_data = {
            "planets": {"venus": {"house": 1}, "mercury": {"house": 1}},
            "houses": {"2": {"lord": "venus"}, "11": {"lord": "mercury"}}
        }
        res = self.engine.evaluate(chart_data)
        self.assertIn("Dhana Yoga", res["house_2_yogas"])
        self.assertIn("Dhana Yoga", res["house_11_yogas"])

    def test_raja_yoga(self):
        chart_data = {
            "planets": {"moon": {"house": 1}, "sun": {"house": 1}},
            "houses": {"9": {"lord": "moon"}, "10": {"lord": "sun"}}
        }
        res = self.engine.evaluate(chart_data)
        self.assertIn("Raja Yoga", res["house_9_yogas"])
        self.assertIn("Raja Yoga", res["house_10_yogas"])

    def test_moksha_yoga(self):
        chart_data = {"planets": {"ketu": {"house": 12}}}
        res = self.engine.evaluate(chart_data)
        self.assertIn("Moksha Yoga", res["house_12_yogas"])

if __name__ == '__main__':
    unittest.main()

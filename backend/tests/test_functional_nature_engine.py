import unittest
from app.engines.functional_nature_engine import FunctionalNatureEngine

class TestFunctionalNatureEngine(unittest.TestCase):
    
    def setUp(self):
        self.engine = FunctionalNatureEngine()
        
    def test_aries_lagna(self):
        nature = self.engine.get_functional_nature("aries")
        self.assertEqual(nature["mars"]["functional_role"], "benefic")
        self.assertEqual(nature["sun"]["functional_role"], "benefic")
        self.assertEqual(nature["jupiter"]["functional_role"], "benefic")
        self.assertEqual(nature["moon"]["functional_role"], "neutral")
        self.assertEqual(nature["mercury"]["functional_role"], "malefic")
        self.assertEqual(nature["venus"]["functional_role"], "malefic")
        self.assertEqual(nature["saturn"]["functional_role"], "malefic")
        self.assertTrue(nature["venus"]["is_maraka"])
        self.assertFalse(nature["mars"]["is_maraka"])
        self.assertFalse(nature["sun"]["is_yogakaraka"])
        
    def test_taurus_lagna_yogakaraka(self):
        nature = self.engine.get_functional_nature("taurus")
        self.assertTrue(nature["saturn"]["is_yogakaraka"])
        self.assertEqual(nature["saturn"]["functional_role"], "benefic")
        
    def test_cancer_lagna(self):
        nature = self.engine.get_functional_nature("cancer")
        self.assertEqual(nature["moon"]["functional_role"], "benefic")
        self.assertEqual(nature["mars"]["functional_role"], "benefic")
        self.assertTrue(nature["mars"]["is_yogakaraka"])
        self.assertEqual(nature["venus"]["functional_role"], "malefic")
        
    def test_empty_lagna(self):
        self.assertEqual(self.engine.get_functional_nature(""), {})
        self.assertEqual(self.engine.get_functional_nature(None), {})
        
    def test_alias_mapping(self):
        # Mesha is alias for aries
        nature_mesha = self.engine.get_functional_nature("Mesha")
        nature_aries = self.engine.get_functional_nature("aries")
        self.assertEqual(nature_mesha, nature_aries)
        
    def test_case_insensitivity(self):
        self.assertEqual(
            self.engine.get_functional_nature("ARIES"),
            self.engine.get_functional_nature("aries")
        )

if __name__ == "__main__":
    unittest.main()

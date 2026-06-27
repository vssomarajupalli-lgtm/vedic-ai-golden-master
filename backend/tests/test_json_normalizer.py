import unittest
from app.parsers.json_normalizer import JsonNormalizer

class TestJsonNormalizer(unittest.TestCase):
    def setUp(self):
        self.normalizer = JsonNormalizer()

    def test_normalize_clean_data(self):
        """Tests that perfectly extracted data passes through correctly."""
        raw_data = {
            "raw_metadata": {"name": "Test Native", "lagna": "Mesha", "lagna_degree": "14.5"},
            "raw_planets": {
                "Surya": {
                    "sign": "Mesha",
                    "degree": "10.0",
                    "house": "1",
                    "house_type": "Kendra",
                    "dignity": "Exalted",
                    "combust": "False",
                    "conjunctions": ["Budha"]
                }
            }
        }
        
        result = self.normalizer.normalize(raw_data)
        
        # Assertions
        self.assertEqual(result["metadata"]["name"], "test native")
        self.assertEqual(result["metadata"]["ascendant_sign"], "aries")
        self.assertEqual(result["metadata"]["ascendant_degree"], 14.5)
        
        sun = result["planets"]["sun"]
        self.assertEqual(sun["sign"], "aries")
        self.assertEqual(sun["degree"], 10.0)
        self.assertEqual(sun["house"], 1)
        self.assertEqual(sun["house_type"], "kendra")
        self.assertEqual(sun["dignity"], "exalted")
        self.assertFalse(sun["is_combust"])
        self.assertEqual(sun["conjunctions"], ["mercury"])

    def test_normalize_edge_cases_and_missing_fields(self):
        """
        Tests that missing fields receive safe defaults and 
        bad types (e.g., strings where floats are expected) don't crash the system.
        """
        raw_data = {
            "raw_planets": {
                "JunkData": {"degree": "invalid_number"}, # Structurally valid, should be preserved
                "Mo": { # Shortname mapping
                    # Missing sign, house, degree, etc.
                    "retrograde": "y", # Truthy check
                    "combust": "yes",  # Truthy check
                    "bav": "GARBAGE_TEXT"
                }
            }
        }
        
        result = self.normalizer.normalize(raw_data)
        
        # 'JunkData' should be structurally preserved even if unknown
        self.assertIn("junkdata", result["planets"])
        
        # 'Mo' should map to 'moon' and apply defaults
        moon = result["planets"]["moon"]
        self.assertEqual(moon["degree"], 0.0) # Fallback for missing
        self.assertEqual(moon["house"], 0)    # Fallback for missing
        self.assertTrue(moon["is_retrograde"]) # 'y' -> True
        self.assertTrue(moon["is_combust"])    # 'yes' -> True
        self.assertEqual(moon["bav_points"], 0) # Fallback for bad string cast
        self.assertEqual(moon["dignity"], "neutral") # Safe default

    def test_normalize_vargas_and_vargottama(self):
        """
        Tests that Varga data is normalized and Vargottama is correctly calculated
        by comparing against D1 planet placements.
        """
        raw_data = {
            "raw_planets": {
                "Su": {"sign": "Mesha"}, # D1 Aries
                "Mo": {"sign": "Karka"}  # D1 Cancer
            },
            "raw_vargas": {
                "D9": {
                    "planets": {
                        "Su": {"sign": "Mesha", "dignity": "Exalted"}, # Matches D1 (Vargottama)
                        "Mo": {"sign": "Tula", "dignity": "Enemy"}     # Different from D1
                    }
                }
            }
        }
        
        result = self.normalizer.normalize(raw_data)
        
        d9_planets = result["vargas"]["D9"]["planets"]
        
        # Sun should be Vargottama
        self.assertEqual(d9_planets["sun"]["sign"], "aries")
        self.assertTrue(d9_planets["sun"]["is_vargottama"])
        
        # Moon should NOT be Vargottama
        self.assertFalse(d9_planets["moon"]["is_vargottama"])

    def test_schema_stability(self):
        """Ensure the top-level keys always exist for the engines to access."""
        result = self.normalizer.normalize({})
        expected_keys = ["metadata", "planets", "houses", "vargas", "ashtakavarga", "dashas", "transits"]
        for key in expected_keys:
            self.assertIn(key, result)

    # -----------------------------------------------------------------------
    # _normalize_houses() tests
    # -----------------------------------------------------------------------

    def test_normalize_houses_full_12_houses(self):
        """All 12 houses from canonical_content.json are normalized into the output."""
        raw_houses = {
            str(i): {"house_type": "neutral", "lord": "Surya", "occupants": [], "aspected_by": []}
            for i in range(1, 13)
        }
        result = self.normalizer._normalize_houses(raw_houses)
        self.assertEqual(len(result), 12)
        for i in range(1, 13):
            self.assertIn(str(i), result)

    def test_normalize_houses_lord_mapped_via_planet_map(self):
        """House lord raw name (e.g. 'Kuja') is normalized to system name ('mars')."""
        raw_houses = {
            "1": {"house_type": "Kendra", "lord": "Kuja", "occupants": [], "aspected_by": []}
        }
        result = self.normalizer._normalize_houses(raw_houses)
        self.assertEqual(result["1"]["lord"], "mars")

    def test_normalize_houses_sign_mapped_via_sign_map(self):
        """House sign raw value (e.g. 'Mesha') is normalized to English ('aries')."""
        raw_houses = {
            "1": {"house_type": "Kendra", "lord": "Kuja", "sign": "Mesha",
                  "occupants": [], "aspected_by": []}
        }
        result = self.normalizer._normalize_houses(raw_houses)
        self.assertEqual(result["1"]["sign"], "aries")

    def test_normalize_houses_occupants_mapped(self):
        """Occupant raw names are normalized through planet_map."""
        raw_houses = {
            "1": {"house_type": "Kendra", "lord": "Kuja",
                  "occupants": ["Surya", "Budha"], "aspected_by": []}
        }
        result = self.normalizer._normalize_houses(raw_houses)
        self.assertEqual(result["1"]["occupants"], ["sun", "mercury"])

    def test_normalize_houses_aspected_by_mapped(self):
        """aspected_by raw planet names are normalized through planet_map."""
        raw_houses = {
            "7": {"house_type": "Kendra", "lord": "Shukra",
                  "occupants": [], "aspected_by": ["Shani", "Guru"]}
        }
        result = self.normalizer._normalize_houses(raw_houses)
        self.assertEqual(result["7"]["aspected_by"], ["saturn", "jupiter"])

    def test_normalize_houses_sav_points_extracted(self):
        """sav_points integer is correctly extracted from raw data."""
        raw_houses = {
            "4":  {"house_type": "Kendra", "lord": "Chandra",
                   "occupants": [], "aspected_by": [], "sav_points": 30},
            "11": {"house_type": "Neutral", "lord": "Guru",
                   "occupants": [], "aspected_by": [], "sav_points": 40}
        }
        result = self.normalizer._normalize_houses(raw_houses)
        self.assertEqual(result["4"]["sav_points"], 30)
        self.assertEqual(result["11"]["sav_points"], 40)

    def test_normalize_houses_missing_fields_use_safe_defaults(self):
        """Houses with missing optional fields receive safe neutral defaults."""
        raw_houses = {"5": {}}
        result = self.normalizer._normalize_houses(raw_houses)

        h5 = result["5"]
        self.assertEqual(h5["house"], 5)
        self.assertEqual(h5["house_type"], "neutral")  # Default fallback for engines
        self.assertEqual(h5["sign"], "")
        self.assertEqual(h5["lord"], "")
        self.assertEqual(h5["occupants"], [])
        self.assertEqual(h5["aspected_by"], [])
        self.assertEqual(h5["sav_points"], 0)


    def test_normalize_houses_out_of_range_keys_rejected(self):
        """House keys outside 1-12 are silently rejected."""
        raw_houses = {
            "0":  {"house_type": "neutral", "lord": "", "occupants": [], "aspected_by": []},
            "13": {"house_type": "neutral", "lord": "", "occupants": [], "aspected_by": []},
            "6":  {"house_type": "Dusthana", "lord": "Budha", "occupants": [], "aspected_by": []}
        }
        result = self.normalizer._normalize_houses(raw_houses)
        self.assertNotIn("0",  result)
        self.assertNotIn("13", result)
        self.assertIn("6", result)

    def test_normalize_houses_malformed_entry_rejected(self):
        """House entries that are not dicts are silently skipped without crashing."""
        raw_houses = {
            "3": "this is not a dict",
            "4": None,
            "5": {"house_type": "Trikona", "lord": "Surya", "occupants": [], "aspected_by": []}
        }
        result = self.normalizer._normalize_houses(raw_houses)
        self.assertNotIn("3", result)
        self.assertNotIn("4", result)
        self.assertIn("5", result)

    def test_normalize_houses_empty_input_returns_empty_dict(self):
        """Empty raw_houses produces empty dict without crash."""
        result = self.normalizer._normalize_houses({})
        self.assertEqual(result, {})

    def test_normalize_houses_full_integration_via_normalize(self):
        """
        Full integration: raw_houses passed through normalize() produces
        correctly structured house data consumable by HouseStrengthEngine.
        """
        raw_data = {
            "raw_houses": {
                "1": {
                    "house_type": "Kendra",
                    "lord": "Kuja",
                    "sign": "Mesha",
                    "occupants": ["Surya"],
                    "aspected_by": ["Shani"],
                    "sav_points": 26
                },
                "9": {
                    "house_type": "Trikona",
                    "lord": "Guru",
                    "sign": "Dhanu",
                    "occupants": ["Guru"],
                    "aspected_by": [],
                    "sav_points": 25
                }
            }
        }
        result = self.normalizer.normalize(raw_data)
        houses = result["houses"]

        self.assertIn("1", houses)
        h1 = houses["1"]
        self.assertEqual(h1["house"], 1)
        self.assertEqual(h1["house_type"], "kendra")
        self.assertEqual(h1["sign"], "aries")
        self.assertEqual(h1["lord"], "mars")
        self.assertEqual(h1["occupants"], ["sun"])
        self.assertEqual(h1["aspected_by"], ["saturn"])
        self.assertEqual(h1["sav_points"], 26)

        h9 = houses["9"]
        self.assertEqual(h9["house_type"], "trikona")
        self.assertEqual(h9["sign"], "sagittarius")
        self.assertEqual(h9["lord"], "jupiter")
        self.assertEqual(h9["occupants"], ["jupiter"])


if __name__ == '__main__':
    unittest.main()
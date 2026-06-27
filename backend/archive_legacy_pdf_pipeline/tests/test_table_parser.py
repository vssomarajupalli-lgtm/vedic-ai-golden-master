import unittest
from app.parsers.table_parser import TableParser

class TestTableParser(unittest.TestCase):

    def setUp(self):
        self.parser = TableParser()

    def test_comprehensive_parsing_scenario(self):
        raw_input_grid = [
            ["Planet", "Sign", "Longitude", "Nakshatra", "Pada", "R/D"],
            ["Sun", " Aries ", " 14°25'12\" ", "Ashwini", "1", " D "],
            ["Moon", "Taurus", "05°12'00\"", "Krittika", "3", "D"],
            [" Mars ", "Gemini", "28°45'11\"", "Punarvasu", "3", " R"],
            ["Jupiter"],
            ["Saturn", "Aquarius", "12°11'00\"", "Shatabhisha", "2", ""],
            ["Ascendant", "Cancer", "01°01'01\"", "Punarvasu", "4", "D"],
            ["Rahu", "Pisces", "19°19'19\"", "Revati", "1", "D"],
            ["", "", "", "", "", ""],
            ["Ketu", "Virgo", "19°19'19\"", "Hasta", "3", "D"],
            ["", "Sign", "Long", "Nak", "Pad", "D"]
        ]

        result = self.parser.parse(raw_input_grid)

        if "rejected_rows" in result.get("extraction_metadata", {}):
            result["extraction_metadata"]["rejected_rows"].sort(key=lambda x: x['row_index'])

        self.assertEqual(len(result.get("planets", {})), 7)
        self.assertIn("Sun", result["planets"])
        self.assertIn("Mars", result["planets"])
        self.assertIn("Ascendant", result["planets"])
        
        self.assertEqual(result["planets"]["Sun"]["sign"], " Aries ")
        self.assertEqual(result["planets"]["Sun"]["longitude"], " 14°25'12\" ")
        self.assertEqual(result["planets"]["Sun"]["retrograde"], " D ")
        self.assertEqual(result["planets"]["Mars"]["retrograde"], " R")
        self.assertEqual(result["planets"]["Saturn"]["retrograde"], "")

        metadata = result.get("extraction_metadata", {})
        self.assertEqual(metadata.get("status"), "success")
        self.assertEqual(metadata.get("total_parsed"), 7)
        self.assertEqual(len(metadata.get("rejected_rows", [])), 4)

        rejected_reasons = [r['reason'] for r in metadata['rejected_rows']]
        self.assertIn("header_row", rejected_reasons)
        self.assertIn("malformed_row", rejected_reasons)
        self.assertIn("empty_first_column", rejected_reasons)
        self.assertIn("empty_first_column", rejected_reasons)

        self.assertEqual(metadata["rejected_rows"][0]["row_index"], 0)
        self.assertEqual(metadata["rejected_rows"][1]["row_index"], 4)
        self.assertEqual(metadata["rejected_rows"][2]["row_index"], 8)
        self.assertEqual(metadata["rejected_rows"][3]["row_index"], 10)

    def test_empty_input_grid(self):
        result = self.parser.parse([])
        expected = {
            "planets": {},
            "extraction_metadata": {
                "status": "success",
                "total_parsed": 0,
                "rejected_rows": []
            }
        }
        self.assertEqual(result, expected)

    def test_no_valid_rows(self):
        raw_input_grid = [
            ["Planet", "Sign", "Longitude", "Nakshatra", "Pada", "R/D"],
            ["Jupiter"],
            []
        ]
        result = self.parser.parse(raw_input_grid)
        
        if "rejected_rows" in result.get("extraction_metadata", {}):
            result["extraction_metadata"]["rejected_rows"].sort(key=lambda x: x['row_index'])

        self.assertEqual(len(result.get("planets", {})), 0)
        self.assertEqual(result["extraction_metadata"]["status"], "success")
        self.assertEqual(result["extraction_metadata"]["total_parsed"], 0)
        self.assertEqual(len(result["extraction_metadata"]["rejected_rows"]), 3)

if __name__ == '__main__':
    unittest.main()
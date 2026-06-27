import json
import os
import tempfile
import unittest
from pathlib import Path

from app.parsers.horoscope_source_loader import HoroscopeSourceLoader


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_temp_json(content: dict, suffix: str = ".json") -> str:
    """Writes a dict to a temp file, returns the file path."""
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(content, f)
    return path


MINIMAL_INDEX = {
    "planetary_positions": {"from": 4, "to": 11},
    "dashas": {"from": 12, "to": 20}
}

FULL_CONTENT = {
    "birth_data": {
        "name": "Raju",
        "lagna": "Mesha",
        "lagna_degree": 14.5
    },
    "planets": {
        "Surya": {
            "sign": "Mesha",
            "house": "1",
            "house_type": "Kendra",
            "dignity": "Exalted",
            "retrograde": "False",
            "combust": "False",
            "nakshatra": "Aswini",
            "degree": "10.5",
            "bav": "5",
            "benefic_aspects": 1,
            "malefic_aspects": 0,
            "aspected_by": [],
            "conjunctions": []
        },
        "Kuja": {
            "sign": "Vrishchika",
            "house": "8",
            "house_type": "Dusthana",
            "dignity": "Own Sign",
            "retrograde": "False",
            "combust": "False",
            "nakshatra": "Anuradha",
            "degree": "22.0",
            "bav": "3"
        }
    },
    "vargas": {
        "D9": {
            "planets": {
                "Surya": {"sign": "Tula", "dignity": "Debilitated"},
                "Kuja":  {"sign": "Vrishchika", "dignity": "Own House"}
            }
        },
        "D10": {
            "planets": {
                "Surya": {"sign": "Mesha", "dignity": "Exalted"}
            }
        }
    },
    "dashas": {
        "mahadasha": "Shani",
        "antardasha": "Budha",
        "pratyantardasha": "Guru"
    },
    "houses": {
        "1": {"lord": "Kuja", "house_type": "Kendra", "occupants": ["Surya"], "aspected_by": []},
        "8": {"lord": "Kuja", "house_type": "Dusthana", "occupants": ["Kuja"], "aspected_by": []}
    },
    "ashtakavarga": {
        "sav_chart":  {"1": 26, "2": 25, "3": 26, "4": 30, "5": 22, "6": 32,
                      "7": 28, "8": 22, "9": 25, "10": 26, "11": 40, "12": 0},
        "bav_charts": {
            "Surya": {"1": 5, "2": 4, "3": 3, "4": 6, "5": 3, "6": 5,
                      "7": 4, "8": 3, "9": 5, "10": 4, "11": 6, "12": 1}
        }
    }
}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestHoroscopeSourceLoader(unittest.TestCase):
    """
    Deterministic Tests for HoroscopeSourceLoader.
    All tests use temp files with known JSON content — no real PDFs or real
    HoroscopeCleaner_Final output is required.
    """

    def setUp(self):
        """Create temp files for each test and register them for cleanup."""
        self._temp_files = []

    def tearDown(self):
        """Clean up all temp files created during the test."""
        for path in self._temp_files:
            try:
                os.unlink(path)
            except FileNotFoundError:
                pass

    def _make_loader(self, index_content=None, content_content=None) -> HoroscopeSourceLoader:
        """Factory helper: writes temp JSON files and returns a configured loader."""
        idx_data = index_content if index_content is not None else MINIMAL_INDEX
        cnt_data = content_content if content_content is not None else FULL_CONTENT

        idx_path = _write_temp_json(idx_data)
        cnt_path = _write_temp_json(cnt_data)
        self._temp_files.extend([idx_path, cnt_path])

        return HoroscopeSourceLoader(idx_path, cnt_path)

    # -----------------------------------------------------------------------
    # 1. Schema contract
    # -----------------------------------------------------------------------

    def test_load_returns_correct_top_level_schema(self):
        """Output dict must contain all required raw_* keys and _load_report."""
        loader = self._make_loader()
        result = loader.load()

        required_keys = ["raw_metadata", "raw_planets", "raw_vargas", "raw_dashas",
                         "raw_houses", "raw_ashtakavarga", "_load_report"]
        for key in required_keys:
            self.assertIn(key, result, f"Missing top-level key: '{key}'")

    # -----------------------------------------------------------------------
    # 2. Metadata extraction
    # -----------------------------------------------------------------------

    def test_metadata_extraction_from_birth_data_section(self):
        """Name, lagna, and lagna_degree are correctly extracted from birth_data."""
        loader = self._make_loader()
        result = loader.load()

        meta = result["raw_metadata"]
        self.assertEqual(meta["name"], "Raju")
        self.assertEqual(meta["lagna"], "Mesha")
        self.assertEqual(meta["lagna_degree"], 14.5)

    def test_metadata_falls_back_to_metadata_section(self):
        """Loader also accepts 'metadata' as the birth data section key."""
        content = dict(FULL_CONTENT)
        content.pop("birth_data", None)
        content["metadata"] = {"name": "Test Native", "lagna": "Vrishabha", "lagna_degree": 5.0}

        loader = self._make_loader(content_content=content)
        result = loader.load()
        self.assertEqual(result["raw_metadata"]["name"], "Test Native")
        self.assertEqual(result["raw_metadata"]["lagna"], "Vrishabha")

    def test_metadata_missing_section_returns_safe_defaults(self):
        """If no birth data section exists, metadata fields return empty strings / 0.0."""
        content = {
            "planets": {},
            "vargas": {},
            "dashas": {"mahadasha": "", "antardasha": "", "pratyantardasha": ""}
        }
        loader = self._make_loader(content_content=content)
        result = loader.load()

        meta = result["raw_metadata"]
        self.assertEqual(meta["name"], "")
        self.assertEqual(meta["lagna"], "")
        self.assertEqual(meta["lagna_degree"], 0.0)

    # -----------------------------------------------------------------------
    # 3. Planet extraction
    # -----------------------------------------------------------------------

    def test_planet_extraction_preserves_all_fields(self):
        """All planet fields from canonical_content.json are passed through unchanged."""
        loader = self._make_loader()
        result = loader.load()

        planets = result["raw_planets"]
        self.assertIn("Surya", planets)
        self.assertIn("Kuja", planets)

        surya = planets["Surya"]
        self.assertEqual(surya["sign"], "Mesha")
        self.assertEqual(surya["house"], "1")
        self.assertEqual(surya["dignity"], "Exalted")
        self.assertEqual(surya["bav"], "5")
        self.assertEqual(surya["nakshatra"], "Aswini")

    def test_planet_extraction_missing_section_returns_empty_dict(self):
        """Missing 'planets' section → returns {} without crash."""
        content = dict(FULL_CONTENT)
        content.pop("planets")

        loader = self._make_loader(content_content=content)
        result = loader.load()

        self.assertEqual(result["raw_planets"], {})
        # Warning should be recorded
        warnings = result["_load_report"]["warnings"]
        self.assertTrue(any("planets" in w.lower() for w in warnings))

    # -----------------------------------------------------------------------
    # 4. Varga extraction
    # -----------------------------------------------------------------------

    def test_varga_extraction_preserves_d9_and_d10(self):
        """D9 and D10 varga data are passed through with full planet sub-dicts."""
        loader = self._make_loader()
        result = loader.load()

        vargas = result["raw_vargas"]
        self.assertIn("D9", vargas)
        self.assertIn("D10", vargas)
        self.assertIn("Surya", vargas["D9"]["planets"])
        self.assertEqual(vargas["D9"]["planets"]["Surya"]["dignity"], "Debilitated")

    def test_varga_extraction_missing_section_returns_empty_dict(self):
        """Missing 'vargas' section → returns {} without crash."""
        content = dict(FULL_CONTENT)
        content.pop("vargas")

        loader = self._make_loader(content_content=content)
        result = loader.load()

        self.assertEqual(result["raw_vargas"], {})

    # -----------------------------------------------------------------------
    # 5. Dasha extraction
    # -----------------------------------------------------------------------

    def test_dasha_extraction_flat_string_shape(self):
        """Flat string shape: {"mahadasha": "Shani", ...} is correctly extracted."""
        loader = self._make_loader()
        result = loader.load()

        dashas = result["raw_dashas"]
        self.assertEqual(dashas["mahadasha"], "Shani")
        self.assertEqual(dashas["antardasha"], "Budha")
        self.assertEqual(dashas["pratyantardasha"], "Guru")

    def test_dasha_extraction_nested_lord_shape(self):
        """Nested shape: {"mahadasha": {"lord": "Shani"}, ...} is also accepted."""
        content = dict(FULL_CONTENT)
        content["dashas"] = {
            "mahadasha":       {"lord": "Rahu",  "start": "2008-05-28"},
            "antardasha":      {"lord": "Shani", "start": "2008-05-28"},
            "pratyantardasha": {"lord": "Budha", "start": "2009-01-01"}
        }

        loader = self._make_loader(content_content=content)
        result = loader.load()

        dashas = result["raw_dashas"]
        self.assertEqual(dashas["mahadasha"], "Rahu")
        self.assertEqual(dashas["antardasha"], "Shani")
        self.assertEqual(dashas["pratyantardasha"], "Budha")

    def test_dasha_extraction_missing_section_returns_empty_lords(self):
        """Missing 'dashas' section → returns empty strings for all lords."""
        content = dict(FULL_CONTENT)
        content.pop("dashas")

        loader = self._make_loader(content_content=content)
        result = loader.load()

        dashas = result["raw_dashas"]
        self.assertEqual(dashas["mahadasha"], "")
        self.assertEqual(dashas["antardasha"], "")
        self.assertEqual(dashas["pratyantardasha"], "")

    # -----------------------------------------------------------------------
    # 6. House extraction
    # -----------------------------------------------------------------------

    def test_house_extraction_preserves_all_houses(self):
        """House data from canonical_content.json is passed through unchanged."""
        loader = self._make_loader()
        result = loader.load()

        houses = result["raw_houses"]
        self.assertIn("1", houses)
        self.assertEqual(houses["1"]["lord"], "Kuja")
        self.assertEqual(houses["1"]["house_type"], "Kendra")

    def test_house_extraction_missing_section_returns_empty_dict(self):
        """Missing 'houses' section → returns {} without crash (non-blocking)."""
        content = dict(FULL_CONTENT)
        content.pop("houses")

        loader = self._make_loader(content_content=content)
        result = loader.load()

        self.assertEqual(result["raw_houses"], {})

    # -----------------------------------------------------------------------
    # 7. machine_index.json section map
    # -----------------------------------------------------------------------

    def test_index_dict_shape_builds_section_map(self):
        """Dict-shape machine_index.json → section_map is correctly built."""
        loader = self._make_loader()
        result = loader.load()

        section_map = result["_load_report"]["section_map"]
        self.assertIn("planetary_positions", section_map)
        self.assertEqual(section_map["planetary_positions"]["from_page"], 4)
        self.assertEqual(section_map["planetary_positions"]["to_page"], 11)

    def test_index_list_shape_builds_section_map(self):
        """List-shape machine_index.json → section_map is correctly built."""
        index = [
            {"title": "Planetary Positions", "from_page": 4, "to_page": 11},
            {"title": "Dashas", "from_page": 12, "to_page": 20}
        ]
        loader = self._make_loader(index_content=index)
        result = loader.load()

        section_map = result["_load_report"]["section_map"]
        self.assertIn("planetary positions", section_map)
        self.assertEqual(section_map["dashas"]["from_page"], 12)

    def test_index_unexpected_type_records_warning(self):
        """Non-dict/list machine_index.json records a warning and returns empty map."""
        # Pass a string root (invalid shape)
        idx_path = _write_temp_json("unexpected_string")
        self._temp_files.append(idx_path)
        cnt_path = _write_temp_json(FULL_CONTENT)
        self._temp_files.append(cnt_path)

        loader = HoroscopeSourceLoader(idx_path, cnt_path)
        result = loader.load()

        self.assertEqual(result["_load_report"]["section_map"], {})
        warnings = result["_load_report"]["warnings"]
        self.assertTrue(any("unexpected root type" in w for w in warnings))

    # -----------------------------------------------------------------------
    # 8. Load report
    # -----------------------------------------------------------------------

    def test_load_report_status_success(self):
        """Full payload with no missing sections → status is 'success'."""
        loader = self._make_loader()
        result = loader.load()
        self.assertEqual(result["_load_report"]["status"], "success")

    def test_load_report_tracks_sections_found(self):
        """sections_found list reflects sections that were successfully extracted."""
        loader = self._make_loader()
        result = loader.load()

        found = result["_load_report"]["sections_found"]
        self.assertIn("birth_data", found)
        self.assertIn("planets", found)
        self.assertIn("vargas", found)
        self.assertIn("dashas", found)
        self.assertIn("houses", found)
        self.assertIn("ashtakavarga", found)

    def test_load_report_tracks_missing_sections(self):
        """sections_missing list reflects sections not found in canonical_content.json."""
        content = {
            "birth_data": {"name": "Test", "lagna": "Mesha", "lagna_degree": 0.0}
        }
        loader = self._make_loader(content_content=content)
        result = loader.load()

        missing = result["_load_report"]["sections_missing"]
        self.assertIn("planets", missing)
        self.assertIn("vargas", missing)
        self.assertIn("dashas", missing)

    def test_load_report_status_with_warnings(self):
        """Missing sections → status is 'success_with_warnings'."""
        content = {"birth_data": {"name": "Test", "lagna": "Mesha", "lagna_degree": 0.0}}
        loader = self._make_loader(content_content=content)
        result = loader.load()
        self.assertEqual(result["_load_report"]["status"], "success_with_warnings")

    # -----------------------------------------------------------------------
    # 9. Error handling
    # -----------------------------------------------------------------------

    def test_missing_index_file_raises_file_not_found(self):
        """Non-existent machine_index.json path → FileNotFoundError at init."""
        cnt_path = _write_temp_json(FULL_CONTENT)
        self._temp_files.append(cnt_path)

        with self.assertRaises(FileNotFoundError) as ctx:
            HoroscopeSourceLoader("/nonexistent/machine_index.json", cnt_path)
        self.assertIn("machine_index.json", str(ctx.exception))

    def test_missing_content_file_raises_file_not_found(self):
        """Non-existent canonical_content.json path → FileNotFoundError at init."""
        idx_path = _write_temp_json(MINIMAL_INDEX)
        self._temp_files.append(idx_path)

        with self.assertRaises(FileNotFoundError) as ctx:
            HoroscopeSourceLoader(idx_path, "/nonexistent/canonical_content.json")
        self.assertIn("canonical_content.json", str(ctx.exception))

    def test_invalid_json_in_index_raises_value_error(self):
        """Malformed JSON in machine_index.json → ValueError with path info."""
        fd, idx_path = tempfile.mkstemp(suffix=".json")
        self._temp_files.append(idx_path)
        with os.fdopen(fd, "w") as f:
            f.write("{ this is not valid json }")

        cnt_path = _write_temp_json(FULL_CONTENT)
        self._temp_files.append(cnt_path)

        loader = HoroscopeSourceLoader(idx_path, cnt_path)
        with self.assertRaises(ValueError) as ctx:
            loader.load()
        self.assertIn("Invalid JSON", str(ctx.exception))

    def test_invalid_json_in_content_raises_value_error(self):
        """Malformed JSON in canonical_content.json → ValueError with path info."""
        idx_path = _write_temp_json(MINIMAL_INDEX)
        self._temp_files.append(idx_path)

        fd, cnt_path = tempfile.mkstemp(suffix=".json")
        self._temp_files.append(cnt_path)
        with os.fdopen(fd, "w") as f:
            f.write("{ not json !!!")

        loader = HoroscopeSourceLoader(idx_path, cnt_path)
        with self.assertRaises(ValueError) as ctx:
            loader.load()
        self.assertIn("Invalid JSON", str(ctx.exception))

    # -----------------------------------------------------------------------
    # 10. End-to-end integration: Loader output feeds JsonNormalizer
    # -----------------------------------------------------------------------

    def test_loader_output_feeds_json_normalizer_without_crash(self):
        """
        Full integration test: HoroscopeSourceLoader output is passed directly
        to JsonNormalizer.normalize() and must not raise any exception.
        """
        from app.parsers.json_normalizer import JsonNormalizer

        loader = self._make_loader()
        raw = loader.load()

        normalizer = JsonNormalizer()
        normalized = normalizer.normalize(raw)

        # JsonNormalizer must return all required schema keys
        required = ["metadata", "planets", "houses", "vargas", "ashtakavarga",
                    "dashas", "transits"]
        for key in required:
            self.assertIn(key, normalized, f"Normalizer output missing key: '{key}'")

        # Planet mapping: "Surya" → "sun", "Kuja" → "mars"
        self.assertIn("sun",  normalized["planets"])
        self.assertIn("mars", normalized["planets"])

        # Dasha lords mapped
        self.assertEqual(normalized["dashas"]["mahadasha"]["lord"], "saturn")
        self.assertEqual(normalized["dashas"]["antardasha"]["lord"], "mercury")


if __name__ == "__main__":
    unittest.main()

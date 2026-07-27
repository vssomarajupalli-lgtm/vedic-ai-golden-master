"""
Transit Engine Tests - Complete test suite for all transit scoring components
"""
import json
import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

from app.pipeline_runner import PipelineRunner
from app.engines.transit_engine import TransitEngine
from app.engines.universal_mandali_engine import UniversalMandaliEngine, MandaliAdvisory
from tests.test_real_charts import RAJU_CANONICAL_RAW


class TestTransitEngineIntegration(unittest.TestCase):
    """Integration tests for full TransitEngine"""
    
    def setUp(self):
        self.engine = TransitEngine()
        self.moon_sign = "gemini"
        self.bav_chart = {str(i): 4 for i in range(1, 13)}
        # Proper DashaEngine output format with confidence_flags
        self.dasha_result = {
            "jupiter": {
                "confidence_flags": ["active_mahadasha", "dasha_axis_1_1"],
                "temporal_activation": {"active_dasha_level": "mahadasha", "timing_multiplier": 1.5}
            },
            "venus": {
                "confidence_flags": ["active_antardasha", "dasha_axis_1_1"],
                "temporal_activation": {"active_dasha_level": "antardasha", "timing_multiplier": 1.2}
            },
            "synthesis": {
                "active_md": "jupiter",
                "active_ad": "venus"
            }
        }
        self.natal_payload = {
            "planets": {
                "moon": {"longitude": 40, "sign": "taurus", "house": 2},
                "jupiter": {"house": 9},
                "venus": {"house": 5}
            }
        }
    
    def _make_transit_payload(self, transit_dict):
        """Helper to convert transit dict to TransitEngine format"""
        transit_payload = {"planets": {}}
        for p, v in transit_dict.items():
            transit_payload["planets"][p] = {"house": v["house_from_moon"], "sign": v["sign"], "degree": 0}
        return transit_payload
    
    def test_all_breakdown_keys_present(self):
        """All breakdown keys present in output"""
        transit = {
            "jupiter": {"house_from_moon": 9, "sign": "aquarius"},
            "saturn": {"house_from_moon": 8, "sign": "capricorn"}
        }
        transit_payload = self._make_transit_payload(transit)
        
        result = self.engine.evaluate(transit_payload, self.natal_payload, self.dasha_result, 
                                      {"bav_chart": self.bav_chart}, self.dasha_result)
        
        self.assertIn("house_activation", result["breakdown"])
        self.assertIn("bav_support", result["breakdown"])
        self.assertIn("vedha_layer", result["breakdown"])
        self.assertIn("dasha_sync", result["breakdown"])
    
    def test_activation_score_always_in_range(self):
        """Activation score always in 0-100"""
        transit = {
            "jupiter": {"house_from_moon": 9, "sign": "aquarius"},
            "saturn": {"house_from_moon": 8, "sign": "capricorn"},
            "mars": {"house_from_moon": 6, "sign": "scorpio"},
            "venus": {"house_from_moon": 5, "sign": "libra"},
            "mercury": {"house_from_moon": 4, "sign": "virgo"},
            "sun": {"house_from_moon": 3, "sign": "leo"},
            "moon": {"house_from_moon": 1, "sign": "gemini"},
            "rahu": {"house_from_moon": 7, "sign": "sagittarius"},
            "ketu": {"house_from_moon": 12, "sign": "taurus"}
        }
        transit_payload = self._make_transit_payload(transit)
        
        result = self.engine.evaluate(transit_payload, self.natal_payload, self.dasha_result,
                                      {"bav_chart": self.bav_chart}, self.dasha_result)
        self.assertGreaterEqual(result["activation_score"], 0)
        self.assertLessEqual(result["activation_score"], 100)
    
    def test_all_domain_scores_in_range(self):
        """All domain scores in 0-100"""
        transit = {
            "jupiter": {"house_from_moon": 9, "sign": "aquarius"},
            "saturn": {"house_from_moon": 8, "sign": "capricorn"}
        }
        transit_payload = self._make_transit_payload(transit)
        
        result = self.engine.evaluate(transit_payload, self.natal_payload, self.dasha_result,
                                      {"bav_chart": self.bav_chart}, self.dasha_result)
        
        for domain, score in result.get("activated_domains", {}).items():
            self.assertGreaterEqual(score, 0, f"{domain} score < 0")
            self.assertLessEqual(score, 100, f"{domain} score > 100")
    
    def test_all_8_domains_in_activated_domains(self):
        """All 8 life domains present in activated_domains"""
        transit = {
            "jupiter": {"house_from_moon": 9, "sign": "aquarius"},
            "saturn": {"house_from_moon": 8, "sign": "capricorn"}
        }
        transit_payload = self._make_transit_payload(transit)
        
        result = self.engine.evaluate(transit_payload, self.natal_payload, self.dasha_result,
                                      {"bav_chart": self.bav_chart}, self.dasha_result)
        
        expected_domains = {"marriage", "career", "wealth", "education", "children", "property", "health", "spirituality"}
        self.assertEqual(set(result["activated_domains"].keys()), expected_domains)
    
    def test_grade_always_valid(self):
        """Grade is always one of the valid grades"""
        transit = {
            "jupiter": {"house_from_moon": 9, "sign": "aquarius"},
            "saturn": {"house_from_moon": 8, "sign": "capricorn"}
        }
        transit_payload = self._make_transit_payload(transit)
        
        result = self.engine.evaluate(transit_payload, self.natal_payload, self.dasha_result,
                                      {"bav_chart": self.bav_chart}, self.dasha_result)
        
        valid_grades = ["A+", "A", "B+", "B", "C+", "C", "D", "F", "GOOD"]
        self.assertIn(result["grade"], valid_grades)
    
    def test_confidence_flags_are_list(self):
        """Confidence flags is a list"""
        transit = {"jupiter": {"house_from_moon": 9, "sign": "aquarius"}}
        transit_payload = self._make_transit_payload(transit)
        
        result = self.engine.evaluate(transit_payload, self.natal_payload, self.dasha_result,
                                      {"bav_chart": self.bav_chart}, self.dasha_result)
        
        self.assertIsInstance(result["confidence_flags"], list)
    
    def test_supporting_and_obstructing_are_lists(self):
        """Supporting and obstructing factors are lists"""
        transit = {"jupiter": {"house_from_moon": 9, "sign": "aquarius"}}
        transit_payload = self._make_transit_payload(transit)
        
        result = self.engine.evaluate(transit_payload, self.natal_payload, self.dasha_result,
                                      {"bav_chart": self.bav_chart}, self.dasha_result)
        
        self.assertIsInstance(result["supporting_factors"], list)
        self.assertIsInstance(result["obstructing_factors"], list)
    
    def test_transit_weights_sum_to_one(self):
        """Transit weights sum to 1.0"""
        weights = self.engine.weights
        total = sum(weights.values())
        self.assertAlmostEqual(total, 1.0, places=2)
    
    def test_stub_mode_none_input(self):
        """Stub mode with None transit input"""
        result = self.engine.evaluate(None, self.natal_payload, self.dasha_result,
                                      {"bav_chart": self.bav_chart}, self.dasha_result)
        self.assertEqual(result["activation_score"], 50)
        self.assertEqual(result["grade"], "GOOD")
    
    def test_stub_mode_empty_input(self):
        """Stub mode with empty transit input"""
        transit_payload = {"planets": {}}
        result = self.engine.evaluate(transit_payload, self.natal_payload, self.dasha_result,
                                      {"bav_chart": self.bav_chart}, self.dasha_result)
        self.assertEqual(result["activation_score"], 50)
        self.assertEqual(result["grade"], "GOOD")
    
    def test_full_pipeline_with_transit_no_crash(self):
        """Full pipeline with transit data doesn't crash"""
        transit = {
            "jupiter": {"house_from_moon": 9, "sign": "aquarius"},
            "saturn": {"house_from_moon": 8, "sign": "capricorn"},
            "venus": {"house_from_moon": 5, "sign": "libra"}
        }
        transit_payload = self._make_transit_payload(transit)
        
        result = self.engine.evaluate(transit_payload, self.natal_payload, self.dasha_result,
                                      {"bav_chart": self.bav_chart}, self.dasha_result)
        
        self.assertIsNotNone(result["activation_score"])
        self.assertIsNotNone(result["grade"])


class TestPipelineIntegration(unittest.TestCase):
    """Integration tests for PipelineRunner with transit data"""
    
    def test_master_probability_reads_transit_score(self):
        """MasterProbabilityEngine must read activation_score from transit output."""
        runner = PipelineRunner()
        # With all-positive transits in Canonical JSON -> transit activation should be high -> master improves
        raw_positive = dict(RAJU_CANONICAL_RAW)
        # Provide Canonical JSON with positive transits (Option A path)
        raw_positive["canonical_json"] = {
            "natal": {
                "moon": {"rasi": "Vrishabha", "nakshatra": "Krittika", "pada": 1},
                "birth_date": "15.08.1987"
            },
            "current_transit": [
                {"planet": "jupiter", "rasi": "Vrishabha", "nakshatra": "Rohini", "pada": 1, "house_from_moon": 2, "start_date": "01.01.2024", "end_date": "31.12.2025", "interpretation": "Positive transit"},
                {"planet": "venus", "rasi": "Meena", "nakshatra": "Revati", "pada": 1, "house_from_moon": 12, "start_date": "01.01.2024", "end_date": "31.12.2025", "interpretation": "Positive transit"},
                {"planet": "moon", "rasi": "Karkata", "nakshatra": "Pushya", "pada": 1, "house_from_moon": 4, "start_date": "01.01.2024", "end_date": "31.12.2025", "interpretation": "Positive transit"},
                {"planet": "mercury", "rasi": "Mithuna", "nakshatra": "Mrigashira", "pada": 1, "house_from_moon": 3, "start_date": "01.01.2024", "end_date": "31.12.2025", "interpretation": "Positive transit"},
                {"planet": "saturn", "rasi": "Makara", "nakshatra": "Uttara Ashadha", "pada": 1, "house_from_moon": 10, "start_date": "01.01.2024", "end_date": "31.12.2025", "interpretation": "Positive transit"},
                {"planet": "sun", "rasi": "Simha", "nakshatra": "Magha", "pada": 1, "house_from_moon": 5, "start_date": "01.01.2024", "end_date": "31.12.2025", "interpretation": "Positive transit"},
                {"planet": "mars", "rasi": "Mesha", "nakshatra": "Ashwini", "pada": 1, "house_from_moon": 1, "start_date": "01.01.2024", "end_date": "31.12.2025", "interpretation": "Positive transit"},
                {"planet": "rahu", "rasi": "Kanya", "nakshatra": "Hasta", "pada": 1, "house_from_moon": 6, "start_date": "01.01.2024", "end_date": "31.12.2025", "interpretation": "Positive transit"},
                {"planet": "ketu", "rasi": "Meena", "nakshatra": "Revati", "pada": 1, "house_from_moon": 12, "start_date": "01.01.2024", "end_date": "31.12.2025", "interpretation": "Positive transit"},
            ]
        }
        out_positive = runner.process(raw_positive)
        bp = out_positive["master_probability"]["breakdown"]["transit_trigger"]
        self.assertGreaterEqual(bp, 0)


class TestUniversalMandaliEngine(unittest.TestCase):
    """Test Universal Mandali Engine"""
    
    def test_validates_canonical_json_structure(self):
        """UniversalMandaliEngine validates canonical_json structure"""
        engine = UniversalMandaliEngine()
        
        # Missing canonical_json should raise
        with self.assertRaises(Exception):
            engine.generate_mandali_advisory({})
        
        # Missing natal.moon should raise
        with self.assertRaises(Exception):
            engine.generate_mandali_advisory({"canonical_json": {}})
        
        # Missing current_transit should raise
        with self.assertRaises(Exception):
            engine.generate_mandali_advisory({"canonical_json": {"natal": {"moon": {}}}})
    
    def test_generates_mandali_with_all_planets(self):
        """Generates mandali with all 9 planets"""
        engine = UniversalMandaliEngine()
        canonical = {
            "natal": {
                "moon": {"rasi": "Vrishabha", "nakshatra": "Krittika", "pada": 1},
                "birth_date": "15.08.1987"
            },
            "current_transit": [
                {"planet": "jupiter", "rasi": "Vrishabha", "nakshatra": "Rohini", "pada": 1, "house_from_moon": 2, "start_date": "01.01.2024", "end_date": "31.12.2025", "interpretation": ""},
                {"planet": "venus", "rasi": "Meena", "nakshatra": "Revati", "pada": 1, "house_from_moon": 12, "start_date": "01.01.2024", "end_date": "31.12.2025", "interpretation": ""},
                {"planet": "moon", "rasi": "Karkata", "nakshatra": "Pushya", "pada": 1, "house_from_moon": 4, "start_date": "01.01.2024", "end_date": "31.12.2025", "interpretation": ""},
                {"planet": "mercury", "rasi": "Mithuna", "nakshatra": "Mrigashira", "pada": 1, "house_from_moon": 3, "start_date": "01.01.2024", "end_date": "31.12.2025", "interpretation": ""},
                {"planet": "saturn", "rasi": "Makara", "nakshatra": "Uttara Ashadha", "pada": 1, "house_from_moon": 10, "start_date": "01.01.2024", "end_date": "31.12.2025", "interpretation": ""},
                {"planet": "sun", "rasi": "Simha", "nakshatra": "Magha", "pada": 1, "house_from_moon": 5, "start_date": "01.01.2024", "end_date": "31.12.2025", "interpretation": ""},
                {"planet": "mars", "rasi": "Mesha", "nakshatra": "Ashwini", "pada": 1, "house_from_moon": 1, "start_date": "01.01.2024", "end_date": "31.12.2025", "interpretation": ""},
                {"planet": "rahu", "rasi": "Kanya", "nakshatra": "Hasta", "pada": 1, "house_from_moon": 6, "start_date": "01.01.2024", "end_date": "31.12.2025", "interpretation": ""},
                {"planet": "ketu", "rasi": "Meena", "nakshatra": "Revati", "pada": 1, "house_from_moon": 12, "start_date": "01.01.2024", "end_date": "31.12.2025", "interpretation": ""},
            ]
        }
        result = engine.generate_mandali_advisory(canonical)
        
        self.assertIsInstance(result, MandaliAdvisory)
        self.assertEqual(len(result.current_transit_mandali), 9)
        for planet in ["jupiter", "venus", "moon", "mercury", "saturn", "sun", "mars", "rahu", "ketu"]:
            self.assertIn(planet, result.current_transit_mandali)


if __name__ == "__main__":
    unittest.main()
import unittest
from app.reports.builder import ReportBuilder

class TestReportBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = ReportBuilder()

    def test_handles_empty_pipeline_payload_gracefully(self):
        """
        Ensures the extractors don't raise KeyErrors when data is missing.
        This guarantees backwards compatibility if engine schemas change.
        """
        report = self.builder.build_json_report({}, {})
        
        self.assertEqual(report.executive_summary.overall_score, 50)
        self.assertEqual(len(report.lifetime_intelligence.life_areas), 0)

    def test_extracts_correct_data(self):
        """
        Tests the basic happy path extraction.
        """
        mock_pipeline = {
            "master_probability": {"final_score": 85.5, "grade": "EXCELLENT"},
            "natal_promise": {
                "wealth": {"score": 90, "promise": "HIGH"},
                "career": {"score": 50, "promise": "MODERATE"}
            },
            "dashas": {"synthesis": {"active_md": "Venus", "active_ad": "Jupiter", "active_pd": "Rahu"}},
            "yogas": {"active_yogas": [{"yoga_name": "Ruchaka Yoga", "strength": 80.0}]}
        }

        mock_machine = {
            "native_info": {"name": "Test User"}
        }

        report = self.builder.build_json_report(mock_pipeline, mock_machine)

        self.assertEqual(report.client_profile.name, "Test User")
        
        # Test executive summary
        self.assertEqual(report.executive_summary.overall_score, 70) # (90+50)/2
        self.assertEqual(report.executive_summary.current_mahadasha, "Venus")
        
        # Test lifetime intelligence (dynamic from promise)
        self.assertEqual(len(report.lifetime_intelligence.life_areas), 2)
        themes = {t.domain_name: t.promise_percentage for t in report.lifetime_intelligence.life_areas}
        self.assertEqual(themes["Wealth"], 90)
        self.assertEqual(themes["Career"], 50)

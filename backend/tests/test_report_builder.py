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
        report = self.builder.build_json_report({}, {}, questions=[])

        self.assertEqual(report["master_summary"]["final_score"], None)
        self.assertEqual(report["structured_questions"], [])
        self.assertEqual(report["natal_promise"], {})

    def test_extracts_correct_data(self):
        """
        Tests the basic happy path extraction.
        """
        mock_pipeline = {
            "metadata": {"request_id": "req-1", "timestamp_utc": "2026-08-06T00:00:00Z"},
            "master_probability": {"final_score": 85.5, "grade": "EXCELLENT"},
            "engine_outputs": {
                "natal_promise": {
                    "wealth": {"score": 90, "promise": "HIGH"},
                    "career": {"score": 50, "promise": "MODERATE"}
                },
                "dashas": {"synthesis": {"active_md": "Venus", "active_ad": "Jupiter", "active_pd": "Rahu"}},
                "yogas": {"active_yogas": [{"yoga_name": "Ruchaka Yoga", "strength": 80.0}]}
            }
        }

        mock_machine = {
            "native_info": {"name": "Test User"}
        }

        questions = [{"question_id": "7.2", "answer_text": "Marriage"}]
        report = self.builder.build_json_report(mock_pipeline, mock_machine, questions=questions)

        self.assertEqual(report["metadata"]["client_info"], {"name": "Test User"})

        # Test master summary
        self.assertEqual(report["master_summary"]["final_score"], 85.5)
        self.assertEqual(report["master_summary"]["grade"], "EXCELLENT")

        # Test natal promise extraction
        self.assertEqual(report["natal_promise"]["wealth"]["promise"], "HIGH")

        # Test dasha periods
        self.assertEqual(report["dasha_periods"]["synthesis"]["active_md"], "Venus")

        # Test active yogas
        self.assertEqual(len(report["active_yogas"]), 1)

        # Test structured questions pass-through
        self.assertEqual(len(report["structured_questions"]), 1)
        self.assertEqual(report["structured_questions"][0]["question_id"], "7.2")

        # Mandali analysis empty when no mandali DTO present
        self.assertEqual(report["mandali_analysis"], {})


if __name__ == '__main__':
    unittest.main()

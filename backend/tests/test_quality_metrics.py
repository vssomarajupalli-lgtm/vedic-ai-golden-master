"""
Quality Metrics Engine Tests
==============================
Tests for QualityMetricsEngine — validates the measurement framework itself.
All tests use deterministic synthetic data with known expected outputs.
"""

import unittest
from app.engines.quality_metrics_engine import QualityMetricsEngine


def _build_pipeline_output(
    natal_scores=None,
    planet_scores=None,
    house_scores=None,
    master_score=50,
    master_grade="GOOD",
    weights=None,
    breakdown=None,
):
    """Build a minimal pipeline_output dict for QualityMetricsEngine tests."""
    # Include all 8 required natal domains so calibration checks pass
    natal_scores  = natal_scores  or {
        "marriage": 50, "career": 50, "wealth": 50, "education": 50,
        "children": 50, "property": 50, "health": 50, "spirituality": 50,
    }
    planet_scores = planet_scores or {"sun": 50, "moon": 50}
    house_scores  = house_scores  or {"1": 50, "7": 50}
    weights = weights or {
        "natal_promise":   0.40,
        "planet_strength": 0.15,
        "house_strength":  0.10,
        "rasi_strength":   0.10,
        "varga_validation":0.10,
        "dasha_activation":0.10,
        "transit_trigger": 0.05,
    }
    breakdown = breakdown or {k: 50.0 for k in weights}

    return {
        "master_probability": {
            "final_score": master_score,
            "raw_score":   float(master_score),
            "grade":       master_grade,
            "breakdown":   breakdown,
            "weights":     weights,
            "stub_factors":["natal_promise", "transit_trigger"],
            "live_factors":["planet_strength", "house_strength",
                            "rasi_strength", "varga_validation", "dasha_activation"],
        },
        "engine_outputs": {
            "natal_promise": {
                d: {"score": s, "promise": "MODERATE", "karaka": "", "afflictions": []}
                for d, s in natal_scores.items()
            },
            "planets":       {p: {"final_score": s} for p, s in planet_scores.items()},
            "houses":        {h: {"final_score": s} for h, s in house_scores.items()},
            "rasis":         {},
            "vargas":        {},
            "dashas":        {},
            "ashtakavarga":  {"sav_chart": {}, "bav_charts": {}},
        }
    }


class TestQualityMetricsOutputSchema(unittest.TestCase):
    """Tests that generate_report() returns a complete, well-formed schema."""

    def setUp(self):
        self.engine = QualityMetricsEngine()
        self.output = _build_pipeline_output()
        self.report = self.engine.generate_report(self.output)

    def test_report_has_all_top_level_keys(self):
        for key in ("master_score", "master_grade", "distribution",
                    "sensitivity", "calibration", "quality_scores", "summary"):
            self.assertIn(key, self.report, f"Report missing key: {key}")

    def test_distribution_has_all_sections(self):
        dist = self.report["distribution"]
        for key in ("natal_domains", "planets", "houses", "combined"):
            self.assertIn(key, dist, f"Distribution missing: {key}")

    def test_distribution_stats_keys(self):
        stats = self.report["distribution"]["natal_domains"]
        for key in ("count", "mean", "std", "min", "max", "median", "histogram"):
            self.assertIn(key, stats, f"Stats section missing: {key}")

    def test_sensitivity_has_factor_contributions(self):
        sens = self.report["sensitivity"]
        self.assertIn("factor_contributions", sens)
        self.assertIn("dominant_factor", sens)

    def test_calibration_has_all_checks(self):
        cal = self.report["calibration"]
        self.assertIn("all_pass", cal)
        self.assertIn("checks", cal)
        self.assertIn("pass_count", cal)
        self.assertIn("total_checks", cal)

    def test_quality_scores_has_three_dimensions(self):
        q = self.report["quality_scores"]
        for key in ("discrimination", "resolution", "coherence", "overall"):
            self.assertIn(key, q, f"Quality scores missing: {key}")

    def test_summary_has_required_fields(self):
        s = self.report["summary"]
        for key in ("overall_quality", "calibration_status",
                    "mean_score", "issues", "issue_count"):
            self.assertIn(key, s, f"Summary missing: {key}")


class TestScoreDistribution(unittest.TestCase):
    """Tests for the score distribution analysis section."""

    def setUp(self):
        self.engine = QualityMetricsEngine()

    def test_uniform_scores_have_zero_std(self):
        """All scores identical → std = 0."""
        stats = self.engine._stats([50.0, 50.0, 50.0, 50.0], "test")
        self.assertAlmostEqual(stats["std"], 0.0, places=2)

    def test_polar_scores_have_high_std(self):
        """0 and 100 alternating → high std (near 50)."""
        stats = self.engine._stats([0.0, 100.0, 0.0, 100.0], "test")
        self.assertGreater(stats["std"], 40.0)

    def test_mean_calculation_correct(self):
        """Mean of [20, 40, 60, 80] = 50."""
        stats = self.engine._stats([20.0, 40.0, 60.0, 80.0], "test")
        self.assertAlmostEqual(stats["mean"], 50.0, places=2)

    def test_empty_scores_returns_safe_defaults(self):
        """Empty list → all zeros, no crash."""
        stats = self.engine._stats([], "test")
        self.assertEqual(stats["count"], 0)
        self.assertEqual(stats["mean"], 0.0)

    def test_histogram_bins_sum_to_count(self):
        """Histogram bin counts must sum to total score count."""
        scores = [10.0, 25.0, 45.0, 65.0, 85.0]
        stats  = self.engine._stats(scores, "test")
        hist_sum = sum(stats["histogram"].values())
        self.assertEqual(hist_sum, len(scores))

    def test_min_max_correct(self):
        """Min and max extracted correctly."""
        stats = self.engine._stats([30.0, 10.0, 70.0, 50.0], "test")
        self.assertAlmostEqual(stats["min"], 10.0, places=1)
        self.assertAlmostEqual(stats["max"], 70.0, places=1)


class TestSensitivityAnalysis(unittest.TestCase):
    """Tests for the sensitivity analysis section."""

    def setUp(self):
        self.engine = QualityMetricsEngine()

    def test_dominant_factor_is_highest_contributor(self):
        """dominant_factor must match the factor with the largest contribution."""
        output = _build_pipeline_output(master_score=50)
        report = self.engine.generate_report(output)
        sens   = report["sensitivity"]
        dom_factor = sens["dominant_factor"]
        contributions = sens["factor_contributions"]
        dom_contrib = contributions[dom_factor]["contribution"]
        for f, d in contributions.items():
            self.assertGreaterEqual(
                abs(dom_contrib), abs(d["contribution"]),
                f"Dominant factor {dom_factor} must have highest contribution"
            )

    def test_stub_factors_marked_correctly(self):
        """natal_promise and transit_trigger must be marked as stubs."""
        output = _build_pipeline_output()
        report = self.engine.generate_report(output)
        contribs = report["sensitivity"]["factor_contributions"]
        for stub in ("natal_promise", "transit_trigger"):
            if stub in contribs:
                self.assertTrue(contribs[stub]["is_stub"],
                    f"{stub} must be marked as is_stub=True")

    def test_contribution_pct_approximately_correct(self):
        """
        With all factors at 50.0 and master_score=50:
        natal_promise contribution = 50 × 0.40 = 20 → 40% of master score.
        """
        output = _build_pipeline_output(master_score=50)
        report = self.engine.generate_report(output)
        natal_entry = report["sensitivity"]["factor_contributions"].get("natal_promise", {})
        self.assertAlmostEqual(natal_entry["contribution"], 20.0, delta=1.0)


class TestCalibrationChecks(unittest.TestCase):
    """Tests for the calibration report section."""

    def setUp(self):
        self.engine = QualityMetricsEngine()

    def test_all_calibration_checks_pass_on_clean_input(self):
        """A clean, well-formed pipeline output must pass all calibration checks."""
        output = _build_pipeline_output(master_score=50, master_grade="GOOD")
        report = self.engine.generate_report(output)
        cal = report["calibration"]
        self.assertTrue(cal["all_pass"],
            f"All calibration checks should pass. Failed: "
            f"{[k for k,v in cal['checks'].items() if not v.get('pass')]}")

    def test_out_of_range_planet_score_fails_check(self):
        """Planet score > 100 must fail planet_scores_in_range check."""
        output = _build_pipeline_output(planet_scores={"sun": 150})
        report = self.engine.generate_report(output)
        check  = report["calibration"]["checks"]["planet_scores_in_range"]
        self.assertFalse(check["pass"],
            "Score 150 must fail planet_scores_in_range check")

    def test_wrong_grade_fails_consistency_check(self):
        """Score 75 with grade 'TOO WEAK' must fail grade_consistent_with_score."""
        output = _build_pipeline_output(master_score=75, master_grade="TOO WEAK")
        report = self.engine.generate_report(output)
        check  = report["calibration"]["checks"]["grade_consistent_with_score"]
        self.assertFalse(check["pass"],
            "Score=75, grade=TOO WEAK must fail grade consistency check")

    def test_valid_grade_passes_consistency_check(self):
        """Score 75 with grade 'VERY GOOD' must pass grade consistency."""
        output = _build_pipeline_output(master_score=75, master_grade="VERY GOOD")
        report = self.engine.generate_report(output)
        check  = report["calibration"]["checks"]["grade_consistent_with_score"]
        self.assertTrue(check["pass"],
            "Score=75, grade=VERY GOOD must pass grade consistency check")

    def test_weights_not_summing_to_one_fails(self):
        """Weights summing to 0.9 (not 1.0) must fail weights_sum_to_one."""
        bad_weights = {
            "natal_promise": 0.35, "planet_strength": 0.10,
            "house_strength": 0.10, "rasi_strength": 0.10,
            "varga_validation": 0.10, "dasha_activation": 0.10,
            "transit_trigger": 0.05,
        }  # sum = 0.90
        breakdown = {k: 50.0 for k in bad_weights}
        output = _build_pipeline_output(weights=bad_weights, breakdown=breakdown,
                                        master_score=50, master_grade="GOOD")
        report = self.engine.generate_report(output)
        check  = report["calibration"]["checks"]["weights_sum_to_one"]
        self.assertFalse(check["pass"],
            "Weights summing to 0.90 must fail weights_sum_to_one check")


class TestPredictionQuality(unittest.TestCase):
    """Tests for the prediction quality scores section."""

    def setUp(self):
        self.engine = QualityMetricsEngine()

    def test_identical_scores_have_zero_discrimination(self):
        """If all scores are identical (no variation), discrimination = 0."""
        scores = [50.0] * 10
        disc = self.engine._discrimination_score(scores)
        self.assertAlmostEqual(disc, 0.0, places=2)

    def test_polar_scores_have_high_discrimination(self):
        """Alternating 0 and 100 → maximum discrimination."""
        scores = [0.0, 100.0] * 5
        disc = self.engine._discrimination_score(scores)
        self.assertGreater(disc, 0.8)

    def test_zero_range_has_zero_resolution(self):
        """All same score → 0 range → resolution = 0."""
        scores = [50.0] * 5
        res = self.engine._resolution_score(scores)
        self.assertAlmostEqual(res, 0.0, places=2)

    def test_full_range_has_perfect_resolution(self):
        """[0, 100] range → resolution = 1.0."""
        scores = [0.0, 100.0]
        res = self.engine._resolution_score(scores)
        self.assertAlmostEqual(res, 1.0, places=2)

    def test_clean_master_has_high_coherence(self):
        """Clean master result must have coherence score = 1.0."""
        master = {
            "final_score": 50,
            "grade":       "GOOD",
            "breakdown":   {k: 50.0 for k in [
                "natal_promise", "planet_strength", "house_strength",
                "rasi_strength", "varga_validation", "dasha_activation",
                "transit_trigger"]},
            "weights":     {
                "natal_promise": 0.40, "planet_strength": 0.15,
                "house_strength": 0.10, "rasi_strength": 0.10,
                "varga_validation": 0.10, "dasha_activation": 0.10,
                "transit_trigger": 0.05,
            },
            "stub_factors":["natal_promise", "transit_trigger"],
            "live_factors":["planet_strength", "house_strength", "rasi_strength",
                            "varga_validation", "dasha_activation"],
        }
        coherence = self.engine._coherence_score(master)
        self.assertAlmostEqual(coherence, 1.0, places=2)

    def test_quality_scores_all_in_0_1_range(self):
        """All quality dimension scores must be in [0.0, 1.0]."""
        output = _build_pipeline_output(
            natal_scores={"marriage": 20, "career": 70, "wealth": 50},
            planet_scores={"sun": 80, "moon": 30, "saturn": 50},
            house_scores={"1": 60, "7": 20, "9": 70},
        )
        report = self.engine.generate_report(output)
        q = report["quality_scores"]
        for dim in ("discrimination", "resolution", "coherence", "overall"):
            val = q[dim]
            self.assertGreaterEqual(val, 0.0, f"{dim} must be ≥ 0")
            self.assertLessEqual(val, 1.0, f"{dim} must be ≤ 1")


class TestQualityMetricsIntegration(unittest.TestCase):
    """
    Integration tests using the full PipelineRunner on Raju's chart.
    """

    @classmethod
    def setUpClass(cls):
        from app.pipeline_runner import PipelineRunner
        from tests.test_real_charts import RAJU_CANONICAL_RAW
        runner = PipelineRunner()
        pipeline_out = runner.process(RAJU_CANONICAL_RAW)
        engine = QualityMetricsEngine()
        cls.report = engine.generate_report(pipeline_out)

    def test_raju_all_calibration_checks_pass(self):
        """Raju's chart must pass all 8 calibration checks."""
        cal = self.report["calibration"]
        self.assertTrue(cal["all_pass"],
            f"Calibration failures: "
            f"{[k for k, v in cal['checks'].items() if not v.get('pass')]}")

    def test_raju_discrimination_above_zero(self):
        """Raju has varied planet placements → discrimination should be > 0."""
        self.assertGreater(
            self.report["quality_scores"]["discrimination"], 0.0,
            "Raju chart must have non-zero discrimination score"
        )

    def test_raju_summary_calibration_pass(self):
        """Raju summary must show calibration PASS."""
        self.assertEqual(self.report["summary"]["calibration_status"], "PASS",
            "Raju chart calibration_status must be PASS")

    def test_raju_report_master_score_in_range(self):
        """Master score in report must match range [0, 100]."""
        ms = self.report["master_score"]
        self.assertGreaterEqual(ms, 0)
        self.assertLessEqual(ms, 100)

    def test_raju_dominant_factor_is_natal_promise(self):
        """
        With natal_promise at 40% weight, it should dominate contributions.
        """
        dom = self.report["sensitivity"]["dominant_factor"]
        self.assertEqual(dom, "natal_promise",
            f"Natal promise (40% weight) should be dominant factor, got {dom}")


if __name__ == "__main__":
    unittest.main()

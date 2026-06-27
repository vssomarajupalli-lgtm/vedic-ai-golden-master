"""
Quality Metrics Engine
======================
Deterministic prediction quality measurement framework for the Vedic AI system.

Provides four measurement categories:

1. Score Distribution Analysis
   - Histogram of scores across domains/charts
   - Mean, median, std-dev of score distributions
   - Detection of score clustering (are scores too narrow / too wide?)

2. Sensitivity Analysis
   - How much does each factor contribute to variance?
   - Per-factor contribution ratios
   - Factor correlation analysis

3. Calibration Report
   - Consistency checks (weights sum to 1, scores in range, etc.)
   - Placeholder for future: compare predicted probabilities vs known outcomes

4. Prediction Quality Scores
   - Discrimination score: does the system differentiate strong vs weak charts?
   - Resolution score: can the system produce the full 0–100 range?
   - Coherence score: are domain scores internally consistent?

Architecture Rules:
    - Zero AI/ML. Pure arithmetic analysis.
    - Stateless — no runtime state retained between calls.
    - All inputs are pre-computed engine outputs. Zero re-calculation.
"""

from typing import Dict, Any, List, Optional
import math


class QualityMetricsEngine:
    """
    Deterministic quality measurement engine for Vedic AI prediction outputs.

    Usage:
        engine = QualityMetricsEngine()
        report = engine.generate_report(pipeline_output)

    Returns a structured quality report with distribution analysis,
    sensitivity breakdown, and calibration validation results.
    """

    # Healthy score distribution constants
    _IDEAL_MEAN_MIN  = 35.0  # mean should be above 35 (not perpetually weak)
    _IDEAL_MEAN_MAX  = 70.0  # mean should be below 70 (not perpetually strong)
    _IDEAL_STD_MIN   = 10.0  # standard deviation should be > 10 (spread-out scores)
    _IDEAL_STD_MAX   = 35.0  # standard deviation should be < 35 (not too polarised)

    def __init__(self):
        pass

    # -------------------------------------------------------------------------
    # Public Interface
    # -------------------------------------------------------------------------

    def generate_report(self, pipeline_output: dict) -> dict:
        """
        Generates a comprehensive quality metrics report from pipeline output.

        Args:
            pipeline_output (dict): Full PipelineRunner.process() output.

        Returns:
            dict: Structured quality report with all four measurement categories.
        """
        engine_outputs = pipeline_output.get("engine_outputs", {})
        natal_results  = engine_outputs.get("natal_promise", {})
        planet_results = engine_outputs.get("planets", {})
        house_results  = engine_outputs.get("houses", {})
        master_result  = pipeline_output.get("master_probability", {})

        # Extract all scores
        natal_scores  = self._extract_natal_scores(natal_results)
        planet_scores = self._extract_planet_scores(planet_results)
        house_scores  = self._extract_house_scores(house_results)

        # Compute all four report sections
        distribution = self._score_distribution(natal_scores, planet_scores, house_scores)
        sensitivity  = self._sensitivity_analysis(engine_outputs, master_result)
        calibration  = self._calibration_check(engine_outputs, master_result)
        quality      = self._prediction_quality(
            natal_scores, planet_scores, house_scores, master_result
        )

        return {
            "master_score":   master_result.get("final_score", 0),
            "master_grade":   master_result.get("grade", "UNKNOWN"),
            "distribution":   distribution,
            "sensitivity":    sensitivity,
            "calibration":    calibration,
            "quality_scores": quality,
            "summary":        self._summary(distribution, calibration, quality)
        }

    # -------------------------------------------------------------------------
    # 1. Score Distribution Analysis
    # -------------------------------------------------------------------------

    def _score_distribution(
        self,
        natal_scores:  List[float],
        planet_scores: List[float],
        house_scores:  List[float],
    ) -> dict:
        """Computes distribution statistics for each score type."""
        return {
            "natal_domains":  self._stats(natal_scores,  "natal_promise"),
            "planets":        self._stats(planet_scores, "planet_strength"),
            "houses":         self._stats(house_scores,  "house_strength"),
            "combined":       self._stats(
                natal_scores + planet_scores + house_scores, "all_factors"
            ),
        }

    def _stats(self, scores: List[float], label: str) -> dict:
        """Computes basic statistics for a list of scores."""
        if not scores:
            return {"label": label, "count": 0, "mean": 0.0, "std": 0.0,
                    "min": 0.0, "max": 0.0, "median": 0.0, "histogram": {}}

        n      = len(scores)
        mean   = sum(scores) / n
        std    = math.sqrt(sum((s - mean) ** 2 for s in scores) / n)
        sorted_s = sorted(scores)
        median = sorted_s[n // 2] if n % 2 == 1 else (sorted_s[n//2-1] + sorted_s[n//2]) / 2
        hist   = self._histogram(scores, bins=5)

        return {
            "label":    label,
            "count":    n,
            "mean":     round(mean,   2),
            "std":      round(std,    2),
            "min":      round(sorted_s[0],  2),
            "max":      round(sorted_s[-1], 2),
            "median":   round(median, 2),
            "histogram": hist,
        }

    def _histogram(self, scores: List[float], bins: int = 5) -> dict:
        """
        Divides [0, 100] into equal-width bins and counts scores in each.
        Returns: {"0-20": 3, "20-40": 5, ...}
        """
        width  = 100 // bins
        counts = {f"{i*width}-{(i+1)*width}": 0 for i in range(bins)}
        for s in scores:
            idx = min(int(s // width), bins - 1)
            key = f"{idx*width}-{(idx+1)*width}"
            counts[key] += 1
        return counts

    # -------------------------------------------------------------------------
    # 2. Sensitivity Analysis
    # -------------------------------------------------------------------------

    def _sensitivity_analysis(self, engine_outputs: dict, master_result: dict) -> dict:
        """
        Computes how much each factor contributed to the master score.
        Contribution = factor_score × weight / master_score (% of total).
        """
        breakdown = master_result.get("breakdown", {})
        weights   = master_result.get("weights",   {})

        if not breakdown or not weights:
            return {"error": "No breakdown/weights data in master_result"}

        master_score = master_result.get("final_score", 0) or 1  # avoid div-by-zero

        contributions = {}
        for factor, score in breakdown.items():
            w    = weights.get(factor, 0.0)
            contrib = round(score * w, 2)
            pct     = round((contrib / (master_score if master_score else 1)) * 100, 1)
            contributions[factor] = {
                "factor_score":   round(score, 2),
                "weight":         w,
                "contribution":   contrib,
                "contribution_pct": pct,
                "is_stub":        factor in master_result.get("stub_factors", [])
            }

        # Sort by contribution descending
        sorted_contribs = dict(
            sorted(contributions.items(),
                   key=lambda x: abs(x[1]["contribution"]), reverse=True)
        )

        return {
            "factor_contributions": sorted_contribs,
            "dominant_factor":      next(iter(sorted_contribs)),
            "stub_contribution_pct": round(
                sum(v["contribution_pct"] for v in sorted_contribs.values()
                    if v["is_stub"]), 1
            ),
        }

    # -------------------------------------------------------------------------
    # 3. Calibration Report
    # -------------------------------------------------------------------------

    def _calibration_check(self, engine_outputs: dict, master_result: dict) -> dict:
        """
        Validates mathematical invariants and consistency of the pipeline output.
        Returns a dict of checks with pass/fail status.
        """
        checks = {}

        # Check 1: Weights sum to 1.0
        weights = master_result.get("weights", {})
        w_sum   = sum(weights.values()) if weights else 0.0
        checks["weights_sum_to_one"] = {
            "pass":     abs(w_sum - 1.0) < 1e-6,
            "expected": 1.0,
            "actual":   round(w_sum, 6),
        }

        # Check 2: Master score in [0, 100]
        ms = master_result.get("final_score", -1)
        checks["master_score_in_range"] = {
            "pass":     0 <= ms <= 100,
            "expected": "[0, 100]",
            "actual":   ms,
        }

        # Check 3: All planet scores in [0, 100]
        planet_results = engine_outputs.get("planets", {})
        planet_oob = [
            p for p, d in planet_results.items()
            if not (0 <= d.get("final_score", 50) <= 100)
        ]
        checks["planet_scores_in_range"] = {
            "pass":          len(planet_oob) == 0,
            "out_of_bounds": planet_oob,
        }

        # Check 4: All house scores in [0, 100]
        house_results = engine_outputs.get("houses", {})
        house_oob = [
            h for h, d in house_results.items()
            if not (0 <= d.get("final_score", 50) <= 100)
        ]
        checks["house_scores_in_range"] = {
            "pass":          len(house_oob) == 0,
            "out_of_bounds": house_oob,
        }

        # Check 5: All 8 natal domains present
        natal = engine_outputs.get("natal_promise", {})
        expected_domains = {
            "marriage", "career", "wealth", "education",
            "children", "property", "health", "spirituality"
        }
        missing_domains = expected_domains - set(natal.keys())
        checks["all_natal_domains_present"] = {
            "pass":    len(missing_domains) == 0,
            "missing": list(missing_domains),
        }

        # Check 6: Natal promise scores in [0, 100]
        natal_oob = [
            d for d, data in natal.items()
            if not (0 <= data.get("score", 50) <= 100)
        ]
        checks["natal_scores_in_range"] = {
            "pass":          len(natal_oob) == 0,
            "out_of_bounds": natal_oob,
        }

        # Check 7: Master score consistent with grade
        grade       = master_result.get("grade", "")
        grade_check = self._validate_grade_consistency(ms, grade)
        checks["grade_consistent_with_score"] = grade_check

        # Check 8: Breakdown factors match live_factors + stub_factors
        all_factors    = set(master_result.get("breakdown", {}).keys())
        live_factors   = set(master_result.get("live_factors", []))
        stub_factors   = set(master_result.get("stub_factors", []))
        declared_all   = live_factors | stub_factors
        undeclared     = all_factors - declared_all
        checks["all_factors_declared"] = {
            "pass":       len(undeclared) == 0,
            "undeclared": list(undeclared),
        }

        all_pass = all(v.get("pass", False) for v in checks.values())
        return {
            "all_pass":     all_pass,
            "pass_count":   sum(1 for v in checks.values() if v.get("pass")),
            "total_checks": len(checks),
            "checks":       checks,
        }

    def _validate_grade_consistency(self, score: int, grade: str) -> dict:
        """Checks that the score falls in the correct grade band."""
        grade_bands = [
            (80, "EXCELLENT"),
            (65, "VERY GOOD"),
            (50, "GOOD"),
            (35, "WEAK"),
            (0,  "TOO WEAK"),
        ]
        expected_grade = "TOO WEAK"
        for threshold, label in grade_bands:
            if score >= threshold:
                expected_grade = label
                break
        return {
            "pass":           grade == expected_grade,
            "score":          score,
            "actual_grade":   grade,
            "expected_grade": expected_grade,
        }

    # -------------------------------------------------------------------------
    # 4. Prediction Quality Scores
    # -------------------------------------------------------------------------

    def _prediction_quality(
        self,
        natal_scores:  List[float],
        planet_scores: List[float],
        house_scores:  List[float],
        master_result: dict
    ) -> dict:
        """
        Computes three quality dimensions:
            - Discrimination: can the system distinguish strong from weak placements?
            - Resolution:     does the system use the full [0, 100] range?
            - Coherence:      are the scores internally consistent?
        Each score is 0.0 – 1.0, where 1.0 = perfect.
        """
        all_scores = natal_scores + planet_scores + house_scores
        if not all_scores:
            return {"discrimination": 0.0, "resolution": 0.0, "coherence": 0.0}

        discrimination = self._discrimination_score(all_scores)
        resolution     = self._resolution_score(all_scores)
        coherence      = self._coherence_score(master_result)

        overall = round((discrimination + resolution + coherence) / 3, 3)

        return {
            "discrimination":           round(discrimination, 3),
            "discrimination_label":     self._quality_label(discrimination),
            "resolution":               round(resolution, 3),
            "resolution_label":         self._quality_label(resolution),
            "coherence":                round(coherence, 3),
            "coherence_label":          self._quality_label(coherence),
            "overall":                  overall,
            "overall_label":            self._quality_label(overall),
        }

    def _discrimination_score(self, scores: List[float]) -> float:
        """
        Measures how well the system differentiates strong from weak placements.
        Based on the normalized standard deviation of the score distribution.
        std/50 is the discrimination score (50 = maximum possible std for [0,100]).
        """
        if len(scores) < 2:
            return 0.0
        mean = sum(scores) / len(scores)
        std  = math.sqrt(sum((s - mean) ** 2 for s in scores) / len(scores))
        # Normalize: 50 = max possible std → score 1.0
        return min(1.0, std / 50.0)

    def _resolution_score(self, scores: List[float]) -> float:
        """
        Measures how much of the [0, 100] range the system utilizes.
        range_used / 100 = resolution score.
        """
        if not scores:
            return 0.0
        used_range = max(scores) - min(scores)
        return min(1.0, used_range / 100.0)

    def _coherence_score(self, master_result: dict) -> float:
        """
        Measures internal consistency of the master probability output.
        Based on calibration: if all checks pass, coherence = 1.0.
        Per failed check: -0.125 (8 checks total).
        """
        breakdown = master_result.get("breakdown", {})
        weights   = master_result.get("weights", {})
        if not breakdown or not weights:
            return 0.0

        # Check 1: weights sum to 1
        w_sum   = sum(weights.values())
        ok_w    = abs(w_sum - 1.0) < 1e-6

        # Check 2: master score in range
        ms      = master_result.get("final_score", -1)
        ok_ms   = 0 <= ms <= 100

        # Check 3: all factor scores in [0, 100]
        ok_f    = all(0 <= v <= 100 for v in breakdown.values())

        # Check 4: no unexpected factors
        declared = set(master_result.get("live_factors", [])) | set(master_result.get("stub_factors", []))
        ok_d    = set(breakdown.keys()) <= declared

        score = sum([ok_w, ok_ms, ok_f, ok_d]) / 4.0
        return score

    @staticmethod
    def _quality_label(score: float) -> str:
        """Maps a 0–1 quality score to a human-readable label."""
        if score >= 0.80: return "EXCELLENT"
        if score >= 0.60: return "GOOD"
        if score >= 0.40: return "FAIR"
        if score >= 0.20: return "POOR"
        return "CRITICAL"

    # -------------------------------------------------------------------------
    # Summary Generation
    # -------------------------------------------------------------------------

    def _summary(self, distribution: dict, calibration: dict, quality: dict) -> dict:
        """
        Generates a human-readable summary of the quality report.
        """
        all_cal_pass   = calibration["all_pass"]
        overall_q      = quality.get("overall", 0.0)
        overall_label  = quality.get("overall_label", "UNKNOWN")
        dist_combined  = distribution.get("combined", {})
        mean_score     = dist_combined.get("mean", 0.0)
        std_score      = dist_combined.get("std", 0.0)

        issues = []
        if not all_cal_pass:
            failed = [
                name for name, check in calibration["checks"].items()
                if not check.get("pass")
            ]
            issues.append(f"Calibration failures: {', '.join(failed)}")

        if mean_score < self._IDEAL_MEAN_MIN:
            issues.append(f"Mean score {mean_score} is low — chart may be generally weak")
        elif mean_score > self._IDEAL_MEAN_MAX:
            issues.append(f"Mean score {mean_score} is high — verify scoring calibration")

        if std_score < self._IDEAL_STD_MIN:
            issues.append(f"Std dev {std_score} is low — scores may be too clustered")
        elif std_score > self._IDEAL_STD_MAX:
            issues.append(f"Std dev {std_score} is high — scores may be too polarized")

        return {
            "overall_quality":    overall_label,
            "calibration_status": "PASS" if all_cal_pass else "FAIL",
            "mean_score":         mean_score,
            "score_spread":       std_score,
            "issues":             issues,
            "issue_count":        len(issues),
        }

    # -------------------------------------------------------------------------
    # Score Extraction Helpers
    # -------------------------------------------------------------------------

    @staticmethod
    def _extract_natal_scores(natal_results: dict) -> List[float]:
        """Extracts domain scores from natal_promise results."""
        return [
            float(data["score"])
            for data in natal_results.values()
            if isinstance(data, dict) and "score" in data
        ]

    @staticmethod
    def _extract_planet_scores(planet_results: dict) -> List[float]:
        """Extracts final_score from planet results."""
        return [
            float(data["final_score"])
            for data in planet_results.values()
            if isinstance(data, dict) and "final_score" in data
        ]

    @staticmethod
    def _extract_house_scores(house_results: dict) -> List[float]:
        """Extracts final_score from house results."""
        return [
            float(data["final_score"])
            for data in house_results.values()
            if isinstance(data, dict) and "final_score" in data
        ]

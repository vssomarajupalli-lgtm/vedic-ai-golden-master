import unittest
from app.engines.question_engine import QuestionEngine, DOMAIN_KEYWORDS, DOMAIN_PRIORITY
from app.pipeline_runner import PipelineRunner


class TestQuestionEngineRouting(unittest.TestCase):
    """Tests for deterministic keyword-based domain routing."""

    def setUp(self):
        self.engine = QuestionEngine()

    def _route(self, q):
        return self.engine.route_domain(q)

    # -----------------------------------------------------------------------
    # Marriage routing
    # -----------------------------------------------------------------------
    def test_route_marriage_exact(self):
        self.assertEqual(self._route("Will I get married?"), "marriage")

    def test_route_marriage_spouse(self):
        self.assertEqual(self._route("When will I find my spouse?"), "marriage")

    def test_route_marriage_husband(self):
        self.assertEqual(self._route("Will my husband return?"), "marriage")

    def test_route_marriage_wife(self):
        self.assertEqual(self._route("When will I find a wife?"), "marriage")

    def test_route_marriage_divorce(self):
        self.assertEqual(self._route("Is divorce indicated?"), "marriage")

    def test_route_marriage_relationship(self):
        self.assertEqual(self._route("Any relationship in my chart?"), "marriage")

    # -----------------------------------------------------------------------
    # Career routing
    # -----------------------------------------------------------------------
    def test_route_career_exact(self):
        self.assertEqual(self._route("Will my career improve?"), "career")

    def test_route_career_job(self):
        self.assertEqual(self._route("When will I get a job?"), "career")

    def test_route_career_promotion(self):
        self.assertEqual(self._route("Will I get a promotion?"), "career")

    def test_route_career_business(self):
        self.assertEqual(self._route("Should I start a business?"), "career")

    def test_route_career_abroad(self):
        self.assertEqual(self._route("Will I go abroad for work?"), "career")

    # -----------------------------------------------------------------------
    # Wealth routing
    # -----------------------------------------------------------------------
    def test_route_wealth_exact(self):
        self.assertEqual(self._route("Will I become wealthy?"), "wealth")

    def test_route_wealth_money(self):
        self.assertEqual(self._route("When will I have money?"), "wealth")

    def test_route_wealth_financial(self):
        self.assertEqual(self._route("Is my financial situation improving?"), "wealth")

    def test_route_wealth_debt(self):
        self.assertEqual(self._route("Will I clear my debt?"), "wealth")

    # -----------------------------------------------------------------------
    # Education routing
    # -----------------------------------------------------------------------
    def test_route_education_exact(self):
        self.assertEqual(self._route("Will I complete my education?"), "education")

    def test_route_education_study(self):
        self.assertEqual(self._route("Should I study abroad?"), "education")

    def test_route_education_exam(self):
        self.assertEqual(self._route("Will I pass the exam?"), "education")

    def test_route_education_degree(self):
        self.assertEqual(self._route("When will I get my degree?"), "education")

    # -----------------------------------------------------------------------
    # Children routing
    # -----------------------------------------------------------------------
    def test_route_children_exact(self):
        self.assertEqual(self._route("Will I have children?"), "children")

    def test_route_children_baby(self):
        self.assertEqual(self._route("When will we have a baby?"), "children")

    def test_route_children_pregnancy(self):
        self.assertEqual(self._route("Is pregnancy indicated?"), "children")

    def test_route_children_son(self):
        self.assertEqual(self._route("Will I have a son?"), "children")

    # -----------------------------------------------------------------------
    # Property routing
    # -----------------------------------------------------------------------
    def test_route_property_exact(self):
        self.assertEqual(self._route("Will I own property?"), "property")

    def test_route_property_house(self):
        self.assertEqual(self._route("When will I buy a house?"), "property")

    def test_route_property_land(self):
        self.assertEqual(self._route("Is land purchase indicated?"), "property")

    # -----------------------------------------------------------------------
    # Health routing
    # -----------------------------------------------------------------------
    def test_route_health_exact(self):
        self.assertEqual(self._route("How is my health?"), "health")

    def test_route_health_illness(self):
        self.assertEqual(self._route("Will my illness resolve?"), "health")

    def test_route_health_surgery(self):
        self.assertEqual(self._route("Is surgery indicated in my chart?"), "health")

    def test_route_health_longevity(self):
        self.assertEqual(self._route("What is my longevity?"), "health")

    # -----------------------------------------------------------------------
    # Spirituality routing
    # -----------------------------------------------------------------------
    def test_route_spirituality_exact(self):
        self.assertEqual(self._route("Am I spiritually inclined?"), "spirituality")

    def test_route_spirituality_meditation(self):
        self.assertEqual(self._route("Will I take up meditation?"), "spirituality")

    def test_route_spirituality_pilgrimage(self):
        self.assertEqual(self._route("Will I go on a pilgrimage?"), "spirituality")

    # -----------------------------------------------------------------------
    # Edge cases
    # -----------------------------------------------------------------------
    def test_route_unrecognised_returns_none(self):
        """Question with no matching keyword → None."""
        self.assertIsNone(self._route("What is my lucky number?"))

    def test_route_empty_string_returns_none(self):
        self.assertIsNone(self._route(""))

    def test_route_case_insensitive(self):
        """Routing must be case-insensitive."""
        self.assertEqual(self._route("WILL I GET MARRIED?"),   "marriage")
        self.assertEqual(self._route("Will I GET A JOB?"),     "career")
        self.assertEqual(self._route("HEALTH QUESTION"),       "health")

    def test_route_priority_marriage_over_children(self):
        """'marriage' keyword appears before 'children' in DOMAIN_PRIORITY → marriage wins."""
        result = self._route("Will my marriage produce children?")
        # 'marriage' is earlier in DOMAIN_PRIORITY than 'children'
        self.assertEqual(result, "marriage")

    def test_all_priority_domains_have_keywords(self):
        """Every domain in DOMAIN_PRIORITY must have at least one keyword."""
        for domain in DOMAIN_PRIORITY:
            self.assertIn(domain, DOMAIN_KEYWORDS)
            self.assertGreater(len(DOMAIN_KEYWORDS[domain]), 0,
                               f"{domain} has no keywords")


class TestQuestionEngineAnswer(unittest.TestCase):
    """Tests for full answer_question() output schema and scoring via PipelineRunner."""

    def setUp(self):
        self.runner = PipelineRunner()

    # -----------------------------------------------------------------------
    # Fixture: minimal pipeline output
    # -----------------------------------------------------------------------

    def _pipeline_output(
        self,
        natal_scores=None,
        planet_scores=None,
        house_scores=None,
        dasha_data=None,
    ):
        """Build a minimal pipeline output dict for testing."""
        natal_scores   = natal_scores   or {}
        planet_scores  = planet_scores  or {}
        house_scores   = house_scores   or {}
        dasha_data     = dasha_data     or {}

        return {
            "engine_outputs": {
                "natal_promise": {
                    domain: {"score": score, "promise": "MODERATE",
                             "karaka": "venus", "afflictions": []}
                    for domain, score in natal_scores.items()
                },
                "planets":  {p: {"final_score": s} for p, s in planet_scores.items()},
                "houses":   {h: {"final_score": s} for h, s in house_scores.items()},
                "rasis":    {},
                "vargas":   {},
                "dashas":   dasha_data,
                "transit":  {"activation_score": 50},
                "ashtakavarga": {
                    "dasha_bav_support": {
                        "timing_confidence": "moderate",
                        "timing_confidence_multiplier": 1.05
                    },
                    "sav_chart": {}
                }
            }
        }

    # -----------------------------------------------------------------------
    # Output schema
    # -----------------------------------------------------------------------

    def test_answer_has_required_keys(self):
        """answer() must return all required top-level keys."""
        output = self._pipeline_output(natal_scores={"marriage": 60})
        result = self.runner.answer_question("Will I get married?", output)
        for key in ("question", "domain", "routed", "probability",
                    "natal_promise", "timing", "transit", "factor_breakdown", "answer_text"):
            self.assertIn(key, result, f"Missing key: {key}")

    def test_probability_has_score_grade_raw(self):
        output = self._pipeline_output(natal_scores={"marriage": 60})
        result = self.runner.answer_question("Will I get married?", output)
        for key in ("score", "grade", "raw"):
            self.assertIn(key, result["probability"])

    def test_natal_promise_has_required_fields(self):
        output = self._pipeline_output(natal_scores={"career": 55})
        result = self.runner.answer_question("Will my career improve?", output)
        for key in ("score", "promise", "karaka", "afflictions"):
            self.assertIn(key, result["natal_promise"])

    def test_timing_has_required_fields(self):
        output = self._pipeline_output(natal_scores={"wealth": 45})
        result = self.runner.answer_question("Will I have money?", output)
        for key in ("mahadasha", "antardasha", "bav_timing_confidence",
                    "activation_level"):
            self.assertIn(key, result["timing"])

    # -----------------------------------------------------------------------
    # Domain routing reflected in answer
    # -----------------------------------------------------------------------

    def test_routed_true_for_known_domain(self):
        output = self._pipeline_output(natal_scores={"marriage": 50})
        result = self.runner.answer_question("Will I get married?", output)
        self.assertTrue(result["routed"])
        self.assertEqual(result["domain"], "marriage")

    def test_routed_false_for_unknown_question(self):
        output = self._pipeline_output(natal_scores={"marriage": 50})
        result = self.runner.answer_question("What is my lucky number?", output)
        self.assertFalse(result["routed"])
        self.assertIsNone(result["domain"])

    def test_domain_natal_score_used_not_average(self):
        """
        Marriage natal=80, career natal=20.
        Marriage question should use 80, not the average (50).
        """
        output = self._pipeline_output(
            natal_scores={"marriage": 80, "career": 20, "wealth": 50,
                          "health": 50, "education": 50, "children": 50,
                          "property": 50, "spirituality": 50}
        )
        marriage_result = self.runner.answer_question("Will I get married?", output)
        career_result   = self.runner.answer_question("When will I get a job?",  output)

        self.assertGreater(
            marriage_result["probability"]["score"],
            career_result["probability"]["score"],
            "Marriage (natal=80) should have higher probability than career (natal=20)"
        )

    def test_natal_score_reflected_in_natal_promise(self):
        """Domain-specific natal score must appear in natal_promise.score."""
        output = self._pipeline_output(natal_scores={"children": 35})
        result = self.runner.answer_question("Will I have children?", output)
        self.assertEqual(result["natal_promise"]["score"], 35)

    # -----------------------------------------------------------------------
    # Promise grade mapping
    # -----------------------------------------------------------------------

    def test_promise_strong_for_high_natal(self):
        output = self._pipeline_output(natal_scores={"health": 75})
        result = self.runner.answer_question("How is my health?", output)
        self.assertEqual(result["natal_promise"]["promise"], "STRONG")

    def test_promise_present_for_low_natal(self):
        output = self._pipeline_output(natal_scores={"marriage": 20})
        result = self.runner.answer_question("Will I get married?", output)
        self.assertEqual(result["natal_promise"]["promise"], "PRESENT")

    def test_promise_moderate_for_mid_natal(self):
        output = self._pipeline_output(natal_scores={"career": 55})
        result = self.runner.answer_question("Will my career improve?", output)
        self.assertEqual(result["natal_promise"]["promise"], "MODERATE")

    # -----------------------------------------------------------------------
    # Probability score bounds
    # -----------------------------------------------------------------------

    def test_probability_score_within_0_100(self):
        output = self._pipeline_output(natal_scores={"marriage": 90})
        result = self.runner.answer_question("Will I get married?", output)
        self.assertGreaterEqual(result["probability"]["score"], 0)
        self.assertLessEqual(result["probability"]["score"],    100)

    def test_probability_not_zero_with_moderate_inputs(self):
        output = self._pipeline_output(natal_scores={"education": 55})
        result = self.runner.answer_question("Will I pass the exam?", output)
        self.assertGreater(result["probability"]["score"], 0)

    # -----------------------------------------------------------------------
    # Timing evidence
    # -----------------------------------------------------------------------

    def test_timing_activation_high_for_large_multiplier(self):
        """Multiplier ≥ 1.20 → activation_level = HIGH."""
        dasha = {
            "synthesis": {
                "active_md": "saturn",
                "dasha_strength": 62.5
            }
        }
        output = self._pipeline_output(natal_scores={"wealth": 50}, dasha_data=dasha)
        result = self.runner.answer_question("Will I have money?", output)
        self.assertEqual(result["timing"]["activation_level"], "HIGH")

    def test_timing_activation_neutral_for_1_0_multiplier(self):
        """Multiplier = 1.0 → activation_level = NEUTRAL."""
        dasha = {
            "synthesis": {
                "active_md": "saturn",
                "dasha_strength": 50.0
            }
        }
        output = self._pipeline_output(natal_scores={"career": 50}, dasha_data=dasha)
        result = self.runner.answer_question("Will my career improve?", output)
        self.assertEqual(result["timing"]["activation_level"], "NEUTRAL")

    def test_timing_mahadasha_lord_extracted(self):
        dasha = {
            "synthesis": {
                "active_md": "jupiter"
            }
        }
        output = self._pipeline_output(natal_scores={"wealth": 50}, dasha_data=dasha)
        result = self.runner.answer_question("Will I become wealthy?", output)
        self.assertEqual(result["timing"]["mahadasha"], "jupiter")

    # -----------------------------------------------------------------------
    # Answer text
    # -----------------------------------------------------------------------

    def test_answer_text_is_string(self):
        output = self._pipeline_output(natal_scores={"marriage": 50})
        result = self.runner.answer_question("Will I get married?", output)
        self.assertIsInstance(result["answer_text"], str)
        self.assertGreater(len(result["answer_text"]), 20)

    def test_answer_text_contains_domain(self):
        output = self._pipeline_output(natal_scores={"health": 40})
        result = self.runner.answer_question("How is my health?", output)
        self.assertIn("Health", result["answer_text"])

    def test_answer_text_unrouted_mentions_domain_unknown(self):
        output = self._pipeline_output(natal_scores={})
        result = self.runner.answer_question("What is my lucky number?", output)
        self.assertIn("could not be determined", result["answer_text"])

    # -----------------------------------------------------------------------
    # _activation_label unit test
    # -----------------------------------------------------------------------

    def test_activation_label_thresholds(self):
        self.assertEqual(QuestionEngine._activation_label(1.25), "HIGH")
        self.assertEqual(QuestionEngine._activation_label(1.15), "MODERATE")
        self.assertEqual(QuestionEngine._activation_label(1.05), "NEUTRAL")
        self.assertEqual(QuestionEngine._activation_label(0.90), "SUPPRESSED")


class TestQuestionEngineIntegration(unittest.TestCase):
    """
    Integration-style tests using PipelineRunner.
    """

    def setUp(self):
        self.runner = PipelineRunner()

    def _minimal_pipeline_output(self, natal_marriage=50):
        """Produce a pipeline-shaped output dict."""
        return {
            "engine_outputs": {
                "natal_promise": {
                    "marriage": {
                        "score": natal_marriage,
                        "promise": "MODERATE",
                        "karaka": "venus",
                        "afflictions": ["saturn_in_7"]
                    }
                },
                "planets": {"venus": {"final_score": 40}, "saturn": {"final_score": 50}},
                "houses":  {"7": {"final_score": 20}},
                "rasis":   {},
                "vargas":  {},
                "transit": {"activation_score": 50},
                "dashas":  {
                    "synthesis": {
                        "active_md": "saturn",
                        "active_ad": "jupiter",
                        "active_pd": "mars",
                        "dasha_strength": 60.5
                    }
                },
                "ashtakavarga": {
                    "dasha_bav_support": {
                        "timing_confidence": "moderate",
                        "timing_confidence_multiplier": 1.05
                    },
                    "sav_chart": {}
                }
            }
        }

    def test_marriage_question_with_saturn_in_7_affliction(self):
        """
        Marriage question with Saturn in H7 affliction in natal data.
        The affliction should appear in the answer's natal_promise.
        """
        output = self._minimal_pipeline_output(natal_marriage=20)
        result = self.runner.answer_question("Will I get married?", output)
        self.assertEqual(result["domain"], "marriage")
        self.assertIn("saturn_in_7", result["natal_promise"]["afflictions"])
        # Low natal promise → PRESENT
        self.assertEqual(result["natal_promise"]["promise"], "PRESENT")

    def test_answer_text_includes_dasha_lords(self):
        """Answer text must mention the Mahadasha lord."""
        output = self._minimal_pipeline_output()
        result = self.runner.answer_question("Will I get married?", output)
        self.assertIn("Saturn", result["answer_text"])

    def test_probability_improves_with_better_natal(self):
        """High natal marriage promise → higher probability than low natal."""
        low  = self._minimal_pipeline_output(natal_marriage=15)
        high = self._minimal_pipeline_output(natal_marriage=80)
        low_result  = self.runner.answer_question("Will I get married?", low)
        high_result = self.runner.answer_question("Will I get married?", high)
        self.assertGreater(
            high_result["probability"]["score"],
            low_result["probability"]["score"]
        )

if __name__ == "__main__":
    unittest.main()

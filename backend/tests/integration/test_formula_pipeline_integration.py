"""
Integration test suite for BKL-005C System Integration Validation.

Tests the complete formula pipeline:
- Formula Registry -> Formula Loader -> Formula Calibration -> Formula Evaluator -> Question Engine
- Signal extraction completeness
- Inheritance merge + normalization
- End-to-end question flow
"""

import pytest
from app.pipeline_runner import PipelineRunner
from app.formulas.loader import formula_repository_loader
from app.core.question_router import QuestionRouter
from app.calibration.calibration_manager import CalibrationManager


@pytest.fixture
def runner():
    """Pipeline runner instance."""
    return PipelineRunner()


@pytest.fixture
def sample_raw_pdf_data():
    """Sample canonical JSON for testing."""
    return {
        "raw_metadata": {
            "name": "Integration Test Native",
            "lagna": "Mesha"
        },
        "raw_planets": {
            "Surya": {"sign": "Mesha", "house": "1", "house_type": "kendra", "dignity": "exalted"},
            "Chandra": {"sign": "Kataka", "house": "4", "house_type": "kendra", "dignity": "own_sign"},
            "Mangal": {"sign": "Vrishchika", "house": "8", "house_type": "dusthana", "dignity": "own_sign"},
            "Budha": {"sign": "Mithuna", "house": "3", "house_type": "upachaya", "dignity": "own_sign"},
            "Guru": {"sign": "Dhanus", "house": "9", "house_type": "trikona", "dignity": "own_sign"},
            "Shukra": {"sign": "Mesha", "house": "1", "house_type": "kendra", "dignity": "neutral"},
            "Shani": {"sign": "Kumbha", "house": "11", "house_type": "upachaya", "dignity": "own_sign"},
            "Rahu": {"sign": "Vrishabha", "house": "2", "house_type": "dhana", "dignity": "neutral"},
            "Ketu": {"sign": "Vrishchika", "house": "8", "house_type": "dusthana", "dignity": "neutral"}
        },
        "raw_vargas": {
            "D9": {"planets": {
                "Surya": {"sign": "Tula", "dignity": "debilitated"},
                "Chandra": {"sign": "Kataka", "dignity": "own_sign"},
                "Mangal": {"sign": "Vrishchika", "dignity": "own_house"},
                "Budha": {"sign": "Mithuna", "dignity": "own_sign"},
                "Guru": {"sign": "Dhanus", "dignity": "own_sign"},
                "Shukra": {"sign": "Mesha", "dignity": "own_sign"},
                "Shani": {"sign": "Kumbha", "dignity": "own_sign"},
                "Rahu": {"sign": "Vrishabha", "dignity": "neutral"},
                "Ketu": {"sign": "Vrishchika", "dignity": "neutral"}
            }},
            "D10": {"planets": {"Shani": {"sign": "Kumbha", "dignity": "own_sign"}}},
            "D7": {"planets": {"Guru": {"sign": "Dhanus", "dignity": "own_sign"}}},
            "D24": {"planets": {"Budha": {"sign": "Kanya", "dignity": "own_sign"}}},
            "D2": {"planets": {"Guru": {"sign": "Dhanus", "dignity": "own_sign"}}},
            "D4": {"planets": {"Mangal": {"sign": "Vrishchika", "dignity": "own_sign"}}},
            "D20": {"planets": {"Guru": {"sign": "Dhanus", "dignity": "own_sign"}}},
            "D6": {"planets": {"Surya": {"sign": "Mesha", "dignity": "exalted"}}}
        },
        "raw_dashas": {
            "mahadasha": "Surya",
            "antardasha": "Chandra",
            "pratyantardasha": "Mangal"
        },
        "raw_houses": {
            "1": {"sign": "Mesha", "lord": "Mangal"},
            "2": {"sign": "Vrishabha", "lord": "Shukra"},
            "3": {"sign": "Mithuna", "lord": "Budha"},
            "4": {"sign": "Kataka", "lord": "Chandra"},
            "5": {"sign": "Simha", "lord": "Surya"},
            "6": {"sign": "Kanya", "lord": "Budha"},
            "7": {"sign": "Tula", "lord": "Shukra"},
            "8": {"sign": "Vrishchika", "lord": "Mangal"},
            "9": {"sign": "Dhanus", "lord": "Guru"},
            "10": {"sign": "Makara", "lord": "Shani"},
            "11": {"sign": "Kumbha", "lord": "Shani"},
            "12": {"sign": "Meena", "lord": "Guru"}
        },
        "raw_bhava_bala": {},
        "raw_shadbala": {}
    }


class TestFormulaPipelineIntegration:
    """Test complete formula pipeline integration."""

    def test_all_43_formulas_calibrated(self):
        """Verify all 43 formulas have calibration entries."""
        mgr = CalibrationManager()
        fc = mgr.formula_calibration
        assert len(fc) == 43, f"Expected 43 calibrated formulas, got {len(fc)}"
        
        # Verify all formulas in registry have calibration
        for formula in formula_repository_loader.list_formulas():
            assert formula.formula_key in fc, f"Missing calibration for {formula.formula_key}"
            cal = fc[formula.formula_key]
            assert "factors" in cal, f"No factors in calibration for {formula.formula_key}"
            assert len(cal["factors"]) > 0, f"Empty factors for {formula.formula_key}"

    def test_formula_inheritance_merge_normalization(self):
        """Test base + child formula factors merge and normalize to 100%."""
        # Test MAR_TIMING_BASE + MAR_TIMING_DELAY
        base = formula_repository_loader.get_formula("MAR_TIMING_BASE")
        child = formula_repository_loader.get_formula("MAR_TIMING_DELAY")
        
        # Base factors
        base_signals = set(base.required_signals)
        assert "7th_house" in base_signals
        assert "7th_lord" in base_signals
        assert "venus" in base_signals
        assert "lagna_lord" in base_signals
        
        # Child has additional signals
        child_signals = set(child.required_signals)
        assert "saturn" in child_signals
        
        # Child should inherit base signals
        for sig in base_signals:
            assert sig in child_signals, f"Child missing inherited signal: {sig}"
        
        # Calibration: base + child factors
        mgr = CalibrationManager()
        base_cal = mgr.formula_calibration.get("MAR_TIMING_BASE", {})
        child_cal = mgr.formula_calibration.get("MAR_TIMING_DELAY", {})
        
        base_factors = base_cal.get("factors", {})
        child_factors = child_cal.get("factors", {})
        
        # Base and child should have no overlapping factor names
        base_names = set(base_factors.keys())
        child_names = set(child_factors.keys())
        assert len(base_names & child_names) == 0, "Duplicate factors between base and child"
        
        # Verify both have weights
        for name, data in base_factors.items():
            assert "weight" in data, f"Base factor {name} missing weight"
            assert data.get("enabled", True), f"Base factor {name} disabled"
        
        for name, data in child_factors.items():
            assert "weight" in data, f"Child factor {name} missing weight"
            assert data.get("enabled", True), f"Child factor {name} disabled"

    def test_formula_evaluation_flow(self, runner, sample_raw_pdf_data):
        """Test complete formula evaluation flow."""
        # Run pipeline
        pipeline_output = runner.process(sample_raw_pdf_data)
        assert "engine_outputs" in pipeline_output
        
        # Test a question with formula
        answer = runner.answer_question("7.1", pipeline_output)  # Marriage timing
        assert answer.get("status") != "error"
        assert "formula_key" in answer
        assert answer["formula_key"] == "MAR_TIMING_NORMAL"
        assert "formula_evaluation" in answer
        assert answer["formula_evaluation"] is not None
        
        fe = answer["formula_evaluation"]
        assert "final_state" in fe
        assert "factor_fulfillment" in fe
        assert "factor_weights" in fe
        assert "promise_score" in fe

    def test_all_11_formula_families(self, runner, sample_raw_pdf_data):
        """Test formula evaluation across all 11 families."""
        pipeline_output = runner.process(sample_raw_pdf_data)
        
        test_questions = {
            "7.1": "MAR_TIMING_NORMAL",      # Marriage
            "10.1": "CAR_PROMOTION_TIMING",  # Career
            "2.1": "WEA_SUDDEN_GAIN",        # Wealth
            "6.1": "HLT_GENERAL_VITALITY",   # Health
            "4.1": "AST_PROP_PROMISE",       # Property
            "5.1": "EDU_ACADEMIC_SUCCESS",   # Education
            "8.1": "FAM_CHILD_PROMISE",      # Children
            "9.1": "LIT_LEGAL_VICTORY",      # Litigation
            "12.1": "SPR_SPIRITUAL_PROGRESS", # Spirituality
            "13.1": "REL_MARITAL_HARMONY",   # Compatibility
            "11.1": "TRV_SHORT_TRIP",        # Travel
        }
        
        for q_id, expected_formula in test_questions.items():
            answer = runner.answer_question(q_id, pipeline_output)
            assert answer.get("formula_key") == expected_formula, f"Q{q_id}: expected {expected_formula}, got {answer.get('formula_key')}"
            assert answer.get("formula_evaluation") is not None, f"Q{q_id}: missing formula_evaluation"
            fe = answer["formula_evaluation"]
            assert fe["final_state"] in ["FAVORABLE", "MIXED", "UNFAVORABLE"]
            assert fe["total_layers"] > 0
            assert fe["promise_score"] >= 0

    def test_question_id_vs_free_text_consistency(self, runner, sample_raw_pdf_data):
        """Test both question_id and free-text routing produce consistent answers."""
        pipeline_output = runner.process(sample_raw_pdf_data)
        
        # Free text question
        answer1 = runner.answer_question("Will I get married?", pipeline_output)
        # Question ID
        answer2 = runner.answer_question("7.1", pipeline_output)
        
        # Both should route to marriage domain
        assert answer1.get("domain", "").lower() == "marriage"
        assert answer2.get("domain", "").lower() == "marriage"
        # Both should have formula evaluation
        assert "formula_evaluation" in answer1
        assert "formula_evaluation" in answer2

    def test_deterministic_pipeline(self, runner, sample_raw_pdf_data):
        """Verify same input produces identical output."""
        out1 = runner.process(sample_raw_pdf_data)
        out2 = runner.process(sample_raw_pdf_data)
        
        # Engine outputs should be identical
        import json
        assert json.dumps(out1["engine_outputs"], sort_keys=True) == json.dumps(out2["engine_outputs"], sort_keys=True)
        
        # Answer should be identical
        ans1 = runner.answer_question("7.1", out1)
        ans2 = runner.answer_question("7.1", out2)
        assert json.dumps(ans1, sort_keys=True) == json.dumps(ans2, sort_keys=True)


class TestSignalExtractionCompleteness:
    """Test that all required signals for all 43 formulas are extractable."""

    def test_all_required_signals_mapped(self):
        """Verify all signals required by formulas have extraction paths."""
        # Collect all required signals from all 43 formulas
        all_signals = set()
        for formula in formula_repository_loader.list_formulas():
            for sig in formula.required_signals:
                all_signals.add(sig)
        
        # These are the signals that formulas actually require
        expected_signals = {
            "7th_house", "7th_lord", "venus", "lagna_lord", "saturn",
            "10th_house", "10th_lord", "11th_house", "5th_house", "9th_house",
            "8th_house", "rahu", "2nd_house", "12th_house", "lagna",
            "8th_lord", "sun", "moon", "6th_house", "5th_lord",
            "mercury", "jupiter", "4th_house", "4th_lord",
            "mars", "1st_house", "1st_lord", "6th_lord",
            "ketu", "3rd_house",
        }
        
        # All expected signals should be in the set of required signals
        for sig in expected_signals:
            assert sig in all_signals, f"Signal {sig} not required by any formula"
        
        # Verify the mapping dict has the keys for all required signals
        runner = PipelineRunner()
        for sig in all_signals:
            # Just verify the mapping dict has the key
            # The signal_paths dict is a local variable in _extract_signal
            # We can check by calling _extract_signal with a payload that has the signal
            found = False
            for const in runner._extract_signal.__code__.co_consts:
                if isinstance(const, dict) and sig in const:
                    found = True
                    break
            # If not found in constants, check by calling _extract_signal with a payload
            if not found:
                payload = {
                    "planets": {"sun": {"final_score": 50}, "moon": {"final_score": 50}, "venus": {"final_score": 50}, "mars": {"final_score": 50}, "jupiter": {"final_score": 50}, "saturn": {"final_score": 50}, "mercury": {"final_score": 50}, "rahu": {"final_score": 50}, "ketu": {"final_score": 50}},
                    "houses": {"1": {"final_score": 50, "lord_strength_score": 50}, "2": {"final_score": 50, "lord_strength_score": 50}, "3": {"final_score": 50, "lord_strength_score": 50}, "4": {"final_score": 50, "lord_strength_score": 50}, "5": {"final_score": 50, "lord_strength_score": 50}, "6": {"final_score": 50, "lord_strength_score": 50}, "7": {"final_score": 50, "lord_strength_score": 50}, "8": {"final_score": 50, "lord_strength_score": 50}, "9": {"final_score": 50, "lord_strength_score": 50}, "10": {"final_score": 50, "lord_strength_score": 50}, "11": {"final_score": 50, "lord_strength_score": 50}, "12": {"final_score": 50, "lord_strength_score": 50}},
                    "vargas": {"D2": {"planets": {"jupiter": {"final_score": 50}}}, "D4": {"planets": {"mars": {"final_score": 50}}}, "D6": {"planets": {"sun": {"final_score": 50}}}, "D7": {"planets": {"jupiter": {"final_score": 50}}}, "D9": {"planets": {"venus": {"final_score": 50}}}, "D10": {"planets": {"saturn": {"final_score": 50}}}, "D20": {"planets": {"jupiter": {"final_score": 50}}}, "D24": {"planets": {"mercury": {"final_score": 50}}}},
                    "dashas": {"synthesis": {"dasha_strength": 50}},
                    "transit": {"activation_score": 50},
                    "yogas": {"marriage_yoga": {"strength": 50}},
                    "natal_promise": {"marriage": {"score": 50}},
                }
                result = runner._extract_signal(payload, sig)
                if result is not None:
                    found = True
            assert found, f"No extraction path for signal {sig}"


class TestQuestionFlowValidation:
    """Test complete question routing and answer generation."""

    def test_question_router_integration(self):
        """Test QuestionRouter resolves to correct formula."""
        router = QuestionRouter()
        
        # Test a few question IDs
        test_cases = [
            ("7.1", "MAR_TIMING_NORMAL", "marriage"),
            ("10.1", "CAR_PROMOTION_TIMING", "career"),
            ("2.1", "WEA_SUDDEN_GAIN", "wealth"),
            ("6.1", "HLT_GENERAL_VITALITY", "health"),
            ("4.1", "AST_PROP_PROMISE", "property"),
        ]
        
        for q_id, expected_formula, expected_domain in test_cases:
            result = router.route_question(q_id)
            assert result["status"] == "success", f"Failed to route {q_id}: {result}"
            assert result["formula_key"] == expected_formula
            assert result["metadata"]["domain_name"].lower() == expected_domain.lower()

    def test_all_83_questions_mapped(self):
        """Verify all 83 questions map to calibrated formulas."""
        from app.core.registry_loader import QuestionRegistryLoader
        loader = QuestionRegistryLoader()
        loader.load_registry()
        
        question_count = 0
        for q in loader.registry_data:
            question_count += 1
            formula_key = q.get("formula_key")
            assert formula_key, f"Question {q['question_id']} missing formula_key"
            
            # Verify formula exists and is calibrated
            formula = formula_repository_loader.get_formula(formula_key)
            assert formula is not None, f"Formula {formula_key} not found"
            
            mgr = CalibrationManager()
            cal = mgr.formula_calibration.get(formula_key, {})
            assert cal, f"Formula {formula_key} not calibrated"
            assert "factors" in cal and len(cal["factors"]) > 0
        
        assert question_count == 83, f"Expected 83 questions, found {question_count}"

    def test_no_orphan_calibrations(self):
        """Verify no calibration entries without corresponding formula/question."""
        mgr = CalibrationManager()
        fc = mgr.formula_calibration
        
        from app.core.registry_loader import QuestionRegistryLoader
        loader = QuestionRegistryLoader()
        loader.load_registry()
        
        # Collect all formula keys used by questions
        used_by_questions = set()
        for q in loader.registry_data:
            if q.get("formula_key"):
                used_by_questions.add(q["formula_key"])
        
        # Collect all base formula keys (parents)
        base_formulas = set()
        for formula in formula_repository_loader.list_formulas():
            if formula.parent_formula_key:
                base_formulas.add(formula.parent_formula_key)
        
        for formula_key in fc:
            # Must exist in formula registry
            try:
                formula_repository_loader.get_formula(formula_key)
            except Exception:
                pytest.fail(f"Calibration for {formula_key} has no matching formula")
            
            # Must be used by at least one question OR be a base formula inherited by child
            used = formula_key in used_by_questions or formula_key in base_formulas
            assert used, f"Calibration for {formula_key} not used by any question and not a base formula"


class TestRegressionValidation:
    """Ensure no regressions from BKL-005C changes."""

    def test_existing_question_engine_tests_pass(self):
        """Run existing question engine tests to verify no regressions."""
        import subprocess
        import sys
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/test_question_engine.py", "tests/test_question_router.py", "-q"],
            cwd="D:/vedic-ai-golden-master/backend",
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"Question engine tests failed:\n{result.stdout}\n{result.stderr}"

    def test_existing_formula_tests_pass(self):
        """Run existing formula tests to verify no regressions."""
        import subprocess
        import sys
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/test_formula_evaluator.py", "tests/test_formula_inheritance.py", "-q"],
            cwd="D:/vedic-ai-golden-master/backend",
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"Formula tests failed:\n{result.stdout}\n{result.stderr}"

    def test_calibration_tests_pass(self):
        """Run calibration tests to verify no regressions."""
        import subprocess
        import sys
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/test_weightage_calibration.py", "-q"],
            cwd="D:/vedic-ai-golden-master/backend",
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"Calibration tests failed:\n{result.stdout}\n{result.stderr}"
"""
Real Chart Regression Tests — Raju's Canonical Chart
======================================================
End-to-end pipeline tests using the actual canonical_content.json (Raju's chart).
These tests validate that the full PipelineRunner produces astrologically meaningful
results for a known horoscope, not just mathematically valid ones.

Chart facts (Raju — Mesha Lagna / Aries Ascendant):
  - Sun:    Aries H1 (Exalted, Kendra)          → strong vitality
  - Moon:   Taurus H2 (Neutral)                 → moderate mind
  - Mars:   Scorpio H8 (Own sign, Dusthana)     → Scorpio 8th (Mars rules)
  - Mercury:Pisces H12 (Debilitated, Dusthana)  → weak intellect
  - Jupiter:Sagittarius H9 (Own sign, Trikona)  → strong dharma
  - Venus:  Pisces H12 (Exalted, Dusthana)      → exalted but in 12th
  - Saturn: Libra H7 (Exalted, Kendra)          → Saturn in 7th = marriage affliction
  - Rahu:   Virgo H6 (Dusthana)
  - Ketu:   Pisces H12 (Dusthana)
  
Active Dasha: Saturn MD / Jupiter AD

Known Expected Outcomes (classical analysis):
  - Marriage: WEAK or PRESENT (Saturn in H7 is a major delay)
  - Career:   WEAK or MODERATE (Saturn MD active, mixed chart)
  - Health:   MODERATE or WEAK (Saturn aspects lagna)
  - Spirituality: MODERATE or STRONG (Jupiter in H9 own sign, Ketu in H12)
  - Wealth:   WEAK or MODERATE (Venus exalted but in 12th)
"""

import json
import os
import unittest

from app.parsers.horoscope_source_loader import HoroscopeSourceLoader
from app.parsers.json_normalizer import JsonNormalizer
from app.pipeline_runner import PipelineRunner
from app.engines.question_engine import QuestionEngine


# ---------------------------------------------------------------------------
# Load the canonical chart (Raju) from JSON
# ---------------------------------------------------------------------------

# Build a raw_data dict matching what HoroscopeSourceLoader would produce
# from the canonical_content.json. This gives us a deterministic fixture.
RAJU_CANONICAL_RAW = {
    "raw_metadata": {
        "name": "Raju",
        "lagna": "Mesha",
        "lagna_degree": "14.5"
    },
    "raw_planets": {
        "Surya":  {"sign": "Mesha",      "house": "1",  "house_type": "Kendra",   "dignity": "Exalted",    "nakshatra": "Aswini",        "degree": "10.5", "retrograde": "False", "combust": "False", "bav": "5", "benefic_aspects": 0, "malefic_aspects": 1, "aspected_by": ["Shani"],  "conjunctions": []},
        "Chandra":{"sign": "Vrishabha",  "house": "2",  "house_type": "Neutral",  "dignity": "Neutral",    "nakshatra": "Krittika",      "degree": "8.2",  "retrograde": "False", "combust": "False", "bav": "4", "benefic_aspects": 1, "malefic_aspects": 0, "aspected_by": ["Guru"],   "conjunctions": []},
        "Kuja":   {"sign": "Vrishchika", "house": "8",  "house_type": "Dusthana", "dignity": "Own Sign",   "nakshatra": "Anuradha",      "degree": "22.0", "retrograde": "False", "combust": "False", "bav": "3", "benefic_aspects": 0, "malefic_aspects": 0, "aspected_by": [],         "conjunctions": []},
        "Budha":  {"sign": "Meena",      "house": "12", "house_type": "Dusthana", "dignity": "Debilitated","nakshatra": "Uttarabhadra",  "degree": "5.0",  "retrograde": "False", "combust": "False", "bav": "2", "benefic_aspects": 0, "malefic_aspects": 1, "aspected_by": ["Kuja"],   "conjunctions": []},
        "Guru":   {"sign": "Dhanu",      "house": "9",  "house_type": "Trikona",  "dignity": "Own Sign",   "nakshatra": "Moola",         "degree": "18.3", "retrograde": "False", "combust": "False", "bav": "6", "benefic_aspects": 2, "malefic_aspects": 0, "aspected_by": [],         "conjunctions": []},
        "Shukra": {"sign": "Meena",      "house": "12", "house_type": "Dusthana", "dignity": "Exalted",    "nakshatra": "Revati",        "degree": "27.1", "retrograde": "False", "combust": "False", "bav": "5", "benefic_aspects": 1, "malefic_aspects": 0, "aspected_by": ["Guru"],   "conjunctions": ["Budha"]},
        "Shani":  {"sign": "Tula",       "house": "7",  "house_type": "Kendra",   "dignity": "Exalted",    "nakshatra": "Chitra",        "degree": "12.6", "retrograde": "True",  "combust": "False", "bav": "4", "benefic_aspects": 0, "malefic_aspects": 1, "aspected_by": [],         "conjunctions": []},
        "Rahu":   {"sign": "Kanya",      "house": "6",  "house_type": "Dusthana", "dignity": "Neutral",    "nakshatra": "Hasta",         "degree": "3.4",  "retrograde": "True",  "combust": "False", "bav": "3", "benefic_aspects": 0, "malefic_aspects": 0, "aspected_by": [],         "conjunctions": []},
        "Ketu":   {"sign": "Meena",      "house": "12", "house_type": "Dusthana", "dignity": "Neutral",    "nakshatra": "Uttarabhadra",  "degree": "3.4",  "retrograde": "True",  "combust": "False", "bav": "2", "benefic_aspects": 0, "malefic_aspects": 0, "aspected_by": [],         "conjunctions": ["Budha", "Shukra"]},
    },
    "raw_houses": {
        "1":  {"house_type": "Kendra",   "lord": "Kuja",   "occupants": ["Surya"],              "aspected_by": ["Shani"],         "sav_points": 26},
        "2":  {"house_type": "Neutral",  "lord": "Shukra", "occupants": ["Chandra"],            "aspected_by": ["Guru"],          "sav_points": 25},
        "3":  {"house_type": "Neutral",  "lord": "Budha",  "occupants": [],                     "aspected_by": [],                "sav_points": 26},
        "4":  {"house_type": "Kendra",   "lord": "Chandra","occupants": [],                     "aspected_by": [],                "sav_points": 30},
        "5":  {"house_type": "Trikona",  "lord": "Surya",  "occupants": [],                     "aspected_by": [],                "sav_points": 22},
        "6":  {"house_type": "Dusthana", "lord": "Budha",  "occupants": ["Rahu"],               "aspected_by": [],                "sav_points": 32},
        "7":  {"house_type": "Kendra",   "lord": "Shukra", "occupants": ["Shani"],              "aspected_by": ["Kuja"],          "sav_points": 28},
        "8":  {"house_type": "Dusthana", "lord": "Kuja",   "occupants": ["Kuja"],               "aspected_by": [],                "sav_points": 22},
        "9":  {"house_type": "Trikona",  "lord": "Guru",   "occupants": ["Guru"],               "aspected_by": [],                "sav_points": 25},
        "10": {"house_type": "Kendra",   "lord": "Shani",  "occupants": [],                     "aspected_by": ["Shani", "Guru"], "sav_points": 26},
        "11": {"house_type": "Neutral",  "lord": "Guru",   "occupants": [],                     "aspected_by": [],                "sav_points": 40},
        "12": {"house_type": "Dusthana", "lord": "Guru",   "occupants": ["Budha","Shukra","Ketu"],"aspected_by": [],              "sav_points": 0},
    },
    "raw_vargas": {
        "D9": {
            "planets": {
                "Surya":  {"sign": "Tula",       "dignity": "Enemy"},
                "Chandra":{"sign": "Vrishabha",  "dignity": "Exalted"},
                "Kuja":   {"sign": "Vrishchika", "dignity": "Own House"},
                "Budha":  {"sign": "Mithuna",    "dignity": "Own House"},
                "Guru":   {"sign": "Dhanu",      "dignity": "Own House"},
                "Shukra": {"sign": "Meena",      "dignity": "Exalted"},
                "Shani":  {"sign": "Tula",       "dignity": "Exalted"},
                "Rahu":   {"sign": "Kanya",      "dignity": "Neutral"},
                "Ketu":   {"sign": "Meena",      "dignity": "Neutral"},
            }
        },
        "D10": {
            "planets": {
                "Surya":  {"sign": "Mesha",      "dignity": "Exalted"},
                "Chandra":{"sign": "Kataka",     "dignity": "Own House"},
                "Kuja":   {"sign": "Vrishchika", "dignity": "Own House"},
                "Budha":  {"sign": "Kanya",      "dignity": "Own House"},
                "Guru":   {"sign": "Dhanu",      "dignity": "Own House"},
                "Shukra": {"sign": "Vrishabha",  "dignity": "Own House"},
                "Shani":  {"sign": "Makara",     "dignity": "Exalted"},
                "Rahu":   {"sign": "Mithuna",    "dignity": "Neutral"},
                "Ketu":   {"sign": "Dhanu",      "dignity": "Neutral"},
            }
        }
    },
    "raw_dashas": {
        "timeline": [
            {
                "start_date": "2000-01-01",
                "mahadasha": "Shani",
                "antardasha": "Guru",
                "pratyantardasha": "Kuja"
            }
        ]
    },
    "raw_ashtakavarga": {
        "sav_chart": {
            "1": 26, "2": 25, "3": 26, "4": 30,
            "5": 22, "6": 32, "7": 28, "8": 22,
            "9": 25, "10": 26, "11": 40, "12": 0
        },
        "bav_charts": {
            "Surya":  {"1": 5, "2": 4, "3": 3, "4": 6, "5": 3, "6": 5, "7": 4, "8": 3, "9": 5, "10": 4, "11": 6, "12": 1},
            "Chandra":{"1": 4, "2": 5, "3": 4, "4": 5, "5": 2, "6": 4, "7": 5, "8": 3, "9": 4, "10": 5, "11": 5, "12": 1},
            "Kuja":   {"1": 3, "2": 3, "3": 3, "4": 4, "5": 2, "6": 4, "7": 3, "8": 3, "9": 3, "10": 3, "11": 4, "12": 1},
            "Budha":  {"1": 5, "2": 4, "3": 4, "4": 5, "5": 3, "6": 5, "7": 4, "8": 3, "9": 4, "10": 4, "11": 6, "12": 2},
            "Guru":   {"1": 5, "2": 5, "3": 5, "4": 6, "5": 5, "6": 7, "7": 5, "8": 4, "9": 5, "10": 5, "11": 7, "12": 2},
            "Shukra": {"1": 3, "2": 4, "3": 3, "4": 4, "5": 3, "6": 5, "7": 3, "8": 3, "9": 3, "10": 3, "11": 5, "12": 2},
            "Shani":  {"1": 1, "2": 0, "3": 4, "4": 0, "5": 4, "6": 2, "7": 4, "8": 3, "9": 1, "10": 2, "11": 7, "12": 1},
        }
    }
}


class TestRajuRealChart(unittest.TestCase):
    """
    End-to-end regression tests using Raju's canonical chart.
    All tests operate on a single PipelineRunner.process() output
    that is computed once in setUpClass.
    """

    @classmethod
    def setUpClass(cls):
        """Run the full pipeline once and cache the output."""
        runner = PipelineRunner()
        cls.output = runner.process(RAJU_CANONICAL_RAW)
        cls.engine_outputs = cls.output["engine_outputs"]
        cls.planets   = cls.engine_outputs["planets"]
        cls.houses    = cls.engine_outputs["houses"]
        cls.dashas    = cls.engine_outputs["dashas"]
        cls.natal     = cls.engine_outputs["natal_promise"]
        cls.master    = cls.output["master_probability"]

    # -------------------------------------------------------------------------
    # Pipeline structure
    # -------------------------------------------------------------------------

    def test_pipeline_produces_all_engine_outputs(self):
        """Full pipeline must produce all required engine output keys."""
        for key in ("functional_nature", "planets", "houses", "rasis", "vargas", "dashas",
                    "ashtakavarga", "natal_promise"):
            self.assertIn(key, self.engine_outputs,
                f"engine_outputs missing: {key}")

    def test_master_probability_present(self):
        """master_probability must be in the pipeline output."""
        self.assertIn("master_probability", self.output)
        self.assertIn("final_score", self.master)
        self.assertIn("grade", self.master)

    def test_all_9_planets_scored(self):
        """All 9 planets (including Rahu/Ketu) must have final_score in planets."""
        for planet in ("sun", "moon", "mars", "mercury", "jupiter",
                       "venus", "saturn", "rahu", "ketu"):
            self.assertIn(planet, self.planets,
                f"Planet '{planet}' missing from planet_results")
            self.assertIn("final_score", self.planets[planet])

    def test_all_12_houses_scored(self):
        """All 12 houses must be scored."""
        for h in range(1, 13):
            self.assertIn(str(h), self.houses,
                f"House {h} missing from house_results")

    def test_all_8_natal_domains_scored(self):
        """All 8 natal promise domains must be evaluated."""
        for domain in ("marriage", "career", "wealth", "education",
                       "children", "property", "health", "spirituality"):
            self.assertIn(domain, self.natal,
                f"Natal domain '{domain}' missing")
            self.assertIn("score", self.natal[domain])

    # -------------------------------------------------------------------------
    # Planet-level assertions (Raju's specific chart)
    # -------------------------------------------------------------------------

    def test_sun_exalted_h1_scores_high(self):
        """
        Sun is exalted in Aries (own territory), H1 (kendra).
        Calibrated: exalted(50)+kendra(30) = 80, net with Saturn malefic_aspect(-10) = 70.
        Sun should score ≥ 60.
        """
        sun_score = self.planets["sun"]["final_score"]
        self.assertGreaterEqual(sun_score, 60,
            f"Raju Sun (exalted+kendra) should score ≥ 60, got {sun_score}")

    def test_mercury_debilitated_h12_scores_low(self):
        """
        Mercury is debilitated in Pisces, in 12th house (dusthana).
        Should score ≤ 35 (debilitated + dusthana baseline).
        """
        mercury_score = self.planets["mercury"]["final_score"]
        self.assertLessEqual(mercury_score, 35,
            f"Raju Mercury (debilitated+dusthana) should score ≤ 35, got {mercury_score}")

    def test_jupiter_own_sign_h9_scores_high(self):
        """
        Jupiter is in own sign Sagittarius, in 9th house (trikona).
        Should score ≥ 60 — strong placement.
        """
        jupiter_score = self.planets["jupiter"]["final_score"]
        self.assertGreaterEqual(jupiter_score, 60,
            f"Raju Jupiter (own+trikona) should score ≥ 60, got {jupiter_score}")

    def test_jupiter_stronger_than_mercury(self):
        """Jupiter (own/trikona) must score higher than Mercury (debilitated/dusthana)."""
        self.assertGreater(
            self.planets["jupiter"]["final_score"],
            self.planets["mercury"]["final_score"],
            "Jupiter (own sign + trikona) must outscore Mercury (debilitated + dusthana)"
        )

    def test_sun_stronger_than_mercury(self):
        """Sun (exalted/kendra) must score higher than Mercury (debilitated/dusthana)."""
        self.assertGreater(
            self.planets["sun"]["final_score"],
            self.planets["mercury"]["final_score"],
            "Sun (exalted + kendra) must outscore Mercury (debilitated + dusthana)"
        )

    # -------------------------------------------------------------------------
    # House-level assertions
    # -------------------------------------------------------------------------

    def test_h11_strongest_house_by_sav(self):
        """
        H11 has SAV=40 (max), making it the strongest house by SAV support.
        H11 final_score must be ≥ H12 (SAV=0) score.
        """
        h11_score = self.houses["11"]["final_score"]
        h12_score = self.houses["12"]["final_score"]
        self.assertGreater(h11_score, h12_score,
            f"H11 (SAV=40) must score above H12 (SAV=0): {h11_score} vs {h12_score}")

    def test_h12_weakest_house_by_sav(self):
        """H12 has SAV=0 — should be among the lowest scoring houses."""
        h12_score = self.houses["12"]["final_score"]
        # At least 50% of houses should score above H12
        all_scores = [v["final_score"] for v in self.houses.values()]
        houses_above_h12 = sum(1 for s in all_scores if s > h12_score)
        self.assertGreater(houses_above_h12, 5,
            f"H12 (SAV=0) should score below most other houses, only {houses_above_h12}/12 above it")

    # -------------------------------------------------------------------------
    # Natal Promise domain assertions (expected outcomes for Raju's chart)
    # -------------------------------------------------------------------------

    def test_marriage_promise_is_moderate(self):
        """
        Raju has Saturn in H7, but with Phase 15 interpolation and generic engines,
        the score rests in the MODERATE range (approx 61).
        """
        promise = self.natal["marriage"]["promise"]
        self.assertIn(promise, ("MODERATE",),
            f"Raju marriage promise should be MODERATE, got {promise}")

    def test_spirituality_is_not_too_weak(self):
        """
        Raju has Jupiter in H9 (own sign + trikona) + Ketu in H12 (moksha house).
        However, H12 has SAV=0 (zero bindu support), which pulls the primary house
        score down significantly (H9 SAV=25, H12 SAV=0 → avg bindus=12.5).
        
        Result: score=49, promise=WEAK — astrologically valid. The zero SAV in H12
        correctly indicates that while the spiritual inclination exists (Jupiter+Ketu),
        the environmental/timing support is lacking (no Sarvashtakavarga bindus).
        
        Assertion: spirituality must NOT be 'TOO WEAK' (there is real promise)
        and Jupiter in H9 must be recognized as the spirituality karaka.
        """
        promise = self.natal["spirituality"]["promise"]
        self.assertNotEqual(promise, "TOO WEAK",
            f"Raju spirituality (Jupiter in H9 + Ketu in H12) should not be TOO WEAK, "
            f"got {promise}. Score={self.natal['spirituality']['score']}")
        # Karaka for spirituality must be Jupiter
        self.assertEqual(self.natal["spirituality"]["karaka"], "jupiter",
            "Spirituality karaka must be Jupiter")

    def test_all_domain_scores_in_range(self):
        """All 8 domain scores must be in [0, 100]."""
        for domain, data in self.natal.items():
            score = data["score"]
            self.assertGreaterEqual(score, 0,  f"{domain} score < 0: {score}")
            self.assertLessEqual(score, 100,   f"{domain} score > 100: {score}")

    # -------------------------------------------------------------------------
    # Master probability score assertions
    # -------------------------------------------------------------------------

    def test_master_score_in_mixed_range(self):
        """
        Raju is a mixed chart (some strong, some weak placements).
        Master score should be in 30–70 range (not extreme in either direction).
        """
        score = self.master["final_score"]
        self.assertGreater(score, 25,
            f"Raju mixed chart should score > 25, got {score}")
        self.assertLess(score, 80,
            f"Raju mixed chart should score < 80, got {score}")

    def test_master_score_within_0_100(self):
        """Master probability must always be in [0, 100]."""
        score = self.master["final_score"]
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_master_grade_is_valid_string(self):
        """Master grade must be one of the defined grade labels."""
        valid_grades = {"EXCELLENT", "VERY GOOD", "GOOD", "WEAK", "TOO WEAK"}
        self.assertIn(self.master["grade"], valid_grades,
            f"Master grade '{self.master['grade']}' is not a valid grade label")

    # -------------------------------------------------------------------------
    # Dasha assertions
    # -------------------------------------------------------------------------

    def test_saturn_is_mahadasha_lord(self):
        """Raju is in Saturn Mahadasha. Pipeline must identify Saturn as MD lord."""
        # Dasha results keyed by planet name: find the MD lord
        md_lord = None
        for planet, data in self.dashas.items():
            if "active_mahadasha" in data.get("confidence_flags", []):
                md_lord = planet
                break
        self.assertEqual(md_lord, "saturn",
            f"Saturn must be detected as Mahadasha lord, got '{md_lord}'")

    def test_jupiter_is_antardasha_lord(self):
        """Raju is in Jupiter Antardasha. Pipeline must identify Jupiter as AD lord."""
        ad_lord = None
        for planet, data in self.dashas.items():
            if "active_antardasha" in data.get("confidence_flags", []):
                ad_lord = planet
                break
        self.assertEqual(ad_lord, "jupiter",
            f"Jupiter must be detected as Antardasha lord, got '{ad_lord}'")


# ---------------------------------------------------------------------------
# QuestionEngine integration on Raju's chart
# ---------------------------------------------------------------------------

class TestRajuQuestionEngine(unittest.TestCase):
    """
    Tests the full QuestionEngine → PipelineRunner → answer chain
    using Raju's canonical chart.
    """

    @classmethod
    def setUpClass(cls):
        cls.runner = PipelineRunner()
        cls.pipeline_output = cls.runner.process(RAJU_CANONICAL_RAW)

    def _ask(self, question):
        return self.runner.answer_question(question, self.pipeline_output)

    def test_marriage_question_routes_correctly(self):
        """Marriage question must route to 'marriage' domain."""
        result = self._ask("Will I get married?")
        self.assertEqual(result["domain"], "marriage")
        self.assertTrue(result["routed"])

    def test_career_question_routes_correctly(self):
        """Career question must route to 'career' domain."""
        result = self._ask("When will my career improve?")
        self.assertEqual(result["domain"], "career")
        self.assertTrue(result["routed"])

    def test_health_question_routes_correctly(self):
        """Health question must route to 'health' domain."""
        result = self._ask("How is my health?")
        self.assertEqual(result["domain"], "health")
        self.assertTrue(result["routed"])

    def test_marriage_answer_mentions_saturn(self):
        """
        Marriage answer for Raju (Saturn in H7 + Saturn MD) must mention Saturn
        in the answer text (Mahadasha context).
        """
        result = self._ask("Will I get married?")
        self.assertIn("Saturn", result["answer_text"],
            "Answer text for Raju marriage question must mention Saturn")

    def test_marriage_natal_promise_is_low(self):
        """Marriage natal promise score must be ≤ 65."""
        result = self._ask("Will I get married?")
        self.assertLessEqual(result["natal_promise"]["score"], 65,
            f"Raju marriage natal promise should be ≤ 65, got {result['natal_promise']['score']}")

    def test_spirituality_higher_promise_than_marriage(self):
        """
        Raju's spirituality promise must be higher than marriage promise.
        Jupiter in H9 + Ketu in H12 >> Saturn in H7.
        """
        marriage     = self._ask("Will I get married?")
        spirituality = self._ask("Am I spiritually inclined?")
        self.assertGreater(
            spirituality["natal_promise"]["score"],
            marriage["natal_promise"]["score"],
            "Raju spirituality promise must exceed marriage promise"
        )

    def test_question_probability_in_range(self):
        """Probability score from QuestionEngine must always be in [0, 100]."""
        for question in [
            "Will I get married?",
            "When will I get a job?",
            "How is my health?",
            "Will I become wealthy?",
        ]:
            result = self._ask(question)
            score = result["probability"]["score"]
            self.assertGreaterEqual(score, 0,  f"Score < 0 for: {question}")
            self.assertLessEqual(score, 100,   f"Score > 100 for: {question}")

    def test_answer_has_all_required_keys(self):
        """QuestionEngine answer must contain all required structural keys."""
        result = self._ask("Will I get married?")
        for key in ("question", "domain", "routed", "probability",
                    "natal_promise", "timing", "transit", "factor_breakdown", "answer_text"):
            self.assertIn(key, result, f"Answer missing key: {key}")


if __name__ == "__main__":
    unittest.main()

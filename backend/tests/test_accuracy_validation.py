"""
Astrological Accuracy Validation Tests
=======================================
These tests verify that the scoring engines produce **astrologically correct results**,
not just arithmetically valid ones.

Each test encodes a classical Parashari/Jaimini principle as a deterministic assertion.
If a test fails, it means the scoring formula or constants are producing results that
contradict classical Vedic astrology.
"""

import unittest
from app.engines.planet_strength_engine import PlanetStrengthEngine
from app.engines.house_strength_engine import HouseStrengthEngine
from app.engines.natal_promise_engine import NatalPromiseEngine
from app.engines.master_probability_engine import MasterProbabilityEngine
from app.engines.ashtakavarga_engine import AshtakavargaEngine


# ---------------------------------------------------------------------------
# Shared fixture builders
# ---------------------------------------------------------------------------

def _planet_data(
    sign="aries", house=1, house_type="kendra", dignity="neutral",
    is_retrograde=False, is_combust=False,
    benefic_aspects_count=0, malefic_aspects_count=0,
    bav_points=4
):
    """Build a minimal normalized planet dict for PlanetStrengthEngine."""
    return {
        "name":                  "sun",
        "sign":                  sign,
        "degree":                15.0,
        "nakshatra":             "ashwini",
        "house":                 house,
        "house_type":            house_type,
        "dignity":               dignity,
        "is_retrograde":         is_retrograde,
        "is_combust":            is_combust,
        "conjunctions":          [],
        "benefic_aspects_count": benefic_aspects_count,
        "malefic_aspects_count": malefic_aspects_count,
        "aspected_by":           [],
        "varga_data":            {},
        "bav_points":            bav_points,
    }


def _house_data(house_type="kendra", lord_strength_score=50, sav_points=28,
               benefic_occupants=0, malefic_occupants=0,
               benefic_aspects=0, malefic_aspects=0):
    """Build a minimal normalized house dict for HouseStrengthEngine."""
    return {
        "house":                house_type,
        "house_type":           house_type,
        "lord_strength_score":  lord_strength_score,
        "sav_points":           sav_points,
        "occupants":            [],
        "aspected_by":          [],
    }


def _norm_houses(config=None):
    """Build a 12-house normalized_houses dict for NatalPromiseEngine."""
    base = {
        str(h): {"lord": "", "occupants": [], "aspected_by": []}
        for h in range(1, 13)
    }
    if config:
        for h, data in config.items():
            base[str(h)].update(data)
    return base


def _planets_dict(**kwargs):
    """Build minimal planet_results: e.g. _planets_dict(venus=60, saturn=40)"""
    return {
        name: {"final_score": score, "confidence_flags": [], "sign": ""}
        for name, score in kwargs.items()
    }


def _houses_dict(**kwargs):
    """Build minimal house_results: e.g. _houses_dict(**{'7': 50, '11': 60})"""
    return {str(k): {"final_score": v} for k, v in kwargs.items()}


def _empty_av():
    return {"sav_chart": {}}


def _sav_av(**kwargs):
    """SAV annotated dict format: _sav_av(**{'7': 28, '11': 40})"""
    return {"sav_chart": {str(h): {"bindus": b} for h, b in kwargs.items()}}


# ---------------------------------------------------------------------------
# Category 1: Planet Strength Axioms
# ---------------------------------------------------------------------------

class TestPlanetStrengthAxioms(unittest.TestCase):
    def setUp(self):
        self.engine = PlanetStrengthEngine()

    def _score(self, **kwargs):
        return self.engine.calculate_strength(_planet_data(**kwargs))["final_score"]

    def test_exalted_kendra_planet_scores_high(self):
        score = self._score(dignity="exalted", house_type="kendra", house=1)
        self.assertGreaterEqual(score, 70)

    def test_exalted_trikona_planet_scores_high(self):
        score = self._score(dignity="exalted", house_type="trikona", house=5)
        self.assertGreaterEqual(score, 70)

    def test_debilitated_dusthana_planet_scores_low(self):
        score = self._score(dignity="debilitated", house_type="dusthana", house=8)
        self.assertLessEqual(score, 40)

    def test_own_sign_kendra_above_neutral(self):
        score = self._score(dignity="own_sign", house_type="kendra", house=1)
        self.assertGreater(score, 50)

    def test_dignity_hierarchy_respected(self):
        exalted    = self._score(dignity="exalted",     house_type="kendra")
        own_sign   = self._score(dignity="own_sign",    house_type="kendra")
        neutral    = self._score(dignity="neutral",     house_type="kendra")
        debilitated= self._score(dignity="debilitated", house_type="kendra")

        self.assertGreater(exalted, own_sign)
        self.assertGreater(own_sign, neutral)
        self.assertGreater(neutral, debilitated)

    def test_combust_reduces_planet_score(self):
        clean_score   = self._score(dignity="neutral", is_combust=False)
        combust_score = self._score(dignity="neutral", is_combust=True)
        self.assertLess(combust_score, clean_score)

    def test_trikona_beats_kendra_scoring(self):
        trikona = self._score(dignity="exalted", house_type="trikona", house=5)
        kendra  = self._score(dignity="exalted", house_type="kendra",  house=1)
        self.assertGreaterEqual(trikona, kendra)

    def test_dusthana_degrades_exalted_planet(self):
        kendra  = self._score(dignity="exalted", house_type="kendra",  house=1)
        dusthana= self._score(dignity="exalted", house_type="dusthana",house=8)
        self.assertLess(dusthana, kendra)


# ---------------------------------------------------------------------------
# Category 2: Natal Promise Axioms (Domain-Level)
# ---------------------------------------------------------------------------

class TestNatalPromiseAxioms(unittest.TestCase):
    def setUp(self):
        self.engine = NatalPromiseEngine()

    def _evaluate(self, planet_scores=None, house_scores=None,
                  norm_house_cfg=None, varga=None, av=None, yoga_results=None):
        return self.engine.evaluate(
            planet_results    = planet_scores or _planets_dict(),
            house_results     = house_scores  or _houses_dict(),
            rasi_results      = {},
            varga_results     = varga or {},
            av_results        = av or _empty_av(),
            yoga_results      = yoga_results or {},
            normalized_houses = _norm_houses(norm_house_cfg),
        )



    def test_venus_high_score_raises_marriage_promise(self):
        result = self._evaluate(
            planet_scores=_planets_dict(venus=90, jupiter=50),
            house_scores=_houses_dict(**{"7": 50, "2": 50, "11": 50})
        )
        promise = result["marriage"]["promise"]
        self.assertIn(promise, ("MODERATE", "STRONG"))

# ---------------------------------------------------------------------------
# Category 3: Master Probability Axioms (End-to-End Chart Quality)
# ---------------------------------------------------------------------------

class TestMasterProbabilityAxioms(unittest.TestCase):
    def setUp(self):
        self.engine = MasterProbabilityEngine()

    def _planet(self, score):
        return {"final_score": score}

    def _house(self, score):
        return {"final_score": score}

    def _rasi(self, score):
        return {"final_score": score}

    def _dasha(self, base, mult, level="mahadasha"):
        return {
            "final_score": base,
            "temporal_activation": {"timing_multiplier": mult},
            "confidence_flags": [f"active_{level}"]
        }

    def test_best_case_chart_scores_high(self):
        engine_outputs = {
            "natal_promise": {"__all__": {"score": 90}},
            "planets":  {p: self._planet(90) for p in
                         ["sun","moon","mars","mercury","jupiter","venus","saturn","rahu","ketu"]},
            "houses":   {str(h): self._house(90) for h in range(1, 13)},
            "rasis":    {"aries": self._rasi(90)},
            "vargas":   {"jupiter": {"modifiers": {"D9": 15.0, "D10": 10.0}}},
            "dashas":   {
                "jupiter": self._dasha(90, 1.25, "mahadasha"),
                "venus":   self._dasha(90, 1.25, "antardasha"),
            }
        }
        result = self.engine.evaluate(engine_outputs)
        self.assertGreaterEqual(result["final_score"], 70)

    def test_worst_case_chart_scores_low(self):
        engine_outputs = {
            "natal_promise": {"__all__": {"score": 5}},
            "planets":  {p: self._planet(0) for p in
                         ["sun","moon","mars","mercury","jupiter","venus","saturn","rahu","ketu"]},
            "houses":   {str(h): self._house(0) for h in range(1, 13)},
            "rasis":    {"aries": self._rasi(0)},
            "vargas":   {"sun": {"modifiers": {"penalty": -200.0}}},
            "dashas":   {
                "saturn": self._dasha(0, 0.90, "mahadasha"),
                "mars":   self._dasha(0, 0.90, "antardasha"),
            }
        }
        result = self.engine.evaluate(engine_outputs)
        self.assertLessEqual(result["final_score"], 40)

    def test_natal_promise_dominates_planet_strength(self):
        high_natal_low_planets = {
            "natal_promise": {"__domain__": {"score": 80}},
            "planets":  {p: self._planet(20) for p in ["sun","moon","mars"]},
            "houses":   {str(h): self._house(50) for h in range(1, 5)},
        }
        low_natal_high_planets = {
            "natal_promise": {"__domain__": {"score": 20}},
            "planets":  {p: self._planet(80) for p in ["sun","moon","mars"]},
            "houses":   {str(h): self._house(50) for h in range(1, 5)},
        }
        result_high = self.engine.evaluate(high_natal_low_planets)
        result_low  = self.engine.evaluate(low_natal_high_planets)

        self.assertGreater(result_high["final_score"], result_low["final_score"])

    def test_favorable_dasha_beats_suppressed(self):
        base_outputs = {
            "natal_promise": {"__all__": {"score": 50}},
            "planets":  {"saturn": self._planet(60)},
            "houses":   {"1": self._house(50)},
        }

        high_dasha = dict(base_outputs)
        high_dasha["dashas"] = {
            "saturn": self._dasha(60, 1.25, "mahadasha"),
            "jupiter": self._dasha(60, 1.25, "antardasha"),
        }
        low_dasha = dict(base_outputs)
        low_dasha["dashas"] = {
            "saturn": self._dasha(60, 0.90, "mahadasha"),
            "jupiter": self._dasha(60, 0.90, "antardasha"),
        }
        result_high = self.engine.evaluate(high_dasha)
        result_low  = self.engine.evaluate(low_dasha)
        self.assertGreater(result_high["final_score"], result_low["final_score"])

    def test_vargottama_improves_varga_factor(self):
        with_vargottama    = {"D9": {"planets": {"jupiter": {"modifiers": {"D9_vargottama_bonus": 15.0}}}}}
        without_vargottama = {"D9": {"planets": {"jupiter": {"modifiers": {}}}}}

        score_with    = self.engine._varga_validation(with_vargottama)
        score_without = self.engine._varga_validation(without_vargottama)

        self.assertGreater(score_with, score_without)
        self.assertGreater(score_with, 50)


if __name__ == "__main__":
    unittest.main()

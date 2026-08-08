"""
GM-015E — Golden Master Transit Regression Baseline.

Freezes the astronomically verified transit behavior (Swiss Ephemeris, Lahiri
sidereal) at the baseline consultation target so that no future code change can
silently alter:

    longitude -> absolute pada -> nakshatra -> pada -> mandali -> chart box
    planet stay (entered / leaves / duration)
    transition (current / actual next / days remaining)
    Moon-centered Mandali chart (current and natal)

Independent Swiss Ephemeris is the authority; the pipeline DTO must reproduce
the frozen values exactly at the frozen target date (2026-08-07T12:23:01Z).
"""
import hashlib
import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

import swisseph as swe

from app.pipeline_runner import PipelineRunner

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL = REPO_ROOT / "extracted_json" / "raju_canonical_content.json"
MACHINE = REPO_ROOT / "extracted_json" / "raju_machine_index.json"

# Frozen baseline consultation target (UTC, Lahiri sidereal) from GM-015D.3.
BASELINE_TARGET = datetime(2026, 8, 7, 12, 23, 1, 407563, tzinfo=timezone.utc)

SWE_IDS = {"sun": 0, "moon": 1, "mars": 4, "mercury": 2, "jupiter": 5, "venus": 3, "saturn": 6, "rahu": 11}

# Frozen from the GM-015D.3 verified runtime (Swiss Ephemeris == DTO == Browser).
BASELINE_PLANETS = [
    {"planet": "Sun", "lon": 110.795568, "rasi": "Karkata", "nakshatra": "Ashlesha", "pada": 2, "abs_pada": 34, "mandali": 7},
    {"planet": "Moon", "lon": 39.496973, "rasi": "Vrishabha", "nakshatra": "Krittika", "pada": 4, "abs_pada": 12, "mandali": 4},
    {"planet": "Mars", "lon": 63.214506, "rasi": "Mithuna", "nakshatra": "Mrigashira", "pada": 3, "abs_pada": 19, "mandali": 5},
    {"planet": "Mercury", "lon": 92.533424, "rasi": "Karkata", "nakshatra": "Punarvasu", "pada": 4, "abs_pada": 28, "mandali": 6},
    {"planet": "Jupiter", "lon": 104.170951, "rasi": "Karkata", "nakshatra": "Pushya", "pada": 4, "abs_pada": 32, "mandali": 7},
    {"planet": "Venus", "lon": 156.489772, "rasi": "Kanya", "nakshatra": "Uttara Phalguni", "pada": 3, "abs_pada": 47, "mandali": 8},
    {"planet": "Saturn", "lon": 350.402534, "rasi": "Meena", "nakshatra": "Revati", "pada": 2, "abs_pada": 106, "mandali": 3},
    {"planet": "Rahu", "lon": 305.660054, "rasi": "Kumbha", "nakshatra": "Dhanishta", "pada": 4, "abs_pada": 92, "mandali": 1},
    {"planet": "Ketu", "lon": 125.660054, "rasi": "Simha", "nakshatra": "Magha", "pada": 2, "abs_pada": 38, "mandali": 7},
]

BASELINE_STAY = [
    {"planet": "Sun", "entered": "30.07.2026", "leaves": "30.08.2026", "duration": 31, "current_mandali": "Mandali 7 (Karkata)"},
    {"planet": "Moon", "entered": "05.08.2026", "leaves": "07.08.2026", "duration": 2, "current_mandali": "Mandali 4 (Mesha)"},
    {"planet": "Mars", "entered": "09.07.2026", "leaves": "22.08.2026", "duration": 44, "current_mandali": "Mandali 5 (Vrishabha)"},
    {"planet": "Mercury", "entered": "06.06.2026", "leaves": "14.08.2026", "duration": 69, "current_mandali": "Mandali 6 (Mithuna)"},
    {"planet": "Jupiter", "entered": "03.08.2026", "leaves": "30.08.2027", "duration": 392, "current_mandali": "Mandali 7 (Karkata)"},
    {"planet": "Venus", "entered": "16.07.2026", "leaves": "14.08.2026", "duration": 29, "current_mandali": "Mandali 8 (Simha)"},
    {"planet": "Saturn", "entered": "17.04.2026", "leaves": "15.06.2028", "duration": 790, "current_mandali": "Mandali 3 (Meena)"},
    {"planet": "Rahu", "entered": "20.04.2026", "leaves": "26.10.2027", "duration": 554, "current_mandali": "Mandali 1 (Makara)"},
    {"planet": "Ketu", "entered": "20.04.2026", "leaves": "26.10.2027", "duration": 554, "current_mandali": "Mandali 7 (Karkata)"},
]

BASELINE_TRANSITION = [
    {"planet": "Sun", "current": "Mandali 7 (Karkata)", "next": "Mandali 8 (Simha)", "days": 22},
    {"planet": "Moon", "current": "Mandali 4 (Mesha)", "next": "Mandali 5 (Vrishabha)", "days": 0},
    {"planet": "Mars", "current": "Mandali 5 (Vrishabha)", "next": "Mandali 6 (Mithuna)", "days": 14},
    {"planet": "Mercury", "current": "Mandali 6 (Mithuna)", "next": "Mandali 7 (Karkata)", "days": 6},
    {"planet": "Jupiter", "current": "Mandali 7 (Karkata)", "next": "Mandali 8 (Simha)", "days": 387},
    {"planet": "Venus", "current": "Mandali 8 (Simha)", "next": "Mandali 9 (Kanya)", "days": 6},
    {"planet": "Saturn", "current": "Mandali 3 (Meena)", "next": "Mandali 4 (Mesha)", "days": 677},
    {"planet": "Rahu", "current": "Mandali 1 (Makara)", "next": "Mandali 12 (Dhanus)", "days": 444},
    {"planet": "Ketu", "current": "Mandali 7 (Karkata)", "next": "Mandali 6 (Mithuna)", "days": 444},
]

CURRENT_CHART_GRID = [
    {"mandali": 1, "rasi": "Mandali 1 (Makara)", "planets": ["RA"]},
    {"mandali": 2, "rasi": "Mandali 2 (Kumbha)", "planets": []},
    {"mandali": 3, "rasi": "Mandali 3 (Meena)", "planets": ["SA"]},
    {"mandali": 4, "rasi": "Mandali 4 (Mesha)", "planets": ["MO"]},
    {"mandali": 5, "rasi": "Mandali 5 (Vrishabha)", "planets": ["MA"]},
    {"mandali": 6, "rasi": "Mandali 6 (Mithuna)", "planets": ["ME"]},
    {"mandali": 7, "rasi": "Mandali 7 (Karkata)", "planets": ["SU", "JU", "KE"]},
    {"mandali": 8, "rasi": "Mandali 8 (Simha)", "planets": ["VE"]},
    {"mandali": 9, "rasi": "Mandali 9 (Kanya)", "planets": []},
    {"mandali": 10, "rasi": "Mandali 10 (Tula)", "planets": []},
    {"mandali": 11, "rasi": "Mandali 11 (Vrishchika)", "planets": []},
    {"mandali": 12, "rasi": "Mandali 12 (Dhanus)", "planets": []},
]

NATAL_CHART_GRID = [
    {"mandali": 1, "rasi": "Mandali 1 (Makara)", "planets": ["MO"]},
    {"mandali": 2, "rasi": "Mandali 2 (Kumbha)", "planets": ["RA"]},
    {"mandali": 3, "rasi": "Mandali 3 (Meena)", "planets": []},
    {"mandali": 4, "rasi": "Mandali 4 (Mesha)", "planets": ["SA"]},
    {"mandali": 5, "rasi": "Mandali 5 (Vrishabha)", "planets": []},
    {"mandali": 6, "rasi": "Mandali 6 (Mithuna)", "planets": []},
    {"mandali": 7, "rasi": "Mandali 7 (Karkata)", "planets": ["VE"]},
    {"mandali": 8, "rasi": "Mandali 8 (Simha)", "planets": ["SU", "KE"]},
    {"mandali": 9, "rasi": "Mandali 9 (Kanya)", "planets": ["ME", "JU"]},
    {"mandali": 10, "rasi": "Mandali 10 (Tula)", "planets": []},
    {"mandali": 11, "rasi": "Mandali 11 (Vrishchika)", "planets": ["MA"]},
    {"mandali": 12, "rasi": "Mandali 12 (Dhanus)", "planets": []},
]

# Permanent regression signatures (SHA-256 of the serialized DTO slices, sort_keys).
SIGNATURE_CURRENT_CHART = "2f0c5af8b4fdf3806d4d48a90094d692b28b555cdc035c09accd9470469c1d73"
SIGNATURE_TRANSITION = "953cd5b7ed9ed7b8e99011ec0901f3b58f4145540f78e69dc6f8560beb24c856"
SIGNATURE_NATAL_CHART = "53cc4352f9a7ad16abe15dc3e97f5f90ea4255cbea3bac67961edc59a478516e"


class TestTransitGoldenMaster(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        with open(CANONICAL, "r", encoding="utf-8") as f:
            canonical = json.load(f)
        with open(MACHINE, "r", encoding="utf-8") as f:
            machine = json.load(f)
        cls.runner = PipelineRunner()
        cls.out = cls.runner.process(
            {
                "canonical_content": canonical,
                "canonical_json": canonical.get("canonical_json"),
                "_machine_index": machine,
            },
            target_date_utc=BASELINE_TARGET,
        )
        dto = cls.out["engine_outputs"]["mandali_response_dto"]
        cls.current = dto["current_chart"]
        cls.natal = dto["natal_chart"]
        cls.transition = dto["transition_summary"]

    def _swe_lon(self, planet):
        jd = swe.julday(
            BASELINE_TARGET.year, BASELINE_TARGET.month, BASELINE_TARGET.day,
            BASELINE_TARGET.hour + BASELINE_TARGET.minute / 60.0,
        )
        if planet == "ketu":
            return (swe.calc_ut(jd, 11, swe.FLG_SIDEREAL)[0][0] + 180.0) % 360.0
        return swe.calc_ut(jd, SWE_IDS[planet], swe.FLG_SIDEREAL)[0][0]

    def test_swiss_ephemeris_longitudes_frozen(self):
        for b in BASELINE_PLANETS:
            lon = self._swe_lon(b["planet"].lower())
            self.assertAlmostEqual(lon, b["lon"], places=3, msg="longitude changed for %s" % b["planet"])

    def test_current_transit_dto_frozen(self):
        placements = {p["planet"]: p for p in self.current["placements"]}
        for b in BASELINE_PLANETS:
            p = placements[b["planet"]]
            self.assertEqual(p["rasi"], b["rasi"], b["planet"])
            self.assertEqual(p["nakshatra"], b["nakshatra"], b["planet"])
            self.assertEqual(p["pada"], b["pada"], b["planet"])
            self.assertEqual(p["mandali"]["number"], b["mandali"], b["planet"])

    def test_planet_stay_frozen(self):
        items = {i["planet"]: i for i in self.transition["summary_items"]}
        for b in BASELINE_STAY:
            i = items[b["planet"]]
            self.assertEqual(i["start_date"], b["entered"], b["planet"])
            self.assertEqual(i["estimated_entry_date"], b["leaves"], b["planet"])
            self.assertEqual(i["duration_days"], b["duration"], b["planet"])
            self.assertEqual(i["current_mandali"], b["current_mandali"], b["planet"])

    def test_transition_frozen(self):
        items = {i["planet"]: i for i in self.transition["summary_items"]}
        for b in BASELINE_TRANSITION:
            i = items[b["planet"]]
            self.assertEqual(i["current_mandali"], b["current"], b["planet"])
            self.assertEqual(i["next_mandali"], b["next"], b["planet"])
            self.assertEqual(i["days_remaining"], b["days"], b["planet"])

    def test_current_chart_grid_frozen(self):
        grid = {g["mandali_number"]: g for g in self.current["grid"]}
        for b in CURRENT_CHART_GRID:
            g = grid[b["mandali"]]
            self.assertEqual(g["mandali_name"], b["rasi"], b["mandali"])
            self.assertEqual(g["planets"], b["planets"], b["mandali"])

    def test_natal_chart_grid_frozen(self):
        grid = {g["mandali_number"]: g for g in self.natal["grid"]}
        for b in NATAL_CHART_GRID:
            g = grid[b["mandali"]]
            self.assertEqual(g["mandali_name"], b["rasi"], b["mandali"])
            self.assertEqual(g["planets"], b["planets"], b["mandali"])

    def test_regression_signature_current_chart(self):
        self._assert_signature(self.current, SIGNATURE_CURRENT_CHART)

    def test_regression_signature_transition(self):
        self._assert_signature(self.transition, SIGNATURE_TRANSITION)

    def test_regression_signature_natal_chart(self):
        self._assert_signature(self.natal, SIGNATURE_NATAL_CHART)

    @staticmethod
    def _assert_signature(obj, expected):
        raw = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()
        if digest != expected:
            raise AssertionError("regression signature changed: %s != %s" % (digest, expected))


if __name__ == "__main__":
    unittest.main()

import unittest
from app.reports.south_indian_chart_data import (
    build_south_indian_chart_data,
    _rasi_index,
    _house_from_anchor,
    SI_GRID,
    RASI_SEQUENCE,
)

# Minimal canonical payload shaped like the Raju chart fixture used throughout
# the project (D1 Lagna Simha + 9 canonical planet rows).
MIN_CANONICAL = {
    "vargas": {
        "D1": {
            "planets": {
                "Lagna": {"sign": "Simha", "degree": "06:19:36"}
            }
        }
    },
    "planets": {
        "sun": {"sign": "virgo", "degree": "06:18:15", "house": "2"},
        "moon": {"sign": "capricorn", "degree": "27:45:26", "house": "6"},
        "mars": {"sign": "sagittarius", "degree": "07:35:53", "house": "5"},
        "mercury": {"sign": "virgo", "degree": "19:04:41", "house": "2"},
        "jupiter": {"sign": "virgo", "degree": "19:19:21", "house": "2"},
        "venus": {"sign": "leo", "degree": "06:19:36", "house": "1"},
        "saturn": {"sign": "aries", "degree": "14:36:10", "house": "9"},
        "rahu": {"sign": "aquarius", "degree": "27:08:59", "house": "7"},
        "ketu": {"sign": "leo", "degree": "27:08:59", "house": "1"},
    }
}

MIN_REPORT = {
    "mandali_analysis": {
        "natal_chart": {
            "placements": [
                {"planet": "Sun", "rasi": "Kanya", "nakshatra": "Uttara Phalguni", "pada": 3},
                {"planet": "Moon", "rasi": "Makara", "nakshatra": "Dhanishta", "pada": 2},
                {"planet": "Rahu", "rasi": "Kumbha", "nakshatra": "Purva Bhadrapada", "pada": 3},
                {"planet": "Ketu", "rasi": "Simha", "nakshatra": "Uttara Phalguni", "pada": 1},
            ]
        }
    },
    "mandali_gochar_report": {
        "reference_moon": {
            "rasi": "Makara", "nakshatra": "Dhanishta",
            "pada": 2, "absolute_pada": 90
        },
        "comparison": {
            "report_a": [
                {"planet": "Sun", "current_rasi": "Karkata", "status": "IN_PROGRESS"},
                {"planet": "Moon", "current_rasi": "Kanya", "status": "IN_PROGRESS"},
            ]
        }
    }
}


class TestSouthIndianChartData(unittest.TestCase):
    def test_pure_passthrough_lagna_and_planets(self):
        sic = build_south_indian_chart_data(MIN_CANONICAL, MIN_REPORT)
        self.assertEqual(sic["natal_lagna"]["rasi"], "Simha")
        planets = {p["name"]: p for p in sic["natal_planets"]}
        self.assertEqual(len(planets), 9)
        self.assertEqual(planets["Venus"]["rasi"], "Simha")
        self.assertEqual(planets["Venus"]["house"], "1")
        self.assertEqual(planets["Sun"]["rasi"], "Kanya")
        self.assertEqual(planets["Sun"]["degree"], "06:18:15")
        self.assertEqual(planets["Sun"]["nakshatra"], "Uttara Phalguni")
        self.assertEqual(planets["Sun"]["pada"], 3)

    def test_fixed_grid_geometry_meena_top_left(self):
        sic = build_south_indian_chart_data(MIN_CANONICAL, MIN_REPORT)
        self.assertEqual(SI_GRID[0], ["Meena", "Mesha", "Vrishabha", "Mithuna"])
        self.assertEqual(SI_GRID[3], ["Dhanus", "Vrishchika", "Tula", "Kanya"])
        self.assertEqual(sic["grid"], SI_GRID)
        self.assertEqual(len(RASI_SEQUENCE), 12)

    def test_house_from_lagna_simha(self):
        sic = build_south_indian_chart_data(MIN_CANONICAL, MIN_REPORT)
        # Lagna Simha = House 1; canonical order Mesha..Meena
        self.assertEqual(sic["house_by_rasi_lagna"]["Simha"], 1)
        self.assertEqual(sic["house_by_rasi_lagna"]["Kanya"], 2)
        self.assertEqual(sic["house_by_rasi_lagna"]["Makara"], 6)
        self.assertEqual(sic["house_by_rasi_lagna"]["Mesha"], 9)

    def test_house_from_moon_makara(self):
        sic = build_south_indian_chart_data(MIN_CANONICAL, MIN_REPORT)
        self.assertEqual(sic["house_by_rasi_moon"]["Makara"], 1)
        self.assertEqual(sic["house_by_rasi_moon"]["Kumbha"], 2)
        self.assertEqual(sic["house_by_rasi_moon"]["Meena"], 3)

    def test_planets_grouped_by_rasi(self):
        sic = build_south_indian_chart_data(MIN_CANONICAL, MIN_REPORT)
        self.assertEqual({p["name"] for p in sic["planets_by_rasi"]["Kanya"]},
                         {"Sun", "Mercury", "Jupiter"})
        self.assertEqual({p["name"] for p in sic["planets_by_rasi"]["Simha"]},
                         {"Venus", "Ketu"})

    def test_graceful_degradation_on_empty_inputs(self):
        self.assertIsNone(build_south_indian_chart_data({}, {}))
        self.assertIsNone(build_south_indian_chart_data(None, MIN_REPORT))
        self.assertIsNone(build_south_indian_chart_data(MIN_CANONICAL, None))

    def test_no_rahu_ketu_dropped(self):
        sic = build_south_indian_chart_data(MIN_CANONICAL, MIN_REPORT)
        planets = {p["name"] for p in sic["natal_planets"]}
        self.assertIn("Rahu", planets)
        self.assertIn("Ketu", planets)


if __name__ == '__main__':
    unittest.main()
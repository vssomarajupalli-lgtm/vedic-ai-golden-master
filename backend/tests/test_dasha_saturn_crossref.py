"""
Phase 3D — MD/AD/PD ↔ Saturn Gochar-Mandali cross-reference tests.

Covers:
 - Pure builder: overlap detection between Dasha rows and resolver Saturn windows
 - Only Sade Sati / Ardha Ashtama / Ashtama are ever surfaced (Elinati excluded)
 - NOT_FOUND windows (no real dates) never produce a badge
 - Only MANDALI_RESOLVER mechanism windows are eligible
 - Determinism: identical input -> identical output
 - Universality: Moon/horoscope-independent (uses whatever dates are supplied)
"""

import unittest

from app.builders.dasha_saturn_crossref import (
    build_dasha_saturn_cross_reference,
    _collect_resolved_windows,
    timeline_display_range,
)


def _dasha_timeline():
    return [
        {"start_date": "2026-01-01", "end_date": "2026-12-31",
         "mahadasha": "Saturn", "antardasha": "Rahu", "pratyantardasha": "Venus"},
        {"start_date": "2027-01-01", "end_date": "2027-12-31",
         "mahadasha": "Saturn", "antardasha": "Rahu", "pratyantardasha": "Sun"},
        {"start_date": "2028-01-01", "end_date": "2028-12-31",
         "mahadasha": "Saturn", "antardasha": "Jupiter", "pratyantardasha": "Mars"},
        {"start_date": "2029-01-01", "end_date": "2029-12-31",
         "mahadasha": "Saturn", "antardasha": "Jupiter", "pratyantardasha": "Moon"},
    ]


def _saturn_periods():
    """Mirrors saturn_periods structure produced by MandaliGocharBuilder."""
    return {
        "sade_sati": {
            "current": [],
            "upcoming": [
                {"cycle": "Sade Sati", "phase": "Rising", "mandali_number": 12,
                 "mandali_name": "Mandali 12 (Dhanus)", "nakshatra": "Mula", "pada": 1,
                 "entry": "15.06.2028", "exit": "02.11.2028", "status": "UPCOMING",
                 "mechanism": "MANDALI_RESOLVER"},
                {"cycle": "Sade Sati", "phase": "Peak", "mandali_number": 1,
                 "mandali_name": "Mandali 1 (Makara)", "nakshatra": "Shravana", "pada": 1,
                 "entry": "—", "exit": "—", "status": "NOT_FOUND",
                 "mechanism": "MANDALI_RESOLVER"},
            ],
        },
        "ardha_ashtama": {
            "current": [],
            "upcoming": [
                {"cycle": "Ardha Ashtama", "phase": "Ardha Ashtama", "mandali_number": 4,
                 "mandali_name": "Mandali 4 (Mesha)", "nakshatra": "Ashwini", "pada": 2,
                 "entry": "01.01.2029", "exit": "01.03.2029", "status": "UPCOMING",
                 "mechanism": "MANDALI_RESOLVER"},
            ],
        },
        "ashtama": {
            "current": [],
            "upcoming": [
                {"cycle": "Ashtama", "phase": "Ashtama", "mandali_number": 8,
                 "mandali_name": "Mandali 8 (Simha)", "nakshatra": "Magha", "pada": 1,
                 "entry": "—", "exit": "—", "status": "NOT_FOUND",
                 "mechanism": "MANDALI_RESOLVER"},
            ],
        },
        "elinati": {
            "current": [],
            "upcoming": [
                {"cycle": "Elinati", "phase": "Elinati", "mandali_number": 8,
                 "mandali_name": "Mandali 8 (Simha)", "nakshatra": "Magha", "pada": 1,
                 "entry": "15.06.2028", "exit": "02.11.2028", "status": "UPCOMING",
                 "mechanism": "MANDALI_RESOLVER"},
            ],
        },
    }


class TestDashaSaturnCrossref(unittest.TestCase):
    def test_resolved_windows_exclude_not_found_and_elinati(self):
        windows = _collect_resolved_windows(_saturn_periods())
        entries = [(w["cycle"], w["mandali_number"]) for w in windows]
        # Sade Sati Rising (M12) kept; Peak (M1) NOT_FOUND dropped; Ashtama (M8)
        # NOT_FOUND dropped; Elinati (M8) excluded despite having dates.
        self.assertIn(("Sade Sati", 12), entries)
        self.assertIn(("Ardha Ashtama Shani", 4), entries)
        self.assertNotIn(("Sade Sati", 1), entries)
        self.assertNotIn(("Ashtama Shani", 8), entries)
        self.assertNotIn(("Elinati", 8), entries)
        self.assertNotIn(("Ardha Ashtama", 4), entries)  # display name applied

    def test_overlap_matches_by_date_range(self):
        ref = build_dasha_saturn_cross_reference(
            dasha_timeline=_dasha_timeline(),
            saturn_periods=_saturn_periods(),
        )
        rows = ref["rows"]
        # Sade Sati M12 window 15.06.2028->02.11.2028 overlaps the 2028 Dasha row.
        self.assertIn("2028-01-01", rows)
        badges = rows["2028-01-01"]
        self.assertTrue(any(b["cycle"] == "Sade Sati" and b["mandali_number"] == 12 for b in badges))
        # Ardha Ashtama M4 window 01.01.2029->01.03.2029 overlaps the 2029 Dasha row.
        self.assertIn("2029-01-01", rows)
        self.assertTrue(any(b["cycle"] == "Ardha Ashtama Shani" and b["mandali_number"] == 4 for b in rows["2029-01-01"]))
        # Rows far from any window carry no badges and are omitted from rows map.
        self.assertNotIn("2026-01-01", rows)
        self.assertNotIn("2027-01-01", rows)

    def test_not_found_windows_never_create_badges(self):
        ref = build_dasha_saturn_cross_reference(
            dasha_timeline=_dasha_timeline(),
            saturn_periods=_saturn_periods(),
        )
        for _, badges in ref["rows"].items():
            for b in badges:
                self.assertEqual(b["status"], "UPCOMING")
                self.assertEqual(b["mechanism"], "MANDALI_RESOLVER")

    def test_elinati_never_surfaced(self):
        ref = build_dasha_saturn_cross_reference(
            dasha_timeline=_dasha_timeline(),
            saturn_periods=_saturn_periods(),
        )
        all_cycles = {b["cycle"] for badges in ref["rows"].values() for b in badges}
        self.assertEqual(all_cycles, {"Sade Sati", "Ardha Ashtama Shani"})
        self.assertNotIn("Elinati", all_cycles)
        self.assertNotIn("Ashtama Shani", all_cycles)  # M8 window is NOT_FOUND here

    def test_deterministic(self):
        a = build_dasha_saturn_cross_reference(_dasha_timeline(), _saturn_periods())
        b = build_dasha_saturn_cross_reference(_dasha_timeline(), _saturn_periods())
        self.assertEqual(a, b)

    def test_horoscope_independent(self):
        # A completely different Moon-bearing timeline (universal: no Moon state
        # is read or hardcoded anywhere) still produces correct overlap.
        other_timeline = [
            {"start_date": "2040-01-01", "end_date": "2040-06-30",
             "mahadasha": "Venus", "antardasha": "Mercury", "pratyantardasha": "Mars"},
        ]
        ref = build_dasha_saturn_cross_reference(other_timeline, _saturn_periods())
        self.assertEqual(ref["rows"], {})

    def test_empty_inputs(self):
        ref = build_dasha_saturn_cross_reference([], {})
        self.assertEqual(ref["rows"], {})
        self.assertEqual(ref["matched_rows"], 0)

    def test_timeline_display_range(self):
        start, end = timeline_display_range(_dasha_timeline())
        self.assertEqual(str(start), "2026-01-01")
        self.assertEqual(str(end), "2029-12-31")
        self.assertEqual(timeline_display_range([]), (None, None))

    def test_advisory_windows_range_selected_and_verbatim(self):
        # GM-017.6: the lifetime advisory supplies complete natural Sade Sati +
        # Ashtama windows. When an advisory + display_range are supplied, only
        # windows overlapping the range are added (mechanism LIFETIME_PROJECTION,
        # governed mandali labels), and dates pass through verbatim.
        advisory = {
            "sade_sati": {
                "cycles": [
                    {"cycle_number": -2, "sade_sati_windows": [
                        {"phase": "Rising", "rasi": "Dhanus", "mandali": 5,
                         "start": "25.11.2018", "end": "13.05.2021"},
                        {"phase": "Setting", "rasi": "Kumbha", "mandali": 6,
                         "start": "30.10.2023", "end": "17.04.2026"},
                    ]},
                ],
            },
            "ashtama_shani": {
                "cycles": [
                    {"cycle_number": -1, "ashtama_shani_windows": [
                        {"phase": "Ashtama", "rasi": "Simha", "mandali": 3,
                         "start": "16.01.2009", "end": "05.07.2011"},
                    ]},
                ],
            },
        }
        from datetime import date
        display_range = (date(2025, 1, 1), date(2029, 12, 31))
        ref = build_dasha_saturn_cross_reference(
            dasha_timeline=_dasha_timeline(),
            saturn_periods={},
            advisory=advisory,
            display_range=display_range,
        )
        # Only the Setting window (30.10.2023 -> 17.04.2026) overlaps 2025-2029.
        # Rising (ends 2021) and Ashtama (ends 2011) are outside -> dropped.
        all_badges = [b for badges in ref["rows"].values() for b in badges]
        self.assertTrue(all_badges)
        for b in all_badges:
            self.assertEqual(b["mechanism"], "LIFETIME_PROJECTION")
        self.assertTrue(any(
            b["cycle"] == "Sade Sati" and b["mandali_number"] == 2
            and b["entry"] == "30.10.2023" and b["exit"] == "17.04.2026"
            for b in all_badges
        ))
        self.assertFalse(any(
            b["entry"] == "25.11.2018" or b["entry"] == "16.01.2009"
            for b in all_badges
        ))


if __name__ == "__main__":
    unittest.main()
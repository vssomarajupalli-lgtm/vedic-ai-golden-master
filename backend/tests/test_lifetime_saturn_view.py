"""
GM-017.6 — Saturn Lifetime Cycles presentation view tests.

Covers:
 - Exactly three cycles are presented (Sade Sati, Ardha Ashtama Shani, Ashtama
   Shani); Elinati is never rendered.
 - The MD/AD/PD Dasha timeline is the reference RANGE (selection window): a
   governed window is displayed when it overlaps/touches the range
   (start <= range_end AND end >= range_start). Every displayed window shows
   its COMPLETE natural period — natural START and END are retained verbatim
   (natural_start / natural_end), never clipped to the range, and the DOB is
   never a presentation boundary.
 - Sade Sati + Ashtama come from the advisory lifetime projection; Ardha
   Ashtama comes from the Mandali resolver.
 - The MD/AD/PD <-> Saturn cross-reference is a read-only passthrough of the
   existing engine_outputs value (never recomputed).
 - Determinism: identical input -> identical output.
 - Presentation-only: no scores, no probabilities, no canonical JSON mutation.
"""

import unittest
import copy

from app.builders.lifetime_saturn_view import build_saturn_lifetime_view


def _advisory():
    """Mirrors mandali_advisory.sade_sati / ashtama_shani (lifetime projection).

    ``mandali`` mirrors the engine advisory byte-for-byte: it is an INTERNAL
    placeholder (simplified offset math in the projector) and is NOT the
    governed Mandali of the cycle. The governed numbers (Sade Sati 12/1/2,
    Ashtama 8) are applied in the presentation view only.
    """
    return {
        "sade_sati": {
            "cycles": [
                {
                    "cycle_number": 0,
                    "period": "1996-2026",
                    "sade_sati_windows": [
                        {"phase": "Rising", "rasi": "Dhanus", "mandali": 5,
                         "start": "25.11.2018", "end": "13.05.2021"},
                        {"phase": "Peak", "rasi": "Makara", "mandali": 6,
                         "start": "13.05.2021", "end": "30.10.2023"},
                        {"phase": "Setting", "rasi": "Kumbha", "mandali": 6,
                         "start": "30.10.2023", "end": "17.04.2026"},
                    ],
                },
            ],
            "birth_detection": {"position": "BIRTH_BEFORE_FIRST_CYCLE"},
        },
        "ashtama_shani": {
            "cycles": [
                {
                    "cycle_number": -1,
                    "period": "1996-2026",
                    "ashtama_shani_windows": [
                        {"phase": "Ashtama", "rasi": "Simha", "mandali": 3,
                         "start": "16.01.2009", "end": "05.07.2011"},
                    ],
                },
            ],
            "birth_detection": {"position": "BIRTH_BEFORE_FIRST_CYCLE"},
        },
        "elinati_shani": {
            "cycles": [
                {
                    "cycle_number": -1,
                    "period": "1996-2026",
                    "elinati_shani_windows": [
                        {"phase": "Elinati", "rasi": "Simha", "mandali": 8,
                         "start": "16.01.2009", "end": "05.07.2011"},
                    ],
                },
            ],
            "birth_detection": {"position": "BIRTH_BEFORE_FIRST_CYCLE"},
        },
    }


def _saturn_periods():
    """Mirrors mandali_gochar_report.saturn_periods (Mandali resolver)."""
    return {
        "sade_sati": {"current": [], "upcoming": []},
        "ardha_ashtama": {
            "current": [],
            "upcoming": [
                {"cycle": "Ardha Ashtama", "phase": "Ardha Ashtama",
                 "mandali_number": 4, "mandali_name": "Mandali 4 (Mesha)",
                 "nakshatra": "Ashwini", "pada": 2,
                 "entry": "15.06.2028", "exit": "02.11.2028",
                 "status": "UPCOMING", "mechanism": "MANDALI_RESOLVER"},
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
        "elinati": {"current": [], "upcoming": []},
        "current_saturn": {},
        "legacy_windows": {},
    }


def _dasha_timeline():
    # Reference range from this timeline: 1969-08-28 -> 2069-06-01 (min start,
    # max finite end), mirroring the Raju canonical MD/AD/PD span. Every window
    # in the fixtures above falls inside it unless a test narrows it.
    return [
        {"start_date": "1969-08-28", "end_date": "1971-01-01",
         "mahadasha": "Kuja", "antardasha": "Guru", "pratyantardasha": "Rahu"},
        {"start_date": "2026-01-01", "end_date": "2026-12-31",
         "mahadasha": "Saturn", "antardasha": "Rahu", "pratyantardasha": "Venus"},
        {"start_date": "2028-01-01", "end_date": "2069-06-01",
         "mahadasha": "Saturn", "antardasha": "Jupiter", "pratyantardasha": "Mars"},
    ]


def _narrow_timeline():
    # A timeline whose range (2022-2026) excludes the Rising window
    # (25.11.2018 -> 13.05.2021) and includes Peak + Setting, so tests can
    # exercise overlap selection.
    return [
        {"start_date": "2022-01-01", "end_date": "2024-12-31",
         "mahadasha": "Kuja", "antardasha": "Guru", "pratyantardasha": "Rahu"},
        {"start_date": "2025-01-01", "end_date": "2026-12-31",
         "mahadasha": "Saturn", "antardasha": "Rahu", "pratyantardasha": "Venus"},
    ]


def _cross_reference():
    return {
        "source": "MANDALI_RESOLVER",
        "displayed_cycles": ["Sade Sati", "Ardha Ashtama Shani", "Ashtama Shani"],
        "matched_rows": 1,
        "resolved_window_count": 2,
        "rows": {
            "2028-01-01": [
                {"cycle": "Ardha Ashtama Shani", "phase": "Ardha Ashtama",
                 "mandali_number": 4, "mandali_name": "Mandali 4 (Mesha)",
                 "entry": "15.06.2028", "exit": "02.11.2028",
                 "status": "UPCOMING", "mechanism": "MANDALI_RESOLVER"},
            ],
        },
    }


def _engine_outputs(dob_dependent_advisory=None, saturn_periods=None,
                    cross_reference=None, timeline=None):
    """Build a representative engine_outputs dict (existing data, unchanged)."""
    return {
        "mandali_advisory": dob_dependent_advisory if dob_dependent_advisory is not None
                            else _advisory(),
        "mandali_gochar_report": {
            "saturn_periods": saturn_periods if saturn_periods is not None
                               else _saturn_periods(),
        },
        "dashas": {"timeline": timeline if timeline is not None else _dasha_timeline()},
        "dasha_saturn_cross_reference": cross_reference if cross_reference is not None
                                        else _cross_reference(),
    }


class TestSaturnLifetimeView(unittest.TestCase):
    def test_exactly_three_cycles_in_order(self):
        view = build_saturn_lifetime_view(_engine_outputs(), dob="1969-09-23")
        keys = [c["key"] for c in view["cycles"]]
        self.assertEqual(keys, ["sade_sati", "ardha_ashtama", "ashtama_shani"])
        titles = [c["title"] for c in view["cycles"]]
        self.assertEqual(titles,
                         ["Sade Sati", "Ardha Ashtama Shani", "Ashtama Shani"])
        # Elinati is never a top-level cycle.
        self.assertNotIn("elinati", keys)

    def test_windows_never_surface_elinati_rows(self):
        view = build_saturn_lifetime_view(_engine_outputs(), dob="1969-09-23")
        all_phases = [
            w["phase"] for c in view["cycles"] for w in c["windows"]
        ]
        self.assertNotIn("Elinati", all_phases)

    def test_md_ad_pd_range_is_selection_window_not_boundary(self):
        view = build_saturn_lifetime_view(_engine_outputs(), dob="1969-09-23")
        self.assertEqual(view["md_ad_pd_range"]["start"], "28.08.1969")
        self.assertEqual(view["md_ad_pd_range"]["end"], "01.06.2069")

    def test_overlapping_window_shows_complete_natural_period(self):
        # Window spans the range start (starts before it, ends inside it): the
        # COMPLETE natural period is shown verbatim — never clipped to the range
        # and never lifted to the DOB.
        advisory = _advisory()
        advisory["sade_sati"]["cycles"][0]["sade_sati_windows"][0] = {
            "phase": "Rising", "rasi": "Dhanus", "mandali": 12,
            "start": "01.01.1960", "end": "01.01.1980",
        }
        view = build_saturn_lifetime_view(
            _engine_outputs(dob_dependent_advisory=advisory), dob="1969-09-23"
        )
        sade_sati = view["cycles"][0]["windows"]
        self.assertEqual(len(sade_sati), 3)
        rising = [w for w in sade_sati if w["phase"] == "Rising"][0]
        self.assertEqual(rising["start"], "01.01.1960")        # natural START
        self.assertEqual(rising["natural_start"], "01.01.1960")
        self.assertEqual(rising["end"], "01.01.1980")          # natural END
        self.assertEqual(rising["natural_end"], "01.01.1980")
        self.assertNotIn("clipped_to_dob", rising)

    def test_window_outside_range_is_dropped(self):
        # Ashtama window 1950-1960 ends before the 1969-08-28 range start -> dropped.
        advisory = _advisory()
        advisory["ashtama_shani"]["cycles"][0]["ashtama_shani_windows"][0] = {
            "phase": "Ashtama", "rasi": "Simha", "mandali": 8,
            "start": "01.01.1950", "end": "01.01.1960",
        }
        view = build_saturn_lifetime_view(
            _engine_outputs(dob_dependent_advisory=advisory), dob="1969-09-23"
        )
        self.assertEqual(view["cycles"][2]["windows"], [])

    def test_window_starting_after_range_is_dropped(self):
        # A future window fully after the range end (2069-06-01) is dropped.
        advisory = _advisory()
        advisory["sade_sati"]["cycles"][0]["sade_sati_windows"].append(
            {"phase": "Rising", "rasi": "Dhanus", "mandali": 12,
             "start": "01.01.2100", "end": "01.01.2102"}
        )
        view = build_saturn_lifetime_view(
            _engine_outputs(dob_dependent_advisory=advisory), dob="1969-09-23"
        )
        starts = [w["start"] for w in view["cycles"][0]["windows"]]
        self.assertNotIn("01.01.2100", starts)

    def test_narrow_range_selects_only_overlapping_windows(self):
        # Timeline 2022-2026: the Rising window (2018-2021) ends before the 2022
        # range start and is dropped; Peak and Setting overlap the range and are
        # kept with their natural dates.
        view = build_saturn_lifetime_view(
            _engine_outputs(timeline=_narrow_timeline()), dob="1969-09-23"
        )
        sade_sati = view["cycles"][0]["windows"]
        self.assertEqual(
            [(w["phase"], w["start"], w["end"]) for w in sade_sati],
            [("Peak", "13.05.2021", "30.10.2023"),
             ("Setting", "30.10.2023", "17.04.2026")],
        )
        self.assertEqual(view["md_ad_pd_range"]["start"], "01.01.2022")
        self.assertEqual(view["md_ad_pd_range"]["end"], "31.12.2026")

    def test_windows_within_range_keep_natural_start_and_end(self):
        view = build_saturn_lifetime_view(_engine_outputs(), dob="1969-09-23")
        for cycle in view["cycles"]:
            for w in cycle["windows"]:
                self.assertEqual(w["start"], w["natural_start"])
                self.assertEqual(w["end"], w["natural_end"])
                self.assertNotIn("clipped_to_dob", w)

    def test_ardha_ashtama_from_resolver_and_mandali_label(self):
        view = build_saturn_lifetime_view(_engine_outputs(), dob="1969-09-23")
        ardha = view["cycles"][1]
        self.assertEqual(len(ardha["windows"]), 1)
        self.assertEqual(ardha["windows"][0]["mandali"], "Mandali 4 (Mesha)")
        self.assertEqual(ardha["windows"][0]["start"], "15.06.2028")
        self.assertEqual(ardha["windows"][0]["end"], "02.11.2028")

    def test_resolver_not_found_rows_never_invent_dates(self):
        view = build_saturn_lifetime_view(_engine_outputs(), dob="1969-09-23")
        # Ashtama resolver row is NOT_FOUND (entry/exit "—") and the advisory
        # ashtama window (2009-2011) is the only Ashtama row surfaced.
        ashtama = view["cycles"][2]
        self.assertEqual(len(ashtama["windows"]), 1)
        self.assertEqual(ashtama["windows"][0]["start"], "16.01.2009")
        self.assertNotIn("—", ashtama["windows"][0]["start"])

    def test_cross_reference_is_read_only_passthrough(self):
        view = build_saturn_lifetime_view(_engine_outputs(), dob="1969-09-23")
        xref = view["cross_reference"]
        self.assertEqual(xref["source"], "MANDALI_RESOLVER")
        self.assertEqual(xref["matched_rows"], 1)
        self.assertEqual(len(xref["rows"]), 1)
        row = xref["rows"][0]
        self.assertEqual(row["start_date"], "2028-01-01")
        self.assertEqual(row["md"], "Saturn")
        self.assertEqual(row["ad"], "Jupiter")
        self.assertEqual(row["pd"], "Mars")
        self.assertEqual(row["saturn_periods"][0]["mechanism"], "MANDALI_RESOLVER")
        self.assertEqual(row["saturn_periods"][0]["cycle"], "Ardha Ashtama Shani")

    def test_sade_sati_displays_governed_mandali_12_1_2(self):
        # Advisory carries internal placeholder mandali (5/6/6); the presentation
        # must surface the governed 12 -> 1 -> 2 for Rising/Peak/Setting.
        view = build_saturn_lifetime_view(_engine_outputs(), dob="1969-09-23")
        sade_sati = view["cycles"][0]["windows"]
        self.assertEqual(
            [(w["phase"], w["mandali"]) for w in sade_sati],
            [("Rising", "12"), ("Peak", "1"), ("Setting", "2")],
        )

    def test_ashtama_displays_governed_mandali_8(self):
        # Advisory carries internal placeholder mandali (3); the presentation
        # must surface the governed Mandali 8 for Ashtama Shani.
        view = build_saturn_lifetime_view(_engine_outputs(), dob="1969-09-23")
        ashtama = view["cycles"][2]["windows"]
        self.assertTrue(all(w["mandali"] == "8" for w in ashtama))

    def test_unrecognized_phase_falls_back_to_advisory_mandali(self):
        # A governed phase not covered by the mapping keeps the advisory value
        # as a fallback (never invents a number).
        advisory = _advisory()
        advisory["sade_sati"]["cycles"][0]["sade_sati_windows"].append(
            {"phase": "Unknown", "rasi": "Meena", "mandali": 7,
             "start": "01.01.2030", "end": "01.01.2032"}
        )
        view = build_saturn_lifetime_view(
            _engine_outputs(dob_dependent_advisory=advisory), dob="1969-09-23"
        )
        sade_sati = view["cycles"][0]["windows"]
        unknown = [w for w in sade_sati if w["phase"] == "Unknown"]
        self.assertEqual(len(unknown), 1)
        self.assertEqual(unknown[0]["mandali"], "7")

    def test_cross_reference_rows_keyed_by_dasha_start_date(self):
        # MD/AD/PD placement requirement: every cross-reference row is keyed by
        # an existing Dasha timeline start_date, and the MD/AD/PD labels shown
        # are exactly the timeline's labels at that date.
        view = build_saturn_lifetime_view(_engine_outputs(), dob="1969-09-23")
        xref = view["cross_reference"]
        timeline_dates = {str(r["start_date"]) for r in _dasha_timeline()}
        for row in xref["rows"]:
            self.assertIn(row["start_date"], timeline_dates)
            by_date = {str(r["start_date"]): r for r in _dasha_timeline()}[row["start_date"]]
            self.assertEqual(row["md"], by_date["mahadasha"])
            self.assertEqual(row["ad"], by_date["antardasha"])
            self.assertEqual(row["pd"], by_date["pratyantardasha"])

    def test_no_engine_output_mutation(self):
        eo = _engine_outputs()
        snapshot = copy.deepcopy(eo)
        build_saturn_lifetime_view(eo, dob="1969-09-23")
        self.assertEqual(eo, snapshot)

    def test_deterministic(self):
        a = build_saturn_lifetime_view(_engine_outputs(), dob="1969-09-23")
        b = build_saturn_lifetime_view(_engine_outputs(), dob="1969-09-23")
        self.assertEqual(a, b)

    def test_dob_accepted_in_both_formats(self):
        iso = build_saturn_lifetime_view(_engine_outputs(), dob="1969-09-23")
        dmy = build_saturn_lifetime_view(_engine_outputs(), dob="23.09.1969")
        self.assertEqual(iso["dob"], "23.09.1969")
        self.assertEqual(dmy["dob"], "23.09.1969")
        self.assertEqual(iso["cycles"], dmy["cycles"])

    def test_empty_inputs_are_graceful(self):
        view = build_saturn_lifetime_view({}, dob="")
        self.assertEqual(len(view["cycles"]), 3)
        for cycle in view["cycles"]:
            self.assertEqual(cycle["windows"], [])
        self.assertEqual(view["cross_reference"]["rows"], [])
        self.assertIsNone(view["md_ad_pd_range"]["start"])
        self.assertIsNone(view["md_ad_pd_range"]["end"])

    def test_report_builder_emits_saturn_lifetime_cycles(self):
        from app.reports.builder import ReportBuilder
        report = ReportBuilder().build_json_report(
            {
                "metadata": {"dob": "14.05.1980", "name": "Test User"},
                "master_probability": {},
                "engine_outputs": _engine_outputs(),
            },
            {},
            questions=[],
        )
        self.assertIn("saturn_lifetime_cycles", report)
        self.assertEqual(report["saturn_lifetime_cycles"]["dob"], "14.05.1980")


if __name__ == "__main__":
    unittest.main()

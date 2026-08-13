"""
Tests for the Present Gochar Rasi-Mandali report (Report B).

Covers:
 - MandaliGocharBuilder output structure (12 Rasi boxes x 9 Nakshatra-Pada slots)
 - Planet placement at the exact Nakshatra-Pada position
 - Report B Mandali-based period rows (entry/exit/next/status/duration)
 - Report A Rasi-based period rows (side-by-side)
 - Saturn special periods resolved through the actual Mandali resolver
   (legacy Rasi-based lifetime windows preserved and labelled)
 - Pipeline / report-layer data flow (engine_outputs["mandali_gochar_report"],
   engine_outputs["mandali"], transit metadata)

Existing engine/golden-master behavior must remain unchanged (regression-free).
"""

import datetime
import unittest

from app.builders.mandali_gochar_builder import MandaliGocharBuilder
from app.engines.canonical_reference_data import (
    get_canonical_reference_data,
    reset_canonical_reference_data,
)
from app.engines.mandali_grid_construction import build_mandali_grid


TARGET = datetime.datetime(2026, 8, 7, 12, 23, 1, tzinfo=datetime.timezone.utc)


class _MockAdapter:
    """Deterministic stand-in for MandaliTransitAdapter (hermetic tests)."""

    def __init__(self):
        self.datetimes = {}
        self.rasi = {}
        self.next_entry = {}
        self.next_exit = {}
        self.transit_pada = {}

    def calculate_transit_datetimes(self, planet, grid, target):
        return self.datetimes.get(planet, (None, None, None))

    def find_rasi_period(self, planet, target):
        return self.rasi.get(planet, (None, None, None, None))

    def find_next_entry(self, planet, grid, target_mandali, from_date):
        return self.next_entry.get((planet, target_mandali))

    def find_next_exit(self, planet, grid, target_mandali, from_date):
        return self.next_exit.get((planet, target_mandali))

    def get_transit_pada(self, planet, date):
        return self.transit_pada.get(planet)


def _rajus_transit():
    """Canonical-format current_transit matching the frozen golden-master chart
    (Raju: Moon Dhanishta P2 = absolute pada 90)."""
    return [
        {"planet": "Sun", "rasi": "Karkata", "nakshatra": "Ashlesha", "pada": 2,
         "start_date": "30.07.2026", "end_date": "30.08.2026", "next_mandali": 8,
         "house_from_moon": 7, "interpretation": "Sun h7"},
        {"planet": "Moon", "rasi": "Vrishabha", "nakshatra": "Krittika", "pada": 4,
         "start_date": "05.08.2026", "end_date": "07.08.2026", "next_mandali": 5,
         "house_from_moon": 5, "interpretation": "Moon h5"},
        {"planet": "Mars", "rasi": "Mithuna", "nakshatra": "Mrigashira", "pada": 3,
         "start_date": "09.07.2026", "end_date": "22.08.2026", "next_mandali": 6,
         "house_from_moon": 6, "interpretation": "Mars h6"},
        {"planet": "Mercury", "rasi": "Karkata", "nakshatra": "Punarvasu", "pada": 4,
         "start_date": "06.06.2026", "end_date": "14.08.2026", "next_mandali": 7,
         "house_from_moon": 7, "interpretation": "Mercury h7"},
        {"planet": "Jupiter", "rasi": "Karkata", "nakshatra": "Pushya", "pada": 4,
         "start_date": "03.08.2026", "end_date": "30.08.2027", "next_mandali": 8,
         "house_from_moon": 7, "interpretation": "Jupiter h7"},
        {"planet": "Venus", "rasi": "Kanya", "nakshatra": "Uttara Phalguni", "pada": 3,
         "start_date": "16.07.2026", "end_date": "14.08.2026", "next_mandali": 9,
         "house_from_moon": 9, "interpretation": "Venus h9"},
        {"planet": "Saturn", "rasi": "Meena", "nakshatra": "Revati", "pada": 2,
         "start_date": "17.04.2026", "end_date": "15.06.2028", "next_mandali": 4,
         "house_from_moon": 3, "interpretation": "Saturn h3"},
        {"planet": "Rahu", "rasi": "Kumbha", "nakshatra": "Dhanishta", "pada": 4,
         "start_date": "20.04.2026", "end_date": "26.10.2027", "next_mandali": 12,
         "house_from_moon": 2, "interpretation": "Rahu h2"},
        {"planet": "Ketu", "rasi": "Simha", "nakshatra": "Magha", "pada": 2,
         "start_date": "20.04.2026", "end_date": "26.10.2027", "next_mandali": 6,
         "house_from_moon": 8, "interpretation": "Ketu h8"},
    ]


class TestMandaliGocharReport(unittest.TestCase):
    def setUp(self):
        reset_canonical_reference_data()
        self.ref_data = get_canonical_reference_data()
        self.grid = build_mandali_grid("Dhanishta", 2)
        self.adapter = _MockAdapter()
        self.builder = MandaliGocharBuilder(self.ref_data, self.adapter)

    def tearDown(self):
        reset_canonical_reference_data()

    # ------------------------------------------------------------------
    # Chart — 12 Rasi boxes, 9 Nakshatra-Pada positions each
    # ------------------------------------------------------------------

    def test_chart_has_12_boxes_and_108_padas(self):
        report = self.builder.build(
            current_transit=_rajus_transit(),
            mandali_grid=self.grid,
            target_date_utc=TARGET,
        )
        self.assertEqual(len(report.chart), 12)
        total = 0
        for cell in report.chart:
            self.assertEqual(len(cell.padas), 9)
            total += len(cell.padas)
            # Each pada slot carries its nakshatra + pada number
            for slot in cell.padas:
                self.assertTrue(slot.nakshatra)
                self.assertIn(slot.pada, (1, 2, 3, 4))
        self.assertEqual(total, 108)

    def test_chart_planet_placed_at_exact_pada(self):
        report = self.builder.build(
            current_transit=_rajus_transit(),
            mandali_grid=self.grid,
            target_date_utc=TARGET,
        )
        # Golden-master abs padas: Sun Ashlesha P2 = 34 (Mandali 7, slot 3),
        # Saturn Revati P2 = 106 (Mandali 3, slot 3), Rahu Dhanishta P4 = 92
        # (Mandali 1, slot 7), Moon Krittika P4 = 12 (Mandali 4, slot 8).
        expected = {
            "SU": (7, 34, 3),
            "SA": (3, 106, 3),
            "RA": (1, 92, 7),
            "MO": (4, 12, 8),
        }
        for code, (mandali_number, absolute_pada, position) in expected.items():
            cell = next(c for c in report.chart if c.mandali_number == mandali_number)
            slot = next(s for s in cell.padas if s.absolute_pada == absolute_pada)
            self.assertIn(code, slot.planets)
            self.assertEqual(slot.position, position)

    def test_chart_person_specific_moon_center(self):
        """Mandali 1 box reflects the natal Moon's Rasi (person-specific)."""
        report = self.builder.build(
            current_transit=_rajus_transit(),
            mandali_grid=self.grid,
            target_date_utc=TARGET,
        )
        self.assertEqual(report.reference_moon["rasi"], "Makara")
        self.assertEqual(report.reference_moon["nakshatra"], "Dhanishta")
        self.assertEqual(report.reference_moon["pada"], 2)
        self.assertEqual(report.reference_moon["absolute_pada"], 90)
        self.assertEqual(report.chart[0].rasi, "Makara")

    # ------------------------------------------------------------------
    # R2 — Fixed universal Rasi -> Nakshatra-Pada reference
    # ------------------------------------------------------------------

    def test_fixed_rasi_map_covers_108_padas_in_sequence_order(self):
        report = self.builder.build(
            current_transit=_rajus_transit(),
            mandali_grid=self.grid,
            target_date_utc=TARGET,
        )
        expected_sequence = [
            "Mesha", "Vrishabha", "Mithuna", "Karkata", "Simha", "Kanya",
            "Tula", "Vrishchika", "Dhanus", "Makara", "Kumbha", "Meena",
        ]
        self.assertEqual(list(report.fixed_rasi_map.keys()), expected_sequence)
        total = 0
        for rasi, entry in report.fixed_rasi_map.items():
            self.assertEqual(entry["pada_count"], 9, rasi)
            self.assertEqual(len(entry["absolute_padas"]), 9, rasi)
            total += entry["pada_count"]
        self.assertEqual(total, 108)

    def test_fixed_rasi_map_authoritative_kumbha_meena_boundary(self):
        """Registry truth: Purva Bhadrapada P1-P3 -> Kumbha, P4 -> Meena.

        The universal reference must match the authoritative registry exactly
        (this is the boundary that a previous self-check doc got wrong)."""
        report = self.builder.build(
            current_transit=_rajus_transit(),
            mandali_grid=self.grid,
            target_date_utc=TARGET,
        )
        kumbha_bands = report.fixed_rasi_map["Kumbha"]["nakshatra_padas"]
        meena_bands = report.fixed_rasi_map["Meena"]["nakshatra_padas"]

        purva_kumbha = next(b for b in kumbha_bands if b["nakshatra"] == "Purva Bhadrapada")
        self.assertEqual((purva_kumbha["pada_from"], purva_kumbha["pada_to"]), (1, 3))
        self.assertEqual(purva_kumbha["display"], "P1-P3")

        purva_meena = next(b for b in meena_bands if b["nakshatra"] == "Purva Bhadrapada")
        self.assertEqual((purva_meena["pada_from"], purva_meena["pada_to"]), (4, 4))
        self.assertEqual(purva_meena["display"], "P4")

    def test_fixed_rasi_map_matches_registry_get_rasi(self):
        """Every absolute pada in the map must equal get_rasi() from the registry."""
        report = self.builder.build(
            current_transit=_rajus_transit(),
            mandali_grid=self.grid,
            target_date_utc=TARGET,
        )
        for absolute_pada in range(1, 109):
            nakshatra, pada = self.ref_data.get_nakshatra_pada(absolute_pada)
            expected_rasi = self.ref_data.get_rasi(nakshatra, pada)
            owner_rasi = next(
                r for r, entry in report.fixed_rasi_map.items()
                if absolute_pada in entry["absolute_padas"]
            )
            self.assertEqual(owner_rasi, expected_rasi, absolute_pada)

    def test_fixed_rasi_map_deterministic(self):
        r1 = self.builder.build(
            current_transit=_rajus_transit(), mandali_grid=self.grid,
            target_date_utc=TARGET,
        ).fixed_rasi_map
        r2 = self.builder.build(
            current_transit=_rajus_transit(), mandali_grid=self.grid,
            target_date_utc=TARGET,
        ).fixed_rasi_map
        self.assertEqual(r1, r2)

    # ------------------------------------------------------------------
    # Report B — Mandali-based period rows
    # ------------------------------------------------------------------

    def test_mandali_period_row(self):
        report = self.builder.build(
            current_transit=_rajus_transit(),
            mandali_grid=self.grid,
            target_date_utc=TARGET,
        )
        saturn = next(p for p in report.periods if p.planet == "Saturn")
        self.assertEqual(saturn.mandali_number, 3)
        self.assertEqual(saturn.mandali_name, "Mandali 3 (Meena)")
        self.assertEqual(saturn.current_rasi, "Meena")
        self.assertEqual(saturn.nakshatra, "Revati")
        self.assertEqual(saturn.pada, 2)
        self.assertEqual(saturn.entry_date, "17.04.2026")
        self.assertEqual(saturn.exit_date, "15.06.2028")
        self.assertEqual(saturn.next_mandali.number, 4)
        self.assertEqual(saturn.status, "IN_PROGRESS")
        self.assertEqual(saturn.mandali_status, "FAVORABLE")

    def test_mandali_period_datetime_precision(self):
        """Entry/exit datetimes come from the ephemeris adapter when available."""
        entry = datetime.datetime(2026, 4, 17, 3, 15, 0, tzinfo=datetime.timezone.utc)
        exit_ = datetime.datetime(2028, 6, 15, 11, 30, 0, tzinfo=datetime.timezone.utc)
        self.adapter.datetimes["saturn"] = (entry, exit_, 4)
        report = self.builder.build(
            current_transit=_rajus_transit(),
            mandali_grid=self.grid,
            target_date_utc=TARGET,
        )
        saturn = next(p for p in report.periods if p.planet == "Saturn")
        self.assertEqual(saturn.entry_datetime, "2026-04-17T03:15:00+00:00")
        self.assertEqual(saturn.exit_datetime, "2028-06-15T11:30:00+00:00")

    def test_mandali_period_status_upcoming_and_completed(self):
        past = datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc)
        future = datetime.datetime(2030, 1, 1, tzinfo=datetime.timezone.utc)
        report_past = self.builder.build(
            current_transit=_rajus_transit(), mandali_grid=self.grid,
            target_date_utc=past,
        )
        saturn_past = next(p for p in report_past.periods if p.planet == "Saturn")
        # 2020 is before entry 17.04.2026 for the SAME current arc -> the grid
        # arc is defined by the current_transit dates, so status uses those dates.
        self.assertEqual(saturn_past.status, "UPCOMING")

        report_future = self.builder.build(
            current_transit=_rajus_transit(), mandali_grid=self.grid,
            target_date_utc=future,
        )
        saturn_future = next(p for p in report_future.periods if p.planet == "Saturn")
        self.assertEqual(saturn_future.status, "COMPLETED")

    # ------------------------------------------------------------------
    # Report A — Rasi-based period rows
    # ------------------------------------------------------------------

    def test_rasi_period_row(self):
        entry = datetime.datetime(2025, 3, 29, 0, 0, 0)
        exit_ = datetime.datetime(2027, 6, 2, 0, 0, 0)
        self.adapter.rasi["saturn"] = (entry, exit_, 0, 11)  # next Mesha(0)
        report = self.builder.build(
            current_transit=_rajus_transit(),
            mandali_grid=self.grid,
            target_date_utc=TARGET,
        )
        a = report.comparison["report_a"]
        saturn = next(r for r in a if r["planet"] == "Saturn")
        self.assertEqual(saturn["current_rasi"], "Meena")
        self.assertEqual(saturn["rasi_number"], 12)
        self.assertEqual(saturn["rasi_entry"], "29.03.2025")
        self.assertEqual(saturn["rasi_exit"], "02.06.2027")
        self.assertEqual(saturn["next_rasi"], "Mesha")
        self.assertEqual(saturn["status"], "IN_PROGRESS")

    def test_comparison_report_a_and_b_aligned(self):
        report = self.builder.build(
            current_transit=_rajus_transit(),
            mandali_grid=self.grid,
            target_date_utc=TARGET,
        )
        self.assertEqual(len(report.comparison["report_a"]), len(report.periods))
        self.assertEqual(len(report.comparison["report_b"]), len(report.periods))
        self.assertTrue(report.comparison["note"])

    # ------------------------------------------------------------------
    # Saturn special periods — actual Mandali resolver + preserved legacy
    # ------------------------------------------------------------------

    def test_saturn_periods_present_with_mech_label(self):
        self.adapter.next_entry[("saturn", 4)] = datetime.datetime(
            2028, 6, 15, 0, 0, 0, tzinfo=datetime.timezone.utc
        )
        self.adapter.next_exit[("saturn", 4)] = (
            datetime.datetime(2028, 11, 2, 0, 0, 0, tzinfo=datetime.timezone.utc),
            3,
        )
        self.adapter.transit_pada["saturn"] = ("Bharani", 1)

        advisory = {
            "sade_sati": {"cycles": [], "birth_detection": {}},
            "elinati_shani": {"cycles": []},
            "ashtama_shani": {"cycles": []},
        }
        report = self.builder.build(
            current_transit=_rajus_transit(),
            mandali_grid=self.grid,
            target_date_utc=TARGET,
            advisory=advisory,
        )
        sp = report.saturn_periods

        # Saturn is in Mandali 3 -> Sade Sati not active.
        self.assertFalse(sp.sade_sati.current)
        # Ardha Ashtama (4th from Moon) is the next Saturn window -> upcoming.
        self.assertTrue(sp.ardha_ashtama.upcoming)
        ardha = sp.ardha_ashtama.upcoming[0]
        self.assertEqual(ardha.phase, "Ardha Ashtama")
        self.assertEqual(ardha.mandali_number, 4)
        self.assertEqual(ardha.entry, "15.06.2028")
        self.assertEqual(ardha.status, "UPCOMING")
        self.assertEqual(ardha.mechanism, "MANDALI_RESOLVER")

        # Ashtama + Elinati both resolve to the 8th from Moon (Mandali 8).
        for group in (sp.ashtama, sp.elinati):
            self.assertTrue(any(r.mandali_number == 8 for r in group.upcoming))

        # Legacy Rasi-based lifetime windows preserved and clearly labelled.
        self.assertEqual(
            sp.legacy_windows["mechanism"],
            "RASI_BASED_LIFETIME_WINDOWS_LCP07_09_PRESERVED",
        )
        self.assertEqual(sp.legacy_windows["sade_sati"], advisory["sade_sati"])

    def test_saturn_aktive_window_uses_current_transit(self):
        """When Saturn currently occupies the target Mandali, the window is ACTIVE
        with the current transit entry/exit."""
        transit = _rajus_transit()
        # Move Saturn into Mandali 8 (Simha): Purva Phalguni P1 = abs 41.
        for tp in transit:
            if tp["planet"] == "Saturn":
                tp["rasi"] = "Simha"
                tp["nakshatra"] = "Purva Phalguni"
                tp["pada"] = 1
                tp["start_date"] = "01.01.2026"
                tp["end_date"] = "01.01.2028"
                tp["next_mandali"] = 9
        report = self.builder.build(
            current_transit=transit,
            mandali_grid=self.grid,
            target_date_utc=TARGET,
        )
        sp = report.saturn_periods
        self.assertTrue(sp.ashtama.current)
        self.assertTrue(sp.elinati.current)
        self.assertEqual(sp.ashtama.current[0].status, "ACTIVE")
        self.assertEqual(sp.ashtama.current[0].entry, "01.01.2026")

    # ------------------------------------------------------------------
    # Pipeline / report-layer data flow (regression + integration)
    # ------------------------------------------------------------------

    def test_pipeline_emits_gochar_report_and_mandali_block(self):
        import json
        import swisseph as swe
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        from app.pipeline_runner import PipelineRunner
        from app.reports.builder import ReportBuilder

        canonical = json.load(
            open("D:/vedic-ai-golden-master/extracted_json/raju_canonical_content.json", encoding="utf-8")
        )
        machine = json.load(
            open("D:/vedic-ai-golden-master/extracted_json/raju_machine_index.json", encoding="utf-8")
        )
        runner = PipelineRunner()
        out = runner.process(
            {"canonical_content": canonical, "_machine_index": machine},
            target_date_utc=TARGET,
        )
        eo = out["engine_outputs"]

        # New Rasi-Mandali Gochar report is present and structurally sound.
        mgr = eo["mandali_gochar_report"]
        self.assertEqual(mgr["schema_version"], "1.0")
        self.assertEqual(len(mgr["chart"]), 12)
        self.assertEqual(len(mgr["periods"]), 9)
        # Chart carries the frozen golden-master placements.
        sun_cell = next(c for c in mgr["chart"] if c["mandali_number"] == 7)
        sun_slot = next(s for s in sun_cell["padas"] if s["absolute_pada"] == 34)
        self.assertIn("SU", sun_slot["planets"])

        # Repaired data flow for the existing report layer.
        self.assertIn("transit_houses", eo["mandali"])
        self.assertEqual(eo["mandali"]["transit_houses"]["saturn"], 3)
        self.assertEqual(eo["mandali"]["sade_sati_status"], "Not Active")
        self.assertEqual(eo["transit"]["metadata"]["target_date"], TARGET.strftime('%Y-%m-%d'))
        self.assertIn("saturn", eo["transit"]["activated_planets"])

        # Report-level JSON carries both Report A and Report B.
        report = ReportBuilder().build_json_report(out, machine, questions=[])
        self.assertIn("mandali_gochar_report", report)
        self.assertIn("gochara_report", report)
        self.assertEqual(report["gochara_report"]["transit_strength"], out.get("engine_outputs", {}).get("transit", {}).get("activation_score"))
        mandali_block = report["gochara_report"]["mandali"]
        self.assertEqual(mandali_block["mandali_number"], 3)
        self.assertTrue(mandali_block["activated_planets"])

        # Phase 3D — MD/AD/PD ↔ Saturn cross-reference is emitted backend-side.
        xref = eo["dasha_saturn_cross_reference"]
        self.assertEqual(xref["source"], "MANDALI_RESOLVER")
        self.assertEqual(xref["displayed_cycles"],
                         ["Sade Sati", "Ardha Ashtama Shani", "Ashtama Shani"])
        # Every surfaced badge originates from the Mandali resolver only.
        for _start, badges in xref["rows"].items():
            for b in badges:
                self.assertEqual(b["mechanism"], "MANDALI_RESOLVER")
                self.assertNotEqual(b["cycle"], "Elinati")
        # Lifetime timeline rows carry the same backend-derived badges.
        for trow in report["lifetime_intelligence"]["timeline"]:
            self.assertIn("saturn_periods", trow)
            for b in trow["saturn_periods"]:
                self.assertEqual(b["mechanism"], "MANDALI_RESOLVER")


if __name__ == "__main__":
    unittest.main()
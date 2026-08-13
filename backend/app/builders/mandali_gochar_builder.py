"""
MandaliGocharBuilder — Present Gochar Rasi-Mandali report (Report B)
====================================================================

Composes the Rasi-Mandali Gochar output that sits ALONGSIDE the existing
regular Rasi-based gochar — both are preserved for side-by-side comparison.

Ownership (One formula / One owner):
 - Longitude -> (Nakshatra, Pada)  : EphemerisService + MandaliGenerator.get_absolute_pada
                                      + CanonicalReferenceData (all existing owners).
 - Longitude -> Mandali            : MandaliGrid construction/resolution (existing owners).
 - Mandali period dates            : MandaliTransitAdapter (existing owner; ephemeris
                                      boundary-crossing scans).
 - Rasi period dates               : MandaliTransitAdapter.find_rasi_period (added to the
                                      existing adapter — same ephemeris architecture).
 - Saturn special periods          : resolved through the ACTUAL Mandali resolver
                                      (this module) — the legacy Rasi-based lifetime
                                      windows are preserved verbatim and clearly labelled.

This module performs NO astronomy itself. All astronomical inputs are obtained
through the injected adapter (ephemeris) and registry data.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.engines.canonical_reference_data import CanonicalReferenceData
from app.engines.mandali_transit_adapter import MandaliTransitAdapter
from app.engines.mandali_grid_construction import MandaliGrid, Mandali
from app.schemas.mandali_gochar import (
    MandaliGocharReport,
    MandaliGocharCell,
    MandaliPadaSlot,
    MandaliPeriodEntry,
    NextMandaliRef,
    RasiGocharEntry,
    SaturnMandaliPeriod,
    SaturnPeriods,
    SaturnPeriodGroup,
)

# Canonical transit planet display order (Sun -> Ketu).
PLANET_ORDER = ["sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn", "rahu", "ketu"]

_UNRESOLVED = "—"


class MandaliGocharBuilder:
    """Builds the Present Gochar Rasi-Mandali report from existing engine data."""

    def __init__(
        self,
        ref_data: CanonicalReferenceData,
        adapter: MandaliTransitAdapter,
    ):
        self._ref_data = ref_data
        self._adapter = adapter

    # -------------------------------------------------------------------------
    # Public entry point
    # -------------------------------------------------------------------------

    def build(
        self,
        current_transit: List[Dict[str, Any]],
        mandali_grid: MandaliGrid,
        target_date_utc: datetime,
        advisory: Optional[Dict[str, Any]] = None,
    ) -> MandaliGocharReport:
        """
        Build the full Rasi-Mandali Gochar report.

        Args:
            current_transit: Canonical-format transit list from the existing
                MandaliTransitAdapter (or Canonical JSON). Each entry:
                {planet, rasi, nakshatra, pada, start_date, end_date,
                 next_mandali, house_from_moon, interpretation}.
            mandali_grid: Moon-centered MandaliGrid (existing owner).
            target_date_utc: Consultation target datetime (UTC).
            advisory: Optional mandali_advisory dict (UniversalMandaliEngine
                output) whose legacy Rasi-based Saturn windows are preserved
                verbatim and labelled.
        """
        target = target_date_utc if target_date_utc else datetime.now(timezone.utc)

        reference_moon = {
            "rasi": mandali_grid.moon_rasi,
            "nakshatra": mandali_grid.moon_nakshatra,
            "pada": mandali_grid.moon_pada,
            "absolute_pada": mandali_grid.moon_absolute_pada,
        }

        chart = self._build_chart(current_transit, mandali_grid)

        period_rows = []
        rasi_rows = []
        for planet_key in PLANET_ORDER:
            tp = self._find_transit(current_transit, planet_key)
            if not tp:
                continue
            period_rows.append(self._build_mandali_period(tp, mandali_grid, target))
            rasi_rows.append(self._build_rasi_period(tp, target))

        saturn_periods = self._build_saturn_periods(
            current_transit, mandali_grid, target, advisory
        )

        comparison = {
            "note": (
                "Report A is the regular Rasi-based gochar (Rasi boundaries). "
                "Report B is the Moon-centered Rasi-Mandali gochar (9-pada Mandali "
                "arc boundaries). Both are produced by the same ephemeris architecture "
                "and are intentionally kept separate for R&D and validation comparison."
            ),
            "report_a": [asdict(r) for r in rasi_rows],
            "report_b": [asdict(r) for r in period_rows],
        }

        return MandaliGocharReport(
            schema_version="1.0",
            # Day-granularity serialization matching the pipeline convention
            # (DashaEngine writes target_date as %Y-%m-%d) — keeps engine_outputs
            # free of wall-clock microsecond timestamps so identical input
            # produces identical output.
            target_date=target.strftime('%Y-%m-%d'),
            reference_moon=reference_moon,
            chart=chart,
            periods=period_rows,
            saturn_periods=saturn_periods,
            comparison=comparison,
        )

    # -------------------------------------------------------------------------
    # Chart — 12 Rasi-Mandali boxes, 9 Nakshatra-Pada positions each
    # -------------------------------------------------------------------------

    def _build_chart(
        self,
        current_transit: List[Dict[str, Any]],
        mandali_grid: MandaliGrid,
    ) -> List[MandaliGocharCell]:
        cells: List[MandaliGocharCell] = []
        for mandali in mandali_grid.mandalis:
            slots: List[MandaliPadaSlot] = []
            for position, pada_detail in enumerate(mandali.pada_details, start=1):
                slots.append(
                    MandaliPadaSlot(
                        position=position,
                        absolute_pada=pada_detail.absolute_pada,
                        nakshatra=pada_detail.nakshatra,
                        pada=pada_detail.pada,
                        planets=[],
                    )
                )
            cells.append(
                MandaliGocharCell(
                    mandali_number=mandali.number,
                    mandali_name=f"Mandali {mandali.number} ({mandali.rasi_name})",
                    rasi=mandali.rasi_name,
                    center_pada=mandali.center_pada,
                    padas=slots,
                )
            )

        # Place each transit planet at its exact Nakshatra-Pada position.
        for tp in current_transit:
            try:
                absolute_pada = self._ref_data.get_absolute_pada(
                    tp["nakshatra"], tp["pada"]
                )
                mandali_number = mandali_grid.find_mandali_for_pada(absolute_pada)
            except Exception:
                continue
            cell = next(
                (c for c in cells if c.mandali_number == mandali_number), None
            )
            if not cell:
                continue
            slot = next(
                (s for s in cell.padas if s.absolute_pada == absolute_pada), None
            )
            if not slot:
                continue
            code = self._short_code(tp["planet"])
            updated_slots = [
                MandaliPadaSlot(
                    position=s.position,
                    absolute_pada=s.absolute_pada,
                    nakshatra=s.nakshatra,
                    pada=s.pada,
                    planets=s.planets + [code] if s is slot else list(s.planets),
                )
                for s in cell.padas
            ]
            cells = [
                MandaliGocharCell(
                    mandali_number=c.mandali_number,
                    mandali_name=c.mandali_name,
                    rasi=c.rasi,
                    center_pada=c.center_pada,
                    padas=updated_slots if c.mandali_number == mandali_number else c.padas,
                )
                if c.mandali_number == mandali_number
                else c
                for c in cells
            ]

        return cells

    # -------------------------------------------------------------------------
    # Report B — Mandali-based period rows
    # -------------------------------------------------------------------------

    def _build_mandali_period(
        self,
        tp: Dict[str, Any],
        mandali_grid: MandaliGrid,
        target: datetime,
    ) -> MandaliPeriodEntry:
        planet_key = tp["planet"]
        rasi = tp.get("rasi", "")
        rasi_number = self._rasi_number(rasi)

        nakshatra = tp.get("nakshatra", "")
        pada = int(tp.get("pada", 0) or 0)

        mandali_number, mandali = self._resolve_mandali(
            nakshatra, pada, mandali_grid
        )

        entry_dt, exit_dt, next_mandali_num = None, None, None
        try:
            entry_dt, exit_dt, next_mandali_num = self._adapter.calculate_transit_datetimes(
                planet_key.lower(), mandali_grid, target
            )
        except Exception:
            pass

        entry_date = tp.get("start_date") or self._fmt_date(entry_dt)
        exit_date = tp.get("end_date") or self._fmt_date(exit_dt)
        if next_mandali_num is None:
            next_mandali_num = tp.get("next_mandali") or ((mandali_number % 12) + 1)

        entry_dt, exit_dt = self._normalize_pair(entry_dt, exit_dt)
        status = self._period_status(target, entry_dt, exit_dt, entry_date, exit_date)
        duration_days = self._duration_days(entry_dt, exit_dt, entry_date, exit_date)
        days_remaining = self._days_remaining(target, exit_dt, exit_date)

        return MandaliPeriodEntry(
            planet=planet_key,
            current_rasi=rasi,
            rasi_number=rasi_number,
            nakshatra=nakshatra,
            pada=pada,
            mandali_number=mandali_number,
            mandali_name=self._mandali_name(mandali_number, mandali),
            entry_date=entry_date,
            entry_datetime=entry_dt.isoformat() if entry_dt else "",
            exit_date=exit_date,
            exit_datetime=exit_dt.isoformat() if exit_dt else "",
            next_mandali=self._next_mandali_ref(next_mandali_num, mandali_grid),
            status=status,
            duration_days=duration_days,
            days_remaining=days_remaining,
            mandali_status=self._mandali_status(mandali_number),
        )

    # -------------------------------------------------------------------------
    # Report A — regular Rasi-based period rows
    # -------------------------------------------------------------------------

    def _build_rasi_period(
        self,
        tp: Dict[str, Any],
        target: datetime,
    ) -> RasiGocharEntry:
        planet_key = tp["planet"]
        rasi = tp.get("rasi", "")
        rasi_number = self._rasi_number(rasi)

        entry_dt, exit_dt, next_rasi, _ = None, None, None, None
        try:
            entry_dt, exit_dt, next_rasi, _ = self._adapter.find_rasi_period(
                planet_key.lower(), target
            )
        except Exception:
            pass

        entry_date = self._fmt_date(entry_dt)
        exit_date = self._fmt_date(exit_dt)
        next_rasi_name = self._rasi_name(next_rasi)

        entry_dt, exit_dt = self._normalize_pair(entry_dt, exit_dt)
        status = self._period_status(target, entry_dt, exit_dt, entry_date, exit_date)
        duration_days = self._duration_days(entry_dt, exit_dt, entry_date, exit_date)
        days_remaining = self._days_remaining(target, exit_dt, exit_date)

        return RasiGocharEntry(
            planet=planet_key,
            current_rasi=rasi,
            rasi_number=rasi_number,
            rasi_entry=entry_date,
            rasi_exit=exit_date,
            next_rasi=next_rasi_name,
            status=status,
            duration_days=duration_days,
            days_remaining=days_remaining,
        )

    # -------------------------------------------------------------------------
    # Saturn special periods — resolved through the actual Mandali grid
    # -------------------------------------------------------------------------

    def _build_saturn_periods(
        self,
        current_transit: List[Dict[str, Any]],
        mandali_grid: MandaliGrid,
        target: datetime,
        advisory: Optional[Dict[str, Any]],
    ) -> SaturnPeriods:
        saturn = self._find_transit(current_transit, "saturn")
        current_saturn = {}
        if saturn:
            nakshatra = saturn.get("nakshatra", "")
            pada = int(saturn.get("pada", 0) or 0)
            saturn_mandali, saturn_mandali_obj = self._resolve_mandali(
                nakshatra, pada, mandali_grid
            )
            active_flags = []
            if saturn_mandali in (12, 1, 2):
                phase = {12: "Rising", 1: "Peak", 2: "Setting"}[saturn_mandali]
                active_flags.append(f"Sade Sati ({phase} phase)")
            if saturn_mandali == 4:
                active_flags.append("Ardha Ashtama (4th from Moon)")
            if saturn_mandali == 8:
                active_flags.append("Ashtama / Elinati (8th from Moon)")
            current_saturn = {
                "planet": "Saturn",
                "mandali_number": saturn_mandali,
                "mandali_name": self._mandali_name(saturn_mandali, saturn_mandali_obj),
                "rasi": saturn_mandali_obj.rasi_name,
                "nakshatra": nakshatra,
                "pada": pada,
                "entry_date": saturn.get("start_date", _UNRESOLVED),
                "exit_date": saturn.get("end_date", _UNRESOLVED),
                "next_mandali": saturn.get("next_mandali"),
                "active_flags": active_flags,
            }
        else:
            saturn_mandali = None
            saturn_mandali_obj = None

        # (phase, target_mandali) per cycle. Elinati and Ashtama both resolve to
        # the 8th from Moon per the repository's LCP-08/LCP-09 definition.
        sade_sati_targets = [(12, "Rising"), (1, "Peak"), (2, "Setting")]

        sade_sati = SaturnPeriodGroup(
            current=[], upcoming=[]
        )
        for target_slot, phase in sade_sati_targets:
            row = self._saturn_window_row(
                "Sade Sati", phase, target_slot, saturn_mandali,
                current_transit, mandali_grid, target,
            )
            self._add_window_row(sade_sati, row)

        ardha = SaturnPeriodGroup(
            current=[], upcoming=[]
        )
        self._add_window_row(
            ardha,
            self._saturn_window_row(
                "Ardha Ashtama", "Ardha Ashtama", 4, saturn_mandali,
                current_transit, mandali_grid, target,
            ),
        )

        ashtama = SaturnPeriodGroup(current=[], upcoming=[])
        self._add_window_row(
            ashtama,
            self._saturn_window_row(
                "Ashtama", "Ashtama", 8, saturn_mandali,
                current_transit, mandali_grid, target,
            ),
        )

        elinati = SaturnPeriodGroup(current=[], upcoming=[])
        self._add_window_row(
            elinati,
            self._saturn_window_row(
                "Elinati", "Elinati", 8, saturn_mandali,
                current_transit, mandali_grid, target,
            ),
        )

        legacy_windows = {}
        if advisory:
            legacy_windows = {
                "mechanism": "RASI_BASED_LIFETIME_WINDOWS_LCP07_09_PRESERVED",
                "sade_sati": advisory.get("sade_sati"),
                "elinati_shani": advisory.get("elinati_shani"),
                "ashtama_shani": advisory.get("ashtama_shani"),
            }

        return SaturnPeriods(
            sade_sati=sade_sati,
            ardha_ashtama=ardha,
            ashtama=ashtama,
            elinati=elinati,
            current_saturn=current_saturn,
            legacy_windows=legacy_windows,
        )

    def _saturn_window_row(
        self,
        cycle: str,
        phase: str,
        target_mandali_no: int,
        saturn_mandali: Optional[int],
        current_transit: List[Dict[str, Any]],
        mandali_grid: MandaliGrid,
        target: datetime,
    ) -> SaturnMandaliPeriod:
        mandali = mandali_grid.get_mandali(target_mandali_no)

        if saturn_mandali == target_mandali_no:
            saturn = self._find_transit(current_transit, "saturn") or {}
            entry = saturn.get("start_date", _UNRESOLVED)
            exit_ = saturn.get("end_date", _UNRESOLVED)
            next_mandali = saturn.get("next_mandali")
            nakshatra = saturn.get("nakshatra", "")
            pada = int(saturn.get("pada", 0) or 0)
            return SaturnMandaliPeriod(
                cycle=cycle,
                phase=phase,
                rasi=mandali.rasi_name,
                mandali_number=target_mandali_no,
                mandali_name=self._mandali_name(target_mandali_no, mandali),
                nakshatra=nakshatra,
                pada=pada,
                entry=entry,
                exit=exit_,
                next_mandali=next_mandali,
                status="ACTIVE",
                mechanism="MANDALI_RESOLVER",
            )

        entry_dt = None
        exit_dt = None
        next_mandali = None
        nakshatra = ""
        pada = 0
        status = "UPCOMING"
        try:
            entry_dt = self._adapter.find_next_entry(
                "saturn", mandali_grid, target_mandali_no, target
            )
            if entry_dt is not None:
                exit_dt, next_mandali = self._adapter.find_next_exit(
                    "saturn", mandali_grid, target_mandali_no, entry_dt
                )
                pada_info = self._adapter.get_transit_pada("saturn", entry_dt)
                if pada_info:
                    nakshatra, pada = pada_info
            else:
                status = "NOT_FOUND"
        except Exception:
            status = "NOT_FOUND"

        return SaturnMandaliPeriod(
            cycle=cycle,
            phase=phase,
            rasi=mandali.rasi_name,
            mandali_number=target_mandali_no,
            mandali_name=self._mandali_name(target_mandali_no, mandali),
            nakshatra=nakshatra,
            pada=pada,
            entry=self._fmt_date(entry_dt) if entry_dt else _UNRESOLVED,
            exit=self._fmt_date(exit_dt) if exit_dt else _UNRESOLVED,
            next_mandali=next_mandali,
            status=status,
            mechanism="MANDALI_RESOLVER",
        )

    @staticmethod
    def _add_window_row(group: SaturnPeriodGroup, row: SaturnMandaliPeriod) -> None:
        if row.status == "ACTIVE":
            group.current.append(row)
        else:
            group.upcoming.append(row)

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _find_transit(
        self, current_transit: List[Dict[str, Any]], planet_key: str
    ) -> Optional[Dict[str, Any]]:
        lower = planet_key.lower()
        for tp in current_transit:
            if str(tp.get("planet", "")).lower() == lower:
                return tp
        return None

    def _resolve_mandali(
        self, nakshatra: str, pada: int, mandali_grid: MandaliGrid
    ) -> tuple:
        try:
            absolute_pada = self._ref_data.get_absolute_pada(nakshatra, pada)
            number = mandali_grid.find_mandali_for_pada(absolute_pada)
            mandali = mandali_grid.get_mandali(number)
            return number, mandali
        except Exception:
            return 1, mandali_grid.get_mandali(1)

    @staticmethod
    def _mandali_name(number: int, mandali) -> str:
        """Display name of a Mandali, e.g. 'Mandali 3 (Meena)'."""
        rasi = getattr(mandali, "rasi_name", "")
        return f"Mandali {number} ({rasi})" if rasi else f"Mandali {number}"

    def _rasi_number(self, rasi: str) -> int:
        idx = self._rasi_index(rasi)
        return idx + 1 if idx is not None else 0

    def _rasi_index(self, rasi: str) -> Optional[int]:
        if not rasi:
            return None
        sequence = self._ref_data.get_rasi_sequence()
        lower = rasi.strip().lower()
        for i, name in enumerate(sequence):
            if name.lower() == lower:
                return i
        return None

    def _rasi_name(self, rasi_index: Optional[int]) -> str:
        if rasi_index is None:
            return _UNRESOLVED
        sequence = self._ref_data.get_rasi_sequence()
        return sequence[rasi_index % 12]

    def _next_mandali_ref(self, number: int, mandali_grid: MandaliGrid) -> NextMandaliRef:
        try:
            mandali = mandali_grid.get_mandali(number)
            return NextMandaliRef(number=number, name=self._mandali_name(number, mandali))
        except Exception:
            return NextMandaliRef(number=number, name=f"Mandali {number}")

    def _mandali_status(self, number: int) -> str:
        if number <= 4:
            return "FAVORABLE"
        if number <= 8:
            return "NEUTRAL"
        return "CHALLENGING"

    @staticmethod
    def _short_code(planet: str) -> str:
        return str(planet)[:2].upper()

    @staticmethod
    def _fmt_date(dt: Optional[datetime]) -> str:
        if dt is None:
            return _UNRESOLVED
        return dt.strftime("%d.%m.%Y")

    @staticmethod
    def _parse_date(date_str: Optional[str]) -> Optional[datetime]:
        if not date_str or date_str == _UNRESOLVED:
            return None
        try:
            return datetime.strptime(date_str, "%d.%m.%Y")
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _normalize_pair(
        entry_dt: Optional[datetime], exit_dt: Optional[datetime]
    ) -> tuple:
        """Return a (entry_dt, exit_dt) pair with matching tz-awareness."""
        if entry_dt is None or exit_dt is None:
            return entry_dt, exit_dt
        if (entry_dt.tzinfo is None) != (exit_dt.tzinfo is None):
            if entry_dt.tzinfo is None:
                entry_dt = entry_dt.replace(tzinfo=timezone.utc)
            else:
                exit_dt = exit_dt.replace(tzinfo=timezone.utc)
        return entry_dt, exit_dt

    @staticmethod
    def _naive(target: datetime) -> datetime:
        return target.replace(tzinfo=None) if target.tzinfo is not None else target

    def _period_status(
        self,
        target: datetime,
        entry_dt: Optional[datetime],
        exit_dt: Optional[datetime],
        entry_date: str,
        exit_date: str,
    ) -> str:
        if entry_dt is not None and exit_dt is not None:
            if entry_dt.tzinfo is not None:
                target_cmp = target
            else:
                target_cmp = self._naive(target)
            if target_cmp < entry_dt:
                return "UPCOMING"
            if target_cmp <= exit_dt:
                return "IN_PROGRESS"
            return "COMPLETED"

        entry_d = self._parse_date(entry_date)
        exit_d = self._parse_date(exit_date)
        if entry_d is None or exit_d is None:
            return "UNRESOLVED"
        target_d = self._naive(target).replace(hour=0, minute=0, second=0, microsecond=0)
        if target_d < entry_d:
            return "UPCOMING"
        if target_d <= exit_d:
            return "IN_PROGRESS"
        return "COMPLETED"

    def _duration_days(
        self,
        entry_dt: Optional[datetime],
        exit_dt: Optional[datetime],
        entry_date: str,
        exit_date: str,
    ) -> int:
        if entry_dt is not None and exit_dt is not None:
            entry_dt, exit_dt = self._normalize_pair(entry_dt, exit_dt)
            return max(0, (exit_dt - entry_dt).days)
        entry_d = self._parse_date(entry_date)
        exit_d = self._parse_date(exit_date)
        if entry_d is None or exit_d is None:
            return -1
        return max(0, (exit_d - entry_d).days)

    def _days_remaining(
        self,
        target: datetime,
        exit_dt: Optional[datetime],
        exit_date: str,
    ) -> int:
        if exit_dt is not None:
            exit_ = exit_dt if exit_dt.tzinfo is not None else exit_dt.replace(tzinfo=timezone.utc)
            target_aware = target if target.tzinfo is not None else target.replace(tzinfo=timezone.utc)
            return max(0, (exit_ - target_aware).days)
        exit_d = self._parse_date(exit_date)
        if exit_d is None:
            return -1
        target_d = self._naive(target).replace(hour=0, minute=0, second=0, microsecond=0)
        return max(0, (exit_d - target_d).days)
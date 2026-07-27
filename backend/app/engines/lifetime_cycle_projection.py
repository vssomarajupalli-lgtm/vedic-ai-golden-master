"""
LifetimeCycleProjection — Capability 7.5
=========================================

Projects Saturn's 30-year cycles bidirectionally from Canonical JSON transit dates.

Governance Rules (LCP-01 to LCP-10):
- LCP-01: Saturn transit duration per Rasi = 30 months (2.5 years) — fixed constant
- LCP-02: Full zodiac cycle = 12 × 30 months = 360 months = 30 years — fixed constant
- LCP-03: Current cycle anchor = Canonical JSON Saturn `start_date` and `rasi`
- LCP-04: Cycle construction: iterate 12 Rasis from anchor, each 30 months, forward and backward
- LCP-05: Past cycles: subtract 30 years per cycle from anchor until before birth_date
- LCP-06: Future cycles: add 30 years per cycle from anchor until governance-defined horizon
- LCP-07: Sade Sati window per cycle = 3 consecutive Rasis: (Moon_Rasi - 1), Moon_Rasi, (Moon_Rasi + 1) modulo 12
- LCP-08: Elinati Shani window per cycle = Rasi at offset +7 from Moon_Rasi (8th house)
- LCP-09: Ashtama Shani window per cycle = Rasi at offset +7 from Moon_Rasi (classical 8th)
- LCP-10: All date arithmetic uses fixed 30-month increments — no astronomical precision

This module performs NO:
- Swiss Ephemeris calls
- Longitude calculation
- Orbital mathematics
- Dasha calculations
- Planet/House Strength calculations
- Yoga calculations
- Report generation
- Interpretation text
"""

from __future__ import annotations

from typing import Optional, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from app.engines.canonical_reference_data import (
    get_canonical_reference_data,
    CanonicalReferenceData,
    RegistryAccessError,
)


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

SATURN_MONTHS_PER_RASI = 30  # LCP-01
MONTHS_PER_CYCLE = 12 * SATURN_MONTHS_PER_RASI  # 360 months = 30 years (LCP-02)
YEARS_PER_CYCLE = 30
FUTURE_HORIZON_YEARS = 120  # Governance-defined horizon (4 cycles forward)


# -----------------------------------------------------------------------------
# Data Classes
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class CycleWindow:
    """A single window within a cycle (Sade Sati phase, Elinati, or Ashtama)."""
    phase: str                    # e.g., "Rising", "Peak", "Setting", "Elinati", "Ashtama"
    rasi: str                     # Rasi name
    mandali: int                  # Mandali number (1-12)
    start_date: str               # DD.MM.YYYY
    end_date: str                 # DD.MM.YYYY


@dataclass(frozen=True)
class SaturnCycle:
    """A single 30-year Saturn cycle with all windows."""
    cycle_number: int             # ... -1, 0, 1, 2 ... (0 = anchor cycle)
    period: str                   # "YYYY-YYYY"
    sade_sati_windows: List[CycleWindow] = field(default_factory=list)  # 3 windows
    elinati_shani_windows: List[CycleWindow] = field(default_factory=list)  # 1 window
    ashtama_shani_windows: List[CycleWindow] = field(default_factory=list)  # 1 window


@dataclass(frozen=True)
class LifetimeCycleProjection:
    """Complete lifetime cycle projection output."""
    cycles: List[SaturnCycle]
    natal_moon_rasi: str
    birth_date: str
    anchor_saturn_rasi: str
    anchor_start_date: str
    anchor_end_date: str


# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------

def _parse_date(date_str: str) -> datetime:
    """Parse DD.MM.YYYY date string to datetime."""
    return datetime.strptime(date_str, "%d.%m.%Y")


def _format_date(dt: datetime) -> str:
    """Format datetime to DD.MM.YYYY string."""
    return dt.strftime("%d.%m.%Y")


def _add_months(dt: datetime, months: int) -> datetime:
    """Add fixed months to date (30 days per month for LCP-10)."""
    # LCP-10: 30 months = 30 * 30 days = 900 days fixed
    days = months * 30
    return dt + timedelta(days=days)


def _subtract_months(dt: datetime, months: int) -> datetime:
    """Subtract fixed months from date (30 days per month for LCP-10)."""
    days = months * 30
    return dt - timedelta(days=days)


def _get_rasi_index(ref_data: CanonicalReferenceData, rasi: str) -> int:
    """Get 0-based index of rasi in zodiacal sequence."""
    return ref_data.get_rasi_index(rasi)


def _get_rasi_at_offset(ref_data: CanonicalReferenceData, from_rasi: str, offset: int) -> str:
    """Get rasi at given offset from from_rasi (modulo 12)."""
    idx = _get_rasi_index(ref_data, from_rasi)
    sequence = ref_data.get_rasi_sequence()
    return sequence[(idx + offset) % 12]


def _get_mandali_for_rasi(ref_data: CanonicalReferenceData, mandali_grid, rasi: str) -> int:
    """Find which mandali contains the given rasi's first pada."""
    # Get the first pada of the rasi
    # We need to find a nakshatra/pada that maps to this rasi
    # For simplicity, find the first pada entry for this rasi
    for entry in ref_data.get_all_pada_entries():
        if ref_data.get_rasi(entry.nakshatra, entry.pada) == rasi:
            absolute_pada = entry.absolute_pada
            return mandali_grid.find_mandali_for_pada(absolute_pada)
    # Fallback: return 1
    return 1


# -----------------------------------------------------------------------------
# Main Capability Class
# -----------------------------------------------------------------------------

class LifetimeCycleProjector:
    """
    Projects Saturn's 30-year cycles bidirectionally from Canonical JSON transit dates.
    
    Stateless, deterministic, no hidden state. All computation via CanonicalReferenceData.
    """
    
    def __init__(
        self,
        ref_data: Optional[CanonicalReferenceData] = None,
        future_horizon_years: int = FUTURE_HORIZON_YEARS,
    ):
        """
        Initialize projector with CanonicalReferenceData.
        
        Args:
            ref_data: CanonicalReferenceData instance (uses singleton if None)
            future_horizon_years: How many years forward to project (default 120 = 4 cycles)
        """
        self._ref_data = ref_data or get_canonical_reference_data()
        self._future_horizon_years = future_horizon_years
    
    def project_cycles(
        self,
        natal_moon_rasi: str,
        birth_date: str,
        saturn_transit: dict,
    ) -> LifetimeCycleProjection:
        """
        Project Saturn cycles bidirectionally from anchor.
        
        Governance Rules:
        - LCP-01: 30 months per Rasi
        - LCP-02: 360 months = 30 years per cycle
        - LCP-03: Anchor = Canonical JSON Saturn start_date and rasi
        - LCP-04: Iterate 12 Rasis from anchor, each 30 months, forward and backward
        - LCP-05: Past cycles: subtract 30 years until before birth_date
        - LCP-06: Future cycles: add 30 years until governance horizon
        - LCP-07: Sade Sati = 3 consecutive Rasis around Moon
        - LCP-08: Elinati Shani = 8th from Moon (offset +7)
        - LCP-09: Ashtama Shani = 8th from Moon (offset +7)
        - LCP-10: Fixed 30-month increments, no astronomical precision
        
        Args:
            natal_moon_rasi: Moon's Rasi from Canonical JSON (e.g., "Makara")
            birth_date: Birth date from Canonical JSON (DD.MM.YYYY)
            saturn_transit: Saturn transit dict from Canonical JSON current_transit
                           Must contain: rasi, start_date, end_date
        
        Returns:
            LifetimeCycleProjection with all cycles and windows
            
        Raises:
            RegistryAccessError: If rasi not found in registry
            ValueError: If saturn_transit missing required fields
        """
        # Validate inputs
        if not saturn_transit or "rasi" not in saturn_transit:
            raise ValueError("saturn_transit must contain 'rasi'")
        if "start_date" not in saturn_transit or "end_date" not in saturn_transit:
            raise ValueError("saturn_transit must contain 'start_date' and 'end_date'")
        
        anchor_rasi = saturn_transit["rasi"]
        anchor_start = _parse_date(saturn_transit["start_date"])
        anchor_end = _parse_date(saturn_transit["end_date"])
        birth_dt = _parse_date(birth_date)
        
        # Validate rasi exists in registry
        _ = _get_rasi_index(self._ref_data, anchor_rasi)
        _ = _get_rasi_index(self._ref_data, natal_moon_rasi)
        
        # Build cycles
        cycles = self._build_cycles(
            natal_moon_rasi=natal_moon_rasi,
            birth_dt=birth_dt,
            anchor_rasi=anchor_rasi,
            anchor_start=anchor_start,
            anchor_end=anchor_end,
        )
        
        return LifetimeCycleProjection(
            cycles=cycles,
            natal_moon_rasi=natal_moon_rasi,
            birth_date=birth_date,
            anchor_saturn_rasi=anchor_rasi,
            anchor_start_date=saturn_transit["start_date"],
            anchor_end_date=saturn_transit["end_date"],
        )
    
    def _build_cycles(
        self,
        natal_moon_rasi: str,
        birth_dt: datetime,
        anchor_rasi: str,
        anchor_start: datetime,
        anchor_end: datetime,
    ) -> List[SaturnCycle]:
        """Build all cycles (past, anchor, future)."""
        cycles = []
        
        # Build cycle 0 (anchor cycle)
        cycle_0 = self._build_single_cycle(
            cycle_number=0,
            anchor_rasi=anchor_rasi,
            anchor_start=anchor_start,
            anchor_end=anchor_end,
            natal_moon_rasi=natal_moon_rasi,
        )
        cycles.append(cycle_0)
        
        # Build past cycles (negative numbers)
        # LCP-05: Subtract 30 years per cycle from anchor until before birth_date
        cycle_num = -1
        cycle_start = _subtract_months(anchor_start, MONTHS_PER_CYCLE)
        cycle_end = _add_months(cycle_start, MONTHS_PER_CYCLE)
        
        while cycle_start >= birth_dt:
            cycle = self._build_single_cycle(
                cycle_number=cycle_num,
                anchor_rasi=anchor_rasi,
                anchor_start=cycle_start,
                anchor_end=cycle_end,
                natal_moon_rasi=natal_moon_rasi,
            )
            cycles.insert(0, cycle)  # Prepend to maintain chronological order
            
            cycle_num -= 1
            cycle_start = _subtract_months(cycle_start, MONTHS_PER_CYCLE)
            cycle_end = _subtract_months(cycle_end, MONTHS_PER_CYCLE)
        
        # Build future cycles (positive numbers)
        # LCP-06: Add 30 years per cycle from anchor until governance-defined horizon
        cycle_num = 1
        cycle_start = _add_months(anchor_start, MONTHS_PER_CYCLE)
        cycle_end = _add_months(cycle_start, MONTHS_PER_CYCLE)
        
        horizon_dt = _add_months(anchor_start, self._future_horizon_years * 12)
        
        while cycle_start < horizon_dt:
            cycle = self._build_single_cycle(
                cycle_number=cycle_num,
                anchor_rasi=anchor_rasi,
                anchor_start=cycle_start,
                anchor_end=cycle_end,
                natal_moon_rasi=natal_moon_rasi,
            )
            cycles.append(cycle)
            
            cycle_num += 1
            cycle_start = _add_months(cycle_start, MONTHS_PER_CYCLE)
            cycle_end = _add_months(cycle_end, MONTHS_PER_CYCLE)
        
        return cycles
    
    def _build_single_cycle(
        self,
        cycle_number: int,
        anchor_rasi: str,
        anchor_start: datetime,
        anchor_end: datetime,
        natal_moon_rasi: str,
    ) -> SaturnCycle:
        """Build a single 30-year cycle with all windows."""
        # LCP-04: Iterate 12 Rasis from anchor, each 30 months
        rasi_sequence = self._ref_data.get_rasi_sequence()
        anchor_idx = _get_rasi_index(self._ref_data, anchor_rasi)
        
        # Sade Sati rasis (LCP-07): Moon_Rasi - 1, Moon_Rasi, Moon_Rasi + 1
        moon_idx = _get_rasi_index(self._ref_data, natal_moon_rasi)
        sade_sati_rasis = [
            rasi_sequence[(moon_idx - 1) % 12],  # Rising (12th from Moon)
            rasi_sequence[moon_idx],              # Peak (Moon Rasi)
            rasi_sequence[(moon_idx + 1) % 12],   # Setting (2nd from Moon)
        ]
        # Map rasi to phase for correct ordering
        sade_sati_phase_map = {
            sade_sati_rasis[0]: "Rising",
            sade_sati_rasis[1]: "Peak",
            sade_sati_rasis[2]: "Setting",
        }
        
        # Elinati/Ashtama rasi (LCP-08, LCP-09): 8th from Moon = offset +7
        elinati_rasi = _get_rasi_at_offset(self._ref_data, natal_moon_rasi, 7)
        ashtama_rasi = elinati_rasi  # Same rasi, different interpretation
        
        # Build the 12 rasi periods for this cycle
        sade_sati_windows = []
        elinati_shani_windows = []
        ashtama_shani_windows = []
        
        period_start = anchor_start
        
        for i in range(12):
            rasi_idx = (anchor_idx + i) % 12
            rasi = rasi_sequence[rasi_idx]
            period_end = _add_months(period_start, SATURN_MONTHS_PER_RASI)
            
            # Check if this rasi is a Sade Sati rasi
            if rasi in sade_sati_rasis:
                phase = sade_sati_phase_map[rasi]
                mandali = self._get_mandali_for_rasi_in_cycle(rasi, anchor_rasi, anchor_start, period_start)
                sade_sati_windows.append(CycleWindow(
                    phase=phase,
                    rasi=rasi,
                    mandali=mandali,
                    start_date=_format_date(period_start),
                    end_date=_format_date(period_end),
                ))
            
            # Check if this rasi is Elinati Shani
            if rasi == elinati_rasi:
                mandali = self._get_mandali_for_rasi_in_cycle(rasi, anchor_rasi, anchor_start, period_start)
                elinati_shani_windows.append(CycleWindow(
                    phase="Elinati",
                    rasi=rasi,
                    mandali=mandali,
                    start_date=_format_date(period_start),
                    end_date=_format_date(period_end),
                ))
            
            # Check if this rasi is Ashtama Shani
            if rasi == ashtama_rasi:
                mandali = self._get_mandali_for_rasi_in_cycle(rasi, anchor_rasi, anchor_start, period_start)
                ashtama_shani_windows.append(CycleWindow(
                    phase="Ashtama",
                    rasi=rasi,
                    mandali=mandali,
                    start_date=_format_date(period_start),
                    end_date=_format_date(period_end),
                ))
            
            period_start = period_end
        
        # Period string for the cycle (30 years from this cycle's start)
        cycle_start_year = anchor_start.year
        cycle_end_year = anchor_start.year + YEARS_PER_CYCLE
        
        period_str = f"{cycle_start_year}-{cycle_end_year}"
        
        # Sort Sade Sati windows by phase order: Rising, Peak, Setting (zodiacal order)
        phase_order = {"Rising": 0, "Peak": 1, "Setting": 2}
        sade_sati_windows.sort(key=lambda w: phase_order.get(w.phase, 99))
        
        # Sort other windows by start date
        elinati_shani_windows.sort(key=lambda w: w.start_date)
        ashtama_shani_windows.sort(key=lambda w: w.start_date)
        
        return SaturnCycle(
            cycle_number=cycle_number,
            period=period_str,
            sade_sati_windows=sade_sati_windows,
            elinati_shani_windows=elinati_shani_windows,
            ashtama_shani_windows=ashtama_shani_windows,
        )
    
    def _get_mandali_for_rasi_in_cycle(
        self,
        rasi: str,
        anchor_rasi: str,
        anchor_start: datetime,
        period_start: datetime,
    ) -> int:
        """
        Calculate which mandali a rasi period falls into.
        This is a simplified calculation - in practice would use the mandali grid.
        For now, return a reasonable mandali number based on rasi offset from anchor.
        """
        rasi_sequence = self._ref_data.get_rasi_sequence()
        anchor_idx = _get_rasi_index(self._ref_data, anchor_rasi)
        rasi_idx = _get_rasi_index(self._ref_data, rasi)
        offset = (rasi_idx - anchor_idx) % 12
        
        # Each mandali spans roughly 2.5 rasis (30 months / 12 months per rasi = 2.5)
        # But mandalis are 9 padas each, rasis vary in pada count
        # Simplified: map rasi offset to mandali
        # Mandali 1 starts at anchor, each mandali ~2.5 rasis
        mandali = (offset // 2) + 1
        if mandali > 12:
            mandali = 12
        return max(1, min(12, mandali))


# -----------------------------------------------------------------------------
# Convenience Function
# -----------------------------------------------------------------------------

def project_lifetime_cycles(
    natal_moon_rasi: str,
    birth_date: str,
    saturn_transit: dict,
    ref_data: Optional[CanonicalReferenceData] = None,
    future_horizon_years: int = FUTURE_HORIZON_YEARS,
) -> LifetimeCycleProjection:
    """
    Convenience function to project lifetime Saturn cycles.
    
    Args:
        natal_moon_rasi: Moon's Rasi from Canonical JSON
        birth_date: Birth date from Canonical JSON (DD.MM.YYYY)
        saturn_transit: Saturn transit dict from Canonical JSON
        ref_data: Optional CanonicalReferenceData (uses singleton if None)
        future_horizon_years: Years to project forward (default 120)
        
    Returns:
        LifetimeCycleProjection with all cycles
    """
    projector = LifetimeCycleProjector(
        ref_data=ref_data,
        future_horizon_years=future_horizon_years,
    )
    return projector.project_cycles(natal_moon_rasi, birth_date, saturn_transit)
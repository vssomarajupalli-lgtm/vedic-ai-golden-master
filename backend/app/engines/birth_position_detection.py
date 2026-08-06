"""
BirthPositionDetection — Capability 7.6
========================================

Classifies native's birth position relative to each major cycle window.

Governance Rules (BPD-01 to BPD-06):
- BPD-01: For each window: if birth_date ∈ [start_date, end_date] → BIRTH_INSIDE
- BPD-02: If birth_date < start_date of first window → BIRTH_BEFORE_FIRST_CYCLE
- BPD-03: If birth_date < start_date of window N and birth_date > end_date of window N-1 → BIRTH_BEFORE_THIS_CYCLE
- BPD-04: If birth_date > end_date of last window → BIRTH_AFTER_LAST_CYCLE
- BPD-05: Classification is per-window-type (Sade Sati, Elinati, Ashtama) — independent
- BPD-06: Output includes: position enum, cycle_number, phase, human-readable description

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

from typing import Optional, List, Literal
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from app.engines.canonical_reference_data import (
    get_canonical_reference_data,
    CanonicalReferenceData,
    RegistryAccessError,
)
from app.engines.lifetime_cycle_projection import (
    LifetimeCycleProjection,
    SaturnCycle,
    CycleWindow,
)


# -----------------------------------------------------------------------------
# Enums
# -----------------------------------------------------------------------------

class BirthPosition(str, Enum):
    """Birth position relative to a cycle window."""
    BIRTH_INSIDE = "BIRTH_INSIDE"
    BIRTH_BEFORE_THIS_CYCLE = "BIRTH_BEFORE_THIS_CYCLE"
    BIRTH_BEFORE_FIRST_CYCLE = "BIRTH_BEFORE_FIRST_CYCLE"
    BIRTH_AFTER_LAST_CYCLE = "BIRTH_AFTER_LAST_CYCLE"
    BIRTH_OUTSIDE = "BIRTH_OUTSIDE"


class WindowType(str, Enum):
    """Type of cycle window."""
    SADE_SATI = "Sade Sati"
    ELINATI_SHANI = "Elinati Shani"
    ASHTAMA_SHANI = "Ashtama Shani"


# -----------------------------------------------------------------------------
# Data Classes
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class BirthPositionResult:
    """Result of birth position detection for a single window."""
    position: BirthPosition
    cycle_number: int
    phase: str
    description: str
    window_type: WindowType
    window_start_date: str
    window_end_date: str


@dataclass(frozen=True)
class BirthPositionDetection:
    """Complete birth position detection results for all window types."""
    sade_sati: List[BirthPositionResult]
    elinati_shani: List[BirthPositionResult]
    ashtama_shani: List[BirthPositionResult]
    birth_date: str
    natal_moon_rasi: str


# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------

def _parse_date(date_str: str) -> datetime:
    """Parse DD.MM.YYYY date string to datetime."""
    return datetime.strptime(date_str, "%d.%m.%Y")


def _format_date(dt: datetime) -> str:
    """Format datetime to DD.MM.YYYY string."""
    return dt.strftime("%d.%m.%Y")


# -----------------------------------------------------------------------------
# Main Capability Class
# -----------------------------------------------------------------------------

class BirthPositionDetector:
    """
    Detects native's birth position relative to cycle windows.
    
    Stateless, deterministic, no hidden state. All computation via CanonicalReferenceData.
    """
    
    def __init__(
        self,
        ref_data: Optional[CanonicalReferenceData] = None,
    ):
        """
        Initialize detector with CanonicalReferenceData.
        
        Args:
            ref_data: CanonicalReferenceData instance (uses singleton if None)
        """
        self._ref_data = ref_data or get_canonical_reference_data()
    
    def detect_birth_position(
        self,
        birth_date: str,
        natal_moon_rasi: str,
        lifetime_projection: LifetimeCycleProjection,
    ) -> BirthPositionDetection:
        """
        Detect birth position for all window types.
        
        Governance Rules:
        - BPD-01: birth_date ∈ [start_date, end_date] → BIRTH_INSIDE
        - BPD-02: birth_date < start_date of first window → BIRTH_BEFORE_FIRST_CYCLE
        - BPD-03: birth_date between windows → BIRTH_BEFORE_THIS_CYCLE
        - BPD-04: birth_date > end_date of last window → BIRTH_AFTER_LAST_CYCLE
        - BPD-05: Classification per-window-type (independent)
        - BPD-06: Output includes position enum, cycle_number, phase, description
        
        Args:
            birth_date: Birth date from Canonical JSON (DD.MM.YYYY)
            natal_moon_rasi: Moon's Rasi from Canonical JSON
            lifetime_projection: LifetimeCycleProjection from Capability 7.5
            
        Returns:
            BirthPositionDetection with results for all window types
        """
        birth_dt = _parse_date(birth_date)
        
        # Collect all windows by type across all cycles
        # Use tuples of (window, cycle_number) to avoid modifying frozen dataclass
        sade_sati_windows = []
        elinati_windows = []
        ashtama_windows = []
        
        for cycle in lifetime_projection.cycles:
            for window in cycle.sade_sati_windows:
                sade_sati_windows.append((window, cycle.cycle_number))
            for window in cycle.elinati_shani_windows:
                elinati_windows.append((window, cycle.cycle_number))
            for window in cycle.ashtama_shani_windows:
                ashtama_windows.append((window, cycle.cycle_number))
        
        # Sort windows by start date
        sade_sati_windows.sort(key=lambda w: _parse_date(w[0].start_date))
        elinati_windows.sort(key=lambda w: _parse_date(w[0].start_date))
        ashtama_windows.sort(key=lambda w: _parse_date(w[0].start_date))
        
        # Classify for each window type (BPD-05: independent per type)
        sade_sati_results = self._classify_window_type(
            birth_dt, sade_sati_windows, WindowType.SADE_SATI
        )
        elinati_results = self._classify_window_type(
            birth_dt, elinati_windows, WindowType.ELINATI_SHANI
        )
        ashtama_results = self._classify_window_type(
            birth_dt, ashtama_windows, WindowType.ASHTAMA_SHANI
        )
        
        return BirthPositionDetection(
            sade_sati=sade_sati_results,
            elinati_shani=elinati_results,
            ashtama_shani=ashtama_results,
            birth_date=birth_date,
            natal_moon_rasi=natal_moon_rasi,
        )
    
    def _classify_window_type(
        self,
        birth_dt: datetime,
        windows: List[tuple],
        window_type: WindowType,
    ) -> List[BirthPositionResult]:
        """Classify birth position for a specific window type.
        
        windows: List of tuples (CycleWindow, cycle_number)
        """
        if not windows:
            return []

        # BPD-02: Before first window
        first_window, first_cycle_num = windows[0]
        if birth_dt < _parse_date(first_window.start_date):
            position = BirthPosition.BIRTH_BEFORE_FIRST_CYCLE
            description = f"Born before the first {window_type.value} period."
            return [BirthPositionResult(
                position=position,
                cycle_number=first_cycle_num,
                phase=first_window.phase,
                description=description,
                window_type=window_type,
                window_start_date=first_window.start_date,
                window_end_date=first_window.end_date,
            )]

        # BPD-04: After last window
        last_window, last_cycle_num = windows[-1]
        if birth_dt > _parse_date(last_window.end_date):
            position = BirthPosition.BIRTH_AFTER_LAST_CYCLE
            description = f"Born after the final projected {window_type.value} period."
            return [BirthPositionResult(
                position=position,
                cycle_number=last_cycle_num,
                phase=last_window.phase,
                description=description,
                window_type=window_type,
                window_start_date=last_window.start_date,
                window_end_date=last_window.end_date,
            )]

        # BPD-01 & BPD-03: Inside a window or between windows
        # Phase 1: exact window-START match takes precedence (resolves shared
        # boundaries where one window ends and the next begins on the same date).
        for window, cycle_num in windows:
            window_start = _parse_date(window.start_date)
            if birth_dt == window_start:
                position = BirthPosition.BIRTH_INSIDE
                description = f"Born during the {window_type.value} {window.phase} phase of cycle {cycle_num}."
                return [BirthPositionResult(
                    position=position,
                    cycle_number=cycle_num,
                    phase=window.phase,
                    description=description,
                    window_type=window_type,
                    window_start_date=window.start_date,
                    window_end_date=window.end_date,
                )]

        # Phase 2: birth strictly inside a window (inclusive start/end per BPD-01)
        for i, (window, cycle_num) in enumerate(windows):
            window_start = _parse_date(window.start_date)
            window_end = _parse_date(window.end_date)

            if window_start < birth_dt <= window_end:
                position = BirthPosition.BIRTH_INSIDE
                description = f"Born during the {window_type.value} {window.phase} phase of cycle {cycle_num}."
                return [BirthPositionResult(
                    position=position,
                    cycle_number=cycle_num,
                    phase=window.phase,
                    description=description,
                    window_type=window_type,
                    window_start_date=window.start_date,
                    window_end_date=window.end_date,
                )]

            # BPD-03: Between windows
            if i > 0:
                # Check if birth is between previous window end and current window start
                prev_window, prev_cycle_num = windows[i-1]
                prev_end = _parse_date(prev_window.end_date)
                if prev_end < birth_dt < window_start:
                    # BPD-03: Between windows
                    position = BirthPosition.BIRTH_BEFORE_THIS_CYCLE
                    description = f"Born between {window_type.value} cycles (after cycle {prev_cycle_num}, before cycle {cycle_num})."
                    return [BirthPositionResult(
                        position=position,
                        cycle_number=cycle_num,  # Relative to the upcoming cycle
                        phase=window.phase,
                        description=description,
                        window_type=window_type,
                        window_start_date=window.start_date,
                        window_end_date=window.end_date,
                    )]

        return []  # Should be unreachable if windows is not empty


# -----------------------------------------------------------------------------
# Convenience Function
# -----------------------------------------------------------------------------

def detect_birth_position(
    birth_date: str,
    natal_moon_rasi: str,
    lifetime_projection: LifetimeCycleProjection,
    ref_data: Optional[CanonicalReferenceData] = None,
) -> BirthPositionDetection:
    """
    Convenience function to detect birth position.
    
    Args:
        birth_date: Birth date from Canonical JSON (DD.MM.YYYY)
        natal_moon_rasi: Moon's Rasi from Canonical JSON
        lifetime_projection: LifetimeCycleProjection from Capability 7.5
        ref_data: Optional CanonicalReferenceData (uses singleton if None)
        
    Returns:
        BirthPositionDetection with results for all window types
    """
    detector = BirthPositionDetector(ref_data=ref_data)
    return detector.detect_birth_position(birth_date, natal_moon_rasi, lifetime_projection)
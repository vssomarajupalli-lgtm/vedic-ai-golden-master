from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass(frozen=True)
class MandaliPadaSlot:
    """A single Nakshatra-Pada position inside a Mandali Gochar cell."""
    position: int                    # 1-9 (slot within the Mandali arc)
    absolute_pada: int               # 1-108
    nakshatra: str                   # e.g. "Dhanishta"
    pada: int                        # 1-4 (quarter of the nakshatra)
    planets: List[str] = field(default_factory=list)  # short planet codes at this exact pada


@dataclass(frozen=True)
class MandaliGocharCell:
    """One Rasi box of the Present Gochar Mandali chart (9 pada positions)."""
    mandali_number: int              # 1-12 (Moon-relative Mandali number)
    mandali_name: str                # "Mandali 1 (Makara)"
    rasi: str                        # Rasi of this Mandali cell
    center_pada: int                 # 1-108
    padas: List[MandaliPadaSlot]     # exactly 9 slots


@dataclass(frozen=True)
class NextMandaliRef:
    """Reference to the next Mandali a planet will enter."""
    number: int
    name: str


@dataclass(frozen=True)
class MandaliPeriodEntry:
    """Report B row — Mandali-based transit period for a single planet."""
    planet: str
    current_rasi: str                # planet's actual zodiac Rasi
    rasi_number: int                 # 1-12 zodiacal (Mesha=1 .. Meena=12)
    nakshatra: str
    pada: int
    mandali_number: int              # Moon-relative Mandali
    mandali_name: str
    entry_date: str                  # DD.MM.YYYY (canonical date format)
    entry_datetime: str              # ISO-8601 UTC instant
    exit_date: str                   # DD.MM.YYYY
    exit_datetime: str               # ISO-8601 UTC instant
    next_mandali: NextMandaliRef
    status: str                      # IN_PROGRESS | UPCOMING | COMPLETED | UNRESOLVED
    duration_days: int
    days_remaining: int
    mandali_status: str              # FAVORABLE | NEUTRAL | CHALLENGING


@dataclass(frozen=True)
class RasiGocharEntry:
    """Report A row — regular Rasi-based gochar period for a single planet."""
    planet: str
    current_rasi: str
    rasi_number: int                 # 1-12 zodiacal
    rasi_entry: str                  # DD.MM.YYYY or "—"
    rasi_exit: str                   # DD.MM.YYYY or "—"
    next_rasi: str
    status: str                      # IN_PROGRESS | UPCOMING | COMPLETED | UNRESOLVED
    duration_days: int
    days_remaining: int


@dataclass(frozen=True)
class SaturnMandaliPeriod:
    """A single Saturn special-period window resolved from the actual
    Moon-centered Mandali resolver (not the legacy Rasi heuristic)."""
    cycle: str                       # "Sade Sati", "Ardha Ashtama", "Ashtama", "Elinati"
    phase: str                       # "Rising"|"Peak"|"Setting"|"Ardha Ashtama"|"Ashtama"...
    rasi: str                        # Mandali cell Rasi
    mandali_number: int
    mandali_name: str
    nakshatra: str
    pada: int
    entry: str                       # DD.MM.YYYY or "—"
    exit: str                        # DD.MM.YYYY or "—"
    next_mandali: Optional[int]
    status: str                      # ACTIVE | UPCOMING | NOT_FOUND | INACTIVE
    mechanism: str                   # "MANDALI_RESOLVER"


@dataclass(frozen=True)
class SaturnPeriodGroup:
    current: List[SaturnMandaliPeriod] = field(default_factory=list)
    upcoming: List[SaturnMandaliPeriod] = field(default_factory=list)


@dataclass(frozen=True)
class SaturnPeriods:
    """Saturn special periods in the Moon-centered Mandali frame.

    Two mechanisms are preserved side by side:
     - the Mandali-based periods (resolved through the actual Mandali grid), and
     - the legacy Rasi-based lifetime windows from UniversalMandaliEngine
       (carried verbatim in `legacy_windows` and clearly labelled).
    """
    sade_sati: SaturnPeriodGroup
    ardha_ashtama: SaturnPeriodGroup
    ashtama: SaturnPeriodGroup
    elinati: SaturnPeriodGroup
    current_saturn: Dict[str, Any] = field(default_factory=dict)
    legacy_windows: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class MandaliGocharReport:
    """Complete Present Gochar Rasi-Mandali report (Report B) including the
    Rasi-Mandali chart, per-planet Mandali periods, Saturn special periods, and
    the side-by-side comparison with the regular Rasi-based gochar (Report A)."""
    schema_version: str
    target_date: str
    reference_moon: Dict[str, Any]
    chart: List[MandaliGocharCell]
    periods: List[MandaliPeriodEntry]
    saturn_periods: SaturnPeriods
    comparison: Dict[str, Any]
    # R2 — Fixed universal Rasi -> Nakshatra-Pada reference (12 Rasis, 9
    # absolute padas each). Built once from the authoritative
    # nakshatra_rasi_registry + rasi_sequence_registry (identity-person
    # independent), never hardcoded. Additive presentation field only.
    fixed_rasi_map: Dict[str, Any] = field(default_factory=dict)
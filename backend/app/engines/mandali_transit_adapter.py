"""
MandaliTransitAdapter — Transforms runtime transit snapshot to Mandali input format.
=================================================================================

This adapter bridges EphemerisService output to UniversalMandaliEngine's
required current_transit format. It reuses existing repository services
without duplicating any calculations.

Governance:
- No new astronomy calculations
- No new Nakshatra logic
- No new House calculations
- Pure transformation layer
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

from app.engines.canonical_reference_data import get_canonical_reference_data
from app.engines.nakshatra_pada_resolver import NakshatraPadaResolver
from app.engines.transit_mandali_resolution import TransitMandaliResolver
from app.engines.mandali_generator import MandaliGenerator
from app.engines.mandali_grid_construction import MandaliGrid, MandaliGridConstruction
from app.utils.ephemeris_service import EphemerisService


# Maximum number of days scanned backward/forward to locate the transit planet's
# entry into and exit from its current Mandali. Covers the slowest planets
# (Saturn ~30° per ~2.5-3.1 years including retrograde; lunar nodes ~1.6 years).
_TRANSIT_SCAN_MAX_DAYS = 1500


@dataclass(frozen=True)
class MandaliInputDTO:
    """
    Immutable input DTO for UniversalMandaliEngine.
    Contains ONLY natal reference and current transit snapshot.
    """
    natal: Dict[str, Any]           # {"moon": {"rasi": str, "nakshatra": str, "pada": int}, "birth_date": str}
    current_transit: List[Dict[str, Any]]  # List of transit planet dicts per Mandali schema


class MandaliTransitAdapter:
    """
    Transforms EphemerisService runtime snapshot into Mandali-compatible
    current_transit structure using existing repository services.
    
    Responsibilities:
    - Convert EphemerisService output format to Mandali list format
    - Resolve nakshatra/pada from longitude (via NakshatraPadaResolver)
    - Compute house_from_moon (via TransitMandaliResolver logic)
    - Fetch interpretation from reference data
    - Calculate start/end dates for transit duration
    
    Does NOT:
    - Perform astronomical calculations
    - Duplicate Nakshatra resolution logic
    - Duplicate House-from-Moon logic
    - Mutate Canonical JSON
    """

    def __init__(
        self,
        ephemeris_service: Optional[EphemerisService] = None,
        pada_resolver: Optional[NakshatraPadaResolver] = None,
        transit_resolver: Optional[TransitMandaliResolver] = None,
        ref_data=None,
    ):
        self._ephemeris = ephemeris_service or EphemerisService()
        self._pada_resolver = pada_resolver or NakshatraPadaResolver(ref_data or get_canonical_reference_data())
        self._transit_resolver = transit_resolver
        self._ref_data = ref_data or get_canonical_reference_data()

    def adapt(
        self,
        ephemeris_snapshot: Dict[str, Any],
        natal_moon_sign: str,
        natal_moon_nakshatra: str,
        natal_moon_pada: int,
        target_date_utc: datetime,
    ) -> List[Dict[str, Any]]:
        """
        Transform EphemerisService snapshot to UniversalMandaliEngine current_transit format.
        
        Args:
            ephemeris_snapshot: Output from EphemerisService.generate_transit_snapshot()
            natal_moon_sign: Natal Moon rasi (e.g., "taurus")
            natal_moon_nakshatra: Natal Moon nakshatra (e.g., "Krittika")
            natal_moon_pada: Natal Moon pada (1-4)
            target_date_utc: Consultation date for transit duration calculation
            
        Returns:
            List of transit planet dicts matching Mandali current_transit schema
        """
        transit_planets = ephemeris_snapshot.get("planets", {})
        result = []

        # Deterministic 12-Mandali grid centered on the Natal Moon, identical to
        # the grid used by MandaliGridConstruction/UniversalMandaliEngine.
        grid = MandaliGridConstruction(
            ref_data=self._ref_data,
            pada_resolver=self._pada_resolver,
        ).build_grid(
            natal_moon_nakshatra=natal_moon_nakshatra,
            natal_moon_pada=natal_moon_pada,
        )

        for planet_name, planet_data in transit_planets.items():
            if planet_name == "ascendant":
                continue

            # Resolve nakshatra and pada from longitude using the same deterministic
            # chain as the natal path (longitude -> absolute pada -> reference data).
            longitude = planet_data.get("longitude", 0.0)
            nakshatra, pada = self._resolve_nakshatra_pada(longitude)

            # Compute classical house from Moon using existing logic
            house_from_moon = self._compute_house_from_moon(
                natal_moon_sign=natal_moon_sign,
                transit_sign=planet_data["sign"],
            )

            # Get interpretation from reference data
            interpretation = self._get_interpretation(planet_name, house_from_moon)

            # Calculate transit duration (start/end dates) from real planetary
            # motion across the Mandali arc boundaries (ephemeris crossings),
            # and the Mandali the planet actually enters at the exit crossing.
            start_date, end_date, next_mandali = self._calculate_transit_dates(planet_name, grid, target_date_utc)

            transit_entry = {
                "planet": planet_name.capitalize(),
                "rasi": planet_data["sign"].capitalize(),
                "nakshatra": nakshatra,
                "pada": pada,
                "start_date": start_date,
                "end_date": end_date,
                "next_mandali": next_mandali,
                "house_from_moon": house_from_moon,
                "interpretation": interpretation,
            }
            result.append(transit_entry)

        return result

    def _resolve_nakshatra_pada(self, longitude: float) -> tuple:
        """Resolve nakshatra and pada from sidereal longitude.

        Uses the same deterministic chain as the natal path:
            longitude -> absolute pada (MandaliGenerator) -> reference data.
        This guarantees the transit nakshatra/pada is zodiacally consistent with
        the transit rasi (previously the hand-rolled lookup indexed an
        alphabetically-sorted nakshatra list, breaking zodiac order).
        """
        absolute_pada = MandaliGenerator.get_absolute_pada(longitude)
        return self._ref_data.get_nakshatra_pada(absolute_pada)

    def _compute_house_from_moon(self, natal_moon_sign: str, transit_sign: str) -> int:
        """Compute classical house from Moon using existing logic (reused from TransitMandaliResolver)."""
        signs_order = [
            "Mesha", "Vrishabha", "Mithuna", "Karkata", "Simha", "Kanya",
            "Tula", "Vrishchika", "Dhanus", "Makara", "Kumbha", "Meena"
        ]
        
        try:
            moon_idx = signs_order.index(natal_moon_sign.title())
            transit_idx = signs_order.index(transit_sign.title())
            # House from Moon: (transit - moon) mod 12 + 1
            house = ((transit_idx - moon_idx) % 12) + 1
            return house
        except ValueError:
            return 1  # fallback

    def _get_interpretation(self, planet: str, house_from_moon: int) -> str:
        """Fetch interpretation from reference data registry."""
        # Check if reference data has interpretations
        interpretations = getattr(self._ref_data, 'transit_interpretations', {})
        key = f"{planet}_h{house_from_moon}"
        return interpretations.get(key, f"{planet.capitalize()} transiting house {house_from_moon} from Moon")

    def _calculate_transit_dates(self, planet: str, grid, target_date: datetime) -> tuple:
        """Calculate the actual entry/exit dates and the next Mandali for a planet.

        The dates are the moments the planet's sidereal longitude crossed into
        and out of its current Mandali arc, scanned from the ephemeris in both
        time directions. The next Mandali is the Mandali the planet actually
        enters at the exit crossing (determined by the real crossing, not a
        fixed 'current + 1'). No placeholder arithmetic is used: when a crossing
        cannot be resolved the dates are reported as '—' and next Mandali as
        None rather than fabricating values.
        """
        try:
            target_mandali = self._mandali_at(planet, grid, target_date)
        except Exception:
            return "—", "—", None

        # Entry: most recent past transition INTO the current Mandali.
        entry = self._find_transition(
            planet, grid, target_mandali, target_date, look_backward=True
        )
        # Exit: next future transition OUT of the current Mandali.
        exit_ = self._find_transition(
            planet, grid, target_mandali, target_date, look_backward=False
        )

        if entry is None or exit_ is None:
            return "—", "—", None

        entry_dt, _ = entry
        exit_dt, next_mandali = exit_
        fmt = "%d.%m.%Y"
        return entry_dt.strftime(fmt), exit_dt.strftime(fmt), next_mandali

    def _mandali_at(self, planet: str, grid, date: datetime) -> int:
        """Return the Mandali number containing the planet at a given UTC datetime."""
        longitude = self._ephemeris.get_longitude(planet, date)
        absolute_pada = MandaliGenerator.get_absolute_pada(longitude)
        return grid.find_mandali_for_pada(absolute_pada)

    def _find_transition(
        self,
        planet: str,
        grid,
        target_mandali: int,
        target_date: datetime,
        look_backward: bool,
    ) -> tuple | None:
        """Find the UTC instant of the nearest Mandali transition for the planet.

        Args:
            look_backward: True -> most recent entry INTO target_mandali;
                           False -> next exit OUT of target_mandali.
        Returns:
            (crossing_instant, mandali_entered_at_crossing), or None if not found
            within the scan window. The mandali entered at the crossing is the
            post-crossing Mandali (for the exit scan this is the actual next
            Mandali, which for a retrograde planet may be the previous Mandali).
        """
        step = timedelta(days=1)
        day = 1
        while day <= _TRANSIT_SCAN_MAX_DAYS:
            t_outer = target_date - step * day if look_backward else target_date + step * (day - 1)
            t_inner = t_outer + step  # always toward the target date
            m_outer = self._mandali_at(planet, grid, t_outer)
            m_inner = self._mandali_at(planet, grid, t_inner)
            if m_outer != m_inner:
                # Transition occurred between t_outer and t_inner. The predicate
                # "(mandali == target_mandali)" is monotone across the interval;
                # locate the flip with bisection. m_inner is the Mandali on the
                # post-crossing side (the one the planet enters).
                target_value = m_inner == target_mandali
                crossing = self._bisect_transition(planet, grid, target_mandali, t_outer, t_inner, target_value)
                return crossing, m_inner
            day += 1
        return None

    def _bisect_transition(
        self,
        planet: str,
        grid,
        target_mandali: int,
        lo: datetime,
        hi: datetime,
        target_value: bool,
    ) -> datetime:
        """Bisect to the instant where (mandali == target_mandali) flips.

        Predicate is monotone across [lo, hi]: it equals target_value after the
        crossing and not-target_value before it (or vice versa).
        """
        for _ in range(45):
            mid = lo + (hi - lo) / 2
            if (self._mandali_at(planet, grid, mid) == target_mandali) == target_value:
                hi = mid
            else:
                lo = mid
        return hi
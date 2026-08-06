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
from datetime import datetime

from app.engines.canonical_reference_data import get_canonical_reference_data
from app.engines.nakshatra_pada_resolver import NakshatraPadaResolver
from app.engines.transit_mandali_resolution import TransitMandaliResolver
from app.utils.ephemeris_service import EphemerisService


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

        for planet_name, planet_data in transit_planets.items():
            if planet_name == "ascendant":
                continue

            # Resolve nakshatra and pada from longitude using existing resolver
            longitude = planet_data.get("longitude", 0.0)
            nakshatra, pada = self._resolve_nakshatra_pada(longitude)

            # Compute classical house from Moon using existing logic
            house_from_moon = self._compute_house_from_moon(
                natal_moon_sign=natal_moon_sign,
                transit_sign=planet_data["sign"],
            )

            # Get interpretation from reference data
            interpretation = self._get_interpretation(planet_name, house_from_moon)

            # Calculate transit duration (start/end dates)
            start_date, end_date = self._calculate_transit_dates(planet_name, target_date_utc)

            transit_entry = {
                "planet": planet_name.capitalize(),
                "rasi": planet_data["sign"].capitalize(),
                "nakshatra": nakshatra,
                "pada": pada,
                "start_date": start_date,
                "end_date": end_date,
                "house_from_moon": house_from_moon,
                "interpretation": interpretation,
            }
            result.append(transit_entry)

        return result

    def _resolve_nakshatra_pada(self, longitude: float) -> tuple:
        """Resolve nakshatra and pada from sidereal longitude using existing resolver."""
        # NakshatraPadaResolver.resolve() expects nakshatra_name and pada
        # We need to work backwards: longitude -> nakshatra -> pada
        # The resolver can give us absolute pada from nakshatra + pada
        # For reverse lookup, we compute from longitude directly
        
        # Each nakshatra = 13°20' = 13.333... degrees
        # Each pada = 3°20' = 3.333... degrees
        nakshatra_span = 13 + 1/3  # 13.333...
        pada_span = 3 + 1/3       # 3.333...
        
        # Nakshatra index (0-26)
        nakshatra_index = int(longitude / nakshatra_span) % 27
        
        # Pada within nakshatra (1-4)
        pada_in_nakshatra = int((longitude % nakshatra_span) / pada_span) + 1
        
        # Get nakshatra name from canonical reference data using existing method
        all_nakshatras = self._ref_data.get_all_nakshatras() if hasattr(self._ref_data, 'get_all_nakshatras') else []
        if nakshatra_index < len(all_nakshatras):
            nakshatra_name = sorted(all_nakshatras)[nakshatra_index]
        else:
            # Fallback: compute from absolute pada
            absolute_pada = (nakshatra_index * 4) + pada_in_nakshatra
            nakshatra_name, _ = self._ref_data.get_nakshatra_pada(absolute_pada)
        
        return nakshatra_name, pada_in_nakshatra

    def _compute_house_from_moon(self, natal_moon_sign: str, transit_sign: str) -> int:
        """Compute classical house from Moon using existing logic (reused from TransitMandaliResolver)."""
        signs_order = [
            "aries", "taurus", "gemini", "cancer", "leo", "virgo",
            "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
        ]
        
        try:
            moon_idx = signs_order.index(natal_moon_sign.lower())
            transit_idx = signs_order.index(transit_sign.lower())
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

    def _calculate_transit_dates(self, planet: str, target_date: datetime) -> tuple:
        """Calculate transit start and end dates based on planet's average transit duration."""
        # Average transit durations (days) for each planet
        durations = {
            "sun": 30,
            "moon": 2.5,
            "mars": 45,
            "mercury": 20,
            "jupiter": 365,
            "venus": 25,
            "saturn": 730,
            "rahu": 540,
            "ketu": 540,
        }
        
        days = durations.get(planet, 30)
        
        # Approximate: target_date is middle of transit
        from datetime import timedelta
        half = timedelta(days=days / 2)
        start = target_date - half
        end = target_date + half
        
        # Format as DD.MM.YYYY
        fmt = "%d.%m.%Y"
        return start.strftime(fmt), end.strftime(fmt)
"""
MandaliPlacementFactory — Pure mapping layer for placement DTOs.
=============================================================

Creates placement DTOs from MandaliAdvisory + canonical data.
Zero calculations. Zero astronomy. Zero formatting.
"""

from __future__ import annotations

from typing import List, Dict, Any
from app.schemas.natal_chart import NatalPlanetPlacement
from app.schemas.current_chart import CurrentTransitPlanetPlacement
from app.engines.mandali_grid_construction import MandaliGrid
from app.engines.mandali_generator import MandaliGenerator
from app.engines.canonical_reference_data import get_canonical_reference_data


# Canonical natal planet order (Sun -> Ketu), matching the transit planet set.
NATAL_PLANET_IDS: List[str] = [
    "sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn", "rahu", "ketu",
]


class MandaliPlacementFactory:
    """
    Factory for creating placement DTOs from MandaliAdvisory and canonical data.
    
    Responsibilities:
    - Map MandaliAdvisory data to placement DTOs
    - Zero calculations, zero astronomy, zero formatting
    - Pure DTO construction
    
    Does NOT:
    - Perform calculations
    - Access Ephemeris
    - Compute Nakshatra/Pada
    - Format for presentation
    """

    def build_natal(
        self,
        natal_planets: Dict[str, Any],
        mandali_grid: MandaliGrid,
    ) -> List[NatalPlanetPlacement]:
        """
        Build natal planet placements DTO list.

        Args:
            natal_planets: Normalized natal planets collection keyed by planet id
                (e.g. {"sun": {...}, "moon": {...}, ...}) with longitude per planet.
            mandali_grid: The constructed MandaliGrid

        Returns:
            List of NatalPlanetPlacement DTOs, one per natal planet
        """
        # Same resolution chain as Current Transit: longitude -> absolute pada
        # -> nakshatra/pada -> Mandali (reuses MandaliGenerator + reference data).
        ref_data = get_canonical_reference_data()
        placements = []

        for planet_id in NATAL_PLANET_IDS:
            planet_data = natal_planets.get(planet_id)
            if not planet_data:
                continue

            longitude = planet_data.get("longitude") or 0.0
            absolute_pada = MandaliGenerator.get_absolute_pada(longitude)
            nakshatra, pada = ref_data.get_nakshatra_pada(absolute_pada)

            mandali_num = mandali_grid.find_mandali_for_pada(absolute_pada)
            mandali = mandali_grid.get_mandali(mandali_num)

            mandali_dict = {
                "number": mandali.number,
                "name": f"Mandali {mandali.number} ({mandali.rasi_name})",
            }

            placements.append(
                NatalPlanetPlacement(
                    planet=planet_data.get("name", planet_id).capitalize(),
                    rasi=planet_data.get("sign", ""),
                    nakshatra=nakshatra,
                    pada=pada,
                    mandali=mandali_dict,
                )
            )

        return placements

    def build_current(
        self,
        transit_resolutions: List[Any],  # List[TransitMandaliResolution]
        mandali_grid: MandaliGrid,
    ) -> List[CurrentTransitPlanetPlacement]:
        """
        Build current transit planet placements DTO list.
        
        Args:
            transit_resolutions: List of TransitMandaliResolution from MandaliAdvisory
            mandali_grid: The constructed MandaliGrid
            
        Returns:
            List of CurrentTransitPlanetPlacement DTOs
        """
        placements = []
        
        for res in transit_resolutions:
            mandali_num = res.mandali["number"]
            transit_mandali = mandali_grid.get_mandali(mandali_num)
            
            mandali_dict = {
                "number": transit_mandali.number,
                "name": f"Mandali {transit_mandali.number} ({transit_mandali.rasi_name})",
            }
            
            # Determine status from transit_mandali position
            status = "NEUTRAL"
            mandali_num = res.mandali["number"]
            if mandali_num <= 4:
                status = "FAVORABLE"
            elif mandali_num >= 9:
                status = "CHALLENGING"
            
            placements.append(
                CurrentTransitPlanetPlacement(
                    planet=res.planet,
                    # TMR-04: preserve original Canonical JSON rasi/nakshatra/pada
                    rasi=res.original.get("rasi", ""),
                    nakshatra=res.original.get("nakshatra", ""),
                    pada=res.original.get("pada", 0),
                    mandali=mandali_dict,
                    status=status,
                )
            )
        
        return placements


# Convenience function for direct usage
def create_placement_factory() -> MandaliPlacementFactory:
    """Create a MandaliPlacementFactory instance."""
    return MandaliPlacementFactory()
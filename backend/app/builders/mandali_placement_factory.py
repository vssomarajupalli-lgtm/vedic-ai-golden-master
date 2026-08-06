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
        moon_rasi: str,
        moon_nakshatra: str,
        moon_pada: int,
        moon_absolute_pada: int,
        mandali_grid: MandaliGrid,
    ) -> List[NatalPlanetPlacement]:
        """
        Build natal planet placements DTO list.
        
        Args:
            moon_rasi: Natal Moon rasi from canonical JSON
            moon_nakshatra: Natal Moon nakshatra from canonical JSON
            moon_pada: Natal Moon pada from canonical JSON
            moon_absolute_pada: Absolute pada index (1-108) for Moon
            mandali_grid: The constructed MandaliGrid
            
        Returns:
            List of NatalPlanetPlacement DTOs
        """
        # Find the Mandali containing the natal Moon
        natal_mandali_num = mandali_grid.find_mandali_for_pada(moon_absolute_pada)
        natal_mandali = mandali_grid.get_mandali(natal_mandali_num)
        
        mandali_dict = {
            "number": natal_mandali.number,
            "name": f"Mandali {natal_mandali.number} ({natal_mandali.rasi_name})",
        }
        
        return [
            NatalPlanetPlacement(
                planet="Moon",
                rasi=moon_rasi,
                nakshatra=moon_nakshatra,
                pada=moon_pada,
                mandali=mandali_dict,
            )
        ]

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
                    rasi=res.mandali.get("rasi", ""),
                    nakshatra=res.mandali.get("nakshatra", ""),
                    pada=res.mandali.get("pada", 0),
                    mandali=mandali_dict,
                    status=status,
                )
            )
        
        return placements


# Convenience function for direct usage
def create_placement_factory() -> MandaliPlacementFactory:
    """Create a MandaliPlacementFactory instance."""
    return MandaliPlacementFactory()
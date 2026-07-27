"""
TransitMandaliResolution — Capability 7.4
==========================================

Resolves each transit planet's Canonical JSON position to a Mandali number.

Governance Rules (TMR-01 to TMR-05):
- TMR-01: Transit Absolute Pada = NakshatraPadaResolver(transit_nakshatra, transit_pada)
- TMR-02: Transit Mandali = unique Mandali N where Transit Absolute Pada ∈ mandali_grid[N].padas
- TMR-03: Exactly one Mandali contains the transit pada (guaranteed by MGC-05)
- TMR-04: Original Canonical JSON values (rasi, nakshatra, pada) are preserved in output — never modified
- TMR-05: Classical house_from_moon from Canonical JSON is preserved alongside Mandali number

This module performs NO:
- Longitude calculation
- Swiss Ephemeris calls
- Orbital mathematics
- Transit calculation
- Astrology interpretation
- Strength calculation
- Dasha logic
- Report generation
"""

from __future__ import annotations

from typing import Optional
from dataclasses import dataclass

from app.engines.canonical_reference_data import (
    get_canonical_reference_data,
    CanonicalReferenceData,
    RegistryAccessError,
)
from app.engines.nakshatra_pada_resolver import NakshatraPadaResolver
from app.engines.mandali_grid_construction import MandaliGrid, MandaliGridConstruction


@dataclass(frozen=True)
class TransitMandaliResolution:
    """
    Result of resolving a single transit planet to its Mandali.
    
    Output schema per GOCHARA_MANDALI_GOVERNANCE_v1.md Section 7.4
    """
    planet: str
    original: dict  # {"rasi": str, "nakshatra": str, "pada": int}
    mandali: dict   # {"number": int, "name": str, "center_nakshatra": str, "center_pada": int}
    house_from_moon_classical: int
    house_from_moon_mandali: int
    interpretation_ref: str


class TransitMandaliResolver:
    """
    Resolves transit planets to Mandali numbers using Canonical JSON data only.
    
    Stateless, deterministic, no hidden state. All resolution via CanonicalReferenceData.
    """
    
    def __init__(
        self,
        ref_data: Optional[CanonicalReferenceData] = None,
        pada_resolver: Optional[NakshatraPadaResolver] = None,
        grid_constructor: Optional[MandaliGridConstruction] = None,
    ):
        """
        Initialize resolver with dependencies.
        
        Args:
            ref_data: CanonicalReferenceData instance (uses singleton if None)
            pada_resolver: NakshatraPadaResolver instance (creates new if None)
            grid_constructor: MandaliGridConstruction instance (creates new if None)
        """
        self._ref_data = ref_data or get_canonical_reference_data()
        self._pada_resolver = pada_resolver or NakshatraPadaResolver(self._ref_data)
        self._grid_constructor = grid_constructor or MandaliGridConstruction(
            ref_data=self._ref_data, 
            pada_resolver=self._pada_resolver
        )
    
    def resolve_transit_planet(
        self,
        planet: str,
        transit_nakshatra: str,
        transit_pada: int,
        transit_rasi: str,
        house_from_moon: int,
        interpretation: str,
        mandali_grid: MandaliGrid,
    ) -> TransitMandaliResolution:
        """
        Resolve a single transit planet to its Mandali.
        
        Governance Rules:
        - TMR-01: Transit Absolute Pada = NakshatraPadaResolver(transit_nakshatra, transit_pada)
        - TMR-02: Transit Mandali = unique Mandali N where Transit Absolute Pada ∈ mandali_grid[N].padas
        - TMR-03: Exactly one Mandali contains the transit pada (guaranteed by MGC-05)
        - TMR-04: Original Canonical JSON values preserved — never modified
        - TMR-05: Classical house_from_moon preserved alongside Mandali number
        
        Args:
            planet: Planet name (e.g., "Saturn", "Jupiter")
            transit_nakshatra: Transit Nakshatra from Canonical JSON
            transit_pada: Transit Pada (1-4) from Canonical JSON
            transit_rasi: Transit Rasi from Canonical JSON
            house_from_moon: Classical Rasi-house from Moon (1-12) from Canonical JSON
            interpretation: Canonical interpretation text from Canonical JSON
            mandali_grid: MandaliGrid from MandaliGridConstruction
            
        Returns:
            TransitMandaliResolution with all required output fields
            
        Raises:
            RegistryAccessError: If nakshatra/pada not found in registry
            ValueError: If pada not found in any Mandali (should never happen per MGC-05)
        """
        # TMR-01: Transit Absolute Pada = NakshatraPadaResolver(transit_nakshatra, transit_pada)
        transit_absolute_pada = self._pada_resolver.resolve(transit_nakshatra, transit_pada)
        
        # TMR-02: Find Mandali containing this pada
        mandali_number = mandali_grid.find_mandali_for_pada(transit_absolute_pada)
        
        # Get Mandali details
        mandali = mandali_grid.get_mandali(mandali_number)
        
        # TMR-04: Preserve original Canonical JSON values
        original = {
            "rasi": transit_rasi,
            "nakshatra": transit_nakshatra,
            "pada": transit_pada,
        }
        
        # TMR-05: Classical house_from_moon preserved
        house_from_moon_classical = house_from_moon
        
        # Mandali house = Mandali number (1-12)
        house_from_moon_mandali = mandali_number
        
        # Mandali name = "Mandali N"
        mandali_name = f"Mandali {mandali_number}"
        
        mandali_info = {
            "number": mandali_number,
            "name": mandali_name,
            "center_nakshatra": mandali.center_nakshatra,
            "center_pada": mandali.center_pada,
        }
        
        return TransitMandaliResolution(
            planet=planet,
            original=original,
            mandali=mandali_info,
            house_from_moon_classical=house_from_moon_classical,
            house_from_moon_mandali=house_from_moon_mandali,
            interpretation_ref=interpretation,
        )
    
    def resolve_all_transit_planets(
        self,
        transit_planets: list[dict],
        mandali_grid: MandaliGrid,
    ) -> list[TransitMandaliResolution]:
        """
        Resolve all transit planets to their Mandalis.
        
        Args:
            transit_planets: List of transit planet dicts from Canonical JSON
                            Each: {"planet", "rasi", "nakshatra", "pada", "house_from_moon", "interpretation"}
            mandali_grid: MandaliGrid from MandaliGridConstruction
            
        Returns:
            List of TransitMandaliResolution objects
        """
        results = []
        for tp in transit_planets:
            resolution = self.resolve_transit_planet(
                planet=tp["planet"],
                transit_nakshatra=tp["nakshatra"],
                transit_pada=tp["pada"],
                transit_rasi=tp["rasi"],
                house_from_moon=tp["house_from_moon"],
                interpretation=tp["interpretation"],
                mandali_grid=mandali_grid,
            )
            results.append(resolution)
        return results


# Convenience function
def resolve_transit_mandali(
    transit_planets: list[dict],
    mandali_grid: MandaliGrid,
    ref_data: Optional[CanonicalReferenceData] = None,
    pada_resolver: Optional[NakshatraPadaResolver] = None,
    grid_constructor: Optional[MandaliGridConstruction] = None,
) -> list[TransitMandaliResolution]:
    """
    Convenience function to resolve all transit planets to Mandalis.
    
    Args:
        transit_planets: List of transit planet dicts from Canonical JSON
        mandali_grid: MandaliGrid from MandaliGridConstruction
        ref_data: Optional CanonicalReferenceData (uses singleton if None)
        pada_resolver: Optional NakshatraPadaResolver (creates new if None)
        grid_constructor: Optional MandaliGridConstruction (creates new if None)
        
    Returns:
        List of TransitMandaliResolution objects
    """
    resolver = TransitMandaliResolver(
        ref_data=ref_data,
        pada_resolver=pada_resolver,
        grid_constructor=grid_constructor,
    )
    return resolver.resolve_all_transit_planets(transit_planets, mandali_grid)
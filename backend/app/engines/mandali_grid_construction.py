"""
MandaliGridConstruction — Capability 7.3
=========================================

Constructs the 12-Mandali grid centered on the Natal Moon Pada.

Governance Rules (MGC-01 to MGC-07):
- MGC-01: Moon Absolute Pada = NakshatraPadaResolver(natal_moon_nakshatra, natal_moon_pada)
- MGC-02: Mandali 1 center = Moon Absolute Pada
- MGC-03: Mandali N center = ((Moon_Absolute_Pada + (N-1)×9 - 1) mod 108) + 1
- MGC-04: Each Mandali contains exactly 9 padas: center ±4 (modulo 108 wrap)
- MGC-05: All 108 padas covered exactly once across 12 Mandalis (no gaps, no overlaps)
- MGC-06: Mandali Rasi name = Rasi of center pada's Nakshatra (from nakshatra_rasi_registry)
- MGC-07: Output is deterministic: identical inputs → identical grid

This module performs NO:
- Longitude calculation
- Swiss Ephemeris calls
- Orbital mathematics
- Transit calculation
- Astrology interpretation
- Strength calculation
"""

from __future__ import annotations

from typing import Optional
from dataclasses import dataclass
from app.engines.canonical_reference_data import (
    get_canonical_reference_data,
    CanonicalReferenceData,
    NakshatraPadaEntry,
)
from app.engines.nakshatra_pada_resolver import NakshatraPadaResolver


@dataclass(frozen=True)
class Mandali:
    """Single Mandali in the 12-Mandali grid."""
    number: int                    # 1-12
    center_pada: int               # 1-108
    center_nakshatra: str          # e.g., "Dhanishta"
    center_pada_num: int           # 1-4
    rasi_name: str                 # e.g., "Makara"
    padas: tuple[int, ...]         # 9 absolute pada indices
    pada_details: tuple[NakshatraPadaEntry, ...]  # Full details for each pada


@dataclass(frozen=True)
class MandaliGrid:
    """Complete 12-Mandali grid centered on Natal Moon."""
    mandalis: tuple[Mandali, ...]  # 12 Mandalis, index 0 = Mandali 1
    moon_absolute_pada: int        # 1-108
    moon_nakshatra: str
    moon_pada: int
    moon_rasi: str
    
    def get_mandali(self, mandali_number: int) -> Mandali:
        """Get Mandali by number (1-12)."""
        if not 1 <= mandali_number <= 12:
            raise ValueError(f"mandali_number must be 1-12, got {mandali_number}")
        return self.mandalis[mandali_number - 1]
    
    def find_mandali_for_pada(self, absolute_pada: int) -> int:
        """Find which Mandali contains the given absolute pada."""
        for mandali in self.mandalis:
            if absolute_pada in mandali.padas:
                return mandali.number
        raise ValueError(f"Pada {absolute_pada} not found in any Mandali")


class MandaliGridConstruction:
    """
    Constructs the 12-Mandali grid centered on the Natal Moon.
    
    Governance Rules (MGC-01 to MGC-07):
    - MGC-01: Moon Absolute Pada from NakshatraPadaResolver
    - MGC-02: Mandali 1 center = Moon Absolute Pada
    - MGC-03: Mandali N center = ((Moon + (N-1)*9 - 1) mod 108) + 1
    - MGC-04: Each Mandali = 9 padas (center ±4, modulo 108)
    - MGC-05: All 108 padas covered exactly once
    - MGC-06: Mandali Rasi = Rasi of center pada's Nakshatra
    - MGC-07: Deterministic output
    """
    
    def __init__(
        self,
        ref_data: Optional[CanonicalReferenceData] = None,
        pada_resolver: Optional[NakshatraPadaResolver] = None,
    ):
        """
        Initialize with CanonicalReferenceData and NakshatraPadaResolver.
        
        Args:
            ref_data: CanonicalReferenceData instance (uses singleton if None)
            pada_resolver: NakshatraPadaResolver instance (creates new if None)
        """
        self._ref_data = ref_data or get_canonical_reference_data()
        self._pada_resolver = pada_resolver or NakshatraPadaResolver(self._ref_data)
    
    def build_grid(
        self,
        natal_moon_nakshatra: str,
        natal_moon_pada: int,
    ) -> MandaliGrid:
        """
        Build the complete 12-Mandali grid centered on Natal Moon.
        
        Governance Rules:
        - MGC-01: Moon Absolute Pada = NakshatraPadaResolver(nakshatra, pada)
        - MGC-02: Mandali 1 center = Moon Absolute Pada
        - MGC-03: Mandali N center = ((Moon + (N-1)*9 - 1) mod 108) + 1
        - MGC-04: Each Mandali = 9 padas (center ±4, modulo 108)
        - MGC-05: All 108 padas covered exactly once
        - MGC-06: Mandali Rasi = Rasi of center pada's Nakshatra
        - MGC-07: Deterministic output
        
        Args:
            natal_moon_nakshatra: Moon's Nakshatra from Canonical JSON
            natal_moon_pada: Moon's Pada (1-4) from Canonical JSON
            
        Returns:
            MandaliGrid with 12 Mandalis
            
        Raises:
            RegistryAccessError: If nakshatra/pada not found in registry
        """
        # MGC-01: Moon Absolute Pada
        moon_absolute_pada = self._pada_resolver.resolve(natal_moon_nakshatra, natal_moon_pada)
        
        # Get Moon's Rasi from registry
        moon_rasi = self._ref_data.get_rasi(natal_moon_nakshatra, natal_moon_pada)
        
        mandalis = []
        
        for n in range(1, 13):
            # MGC-03: Mandali N center
            center_pada = ((moon_absolute_pada + (n - 1) * 9 - 1) % 108) + 1
            
            # MGC-04: 9 padas (center ±4, modulo 108 wrap)
            padas = []
            for offset in range(-4, 5):
                p = ((center_pada + offset - 1) % 108) + 1
                padas.append(p)
            
            # Get center pada details
            center_entry = self._ref_data.get_pada_entry(center_pada)
            center_nakshatra = center_entry.nakshatra
            center_pada_num = center_entry.pada
            
            # MGC-06: Mandali Rasi = Rasi of center pada's Nakshatra
            rasi_name = self._ref_data.get_rasi(center_nakshatra, center_pada_num)
            
            # Get full pada details for all 9 padas
            pada_details = tuple(self._ref_data.get_pada_entry(p) for p in padas)
            
            mandali = Mandali(
                number=n,
                center_pada=center_pada,
                center_nakshatra=center_nakshatra,
                center_pada_num=center_pada_num,
                rasi_name=rasi_name,
                padas=tuple(padas),
                pada_details=pada_details,
            )
            mandalis.append(mandali)
        
        # MGC-05: Verify all 108 padas covered exactly once (deterministic check)
        self._verify_grid_integrity(mandalis)
        
        return MandaliGrid(
            mandalis=tuple(mandalis),
            moon_absolute_pada=moon_absolute_pada,
            moon_nakshatra=natal_moon_nakshatra,
            moon_pada=natal_moon_pada,
            moon_rasi=moon_rasi,
        )
    
    def _verify_grid_integrity(self, mandalis: list[Mandali]) -> None:
        """
        Verify MGC-05: All 108 padas covered exactly once, no gaps, no overlaps.
        
        This is a deterministic verification that always passes for valid inputs.
        """
        all_padas = []
        for mandali in mandalis:
            all_padas.extend(mandali.padas)
        
        # Check count
        if len(all_padas) != 108:
            raise ValueError(f"Grid has {len(all_padas)} padas, expected 108")
        
        # Check no duplicates
        if len(set(all_padas)) != 108:
            raise ValueError("Grid has duplicate padas")
        
        # Check all 1-108 present
        if set(all_padas) != set(range(1, 109)):
            raise ValueError("Grid missing some padas or has out-of-range padas")
        
        # Check each mandali has exactly 9 padas
        for mandali in mandalis:
            if len(mandali.padas) != 9:
                raise ValueError(f"Mandali {mandali.number} has {len(mandali.padas)} padas, expected 9")
        
        # Check mandali centers are 9 apart
        for i in range(11):
            diff = (mandalis[i + 1].center_pada - mandalis[i].center_pada) % 108
            if diff != 9:
                raise ValueError(f"Mandali centers not 9 apart: {mandalis[i].number} to {mandalis[i+1].number} diff={diff}")


# Convenience function
def build_mandali_grid(
    natal_moon_nakshatra: str,
    natal_moon_pada: int,
    ref_data: Optional[CanonicalReferenceData] = None,
    pada_resolver: Optional[NakshatraPadaResolver] = None,
) -> MandaliGrid:
    """
    Convenience function to build Mandali grid.
    
    Args:
        natal_moon_nakshatra: Moon's Nakshatra from Canonical JSON
        natal_moon_pada: Moon's Pada (1-4) from Canonical JSON
        ref_data: Optional CanonicalReferenceData (uses singleton if None)
        pada_resolver: Optional NakshatraPadaResolver (creates new if None)
        
    Returns:
        MandaliGrid with 12 Mandalis
    """
    constructor = MandaliGridConstruction(ref_data=ref_data, pada_resolver=pada_resolver)
    return constructor.build_grid(natal_moon_nakshatra, natal_moon_pada)
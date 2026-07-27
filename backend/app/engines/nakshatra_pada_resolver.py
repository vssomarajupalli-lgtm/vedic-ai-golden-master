"""
NakshatraPadaResolver — Capability 7.2
=======================================

Resolves (Nakshatra, Pada) → Absolute Pada (1-108) using only CanonicalReferenceData.

Governance Rules (NPR-01 to NPR-05):
- NPR-01: Input: nakshatra (string), pada (1-4) from Canonical JSON
- NPR-02: Lookup in nakshatra_pada_registry — exact match required
- NPR-03: Output: absolute pada index (1-108)
- NPR-04: No longitude input; no trigonometric calculation
- NPR-05: Missing nakshatra/pada in registry → hard error

This module performs NO:
- Longitude calculation
- Swiss Ephemeris calls
- Orbital mathematics
- Mandali calculation
- Transit calculation
- Astrology interpretation
- Strength calculation
- Rasi computation outside registry lookups
"""

from __future__ import annotations

from typing import Optional
from app.engines.canonical_reference_data import (
    get_canonical_reference_data,
    CanonicalReferenceData,
    RegistryAccessError,
)


class NakshatraPadaResolver:
    """
    Resolves (Nakshatra, Pada) to Absolute Pada (1-108) using CanonicalReferenceData.
    
    Stateless, deterministic, no hidden state. All resolution via CanonicalReferenceData.
    """
    
    def __init__(self, ref_data: Optional[CanonicalReferenceData] = None):
        """
        Initialize resolver with CanonicalReferenceData instance.
        
        Args:
            ref_data: CanonicalReferenceData instance. If None, uses singleton.
        """
        self._ref_data = ref_data or get_canonical_reference_data()
    
    def resolve(self, nakshatra: str, pada: int) -> int:
        """
        Resolve (Nakshatra, Pada) to Absolute Pada (1-108).
        
        Governance Rules:
        - NPR-01: Input from Canonical JSON (nakshatra string, pada 1-4)
        - NPR-02: Exact match lookup in nakshatra_pada_registry
        - NPR-03: Output absolute pada index (1-108)
        - NPR-04: No longitude, no trigonometry
        - NPR-05: Missing nakshatra/pada → hard error (RegistryAccessError)
        
        Args:
            nakshatra: Nakshatra name (e.g., "Dhanishta")
            pada: Pada number (1-4)
            
        Returns:
            Absolute pada index (1-108)
            
        Raises:
            RegistryAccessError: If nakshatra/pada not found in registry
        """
        # NPR-04: No longitude, no trigonometry
        # NPR-05: Validate pada type and range before registry lookup
        if not isinstance(pada, int):
            raise RegistryAccessError(f"pada must be integer, got {type(pada).__name__}")
        if not 1 <= pada <= 4:
            raise RegistryAccessError(f"pada must be 1-4, got {pada}")
        # NPR-01, NPR-02: Direct registry lookup
        return self._ref_data.get_absolute_pada(nakshatra, pada)
    
    def resolve_batch(self, nakshatra_pada_pairs: list[tuple[str, int]]) -> list[int]:
        """
        Resolve multiple (Nakshatra, Pada) pairs to absolute padas.
        
        Args:
            nakshatra_pada_pairs: List of (nakshatra, pada) tuples
            
        Returns:
            List of absolute pada indices (1-108)
        """
        return [self.resolve(nakshatra, pada) for nakshatra, pada in nakshatra_pada_pairs]
    
    def get_nakshatra_pada(self, absolute_pada: int) -> tuple[str, int]:
        """
        Reverse lookup: Absolute Pada → (Nakshatra, Pada).
        
        Args:
            absolute_pada: Absolute pada index (1-108)
            
        Returns:
            Tuple of (nakshatra_name, pada_number)
        """
        return self._ref_data.get_nakshatra_pada(absolute_pada)
    
    def validate_all_padas(self) -> bool:
        """
        Validate all 108 padas resolve correctly.
        
        Returns:
            True if all validations pass
            
        Raises:
            AssertionError: If any validation fails
        """
        ref_data = self._ref_data
        
        # Check all 108 padas
        for absolute_pada in range(1, 109):
            nakshatra, pada = ref_data.get_nakshatra_pada(absolute_pada)
            resolved = self.resolve(nakshatra, pada)
            assert resolved == absolute_pada, f"Round-trip failed for {absolute_pada}: {nakshatra} P{pada} → {resolved}"
        
        # Check each nakshatra has exactly 4 padas
        for nakshatra in ref_data.get_all_nakshatras():
            count = 0
            for pada in range(1, 5):
                try:
                    self.resolve(nakshatra, pada)
                    count += 1
                except RegistryAccessError:
                    pass
            assert count == 4, f"Nakshatra {nakshatra} has {count} valid padas, expected 4"
        
        return True


# Convenience function for direct use
def resolve_nakshatra_pada(nakshatra: str, pada: int) -> int:
    """
    Convenience function to resolve (Nakshatra, Pada) → Absolute Pada.
    
    Uses singleton CanonicalReferenceData.
    
    Args:
        nakshatra: Nakshatra name
        pada: Pada number (1-4)
        
    Returns:
        Absolute pada index (1-108)
    """
    resolver = NakshatraPadaResolver()
    return resolver.resolve(nakshatra, pada)
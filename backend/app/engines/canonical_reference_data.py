"""
CanonicalReferenceData — Registry Loader for Universal Gochara Mandali Model A
=============================================================================

Loads and validates canonical reference data registries per
GOCHARA_MANDALI_GOVERNANCE_v1.md Section 6 and Capability 7.1.

Governance Rules (CRD-01 to CRD-04):
- CRD-01: Registries loaded once at startup; never modified at runtime
- CRD-02: Registries versioned; engine declares required registry version
- CRD-03: Missing or mismatched registry version → hard error (fail-fast)
- CRD-04: No engine embeds registry data; all access via this capability

This module performs NO astrology calculations, NO Mandali calculations,
NO transit logic, NO interpretation logic, NO engine integration.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

REGISTRY_DIR = Path(__file__).parent.parent / "config"

REQUIRED_REGISTRIES = {
    "nakshatra_pada_registry": {
        "filename": "nakshatra_pada_registry.json",
        "required_version": "1.0",
        "required_keys": ["registry_id", "version", "entries"],
        "entry_count": 108,
    },
    "nakshatra_rasi_registry": {
        "filename": "nakshatra_rasi_registry.json",
        "required_version": "1.0",
        "required_keys": ["registry_id", "version", "mappings"],
        "entry_count": 108,
    },
    "rasi_sequence_registry": {
        "filename": "rasi_sequence_registry.json",
        "required_version": "1.0",
        "required_keys": ["registry_id", "version", "sequence"],
        "entry_count": 12,
    },
}


# -----------------------------------------------------------------------------
# Exceptions
# -----------------------------------------------------------------------------

class RegistryError(Exception):
    """Base exception for registry errors."""
    pass


class RegistryNotFoundError(RegistryError):
    """Registry file not found."""
    pass


class RegistryVersionMismatchError(RegistryError):
    """Registry version does not match required version."""
    pass


class RegistryIntegrityError(RegistryError):
    """Registry data fails integrity validation."""
    pass


class RegistryAccessError(RegistryError):
    """Error accessing registry data."""
    pass


# -----------------------------------------------------------------------------
# Data Classes
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class NakshatraPadaEntry:
    """Single entry in nakshatra_pada_registry."""
    absolute_pada: int
    nakshatra: str
    pada: int


@dataclass(frozen=True)
class NakshatraRasiMapping:
    """Single entry in nakshatra_rasi_registry."""
    nakshatra: str
    pada: int
    rasi: str


@dataclass
class CanonicalReferenceData:
    """
    Immutable container for all canonical reference data.
    
    Loaded once at startup. All access is read-only.
    """
    # Registry metadata
    nakshatra_pada_version: str
    nakshatra_rasi_version: str
    rasi_sequence_version: str
    
    # Nakshatra-Pada Registry (108 entries)
    _pada_entries: List[NakshatraPadaEntry] = field(repr=False)
    _rasi_mappings: List[NakshatraRasiMapping] = field(repr=False)
    _rasi_sequence: List[str] = field(repr=False)
    
    # Lookup indices (built in __post_init__)
    _pada_by_absolute: Dict[int, NakshatraPadaEntry] = field(repr=False, default_factory=dict)
    _pada_by_nakshatra_pada: Dict[Tuple[str, int], NakshatraPadaEntry] = field(repr=False, default_factory=dict)
    _rasi_by_nakshatra_pada: Dict[Tuple[str, int], str] = field(repr=False, default_factory=dict)
    _nakshatras: set = field(repr=False, default_factory=set)
    _rasis: set = field(repr=False, default_factory=set)
    _rasi_to_index: Dict[str, int] = field(repr=False, default_factory=dict)
    
    def __post_init__(self):
        """Build lookup indices after initialization."""
        # Build pada lookup indices
        for entry in self._pada_entries:
            self._pada_by_absolute[entry.absolute_pada] = entry
            self._pada_by_nakshatra_pada[(entry.nakshatra, entry.pada)] = entry
        
        # Build rasi lookup indices
        for mapping in self._rasi_mappings:
            self._rasi_by_nakshatra_pada[(mapping.nakshatra, mapping.pada)] = mapping.rasi
            self._nakshatras.add(mapping.nakshatra)
            self._rasis.add(mapping.rasi)
        
        # Build rasi sequence index
        for idx, rasi in enumerate(self._rasi_sequence):
            self._rasi_to_index[rasi] = idx
    
    # -------------------------------------------------------------------------
    # Nakshatra-Pada Access Methods
    # -------------------------------------------------------------------------
    
    def get_pada_entry(self, absolute_pada: int) -> NakshatraPadaEntry:
        """
        Get nakshatra and pada for an absolute pada index (1-108).
        
        Args:
            absolute_pada: Absolute pada index (1-108)
            
        Returns:
            NakshatraPadaEntry with nakshatra and pada
            
        Raises:
            RegistryAccessError: If absolute_pada not in 1-108
        """
        if not 1 <= absolute_pada <= 108:
            raise RegistryAccessError(f"absolute_pada must be 1-108, got {absolute_pada}")
        entry = self._pada_by_absolute.get(absolute_pada)
        if entry is None:
            raise RegistryAccessError(f"No entry for absolute_pada={absolute_pada}")
        return entry
    
    def get_absolute_pada(self, nakshatra: str, pada: int) -> int:
        """
        Get absolute pada index (1-108) for a nakshatra and pada.
        
        Args:
            nakshatra: Nakshatra name (e.g., "Dhanishta")
            pada: Pada number (1-4)
            
        Returns:
            Absolute pada index (1-108)
            
        Raises:
            RegistryAccessError: If nakshatra/pada combination not found
        """
        if not 1 <= pada <= 4:
            raise RegistryAccessError(f"pada must be 1-4, got {pada}")
        entry = self._pada_by_nakshatra_pada.get((nakshatra, pada))
        if entry is None:
            raise RegistryAccessError(f"No entry for nakshatra={nakshatra}, pada={pada}")
        return entry.absolute_pada
    
    def get_nakshatra_pada(self, absolute_pada: int) -> Tuple[str, int]:
        """
        Get (nakshatra, pada) tuple for an absolute pada index.
        
        Args:
            absolute_pada: Absolute pada index (1-108)
            
        Returns:
            Tuple of (nakshatra_name, pada_number)
        """
        entry = self.get_pada_entry(absolute_pada)
        return (entry.nakshatra, entry.pada)
    
    def get_all_pada_entries(self) -> List[NakshatraPadaEntry]:
        """Get all 108 pada entries in absolute order."""
        return list(self._pada_entries)
    
    # -------------------------------------------------------------------------
    # Nakshatra-Rasi Access Methods
    # -------------------------------------------------------------------------
    
    def get_rasi(self, nakshatra: str, pada: int) -> str:
        """
        Get rasi for a nakshatra and pada.
        
        Args:
            nakshatra: Nakshatra name
            pada: Pada number (1-4)
            
        Returns:
            Rasi name (e.g., "Makara")
            
        Raises:
            RegistryAccessError: If combination not found
        """
        if not 1 <= pada <= 4:
            raise RegistryAccessError(f"pada must be 1-4, got {pada}")
        rasi = self._rasi_by_nakshatra_pada.get((nakshatra, pada))
        if rasi is None:
            raise RegistryAccessError(f"No rasi mapping for nakshatra={nakshatra}, pada={pada}")
        return rasi
    
    def get_all_nakshatras(self) -> List[str]:
        """Get sorted list of all 27 nakshatras."""
        return sorted(self._nakshatras)
    
    def get_all_rasis(self) -> List[str]:
        """Get sorted list of all 12 rasis."""
        return sorted(self._rasis)
    
    # -------------------------------------------------------------------------
    # Rasi Sequence Access Methods
    # -------------------------------------------------------------------------
    
    def get_rasi_sequence(self) -> List[str]:
        """Get the 12 rasis in zodiacal order."""
        return list(self._rasi_sequence)
    
    def get_rasi_index(self, rasi: str) -> int:
        """
        Get 0-based index of rasi in zodiacal sequence.
        
        Args:
            rasi: Rasi name
            
        Returns:
            Index 0-11
            
        Raises:
            RegistryAccessError: If rasi not found
        """
        idx = self._rasi_to_index.get(rasi)
        if idx is None:
            raise RegistryAccessError(f"Rasi not found in sequence: {rasi}")
        return idx
    
    def get_next_rasi(self, rasi: str) -> str:
        """Get next rasi in zodiacal order (wraps)."""
        idx = self.get_rasi_index(rasi)
        return self._rasi_sequence[(idx + 1) % 12]
    
    def get_previous_rasi(self, rasi: str) -> str:
        """Get previous rasi in zodiacal order (wraps)."""
        idx = self.get_rasi_index(rasi)
        return self._rasi_sequence[(idx - 1) % 12]
    
    def get_rasi_offset(self, from_rasi: str, to_rasi: str) -> int:
        """
        Get offset from from_rasi to to_rasi (0-11).
        
        Args:
            from_rasi: Starting rasi
            to_rasi: Target rasi
            
        Returns:
            Offset (0-11) where 0 = same rasi
        """
        from_idx = self.get_rasi_index(from_rasi)
        to_idx = self.get_rasi_index(to_rasi)
        return (to_idx - from_idx) % 12
    
    # -------------------------------------------------------------------------
    # Validation & Metadata
    # -------------------------------------------------------------------------
    
    def validate_integrity(self) -> bool:
        """
        Validate all registry integrity constraints.
        
        Returns:
            True if all validations pass
            
        Raises:
            RegistryIntegrityError: If any validation fails
        """
        # Check pada registry
        if len(self._pada_entries) != 108:
            raise RegistryIntegrityError(f"Expected 108 pada entries, got {len(self._pada_entries)}")
        
        # Check continuous 1-108
        expected_padas = set(range(1, 109))
        actual_padas = set(self._pada_by_absolute.keys())
        if actual_padas != expected_padas:
            missing = expected_padas - actual_padas
            extra = actual_padas - expected_padas
            raise RegistryIntegrityError(f"Pada ID mismatch. Missing: {missing}, Extra: {extra}")
        
        # Check 27 nakshatras × 4 padas
        if len(self._nakshatras) != 27:
            raise RegistryIntegrityError(f"Expected 27 nakshatras, got {len(self._nakshatras)}")
        
        for nakshatra in self._nakshatras:
            count = sum(1 for e in self._pada_entries if e.nakshatra == nakshatra)
            if count != 4:
                raise RegistryIntegrityError(f"Nakshatra {nakshatra} has {count} padas, expected 4")
        
        # Check rasi registry
        if len(self._rasi_mappings) != 108:
            raise RegistryIntegrityError(f"Expected 108 rasi mappings, got {len(self._rasi_mappings)}")
        
        # Check all nakshatra-pada pairs have rasi mapping
        for entry in self._pada_entries:
            key = (entry.nakshatra, entry.pada)
            if key not in self._rasi_by_nakshatra_pada:
                raise RegistryIntegrityError(f"Missing rasi mapping for {key}")
        
        # Check rasi sequence
        if len(self._rasi_sequence) != 12:
            raise RegistryIntegrityError(f"Expected 12 rasis in sequence, got {len(self._rasi_sequence)}")
        
        expected_sequence = [
            "Mesha", "Vrishabha", "Mithuna", "Karkata", "Simha", "Kanya",
            "Tula", "Vrishchika", "Dhanus", "Makara", "Kumbha", "Meena"
        ]
        if self._rasi_sequence != expected_sequence:
            raise RegistryIntegrityError(f"Rasi sequence mismatch. Expected {expected_sequence}, got {self._rasi_sequence}")
        
        # Check all rasis in sequence are in rasi set
        if set(self._rasi_sequence) != self._rasis:
            raise RegistryIntegrityError(f"Rasi sequence set mismatch. Sequence: {set(self._rasi_sequence)}, Mappings: {self._rasis}")
        
        return True


# -----------------------------------------------------------------------------
# Loader Function
# -----------------------------------------------------------------------------

def load_canonical_reference_data(
    registry_dir: Optional[Path] = None,
    required_versions: Optional[Dict[str, str]] = None
) -> CanonicalReferenceData:
    """
    Load and validate all canonical reference registries.
    
    This is the single entry point for loading reference data.
    Called once at application startup.
    
    Args:
        registry_dir: Directory containing registry JSON files.
                      Defaults to backend/app/config/
        required_versions: Optional dict overriding required versions.
        
    Returns:
        CanonicalReferenceData instance with all registries loaded and validated.
        
    Raises:
        RegistryNotFoundError: If any registry file is missing
        RegistryVersionMismatchError: If registry version doesn't match required
        RegistryIntegrityError: If registry data fails integrity checks
    """
    if registry_dir is None:
        registry_dir = REGISTRY_DIR
    
    if required_versions is None:
        required_versions = {k: v["required_version"] for k, v in REQUIRED_REGISTRIES.items()}
    
    # Load all three registries
    registries = {}
    for registry_id, config in REQUIRED_REGISTRIES.items():
        file_path = registry_dir / config["filename"]
        
        if not file_path.exists():
            raise RegistryNotFoundError(f"Registry file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise RegistryIntegrityError(f"Invalid JSON in {file_path}: {e}")
        
        # Validate required keys
        for key in config["required_keys"]:
            if key not in data:
                raise RegistryIntegrityError(f"Registry {registry_id} missing required key: {key}")
        
        # Validate version
        actual_version = data.get("version")
        required_version = required_versions.get(registry_id, config["required_version"])
        if actual_version != required_version:
            raise RegistryVersionMismatchError(
                f"Registry {registry_id} version mismatch. "
                f"Required: {required_version}, Found: {actual_version}"
            )
        
        # Validate entry count
        entry_key = "entries" if "entries" in data else ("mappings" if "mappings" in data else "sequence")
        actual_count = len(data[entry_key])
        expected_count = config["entry_count"]
        if actual_count != expected_count:
            raise RegistryIntegrityError(
                f"Registry {registry_id} entry count mismatch. "
                f"Expected: {expected_count}, Found: {actual_count}"
            )
        
        registries[registry_id] = data
    
    # Build CanonicalReferenceData object
    # Nakshatra-Pada Registry
    pada_entries = [
        NakshatraPadaEntry(
            absolute_pada=e["absolute_pada"],
            nakshatra=e["nakshatra"],
            pada=e["pada"]
        )
        for e in registries["nakshatra_pada_registry"]["entries"]
    ]
    
    # Nakshatra-Rasi Registry
    rasi_mappings = [
        NakshatraRasiMapping(
            nakshatra=m["nakshatra"],
            pada=m["pada"],
            rasi=m["rasi"]
        )
        for m in registries["nakshatra_rasi_registry"]["mappings"]
    ]
    
    # Rasi Sequence Registry
    rasi_sequence = registries["rasi_sequence_registry"]["sequence"]
    
    # Create container
    ref_data = CanonicalReferenceData(
        nakshatra_pada_version=registries["nakshatra_pada_registry"]["version"],
        nakshatra_rasi_version=registries["nakshatra_rasi_registry"]["version"],
        rasi_sequence_version=registries["rasi_sequence_registry"]["version"],
        _pada_entries=pada_entries,
        _rasi_mappings=rasi_mappings,
        _rasi_sequence=rasi_sequence,
    )
    
    # Validate integrity
    ref_data.validate_integrity()
    
    return ref_data


# -----------------------------------------------------------------------------
# Singleton Access (for convenience)
# -----------------------------------------------------------------------------

_canonical_instance: Optional[CanonicalReferenceData] = None


def get_canonical_reference_data() -> CanonicalReferenceData:
    """
    Get singleton instance of CanonicalReferenceData.
    
    Loads on first call, returns cached instance thereafter.
    Implements CRD-01: loaded once at startup, never modified.
    
    Returns:
        CanonicalReferenceData instance
    """
    global _canonical_instance
    if _canonical_instance is None:
        _canonical_instance = load_canonical_reference_data()
    return _canonical_instance


def reset_canonical_reference_data() -> None:
    """
    Reset singleton instance (for testing only).
    
    WARNING: Only use in test environments.
    """
    global _canonical_instance
    _canonical_instance = None
"""
Unit tests for CanonicalReferenceData loader.
Tests governance rules CRD-01 to CRD-04 and all access methods.
"""

import unittest
import tempfile
import json
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.engines.canonical_reference_data import (
    load_canonical_reference_data,
    get_canonical_reference_data,
    reset_canonical_reference_data,
    CanonicalReferenceData,
    RegistryNotFoundError,
    RegistryVersionMismatchError,
    RegistryIntegrityError,
    RegistryAccessError,
    REQUIRED_REGISTRIES,
)


class TestCanonicalReferenceData(unittest.TestCase):
    """Test CanonicalReferenceData loading and access methods."""
    
    def setUp(self):
        """Reset singleton before each test."""
        reset_canonical_reference_data()
    
    def tearDown(self):
        """Reset singleton after each test."""
        reset_canonical_reference_data()
    
    def test_load_default_registries(self):
        """Test loading registries from default location."""
        ref_data = load_canonical_reference_data()
        
        # Check versions
        self.assertEqual(ref_data.nakshatra_pada_version, "1.0")
        self.assertEqual(ref_data.nakshatra_rasi_version, "1.0")
        self.assertEqual(ref_data.rasi_sequence_version, "1.0")
        
        # Check entry counts
        self.assertEqual(len(ref_data._pada_entries), 108)
        self.assertEqual(len(ref_data._rasi_mappings), 108)
        self.assertEqual(len(ref_data._rasi_sequence), 12)
    
    def test_singleton_behavior(self):
        """Test singleton returns same instance (CRD-01)."""
        ref1 = get_canonical_reference_data()
        ref2 = get_canonical_reference_data()
        self.assertIs(ref1, ref2)
    
    def test_get_pada_entry(self):
        """Test get_pada_entry access method."""
        ref_data = get_canonical_reference_data()
        
        # Test first pada
        entry = ref_data.get_pada_entry(1)
        self.assertEqual(entry.absolute_pada, 1)
        self.assertEqual(entry.nakshatra, "Ashwini")
        self.assertEqual(entry.pada, 1)
        
        # Test last pada
        entry = ref_data.get_pada_entry(108)
        self.assertEqual(entry.absolute_pada, 108)
        self.assertEqual(entry.nakshatra, "Revati")
        self.assertEqual(entry.pada, 4)
        
        # Test middle pada (Dhanishta Pada 2 = 90)
        entry = ref_data.get_pada_entry(90)
        self.assertEqual(entry.absolute_pada, 90)
        self.assertEqual(entry.nakshatra, "Dhanishta")
        self.assertEqual(entry.pada, 2)
    
    def test_get_pada_entry_invalid(self):
        """Test get_pada_entry with invalid input."""
        ref_data = get_canonical_reference_data()
        
        with self.assertRaises(RegistryAccessError):
            ref_data.get_pada_entry(0)
        
        with self.assertRaises(RegistryAccessError):
            ref_data.get_pada_entry(109)
        
        with self.assertRaises(RegistryAccessError):
            ref_data.get_pada_entry(-1)
    
    def test_get_absolute_pada(self):
        """Test get_absolute_pada access method."""
        ref_data = get_canonical_reference_data()
        
        # Test Ashwini Pada 1
        pada = ref_data.get_absolute_pada("Ashwini", 1)
        self.assertEqual(pada, 1)
        
        # Test Ashwini Pada 4
        pada = ref_data.get_absolute_pada("Ashwini", 4)
        self.assertEqual(pada, 4)
        
        # Test Dhanishta Pada 2 (Raju chart Moon)
        pada = ref_data.get_absolute_pada("Dhanishta", 2)
        self.assertEqual(pada, 90)
        
        # Test Revati Pada 4
        pada = ref_data.get_absolute_pada("Revati", 4)
        self.assertEqual(pada, 108)
    
    def test_get_absolute_pada_invalid(self):
        """Test get_absolute_pada with invalid input."""
        ref_data = get_canonical_reference_data()
        
        with self.assertRaises(RegistryAccessError):
            ref_data.get_absolute_pada("Ashwini", 0)
        
        with self.assertRaises(RegistryAccessError):
            ref_data.get_absolute_pada("Ashwini", 5)
        
        with self.assertRaises(RegistryAccessError):
            ref_data.get_absolute_pada("InvalidNakshatra", 1)
    
    def test_get_nakshatra_pada(self):
        """Test get_nakshatra_pada access method."""
        ref_data = get_canonical_reference_data()
        
        nakshatra, pada = ref_data.get_nakshatra_pada(1)
        self.assertEqual(nakshatra, "Ashwini")
        self.assertEqual(pada, 1)
        
        nakshatra, pada = ref_data.get_nakshatra_pada(90)
        self.assertEqual(nakshatra, "Dhanishta")
        self.assertEqual(pada, 2)
        
        nakshatra, pada = ref_data.get_nakshatra_pada(108)
        self.assertEqual(nakshatra, "Revati")
        self.assertEqual(pada, 4)
    
    def test_get_rasi(self):
        """Test get_rasi access method."""
        ref_data = get_canonical_reference_data()
        
        # Test nakshatras within single rasi
        self.assertEqual(ref_data.get_rasi("Ashwini", 1), "Mesha")
        self.assertEqual(ref_data.get_rasi("Ashwini", 4), "Mesha")
        self.assertEqual(ref_data.get_rasi("Bharani", 1), "Mesha")
        self.assertEqual(ref_data.get_rasi("Rohini", 1), "Vrishabha")
        
        # Test nakshatras spanning rasi boundaries
        # Krittika: Pada 1=Mesha, Pada 2-4=Vrishabha
        self.assertEqual(ref_data.get_rasi("Krittika", 1), "Mesha")
        self.assertEqual(ref_data.get_rasi("Krittika", 2), "Vrishabha")
        self.assertEqual(ref_data.get_rasi("Krittika", 3), "Vrishabha")
        self.assertEqual(ref_data.get_rasi("Krittika", 4), "Vrishabha")
        
        # Mrigashira: Pada 1-2=Vrishabha, Pada 3-4=Mithuna
        self.assertEqual(ref_data.get_rasi("Mrigashira", 1), "Vrishabha")
        self.assertEqual(ref_data.get_rasi("Mrigashira", 2), "Vrishabha")
        self.assertEqual(ref_data.get_rasi("Mrigashira", 3), "Mithuna")
        self.assertEqual(ref_data.get_rasi("Mrigashira", 4), "Mithuna")
        
        # Punarvasu: Pada 1-3=Mithuna, Pada 4=Karkata
        self.assertEqual(ref_data.get_rasi("Punarvasu", 1), "Mithuna")
        self.assertEqual(ref_data.get_rasi("Punarvasu", 3), "Mithuna")
        self.assertEqual(ref_data.get_rasi("Punarvasu", 4), "Karkata")
        
        # Dhanishta: Pada 1-2=Makara, Pada 3-4=Kumbha
        self.assertEqual(ref_data.get_rasi("Dhanishta", 1), "Makara")
        self.assertEqual(ref_data.get_rasi("Dhanishta", 2), "Makara")
        self.assertEqual(ref_data.get_rasi("Dhanishta", 3), "Kumbha")
        self.assertEqual(ref_data.get_rasi("Dhanishta", 4), "Kumbha")
    
    def test_get_rasi_invalid(self):
        """Test get_rasi with invalid input."""
        ref_data = get_canonical_reference_data()
        
        with self.assertRaises(RegistryAccessError):
            ref_data.get_rasi("Ashwini", 0)
        
        with self.assertRaises(RegistryAccessError):
            ref_data.get_rasi("Ashwini", 5)
        
        with self.assertRaises(RegistryAccessError):
            ref_data.get_rasi("InvalidNakshatra", 1)
    
    def test_get_all_nakshatras(self):
        """Test get_all_nakshatras returns 27 sorted nakshatras."""
        ref_data = get_canonical_reference_data()
        nakshatras = ref_data.get_all_nakshatras()
        
        self.assertEqual(len(nakshatras), 27)
        self.assertEqual(nakshatras, sorted(nakshatras))
        
        # Check first and last
        self.assertEqual(nakshatras[0], "Anuradha")  # Alphabetically first
        self.assertEqual(nakshatras[-1], "Vishakha")  # Alphabetically last
    
    def test_get_all_rasis(self):
        """Test get_all_rasis returns 12 sorted rasis."""
        ref_data = get_canonical_reference_data()
        rasis = ref_data.get_all_rasis()
        
        self.assertEqual(len(rasis), 12)
        self.assertEqual(rasis, sorted(rasis))
    
    def test_get_rasi_sequence(self):
        """Test get_rasi_sequence returns correct zodiacal order."""
        ref_data = get_canonical_reference_data()
        sequence = ref_data.get_rasi_sequence()
        
        expected = [
            "Mesha", "Vrishabha", "Mithuna", "Karkata", "Simha", "Kanya",
            "Tula", "Vrishchika", "Dhanus", "Makara", "Kumbha", "Meena"
        ]
        self.assertEqual(sequence, expected)
    
    def test_get_rasi_index(self):
        """Test get_rasi_index returns correct 0-based index."""
        ref_data = get_canonical_reference_data()
        
        self.assertEqual(ref_data.get_rasi_index("Mesha"), 0)
        self.assertEqual(ref_data.get_rasi_index("Vrishabha"), 1)
        self.assertEqual(ref_data.get_rasi_index("Mithuna"), 2)
        self.assertEqual(ref_data.get_rasi_index("Meena"), 11)
    
    def test_get_rasi_index_invalid(self):
        """Test get_rasi_index with invalid rasi."""
        ref_data = get_canonical_reference_data()
        
        with self.assertRaises(RegistryAccessError):
            ref_data.get_rasi_index("InvalidRasi")
    
    def test_get_next_rasi(self):
        """Test get_next_rasi wraps correctly."""
        ref_data = get_canonical_reference_data()
        
        self.assertEqual(ref_data.get_next_rasi("Mesha"), "Vrishabha")
        self.assertEqual(ref_data.get_next_rasi("Meena"), "Mesha")  # Wrap
    
    def test_get_previous_rasi(self):
        """Test get_previous_rasi wraps correctly."""
        ref_data = get_canonical_reference_data()
        
        self.assertEqual(ref_data.get_previous_rasi("Vrishabha"), "Mesha")
        self.assertEqual(ref_data.get_previous_rasi("Mesha"), "Meena")  # Wrap
    
    def test_get_rasi_offset(self):
        """Test get_rasi_offset calculates correct offset."""
        ref_data = get_canonical_reference_data()
        
        # Same rasi
        self.assertEqual(ref_data.get_rasi_offset("Mesha", "Mesha"), 0)
        
        # Adjacent
        self.assertEqual(ref_data.get_rasi_offset("Mesha", "Vrishabha"), 1)
        
        # Across boundary
        self.assertEqual(ref_data.get_rasi_offset("Meena", "Mesha"), 1)
        
        # Full circle
        self.assertEqual(ref_data.get_rasi_offset("Mesha", "Meena"), 11)
        
        # Example: Moon in Makara (index 9), Saturn in Meena (index 11)
        # Offset = (11 - 9) % 12 = 2
        self.assertEqual(ref_data.get_rasi_offset("Makara", "Meena"), 2)
    
    def test_get_all_pada_entries(self):
        """Test get_all_pada_entries returns all 108 in order."""
        ref_data = get_canonical_reference_data()
        entries = ref_data.get_all_pada_entries()
        
        self.assertEqual(len(entries), 108)
        self.assertEqual(entries[0].absolute_pada, 1)
        self.assertEqual(entries[-1].absolute_pada, 108)
        
        # Check they're in order
        for i, entry in enumerate(entries):
            self.assertEqual(entry.absolute_pada, i + 1)
    
    def test_validate_integrity(self):
        """Test validate_integrity passes for valid registries."""
        ref_data = get_canonical_reference_data()
        self.assertTrue(ref_data.validate_integrity())
    
    def test_registry_not_found_error(self):
        """Test RegistryNotFoundError for missing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaises(RegistryNotFoundError):
                load_canonical_reference_data(registry_dir=Path(tmpdir))
    
    def test_registry_version_mismatch_error(self):
        """Test RegistryVersionMismatchError for wrong version."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            # Create valid registry files but with wrong version
            for reg_id, config in REQUIRED_REGISTRIES.items():
                file_path = tmpdir / config["filename"]
                data = {
                    "registry_id": reg_id,
                    "version": "99.0",  # Wrong version
                    "entries" if "entries" in config["required_keys"] else "mappings": []
                }
                if reg_id == "rasi_sequence_registry":
                    data["sequence"] = []
                with open(file_path, 'w') as f:
                    json.dump(data, f)
            
            with self.assertRaises(RegistryVersionMismatchError):
                load_canonical_reference_data(registry_dir=tmpdir)
    
    def test_registry_integrity_error_missing_key(self):
        """Test RegistryIntegrityError for missing required key."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            for reg_id, config in REQUIRED_REGISTRIES.items():
                file_path = tmpdir / config["filename"]
                data = {
                    "registry_id": reg_id,
                    "version": "1.0",
                    # Missing required keys
                }
                with open(file_path, 'w') as f:
                    json.dump(data, f)
            
            with self.assertRaises(RegistryIntegrityError):
                load_canonical_reference_data(registry_dir=tmpdir)
    
    def test_registry_integrity_error_entry_count(self):
        """Test RegistryIntegrityError for wrong entry count."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            for reg_id, config in REQUIRED_REGISTRIES.items():
                file_path = tmpdir / config["filename"]
                data = {
                    "registry_id": reg_id,
                    "version": "1.0",
                    "entries" if "entries" in config["required_keys"] else "mappings": [{}],  # Wrong count
                }
                if reg_id == "rasi_sequence_registry":
                    data["sequence"] = [{}]
                with open(file_path, 'w') as f:
                    json.dump(data, f)
            
            with self.assertRaises(RegistryIntegrityError):
                load_canonical_reference_data(registry_dir=tmpdir)


class TestCanonicalReferenceDataDeterminism(unittest.TestCase):
    """Test deterministic behavior (CGP-03)."""
    
    def setUp(self):
        reset_canonical_reference_data()
    
    def tearDown(self):
        reset_canonical_reference_data()
    
    def test_deterministic_output(self):
        """Test identical input produces identical output."""
        ref1 = load_canonical_reference_data()
        ref2 = load_canonical_reference_data()
        
        # Same data
        self.assertEqual(ref1.nakshatra_pada_version, ref2.nakshatra_pada_version)
        self.assertEqual(len(ref1._pada_entries), len(ref2._pada_entries))
        
        # Same access results
        for i in range(1, 109):
            entry1 = ref1.get_pada_entry(i)
            entry2 = ref2.get_pada_entry(i)
            self.assertEqual(entry1.absolute_pada, entry2.absolute_pada)
            self.assertEqual(entry1.nakshatra, entry2.nakshatra)
            self.assertEqual(entry1.pada, entry2.pada)
    
    def test_no_hidden_state(self):
        """Test no hidden state between calls."""
        ref_data = get_canonical_reference_data()
        
        # Multiple calls to same method
        for _ in range(10):
            entry = ref_data.get_pada_entry(90)
            self.assertEqual(entry.nakshatra, "Dhanishta")
            self.assertEqual(entry.pada, 2)


if __name__ == "__main__":
    unittest.main()
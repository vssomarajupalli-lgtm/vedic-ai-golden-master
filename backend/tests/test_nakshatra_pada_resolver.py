"""
Unit tests for NakshatraPadaResolver (Capability 7.2).

Tests governance rules NPR-01 to NPR-05 and validation requirements.
"""

import unittest
import sys
import inspect
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.engines.nakshatra_pada_resolver import (
    NakshatraPadaResolver,
    resolve_nakshatra_pada,
)
from app.engines.canonical_reference_data import (
    get_canonical_reference_data,
    reset_canonical_reference_data,
    RegistryAccessError,
)


class TestNakshatraPadaResolver(unittest.TestCase):
    """Test NakshatraPadaResolver governance rules and functionality."""
    
    def setUp(self):
        """Reset singleton before each test."""
        reset_canonical_reference_data()
        self.resolver = NakshatraPadaResolver()
    
    def tearDown(self):
        """Reset singleton after each test."""
        reset_canonical_reference_data()
    
    # -------------------------------------------------------------------------
    # NPR-01: Input from Canonical JSON (nakshatra string, pada 1-4)
    # NPR-02: Exact match lookup in nakshatra_pada_registry
    # NPR-03: Output absolute pada index (1-108)
    # -------------------------------------------------------------------------
    
    def test_resolve_first_pada(self):
        """Test resolving first pada (Ashwini Pada 1 = 1)."""
        result = self.resolver.resolve("Ashwini", 1)
        self.assertEqual(result, 1)
    
    def test_resolve_last_pada(self):
        """Test resolving last pada (Revati Pada 4 = 108)."""
        result = self.resolver.resolve("Revati", 4)
        self.assertEqual(result, 108)
    
    def test_resolve_raju_moon(self):
        """Test Raju chart Moon: Dhanishta Pada 2 = 90."""
        result = self.resolver.resolve("Dhanishta", 2)
        self.assertEqual(result, 90)
    
    def test_resolve_all_padas_sequential(self):
        """Test all 108 padas resolve to correct absolute index."""
        ref_data = get_canonical_reference_data()
        
        for absolute_pada in range(1, 109):
            nakshatra, pada = ref_data.get_nakshatra_pada(absolute_pada)
            resolved = self.resolver.resolve(nakshatra, pada)
            self.assertEqual(
                resolved, absolute_pada,
                f"Failed for {nakshatra} P{pada}: expected {absolute_pada}, got {resolved}"
            )
    
    def test_each_nakshatra_has_four_padas(self):
        """Test each nakshatra has exactly 4 valid padas (1-4)."""
        ref_data = get_canonical_reference_data()
        
        for nakshatra in ref_data.get_all_nakshatras():
            for pada in range(1, 5):
                result = self.resolver.resolve(nakshatra, pada)
                self.assertTrue(1 <= result <= 108)
            
            # Verify they're sequential
            padas = [self.resolver.resolve(nakshatra, p) for p in range(1, 5)]
            self.assertEqual(padas[1], padas[0] + 1)
            self.assertEqual(padas[2], padas[1] + 1)
            self.assertEqual(padas[3], padas[2] + 1)
    
    # -------------------------------------------------------------------------
    # NPR-04: No longitude input; no trigonometric calculation
    # -------------------------------------------------------------------------
    
    def test_no_longitude_parameter(self):
        """Verify resolver signature has no longitude parameter."""
        # Check unbound method to include 'self'
        sig = inspect.signature(NakshatraPadaResolver.resolve)
        params = list(sig.parameters.keys())
        self.assertEqual(params, ['self', 'nakshatra', 'pada'])
        self.assertNotIn('longitude', params)
        self.assertNotIn('degree', params)
    
    def test_no_trigonometry_imports(self):
        """Verify no math/trigonometry imports or function calls in resolver module."""
        import app.engines.nakshatra_pada_resolver as module
        source = inspect.getsource(module)
        self.assertNotIn('math.', source)
        self.assertNotIn('import math', source)
        self.assertNotIn('from math', source)
        # Check for actual function calls, not just words in docstrings
        self.assertNotIn('math.sin', source)
        self.assertNotIn('math.cos', source)
        self.assertNotIn('math.tan', source)
        self.assertNotIn('math.floor', source)
        self.assertNotIn('math.ceil', source)
        self.assertNotIn('sin(', source)
        self.assertNotIn('cos(', source)
        self.assertNotIn('tan(', source)
        self.assertNotIn('floor(', source)
        self.assertNotIn('ceil(', source)
    
    # -------------------------------------------------------------------------
    # NPR-05: Missing nakshatra/pada -> hard error (RegistryAccessError)
    # -------------------------------------------------------------------------
    
    def test_invalid_nakshatra_fails_fast(self):
        """Test invalid nakshatra raises RegistryAccessError."""
        with self.assertRaises(RegistryAccessError) as cm:
            self.resolver.resolve("InvalidNakshatra", 1)
        self.assertIn("InvalidNakshatra", str(cm.exception))
    
    def test_invalid_pada_zero_fails_fast(self):
        """Test pada=0 raises RegistryAccessError."""
        with self.assertRaises(RegistryAccessError) as cm:
            self.resolver.resolve("Ashwini", 0)
        self.assertIn("pada must be 1-4", str(cm.exception))
    
    def test_invalid_pada_five_fails_fast(self):
        """Test pada=5 raises RegistryAccessError."""
        with self.assertRaises(RegistryAccessError) as cm:
            self.resolver.resolve("Ashwini", 5)
        self.assertIn("pada must be 1-4", str(cm.exception))
    
    def test_invalid_pada_negative_fails_fast(self):
        """Test negative pada raises RegistryAccessError."""
        with self.assertRaises(RegistryAccessError):
            self.resolver.resolve("Ashwini", -1)
    
    # -------------------------------------------------------------------------
    # Determinism (CGP-03)
    # -------------------------------------------------------------------------
    
    def test_deterministic_output(self):
        """Test identical input produces identical output."""
        for _ in range(100):
            result = self.resolver.resolve("Dhanishta", 2)
            self.assertEqual(result, 90)
    
    def test_no_hidden_state(self):
        """Test no hidden state between calls."""
        # Multiple calls should not affect each other
        for _ in range(50):
            r1 = self.resolver.resolve("Ashwini", 1)
            r2 = self.resolver.resolve("Revati", 4)
            r3 = self.resolver.resolve("Dhanishta", 2)
            self.assertEqual(r1, 1)
            self.assertEqual(r2, 108)
            self.assertEqual(r3, 90)
    
    # -------------------------------------------------------------------------
    # Additional Methods
    # -------------------------------------------------------------------------
    
    def test_resolve_batch(self):
        """Test batch resolution."""
        pairs = [("Ashwini", 1), ("Dhanishta", 2), ("Revati", 4)]
        results = self.resolver.resolve_batch(pairs)
        self.assertEqual(results, [1, 90, 108])
    
    def test_get_nakshatra_pada_reverse(self):
        """Test reverse lookup: absolute pada -> (nakshatra, pada)."""
        self.assertEqual(self.resolver.get_nakshatra_pada(1), ("Ashwini", 1))
        self.assertEqual(self.resolver.get_nakshatra_pada(90), ("Dhanishta", 2))
        self.assertEqual(self.resolver.get_nakshatra_pada(108), ("Revati", 4))
    
    def test_validate_all_padas(self):
        """Test validate_all_padas passes."""
        self.assertTrue(self.resolver.validate_all_padas())
    
    # -------------------------------------------------------------------------
    # Convenience Function
    # -------------------------------------------------------------------------
    
    def test_convenience_function(self):
        """Test resolve_nakshatra_pada convenience function."""
        self.assertEqual(resolve_nakshatra_pada("Ashwini", 1), 1)
        self.assertEqual(resolve_nakshatra_pada("Dhanishta", 2), 90)
        self.assertEqual(resolve_nakshatra_pada("Revati", 4), 108)
    
    # -------------------------------------------------------------------------
    # Edge Cases
    # -------------------------------------------------------------------------
    
    def test_nakshatra_case_sensitivity(self):
        """Test nakshatra names are case-sensitive (exact match)."""
        # Exact match works
        self.assertEqual(self.resolver.resolve("Ashwini", 1), 1)
        
        # Wrong case fails
        with self.assertRaises(RegistryAccessError):
            self.resolver.resolve("ashwini", 1)
        
        with self.assertRaises(RegistryAccessError):
            self.resolver.resolve("ASHWINI", 1)
    
    def test_pada_type_validation(self):
        """Test pada must be integer."""
        with self.assertRaises(RegistryAccessError):
            self.resolver.resolve("Ashwini", "1")  # string
        
        with self.assertRaises(RegistryAccessError):
            self.resolver.resolve("Ashwini", 1.0)  # float


class TestNakshatraPadaResolverIntegration(unittest.TestCase):
    """Integration tests with CanonicalReferenceData."""
    
    def setUp(self):
        reset_canonical_reference_data()
        self.resolver = NakshatraPadaResolver()
    
    def tearDown(self):
        reset_canonical_reference_data()
    
    def test_uses_canonical_reference_data(self):
        """Test resolver uses CanonicalReferenceData internally."""
        resolver = NakshatraPadaResolver()
        self.assertIsNotNone(resolver._ref_data)
        self.assertEqual(resolver._ref_data.nakshatra_pada_version, "1.0")
    
    def test_custom_ref_data_injection(self):
        """Test resolver accepts custom CanonicalReferenceData."""
        ref_data = get_canonical_reference_data()
        resolver = NakshatraPadaResolver(ref_data=ref_data)
        self.assertIs(resolver._ref_data, ref_data)
    
    def test_all_108_padas_covered(self):
        """Test all 108 padas are covered exactly once."""
        ref_data = get_canonical_reference_data()
        resolved_padas = set()
        
        for nakshatra in ref_data.get_all_nakshatras():
            for pada in range(1, 5):
                absolute = self.resolver.resolve(nakshatra, pada)
                resolved_padas.add(absolute)
        
        self.assertEqual(len(resolved_padas), 108)
        self.assertEqual(resolved_padas, set(range(1, 109)))


if __name__ == "__main__":
    unittest.main()
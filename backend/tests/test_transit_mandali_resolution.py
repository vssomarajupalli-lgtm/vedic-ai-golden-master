"""
Unit tests for TransitMandaliResolution (Capability 7.4).

Tests governance rules TMR-01 to TMR-05 and validation requirements.
"""

import unittest
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.engines.transit_mandali_resolution import (
    TransitMandaliResolver,
    resolve_transit_mandali,
    TransitMandaliResolution,
)
from app.engines.mandali_grid_construction import (
    MandaliGridConstruction,
    build_mandali_grid,
)
from app.engines.canonical_reference_data import (
    get_canonical_reference_data,
    reset_canonical_reference_data,
    RegistryAccessError,
)
from app.engines.nakshatra_pada_resolver import NakshatraPadaResolver


class TestTransitMandaliResolution(unittest.TestCase):
    """Test TransitMandaliResolution governance rules TMR-01 to TMR-05."""
    
    def setUp(self):
        """Reset singletons before each test."""
        reset_canonical_reference_data()
        self.resolver = TransitMandaliResolver()
        # Build grid for Raju chart: Moon = Dhanishta Pada 2 = Absolute Pada 90
        self.mandali_grid = build_mandali_grid("Dhanishta", 2)
    
    def tearDown(self):
        """Reset singletons after each test."""
        reset_canonical_reference_data()
    
    # -------------------------------------------------------------------------
    # TMR-01: Transit Absolute Pada = NakshatraPadaResolver(transit_nakshatra, transit_pada)
    # -------------------------------------------------------------------------
    
    def test_tmr01_transit_absolute_pada_resolution(self):
        """TMR-01: Transit Absolute Pada resolved via NakshatraPadaResolver."""
        # Saturn in Shatabhisha Pada 3 = Absolute Pada 95 (from registry)
        transit_planets = [{
            "planet": "Saturn",
            "rasi": "Kumbha",
            "nakshatra": "Shatabhisha",
            "pada": 3,
            "house_from_moon": 2,
            "interpretation": "Saturn in Shatabhisha",
        }]
        
        results = self.resolver.resolve_all_transit_planets(transit_planets, self.mandali_grid)
        
        self.assertEqual(len(results), 1)
        result = results[0]
        
        # Verify absolute pada was resolved correctly
        # Shatabhisha P3 = absolute pada 95 (from registry)
        # Mandali 2 has padas 95-103, center=99
        self.assertEqual(result.mandali["number"], 2)
        self.assertEqual(result.mandali["center_pada"], 99)
        self.assertEqual(result.mandali["center_nakshatra"], "Purva Bhadrapada")
    
    def test_tmr01_various_transit_positions(self):
        """TMR-01: Test various transit positions resolve correctly."""
        test_cases = [
            # (nakshatra, pada, expected_mandali, expected_center_pada)
            ("Dhanishta", 2, 1, 90),      # Moon's own position
            ("Shatabhisha", 3, 2, 99),    # Mandali 2
            ("Revati", 4, 3, 108),        # Mandali 3 (wrap)
            ("Krittika", 1, 4, 9),        # Mandali 4
            ("Mrigashira", 2, 5, 18),     # Mandali 5
            ("Punarvasu", 3, 6, 27),      # Mandali 6
            ("Ashlesha", 4, 7, 36),       # Mandali 7
            ("Uttara Phalguni", 1, 8, 45), # Mandali 8
            ("Chitra", 2, 9, 54),         # Mandali 9
            ("Vishakha", 3, 10, 63),      # Mandali 10
            ("Jyeshtha", 4, 11, 72),      # Mandali 11
            ("Uttara Ashadha", 1, 12, 81), # Mandali 12
        ]
        
        for nakshatra, pada, expected_mandali, expected_center in test_cases:
            with self.subTest(nakshatra=nakshatra, pada=pada):
                transit_planets = [{
                    "planet": "TestPlanet",
                    "rasi": "TestRasi",
                    "nakshatra": nakshatra,
                    "pada": pada,
                    "house_from_moon": 1,
                    "interpretation": "Test",
                }]
                
                results = self.resolver.resolve_all_transit_planets(transit_planets, self.mandali_grid)
                result = results[0]
                
                self.assertEqual(result.mandali["number"], expected_mandali)
                self.assertEqual(result.mandali["center_pada"], expected_center)
    
    # -------------------------------------------------------------------------
    # TMR-02: Transit Mandali = unique Mandali N where Transit Absolute Pada ∈ mandali_grid[N].padas
    # -------------------------------------------------------------------------
    
    def test_tmr02_unique_mandali_assignment(self):
        """TMR-02: Each transit pada maps to exactly one Mandali."""
        # Test all 108 padas map to exactly one mandali
        for absolute_pada in range(1, 109):
            with self.subTest(pada=absolute_pada):
                # Find which mandali contains this pada
                mandali_num = self.mandali_grid.find_mandali_for_pada(absolute_pada)
                self.assertTrue(1 <= mandali_num <= 12)
                
                # Verify the pada is in that mandali's padas
                mandali = self.mandali_grid.get_mandali(mandali_num)
                self.assertIn(absolute_pada, mandali.padas)
    
    def test_tmr02_no_overlaps(self):
        """TMR-02: No pada belongs to more than one Mandali."""
        pada_to_mandali = {}
        for n in range(1, 13):
            mandali = self.mandali_grid.get_mandali(n)
            for pada in mandali.padas:
                self.assertNotIn(pada, pada_to_mandali, f"Pada {pada} in multiple mandalis")
                pada_to_mandali[pada] = n
        
        self.assertEqual(len(pada_to_mandali), 108)
    
    # -------------------------------------------------------------------------
    # TMR-03: Exactly one Mandali contains the transit pada (guaranteed by MGC-05)
    # -------------------------------------------------------------------------
    
    def test_tmr03_exactly_one_mandali_per_pada(self):
        """TMR-03: MGC-05 guarantees exactly one Mandali per pada."""
        # This is verified by MGC-05 tests, but we verify integration here
        for absolute_pada in range(1, 109):
            mandali_num = self.mandali_grid.find_mandali_for_pada(absolute_pada)
            self.assertTrue(1 <= mandali_num <= 12)
            
            # Verify no other mandali contains this pada
            count = 0
            for n in range(1, 13):
                if absolute_pada in self.mandali_grid.get_mandali(n).padas:
                    count += 1
            self.assertEqual(count, 1, f"Pada {absolute_pada} found in {count} mandalis")
    
    # -------------------------------------------------------------------------
    # TMR-04: Original Canonical JSON values preserved — never modified
    # -------------------------------------------------------------------------
    
    def test_tmr04_original_values_preserved(self):
        """TMR-04: Original rasi, nakshatra, pada preserved in output."""
        transit_planets = [{
            "planet": "Saturn",
            "rasi": "Kumbha",
            "nakshatra": "Shatabhisha",
            "pada": 3,
            "house_from_moon": 2,
            "interpretation": "Saturn in Shatabhisha",
        }]
        
        results = self.resolver.resolve_all_transit_planets(transit_planets, self.mandali_grid)
        result = results[0]
        
        # Original values preserved exactly
        self.assertEqual(result.original["rasi"], "Kumbha")
        self.assertEqual(result.original["nakshatra"], "Shatabhisha")
        self.assertEqual(result.original["pada"], 3)
        self.assertEqual(result.planet, "Saturn")
        self.assertEqual(result.interpretation_ref, "Saturn in Shatabhisha")
    
    def test_tmr04_multiple_planets_preserved(self):
        """TMR-04: Multiple planets all preserve original values."""
        transit_planets = [
            {
                "planet": "Saturn",
                "rasi": "Kumbha",
                "nakshatra": "Shatabhisha",
                "pada": 3,
                "house_from_moon": 2,
                "interpretation": "Saturn interpretation",
            },
            {
                "planet": "Jupiter",
                "rasi": "Mithuna",
                "nakshatra": "Punarvasu",
                "pada": 3,
                "house_from_moon": 6,
                "interpretation": "Jupiter interpretation",
            },
            {
                "planet": "Rahu",
                "rasi": "Kumbha",
                "nakshatra": "Shatabhisha",
                "pada": 1,
                "house_from_moon": 2,
                "interpretation": "Rahu interpretation",
            },
        ]
        
        results = self.resolver.resolve_all_transit_planets(transit_planets, self.mandali_grid)
        
        self.assertEqual(len(results), 3)
        
        # Saturn
        self.assertEqual(results[0].original["rasi"], "Kumbha")
        self.assertEqual(results[0].original["nakshatra"], "Shatabhisha")
        self.assertEqual(results[0].original["pada"], 3)
        
        # Jupiter
        self.assertEqual(results[1].original["rasi"], "Mithuna")
        self.assertEqual(results[1].original["nakshatra"], "Punarvasu")
        self.assertEqual(results[1].original["pada"], 3)
        
        # Rahu
        self.assertEqual(results[2].original["rasi"], "Kumbha")
        self.assertEqual(results[2].original["nakshatra"], "Shatabhisha")
        self.assertEqual(results[2].original["pada"], 1)
    
    # -------------------------------------------------------------------------
    # TMR-05: Classical house_from_moon preserved alongside Mandali number
    # -------------------------------------------------------------------------
    
    def test_tmr05_classical_house_preserved(self):
        """TMR-05: Classical house_from_moon preserved in output."""
        transit_planets = [{
            "planet": "Saturn",
            "rasi": "Kumbha",
            "nakshatra": "Shatabhisha",
            "pada": 3,
            "house_from_moon": 2,
            "interpretation": "Test",
        }]
        
        results = self.resolver.resolve_all_transit_planets(transit_planets, self.mandali_grid)
        result = results[0]
        
        # Classical house preserved
        self.assertEqual(result.house_from_moon_classical, 2)
        
        # Mandali house = Mandali number
        self.assertEqual(result.house_from_moon_mandali, result.mandali["number"])
    
    def test_tmr05_various_classical_houses(self):
        """TMR-05: Various classical houses preserved correctly."""
        test_cases = [
            (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
            (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12),
        ]
        
        for classical_house, expected_mandali_house in test_cases:
            with self.subTest(classical=classical_house):
                transit_planets = [{
                    "planet": "Test",
                    "rasi": "Mesha",
                    "nakshatra": "Ashwini",
                    "pada": 1,
                    "house_from_moon": classical_house,
                    "interpretation": "Test",
                }]
                
                results = self.resolver.resolve_all_transit_planets(transit_planets, self.mandali_grid)
                result = results[0]
                
                self.assertEqual(result.house_from_moon_classical, classical_house)
                self.assertEqual(result.house_from_moon_mandali, result.mandali["number"])
    
    # -------------------------------------------------------------------------
    # Output Structure Validation
    # -------------------------------------------------------------------------
    
    def test_output_structure_complete(self):
        """Verify all required output fields present."""
        transit_planets = [{
            "planet": "Saturn",
            "rasi": "Kumbha",
            "nakshatra": "Shatabhisha",
            "pada": 3,
            "house_from_moon": 2,
            "interpretation": "Test interpretation",
        }]
        
        results = self.resolver.resolve_all_transit_planets(transit_planets, self.mandali_grid)
        result = results[0]
        
        # Check all required fields
        self.assertIsInstance(result.planet, str)
        self.assertIsInstance(result.original, dict)
        self.assertIn("rasi", result.original)
        self.assertIn("nakshatra", result.original)
        self.assertIn("pada", result.original)
        self.assertIsInstance(result.mandali, dict)
        self.assertIn("number", result.mandali)
        self.assertIn("name", result.mandali)
        self.assertIn("center_nakshatra", result.mandali)
        self.assertIn("center_pada", result.mandali)
        self.assertIsInstance(result.house_from_moon_classical, int)
        self.assertIsInstance(result.house_from_moon_mandali, int)
        self.assertIsInstance(result.interpretation_ref, str)
    
    def test_mandali_name_format(self):
        """Verify Mandali name format is 'Mandali N'."""
        transit_planets = [{
            "planet": "Saturn",
            "rasi": "Kumbha",
            "nakshatra": "Shatabhisha",
            "pada": 3,
            "house_from_moon": 2,
            "interpretation": "Test",
        }]
        
        results = self.resolver.resolve_all_transit_planets(transit_planets, self.mandali_grid)
        result = results[0]
        
        self.assertEqual(result.mandali["name"], f"Mandali {result.mandali['number']}")
    
    # -------------------------------------------------------------------------
    # Error Handling
    # -------------------------------------------------------------------------
    
    def test_invalid_nakshatra_raises_error(self):
        """Invalid nakshatra raises RegistryAccessError."""
        transit_planets = [{
            "planet": "Saturn",
            "rasi": "Kumbha",
            "nakshatra": "InvalidNakshatra",
            "pada": 1,
            "house_from_moon": 2,
            "interpretation": "Test",
        }]
        
        with self.assertRaises(RegistryAccessError):
            self.resolver.resolve_all_transit_planets(transit_planets, self.mandali_grid)
    
    def test_invalid_pada_raises_error(self):
        """Invalid pada raises RegistryAccessError."""
        transit_planets = [{
            "planet": "Saturn",
            "rasi": "Kumbha",
            "nakshatra": "Shatabhisha",
            "pada": 5,  # Invalid: must be 1-4
            "house_from_moon": 2,
            "interpretation": "Test",
        }]
        
        with self.assertRaises(RegistryAccessError):
            self.resolver.resolve_all_transit_planets(transit_planets, self.mandali_grid)
    
    def test_invalid_pada_zero_raises_error(self):
        """Pada zero raises RegistryAccessError."""
        transit_planets = [{
            "planet": "Saturn",
            "rasi": "Kumbha",
            "nakshatra": "Shatabhisha",
            "pada": 0,
            "house_from_moon": 2,
            "interpretation": "Test",
        }]
        
        with self.assertRaises(RegistryAccessError):
            self.resolver.resolve_all_transit_planets(transit_planets, self.mandali_grid)
    
    # -------------------------------------------------------------------------
    # Determinism
    # -------------------------------------------------------------------------
    
    def test_deterministic_output(self):
        """Identical inputs produce identical outputs."""
        transit_planets = [{
            "planet": "Saturn",
            "rasi": "Kumbha",
            "nakshatra": "Shatabhisha",
            "pada": 3,
            "house_from_moon": 2,
            "interpretation": "Test",
        }]
        
        for _ in range(10):
            results1 = self.resolver.resolve_all_transit_planets(transit_planets, self.mandali_grid)
            results2 = self.resolver.resolve_all_transit_planets(transit_planets, self.mandali_grid)
            
            self.assertEqual(len(results1), len(results2))
            for r1, r2 in zip(results1, results2):
                self.assertEqual(r1.planet, r2.planet)
                self.assertEqual(r1.original, r2.original)
                self.assertEqual(r1.mandali, r2.mandali)
                self.assertEqual(r1.house_from_moon_classical, r2.house_from_moon_classical)
                self.assertEqual(r1.house_from_moon_mandali, r2.house_from_moon_mandali)
                self.assertEqual(r1.interpretation_ref, r2.interpretation_ref)
    
    # -------------------------------------------------------------------------
    # Convenience Function
    # -------------------------------------------------------------------------
    
    def test_convenience_function(self):
        """Test resolve_transit_mandali convenience function."""
        transit_planets = [{
            "planet": "Saturn",
            "rasi": "Kumbha",
            "nakshatra": "Shatabhisha",
            "pada": 3,
            "house_from_moon": 2,
            "interpretation": "Test",
        }]
        
        results = resolve_transit_mandali(transit_planets, self.mandali_grid)
        
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], TransitMandaliResolution)
        self.assertEqual(results[0].planet, "Saturn")
        self.assertEqual(results[0].mandali["number"], 2)
    
    # -------------------------------------------------------------------------
    # Dependency Injection
    # -------------------------------------------------------------------------
    
    def test_custom_dependency_injection(self):
        """Test custom ref_data, pada_resolver, grid_constructor injection."""
        ref_data = get_canonical_reference_data()
        pada_resolver = NakshatraPadaResolver(ref_data)
        grid_constructor = MandaliGridConstruction(ref_data=ref_data, pada_resolver=pada_resolver)
        
        resolver = TransitMandaliResolver(
            ref_data=ref_data,
            pada_resolver=pada_resolver,
            grid_constructor=grid_constructor,
        )
        
        self.assertIs(resolver._ref_data, ref_data)
        self.assertIs(resolver._pada_resolver, pada_resolver)
        self.assertIs(resolver._grid_constructor, grid_constructor)
        
        # Verify it works
        transit_planets = [{
            "planet": "Saturn",
            "rasi": "Kumbha",
            "nakshatra": "Shatabhisha",
            "pada": 3,
            "house_from_moon": 2,
            "interpretation": "Test",
        }]
        
        results = resolver.resolve_all_transit_planets(transit_planets, self.mandali_grid)
        self.assertEqual(len(results), 1)


class TestTransitMandaliResolutionIntegration(unittest.TestCase):
    """Integration tests with CanonicalReferenceData and NakshatraPadaResolver."""
    
    def setUp(self):
        reset_canonical_reference_data()
    
    def tearDown(self):
        reset_canonical_reference_data()
    
    def test_uses_canonical_reference_data(self):
        """Test that resolver uses CanonicalReferenceData."""
        resolver = TransitMandaliResolver()
        self.assertIsNotNone(resolver._ref_data)
        self.assertEqual(resolver._ref_data.nakshatra_pada_version, "1.0")
    
    def test_uses_nakshatra_pada_resolver(self):
        """Test that resolver uses NakshatraPadaResolver."""
        resolver = TransitMandaliResolver()
        self.assertIsNotNone(resolver._pada_resolver)
        self.assertIsInstance(resolver._pada_resolver, NakshatraPadaResolver)
    
    def test_uses_mandali_grid_construction(self):
        """Test that resolver uses MandaliGridConstruction."""
        resolver = TransitMandaliResolver()
        self.assertIsNotNone(resolver._grid_constructor)
        self.assertIsInstance(resolver._grid_constructor, MandaliGridConstruction)


if __name__ == "__main__":
    unittest.main()
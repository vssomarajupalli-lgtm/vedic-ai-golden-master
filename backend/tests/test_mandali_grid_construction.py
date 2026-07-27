"""
Unit tests for MandaliGridConstruction (Capability 7.3).

Tests governance rules MGC-01 to MGC-07 and validation requirements.
"""

import unittest
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.engines.mandali_grid_construction import (
    MandaliGridConstruction,
    build_mandali_grid,
    MandaliGrid,
    Mandali,
)
from app.engines.canonical_reference_data import (
    get_canonical_reference_data,
    reset_canonical_reference_data,
    RegistryAccessError,
)
from app.engines.nakshatra_pada_resolver import NakshatraPadaResolver


class TestMandaliGridConstruction(unittest.TestCase):
    """Test MandaliGridConstruction governance rules MGC-01 to MGC-07."""
    
    def setUp(self):
        """Reset singletons before each test."""
        reset_canonical_reference_data()
        self.constructor = MandaliGridConstruction()
    
    def tearDown(self):
        """Reset singletons after each test."""
        reset_canonical_reference_data()
    
    # -------------------------------------------------------------------------
    # MGC-01: Moon Absolute Pada from NakshatraPadaResolver
    # -------------------------------------------------------------------------
    
    def test_mgc01_moon_absolute_pada(self):
        """MGC-01: Moon Absolute Pada = NakshatraPadaResolver(nakshatra, pada)."""
        # Raju chart: Dhanishta Pada 2 = 90
        grid = self.constructor.build_grid("Dhanishta", 2)
        self.assertEqual(grid.moon_absolute_pada, 90)
        self.assertEqual(grid.moon_nakshatra, "Dhanishta")
        self.assertEqual(grid.moon_pada, 2)
        self.assertEqual(grid.moon_rasi, "Makara")
    
    def test_mgc01_various_moon_positions(self):
        """Test MGC-01 with various Moon positions."""
        test_cases = [
            ("Ashwini", 1, 1, "Mesha"),
            ("Bharani", 4, 8, "Mesha"),
            ("Krittika", 1, 9, "Mesha"),
            ("Krittika", 2, 10, "Vrishabha"),
            ("Revati", 4, 108, "Meena"),
        ]
        
        for nakshatra, pada, expected_pada, expected_rasi in test_cases:
            with self.subTest(nakshatra=nakshatra, pada=pada):
                grid = self.constructor.build_grid(nakshatra, pada)
                self.assertEqual(grid.moon_absolute_pada, expected_pada)
                self.assertEqual(grid.moon_rasi, expected_rasi)
    
    # -------------------------------------------------------------------------
    # MGC-02: Mandali 1 center = Moon Absolute Pada
    # -------------------------------------------------------------------------
    
    def test_mgc02_mandali_1_center(self):
        """MGC-02: Mandali 1 center = Moon Absolute Pada."""
        grid = self.constructor.build_grid("Dhanishta", 2)  # Moon = 90
        mandali_1 = grid.get_mandali(1)
        self.assertEqual(mandali_1.center_pada, 90)
        self.assertEqual(mandali_1.number, 1)
    
    def test_mgc02_various_moons(self):
        """Test MGC-02 with various Moon positions."""
        test_cases = [
            ("Ashwini", 1, 1),
            ("Revati", 4, 108),
            ("Mrigashira", 3, 19),
        ]
        
        for nakshatra, pada, expected_center in test_cases:
            with self.subTest(nakshatra=nakshatra, pada=pada):
                grid = self.constructor.build_grid(nakshatra, pada)
                self.assertEqual(grid.get_mandali(1).center_pada, expected_center)
    
    # -------------------------------------------------------------------------
    # MGC-03: Mandali N center = ((Moon + (N-1)*9 - 1) mod 108) + 1
    # -------------------------------------------------------------------------
    
    def test_mgc03_mandali_centers_spacing(self):
        """MGC-03: Mandali centers are 9 padas apart."""
        grid = self.constructor.build_grid("Dhanishta", 2)  # Moon = 90
        
        centers = [grid.get_mandali(n).center_pada for n in range(1, 13)]
        
        # Check each center is 9 apart (modulo 108)
        for i in range(11):
            diff = (centers[i + 1] - centers[i]) % 108
            self.assertEqual(diff, 9, f"Centers {i+1} to {i+2} not 9 apart")
        
        # Check wrap-around from 12 to 1
        diff = (centers[0] - centers[11]) % 108
        self.assertEqual(diff, 9)
    
    def test_mgc03_specific_centers(self):
        """Test specific Mandali centers for Raju chart (Moon=90)."""
        grid = self.constructor.build_grid("Dhanishta", 2)
        
        expected_centers = {
            1: 90,   # Dhanishta P2
            2: 99,   # Purva Bhadrapada P3
            3: 108,  # Revati P4
            4: 9,    # Krittika P1
            5: 18,   # Mrigashira P2
            6: 27,   # Punarvasu P3
            7: 36,   # Ashlesha P4
            8: 45,   # Uttara Phalguni P1
            9: 54,   # Chitra P2
            10: 63,  # Vishakha P3
            11: 72,  # Jyeshtha P4
            12: 81,  # Uttara Ashadha P1
        }
        
        for n, expected in expected_centers.items():
            with self.subTest(mandali=n):
                self.assertEqual(grid.get_mandali(n).center_pada, expected)
    
    # -------------------------------------------------------------------------
    # MGC-04: Each Mandali = 9 padas (center ±4, modulo 108)
    # -------------------------------------------------------------------------
    
    def test_mgc04_mandali_size(self):
        """MGC-04: Each Mandali contains exactly 9 padas."""
        grid = self.constructor.build_grid("Dhanishta", 2)
        
        for n in range(1, 13):
            mandali = grid.get_mandali(n)
            self.assertEqual(len(mandali.padas), 9, f"Mandali {n} has {len(mandali.padas)} padas")
    
    def test_mgc04_pada_range(self):
        """MGC-04: Padas are center ±4 with modulo 108 wrap."""
        grid = self.constructor.build_grid("Dhanishta", 2)  # Moon=90
        
        # Mandali 1: center=90, padas=86-94
        mandali_1 = grid.get_mandali(1)
        self.assertEqual(mandali_1.padas, (86, 87, 88, 89, 90, 91, 92, 93, 94))
        
        # Mandali 3: center=108, padas=104-108,1-4 (wrap)
        mandali_3 = grid.get_mandali(3)
        self.assertEqual(mandali_3.padas, (104, 105, 106, 107, 108, 1, 2, 3, 4))
        
        # Mandali 12: center=81, padas=77-85
        mandali_12 = grid.get_mandali(12)
        self.assertEqual(mandali_12.padas, (77, 78, 79, 80, 81, 82, 83, 84, 85))
        
        # Mandali 4: center=9, padas=5-13 (wrap)
        mandali_4 = grid.get_mandali(4)
        self.assertEqual(mandali_4.padas, (5, 6, 7, 8, 9, 10, 11, 12, 13))
    
    # -------------------------------------------------------------------------
    # MGC-05: All 108 padas covered exactly once (no gaps, no overlaps)
    # -------------------------------------------------------------------------
    
    def test_mgc05_all_padas_covered(self):
        """MGC-05: All 108 padas covered exactly once."""
        grid = self.constructor.build_grid("Dhanishta", 2)
        
        all_padas = []
        for n in range(1, 13):
            all_padas.extend(grid.get_mandali(n).padas)
        
        # Check count
        self.assertEqual(len(all_padas), 108)
        
        # Check no duplicates
        self.assertEqual(len(set(all_padas)), 108)
        
        # Check all 1-108 present
        self.assertEqual(set(all_padas), set(range(1, 109)))
    
    def test_mgc05_various_moons(self):
        """Test MGC-05 with various Moon positions."""
        test_cases = [
            ("Ashwini", 1),
            ("Bharani", 4),
            ("Krittika", 2),
            ("Revati", 4),
            ("Mrigashira", 3),
        ]
        
        for nakshatra, pada in test_cases:
            with self.subTest(nakshatra=nakshatra, pada=pada):
                grid = self.constructor.build_grid(nakshatra, pada)
                
                all_padas = []
                for n in range(1, 13):
                    all_padas.extend(grid.get_mandali(n).padas)
                
                self.assertEqual(len(all_padas), 108)
                self.assertEqual(len(set(all_padas)), 108)
                self.assertEqual(set(all_padas), set(range(1, 109)))
    
    # -------------------------------------------------------------------------
    # MGC-06: Mandali Rasi = Rasi of center pada's Nakshatra
    # -------------------------------------------------------------------------
    
    def test_mgc06_mandali_rasi_names(self):
        """MGC-06: Mandali Rasi = Rasi of center pada's Nakshatra."""
        grid = self.constructor.build_grid("Dhanishta", 2)
        
        expected_rasis = {
            1: "Makara",    # Dhanishta P2
            2: "Kumbha",    # Purva Bhadrapada P3
            3: "Meena",     # Revati P4
            4: "Mesha",     # Krittika P1
            5: "Vrishabha", # Mrigashira P2
            6: "Mithuna",   # Punarvasu P3
            7: "Karkata",   # Ashlesha P4
            8: "Simha",     # Uttara Phalguni P1
            9: "Kanya",     # Chitra P2
            10: "Tula",     # Vishakha P3
            11: "Vrishchika", # Jyeshtha P4
            12: "Dhanus",   # Uttara Ashadha P1
        }
        
        for n, expected_rasi in expected_rasis.items():
            with self.subTest(mandali=n):
                self.assertEqual(grid.get_mandali(n).rasi_name, expected_rasi)
    
    # -------------------------------------------------------------------------
    # MGC-07: Deterministic output
    # -------------------------------------------------------------------------
    
    def test_mgc07_deterministic(self):
        """MGC-07: Identical inputs produce identical output."""
        for _ in range(10):
            grid1 = self.constructor.build_grid("Dhanishta", 2)
            grid2 = self.constructor.build_grid("Dhanishta", 2)
            
            self.assertEqual(grid1.moon_absolute_pada, grid2.moon_absolute_pada)
            self.assertEqual(grid1.moon_nakshatra, grid2.moon_nakshatra)
            self.assertEqual(grid1.moon_pada, grid2.moon_pada)
            self.assertEqual(grid1.moon_rasi, grid2.moon_rasi)
            
            for n in range(1, 13):
                m1 = grid1.get_mandali(n)
                m2 = grid2.get_mandali(n)
                self.assertEqual(m1.number, m2.number)
                self.assertEqual(m1.center_pada, m2.center_pada)
                self.assertEqual(m1.center_nakshatra, m2.center_nakshatra)
                self.assertEqual(m1.center_pada_num, m2.center_pada_num)
                self.assertEqual(m1.rasi_name, m2.rasi_name)
                self.assertEqual(m1.padas, m2.padas)
    
    # -------------------------------------------------------------------------
    # Additional Methods
    # -------------------------------------------------------------------------
    
    def test_find_mandali_for_pada(self):
        """Test find_mandali_for_pada method."""
        grid = self.constructor.build_grid("Dhanishta", 2)
        
        # Moon pada 90 is in Mandali 1 (center=90, padas=86-94)
        self.assertEqual(grid.find_mandali_for_pada(90), 1)
        
        # Pada 95 is in Mandali 2 (center=99, padas=95-103)
        self.assertEqual(grid.find_mandali_for_pada(95), 2)
        
        # Pada 108 is in Mandali 3 (center=108, padas=104-108,1-4)
        self.assertEqual(grid.find_mandali_for_pada(108), 3)
        
        # Pada 1 is in Mandali 3 (wrap)
        self.assertEqual(grid.find_mandali_for_pada(1), 3)
        
        # Pada 81 is in Mandali 12 (center=81, padas=77-85)
        self.assertEqual(grid.find_mandali_for_pada(81), 12)
        
        # Pada 9 is in Mandali 4 (center=9, padas=5-13)
        self.assertEqual(grid.find_mandali_for_pada(9), 4)
    
    def test_find_mandali_invalid_pada(self):
        """Test find_mandali_for_pada with invalid pada."""
        grid = self.constructor.build_grid("Dhanishta", 2)
        
        with self.assertRaises(ValueError):
            grid.find_mandali_for_pada(0)
        
        with self.assertRaises(ValueError):
            grid.find_mandali_for_pada(109)
    
    def test_get_mandali_invalid_number(self):
        """Test get_mandali with invalid number."""
        grid = self.constructor.build_grid("Dhanishta", 2)
        
        with self.assertRaises(ValueError):
            grid.get_mandali(0)
        
        with self.assertRaises(ValueError):
            grid.get_mandali(13)
    
    # -------------------------------------------------------------------------
    # Convenience Function
    # -------------------------------------------------------------------------
    
    def test_build_mandali_grid_convenience(self):
        """Test build_mandali_grid convenience function."""
        grid = build_mandali_grid("Dhanishta", 2)
        
        self.assertIsInstance(grid, MandaliGrid)
        self.assertEqual(grid.moon_absolute_pada, 90)
        self.assertEqual(len(grid.mandalis), 12)
    
    def test_custom_ref_data_injection(self):
        """Test constructor with custom ref_data and pada_resolver."""
        ref_data = get_canonical_reference_data()
        pada_resolver = NakshatraPadaResolver(ref_data)
        
        constructor = MandaliGridConstruction(ref_data=ref_data, pada_resolver=pada_resolver)
        grid = constructor.build_grid("Dhanishta", 2)
        
        self.assertEqual(grid.moon_absolute_pada, 90)
    
    # -------------------------------------------------------------------------
    # Error Handling
    # -------------------------------------------------------------------------
    
    def test_invalid_nakshatra(self):
        """Test invalid nakshatra raises RegistryAccessError."""
        with self.assertRaises(RegistryAccessError):
            self.constructor.build_grid("InvalidNakshatra", 1)
    
    def test_invalid_pada(self):
        """Test invalid pada raises RegistryAccessError."""
        with self.assertRaises(RegistryAccessError):
            self.constructor.build_grid("Ashwini", 0)
        
        with self.assertRaises(RegistryAccessError):
            self.constructor.build_grid("Ashwini", 5)
    
    # -------------------------------------------------------------------------
    # Pada Details
    # -------------------------------------------------------------------------
    
    def test_pada_details_included(self):
        """Test that pada_details are included in each Mandali."""
        grid = self.constructor.build_grid("Dhanishta", 2)
        
        for n in range(1, 13):
            mandali = grid.get_mandali(n)
            self.assertEqual(len(mandali.pada_details), 9)
            
            for detail in mandali.pada_details:
                # NakshatraPadaEntry is a dataclass, not a tuple
                self.assertTrue(hasattr(detail, 'absolute_pada'))
                self.assertTrue(hasattr(detail, 'nakshatra'))
                self.assertTrue(hasattr(detail, 'pada'))
                self.assertIsInstance(detail.absolute_pada, int)
                self.assertIsInstance(detail.nakshatra, str)
                self.assertIsInstance(detail.pada, int)


class TestMandaliGridConstructionIntegration(unittest.TestCase):
    """Integration tests with CanonicalReferenceData and NakshatraPadaResolver."""
    
    def setUp(self):
        reset_canonical_reference_data()
    
    def tearDown(self):
        reset_canonical_reference_data()
    
    def test_uses_canonical_reference_data(self):
        """Test that constructor uses CanonicalReferenceData."""
        constructor = MandaliGridConstruction()
        self.assertIsNotNone(constructor._ref_data)
        self.assertEqual(constructor._ref_data.nakshatra_pada_version, "1.0")
    
    def test_uses_nakshatra_pada_resolver(self):
        """Test that constructor uses NakshatraPadaResolver."""
        constructor = MandaliGridConstruction()
        self.assertIsNotNone(constructor._pada_resolver)
        self.assertIsInstance(constructor._pada_resolver, NakshatraPadaResolver)
    
    def test_custom_injection(self):
        """Test custom ref_data and pada_resolver injection."""
        ref_data = get_canonical_reference_data()
        pada_resolver = NakshatraPadaResolver(ref_data)
        
        constructor = MandaliGridConstruction(ref_data=ref_data, pada_resolver=pada_resolver)
        self.assertIs(constructor._ref_data, ref_data)
        self.assertIs(constructor._pada_resolver, pada_resolver)


if __name__ == "__main__":
    unittest.main()
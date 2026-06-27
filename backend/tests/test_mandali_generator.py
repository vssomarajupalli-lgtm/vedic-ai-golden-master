import unittest
from app.engines.mandali_generator import MandaliGenerator

class TestMandaliGenerator(unittest.TestCase):

    def test_absolute_pada_calculation(self):
        # 0.0 -> Pada 1
        self.assertEqual(MandaliGenerator.get_absolute_pada(0.0), 1)
        # 3.333333 -> Pada 2
        self.assertEqual(MandaliGenerator.get_absolute_pada(3.333334), 2)
        # 120.0 -> 120 / (10/3) = 120 * 3 / 10 = 36. So 120.0 falls in Pada 37 (since 0 to 119.999 is 1 to 36)
        # Wait: 119.999 / 3.333 = 35.99 -> floor is 35. +1 = 36.
        # 120.0 / 3.333 = 36.0. floor is 36. +1 = 37.
        self.assertEqual(MandaliGenerator.get_absolute_pada(120.0), 37)
        # 359.99 -> Pada 108
        self.assertEqual(MandaliGenerator.get_absolute_pada(359.99), 108)

    def test_generate_mandali_grid_dhanishta(self):
        # Moon = Dhanishta Pada 2 = Pada 90
        moon_pada = 90
        grid = MandaliGenerator.generate_mandali_grid(moon_pada)
        
        # Mandali 1 should be centered on 90, spanning 86 to 94
        self.assertEqual(grid[1]["center"], 90)
        self.assertEqual(grid[1]["padas"], [86, 87, 88, 89, 90, 91, 92, 93, 94])
        
        # Mandali 2 should be centered on 99, spanning 95 to 103
        self.assertEqual(grid[2]["center"], 99)
        self.assertEqual(grid[2]["padas"], [95, 96, 97, 98, 99, 100, 101, 102, 103])
        
        # Mandali 3 should wrap around 108 -> 1
        self.assertEqual(grid[3]["center"], 108)
        self.assertEqual(grid[3]["padas"], [104, 105, 106, 107, 108, 1, 2, 3, 4])
        
        # Mandali 12 should be centered on 81, spanning 77 to 85
        self.assertEqual(grid[12]["center"], 81)
        self.assertEqual(grid[12]["padas"], [77, 78, 79, 80, 81, 82, 83, 84, 85])

    def test_resolve_transit_mandali(self):
        moon_pada = 90
        
        # Transit at 300.0 degrees: 300 / 3.333 = 90. -> floor + 1 = 91
        # Pada 91 belongs to Mandali 1 in Dhanishta example.
        mandali = MandaliGenerator.resolve_transit_mandali(300.0, moon_pada)
        self.assertEqual(mandali, 1)
        
        # Transit at Pada 105 (Mandali 3)
        # 105 padas * (10/3) = 350.0 degrees. 349.0 degrees should fall in Pada 105.
        mandali = MandaliGenerator.resolve_transit_mandali(349.0, moon_pada)
        self.assertEqual(mandali, 3)

if __name__ == "__main__":
    unittest.main()

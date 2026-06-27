import unittest
import datetime
from app.utils.ephemeris_service import EphemerisService

class TestEphemerisService(unittest.TestCase):
    def setUp(self):
        self.service = EphemerisService()

    def test_planet_map_initialization(self):
        """Test that the planet map has the correct standard planets."""
        self.assertIn("sun", self.service.planet_map)
        self.assertIn("moon", self.service.planet_map)
        self.assertIn("saturn", self.service.planet_map)
        self.assertIn("rahu", self.service.planet_map)
        self.assertNotIn("ketu", self.service.planet_map) # Ketu is dynamically generated

    def test_zodiac_signs_order(self):
        """Test that zodiac signs are correctly ordered."""
        self.assertEqual(len(self.service.zodiac_signs), 12)
        self.assertEqual(self.service.zodiac_signs[0], "aries")
        self.assertEqual(self.service.zodiac_signs[11], "pisces")

    def test_generate_transit_snapshot_stub(self):
        """Test the stubbed generation logic."""
        dt = datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc)
        snapshot = self.service.generate_transit_snapshot(dt)
        self.assertIsInstance(snapshot, dict)
        self.assertIn("planets", snapshot)
        self.assertIn("jupiter", snapshot["planets"])
        self.assertIn("ketu", snapshot["planets"])
        self.assertIn("rahu", snapshot["planets"])

    def test_calculate_planet_position_stub(self):
        """Test the stubbed position calculation."""
        # Using a deterministic julian day 2460000.5
        result = self.service._calculate_planet_position("jupiter", 5, 2460000.5)
        self.assertEqual(result["name"], "jupiter")
        self.assertIn("sign", result)
        self.assertIn("degree", result)
        self.assertIn("is_retrograde", result)

    def test_ketu_derivation(self):
        """Test that Ketu is exactly 6 signs opposite Rahu."""
        rahu = {
            "name": "rahu",
            "sign": "aries",
            "degree": 15.5,
            "longitude": 15.5
        }
        ketu = self.service._calculate_ketu_position(rahu)
        self.assertEqual(ketu["name"], "ketu")
        self.assertEqual(ketu["sign"], "libra")
        self.assertEqual(ketu["degree"], 15.5)

if __name__ == '__main__':
    unittest.main()

import datetime
import logging
from typing import Dict, Any

try:
    import swisseph as swe
    HAS_SWE = True
except ImportError:
    HAS_SWE = False
    logging.warning("pyswisseph not installed. EphemerisService will use synthetic fallback data.")

class EphemerisService:
    """
    Lightweight, stateless wrapper for the Swiss Ephemeris (pyswisseph).
    Generates deterministic planetary transit snapshots for future dates.
    Strictly provides astronomical data; contains ZERO astrological reasoning.
    """

    def __init__(self):
        if HAS_SWE:
            swe.set_sid_mode(swe.SIDM_LAHIRI)
        
        self.planet_map = {
            "sun": 0,       # swe.SUN
            "moon": 1,      # swe.MOON
            "mars": 4,      # swe.MARS
            "mercury": 2,   # swe.MERCURY
            "jupiter": 5,   # swe.JUPITER
            "venus": 3,     # swe.VENUS
            "saturn": 6,    # swe.SATURN
            "rahu": 11,     # swe.TRUE_NODE
        }
        
        self.zodiac_signs = [
            "aries", "taurus", "gemini", "cancer", 
            "leo", "virgo", "libra", "scorpio", 
            "sagittarius", "capricorn", "aquarius", "pisces"
        ]

    def generate_transit_snapshot(self, target_date_utc: datetime.datetime = None) -> Dict[str, Any]:
        """
        Generates a normalized snapshot of planetary positions for a specific UTC date.
        """
        target_date_utc = target_date_utc or datetime.datetime.now(datetime.timezone.utc)
        
        if HAS_SWE:
            julian_day = swe.julday(
                target_date_utc.year, target_date_utc.month, target_date_utc.day, 
                target_date_utc.hour + target_date_utc.minute/60.0
            )
        else:
            # Synthetic julian day equivalent for fallback math
            epoch = datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc)
            # Ensure target_date_utc is aware before subtracting
            if target_date_utc.tzinfo is None:
                target_date_utc = target_date_utc.replace(tzinfo=datetime.timezone.utc)
            julian_day = (target_date_utc - epoch).days + 2451545.0

        snapshot = {"planets": {}}
        
        for planet_name, swe_id in self.planet_map.items():
            snapshot["planets"][planet_name] = self._calculate_planet_position(planet_name, swe_id, julian_day)
            
        snapshot["planets"]["ketu"] = self._calculate_ketu_position(snapshot["planets"]["rahu"])

        return snapshot

    def _calculate_planet_position(self, planet_name: str, swe_id: int, julian_day: float) -> Dict[str, Any]:
        """
        Calculates sidereal longitude and speed for a single planet.
        Converts 0-360 degree format into normalized Sign + Degree.
        """
        if HAS_SWE:
            results = swe.calc_ut(julian_day, swe_id, swe.FLG_SIDEREAL)
            raw_longitude = results[0][0]
            speed = results[0][3]
        else:
            # Synthetic fallback: predictable pseudo-orbit based on julian day
            # This ensures tests and pipelines run deterministically when SWE is missing.
            orbit_speeds = {
                "sun": 0.9856, "moon": 13.176, "mars": 0.524, 
                "mercury": 1.383, "jupiter": 0.083, "venus": 1.20, 
                "saturn": 0.033, "rahu": -0.052
            }
            avg_speed = orbit_speeds.get(planet_name, 1.0)
            raw_longitude = (julian_day * avg_speed) % 360.0
            speed = avg_speed

        sign_index = int(raw_longitude // 30)
        degree_in_sign = round(raw_longitude % 30, 2)
        is_retrograde = speed < 0

        return {
            "name": planet_name,
            "sign": self.zodiac_signs[sign_index],
            "degree": degree_in_sign,
            "longitude": raw_longitude,
            "is_retrograde": is_retrograde
        }

    def _calculate_ketu_position(self, rahu_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Derives Ketu's position by adding 180 degrees (6 signs) to Rahu.
        """
        rahu_sign_idx = self.zodiac_signs.index(rahu_data["sign"])
        ketu_sign_idx = (rahu_sign_idx + 6) % 12
        ketu_longitude = (rahu_data["longitude"] + 180.0) % 360.0
        
        return {
            "name": "ketu",
            "sign": self.zodiac_signs[ketu_sign_idx],
            "degree": rahu_data["degree"],
            "longitude": ketu_longitude,
            "is_retrograde": True
        }
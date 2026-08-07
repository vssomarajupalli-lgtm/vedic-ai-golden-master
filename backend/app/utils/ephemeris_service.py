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
            "Mesha", "Vrishabha", "Mithuna", "Karkata", 
            "Simha", "Kanya", "Tula", "Vrishchika", 
            "Dhanus", "Makara", "Kumbha", "Meena"
        ]

    def _julian_day(self, target_date_utc: datetime.datetime) -> float:
        """
        Convert a UTC datetime to a Julian day number.
        Uses Swiss Ephemeris when available; otherwise a synthetic epoch equivalent.
        """
        if HAS_SWE:
            return swe.julday(
                target_date_utc.year, target_date_utc.month, target_date_utc.day,
                target_date_utc.hour + target_date_utc.minute / 60.0
            )
        epoch = datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc)
        if target_date_utc.tzinfo is None:
            target_date_utc = target_date_utc.replace(tzinfo=datetime.timezone.utc)
        return (target_date_utc - epoch).days + 2451545.0

    def get_longitude(self, planet_name: str, date_utc: datetime.datetime) -> float:
        """
        Return the sidereal longitude (0.0-360.0) of a planet at a given UTC datetime.

        Uses the same sidereal (Lahiri) computation as generate_transit_snapshot.
        Ketu is derived as Rahu + 180 degrees, matching _calculate_ketu_position.
        """
        if planet_name == "ketu":
            rahu_lon = self.get_longitude("rahu", date_utc)
            return (rahu_lon + 180.0) % 360.0
        if planet_name not in self.planet_map:
            raise ValueError(f"Unknown planet: {planet_name}")
        position = self._calculate_planet_position(
            planet_name, self.planet_map[planet_name], self._julian_day(date_utc)
        )
        return position["longitude"]

    def generate_transit_snapshot(self, target_date_utc: datetime.datetime = None) -> Dict[str, Any]:
        """
        Generates a normalized snapshot of planetary positions for a specific UTC date.
        """
        target_date_utc = target_date_utc or datetime.datetime.now(datetime.timezone.utc)
        
        julian_day = self._julian_day(target_date_utc)

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
            # The pyswisseph sidereal mode is a GLOBAL setting that may be reset
            # to its default (Fagan-Bradley) by the host process. Re-assert the
            # Lahiri mode immediately before every calculation so the result is
            # always deterministic and consistent (snapshot + transit-date scans).
            swe.set_sid_mode(swe.SIDM_LAHIRI)
            # FLG_SPEED is required for pyswisseph to compute velocities; without
            # it results[0][3] is always 0 and is_retrograde can never be True.
            # Adding it does not change the longitude.
            results = swe.calc_ut(julian_day, swe_id, swe.FLG_SIDEREAL | swe.FLG_SPEED)
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
            "speed": speed,
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
            "speed": rahu_data.get("speed", 0.0),
            "is_retrograde": True
        }
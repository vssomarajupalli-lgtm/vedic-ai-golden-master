class FunctionalNatureEngine:
    """
    Determines the functional nature (benefic, malefic, neutral, yogakaraka, maraka)
    of planets based strictly on the Ascendant (Lagna) sign.
    
    This engine operates independently of PlanetStrengthEngine and provides
    a structural astrological map to be consumed by downstream logic (Natal Promise, Dashas).
    """

    # Static Parashari functional mapping per Lagna.
    # Excludes Rahu and Ketu, as they act according to their dispositor.
    _MAP = {
        "aries": {
            "mars":    {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "sun":     {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "jupiter": {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "moon":    {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": False},
            "mercury": {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "venus":   {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": True},
            "saturn":  {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
        },
        "taurus": {
            "venus":   {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "saturn":  {"functional_role": "benefic", "is_yogakaraka": True,  "is_maraka": False},
            "mercury": {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "sun":     {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": False},
            "mars":    {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": True},
            "moon":    {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "jupiter": {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
        },
        "gemini": {
            "mercury": {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "venus":   {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "moon":    {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": True},
            "saturn":  {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": False},
            "sun":     {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "mars":    {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "jupiter": {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
        },
        "cancer": {
            "moon":    {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "mars":    {"functional_role": "benefic", "is_yogakaraka": True,  "is_maraka": False},
            "jupiter": {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "sun":     {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": True},
            "mercury": {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "venus":   {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "saturn":  {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
        },
        "leo": {
            "sun":     {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "mars":    {"functional_role": "benefic", "is_yogakaraka": True,  "is_maraka": False},
            "jupiter": {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "moon":    {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": False},
            "mercury": {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": True},
            "venus":   {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "saturn":  {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
        },
        "virgo": {
            "mercury": {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "venus":   {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "sun":     {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": False},
            "saturn":  {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": False},
            "moon":    {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "mars":    {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "jupiter": {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": True},
        },
        "libra": {
            "venus":   {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "saturn":  {"functional_role": "benefic", "is_yogakaraka": True,  "is_maraka": False},
            "mercury": {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "moon":    {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": False},
            "sun":     {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "mars":    {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": True},
            "jupiter": {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
        },
        "scorpio": {
            "mars":    {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "sun":     {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "moon":    {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "jupiter": {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "mercury": {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "venus":   {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": True},
            "saturn":  {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
        },
        "sagittarius": {
            "jupiter": {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "sun":     {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "mars":    {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "moon":    {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": False},
            "mercury": {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": True},
            "venus":   {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "saturn":  {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": True},
        },
        "capricorn": {
            "saturn":  {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "venus":   {"functional_role": "benefic", "is_yogakaraka": True,  "is_maraka": False},
            "mercury": {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "sun":     {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": False},
            "moon":    {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": True},
            "mars":    {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "jupiter": {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
        },
        "aquarius": {
            "saturn":  {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "venus":   {"functional_role": "benefic", "is_yogakaraka": True,  "is_maraka": False},
            "mars":    {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "mercury": {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": False},
            "sun":     {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": True},
            "moon":    {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "jupiter": {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": True},
        },
        "pisces": {
            "jupiter": {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "moon":    {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "mars":    {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": True},
            "sun":     {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "mercury": {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": True},
            "venus":   {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "saturn":  {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
        }
    }

    def __init__(self, calibration=None):
        if calibration is None:
            from app.calibration.calibration_manager import CalibrationManager
            calibration = CalibrationManager()
        pass

    def get_functional_nature(self, lagna: str) -> dict:
        """
        Retrieves the functional nature map for all visible planets based on the Ascendant sign.
        
        Args:
            lagna (str): The Ascendant sign (e.g. "aries", "taurus", etc.)
            
        Returns:
            dict: Mapping of planet names to their functional properties. Returns
                  an empty dictionary if the lagna is unknown.
        """
        if not lagna:
            return {}
        
        lagna_key = lagna.lower().strip()
        
        # We perform a fallback alias mapping for common sanskrit-english names just in case
        alias_map = {
            "mesha": "aries", "vrishabha": "taurus", "mithuna": "gemini",
            "kataka": "cancer", "simha": "leo", "kanya": "virgo",
            "tula": "libra", "vrishchika": "scorpio", "dhanu": "sagittarius",
            "makara": "capricorn", "kumbha": "aquarius", "meena": "pisces"
        }
        
        mapped_lagna = alias_map.get(lagna_key, lagna_key)
        
        return self._MAP.get(mapped_lagna, {})

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
        "Mesha": {
            "mars":    {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "sun":     {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "jupiter": {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "moon":    {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": False},
            "mercury": {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "venus":   {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": True},
            "saturn":  {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
        },
        "Vrishabha": {
            "venus":   {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "saturn":  {"functional_role": "benefic", "is_yogakaraka": True,  "is_maraka": False},
            "mercury": {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "sun":     {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": False},
            "mars":    {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": True},
            "moon":    {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "jupiter": {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
        },
        "Mithuna": {
            "mercury": {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "venus":   {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "moon":    {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": True},
            "saturn":  {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": False},
            "sun":     {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "mars":    {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "jupiter": {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
        },
        "Karkata": {
            "moon":    {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "mars":    {"functional_role": "benefic", "is_yogakaraka": True,  "is_maraka": False},
            "jupiter": {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "sun":     {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": True},
            "mercury": {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "venus":   {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "saturn":  {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
        },
        "Simha": {
            "sun":     {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "mars":    {"functional_role": "benefic", "is_yogakaraka": True,  "is_maraka": False},
            "jupiter": {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "moon":    {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": False},
            "mercury": {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": True},
            "venus":   {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "saturn":  {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
        },
        "Kanya": {
            "mercury": {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "venus":   {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "sun":     {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": False},
            "saturn":  {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": False},
            "moon":    {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "mars":    {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "jupiter": {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": True},
        },
        "Tula": {
            "venus":   {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "saturn":  {"functional_role": "benefic", "is_yogakaraka": True,  "is_maraka": False},
            "mercury": {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "moon":    {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": False},
            "sun":     {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "mars":    {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": True},
            "jupiter": {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
        },
        "Vrishchika": {
            "mars":    {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "sun":     {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "moon":    {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "jupiter": {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "mercury": {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "venus":   {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": True},
            "saturn":  {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
        },
        "Dhanus": {
            "jupiter": {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "sun":     {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "mars":    {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "moon":    {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": False},
            "mercury": {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": True},
            "venus":   {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "saturn":  {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": True},
        },
        "Makara": {
            "saturn":  {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "venus":   {"functional_role": "benefic", "is_yogakaraka": True,  "is_maraka": False},
            "mercury": {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "sun":     {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": False},
            "moon":    {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": True},
            "mars":    {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "jupiter": {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
        },
        "Kumbha": {
            "saturn":  {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "venus":   {"functional_role": "benefic", "is_yogakaraka": True,  "is_maraka": False},
            "mars":    {"functional_role": "benefic", "is_yogakaraka": False, "is_maraka": False},
            "mercury": {"functional_role": "neutral", "is_yogakaraka": False, "is_maraka": False},
            "sun":     {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": True},
            "moon":    {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": False},
            "jupiter": {"functional_role": "malefic", "is_yogakaraka": False, "is_maraka": True},
        },
        "Meena": {
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
            lagna (str): The Ascendant sign (canonical Sanskrit, e.g. "Mesha", "Vrishabha")
            
        Returns:
            dict: Mapping of planet names to their functional properties. Returns
                  an empty dictionary if the lagna is unknown.
        """
        if not lagna:
            return {}
        
        lagna_key = lagna.lower().strip()
        
        # We perform a fallback alias mapping for common sanskrit-english names just in case
        alias_map = {
            "mesha": "Mesha", "vrishabha": "Vrishabha", "mithuna": "Mithuna",
            "karkata": "Karkata", "simha": "Simha", "kanya": "Kanya",
            "tula": "Tula", "vrishchika": "Vrishchika", "dhanus": "Dhanus",
            "makara": "Makara", "kumbha": "Kumbha", "meena": "Meena",
            "aries": "Mesha", "taurus": "Vrishabha", "gemini": "Mithuna",
            "cancer": "Karkata", "leo": "Simha", "virgo": "Kanya",
            "libra": "Tula", "scorpio": "Vrishchika", "sagittarius": "Dhanus",
            "capricorn": "Makara", "aquarius": "Kumbha", "pisces": "Meena"
        }
        
        mapped_lagna = alias_map.get(lagna_key, lagna_key)
        
        return self._MAP.get(mapped_lagna, {})

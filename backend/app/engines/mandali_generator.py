import math

class MandaliGenerator:
    """
    MandaliGenerator — Moon-Centered Gochara Transit Boundaries
    =========================================================
    
    Generates dynamic Moon-centered Mandalis for transit evaluation
    as specified in GOCHARA_MANDALI_GOVERNANCE_v1.md.
    
    Axioms:
    - 1 Mandali = 9 Padas
    - Moon Pada = Center of Mandali 1
    - 12 Mandalis = exactly 108 Padas (no overlaps, no gaps)
    """

    @staticmethod
    def get_absolute_pada(longitude_deg: float) -> int:
        """
        Translates a planetary longitude (0.0 to 360.0) into its 
        absolute Nakshatra Pada index (1 to 108).
        
        Formula: 108 padas / 360 degrees = 3.333333 degrees per pada.
        """
        # Ensure longitude is within 0.0-359.999...
        long_mod = longitude_deg % 360.0
        # 360 / 108 = 10 / 3
        pada_float = long_mod / (10.0 / 3.0)
        return math.floor(pada_float) + 1

    @staticmethod
    def generate_mandali_grid(moon_pada: int) -> dict:
        """
        Constructs the 12-block static grid centered entirely on the Natal Moon.
        
        Returns a dict mapping Mandali integer (1-12) to a dictionary:
        { "center": int, "padas": list[int] }
        """
        grid = {}
        for n in range(1, 13):
            # Calculate the center of this Mandali
            # N=1 is center. N=2 is +9 padas.
            offset_padas = (n - 1) * 9
            center = ((moon_pada + offset_padas - 1) % 108) + 1
            
            # The 9 padas include center, 4 before, and 4 after
            padas = []
            for offset in range(-4, 5):
                p = ((center + offset - 1) % 108) + 1
                padas.append(p)
                
            grid[n] = {
                "center": center,
                "padas": padas
            }
            
        return grid

    @classmethod
    def resolve_transit_mandali(cls, transit_longitude: float, moon_pada: int) -> int:
        """
        Calculates the Transit Planet's absolute pada and resolves it
        to the correct Mandali Number (1-12) relative to the Natal Moon.
        """
        transit_pada = cls.get_absolute_pada(transit_longitude)
        grid = cls.generate_mandali_grid(moon_pada)
        
        for mandali_num, data in grid.items():
            if transit_pada in data["padas"]:
                return mandali_num
                
        # Failsafe (mathematically should never be reached)
        return 1

    @classmethod
    def evaluate(cls, transit_payload: dict, natal_payload: dict) -> dict:
        """
        Evaluates the transit planets against the Moon-centered Mandali grid.
        Returns the canonical Mandali output schema.
        """
        if not transit_payload or "planets" not in transit_payload:
            return cls._stub_result()

        t_planets = transit_payload["planets"]
        moon_longitude = natal_payload.get("planets", {}).get("moon", {}).get("longitude", 0.0)
        moon_pada = cls.get_absolute_pada(moon_longitude)

        t_houses = {}
        activated_planets = []
        for p, v in t_planets.items():
            if "longitude" in v:
                m_num = cls.resolve_transit_mandali(v["longitude"], moon_pada)
                t_houses[p] = m_num
                activated_planets.append(p)

        grid = cls.generate_mandali_grid(moon_pada)
        sat_house = t_houses.get("saturn", 0)
        activated_zones = list(set(t_houses.values()))

        return {
            "transit_houses": t_houses,
            "moon_pada": moon_pada,
            "grid": grid,
            "current_mandali": f"Mandali {sat_house}" if sat_house else "Unknown",
            "mandali_number": sat_house,
            "reference_moon": f"Pada {moon_pada}",
            "activated_planets": activated_planets,
            "activated_zones": activated_zones,
            "activated_bhavas": activated_zones,
            "score": 50, # Stub for TransitEngine to replace or use
            "confidence_flags": [],
            "explanation": "Mandali evaluation based on Moon position"
        }

    @classmethod
    def _stub_result(cls) -> dict:
        return {
            "transit_houses": {},
            "moon_pada": 0,
            "grid": {},
            "current_mandali": "Unknown",
            "mandali_number": 0,
            "reference_moon": "Unknown",
            "activated_planets": [],
            "activated_zones": [],
            "activated_bhavas": [],
            "score": 50,
            "confidence_flags": ["transit_stub_no_input"],
            "explanation": "No transit data supplied"
        }

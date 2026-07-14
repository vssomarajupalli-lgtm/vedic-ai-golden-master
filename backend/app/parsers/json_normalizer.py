class JsonNormalizer:
    """
    Transforms raw, unformatted extraction data into the stable, 
    deterministic JSON schema required by the astrology engines.
    Acts as a firewall preventing parser bugs from crashing calculations.
    """
    
    def __init__(self):
        # Dictionaries to map common PDF variations to standard system keys
        self.planet_map = {
            "su": "sun", "surya": "sun", 
            "mo": "moon", "chandra": "moon",
            "ma": "mars", "mangala": "mars", "kuja": "mars",
            "me": "mercury", "budha": "mercury",
            "ju": "jupiter", "guru": "jupiter",
            "ve": "venus", "shukra": "venus",
            "sa": "saturn", "shani": "saturn",
            "ra": "rahu",
            "ke": "ketu",
            "lagna": "ascendant", "ascendant": "ascendant"
        }
        
        self.sign_map = {
            # --- Aries ---
            "ar": "aries", "ari": "aries", "mesha": "aries", "mesh": "aries",

            # --- Taurus ---
            "ta": "taurus", "tau": "taurus",
            "vrishabha": "taurus", "vrishaba": "taurus", "vrushabha": "taurus",

            # --- Gemini ---
            "ge": "gemini", "gem": "gemini",
            "mithuna": "gemini", "mithun": "gemini", "mithunam": "gemini",

            # --- Cancer ---
            "ca": "cancer", "can": "cancer",
            "kataka": "cancer", "karka": "cancer", "karkataka": "cancer",
            "katakam": "cancer",

            # --- Leo ---
            "le": "leo",
            "simha": "leo", "singh": "leo", "simham": "leo",

            # --- Virgo ---
            "vi": "virgo", "vir": "virgo",
            "kanya": "virgo", "kani": "virgo", "kanyam": "virgo",

            # --- Libra ---
            "li": "libra", "lib": "libra",
            "tula": "libra", "thula": "libra", "tulam": "libra",

            # --- Scorpio ---
            "sc": "scorpio", "sco": "scorpio",
            "vrishchika": "scorpio", "vrischika": "scorpio", "vrischikam": "scorpio",
            "vruschika": "scorpio", "scorpius": "scorpio",

            # --- Sagittarius ---
            "sa": "sagittarius", "sag": "sagittarius",
            "dhanu": "sagittarius", "dhanus": "sagittarius", "dhanush": "sagittarius",
            "dhanussu": "sagittarius",

            # --- Capricorn ---
            "cp": "capricorn", "cap": "capricorn",
            "makara": "capricorn", "makar": "capricorn", "makaram": "capricorn",

            # --- Aquarius ---
            "aq": "aquarius", "aqu": "aquarius",
            "kumbha": "aquarius", "kumbam": "aquarius",

            # --- Pisces ---
            "pi": "pisces", "pis": "pisces",
            "meena": "pisces", "meen": "pisces", "meenam": "pisces",
            "meena rasi": "pisces",
        }

    def normalize(self, raw_data: dict) -> dict:
        """Main entry point to normalize a complete raw extraction dictionary."""
        print("====== DEBUG START ======")
        print("JsonNormalizer received keys:", list(raw_data.keys()))
        normalized_planets = self._normalize_planets(raw_data.get("raw_planets") or raw_data.get("planets", {}))
        print("Normalized Planets Count:", len(normalized_planets))
        return {
            "metadata": self._normalize_metadata(raw_data.get("raw_metadata") or raw_data.get("metadata") or raw_data.get("birth_data", {})),
            "planets": normalized_planets,
            "houses": self._normalize_houses(raw_data.get("raw_houses") or raw_data.get("houses", {})),
            "vargas": self._normalize_vargas(raw_data.get("raw_vargas") or raw_data.get("vargas", {}), normalized_planets),
            "ashtakavarga": self._normalize_ashtakavarga(raw_data.get("raw_ashtakavarga") or raw_data.get("ashtakavarga", {})),
            "dashas": self._normalize_dashas(raw_data.get("raw_dashas") or raw_data.get("dashas", {})),
            "shadbala": self._normalize_shadbala(raw_data.get("raw_shadbala") or raw_data.get("shadbala", {})),
            "bhava_bala": self._normalize_bhava_bala(raw_data.get("raw_bhava_bala") or raw_data.get("bhava_bala", {})),
            "doshas": self._normalize_doshas(raw_data.get("raw_doshas") or raw_data.get("doshas", {})),
            "transits": {         # Placeholder for Phase 7 Transit Engine
                "active_modifiers": []
            }
        }

    def _normalize_metadata(self, raw_metadata: dict) -> dict:
        return {
            "name": self._clean_string(raw_metadata.get("name", "Unknown")),
            "ascendant_sign": self._clean_name(raw_metadata.get("lagna", ""), self.sign_map) or "aries",
            "ascendant_degree": self._extract_float(raw_metadata.get("lagna_degree", 0.0)),
            "dob": self._normalize_date(raw_metadata.get("birth_date") or raw_metadata.get("dob") or raw_metadata.get("date_of_birth") or ""),
            "tob": self._clean_string(raw_metadata.get("birth_time") or raw_metadata.get("tob") or raw_metadata.get("time_of_birth") or "Unknown"),
            "pob": self._clean_string(raw_metadata.get("birth_place") or raw_metadata.get("pob") or raw_metadata.get("place_of_birth") or "Unknown"),
            "latitude": self._extract_float(raw_metadata.get("latitude") or raw_metadata.get("lat", 0.0)) or None,
            "longitude": self._extract_float(raw_metadata.get("longitude") or raw_metadata.get("lon", 0.0)) or None,
            "timezone": self._extract_float(raw_metadata.get("timezone") or raw_metadata.get("tz", 0.0)) or None
        }

    def _normalize_planets(self, raw_planets: dict) -> dict:
        normalized = {}
        for raw_name, p_data in raw_planets.items():
            std_name = self._clean_name(raw_name, self.planet_map)
            if not std_name:
                continue  # Skip junk rows that aren't planets
                
            normalized[std_name] = {
                "name": std_name,
                "sign": self._clean_name(p_data.get("sign", ""), self.sign_map),
                "degree": self._extract_float(p_data.get("degree", 0.0)),
                "longitude": self._calculate_longitude(
                    self._clean_name(p_data.get("sign", ""), self.sign_map),
                    self._extract_float(p_data.get("degree", 0.0))
                ),
                "nakshatra": self._clean_string(p_data.get("nakshatra", "")),
                "house": self._extract_int(p_data.get("house", 0)),
                "house_type": self._clean_string(p_data.get("house_type", "neutral")),
                "dignity": self._clean_string(p_data.get("dignity", "neutral")),
                "is_retrograde": self._extract_boolean(p_data.get("retrograde")),
                "is_combust": self._extract_boolean(p_data.get("combust")),
                "conjunctions": [self._clean_name(c, self.planet_map) for c in p_data.get("conjunctions", []) if self._clean_name(c, self.planet_map)],
                "benefic_aspects_count": self._extract_int(p_data.get("benefic_aspects", 0)),
                "malefic_aspects_count": self._extract_int(p_data.get("malefic_aspects", 0)),
                "aspected_by": [self._clean_name(a, self.planet_map) for a in p_data.get("aspected_by", []) if self._clean_name(a, self.planet_map)],
                "varga_data": {},
                "bav_points": self._extract_int(p_data.get("bav", 0))
            }
        return normalized

    def _normalize_vargas(self, raw_vargas: dict, d1_planets: dict) -> dict:
        """Structures Varga data and automatically detects Vargottama alignments."""
        normalized = {}
        for varga_id, varga_data in raw_vargas.items():
            v_id = varga_id.upper() # e.g., "D9", "D10"
            normalized[v_id] = {"planets": {}}
            
            # Identify Lagna sign for House derivation
            lagna_sign = ""
            for raw_name, p_data in varga_data.get("planets", {}).items():
                std_name = self._clean_name(raw_name, self.planet_map)
                if std_name == "ascendant":
                    lagna_sign = self._clean_name(p_data.get("sign", ""), self.sign_map)
                    break
            
            SIGNS_IN_ORDER = [
                "aries", "taurus", "gemini", "cancer", "leo", "virgo",
                "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
            ]
            lagna_idx = SIGNS_IN_ORDER.index(lagna_sign) if lagna_sign in SIGNS_IN_ORDER else -1
            
            for raw_name, p_data in varga_data.get("planets", {}).items():
                std_name = self._clean_name(raw_name, self.planet_map)
                if not std_name:
                    continue # Skip junk
                    
                varga_sign = self._clean_name(p_data.get("sign", ""), self.sign_map)
                d1_sign = d1_planets.get(std_name, {}).get("sign", "")
                
                # Derive House Number from Varga Lagna
                house_num = 0
                if lagna_idx != -1 and varga_sign in SIGNS_IN_ORDER:
                    planet_sign_idx = SIGNS_IN_ORDER.index(varga_sign)
                    house_num = (planet_sign_idx - lagna_idx) % 12 + 1
                
                normalized[v_id]["planets"][std_name] = {
                    "sign": varga_sign,
                    "house": house_num,
                    "degree": self._extract_float(p_data.get("degree", 0.0)),
                    "longitude": self._calculate_longitude(
                        varga_sign,
                        self._extract_float(p_data.get("degree", 0.0))
                    ),
                    "dignity": self._clean_string(p_data.get("dignity", "neutral")),
                    "is_vargottama": bool(varga_sign and d1_sign and varga_sign == d1_sign)
                }
        return normalized

    def _normalize_dashas(self, raw_dashas: dict) -> dict:
        """Structures the active time periods extracted from the PDF timeline."""
        normalized = {
            "mahadasha": {
                "lord": self._clean_name(raw_dashas.get("mahadasha", ""), self.planet_map)
            },
            "antardasha": {
                "lord": self._clean_name(raw_dashas.get("antardasha", ""), self.planet_map)
            },
            "pratyantardasha": {
                "lord": self._clean_name(raw_dashas.get("pratyantardasha", ""), self.planet_map)
            }
        }
        
        if "timeline" in raw_dashas:
            # We preserve the canonical timeline structure directly, optionally cleaning lords
            timeline = []
            for row in raw_dashas.get("timeline", []):
                timeline.append({
                    "mahadasha": self._clean_name(row.get("mahadasha", ""), self.planet_map),
                    "antardasha": self._clean_name(row.get("antardasha", ""), self.planet_map),
                    "pratyantardasha": self._clean_name(row.get("pratyantardasha", ""), self.planet_map),
                    "start_date": self._normalize_date(row.get("start_date", "")),
                    "age_years": self._extract_float(row.get("age_years", 0.0))
                })
            normalized["timeline"] = timeline
            
        if "birth_balance" in raw_dashas:
            normalized["birth_balance"] = raw_dashas["birth_balance"]
            
        return normalized

    def _normalize_houses(self, raw_houses: dict) -> dict:
        """
        Normalizes raw house data for all 12 bhavas.

        Accepts the raw_houses dict passed through by HoroscopeSourceLoader.
        Each key is a house number string ("1"–"12").

        Normalized fields per house:
            house        (int)  : House number 1–12
            house_type   (str)  : Kendra / Trikona / Dusthana / Upachaya / Neutral
            sign         (str)  : Zodiac sign of the house (normalized via sign_map)
            lord         (str)  : Ruling planet (normalized via planet_map)
            occupants    (list) : Planets present in the house (planet_map normalized)
            aspected_by  (list) : Planets aspecting the house (planet_map normalized)
            sav_points   (int)  : Sarvashtakavarga bindus (0 if absent)

        Houses with missing or unparseable keys receive safe neutral defaults.
        Houses beyond 1–12 range are silently rejected.
        """
        normalized = {}

        for raw_key, h_data in raw_houses.items():
            # --- Validate and extract house number ---
            house_num = self._extract_int(raw_key)
            if house_num < 1 or house_num > 12:
                continue  # Reject out-of-range keys defensively

            if not isinstance(h_data, dict):
                continue  # Reject malformed entries

            # --- Normalize occupants: raw planet names → standard system names ---
            raw_occupants = h_data.get("occupants", [])
            occupants = [
                self._clean_name(p, self.planet_map)
                for p in raw_occupants
                if self._clean_name(p, self.planet_map)
            ]

            # --- Normalize aspected_by: same planet_map pass-through ---
            raw_aspects = h_data.get("aspected_by", [])
            aspected_by = [
                self._clean_name(p, self.planet_map)
                for p in raw_aspects
                if self._clean_name(p, self.planet_map)
            ]

            # --- Assemble normalized house record ---
            normalized[str(house_num)] = {
                "house":       house_num,
                "house_type":  self._clean_string(h_data.get("house_type", "neutral")),
                "sign":        self._clean_name(h_data.get("sign", ""), self.sign_map),
                "lord":        self._clean_name(h_data.get("lord", ""), self.planet_map),
                "occupants":   occupants,
                "aspected_by": aspected_by,
                "sav_points":  self._extract_int(h_data.get("sav_points", 0))
            }

        return normalized

    def _normalize_ashtakavarga(self, raw_av: dict) -> dict:
        """
        Normalizes the raw Ashtakavarga data extracted by HoroscopeSourceLoader.

        SAV Chart normalization:
            - Keys normalized to str(1)–str(12)
            - Bindu values coerced to int via _extract_int()

        BAV Charts normalization:
            - Planet name keys normalized through planet_map
            - House keys normalized to str(1)–str(12)
            - Bindu values coerced to int via _extract_int()
            - Rahu and Ketu are excluded (no BAV charts in classical Parashari AV)
            - Out-of-range house keys (< 1 or > 12) silently rejected

        Returns safe empty dicts on missing or malformed input.
        """
        if not raw_av or not isinstance(raw_av, dict):
            return {"sav_chart": {}, "bav_charts": {}}

        # --- Normalize SAV chart ---
        sav_normalized = {}
        for raw_sign, bindus in raw_av.get("sav_chart", {}).items():
            std_sign = self._clean_name(raw_sign, self.sign_map)
            if std_sign:
                sav_normalized[std_sign] = self._extract_int(bindus)

        # --- Normalize BAV charts ---
        # Classical Parashari AV includes 7 planets (excludes Rahu/Ketu)
        excluded_planets = {"rahu", "ketu"}
        bav_normalized = {}

        for raw_planet, sign_bindus in raw_av.get("bav_charts", {}).items():
            std_planet = self._clean_name(raw_planet, self.planet_map)
            if not std_planet or std_planet in excluded_planets:
                continue
            if not isinstance(sign_bindus, dict):
                continue

            planet_bav = {}
            for raw_sign, bindus in sign_bindus.items():
                std_sign = self._clean_name(raw_sign, self.sign_map)
                if std_sign:
                    planet_bav[std_sign] = self._extract_int(bindus)

            if planet_bav:
                bav_normalized[std_planet] = planet_bav

        return {
            "sav_chart":  sav_normalized,
            "bav_charts": bav_normalized
        }

    def _normalize_shadbala(self, raw_shadbala: dict) -> dict:
        normalized = {}
        if not isinstance(raw_shadbala, dict):
            return normalized
            
        for raw_name, s_data in raw_shadbala.items():
            std_name = self._clean_name(raw_name, self.planet_map)
            if not std_name:
                continue
            
            sthana = self._extract_float(s_data.get("sthana_bala", 0.0))
            dig = self._extract_float(s_data.get("dig_bala", 0.0))
            kala = self._extract_float(s_data.get("kala_bala", 0.0))
            cheshta = self._extract_float(s_data.get("cheshta_bala", 0.0))
            naisargika = self._extract_float(s_data.get("naisargika_bala", 0.0))
            drik = self._extract_float(s_data.get("drik_bala", 0.0))
            
            total_strength = self._extract_float(s_data.get("total_strength", s_data.get("total_bala", 0.0)))
                
            normalized[std_name] = {
                "sthana_bala": sthana,
                "dig_bala": dig,
                "kala_bala": kala,
                "cheshta_bala": cheshta,
                "naisargika_bala": naisargika,
                "drik_bala": drik,
                "total_strength": total_strength,
                "required_percentage": self._extract_float(s_data.get("required_percentage", 0.0))
            }
        return normalized

    def _normalize_bhava_bala(self, raw_bhava_bala: dict) -> dict:
        normalized = {}
        if not isinstance(raw_bhava_bala, dict):
            return normalized
            
        for raw_house, b_data in raw_bhava_bala.items():
            house_num = self._extract_int(raw_house)
            if house_num < 1 or house_num > 12:
                continue
                
            normalized[str(house_num)] = {
                "lord_strength": self._extract_float(b_data.get("lord_strength", 0.0)),
                "dig_bala": self._extract_float(b_data.get("dig_bala", 0.0)),
                "drishti_bala": self._extract_float(b_data.get("drishti_bala", 0.0)),
                "total_bala": self._extract_float(b_data.get("total_bala", 0.0))
            }
        return normalized

    def _normalize_doshas(self, raw_doshas: dict) -> dict:
        """Passes through dosha data unmodified for backend processing."""
        if not isinstance(raw_doshas, dict):
            return {}
        return raw_doshas

    # --- Isolated Helper Methods ---

    def _clean_string(self, val: any) -> str:
        return str(val).strip().lower() if val else ""

    def _normalize_date(self, date_str: str) -> str:
        if not date_str or str(date_str).strip().lower() == "unknown":
            return "Unknown"
        import datetime
        import re
        val = str(date_str).strip()
        
        # Clean out non-ASCII and fix spacing for OCR artifacts
        val = re.sub(r'[^\x00-\x7F]+', '', val)
        val = re.sub(r'\s*-\s*', '-', val)
        val = re.sub(r'\s*/\s*', '/', val)
        val = re.sub(r'\s+', ' ', val).strip()

        formats = ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d", "%d %b %Y", "%d %B %Y"]
        for fmt in formats:
            try:
                dt = datetime.datetime.strptime(val, fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                pass
        return str(date_str).strip()

    def _clean_name(self, val: str, mapping_dict: dict) -> str:
        cleaned = self._clean_string(val)
        return mapping_dict.get(cleaned, cleaned)

    def _extract_float(self, val: any) -> float:
        if isinstance(val, str) and ":" in val:
            parts = val.split(":")
            if len(parts) == 3:
                try:
                    return round(float(parts[0]) + float(parts[1])/60 + float(parts[2])/3600, 4)
                except ValueError:
                    return 0.0
            elif len(parts) == 2:
                try:
                    return round(float(parts[0]) + float(parts[1])/60, 4)
                except ValueError:
                    return 0.0
        try: return float(val)
        except (ValueError, TypeError): return 0.0

    def _extract_int(self, val: any) -> int:
        try: return int(float(val)) # float cast first handles strings like "14.0"
        except (ValueError, TypeError): return 0

    def _extract_boolean(self, value: any) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            v = value.strip().lower()
            return v in ("true", "yes", "1", "y", "r", "retrograde", "c", "combust")
        return bool(value)

    def _calculate_longitude(self, sign_name: str, degree: float) -> float:
        """Helper to compute absolute 0-360 longitude from sign and degree."""
        SIGNS_IN_ORDER = [
            "aries", "taurus", "gemini", "cancer", "leo", "virgo",
            "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
        ]
        try:
            sign_idx = SIGNS_IN_ORDER.index(sign_name)
            return round((sign_idx * 30.0) + degree, 4)
        except ValueError:
            return degree
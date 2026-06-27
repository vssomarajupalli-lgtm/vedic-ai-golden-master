from app.config.yoga_registry import YOGA_REGISTRY

class YogaEngine:
    """
    Yoga Engine for detection and classification only.
    No scores, probabilities, or mathematical weights are applied.
    """
    
    def __init__(self, calibration=None):
        if calibration is None:
            from app.calibration.calibration_manager import CalibrationManager
            calibration = CalibrationManager()
        self.registry = YOGA_REGISTRY

    def evaluate(self, chart_data: dict, planet_results: dict = None, house_results: dict = None) -> dict:
        """
        Detects yogas present in the chart and categorizes them by house.
        """
        results = {f"house_{i}_yogas": [] for i in range(1, 13)}
        results["universal_yogas"] = []
        results["yoga_traces"] = {}
        
        def add_trace(name: str, trace: dict):
            results["yoga_traces"][name] = trace
            if trace["status"] == "PASSED":
                info = self.registry.get(name)
                if not info: return
                houses = info.get("houses", [])
                for h in houses:
                    if h == "universal":
                        if name not in results["universal_yogas"]:
                            results["universal_yogas"].append(name)
                    else:
                        h_key = f"house_{h}_yogas"
                        if h_key in results and name not in results[h_key]:
                            results[h_key].append(name)

        # --- UNIVERSAL YOGAS ---
        add_trace("Gaja Kesari Yoga", self._detect_gaja_kesari_yoga(chart_data))
        add_trace("Neecha Bhanga Raja Yoga", self._detect_neecha_bhanga_raja_yoga(chart_data))
        add_trace("Adhi Yoga", self._detect_adhi_yoga(chart_data))

        # --- PANCHA MAHAPURUSHA YOGAS ---
        add_trace("Ruchaka Yoga", self._detect_ruchaka_yoga(chart_data))
        add_trace("Bhadra Yoga", self._detect_bhadra_yoga(chart_data))
        add_trace("Hamsa Yoga", self._detect_hamsa_yoga(chart_data))
        add_trace("Malavya Yoga", self._detect_malavya_yoga(chart_data))
        add_trace("Sasa Yoga", self._detect_sasa_yoga(chart_data))

        # --- WEALTH YOGAS ---
        add_trace("Dhana Yoga", self._detect_dhana_yoga(chart_data))
        add_trace("Lakshmi Yoga", self._detect_lakshmi_yoga(chart_data))
        add_trace("Vasumathi Yoga", self._detect_vasumathi_yoga(chart_data))

        # --- CAREER YOGAS ---
        add_trace("Raja Yoga", self._detect_raja_yoga(chart_data))
        add_trace("Dharma Karma Adhipati Yoga", self._detect_dharma_karma_adhipati_yoga(chart_data))
        add_trace("Amala Yoga", self._detect_amala_yoga(chart_data))

        # --- EDUCATION YOGAS ---
        add_trace("Saraswati Yoga", self._detect_saraswati_yoga(chart_data))
        add_trace("Vidya Yoga", self._detect_vidya_yoga(chart_data))

        # --- MARRIAGE YOGAS ---
        add_trace("Kalatra Yoga", self._detect_kalatra_yoga(chart_data))
        add_trace("Saubhagya Yoga", self._detect_saubhagya_yoga(chart_data))

        # --- CHILDREN YOGAS ---
        add_trace("Putra Yoga", self._detect_putra_yoga(chart_data))
        add_trace("Santana Yoga", self._detect_santana_yoga(chart_data))

        # --- SPIRITUAL YOGAS ---
        add_trace("Moksha Yoga", self._detect_moksha_yoga(chart_data))
        add_trace("Sanyasa Yoga", self._detect_sanyasa_yoga(chart_data))
        add_trace("Parivraja Yoga", self._detect_parivraja_yoga(chart_data))

        return results

    # -------------------------------------------------------------------------
    # Detection Stubs
    # -------------------------------------------------------------------------

    def _get_planet_house(self, chart_data: dict, planet: str) -> int:
        return chart_data.get("planets", {}).get(planet, {}).get("house", -1)

    def _get_planet_dignity(self, chart_data: dict, planet: str) -> str:
        return chart_data.get("planets", {}).get(planet, {}).get("dignity", "neutral")

    def _get_lord_of_house(self, chart_data: dict, house: int) -> str:
        return chart_data.get("houses", {}).get(str(house), {}).get("lord", "")

    def _is_kendra(self, house: int) -> bool:
        return house in [1, 4, 7, 10]

    def _is_trikona(self, house: int) -> bool:
        return house in [1, 5, 9]

    def _build_trace(self, name: str, rules: list) -> dict:
        status = "PASSED"
        failure_reason = None
        for rule in rules:
            if not rule["result"]:
                status = "FAILED"
                if failure_reason is None:
                    failure_reason = rule.get("fail_msg", f"Rule failed: {rule['rule']}")
        
        # Clean up fail_msg from output
        clean_rules = [{"rule": r["rule"], "result": r["result"]} for r in rules]

        return {
            "yoga_name": name,
            "status": status,
            "rules": clean_rules,
            "failure_reason": failure_reason
        }

    # --- UNIVERSAL ---
    def _detect_gaja_kesari_yoga(self, chart_data: dict) -> dict:
        jup_house = self._get_planet_house(chart_data, "jupiter")
        moon_house = self._get_planet_house(chart_data, "moon")
        
        valid_placement = jup_house != -1 and moon_house != -1
        
        is_kendra = False
        if valid_placement:
            diff = (jup_house - moon_house) % 12
            if diff < 0: diff += 12
            relative_house = diff + 1
            is_kendra = self._is_kendra(relative_house)

        rules = [
            {"rule": "Jupiter and Moon must have valid house placements", "result": valid_placement, "fail_msg": "Missing house placements for Jupiter or Moon."},
            {"rule": "Jupiter must be in a Kendra from the Moon", "result": is_kendra, "fail_msg": "Jupiter is not in a Kendra from the Moon."}
        ]
        return self._build_trace("Gaja Kesari Yoga", rules)

    def _detect_neecha_bhanga_raja_yoga(self, chart_data: dict) -> dict:
        has_debilitated = False
        dispositor_in_kendra = False
        failed_planet = None

        for p, data in chart_data.get("planets", {}).items():
            if data.get("dignity") == "debilitated":
                has_debilitated = True
                failed_planet = p.capitalize()
                dispositor = chart_data.get("houses", {}).get(str(data.get("house")), {}).get("lord")
                if dispositor:
                    disp_house = self._get_planet_house(chart_data, dispositor)
                    if self._is_kendra(disp_house):
                        dispositor_in_kendra = True
                        break

        rules = [
            {"rule": "Chart must contain a debilitated planet", "result": has_debilitated, "fail_msg": "No debilitated planets found in the chart."},
            {"rule": "Debilitated planet's dispositor must be in a Kendra", "result": dispositor_in_kendra, "fail_msg": f"Dispositor of {failed_planet} is not in a Kendra." if failed_planet else "N/A"}
        ]
        return self._build_trace("Neecha Bhanga Raja Yoga", rules)

    def _detect_adhi_yoga(self, chart_data: dict) -> dict:
        moon_house = self._get_planet_house(chart_data, "moon")
        valid_moon = moon_house != -1
        
        count = 0
        if valid_moon:
            benefics = ["mercury", "jupiter", "venus"]
            for b in benefics:
                h = self._get_planet_house(chart_data, b)
                if h != -1:
                    rel = ((h - moon_house) % 12) + 1
                    if rel in [6, 7, 8]:
                        count += 1
                        
        has_benefics = count >= 2
        
        rules = [
            {"rule": "Moon must have a valid house placement", "result": valid_moon, "fail_msg": "Missing house placement for Moon."},
            {"rule": "At least 2 benefics must be in 6th, 7th, or 8th from Moon", "result": has_benefics, "fail_msg": f"Only found {count} benefics in 6, 7, 8 from Moon."}
        ]
        return self._build_trace("Adhi Yoga", rules)

    # --- PANCHA MAHAPURUSHA ---
    def _check_mahapurusha(self, chart_data: dict, planet: str, yoga_name: str) -> dict:
        h = self._get_planet_house(chart_data, planet)
        d = self._get_planet_dignity(chart_data, planet)
        
        is_kendra = self._is_kendra(h)
        is_strong = d in ["own_sign", "exalted", "moolatrikona"]
        
        rules = [
            {"rule": f"{planet.capitalize()} must be in a Kendra (1, 4, 7, 10)", "result": is_kendra, "fail_msg": f"{planet.capitalize()} is placed in house {h}, not a Kendra."},
            {"rule": f"{planet.capitalize()} must be in Own Sign, Exalted, or Moolatrikona", "result": is_strong, "fail_msg": f"{planet.capitalize()} dignity is {d}."}
        ]
        return self._build_trace(yoga_name, rules)

    def _detect_ruchaka_yoga(self, chart_data: dict) -> dict:
        return self._check_mahapurusha(chart_data, "mars", "Ruchaka Yoga")

    def _detect_bhadra_yoga(self, chart_data: dict) -> dict:
        return self._check_mahapurusha(chart_data, "mercury", "Bhadra Yoga")

    def _detect_hamsa_yoga(self, chart_data: dict) -> dict:
        return self._check_mahapurusha(chart_data, "jupiter", "Hamsa Yoga")

    def _detect_malavya_yoga(self, chart_data: dict) -> dict:
        return self._check_mahapurusha(chart_data, "venus", "Malavya Yoga")

    def _detect_sasa_yoga(self, chart_data: dict) -> dict:
        return self._check_mahapurusha(chart_data, "saturn", "Sasa Yoga")

    # --- WEALTH ---
    def _detect_dhana_yoga(self, chart_data: dict) -> dict:
        l2 = self._get_lord_of_house(chart_data, 2)
        l11 = self._get_lord_of_house(chart_data, 11)
        
        has_lords = bool(l2 and l11)
        h2 = self._get_planet_house(chart_data, l2) if l2 else -1
        h11 = self._get_planet_house(chart_data, l11) if l11 else -1
        
        same_house = has_lords and h2 == h11 and h2 != -1
        
        rules = [
            {"rule": "2nd and 11th Lords must be identifiable", "result": has_lords, "fail_msg": "Missing 2nd or 11th Lord."},
            {"rule": "2nd and 11th Lords must be conjunct in the same house", "result": same_house, "fail_msg": "2nd and 11th Lords are not in the same house."}
        ]
        return self._build_trace("Dhana Yoga", rules)

    def _detect_lakshmi_yoga(self, chart_data: dict) -> dict:
        l9 = self._get_lord_of_house(chart_data, 9)
        has_l9 = bool(l9)
        
        h9 = self._get_planet_house(chart_data, l9) if l9 else -1
        d9 = self._get_planet_dignity(chart_data, l9) if l9 else "neutral"
        
        l1 = self._get_lord_of_house(chart_data, 1)
        d1 = self._get_planet_dignity(chart_data, l1) if l1 else "neutral"
        
        is_kendra = has_l9 and self._is_kendra(h9)
        is_strong = d9 in ["own_sign", "exalted"]
        l1_not_debilitated = d1 not in ["debilitated"]
        
        rules = [
            {"rule": "9th Lord must be identifiable", "result": has_l9, "fail_msg": "Missing 9th Lord."},
            {"rule": "9th Lord must be in a Kendra", "result": is_kendra, "fail_msg": "9th Lord is not in a Kendra."},
            {"rule": "9th Lord must be in Own Sign or Exalted", "result": is_strong, "fail_msg": "9th Lord lacks required dignity."},
            {"rule": "Lagna Lord must not be debilitated", "result": l1_not_debilitated, "fail_msg": "Lagna Lord is debilitated."}
        ]
        return self._build_trace("Lakshmi Yoga", rules)

    def _detect_vasumathi_yoga(self, chart_data: dict) -> dict:
        benefics = ["jupiter", "venus", "mercury"]
        count = 0
        for b in benefics:
            h = self._get_planet_house(chart_data, b)
            if h in [3, 6, 10, 11]:
                count += 1
                
        has_benefics = count >= 2
        rules = [
            {"rule": "At least 2 benefics must be in Upachaya houses (3, 6, 10, 11)", "result": has_benefics, "fail_msg": f"Found {count} benefics in Upachaya houses."}
        ]
        return self._build_trace("Vasumathi Yoga", rules)

    # --- CAREER ---
    def _detect_raja_yoga(self, chart_data: dict) -> dict:
        l9 = self._get_lord_of_house(chart_data, 9)
        l10 = self._get_lord_of_house(chart_data, 10)
        l4 = self._get_lord_of_house(chart_data, 4)
        l5 = self._get_lord_of_house(chart_data, 5)
        
        pairs = [(l9, l10), (l4, l5), (l5, l10), (l4, l9)]
        found_conjunct = False
        
        for p1, p2 in pairs:
            if p1 and p2:
                h1 = self._get_planet_house(chart_data, p1)
                h2 = self._get_planet_house(chart_data, p2)
                if h1 == h2 and h1 != -1:
                    found_conjunct = True
                    break
                    
        rules = [
            {"rule": "A Kendra Lord must be conjunct a Trikona Lord", "result": found_conjunct, "fail_msg": "No Kendra Lord is conjunct a Trikona Lord."}
        ]
        return self._build_trace("Raja Yoga", rules)

    def _detect_dharma_karma_adhipati_yoga(self, chart_data: dict) -> dict:
        l9 = self._get_lord_of_house(chart_data, 9)
        l10 = self._get_lord_of_house(chart_data, 10)
        
        has_lords = bool(l9 and l10)
        h9 = self._get_planet_house(chart_data, l9) if l9 else -1
        h10 = self._get_planet_house(chart_data, l10) if l10 else -1
        
        conjunct = has_lords and h9 == h10 and h9 != -1
        
        rules = [
            {"rule": "9th and 10th Lords must be identifiable", "result": has_lords, "fail_msg": "Missing 9th or 10th Lord."},
            {"rule": "9th and 10th Lords must be conjunct", "result": conjunct, "fail_msg": "9th and 10th Lords are not conjunct."}
        ]
        return self._build_trace("Dharma Karma Adhipati Yoga", rules)

    def _detect_amala_yoga(self, chart_data: dict) -> dict:
        found_benefic = False
        for b in ["jupiter", "venus", "mercury", "moon"]:
            if self._get_planet_house(chart_data, b) == 10:
                found_benefic = True
                break
                
        rules = [
            {"rule": "A natural benefic must be in the 10th house from Lagna", "result": found_benefic, "fail_msg": "No natural benefic found in the 10th house."}
        ]
        return self._build_trace("Amala Yoga", rules)

    # --- EDUCATION ---
    def _detect_saraswati_yoga(self, chart_data: dict) -> dict:
        all_in_kendra_trikona = True
        failed_planet = None
        for b in ["jupiter", "venus", "mercury"]:
            h = self._get_planet_house(chart_data, b)
            if not (self._is_kendra(h) or self._is_trikona(h) or h == 2):
                all_in_kendra_trikona = False
                failed_planet = b.capitalize()
                break
                
        jup_strong = self._get_planet_dignity(chart_data, "jupiter") in ["own_sign", "exalted"]
        
        rules = [
            {"rule": "Jupiter, Venus, and Mercury must be in Kendra, Trikona, or 2nd house", "result": all_in_kendra_trikona, "fail_msg": f"{failed_planet} is poorly placed."},
            {"rule": "Jupiter must be in Own Sign or Exalted", "result": jup_strong, "fail_msg": "Jupiter lacks required dignity."}
        ]
        return self._build_trace("Saraswati Yoga", rules)

    def _detect_vidya_yoga(self, chart_data: dict) -> dict:
        found_benefic = False
        for b in ["jupiter", "venus", "mercury"]:
            if self._get_planet_house(chart_data, b) == 5:
                found_benefic = True
                break
                
        rules = [
            {"rule": "A natural benefic must be in the 5th house", "result": found_benefic, "fail_msg": "No natural benefic found in the 5th house."}
        ]
        return self._build_trace("Vidya Yoga", rules)

    # --- MARRIAGE ---
    def _detect_kalatra_yoga(self, chart_data: dict) -> dict:
        d_ven = self._get_planet_dignity(chart_data, "venus")
        l7 = self._get_lord_of_house(chart_data, 7)
        d_l7 = self._get_planet_dignity(chart_data, l7) if l7 else "neutral"
        
        ven_strong = d_ven in ["own_sign", "exalted"]
        l7_strong = d_l7 in ["own_sign", "exalted"]
        
        rules = [
            {"rule": "Venus must be in Own Sign or Exalted", "result": ven_strong, "fail_msg": "Venus lacks required dignity."},
            {"rule": "7th Lord must be in Own Sign or Exalted", "result": l7_strong, "fail_msg": "7th Lord lacks required dignity."}
        ]
        return self._build_trace("Kalatra Yoga", rules)

    def _detect_saubhagya_yoga(self, chart_data: dict) -> dict:
        l7 = self._get_lord_of_house(chart_data, 7)
        l9 = self._get_lord_of_house(chart_data, 9)
        
        has_lords = bool(l7 and l9)
        h7 = self._get_planet_house(chart_data, l7) if l7 else -1
        h9 = self._get_planet_house(chart_data, l9) if l9 else -1
        
        conjunct = has_lords and h7 == h9 and h7 != -1
        
        rules = [
            {"rule": "7th and 9th Lords must be identifiable", "result": has_lords, "fail_msg": "Missing 7th or 9th Lord."},
            {"rule": "7th and 9th Lords must be conjunct", "result": conjunct, "fail_msg": "7th and 9th Lords are not conjunct."}
        ]
        return self._build_trace("Saubhagya Yoga", rules)

    # --- CHILDREN ---
    def _detect_putra_yoga(self, chart_data: dict) -> dict:
        l5 = self._get_lord_of_house(chart_data, 5)
        has_l5 = bool(l5)
        
        h5 = self._get_planet_house(chart_data, l5) if l5 else -1
        d5 = self._get_planet_dignity(chart_data, l5) if l5 else "neutral"
        
        l5_strong = d5 in ["own_sign", "exalted"]
        l5_well_placed = h5 in [1, 5, 9, 10, 11]
        
        rules = [
            {"rule": "5th Lord must be identifiable", "result": has_l5, "fail_msg": "Missing 5th Lord."},
            {"rule": "5th Lord must be in Own Sign or Exalted", "result": l5_strong, "fail_msg": "5th Lord lacks required dignity."},
            {"rule": "5th Lord must be in a supportive house (1, 5, 9, 10, 11)", "result": l5_well_placed, "fail_msg": "5th Lord is poorly placed."}
        ]
        return self._build_trace("Putra Yoga", rules)

    def _detect_santana_yoga(self, chart_data: dict) -> dict:
        l5 = self._get_lord_of_house(chart_data, 5)
        has_l5 = bool(l5)
        
        h5 = self._get_planet_house(chart_data, l5) if l5 else -1
        hj = self._get_planet_house(chart_data, "jupiter")
        
        conjunct = has_l5 and h5 == hj and h5 != -1
        
        rules = [
            {"rule": "5th Lord must be identifiable", "result": has_l5, "fail_msg": "Missing 5th Lord."},
            {"rule": "5th Lord must be conjunct Jupiter", "result": conjunct, "fail_msg": "5th Lord is not conjunct Jupiter."}
        ]
        return self._build_trace("Santana Yoga", rules)

    # --- SPIRITUAL ---
    def _detect_moksha_yoga(self, chart_data: dict) -> dict:
        ketu_12 = self._get_planet_house(chart_data, "ketu") == 12
        rules = [
            {"rule": "Ketu must be in the 12th house", "result": ketu_12, "fail_msg": "Ketu is not in the 12th house."}
        ]
        return self._build_trace("Moksha Yoga", rules)

    def _detect_sanyasa_yoga(self, chart_data: dict) -> dict:
        houses = {}
        for p, data in chart_data.get("planets", {}).items():
            if p not in ["rahu", "ketu"]:
                h = data.get("house")
                houses[h] = houses.get(h, 0) + 1
        
        four_planets = any(v >= 4 for v in houses.values())
        rules = [
            {"rule": "4 or more true planets must be conjunct in a single house", "result": four_planets, "fail_msg": "No house contains 4 or more planets."}
        ]
        return self._build_trace("Sanyasa Yoga", rules)

    def _detect_parivraja_yoga(self, chart_data: dict) -> dict:
        h_moon = self._get_planet_house(chart_data, "moon")
        h_sat = self._get_planet_house(chart_data, "saturn")
        
        valid = h_moon != -1 and h_sat != -1
        diff = abs(h_moon - h_sat) if valid else -1
        aspected = diff == 0 or diff == 6
        
        rules = [
            {"rule": "Moon and Saturn must have valid placements", "result": valid, "fail_msg": "Missing placements for Moon or Saturn."},
            {"rule": "Moon must be conjunct or opposite Saturn", "result": aspected, "fail_msg": "Moon and Saturn are neither conjunct nor opposite."}
        ]
        return self._build_trace("Parivraja Yoga", rules)

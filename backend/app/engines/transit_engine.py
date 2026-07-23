"""
TransitEngine — Deterministic Gochara Transit Scoring Engine
=============================================================

Evaluates current planetary transits against a natal chart to produce a
single `activation_score` [0-100] that replaces the transit_trigger stub
in MasterProbabilityEngine.

Classical foundation: Parashari Gochara (transit quality per house),
Ashtakavarga transit validation, Vedha obstruction, and Dasha-Transit
synchronisation.

Architecture Rules (all enforced here):
    Rule 4: Zero astrological recalculation — consumes pre-computed scores only.
    Rule 2: No AI/ML — pure arithmetic.
    Rule 5: Stateless — no runtime state between calls.
    Rule 6: clamp_score() applied at all output boundaries.
    Rule 10: Pure stdlib — no external dependencies.

Stub fallback: if `transit_payload` is absent or contains no planets, the
engine returns activation_score=50 (neutral) with a "transit_stub_no_input"
confidence flag. All existing tests that do not supply transit positions
continue to pass unchanged.
"""

from app.config.astrology_constants import (
    TRANSIT_HOUSE_QUALITY,
    TRANSIT_CONJUNCTION_MATRIX,
    TRANSIT_ASPECT_WEIGHTS,
    TRANSIT_SPECIAL_ASPECTS,
    TRANSIT_SPECIAL_ASPECT_WEIGHT,
    TRANSIT_WEIGHTS,
    TRANSIT_VEDHA_CAP,
    TRANSIT_DASHA_SYNC_BONUSES,
    VEDHA_PAIRS,
    NATURAL_BENEFICS,
    NATURAL_MALEFICS,
    PROBABILITY_GRADES,
    DOMAIN_CONFIG,
)
from app.utils.astrology_math import clamp_score
from app.engines.mandali_generator import MandaliGenerator


class TransitEngine:
    """
    Deterministic transit scoring engine (Gochara System).

    Consumes:
        transit_payload       — current transit planet positions {planet: {house, sign, degree}}
        natal_payload         — JsonNormalizer output (normalized_payload)
        dasha_results         — DashaEngine outputs (timing multipliers)
        av_results            — AshtakavargaEngine outputs (BAV charts)
        natal_promise_results — NatalPromiseEngine domain promise scores

    Produces:
        activation_score    — [0, 100]  feeds MasterProbabilityEngine 5% weight
        grade               — PROBABILITY_GRADES label
        activated_domains   — per-domain transit score dict
        supporting_factors  — list of positive transit factor dicts
        obstructing_factors — list of negative transit factor dicts
        breakdown           — per sub-system scores
        confidence_flags    — string flags (e.g. "saturn_sadesati")
        stub_factors        — ["all"] when no transit data supplied
        transit_houses      — resolved transit house positions per planet
    """

    # Natural benefics and malefics (reuses constants, stored locally for fast lookup)
    _BENEFIC_PLANETS = set(NATURAL_BENEFICS)   # jupiter, venus, moon, mercury
    _MALEFIC_PLANETS = set(NATURAL_MALEFICS)   # saturn, mars, sun, rahu, ketu

    def __init__(self, calibration=None):
        if calibration is None:
            from app.calibration.calibration_manager import CalibrationManager
            calibration = CalibrationManager()
        self.weights       = calibration.transit.get('TRANSIT_WEIGHTS', {})
        self.vedha_pairs   = calibration.transit.get('VEDHA_PAIRS', {})
        self.house_quality = calibration.transit.get('TRANSIT_HOUSE_QUALITY', {})
        self.conj_matrix   = calibration.transit.get('TRANSIT_CONJUNCTION_MATRIX', {})
        self.aspect_weights = calibration.transit.get('TRANSIT_ASPECT_WEIGHTS', {})
        self.special_aspects = calibration.transit.get('TRANSIT_SPECIAL_ASPECTS', {})
        self.special_weight  = calibration.transit.get('TRANSIT_SPECIAL_ASPECT_WEIGHT', 0)
        self.vedha_cap     = calibration.transit.get('TRANSIT_VEDHA_CAP', 0)
        self.sync_bonuses  = calibration.transit.get('TRANSIT_DASHA_SYNC_BONUSES', {})
        self.stub_score    = 50.0

    # -------------------------------------------------------------------------
    # Public Interface
    # -------------------------------------------------------------------------

    def evaluate(
        self,
        transit_payload:       dict,
        natal_payload:         dict,
        dasha_results:         dict = None,
        av_results:            dict = None,
        natal_promise_results: dict = None,
    ) -> dict:
        """
        Evaluates all five transit sub-systems and returns the full result dict.

        Args:
            transit_payload       (dict): Current transit positions — {"planets": {planet: {house, sign, degree}}}
            natal_payload         (dict): JsonNormalizer output (normalized_payload).
            dasha_results         (dict): DashaEngine outputs.
            av_results            (dict): AshtakavargaEngine outputs.
            natal_promise_results (dict): NatalPromiseEngine per-domain promise scores.

        Returns:
            dict: Full transit evaluation payload (see class docstring).
        """
        dasha_results         = dasha_results or {}
        av_results            = av_results or {}
        natal_promise_results = natal_promise_results or {}

        transit_planets = (transit_payload or {}).get("planets", {})

        # Graceful stub fallback — no transit data supplied
        if not transit_planets:
            return self._stub_result()

        natal_planets = natal_payload.get("planets", {}) if natal_payload else {}

        # --- Normalize transit planet house numbers (Mandali injection point) ---
        moon_longitude = natal_planets.get("moon", {}).get("longitude", None)
        moon_pada = None
        if moon_longitude is not None:
            moon_pada = MandaliGenerator.get_absolute_pada(moon_longitude)
            
        t_houses = {}
        for p, v in transit_planets.items():
            if "longitude" in v and moon_pada is not None:
                # Phase 7 Governance: Moon-Centered Mandali Resolution
                t_houses[p] = MandaliGenerator.resolve_transit_mandali(v["longitude"], moon_pada)
            else:
                # Legacy fallback for tests supplying only classical {house: N} mocks
                t_houses[p] = int(v.get("house", 0))

        # --- Run all 5 sub-systems ---
        house_act, house_factors    = self._compute_house_activation(t_houses)
        bav_support                 = self._compute_bav_support(t_houses, av_results)
        planet_act, planet_factors  = self._compute_planet_activation(t_houses, natal_planets)
        dasha_sync, sync_factors    = self._compute_dasha_sync(t_houses, natal_planets, dasha_results, av_results)
        vedha_raw, vedha_factors    = self._compute_vedha_layer(t_houses)

        # --- Master weighted sum ---
        breakdown = {
            "house_activation":  house_act,
            "bav_support":       bav_support,
            "planet_activation": planet_act,
            "dasha_sync":        dasha_sync,
            "vedha_layer":       vedha_raw,
        }
        activation_raw = sum(breakdown[k] * self.weights[k] for k in self.weights)
        activation_score = clamp_score(activation_raw)

        # --- Domain activation ---
        activated_domains = self._compute_domain_activation(t_houses, av_results, natal_promise_results)

        # --- Collate factors ---
        all_supporting = [f for f in (house_factors + planet_factors + sync_factors + vedha_factors)
                          if f["score"] > 0]
        all_obstructing = [f for f in (house_factors + planet_factors + sync_factors + vedha_factors)
                           if f["score"] < 0]
        all_supporting.sort(key=lambda x: -x["score"])
        all_obstructing.sort(key=lambda x: x["score"])

        # --- Confidence flags ---
        flags = self._generate_confidence_flags(t_houses, natal_planets, dasha_results)

        return {
            "activation_score":   activation_score,
            "grade":              self._grade(activation_score),
            "activated_domains":  activated_domains,
            "supporting_factors": all_supporting,
            "obstructing_factors": all_obstructing,
            "breakdown":          breakdown,
            "confidence_flags":   flags,
            "stub_factors":       [],
            "transit_houses":     t_houses,
        }

    # -------------------------------------------------------------------------
    # Sub-system 1 — House Activation (30%)
    # -------------------------------------------------------------------------

    def _compute_house_activation(self, t_houses: dict) -> tuple:
        """
        Scores each transiting planet's quality in the house it occupies.

        Formula:
            house_quality(planet, transit_house) =
                TRANSIT_HOUSE_QUALITY[planet].get(house, 0)  [-8, 0, +12]

            house_activation_raw = average(per-planet quality)
            house_activation     = clamp(house_activation_raw + 50, 0, 100)

        The +50 centres the signed average onto the 0-100 scale.

        Returns:
            (int score, list of factor dicts)
        """
        scores = []
        factors = []

        for planet, house in t_houses.items():
            if house < 1 or house > 12:
                continue
            quality = self.house_quality.get(planet, {}).get(house, 0)
            scores.append(quality)
            if quality != 0:
                factors.append({
                    "factor":  f"{planet}_transits_h{house}",
                    "score":   quality,
                    "planet":  planet,
                    "house":   house,
                    "source":  "house_activation",
                })

        if not scores:
            return 50, []

        raw_avg = sum(scores) / len(scores)
        final   = clamp_score(raw_avg + 50)
        return final, factors

    # -------------------------------------------------------------------------
    # Sub-system 2 — BAV Transit Support (20%)
    # -------------------------------------------------------------------------

    def _compute_bav_support(self, t_houses: dict, av_results: dict) -> int:
        """
        Validates each transit using its BAV bindu count in the transit house.

        Formula:
            bav_score(planet, transit_house) = (bindus / 8) × 100
            bav_support = average(bav_score per planet)

        Missing BAV chart → defaults to 4 bindus (neutral, score=50).

        Returns:
            int score [0, 100]
        """
        bav_charts = (av_results or {}).get("bav_charts", {})
        scores = []

        for planet, house in t_houses.items():
            if house < 1 or house > 12:
                scores.append(50.0)   # unknown house → neutral
                continue
            planet_chart = bav_charts.get(planet, {})
            bindus = int(planet_chart.get(str(house), {}).get("bindus", 4)
                         if isinstance(planet_chart.get(str(house), {}), dict)
                         else planet_chart.get(str(house), 4))
            bav_score = round((bindus / 8) * 100, 2)
            scores.append(bav_score)

        if not scores:
            return 50

        return clamp_score(sum(scores) / len(scores))

    # -------------------------------------------------------------------------
    # Sub-system 3 — Vedha Obstruction Layer (10%)
    # -------------------------------------------------------------------------

    def _compute_vedha_layer(self, t_houses: dict) -> tuple:
        """
        Applies Vedha (obstruction) penalties when a malefic transit occupies
        the Vedha house of a positive transit.

        Only positive transits can be blocked. Negative transits are unchanged.

        Formula:
            For each planet P with positive Gochara quality in house H:
                V = VEDHA_PAIRS[H]
                If any malefic transits house V:
                    vedha_penalty -= 5 (per blocked planet)
            vedha_penalty = max(TRANSIT_VEDHA_CAP, vedha_penalty)
            vedha_layer   = clamp(50 + vedha_penalty, 0, 100)

        Returns:
            (int score, list of factor dicts)
        """
        malefic_houses = {
            house for planet, house in t_houses.items()
            if planet in self._MALEFIC_PLANETS and 1 <= house <= 12
        }

        vedha_penalty = 0
        factors = []

        for planet, house in t_houses.items():
            if house < 1 or house > 12:
                continue
            quality = self.house_quality.get(planet, {}).get(house, 0)
            if quality <= 0:
                continue   # only positive transits can be Vedha-blocked
            vedha_house = self.vedha_pairs.get(house)
            if vedha_house and vedha_house in malefic_houses:
                vedha_penalty -= 5
                factors.append({
                    "factor":  f"vedha_h{house}_by_malefic_in_h{vedha_house}",
                    "score":   -5,
                    "planet":  planet,
                    "house":   house,
                    "source":  "vedha_obstruction",
                })

        vedha_penalty = max(self.vedha_cap, vedha_penalty)
        final = clamp_score(50 + vedha_penalty)
        return final, factors

    # -------------------------------------------------------------------------
    # Sub-system 4 — Planet Activation (20%)
    # -------------------------------------------------------------------------

    def _compute_planet_activation(self, t_houses: dict, natal_planets: dict) -> tuple:
        """
        Scores transiting planets conjuncting or aspecting natal planets.

        Conjunction: transit planet in same house as natal planet.
        7th aspect: transit planet's 7th house falls on natal planet's house.
        Special aspects: Saturn (3, 10), Jupiter (5, 9), Mars (4, 8) at 60% weight.

        Formula:
            planet_activation_raw = sum(conjunction + aspect scores per pair)
            planet_activation     = clamp(planet_activation_raw + 50, 0, 100)

        Returns:
            (int score, list of factor dicts)
        """
        total = 0.0
        factors = []

        for t_planet, t_house in t_houses.items():
            if t_house < 1 or t_house > 12:
                continue
            t_nature = "benefic" if t_planet in self._BENEFIC_PLANETS else "malefic"

            for n_planet, n_data in natal_planets.items():
                n_house = int(n_data.get("house", 0))
                if n_house < 1 or n_house > 12:
                    continue
                n_nature = "benefic" if n_planet in self._BENEFIC_PLANETS else "malefic"

                # Check conjunction (same house)
                if t_house == n_house:
                    score = self.conj_matrix.get((t_planet, n_nature), 0)
                    if score != 0:
                        total += score
                        factors.append({
                            "factor":  f"{t_planet}_conjuncts_natal_{n_planet}",
                            "score":   score,
                            "planet":  t_planet,
                            "house":   t_house,
                            "source":  "conjunction",
                        })
                    continue  # conjunction takes priority over aspect

                # Check special aspects first (they include 7th)
                aspect_houses = self.special_aspects.get(t_planet, [7])
                for aspect_offset in aspect_houses:
                    aspected_house = ((t_house - 1 + aspect_offset - 1) % 12) + 1
                    if aspected_house == n_house:
                        base_score = self.aspect_weights.get((t_nature, n_nature), 0)
                        # Apply weight reduction for non-7th special aspects
                        weight = 1.0 if aspect_offset == 7 else self.special_weight
                        score  = round(base_score * weight)
                        if score != 0:
                            total += score
                            factors.append({
                                "factor":  f"{t_planet}_aspects_{aspect_offset}th_natal_{n_planet}",
                                "score":   score,
                                "planet":  t_planet,
                                "house":   t_house,
                                "source":  "aspect",
                            })
                        break  # one aspect per transit-natal planet pair

        final = clamp_score(total + 50)
        return final, factors

    # -------------------------------------------------------------------------
    # Sub-system 5 — Dasha-Transit Sync (20%)
    # -------------------------------------------------------------------------

    def _compute_dasha_sync(
        self,
        t_houses:      dict,
        natal_planets: dict,
        dasha_results: dict,
        av_results:    dict,
    ) -> tuple:
        """
        Scores alignment between current transit positions and active dasha lords.

        Starts from neutral 50 and adds bonuses for each sync condition detected.

        Formula (baseline = 50):
            +20 × md_mult   if transit_planet == MD lord
            +12 × ad_mult   if transit_planet == AD lord
            +8              if transit_planet 7th-aspects MD lord's natal house
            +5              if transit_planet 7th-aspects AD lord's natal house
            +6              if transit_planet occupies same house as MD lord natal
            +8              if MD lord has ≥5 BAV bindus in its current transit house

        sync_score = clamp(50 + total_bonus, 0, 100)

        Returns:
            (int score, list of factor dicts)
        """
        if not dasha_results:
            return 50, []

        # Extract MD / AD lords and their timing multipliers
        md_lord = None
        ad_lord = None
        md_mult = 1.0
        ad_mult = 1.0
        md_natal_house = 0
        ad_natal_house = 0

        for lord, data in dasha_results.items():
            if lord in ("synthesis", "timeline"):
                continue
            flags = data.get("confidence_flags", [])
            mult  = data.get("temporal_activation", {}).get("timing_multiplier", 1.0)
            n_house = int(natal_planets.get(lord, {}).get("house", 0))
            if "active_mahadasha" in flags:
                md_lord        = lord
                md_mult        = mult
                md_natal_house = n_house
            elif "active_antardasha" in flags:
                ad_lord        = lord
                ad_mult        = mult
                ad_natal_house = n_house

        total_bonus = 0.0
        factors     = []
        bonuses     = self.sync_bonuses

        for t_planet, t_house in t_houses.items():
            if t_house < 1 or t_house > 12:
                continue

            # Case 1: Transit planet IS the MD lord
            if t_planet == md_lord:
                bonus = round(bonuses["transit_is_md_lord"] * md_mult, 1)
                total_bonus += bonus
                factors.append({
                    "factor":  "dasha_transit_sync_md",
                    "score":   bonus,
                    "planet":  t_planet,
                    "house":   t_house,
                    "source":  "dasha_sync",
                })

            # Case 2: Transit planet IS the AD lord
            elif t_planet == ad_lord:
                bonus = round(bonuses["transit_is_ad_lord"] * ad_mult, 1)
                total_bonus += bonus
                factors.append({
                    "factor":  "dasha_transit_sync_ad",
                    "score":   bonus,
                    "planet":  t_planet,
                    "house":   t_house,
                    "source":  "dasha_sync",
                })

            # Case 3: Transit planet 7th-aspects MD lord natal house
            if md_natal_house > 0:
                seventh_from_t = ((t_house - 1 + 6) % 12) + 1
                if seventh_from_t == md_natal_house and t_planet != md_lord:
                    b = bonuses["transit_aspects_md_natal"]
                    total_bonus += b
                    factors.append({
                        "factor":  f"{t_planet}_aspects_md_lord_natal",
                        "score":   b,
                        "planet":  t_planet,
                        "house":   t_house,
                        "source":  "dasha_sync",
                    })

            # Case 4: Transit planet 7th-aspects AD lord natal house
            if ad_natal_house > 0:
                seventh_from_t = ((t_house - 1 + 6) % 12) + 1
                if seventh_from_t == ad_natal_house and t_planet != ad_lord:
                    b = bonuses["transit_aspects_ad_natal"]
                    total_bonus += b
                    factors.append({
                        "factor":  f"{t_planet}_aspects_ad_lord_natal",
                        "score":   b,
                        "planet":  t_planet,
                        "house":   t_house,
                        "source":  "dasha_sync",
                    })

            # Case 5: Transit planet in same natal house as MD lord natal
            if md_natal_house > 0 and t_house == md_natal_house and t_planet != md_lord:
                b = bonuses["transit_same_sign_as_md"]
                total_bonus += b
                factors.append({
                    "factor":  f"{t_planet}_in_md_lord_natal_house",
                    "score":   b,
                    "planet":  t_planet,
                    "house":   t_house,
                    "source":  "dasha_sync",
                })

        # Case 6: MD lord's BAV bindus in its current transit house >= 5
        if md_lord and md_lord in t_houses:
            md_transit_house = t_houses[md_lord]
            bav_charts = (av_results or {}).get("bav_charts", {})
            planet_chart = bav_charts.get(md_lord, {})
            house_entry  = planet_chart.get(str(md_transit_house), {})
            bindus = int(house_entry.get("bindus", 0)
                         if isinstance(house_entry, dict)
                         else house_entry)
            if bindus >= 5:
                b = bonuses["md_transit_bav_high"]
                total_bonus += b
                factors.append({
                    "factor":  f"md_lord_{md_lord}_transit_bav_high",
                    "score":   b,
                    "planet":  md_lord,
                    "house":   md_transit_house,
                    "source":  "dasha_sync",
                })

        final = clamp_score(50 + total_bonus)
        return final, factors

    # -------------------------------------------------------------------------
    # Domain Activation
    # -------------------------------------------------------------------------

    def _compute_domain_activation(
        self,
        t_houses:             dict,
        av_results:           dict,
        natal_promise_results: dict,
    ) -> dict:
        """
        Maps transit house quality scores to each of the 8 NatalPromise domains.

        Formula per domain:
            house_transit_score(H) = clamp(quality_for_house(H) + 50, 0, 100)
            domain_transit_score   =
                house_transit_score(primary_house)                * 0.50
                + avg(house_transit_score(support_houses))        * 0.30
                + bav_transit_score(karaka_planet, primary_house) * 0.20

        Returns:
            dict mapping domain_name → int score [0, 100]
        """
        # Pre-compute house-level transit quality scores [0, 100]
        house_transit_scores = {}
        for h in range(1, 13):
            raw_sum = 0
            count   = 0
            for planet, t_house in t_houses.items():
                if t_house == h:
                    raw_sum += self.house_quality.get(planet, {}).get(h, 0)
                    count   += 1
            # If no transit planet in this house, house quality = 0 (neutral)
            raw_avg = (raw_sum / count) if count > 0 else 0
            house_transit_scores[h] = clamp_score(raw_avg + 50)

        bav_charts = (av_results or {}).get("bav_charts", {})
        result = {}

        for domain, cfg in DOMAIN_CONFIG.items():
            primary_raw = cfg.get("primary_house", "1")
            primary_houses = [primary_raw] if isinstance(primary_raw, str) else primary_raw
            support_houses = cfg.get("support_houses", [])

            # Primary house contribution
            primary_scores = [
                house_transit_scores.get(int(h), 50) for h in primary_houses
            ]
            primary_score = sum(primary_scores) / len(primary_scores) if primary_scores else 50

            # Support house contribution
            support_scores = [
                house_transit_scores.get(int(h), 50) for h in support_houses
            ]
            support_score = sum(support_scores) / len(support_scores) if support_scores else 50

            # BAV contribution: karaka planet's BAV in the primary house
            # (use average BAV over primary houses for simplicity)
            bav_score = 50.0  # default neutral
            karaka_list = self._get_domain_karakas(domain)
            if karaka_list and primary_houses:
                ph = int(primary_houses[0])
                karaka_bav_scores = []
                for karaka in karaka_list:
                    planet_chart = bav_charts.get(karaka, {})
                    house_entry  = planet_chart.get(str(ph), {})
                    bindus = int(house_entry.get("bindus", 4)
                                 if isinstance(house_entry, dict)
                                 else house_entry)
                    karaka_bav_scores.append((bindus / 8) * 100)
                if karaka_bav_scores:
                    bav_score = sum(karaka_bav_scores) / len(karaka_bav_scores)

            domain_score = (
                primary_score * 0.50
                + support_score * 0.30
                + bav_score    * 0.20
            )
            result[domain] = clamp_score(domain_score)

        return result

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _get_domain_karakas(self, domain: str) -> list:
        """Returns the primary natural significator(s) for a domain."""
        karakas = {
            "marriage":    ["venus"],
            "career":      ["sun", "saturn"],
            "wealth":      ["jupiter", "venus"],
            "education":   ["mercury", "jupiter"],
            "children":    ["jupiter"],
            "property":    ["mars", "moon"],
            "health":      ["sun"],
            "spirituality": ["jupiter", "ketu"],
        }
        return karakas.get(domain, [])

    def _get_aspected_houses(self, planet: str, from_house: int) -> list:
        """
        Returns all houses aspected by a planet from a given house.
        Returns list of (aspected_house, aspect_weight_factor) tuples.
        Universal 7th aspect (factor=1.0) plus any planet-specific special aspects.
        """
        aspects = []
        aspect_offsets = self.special_aspects.get(planet, [7])
        for offset in aspect_offsets:
            aspected = ((from_house - 1 + offset - 1) % 12) + 1
            weight   = 1.0 if offset == 7 else self.special_weight
            aspects.append((aspected, weight))
        return aspects

    def _grade(self, score: int) -> str:
        """Maps activation_score to PROBABILITY_GRADES label."""
        for threshold, label in PROBABILITY_GRADES:
            if score >= threshold:
                return label
        return "TOO WEAK"

    def _generate_confidence_flags(
        self,
        t_houses:      dict,
        natal_planets: dict,
        dasha_results: dict,
    ) -> list:
        """
        Generates human-readable confidence flags for notable transit conditions.

        Current flags:
            "jupiter_transit_positive"  — Jupiter in a classically positive house
            "saturn_transit_negative"   — Saturn in a classically negative house
            "saturn_sadesati"           — Saturn transiting H12, H1, or H2 relative to natal Moon
            "dasha_lord_transiting"     — Transit planet matches an active dasha lord
            "all_malefics_obstructing"  — All natural malefics in negative houses
        """
        flags = []

        # Jupiter in positive house
        jup_house = t_houses.get("jupiter", 0)
        if jup_house and self.house_quality.get("jupiter", {}).get(jup_house, 0) > 0:
            flags.append("jupiter_transit_positive")

        # Saturn in negative house
        sat_house = t_houses.get("saturn", 0)
        if sat_house and self.house_quality.get("saturn", {}).get(sat_house, 0) < 0:
            flags.append("saturn_transit_negative")

        # Sadesati — Saturn transiting previous, current, or next Mandali
        # Because t_houses represents the relative Mandali (where 1 = Natal Moon),
        # Sade Sati is strictly active in Mandali 12, 1, and 2.
        if sat_house and sat_house in {12, 1, 2}:
            flags.append("saturn_sadesati")

        # Dasha lord transiting
        active_lords = set()
        for lord, data in (dasha_results or {}).items():
            if lord in ("synthesis", "timeline"):
                continue
            cf = data.get("confidence_flags", [])
            if "active_mahadasha" in cf or "active_antardasha" in cf:
                active_lords.add(lord)
        if any(p in active_lords for p in t_houses):
            flags.append("dasha_lord_transiting")

        # All natural malefics in negative houses
        malefic_planets = [p for p in self._MALEFIC_PLANETS if p in t_houses]
        if malefic_planets and all(
            self.house_quality.get(p, {}).get(t_houses[p], 0) < 0
            for p in malefic_planets
        ):
            flags.append("all_malefics_obstructing")

        return flags

    def _stub_result(self) -> dict:
        """
        Returns a neutral stub payload when no transit data is supplied.
        activation_score = 50 (neutral) — identical to the previous
        _transit_trigger_stub() return value.
        """
        return {
            "activation_score":    50,
            "grade":               "GOOD",
            "activated_domains":   {d: 50 for d in DOMAIN_CONFIG},
            "supporting_factors":  [],
            "obstructing_factors": [],
            "breakdown":           {k: 50 for k in self.weights},
            "confidence_flags":    ["transit_stub_no_input"],
            "stub_factors":        ["all"],
        }
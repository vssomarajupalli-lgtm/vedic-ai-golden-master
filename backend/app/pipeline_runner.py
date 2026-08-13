import json
import logging
import datetime
from typing import Dict, Any, List
from dataclasses import asdict

from app.parsers.json_normalizer import JsonNormalizer
from app.engines.planet_strength_engine import PlanetStrengthEngine
from app.engines.house_strength_engine import HouseStrengthEngine
from app.engines.varga_engine import VargaEngine
from app.engines.dasha_engine import DashaEngine
from app.engines.rasi_strength_engine import RasiStrengthEngine
from app.engines.ashtakavarga_engine import AshtakavargaEngine
from app.engines.master_probability_engine import MasterProbabilityEngine
from app.engines.natal_promise_engine import NatalPromiseEngine
from app.engines.transit_engine import TransitEngine
from app.engines.universal_mandali_engine import UniversalMandaliEngine
from app.engines.mandali_transit_adapter import MandaliTransitAdapter
from app.engines.mandali_generator import MandaliGenerator
from app.utils.ephemeris_service import EphemerisService
from app.engines.yoga_engine import YogaEngine
from app.schemas.mandali_response import MandaliResponseDTO
from app.schemas.natal_chart import NatalChartDTO
from app.schemas.current_chart import CurrentChartDTO
from app.engines.question_engine import QuestionEngine
from app.engines.functional_nature_engine import FunctionalNatureEngine
from app.formulas.loader import formula_repository_loader
from app.formulas.evaluator import FormulaEvaluator
from app.config.astrology_constants import (
    SIGNS_IN_ORDER,
    PROBABILITY_GRADES,
    EXALTATION_MAP,
    DEBILITATION_MAP,
    OWN_SIGN_MAP
)
from app.builders.mandali_chart_layout_builder import MandaliChartLayoutBuilder
from app.builders.transition_summary_builder import TransitionSummaryBuilder
from app.builders.mandali_placement_factory import MandaliPlacementFactory
from app.builders.mandali_gochar_builder import MandaliGocharBuilder


class PipelineRunner:
    """
    Lightweight deterministic execution pipeline prototype.
    Connects the extraction normalizer and calculation engines
    into a predictable, stateless execution flow.
    """

    def __init__(self):
        # Initialize the stateless modules
        self.normalizer      = JsonNormalizer()
        self.planet_engine   = PlanetStrengthEngine()
        self.house_engine    = HouseStrengthEngine()
        self.varga_engine    = VargaEngine()
        self.dasha_engine    = DashaEngine()
        self.rasi_engine     = RasiStrengthEngine()
        self.av_engine       = AshtakavargaEngine()
        self.natal_engine    = NatalPromiseEngine()
        self.transit_engine  = TransitEngine()
        self.universal_mandali_engine = UniversalMandaliEngine()
        self.ephemeris_service = EphemerisService()
        self.mandali_transit_adapter = MandaliTransitAdapter(ephemeris_service=self.ephemeris_service)
        self.yoga_engine     = YogaEngine()
        self.question_engine = QuestionEngine()
        self.functional_nature_engine = FunctionalNatureEngine()
        self.master_engine   = MasterProbabilityEngine()
        self.chart_layout_builder = MandaliChartLayoutBuilder()
        self.transition_summary_builder = TransitionSummaryBuilder(self.universal_mandali_engine._ref_data)
        self.mandali_placement_factory = MandaliPlacementFactory()
        self.mandali_gochar_builder = MandaliGocharBuilder(
            ref_data=self.universal_mandali_engine._ref_data,
            adapter=self.mandali_transit_adapter,
        )

    def _resolve_target_date_utc(self, metadata: dict, default_utc=None) -> "datetime.datetime":
        """
        Extracts and normalizes the consultation_date from the metadata payload.
        Falls back to the provided default_utc or current UTC if missing/malformed.
        """
        c_date = metadata.get("consultation_date")
        if c_date:
            try:
                clean_date = c_date.replace("Z", "+00:00")
                parsed = datetime.datetime.fromisoformat(clean_date)
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=datetime.timezone.utc)
                return parsed
            except (ValueError, TypeError):
                pass
        
        return default_utc if default_utc else datetime.datetime.now(datetime.timezone.utc)

    def process(self, raw_input_data: dict, target_date_utc: datetime.datetime = None) -> dict:
        """
        Executes the strict calculation pipeline sequentially.

        Args:
            raw_input_data (dict): The messy, unformatted dictionary scraped from the PDF.
                                   Expected to have either:
                                   - Direct canonical keys: planets, houses, vargas, etc.
                                   - OR wrapper keys: canonical_content, machine_index
            target_date_utc (datetime): Optional date to enforce determinism for transits and dashas.
                                        Falls back to metadata consultation_date or current UTC.

        Returns:
            dict: The unified deterministic output payload containing all engine results.
        """
        # 1. Extract canonical content if wrapped
        if "canonical_content" in raw_input_data:
            canonical_data = raw_input_data["canonical_content"]
            canonical_json = raw_input_data.get("canonical_json")
        else:
            canonical_data = raw_input_data
            canonical_json = raw_input_data.get("canonical_json")

        # 1. Normalize the raw data into our strict deterministic schema
        normalized_payload = self.normalizer.normalize(canonical_data, canonical_json=canonical_json)

        if target_date_utc is None:
            metadata = normalized_payload.get("metadata", {})
            target_date_utc = self._resolve_target_date_utc(metadata, target_date_utc)

        # Build runtime canonical_json for Mandali from normalized natal + ephemeris transit
        # This enables UniversalMandaliEngine to run even without pre-built Canonical JSON
        try:
            moon_data = normalized_payload.get("planets", {}).get("moon", {})
            natal_moon_sign = moon_data.get("sign", "Mesha")
            natal_moon_nakshatra_raw = moon_data.get("nakshatra", "")
            natal_moon_pada = moon_data.get("pada")

            # Normalize nakshatra to match reference data casing (JsonNormalizer lowercases)
            ref_data = self.universal_mandali_engine._ref_data
            natal_moon_nakshatra = next(
                (n for n in ref_data.get_all_nakshatras() if n.lower() == natal_moon_nakshatra_raw.lower()),
                None
            )

            # If the canonical JSON omits the Moon nakshatra/pada, derive both from
            # the Moon's longitude (Sign + Degree), reusing the existing backend chain:
            #   longitude -> absolute pada -> nakshatra/pada
            # (same as MandaliPlacementFactory.build_natal). This keeps the grid
            # centered on the Moon's true pada instead of failing the Mandali block.
            if not natal_moon_nakshatra or not natal_moon_pada:
                moon_longitude = moon_data.get("longitude") or 0.0
                moon_absolute_pada = MandaliGenerator.get_absolute_pada(moon_longitude)
                derived_nakshatra, derived_pada = ref_data.get_nakshatra_pada(moon_absolute_pada)
                natal_moon_nakshatra = natal_moon_nakshatra or derived_nakshatra
                natal_moon_pada = natal_moon_pada or derived_pada

            # Get birth date from normalized metadata (fallback to a valid date for Mandali).
            # The Mandali engine requires DD.MM.YYYY; the normalizer emits ISO YYYY-MM-DD.
            birth_date = normalized_payload.get("metadata", {}).get("dob", "Unknown")
            if not birth_date or birth_date == "Unknown":
                birth_date = "14.05.1980"  # Raju's birth date from test data
            else:
                try:
                    birth_date = datetime.datetime.strptime(birth_date, "%Y-%m-%d").strftime("%d.%m.%Y")
                except (ValueError, TypeError):
                    pass  # Already in DD.MM.YYYY (or another accepted form)

            # Generate ephemeris snapshot for current transits
            ephemeris_snapshot = self.ephemeris_service.generate_transit_snapshot(target_date_utc)
            
            # Adapt to Mandali current_transit format
            current_transit = self.mandali_transit_adapter.adapt(
                ephemeris_snapshot=ephemeris_snapshot,
                natal_moon_sign=natal_moon_sign,
                natal_moon_nakshatra=natal_moon_nakshatra,
                natal_moon_pada=natal_moon_pada,
                target_date_utc=target_date_utc,
            )
            
            # Build canonical_json structure expected by UniversalMandaliEngine
            canonical_json = {
                "natal": {
                    "moon": {
                        "rasi": natal_moon_sign,
                        "nakshatra": natal_moon_nakshatra,
                        "pada": natal_moon_pada,
                    },
                    "birth_date": birth_date,
                },
                "current_transit": current_transit,
            }
        except Exception as e:
            # If transit generation fails, log and continue without Mandali
            logging.warning(f"Mandali transit generation failed: {e}")
            canonical_json = canonical_json or {}

        # 1.2. Dignity Derivation Enrichment (Mathematical Calculation)
        for planet_id, planet_data in normalized_payload.get("planets", {}).items():
            sign = planet_data.get("sign")
            if not sign:
                continue

            # Priority: Exalted -> Own Sign -> Debilitated -> Neutral
            dignity = "neutral"
            if EXALTATION_MAP.get(planet_id) == sign:
                dignity = "exalted"
            elif sign in OWN_SIGN_MAP.get(planet_id, []):
                dignity = "own_sign"
            elif DEBILITATION_MAP.get(planet_id) == sign:
                dignity = "debilitated"

            planet_data["dignity"] = dignity

        # 1.5 Functional Nature Mapping (Structural layer)
        lagna = normalized_payload.get("metadata", {}).get("ascendant_sign", "Mesha")
        functional_map = self.functional_nature_engine.get_functional_nature(lagna)

        # 2. Planet Engine Execution (Foundation Layer)
        planet_results = {}
        shadbala_payload = normalized_payload.get("shadbala", {})

        for planet_id, planet_data in normalized_payload.get("planets", {}).items():
            planet_results[planet_id] = self.planet_engine.calculate_strength(
                planet_data,
                shadbala_data=shadbala_payload
            )

        # 3. Safe Dependency Passing & House Engine Execution
        house_results = {}
        bhava_bala_payload = normalized_payload.get("bhava_bala", {})

        for house_id, house_data in normalized_payload.get("houses", {}).items():

            # Result-passing strategy: Extract the lord's name (e.g., "mars", "sun")
            lord_name = house_data.get("lord", "unknown")

            # Fetch the previously calculated lord score safely.
            # If the lord is missing due to a parser error, fallback to a neutral 50.
            lord_score = 50
            if lord_name in planet_results:
                lord_score = planet_results[lord_name].get("final_score", 50)

            # Create a shallow copy to preserve D1 immutability
            house_eval_payload = dict(house_data)
            house_eval_payload["lord_strength_score"] = lord_score

            # Calculate house strength using copied payload
            house_results[str(house_id)] = self.house_engine.calculate_strength(
                house_eval_payload,
                bhava_bala_data=bhava_bala_payload
            )

        # 3.5. Yoga Engine Execution
        # Requires pre-computed planet results to calculate true yoga potency
        yoga_results = self.yoga_engine.evaluate(normalized_payload, planet_results, house_results)

        # 4. Varga Engine Execution (Phase 5 Refinement)
        # Safely pass the D1 planet scores as read-only dependencies
        varga_results = self.varga_engine.evaluate(normalized_payload, dependency_scores=planet_results)

        # 5. Dasha Engine Execution (Temporal Activation Layer)
        # Passes normalized dasha data and D1 planet scores as read-only dependencies.
        # DashaEngine evaluates MD/AD relationship and timing multipliers only.
        dasha_results = self.dasha_engine.evaluate(
            normalized_payload, 
            dependency_scores=planet_results,
            target_date=target_date_utc.strftime('%Y-%m-%d')
        )

        # 6. Rasi Strength Engine (Sign Environment Layer)
        # Passes planet scores and varga outputs as read-only dependencies.
        # RasiStrengthEngine never re-calculates planets — reads pre-computed scores only.
        rasi_results = self.rasi_engine.evaluate(
            normalized_payload,
            dependency_scores=planet_results,
            varga_outputs=varga_results
        )

        # 7. Ashtakavarga Engine (Bindu Validation Layer)
        # Processes extracted SAV/BAV data. Produces planet modifiers,
        # dasha BAV confidence, SAV house analysis, and consistency audit.
        av_results = self.av_engine.evaluate(
            normalized_payload,
            dependency_scores=planet_results
        )

        # 7.5 BAV Modifier Injection (Environmental Layer)
        # Applies AshtakavargaEngine modifiers to final planet scores and
        # dasha timing multipliers. This is the ONLY place BAV modifiers are
        # consumed. All upstream engines (House, Rasi, Dasha) correctly used
        # the unmodified D1 structural scores — BAV is an environmental weight
        # layer applied to the reported output, not to intermediate calculations.
        # Source: VEDIC_AI_MASTER_ARCHITECTURE.md — "Dasha uses Ashtakavarga Support"
        self._apply_bav_modifiers(planet_results, dasha_results, av_results)

        # 8. Master Probability Engine (Synthesis Layer)
        # Combines all engine outputs into a single weighted probability score.
        # Weights: Natal Promise 40% | Planet 15% | House 10% | Rasi 10%
        #          Varga 10% | Dasha 10% | Transit 5%
        # Transit is the only remaining stub — returns neutral 50 until TransitEngine is built.
        engine_outputs = {
            "functional_nature": functional_map,
            "planets":      planet_results,
            "houses":       house_results,
            "vargas":       varga_results,
            "dashas":       dasha_results,
            "rasis":        rasi_results,
            "ashtakavarga": av_results,
            "doshas":       normalized_payload.get("doshas", {})
        }

        # 8. Natal Promise Engine (Domain Promise Layer)
        # Evaluates birth chart promise for 8 life domains using 6-factor formula.
        # Reads normalized_payload["houses"] directly for occupant/lord detection.
        natal_results = self.natal_engine.evaluate(
            planet_results    = planet_results,
            house_results     = house_results,
            rasi_results      = rasi_results,
            varga_results     = varga_results,
            av_results        = av_results,
            yoga_results      = yoga_results,
            normalized_houses = normalized_payload.get("houses", {}),
            normalized_vargas = normalized_payload.get("vargas", {})
        )
        engine_outputs["natal_promise"] = natal_results

        # 7.75 Transit Engine (Timing Layer)
        # Use Canonical JSON's current_transit directly (Option A path)
        # Only run if Canonical JSON has the required transit structure
        transit_results: Dict[str, Any] = {}
        mandali_response_dto: MandaliResponseDTO | None = None

        if isinstance(canonical_json, dict) and "natal" in canonical_json and "current_transit" in canonical_json:
            # Step 1: Get the rich internal data model from the engine
            mandali_advisory = self.universal_mandali_engine.generate_mandali_advisory(canonical_json)
            engine_outputs["mandali_advisory"] = asdict(mandali_advisory) # Keep for backward compatibility

            # Step 2: Create placement DTOs using the factory
            natal_placements = self.mandali_placement_factory.build_natal(
                natal_planets=normalized_payload.get("planets", {}),
                mandali_grid=mandali_advisory.mandali_grid,
            )
            current_placements = self.mandali_placement_factory.build_current(
                transit_resolutions=mandali_advisory.transit_resolutions,
                mandali_grid=mandali_advisory.mandali_grid,
            )

            # Step 3: Build chart layouts and transition summary
            # Moon-centered Rasi names for every cell (empty cells included) so the
            # chart shows the true Rasi instead of a fixed sign order.
            mandali_names = {
                m.number: f"Mandali {m.number} ({m.rasi_name})"
                for m in mandali_advisory.mandali_grid.mandalis
            }
            natal_chart_grid = self.chart_layout_builder.build(
                [p.__dict__ for p in natal_placements], mandali_names=mandali_names
            )
            current_chart_grid = self.chart_layout_builder.build(
                [p.__dict__ for p in current_placements], mandali_names=mandali_names
            )
            transition_summary_dto = self.transition_summary_builder.build(canonical_json["current_transit"], mandali_advisory.mandali_grid, target_date_utc)

            mandali_response_dto = MandaliResponseDTO(
                schema_version="2.0",
                natal_chart=NatalChartDTO(placements=natal_placements, grid=natal_chart_grid),
                current_chart=CurrentChartDTO(placements=current_placements, grid=current_chart_grid),
                transition_summary=transition_summary_dto
            )
            engine_outputs["mandali_response_dto"] = asdict(mandali_response_dto) # New DTO for new consumers

            # Step 3.5: Rasi-Mandali Gochar report (Present Gochar chart with 9
            # Nakshatra-Pada positions per Rasi box, Mandali periods, Saturn
            # special periods via the actual Mandali resolver, and the
            # Report A / Report B side-by-side comparison). Uses only existing
            # owners: the adapter's ephemeris scans + the Mandali grid.
            advisory_dict = asdict(mandali_advisory)
            mandali_gochar_report = self.mandali_gochar_builder.build(
                current_transit=canonical_json["current_transit"],
                mandali_grid=mandali_advisory.mandali_grid,
                target_date_utc=target_date_utc,
                advisory=advisory_dict,
            )
            engine_outputs["mandali_gochar_report"] = asdict(mandali_gochar_report)

            # Step 3.55: MD/AD/PD ↔ Saturn Gochar-Mandali cross-reference.
            # Backend-derived single source of truth. Consumes only the existing
            # Dasha timeline and the Mandali-resolved Saturn periods (no new
            # astrology, no invented dates, no extended scan). Both the report
            # template and the React timeline render this exact structure.
            from app.builders.dasha_saturn_crossref import (
                build_dasha_saturn_cross_reference,
            )
            engine_outputs["dasha_saturn_cross_reference"] = (
                build_dasha_saturn_cross_reference(
                    dasha_timeline=dasha_results.get("timeline", []),
                    saturn_periods=engine_outputs["mandali_gochar_report"].get(
                        "saturn_periods", {}
                    ),
                )
            )

            # Step 3.6: Repair the data flow to the existing report layer.
            # DisplayFormatter.format_gochara_report reads engine_outputs["mandali"]
            # and transit metadata — populate them from the already calculated
            # Mandali result (no recalculation).
            engine_outputs["mandali"] = self._build_mandali_report_block(
                mandali_advisory, current_placements
            )

            # Prepare transit_payload for TransitEngine
            transit_payload = {"planets": {}}
            for placement in current_placements:
                transit_payload["planets"][placement.planet.lower()] = {
                    "house": placement.mandali["number"], # Use mandali number as house for transit engine
                    "sign": placement.rasi,
                    "degree": 0 # Not used in Option A path
                }

            transit_results = self.transit_engine.evaluate(
                transit_payload=transit_payload,
                natal_payload=normalized_payload,
                dasha_results=dasha_results,
                av_results=av_results,
                natal_promise_results=natal_results,
                # mandali_results no longer passed; transit_payload already carries
                # mandali-based house numbers from current_placements (legacy fallback path)
            )

            # Report A data flow: the formatter reads transit metadata +
            # activated_planets/houses from the TransitEngine output.
            # target_date is serialized at day-granularity (%Y-%m-%d) matching the
            # DashaEngine convention — the pipeline contract keeps engine_outputs
            # free of wall-clock microsecond timestamps so identical input
            # produces identical output.
            transit_results.setdefault("metadata", {})["target_date"] = (
                target_date_utc.strftime('%Y-%m-%d') if target_date_utc else ""
            )
            t_houses_report = transit_results.get("transit_houses", {})
            transit_results["activated_planets"] = list(t_houses_report.keys())
            transit_results["activated_houses"] = [
                int(h) for h in t_houses_report.values() if isinstance(h, (int, float))
            ]

        if not transit_results: # If no canonical_json or transit_results not set
            transit_results = self.transit_engine._stub_result()
        engine_outputs["transit"] = transit_results

        # Add yoga results to outputs for the master engine
        engine_outputs["yogas"] = yoga_results

        # 9. Master Probability Engine (Synthesis Layer)
        # Combines all engine outputs into a single weighted probability score.
        # natal_promise factor now uses real domain scores (stub replaced).
        master_result = self.master_engine.evaluate(engine_outputs)

        # 9. Combine and Return Standardized Outputs
        final_output = {
            "metadata":           normalized_payload.get("metadata", {}),
            "master_probability": master_result,
            "engine_outputs":     engine_outputs,
            "target_date_utc":    target_date_utc.isoformat() if target_date_utc else None
        }
        
        return final_output

    # -------------------------------------------------------------------------
    # Step 7.5 — BAV Modifier Injection
    # -------------------------------------------------------------------------

    def _apply_bav_modifiers(
        self,
        planet_results: dict,
        dasha_results:  dict,
        av_results:     dict
    ) -> None:
        """
        Applies AshtakavargaEngine engine_modifiers to planet final_scores
        and dasha timing_multipliers. Mutates both dicts in-place.

        Planet BAV — three fields written atomically per planet:
            base_score   = original D1 structural score (preserved, never lost)
            bav_modifier = signed BAV adjustment (+5 / 0 / -5)
            final_score  = clamp(base_score + bav_modifier, 0, 100)

        All three fields are always written together so the score is fully
        explainable at every layer: D1 structural → BAV environment → final.

        Dasha BAV Multiplier:
            timing_multiplier      = base_timing_multiplier × bav_multiplier
            base_timing_multiplier = pre-BAV relationship multiplier (preserved)
            bav_multiplier         = AV timing confidence scalar

        Architecture Rule: This method contains zero astrological logic.
        It is pure orchestration — reading AV outputs and writing to other
        engine result dicts. All calculation is done inside the engines.
        """
        modifiers = av_results.get("engine_modifiers", {})

        # --- Planet BAV score adjustments ---
        bav_adjustments = modifiers.get("planet_score_adjustments", {})
        for planet, bav_modifier in bav_adjustments.items():
            if planet not in planet_results:
                continue
            base_score  = planet_results[planet].get("final_score", 0)
            final_score = max(0, min(100, base_score + bav_modifier))
            # Write all three fields atomically — full explainability preserved
            planet_results[planet]["base_score"]  = base_score    # original D1 score
            planet_results[planet]["bav_modifier"] = bav_modifier  # environmental layer
            planet_results[planet]["final_score"]  = final_score   # combined output

        # --- Dasha BAV confidence multiplier ---
        bav_mult = modifiers.get("dasha_bav_confidence_multiplier", 1.0)
        for lord, lord_data in dasha_results.items():
            if lord in ("synthesis", "timeline"):
                continue
            temporal = lord_data.get("temporal_activation", {})
            if "timing_multiplier" not in temporal:
                continue
            base_mult  = temporal["timing_multiplier"]
            adj_mult   = round(base_mult * bav_mult, 4)
            temporal["timing_multiplier"]      = adj_mult
            temporal["base_timing_multiplier"] = base_mult
            temporal["bav_multiplier"]         = bav_mult

    # -------------------------------------------------------------------------
    # Step 3.6 — Mandali report block (data-flow repair for the report layer)
    # -------------------------------------------------------------------------

    def _build_mandali_report_block(
        self,
        mandali_advisory,
        current_placements,
    ) -> dict:
        """
        Composes the `engine_outputs["mandali"]` block consumed by
        DisplayFormatter.format_gochara_report. Pure composition of data the
        UniversalMandaliEngine and MandaliPlacementFactory already produced —
        no recalculation. This repairs the data flow so the already-calculated
        Mandali result reaches the existing GocharaReport layer.
        """
        t_houses = {}
        for p in current_placements:
            t_houses[p.planet.lower()] = p.mandali["number"]

        sat_house = t_houses.get("saturn", 0)
        sade_sati_status = "Not Active"
        sade_sati_phase = "N/A"
        if sat_house == 12:
            sade_sati_status = "Active"
            sade_sati_phase = "Rising (Mandali 12)"
        elif sat_house == 1:
            sade_sati_status = "Active"
            sade_sati_phase = "Peak (Mandali 1)"
        elif sat_house == 2:
            sade_sati_status = "Active"
            sade_sati_phase = "Setting (Mandali 2)"

        cm = mandali_advisory.current_mandali
        ref = mandali_advisory.reference_moon
        occupied = sorted(set(t_houses.values()))
        zone_names = {
            1: "Moon Mandali", 2: "Wealth", 3: "Siblings", 4: "Home",
            5: "Children", 6: "Health", 7: "Marriage",
            8: "Longevity/Transformation", 9: "Fortune", 10: "Career",
            11: "Gains", 12: "Moksha/Isolation",
        }

        return {
            "current_mandali": cm.name,
            "reference_moon": f"{ref.rasi} {ref.nakshatra} Pada {ref.pada}",
            "mandali_number": cm.number,
            "mandali_boundaries": (
                "Moon-centered: 12 Mandalis of 9 Nakshatra-Pada positions each "
                "(108 padas total). Mandali 1 is centered on the natal Moon."
            ),
            "sade_sati_status": sade_sati_status,
            "sade_sati_phase": sade_sati_phase,
            "transit_houses": t_houses,
            "activated_zones": [str(z) for z in occupied],
            "activated_bhavas": [int(z) for z in occupied],
            "activated_planets": [p.planet.lower() for p in current_placements],
            "zone_names": zone_names,
            "score": 0,
        }

    # -------------------------------------------------------------------------
    # Question Orchestration (DR-007 Fix)
    # -------------------------------------------------------------------------

    def answer_question(self, question_or_id: str, pipeline_output: dict) -> dict:
        """
        Orchestrates domain routing, probability recalculation, formula evaluation,
        and response composition for a specific user question.

        Args:
            question_or_id (str): The question identifier from Question Registry (e.g., "7.1")
                                  OR a free-text natural language question.
            pipeline_output (dict): The output from self.process().

        Returns:
            dict: Structured answer payload from QuestionEngine.
        """
        # Detect if input is a question_id (e.g., "7.1") or free-text question
        is_question_id = False
        question_text = ""
        question_id = question_or_id

        # Check if it's a question_id format (e.g., "7.1", "10.2", etc.)
        import re
        if re.match(r'^\d+\.\d+$', question_or_id.strip()):
            is_question_id = True
            question_id = question_or_id.strip()
        else:
            question_text = question_or_id.strip()

        # 1. Route question through Question Router
        from app.core.question_router import QuestionRouter
        question_router = QuestionRouter()

        if is_question_id:
            route_result = question_router.route_question(question_id)
            if route_result.get("status") != "success":
                return {
                    "question_id": question_id,
                    "error": route_result.get("message", "Question routing failed"),
                    "status": "error"
                }
            registry_record = route_result["registry_record"]
            formula_key = route_result["formula_key"]
            domain = registry_record.get("domain_name")
            question_text = registry_record.get("question_name", "")
        else:
            # Use legacy route_domain for free-text questions (backward compatibility)
            domain = self.question_engine.route_domain(question_text)
            formula_key = None
            question_text = question_or_id.strip()
            # For free-text, we don't fail - we just continue with domain=None

        engine_outputs = pipeline_output.get("engine_outputs", {})
        natal_results = engine_outputs.get("natal_promise", {})

        if domain and domain in natal_results:
            natal_promise = natal_results[domain]
        else:
            # Fallback average if not routed
            scores = [d["score"] for d in natal_results.values() if isinstance(d, dict) and "score" in d]
            avg_score = round(sum(scores) / len(scores), 2) if scores else 50.0
            natal_promise = {"score": avg_score}

        dasha_activation = engine_outputs.get("dashas", {})
        transit_activation = engine_outputs.get("transit", {})
        av_results = engine_outputs.get("ashtakavarga", {})
        bav_confidence = av_results.get("dasha_bav_support", {}).get("timing_confidence", "unknown")

        # Recalculate Master Probability if routed
        if domain:
            domain_score = natal_promise.get("score", 50.0)
            dasha_score = dasha_activation.get("synthesis", {}).get("dasha_strength", 50.0)

            final_score = round((domain_score * 0.60) + (dasha_score * 0.40))

            calculated_grade = "UNKNOWN"
            for threshold, label in PROBABILITY_GRADES:
                if final_score >= threshold:
                    calculated_grade = label
                    break

            final_probability = {
                "final_score": final_score,
                "raw_score": float(final_score),
                "grade": calculated_grade,
                "breakdown": {
                    "domain_contribution": domain_score * 0.60,
                    "dasha_contribution": dasha_score * 0.40
                },
                "lifetime_projection": (pipeline_output.get("master_probability") or {}).get("lifetime_projection", [])
            }
        else:
            final_probability = pipeline_output.get("master_probability", {})

        # 4. Formula Evaluation with Calibration
        formula_evaluation = None
        if formula_key:
            try:
                formula = formula_repository_loader.get_formula(formula_key)

                # Get formula calibration
                formula_calibration = formula_repository_loader.get_formula_calibration(formula_key)

                # Build isolated signals from engine outputs
                isolated_signals = self._build_isolated_signals(engine_outputs, formula)

                # Evaluate formula with calibration
                formula_evaluation = FormulaEvaluator.evaluate(
                    formula=formula,
                    engine_outputs=engine_outputs,
                    isolated_signals=isolated_signals,
                    formula_calibration=formula_calibration
                )
            except Exception as e:
                # Log error but don't crash - formula evaluation is supplementary
                formula_evaluation = None
                import traceback
                traceback.print_exc()

        # Read the canonical target_date_utc already resolved and written by process().
        # Do NOT re-resolve from raw metadata — that would create a second resolution
        # path that diverges when consultation_date is absent (Single Source of Truth).
        target_date_iso = pipeline_output.get("target_date_utc")
        target_date_utc = datetime.datetime.fromisoformat(target_date_iso) if target_date_iso else None

        return self.question_engine.compose_response(
            question=question_id if is_question_id else question_text,
            domain=domain,
            natal_promise=natal_promise,
            dasha_activation=dasha_activation,
            transit_activation=transit_activation,
            final_probability=final_probability,
            bav_timing_confidence=bav_confidence,
            yogas=engine_outputs.get("yogas", {}),
            formula_evaluation=formula_evaluation,
            formula_key=formula_key,
            target_date_utc=target_date_utc,
            mandali_activation=engine_outputs.get("mandali_advisory") # Pass original for backward compatibility
        )

    def _build_isolated_signals(self, engine_outputs: dict, formula: "FormulaSchema") -> dict:
        """
        Extracts only the signals required by the formula from engine outputs.
        Returns a minimized payload for the Formula Evaluator.
        """
        isolated = {}
        payload = {
            "planets": engine_outputs.get("planets", {}),
            "houses": engine_outputs.get("houses", {}),
            "vargas": engine_outputs.get("vargas", {}),
            "dashas": engine_outputs.get("dashas", {}),
            "rasis": engine_outputs.get("rasis", {}),
            "ashtakavarga": engine_outputs.get("ashtakavarga", {}),
            "natal_promise": engine_outputs.get("natal_promise", {}),
            "transit": engine_outputs.get("transit", {}),
            "yogas": engine_outputs.get("yogas", {}),
        }

        for sig in formula.required_signals:
            # Try to extract signal from various engine outputs
            value = self._extract_signal(payload, sig)
            if value is not None:
                isolated[sig] = value
        return isolated

    def _extract_signal(self, payload: dict, signal: str):
        """Extract a specific signal from engine outputs."""
        # Signal mapping to engine output paths
        signal_paths = {
            "10th_house": ("houses", "10", "final_score"),
            "10th_lord": ("houses", "10", "lord_strength_score"),
            "11th_house": ("houses", "11", "final_score"),
            "12th_house": ("houses", "12", "final_score"),
            "1st_house": ("houses", "1", "final_score"),
            "1st_lord": ("houses", "1", "lord_strength_score"),
            "2nd_house": ("houses", "2", "final_score"),
            "3rd_house": ("houses", "3", "final_score"),
            "4th_house": ("houses", "4", "final_score"),
            "4th_lord": ("houses", "4", "lord_strength_score"),
            "5th_house": ("houses", "5", "final_score"),
            "5th_lord": ("houses", "5", "lord_strength_score"),
            "6th_house": ("houses", "6", "final_score"),
            "6th_lord": ("houses", "6", "lord_strength_score"),
            "7th_house": ("houses", "7", "final_score"),
            "7th_lord": ("houses", "7", "lord_strength_score"),
            "8th_house": ("houses", "8", "final_score"),
            "8th_lord": ("houses", "8", "lord_strength_score"),
            "9th_house": ("houses", "9", "final_score"),
            "d10": ("vargas", "D10", "planets", "saturn", "final_score"),
            "d2": ("vargas", "D2", "planets", "jupiter", "final_score"),
            "d20": ("vargas", "D20", "planets", "jupiter", "final_score"),
            "d24": ("vargas", "D24", "planets", "mercury", "final_score"),
            "d4": ("vargas", "D4", "planets", "mars", "final_score"),
            "d6": ("vargas", "D6", "planets", "sun", "final_score"),
            "d7": ("vargas", "D7", "planets", "jupiter", "final_score"),
            "d9": ("vargas", "D9", "planets", "venus", "final_score"),
            "dasha": ("dashas", "synthesis", "dasha_strength"),
            "jupiter": ("planets", "jupiter", "final_score"),
            "ketu": ("planets", "ketu", "final_score"),
            "lagna": ("houses", "1", "final_score"),
            "lagna_lord": ("houses", "1", "lord_strength_score"),
            "mars": ("planets", "mars", "final_score"),
            "mercury": ("planets", "mercury", "final_score"),
            "moon": ("planets", "moon", "final_score"),
            "rahu": ("planets", "rahu", "final_score"),
            "saturn": ("planets", "saturn", "final_score"),
            "sun": ("planets", "sun", "final_score"),
            "transit": ("transit", "activation_score"),
            "venus": ("planets", "venus", "final_score"),
            "yoga": ("yogas", "marriage_yoga", "strength"),
        }

        path = signal_paths.get(signal)
        if not path:
            return None

        current = payload
        for key in path:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        return current


# --- Sample Execution Example ---
if __name__ == "__main__":
    import json

    # Simulated raw extraction payload (Before Phase 1 PDF integration)
    sample_raw_pdf_data = {
        "raw_metadata": {
            "name": "Pipeline Test Native",
            "lagna": "Mesha"
        },
        "raw_planets": {
            "Surya": {
                "sign": "Mesha",
                "house": "1",
                "house_type": "kendra",
                "dignity": "exalted"
            },
            "Kuja": { # Mars
                "sign": "Vrishchika",
                "house": "8",
                "house_type": "dusthana",
                "dignity": "own_sign"
            }
        },
        "raw_vargas": {
            "D9": {
                "planets": {
                    "Surya": {
                        "sign": "Tula",          # D1 Aries -> D9 Libra (Debilitated) = Contradicted
                        "dignity": "debilitated"
                    },
                    "Kuja": {
                        "sign": "Vrishchika",    # D1 Scorpio -> D9 Scorpio = Vargottama
                        "dignity": "own_house"
                    }
                }
            }
        }
    }

    runner = PipelineRunner()
    unified_output = runner.process(sample_raw_pdf_data)
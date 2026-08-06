"""
UniversalMandaliEngine — Capability 7.7
========================================

Orchestrates capabilities 7.1 through 7.6 to produce the mandali_advisory output.

This is a COMPOSITION ENGINE only.
- It owns NO mathematical formulas
- It owns NO astrology rules
- It owns NO hidden calculations
- It ONLY orchestrates and composes the 6 existing capabilities

Governance Rules (UME-01 to UME-05):
- UME-01: Executes capabilities in sequence: 7.1 → 7.2 → 7.3 → 7.4 → 7.5 → 7.6
- UME-02: All steps deterministic, stateless, traceable to Canonical JSON + Rules
- UME-03: Produces ONLY mandali_advisory — no scores, no strengths, no probabilities
- UME-04: Never modifies other engine outputs (CGP-05, CGP-07)
- UME-05: Output schema versioned per CGP-10
"""

from __future__ import annotations

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

from app.engines.canonical_reference_data import (
    get_canonical_reference_data,
    CanonicalReferenceData,
    RegistryAccessError,
)
from app.engines.nakshatra_pada_resolver import NakshatraPadaResolver
from app.engines.mandali_grid_construction import (
    MandaliGridConstruction,
    MandaliGrid,
    Mandali,
)
from app.engines.transit_mandali_resolution import (
    TransitMandaliResolver,
    TransitMandaliResolution,
)
from app.engines.lifetime_cycle_projection import (
    LifetimeCycleProjector,
    LifetimeCycleProjection,
    SaturnCycle,
    CycleWindow,
)
from app.engines.birth_position_detection import (
    BirthPositionDetector,
    BirthPositionDetection,
    BirthPositionResult,
    BirthPosition,
    WindowType,
)

# -----------------------------------------------------------------------------
# Exceptions
# -----------------------------------------------------------------------------

class UniversalMandaliEngineError(Exception):
    """Base exception for UniversalMandaliEngine errors."""
    pass


class InvalidInputError(UniversalMandaliEngineError):
    """Invalid or missing input from Canonical JSON."""
    pass


class CompositionError(UniversalMandaliEngineError):
    """Error during capability composition."""
    pass


# -----------------------------------------------------------------------------
# Output Data Classes (mandali_advisory schema per Section 12)
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class CurrentMandali:
    """Current active Mandali information."""
    number: int
    name: str
    center_nakshatra: str
    center_pada: int


@dataclass(frozen=True)
class ReferenceMoon:
    """Reference Moon position from Canonical JSON."""
    rasi: str
    nakshatra: str
    pada: int
    mandali_1_center: str


@dataclass(frozen=True)
class TransitMandaliPosition:
    """Single transit planet's Mandali position."""
    planet: str
    mandali: Dict[str, Any]
    house_from_moon_classical: int
    house_from_moon_mandali: int
    status: str  # FAVORABLE | NEUTRAL | CHALLENGING
    interpretation_key: str


@dataclass(frozen=True)
class MandaliActivation:
    """Active Mandali with its planets."""
    mandali: int
    planets: List[str]
    activation_strength: str  # HIGH | MEDIUM | LOW


@dataclass(frozen=True)
class SadeSatiWindow:
    """Single Sade Sati phase window."""
    phase: str  # Rising | Peak | Setting
    rasi: str
    mandali: int
    start: str
    end: str
    birth_position: str


@dataclass(frozen=True)
class SadeSati:
    """Sade Sati projection with birth detection."""
    cycles: List[Dict[str, Any]]
    birth_detection: Dict[str, Any]


@dataclass(frozen=True)
class ElinatiShani:
    """Elinati Shani projection with birth detection."""
    cycles: List[Dict[str, Any]]
    birth_detection: Dict[str, Any]


@dataclass(frozen=True)
class AshtamaShani:
    """Ashtama Shani projection with birth detection."""
    cycles: List[Dict[str, Any]]
    birth_detection: Dict[str, Any]


@dataclass(frozen=True)
class TimelineEvent:
    """Timeline event entry."""
    period: str
    cycle: int
    events: List[str]


@dataclass(frozen=True)
class MandaliAdvisory:
    """
    Complete mandali_advisory output per GOCHARA_MANDALI_GOVERNANCE_v1.md Section 12.
    
    This is the ONLY output of the UniversalMandaliEngine.
    """
    schema_version: str
    reference_moon: ReferenceMoon
    current_mandali: CurrentMandali
    current_transit_mandali: Dict[str, TransitMandaliPosition]
    mandali_activations: List[MandaliActivation]
    sade_sati: SadeSati
    elinati_shani: ElinatiShani
    ashtama_shani: AshtamaShani
    timeline: List[TimelineEvent]
    important_advisory_statements: List[str]
    upcoming_mandali_events: List[Dict[str, Any]]


# -----------------------------------------------------------------------------
# Universal Mandali Engine — Composition Engine (Capability 7.7)
# -----------------------------------------------------------------------------

class UniversalMandaliEngine:
    """
    UniversalMandaliEngine — Capability 7.7
    
    Composes capabilities 7.1 through 7.6 to produce the mandali_advisory output.
    
    This engine:
    - Owns NO mathematical formulas
    - Owns NO astrology rules
    - Owns NO hidden calculations
    - ONLY orchestrates and composes the 6 existing capabilities
    """
    
    def __init__(
        self,
        ref_data: Optional[CanonicalReferenceData] = None,
        pada_resolver: Optional[NakshatraPadaResolver] = None,
        grid_constructor: Optional[MandaliGridConstruction] = None,
        transit_resolver: Optional[TransitMandaliResolver] = None,
        cycle_projector: Optional[LifetimeCycleProjector] = None,
        birth_detector: Optional[BirthPositionDetector] = None,
    ):
        """
        Initialize the Universal Mandali Engine with all 6 capabilities.
        
        Args:
            ref_data: CanonicalReferenceData instance (uses singleton if None)
            pada_resolver: NakshatraPadaResolver instance (creates new if None)
            grid_constructor: MandaliGridConstruction instance (creates new if None)
            transit_resolver: TransitMandaliResolver instance (creates new if None)
            cycle_projector: LifetimeCycleProjector instance (creates new if None)
            birth_detector: BirthPositionDetector instance (creates new if None)
        """
        # Initialize dependencies (singleton or injected)
        self._ref_data = ref_data or get_canonical_reference_data()
        self._pada_resolver = pada_resolver or NakshatraPadaResolver(self._ref_data)
        self._grid_constructor = grid_constructor or MandaliGridConstruction(
            ref_data=self._ref_data, 
            pada_resolver=self._pada_resolver
        )
        self._transit_resolver = transit_resolver or TransitMandaliResolver(
            ref_data=self._ref_data,
            pada_resolver=self._pada_resolver,
            grid_constructor=self._grid_constructor,
        )
        self._cycle_projector = cycle_projector or LifetimeCycleProjector(
            ref_data=self._ref_data
        )
        self._birth_detector = birth_detector or BirthPositionDetector(
            ref_data=self._ref_data
        )
    
    def generate_mandali_advisory(
        self,
        canonical_json: Dict[str, Any],
    ) -> MandaliAdvisory:
        """
        Generate the complete mandali_advisory from Canonical JSON.
        
        This is the single public entry point. It orchestrates all 6 capabilities
        in sequence: 7.1 → 7.2 → 7.3 → 7.4 → 7.5 → 7.6
        
        Args:
            canonical_json: Canonical JSON input with structure:
                {
                    "natal": {
                        "moon": {"rasi": str, "nakshatra": str, "pada": int},
                        "birth_date": "DD.MM.YYYY"
                    },
                    "current_transit": [
                        {
                            "planet": str,
                            "rasi": str,
                            "nakshatra": str,
                            "pada": int,
                            "start_date": "DD.MM.YYYY",
                            "end_date": "DD.MM.YYYY",
                            "house_from_moon": int,
                            "interpretation": str
                        }
                    ]
                }
        
        Returns:
            MandaliAdvisory: Complete advisory object per Section 12 schema
            
        Raises:
            InvalidInputError: If Canonical JSON structure is invalid
            CompositionError: If any capability fails
        """
        # ================================================================
        # VALIDATE INPUT — Canonical JSON Contract
        # ================================================================
        self._validate_canonical_json(canonical_json)
        
        natal = canonical_json["natal"]
        current_transit = canonical_json["current_transit"]
        
        # Extract natal moon data
        moon_rasi = natal["moon"]["rasi"]
        moon_nakshatra = natal["moon"]["nakshatra"]
        moon_pada = natal["moon"]["pada"]
        birth_date = natal["birth_date"]
        
        # ================================================================
        # CAPABILITY 7.1: CanonicalReferenceData (already loaded via singleton)
        # ================================================================
        # Registry loaded and validated at initialization
        
        # ================================================================
        # CAPABILITY 7.2: NakshatraPadaResolver
        # ================================================================
        # Moon Absolute Pada = resolve(natal_moon_nakshatra, natal_moon_pada)
        moon_absolute_pada = self._pada_resolver.resolve(moon_nakshatra, moon_pada)
        
        # ================================================================
        # CAPABILITY 7.3: MandaliGridConstruction
        # ================================================================
        mandali_grid = self._grid_constructor.build_grid(
            natal_moon_nakshatra=moon_nakshatra,
            natal_moon_pada=moon_pada,
        )
        
        # ================================================================
        # CAPABILITY 7.4: TransitMandaliResolution
        # ================================================================
        transit_resolutions = self._transit_resolver.resolve_all_transit_planets(
            transit_planets=current_transit,
            mandali_grid=mandali_grid,
        )
        
        # ================================================================
        # CAPABILITY 7.5: LifetimeCycleProjection
        # ================================================================
        # Find Saturn transit
        saturn_transit = self._find_saturn_transit(current_transit)
        if not saturn_transit:
            raise InvalidInputError("Saturn transit missing from current_transit")
        
        lifetime_projection = self._cycle_projector.project_cycles(
            natal_moon_rasi=moon_rasi,
            birth_date=birth_date,
            saturn_transit=saturn_transit,
        )
        
        # ================================================================
        # CAPABILITY 7.6: BirthPositionDetection
        # ================================================================
        birth_position = self._birth_detector.detect_birth_position(
            birth_date=birth_date,
            natal_moon_rasi=moon_rasi,
            lifetime_projection=lifetime_projection,
        )
        
        # ================================================================
        # COMPOSE OUTPUT — mandali_advisory schema (Section 12)
        # ================================================================
        advisory = self._compose_advisory(
            moon_rasi=moon_rasi,
            moon_nakshatra=moon_nakshatra,
            moon_pada=moon_pada,
            moon_absolute_pada=moon_absolute_pada,
            mandali_grid=mandali_grid,
            transit_resolutions=transit_resolutions,
            lifetime_projection=lifetime_projection,
            birth_position=birth_position,
            current_transit=current_transit,
        )
        
        return advisory
    
    def _validate_canonical_json(self, canonical_json: Dict[str, Any]) -> None:
        """Validate Canonical JSON input structure."""
        if not isinstance(canonical_json, dict):
            raise InvalidInputError("Canonical JSON must be a dictionary")
        
        if "natal" not in canonical_json:
            raise InvalidInputError("Missing 'natal' section in Canonical JSON")
        
        if "current_transit" not in canonical_json:
            raise InvalidInputError("Missing 'current_transit' section in Canonical JSON")
        
        natal = canonical_json["natal"]
        required_natal = ["moon", "birth_date"]
        for key in required_natal:
            if key not in natal:
                raise InvalidInputError(f"Missing '{key}' in natal section")
        
        moon = natal["moon"]
        required_moon = ["rasi", "nakshatra", "pada"]
        for key in required_moon:
            if key not in moon:
                raise InvalidInputError(f"Missing '{key}' in natal.moon")
        
        # Validate pada range
        moon_pada = moon["pada"]
        if not isinstance(moon_pada, int) or not 1 <= moon_pada <= 4:
            raise InvalidInputError(f"Invalid moon pada: {moon_pada} (must be 1-4)")
        
        # Validate current_transit
        current_transit = canonical_json["current_transit"]
        if not isinstance(current_transit, list):
            raise InvalidInputError("current_transit must be a list")
        
        for i, tp in enumerate(current_transit):
            required = ["planet", "rasi", "nakshatra", "pada", "start_date", "end_date", "house_from_moon", "interpretation"]
            for key in required:
                if key not in tp:
                    raise InvalidInputError(f"Transit planet {i} missing '{key}'")
    
    def _find_saturn_transit(self, current_transit: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Find Saturn transit in current_transit list."""
        for tp in current_transit:
            if tp.get("planet", "").lower() == "saturn":
                return tp
        return None
    
    def _compose_advisory(
        self,
        moon_rasi: str,
        moon_nakshatra: str,
        moon_pada: int,
        moon_absolute_pada: int,
        mandali_grid: MandaliGrid,
        transit_resolutions: List[TransitMandaliResolution],
        lifetime_projection: LifetimeCycleProjection,
        birth_position: BirthPositionDetection,
        current_transit: List[Dict[str, Any]],
    ) -> MandaliAdvisory:
        """Compose the final mandali_advisory from all capability outputs."""
        
        # ---- Current Mandali ----
        # Current active Mandali = Mandali containing current Saturn transit
        saturn_transit = self._find_saturn_transit(current_transit)
        saturn_absolute_pada = None
        if saturn_transit:
            saturn_absolute_pada = self._pada_resolver.resolve(
                saturn_transit["nakshatra"], 
                saturn_transit["pada"]
            )
        
        current_mandali_num = mandali_grid.find_mandali_for_pada(saturn_absolute_pada) if saturn_absolute_pada else 1
        current_mandali = mandali_grid.get_mandali(current_mandali_num)
        
        current_mandali_info = CurrentMandali(
            number=current_mandali.number,
            name=f"Mandali {current_mandali.number}",
            center_nakshatra=current_mandali.center_nakshatra,
            center_pada=current_mandali.center_pada_num,
        )
        
        # ---- Reference Moon ----
        ref_moon = ReferenceMoon(
            rasi=mandali_grid.moon_rasi,
            nakshatra=mandali_grid.moon_nakshatra,
            pada=mandali_grid.moon_pada,
            mandali_1_center=mandali_grid.mandalis[0].center_nakshatra,
        )
        
        # ---- Current Transit Mandali Positions ----
        transit_positions = {}
        for res in transit_resolutions:
            status = self._determine_status(res, mandali_grid)
            transit_positions[res.planet] = TransitMandaliPosition(
                planet=res.planet,
                mandali={
                    "number": res.mandali["number"],
                    "name": res.mandali["name"],
                    "center_nakshatra": res.mandali["center_nakshatra"],
                    "center_pada": res.mandali["center_pada"],
                },
                house_from_moon_classical=res.house_from_moon_classical,
                house_from_moon_mandali=res.house_from_moon_mandali,
                status=status,
                interpretation_key=res.interpretation_ref,
            )
        
        # ---- Mandali Activations ----
        mandali_activations = self._compute_mandali_activations(transit_resolutions)
        
        # ---- Sade Sati ----
        sade_sati = self._compose_sade_sati(lifetime_projection, birth_position)
        
        # ---- Elinati Shani ----
        elinati_shani = self._compose_elinati_shani(lifetime_projection, birth_position)
        
        # ---- Ashtama Shani ----
        ashtama_shani = self._compose_ashtama_shani(lifetime_projection, birth_position)
        
        # ---- Timeline ----
        timeline = self._compose_timeline(lifetime_projection)
        
        # ---- Advisory Statements ----
        advisory_statements = self._generate_advisory_statements(
            transit_resolutions, lifetime_projection, birth_position
        )
        
        # ---- Upcoming Events ----
        upcoming_events = self._generate_upcoming_events(lifetime_projection)
        
        return MandaliAdvisory(
            schema_version="1.0",
            reference_moon=ref_moon,
            current_mandali=current_mandali_info,
            current_transit_mandali=transit_positions,
            mandali_activations=mandali_activations,
            sade_sati=sade_sati,
            elinati_shani=elinati_shani,
            ashtama_shani=ashtama_shani,
            timeline=timeline,
            important_advisory_statements=advisory_statements,
            upcoming_mandali_events=upcoming_events,
        )
    
    def _determine_status(self, resolution: TransitMandaliResolution, mandali_grid: MandaliGrid) -> str:
        """Determine transit planet status based on Mandali position."""
        # Simple rule: Mandali 1-4 = FAVORABLE, 5-8 = NEUTRAL, 9-12 = CHALLENGING
        mandali_num = resolution.mandali["number"]
        if mandali_num <= 4:
            return "FAVORABLE"
        elif mandali_num <= 8:
            return "NEUTRAL"
        else:
            return "CHALLENGING"
    
    def _compute_mandali_activations(self, transit_resolutions: List[TransitMandaliResolution]) -> List[MandaliActivation]:
        """Group transit planets by their Mandali and compute activation strength."""
        mandali_planets = {}
        for res in transit_resolutions:
            m_num = res.mandali["number"]
            if m_num not in mandali_planets:
                mandali_planets[m_num] = []
            mandali_planets[m_num].append(res.planet)
        
        activations = []
        for m_num, planets in sorted(mandali_planets.items()):
            count = len(planets)
            if count >= 3:
                strength = "HIGH"
            elif count == 2:
                strength = "MEDIUM"
            else:
                strength = "LOW"
            
            activations.append(MandaliActivation(
                mandali=m_num,
                planets=planets,
                activation_strength=strength,
            ))
        
        return activations
    
    def _compose_sade_sati(
        self, 
        projection: LifetimeCycleProjection, 
        birth_position: BirthPositionDetection
    ) -> SadeSati:
        """Compose Sade Sati section from lifetime projection and birth position."""
        cycles = []
        for cycle in projection.cycles:
            # Sade Sati windows for this cycle
            sade_sati_windows = []
            for w in cycle.sade_sati_windows:
                # Find birth position for this window
                bp = None
                for r in birth_position.sade_sati:
                    if r.cycle_number == cycle.cycle_number and r.phase == w.phase:
                        bp = r
                        break
                
                position_enum = bp.position if bp else BirthPosition.BIRTH_AFTER_LAST_CYCLE
                position_str = position_enum.value
                
                sade_sati_windows.append({
                    "phase": w.phase,
                    "rasi": w.rasi,
                    "mandali": w.mandali,
                    "start": w.start_date,
                    "end": w.end_date,
                    "birth_position": position_str,
                })
            
            cycles.append({
                "cycle_number": cycle.cycle_number,
                "period": cycle.period,
                "sade_sati_windows": sade_sati_windows,
            })
        
        # Overall birth detection
        sade_sati_positions = birth_position.sade_sati
        if not sade_sati_positions:
            overall_bd = {"position": "NO_WINDOWS", "description": "No Sade Sati windows found"}
        else:
            # Find most relevant position (prefer INSIDE, then BEFORE, then AFTER)
            inside = [r for r in sade_sati_positions if r.position == BirthPosition.BIRTH_INSIDE]
            before = [r for r in sade_sati_positions if r.position in (BirthPosition.BIRTH_BEFORE_FIRST_CYCLE, BirthPosition.BIRTH_BEFORE_THIS_CYCLE)]
            after = [r for r in sade_sati_positions if r.position == BirthPosition.BIRTH_AFTER_LAST_CYCLE]
            
            if inside:
                r = inside[0]
                overall_bd = {"position": r.position.value, "cycle": r.cycle_number, "phase": r.phase, "description": r.description}
            elif before:
                r = before[0]
                overall_bd = {"position": r.position.value, "cycle": r.cycle_number, "phase": r.phase, "description": r.description}
            else:
                r = after[0]
                overall_bd = {"position": r.position.value, "cycle": r.cycle_number, "phase": r.phase, "description": r.description}
        
        return SadeSati(cycles=cycles, birth_detection=overall_bd)
    
    def _compose_elinati_shani(self, projection: LifetimeCycleProjection, birth_position: BirthPositionDetection) -> ElinatiShani:
        """Compose Elinati Shani section."""
        cycles = []
        for cycle in projection.cycles:
            windows = []
            for w in cycle.elinati_shani_windows:
                bp = None
                for r in birth_position.elinati_shani:
                    if r.cycle_number == cycle.cycle_number and r.phase == w.phase:
                        bp = r
                        break
                
                position_str = bp.position.value if bp else BirthPosition.BIRTH_AFTER_LAST_CYCLE.value
                
                windows.append({
                    "phase": w.phase,
                    "rasi": w.rasi,
                    "mandali": w.mandali,
                    "start": w.start_date,
                    "end": w.end_date,
                    "birth_position": position_str,
                })
            
            cycles.append({
                "cycle_number": cycle.cycle_number,
                "period": cycle.period,
                "elinati_shani_windows": windows,
            })
        
        # Overall birth detection
        positions = birth_position.elinati_shani
        if not positions:
            overall_bd = {"position": "NO_WINDOWS", "description": "No Elinati Shani windows found"}
        else:
            inside = [r for r in positions if r.position == BirthPosition.BIRTH_INSIDE]
            if inside:
                r = inside[0]
                overall_bd = {"position": r.position.value, "cycle": r.cycle_number, "phase": r.phase, "description": r.description}
            else:
                r = positions[0]
                overall_bd = {"position": r.position.value, "cycle": r.cycle_number, "phase": r.phase, "description": r.description}
        
        return ElinatiShani(cycles=cycles, birth_detection=overall_bd)
    
    def _compose_ashtama_shani(self, projection: LifetimeCycleProjection, birth_position: BirthPositionDetection) -> AshtamaShani:
        """Compose Ashtama Shani section."""
        cycles = []
        for cycle in projection.cycles:
            windows = []
            for w in cycle.ashtama_shani_windows:
                bp = None
                for r in birth_position.ashtama_shani:
                    if r.cycle_number == cycle.cycle_number and r.phase == w.phase:
                        bp = r
                        break
                
                position_str = bp.position.value if bp else BirthPosition.BIRTH_AFTER_LAST_CYCLE.value
                
                windows.append({
                    "phase": w.phase,
                    "rasi": w.rasi,
                    "mandali": w.mandali,
                    "start": w.start_date,
                    "end": w.end_date,
                    "birth_position": position_str,
                })
            
            cycles.append({
                "cycle_number": cycle.cycle_number,
                "period": cycle.period,
                "ashtama_shani_windows": windows,
            })
        
        positions = birth_position.ashtama_shani
        if not positions:
            overall_bd = {"position": "NO_WINDOWS", "description": "No Ashtama Shani windows found"}
        else:
            inside = [r for r in positions if r.position == BirthPosition.BIRTH_INSIDE]
            if inside:
                r = inside[0]
                overall_bd = {"position": r.position.value, "cycle": r.cycle_number, "phase": r.phase, "description": r.description}
            else:
                r = positions[0]
                overall_bd = {"position": r.position.value, "cycle": r.cycle_number, "phase": r.phase, "description": r.description}
        
        return AshtamaShani(cycles=cycles, birth_detection=overall_bd)
    
    def _compose_timeline(self, projection: LifetimeCycleProjection) -> List[TimelineEvent]:
        """Compose timeline from lifetime projection."""
        timeline = []
        for cycle in projection.cycles:
            events = []
            for w in cycle.sade_sati_windows:
                events.append(f"Sade Sati {w.phase} in {w.rasi} (Mandali {w.mandali})")
            for w in cycle.elinati_shani_windows:
                events.append(f"Elinati Shani in {w.rasi} (Mandali {w.mandali})")
            for w in cycle.ashtama_shani_windows:
                events.append(f"Ashtama Shani in {w.rasi} (Mandali {w.mandali})")
            
            if events:
                timeline.append(TimelineEvent(
                    period=cycle.period,
                    cycle=cycle.cycle_number,
                    events=events,
                ))
        
        return timeline
    
    def _generate_advisory_statements(
        self,
        transit_resolutions: List[TransitMandaliResolution],
        projection: LifetimeCycleProjection,
        birth_position: BirthPositionDetection,
    ) -> List[str]:
        """Generate human-readable advisory statements."""
        statements = []
        
        # Current transit statements
        for res in transit_resolutions:
            mandali_num = res.mandali["number"]
            if mandali_num <= 4:
                statements.append(f"{res.planet} in Mandali {mandali_num} ({res.mandali['center_nakshatra']}) — Favorable period for matters related to {res.planet}.")
            elif mandali_num >= 9:
                statements.append(f"{res.planet} in Mandali {mandali_num} ({res.mandali['center_nakshatra']}) — Challenging period; exercise caution in {res.planet}-related matters.")
            else:
                statements.append(f"{res.planet} in Mandali {mandali_num} ({res.mandali['center_nakshatra']}) — Neutral period for {res.planet} matters.")
        
        # Sade Sati statements
        bp = birth_position.sade_sati
        inside_ss = [r for r in bp if r.position == BirthPosition.BIRTH_INSIDE]
        if inside_ss:
            for r in inside_ss:
                statements.append(f"Currently in Sade Sati {r.phase} phase (Cycle {r.cycle_number}). {r.description}")
        else:
            before_ss = [r for r in bp if r.position in (BirthPosition.BIRTH_BEFORE_FIRST_CYCLE, BirthPosition.BIRTH_BEFORE_THIS_CYCLE)]
            if before_ss:
                r = before_ss[0]
                statements.append(f"Sade Sati {r.phase} approaches in Cycle {r.cycle_number}. {r.description}")
            else:
                after_ss = [r for r in bp if r.position == BirthPosition.BIRTH_AFTER_LAST_CYCLE]
                if after_ss:
                    r = after_ss[0]
                    statements.append(f"Sade Sati {r.phase} completed in Cycle {r.cycle_number}. {r.description}")
        
        # Elinati/Ashtama statements
        for r in birth_position.elinati_shani:
            if r.position == BirthPosition.BIRTH_INSIDE:
                statements.append(f"Currently in Elinati Shani ({r.phase}, Cycle {r.cycle_number}). {r.description}")
                break
        
        for r in birth_position.ashtama_shani:
            if r.position == BirthPosition.BIRTH_INSIDE:
                statements.append(f"Currently in Ashtama Shani ({r.phase}, Cycle {r.cycle_number}). {r.description}")
                break
        
        return statements
    
    def _generate_upcoming_events(self, projection: LifetimeCycleProjection) -> List[Dict[str, Any]]:
        """Generate upcoming mandali events from projection."""
        events = []
        today = datetime.now()
        
        for cycle in projection.cycles:
            for w in cycle.sade_sati_windows:
                start = datetime.strptime(w.start_date, "%d.%m.%Y")
                if start >= today:
                    events.append({
                        "event": f"Sade Sati {w.phase} begins",
                        "date": w.start_date,
                        "mandali": w.mandali,
                    })
            
            for w in cycle.elinati_shani_windows:
                start = datetime.strptime(w.start_date, "%d.%m.%Y")
                if start >= today:
                    events.append({
                        "event": f"Elinati Shani begins",
                        "date": w.start_date,
                        "mandali": w.mandali,
                    })
            
            for w in cycle.ashtama_shani_windows:
                start = datetime.strptime(w.start_date, "%d.%m.%Y")
                if start >= today:
                    events.append({
                        "event": f"Ashtama Shani begins",
                        "date": w.start_date,
                        "mandali": w.mandali,
                    })
        
        # Sort by date and limit
        events.sort(key=lambda e: e["date"])
        return events[:10]


# -----------------------------------------------------------------------------
# Convenience Function
# -----------------------------------------------------------------------------

def generate_mandali_advisory(canonical_json: Dict[str, Any]) -> MandaliAdvisory:
    """
    Convenience function to generate mandali_advisory from Canonical JSON.
    
    Args:
        canonical_json: Canonical JSON input
        
    Returns:
        MandaliAdvisory object
    """
    engine = UniversalMandaliEngine()
    return engine.generate_mandali_advisory(canonical_json)

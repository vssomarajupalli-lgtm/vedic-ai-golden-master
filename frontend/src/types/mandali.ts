// Frontend types mirroring the backend MandaliResponseDTO / MandaliAdvisory DTOs.
// Presentation-only: the backend is the Single Source of Truth. 
// Shapes match app/schemas/mandali_response.py, natal_chart.py, current_chart.py,
// mandali_chart_cell.py, transition_summary.py, and universal_mandali_engine.py dataclasses.

export interface MandaliChartCell {
  mandali_number: number;
  mandali_name: string;
  planets: string[];
}

export interface NatalPlanetPlacement {
  planet: string;
  rasi: string;
  nakshatra: string;
  pada: number;
  mandali: { number: number; name: string };
}

export interface NatalChartDTO {
  chart_name: string;
  placements: NatalPlanetPlacement[];
  grid: MandaliChartCell[];
}

export interface CurrentTransitPlanetPlacement {
  planet: string;
  rasi: string;
  nakshatra: string;
  pada: number;
  mandali: { number: number; name: string };
  status: string; // FAVORABLE | NEUTRAL | CHALLENGING
}

export interface CurrentChartDTO {
  chart_name: string;
  placements: CurrentTransitPlanetPlacement[];
  grid: MandaliChartCell[];
}

export interface PlanetTransitionSummaryItem {
  planet: string;
  current_rasi: string;
  current_nakshatra: string;
  current_pada: number;
  current_mandali: string;
  next_mandali: string;
  estimated_entry_date: string;
  days_remaining: number;
}

export interface TransitionSummaryDTO {
  summary_items: PlanetTransitionSummaryItem[];
}

export interface MandaliAnalysisDTO {
  schema_version: string;
  natal_chart: NatalChartDTO;
  current_chart: CurrentChartDTO;
  transition_summary: TransitionSummaryDTO;
}

// --- MandaliAdvisory (the advisory output of UniversalMandaliEngine) ---

export interface ReferenceMoon {
  rasi: string;
  nakshatra: string;
  pada: number;
  mandali_1_center: string;
}

export interface CurrentMandali {
  number: number;
  name: string;
  center_nakshatra: string;
  center_pada: number;
}

export interface MandaliCycleEntry {
  cycle_number: number;
  period: string;
  events?: string[];
}

export interface MandaliAdvisoryDTO {
  schema_version: string;
  reference_moon?: ReferenceMoon;
  current_mandali?: CurrentMandali;
  current_transit_mandali?: Record<string, unknown>;
  transit_resolutions?: unknown[];
  mandali_activations?: { mandali: number; planets: string[]; activation_strength: string }[];
  sade_sati?: { cycles: MandaliCycleEntry[]; birth_detection?: Record<string, unknown> };
  elinati_shani?: { cycles: MandaliCycleEntry[]; birth_detection?: Record<string, unknown> };
  ashtama_shani?: { cycles: MandaliCycleEntry[]; birth_detection?: Record<string, unknown> };
  timeline?: { period: string; cycle: number; events: string[] }[];
  important_advisory_statements?: string[];
  upcoming_mandali_events?: { event: string; date: string; mandali: number }[];
  moon_absolute_pada?: number;
  mandali_grid?: unknown;
}

// ---------------------------------------------------------------------------
// MandaliGocharReport — Present Gochar Rāśi-Mandali report (Report B)
// Frontend types mirroring backend/app/schemas/mandali_gochar.py exactly.
// The frontend is a renderer only; the backend is authoritative.
// ---------------------------------------------------------------------------

/** A single Nakshatra-Pada position inside a Mandali Gochar cell (1 of 9). */
export interface MandaliPadaSlot {
  position: number;          // 1-9 (slot within the Mandali arc)
  absolute_pada: number;     // 1-108
  nakshatra: string;         // e.g. "Dhanishta"
  pada: number;              // 1-4 (quarter of the nakshatra)
  planets: string[];         // short planet codes at this exact pada (e.g. "SU", "RA")
}

/** One Rāśi box of the Present Gochar Mandali chart (9 pada positions). */
export interface MandaliGocharCell {
  mandali_number: number;    // 1-12 (Moon-relative Mandali number)
  mandali_name: string;      // "Mandali 1 (Makara)"
  rasi: string;              // Rāśi of this Mandali cell
  center_pada: number;       // 1-108
  padas: MandaliPadaSlot[];  // exactly 9 slots
}

/** Reference to the next Mandali a planet will enter. */
export interface NextMandaliRef {
  number: number;
  name: string;
}

/** Report B row — Mandali-based transit period for a single planet. */
export interface MandaliPeriodEntry {
  planet: string;            // "Sun", "Moon", ...
  current_rasi: string;      // planet's actual zodiac Rāśi
  rasi_number: number;       // 1-12 zodiacal (Mesha=1 .. Meena=12)
  nakshatra: string;
  pada: number;
  mandali_number: number;    // Moon-relative Mandali
  mandali_name: string;
  entry_date: string;        // DD.MM.YYYY
  entry_datetime: string;    // ISO-8601 UTC instant
  exit_date: string;         // DD.MM.YYYY
  exit_datetime: string;     // ISO-8601 UTC instant
  next_mandali: NextMandaliRef;
  status: string;            // IN_PROGRESS | UPCOMING | COMPLETED | UNRESOLVED
  duration_days: number;
  days_remaining: number;
  mandali_status: string;    // FAVORABLE | NEUTRAL | CHALLENGING
}

/** Report A row — regular Rāśi-based gochar period for a single planet. */
export interface RasiGocharEntry {
  planet: string;
  current_rasi: string;
  rasi_number: number;       // 1-12 zodiacal
  rasi_entry: string;        // DD.MM.YYYY or "—"
  rasi_exit: string;         // DD.MM.YYYY or "—"
  next_rasi: string;
  status: string;            // IN_PROGRESS | UPCOMING | COMPLETED | UNRESOLVED
  duration_days: number;
  days_remaining: number;
}

/** A single Saturn special-period window resolved from the Mandali resolver. */
export interface SaturnMandaliPeriod {
  cycle: string;             // "Sade Sati", "Ardha Ashtama", "Ashtama", "Elinati"
  phase: string;             // "Rising"|"Peak"|"Setting"|...
  rasi: string;              // Mandali cell Rāśi
  mandali_number: number;
  mandali_name: string;
  nakshatra: string;
  pada: number;
  entry: string;             // DD.MM.YYYY or "—"
  exit: string;              // DD.MM.YYYY or "—"
  next_mandali: number | null;
  status: string;            // ACTIVE | UPCOMING | NOT_FOUND | INACTIVE
  mechanism: string;         // "MANDALI_RESOLVER"
}

export interface SaturnPeriodGroup {
  current: SaturnMandaliPeriod[];
  upcoming: SaturnMandaliPeriod[];
}

export interface SaturnPeriods {
  sade_sati: SaturnPeriodGroup;
  ardha_ashtama: SaturnPeriodGroup;
  ashtama: SaturnPeriodGroup;
  elinati: SaturnPeriodGroup;
  current_saturn: CurrentSaturnPosition;
  legacy_windows: LegacyRasiSaturnWindows;
}

/** Saturn's current Mandali position (saturn_periods.current_saturn). */
export interface CurrentSaturnPosition {
  planet?: string;
  mandali_number?: number;
  mandali_name?: string;
  rasi?: string;
  nakshatra?: string;
  pada?: number;
  entry_date?: string;
  exit_date?: string;
  next_mandali?: number | null;
  active_flags?: string[];
}

/** One legacy Rāśi-based lifetime Saturn cycle (UniversalMandaliEngine output). */
export interface LegacySaturnCycle {
  cycle_number: number;
  period: string;
  [windowKey: string]: unknown;
}

export interface LegacySaturnGroup {
  cycles?: LegacySaturnCycle[];
  birth_detection?: {
    position?: string;
    cycle?: number;
    phase?: string;
    description?: string;
  };
}

/** Legacy Rāśi-based Saturn windows preserved verbatim from the advisory. */
export interface LegacyRasiSaturnWindows {
  mechanism?: string;
  sade_sati?: LegacySaturnGroup;
  elinati_shani?: LegacySaturnGroup;
  ashtama_shani?: LegacySaturnGroup;
}

/** One Nakshatra-Pada band inside a fixed universal Rāśi (e.g. "Shatabhisha P1-P4"). */
export interface FixedRasiBand {
  nakshatra: string;
  pada_from: number;
  pada_to: number;
  display: string; // "P1-P4" | "P3-P4" | "P1" ...
}

/** One Rāśi entry of the identity-independent universal reference (9 absolute padas). */
export interface FixedRasiMapEntry {
  absolute_padas: number[];   // 1-108
  nakshatra_padas: FixedRasiBand[];
  pada_count: number;         // always 9
}

export interface MandaliGocharReport {
  schema_version: string;
  target_date: string;       // YYYY-MM-DD
  reference_moon: {
    rasi: string;
    nakshatra: string;
    pada: number;
    absolute_pada: number;
  };
  chart: MandaliGocharCell[];
  periods: MandaliPeriodEntry[];
  saturn_periods: SaturnPeriods;
  comparison: {
    note: string;
    report_a: RasiGocharEntry[];
    report_b: MandaliPeriodEntry[];
  };
  fixed_rasi_map: Record<string, FixedRasiMapEntry>;
}
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
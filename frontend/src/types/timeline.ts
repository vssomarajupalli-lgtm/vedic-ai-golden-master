export type TimelineType = 
  | 'mahadasha' 
  | 'antardasha' 
  | 'pratyantardasha' 
  | 'future-events' 
  | 'transit' 
  | 'gochara'
  | 'combined';

export interface TimelineVisualizationProps {
  type: TimelineType;
  data: TimelineData;
  options: TimelineOptions;
  mode: 'standard' | 'professional' | 'expert';
}

export interface TimelineData {
  mahadasha?: MahadashaPeriod[];
  currentMahadasha?: MahadashaPeriod;
  antardasha?: AntardashaPeriod[];
  currentAntardasha?: AntardashaPeriod;
  pratyantardasha?: PratyantardashaPeriod[];
  currentPratyantardasha?: PratyantardashaPeriod;
  futureEvents?: FutureEvent[];
  transitWindows?: GocharaWindow[];
  currentTransits?: PlanetTransit[];
  combined?: CombinedTimelineData;
}

export interface TimelineOptions {
  height: number;
  showLabels: boolean;
  showCurrentMarker: boolean;
  showFutureMarkers: boolean;
  interactive: boolean;
  zoomable: boolean;
  exportable: boolean;
  colorScheme: 'standard' | 'professional' | 'accessibility';
  
  zoomLevel: 'year' | 'month' | 'week' | 'day';
  minZoom: 'year' | 'month' | 'week';
  maxZoom: 'year' | 'month' | 'week' | 'day';
  showPastMarkers: boolean;
  markerStyle: 'line' | 'dot' | 'flag';
  syncTracks: boolean;
  syncGroup: string;
  visibleTracks: TimelineTrack[];
  trackOrder: string[];
}

interface TimelineTrack {
  id: string;
  label: string;
  type: 'mahadasha' | 'antardasha' | 'pratyantardasha' | 'gochara' | 'events' | 'transit';
  visible: boolean;
  color: string;
  height: number;
  data: TimelineTrackData;
}

interface TimelineTrackData {
  periods?: MahadashaPeriod[] | AntardashaPeriod[] | PratyantardashaPeriod[];
  events?: FutureEvent[];
  transits?: GocharaWindow[];
}

interface MahadashaPeriod {
  planet: string;
  startDate: string;
  endDate: string;
  duration: string;
  strength: 'strong' | 'moderate' | 'weak';
  significance: string;
}

interface AntardashaPeriod {
  planet: string;
  startDate: string;
  endDate: string;
  duration: string;
  mahadashaLord: string;
}

interface PratyantardashaPeriod {
  planet: string;
  startDate: string;
  endDate: string;
  duration: string;
  antardashaLord: string;
}

interface FutureEvent {
  event: string;
  domain: string;
  startDate: string;
  endDate: string;
  probability: number;
  confidence: 'high' | 'moderate' | 'low';
  triggers: string[];
}

interface GocharaWindow {
  planet: string;
  mandali: string;
  startDate: string;
  endDate: string;
  durationDays: number;
  type: 'sade-sati' | 'elinati' | 'ashtama' | 'favorable' | 'challenging' | 'neutral';
  intensity: 'high' | 'moderate' | 'low';
  affectedDomains: number[];
  activationWindow: { startDate: string; endDate: string; isActive: boolean; daysRemaining?: number };
  expectedInfluence: { domainId: number; domainName: string; influence: 'favorable' | 'challenging' | 'neutral' | 'transformative'; keyEvents: string[]; recommendations: string[] };
  timingConfidence: { overall: 'high' | 'moderate' | 'low'; factors: { factor: string; impact: 'positive' | 'negative' | 'neutral'; weight: number }[] };
  status: 'current' | 'upcoming' | 'future' | 'completed' | 'historical';
  daysUntilStart?: number;
  daysUntilEnd?: number;
}

interface PlanetTransit {
  planet: string;
  longitude: number;
  mandali: string;
  mandaliPosition: number;
  mandaliCenter: string;
  status: 'favorable' | 'challenging' | 'neutral';
  intensity: 'high' | 'moderate' | 'low';
  affectedHouses: number[];
  affectedDomains: number[];
  description: string;
}

interface CombinedTimelineData {
  mahadasha: MahadashaPeriod[];
  antardasha: AntardashaPeriod[];
  pratyantardasha: PratyantardashaPeriod[];
  futureEvents: FutureEvent[];
  transits: GocharaWindow[];
  currentTransits: PlanetTransit[];
}
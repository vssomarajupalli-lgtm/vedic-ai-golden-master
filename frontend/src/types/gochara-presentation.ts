export interface GocharaPresentation {
  currentGochara: CurrentGocharaSnapshot;
  futureGocharaWindows: GocharaWindow[];
  transitStrength: TransitStrengthAnalysis;
  transitIntensity: TransitIntensityAnalysis;
  affectedLifeDomains: AffectedDomain[];
  activationWindow: ActivationWindow;
  expectedInfluence: ExpectedInfluence;
  timingConfidence: TimingConfidence;
  periodClassification: GocharaPeriodClassification;
}

interface CurrentGocharaSnapshot {
  timestamp: Date;
  planets: PlanetTransit[];
  mandaliPositions: MandaliPosition[];
  sadeSatiStatus: SadeSatiStatus;
  elinatiShaniStatus: ElinatiShaniStatus;
  ashtamaShaniStatus: AshtamaShaniStatus;
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

interface MandaliPosition {
  mandali: string;
  planet: string;
  position: number;
}

interface SadeSatiStatus {
  active: boolean;
  phase: 'first' | 'second' | 'third';
  startDate: string;
  endDate: string;
}

interface ElinatiShaniStatus {
  active: boolean;
  startDate: string;
  endDate: string;
}

interface AshtamaShaniStatus {
  active: boolean;
  startDate: string;
  endDate: string;
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
  activationWindow: ActivationWindow;
  expectedInfluence: ExpectedInfluence;
  timingConfidence: TimingConfidence;
  status: 'current' | 'upcoming' | 'future' | 'completed' | 'historical';
  daysUntilStart?: number;
  daysUntilEnd?: number;
}

interface TransitStrengthAnalysis {
  planet: string;
  strength: number;
  classification: 'strong' | 'moderate' | 'weak';
  factors: StrengthFactor[];
}

interface StrengthFactor {
  factor: string;
  value: number;
  weight: number;
}

interface TransitIntensityAnalysis {
  planet: string;
  intensity: 'high' | 'moderate' | 'low';
  duration: string;
  peakDate: string;
  description: string;
}

interface AffectedDomain {
  domainId: number;
  domainName: string;
  planets: string[];
  netInfluence: 'positive' | 'negative' | 'mixed';
  confidence: number;
}

interface ActivationWindow {
  startDate: string;
  endDate: string;
  isActive: boolean;
  daysRemaining?: number;
}

interface ExpectedInfluence {
  domainId: number;
  domainName: string;
  influence: 'favorable' | 'challenging' | 'neutral' | 'transformative';
  keyEvents: string[];
  recommendations: string[];
}

interface TimingConfidence {
  overall: 'high' | 'moderate' | 'low';
  factors: ConfidenceFactor[];
}

interface ConfidenceFactor {
  factor: string;
  impact: 'positive' | 'negative' | 'neutral';
  weight: number;
}

interface GocharaPeriodClassification {
  current: GocharaPeriod[];
  upcoming: GocharaPeriod[];
  future: GocharaPeriod[];
  completed: GocharaPeriod[];
  historical: GocharaPeriod[];
}

interface GocharaPeriod {
  planet: string;
  mandali: string;
  type: 'sade-sati' | 'elinati' | 'ashtama' | 'favorable' | 'challenging' | 'neutral';
  startDate: string;
  endDate: string;
  durationDays: number;
  intensity: 'high' | 'moderate' | 'low';
  affectedDomains: number[];
  activationWindow: ActivationWindow;
  expectedInfluence: ExpectedInfluence;
  timingConfidence: TimingConfidence;
  status: 'current' | 'upcoming' | 'future' | 'completed' | 'historical';
  daysUntilStart?: number;
  daysUntilEnd?: number;
}
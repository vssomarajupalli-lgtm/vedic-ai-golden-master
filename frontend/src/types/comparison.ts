export const MAX_COMPARISON_CHARTS_V1 = 5;

export interface ComparisonWorkspace {
  id: string;
  name: string;
  charts: ComparisonChart[];
  comparisonConfig: ComparisonConfig;
  createdAt: Date;
  updatedAt: Date;
}

export interface ComparisonChart {
  id: string;
  label: string;
  birthData: BirthData;
  color: string;
  isPrimary: boolean;
}

export interface ComparisonConfig {
  selectedDomains: DomainSelection[];
  comparisonMode: ComparisonMode;
  maxCharts: number;
  outputFormat: ComparisonOutputFormat;
}

export interface DomainSelection {
  domainId: number;
  domainName: string;
  selectedQuestions: string[];
  comparisonType: 'side-by-side' | 'differential' | 'overlay';
  enabled: boolean;
}

export type SupportedDomain = 
  | 'marriage'
  | 'career'
  | 'business'
  | 'health'
  | 'education'
  | 'children'
  | 'property'
  | 'foreign-settlement'
  | 'wealth'
  | 'spiritual-growth'
  | 'retirement'
  | 'medical'
  | string;

export type ComparisonMode = 'side-by-side' | 'differential' | 'overlay';
export type ComparisonOutputFormat = 'table' | 'chart' | 'report';

export interface ComparisonResult {
  id: string;
  workspaceId: string;
  chartResults: Map<string, ComparisonChartResult>;
  generatedAt: Date;
}

export interface ComparisonChartResult {
  chartId: string;
  chartLabel: string;
  domainResults: ComparisonDomainResult[];
}

export interface ComparisonDomainResult {
  domainId: number;
  domainName: string;
  questionResults: ComparisonQuestionResult[];
}

export interface ComparisonQuestionResult {
  questionId: string;
  questionTitle: string;
  chartResults: ChartQuestionResult[];
}

export interface ChartQuestionResult {
  chartId: string;
  probability: ProbabilityData;
  timing: TimingData;
  evidence: EvidenceItem[];
  planetaryPositions: PlanetaryPosition[];
  dashaStatus: DashaStatus;
  gocharaStatus: GocharaStatus;
}

export interface BirthData {
  date: string;
  time: string;
  timezone: string;
  latitude: number;
  longitude: number;
  place: string;
}

export interface ProbabilityData {
  score: number;
  grade: string;
  raw: number;
}

export interface TimingData {
  activation: number;
  probability: number;
  window: { start: string; end: string };
}

export interface EvidenceItem {
  factor: string;
  value: string;
  weight: number;
}

export interface PlanetaryPosition {
  planet: string;
  sign: string;
  house: number;
  degree: number;
}

export interface DashaStatus {
  mahadasha: string;
  antardasha: string;
  pratyantardasha: string;
  remaining: string;
}

export interface GocharaStatus {
  planet: string;
  sign: string;
  house: number;
  effect: 'favorable' | 'challenging' | 'neutral';
}
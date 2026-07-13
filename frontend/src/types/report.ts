import type { ConsultationStructure, BirthData, ClientProfile, ReportFormatting, ReportVersion, ReportMetadata } from './consultation';

export interface ConsultationReport {
  id: string;
  consultationId: string;
  version: number;
  structure: ConsultationStructure;
  birthData: BirthData;
  client: ClientProfile;
  computed: ComputedReportData;
  formatting: ReportFormatting;
  metadata: ReportMetadata;
  history: ReportVersion[];
}

export interface ComputedReportData {
  executiveSummary: ExecutiveSummaryData;
  chapters: ComputedChapter[];
  appendices: ComputedAppendixData;
  evidenceIndex: EvidenceIndex;
}

export interface ComputedChapter {
  chapterId: string;
  title: string;
  questions: ComputedQuestion[];
  summary: ChapterSummary;
}

export interface ComputedQuestion {
  questionId: string;
  title: string;
  domain: string;
  formulaKey: string;
  result: QuestionResult;
  evidence: EvidenceItem[];
  timing: TimingData;
  probability: ProbabilityData;
  formulaVerification: FormulaVerificationData;
}

export interface ExecutiveSummaryData {
  overallDirection: string;
  topDomains: DomainSummary[];
  keyStrengths: string[];
  keyChallenges: string[];
  criticalWindows: TimingWindow[];
  primaryRecommendations: string[];
}

export interface DomainSummary {
  domainId: number;
  domainName: string;
  probability: number;
  grade: string;
}

export interface ChapterSummary {
  overallProbability: number;
  overallGrade: string;
  keyInsights: string[];
}

export interface ComputedAppendixData {
  birthChart: BirthChartData;
  planetaryPositions: PlanetaryPosition[];
  dashaTimeline: DashaPeriod[];
  transitCalendar: TransitEvent[];
  vimshottariDetails: VimshottariDetail[];
  ashtakavargaGrid: AshtakavargaData[];
}

export interface EvidenceIndex {
  items: EvidenceItem[];
  byQuestion: Record<string, EvidenceItem[]>;
  byFactor: Record<string, EvidenceItem[]>;
}

export interface EvidenceItem {
  id: string;
  label: string;
  factor: string;
  weight: number;
  value: number;
  description: string;
}

export interface QuestionResult {
  questionId: string;
  probability: ProbabilityData;
  timing: TimingData;
  evidence: EvidenceItem[];
  formulaVerification: FormulaVerificationData;
}

export interface ProbabilityData {
  score: number;
  grade: 'weak' | 'moderate' | 'high';
  confidence: number;
}

export interface TimingData {
  mahadasha: string;
  antardasha: string;
  pratyantardasha: string;
  windows: TimingWindow[];
  confidence: 'high' | 'moderate' | 'low';
}

export interface TimingWindow {
  startDate: string;
  endDate: string;
  probability: number;
  label: string;
}

export interface FormulaVerificationData {
  formulaId: string;
  version: string;
  factors: FormulaFactor[];
  weights: Record<string, number>;
}

export interface FormulaFactor {
  factorId: string;
  name: string;
  weight: number;
  value: number;
  contribution: number;
}

export interface ChapterSummary {
  overallProbability: number;
  overallGrade: string;
  keyInsights: string[];
}

export interface ComputedAppendixData {
  birthChart: BirthChartData;
  planetaryPositions: PlanetaryPosition[];
  dashaTimeline: DashaPeriod[];
  transitCalendar: TransitEvent[];
  vimshottariDetails: VimshottariDetail[];
  ashtakavargaGrid: AshtakavargaData[];
}

export interface EvidenceIndex {
  items: EvidenceItem[];
  byQuestion: Record<string, EvidenceItem[]>;
  byFactor: Record<string, EvidenceItem[]>;
}

export interface EvidenceItem {
  id: string;
  label: string;
  factor: string;
  weight: number;
  value: number;
  description: string;
}

export interface QuestionResult {
  questionId: string;
  probability: ProbabilityData;
  timing: TimingData;
  evidence: EvidenceItem[];
  formulaVerification: FormulaVerificationData;
}

export interface ProbabilityData {
  score: number;
  grade: 'weak' | 'moderate' | 'high';
  confidence: number;
}

export interface TimingData {
  mahadasha: string;
  antardasha: string;
  pratyantardasha: string;
  windows: TimingWindow[];
  confidence: 'high' | 'moderate' | 'low';
}

export interface TimingWindow {
  startDate: string;
  endDate: string;
  probability: number;
  label: string;
}

export interface FormulaVerificationData {
  formulaId: string;
  version: string;
  factors: FormulaFactor[];
  weights: Record<string, number>;
}

export interface FormulaFactor {
  factorId: string;
  name: string;
  weight: number;
  value: number;
  contribution: number;
}

export interface ChapterSummary {
  overallProbability: number;
  overallGrade: string;
  keyInsights: string[];
}

export interface ComputedAppendixData {
  birthChart: BirthChartData;
  planetaryPositions: PlanetaryPosition[];
  dashaTimeline: DashaPeriod[];
  transitCalendar: TransitEvent[];
  vimshottariDetails: VimshottariDetail[];
  ashtakavargaGrid: AshtakavargaData[];
}

export interface EvidenceIndex {
  items: EvidenceItem[];
  byQuestion: Record<string, EvidenceItem[]>;
  byFactor: Record<string, EvidenceItem[]>;
}

export interface EvidenceItem {
  id: string;
  label: string;
  factor: string;
  weight: number;
  value: number;
  description: string;
}

export interface QuestionResult {
  questionId: string;
  probability: ProbabilityData;
  timing: TimingData;
  evidence: EvidenceItem[];
  formulaVerification: FormulaVerificationData;
}

export interface ProbabilityData {
  score: number;
  grade: 'weak' | 'moderate' | 'high';
  confidence: number;
}

export interface TimingData {
  mahadasha: string;
  antardasha: string;
  pratyantardasha: string;
  windows: TimingWindow[];
  confidence: 'high' | 'moderate' | 'low';
}

export interface TimingWindow {
  startDate: string;
  endDate: string;
  probability: number;
  label: string;
}

export interface FormulaVerificationData {
  formulaId: string;
  version: string;
  factors: FormulaFactor[];
  weights: Record<string, number>;
}

export interface FormulaFactor {
  factorId: string;
  name: string;
  weight: number;
  value: number;
  contribution: number;
}

export interface ChapterSummary {
  overallProbability: number;
  overallGrade: string;
  keyInsights: string[];
}

export interface ComputedAppendixData {
  birthChart: BirthChartData;
  planetaryPositions: PlanetaryPosition[];
  dashaTimeline: DashaPeriod[];
  transitCalendar: TransitEvent[];
  vimshottariDetails: VimshottariDetail[];
  ashtakavargaGrid: AshtakavargaData[];
}

export interface EvidenceIndex {
  items: EvidenceItem[];
  byQuestion: Record<string, EvidenceItem[]>;
  byFactor: Record<string, EvidenceItem[]>;
}

export interface EvidenceItem {
  id: string;
  label: string;
  factor: string;
  weight: number;
  value: number;
  description: string;
}

export interface QuestionResult {
  questionId: string;
  probability: ProbabilityData;
  timing: TimingData;
  evidence: EvidenceItem[];
  formulaVerification: FormulaVerificationData;
}

export interface ProbabilityData {
  score: number;
  grade: 'weak' | 'moderate' | 'high';
  confidence: number;
}

export interface TimingData {
  mahadasha: string;
  antardasha: string;
  pratyantardasha: string;
  windows: TimingWindow[];
  confidence: 'high' | 'moderate' | 'low';
}

export interface TimingWindow {
  startDate: string;
  endDate: string;
  probability: number;
  label: string;
}

export interface FormulaVerificationData {
  formulaId: string;
  version: string;
  factors: FormulaFactor[];
  weights: Record<string, number>;
}

export interface FormulaFactor {
  factorId: string;
  name: string;
  weight: number;
  value: number;
  contribution: number;
}

export interface ReportVersion {
  version: number;
  timestamp: Date;
  author: string;
  changes: string;
  reportSnapshotId: string;
}

export interface ReportMetadata {
  reportId: string;
  reportVersion: number;
  reportType: 'consultation' | 'comparison' | 'template';
  generationDate: Date;
  generatedBy: string;
  generationDurationMs: number;
  engineVersions: Record<string, string>;
  formulaRegistryVersion: string;
  questionCatalogVersion: string;
  calibrationProfileVersion: string;
  desktopRuntimeVersion?: string;
  serverRuntimeVersion?: string;
  browserRuntimeVersion?: string;
  chartId: string;
  chartName: string;
  birthDataHash: string;
  pageCount: number;
  wordCount: number;
  questionCount: number;
  domainCount: number;
  checksum: string;
  signature?: string;
  consultationSnapshotId: string;
  reproductionInstructions: string;
}
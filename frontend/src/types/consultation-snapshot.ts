export interface ConsultationSnapshot {
  snapshotId: string;
  consultationId: string;
  version: number;
  capturedAt: Date;
  capturedBy: string;
  captureReason: 'report_generation' | 'manual' | 'scheduled' | 'comparison_baseline';
  consultationState: ConsultationStateCapture;
  calibrationState: CalibrationStateCapture;
  engineState: EngineStateCapture;
  reportState: ReportStateCapture;
  metadata: SnapshotMetadata;
}

interface ConsultationStateCapture {
  consultation: Consultation;
  selectedQuestions: string[];
  structure: ConsultationStructure;
  birthData: BirthData;
  clientProfile: ClientProfile;
}

interface CalibrationStateCapture {
  activeProfile: string;
  profileVersion: string;
  profileHash: string;
  profileContent: CalibrationProfile;
  overrides: CalibrationOverride[];
}

interface EngineStateCapture {
  engineVersions: Record<string, string>;
  engineConfigs: Record<string, EngineConfig>;
  pipelineConfig: PipelineConfig;
}

interface ReportStateCapture {
  generatedReport: ConsultationReport;
  generationMetadata: ReportMetadata;
  outputFormats: GeneratedOutput[];
}

interface SnapshotMetadata {
  snapshotSizeBytes: number;
  compressionAlgorithm: 'gzip' | 'none';
  encryptionAlgorithm?: 'AES-256-GCM';
  storageLocation: 'local' | 'cloud' | 'hybrid';
  retentionPolicy: 'permanent' | '7_years' | '1_year';
  tags: string[];
  repository: RepositoryMetadata;
  build: BuildMetadata;
}

interface RepositoryMetadata {
  repositoryUrl: string;
  gitCommit: string;
  gitTag: string;
  gitBranch: string;
  architectureVersion: string;
  dirtyWorkingTree: boolean;
}

interface BuildMetadata {
  architectureVersion: string;
  questionCatalogVersion: string;
  formulaRegistryVersion: string;
  calibrationVersion: string;
  desktopRuntimeVersion: string;
  serverRuntimeVersion?: string;
  frontendVersion: string;
  backendVersion: string;
  buildTimestamp: Date;
  buildCommit: string;
  buildTag: string;
}

export interface SnapshotManager {
  createSnapshot(
    consultation: Consultation,
    generatedReport: ConsultationReport,
    reason: 'report_generation' | 'manual' | 'scheduled' | 'comparison_baseline'
  ): Promise<ConsultationSnapshot>;
  reproduceFromSnapshot(snapshotId: string): Promise<ReproductionResult>;
  getSnapshots(consultationId: string): Promise<ConsultationSnapshot[]>;
  compareSnapshots(baselineId: string, currentId: string): Promise<SnapshotComparison>;
}

interface ReproductionResult {
  success: boolean;
  report?: ConsultationReport;
  differences: string[];
}

interface SnapshotComparison {
  baselineId: string;
  currentId: string;
  differences: SnapshotDifference[];
  similarity: number;
}

interface SnapshotDifference {
  path: string;
  baseline: any;
  current: any;
  type: 'added' | 'removed' | 'modified';
}

interface Consultation {
  id: string;
  title: string;
  client: ClientProfile;
  birthData: BirthData;
  structure: ConsultationStructure;
  formatting: ReportFormatting;
  metadata: ConsultationMetadata;
  createdAt: Date;
  updatedAt: Date;
  generatedAt?: Date;
}

interface ClientProfile {
  name: string;
  email?: string;
  phone?: string;
  notes?: string;
  tags: string[];
}

interface BirthData {
  date: string;
  time: string;
  timezone: string;
  latitude: number;
  longitude: number;
  place: string;
}

interface ConsultationStructure {
  coverPage: CoverPageConfig;
  executiveSummary: ExecutiveSummaryConfig;
  chapters: Chapter[];
  appendices: AppendixConfig;
}

interface CoverPageConfig {
  include: boolean;
  title: string;
  clientName: boolean;
  birthDetails: boolean;
  dateGenerated: boolean;
}

interface ExecutiveSummaryConfig {
  mode: 'auto' | 'custom' | 'none';
  customText?: string;
  includeKeyMetrics: boolean;
  includeRecommendations: boolean;
}

interface Chapter {
  id: string;
  title: string;
  order: number;
  included: boolean;
  customIntro?: string;
  questions: ChapterQuestion[];
}

interface ChapterQuestion {
  questionId: string;
  domainId: number;
  order: number;
  included: boolean;
  customLabel?: string;
}

interface AppendixConfig {
  birthChart: boolean;
  planetaryPositions: boolean;
  dashaTimeline: boolean;
  transitCalendar: boolean;
  vimshottariDetails: boolean;
  ashtakavargaGrid: boolean;
}

interface ReportFormatting {
  pageSize: 'A4' | 'Letter';
  orientation: 'portrait' | 'landscape';
  margins: { top: number; bottom: number; left: number; right: number };
  header: HeaderFooterConfig;
  footer: HeaderFooterConfig;
  pageNumbers: PageNumberConfig;
  typography: TypographyConfig;
  branding: BrandingConfig;
}

interface HeaderFooterConfig {
  enabled: boolean;
  left?: string;
  center?: string;
  right?: string;
}

interface PageNumberConfig {
  enabled: boolean;
  format: 'arabic' | 'roman' | 'alphabetic';
  startNumber: number;
}

interface TypographyConfig {
  fontFamily: string;
  fontSize: number;
  lineHeight: number;
  headingFontFamily: string;
}

interface BrandingConfig {
  logo?: string;
  headerColor: string;
  footerColor: string;
  accentColor: string;
}

interface ConsultationMetadata {
  version: number;
  createdAt: Date;
  updatedAt: Date;
  generatedAt?: Date;
  templateId?: string;
  tags: string[];
}

interface BirthData {
  date: string;
  time: string;
  timezone: string;
  latitude: number;
  longitude: number;
  place: string;
}

interface ClientProfile {
  name: string;
  email?: string;
  phone?: string;
  notes?: string;
  tags: string[];
}

interface ConsultationStructure {
  coverPage: CoverPageConfig;
  executiveSummary: ExecutiveSummaryConfig;
  chapters: Chapter[];
  appendices: AppendixConfig;
}

interface Chapter {
  id: string;
  title: string;
  order: number;
  included: boolean;
  customIntro?: string;
  questions: ChapterQuestion[];
}

interface ChapterQuestion {
  questionId: string;
  domainId: number;
  order: number;
  included: boolean;
  customLabel?: string;
}

interface CoverPageConfig {
  include: boolean;
  title: string;
  clientName: boolean;
  birthDetails: boolean;
  dateGenerated: boolean;
}

interface ExecutiveSummaryConfig {
  mode: 'auto' | 'custom' | 'none';
  customText?: string;
  includeKeyMetrics: boolean;
  includeRecommendations: boolean;
}

interface AppendixConfig {
  birthChart: boolean;
  planetaryPositions: boolean;
  dashaTimeline: boolean;
  transitCalendar: boolean;
  vimshottariDetails: boolean;
  ashtakavargaGrid: boolean;
}

interface ReportFormatting {
  pageSize: 'A4' | 'Letter';
  orientation: 'portrait' | 'landscape';
  margins: { top: number; bottom: number; left: number; right: number };
  header: HeaderFooterConfig;
  footer: HeaderFooterConfig;
  pageNumbers: PageNumberConfig;
  typography: TypographyConfig;
  branding: BrandingConfig;
}

interface HeaderFooterConfig {
  enabled: boolean;
  left?: string;
  center?: string;
  right?: string;
}

interface PageNumberConfig {
  enabled: boolean;
  format: 'arabic' | 'roman' | 'alphabetic';
  startNumber: number;
}

interface TypographyConfig {
  fontFamily: string;
  fontSize: number;
  lineHeight: number;
  headingFontFamily: string;
}

interface BrandingConfig {
  logo?: string;
  headerColor: string;
  footerColor: string;
  accentColor: string;
}

interface CalibrationProfile {
  version: string;
  formulaCalibration: Record<string, FormulaCalibration>;
  lastUpdated: Date;
}

interface FormulaCalibration {
  factors: FactorCalibration[];
  weightSum: number;
  normalized: boolean;
}

interface FactorCalibration {
  factorId: string;
  weight: number;
  enabled: boolean;
  description: string;
}

interface CalibrationOverride {
  factorId: string;
  weight: number;
  reason: string;
  appliedAt: Date;
}

interface EngineConfig {
  enabled: boolean;
  parameters: Record<string, any>;
}

interface PipelineConfig {
  enabledEngines: string[];
  executionOrder: string[];
  timeoutMs: number;
}

interface GeneratedOutput {
  format: 'pdf' | 'html' | 'print' | 'archive';
  timestamp: Date;
  filePath?: string;
  url?: string;
}

interface ConsultationReport {
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

interface ComputedReportData {
  executiveSummary: ExecutiveSummaryData;
  chapters: ComputedChapter[];
  appendices: ComputedAppendixData;
  evidenceIndex: EvidenceIndex;
}

interface ExecutiveSummaryData {
  overallDirection: string;
  topDomains: DomainSummary[];
  keyStrengths: string[];
  keyChallenges: string[];
  criticalWindows: TimingWindow[];
  primaryRecommendations: string[];
}

interface DomainSummary {
  domainId: number;
  domainName: string;
  probability: number;
  grade: string;
}

interface TimingWindow {
  period: string;
  probability: number;
  domain: string;
}

interface ComputedChapter {
  chapterId: string;
  title: string;
  questions: ComputedQuestion[];
  summary: ChapterSummary;
}

interface ComputedQuestion {
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

interface QuestionResult {
  score: number;
  grade: string;
  details: string;
}

interface EvidenceItem {
  factor: string;
  value: string;
  weight: number;
}

interface TimingData {
  activation: number;
  probability: number;
  window: { start: string; end: string };
}

interface ProbabilityData {
  score: number;
  grade: string;
  raw: number;
}

interface FormulaVerificationData {
  formulaId: string;
  version: string;
  factors: FactorVerification[];
}

interface FactorVerification {
  factorId: string;
  value: number;
  normalized: number;
  contribution: number;
}

interface ChapterSummary {
  keyInsights: string[];
  overallGrade: string;
}

interface ComputedAppendixData {
  birthChart?: BirthChartData;
  planetaryPositions?: PlanetaryPositionData[];
  dashaTimeline?: DashaTimelineData;
  transitCalendar?: TransitCalendarData;
  vimshottariDetails?: VimshottariDetailData;
  ashtakavargaGrid?: AshtakavargaGridData;
}

interface BirthChartData {
  svg: string;
  ascendant: string;
  planets: PlanetaryPositionData[];
}

interface PlanetaryPositionData {
  planet: string;
  sign: string;
  house: number;
  degree: number;
  nakshatra: string;
  pada: number;
}

interface DashaTimelineData {
  periods: DashaPeriod[];
}

interface DashaPeriod {
  planet: string;
  type: 'mahadasha' | 'antardasha' | 'pratyantardasha';
  startDate: string;
  endDate: string;
  duration: string;
}

interface TransitCalendarData {
  months: TransitMonth[];
}

interface TransitMonth {
  month: string;
  events: TransitEvent[];
}

interface TransitEvent {
  planet: string;
  event: string;
  date: string;
  intensity: 'high' | 'moderate' | 'low';
}

interface VimshottariDetailData {
  mahadasha: DashaPeriod[];
  antardasha: DashaPeriod[];
  pratyantardasha: DashaPeriod[];
}

interface AshtakavargaGridData {
  planets: string[];
  houses: number[][];
  total: number[];
}

interface ReportMetadata {
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

interface ReportVersion {
  version: number;
  timestamp: Date;
  author: string;
  changes: string;
  reportSnapshotId: string;
}

interface ClientProfile {
  name: string;
  email?: string;
  phone?: string;
  notes?: string;
  tags: string[];
}

interface BirthData {
  date: string;
  time: string;
  timezone: string;
  latitude: number;
  longitude: number;
  place: string;
}

interface ClientProfile {
  name: string;
  email?: string;
  phone?: string;
  notes?: string;
  tags: string[];
}

interface ConsultationStructure {
  coverPage: CoverPageConfig;
  executiveSummary: ExecutiveSummaryConfig;
  chapters: Chapter[];
  appendices: AppendixConfig;
}

interface Chapter {
  id: string;
  title: string;
  order: number;
  included: boolean;
  customIntro?: string;
  questions: ChapterQuestion[];
}

interface ChapterQuestion {
  questionId: string;
  domainId: number;
  order: number;
  included: boolean;
  customLabel?: string;
}

interface CoverPageConfig {
  include: boolean;
  title: string;
  clientName: boolean;
  birthDetails: boolean;
  dateGenerated: boolean;
}

interface ExecutiveSummaryConfig {
  mode: 'auto' | 'custom' | 'none';
  customText?: string;
  includeKeyMetrics: boolean;
  includeRecommendations: boolean;
}

interface AppendixConfig {
  birthChart: boolean;
  planetaryPositions: boolean;
  dashaTimeline: boolean;
  transitCalendar: boolean;
  vimshottariDetails: boolean;
  ashtakavargaGrid: boolean;
}

interface ReportFormatting {
  pageSize: 'A4' | 'Letter';
  orientation: 'portrait' | 'landscape';
  margins: { top: number; bottom: number; left: number; right: number };
  header: HeaderFooterConfig;
  footer: HeaderFooterConfig;
  pageNumbers: PageNumberConfig;
  typography: TypographyConfig;
  branding: BrandingConfig;
}

interface HeaderFooterConfig {
  enabled: boolean;
  left?: string;
  center?: string;
  right?: string;
}

interface PageNumberConfig {
  enabled: boolean;
  format: 'arabic' | 'roman' | 'alphabetic';
  startNumber: number;
}

interface TypographyConfig {
  fontFamily: string;
  fontSize: number;
  lineHeight: number;
  headingFontFamily: string;
}

interface BrandingConfig {
  logo?: string;
  headerColor: string;
  footerColor: string;
  accentColor: string;
}

interface ClientProfile {
  name: string;
  email?: string;
  phone?: string;
  notes?: string;
  tags: string[];
}

interface ConsultationStructure {
  coverPage: CoverPageConfig;
  executiveSummary: ExecutiveSummaryConfig;
  chapters: Chapter[];
  appendices: AppendixConfig;
}

interface Chapter {
  id: string;
  title: string;
  order: number;
  included: boolean;
  customIntro?: string;
  questions: ChapterQuestion[];
}

interface ChapterQuestion {
  questionId: string;
  domainId: number;
  order: number;
  included: boolean;
  customLabel?: string;
}

interface CoverPageConfig {
  include: boolean;
  title: string;
  clientName: boolean;
  birthDetails: boolean;
  dateGenerated: boolean;
}

interface ExecutiveSummaryConfig {
  mode: 'auto' | 'custom' | 'none';
  customText?: string;
  includeKeyMetrics: boolean;
  includeRecommendations: boolean;
}

interface AppendixConfig {
  birthChart: boolean;
  planetaryPositions: boolean;
  dashaTimeline: boolean;
  transitCalendar: boolean;
  vimshottariDetails: boolean;
  ashtakavargaGrid: boolean;
}

interface ReportFormatting {
  pageSize: 'A4' | 'Letter';
  orientation: 'portrait' | 'landscape';
  margins: { top: number; bottom: number; left: number; right: number };
  header: HeaderFooterConfig;
  footer: HeaderFooterConfig;
  pageNumbers: PageNumberConfig;
  typography: TypographyConfig;
  branding: BrandingConfig;
}

interface HeaderFooterConfig {
  enabled: boolean;
  left?: string;
  center?: string;
  right?: string;
}

interface PageNumberConfig {
  enabled: boolean;
  format: 'arabic' | 'roman' | 'alphabetic';
  startNumber: number;
}

interface TypographyConfig {
  fontFamily: string;
  fontSize: number;
  lineHeight: number;
  headingFontFamily: string;
}

interface BrandingConfig {
  logo?: string;
  headerColor: string;
  footerColor: string;
  accentColor: string;
}

interface ClientProfile {
  name: string;
  email?: string;
  phone?: string;
  notes?: string;
  tags: string[];
}

interface ConsultationStructure {
  coverPage: CoverPageConfig;
  executiveSummary: ExecutiveSummaryConfig;
  chapters: Chapter[];
  appendices: AppendixConfig;
}

interface Chapter {
  id: string;
  title: string;
  order: number;
  included: boolean;
  customIntro?: string;
  questions: ChapterQuestion[];
}

interface ChapterQuestion {
  questionId: string;
  domainId: number;
  order: number;
  included: boolean;
  customLabel?: string;
}

interface CoverPageConfig {
  include: boolean;
  title: string;
  clientName: boolean;
  birthDetails: boolean;
  dateGenerated: boolean;
}

interface ExecutiveSummaryConfig {
  mode: 'auto' | 'custom' | 'none';
  customText?: string;
  includeKeyMetrics: boolean;
  includeRecommendations: boolean;
}

interface AppendixConfig {
  birthChart: boolean;
  planetaryPositions: boolean;
  dashaTimeline: boolean;
  transitCalendar: boolean;
  vimshottariDetails: boolean;
  ashtakavargaGrid: boolean;
}

interface ReportFormatting {
  pageSize: 'A4' | 'Letter';
  orientation: 'portrait' | 'landscape';
  margins: { top: number; bottom: number; left: number; right: number };
  header: HeaderFooterConfig;
  footer: HeaderFooterConfig;
  pageNumbers: PageNumberConfig;
  typography: TypographyConfig;
  branding: BrandingConfig;
}

interface HeaderFooterConfig {
  enabled: boolean;
  left?: string;
  center?: string;
  right?: string;
}

interface PageNumberConfig {
  enabled: boolean;
  format: 'arabic' | 'roman' | 'alphabetic';
  startNumber: number;
}

interface TypographyConfig {
  fontFamily: string;
  fontSize: number;
  lineHeight: number;
  headingFontFamily: string;
}

interface BrandingConfig {
  logo?: string;
  headerColor: string;
  footerColor: string;
  accentColor: string;
}

interface ClientProfile {
  name: string;
  email?: string;
  phone?: string;
  notes?: string;
  tags: string[];
}

interface ConsultationStructure {
  coverPage: CoverPageConfig;
  executiveSummary: ExecutiveSummaryConfig;
  chapters: Chapter[];
  appendices: AppendixConfig;
}

interface Chapter {
  id: string;
  title: string;
  order: number;
  included: boolean;
  customIntro?: string;
  questions: ChapterQuestion[];
}

interface ChapterQuestion {
  questionId: string;
  domainId: number;
  order: number;
  included: boolean;
  customLabel?: string;
}

interface CoverPageConfig {
  include: boolean;
  title: string;
  clientName: boolean;
  birthDetails: boolean;
  dateGenerated: boolean;
}

interface ExecutiveSummaryConfig {
  mode: 'auto' | 'custom' | 'none';
  customText?: string;
  includeKeyMetrics: boolean;
  includeRecommendations: boolean;
}

interface AppendixConfig {
  birthChart: boolean;
  planetaryPositions: boolean;
  dashaTimeline: boolean;
  transitCalendar: boolean;
  vimshottariDetails: boolean;
  ashtakavargaGrid: boolean;
}

interface ReportFormatting {
  pageSize: 'A4' | 'Letter';
  orientation: 'portrait' | 'landscape';
  margins: { top: number; bottom: number; left: number; right: number };
  header: HeaderFooterConfig;
  footer: HeaderFooterConfig;
  pageNumbers: PageNumberConfig;
  typography: TypographyConfig;
  branding: BrandingConfig;
}

interface HeaderFooterConfig {
  enabled: boolean;
  left?: string;
  center?: string;
  right?: string;
}

interface PageNumberConfig {
  enabled: boolean;
  format: 'arabic' | 'roman' | 'alphabetic';
  startNumber: number;
}

interface TypographyConfig {
  fontFamily: string;
  fontSize: number;
  lineHeight: number;
  headingFontFamily: string;
}

interface BrandingConfig {
  logo?: string;
  headerColor: string;
  footerColor: string;
  accentColor: string;
}

interface ClientProfile {
  name: string;
  email?: string;
  phone?: string;
  notes?: string;
  tags: string[];
}

interface ConsultationStructure {
  coverPage: CoverPageConfig;
  executiveSummary: ExecutiveSummaryConfig;
  chapters: Chapter[];
  appendices: AppendixConfig;
}

interface Chapter {
  id: string;
  title: string;
  order: number;
  included: boolean;
  customIntro?: string;
  questions: ChapterQuestion[];
}

interface ChapterQuestion {
  questionId: string;
  domainId: number;
  order: number;
  included: boolean;
  customLabel?: string;
}

interface CoverPageConfig {
  include: boolean;
  title: string;
  clientName: boolean;
  birthDetails: boolean;
  dateGenerated: boolean;
}

interface ExecutiveSummaryConfig {
  mode: 'auto' | 'custom' | 'none';
  customText?: string;
  includeKeyMetrics: boolean;
  includeRecommendations: boolean;
}

interface AppendixConfig {
  birthChart: boolean;
  planetaryPositions: boolean;
  dashaTimeline: boolean;
  transitCalendar: boolean;
  vimshottariDetails: boolean;
  ashtakavargaGrid: boolean;
}

interface ReportFormatting {
  pageSize: 'A4' | 'Letter';
  orientation: 'portrait' | 'landscape';
  margins: { top: number; bottom: number; left: number; right: number };
  header: HeaderFooterConfig;
  footer: HeaderFooterConfig;
  pageNumbers: PageNumberConfig;
  typography: TypographyConfig;
  branding: BrandingConfig;
}

interface HeaderFooterConfig {
  enabled: boolean;
  left?: string;
  center?: string;
  right?: string;
}

interface PageNumberConfig {
  enabled: boolean;
  format: 'arabic' | 'roman' | 'alphabetic';
  startNumber: number;
}

interface TypographyConfig {
  fontFamily: string;
  fontSize: number;
  lineHeight: number;
  headingFontFamily: string;
}

interface BrandingConfig {
  logo?: string;
  headerColor: string;
  footerColor: string;
  accentColor: string;
}

interface ClientProfile {
  name: string;
  email?: string;
  phone?: string;
  notes?: string;
  tags: string[];
}

interface ConsultationStructure {
  coverPage: CoverPageConfig;
  executiveSummary: ExecutiveSummaryConfig;
  chapters: Chapter[];
  appendices: AppendixConfig;
}

interface Chapter {
  id: string;
  title: string;
  order: number;
  included: boolean;
  customIntro?: string;
  questions: ChapterQuestion[];
}

interface ChapterQuestion {
  questionId: string;
  domainId: number;
  order: number;
  included: boolean;
  customLabel?: string;
}

interface CoverPageConfig {
  include: boolean;
  title: string;
  clientName: boolean;
  birthDetails: boolean;
  dateGenerated: boolean;
}

interface ExecutiveSummaryConfig {
  mode: 'auto' | 'custom' | 'none';
  customText?: string;
  includeKeyMetrics: boolean;
  includeRecommendations: boolean;
}

interface AppendixConfig {
  birthChart: boolean;
  planetaryPositions: boolean;
  dashaTimeline: boolean;
  transitCalendar: boolean;
  vimshottariDetails: boolean;
  ashtakavargaGrid: boolean;
}

interface ReportFormatting {
  pageSize: 'A4' | 'Letter';
  orientation: 'portrait' | 'landscape';
  margins: { top: number; bottom: number; left: number; right: number };
  header: HeaderFooterConfig;
  footer: HeaderFooterConfig;
  pageNumbers: PageNumberConfig;
  typography: TypographyConfig;
  branding: BrandingConfig;
}

interface HeaderFooterConfig {
  enabled: boolean;
  left?: string;
  center?: string;
  right?: string;
}

interface PageNumberConfig {
  enabled: boolean;
  format: 'arabic' | 'roman' | 'alphabetic';
  startNumber: number;
}

interface TypographyConfig {
  fontFamily: string;
  fontSize: number;
  lineHeight: number;
  headingFontFamily: string;
}

interface BrandingConfig {
  logo?: string;
  headerColor: string;
  footerColor: string;
  accentColor: string;
}

interface ClientProfile {
  name: string;
  email?: string;
  phone?: string;
  notes?: string;
  tags: string[];
}

interface ConsultationStructure {
  coverPage: CoverPageConfig;
  executiveSummary: ExecutiveSummaryConfig;
  chapters: Chapter[];
  appendices: AppendixConfig;
}

interface Chapter {
  id: string;
  title: string;
  order: number;
  included: boolean;
  customIntro?: string;
  questions: ChapterQuestion[];
}

interface ChapterQuestion {
  questionId: string;
  domainId: number;
  order: number;
  included: boolean;
  customLabel?: string;
}

interface CoverPageConfig {
  include: boolean;
  title: string;
  clientName: boolean;
  birthDetails: boolean;
  dateGenerated: boolean;
}

interface ExecutiveSummaryConfig {
  mode: 'auto' | 'custom' | 'none';
  customText?: string;
  includeKeyMetrics: boolean;
  includeRecommendations: boolean;
}

interface AppendixConfig {
  birthChart: boolean;
  planetaryPositions: boolean;
  dashaTimeline: boolean;
  transitCalendar: boolean;
  vimshottariDetails: boolean;
  ashtakavargaGrid: boolean;
}

interface ReportFormatting {
  pageSize: 'A4' | 'Letter';
  orientation: 'portrait' | 'landscape';
  margins: { top: number; bottom: number; left: number; right: number };
  header: HeaderFooterConfig;
  footer: HeaderFooterConfig;
  pageNumbers: PageNumberConfig;
  typography: TypographyConfig;
  branding: BrandingConfig;
}

interface HeaderFooterConfig {
  enabled: boolean;
  left?: string;
  center?: string;
  right?: string;
}

interface PageNumberConfig {
  enabled: boolean;
  format: 'arabic' | 'roman' | 'alphabetic';
  startNumber: number;
}

interface TypographyConfig {
  fontFamily: string;
  fontSize: number;
  lineHeight: number;
  headingFontFamily: string;
}

interface BrandingConfig {
  logo?: string;
  headerColor: string;
  footerColor: string;
  accentColor: string;
}

interface ClientProfile {
  name: string;
  email?: string;
  phone?: string;
  notes?: string;
  tags: string[];
}
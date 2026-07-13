export interface Consultation {
  id: string;
  version: number;
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

export interface ClientProfile {
  name: string;
  email?: string;
  phone?: string;
  notes?: string;
  tags: string[];
}

export interface BirthData {
  date: string;
  time: string;
  timezone: string;
  latitude: number;
  longitude: number;
  place: string;
}

export interface ConsultationStructure {
  coverPage: CoverPageConfig;
  executiveSummary: ExecutiveSummaryConfig;
  chapters: Chapter[];
  appendices: AppendixConfig;
}

export interface CoverPageConfig {
  included: boolean;
  title: string;
  showClientName: boolean;
  showBirthDetails: boolean;
  showReportDate: boolean;
  branding: BrandingConfig;
}

export interface ExecutiveSummaryConfig {
  mode: 'auto' | 'custom' | 'none';
  customText?: string;
  includeKeyMetrics: boolean;
  includeRecommendations: boolean;
}

export interface Chapter {
  id: string;
  title: string;
  order: number;
  included: boolean;
  customIntro?: string;
  questions: ChapterQuestion[];
}

export interface ChapterQuestion {
  questionId: string;
  domainId: number;
  order: number;
  included: boolean;
  customLabel?: string;
}

export interface AppendixConfig {
  birthChart: boolean;
  planetaryPositions: boolean;
  dashaTimeline: boolean;
  transitCalendar: boolean;
  vimshottariDetails: boolean;
  ashtakavargaGrid: boolean;
}

export interface ReportFormatting {
  pageSize: 'A4' | 'Letter';
  orientation: 'portrait' | 'landscape';
  margins: { top: number; right: number; bottom: number; left: number };
  header: HeaderFooterConfig;
  footer: HeaderFooterConfig;
  pageNumbers: PageNumberConfig;
  typography: TypographyConfig;
  branding: BrandingConfig;
}

export interface HeaderFooterConfig {
  enabled: boolean;
  left?: string;
  center?: string;
  right?: string;
}

export interface PageNumberConfig {
  enabled: boolean;
  format: 'arabic' | 'roman' | 'appendix';
  position: 'bottom-center' | 'bottom-right' | 'bottom-left';
}

export interface TypographyConfig {
  fontHeading: string;
  fontBody: string;
  fontMono: string;
  fontSizeBase: number;
  lineHeight: number;
}

export interface BrandingConfig {
  logoUrl?: string;
  primaryColor: string;
  secondaryColor: string;
  showWatermark: boolean;
}

export interface ConsultationMetadata {
  consultationId: string;
  reportId?: string;
  version: number;
  generatedAt?: Date;
  generatedBy?: string;
  templateId?: string;
  tags: string[];
}

export interface ClientProfile {
  name: string;
  email?: string;
  phone?: string;
  notes?: string;
  tags: string[];
}

export interface BirthData {
  date: string;
  time: string;
  timezone: string;
  latitude: number;
  longitude: number;
  place: string;
}
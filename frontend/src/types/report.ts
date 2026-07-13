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
export interface ConsultationSnapshot {
  snapshotId: string;
  consultationId: string;
  version: number;
  capturedAt: Date;
  capturedBy: string;
  captureReason: 'report_generation' | 'manual' | 'scheduled';
  questions: string[];
  formulaRegistryVersion: string;
  formulaRegistryHash: string;
  calibrationProfileVersion: string;
  calibrationProfileHash: string;
  decisionLayerVersion: string;
  decisionLayerHash: string;
  reportVersion: string;
  reportHash: string;
  desktopRuntimeVersion: string;
  buildMetadata: {
    architectureVersion: string;
    questionCatalogVersion: string;
    formulaRegistryVersion: string;
    calibrationVersion: string;
    desktopRuntimeVersion: string;
    buildTimestamp: string;
    buildCommit: string;
    buildTag: string;
  };
  metadata: {
    clientName: string;
    birthDataHash: string;
    consultationTitle: string;
    generatedBy: string;
    tags: string[];
  };
  integrity: {
    checksum: string;
    signature?: string;
    reproducible: boolean;
  };
  git: {
    commit: string;
    tag: string;
    branch: string;
    dirty: boolean;
  };
}

export interface SnapshotDifference {
  snapshotId: string;
  comparedTo: string;
  differences: {
    questions: { added: string[]; removed: string[] };
    formulas: { changed: string[] };
    calibration: { changed: string[] };
    decisions: { changed: string[] };
  };
  impactAssessment: 'none' | 'minor' | 'significant' | 'critical';
}
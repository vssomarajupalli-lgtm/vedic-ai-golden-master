export interface FormulaComparison {
  id: string;
  name: string;
  formulaId: string;
  baseline: FormulaSnapshot;
  current: FormulaSnapshot;
  comparisonType: 'version' | 'calibration' | 'engine' | 'manual';
  generatedAt: Date;
  generatedBy: string;
  purpose: 'calibration_verification' | 'formula_refinement' | 'regression_analysis' | 'research';
}

interface FormulaSnapshot {
  version: string;
  calibrationProfile: string;
  engineVersions: Record<string, string>;
  inputs: FormulaInputs;
  outputs: FormulaOutputs;
  probability: number;
  factors: FactorSnapshot[];
  evidence: any[];
  timing: any;
  metadata: SnapshotMetadata;
}

interface FormulaInputs {
  // input parameters
}

interface FormulaOutputs {
  // output values
}

interface FactorSnapshot {
  factorId: string;
  name: string;
  weight: number;
  value: number;
  contribution: number;
}

interface SnapshotMetadata {
  timestamp: Date;
  engineVersions: Record<string, string>;
  calibrationProfile: string;
}

export interface FormulaComparisonResult {
  probabilityDelta: number;
  probabilityDeltaPct: number;
  factorDeltas: FactorDelta[];
  evidenceChanges: EvidenceChange[];
  timingChanges: TimingChange[];
  recommendation: 'accept' | 'review' | 'reject';
}

interface FactorDelta {
  factorId: string;
  baselineValue: number;
  currentValue: number;
  delta: number;
  deltaPct: number;
  impact: 'significant' | 'moderate' | 'minor';
}

interface EvidenceChange {
  evidenceId: string;
  baseline: string;
  current: string;
  changeType: 'added' | 'removed' | 'modified';
}

interface TimingChange {
  windowId: string;
  baselineStart: string;
  currentStart: string;
  baselineEnd: string;
  currentEnd: string;
  deltaDays: number;
}

export interface FormulaReviewWorkflow {
  id: string;
  name: string;
  formulaId: string;
  status: 'draft' | 'in_review' | 'accepted' | 'rejected' | 'archived';
  baseline: FormulaSnapshot;
  current: FormulaSnapshot;
  intermediate?: FormulaSnapshot[];
  comparison: FormulaComparisonResult;
  calibrationImpact: CalibrationImpactAnalysis;
  regressionFlags: RegressionFlag[];
  reviewer: string;
  createdAt: Date;
  reviewedAt?: Date;
  decidedAt?: Date;
  decision: 'accept' | 'reject' | 'needs_revision';
  decisionNotes: string;
  archiveId?: string;
  archivedAt?: Date;
}

interface CalibrationImpactAnalysis {
  affectedQuestions: string[];
  maxProbabilityShift: number;
  weightChanges: number;
  factorChanges: number;
}

interface RegressionFlag {
  type: 'new_factor' | 'weight_shift' | 'probability_shift';
  severity: 'high' | 'medium' | 'low';
  description: string;
}

export interface FormulaComparisonPanelProps {
  workflow: FormulaReviewWorkflow;
  onDecision: (decision: 'accept' | 'reject' | 'needs_revision', notes: string) => void;
  onArchive: () => void;
  mode: 'review' | 'compare' | 'history';
}
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

interface FormulaSnapshot {
  version: string;
  calibrationProfile: string;
  engineVersions: Record<string, string>;
  inputs: FormulaInputs;
  outputs: FormulaOutputs;
  probability: number;
  factors: FactorSnapshot[];
  evidence: EvidenceItem[];
  timing: TimingData;
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

interface FormulaSnapshot {
  version: string;
  calibrationProfile: string;
  engineVersions: Record<string, string>;
  inputs: FormulaInputs;
  outputs: FormulaOutputs;
  probability: number;
  factors: FactorSnapshot[];
  evidence: EvidenceItem[];
  timing: TimingData;
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

interface FormulaSnapshot {
  version: string;
  calibrationProfile: string;
  engineVersions: Record<string, string>;
  inputs: FormulaInputs;
  outputs: FormulaOutputs;
  probability: number;
  factors: FactorSnapshot[];
  evidence: EvidenceItem[];
  timing: TimingData;
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

interface FormulaSnapshot {
  version: string;
  calibrationProfile: string;
  engineVersions: Record<string, string>;
  inputs: FormulaInputs;
  outputs: FormulaOutputs;
  probability: number;
  factors: FactorSnapshot[];
  evidence: EvidenceItem[];
  timing: TimingData;
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

interface FormulaSnapshot {
  version: string;
  calibrationProfile: string;
  engineVersions: Record<string, string>;
  inputs: FormulaInputs;
  outputs: FormulaOutputs;
  probability: number;
  factors: FactorSnapshot[];
  evidence: EvidenceItem[];
  timing: TimingData;
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

interface FormulaSnapshot {
  version: string;
  calibrationProfile: string;
  engineVersions: Record<string, string>;
  inputs: FormulaInputs;
  outputs: FormulaOutputs;
  probability: number;
  factors: FactorSnapshot[];
  evidence: EvidenceItem[];
  timing: TimingData;
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

interface FormulaSnapshot {
  version: string;
  calibrationProfile: string;
  engineVersions: Record<string, string>;
  inputs: FormulaInputs;
  outputs: FormulaOutputs;
  probability: number;
  factors: FactorSnapshot[];
  evidence: EvidenceItem[];
  timing: TimingData;
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

interface FormulaSnapshot {
  version: string;
  calibrationProfile: string;
  engineVersions: Record<string, string>;
  inputs: FormulaInputs;
  outputs: FormulaOutputs;
  probability: number;
  factors: FactorSnapshot[];
  evidence: EvidenceItem[];
  timing: TimingData;
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

interface FormulaSnapshot {
  version: string;
  calibrationProfile: string;
  engineVersions: Record<string, string>;
  inputs: FormulaInputs;
  outputs: FormulaOutputs;
  probability: number;
  factors: FactorSnapshot[];
  evidence: EvidenceItem[];
  timing: TimingData;
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

interface FormulaSnapshot {
  version: string;
  calibrationProfile: string;
  engineVersions: Record<string, string>;
  inputs: FormulaInputs;
  outputs: FormulaOutputs;
  probability: number;
  factors: FactorSnapshot[];
  evidence: EvidenceItem[];
  timing: TimingData;
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

interface FormulaSnapshot {
  version: string;
  calibrationProfile: string;
  engineVersions: Record<string, string>;
  inputs: FormulaInputs;
  outputs: FormulaOutputs;
  probability: number;
  factors: FactorSnapshot[];
  evidence: EvidenceItem[];
  timing: TimingData;
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

interface FormulaSnapshot {
  version: string;
  calibrationProfile: string;
  engineVersions: Record<string, string>;
  inputs: FormulaInputs;
  outputs: FormulaOutputs;
  probability: number;
  factors: FactorSnapshot[];
  evidence: EvidenceItem[];
  timing: TimingData;
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

interface FormulaSnapshot {
  version: string;
  calibrationProfile: string;
  engineVersions: Record<string, string>;
  inputs: FormulaInputs;
  outputs: FormulaOutputs;
  probability: number;
  factors: FactorSnapshot[];
  evidence: EvidenceItem[];
  timing: TimingData;
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

interface FormulaSnapshot {
  version: string;
  calibrationProfile: string;
  engineVersions: Record<string, string>;
  inputs: FormulaInputs;
  outputs: FormulaOutputs;
  probability: number;
  factors: FactorSnapshot[];
  evidence: EvidenceItem[];
  timing: TimingData;
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

interface FormulaSnapshot {
  version: string;
  calibrationProfile: string;
  engineVersions: Record<string, string>;
  inputs: FormulaInputs;
  outputs: FormulaOutputs;
  probability: number;
  factors: FactorSnapshot[];
  evidence: EvidenceItem[];
  timing: TimingData;
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

interface FormulaSnapshot {
  version: string;
  calibrationProfile: string;
  engineVersions: Record<string, string>;
  inputs: FormulaInputs;
  outputs: FormulaOutputs;
  probability: number;
  factors: FactorSnapshot[];
  evidence: EvidenceItem[];
  timing: TimingData;
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

interface FormulaSnapshot {
  version: string;
  calibrationProfile: string;
  engineVersions: Record<string, string>;
  inputs: FormulaInputs;
  outputs: FormulaOutputs;
  probability: number;
  factors: FactorSnapshot[];
  evidence: EvidenceItem[];
  timing: TimingData;
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
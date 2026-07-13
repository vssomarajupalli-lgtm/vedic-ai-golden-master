export interface ImmutableReportGovernance {
  principle: string;
  rules: ImmutableRule[];
  enforcement: EnforcementLevel;
  exceptions: Exception[];
}

interface ImmutableRule {
  id: string;
  description: string;
  scope: 'reports' | 'pdfs' | 'snapshots' | 'version_history' | 'all';
  appliesTo: string[];
  violations: ViolationType[];
}

interface EnforcementLevel {
  level: 'strict' | 'advisory' | 'logged';
  actions: ('block' | 'warn' | 'audit' | 'revert')[];
  requiresApproval: boolean;
}

interface Exception {
  id: string;
  description: string;
  allowedBy: string;
  expiresAt?: Date;
  reason: string;
}

type ViolationType = 
  | 'content_modification'
  | 'formula_override'
  | 'calibration_override'
  | 'decision_override'
  | 'timestamp_tampering'
  | 'checksum_mismatch';

interface Violation {
  ruleId: string;
  type: ViolationType;
  severity: 'critical' | 'high' | 'medium' | 'low';
  detectedAt: Date;
  details: string;
  autoRemediated: boolean;
  remediationAction?: string;
}

export interface ImmutableReportGovernanceState {
  violations: Violation[];
  lastAudit: Date;
  auditResults: AuditResult[];
}

interface AuditResult {
  timestamp: Date;
  reportId: string;
  passed: boolean;
  violations: Violation[];
}

export interface ImmutableReportGovernanceContextType {
  governance: ImmutableReportGovernance;
  state: ImmutableReportGovernanceState;
  validateReport: (reportId: string) => Promise<boolean>;
  validatePDF: (pdfPath: string) => Promise<boolean>;
  validateSnapshot: (snapshotId: string) => Promise<boolean>;
  validateVersionHistory: (historyId: string) => Promise<boolean>;
  reportViolation: (violation: Violation) => void;
  requestException: (exception: Exception) => Promise<boolean>;
}
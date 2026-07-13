import type { ConsultationReport } from './report';

export interface ImmutableReportGovernance {
  principle: string;
  rules: ImmutableRule[];
  enforcement: EnforcementLevel;
  exceptions: Exception[];
}

interface ImmutableRule {
  id: string;
  description: string;
  enforcement: 'hard' | 'soft';
  scope: 'report' | 'pdf' | 'snapshot' | 'version_history';
}

interface EnforcementLevel {
  level: 'hard' | 'soft' | 'advisory';
  automated: boolean;
  auditTrail: boolean;
}

interface Exception {
  condition: string;
  justification: string;
  approvedBy: string;
  expiresAt?: Date;
}

export const IMMUTABLE_REPORT_GOVERNANCE: ImmutableReportGovernance = {
  principle: 'Generated Reports Are Immutable. If formulas, calibration, questions, or decision layer change, previous reports SHALL NEVER change. A completely NEW report shall be generated.',
  rules: [
    {
      id: 'IRG-001',
      description: 'Generated reports shall never be modified after generation',
      enforcement: 'hard',
      scope: 'report',
    },
    {
      id: 'IRG-002',
      description: 'PDF exports are immutable once generated',
      enforcement: 'hard',
      scope: 'pdf',
    },
    {
      id: 'IRG-003',
      description: 'Consultation snapshots are immutable once created',
      enforcement: 'hard',
      scope: 'snapshot',
    },
    {
      id: 'IRG-004',
      description: 'Version history entries are immutable once created',
      enforcement: 'hard',
      scope: 'version_history',
    },
    {
      id: 'IRG-005',
      description: 'If formulas change, previous reports must not change; new report version must be generated',
      enforcement: 'hard',
      scope: 'report',
    },
    {
      id: 'IRG-006',
      description: 'If calibration changes, previous reports must not change; new report version must be generated',
      enforcement: 'hard',
      scope: 'report',
    },
    {
      id: 'IRG-007',
      description: 'If question registry changes, previous reports must not change; new report version must be generated',
      enforcement: 'hard',
      scope: 'report',
    },
    {
      id: 'IRG-008',
      description: 'If decision layer changes, previous reports must not change; new report version must be generated',
      enforcement: 'hard',
      scope: 'report',
    },
  ],
  enforcement: {
    level: 'hard',
    automated: true,
    auditTrail: true,
  },
  exceptions: [],
};

export function validateImmutability(report: ConsultationReport, newVersion: ConsultationReport): ValidationResult {
  const errors: string[] = [];
  
  if (report.metadata.reportId !== newVersion.metadata.reportId) {
    errors.push('Report ID must remain the same for version increments');
  }
  
  if (report.metadata.reportVersion >= newVersion.metadata.reportVersion) {
    errors.push('New version must have higher version number');
  }
  
  return {
    valid: errors.length === 0,
    errors,
  };
}

interface ValidationResult {
  valid: boolean;
  errors: string[];
}
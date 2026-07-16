// BKL-008A.2 — Deterministic Explainability Engine
// Explanation Templates: 5-level explainability (L1-L5)
// Every explanation references: engine, formula, calibration, evidence chain


/**
 * Explanation levels:
 * L1 - Simple: Client-friendly summary, no technical jargon
 * L2 - Professional: Practitioner-level explanation with key metrics
 * L3 - Advanced: Detailed breakdown with subsystem scores
 * L4 - Formula: Full formula transparency with evidence chains
 * L5 - Research: Everything including raw data and calibration constants
 */
export type ExplanationLevel = 'L1' | 'L2' | 'L3' | 'L4' | 'L5';

export interface ExplanationTemplate {
  level: ExplanationLevel;
  name: string;
  description: string;
  /** Sections included at this level */
  sections: ExplanationSection[];
  /** Whether to include formula details */
  includeFormulaDetails: boolean;
  /** Whether to include calibration constants */
  includeCalibrationConstants: boolean;
  /** Whether to include raw data */
  includeRawData: boolean;
  /** Whether to include evidence chains */
  includeEvidenceChains: boolean;
  /** Whether to include AI interpretation */
  includeAIInterpretation: boolean;
  /** Target audience */
  targetAudience: 'client' | 'practitioner' | 'researcher';
}

export interface ExplanationSection {
  id: string;
  title: string;
  /** Content template with {{variables}} */
  template: string;
  /** Required variables for this section */
  requiredVariables: string[];
  /** Sources that must be cited in this section */
  requiredSources: ('engine' | 'formula' | 'calibration')[];
}

export const EXPLANATION_LEVELS: Record<ExplanationLevel, ExplanationTemplate> = {
  L1: {
    level: 'L1',
    name: 'Simple',
    description: 'Client-friendly summary with plain-language explanations',
    sections: [
      {
        id: 'summary',
        title: 'Summary',
        template: 'The consultation for {{clientName}} shows a {{probabilityCategory}} probability of {{domainDescription}}.',
        requiredVariables: ['clientName', 'probabilityCategory', 'domainDescription'],
        requiredSources: ['engine'],
      },
      {
        id: 'key-insight',
        title: 'Key Insight',
        template: 'The most significant finding is {{keyInsight}}, supported by {{supportingEvidence}}.',
        requiredVariables: ['keyInsight', 'supportingEvidence'],
        requiredSources: ['engine'],
      },
      {
        id: 'recommendation',
        title: 'Recommendation',
        template: 'Based on the analysis, {{recommendationText}}.',
        requiredVariables: ['recommendationText'],
        requiredSources: ['engine'],
      },
    ],
    includeFormulaDetails: false,
    includeCalibrationConstants: false,
    includeRawData: false,
    includeEvidenceChains: false,
    includeAIInterpretation: false,
    targetAudience: 'client',
  },
  L2: {
    level: 'L2',
    name: 'Professional',
    description: 'Practitioner-level explanation with key metrics and domain breakdown',
    sections: [
      {
        id: 'summary',
        title: 'Consultation Summary',
        template: '{{clientName}} — {{consultationTitle}} — {{consultationDate}}.\nFinal Probability: {{probabilityValue}}% ({{probabilityCategory}}).\nTransit Activation: {{activationValue}}% — Grade: {{transitGrade}}.',
        requiredVariables: ['clientName', 'consultationTitle', 'consultationDate', 'probabilityValue', 'probabilityCategory', 'activationValue', 'transitGrade'],
        requiredSources: ['engine'],
      },
      {
        id: 'domain-breakdown',
        title: 'Domain Analysis',
        template: '{{domainBreakdown}}',
        requiredVariables: ['domainBreakdown'],
        requiredSources: ['engine', 'formula'],
      },
      {
        id: 'dasha-context',
        title: 'Dasha Period Context',
        template: 'Current Mahadasha: {{md}}. Current Antardasha: {{ad}}.\nDasha influences: {{dashaInfluences}}.',
        requiredVariables: ['md', 'ad', 'dashaInfluences'],
        requiredSources: ['engine'],
      },
      {
        id: 'transit-support',
        title: 'Transit Support Analysis',
        template: 'Transit activation score: {{transitScore}}%.\nSupporting factors: {{supportingFactors}}.\nObstructing factors: {{obstructingFactors}}.\nConfidence flags: {{confidenceFlags}}.',
        requiredVariables: ['transitScore', 'supportingFactors', 'obstructingFactors', 'confidenceFlags'],
        requiredSources: ['engine'],
      },
      {
        id: 'conclusion',
        title: 'Professional Assessment',
        template: '{{professionalAssessment}}',
        requiredVariables: ['professionalAssessment'],
        requiredSources: ['engine', 'formula'],
      },
    ],
    includeFormulaDetails: false,
    includeCalibrationConstants: false,
    includeRawData: false,
    includeEvidenceChains: false,
    includeAIInterpretation: true,
    targetAudience: 'practitioner',
  },
  L3: {
    level: 'L3',
    name: 'Advanced',
    description: 'Detailed breakdown with subsystem scores and formula references',
    sections: [
      {
        id: 'executive-summary',
        title: 'Executive Summary',
        template: '{{executiveSummary}}',
        requiredVariables: ['executiveSummary'],
        requiredSources: ['engine'],
      },
      {
        id: 'subsystem-breakdown',
        title: 'Subsystem Analysis',
        template: '{{subsystemBreakdown}}',
        requiredVariables: ['subsystemBreakdown'],
        requiredSources: ['engine', 'formula'],
      },
      {
        id: 'formula-references',
        title: 'Formula References',
        template: '{{formulaReferences}}',
        requiredVariables: ['formulaReferences'],
        requiredSources: ['formula', 'calibration'],
      },
      {
        id: 'calibration-context',
        title: 'Calibration Context',
        template: 'Calibration Profile: {{calibrationProfile}}.\nKey constants affecting this analysis: {{keyConstants}}.',
        requiredVariables: ['calibrationProfile', 'keyConstants'],
        requiredSources: ['calibration'],
      },
      {
        id: 'confidence-analysis',
        title: 'Confidence Analysis',
        template: '{{confidenceAnalysis}}',
        requiredVariables: ['confidenceAnalysis'],
        requiredSources: ['engine'],
      },
    ],
    includeFormulaDetails: true,
    includeCalibrationConstants: true,
    includeRawData: false,
    includeEvidenceChains: false,
    includeAIInterpretation: true,
    targetAudience: 'practitioner',
  },
  L4: {
    level: 'L4',
    name: 'Formula',
    description: 'Full formula transparency with evidence chains and calibration references',
    sections: [
      {
        id: 'full-analysis',
        title: 'Complete Analysis',
        template: '{{fullAnalysis}}',
        requiredVariables: ['fullAnalysis'],
        requiredSources: ['engine'],
      },
      {
        id: 'formula-evidence',
        title: 'Formula Evidence Chains',
        template: '{{formulaEvidenceChains}}',
        requiredVariables: ['formulaEvidenceChains'],
        requiredSources: ['formula'],
      },
      {
        id: 'calibration-detail',
        title: 'Calibration Detail',
        template: '{{calibrationDetail}}',
        requiredVariables: ['calibrationDetail'],
        requiredSources: ['calibration'],
      },
      {
        id: 'engine-outputs',
        title: 'Engine Output Reference',
        template: '{{engineOutputReference}}',
        requiredVariables: ['engineOutputReference'],
        requiredSources: ['engine'],
      },
      {
        id: 'verification',
        title: 'Verification',
        template: 'All values verified against deterministic engine outputs. Formula Registry v{{formulaVersion}}. Calibration v{{calibrationVersion}}.',
        requiredVariables: ['formulaVersion', 'calibrationVersion'],
        requiredSources: ['formula', 'calibration'],
      },
    ],
    includeFormulaDetails: true,
    includeCalibrationConstants: true,
    includeRawData: true,
    includeEvidenceChains: true,
    includeAIInterpretation: true,
    targetAudience: 'practitioner',
  },
  L5: {
    level: 'L5',
    name: 'Research',
    description: 'Complete research-grade output with all data, formulas, and calibration',
    sections: [
      {
        id: 'research-abstract',
        title: 'Research Abstract',
        template: '{{researchAbstract}}',
        requiredVariables: ['researchAbstract'],
        requiredSources: ['engine'],
      },
      {
        id: 'complete-formula-trace',
        title: 'Complete Formula Trace',
        template: '{{completeFormulaTrace}}',
        requiredVariables: ['completeFormulaTrace'],
        requiredSources: ['formula'],
      },
      {
        id: 'complete-calibration',
        title: 'Complete Calibration Reference',
        template: '{{completeCalibration}}',
        requiredVariables: ['completeCalibration'],
        requiredSources: ['calibration'],
      },
      {
        id: 'raw-engine-outputs',
        title: 'Raw Engine Outputs',
        template: '{{rawEngineOutputs}}',
        requiredVariables: ['rawEngineOutputs'],
        requiredSources: ['engine'],
      },
      {
        id: 'evidence-chain',
        title: 'Complete Evidence Chain',
        template: '{{completeEvidenceChain}}',
        requiredVariables: ['completeEvidenceChain'],
        requiredSources: ['formula', 'calibration'],
      },
      {
        id: 'methodology',
        title: 'Methodology',
        template: '{{methodology}}',
        requiredVariables: ['methodology'],
        requiredSources: ['engine', 'formula', 'calibration'],
      },
    ],
    includeFormulaDetails: true,
    includeCalibrationConstants: true,
    includeRawData: true,
    includeEvidenceChains: true,
    includeAIInterpretation: true,
    targetAudience: 'researcher',
  },
};

export function getExplanationLevel(level: ExplanationLevel): ExplanationTemplate {
  return EXPLANATION_LEVELS[level];
}

export function getLevelLabel(level: ExplanationLevel): string {
  return `${level} — ${EXPLANATION_LEVELS[level].name}`;
}
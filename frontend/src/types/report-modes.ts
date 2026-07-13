export type ReportMode = 'standard' | 'professional' | 'expert' | 'study';

export interface ModeConfiguration {
  mode: ReportMode;
  label: string;
  description: string;
  defaultFor: 'self-user' | 'professional-astrologer' | 'researcher' | 'student';
  
  emphasis: {
    comparison: boolean;
    timelineComparison: boolean;
    formulaComparison: boolean;
    calibrationComparison: boolean;
    transitComparison: boolean;
    reportComparison: boolean;
    learningAnnotations: boolean;
    sideBySideDefault: boolean;
  };
  
  showExecutiveSummary: boolean;
  showSimpleExplanation: boolean;
  showRecommendations: boolean;
  showProbability: boolean;
  showFormulaIds: boolean;
  showTiming: boolean;
  showDasha: boolean;
  showGocharaStrength: boolean;
  showEvidenceSummary: boolean;
  showAshtakavarga: boolean;
  showShadbala: boolean;
  showVargaInformation: boolean;
  showFullFormulaMetadata: boolean;
  showCalibrationMetadata: boolean;
  showTimingBreakdown: boolean;
  showDeterministicEvidence: boolean;
  showFormulaTransparency: boolean;
  showCalibrationTransparency: boolean;
  showFormulaComparison: boolean;
  showExpertPanels: boolean;
  enableFormulaComparison: boolean;
  enableRawDataExport: boolean;
}

export const MODE_CONFIGS: Record<ReportMode, ModeConfiguration> = {
  standard: {
    mode: 'standard',
    label: 'Standard',
    description: 'Clean narrative for personal use',
    defaultFor: 'self-user',
    emphasis: { comparison: false, timelineComparison: false, formulaComparison: false, calibrationComparison: false, transitComparison: false, reportComparison: false, learningAnnotations: false, sideBySideDefault: false },
    showExecutiveSummary: true, showSimpleExplanation: true, showRecommendations: true,
    showProbability: false, showFormulaIds: false, showTiming: false,
    showDasha: false, showGocharaStrength: false, showEvidenceSummary: false,
    showAshtakavarga: false, showShadbala: false, showVargaInformation: false,
    showFullFormulaMetadata: false, showCalibrationMetadata: false,
    showTimingBreakdown: false, showDeterministicEvidence: false,
    showFormulaTransparency: false, showCalibrationTransparency: false,
    showFormulaComparison: false, showExpertPanels: false,
    enableFormulaComparison: false, enableRawDataExport: false,
  },
  professional: {
    mode: 'professional',
    label: 'Professional',
    description: 'Complete consultation for client delivery',
    defaultFor: 'professional-astrologer',
    emphasis: { comparison: false, timelineComparison: false, formulaComparison: false, calibrationComparison: false, transitComparison: false, reportComparison: false, learningAnnotations: false, sideBySideDefault: false },
    showExecutiveSummary: true, showSimpleExplanation: true, showRecommendations: true,
    showProbability: true, showFormulaIds: true, showTiming: true,
    showDasha: true, showGocharaStrength: true, showEvidenceSummary: true,
    showAshtakavarga: false, showShadbala: false, showVargaInformation: false,
    showFullFormulaMetadata: false, showCalibrationMetadata: true,
    showTimingBreakdown: true, showDeterministicEvidence: true,
    showFormulaTransparency: true, showCalibrationTransparency: true,
    showFormulaComparison: false, showExpertPanels: true,
    enableFormulaComparison: false, enableRawDataExport: false,
  },
  expert: {
    mode: 'expert',
    label: 'Expert',
    description: 'Full deterministic transparency for research & calibration',
    defaultFor: 'researcher',
    emphasis: { comparison: false, timelineComparison: false, formulaComparison: false, calibrationComparison: false, transitComparison: false, reportComparison: false, learningAnnotations: false, sideBySideDefault: false },
    showExecutiveSummary: true, showSimpleExplanation: true, showRecommendations: true,
    showProbability: true, showFormulaIds: true, showTiming: true,
    showDasha: true, showGocharaStrength: true, showEvidenceSummary: true,
    showAshtakavarga: true, showShadbala: true, showVargaInformation: true,
    showFullFormulaMetadata: true, showCalibrationMetadata: true,
    showTimingBreakdown: true, showDeterministicEvidence: true,
    showFormulaTransparency: true, showCalibrationTransparency: true,
    showFormulaComparison: true, showExpertPanels: true,
    enableFormulaComparison: true, enableRawDataExport: true,
  },
  study: {
    mode: 'study',
    label: 'Study',
    description: 'Learning, research, and comparative analysis mode',
    defaultFor: 'student',
    emphasis: { comparison: true, timelineComparison: true, formulaComparison: true, calibrationComparison: true, transitComparison: true, reportComparison: true, learningAnnotations: true, sideBySideDefault: true },
    showExecutiveSummary: true, showSimpleExplanation: true, showRecommendations: true,
    showProbability: true, showFormulaIds: true, showTiming: true,
    showDasha: true, showGocharaStrength: true, showEvidenceSummary: true,
    showAshtakavarga: true, showShadbala: true, showVargaInformation: true,
    showFullFormulaMetadata: false, showCalibrationMetadata: true,
    showTimingBreakdown: true, showDeterministicEvidence: true,
    showFormulaTransparency: true, showCalibrationTransparency: true,
    showFormulaComparison: true, showExpertPanels: true,
    enableFormulaComparison: true, enableRawDataExport: false,
  },
};

export function getModeConfig(mode: ReportMode): ModeConfiguration {
  return MODE_CONFIGS[mode];
}
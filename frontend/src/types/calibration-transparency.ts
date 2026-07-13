export interface CalibrationTransparencyData {
  calibrationProfile: string;
  calibrationVersion: string;
  calibrationDate: Date;
  profileStatus: 'default' | 'current' | 'frozen' | 'custom';
  profileDescription: string;
  totalFormulas: number;
  totalFactors: number;
  confidenceClassification: {
    overall: 'high' | 'moderate' | 'low';
    byDomain: Record<string, 'high' | 'moderate' | 'low'>;
    factors: ConfidenceFactor[];
  };
  parameterProfile: {
    profileId: string;
    planetStrengthWeights: Record<string, number>;
    bhavaStrengthWeights: Record<string, number>;
    gocharaWeights: Record<string, number>;
    formulaPercentages: Record<string, number>;
    thresholds: Record<string, number>;
  };
  validationStatus: 'validated' | 'pending' | 'failed';
  validatedAt?: Date;
  validatedBy?: string;
  sourceCommit: string;
  generatedBy: string;
}

interface ConfidenceFactor {
  factor: string;
  status: 'validated' | 'estimated' | 'default';
  confidence: 'high' | 'moderate' | 'low';
  notes?: string;
}

export interface CalibrationTransparencyPanelProps {
  calibrationProfile: string;
  mode: 'professional' | 'expert';
  onClose: () => void;
}
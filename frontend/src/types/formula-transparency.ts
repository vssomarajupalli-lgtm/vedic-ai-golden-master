export interface FormulaTransparencyData {
  formulaId: string;
  formulaVersion: string;
  formulaName: string;
  formulaType: 'base' | 'child';
  parentFormulaId?: string;
  primaryFormula: string;
  supportingFormulas: string[];
  decisionLayerVersion: string;
  decisionLayerAlgorithm: string;
  formulaRegistryVersion: string;
  questionCatalogVersion: string;
  executedAt: Date;
  executionTimeMs: number;
  engineOutputsUsed: string[];
  factors: FormulaFactorTransparency[];
}

interface FormulaFactorTransparency {
  factorId: string;
  factorName: string;
  weightPct: number;
  enabled: boolean;
  engineRequired: string[];
  rawValue: number;
  normalizedValue: number;
  contribution: number;
}

export interface FormulaTransparencyPanelProps {
  formulaId: string;
  mode: 'professional' | 'expert';
  onClose: () => void;
}
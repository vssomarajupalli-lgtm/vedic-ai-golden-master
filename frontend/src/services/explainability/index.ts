// BKL-008A.2 — Deterministic Explainability Engine
// Barrel Export: All explainability services

export { ExplanationService } from './explanationService';
export type { ExplanationRequest, ExplanationResult, ExplanationResultSection } from './explanationService';

export { EXPLANATION_LEVELS, getExplanationLevel, getLevelLabel } from './explanationTemplates';
export type { ExplanationLevel, ExplanationTemplate, ExplanationSection } from './explanationTemplates';

export { EvidenceCollector } from './evidenceCollector';
export type { EvidenceCollection, FormulaReference, CalibrationReference, EngineReference, EvidenceChainEntry } from './evidenceCollector';

export { SourceAttributionGenerator } from './sourceAttributionGenerator';
export type { SourceAttribution } from './sourceAttributionGenerator';
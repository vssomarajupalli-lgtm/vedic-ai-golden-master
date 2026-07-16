// BKL-008A.3 — Deterministic Q&A Engine
// Barrel Export

export { QAService } from './qaService';
export type { QARequest, QAResponse } from './qaService';

export { QuestionClassifier } from './questionClassifier';
export type { ClassifiedQuestion, QuestionClass, IntentMapping } from './questionClassifier';

export { DeterministicEvidenceRetriever } from './evidenceRetriever';
export type { EvidenceBundle, AnswerContext, FormulaEvidence, CalibrationEvidence } from './evidenceRetriever';

export { AnswerGenerator } from './answerGenerator';
export type { StructuredAnswer, AnswerSection, Citation } from './answerGenerator';
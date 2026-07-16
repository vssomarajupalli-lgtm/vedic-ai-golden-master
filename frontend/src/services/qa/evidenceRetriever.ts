// BKL-008A.3 — Deterministic Q&A Engine
// Deterministic Evidence Retriever + Context Builder
// Retrieves relevant evidence from engine outputs; builds answer context

import type { ClassifiedQuestion, QuestionClass } from './questionClassifier';
import { QuestionClassifier } from './questionClassifier';
import { SourceAttributionGenerator } from '../explainability/sourceAttributionGenerator';
import type { SourceAttribution } from '../explainability/sourceAttributionGenerator';

export interface EvidenceBundle {
  /** The question this evidence answers */
  question: ClassifiedQuestion;
  /** Engine outputs relevant to this question */
  engineOutputs: Record<string, unknown>;
  /** Formula references relevant */
  formulaReferences: FormulaEvidence[];
  /** Calibration references relevant */
  calibrationReferences: CalibrationEvidence[];
  /** Source attributions */
  attributions: SourceAttribution[];
  /** Whether sufficient evidence was found */
  hasSufficientEvidence: boolean;
  /** If insufficient, explanation */
  evidenceGapReason?: string;
}

export interface FormulaEvidence {
  formulaId: string;
  name: string;
  domain: string;
  relevance: 'direct' | 'related' | 'contextual';
  evidenceText: string;
}

export interface CalibrationEvidence {
  constantId: string;
  name: string;
  value: number;
  relevance: 'direct' | 'related' | 'contextual';
  description: string;
}

export interface AnswerContext {
  /** The question being answered */
  question: ClassifiedQuestion;
  /** Evidence bundle */
  evidence: EvidenceBundle;
  /** Suggested follow-up questions */
  followUpQuestions: string[];
  /** Confidence in the answer (0-1) */
  confidence: number;
  /** Answer template key */
  answerTemplate: string;
  /** Variables for the answer template */
  templateVariables: Record<string, string>;
}

export class DeterministicEvidenceRetriever {
  /**
   * Retrieve evidence for a classified question from engine outputs.
   */
  static retrieveEvidence(
    question: ClassifiedQuestion,
    allEngineOutputs: Record<string, unknown> | null,
  ): EvidenceBundle {
    const outputs = allEngineOutputs || {};
    const intent = QuestionClassifier.getIntent(question.questionClass);
    const attributions: SourceAttribution[] = [];
    const formulaEvidence: FormulaEvidence[] = [];
    const calibrationEvidence: CalibrationEvidence[] = [];

    if (!intent) {
      return {
        question,
        engineOutputs: {},
        formulaReferences: [],
        calibrationReferences: [],
        attributions: [],
        hasSufficientEvidence: false,
        evidenceGapReason: 'No intent mapping found for this question class.',
      };
    }

    // Collect engine outputs
    const relevantOutputs: Record<string, unknown> = {};
    for (const key of intent.requiredEngineOutputs) {
      if (key in outputs) {
        relevantOutputs[key] = outputs[key];
        const attr = SourceAttributionGenerator.engine(
          DeterministicEvidenceRetriever.getEngineName(key),
          '1.0',
          `Provides data for ${question.questionClass} questions`,
        );
        attributions.push(attr);
      }
    }

    // Collect formula evidence
    for (const domain of intent.requiredFormulaDomains) {
      const formulas = DeterministicEvidenceRetriever.getFormulasForDomain(domain);
      formulaEvidence.push(...formulas);
      for (const f of formulas) {
        const attr = SourceAttributionGenerator.formula(f.formulaId, '1.0', `${f.domain}: ${f.name}`);
        attributions.push(attr);
      }
    }

    // Collect calibration evidence
    const calibrations = DeterministicEvidenceRetriever.getCalibrationsForQuestion(question);
    calibrationEvidence.push(...calibrations);
    for (const c of calibrations) {
      const attr = SourceAttributionGenerator.calibration(
        'standard',
        'v1.0.0',
        `${c.constantId} = ${c.value}`,
      );
      attributions.push(attr);
    }

    const hasSufficient = Object.keys(relevantOutputs).length > 0;

    return {
      question,
      engineOutputs: relevantOutputs,
      formulaReferences: formulaEvidence,
      calibrationReferences: calibrationEvidence,
      attributions,
      hasSufficientEvidence: hasSufficient,
      evidenceGapReason: hasSufficient ? undefined : 'No matching engine outputs found for this question.',
    };
  }

  /**
   * Build answer context from evidence.
   */
  static buildContext(evidence: EvidenceBundle, consultationId: string): AnswerContext {
    const question = evidence.question;
    const followUps = QuestionClassifier.getFollowUpQuestions(question.questionClass, question.entities);

    // Calculate confidence based on evidence sufficiency
    let confidence = evidence.hasSufficientEvidence ? 0.8 : 0.3;
    if (question.confidence > 0.7) confidence = Math.min(confidence + 0.1, 1.0);

    // Build template variables
    const templateVariables: Record<string, string> = {
      question: question.rawQuestion,
      questionClass: question.questionClass,
      entities: question.entities.join(', ') || 'none',
      engineCount: String(Object.keys(evidence.engineOutputs).length),
      formulaCount: String(evidence.formulaReferences.length),
      calibrationCount: String(evidence.calibrationReferences.length),
      consultationId: consultationId.substring(0, 8),
      answerConfidence: String(Math.round(confidence * 100)),
    };

    // Add engine-specific data
    for (const [key, value] of Object.entries(evidence.engineOutputs)) {
      if (value && typeof value === 'object') {
        templateVariables[`engine_${key}`] = DeterministicEvidenceRetriever.formatEngineOutput(key, value);
      }
    }

    return {
      question,
      evidence,
      followUpQuestions: followUps,
      confidence,
      answerTemplate: DeterministicEvidenceRetriever.getAnswerTemplate(question.questionClass),
      templateVariables,
    };
  }

  public static getEngineName(key: string): string {
    const names: Record<string, string> = {
      planetStrength: 'PlanetStrengthEngine',
      bhavaStrength: 'BhavaStrengthEngine',
      dashaOutput: 'DashaEngine',
      transitOutput: 'TransitEngine',
      probabilityOutput: 'MasterProbabilityEngine',
      pipelineOutput: 'PipelineRunner',
    };
    return names[key] || key;
  }

  private static getFormulasForDomain(domain: string): FormulaEvidence[] {
    if (domain === 'All') {
      return [
        { formulaId: 'TRN-HA-001', name: 'House Activation', domain: 'Transit', relevance: 'contextual', evidenceText: 'Measures house activation from transit' },
        { formulaId: 'PLN-DG-001', name: 'Dignity Score', domain: 'Planet Strength', relevance: 'contextual', evidenceText: 'Calculates planetary dignity' },
        { formulaId: 'PRB-AG-001', name: 'Probability Aggregation', domain: 'Probability', relevance: 'contextual', evidenceText: 'Aggregates subsystem scores' },
      ];
    }

    const domainFormulas: Record<string, FormulaEvidence[]> = {
      'Planet Strength': [
        { formulaId: 'PLN-DG-001', name: 'Dignity Score', domain: 'Planet Strength', relevance: 'direct', evidenceText: 'Determines planetary dignity from sign placement' },
        { formulaId: 'PLN-HP-001', name: 'House Placement', domain: 'Planet Strength', relevance: 'direct', evidenceText: 'Evaluates house placement strength' },
      ],
      'House Strength': [
        { formulaId: 'BHV-HS-001', name: 'House Strength', domain: 'House Strength', relevance: 'direct', evidenceText: 'Evaluates bhava strength from occupant planets' },
      ],
      'Transit': [
        { formulaId: 'TRN-HA-001', name: 'House Activation', domain: 'Transit', relevance: 'direct', evidenceText: '30% weight — House activation from transit planets' },
        { formulaId: 'TRN-BV-001', name: 'BAV Support', domain: 'Transit', relevance: 'direct', evidenceText: '20% weight — Ashtakavarga support' },
        { formulaId: 'TRN-PA-001', name: 'Planet Activation', domain: 'Transit', relevance: 'direct', evidenceText: '20% weight — Planet activation strength' },
        { formulaId: 'TRN-DS-001', name: 'Dasha Sync', domain: 'Transit', relevance: 'direct', evidenceText: '20% weight — Dasha synchronization' },
        { formulaId: 'TRN-VD-001', name: 'Vedha Layer', domain: 'Transit', relevance: 'direct', evidenceText: '10% weight — Vedha obstruction layer' },
      ],
      'Dasha': [
        { formulaId: 'DSH-PR-001', name: 'Dasha Period', domain: 'Dasha', relevance: 'direct', evidenceText: 'Calculates dasha period from Vimshottari' },
      ],
      'Probability': [
        { formulaId: 'PRB-AG-001', name: 'Probability Aggregation', domain: 'Probability', relevance: 'direct', evidenceText: 'Aggregates all subsystem scores into final probability' },
      ],
      'Yoga': [
        { formulaId: 'YOG-DT-001', name: 'Yoga Detection', domain: 'Yoga', relevance: 'direct', evidenceText: 'Detects planetary combinations (yogas)' },
      ],
    };

    return domainFormulas[domain] || [];
  }

  private static getCalibrationsForQuestion(question: ClassifiedQuestion): CalibrationEvidence[] {
    const all: CalibrationEvidence[] = [
      { constantId: 'own_sign', name: 'Own Sign', value: 80, relevance: 'contextual', description: 'Planet in own sign gets 80% strength' },
      { constantId: 'friendly', name: 'Friendly', value: 60, relevance: 'contextual', description: 'Planet in friendly sign gets 60% strength' },
      { constantId: 'neutral', name: 'Neutral', value: 50, relevance: 'contextual', description: 'Planet in neutral sign gets 50% strength' },
      { constantId: 'enemy', name: 'Enemy', value: 40, relevance: 'contextual', description: 'Planet in enemy sign gets 40% strength' },
      { constantId: 'debilitated', name: 'Debilitated', value: 20, relevance: 'contextual', description: 'Planet in debilitated sign gets 20% strength' },
    ];

    if (question.questionClass === 'calibration') {
      all.forEach(c => (c.relevance = 'direct'));
    }

    return all;
  }

  private static formatEngineOutput(_key: string, value: unknown): string {
    if (value === null || value === undefined) return 'No data';
    if (typeof value === 'string') return value;
    if (typeof value === 'number') return String(value);
    return JSON.stringify(value, null, 2);
  }

  private static getAnswerTemplate(questionClass: QuestionClass): string {
    const templates: Partial<Record<QuestionClass, string>> = {
      planet: 'planet_strength',
      house: 'house_strength',
      dasha: 'dasha_period',
      transit: 'transit_analysis',
      probability: 'probability_score',
      formula: 'formula_explanation',
      calibration: 'calibration_info',
      recommendation: 'recommendation',
      general: 'general_explanation',
      unsupported: 'unsupported',
    };
    return templates[questionClass] || 'general_explanation';
  }
}
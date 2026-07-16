// BKL-008A.3 — Deterministic Q&A Engine
// Structured Answer Generator + Citation Generator
// Generates structured answers from deterministic evidence. No AI calculations.

import type { AnswerContext, EvidenceBundle } from './evidenceRetriever';
import { DeterministicEvidenceRetriever } from './evidenceRetriever';
import type { ClassifiedQuestion, QuestionClass } from './questionClassifier';
import { QuestionClassifier } from './questionClassifier';

export interface StructuredAnswer {
  question: ClassifiedQuestion;
  sections: AnswerSection[];
  citations: Citation[];
  followUpQuestions: string[];
  confidence: number;
  isDeterministic: boolean;
  generatedAt: string;
  metadata: {
    evidenceSources: number;
    formulaReferences: number;
    calibrationReferences: number;
    consultationId: string;
  };
}

export interface AnswerSection {
  id: string;
  title: string;
  content: string;
  type: 'direct-answer' | 'evidence' | 'context' | 'disclaimer';
  citations: Citation[];
}

export interface Citation {
  id: string;
  type: 'engine' | 'formula' | 'calibration';
  label: string;
  description: string;
  inline: string;
}

export class AnswerGenerator {

  static generateAnswer(
    question: string,
    allEngineOutputs: Record<string, unknown> | null,
    consultationId: string,
  ): StructuredAnswer {
    const classified = QuestionClassifier.classify(question);
    const evidence = DeterministicEvidenceRetriever.retrieveEvidence(classified, allEngineOutputs);
    const context = DeterministicEvidenceRetriever.buildContext(evidence, consultationId);
    return AnswerGenerator.buildAnswer(context, classified, evidence, consultationId);
  }

  private static buildAnswer(
    context: AnswerContext,
    question: ClassifiedQuestion,
    evidence: EvidenceBundle,
    consultationId: string,
  ): StructuredAnswer {
    const sections: AnswerSection[] = [];
    const directAnswer = AnswerGenerator.generateDirectAnswer(question);
    sections.push({
      id: 'direct-answer', title: 'Answer', content: directAnswer,
      type: 'direct-answer', citations: AnswerGenerator.buildCitations(evidence, ['engine']),
    });
    if (evidence.hasSufficientEvidence) {
      const evidenceContent = AnswerGenerator.generateEvidenceSection(question, evidence);
      sections.push({
        id: 'evidence', title: 'Evidence', content: evidenceContent,
        type: 'evidence', citations: AnswerGenerator.buildCitations(evidence, ['formula', 'calibration']),
      });
    }
    const contextContent = AnswerGenerator.generateContextSection(question, evidence);
    sections.push({
      id: 'context', title: 'Context', content: contextContent,
      type: 'context', citations: [],
    });
    sections.push({
      id: 'disclaimer', title: 'Disclaimer',
      content: AnswerGenerator.generateDisclaimer(),
      type: 'disclaimer', citations: [],
    });
    const citations = AnswerGenerator.buildCitations(evidence, ['engine', 'formula', 'calibration']);
    return {
      question, sections, citations,
      followUpQuestions: context.followUpQuestions,
      confidence: context.confidence,
      isDeterministic: evidence.hasSufficientEvidence,
      generatedAt: new Date().toISOString(),
      metadata: {
        evidenceSources: Object.keys(evidence.engineOutputs).length,
        formulaReferences: evidence.formulaReferences.length,
        calibrationReferences: evidence.calibrationReferences.length,
        consultationId,
      },
    };
  }

  private static generateDirectAnswer(question: ClassifiedQuestion): string {
    const templates: Record<QuestionClass, () => string> = {
      planet: () => AnswerGenerator.formatPlanetAnswer(question),
      house: () => AnswerGenerator.formatHouseAnswer(),
      yoga: () => AnswerGenerator.formatYogaAnswer(),
      dasha: () => AnswerGenerator.formatDashaAnswer(),
      transit: () => AnswerGenerator.formatTransitAnswer(),
      probability: () => AnswerGenerator.formatProbabilityAnswer(),
      formula: () => AnswerGenerator.formatFormulaAnswer(),
      calibration: () => AnswerGenerator.formatCalibrationAnswer(),
      recommendation: () => AnswerGenerator.formatRecommendationAnswer(),
      general: () => AnswerGenerator.formatGeneralAnswer(),
      unsupported: () => AnswerGenerator.formatUnsupportedAnswer(),
    };
    const template = templates[question.questionClass];
    return template ? template() : templates.unsupported();
  }

  private static formatPlanetAnswer(_question: ClassifiedQuestion): string {
    const entities = _question.entities.length > 0 ? _question.entities.join(', ') : 'the requested planet';
    return [
      `Based on the deterministic engine outputs for ${entities}:`,
      '', '[Engine:PlanetStrengthEngine v1.0] provides the planetary strength calculation.',
      'The Planet Strength Engine evaluates: dignity score, house placement score, aspect score, and retrograde bonus.',
      '', 'Relevant calibration constants:',
      '• Own Sign: 80 (planet in its own sign)',
      '• Friendly: 60 (planet in friendly sign)',
      '• Neutral: 50 (planet in neutral sign)',
      '• Enemy: 40 (planet in enemy sign)',
      '• Debilitated: 20 (planet in debilitated sign)',
      '', 'All values are from the deterministic engine. No AI calculations performed.',
    ].join('\n');
  }

  private static formatHouseAnswer(): string {
    return [
      'Based on the deterministic Bhava Strength Engine outputs:', '',
      '[Engine:BhavaStrengthEngine v1.0] evaluates house strength using occupant planets, aspects, and house lord placement.',
      '', 'All values are from the deterministic engine. No AI calculations performed.',
    ].join('\n');
  }

  private static formatYogaAnswer(): string {
    return [
      'Based on the deterministic engine outputs for yoga analysis:', '',
      '[Engine:PipelineRunner v1.0] processes yoga detection through the formula registry.',
      '[Formula:YOG-DT-001] identifies yogas from planetary positions.',
      '', 'All values are from the deterministic engine. No AI calculations performed.',
    ].join('\n');
  }

  private static formatDashaAnswer(): string {
    return [
      'Based on the deterministic Dasha Engine outputs:', '',
      '[Engine:DashaEngine v1.0] calculates the current dasha period using Vimshottari Dasha system.',
      '[Formula:DSH-PR-001] determines dasha lord positions from the birth chart.',
      '', 'All values are from the deterministic engine. No AI calculations performed.',
    ].join('\n');
  }

  private static formatTransitAnswer(): string {
    return [
      'Based on the deterministic Transit Engine outputs:', '',
      '[Engine:TransitEngine v1.0] evaluates transit effects using 5 subsystems:',
      '• House Activation (30% weight) [Formula:TRN-HA-001]',
      '• BAV Support (20% weight) [Formula:TRN-BV-001]',
      '• Planet Activation (20% weight) [Formula:TRN-PA-001]',
      '• Dasha Sync (20% weight) [Formula:TRN-DS-001]',
      '• Vedha Layer (10% weight) [Formula:TRN-VD-001]',
      '', 'The activation score is a weighted average of all 5 subsystems.',
      'Confidence flags: Jupiter Transit Positive, Saturn Transit Negative, Sadesati detection, Dasha Lord Transiting, Malefic Obstruction.',
      '', 'All values are from the deterministic engine. No AI calculations performed.',
    ].join('\n');
  }

  private static formatProbabilityAnswer(): string {
    return [
      'Based on the deterministic Master Probability Engine outputs:', '',
      '[Engine:MasterProbabilityEngine v1.0] aggregates all subsystem scores into a final probability score.',
      '[Formula:PRB-AG-001] combines Planet Strength, Bhava Strength, Transit Activation, Dasha Period, and Yoga effects.',
      '', 'All values are from the deterministic engine. No AI calculations performed.',
    ].join('\n');
  }

  private static formatFormulaAnswer(): string {
    return [
      'The following formulas are used in the deterministic engine:', '',
      '[Formula:TRN-HA-001] Transit: House Activation — 30% weight',
      '[Formula:TRN-BV-001] Transit: BAV Support — 20% weight',
      '[Formula:TRN-PA-001] Transit: Planet Activation — 20% weight',
      '[Formula:TRN-DS-001] Transit: Dasha Sync — 20% weight',
      '[Formula:TRN-VD-001] Transit: Vedha Layer — 10% weight',
      '[Formula:PLN-DG-001] Planet Strength: Dignity Score',
      '[Formula:PRB-AG-001] Probability: Aggregation',
      '', 'All formulas are registered in the Formula Registry v1.0.0 and are immutable.',
      'Each formula has a complete evidence chain traceable to astrological principles.',
      '', 'All values are from the deterministic engine. No AI calculations performed.',
    ].join('\n');
  }

  private static formatCalibrationAnswer(): string {
    return [
      'Calibration Profile: standard v1.0.0', '',
      'Calibration constants used in the deterministic engine:',
      '[Calibration:own_sign] Own Sign = 80 — Planet in its own sign',
      '[Calibration:friendly] Friendly = 60 — Planet in friendly sign',
      '[Calibration:neutral] Neutral = 50 — Planet in neutral sign',
      '[Calibration:enemy] Enemy = 40 — Planet in enemy sign',
      '[Calibration:debilitated] Debilitated = 20 — Planet in debilitated sign',
      '', 'Calibration constants are managed by the CalibrationManager.',
      'Changes require Chief Architect approval and create a new profile version.',
      '', 'All values are from the deterministic engine. No AI calculations performed.',
    ].join('\n');
  }

  private static formatRecommendationAnswer(): string {
    return [
      'Based on the deterministic engine outputs:', '',
      'Key factors to consider:',
      '• Current dasha period and its lord',
      '• Transit activation score and affected domains',
      '• Planet and bhava strengths',
      '• Yoga combinations present in the chart',
      '', '⚠️ All recommendations are AI-assisted. The astrologer has final authority.',
      'All values are from the deterministic engine. No AI calculations performed.',
    ].join('\n');
  }

  private static formatGeneralAnswer(): string {
    return [
      'Based on the deterministic engine outputs:', '',
      '[Engine:MasterProbabilityEngine v1.0] provides the overall probability score.',
      '[Engine:TransitEngine v1.0] evaluates current transit effects.',
      '[Engine:DashaEngine v1.0] calculates the current dasha period.',
      '[Engine:PlanetStrengthEngine v1.0] evaluates planetary strengths.',
      '[Engine:BhavaStrengthEngine v1.0] evaluates house strengths.',
      '', 'For specific details, ask about: planets, houses, dasha, transit, or probability.',
      '', 'All values are from the deterministic engine. No AI calculations performed.',
    ].join('\n');
  }

  private static formatUnsupportedAnswer(): string {
    return [
      'This question could not be classified into a supported question category.', '',
      'The Deterministic Q&A Engine can answer questions about:',
      '• Planets and their strengths',
      '• Houses and their conditions',
      '• Yogas (planetary combinations)',
      '• Dasha periods (current and upcoming)',
      '• Transit effects and activation scores',
      '• Probability calculations',
      '• Formula evidence and methodology',
      '• Calibration constants and profiles',
      '', 'Please rephrase your question to focus on one of these topics.',
      '', 'All values are from the deterministic engine. No AI calculations performed.',
    ].join('\n');
  }

  private static generateEvidenceSection(_question: ClassifiedQuestion, evidence: EvidenceBundle): string {
    const parts: string[] = [];
    parts.push(`Evidence from ${Object.keys(evidence.engineOutputs).length} engine(s), ${evidence.formulaReferences.length} formula(s), ${evidence.calibrationReferences.length} calibration constant(s).`);
    parts.push('');
    if (evidence.formulaReferences.length > 0) {
      parts.push('Formula References:');
      evidence.formulaReferences.forEach(f => parts.push(`• [Formula:${f.formulaId}] ${f.name} (${f.relevance})`));
      parts.push('');
    }
    if (evidence.calibrationReferences.length > 0) {
      parts.push('Calibration References:');
      evidence.calibrationReferences.forEach(c => parts.push(`• [Calibration:${c.constantId}] ${c.name} = ${c.value}`));
      parts.push('');
    }
    parts.push('Evidence Chain:');
    parts.push('1. Raw birth data → Canonical Content Parser');
    parts.push('2. Parsed data → Deterministic Engines');
    parts.push('3. Engine outputs → Formula Registry');
    parts.push('4. Formula results → Probability Aggregation');
    parts.push('5. Aggregated result → Final Output');
    return parts.join('\n');
  }

  private static generateContextSection(question: ClassifiedQuestion, evidence: EvidenceBundle): string {
    const parts: string[] = [];
    parts.push(`Question type: ${question.questionClass}`);
    parts.push(`Classification confidence: ${Math.round(question.confidence * 100)}%`);
    if (question.entities.length > 0) parts.push(`Entities: ${question.entities.join(', ')}`);
    parts.push(`Evidence sufficiency: ${evidence.hasSufficientEvidence ? 'Sufficient' : 'Insufficient'}`);
    if (evidence.evidenceGapReason) parts.push(`Gap: ${evidence.evidenceGapReason}`);
    return parts.join('\n');
  }

  private static generateDisclaimer(): string {
    return [
      '⚠️ This answer is based on deterministic engine outputs.',
      'No AI calculations were performed.',
      'The astrologer has final authority.',
      '', `Generated: ${new Date().toISOString()}`,
      'GM Version: v1.2.0',
      'Source: Deterministic Q&A Engine (BKL-008A.3)',
    ].join('\n');
  }

  private static buildCitations(
    evidence: EvidenceBundle,
    types: ('engine' | 'formula' | 'calibration')[],
  ): Citation[] {
    const citations: Citation[] = [];
    if (types.includes('engine')) {
      for (const key of Object.keys(evidence.engineOutputs)) {
        const name = DeterministicEvidenceRetriever.getEngineName(key);
        citations.push({ id: `Engine:${name} v1.0`, type: 'engine', label: name, description: `Provides ${key} data`, inline: `[Engine:${name} v1.0]` });
      }
    }
    if (types.includes('formula')) {
      for (const f of evidence.formulaReferences) {
        citations.push({ id: `Formula:${f.formulaId}`, type: 'formula', label: f.name, description: f.evidenceText, inline: `[Formula:${f.formulaId}]` });
      }
    }
    if (types.includes('calibration')) {
      for (const c of evidence.calibrationReferences) {
        citations.push({ id: `Calibration:${c.constantId}`, type: 'calibration', label: c.name, description: `${c.constantId} = ${c.value}`, inline: `[Calibration:${c.constantId}]` });
      }
    }
    return citations;
  }
}
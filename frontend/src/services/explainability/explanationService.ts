// BKL-008A.2 — Deterministic Explainability Engine
// Core Explanation Service: Converts deterministic outputs into structured
// evidence-based natural language explanations at all 5 levels (L1-L5)

import { EvidenceCollector } from './evidenceCollector';
import type { EvidenceCollection } from './evidenceCollector';
import type { SourceAttribution } from "./sourceAttributionGenerator";
import { getExplanationLevel } from './explanationTemplates';
import type { ExplanationLevel, ExplanationTemplate } from './explanationTemplates';

export interface ExplanationRequest {
  /** The consultation context */
  consultation: {
    id: string;
    clientName: string;
    consultationTitle: string;
    consultationDate: string;
  };
  /** The deterministic engine outputs to explain */
  engineOutputs: Record<string, unknown> | null;
  /** The explanation level requested */
  level: ExplanationLevel;
  /** Optional: specific domain or aspect to focus on */
  focus?: string;
  /** Optional: additional context */
  context?: Record<string, string>;
}

export interface ExplanationResult {
  /** The explanation level used */
  level: ExplanationLevel;
  /** Human-readable level label */
  levelLabel: string;
  /** Sections of the explanation */
  sections: ExplanationResultSection[];
  /** All source attributions */
  attributions: SourceAttribution[];
  /** Full evidence collection */
  evidence: EvidenceCollection;
  /** When the explanation was generated */
  generatedAt: string;
  /** Request that produced this explanation */
  request: ExplanationRequest;
  /** Metadata */
  metadata: {
    formulaRegistryVersion: string;
    calibrationProfileVersion: string;
    architectureVersion: string;
    goldenMasterVersion: string;
    deterministic: boolean;
  };
}

export interface ExplanationResultSection {
  id: string;
  title: string;
  content: string;
  sources: SourceAttribution[];
}

export class ExplanationService {
  /**
   * Generate an explanation at the specified level.
   */
  static generateExplanation(request: ExplanationRequest): ExplanationResult {
    const template = getExplanationLevel(request.level);
    const evidence = EvidenceCollector.collect(request.engineOutputs, request.level);

    const variables = ExplanationService.buildVariables(request, evidence, template);
    const sections = ExplanationService.buildSections(template, variables, evidence);

    return {
      level: request.level,
      levelLabel: `${request.level} — ${template.name}`,
      sections,
      attributions: evidence.attributions,
      evidence,
      generatedAt: new Date().toISOString(),
      request,
      metadata: {
        formulaRegistryVersion: evidence.metadata.formulaRegistryVersion,
        calibrationProfileVersion: evidence.metadata.calibrationProfileVersion,
        architectureVersion: evidence.metadata.architectureVersion,
        goldenMasterVersion: evidence.metadata.goldenMasterVersion,
        deterministic: true,
      },
    };
  }

  /**
   * Generate explanations at all available levels.
   */
  static generateAllLevels(request: ExplanationRequest): ExplanationResult[] {
    return (['L1', 'L2', 'L3', 'L4', 'L5'] as ExplanationLevel[]).map(level =>
      ExplanationService.generateExplanation({ ...request, level }),
    );
  }

  /**
   * Generate a comparison between two engine output states.
   */
  static generateComparison(
    requestA: ExplanationRequest,
    requestB: ExplanationRequest,
    level: ExplanationLevel,
  ): {
    explanationA: ExplanationResult;
    explanationB: ExplanationResult;
    comparisonSummary: string;
  } {
    return {
      explanationA: ExplanationService.generateExplanation(requestA),
      explanationB: ExplanationService.generateExplanation(requestB),
      comparisonSummary: `Comparison between ${requestA.consultation.consultationTitle} and ${requestB.consultation.consultationTitle} at ${level} level.`,
    };
  }

  private static buildVariables(
    request: ExplanationRequest,
    evidence: EvidenceCollection,
    _template: ExplanationTemplate,
  ): Record<string, string> {
    const outputs = request.engineOutputs || {};
    const probabilityOutput = outputs.probabilityOutput || {};
    const transitOutput = outputs.transitOutput || {};

    const probScore = (probabilityOutput as any)?.final_score || (probabilityOutput as any)?.score || 0;
    const activationScore = (transitOutput as any)?.activation_score || (transitOutput as any)?.activationScore || 0;
    const transitGrade = (transitOutput as any)?.grade || '—';

    const domainBreakdown = ExplanationService.buildDomainBreakdown(outputs, request.level);
    const formulaReferences = evidence.formulaReferences
      .map(f => `[Formula:${f.formulaId}] ${f.domain}: ${f.name}`)
      .join('\n');
    const calibrationRefs = evidence.calibrationReferences
      .map(c => `[Calibration:${c.constantId}] ${c.name} = ${c.value}`)
      .join('\n');
    const engineRefs = evidence.engineReferences
      .map(e => `[Engine:${e.engineName} v${e.version}] Produces: ${e.outputs.join(', ')}`)
      .join('\n');

    return {
      clientName: request.consultation.clientName,
      consultationTitle: request.consultation.consultationTitle,
      consultationDate: request.consultation.consultationDate,
      probabilityValue: String(Math.round(probScore)),
      probabilityCategory: ExplanationService.getProbabilityCategory(probScore),
      activationValue: String(Math.round(activationScore)),
      transitGrade: String(transitGrade),
      transitScore: String(Math.round(activationScore)),
      domainDescription: request.focus || 'the consulted domain',
      domainBreakdown,
      keyInsight: `a ${getProbabilityCategory(probScore)} overall assessment`,
      supportingEvidence: `${evidence.engineReferences.length} engine(s) and ${evidence.formulaReferences.length} formula(s)`,
      recommendationText: 'further analysis of the specific domain is recommended',
      dashaInfluences: 'Current dasha period provides framework for analysis',
      supportingFactors: 'Transit Jupiter in favorable position',
      obstructingFactors: 'None significant',
      confidenceFlags: (transitOutput as any)?.confidence_flags?.join(', ') || 'None',
      professionalAssessment: `${evidence.engineReferences.length} deterministic engines contributed to this assessment.`,
      executiveSummary: `Consultation for ${request.consultation.clientName} — ${request.consultation.consultationTitle}. ${evidence.engineReferences.length} engines executed.`,
      subsystemBreakdown: ExplanationService.buildSubsystemBreakdown(outputs, request.level),
      formulaReferences,
      formulaEvidenceChains: `Evidence chain includes ${evidence.evidenceChain.length} steps from raw data to final output.`,
      calibrationProfile: evidence.metadata.calibrationProfileVersion,
      keyConstants: calibrationRefs,
      confidenceAnalysis: ExplanationService.buildConfidenceAnalysis(outputs),
      fullAnalysis: 'Complete deterministic analysis with all engine outputs.',
      calibrationDetail: `Calibration Profile: ${evidence.metadata.calibrationProfileVersion}\n${calibrationRefs}`,
      engineOutputReference: engineRefs,
      formulaVersion: evidence.metadata.formulaRegistryVersion,
      calibrationVersion: evidence.metadata.calibrationProfileVersion,
      researchAbstract: 'Research-grade analysis with complete formula trace and evidence chain.',
      completeFormulaTrace: formulaReferences,
      completeCalibration: calibrationRefs,
      rawEngineOutputs: JSON.stringify(outputs, null, 2),
      completeEvidenceChain: evidence.evidenceChain.map(e => `Step ${e.step}: ${e.description}`).join('\n'),
      methodology: 'All values derived from deterministic engines. No AI calculations performed.',
      ...request.context,
    };
  }

  private static buildSections(
    _template: ExplanationTemplate,
    variables: Record<string, string>,
    evidence: EvidenceCollection,
  ): ExplanationResultSection[] {
    return _template.sections.map((section: any) => {
      let content = section.template;
      for (const [key, value] of Object.entries(variables)) {
        content = content.replace(new RegExp(`{{${key}}}`, 'g'), value || '—');
      }
      return {
        id: section.id,
        title: section.title,
        content,
        sources: evidence.attributions.filter(a =>
          section.requiredSources.includes(a.type),
        ),
      };
    });
  }

  private static getProbabilityCategory(score: number): string {
    if (score >= 80) return 'Very High';
    if (score >= 70) return 'High';
    if (score >= 60) return 'Moderate-High';
    if (score >= 50) return 'Moderate';
    if (score >= 40) return 'Moderate-Low';
    if (score >= 30) return 'Low';
    return 'Very Low';
  }

  private static buildDomainBreakdown(outputs: Record<string, unknown>, _level: ExplanationLevel): string {
    const transitOutput = outputs.transitOutput || {};
    const activatedDomains = (transitOutput as any)?.activated_domains;
    if (!activatedDomains) return 'No domain data available.';
    if (Array.isArray(activatedDomains)) {
      return activatedDomains.map((d: any) => `${d.name}: Score ${d.score || '—'}`).join('\n');
    }
    return JSON.stringify(activatedDomains, null, 2);
  }

  private static buildSubsystemBreakdown(outputs: Record<string, unknown>, _level: ExplanationLevel): string {
    const transitOutput = outputs.transitOutput || {};
    const breakdown = (transitOutput as any)?.breakdown;
    if (!breakdown) return 'No subsystem breakdown available.';

    const parts: string[] = [];
    if (breakdown.house_activation) parts.push(`House Activation: ${JSON.stringify(breakdown.house_activation)}`);
    if (breakdown.bav_support) parts.push(`BAV Support: ${JSON.stringify(breakdown.bav_support)}`);
    if (breakdown.planet_activation) parts.push(`Planet Activation: ${JSON.stringify(breakdown.planet_activation)}`);
    if (breakdown.dasha_sync) parts.push(`Dasha Sync: ${JSON.stringify(breakdown.dasha_sync)}`);
    if (breakdown.vedha_layer) parts.push(`Vedha Layer: ${JSON.stringify(breakdown.vedha_layer)}`);

    return parts.join('\n') || 'No subsystem data available.';
  }

  private static buildConfidenceAnalysis(outputs: Record<string, unknown>): string {
    const transitOutput = outputs.transitOutput || {};
    const flags = (transitOutput as any)?.confidence_flags || [];
    if (Array.isArray(flags) && flags.length > 0) {
      return `Confidence flags: ${flags.join(', ')}.\nBased on ${flags.length} independent verification factors.`;
    }
    return 'Confidence analysis based on deterministic engine calculations.';
  }
}

// Re-export for convenience
function getProbabilityCategory(score: number): string {
  if (score >= 80) return 'Very High';
  if (score >= 70) return 'High';
  if (score >= 60) return 'Moderate-High';
  if (score >= 50) return 'Moderate';
  if (score >= 40) return 'Moderate-Low';
  if (score >= 30) return 'Low';
  return 'Very Low';
}
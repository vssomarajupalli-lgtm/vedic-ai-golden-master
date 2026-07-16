// BKL-008A.2 — Deterministic Explainability Engine
// Evidence Collector: Gathers evidence from formulas, calibration, engines
// Never calculates — only collects and formats existing deterministic data

import { SourceAttributionGenerator } from './sourceAttributionGenerator';
import type { SourceAttribution } from './sourceAttributionGenerator';
import type { ExplanationLevel } from './explanationTemplates';

export interface EvidenceCollection {
  /** All source attributions collected */
  attributions: SourceAttribution[];
  /** Formula references extracted */
  formulaReferences: FormulaReference[];
  /** Calibration references extracted */
  calibrationReferences: CalibrationReference[];
  /** Engine output references */
  engineReferences: EngineReference[];
  /** Evidence chain (formula → calibration → output) */
  evidenceChain: EvidenceChainEntry[];
  /** Collection metadata */
  metadata: {
    collectedAt: string;
    formulaRegistryVersion: string;
    calibrationProfileVersion: string;
    architectureVersion: string;
    goldenMasterVersion: string;
  };
}

export interface FormulaReference {
  formulaId: string;
  name: string;
  domain: string;
  version: string;
  inputParams: string[];
  outputType: string;
}

export interface CalibrationReference {
  constantId: string;
  name: string;
  value: number;
  profile: string;
  description: string;
}

export interface EngineReference {
  engineName: string;
  version: string;
  outputs: string[];
  inputData: string;
}

export interface EvidenceChainEntry {
  step: number;
  description: string;
  source: string;
  formulaRef?: string;
  calibrationRef?: string;
  outputValue?: unknown;
}

export class EvidenceCollector {
  /**
   * Collect all evidence for an explanation at the specified level.
   */
  static collect(
    engineOutputs: Record<string, unknown> | null,
    level: ExplanationLevel,
  ): EvidenceCollection {
    const collection: EvidenceCollection = {
      attributions: [],
      formulaReferences: [],
      calibrationReferences: [],
      engineReferences: [],
      evidenceChain: [],
      metadata: {
        collectedAt: new Date().toISOString(),
        formulaRegistryVersion: '1.0.0',
        calibrationProfileVersion: 'v1.0.0',
        architectureVersion: '1.2.0',
        goldenMasterVersion: 'v1.2.0',
      },
    };

    if (!engineOutputs) return collection;

    // Collect engine references
    collection.engineReferences = EvidenceCollector.collectEngineReferences(engineOutputs);
    collection.engineReferences.forEach(ref => {
      const attr = SourceAttributionGenerator.engine(
        ref.engineName,
        ref.version,
        `Produces: ${ref.outputs.join(', ')}`,
      );
      collection.attributions.push(attr);
    });

    // Collect formula references (from known formula IDs in outputs)
    collection.formulaReferences = EvidenceCollector.collectFormulaReferences(engineOutputs);
    collection.formulaReferences.forEach(ref => {
      const attr = SourceAttributionGenerator.formula(
        ref.formulaId,
        ref.version,
        `${ref.domain}: ${ref.name}`,
      );
      collection.attributions.push(attr);
    });

    // Collect calibration references (at L3+)
    if (level === 'L3' || level === 'L4' || level === 'L5') {
      collection.calibrationReferences = EvidenceCollector.collectCalibrationReferences();
      collection.calibrationReferences.forEach(ref => {
        const attr = SourceAttributionGenerator.calibration(
          ref.profile,
          collection.metadata.calibrationProfileVersion,
          `${ref.constantId} = ${ref.value} (${ref.description})`,
        );
        collection.attributions.push(attr);
      });
    }

    // Build evidence chain (at L4+)
    if (level === 'L4' || level === 'L5') {
      collection.evidenceChain = EvidenceCollector.buildEvidenceChain(
        collection.engineReferences,
        collection.formulaReferences,
        collection.calibrationReferences,
        engineOutputs,
      );
    }

    return collection;
  }

  private static collectEngineReferences(
    outputs: Record<string, unknown>,
  ): EngineReference[] {
    const refs: EngineReference[] = [];

    if (outputs.probabilityOutput) {
      refs.push({
        engineName: 'MasterProbabilityEngine',
        version: '1.0',
        outputs: ['final_score', 'confidence_flags', 'breakdown'],
        inputData: 'TransitEngine + DashaEngine + PlanetStrength output',
      });
    }

    if (outputs.transitOutput) {
      refs.push({
        engineName: 'TransitEngine',
        version: '1.0',
        outputs: ['activation_score', 'grade', 'activated_domains', 'confidence_flags'],
        inputData: 'Planetary positions + Dasha period',
      });
    }

    if (outputs.dashaOutput) {
      refs.push({
        engineName: 'DashaEngine',
        version: '1.0',
        outputs: ['md', 'ad', 'pd', 'dasha_lord_positions'],
        inputData: 'Birth data + Ayanamsa',
      });
    }

    if (outputs.planetStrength) {
      refs.push({
        engineName: 'PlanetStrengthEngine',
        version: '1.0',
        outputs: ['dignity_score', 'house_placement_score', 'aspect_score', 'retrograde_bonus'],
        inputData: 'Planetary positions from canonical content',
      });
    }

    return refs;
  }

  private static collectFormulaReferences(
    outputs: Record<string, unknown>,
  ): FormulaReference[] {
    const refs: FormulaReference[] = [];
    const data = JSON.stringify(outputs);

    // Extract formula IDs from engine outputs (pattern matching)
    const formulaPattern = /(?:formula|FORMULA)[_ ]?([A-Z]{3,4}[-_]\d{3})/g;
    const seen = new Set<string>();
    let match: RegExpExecArray | null;

    while ((match = formulaPattern.exec(data)) !== null) {
      const id = match[1].replace('_', '-');
      if (seen.has(id)) continue;
      seen.add(id);

      refs.push({
        formulaId: id,
        name: this.getFormulaName(id),
        domain: this.getFormulaDomain(id),
        version: '1.0',
        inputParams: [],
        outputType: 'numeric',
      });
    }

    // Always include known formula references
    const knownFormulas = [
      { id: 'TRN-HA-001', name: 'House Activation', domain: 'Transit' },
      { id: 'TRN-BV-001', name: 'BAV Support', domain: 'Transit' },
      { id: 'TRN-PA-001', name: 'Planet Activation', domain: 'Transit' },
      { id: 'TRN-DS-001', name: 'Dasha Sync', domain: 'Transit' },
      { id: 'TRN-VD-001', name: 'Vedha Layer', domain: 'Transit' },
      { id: 'PLN-DG-001', name: 'Dignity Score', domain: 'Planet Strength' },
      { id: 'PLN-HP-001', name: 'House Placement', domain: 'Planet Strength' },
      { id: 'PRB-AG-001', name: 'Probability Aggregation', domain: 'Probability' },
    ];

    for (const f of knownFormulas) {
      if (seen.has(f.id)) continue;
      if (data.includes(f.name.toLowerCase()) || data.includes(f.id)) {
        refs.push({
          formulaId: f.id,
          name: f.name,
          domain: f.domain,
          version: '1.0',
          inputParams: [],
          outputType: 'numeric',
        });
      }
    }

    return refs;
  }

  private static collectCalibrationReferences(): CalibrationReference[] {
    return [
      {
        constantId: 'own_sign',
        name: 'Own Sign Strength',
        value: 80,
        profile: 'standard',
        description: 'Weight multiplier for planet in its own sign',
      },
      {
        constantId: 'friendly',
        name: 'Friendly Sign Strength',
        value: 60,
        profile: 'standard',
        description: 'Weight multiplier for planet in friendly sign',
      },
      {
        constantId: 'neutral',
        name: 'Neutral Sign Strength',
        value: 50,
        profile: 'standard',
        description: 'Weight multiplier for planet in neutral sign',
      },
      {
        constantId: 'enemy',
        name: 'Enemy Sign Strength',
        value: 40,
        profile: 'standard',
        description: 'Weight multiplier for planet in enemy sign',
      },
      {
        constantId: 'debilitated',
        name: 'Debilitated Sign Strength',
        value: 20,
        profile: 'standard',
        description: 'Weight multiplier for planet in debilitated sign',
      },
    ];
  }

  private static buildEvidenceChain(
    engines: EngineReference[],
    _formulas: FormulaReference[],
    calibrations: CalibrationReference[],
    outputs: Record<string, unknown>,
  ): EvidenceChainEntry[] {
    const chain: EvidenceChainEntry[] = [];
    let step = 1;

    chain.push({
      step: step++,
      description: 'Birth data processed through canonical content parser',
      source: 'CanonicalContent',
    });

    for (const engine of engines) {
      chain.push({
        step: step++,
        description: `${engine.engineName} v${engine.version} executed with ${engine.inputData}`,
        source: engine.engineName,
        outputValue: outputs[engine.engineName.toLowerCase().replace('engine', 'Output')],
      });
    }

    for (const cal of calibrations) {
      chain.push({
        step: step++,
        description: `Calibration constant applied: ${cal.constantId} = ${cal.value}`,
        source: 'CalibrationManager',
        calibrationRef: cal.constantId,
      });
    }

    chain.push({
      step: step++,
      description: 'Final probability aggregated from all subsystem scores',
      source: 'MasterProbabilityEngine',
      outputValue: outputs.probabilityOutput,
    });

    return chain;
  }

  private static getFormulaName(id: string): string {
    const names: Record<string, string> = {
      'TRN-HA-001': 'House Activation',
      'TRN-BV-001': 'BAV Support',
      'TRN-PA-001': 'Planet Activation',
      'TRN-DS-001': 'Dasha Sync',
      'TRN-VD-001': 'Vedha Layer',
      'PLN-DG-001': 'Dignity Score',
      'PLN-HP-001': 'House Placement',
      'PRB-AG-001': 'Probability Aggregation',
    };
    return names[id] || id;
  }

  private static getFormulaDomain(id: string): string {
    if (id.startsWith('TRN')) return 'Transit';
    if (id.startsWith('PLN')) return 'Planet Strength';
    if (id.startsWith('BHV')) return 'Bhava Strength';
    if (id.startsWith('DSH')) return 'Dasha';
    if (id.startsWith('PRB')) return 'Probability';
    return 'Unknown';
  }
}
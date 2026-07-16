// BKL-008A.1 — AI Assistant Foundation
// Deterministic Bridge: Read-only bridge to GM-007 deterministic outputs
// AP-002 BR-01–BR-06 Compliant: Read-only; never write; never recalculate

import { useChartStore } from '../../store/useChartStore';

export interface DeterministicContext {
  /** When this snapshot was captured */
  capturedAt: string;
  /** Hash of the source data (for integrity verification) */
  sourceHash: string;
  /** Verbatim engine outputs — the only data AI may access */
  engineOutputs: {
    planetStrength: Record<string, unknown> | null;
    bhavaStrength: Record<string, unknown> | null;
    dashaOutput: Record<string, unknown> | null;
    transitOutput: Record<string, unknown> | null;
    probabilityOutput: Record<string, unknown> | null;
    pipelineOutput: Record<string, unknown> | null;
  };
  /** Reference data (formulas, calibration) for attribution */
  referenceData: {
    formulaRegistryVersion: string;
    calibrationProfileVersion: string;
    questionCatalogVersion: string;
    architectureVersion: string;
    goldenMasterVersion: string;
  };
}

/**
 * DeterministicBridge provides read-only access to GM-007 engine outputs.
 * It is the ONLY way AI can access deterministic data.
 * 
 * AP-002 BR-01: AI may READ any deterministic output
 * AP-002 BR-02: AI must NEVER WRITE to any deterministic store
 * AP-002 BR-03: AI must NEVER MODIFY any engine output
 * AP-002 BR-04: AI must NEVER RECALCULATE any deterministic value
 * AP-002 BR-05: AI must NEVER REINTERPRET engine outputs
 */
export class DeterministicBridge {
  /**
   * Capture the current deterministic state for AI consumption.
   * This is a READ-ONLY snapshot — AI cannot modify it.
   */
  static captureContext(): DeterministicContext {
    const store = useChartStore.getState();

    const context: DeterministicContext = {
      capturedAt: new Date().toISOString(),
      sourceHash: DeterministicBridge.computeHash(store),
      engineOutputs: {
        planetStrength: store.machineIndex as unknown as Record<string, unknown> | null,
        bhavaStrength: store.machineIndex as unknown as Record<string, unknown> | null,
        dashaOutput: store.machineIndex as unknown as Record<string, unknown> | null,
        transitOutput: store.rawOutputs as unknown as Record<string, unknown> | null,
        probabilityOutput: store.report as unknown as Record<string, unknown> | null,
        pipelineOutput: store.rawOutputs as unknown as Record<string, unknown> | null,
      },
      referenceData: {
        formulaRegistryVersion: '1.0.0',
        calibrationProfileVersion: 'v1.0.0',
        questionCatalogVersion: '1.0.0',
        architectureVersion: '1.2.0',
        goldenMasterVersion: 'v1.2.0',
      },
    };

    return context;
  }

  /**
   * Format engine outputs as a string for AI prompt context.
   * This preserves exact values — no rounding, no interpretation.
   */
  static formatForPrompt(context: DeterministicContext): string {
    const parts: string[] = [];

    parts.push('=== DETERMINISTIC ENGINE OUTPUTS (VERBATIM — DO NOT MODIFY) ===');
    parts.push(`Captured: ${context.capturedAt}`);
    parts.push(`Source Hash: ${context.sourceHash}`);
    parts.push(`GM Version: ${context.referenceData.goldenMasterVersion}`);
    parts.push(`Formula Registry: ${context.referenceData.formulaRegistryVersion}`);
    parts.push(`Calibration: ${context.referenceData.calibrationProfileVersion}`);
    parts.push('');

    if (context.engineOutputs.probabilityOutput) {
      parts.push('--- MASTER PROBABILITY OUTPUT ---');
      parts.push(JSON.stringify(context.engineOutputs.probabilityOutput, null, 2));
      parts.push('');
    }

    if (context.engineOutputs.transitOutput) {
      parts.push('--- TRANSIT ENGINE OUTPUT ---');
      parts.push(JSON.stringify(context.engineOutputs.transitOutput, null, 2));
      parts.push('');
    }

    if (context.engineOutputs.dashaOutput) {
      parts.push('--- DASHA ENGINE OUTPUT ---');
      parts.push(JSON.stringify(context.engineOutputs.dashaOutput, null, 2));
      parts.push('');
    }

    if (context.engineOutputs.planetStrength) {
      parts.push('--- PLANET STRENGTH OUTPUT ---');
      parts.push(JSON.stringify(context.engineOutputs.planetStrength, null, 2));
      parts.push('');
    }

    parts.push('=== END DETERMINISTIC OUTPUTS ===');
    parts.push('ALL VALUES ABOVE ARE READ-ONLY. DO NOT MODIFY, RECALCULATE, OR FABRICATE.');

    return parts.join('\n');
  }

  /**
   * Extract specific engine output fields for focused queries.
   */
  static extractFields(context: DeterministicContext, fields: string[]): Record<string, unknown> {
    const result: Record<string, unknown> = {};
    const allOutputs = { ...context.engineOutputs };

    for (const field of fields) {
      const value = DeterministicBridge.getNestedValue(allOutputs, field);
      if (value !== undefined) {
        result[field] = value;
      }
    }

    return result;
  }

  private static getNestedValue(obj: unknown, path: string): unknown {
    const parts = path.split('.');
    let current: any = obj;
    for (const part of parts) {
      if (current == null || typeof current !== 'object') return undefined;
      current = current[part];
    }
    return current;
  }

  /**
   * Compute a simple hash of the store state for integrity verification.
   * In production, this would use SHA-256.
   */
  private static computeHash(store: any): string {
    const data = JSON.stringify({
      machineIndex: store.machineIndex,
      rawOutputs: store.rawOutputs,
      report: store.report,
    });
    // Simple hash for now — replace with SHA-256 in production
    let hash = 0;
    for (let i = 0; i < data.length; i++) {
      const chr = data.charCodeAt(i);
      hash = ((hash << 5) - hash) + chr;
      hash |= 0;
    }
    return 'bridge-' + Math.abs(hash).toString(16);
  }
}
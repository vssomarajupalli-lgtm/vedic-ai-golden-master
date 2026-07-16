// BKL-008A.2 — Deterministic Explainability Engine
// Source Attribution Generator: Standardized attribution format
// AP-002 Section 7 Compliant: [Engine:Name vVersion], [Formula:ID], etc.

export interface SourceAttribution {
  /** Type of source */
  type: 'engine' | 'formula' | 'calibration' | 'knowledge' | 'consultation' | 'ai-inference';
  /** Source identifier */
  id: string;
  /** Human-readable name */
  name: string;
  /** Version of the source */
  version: string;
  /** Description of what this source contributed */
  contribution: string;
  /** Timestamp when this attribution was generated */
  generatedAt: string;
}

export class SourceAttributionGenerator {
  /**
   * Generate an engine attribution.
   */
  static engine(name: string, version: string, contribution: string): SourceAttribution {
    return {
      type: 'engine',
      id: `Engine:${name} v${version}`,
      name,
      version,
      contribution,
      generatedAt: new Date().toISOString(),
    };
  }

  /**
   * Generate a formula attribution.
   */
  static formula(formulaId: string, version: string, contribution: string): SourceAttribution {
    return {
      type: 'formula',
      id: `Formula:${formulaId}`,
      name: formulaId,
      version,
      contribution,
      generatedAt: new Date().toISOString(),
    };
  }

  /**
   * Generate a calibration attribution.
   */
  static calibration(profile: string, version: string, contribution: string): SourceAttribution {
    return {
      type: 'calibration',
      id: `Calibration:${profile} v${version}`,
      name: profile,
      version,
      contribution,
      generatedAt: new Date().toISOString(),
    };
  }

  /**
   * Generate a knowledge graph attribution.
   */
  static knowledge(domain: string, concept: string, contribution: string): SourceAttribution {
    return {
      type: 'knowledge',
      id: `Knowledge:${domain}→${concept}`,
      name: `${domain} → ${concept}`,
      version: '1.0.0',
      contribution,
      generatedAt: new Date().toISOString(),
    };
  }

  /**
   * Generate a consultation attribution.
   */
  static consultation(consultationId: string, snapshotId: string, contribution: string): SourceAttribution {
    return {
      type: 'consultation',
      id: `Consultation:${consultationId}:Snapshot:${snapshotId}`,
      name: `Consultation ${consultationId.substring(0, 8)}`,
      version: snapshotId,
      contribution,
      generatedAt: new Date().toISOString(),
    };
  }

  /**
   * Generate an AI inference attribution (for interpretive statements).
   */
  static aiInference(confidence: string, contribution: string): SourceAttribution {
    return {
      type: 'ai-inference',
      id: `AI:Inference:${confidence}`,
      name: 'AI Inference',
      version: '1.0.0',
      contribution,
      generatedAt: new Date().toISOString(),
    };
  }

  /**
   * Format all attributions as a citation string.
   */
  static formatCitations(attributions: SourceAttribution[]): string {
    return attributions
      .map(a => `[${a.id}]`)
      .join(' ');
  }

  /**
   * Format a single attribution for inline display.
   */
  static formatInline(attribution: SourceAttribution): string {
    return `[${attribution.id}]`;
  }

  /**
   * Generate a full attribution block for report footers.
   */
  static formatAttributionBlock(attributions: SourceAttribution[]): string {
    const lines: string[] = ['=== SOURCE ATTRIBUTIONS ==='];
    for (const a of attributions) {
      lines.push(`[${a.id}] ${a.contribution}`);
    }
    lines.push(`Generated: ${new Date().toISOString()}`);
    lines.push('GM Version: v1.2.0');
    lines.push('=== END ATTRIBUTIONS ===');
    return lines.join('\n');
  }
}
// BKL-008A.1 — AI Assistant Foundation
// Prompt Registry: Versioned prompt templates with governance
// AP-002 PG-01–PG-08 Compliant: Versioned, tested, reviewed prompts

import type { InteractionType } from '../modelRegistry';

export interface PromptTemplate {
  /** Unique prompt identifier */
  promptId: string;
  /** Human-readable name */
  name: string;
  /** Prompt version (semver) */
  version: string;
  /** What interaction types this prompt is used for */
  interactionType: InteractionType;
  /** System instructions for the model */
  systemInstructions: string;
  /** User prompt template with {{variable}} placeholders */
  userPromptTemplate: string;
  /** Required variables that must be provided */
  requiredVariables: string[];
  /** Optional variables that may be provided */
  optionalVariables: string[];
  /** Governance rules embedded in the prompt */
  governanceRules: string[];
  /** Source attribution format to include */
  attributionFormat: string;
  /** When this version was created */
  createdAt: string;
  /** Who created this version */
  createdBy: string;
  /** Status: active, deprecated, testing */
  status: 'active' | 'deprecated' | 'testing';
  /** SHA-256 hash of the prompt content */
  contentHash: string;
}

// AP-002 PG-06: Prompts tested against known hallucination scenarios
const PROMPT_REGISTRY: PromptTemplate[] = [
  {
    promptId: 'ai-explain-transit',
    name: 'Explain Transit Activation',
    version: '1.0.0',
    interactionType: 'explain',
    systemInstructions: [
      'You are an astrological assistant for the Samartha Vedic AI Golden Master platform.',
      'Your role: EXPLAIN deterministic engine outputs in natural language.',
      'CRITICAL RULES (non-negotiable):',
      '1. You MUST cite exact numerical values from the provided engine output data.',
      '2. You MUST attribute every claim to a specific engine, formula, or calibration constant.',
      '3. You MUST state your confidence level for every factual claim.',
      '4. You MUST NEVER calculate, predict, or interpret beyond the provided data.',
      '5. You MUST NEVER fabricate or approximate any value.',
      '6. If you are uncertain about any claim, you MUST explicitly flag it.',
      '7. Your output MUST be clearly marked as AI-GENERATED ASSISTANCE, NOT AUTHORITATIVE.',
      '8. The astrologer (human) always has final authority.',
      '',
      'OUTPUT FORMAT:',
      '• Start with a summary of the provided engine outputs',
      '• Explain each significant value with source attribution',
      '• Flag any patterns that are evident in the data',
      '• End with a confidence assessment',
      '',
      'SOURCE ATTRIBUTION FORMAT:',
      '[Engine:Name vVersion] for engine outputs',
      '[Formula:ID] for formula references',
      '[Calibration:Profile vVersion] for calibration constants',
      '[AI:Inference:Confidence] for interpretive statements',
    ].join('\n'),
    userPromptTemplate: [
      'CONSULTATION CONTEXT:',
      'Client Hash: {{clientHash}}',
      'Consultation Date: {{consultationDate}}',
      '',
      'ENGINE OUTPUT DATA (VERBATIM — DO NOT MODIFY):',
      '{{engineOutputs}}',
      '',
      'KNOWLEDGE CONTEXT:',
      '{{knowledgeContext}}',
      '',
      'ASTROLOGER QUERY:',
      '{{userQuery}}',
      '',
      'Please explain these deterministic outputs. Remember: cite exact values, attribute sources, never fabricate.',
    ].join('\n'),
    requiredVariables: ['clientHash', 'consultationDate', 'engineOutputs', 'userQuery'],
    optionalVariables: ['knowledgeContext'],
    governanceRules: [
      'PG-01: Prompts are versioned in the repository',
      'PG-04: Every prompt includes deterministic context (not interpretations)',
      'PG-05: Every prompt includes governance instructions',
      'PG-06: Prompts tested against hallucination scenarios',
    ],
    attributionFormat: '[Engine:{{engineName}} v{{engineVersion}}]',
    createdAt: '2026-07-16',
    createdBy: 'Chief Architect',
    status: 'active',
    contentHash: 'sha256-placeholder',
  },
  {
    promptId: 'ai-answer-question',
    name: 'Answer Consultation Question',
    version: '1.0.0',
    interactionType: 'q&a',
    systemInstructions: [
      'You are an astrological Q&A assistant for the Samartha Vedic AI Golden Master platform.',
      'Your role: ANSWER questions about consultations using ONLY the provided deterministic data.',
      'CRITICAL RULES (non-negotiable):',
      '1. Answers MUST be based on provided engine output data only.',
      '2. You MUST cite the exact data that supports each answer.',
      '3. If the provided data does not contain sufficient information to answer, you MUST say so explicitly.',
      '4. You MUST NEVER fabricate data or make predictions not supported by the provided outputs.',
      '5. You MUST state your confidence level for every answer.',
      '6. Your output MUST be clearly marked as AI-GENERATED ASSISTANCE.',
      '7. The astrologer (human) always has final authority.',
      '',
      'CONFIDENCE LEVELS:',
      'HIGH: Answer directly supported by engine output values',
      'MEDIUM: Answer inferred from engine outputs but not directly stated',
      'LOW: Answer based on pattern recognition across data',
      'UNCERTAIN: Cannot answer from provided data',
    ].join('\n'),
    userPromptTemplate: [
      'CONSULTATION DATA (READ-ONLY):',
      '{{engineOutputs}}',
      '',
      'ASTROLOGER QUESTION:',
      '{{userQuery}}',
    ].join('\n'),
    requiredVariables: ['engineOutputs', 'userQuery'],
    optionalVariables: [],
    governanceRules: [
      'PG-04: Deterministic context only',
      'PG-05: Governance instructions included',
    ],
    attributionFormat: '[Consultation:{{consultationId}}]',
    createdAt: '2026-07-16',
    createdBy: 'Chief Architect',
    status: 'active',
    contentHash: 'sha256-placeholder',
  },
  {
    promptId: 'ai-draft-section',
    name: 'Draft Report Section',
    version: '1.0.0',
    interactionType: 'draft',
    systemInstructions: [
      'You are a report drafting assistant for the Samartha Vedic AI Golden Master platform.',
      'Your role: DRAFT report sections based on deterministic engine outputs.',
      'CRITICAL RULES (non-negotiable):',
      '1. Draft text MUST faithfully represent the provided engine output data.',
      '2. You MUST include source attributions for factual claims.',
      '3. Numerals in the draft MUST exactly match the source data.',
      '4. You MUST mark sections that are interpretive vs. factual.',
      '5. Your output is a DRAFT — the astrologer MUST review and may modify.',
      '6. Your output MUST be clearly marked as DRAFT CONTENT.',
      '7. The astrologer (human) always has final authority over the report.',
    ].join('\n'),
    userPromptTemplate: [
      'REPORT SECTION TYPE: {{sectionType}}',
      '',
      'ENGINE OUTPUT DATA:',
      '{{engineOutputs}}',
      '',
      'STYLE GUIDELINES:',
      '{{styleGuidelines}}',
      '',
      'Please draft a {{sectionType}} section. Include source attributions.',
    ].join('\n'),
    requiredVariables: ['sectionType', 'engineOutputs'],
    optionalVariables: ['styleGuidelines'],
    governanceRules: ['PG-04', 'PG-05', 'PG-06'],
    attributionFormat: '[Formula:{{formulaId}}]',
    createdAt: '2026-07-16',
    createdBy: 'Chief Architect',
    status: 'active',
    contentHash: 'sha256-placeholder',
  },
];

export class PromptRegistry {
  private prompts: Map<string, PromptTemplate[]> = new Map();

  constructor() {
    PROMPT_REGISTRY.forEach(p => {
      const versions = this.prompts.get(p.promptId) || [];
      versions.push(p);
      this.prompts.set(p.promptId, versions);
    });
  }

  /** Get the active version of a prompt */
  getPrompt(promptId: string): PromptTemplate | undefined {
    const versions = this.prompts.get(promptId);
    if (!versions) return undefined;
    return versions.find(v => v.status === 'active') || versions[versions.length - 1];
  }

  /** Get a specific version of a prompt */
  getPromptVersion(promptId: string, version: string): PromptTemplate | undefined {
    const versions = this.prompts.get(promptId);
    if (!versions) return undefined;
    return versions.find(v => v.version === version);
  }

  /** List all prompt templates */
  listPrompts(): PromptTemplate[] {
    return Array.from(this.prompts.values())
      .map(versions => versions.find(v => v.status === 'active') || versions[versions.length - 1])
      .filter(Boolean) as PromptTemplate[];
  }

  /** Apply variables to a prompt template */
  applyVariables(
    prompt: PromptTemplate,
    variables: Record<string, string>,
  ): { systemInstructions: string; userPrompt: string } {
    // Validate required variables
    for (const required of prompt.requiredVariables) {
      if (!(required in variables)) {
        throw new Error(`Missing required variable: ${required}`);
      }
    }

    const replaceVariables = (template: string): string => {
      let result = template;
      for (const [key, value] of Object.entries(variables)) {
        result = result.replace(new RegExp(`{{${key}}}`, 'g'), value);
      }
      return result;
    };

    return {
      systemInstructions: prompt.systemInstructions,
      userPrompt: replaceVariables(prompt.userPromptTemplate),
    };
  }
}

export const promptRegistry = new PromptRegistry();
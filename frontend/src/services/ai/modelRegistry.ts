// BKL-008A.1 — AI Assistant Foundation
// Model Registry: Central registry of approved AI models
// AP-002 MG-01 Compliant: All models must be explicitly approved

import type { AICapability } from './providers/providerInterface';

export interface ModelRegistryEntry {
  modelId: string;
  providerId: string;
  displayName: string;
  capabilities: AICapability[];
  maxTokens: number;
  costPer1kTokens: number;
  status: 'active' | 'deprecated' | 'unavailable';
  approvedAt: string;
  approvedBy: string;
  minConfidenceThreshold: number;
  maxTokensPerRequest: number;
  approvedFor: InteractionType[];
  providerConfig?: Record<string, unknown>;
}

export type InteractionType = 'q&a' | 'draft' | 'explain' | 'pattern' | 'research';

const APPROVED_MODELS: ModelRegistryEntry[] = [
  {
    modelId: 'openai/gpt-4o-mini',
    providerId: 'openrouter',
    displayName: 'GPT-4o Mini',
    capabilities: ['chat' as AICapability],
    maxTokens: 128000,
    costPer1kTokens: 0.00015,
    status: 'active',
    approvedAt: '2026-07-16',
    approvedBy: 'Chief Architect',
    minConfidenceThreshold: 0.7,
    maxTokensPerRequest: 4096,
    approvedFor: ['q&a', 'explain'],
  },
  {
    modelId: 'anthropic/claude-3-haiku',
    providerId: 'openrouter',
    displayName: 'Claude 3 Haiku',
    capabilities: ['chat' as AICapability],
    maxTokens: 200000,
    costPer1kTokens: 0.00025,
    status: 'active',
    approvedAt: '2026-07-16',
    approvedBy: 'Chief Architect',
    minConfidenceThreshold: 0.75,
    maxTokensPerRequest: 4096,
    approvedFor: ['draft', 'pattern'],
  },
  {
    modelId: 'google/gemma-3-27b-it',
    providerId: 'openrouter',
    displayName: 'Gemma 3 27B',
    capabilities: ['chat' as AICapability],
    maxTokens: 128000,
    costPer1kTokens: 0,
    status: 'active',
    approvedAt: '2026-07-16',
    approvedBy: 'Chief Architect',
    minConfidenceThreshold: 0.6,
    maxTokensPerRequest: 8192,
    approvedFor: ['research', 'q&a'],
  },
];

export class ModelRegistry {
  private models: Map<string, ModelRegistryEntry> = new Map();

  constructor() {
    APPROVED_MODELS.forEach(m => this.models.set(m.modelId, m));
  }

  getModel(modelId: string): ModelRegistryEntry | undefined {
    return this.models.get(modelId);
  }

  listModels(): ModelRegistryEntry[] {
    return Array.from(this.models.values());
  }

  getModelsForInteraction(type: InteractionType): ModelRegistryEntry[] {
    return this.listModels().filter(m => m.approvedFor.includes(type));
  }

  isApprovedFor(modelId: string, type: InteractionType): boolean {
    const model = this.models.get(modelId);
    if (!model) return false;
    return model.approvedFor.includes(type) && model.status === 'active';
  }

  getDefaultModel(type: InteractionType): ModelRegistryEntry {
    const models = this.getModelsForInteraction(type);
    if (models.length === 0) {
      throw new Error(`No approved models for interaction type: ${type}`);
    }
    if (type === 'q&a' || type === 'explain') {
      return models.find(m => m.modelId.includes('gpt-4o-mini')) || models[0];
    }
    if (type === 'draft' || type === 'pattern') {
      return models.find(m => m.modelId.includes('claude')) || models[0];
    }
    return models[0];
  }
}

export const modelRegistry = new ModelRegistry();
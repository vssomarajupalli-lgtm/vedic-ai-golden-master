// BKL-008A.1 — AI Assistant Foundation
// AI Configuration: Centralized configuration for AI services
// AP-002 Compliant: All config stored in secure configuration, never in code

export interface AIConfig {
  /** Active AI provider */
  provider: 'openrouter' | 'self-hosted';
  /** Provider-specific configuration */
  providerConfig: {
    apiKey?: string;
    baseUrl?: string;
    organizationId?: string;
  };
  /** Default model for each interaction type */
  defaultModels: {
    qa: string;
    draft: string;
    explain: string;
    pattern: string;
    research: string;
  };
  /** Global AI settings */
  settings: {
    /** Maximum tokens per response */
    maxTokens: number;
    /** Default temperature (0-1, lower = more deterministic) */
    temperature: number;
    /** Whether AI features are enabled */
    enabled: boolean;
    /** Whether to use self-hosted models for privacy */
    privacyMode: boolean;
    /** Timeout for AI requests (ms) */
    requestTimeout: number;
    /** Maximum retries for failed requests */
    maxRetries: number;
  };
  /** Audit settings */
  audit: {
    /** Whether audit logging is enabled */
    enabled: boolean;
    /** Whether to store full prompt/response content */
    storeFullContent: boolean;
    /** Retention period for audit records (days) */
    retentionDays: number;
  };
  /** UI settings */
  ui: {
    /** Whether to show confidence badges */
    showConfidenceBadges: boolean;
    /** Whether to show source attributions inline */
    showSourceAttributions: boolean;
    /** Whether AI outputs require explicit review before saving */
    requireReviewBeforeSave: boolean;
  };
}

export const DEFAULT_AI_CONFIG: AIConfig = {
  provider: 'openrouter',
  providerConfig: {
    apiKey: undefined, // Set via environment or user config
    baseUrl: 'https://openrouter.ai/api/v1',
  },
  defaultModels: {
    qa: 'openai/gpt-4o-mini',
    draft: 'anthropic/claude-3-haiku',
    explain: 'openai/gpt-4o-mini',
    pattern: 'anthropic/claude-3-haiku',
    research: 'google/gemma-3-27b-it',
  },
  settings: {
    maxTokens: 4096,
    temperature: 0.3,
    enabled: true,
    privacyMode: false,
    requestTimeout: 30000,
    maxRetries: 2,
  },
  audit: {
    enabled: true,
    storeFullContent: true,
    retentionDays: 365,
  },
  ui: {
    showConfidenceBadges: true,
    showSourceAttributions: true,
    requireReviewBeforeSave: true,
  },
};

// In-memory config store — will be persisted via preferences manager in future
let currentConfig: AIConfig = { ...DEFAULT_AI_CONFIG };

export function getAIConfig(): AIConfig {
  return { ...currentConfig };
}

export function updateAIConfig(partial: Partial<AIConfig>): AIConfig {
  currentConfig = { ...currentConfig, ...partial };
  return { ...currentConfig };
}

export function resetAIConfig(): AIConfig {
  currentConfig = { ...DEFAULT_AI_CONFIG };
  return { ...currentConfig };
}
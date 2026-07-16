// BKL-008A.1 — AI Assistant Foundation
// OpenRouter Provider Implementation
// AP-002 Compliant: All AI calls logged; deterministic outputs never sent to AI

import type {
  AIProvider,
  AIProviderConfig,
  AIProviderRequest,
  AIProviderResponse,
  AIProviderError,
  AIProviderModel,
  AICapability,
} from './providerInterface';

interface OpenRouterModelResponse {
  id: string;
  name: string;
  context_length: number;
  pricing: {
    prompt: string;
    completion: string;
  };
}

const DEFAULT_BASE_URL = 'https://openrouter.ai/api/v1';

export class OpenRouterProvider implements AIProvider {
  readonly providerId = 'openrouter';
  readonly providerName = 'OpenRouter';

  private apiKey: string = '';
  private baseUrl: string = DEFAULT_BASE_URL;
  private isInitialized: boolean = false;

  async initialize(config: AIProviderConfig): Promise<void> {
    if (!config.apiKey) {
      throw new Error('OpenRouter API key is required');
    }
    this.apiKey = config.apiKey;
    this.baseUrl = config.baseUrl || DEFAULT_BASE_URL;
    this.isInitialized = true;
  }

  isReady(): boolean {
    return this.isInitialized && !!this.apiKey;
  }

  async sendRequest(request: AIProviderRequest): Promise<AIProviderResponse> {
    if (!this.isReady()) {
      throw new Error('OpenRouter provider is not initialized');
    }

    const startTime = Date.now();

    try {
      const response = await fetch(`${this.baseUrl}/chat/completions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`,
          'HTTP-Referer': 'https://samartha-vedic-ai.com',
          'X-Title': 'Samartha Vedic AI — Golden Master',
        },
        body: JSON.stringify({
          model: request.modelId,
          messages: [
            ...(request.systemInstructions
              ? [{ role: 'system', content: request.systemInstructions }]
              : []),
            { role: 'user', content: request.prompt },
          ],
          temperature: request.temperature ?? 0.3,
          max_tokens: request.maxTokens ?? 2048,
        }),
      });

      if (!response.ok) {
        const errorBody = await response.text();
        throw this.createProviderError(
          `HTTP_${response.status}`,
          errorBody || 'Unknown API error',
          request.modelId,
          response.status >= 500
        );
      }

      const data = await response.json();
      const latency = Date.now() - startTime;

      return {
        content: data.choices?.[0]?.message?.content || '',
        modelId: data.model || request.modelId,
        providerId: this.providerId,
        usage: {
          promptTokens: data.usage?.prompt_tokens || 0,
          completionTokens: data.usage?.completion_tokens || 0,
          totalTokens: data.usage?.total_tokens || 0,
        },
        latency,
        timestamp: new Date().toISOString(),
        metadata: request.metadata,
      };
    } catch (error: any) {
      throw this.createProviderError(
        'NETWORK_ERROR',
        error.message || 'Network request failed',
        request.modelId,
        true,
      );
    }
  }

  async listModels(): Promise<AIProviderModel[]> {
    if (!this.isReady()) return [];

    try {
      const response = await fetch(`${this.baseUrl}/models`, {
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
        },
      });

      if (!response.ok) return [];

      const data = await response.json();
      return (data.data || []).map((m: OpenRouterModelResponse) => ({
        modelId: m.id,
        providerId: this.providerId,
        displayName: m.name || m.id,
        capabilities: ['chat'] as AICapability[],
        maxTokens: m.context_length || 8192,
        costPer1kTokens: parseFloat(m.pricing?.prompt || '0'),
        status: 'active' as const,
      }));
    } catch {
      return [];
    }
  }

  async validateModel(modelId: string): Promise<boolean> {
    const models = await this.listModels();
    return models.some(m => m.modelId === modelId && m.status === 'active');
  }

  async healthCheck(): Promise<boolean> {
    try {
      const models = await this.listModels();
      return models.length > 0;
    } catch {
      return false;
    }
  }

  private createProviderError(
    code: string,
    message: string,
    modelId: string,
    retryable: boolean,
  ): AIProviderError {
    return {
      code,
      message,
      providerId: this.providerId,
      modelId,
      retryable,
      timestamp: new Date().toISOString(),
    };
  }
}
// BKL-008A.1 — AI Assistant Foundation
// Provider Abstraction: Contract that all AI providers must implement
// AP-002 Compliant: Provider-agnostic interface enabling cloud/self-hosted switching

export interface AIProviderConfig {
  apiKey: string;
  baseUrl?: string;
  organizationId?: string;
  timeout?: number;
  maxRetries?: number;
}

export interface AIProviderRequest {
  modelId: string;
  prompt: string;
  systemInstructions?: string;
  temperature?: number;
  maxTokens?: number;
  metadata?: Record<string, unknown>;
}

export interface AIProviderResponse {
  content: string;
  modelId: string;
  providerId: string;
  usage: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
  latency: number; // milliseconds
  timestamp: string;
  metadata?: Record<string, unknown>;
}

export interface AIProviderError {
  code: string;
  message: string;
  providerId: string;
  modelId: string;
  retryable: boolean;
  timestamp: string;
}

export interface AIProvider {
  /** Unique provider identifier */
  readonly providerId: string;

  /** Human-readable provider name */
  readonly providerName: string;

  /** Initialize the provider with configuration */
  initialize(config: AIProviderConfig): Promise<void>;

  /** Check if provider is ready to accept requests */
  isReady(): boolean;

  /** Send a request to the AI model */
  sendRequest(request: AIProviderRequest): Promise<AIProviderResponse>;

  /** List available models for this provider */
  listModels(): Promise<AIProviderModel[]>;

  /** Validate that a given model ID is available and ready */
  validateModel(modelId: string): Promise<boolean>;

  /** Health check — returns true if provider is operational */
  healthCheck(): Promise<boolean>;
}

export interface AIProviderModel {
  modelId: string;
  providerId: string;
  displayName: string;
  capabilities: AICapability[];
  maxTokens: number;
  costPer1kTokens: number;
  status: 'active' | 'deprecated' | 'unavailable';
}

export type AICapability = 'chat' | 'completion' | 'embedding' | 'vision' | 'function-calling';
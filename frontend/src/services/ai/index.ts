// BKL-008A.1 — AI Assistant Foundation
// Barrel Export: All AI services in one import

export { AIService, aiService } from './aiService';
export type { AIRequest, AIResponse } from './aiService';

export { ModelRegistry, modelRegistry } from './modelRegistry';
export type { ModelRegistryEntry, InteractionType } from './modelRegistry';

export { PromptRegistry, promptRegistry } from './prompts/promptRegistry';
export type { PromptTemplate } from './prompts/promptRegistry';

export { PromptVersionManager, promptVersionManager } from './prompts/promptVersionManager';
export type { PromptVersionRecord } from './prompts/promptVersionManager';

export { SessionManager, sessionManager } from './sessionManager';
export type { AISession, AISessionMessage } from './sessionManager';

export { useConversationRepository, createAuditRecord } from './conversationRepository';
export type { AIInteractionRecord } from './conversationRepository';

export { DeterministicBridge } from './deterministicBridge';
export type { DeterministicContext } from './deterministicBridge';

export { getAIConfig, updateAIConfig, resetAIConfig, DEFAULT_AI_CONFIG } from './aiConfig';
export type { AIConfig } from './aiConfig';

export { OpenRouterProvider } from './providers/openRouterProvider';
export type {
  AIProvider,
  AIProviderConfig,
  AIProviderRequest,
  AIProviderResponse,
  AIProviderError,
  AIProviderModel,
  AICapability,
} from './providers/providerInterface';
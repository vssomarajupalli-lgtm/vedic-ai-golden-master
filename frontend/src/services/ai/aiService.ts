// BKL-008A.1 — AI Assistant Foundation
// AI Service Layer: Core orchestrator for all AI interactions
// AP-002 Compliant: Full governance, audit, and deterministic boundary enforcement

import type { InteractionType } from './modelRegistry';
import { modelRegistry } from './modelRegistry';
import { promptRegistry } from './prompts/promptRegistry';
import { sessionManager } from './sessionManager';
import { useConversationRepository, createAuditRecord } from './conversationRepository';
import { DeterministicBridge } from './deterministicBridge';
import type { DeterministicContext } from './deterministicBridge';
import { getAIConfig } from './aiConfig';
import { OpenRouterProvider } from './providers/openRouterProvider';
import type { AIConfig } from './aiConfig';

export interface AIRequest {
  consultationId: string;
  interactionType: InteractionType;
  userQuery: string;
  modelId?: string;
  contextVariables?: Record<string, string>;
  sessionId?: string;
}

export interface AIResponse {
  content: string;
  modelId: string;
  providerId: string;
  confidenceLevel: 'high' | 'medium' | 'low' | 'uncertain';
  confidenceScore: number;
  sourceAttributions: string[];
  auditId: string;
  sessionId: string;
  latency: number;
  tokensUsed: {
    prompt: number;
    completion: number;
    total: number;
  };
}

export class AIService {
  private provider: OpenRouterProvider;
  private initialized: boolean = false;

  constructor() {
    this.provider = new OpenRouterProvider();
  }

  async initialize(): Promise<void> {
    const config = getAIConfig();
    if (!config.settings.enabled) {
      throw new Error('AI features are disabled in configuration');
    }
    const apiKey = config.providerConfig.apiKey;
    if (!apiKey) {
      throw new Error('OpenRouter API key is required');
    }
    await this.provider.initialize({ apiKey, baseUrl: config.providerConfig.baseUrl });
    this.initialized = true;
  }

  async sendRequest(request: AIRequest): Promise<AIResponse> {
    if (!this.initialized) await this.initialize();

    const config = getAIConfig();
    const modelId = request.modelId || config.defaultModels[this.mapInteractionType(request.interactionType)];
    if (!modelRegistry.isApprovedFor(modelId, request.interactionType)) {
      throw new Error(`Model ${modelId} not approved for ${request.interactionType}`);
    }
    const model = modelRegistry.getModel(modelId);
    if (!model) throw new Error(`Model ${modelId} not found in registry`);

    const deterministicContext = DeterministicBridge.captureContext();

    let sessionId = request.sessionId;
    if (!sessionId) {
      const session = sessionManager.createSession(request.consultationId, request.interactionType, modelId);
      sessionId = session.sessionId;
    }

    const promptId = this.getPromptIdForInteraction(request.interactionType);
    const promptTemplate = promptRegistry.getPrompt(promptId);
    if (!promptTemplate) throw new Error(`No prompt template for ${request.interactionType}`);

    const variables: Record<string, string> = {
      ...request.contextVariables,
      clientHash: request.consultationId.substring(0, 8),
      consultationDate: deterministicContext.capturedAt.split('T')[0],
      engineOutputs: DeterministicBridge.formatForPrompt(deterministicContext),
      userQuery: request.userQuery,
    };

    const { systemInstructions, userPrompt } = promptRegistry.applyVariables(promptTemplate, variables);
    const finalPrompt = this.addGovernanceBoundary(userPrompt, deterministicContext);

    const providerResponse = await this.provider.sendRequest({
      modelId,
      prompt: finalPrompt,
      systemInstructions,
      temperature: config.settings.temperature,
      maxTokens: Math.min(config.settings.maxTokens, model.maxTokensPerRequest),
      metadata: {
        consultationId: request.consultationId,
        interactionType: request.interactionType,
        sessionId,
        deterministicHash: deterministicContext.sourceHash,
      },
    });

    const { confidenceLevel, confidenceScore } = this.calculateConfidence(providerResponse.content, deterministicContext);
    const sourceAttributions = this.extractAttributions(providerResponse.content);

    const auditRecord = createAuditRecord({
      consultationId: request.consultationId,
      modelId,
      providerId: this.provider.providerId,
      interactionType: request.interactionType,
      promptContent: finalPrompt,
      responseContent: providerResponse.content,
      sessionId: sessionId || '',
      confidenceLevel,
      confidenceScore,
      validationResult: confidenceLevel === 'uncertain' ? 'FLAGGED' : 'PASS',
      sourceAttributions,
      latency: providerResponse.latency,
      tokensUsed: {
        prompt: providerResponse.usage.promptTokens,
        completion: providerResponse.usage.completionTokens,
        total: providerResponse.usage.totalTokens,
      },
      engineOutputHash: deterministicContext.sourceHash || '',
      engineOutputSnapshot: JSON.stringify(deterministicContext.engineOutputs),
    });

    useConversationRepository.getState().addInteraction(auditRecord);

    sessionManager.addMessage(sessionId || '', {
      role: 'user',
      content: request.userQuery,
      timestamp: new Date().toISOString(),
    });
    sessionManager.addMessage(sessionId || '', {
      role: 'assistant',
      content: providerResponse.content,
      timestamp: new Date().toISOString(),
      metadata: { confidenceLevel, confidenceScore },
    });

    return {
      content: providerResponse.content,
      modelId,
      providerId: this.provider.providerId,
      confidenceLevel,
      confidenceScore,
      sourceAttributions,
      auditId: auditRecord.auditId,
      sessionId: sessionId || '',
      latency: providerResponse.latency,
      tokensUsed: {
        prompt: providerResponse.usage.promptTokens,
        completion: providerResponse.usage.completionTokens,
        total: providerResponse.usage.totalTokens,
      },
    };
  }

  private calculateConfidence(content: string, context: DeterministicContext): { confidenceLevel: 'high' | 'medium' | 'low' | 'uncertain'; confidenceScore: number } {
    const numberPattern = /(\d+\.?\d*)\s*%?/g;
    const aiNumbers = new Set<string>();
    let match: RegExpExecArray | null;
    while ((match = numberPattern.exec(content)) !== null) {
      aiNumbers.add(match[1]);
    }

    const contextStr = JSON.stringify(context.engineOutputs);
    const contextNumbers = new Set<string>();
    const ctxPattern = /(\d+\.?\d*)/g;
    let ctxMatch: RegExpExecArray | null;
    while ((ctxMatch = ctxPattern.exec(contextStr)) !== null) {
      contextNumbers.add(ctxMatch[1]);
    }

    let verified = 0;
    const total = aiNumbers.size;
    for (const num of aiNumbers) {
      if (contextNumbers.has(num)) verified++;
    }
    if (total === 0) return { confidenceLevel: 'medium', confidenceScore: 0.5 };
    const score = verified / total;
    if (score >= 0.9) return { confidenceLevel: 'high', confidenceScore: score };
    if (score >= 0.6) return { confidenceLevel: 'medium', confidenceScore: score };
    if (score >= 0.3) return { confidenceLevel: 'low', confidenceScore: score };
    return { confidenceLevel: 'uncertain', confidenceScore: score };
  }

  private extractAttributions(content: string): string[] {
    const patterns = [/\[Engine:[^\]]+\]/g, /\[Formula:[^\]]+\]/g, /\[Calibration:[^\]]+\]/g, /\[Knowledge:[^\]]+\]/g, /\[Consultation:[^\]]+\]/g];
    const attributions = new Set<string>();
    for (const pattern of patterns) {
      const matches = content.match(pattern);
      if (matches) matches.forEach(m => attributions.add(m));
    }
    return Array.from(attributions);
  }

  private addGovernanceBoundary(prompt: string, context: DeterministicContext): string {
    return [
      '=== GOVERNANCE BOUNDARY (AP-002 COMPLIANT) ===',
      'The following data is READ-ONLY. Do not modify, recalculate, or fabricate.',
      `Source Hash: ${context.sourceHash}`,
      `GM Version: ${context.referenceData.goldenMasterVersion}`,
      '=== END GOVERNANCE BOUNDARY ===',
      '',
      prompt,
    ].join('\n');
  }

  private getPromptIdForInteraction(type: InteractionType): string {
    switch (type) {
      case 'explain': return 'ai-explain-transit';
      case 'q&a': return 'ai-answer-question';
      case 'draft': return 'ai-draft-section';
      case 'pattern': return 'ai-explain-transit';
      case 'research': return 'ai-answer-question';
    }
  }

  private mapInteractionType(type: InteractionType): keyof AIConfig['defaultModels'] {
    switch (type) {
      case 'q&a': return 'qa';
      case 'draft': return 'draft';
      case 'explain': return 'explain';
      case 'pattern': return 'pattern';
      case 'research': return 'research';
    }
  }
}

export const aiService = new AIService();
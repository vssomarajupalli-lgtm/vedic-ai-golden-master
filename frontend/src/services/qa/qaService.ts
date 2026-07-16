// BKL-008A.3 — Deterministic Q&A Engine
// Core Q&A Service

import { AnswerGenerator } from './answerGenerator';
import type { StructuredAnswer } from './answerGenerator';
import { sessionManager } from '../ai/sessionManager';
import { useConversationRepository, createAuditRecord } from '../ai/conversationRepository';
import { getAIConfig } from '../ai/aiConfig';

export interface QARequest {
  question: string;
  consultationId: string;
  engineOutputs: Record<string, unknown> | null;
  sessionId?: string;
}

export interface QAResponse {
  answer: StructuredAnswer;
  sessionId: string;
  auditId: string;
}

export class QAService {
  static async ask(request: QARequest): Promise<QAResponse> {
    const config = getAIConfig();
    const answer = AnswerGenerator.generateAnswer(request.question, request.engineOutputs, request.consultationId);

    let sessionId = request.sessionId;
    if (!sessionId) {
      const session = sessionManager.createSession(request.consultationId, 'q&a', 'deterministic-qa-engine');
      sessionId = session.sessionId;
    }

    sessionManager.addMessage(sessionId, { role: 'user', content: request.question, timestamp: new Date().toISOString() });
    sessionManager.addMessage(sessionId, { role: 'assistant', content: answer.sections.map(s => s.content).join('\n\n'), timestamp: new Date().toISOString(), metadata: { questionClass: answer.question.questionClass, confidence: answer.confidence, isDeterministic: answer.isDeterministic } });

    const auditRecord = createAuditRecord({
      consultationId: request.consultationId, modelId: 'deterministic-qa-engine', providerId: 'internal',
      interactionType: 'q&a', promptContent: request.question, responseContent: JSON.stringify(answer),
      sessionId, confidenceLevel: answer.confidence > 0.8 ? 'high' : answer.confidence > 0.5 ? 'medium' : 'low',
      confidenceScore: answer.confidence, validationResult: answer.isDeterministic ? 'PASS' : 'FLAGGED',
      sourceAttributions: answer.citations.map(c => c.id), engineOutputHash: '', engineOutputSnapshot: JSON.stringify(request.engineOutputs),
    });

    if (config.audit.enabled) useConversationRepository.getState().addInteraction(auditRecord);

    return { answer, sessionId, auditId: auditRecord.auditId };
  }

  static getSuggestedQuestions(engineOutputs: Record<string, unknown> | null): string[] {
    const suggestions: string[] = [];
    if (engineOutputs?.probabilityOutput) suggestions.push('What is the final probability score?');
    if (engineOutputs?.transitOutput) {
      suggestions.push('What is the current transit effect?');
      suggestions.push('Which domains are most activated by transit?');
    }
    if (engineOutputs?.dashaOutput) suggestions.push('What is my current mahadasha?');
    if (engineOutputs?.planetStrength) {
      suggestions.push('What is the strength of Jupiter?');
      suggestions.push('Which planet is strongest in my chart?');
    }
    suggestions.push('Give me a summary of my chart', 'What formulas are used in the analysis?');
    return suggestions;
  }
}
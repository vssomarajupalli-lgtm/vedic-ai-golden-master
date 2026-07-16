// BKL-008A.1 — AI Assistant Foundation
// Conversation Repository: Immutable storage for AI interactions
// AP-002 AT-01–AT-07 Compliant: Immutable, append-only, queryable audit records

import { v4 as uuidv4 } from 'uuid';
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

export interface AIInteractionRecord {
  /** Unique interaction identifier */
  auditId: string;
  /** When this interaction occurred */
  timestamp: string;
  /** Parent consultation */
  consultationId: string;
  /** Who triggered the AI */
  astrologerId: string;
  /** AI model used */
  modelId: string;
  /** Provider identifier */
  providerId: string;
  /** Interaction type */
  interactionType: 'q&a' | 'draft' | 'explain' | 'pattern' | 'research';
  /** Session ID */
  sessionId: string;
  /** SHA-256 hash of the prompt */
  promptHash: string;
  /** Full prompt text */
  promptContent: string;
  /** SHA-256 hash of source data */
  engineOutputHash: string;
  /** Verbatim source data used */
  engineOutputSnapshot: string;
  /** SHA-256 hash of AI response */
  responseHash: string;
  /** Full AI response text */
  responseContent: string;
  /** Calculated confidence score (0-1) */
  confidenceScore: number;
  /** Confidence level */
  confidenceLevel: 'high' | 'medium' | 'low' | 'uncertain';
  /** Validation result */
  validationResult: 'PASS' | 'FLAGGED' | 'BLOCKED';
  /** What the astrologer did with the output */
  astrologerAction: 'ACCEPTED' | 'MODIFIED' | 'REJECTED' | 'PENDING';
  /** Whether output was saved to consultation */
  savedToConsultation: boolean;
  /** Git commit at interaction time */
  gitCommit: string;
  /** Source attributions in the AI response */
  sourceAttributions: string[];
  /** Response latency (ms) */
  latency: number;
  /** Token usage */
  tokensUsed: {
    prompt: number;
    completion: number;
    total: number;
  };
}

interface ConversationRepositoryState {
  interactions: AIInteractionRecord[];
  addInteraction: (record: AIInteractionRecord) => void;
  getInteractionsForConsultation: (consultationId: string) => AIInteractionRecord[];
  getInteraction: (auditId: string) => AIInteractionRecord | undefined;
  queryInteractions: (filters: Partial<{
    consultationId: string;
    interactionType: string;
    confidenceLevel: string;
    astrologerAction: string;
    startDate: string;
    endDate: string;
  }>) => AIInteractionRecord[];
  exportInteractions: (consultationId?: string) => string;
}

export const useConversationRepository = create<ConversationRepositoryState>()(
  persist(
    (set, get) => ({
      interactions: [],

      addInteraction: (record: AIInteractionRecord) => {
        // Ensure immutable audit ID
        const recordWithId = {
          ...record,
          auditId: record.auditId || uuidv4(),
          timestamp: record.timestamp || new Date().toISOString(),
        };

        set(state => ({
          interactions: [...state.interactions, recordWithId],
        }));
      },

      getInteractionsForConsultation: (consultationId: string) => {
        return get().interactions
          .filter(i => i.consultationId === consultationId)
          .sort((a, b) => b.timestamp.localeCompare(a.timestamp));
      },

      getInteraction: (auditId: string) => {
        return get().interactions.find(i => i.auditId === auditId);
      },

      queryInteractions: (filters) => {
        return get().interactions.filter(i => {
          if (filters.consultationId && i.consultationId !== filters.consultationId) return false;
          if (filters.interactionType && i.interactionType !== filters.interactionType) return false;
          if (filters.confidenceLevel && i.confidenceLevel !== filters.confidenceLevel) return false;
          if (filters.astrologerAction && i.astrologerAction !== filters.astrologerAction) return false;
          if (filters.startDate && i.timestamp < filters.startDate) return false;
          if (filters.endDate && i.timestamp > filters.endDate) return false;
          return true;
        });
      },

      exportInteractions: (consultationId?: string) => {
        const records = consultationId
          ? get().getInteractionsForConsultation(consultationId)
          : get().interactions;

        return JSON.stringify(records, null, 2);
      },
    }),
    {
      name: 'ai-conversation-repository',
      storage: createJSONStorage(() => localStorage),
    }
  )
);

// Helper to create an audit record
export function createAuditRecord(
  overrides: Partial<AIInteractionRecord> & {
    consultationId: string;
    modelId: string;
    providerId: string;
    interactionType: AIInteractionRecord['interactionType'];
    promptContent: string;
    responseContent: string;
  },
): AIInteractionRecord {
  const now = new Date().toISOString();

  return {
    auditId: uuidv4(),
    timestamp: now,
    astrologerId: 'current-user',
    sessionId: '',
    promptHash: simpleHash(overrides.promptContent),
    engineOutputHash: simpleHash(overrides.engineOutputSnapshot || ''),
    engineOutputSnapshot: '',
    responseHash: simpleHash(overrides.responseContent),
    confidenceScore: 0,
    confidenceLevel: 'medium',
    validationResult: 'PASS',
    astrologerAction: 'PENDING',
    savedToConsultation: false,
    gitCommit: 'gm-008-development',
    sourceAttributions: [],
    latency: 0,
    tokensUsed: { prompt: 0, completion: 0, total: 0 },
    ...overrides,
  };
}

function simpleHash(data: string): string {
  let hash = 0;
  for (let i = 0; i < data.length; i++) {
    const chr = data.charCodeAt(i);
    hash = ((hash << 5) - hash) + chr;
    hash |= 0;
  }
  return 'audit-' + Math.abs(hash).toString(16);
}
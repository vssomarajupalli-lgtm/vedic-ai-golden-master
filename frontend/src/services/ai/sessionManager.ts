// BKL-008A.1 — AI Assistant Foundation
// Session Manager: Manage AI conversation sessions with context isolation
// AP-002 PR-03: AI interactions isolated to single consultation context

import { v4 as uuidv4 } from 'uuid';

export interface AISession {
  /** Unique session identifier */
  sessionId: string;
  /** The consultation this session is linked to */
  consultationId: string;
  /** When the session was created */
  createdAt: string;
  /** When the session was last active */
  lastActiveAt: string;
  /** The interaction type for this session */
  interactionType: 'q&a' | 'draft' | 'explain' | 'pattern' | 'research';
  /** The model being used for this session */
  modelId: string;
  /** Session status */
  status: 'active' | 'completed' | 'expired';
  /** Number of interactions in this session */
  interactionCount: number;
  /** Context window for the session (previous messages for context) */
  contextWindow: AISessionMessage[];
  /** Maximum context window size */
  maxContextSize: number;
}

export interface AISessionMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  metadata?: Record<string, unknown>;
}

export class SessionManager {
  private sessions: Map<string, AISession> = new Map();
  private readonly DEFAULT_MAX_CONTEXT = 10;
  private readonly SESSION_TIMEOUT_MS = 30 * 60 * 1000; // 30 minutes

  /**
   * Create a new AI session for a consultation.
   */
  createSession(
    consultationId: string,
    interactionType: AISession['interactionType'],
    modelId: string,
  ): AISession {
    const session: AISession = {
      sessionId: uuidv4(),
      consultationId,
      createdAt: new Date().toISOString(),
      lastActiveAt: new Date().toISOString(),
      interactionType,
      modelId,
      status: 'active',
      interactionCount: 0,
      contextWindow: [],
      maxContextSize: this.DEFAULT_MAX_CONTEXT,
    };

    this.sessions.set(session.sessionId, session);
    return session;
  }

  /**
   * Get an active session by ID.
   */
  getSession(sessionId: string): AISession | undefined {
    const session = this.sessions.get(sessionId);
    if (!session) return undefined;

    // Check if session has expired
    if (session.status === 'active' && this.isSessionExpired(session)) {
      session.status = 'expired';
      return undefined;
    }

    session.lastActiveAt = new Date().toISOString();
    return session;
  }

  /**
   * Add a message to the session context window.
   */
  addMessage(sessionId: string, message: AISessionMessage): void {
    const session = this.sessions.get(sessionId);
    if (!session || session.status !== 'active') return;

    session.contextWindow.push(message);
    session.interactionCount++;

    // Trim context window if it exceeds max size
    if (session.contextWindow.length > session.maxContextSize) {
      session.contextWindow = session.contextWindow.slice(-session.maxContextSize);
    }

    session.lastActiveAt = new Date().toISOString();
  }

  /**
   * Get the context window for a session (previous messages).
   */
  getContextWindow(sessionId: string): AISessionMessage[] {
    const session = this.sessions.get(sessionId);
    if (!session) return [];
    return [...session.contextWindow];
  }

  /**
   * Complete a session (mark as done).
   */
  completeSession(sessionId: string): void {
    const session = this.sessions.get(sessionId);
    if (session) {
      session.status = 'completed';
    }
  }

  /**
   * List all active sessions for a consultation.
   */
  getSessionsForConsultation(consultationId: string): AISession[] {
    return Array.from(this.sessions.values())
      .filter(s => s.consultationId === consultationId && s.status === 'active');
  }

  /**
   * Clean up expired sessions.
   */
  cleanupExpiredSessions(): number {
    let cleaned = 0;
    for (const [_id, session] of this.sessions) {
      if (this.isSessionExpired(session)) {
        session.status = 'expired';
        cleaned++;
      }
    }
    return cleaned;
  }

  private isSessionExpired(session: AISession): boolean {
    const lastActive = new Date(session.lastActiveAt).getTime();
    const now = Date.now();
    return now - lastActive > this.SESSION_TIMEOUT_MS;
  }
}

export const sessionManager = new SessionManager();
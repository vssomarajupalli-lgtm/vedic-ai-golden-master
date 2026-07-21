// Consultation Management Types
// GM-012A: Complete Consultation Workspace Implementation

import type { ChartProcessResponse, FinalReportSchema } from './schema';

export type ConsultationStatus = 'draft' | 'active' | 'completed' | 'archived';

export interface ConsultationClient {
  name: string;
  email?: string;
  phone?: string;
  birthData?: {
    date: string;
    time: string;
    place: string;
    latitude: number;
    longitude: number;
    timezone: string;
  };
}

export interface Consultation {
  id: string;
  clientId: string;
  client: ConsultationClient;
  name: string;
  status: ConsultationStatus;
  tags: string[];
  notes: string;
  horoscopeSource: 'horoscope_cleaner' | 'manual' | 'import';
  isPinned: boolean;
  isFavorite: boolean;
  
  // Chart data
  canonicalContent: any;
  machineIndex: any;
  
  // Engine outputs
  rawOutputs: ChartProcessResponse | null;
  report: FinalReportSchema | null;
  questionResults: any[];
  
  // Metadata
  createdAt: string;
  updatedAt: string;
  completedAt?: string;
  lastOpenedAt?: string;
  
  // Auto-save tracking
  autoSaveVersion: number;
  hasUnsavedChanges: boolean;
}

export interface ConsultationCreateInput {
  clientId: string;
  client?: ConsultationClient;
  name: string;
  canonicalContent?: any;
  machineIndex?: any;
  rawOutputs?: ChartProcessResponse | null;
  report?: FinalReportSchema | null;
  questionResults?: any[];
  horoscopeSource?: Consultation['horoscopeSource'];
  tags?: string[];
  notes?: string;
  status?: ConsultationStatus;
}

export interface ConsultationUpdateInput {
  name?: string;
  status?: ConsultationStatus;
  tags?: string[];
  notes?: string;
  canonicalContent?: any;
  machineIndex?: any;
  rawOutputs?: ChartProcessResponse | null;
  report?: FinalReportSchema | null;
  questionResults?: any[];
  client?: { name?: string; email?: string; phone?: string; birthData?: ConsultationClient['birthData'] };
  updatedAt?: string;
  isFavorite?: boolean;
}

export interface ConsultationSearchFilters {
  text?: string;
  clientId?: string;
  status?: ConsultationStatus;
  tags?: string[];
  dateFrom?: string;
  dateTo?: string;
}

export interface ConsultationSortConfig {
  field: 'createdAt' | 'updatedAt' | 'name' | 'status';
  direction: 'asc' | 'desc';
}

export type ViewMode = 'grid' | 'list';

export const DEFAULT_CONSULTATION_STATUS: ConsultationStatus = 'draft';

export function createConsultation(input: ConsultationCreateInput): Consultation {
  const now = new Date().toISOString();
  return {
    id: crypto.randomUUID(),
    clientId: input.clientId,
    client: input.client || { name: '' },
    name: input.name,
    status: input.status || DEFAULT_CONSULTATION_STATUS,
    tags: input.tags || [],
    notes: input.notes || '',
    horoscopeSource: input.horoscopeSource || 'horoscope_cleaner',
    isPinned: false,
    isFavorite: false,
    canonicalContent: input.canonicalContent,
    machineIndex: input.machineIndex,
    rawOutputs: input.rawOutputs || null,
    report: input.report || null,
    questionResults: input.questionResults || [],
    createdAt: now,
    updatedAt: now,
    autoSaveVersion: 0,
    hasUnsavedChanges: false,
  };
}

export function updateConsultation(
  consultation: Consultation,
  input: ConsultationUpdateInput
): Consultation {
  const now = new Date().toISOString();
  const updated: Consultation = {
    ...consultation,
    ...input,
    updatedAt: now,
    autoSaveVersion: consultation.autoSaveVersion + 1,
    hasUnsavedChanges: true,
    // Ensure client is always a valid ConsultationClient
    client: input.client 
      ? { ...consultation.client, ...input.client, name: input.client.name || consultation.client.name }
      : consultation.client,
  };
  
  if (input.status === 'completed' && consultation.status !== 'completed') {
    updated.completedAt = now;
  }
  
  return updated;
}

export function markConsultationSaved(consultation: Consultation): Consultation {
  return {
    ...consultation,
    hasUnsavedChanges: false,
  };
}

export function markConsultationOpened(consultation: Consultation): Consultation {
  return {
    ...consultation,
    lastOpenedAt: new Date().toISOString(),
  };
}
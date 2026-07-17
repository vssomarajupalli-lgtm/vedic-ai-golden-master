// BKL-008C.1 — Client Management Foundation
// Client Domain Types

export type ClientStatus = 'active' | 'inactive' | 'archived';

export interface ClientAudit {
  createdAt: string;
  updatedAt: string;
  version: number;
}

export interface Client {
  id: string;
  name: string;
  email?: string;
  phone?: string;
  notes?: string;
  tags: string[];
  status: ClientStatus;
  consultationIds: string[];
  lastConsultationDate?: string;
  createdAt: string;
  updatedAt: string;
  audit: ClientAudit;
  birthDataHash?: string;
  version: number;
}

export type ClientProfile = Client;

export interface ClientCreateInput {
  name: string;
  email?: string;
  phone?: string;
  notes?: string;
  status?: ClientStatus;
  tags?: string[];
  birthDataHash?: string;
}

export interface ClientUpdateInput {
  name?: string;
  email?: string;
  phone?: string;
  notes?: string;
  status?: ClientStatus;
  tags?: string[];
}

export interface ClientSearchFilters {
  text?: string;
  tags?: string[];
  status?: ClientStatus;
  query?: string;
}

export interface ClientSearchQuery {
  text?: string;
  tags?: string[];
  status?: ClientStatus;
}

export const DEFAULT_CLIENT_STATUS: ClientStatus = 'active';
// BKL-008C.1 — Client Management Foundation
// Client Repository: Zustand store with search, persistence, and CRUD

import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { v4 as uuidv4 } from 'uuid';
import type { ClientStatus, ClientProfile, ClientSearchFilters, ClientCreateInput, ClientAudit } from '../../types/client';

export interface ClientRepositoryState {
  clients: ClientProfile[];
  version: number;

  // CRUD
  createClient: (client: ClientCreateInput) => string;
  updateClient: (id: string, updates: Partial<Omit<ClientProfile, 'id' | 'createdAt' | 'audit'>>) => void;
  deleteClient: (id: string) => boolean;
  restoreClient: (id: string) => boolean;
  getClient: (id: string) => ClientProfile | undefined;
  getClientByBirthHash: (hash: string) => ClientProfile | undefined;
  getClientsByStatus: (status: ClientStatus) => ClientProfile[];
  getClientsByTag: (tag: string) => ClientProfile[];
  getAllClients: () => ClientProfile[];

  // Search
  search: (filters: ClientSearchFilters) => ClientProfile[];
  searchClients: (query: string) => ClientProfile[];
  searchClientsByTags: (tags: string[]) => ClientProfile[];

  // Status
  setClientStatus: (id: string, status: ClientStatus) => void;
  archiveClient: (id: string) => void;
  activateClient: (id: string) => void;

  // Tag management
  addTag: (id: string, tag: string) => void;
  removeTag: (id: string, tag: string) => void;
  clearTags: (id: string) => void;

  // Consultation linkage
  linkConsultation: (clientId: string, consultationId: string) => void;
  unlinkConsultation: (clientId: string, consultationId: string) => void;
  getClientConsultations: (clientId: string) => string[];
  getClientsByConsultationId: (consultationId: string) => ClientProfile[];

  // Tag utilities
  getAllTags: () => string[];

  // Stats
  getStats: () => { total: number; active: number; inactive: number; archived: number };

  // Version
  getVersion: () => number;
  incrementVersion: () => void;
}

function createClientProfile(input: ClientCreateInput): ClientProfile {
  const id = uuidv4();
  const now = new Date().toISOString();
  const audit: ClientAudit = {
    createdAt: now,
    updatedAt: now,
    version: 1,
  };
  return {
    ...input,
    id,
    email: input.email || undefined,
    phone: input.phone || undefined,
    notes: input.notes || undefined,
    status: input.status || 'active',
    tags: input.tags || [],
    consultationIds: [],
    createdAt: now,
    updatedAt: now,
    audit,
    version: 1,
  };
}

export const useClientRepository = create<ClientRepositoryState>()(
  persist(
    (set, get) => ({
      clients: [],
      version: 1,

      createClient: (input) => {
        const newClient = createClientProfile(input);
        set(state => ({ clients: [...state.clients, newClient] }));
        return newClient.id;
      },

      updateClient: (id, updates) => {
        set(state => ({
          clients: state.clients.map(c =>
            c.id === id
              ? {
                  ...c,
                  ...updates,
                  updatedAt: new Date().toISOString(),
                  audit: { ...c.audit, updatedAt: new Date().toISOString(), version: c.audit.version + 1 },
                }
              : c
          ),
        }));
      },

      deleteClient: (id) => {
        const client = get().clients.find(c => c.id === id);
        if (!client) return false;
        set(state => ({
          clients: state.clients.filter(c => c.id !== id),
        }));
        return true;
      },

      restoreClient: (id) => {
        const client = get().clients.find(c => c.id === id);
        if (!client || client.status !== 'archived') return false;
        set(state => ({
          clients: state.clients.map(c =>
            c.id === id ? { ...c, status: 'active' as ClientStatus, updatedAt: new Date().toISOString() } : c
          ),
        }));
        return true;
      },

      getClient: (id) => get().clients.find(c => c.id === id),

      getClientByBirthHash: (hash) => get().clients.find(c => c.birthDataHash === hash),

      getClientsByStatus: (status) => get().clients.filter(c => c.status === status),

      getClientsByTag: (tag) =>
        get().clients.filter(c => c.tags.includes(tag)),

      getAllClients: () => get().clients,

      search: (filters) => {
        let results = [...get().clients];

        if (filters.query) {
          const lower = filters.query.toLowerCase();
          results = results.filter(c =>
            c.name.toLowerCase().includes(lower) ||
            (c.email && c.email.toLowerCase().includes(lower)) ||
            (c.phone && c.phone.toLowerCase().includes(lower)) ||
            c.tags.some(t => t.toLowerCase().includes(lower))
          );
        }
        if (filters.status) {
          results = results.filter(c => c.status === filters.status);
        }
        if (filters.tags && filters.tags.length > 0) {
          const tagSet = new Set(filters.tags.map(t => t.toLowerCase()));
          results = results.filter(c =>
            c.tags.some(t => tagSet.has(t.toLowerCase()))
          );
        }
        return results.sort((a, b) => a.name.localeCompare(b.name));
      },

      searchClients: (query) => {
        const lower = query.toLowerCase();
        return get().clients.filter(c =>
          c.name.toLowerCase().includes(lower) ||
          (c.email && c.email.toLowerCase().includes(lower)) ||
          (c.phone && c.phone.toLowerCase().includes(lower)) ||
          c.tags.some(t => t.toLowerCase().includes(lower))
        );
      },

      searchClientsByTags: (tags) => {
        if (!tags.length) return get().clients;
        const tagSet = new Set(tags.map(t => t.toLowerCase()));
        return get().clients.filter(c =>
          c.tags.some(t => tagSet.has(t.toLowerCase()))
        );
      },

      setClientStatus: (id, status) => {
        set(state => ({
          clients: state.clients.map(c =>
            c.id === id
              ? {
                  ...c,
                  status,
                  updatedAt: new Date().toISOString(),
                  audit: { ...c.audit, updatedAt: new Date().toISOString(), version: c.audit.version + 1 },
                }
              : c
          ),
        }));
      },

      archiveClient: (id) => {
        get().setClientStatus(id, 'archived');
      },

      activateClient: (id) => {
        get().setClientStatus(id, 'active');
      },

      addTag: (id, tag) => {
        set(state => ({
          clients: state.clients.map(c =>
            c.id === id && !c.tags.includes(tag)
              ? {
                  ...c,
                  tags: [...c.tags, tag],
                  updatedAt: new Date().toISOString(),
                  audit: { ...c.audit, updatedAt: new Date().toISOString(), version: c.audit.version + 1 },
                }
              : c
          ),
        }));
      },

      removeTag: (id, tag) => {
        set(state => ({
          clients: state.clients.map(c =>
            c.id === id
              ? {
                  ...c,
                  tags: c.tags.filter(t => t !== tag),
                  updatedAt: new Date().toISOString(),
                  audit: { ...c.audit, updatedAt: new Date().toISOString(), version: c.audit.version + 1 },
                }
              : c
          ),
        }));
      },

      clearTags: (id) => {
        set(state => ({
          clients: state.clients.map(c =>
            c.id === id
              ? {
                  ...c,
                  tags: [],
                  updatedAt: new Date().toISOString(),
                  audit: { ...c.audit, updatedAt: new Date().toISOString(), version: c.audit.version + 1 },
                }
              : c
          ),
        }));
      },

      linkConsultation: (clientId, consultationId) => {
        set(state => ({
          clients: state.clients.map(c =>
            c.id === clientId && !c.consultationIds.includes(consultationId)
              ? {
                  ...c,
                  consultationIds: [...c.consultationIds, consultationId],
                  lastConsultationDate: new Date().toISOString(),
                  updatedAt: new Date().toISOString(),
                  audit: { ...c.audit, updatedAt: new Date().toISOString(), version: c.audit.version + 1 },
                }
              : c
          ),
        }));
      },

      unlinkConsultation: (clientId, consultationId) => {
        set(state => ({
          clients: state.clients.map(c =>
            c.id === clientId
              ? {
                  ...c,
                  consultationIds: c.consultationIds.filter(id => id !== consultationId),
                  updatedAt: new Date().toISOString(),
                  audit: { ...c.audit, updatedAt: new Date().toISOString(), version: c.audit.version + 1 },
                }
              : c
          ),
        }));
      },

      getClientConsultations: (clientId) => {
        const client = get().clients.find(c => c.id === clientId);
        return client?.consultationIds || [];
      },

      getClientsByConsultationId: (consultationId) => {
        return get().clients.filter(c => c.consultationIds.includes(consultationId));
      },

      getAllTags: () => {
        const tagSet = new Set<string>();
        get().clients.forEach(c => c.tags.forEach(t => tagSet.add(t)));
        return Array.from(tagSet).sort();
      },

      getStats: () => {
        const clients = get().clients;
        return {
          total: clients.length,
          active: clients.filter(c => c.status === 'active').length,
          inactive: clients.filter(c => c.status === 'inactive').length,
          archived: clients.filter(c => c.status === 'archived').length,
        };
      },

      getVersion: () => get().version,
      incrementVersion: () => set(state => ({ version: state.version + 1 })),
    }),
    { name: 'client-repository', storage: createJSONStorage(() => localStorage) }
  )
);
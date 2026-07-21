// Consultation Store with localStorage Persistence
// GM-012B: Persistent Consultation Management

import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { 
  Consultation, 
  ConsultationCreateInput, 
  ConsultationUpdateInput,
  ConsultationSearchFilters,
  ConsultationSortConfig 
} from '../types/consultation';
import type { Client } from '../types/client';
import { createConsultation, updateConsultation, markConsultationSaved, markConsultationOpened } from '../types/consultation';

const STORAGE_KEY = 'vedic-ai-consultations';
const MAX_CONSULTATIONS = 500;

interface ConsultationState {
  // Data
  consultations: Consultation[];
  clients: Client[];
  
  // UI State
  selectedConsultationId: string | null;
  searchFilters: ConsultationSearchFilters;
  sortConfig: ConsultationSortConfig;
  viewMode: 'grid' | 'list';
  
  // Actions - Consultations
  createConsultation: (input: ConsultationCreateInput) => Consultation;
  getConsultation: (id: string) => Consultation | undefined;
  updateConsultation: (id: string, input: ConsultationUpdateInput) => void;
  deleteConsultation: (id: string) => void;
  archiveConsultation: (id: string) => void;
  restoreConsultation: (id: string) => void;
  duplicateConsultation: (id: string) => Consultation;
  
  // Actions - Client linkage
  setClients: (clients: Client[]) => void;
  getConsultationsByClient: (clientId: string) => Consultation[];
  
  // Actions - Selection
  selectConsultation: (id: string | null) => void;
  openConsultation: (id: string) => Consultation;
  setActiveConsultation: (id: string) => void;
  getActiveConsultation: () => Consultation | undefined;
  
  // Actions - Tag management
  addTag: (id: string, tag: string) => void;
  removeTag: (id: string, tag: string) => void;
  togglePin: (id: string) => void;
  
  // Actions - Client
  updateClient: (id: string, client: Partial<Consultation['client']>) => void;
  getAllTags: () => string[];
  
  // Actions - Auto-save
  autoSaveConsultation: (id: string) => void;
  markSaved: (id: string) => void;
  
  // Actions - Search/Sort/Filter
  setSearchFilters: (filters: Partial<ConsultationSearchFilters>) => void;
  clearSearchFilters: () => void;
  setSortConfig: (config: ConsultationSortConfig) => void;
  setViewMode: (mode: 'grid' | 'list') => void;
  
  // Computed
  getFilteredConsultations: () => Consultation[];
  getRecentConsultations: (limit?: number) => Consultation[];
  getPinnedConsultations: () => Consultation[];
  
  // Actions - Bulk
  deleteMultiple: (ids: string[]) => void;
  archiveMultiple: (ids: string[]) => void;
  
  // Actions - Import/Export
  exportConsultations: () => string;
  importConsultations: (json: string) => { success: number; failed: number };
  
  // Actions - Reset
  clearAll: () => void;
}

const DEFAULT_SORT: ConsultationSortConfig = { field: 'updatedAt', direction: 'desc' };
const DEFAULT_FILTERS: ConsultationSearchFilters = {};

export const useConsultationStore = create<ConsultationState>()(
  persist(
    (set, get) => ({
      // Initial State
      consultations: [],
      clients: [],
      selectedConsultationId: null,
      searchFilters: DEFAULT_FILTERS,
      sortConfig: DEFAULT_SORT,
      viewMode: 'grid',
      
      // --- Consultation CRUD ---
      
      createConsultation: (input) => {
        const consultation = createConsultation(input);
        set((state) => ({
          consultations: [consultation, ...state.consultations].slice(0, MAX_CONSULTATIONS),
          selectedConsultationId: consultation.id,
        }));
        return consultation;
      },
      
      getConsultation: (id) => {
        return get().consultations.find(c => c.id === id);
      },
      
      updateConsultation: (id, input) => {
        set((state) => ({
          consultations: state.consultations.map(c => 
            c.id === id ? updateConsultation(c, input) : c
          ),
        }));
      },
      
      deleteConsultation: (id) => {
        set((state) => ({
          consultations: state.consultations.filter(c => c.id !== id),
          selectedConsultationId: state.selectedConsultationId === id ? null : state.selectedConsultationId,
        }));
      },
      
      archiveConsultation: (id) => {
        get().updateConsultation(id, { status: 'archived' });
      },
      
      restoreConsultation: (id) => {
        get().updateConsultation(id, { status: 'draft' });
      },
      
      duplicateConsultation: (id) => {
        const original = get().getConsultation(id);
        if (!original) throw new Error('Consultation not found');
        
        const duplicate: Consultation = {
          ...original,
          id: crypto.randomUUID(),
          name: `${original.name} (Copy)`,
          status: 'draft',
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          completedAt: undefined,
          lastOpenedAt: undefined,
          autoSaveVersion: 0,
          hasUnsavedChanges: false,
          isFavorite: false,
        };
        
        set((state) => ({
          consultations: [duplicate, ...state.consultations].slice(0, MAX_CONSULTATIONS),
          selectedConsultationId: duplicate.id,
        }));
        
        return duplicate;
      },
      
      // --- Client Linkage ---
      
      setClients: (clients) => set({ clients }),
      
      getConsultationsByClient: (clientId) => {
        return get().consultations.filter(c => c.clientId === clientId);
      },
      
      // --- Selection ---
      
      selectConsultation: (id) => set({ selectedConsultationId: id }),
      
      openConsultation: (id) => {
        const consultation = get().getConsultation(id);
        if (!consultation) throw new Error('Consultation not found');
        
        const opened = markConsultationOpened(consultation);
        set((state) => ({
          consultations: state.consultations.map(c => c.id === id ? opened : c),
          selectedConsultationId: id,
        }));
        
        return opened;
      },
      
      setActiveConsultation: (id) => set({ selectedConsultationId: id }),
      
      getActiveConsultation: () => {
        const { selectedConsultationId } = get();
        return selectedConsultationId ? get().getConsultation(selectedConsultationId) : undefined;
      },
      
      // --- Tag management ---
      
      addTag: (id, tag) => {
        set((state) => ({
          consultations: state.consultations.map(c => 
            c.id === id && !c.tags.includes(tag)
              ? { ...c, tags: [...c.tags, tag], updatedAt: new Date().toISOString() }
              : c
          ),
        }));
      },
      
      removeTag: (id, tag) => {
        set((state) => ({
          consultations: state.consultations.map(c => 
            c.id === id
              ? { ...c, tags: c.tags.filter(t => t !== tag), updatedAt: new Date().toISOString() }
              : c
          ),
        }));
      },
      
      togglePin: (id) => {
        set((state) => ({
          consultations: state.consultations.map(c => 
            c.id === id
              ? { ...c, isPinned: !c.isPinned, updatedAt: new Date().toISOString() }
              : c
          ),
        }));
      },
      
      // Actions - Client
      updateClient: (id, clientData) => {
        set((state) => ({
          consultations: state.consultations.map(c => 
            c.id === id 
              ? { ...c, client: { ...c.client, ...clientData }, updatedAt: new Date().toISOString() }
              : c
          ),
        }));
      },
      
      autoSaveConsultation: (id) => {
        set((state) => ({
          consultations: state.consultations.map(c => 
            c.id === id && c.hasUnsavedChanges 
              ? { ...c, hasUnsavedChanges: false, autoSaveVersion: c.autoSaveVersion + 1 }
              : c
          ),
        }));
      },
      
      markSaved: (id) => {
        set((state) => ({
          consultations: state.consultations.map(c => 
            c.id === id ? markConsultationSaved(c) : c
          ),
        }));
      },
      
      // --- Search/Sort/Filter ---
      
      setSearchFilters: (filters) => set((state) => ({
        searchFilters: { ...state.searchFilters, ...filters },
      })),
      
      clearSearchFilters: () => set({ searchFilters: DEFAULT_FILTERS }),
      
      setSortConfig: (config) => set({ sortConfig: config }),
      
      setViewMode: (mode) => set({ viewMode: mode }),
      
      getFilteredConsultations: () => {
        const { consultations, searchFilters, sortConfig } = get();
        let filtered = [...consultations];
        
        // Filter by text
        if (searchFilters.text) {
          const lower = searchFilters.text.toLowerCase();
          filtered = filtered.filter(c => 
            c.name.toLowerCase().includes(lower) ||
            c.notes.toLowerCase().includes(lower) ||
            c.tags.some(t => t.toLowerCase().includes(lower))
          );
        }
        
        // Filter by client
        if (searchFilters.clientId) {
          filtered = filtered.filter(c => c.clientId === searchFilters.clientId);
        }
        
        // Filter by status
        if (searchFilters.status) {
          filtered = filtered.filter(c => c.status === searchFilters.status);
        }
        
        // Filter by tags
        if (searchFilters.tags && searchFilters.tags.length > 0) {
          filtered = filtered.filter(c => 
            searchFilters.tags!.some(t => c.tags.includes(t))
          );
        }
        
        // Filter by date range
        if (searchFilters.dateFrom) {
          filtered = filtered.filter(c => c.createdAt >= searchFilters.dateFrom!);
        }
        if (searchFilters.dateTo) {
          filtered = filtered.filter(c => c.createdAt <= searchFilters.dateTo!);
        }
        
        // Sort
        filtered.sort((a, b) => {
          let aVal: any = a[sortConfig.field];
          let bVal: any = b[sortConfig.field];
          
          if (sortConfig.field === 'createdAt' || sortConfig.field === 'updatedAt') {
            aVal = new Date(aVal).getTime();
            bVal = new Date(bVal).getTime();
          }
          
          if (aVal < bVal) return sortConfig.direction === 'asc' ? -1 : 1;
          if (aVal > bVal) return sortConfig.direction === 'asc' ? 1 : -1;
          return 0;
        });
        
        return filtered;
      },
      
      // Computed - Recent & Pinned
      getRecentConsultations: (limit = 5) => {
        return [...get().consultations]
          .sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime())
          .slice(0, limit);
      },
      
      getPinnedConsultations: () => {
        return get().consultations
          .filter(c => c.isPinned)
          .sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime());
      },
      
      // Computed - Tags
      getAllTags: () => {
        const allTags = new Set<string>();
        get().consultations.forEach(c => c.tags.forEach(t => allTags.add(t)));
        return Array.from(allTags).sort();
      },
      
      // --- Bulk Actions ---
      
      deleteMultiple: (ids) => {
        set((state) => ({
          consultations: state.consultations.filter(c => !ids.includes(c.id)),
          selectedConsultationId: ids.includes(state.selectedConsultationId || '') ? null : state.selectedConsultationId,
        }));
      },
      
      archiveMultiple: (ids) => {
        set((state) => ({
          consultations: state.consultations.map(c => 
            ids.includes(c.id) ? { ...c, status: 'archived' as const, updatedAt: new Date().toISOString() } : c
          ),
        }));
      },
      
      // --- Import/Export ---
      
      exportConsultations: () => {
        const { consultations } = get();
        return JSON.stringify(consultations, null, 2);
      },
      
      importConsultations: (json) => {
        try {
          const imported = JSON.parse(json);
          if (!Array.isArray(imported)) throw new Error('Invalid format');
          
          let success = 0;
          let failed = 0;
          
          for (const c of imported) {
            if (c.id && c.clientId && c.name) {
              set((state) => {
                const exists = state.consultations.some(ex => ex.id === c.id);
                if (!exists) {
                  success++;
                  return { consultations: [c, ...state.consultations].slice(0, MAX_CONSULTATIONS) };
                }
                failed++;
                return state;
              });
            } else {
              failed++;
            }
          }
          
          return { success, failed };
        } catch {
          return { success: 0, failed: 1 };
        }
      },
      
      // --- Reset ---
      
      clearAll: () => set({ 
        consultations: [], 
        selectedConsultationId: null,
        searchFilters: DEFAULT_FILTERS,
      }),
    }),
    {
      name: STORAGE_KEY,
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        consultations: state.consultations,
        clients: state.clients,
        searchFilters: state.searchFilters,
        sortConfig: state.sortConfig,
        viewMode: state.viewMode,
      }),
      version: 1,
      migrate: (persistedState: any, version: number) => {
        if (version === 0) {
          // Migration from v0 to v1
          return {
            ...persistedState,
            consultations: persistedState.consultations?.map((c: any) => ({
              ...c,
              autoSaveVersion: c.autoSaveVersion || 0,
              hasUnsavedChanges: c.hasUnsavedChanges || false,
              horoscopeSource: c.horoscopeSource || 'horoscope_cleaner',
              tags: c.tags || [],
            })) || [],
          };
        }
        return persistedState;
      },
    }
  )
);

// Selector hooks for performance
export const useConsultations = () => useConsultationStore((s) => s.consultations);
export const useSelectedConsultation = () => useConsultationStore((s) => 
  s.selectedConsultationId ? s.consultations.find(c => c.id === s.selectedConsultationId) : null
);
export const useFilteredConsultations = () => useConsultationStore((s) => s.getFilteredConsultations());
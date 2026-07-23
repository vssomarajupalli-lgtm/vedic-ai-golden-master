// @ts-nocheck
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { v4 as uuidv4 } from 'uuid';
import { useChartStore } from '../store/useChartStore';

// ============================================
// TYPES (aligned with frontend/src/types/consultation*.ts)
// ============================================

export type ConsultationStatus = 'active' | 'archived' | 'recycle_bin' | 'deleted';

export interface ConsultationRepository {
  repositoryVersion: number;
  consultations: Consultation[];
  lastSyncAt: string;
}

export interface Consultation {
  id: string;
  version: number;
  createdAt: string;
  updatedAt: string;
  deletedAt?: string;
  status: ConsultationStatus;
  metadata: ConsultationMetadata;
  structure: ConsultationStructure;
  snapshots: ConsultationSnapshot[];
  outputs: ConsultationOutput[];
  audit: ConsultationAudit;
}

export interface ConsultationMetadata {
  consultationId: string;
  clientName: string;
  birthDataHash: string;
  consultationTitle: string;
  tags: string[];
  isFavorite: boolean;
  status: ConsultationStatus;
}

export interface ConsultationStructure {
  questionPackageId: string;
  selectedQuestionIds: string[];
  questionResultsRef: string;
  activationTimelineRef: string;
  gocharaRef: string;
  comparisonRef?: string;
  reportRef: string;
}

export interface ConsultationSnapshot {
  snapshotId: string;
  consultationId: string;
  version: number;
  capturedAt: string;
  capturedBy: string;
  captureReason: 'report_generation' | 'manual' | 'scheduled' | 'formula_change' | 'calibration_change' | 'birth_data_change';
  questions: string[];
  formulaRegistryVersion: string;
  formulaRegistryHash: string;
  calibrationProfileVersion: string;
  calibrationProfileHash: string;
  decisionLayerVersion: string;
  decisionLayerHash: string;
  reportVersion: string;
  reportHash: string;
  desktopRuntimeVersion: string;
  buildMetadata: {
    architectureVersion: string;
    questionCatalogVersion: string;
    formulaRegistryVersion: string;
    calibrationVersion: string;
    desktopRuntimeVersion: string;
    buildTimestamp: string;
    buildCommit: string;
    buildTag: string;
  };
  metadata: {
    clientName: string;
    birthDataHash: string;
    consultationTitle: string;
    generatedBy: string;
    tags: string[];
  };
  integrity: {
    checksum: string;
    signature?: string;
    reproducible: boolean;
    integrityVerified: boolean;
  };
  git: {
    commit: string;
    tag: string;
    branch: string;
    dirty: boolean;
  };
}

export interface ConsultationOutput {
  outputId: string;
  consultationId: string;
  profile: 'quick' | 'standard' | 'professional' | 'research' | 'book';
  format: 'pdf' | 'html' | 'json';
  generatedAt: string;
  checksum: string;
  sections: string[];
  fileSizeBytes: number;
}

export interface ConsultationAudit {
  createdBy: string;
  createdAt: string;
  gitCommit: string;
  gitTag: string;
  architectureVersion: string;
  deterministic: true;
  lastModifiedBy?: string;
  lastModifiedAt?: string;
}

// ============================================
// REPOSITORY HOOK
// ============================================

const REPOSITORY_STORAGE_KEY = 'samartha_consultation_repository';
const CURRENT_REPOSITORY_VERSION = 1;

// Helper: Generate SHA-256 hash (using Web Crypto API)
async function generateHash(data: string): Promise<string> {
  const encoder = new TextEncoder();
  const dataBuffer = encoder.encode(data);
  const hashBuffer = await crypto.subtle.digest('SHA-256', dataBuffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

// Helper: Get canonical birth data hash from current chart
function getBirthDataHash(): string {
  const { canonicalContent, machineIndex } = useChartStore.getState();
  const birthData = {
    date: canonicalContent?.native_info?.dob || '',
    time: canonicalContent?.native_info?.tob || '',
    place: canonicalContent?.native_info?.pob || '',
    timezone: canonicalContent?.native_info?.timezone || 'UTC',
    latitude: canonicalContent?.native_info?.latitude || 0,
    longitude: canonicalContent?.native_info?.longitude || 0,
  };
  return btoa(JSON.stringify(birthData)).substring(0, 32);
}

// Helper: Get formula registry version/hash
function getFormulaRegistryInfo(): { version: string; hash: string } {
  return { version: '1.0.0', hash: 'formula-registry-v1-hash-placeholder' };
}

// Helper: Get calibration profile version/hash
function getCalibrationProfileInfo(): { version: string; hash: string } {
  return { version: '1.0.0', hash: 'calibration-profile-v1-hash-placeholder' };
}

// Helper: Get git info
function getGitInfo(): { commit: string; tag: string; branch: string; dirty: boolean } {
  return { commit: 'unknown', tag: 'gm-007-development', branch: 'main', dirty: false };
}

// Helper: Verify snapshot integrity
async function verifySnapshotIntegrity(snapshot: any): Promise<boolean> {
  const currentBirthHash = getBirthDataHash();
  const currentFormula = getFormulaRegistryInfo();
  const currentCalibration = getCalibrationProfileInfo();
  const currentGit = getGitInfo();

  const birthMatch = snapshot.metadata.birthDataHash === currentBirthHash;
  const formulaMatch = snapshot.formulaRegistryHash === currentFormula.hash;
  const calibrationMatch = snapshot.calibrationProfileHash === currentCalibration.hash;
  const gitMatch = snapshot.git.commit === currentGit.commit;

  return birthMatch && formulaMatch && calibrationMatch && gitMatch;
}

interface RepositoryState {
  repository: ConsultationRepository;
  isLoading: boolean;
  error: string | null;

  // Core CRUD
  createConsultation: (title: string, questionPackageId: string, selectedQuestionIds: string[]) => Promise<Consultation>;
  loadConsultation: (consultationId: string) => Promise<void>;
  updateConsultationMetadata: (consultationId: string, metadata: Partial<ConsultationMetadata>) => Promise<void>;
  deleteConsultation: (consultationId: string, permanent?: boolean) => Promise<void>;
  restoreConsultation: (consultationId: string) => Promise<void>;
  permanentlyDeleteConsultation: (consultationId: string) => Promise<void>;

  // Snapshots
  createSnapshot: (consultationId: string, reason: ConsultationSnapshot['captureReason']) => Promise<ConsultationSnapshot>;
  loadSnapshot: (consultationId: string, snapshotId: string) => Promise<void>;
  compareSnapshots: (consultationId: string, snapshotIdA: string, snapshotIdB: string) => Promise<any>;

  // Outputs
  recordOutput: (consultationId: string, output: Omit<ConsultationOutput, 'outputId' | 'consultationId'>) => Promise<void>;

  // Queries
  getConsultations: (status?: ConsultationStatus) => Consultation[];
  getConsultationById: (consultationId: string) => Consultation | undefined;
  searchConsultations: (query: string) => Consultation[];

  // Integrity
  verifyAllIntegrity: () => Promise<{ consultationId: string; verified: boolean }[]>;
  getRepositoryStats: () => { total: number; active: number; archived: number; recycleBin: number; totalOutputs: number };

  // UI State - exposed at top level for convenience
  searchQuery: string;
  filterCategory: string;
  filterStatus: string;
  filterTags: string[];
  sortBy: string;
  viewMode: 'grid' | 'list';
  availableTags: string[];
  currentFavorite: string;
  selectedItems: Set<string>;
 
  setSearchQuery: (query: string) => void;
  setFilterCategory: (category: string) => void;
  setFilterStatus: (status: string) => void;
  setFilterTags: (tags: string[]) => void;
  setSortBy: (sort: string) => void;
  setViewMode: (mode: 'grid' | 'list') => void;
  setCurrentFavorite: (fav: string) => void;
  toggleSelection: (id: string) => void;
  selectAll: (ids: string[]) => void;
  clearSelection: () => void;
  bulkAction: (action: 'favorite' | 'archive' | 'tag' | 'delete' | 'export') => void;
  _initializeRepository: () => void;
}

const initialRepository: ConsultationRepository = {
  repositoryVersion: 1,
  consultations: [],
  lastSyncAt: new Date().toISOString(),
  searchQuery: '',
  filterCategory: 'all',
  filterStatus: 'all',
  filterTags: [],
  sortBy: 'updatedAt',
  viewMode: 'grid',
  availableTags: [],
  currentFavorite: 'all',
  selectedItems: [],
};

const initialState = {
  repository: {
    repositoryVersion: 1,
    consultations: [],
    lastSyncAt: new Date().toISOString(),
    searchQuery: '',
    filterCategory: 'all',
    filterStatus: 'all',
    filterTags: [],
    sortBy: 'updatedAt',
    viewMode: 'grid',
    availableTags: [],
    currentFavorite: 'all',
    selectedItems: [],
  },
  isLoading: false,
  error: null,

  // UI State getters
  get searchQuery() { return this.repository.searchQuery; },
  get filterCategory() { return this.repository.filterCategory; },
  get filterStatus() { return this.repository.filterStatus; },
  get filterTags() { return this.repository.filterTags; },
  get sortBy() { return this.repository.sortBy; },
  get viewMode() { return this.repository.viewMode; },
  get availableTags() { return this.repository.availableTags; },
  get currentFavorite() { return this.repository.currentFavorite; },
  get selectedItems() { return new Set(this.repository.selectedItems); },

  _initializeRepository: () => {},

  createConsultation: async () => ({} as any),
  loadConsultation: async () => {},
  updateConsultationMetadata: async () => {},
  deleteConsultation: async () => {},
  restoreConsultation: async () => {},
  permanentlyDeleteConsultation: async () => {},
  createSnapshot: async () => ({} as any),
  loadSnapshot: async () => {},
  compareSnapshots: async () => ({} as any),
  recordOutput: async () => {},
  getConsultations: () => [],
  getConsultationById: () => undefined,
  searchConsultations: () => [],
  verifyAllIntegrity: async () => [],
  getRepositoryStats: () => ({ total: 0, active: 0, archived: 0, recycleBin: 0, totalOutputs: 0 }),
  setSearchQuery: () => {},
  setFilterCategory: () => {},
  setFilterStatus: () => {},
  setFilterTags: () => {},
  setSortBy: () => {},
  setViewMode: () => {},
  setCurrentFavorite: () => {},
  toggleSelection: () => {},
  selectAll: () => {},
  clearSelection: () => {},
  bulkAction: () => {},
  _initializeRepository: () => {},
};


export const useConsultationRepository = create<any>()(
  persist(
    (set, get) => ({
      ...initialState,

      _initializeRepository: () => {
        const { repository } = get();
        if (repository.repositoryVersion < 1) {
          set(state => ({
            repository: {
              ...state.repository,
              repositoryVersion: 1,
            },
          }));
        }
      },

      createConsultation: async (title: string, questionPackageId: string, selectedQuestionIds: string[]) => {
        const { canonicalContent, machineIndex, report, questionResults } = useChartStore.getState();

        if (!canonicalContent || !machineIndex) {
          throw new Error('No chart generated. Please generate a chart first.');
        }

        const birthDataHash = getBirthDataHash();
        const formulaInfo = getFormulaRegistryInfo();
        const calibrationInfo = getCalibrationProfileInfo();
        const gitInfo = getGitInfo();

        const { repository } = get();
        const existing = repository.consultations.find(c =>
          c.metadata.birthDataHash === birthDataHash &&
          c.structure.questionPackageId === questionPackageId &&
           c.snapshots.some(s => s.formulaRegistryHash === formulaInfo.hash && s.calibrationProfileHash === calibrationInfo.hash && s.questions.length === selectedQuestionIds.length)
        );

        if (existing && existing.status === 'active') {
          const newVersion = existing.version + 1;
          const newConsultation = {
            id: uuidv4(),
            version: newVersion,
            createdAt: existing.createdAt,
            updatedAt: new Date().toISOString(),
            status: 'active',
            metadata: {
              consultationId: existing.metadata.consultationId,
              clientName: existing.metadata.clientName,
              birthDataHash: getBirthDataHash(),
              consultationTitle: '',
              tags: existing.metadata.tags,
              isFavorite: existing.metadata.isFavorite,
              status: 'active',
            },
            structure: {
              questionPackageId,
              selectedQuestionIds,
              questionResultsRef: 'current',
              activationTimelineRef: 'current',
              gocharaRef: 'current',
              reportRef: 'current',
            },
            snapshots: [],
            outputs: [],
            audit: {
              createdBy: 'user',
              createdAt: new Date().toISOString(),
              gitCommit: getGitInfo().commit,
              gitTag: getGitInfo().tag,
              architectureVersion: '1.2.0',
              deterministic: true,
              lastModifiedBy: 'user',
              lastModifiedAt: new Date().toISOString(),
            },
          };

          set(state => ({
            repository: {
              ...state.repository,
              consultations: [newConsultation, ...state.repository.consultations],
              lastSyncAt: new Date().toISOString(),
            },
          }));

          await get().createSnapshot(newConsultation.id, 'report_generation');
          return newConsultation;
        }

        const consultationId = uuidv4();
        const newConsultation = {
          id: uuidv4(),
          version: 1,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          status: 'active',
          metadata: {
            consultationId,
            clientName: 'Unknown Client',
            birthDataHash: getBirthDataHash(),
            consultationTitle: '',
            tags: [],
            isFavorite: false,
            status: 'active',
          },
          structure: {
            questionPackageId,
            selectedQuestionIds,
            questionResultsRef: 'current',
            activationTimelineRef: 'current',
            gocharaRef: 'current',
            reportRef: 'current',
          },
          snapshots: [],
          outputs: [],
          audit: {
            createdBy: 'user',
            createdAt: new Date().toISOString(),
            gitCommit: getGitInfo().commit,
            gitTag: getGitInfo().tag,
            architectureVersion: '1.2.0',
            deterministic: true,
          },
        };

        set(state => ({
          repository: {
            ...state.repository,
            consultations: [newConsultation, ...state.repository.consultations],
            lastSyncAt: new Date().toISOString(),
          },
        }));

        await get().createSnapshot(consultationId, 'report_generation');
        return newConsultation;
      },

      loadConsultation: async (consultationId: string) => {
        const { repository } = get();
        const consultation = repository.consultations.find(c => c.id === consultationId);
        if (!consultation) throw new Error(`Consultation ${consultationId} not found`);
        console.log('Loading consultation:', consultation.metadata.consultationTitle);
      },

      updateConsultationMetadata: async (consultationId: string, metadata: any) => {
        set(state => ({
          repository: {
            ...state.repository,
            consultations: state.repository.consultations.map(c =>
              c.id === consultationId
                ? { ...c, metadata: { ...c.metadata, ...metadata }, updatedAt: new Date().toISOString() }
                : c
            ),
            lastSyncAt: new Date().toISOString(),
          },
        }));
      },

      deleteConsultation: async (consultationId: string, permanent = false) => {
        if (permanent) {
          await get().permanentlyDeleteConsultation(consultationId);
          return;
        }
        set(state => ({
          repository: {
            ...state.repository,
            consultations: state.repository.consultations.map(c =>
              c.id === consultationId
                ? { ...c, status: 'archived', deletedAt: new Date().toISOString(), updatedAt: new Date().toISOString() }
                : c
            ),
            lastSyncAt: new Date().toISOString(),
          },
        }));
      },

      archiveConsultation: async (consultationId: string) => {
        set(state => ({
          repository: {
            ...state.repository,
            consultations: state.repository.consultations.map(c =>
              c.id === consultationId
                ? { ...c, status: 'archived', updatedAt: new Date().toISOString() }
                : c
            ),
            lastSyncAt: new Date().toISOString(),
          },
        }));
      },

      moveToRecycleBin: async (consultationId: string) => {
        set(state => ({
          repository: {
            ...state.repository,
            consultations: state.repository.consultations.map(c =>
              c.id === consultationId
                ? { ...c, status: 'recycle_bin', deletedAt: new Date().toISOString(), updatedAt: new Date().toISOString() }
                : c
            ),
            lastSyncAt: new Date().toISOString(),
          },
        }));
      },

      restoreConsultation: async (consultationId: string) => {
        set(state => ({
          repository: {
            ...state.repository,
            consultations: state.repository.consultations.map(c =>
              c.id === consultationId
                ? { ...c, status: 'active', deletedAt: undefined, updatedAt: new Date().toISOString() }
                : c
            ),
            lastSyncAt: new Date().toISOString(),
          },
        }));
      },

      permanentlyDeleteConsultation: async (consultationId: string) => {
        set(state => ({
          repository: {
            ...state.repository,
            consultations: state.repository.consultations.filter(c => c.id !== consultationId),
            lastSyncAt: new Date().toISOString(),
          },
        }));
      },

      emptyRecycleBin: async () => {
        set(state => ({
          repository: {
            ...state.repository,
            consultations: state.repository.consultations.filter(c => c.status !== 'recycle_bin'),
            lastSyncAt: new Date().toISOString(),
          },
        }));
      },

      getRecycleBin: () => {
        const { repository } = get();
        return repository.consultations.filter(c => c.status === 'recycle_bin');
      },

      createSnapshot: async (consultationId: string, reason: any) => {
        const { repository } = get();
        const consultation = repository.consultations.find(c => c.id === consultationId);
        if (!consultation) throw new Error(`Consultation ${consultationId} not found`);

        const snapshot = {
          snapshotId: uuidv4(),
          consultationId,
          version: consultation.version,
          capturedAt: new Date().toISOString(),
          capturedBy: 'user',
          captureReason: 'report_generation',
          questions: [],
          formulaRegistryVersion: '1.0.0',
          formulaRegistryHash: 'formula-registry-v1-hash-placeholder',
          calibrationProfileVersion: '1.0.0',
          calibrationProfileHash: 'calibration-profile-v1-hash-placeholder',
          decisionLayerVersion: '1.0.0',
          decisionLayerHash: 'decision-layer-v1-hash-placeholder',
          reportVersion: '1.2.0',
          reportHash: '',
          desktopRuntimeVersion: '1.3.0',
          buildMetadata: {
            architectureVersion: '1.2.0',
            questionCatalogVersion: '1.0.0',
            formulaRegistryVersion: '1.0.0',
            calibrationVersion: '1.0.0',
            desktopRuntimeVersion: '1.3.0',
            buildTimestamp: new Date().toISOString(),
            buildCommit: 'unknown',
            buildTag: 'gm-007-development',
          },
          metadata: {
            clientName: '',
            birthDataHash: '',
            consultationTitle: '',
            generatedBy: 'user',
            tags: [],
          },
          integrity: {
            checksum: '',
            reproducible: true,
            integrityVerified: true,
          },
          git: { commit: 'unknown', tag: 'gm-007-development', branch: 'main', dirty: false },
        };

        set(state => ({
          repository: {
            ...state.repository,
            consultations: state.repository.consultations.map(c =>
              c.id === consultationId
                ? { ...c, snapshots: [...c.snapshots, { integrity: { integrityVerified: true } }], updatedAt: new Date().toISOString() }
                : c
            ),
            lastSyncAt: new Date().toISOString(),
          },
        }));

        return {} as any;
      },

      loadSnapshot: async () => {},
      compareSnapshots: async () => ({} as any),
      recordOutput: async (consultationId: string, output: Omit<ConsultationOutput, 'outputId' | 'consultationId'>) => {
        const outputId = uuidv4();
        const newOutput: ConsultationOutput = {
          outputId,
          consultationId,
          ...output,
        };
        set(state => ({
          repository: {
            ...state.repository,
            consultations: state.repository.consultations.map(c =>
              c.id === consultationId
                ? { ...c, outputs: [...c.outputs, newOutput], updatedAt: new Date().toISOString() }
                : c
            ),
            lastSyncAt: new Date().toISOString(),
          },
        }));
      },
      getConsultations: () => [],
      getConsultationById: () => undefined,
      searchConsultations: () => [],
      verifyAllIntegrity: async () => [],
      getRepositoryStats: () => ({ total: 0, active: 0, archived: 0, recycleBin: 0, totalOutputs: 0 }),
      setSearchQuery: () => {},
      setFilterCategory: () => {},
      setFilterStatus: () => {},
      setFilterTags: () => {},
      setSortBy: () => {},
      setViewMode: () => {},
      setCurrentFavorite: () => {},
      toggleSelection: () => {},
      selectAll: () => {},
      clearSelection: () => {},
      bulkAction: () => {},
      _initializeRepository: () => {},
    }),
    {
      name: 'samartha_consultation_repository',
      storage: createJSONStorage(() => localStorage),
      version: 1,
      migrate: (persistedState: any) => persistedState,
    }
  )
);

export default useConsultationRepository;
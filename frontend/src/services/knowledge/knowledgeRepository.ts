// BKL-008B — Deterministic Knowledge Graph Platform
// Knowledge Repository: Zustand store with search, index, and integrity

import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { v4 as uuidv4 } from 'uuid';
import type { KnowledgeNode, KnowledgeRelationship, KnowledgeNodeType, KnowledgeRelationshipType } from './nodeRegistry';

export interface KnowledgeIndex {
  /** Index nodes by type */
  byType: Map<KnowledgeNodeType, string[]>;
  /** Index nodes by domain */
  byDomain: Map<string, string[]>;
  /** Index nodes by source */
  bySource: Map<string, string[]>;
  /** Full-text search index */
  searchIndex: Map<string, string[]>;
}

export interface KnowledgeRepositoryState {
  nodes: KnowledgeNode[];
  relationships: KnowledgeRelationship[];
  version: number;

  // Node CRUD
  addNode: (node: Omit<KnowledgeNode, 'id' | 'createdAt' | 'updatedAt'>) => string;
  updateNode: (id: string, updates: Partial<KnowledgeNode>) => void;
  removeNode: (id: string) => void;
  getNode: (id: string) => KnowledgeNode | undefined;
  getNodesByType: (type: KnowledgeNodeType) => KnowledgeNode[];
  getNodesByDomain: (domain: string) => KnowledgeNode[];
  getNodesBySource: (source: string) => KnowledgeNode[];

  // Relationship CRUD
  addRelationship: (rel: Omit<KnowledgeRelationship, 'id' | 'createdAt'>) => string;
  removeRelationship: (id: string) => void;
  getRelationships: (nodeId: string) => KnowledgeRelationship[];
  getRelationshipsByType: (type: KnowledgeRelationshipType) => KnowledgeRelationship[];

  // Search
  search: (query: string) => KnowledgeNode[];
  searchByType: (query: string, type: KnowledgeNodeType) => KnowledgeNode[];

  // Index
  rebuildIndex: () => void;
  getIndex: () => KnowledgeIndex;

  // Integrity
  validateIntegrity: () => { valid: boolean; issues: string[] };

  // Version
  getVersion: () => number;
  incrementVersion: () => void;
}

export const useKnowledgeRepository = create<KnowledgeRepositoryState>()(
  persist(
    (set, get) => ({
      nodes: [],
      relationships: [],
      version: 1,

      addNode: (node) => {
        const id = uuidv4();
        const now = new Date().toISOString();
        const newNode: KnowledgeNode = { ...node, id, createdAt: now, updatedAt: now };
        set(state => ({ nodes: [...state.nodes, newNode] }));
        return id;
      },

      updateNode: (id, updates) => {
        set(state => ({
          nodes: state.nodes.map(n => n.id === id ? { ...n, ...updates, updatedAt: new Date().toISOString() } : n),
        }));
      },

      removeNode: (id) => {
        set(state => ({
          nodes: state.nodes.filter(n => n.id !== id),
          relationships: state.relationships.filter(r => r.sourceNodeId !== id && r.targetNodeId !== id),
        }));
      },

      getNode: (id) => get().nodes.find(n => n.id === id),

      getNodesByType: (type) => get().nodes.filter(n => n.type === type),

      getNodesByDomain: (domain) => get().nodes.filter(n => n.domain === domain),

      getNodesBySource: (source) => get().nodes.filter(n => n.source === source),

      addRelationship: (rel) => {
        const id = uuidv4();
        const newRel: KnowledgeRelationship = { ...rel, id, createdAt: new Date().toISOString() };
        set(state => ({ relationships: [...state.relationships, newRel] }));
        return id;
      },

      removeRelationship: (id) => {
        set(state => ({ relationships: state.relationships.filter(r => r.id !== id) }));
      },

      getRelationships: (nodeId) => {
        return get().relationships.filter(r => r.sourceNodeId === nodeId || r.targetNodeId === nodeId);
      },

      getRelationshipsByType: (type) => get().relationships.filter(r => r.type === type),

      search: (query) => {
        const lower = query.toLowerCase();
        return get().nodes.filter(n =>
          n.label.toLowerCase().includes(lower) ||
          n.description.toLowerCase().includes(lower) ||
          n.domain.toLowerCase().includes(lower)
        );
      },

      searchByType: (query, type) => {
        const lower = query.toLowerCase();
        return get().nodes.filter(n =>
          n.type === type && (
            n.label.toLowerCase().includes(lower) ||
            n.description.toLowerCase().includes(lower)
          )
        );
      },

      rebuildIndex: () => {
        const { nodes } = get();
        const byType = new Map<KnowledgeNodeType, string[]>();
        const byDomain = new Map<string, string[]>();
        const bySource = new Map<string, string[]>();
        const searchIndex = new Map<string, string[]>();

        for (const node of nodes) {
          // Type index
          const typeList = byType.get(node.type) || [];
          typeList.push(node.id);
          byType.set(node.type, typeList);

          // Domain index
          const domainList = byDomain.get(node.domain) || [];
          domainList.push(node.id);
          byDomain.set(node.domain, domainList);

          // Source index
          const sourceList = bySource.get(node.source) || [];
          sourceList.push(node.id);
          bySource.set(node.source, sourceList);

          // Search index
          const words = `${node.label} ${node.description}`.toLowerCase().split(/\s+/);
          for (const word of words) {
            const wordList = searchIndex.get(word) || [];
            if (!wordList.includes(node.id)) wordList.push(node.id);
            searchIndex.set(word, wordList);
          }
        }
      },

      getIndex: () => {
        const { nodes } = get();
        const byType = new Map<KnowledgeNodeType, string[]>();
        const byDomain = new Map<string, string[]>();
        const bySource = new Map<string, string[]>();
        const searchIndex = new Map<string, string[]>();

        for (const node of nodes) {
          const typeList = byType.get(node.type) || [];
          typeList.push(node.id);
          byType.set(node.type, typeList);
          const domainList = byDomain.get(node.domain) || [];
          domainList.push(node.id);
          byDomain.set(node.domain, domainList);
          const sourceList = bySource.get(node.source) || [];
          sourceList.push(node.id);
          bySource.set(node.source, sourceList);
        }

        return { byType, byDomain, bySource, searchIndex };
      },

      validateIntegrity: () => {
        const { nodes, relationships } = get();
        const issues: string[] = [];
        const nodeIds = new Set(nodes.map(n => n.id));

        // Check all relationships reference valid nodes
        for (const rel of relationships) {
          if (!nodeIds.has(rel.sourceNodeId)) {
            issues.push(`Relationship ${rel.id} references missing source node ${rel.sourceNodeId}`);
          }
          if (!nodeIds.has(rel.targetNodeId)) {
            issues.push(`Relationship ${rel.id} references missing target node ${rel.targetNodeId}`);
          }
        }

        return { valid: issues.length === 0, issues };
      },

      getVersion: () => get().version,
      incrementVersion: () => set(state => ({ version: state.version + 1 })),
    }),
    { name: 'knowledge-repository', storage: createJSONStorage(() => localStorage) }
  )
);
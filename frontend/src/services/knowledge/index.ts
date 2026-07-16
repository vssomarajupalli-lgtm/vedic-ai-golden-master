// BKL-008B — Deterministic Knowledge Graph Platform
// Barrel Export

export { useKnowledgeRepository } from './knowledgeRepository';
export type { KnowledgeIndex, KnowledgeRepositoryState } from './knowledgeRepository';

export { KnowledgeService } from './knowledgeService';
export type { EvidenceChainStep, CrossReference, KnowledgeAuditEntry } from './knowledgeService';

export type { KnowledgeNode, KnowledgeRelationship, KnowledgeNodeType, KnowledgeRelationshipType } from './nodeRegistry';
export { DOMAINS, NODE_TYPES, RELATIONSHIP_TYPES } from './nodeRegistry';

export { seedKnowledgeGraph } from './seedData';
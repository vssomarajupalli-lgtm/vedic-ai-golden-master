// BKL-008B — Deterministic Knowledge Graph Platform
// Knowledge Graph DTO Mapper: Backend (snake_case) → Frontend (camelCase)

import type { KnowledgeNode, KnowledgeRelationship } from './nodeRegistry';

// Raw backend types (snake_case) - mirror Pydantic schemas exactly
interface RawKnowledgeNode {
  id: string;
  type: string;
  label: string;
  description: string;
  source: string;
  domain: string;
  properties: Record<string, unknown>;
  version: number;
  created_at: string;
  updated_at: string;
  evidence?: {
    summary: string;
    level: string;
    confidence: number;
    source: string;
    revision: string;
    traceability: string;
    chain: Array<{ step: number; description: string; node_id: string; relationship_id: string; evidence: string }>;
  };
  references?: Array<{
    node_id: string;
    label: string;
    type: string;
    relationship: string;
    relevance: string;
  }>;
  relationships?: Record<string, number>;
  computed_relationships?: Record<string, Array<{
    node_id: string;
    label: string;
    type: string;
    relationship: string;
    relevance: string;
  }>>;
}

interface RawKnowledgeRelationship {
  id: string;
  type: string;
  source_node_id: string;
  target_node_id: string;
  label: string;
  description: string;
  weight: number;
  evidence: string;
  created_at: string;
}

interface RawKnowledgeGraphState {
  nodes: RawKnowledgeNode[];
  relationships: RawKnowledgeRelationship[];
  version: number;
  node_count: number;
  relationship_count: number;
}

/**
 * Convert a single backend node (snake_case) to frontend node (camelCase).
 * Pure function, no side effects, no mutation.
 */
export function mapNode(raw: RawKnowledgeNode): KnowledgeNode {
  return {
    id: raw.id,
    type: raw.type as KnowledgeNode['type'],
    label: raw.label,
    description: raw.description,
    source: raw.source as KnowledgeNode['source'],
    domain: raw.domain,
    properties: raw.properties,
    version: raw.version,
    createdAt: raw.created_at,
    updatedAt: raw.updated_at,
    evidence: raw.evidence,
    references: raw.references,
    relationships: raw.relationships,
    computed_relationships: raw.computed_relationships,
  };
}

/**
 * Convert a single backend relationship (snake_case) to frontend relationship (camelCase).
 * Pure function, no side effects, no mutation.
 */
export function mapRelationship(raw: RawKnowledgeRelationship): KnowledgeRelationship {
  return {
    id: raw.id,
    type: raw.type as KnowledgeRelationship['type'],
    sourceNodeId: raw.source_node_id,
    targetNodeId: raw.target_node_id,
    label: raw.label,
    description: raw.description,
    weight: raw.weight,
    evidence: raw.evidence,
    createdAt: raw.created_at,
  };
}

/**
 * Convert entire backend graph state (snake_case) to frontend graph state (camelCase).
 * Pure function, no side effects, no mutation.
 */
export function mapGraphState(raw: RawKnowledgeGraphState): {
  nodes: KnowledgeNode[];
  relationships: KnowledgeRelationship[];
  version: number;
} {
  return {
    nodes: raw.nodes.map(mapNode),
    relationships: raw.relationships.map(mapRelationship),
    version: raw.version,
  };
}
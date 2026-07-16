// BKL-008B — Deterministic Knowledge Graph Platform
// Knowledge Service: Search, evidence chains, cross-references, citations, audit, version, integrity

import { useKnowledgeRepository } from './knowledgeRepository';
import type { KnowledgeNode, KnowledgeRelationship } from './nodeRegistry';
import { v4 as uuidv4 } from 'uuid';

export interface EvidenceChainStep {
  step: number;
  description: string;
  nodeId: string;
  relationshipId: string;
  evidence: string;
}

export interface CrossReference {
  node: KnowledgeNode;
  relationship: KnowledgeRelationship;
  relatedNode: KnowledgeNode;
  relevance: 'direct' | 'indirect' | 'contextual';
}

export interface KnowledgeAuditEntry {
  auditId: string;
  action: 'create' | 'update' | 'delete' | 'query';
  nodeId?: string;
  relationshipId?: string;
  timestamp: string;
  details: Record<string, unknown>;
}

export class KnowledgeService {
  /**
   * Semantic retrieval: find nodes conceptually related to a query.
   */
  static semanticRetrieve(query: string, limit: number = 10): KnowledgeNode[] {
    const store = useKnowledgeRepository.getState();
    const results = store.search(query);
    return results.slice(0, limit);
  }

  /**
   * Build an evidence chain from a formula node to its engine outputs.
   */
  static buildEvidenceChain(formulaId: string): EvidenceChainStep[] {
    const store = useKnowledgeRepository.getState();
    const chain: EvidenceChainStep[] = [];
    const visited = new Set<string>();

    const traverse = (nodeId: string, step: number) => {
      if (visited.has(nodeId)) return;
      visited.add(nodeId);

      const node = store.getNode(nodeId);
      if (!node) return;

      const relationships = store.getRelationships(nodeId);
      for (const rel of relationships) {
        if (rel.type === 'derived_from' || rel.type === 'depends_on' || rel.type === 'validated_by') {
          chain.push({
            step,
            description: `${node.label} ${rel.label} ${store.getNode(rel.targetNodeId)?.label || 'unknown'}`,
            nodeId,
            relationshipId: rel.id,
            evidence: rel.evidence || rel.description,
          });
          traverse(rel.targetNodeId, step + 1);
        }
      }
    };

    traverse(formulaId, 1);
    return chain.sort((a, b) => a.step - b.step);
  }

  /**
   * Find cross-references for a node.
   */
  static findCrossReferences(nodeId: string): CrossReference[] {
    const store = useKnowledgeRepository.getState();
    const results: CrossReference[] = [];

    const relationships = store.getRelationships(nodeId);
    for (const rel of relationships) {
      const otherNodeId = rel.sourceNodeId === nodeId ? rel.targetNodeId : rel.sourceNodeId;
      const otherNode = store.getNode(otherNodeId);
      if (!otherNode) continue;

      results.push({
        node: store.getNode(nodeId)!,
        relationship: rel,
        relatedNode: otherNode,
        relevance: rel.weight >= 0.8 ? 'direct' : rel.weight >= 0.5 ? 'indirect' : 'contextual',
      });
    }

    return results;
  }

  /**
   * Generate a citation for a knowledge node.
   */
  static generateCitation(nodeId: string): string {
    const store = useKnowledgeRepository.getState();
    const node = store.getNode(nodeId);
    if (!node) return '';

    const sourcePrefix: Record<string, string> = {
      engine: 'Engine',
      formula: 'Formula',
      calibration: 'Calibration',
      'question-catalog': 'Question Catalog',
      consultation: 'Consultation',
      'decision-register': 'Decision Register',
      governance: 'Governance',
    };

    const prefix = sourcePrefix[node.source] || 'Knowledge';
    return `[${prefix}:${node.label} v${node.version}]`;
  }

  /**
   * Audit a knowledge operation.
   */
  static audit(action: KnowledgeAuditEntry['action'], details: Record<string, unknown> = {}): KnowledgeAuditEntry {
    return {
      auditId: uuidv4(),
      action,
      timestamp: new Date().toISOString(),
      details,
    };
  }

  /**
   * Validate the integrity of the knowledge graph.
   */
  static validateIntegrity(): { valid: boolean; issues: string[] } {
    return useKnowledgeRepository.getState().validateIntegrity();
  }

  /**
   * Get relationships organized by type for a node.
   */
  static getStructuredRelationships(nodeId: string): Record<string, KnowledgeRelationship[]> {
    const store = useKnowledgeRepository.getState();
    const rels = store.getRelationships(nodeId);
    const grouped: Record<string, KnowledgeRelationship[]> = {};

    for (const rel of rels) {
      const key = rel.type;
      if (!grouped[key]) grouped[key] = [];
      grouped[key].push(rel);
    }

    return grouped;
  }
}
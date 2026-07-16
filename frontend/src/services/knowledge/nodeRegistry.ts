// BKL-008B — Deterministic Knowledge Graph Platform
// Knowledge Node Registry: All node types in the knowledge graph

export type KnowledgeNodeType =
  | 'planet'
  | 'house'
  | 'yoga'
  | 'dasha'
  | 'transit'
  | 'formula'
  | 'calibration'
  | 'question'
  | 'consultation'
  | 'document'
  | 'decision'
  | 'governance';

export type KnowledgeRelationshipType =
  | 'influences'
  | 'depends_on'
  | 'explains'
  | 'references'
  | 'activates'
  | 'weakens'
  | 'strengthens'
  | 'derived_from'
  | 'validated_by'
  | 'supersedes';

export interface KnowledgeNode {
  id: string;
  type: KnowledgeNodeType;
  label: string;
  description: string;
  source: 'engine' | 'formula' | 'calibration' | 'question-catalog' | 'consultation' | 'decision-register' | 'governance';
  domain: string;
  properties: Record<string, unknown>;
  version: number;
  createdAt: string;
  updatedAt: string;
}

export interface KnowledgeRelationship {
  id: string;
  type: KnowledgeRelationshipType;
  sourceNodeId: string;
  targetNodeId: string;
  label: string;
  description: string;
  weight: number;
  evidence: string;
  createdAt: string;
}

// DOMAIN CATALOG
export const DOMAINS: Record<string, { label: string; description: string }> = {
  marriage: { label: 'Marriage', description: 'Marriage timing, quality, compatibility, and relationship dynamics' },
  career: { label: 'Career', description: 'Career promise, professional growth, business, and workplace dynamics' },
  wealth: { label: 'Wealth', description: 'Financial accumulation, assets, investments, and prosperity' },
  health: { label: 'Health', description: 'Physical health, vitality, longevity, and medical astrology' },
  children: { label: 'Children', description: 'Progeny, fertility, children welfare, and parenting' },
  property: { label: 'Property', description: 'Real estate, vehicles, land, and asset acquisition' },
  education: { label: 'Education', description: 'Learning, academic achievement, knowledge, and wisdom' },
  travel: { label: 'Travel', description: 'Foreign travel, pilgrimage, relocation, and journeys' },
  spiritual: { label: 'Spiritual', description: 'Spiritual growth, meditation, liberation, and higher purpose' },
  compatibility: { label: 'Compatibility', description: 'Relationship compatibility, synastry, and partnership' },
  retirement: { label: 'Retirement', description: 'Post-career life, pension, legacy, and elder years' },
};

// NODE TYPE CATALOG
export const NODE_TYPES: Record<KnowledgeNodeType, { label: string; icon: string; description: string }> = {
  planet: { label: 'Planet', icon: '🪐', description: 'Celestial body in the birth chart' },
  house: { label: 'House', icon: '🏠', description: 'Bhava (astrological house)' },
  yoga: { label: 'Yoga', icon: '🔗', description: 'Planetary combination (yoga)' },
  dasha: { label: 'Dasha', icon: '⏳', description: 'Planetary period' },
  transit: { label: 'Transit', icon: '🔄', description: 'Current planetary transit effect' },
  formula: { label: 'Formula', icon: '📐', description: 'Registered astrological formula' },
  calibration: { label: 'Calibration', icon: '⚖️', description: 'Calibration constant or profile' },
  question: { label: 'Question', icon: '❓', description: 'Catalogue question' },
  consultation: { label: 'Consultation', icon: '📋', description: 'Saved consultation record' },
  document: { label: 'Document', icon: '📄', description: 'Architecture or governance document' },
  decision: { label: 'Decision', icon: '✍️', description: 'Decision Register entry' },
  governance: { label: 'Governance', icon: '📜', description: 'Governance document or rule' },
};

// RELATIONSHIP TYPE CATALOG
export const RELATIONSHIP_TYPES: Record<KnowledgeRelationshipType, { label: string; direction: string }> = {
  influences: { label: 'influences', direction: '→' },
  depends_on: { label: 'depends on', direction: '→' },
  explains: { label: 'explains', direction: '→' },
  references: { label: 'references', direction: '→' },
  activates: { label: 'activates', direction: '→' },
  weakens: { label: 'weakens', direction: '→' },
  strengthens: { label: 'strengthens', direction: '→' },
  derived_from: { label: 'derived from', direction: '←' },
  validated_by: { label: 'validated by', direction: '←' },
  supersedes: { label: 'supersedes', direction: '→' },
};
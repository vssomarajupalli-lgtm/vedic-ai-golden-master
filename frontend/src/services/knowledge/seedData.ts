// BKL-008B — Deterministic Knowledge Graph Platform
// Knowledge Graph Seed Data: Pre-populated deterministic knowledge

import { useKnowledgeRepository } from './knowledgeRepository';
import type { KnowledgeNode, KnowledgeRelationship } from './nodeRegistry';

export function seedKnowledgeGraph(): void {
  const store = useKnowledgeRepository.getState();

  // Only seed if empty
  if (store.nodes.length > 0) return;

  // === PLANET NODES ===
  createNode('planet', 'Sun', 'Planet', 'engine', 'general', { significance: 'Soul, authority, father, government' });
  createNode('planet', 'Moon', 'Planet', 'engine', 'general', { significance: 'Mind, emotions, mother, public' });
  createNode('planet', 'Mars', 'Planet', 'engine', 'general', { significance: 'Energy, courage, siblings, property' });
  createNode('planet', 'Mercury', 'Planet', 'engine', 'general', { significance: 'Intellect, communication, business' });
  createNode('planet', 'Jupiter', 'Planet', 'engine', 'general', { significance: 'Wisdom, wealth, children, fortune' });
  createNode('planet', 'Venus', 'Planet', 'engine', 'general', { significance: 'Love, beauty, luxury, arts' });
  createNode('planet', 'Saturn', 'Planet', 'engine', 'general', { significance: 'Discipline, longevity, suffering, delay' });
  createNode('planet', 'Rahu', 'Planet', 'engine', 'general', { significance: 'Obsession, foreign, unconventional' });
  createNode('planet', 'Ketu', 'Planet', 'engine', 'general', { significance: 'Detachment, spirituality, past life' });

  // === HOUSE NODES ===
  for (let i = 1; i <= 12; i++) {
    const bhavaNames: Record<number, string> = {
      1: 'Lagna/Ascendant', 2: 'Dhana', 3: 'Sahaja', 4: 'Sukha', 5: 'Putra', 6: 'Shatru',
      7: 'Kalatra', 8: 'Ayush', 9: 'Dharma', 10: 'Karma', 11: 'Labha', 12: 'Vyaya',
    };
    createNode('house', `House ${i}`, `Bhava — ${bhavaNames[i]}`, 'engine', 'house', { houseNumber: i });
  }

  // === FORMULA NODES ===
  const formulas = [
    { id: 'TRN-HA-001', label: 'House Activation', domain: 'transit', desc: '30% weight — Measures house activation from transit planets' },
    { id: 'TRN-BV-001', label: 'BAV Support', domain: 'transit', desc: '20% weight — Ashtakavarga support evaluation' },
    { id: 'TRN-PA-001', label: 'Planet Activation', domain: 'transit', desc: '20% weight — Planet activation strength from transit' },
    { id: 'TRN-DS-001', label: 'Dasha Sync', domain: 'transit', desc: '20% weight — Dasha period synchronization' },
    { id: 'TRN-VD-001', label: 'Vedha Layer', domain: 'transit', desc: '10% weight — Vedha obstruction detection' },
    { id: 'PLN-DG-001', label: 'Dignity Score', domain: 'planet', desc: 'Evaluates planetary dignity from sign placement' },
    { id: 'PLN-HP-001', label: 'House Placement', domain: 'planet', desc: 'Evaluates house placement strength' },
    { id: 'PRB-AG-001', label: 'Probability Aggregation', domain: 'probability', desc: 'Aggregates subsystem scores into final probability' },
    { id: 'DSH-PR-001', label: 'Dasha Period', domain: 'dasha', desc: 'Calculates dasha period from Vimshottari' },
    { id: 'YOG-DT-001', label: 'Yoga Detection', domain: 'yoga', desc: 'Detects planetary combinations (yogas)' },
  ];

  for (const f of formulas) {
    createNode('formula', f.label, f.desc, 'formula', f.domain, { formulaId: f.id });
  }

  // === CALIBRATION NODES ===
  const calibrations = [
    { id: 'own_sign', label: 'Own Sign', desc: '80 — Planet in its own sign gets 80% strength', domain: 'planet' },
    { id: 'friendly', label: 'Friendly Sign', desc: '60 — Planet in friendly sign gets 60% strength', domain: 'planet' },
    { id: 'neutral', label: 'Neutral Sign', desc: '50 — Planet in neutral sign gets 50% strength', domain: 'planet' },
    { id: 'enemy', label: 'Enemy Sign', desc: '40 — Planet in enemy sign gets 40% strength', domain: 'planet' },
    { id: 'debilitated', label: 'Debilitated', desc: '20 — Planet in debilitated sign gets 20% strength', domain: 'planet' },
  ];

  for (const c of calibrations) {
    createNode('calibration', c.label, c.desc, 'calibration', c.domain, { constantId: c.id });
  }

  // === TRANSIT NODES ===
  createNode('transit', 'Transit Activation', 'Overall transit activation score (0-100)', 'engine', 'transit', { hasSubsystems: true });
  createNode('transit', 'Sadesati', 'Saturn transit over Moon sign — 7.5 year period', 'engine', 'transit', { planet: 'Saturn', duration: '7.5 years' });
  createNode('transit', 'Ashtam Shani', 'Saturn transit in 8th house from Moon', 'engine', 'transit', { planet: 'Saturn' });
  createNode('transit', 'Jupiter Return', 'Jupiter returns to natal position every ~12 years', 'engine', 'transit', { planet: 'Jupiter', period: 12 });

  // === DASHA NODES ===
  const dashaPeriods = [
    'Ketu Mahadasha', 'Venus Mahadasha', 'Sun Mahadasha', 'Moon Mahadasha',
    'Mars Mahadasha', 'Rahu Mahadasha', 'Jupiter Mahadasha', 'Saturn Mahadasha', 'Mercury Mahadasha',
  ];
  for (const d of dashaPeriods) {
    createNode('dasha', d, 'Vimshottari Mahadasha period', 'engine', 'dasha', { system: 'Vimshottari' });
  }

  // === GOVERNANCE NODES ===
  createNode('governance', 'AI Governance (AP-002)', 'AI assistance rules and boundaries', 'governance', 'governance', { documentId: 'AP-002' });
  createNode('governance', 'System Governance (AP-003)', 'Platform-wide governance rules', 'governance', 'governance', { documentId: 'AP-003' });
  createNode('governance', 'GM-007 Freeze', 'Permanent freeze of deterministic engines', 'governance', 'governance', { milestone: 'GM-007' });

  store.incrementVersion();

  // === RELATIONSHIPS ===
  // Formula → Calibration dependencies
  for (const f of formulas) {
    const fNode = store.search(f.label)[0];
    if (fNode) {
      for (const c of store.getNodesByType("calibration")) {
        createRelationship(fNode.id, c.id, 'depends_on', `Formula ${f.label} depends on calibration constant ${c.label}`, 0.8, 'Formula-calibration dependency');
      }
    }
  }

  // Formula → Engine node relationships
  const transitNode = store.search('Transit Activation')[0];
  if (transitNode) {
    const transitFormulas = store.getNodesByType('formula').filter(n => n.domain === 'transit');
    for (const f of transitFormulas) {
      createRelationship(f.id, transitNode.id, 'explains', `${f.label} contributes to transit activation`, 0.9, 'Transit subsystem');
    }
  }

  // Planet → Dignity Score
  const dignityNode = store.search('Dignity Score')[0];
  const planetNodes = store.getNodesByType('planet');
  if (dignityNode) {
    for (const p of planetNodes) {
      createRelationship(dignityNode.id, p.id, 'influences', `Dignity score applies to ${p.label}`, 0.7, 'Planet strength');
    }
  }

  // House → Planet occupancy
  const houseNodes = store.getNodesByType('house');
  for (const h of houseNodes) {
    for (const p of planetNodes) {
      createRelationship(h.id, p.id, 'references', `Planet ${p.label} may occupy ${h.label}`, 0.5, 'House-planet relationship');
    }
  }

  // Calibration → Planet Strength
  const planetStrengthNode = store.search('Planet Activation')[0];
  if (planetStrengthNode) {
    for (const c of store.getNodesByType("calibration")) {
      createRelationship(c.id, planetStrengthNode.id, 'influences', `${c.label} calibrates planet strength`, 0.6, 'Calibration influence');
    }
  }

  // Governance relationships
  const aiGov = store.search('AI Governance')[0];
  const sysGov = store.search('System Governance')[0];
  const freeze = store.search('GM-007 Freeze')[0];
  if (aiGov && sysGov) createRelationship(sysGov.id, aiGov.id, 'supersedes', 'System Governance is supreme', 1.0, 'Governance hierarchy');
  if (freeze && sysGov) createRelationship(freeze.id, sysGov.id, 'validated_by', 'Freeze enforced by governance', 1.0, 'Freeze governance');

  store.incrementVersion();
}

function createNode(
  type: KnowledgeNode['type'], label: string, description: string,
  source: KnowledgeNode['source'], domain: string, properties: Record<string, unknown> = {},
): string {
  return useKnowledgeRepository.getState().addNode({ type, label, description, source, domain, properties, version: 1 });
}

function createRelationship(
  sourceNodeId: string, targetNodeId: string, type: KnowledgeRelationship['type'],
  label: string, weight: number, evidence: string,
): string {
  return useKnowledgeRepository.getState().addRelationship({
    type, sourceNodeId, targetNodeId, label, description: label, weight, evidence,
  });
}
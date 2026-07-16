// BKL-008B — Knowledge Explorer Component
import React, { useState, useMemo } from 'react';
import { useKnowledgeRepository, KnowledgeService, NODE_TYPES, RELATIONSHIP_TYPES, DOMAINS } from '../../services/knowledge';
import type { KnowledgeNodeType, KnowledgeRelationshipType } from '../../services/knowledge';

const NODE_TYPE_KEYS = Object.keys(NODE_TYPES) as KnowledgeNodeType[];
const REL_TYPE_KEYS = Object.keys(RELATIONSHIP_TYPES) as KnowledgeRelationshipType[];

export const KnowledgeExplorer: React.FC = () => {
  const { nodes, relationships, getNode, validateIntegrity } = useKnowledgeRepository();
  const [activeTab, setActiveTab] = useState<'graph' | 'relationships' | 'formulas' | 'integrity'>('graph');
  const [query, setQuery] = useState('');
  const [relFilterType, setRelFilterType] = useState<KnowledgeRelationshipType | 'all'>('all');
  const [selectedFormulaId, setSelectedFormulaId] = useState<string | null>(null);

  const integrity = useMemo(() => validateIntegrity(), [nodes, relationships, validateIntegrity]);

  const filteredRels = useMemo(() => {
    const rels = relationships.filter(rel => {
      const source = getNode(rel.sourceNodeId);
      const target = getNode(rel.targetNodeId);
      if (!source || !target) return false;
      if (relFilterType !== 'all' && rel.type !== relFilterType) return false;
      if (query) {
        const lower = query.toLowerCase();
        return source.label.toLowerCase().includes(lower) ||
          target.label.toLowerCase().includes(lower) ||
          rel.label.toLowerCase().includes(lower);
      }
      return true;
    });
    return rels.map(rel => {
      const source = getNode(rel.sourceNodeId);
      const target = getNode(rel.targetNodeId);
      return { rel, source, target };
    }).filter(r => r.source && r.target);
  }, [relationships, getNode, relFilterType, query]);

  const formulaNodes = useMemo(() => nodes.filter(n => n.type === 'formula'), [nodes]);
  const formulaEvidence = useMemo(() => {
    if (!selectedFormulaId) return null;
    return KnowledgeService.buildEvidenceChain(selectedFormulaId);
  }, [selectedFormulaId]);

  const structuredRels = useMemo(() => {
    const grouped: Record<string, number> = {};
    for (const rel of relationships) {
      grouped[rel.type] = (grouped[rel.type] || 0) + 1;
    }
    return REL_TYPE_KEYS.filter(t => grouped[t]).map(type => ({ type, count: grouped[type] }));
  }, [relationships]);

  return (
    <div className="space-y-4">
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
          <span className="text-2xl">🔗</span> Knowledge Explorer
        </h2>
        <p className="text-sm text-gray-500 mt-1">
          Relationship mapping · Formula evidence chains · Graph integrity
        </p>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg border border-gray-200">
        <div className="flex border-b border-gray-200">
          {[
            { id: 'graph' as const, label: '📊 Graph Overview' },
            { id: 'relationships' as const, label: '🔗 Relationship Explorer' },
            { id: 'formulas' as const, label: '📐 Formula Evidence' },
            { id: 'integrity' as const, label: '✅ Integrity' },
          ].map(tab => (
            <button key={tab.id} onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
                activeTab === tab.id ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}>{tab.label}</button>
          ))}
        </div>

        <div className="p-4">
          {/* ── Graph Overview ──────────────────────────────────────── */}
          {activeTab === 'graph' && (
            <div className="space-y-4">
              {/* Summary stats */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div className="bg-indigo-50 rounded-lg p-3 text-center">
                  <div className="text-2xl font-bold text-indigo-700">{nodes.length}</div>
                  <div className="text-xs text-indigo-500">Total Nodes</div>
                </div>
                <div className="bg-emerald-50 rounded-lg p-3 text-center">
                  <div className="text-2xl font-bold text-emerald-700">{relationships.length}</div>
                  <div className="text-xs text-emerald-500">Total Relationships</div>
                </div>
                <div className="bg-purple-50 rounded-lg p-3 text-center">
                  <div className="text-2xl font-bold text-purple-700">{NODE_TYPE_KEYS.filter(t => nodes.some(n => n.type === t)).length}</div>
                  <div className="text-xs text-purple-500">Node Types</div>
                </div>
                <div className="bg-amber-50 rounded-lg p-3 text-center">
                  <div className="text-2xl font-bold text-amber-700">{Object.keys(DOMAINS).filter(d => nodes.some(n => n.domain === d)).length}</div>
                  <div className="text-xs text-amber-500">Domains Active</div>
                </div>
              </div>

              {/* Node types breakdown */}
              <div className="border border-gray-100 rounded-lg p-3">
                <h3 className="font-semibold text-gray-800 text-sm mb-3">Node Distribution by Type</h3>
                <div className="space-y-2">
                  {NODE_TYPE_KEYS.filter(t => nodes.some(n => n.type === t)).map(type => {
                    const count = nodes.filter(n => n.type === type).length;
                    const pct = Math.round((count / nodes.length) * 100);
                    return (
                      <div key={type} className="flex items-center gap-3">
                        <span className="text-sm w-6">{NODE_TYPES[type].icon}</span>
                        <span className="text-xs font-medium text-gray-700 w-20">{NODE_TYPES[type].label}</span>
                        <div className="flex-1 h-2.5 bg-gray-100 rounded-full overflow-hidden">
                          <div className="h-full bg-indigo-400 rounded-full" style={{ width: `${pct}%` }} />
                        </div>
                        <span className="text-xs text-gray-500 w-12 text-right">{count}</span>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Relationship types breakdown */}
              <div className="border border-gray-100 rounded-lg p-3">
                <h3 className="font-semibold text-gray-800 text-sm mb-3">Relationship Type Distribution</h3>
                <div className="space-y-2">
                  {structuredRels.map(({ type, count }) => {
                    const pct = Math.round((count / relationships.length) * 100);
                    return (
                      <div key={type} className="flex items-center gap-3">
                        <span className="text-xs font-medium text-gray-700 w-28">{RELATIONSHIP_TYPES[type].label}</span>
                        <span className="text-xs text-gray-400 w-4">{RELATIONSHIP_TYPES[type].direction}</span>
                        <div className="flex-1 h-2.5 bg-gray-100 rounded-full overflow-hidden">
                          <div className="h-full bg-emerald-400 rounded-full" style={{ width: `${pct}%` }} />
                        </div>
                        <span className="text-xs text-gray-500 w-12 text-right">{count}</span>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Domain coverage */}
              <div className="border border-gray-100 rounded-lg p-3">
                <h3 className="font-semibold text-gray-800 text-sm mb-3">Domain Coverage</h3>
                <div className="flex flex-wrap gap-2">
                  {Object.entries(DOMAINS).map(([key, info]) => {
                    const count = nodes.filter(n => n.domain === key).length;
                    if (count === 0) return null;
                    return (
                      <div key={key} className="px-3 py-1.5 bg-gray-50 border border-gray-100 rounded-full text-xs">
                        <span className="font-medium text-gray-700">{info.label}</span>
                        <span className="text-gray-400 ml-1">({count})</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

          {/* ── Relationship Explorer ──────────────────────────────────── */}
          {activeTab === 'relationships' && (
            <div className="space-y-3">
              <div className="flex gap-2">
                <input type="text" value={query} onChange={e => setQuery(e.target.value)}
                  placeholder="Filter relationships..."
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500" />
                <select value={relFilterType} onChange={e => setRelFilterType(e.target.value as any)}
                  className="px-3 py-2 border border-gray-300 rounded-lg text-sm bg-white">
                  <option value="all">All Types</option>
                  {REL_TYPE_KEYS.map(t => (
                    <option key={t} value={t}>{RELATIONSHIP_TYPES[t].label}</option>
                  ))}
                </select>
              </div>
              {filteredRels.length === 0 ? (
                <p className="text-center text-gray-400 py-12 text-sm">No relationships match this filter.</p>
              ) : (
                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {filteredRels.map(({ rel, source, target }) => (
                    <div key={rel.id} className="p-3 border border-gray-100 rounded-lg text-sm hover:bg-gray-50 transition-colors">
                      <div className="flex items-center gap-2 mb-1.5">
                        <span className="text-sm">{NODE_TYPES[source!.type]?.icon}</span>
                        <span className="font-medium text-gray-900">{source!.label}</span>
                        <span className="px-2 py-0.5 bg-indigo-100 text-indigo-700 rounded text-xs font-medium">
                          {RELATIONSHIP_TYPES[rel.type]?.label || rel.type}
                        </span>
                        <span className="text-sm">{NODE_TYPES[target!.type]?.icon}</span>
                        <span className="font-medium text-gray-900">{target!.label}</span>
                        <span className="ml-auto text-xs text-gray-400 font-mono">w={rel.weight.toFixed(2)}</span>
                      </div>
                      {rel.evidence && (
                        <div className="text-xs text-gray-400 italic">{rel.evidence}</div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* ── Formula Evidence ────────────────────────────────────────── */}
          {activeTab === 'formulas' && (
            <div className="space-y-3">
              <div className="flex gap-2 flex-wrap">
                {formulaNodes.length === 0 ? (
                  <p className="text-gray-400 text-sm py-4">No formula nodes in the graph.</p>
                ) : (
                  formulaNodes.map(fNode => (
                    <button key={fNode.id} onClick={() => setSelectedFormulaId(fNode.id)}
                      className={`px-3 py-1.5 rounded text-xs font-medium transition-colors ${
                        selectedFormulaId === fNode.id ? 'bg-indigo-600 text-white' : 'bg-gray-100 hover:bg-gray-200 text-gray-700'
                      }`}>
                      {fNode.label}
                    </button>
                  ))
                )}
              </div>
              {selectedFormulaId && formulaEvidence && (
                <div className="border border-gray-100 rounded-lg p-3">
                  <div className="font-semibold text-gray-800 text-sm mb-2">
                    Evidence Chain: {nodes.find(n => n.id === selectedFormulaId)?.label || selectedFormulaId}
                  </div>
                  {formulaEvidence.length === 0 ? (
                    <p className="text-gray-400 text-sm py-4">No evidence chain found for this formula.</p>
                  ) : (
                    <div className="relative pl-8">
                      <div className="absolute left-3 top-0 bottom-0 w-0.5 bg-indigo-200" />
                      {formulaEvidence.map((step, i) => (
                        <div key={i} className="relative pb-5 last:pb-0">
                          <div className="absolute left-[-1.35rem] top-1 w-3 h-3 rounded-full bg-indigo-500 border-2 border-white ring-2 ring-indigo-100" />
                          <div className="bg-gray-50 border border-gray-100 rounded-lg p-3">
                            <div className="text-xs font-bold text-indigo-600 mb-1">Step {step.step}</div>
                            <div className="text-sm text-gray-700 mb-1">{step.description}</div>
                            <div className="text-xs text-gray-400 italic">{step.evidence}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {/* ── Integrity ──────────────────────────────────────────────── */}
          {activeTab === 'integrity' && (
            <div className="space-y-4">
              <div className={`p-4 rounded-lg border ${integrity.valid ? 'bg-emerald-50 border-emerald-200' : 'bg-red-50 border-red-200'}`}>
                <div className={`text-lg font-bold ${integrity.valid ? 'text-emerald-700' : 'text-red-700'}`}>
                  {integrity.valid ? '✓ Graph Integrity: VALID' : '✗ Graph Integrity: ISSUES FOUND'}
                </div>
                <div className={`text-sm mt-1 ${integrity.valid ? 'text-emerald-600' : 'text-red-600'}`}>
                  {integrity.valid ? 'All nodes and relationships are properly connected.' : `${integrity.issues.length} integrity issue(s) detected.`}
                </div>
              </div>
              {integrity.issues.length > 0 && (
                <div className="border border-red-100 rounded-lg p-3 bg-red-50">
                  <h4 className="font-semibold text-red-700 text-sm mb-2">Integrity Issues</h4>
                  <ul className="text-xs text-red-600 list-disc ml-4 space-y-1">
                    {integrity.issues.map((issue, i) => <li key={i}>{issue}</li>)}
                  </ul>
                </div>
              )}
              <div className="border border-gray-100 rounded-lg p-3">
                <h4 className="font-semibold text-gray-800 text-sm mb-3">Graph Statistics</h4>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div className="flex justify-between py-1 border-b border-gray-100">
                    <span className="text-gray-500">Total Nodes</span>
                    <span className="font-medium">{nodes.length}</span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-gray-100">
                    <span className="text-gray-500">Total Relationships</span>
                    <span className="font-medium">{relationships.length}</span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-gray-100">
                    <span className="text-gray-500">Node Types Present</span>
                    <span className="font-medium">{NODE_TYPE_KEYS.filter(t => nodes.some(n => n.type === t)).length}</span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-gray-100">
                    <span className="text-gray-500">Relationship Types</span>
                    <span className="font-medium">{structuredRels.length}</span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-gray-100">
                    <span className="text-gray-500">Active Domains</span>
                    <span className="font-medium">{Object.keys(DOMAINS).filter(d => nodes.some(n => n.domain === d)).length}</span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-gray-100">
                    <span className="text-gray-500">Orphaned Relationships</span>
                    <span className={`font-medium ${integrity.issues.length > 0 ? 'text-red-600' : 'text-gray-900'}`}>{integrity.issues.length}</span>
                  </div>
                  <div className="flex justify-between py-1">
                    <span className="text-gray-500">Avg Relationships per Node</span>
                    <span className="font-medium">{nodes.length > 0 ? (relationships.length / nodes.length).toFixed(1) : '0'}</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default KnowledgeExplorer;
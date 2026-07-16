// BKL-008B — Knowledge Graph Viewer Component
import React, { useState, useMemo } from 'react';
import { useKnowledgeRepository, KnowledgeService, NODE_TYPES, DOMAINS } from '../../services/knowledge';
import type { KnowledgeNode, KnowledgeNodeType, CrossReference, EvidenceChainStep } from '../../services/knowledge';

type ViewMode = 'browse' | 'detail' | 'evidence' | 'references' | 'insights' | 'integrity';

export const KnowledgeGraphViewer: React.FC = () => {
  const { nodes, relationships, search, getRelationships, validateIntegrity } = useKnowledgeRepository();
  const [query, setQuery] = useState('');
  const [filterType, setFilterType] = useState<KnowledgeNodeType | 'all'>('all');
  const [filterDomain, setFilterDomain] = useState<string>('all');
  const [selectedNode, setSelectedNode] = useState<KnowledgeNode | null>(null);
  const [viewMode, setViewMode] = useState<ViewMode>('browse');
  const [evidenceChain, setEvidenceChain] = useState<EvidenceChainStep[]>([]);
  const [crossRefs, setCrossRefs] = useState<CrossReference[]>([]);

  const integrity = useMemo(() => validateIntegrity(), [nodes, relationships, validateIntegrity]);

  const filteredNodes = useMemo(() => {
    let result = query ? search(query) : nodes;
    if (filterType !== 'all') result = result.filter(n => n.type === filterType);
    if (filterDomain !== 'all') result = result.filter(n => n.domain === filterDomain);
    return result;
  }, [nodes, query, filterType, filterDomain, search]);

  const nodeRels = useMemo(() => selectedNode ? getRelationships(selectedNode.id) : [], [selectedNode, getRelationships]);

  const handleNodeSelect = (node: KnowledgeNode) => {
    setSelectedNode(node);
    setViewMode('detail');
    setEvidenceChain(KnowledgeService.buildEvidenceChain(node.id));
    setCrossRefs(KnowledgeService.findCrossReferences(node.id));
  };

  const domainStats = useMemo(() => {
    const stats: Record<string, { count: number; label: string }> = {};
    for (const node of nodes) {
      if (!stats[node.domain]) {
        stats[node.domain] = { count: 0, label: DOMAINS[node.domain]?.label || node.domain };
      }
      stats[node.domain].count++;
    }
    return Object.entries(stats).sort((a, b) => b[1].count - a[1].count);
  }, [nodes]);

  const visibleTypes = useMemo(() => {
    const typeCounts: Partial<Record<KnowledgeNodeType, number>> = {};
    for (const node of nodes) {
      typeCounts[node.type] = (typeCounts[node.type] || 0) + 1;
    }
    return (Object.keys(NODE_TYPES) as KnowledgeNodeType[]).filter(t => typeCounts[t]);
  }, [nodes]);

  return (
    <div className="flex flex-col h-full min-h-[calc(100vh-10rem)]">
      {/* Header */}
      <div className="bg-white rounded-lg border border-gray-200 p-4 mb-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
              <span className="text-2xl">📊</span> Knowledge Graph Platform
            </h2>
            <p className="text-sm text-gray-500 mt-1">
              {nodes.length} nodes · {relationships.length} relationships
              <span className={`ml-3 font-medium ${integrity.valid ? 'text-emerald-600' : 'text-red-600'}`}>
                {integrity.valid ? '✓ Integrity Valid' : `✗ ${integrity.issues.length} Issue(s)`}
              </span>
            </p>
          </div>
          <div className="flex gap-2">
            {(['browse', 'insights', 'integrity'] as ViewMode[]).map(mode => (
              <button key={mode} onClick={() => { setSelectedNode(null); setViewMode(mode); }}
                className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
                  !selectedNode && viewMode === mode ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}>
                {mode === 'browse' ? 'Browse' : mode === 'insights' ? 'Domain Insights' : 'Integrity'}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main content area */}
      <div className="flex flex-1 gap-4 min-h-0">
        {/* Left panel: Navigation / Node list */}
        <div className="w-80 flex-shrink-0 bg-white rounded-lg border border-gray-200 flex flex-col">
          {(!selectedNode || viewMode === 'browse' || viewMode === 'insights' || viewMode === 'integrity') && (
            <>
              <div className="p-3 border-b border-gray-200 space-y-2">
                <input type="text" value={query} onChange={e => setQuery(e.target.value)}
                  placeholder="Search knowledge graph..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500" />
                <div className="flex gap-1 flex-wrap">
                  <button onClick={() => setFilterType('all')}
                    className={`px-2 py-1 rounded text-xs ${filterType === 'all' ? 'bg-indigo-600 text-white' : 'bg-gray-100 hover:bg-gray-200'}`}>All</button>
                  {visibleTypes.map(t => (
                    <button key={t} onClick={() => setFilterType(t)}
                      className={`px-2 py-1 rounded text-xs ${filterType === t ? 'bg-indigo-600 text-white' : 'bg-gray-100 hover:bg-gray-200'}`}>
                      {NODE_TYPES[t].icon} {NODE_TYPES[t].label}
                    </button>
                  ))}
                </div>
                <select value={filterDomain} onChange={e => setFilterDomain(e.target.value)}
                  className="w-full px-2 py-1.5 border border-gray-300 rounded text-xs bg-white">
                  <option value="all">All Domains</option>
                  {domainStats.map(([domain, info]) => (
                    <option key={domain} value={domain}>{info.label} ({info.count})</option>
                  ))}
                </select>
              </div>
              {viewMode === 'browse' && (
                <div className="flex-1 overflow-y-auto p-2 space-y-1">
                  {filteredNodes.length === 0 ? (
                    <p className="text-center text-gray-400 py-12 text-sm">
                      {nodes.length === 0 ? 'Knowledge graph is empty. Seed data will populate on first visit.' : 'No nodes match your filter.'}
                    </p>
                  ) : (
                    filteredNodes.map(node => (
                      <div key={node.id} onClick={() => handleNodeSelect(node)}
                        className={`p-2 border rounded cursor-pointer transition-colors text-sm ${
                          selectedNode?.id === node.id ? 'border-indigo-500 bg-indigo-50' : 'border-gray-100 hover:bg-gray-50 hover:border-gray-200'
                        }`}>
                        <div className="flex items-center gap-1.5">
                          <span className="text-base">{NODE_TYPES[node.type]?.icon}</span>
                          <span className="font-medium text-gray-900 truncate">{node.label}</span>
                        </div>
                        <div className="text-xs text-gray-400 mt-0.5 truncate">{node.domain} · v{node.version}</div>
                      </div>
                    ))
                  )}
                </div>
              )}
              {viewMode === 'insights' && (
                <div className="flex-1 overflow-y-auto p-3 space-y-3">
                  <h3 className="font-semibold text-gray-800 text-sm">Domain Knowledge Coverage</h3>
                  {domainStats.map(([domain, info]) => {
                    const maxCount = domainStats[0]?.[1]?.count || 1;
                    const pct = Math.round((info.count / maxCount) * 100);
                    return (
                      <div key={domain} className="space-y-1">
                        <div className="flex justify-between text-xs">
                          <span className="font-medium text-gray-700">{info.label}</span>
                          <span className="text-gray-500">{info.count} nodes</span>
                        </div>
                        <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                          <div className="h-full bg-indigo-500 rounded-full" style={{ width: `${pct}%` }} />
                        </div>
                      </div>
                    );
                  })}
                  <div className="pt-2 border-t border-gray-100">
                    <div className="text-xs text-gray-500">
                      <span className="font-medium">{domainStats.length}</span> domains represented across <span className="font-medium">{nodes.length}</span> nodes
                    </div>
                  </div>
                </div>
              )}
              {viewMode === 'integrity' && (
                <div className="flex-1 overflow-y-auto p-3 space-y-3">
                  <div className={`p-3 rounded-lg border ${integrity.valid ? 'bg-emerald-50 border-emerald-200' : 'bg-red-50 border-red-200'}`}>
                    <div className={`font-semibold text-sm ${integrity.valid ? 'text-emerald-700' : 'text-red-700'}`}>
                      {integrity.valid ? '✓ Knowledge Graph Integrity: VALID' : '✗ Knowledge Graph Integrity: ISSUES DETECTED'}
                    </div>
                    {integrity.issues.length > 0 && (
                      <ul className="mt-2 text-xs text-red-600 list-disc ml-4 space-y-1">
                        {integrity.issues.map((issue, i) => <li key={i}>{issue}</li>)}
                      </ul>
                    )}
                  </div>
                  <div className="text-xs text-gray-500 space-y-1 bg-gray-50 rounded p-3">
                    <div className="flex justify-between"><span>Total Nodes</span><span className="font-medium">{nodes.length}</span></div>
                    <div className="flex justify-between"><span>Total Relationships</span><span className="font-medium">{relationships.length}</span></div>
                    <div className="flex justify-between"><span>Node Types</span><span className="font-medium">{visibleTypes.length}</span></div>
                    <div className="flex justify-between"><span>Domains</span><span className="font-medium">{domainStats.length}</span></div>
                    <div className="flex justify-between"><span>Repository Version</span><span className="font-medium">v{useKnowledgeRepository.getState().version}</span></div>
                  </div>
                </div>
              )}
            </>
          )}
          {selectedNode && (viewMode === 'detail' || viewMode === 'evidence' || viewMode === 'references') && (
            <div className="flex-1 flex flex-col">
              <div className="p-3 border-b border-gray-200 bg-gray-50">
                <button onClick={() => { setSelectedNode(null); setViewMode('browse'); }}
                  className="text-xs text-indigo-600 hover:text-indigo-800 font-medium">&larr; Back to Browse</button>
              </div>
              <div className="p-3 border-b border-gray-100">
                <div className="flex items-center gap-2">
                  <span className="text-xl">{NODE_TYPES[selectedNode.type]?.icon}</span>
                  <div>
                    <div className="font-semibold text-gray-900">{selectedNode.label}</div>
                    <div className="text-xs text-gray-500">{NODE_TYPES[selectedNode.type]?.label} · {selectedNode.domain} · v{selectedNode.version}</div>
                  </div>
                </div>
              </div>
              <div className="flex border-b border-gray-100">
                {[
                  { id: 'detail' as const, label: 'Info' },
                  { id: 'evidence' as const, label: `Evidence (${evidenceChain.length})` },
                  { id: 'references' as const, label: `References (${crossRefs.length})` },
                ].map(tab => (
                  <button key={tab.id} onClick={() => setViewMode(tab.id)}
                    className={`px-3 py-2 text-xs font-medium border-b-2 flex-1 ${
                      viewMode === tab.id ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700'
                    }`}>{tab.label}</button>
                ))}
              </div>
              <div className="flex-1 overflow-y-auto p-3">
                {viewMode === 'detail' && (
                  <div className="space-y-3 text-sm">
                    <div>
                      <div className="text-xs font-medium text-gray-500 uppercase tracking-wide">Description</div>
                      <p className="text-gray-700 mt-1">{selectedNode.description}</p>
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <div className="text-xs font-medium text-gray-500 uppercase tracking-wide">Source</div>
                        <div className="text-gray-700">{selectedNode.source}</div>
                      </div>
                      <div>
                        <div className="text-xs font-medium text-gray-500 uppercase tracking-wide">Domain</div>
                        <div className="text-gray-700">{DOMAINS[selectedNode.domain]?.label || selectedNode.domain}</div>
                      </div>
                      <div>
                        <div className="text-xs font-medium text-gray-500 uppercase tracking-wide">Citation</div>
                        <div className="text-gray-700 font-mono text-xs">{KnowledgeService.generateCitation(selectedNode.id)}</div>
                      </div>
                      <div>
                        <div className="text-xs font-medium text-gray-500 uppercase tracking-wide">Relationships</div>
                        <div className="text-gray-700">{nodeRels.length}</div>
                      </div>
                    </div>
                    {Object.keys(selectedNode.properties).length > 0 && (
                      <div>
                        <div className="text-xs font-medium text-gray-500 uppercase tracking-wide">Properties</div>
                        <div className="bg-gray-50 rounded p-2 mt-1 text-xs font-mono">
                          {JSON.stringify(selectedNode.properties, null, 2)}
                        </div>
                      </div>
                    )}
                  </div>
                )}
                {viewMode === 'evidence' && (
                  <div className="space-y-2">
                    {evidenceChain.length === 0 ? (
                      <p className="text-center text-gray-400 py-8 text-sm">No evidence chain found for this node.</p>
                    ) : (
                      evidenceChain.map(step => (
                        <div key={`${step.step}-${step.relationshipId}`} className="p-2 border border-gray-100 rounded text-sm">
                          <div className="flex items-center gap-1.5 mb-1">
                            <span className="text-xs font-bold bg-indigo-100 text-indigo-700 px-1.5 py-0.5 rounded">Step {step.step}</span>
                            <span className="text-gray-700">{step.description}</span>
                          </div>
                          <div className="text-xs text-gray-400 italic">{step.evidence}</div>
                        </div>
                      ))
                    )}
                  </div>
                )}
                {viewMode === 'references' && (
                  <div className="space-y-2">
                    {crossRefs.length === 0 ? (
                      <p className="text-center text-gray-400 py-8 text-sm">No cross-references found for this node.</p>
                    ) : (
                      crossRefs.map((ref, i) => (
                        <div key={i} className="p-2 border border-gray-100 rounded text-sm">
                          <div className="flex items-center gap-1.5 mb-1">
                            <span className={`text-xs font-bold px-1.5 py-0.5 rounded ${
                              ref.relevance === 'direct' ? 'bg-emerald-100 text-emerald-700' :
                              ref.relevance === 'indirect' ? 'bg-amber-100 text-amber-700' :
                              'bg-gray-100 text-gray-600'
                            }`}>{ref.relevance}</span>
                            <span className="text-xs">{ref.relationship.label || ref.relationship.type}</span>
                          </div>
                          <div className="flex items-center gap-1.5 text-xs text-gray-600">
                            <span>{NODE_TYPES[ref.node.type]?.icon}</span>
                            <span className="font-medium">{ref.node.label}</span>
                            <span className="text-gray-400">{ref.relationship.type === 'derived_from' ? '←' : '→'}</span>
                            <span>{NODE_TYPES[ref.relatedNode.type]?.icon}</span>
                            <span className="font-medium">{ref.relatedNode.label}</span>
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Right panel: Detail view */}
        <div className="flex-1 min-w-0 bg-white rounded-lg border border-gray-200 p-4 overflow-y-auto">
          {!selectedNode && viewMode === 'browse' && (
            <div className="flex flex-col items-center justify-center h-full text-gray-400">
              <div className="text-5xl mb-4">📊</div>
              <p className="text-lg font-medium text-gray-500">Select a node to view details</p>
              <p className="text-sm mt-1">Click any node in the list to explore its evidence chains and cross-references</p>
            </div>
          )}
          {!selectedNode && viewMode === 'insights' && (
            <div className="flex flex-col items-center justify-center h-full text-gray-400">
              <div className="text-5xl mb-4">📈</div>
              <p className="text-lg font-medium text-gray-500">Domain Insights</p>
              <p className="text-sm mt-1">View domain coverage statistics in the left panel</p>
            </div>
          )}
          {!selectedNode && viewMode === 'integrity' && (
            <div className="flex flex-col items-center justify-center h-full text-gray-400">
              <div className="text-5xl mb-4">✅</div>
              <p className="text-lg font-medium text-gray-500">Integrity Report</p>
              <p className="text-sm mt-1">Graph integrity and statistics shown in the left panel</p>
            </div>
          )}
          {selectedNode && viewMode === 'detail' && (
            <div>
              <h3 className="font-semibold text-gray-900 mb-3">Node Relationships</h3>
              {nodeRels.length === 0 ? (
                <p className="text-center text-gray-400 py-12 text-sm">This node has no relationships.</p>
              ) : (
                <div className="space-y-2">
                  {nodeRels.map(rel => {
                    const otherId = rel.sourceNodeId === selectedNode.id ? rel.targetNodeId : rel.sourceNodeId;
                    const otherNode = nodes.find(n => n.id === otherId);
                    if (!otherNode) return null;
                    return (
                      <div key={rel.id} className="p-3 border border-gray-100 rounded-lg text-sm hover:bg-gray-50 transition-colors">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="px-2 py-0.5 bg-indigo-100 text-indigo-700 rounded text-xs font-medium">{rel.type}</span>
                          <span className="text-xs text-gray-500">w={rel.weight.toFixed(2)}</span>
                        </div>
                        <div className="flex items-center gap-1.5 text-gray-700">
                          <span>{NODE_TYPES[selectedNode.type]?.icon}</span>
                          <span className="font-medium">{selectedNode.label}</span>
                          <span className="text-gray-400">{rel.sourceNodeId === selectedNode.id ? '→' : '←'}</span>
                          <span>{NODE_TYPES[otherNode.type]?.icon}</span>
                          <button onClick={() => handleNodeSelect(otherNode)}
                            className="font-medium text-indigo-600 hover:text-indigo-800 hover:underline">{otherNode.label}</button>
                        </div>
                        {rel.evidence && <div className="text-xs text-gray-400 italic mt-1">{rel.evidence}</div>}
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          )}
          {selectedNode && viewMode === 'evidence' && (
            <div>
              <h3 className="font-semibold text-gray-900 mb-3">Evidence Chain Visualization</h3>
              {evidenceChain.length === 0 ? (
                <p className="text-center text-gray-400 py-12 text-sm">No evidence chain for this node.</p>
              ) : (
                <div className="relative pl-8">
                  {/* Vertical line */}
                  <div className="absolute left-3 top-0 bottom-0 w-0.5 bg-indigo-200" />
                  {evidenceChain.map((step, i) => (
                    <div key={i} className="relative pb-6 last:pb-0">
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
          {selectedNode && viewMode === 'references' && (
            <div>
              <h3 className="font-semibold text-gray-900 mb-3">Cross-Reference Map</h3>
              {crossRefs.length === 0 ? (
                <p className="text-center text-gray-400 py-12 text-sm">No cross-references for this node.</p>
              ) : (
                <div className="space-y-3">
                  {crossRefs.map((ref, i) => (
                    <div key={i} className="p-3 border border-gray-100 rounded-lg text-sm">
                      <div className="flex items-center gap-2 mb-2">
                        <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                          ref.relevance === 'direct' ? 'bg-emerald-100 text-emerald-700' :
                          ref.relevance === 'indirect' ? 'bg-amber-100 text-amber-700' :
                          'bg-gray-100 text-gray-600'
                        }`}>{ref.relevance}</span>
                        <span className="px-2 py-0.5 bg-indigo-100 text-indigo-700 rounded text-xs">{ref.relationship.type}</span>
                        <span className="text-xs text-gray-500">w={ref.relationship.weight.toFixed(2)}</span>
                      </div>
                      <div className="flex items-center gap-2 text-gray-700">
                        <span>{NODE_TYPES[ref.node.type]?.icon}</span>
                        <span className="font-medium">{ref.node.label}</span>
                        <span className="text-gray-400">{ref.relationship.type === 'derived_from' || ref.relationship.type === 'validated_by' ? '→' : '→'}</span>
                        <span>{NODE_TYPES[ref.relatedNode.type]?.icon}</span>
                        <button onClick={() => {
                          const targetNode = nodes.find(n => n.id === ref.relatedNode.id);
                          if (targetNode) handleNodeSelect(targetNode);
                        }}
                          className="font-medium text-indigo-600 hover:text-indigo-800 hover:underline">{ref.relatedNode.label}</button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default KnowledgeGraphViewer;
import React, { useState } from 'react';
import { useChartStore } from '../store/useChartStore';
import { ChevronDown, ChevronRight, Activity, Database } from 'lucide-react';

const StatusBadge = ({ status }: { status: 'LIVE DATA' | 'NOT EXPOSED' }) => {
  if (status === 'LIVE DATA') {
    return (
      <span className="inline-flex items-center gap-1 bg-emerald-100 text-emerald-800 px-2.5 py-0.5 rounded text-xs font-bold border border-emerald-200">
        <Activity className="w-3 h-3" />
        {status}
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1 bg-amber-100 text-amber-800 px-2.5 py-0.5 rounded text-xs font-bold border border-amber-200">
      <Database className="w-3 h-3" />
      {status}
    </span>
  );
};

const SectionHeader = ({ title, source, status, isOpen, onToggle }: { title: string, source: string, status: 'LIVE DATA' | 'NOT EXPOSED', isOpen: boolean, onToggle: () => void }) => (
  <button 
    onClick={onToggle}
    className="w-full flex flex-col sm:flex-row items-start sm:items-center justify-between p-4 bg-slate-50 hover:bg-slate-100 transition-colors rounded-t-lg gap-4"
  >
    <div className="flex flex-col items-start gap-1">
      <div className="flex items-center gap-3">
        <h2 className="text-lg font-bold text-slate-800">{title}</h2>
        <StatusBadge status={status} />
      </div>
      <p className="text-xs text-slate-500 font-mono bg-slate-200 px-2 py-0.5 rounded mt-1">
        Source: {source}
      </p>
    </div>
    {isOpen ? <ChevronDown className="w-5 h-5 text-slate-500 flex-shrink-0" /> : <ChevronRight className="w-5 h-5 text-slate-500 flex-shrink-0" />}
  </button>
);

const CollapsibleSection = ({ title, source, status, children, defaultOpen = false }: { title: string, source: string, status: 'LIVE DATA' | 'NOT EXPOSED', children: React.ReactNode, defaultOpen?: boolean }) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  return (
    <div className="border border-slate-200 rounded-lg mb-4 bg-white shadow-sm">
      <SectionHeader title={title} source={source} status={status} isOpen={isOpen} onToggle={() => setIsOpen(!isOpen)} />
      {isOpen && (
        <div className="p-4 border-t border-slate-200">
          {children}
        </div>
      )}
    </div>
  );
};

const JsonViewer = ({ data }: { data: any }) => (
  <pre className="bg-slate-900 text-emerald-400 p-4 rounded-lg overflow-x-auto text-sm font-mono border border-slate-800">
    {JSON.stringify(data, null, 2)}
  </pre>
);

export default function VerificationConsole() {
  const { rawOutputs, questionResults } = useChartStore();

  if (!rawOutputs || !rawOutputs.breakdown) {
    return (
      <div className="flex flex-col items-center justify-center h-64">
        <h1 className="text-2xl font-bold text-slate-800 mb-2">Formula Verification Console</h1>
        <p className="text-slate-500">Please process a chart first to view the verification trace.</p>
      </div>
    );
  }

  const engineOutputs = rawOutputs.breakdown.engine_outputs || {};
  const natalPromise = engineOutputs.natal_promise || {};
  const planets = engineOutputs.planets || {};
  const houses = engineOutputs.houses || {};
  const dashas = engineOutputs.dashas || {};
  const yogas = engineOutputs.yogas || {};
  const yogaTraces = yogas.yoga_traces || {};
  const rasis = engineOutputs.rasis || {};
  const ashtakavarga = engineOutputs.ashtakavarga || {};
  const masterProbability = rawOutputs.breakdown.master_probability || null;
  
  const latestResult = questionResults && questionResults.length > 0 
    ? questionResults[questionResults.length - 1] 
    : null;
  const isolatedSignals = latestResult?.formula_verification?.data_lineage || null;

  return (
    <div className="max-w-7xl mx-auto space-y-6 pb-12">
      <div className="bg-slate-900 text-white p-6 rounded-xl shadow-lg border border-slate-800">
        <h1 className="text-3xl font-bold mb-2">Formula Verification Console</h1>
        <p className="text-slate-300">Internal diagnostics and deterministic formula validation.</p>
      </div>

      {/* A. Domain Formula Trace */}
      <CollapsibleSection 
        title="A. Domain Formula Trace" 
        source="breakdown.engine_outputs.natal_promise" 
        status="LIVE DATA" 
        defaultOpen
      >
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200 border border-slate-200 rounded-lg overflow-hidden">
            <thead className="bg-slate-100">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-bold text-slate-700 uppercase tracking-wider">Domain</th>
                <th className="px-4 py-3 text-left text-xs font-bold text-slate-700 uppercase tracking-wider">Bhava</th>
                <th className="px-4 py-3 text-left text-xs font-bold text-slate-700 uppercase tracking-wider">Bhavadhipati</th>
                <th className="px-4 py-3 text-left text-xs font-bold text-slate-700 uppercase tracking-wider">Karaka</th>
                <th className="px-4 py-3 text-left text-xs font-bold text-slate-700 uppercase tracking-wider">Varga</th>
                <th className="px-4 py-3 text-left text-xs font-black text-indigo-900 uppercase tracking-wider bg-indigo-50">Final Score</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-slate-200">
              {Object.entries(natalPromise).map(([domain, data]: [string, any]) => {
                const bd = data.breakdown || {};
                return (
                  <tr key={domain} className="hover:bg-slate-50">
                    <td className="px-4 py-3 whitespace-nowrap font-bold text-slate-900 capitalize">{domain}</td>
                    <td className="px-4 py-3 whitespace-nowrap text-slate-600 font-mono">{bd.bhava ?? '-'}</td>
                    <td className="px-4 py-3 whitespace-nowrap text-slate-600 font-mono">{bd.bhavadhipati ?? '-'}</td>
                    <td className="px-4 py-3 whitespace-nowrap text-slate-600 font-mono">{bd.karaka ?? '-'}</td>
                    <td className="px-4 py-3 whitespace-nowrap text-slate-600 font-mono">{bd.varga ?? '-'}</td>
                    <td className="px-4 py-3 whitespace-nowrap font-black text-indigo-700 font-mono bg-indigo-50/30">{data.score ?? '-'}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </CollapsibleSection>

      {/* B. Planet Strength Breakdown */}
      <CollapsibleSection 
        title="B. Planet Strength Breakdown" 
        source="breakdown.engine_outputs.planets" 
        status="LIVE DATA"
      >
        <div className="space-y-3">
          {Object.entries(planets).map(([planet, data]: [string, any]) => {
            const bd = data.breakdown || {};
            return (
              <details key={planet} className="group bg-slate-50 rounded-lg border border-slate-200 overflow-hidden">
                <summary className="flex cursor-pointer items-center justify-between p-4 hover:bg-slate-100 transition-colors">
                  <div className="flex items-center gap-4">
                    <span className="capitalize text-lg font-bold text-slate-800 w-24">{planet}</span>
                    <span className="bg-indigo-100 text-indigo-900 border border-indigo-200 px-3 py-1 rounded text-sm font-bold shadow-sm">
                      Final Score: {data.final_score}
                    </span>
                  </div>
                  <ChevronDown className="w-5 h-5 text-slate-400 group-open:rotate-180 transition-transform" />
                </summary>
                <div className="p-4 bg-white border-t border-slate-200 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div className="bg-slate-50 p-3 rounded shadow-sm border border-slate-100">
                    <span className="text-slate-500 block mb-1 text-xs uppercase font-bold tracking-wider">Dignity</span>
                    <span className="font-mono text-slate-800">{bd.dignity ?? '-'}</span>
                  </div>
                  <div className="bg-slate-50 p-3 rounded shadow-sm border border-slate-100">
                    <span className="text-slate-500 block mb-1 text-xs uppercase font-bold tracking-wider">House Placement</span>
                    <span className="font-mono text-slate-800">{bd.house_placement ?? '-'}</span>
                  </div>
                  <div className="bg-slate-50 p-3 rounded shadow-sm border border-slate-100">
                    <span className="text-slate-500 block mb-1 text-xs uppercase font-bold tracking-wider">Aspects</span>
                    <span className="font-mono text-slate-800">{bd.aspects ?? '-'}</span>
                  </div>
                  <div className="bg-slate-50 p-3 rounded shadow-sm border border-slate-100">
                    <span className="text-slate-500 block mb-1 text-xs uppercase font-bold tracking-wider">Conjunctions</span>
                    <span className="font-mono text-slate-800">{bd.conjunctions ?? '-'}</span>
                  </div>
                  <div className="bg-slate-50 p-3 rounded shadow-sm border border-slate-100">
                    <span className="text-slate-500 block mb-1 text-xs uppercase font-bold tracking-wider">Combustion</span>
                    <span className="font-mono text-slate-800">{bd.combustion ?? '-'}</span>
                  </div>
                  <div className="bg-slate-50 p-3 rounded shadow-sm border border-slate-100">
                    <span className="text-slate-500 block mb-1 text-xs uppercase font-bold tracking-wider">Retrogression</span>
                    <span className="font-mono text-slate-800">{bd.retrogression ?? '-'}</span>
                  </div>
                  <div className="bg-slate-50 p-3 rounded shadow-sm border border-slate-100">
                    <span className="text-slate-500 block mb-1 text-xs uppercase font-bold tracking-wider">Shadbala</span>
                    <span className="font-mono text-slate-800">{bd.shadbala?.toFixed(2) ?? '-'}</span>
                  </div>
                  <div className="bg-slate-50 p-3 rounded shadow-sm border border-slate-100">
                    <span className="text-slate-500 block mb-1 text-xs uppercase font-bold tracking-wider">BAV Modifier</span>
                    <span className="font-mono text-slate-800">{data.bav_modifier ?? '-'}</span>
                  </div>
                </div>
              </details>
            );
          })}
        </div>
      </CollapsibleSection>

      {/* C. House Strength Breakdown */}
      <CollapsibleSection 
        title="C. House Strength Breakdown" 
        source="breakdown.engine_outputs.houses" 
        status="LIVE DATA"
      >
        <div className="space-y-3">
          {Object.entries(houses).map(([house, data]: [string, any]) => {
            const bd = data.breakdown || {};
            return (
              <details key={house} className="group bg-slate-50 rounded-lg border border-slate-200 overflow-hidden">
                <summary className="flex cursor-pointer items-center justify-between p-4 hover:bg-slate-100 transition-colors">
                  <div className="flex items-center gap-4">
                    <span className="text-lg font-bold text-slate-800 w-24">House {house}</span>
                    <span className="bg-emerald-100 text-emerald-900 border border-emerald-200 px-3 py-1 rounded text-sm font-bold shadow-sm">
                      Final Score: {data.final_score}
                    </span>
                  </div>
                  <ChevronDown className="w-5 h-5 text-slate-400 group-open:rotate-180 transition-transform" />
                </summary>
                <div className="p-4 bg-white border-t border-slate-200 grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
                  <div className="bg-slate-50 p-3 rounded shadow-sm border border-slate-100">
                    <span className="text-slate-500 block mb-1 text-xs uppercase font-bold tracking-wider">SAV</span>
                    <span className="font-mono text-slate-800">{bd.sav ?? '-'}</span>
                  </div>
                  <div className="bg-slate-50 p-3 rounded shadow-sm border border-slate-100">
                    <span className="text-slate-500 block mb-1 text-xs uppercase font-bold tracking-wider">Occupants</span>
                    <span className="font-mono text-slate-800">{bd.occupants ?? '-'}</span>
                  </div>
                  <div className="bg-slate-50 p-3 rounded shadow-sm border border-slate-100">
                    <span className="text-slate-500 block mb-1 text-xs uppercase font-bold tracking-wider">Benefic Aspects</span>
                    <span className="font-mono text-slate-800">{bd.benefic_aspects ?? '-'}</span>
                  </div>
                  <div className="bg-slate-50 p-3 rounded shadow-sm border border-slate-100">
                    <span className="text-slate-500 block mb-1 text-xs uppercase font-bold tracking-wider">Malefic Aspects</span>
                    <span className="font-mono text-slate-800">{bd.malefic_aspects ?? '-'}</span>
                  </div>
                  <div className="bg-slate-50 p-3 rounded shadow-sm border border-slate-100">
                    <span className="text-slate-500 block mb-1 text-xs uppercase font-bold tracking-wider">House Type</span>
                    <span className="font-mono text-slate-800">{bd.house_type ?? '-'}</span>
                  </div>
                  <div className="bg-slate-50 p-3 rounded shadow-sm border border-slate-100">
                    <span className="text-slate-500 block mb-1 text-xs uppercase font-bold tracking-wider">House Yogas</span>
                    <span className="font-mono text-slate-800">{bd.house_yogas ?? '-'}</span>
                  </div>
                </div>
              </details>
            );
          })}
        </div>
      </CollapsibleSection>

      {/* D. Dasha Formula Console */}
      <CollapsibleSection 
        title="D. Dasha Formula Console" 
        source="breakdown.engine_outputs.dashas.synthesis" 
        status="LIVE DATA"
      >
        {dashas.synthesis ? (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-white border border-amber-200 p-6 rounded-xl shadow-sm text-center relative overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-1 bg-amber-400"></div>
              <h3 className="text-amber-800 font-bold mb-1 text-xs uppercase tracking-wider">Current Mahadasha</h3>
              <p className="text-2xl font-black capitalize text-slate-800">{dashas.synthesis.active_md}</p>
              <div className="mt-3 bg-slate-50 py-2 rounded border border-slate-100">
                <p className="text-slate-500 text-xs uppercase font-bold">MD Strength</p>
                <p className="font-mono font-bold text-lg text-slate-700">{dashas.synthesis.md_strength}</p>
              </div>
            </div>
            
            <div className="bg-white border border-blue-200 p-6 rounded-xl shadow-sm text-center relative overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-1 bg-blue-400"></div>
              <h3 className="text-blue-800 font-bold mb-1 text-xs uppercase tracking-wider">Current Antardasha</h3>
              <p className="text-2xl font-black capitalize text-slate-800">{dashas.synthesis.active_ad}</p>
              <div className="mt-3 bg-slate-50 py-2 rounded border border-slate-100">
                <p className="text-slate-500 text-xs uppercase font-bold">AD Strength</p>
                <p className="font-mono font-bold text-lg text-slate-700">{dashas.synthesis.ad_strength}</p>
              </div>
            </div>
            
            <div className="bg-white border border-purple-200 p-6 rounded-xl shadow-sm text-center relative overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-1 bg-purple-400"></div>
              <h3 className="text-purple-800 font-bold mb-1 text-xs uppercase tracking-wider">Current Pratyantardasha</h3>
              <p className="text-2xl font-black capitalize text-slate-800">{dashas.synthesis.active_pd}</p>
              <div className="mt-3 bg-slate-50 py-2 rounded border border-slate-100">
                <p className="text-slate-500 text-xs uppercase font-bold">PD Strength</p>
                <p className="font-mono font-bold text-lg text-slate-700">{dashas.synthesis.pd_strength}</p>
              </div>
            </div>
            
            <div className="bg-white border border-emerald-200 p-6 rounded-xl shadow-sm text-center relative overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-1 bg-emerald-400"></div>
              <h3 className="text-emerald-800 font-bold mb-1 text-xs uppercase tracking-wider">Activation Index</h3>
              <div className="flex items-center justify-center h-full pb-4">
                <p className="text-4xl font-black text-emerald-600 font-mono">{dashas.synthesis.dasha_strength}%</p>
              </div>
            </div>
          </div>
        ) : (
          <p className="text-slate-500 italic p-4 text-center">No temporal activation data found.</p>
        )}
      </CollapsibleSection>

      {/* E. Signal Trace Console */}
      <CollapsibleSection 
        title="E. Signal Trace Console" 
        source="isolated_signals" 
        status="LIVE DATA"
        defaultOpen
      >
        {!latestResult ? (
          <div className="bg-amber-50 border border-amber-200 p-8 rounded-lg text-center flex flex-col items-center justify-center">
            <Database className="w-12 h-12 text-amber-300 mb-4" />
            <h3 className="text-lg font-bold text-amber-900 mb-2">Signal Trace requires an active query.</h3>
            <p className="text-amber-700 max-w-lg">
              Ask a structured question in the Question Browser to hydrate the signal trace.
            </p>
          </div>
        ) : !isolatedSignals || Object.keys(isolatedSignals).length === 0 ? (
          <div className="bg-slate-50 border border-slate-200 p-8 rounded-lg text-center">
            <p className="text-slate-500">No isolated signals were generated for this question.</p>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="bg-indigo-50 border border-indigo-100 p-4 rounded-lg mb-4">
              <p className="text-indigo-900 font-bold text-sm">Target Formula: <span className="font-normal">{latestResult.question_title}</span></p>
            </div>
            {Object.entries(isolatedSignals).map(([signalKey, signalData]: [string, any]) => {
              const bd = signalData.breakdown || {};
              const meta = signalData.metadata || {};
              
              return (
                <details key={signalKey} className="group bg-white rounded-lg border border-slate-200 overflow-hidden shadow-sm">
                  <summary className="flex cursor-pointer items-center justify-between p-4 hover:bg-slate-50 transition-colors">
                    <div className="flex items-center gap-4">
                      <span className="capitalize text-lg font-bold text-slate-800 w-32">
                        {signalKey.replace(/_/g, ' ')}
                      </span>
                      {signalData.final_score !== undefined && (
                        <span className={`px-3 py-1 rounded text-sm font-bold shadow-sm ${signalData.final_score >= 50 ? 'bg-emerald-100 text-emerald-900 border border-emerald-200' : 'bg-red-100 text-red-900 border border-red-200'}`}>
                          Score: {signalData.final_score}
                        </span>
                      )}
                    </div>
                    <ChevronDown className="w-5 h-5 text-slate-400 group-open:rotate-180 transition-transform" />
                  </summary>
                  <div className="p-4 bg-slate-50 border-t border-slate-200">
                    
                    {/* Metadata Row */}
                    <div className="flex gap-4 mb-4">
                      <span className="bg-slate-200 text-slate-700 text-xs px-2 py-1 rounded font-mono uppercase tracking-wider">
                        Type: {meta.entity_type || 'Unknown'}
                      </span>
                      <span className="bg-slate-200 text-slate-700 text-xs px-2 py-1 rounded font-mono uppercase tracking-wider">
                        ID: {meta.entity_id || signalKey}
                      </span>
                    </div>

                    {/* Breakdown Grid */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      {Object.entries(bd).map(([k, v]: [string, any]) => (
                        <div key={k} className="bg-white p-3 rounded shadow-sm border border-slate-100">
                          <span className="text-slate-500 block mb-1 text-xs uppercase font-bold tracking-wider">
                            {k.replace(/_/g, ' ')}
                          </span>
                          <span className="font-mono text-slate-800">
                            {typeof v === 'number' && !Number.isInteger(v) ? v.toFixed(2) : String(v)}
                          </span>
                        </div>
                      ))}
                    </div>
                    
                    {/* Confidence Flags */}
                    {signalData.confidence_flags && signalData.confidence_flags.length > 0 && (
                      <div className="mt-4 pt-4 border-t border-slate-200">
                        <span className="text-slate-500 block mb-2 text-xs uppercase font-bold tracking-wider">Confidence Flags</span>
                        <div className="flex flex-wrap gap-2">
                          {signalData.confidence_flags.map((flag: string, idx: number) => (
                            <span key={idx} className="bg-amber-100 text-amber-800 border border-amber-200 px-2 py-1 rounded text-xs font-bold">
                              {flag}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </details>
              );
            })}
          </div>
        )}
      </CollapsibleSection>

      {/* F. Yoga Trace Console */}
      <CollapsibleSection 
        title="F. Yoga Trace Console" 
        source="breakdown.engine_outputs.yogas.yoga_traces" 
        status="LIVE DATA"
      >
        {Object.keys(yogaTraces).length === 0 ? (
          <div className="bg-slate-50 border border-slate-200 p-8 rounded-lg text-center">
            <p className="text-slate-500">No yoga trace data available.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {Object.entries(yogaTraces).map(([yogaName, trace]: [string, any]) => (
              <details key={yogaName} className="group bg-white rounded-lg border border-slate-200 overflow-hidden shadow-sm">
                <summary className="flex cursor-pointer items-center justify-between p-4 hover:bg-slate-50 transition-colors">
                  <div className="flex items-center gap-4">
                    <span className="capitalize text-lg font-bold text-slate-800 sm:w-64">
                      {yogaName}
                    </span>
                    <span className={`px-3 py-1 rounded text-sm font-bold shadow-sm ${trace.status === 'PASSED' ? 'bg-emerald-100 text-emerald-900 border border-emerald-200' : 'bg-slate-100 text-slate-600 border border-slate-200'}`}>
                      {trace.status}
                    </span>
                  </div>
                  <ChevronDown className="w-5 h-5 text-slate-400 group-open:rotate-180 transition-transform" />
                </summary>
                <div className="p-4 bg-slate-50 border-t border-slate-200">
                  <div className="space-y-2 mb-4">
                    <h4 className="text-xs uppercase font-bold text-slate-500 tracking-wider mb-2">Condition Trace:</h4>
                    {trace.rules.map((rule: any, idx: number) => (
                      <div key={idx} className="flex items-start gap-2">
                        <span className={rule.result ? "text-emerald-500 font-bold" : "text-red-500 font-bold"}>
                          {rule.result ? "[✓]" : "[✗]"}
                        </span>
                        <span className={`text-sm ${rule.result ? "text-slate-800 font-medium" : "text-slate-500 line-through"}`}>
                          {rule.rule}
                        </span>
                      </div>
                    ))}
                  </div>
                  
                  {trace.failure_reason && (
                    <div className="mt-4 pt-4 border-t border-slate-200">
                      <h4 className="text-xs uppercase font-bold text-slate-500 tracking-wider mb-2">Conclusion:</h4>
                      <p className="text-sm text-red-700 bg-red-50 p-3 rounded border border-red-100">
                        <span className="font-bold">Failure Reason:</span> {trace.failure_reason}
                      </p>
                    </div>
                  )}
                </div>
              </details>
            ))}
          </div>
        )}
      </CollapsibleSection>

      {/* G. Varga Trace Console */}
      <CollapsibleSection 
        title="G. Varga Trace Console" 
        source="breakdown.engine_outputs.vargas" 
        status="LIVE DATA"
      >
        <div className="space-y-6">
          {['D9', 'D10'].map(vargaId => {
            const vargaData = rawOutputs.breakdown?.engine_outputs?.vargas?.[vargaId]?.planets || {};
            if (Object.keys(vargaData).length === 0) return null;
            
            return (
              <div key={vargaId} className="space-y-3">
                <h3 className="text-md font-bold text-slate-700 border-b pb-2">{vargaId} Planets</h3>
                {Object.entries(vargaData).map(([planet, data]: [string, any]) => {
                  const bd = data.breakdown || {};
                  return (
                    <details key={`${vargaId}-${planet}`} className="group bg-white rounded-lg border border-slate-200 overflow-hidden shadow-sm">
                      <summary className="flex cursor-pointer items-center justify-between p-4 hover:bg-slate-50 transition-colors">
                        <div className="flex items-center gap-4">
                          <span className="capitalize text-lg font-bold text-slate-800 sm:w-32">
                            {planet}
                          </span>
                          <span className="bg-emerald-100 text-emerald-900 border border-emerald-200 px-3 py-1 rounded text-sm font-bold shadow-sm">
                            Final Score: {data.final_score}
                          </span>
                        </div>
                        <ChevronDown className="w-5 h-5 text-slate-400 group-open:rotate-180 transition-transform" />
                      </summary>
                      <div className="p-4 bg-slate-50 border-t border-slate-200 grid grid-cols-1 md:grid-cols-2 gap-6">
                        
                        {/* Breakdown */}
                        <div>
                          <h4 className="text-xs uppercase font-bold text-slate-500 tracking-wider mb-2 border-b border-slate-200 pb-1">Breakdown</h4>
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm">
                            {Object.entries(bd).map(([k, v]: [string, any]) => (
                              <div key={k} className="bg-white p-2 rounded border border-slate-100 flex justify-between items-center gap-2">
                                <span className="text-slate-500 capitalize truncate" title={k.replace(/_/g, ' ')}>{k.replace(/_/g, ' ')}</span>
                                <span className="font-mono font-medium text-slate-800 whitespace-nowrap">
                                  {typeof v === 'number' && !Number.isInteger(v) ? v.toFixed(2) : String(v)}
                                </span>
                              </div>
                            ))}
                          </div>
                        </div>

                        {/* Modifiers & Flags */}
                        <div className="space-y-4">
                          {data.modifiers && Object.keys(data.modifiers).length > 0 && (
                            <div>
                              <h4 className="text-xs uppercase font-bold text-slate-500 tracking-wider mb-2 border-b border-slate-200 pb-1">Modifiers</h4>
                              <div className="grid grid-cols-1 gap-2 text-sm">
                                {Object.entries(data.modifiers).map(([k, v]: [string, any]) => (
                                  <div key={k} className="bg-white p-2 rounded border border-slate-100 flex justify-between items-center gap-2">
                                    <span className="text-slate-500 capitalize truncate" title={k.replace(/_/g, ' ')}>{k.replace(/_/g, ' ')}</span>
                                    <span className="font-mono font-medium text-slate-800 whitespace-nowrap">
                                      {typeof v === 'number' && v > 0 ? `+${v}` : v}
                                    </span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                          
                          {data.confidence_flags && data.confidence_flags.length > 0 && (
                            <div>
                              <h4 className="text-xs uppercase font-bold text-slate-500 tracking-wider mb-2 border-b border-slate-200 pb-1">Flags</h4>
                              <div className="flex flex-wrap gap-2">
                                {data.confidence_flags.map((flag: string, idx: number) => (
                                  <span key={idx} className="bg-amber-100 text-amber-800 border border-amber-200 px-2 py-1 rounded text-xs font-bold">
                                    {flag}
                                  </span>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>

                      </div>
                    </details>
                  );
                })}
              </div>
            );
          })}
        </div>
      </CollapsibleSection>

      {/* H. Master Probability Trace */}
      <CollapsibleSection 
        title="H. Master Probability Trace" 
        source="breakdown.master_probability" 
        status="LIVE DATA"
      >
        {!masterProbability ? (
          <div className="bg-slate-50 border border-slate-200 p-8 rounded-lg text-center">
            <p className="text-slate-500">No master probability data available.</p>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="flex items-center justify-between bg-indigo-50 border border-indigo-200 p-6 rounded-lg">
              <div>
                <h3 className="text-indigo-900 font-bold uppercase tracking-wider text-sm mb-1">Final Probability</h3>
                <p className="text-indigo-700 text-sm">Aggregated from all active engine contributors</p>
              </div>
              <div className="text-4xl font-black text-indigo-700 font-mono">
                {masterProbability.final_score}
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-slate-200 border border-slate-200 rounded-lg overflow-hidden">
                <thead className="bg-slate-100">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-bold text-slate-700 uppercase tracking-wider">Contributor</th>
                    <th className="px-4 py-3 text-left text-xs font-bold text-slate-700 uppercase tracking-wider">Score</th>
                    <th className="px-4 py-3 text-left text-xs font-bold text-slate-700 uppercase tracking-wider">Weight</th>
                    <th className="px-4 py-3 text-left text-xs font-black text-slate-700 uppercase tracking-wider">Weighted Contribution</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-slate-200">
                  {masterProbability.live_factors?.map((factor: string) => {
                    const score = masterProbability.breakdown?.[factor] ?? 0;
                    const weight = masterProbability.weights?.[factor] ?? 0;
                    const contribution = score * weight;
                    return (
                      <tr key={factor} className="hover:bg-slate-50">
                        <td className="px-4 py-3 whitespace-nowrap font-bold text-slate-900 capitalize">{factor.replace(/_/g, ' ')}</td>
                        <td className="px-4 py-3 whitespace-nowrap text-slate-600 font-mono">{score.toFixed(1)}</td>
                        <td className="px-4 py-3 whitespace-nowrap text-slate-600 font-mono">× {weight.toFixed(2)}</td>
                        <td className="px-4 py-3 whitespace-nowrap font-black text-slate-800 font-mono bg-slate-50">= {contribution.toFixed(2)}</td>
                      </tr>
                    );
                  })}
                  <tr className="bg-slate-100 border-t-2 border-slate-300">
                    <td colSpan={3} className="px-4 py-3 text-right font-bold text-slate-700 uppercase tracking-wider">Raw Calculation</td>
                    <td className="px-4 py-3 whitespace-nowrap font-black text-indigo-700 font-mono">{masterProbability.raw_score?.toFixed(2) ?? '-'}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        )}
      </CollapsibleSection>

      {/* L. Lifetime Projection Trace */}
      <CollapsibleSection 
        title="L. Lifetime Projection Trace (MD-AD-PD Timeline)" 
        source="breakdown.master_probability.lifetime_projection" 
        status="LIVE DATA"
      >
        {!masterProbability?.lifetime_projection || masterProbability.lifetime_projection.length === 0 ? (
          <div className="bg-slate-50 border border-slate-200 p-8 rounded-lg text-center">
            <p className="text-slate-500">No lifetime projection data available.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-200 border border-slate-200 rounded-lg overflow-hidden text-sm text-center">
              <thead className="bg-slate-100">
                <tr>
                  <th className="px-3 py-2 text-left font-bold text-slate-700 uppercase tracking-wider">Period</th>
                  <th className="px-3 py-2 text-left font-bold text-slate-700 uppercase tracking-wider">MD</th>
                  <th className="px-3 py-2 text-left font-bold text-slate-700 uppercase tracking-wider">AD</th>
                  <th className="px-3 py-2 text-left font-bold text-slate-700 uppercase tracking-wider">PD</th>
                  <th className="px-3 py-2 text-center font-bold text-slate-700 uppercase tracking-wider">Activation</th>
                  <th className="px-3 py-2 text-right font-black text-indigo-700 uppercase tracking-wider bg-indigo-50">Final Prob</th>
                  <th className="px-3 py-2 text-center font-bold text-slate-700 uppercase tracking-wider">Grade</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-slate-200">
                {masterProbability.lifetime_projection.map((proj: any, idx: number) => (
                  <tr key={idx} className="hover:bg-slate-50">
                    <td className="px-3 py-2 whitespace-nowrap text-left text-slate-800">
                      <span className="block font-medium">{proj.start_date || 'Unknown'}</span>
                      <span className="block text-xs text-slate-500">to {proj.end_date || 'Unknown'}</span>
                    </td>
                    <td className="px-3 py-2 whitespace-nowrap capitalize text-slate-600 border-l border-slate-100">{proj.md} ({proj.md_planet_strength?.toFixed(1) ?? '-'})</td>
                    <td className="px-3 py-2 whitespace-nowrap capitalize text-slate-600 border-l border-slate-100">{proj.ad} ({proj.ad_planet_strength?.toFixed(1) ?? '-'})</td>
                    <td className="px-3 py-2 whitespace-nowrap capitalize text-slate-600 border-l border-slate-100">{proj.pd} ({proj.pd_planet_strength?.toFixed(1) ?? '-'})</td>
                    <td className="px-3 py-2 whitespace-nowrap font-mono text-emerald-600 border-l border-slate-100">{proj.activation_pct?.toFixed(1)}%</td>
                    <td className="px-3 py-2 whitespace-nowrap font-mono font-bold text-indigo-700 bg-indigo-50/30 border-l border-slate-100">{proj.final_probability_pct?.toFixed(1)}%</td>
                    <td className="px-3 py-2 whitespace-nowrap text-center">
                      <span className="px-2 py-1 text-[10px] uppercase font-bold rounded bg-slate-100 text-slate-700">
                        {proj.grade}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </CollapsibleSection>

      {/* I. Rasi Trace Console */}
      <CollapsibleSection 
        title="I. Rasi Trace Console" 
        source="breakdown.engine_outputs.rasis" 
        status="LIVE DATA"
      >
        {Object.keys(rasis).length === 0 ? (
          <div className="bg-slate-50 border border-slate-200 p-8 rounded-lg text-center">
            <p className="text-slate-500">No Rasi strength data available.</p>
          </div>
        ) : (
          <div className="space-y-3">
            {Object.entries(rasis).map(([sign, data]: [string, any]) => {
              const bd = data.breakdown || {};
              return (
                <details key={sign} className="group bg-slate-50 rounded-lg border border-slate-200 overflow-hidden">
                  <summary className="flex cursor-pointer items-center justify-between p-4 hover:bg-slate-100 transition-colors">
                    <div className="flex items-center gap-4">
                      <span className="capitalize text-lg font-bold text-slate-800 w-24">{sign}</span>
                      <span className="bg-emerald-100 text-emerald-900 border border-emerald-200 px-3 py-1 rounded text-sm font-bold shadow-sm">
                        Final Score: {data.final_score}
                      </span>
                    </div>
                    <ChevronDown className="w-5 h-5 text-slate-400 group-open:rotate-180 transition-transform" />
                  </summary>
                  <div className="p-4 bg-white border-t border-slate-200 grid grid-cols-1 md:grid-cols-2 gap-6">
                    
                    {/* Breakdown */}
                    <div>
                      <h4 className="text-xs uppercase font-bold text-slate-500 tracking-wider mb-2 border-b border-slate-200 pb-1">Breakdown</h4>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm">
                        {Object.entries(bd).map(([k, v]: [string, any]) => (
                          <div key={k} className="bg-white p-2 rounded border border-slate-100 flex justify-between items-center gap-2">
                            <span className="text-slate-500 capitalize truncate" title={k.replace(/_/g, ' ')}>{k.replace(/_/g, ' ')}</span>
                            <span className="font-mono font-medium text-slate-800 whitespace-nowrap">
                              {typeof v === 'number' && !Number.isInteger(v) ? v.toFixed(2) : String(v)}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Modifiers & Flags */}
                    <div className="space-y-4">
                      {data.modifiers && Object.keys(data.modifiers).length > 0 && (
                        <div>
                          <h4 className="text-xs uppercase font-bold text-slate-500 tracking-wider mb-2 border-b border-slate-200 pb-1">Modifiers</h4>
                          <div className="grid grid-cols-1 gap-2 text-sm">
                            {Object.entries(data.modifiers).map(([k, v]: [string, any]) => (
                              <div key={k} className="bg-white p-2 rounded border border-slate-100 flex justify-between items-center gap-2">
                                <span className="text-slate-500 capitalize truncate" title={k.replace(/_/g, ' ')}>{k.replace(/_/g, ' ')}</span>
                                <span className="font-mono font-medium text-slate-800 whitespace-nowrap">
                                  {typeof v === 'number' && v > 0 ? `+${v}` : v}
                                </span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                      
                      {data.confidence_flags && data.confidence_flags.length > 0 && (
                        <div>
                          <h4 className="text-xs uppercase font-bold text-slate-500 tracking-wider mb-2 border-b border-slate-200 pb-1">Flags</h4>
                          <div className="flex flex-wrap gap-2">
                            {data.confidence_flags.map((flag: string, idx: number) => (
                              <span key={idx} className="bg-amber-100 text-amber-800 border border-amber-200 px-2 py-1 rounded text-xs font-bold">
                                {flag}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>

                  </div>
                </details>
              );
            })}
          </div>
        )}
      </CollapsibleSection>

      {/* J. Engine Output Snapshot */}
      <CollapsibleSection 
        title="J. Engine Output Snapshot" 
        source="breakdown" 
        status="LIVE DATA"
      >
        <JsonViewer data={rawOutputs.breakdown} />
      </CollapsibleSection>

      {/* K. Ashtakavarga Trace Console */}
      <CollapsibleSection 
        title="K. Ashtakavarga Trace" 
        source="breakdown.engine_outputs.ashtakavarga" 
        status="LIVE DATA"
      >
        {Object.keys(ashtakavarga).length === 0 ? (
          <div className="bg-slate-50 border border-slate-200 p-8 rounded-lg text-center">
            <p className="text-slate-500">No Ashtakavarga data available.</p>
          </div>
        ) : (
          <div className="space-y-6">
            
            {/* SAV Summary Table */}
            <div>
              <h3 className="text-md font-bold text-slate-700 border-b pb-2 mb-3">A. SAV Summary Table (Sarvashtakavarga)</h3>
              <div className="overflow-x-auto pb-2">
                <table className="min-w-full divide-y divide-slate-200 border border-slate-200 rounded-lg overflow-hidden text-center text-sm">
                  <thead className="bg-slate-100">
                    <tr>
                      <th className="px-3 py-2 font-bold text-slate-700 uppercase tracking-wider border-r border-slate-200 bg-slate-200">House</th>
                      {Array.from({ length: 12 }, (_, i) => (
                        <th key={i + 1} className="px-3 py-2 font-bold text-slate-700">{i + 1}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-slate-200">
                    <tr>
                      <td className="px-3 py-2 font-bold text-slate-900 border-r border-slate-200 bg-slate-50">SAV</td>
                      {Array.from({ length: 12 }, (_, i) => {
                        const houseData = ashtakavarga.sav_chart?.[(i + 1).toString()] || {};
                        const bindus = houseData.bindus || 0;
                        const isHigh = bindus >= 30;
                        const isLow = bindus <= 25;
                        return (
                          <td key={i + 1} className={`px-3 py-2 font-mono font-bold ${isHigh ? 'text-emerald-600 bg-emerald-50' : isLow ? 'text-red-600 bg-red-50' : 'text-slate-700'}`}>
                            {bindus}
                          </td>
                        );
                      })}
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            {/* BAV Matrix Grid */}
            <div>
              <h3 className="text-md font-bold text-slate-700 border-b pb-2 mb-3">B. BAV Matrix (Bhinnashtakavarga)</h3>
              <div className="overflow-x-auto pb-2">
                <table className="min-w-full divide-y divide-slate-200 border border-slate-200 rounded-lg overflow-hidden text-center text-sm">
                  <thead className="bg-slate-100">
                    <tr>
                      <th className="px-3 py-2 font-bold text-slate-700 uppercase tracking-wider border-r border-slate-200 bg-slate-200 text-left">Planet</th>
                      {Array.from({ length: 12 }, (_, i) => (
                        <th key={i + 1} className="px-3 py-2 font-bold text-slate-700 text-xs text-slate-500">H{i + 1}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-slate-200">
                    {['sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn'].map(planet => {
                      const planetData = ashtakavarga.bav_charts?.[planet] || {};
                      return (
                        <tr key={planet} className="hover:bg-slate-50">
                          <td className="px-3 py-2 font-bold text-slate-900 capitalize border-r border-slate-200 bg-slate-50 text-left flex items-center gap-2">
                            <span className="w-2 h-2 rounded-full bg-indigo-400"></span>
                            {planet}
                          </td>
                          {Array.from({ length: 12 }, (_, i) => {
                            const bindus = planetData[(i + 1).toString()]?.bindus ?? '-';
                            const isHigh = bindus >= 5;
                            const isLow = bindus <= 3;
                            return (
                              <td key={i + 1} className={`px-3 py-2 font-mono ${isHigh ? 'text-emerald-600 font-bold' : isLow ? 'text-slate-400' : 'text-slate-700'}`}>
                                {bindus}
                              </td>
                            );
                          })}
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Analytics Card */}
            {ashtakavarga.sav_analytics && (
              <div>
                <h3 className="text-md font-bold text-slate-700 border-b pb-2 mb-3">C. Analytics Card</h3>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                  <div className="bg-white border border-slate-200 p-4 rounded-lg shadow-sm text-center">
                    <p className="text-xs uppercase font-bold text-slate-500 mb-1">Strongest House</p>
                    <p className="text-2xl font-black text-emerald-600 font-mono">H{ashtakavarga.sav_analytics.peak_house}</p>
                  </div>
                  <div className="bg-white border border-slate-200 p-4 rounded-lg shadow-sm text-center">
                    <p className="text-xs uppercase font-bold text-slate-500 mb-1">Weakest House</p>
                    <p className="text-2xl font-black text-red-600 font-mono">H{ashtakavarga.sav_analytics.weakest_house}</p>
                  </div>
                  <div className="bg-white border border-slate-200 p-4 rounded-lg shadow-sm text-center">
                    <p className="text-xs uppercase font-bold text-slate-500 mb-1">Total Bindus</p>
                    <p className="text-2xl font-black text-indigo-600 font-mono">{ashtakavarga.sav_analytics.total_bindus}</p>
                  </div>
                  <div className="bg-white border border-slate-200 p-4 rounded-lg shadow-sm text-center">
                    <p className="text-xs uppercase font-bold text-slate-500 mb-1">Avg Per House</p>
                    <p className="text-2xl font-black text-slate-700 font-mono">{ashtakavarga.sav_analytics.average_per_house}</p>
                  </div>
                  <div className="bg-white border border-slate-200 p-4 rounded-lg shadow-sm text-center flex flex-col justify-center items-center">
                    <p className="text-xs uppercase font-bold text-slate-500 mb-2">Math Validation</p>
                    {ashtakavarga.sav_analytics.bav_consistency_check ? (
                      <span className="bg-emerald-100 text-emerald-800 border border-emerald-200 px-3 py-1 rounded text-xs font-bold w-full">PASSED</span>
                    ) : (
                      <span className="bg-red-100 text-red-800 border border-red-200 px-3 py-1 rounded text-xs font-bold w-full">FAILED</span>
                    )}
                  </div>
                </div>
              </div>
            )}
            
          </div>
        )}
      </CollapsibleSection>

    </div>
  );
}

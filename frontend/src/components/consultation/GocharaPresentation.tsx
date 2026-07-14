// @ts-nocheck
import React, { useMemo } from 'react';
import { 
  ChevronDown, ChevronRight,
  Calendar, CheckCircle, Zap,
  Users, Sun, Moon,
  Shield, Target
} from 'lucide-react';

interface GocharaPresentationProps {
  rawOutputs: any;
  questionResults?: any[];
  mode: 'standard' | 'professional' | 'expert' | 'study';
  className?: string;
}

export const GocharaPresentation: React.FC<GocharaPresentationProps> = ({
  rawOutputs,
  questionResults = [],
  mode = 'standard',
  className = ''
}) => {
  const gocharaData = useMemo(() => {
    if (!rawOutputs?.breakdown?.engine_outputs?.transit) return null;
    
    const transit = rawOutputs.breakdown.engine_outputs.transit;
    const planets = rawOutputs.breakdown.engine_outputs.planets || {};
    const houses = rawOutputs.breakdown.engine_outputs.houses || {};
    const dashas = rawOutputs.breakdown.engine_outputs.dashas?.synthesis || {};
    
    return {
      transit,
      planets,
      houses,
      dashas,
      currentTransits: transit.current_transits || [],
      upcomingWindows: transit.upcoming_windows || [],
      elinatiShani: transit.elinati_shani || null,
      sadeSati: transit.sade_sati || null,
      ashtamaShani: transit.ashtama_shani || null,
      mandaliPositions: transit.mandali_positions || [],
      affectedDomains: transit.affected_domains || []
    };
  }, [rawOutputs]);

  if (!gocharaData) {
    return (
      <div className={`bg-gray-50 rounded-lg p-8 text-center ${className}`}>
        <MapPin className="w-12 h-12 text-gray-300 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">Gochara Presentation</h3>
        <p className="text-gray-500">Calculate a chart to view deterministic transit analysis.</p>
      </div>
    );
  }

  const { 
    transit, 
    planets, 
    houses, 
    dashas, 
    currentTransits, 
    upcomingWindows,
    elinatiShani,
    sadeSati,
    ashtamaShani,
    mandaliPositions,
    affectedDomains
  } = gocharaData;

  const activationScore = transit.activation_score || 0;
  const mdLord = dashas.active_md || '';
  const adLord = dashas.active_ad || '';

  return (
    <div className={`bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden ${className}`}>
      <div className="bg-gradient-to-r from-purple-600 to-indigo-700 p-6 text-white">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold">Gochara (Transit) Presentation</h2>
            <p className="text-purple-100 text-sm">Deterministic Transit Analysis · Phase 14H.1 Design Recovery</p>
          </div>
          <span className={`px-3 py-1 rounded-full text-xs font-medium ${mode === 'expert' ? 'bg-yellow-200 text-yellow-900' : mode === 'professional' ? 'bg-blue-200 text-blue-900' : mode === 'study' ? 'bg-green-200 text-green-900' : 'bg-gray-200 text-gray-900'}`}>
            {mode.toUpperCase()} MODE
          </span>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <GocharaMetric label="TRANSIT ACTIVATION" value={`${activationScore}%`} icon={Zap} grade={getGrade(activationScore)} />
          <GocharaMetric label="MD LORD TRANSIT" value={transit.md_lord_transit_strength ? `${transit.md_lord_transit_strength}%` : '—'} icon={Sun} grade={transit.md_lord_transit_strength ? getGrade(transit.md_lord_transit_strength) : '—'} />
          <GocharaMetric label="AD LORD TRANSIT" value={transit.ad_lord_transit_strength ? `${transit.ad_lord_transit_strength}%` : '—'} icon={Moon} grade={transit.ad_lord_transit_strength ? getGrade(transit.ad_lord_transit_strength) : '—'} />
          <GocharaMetric label="DASHA SYNC BONUS" value={`${transit.dasha_sync_bonus || 0}%`} icon={Target} grade={getGrade(transit.dasha_sync_bonus || 0)} />
          <GocharaMetric label="TIMING CONFIDENCE" value={transit.timing_confidence || 'MODERATE'} icon={Shield} grade={transit.timing_confidence || 'MODERATE'} />
        </div>
      </div>

      <div className="p-6 space-y-6">
        <CurrentTransitsSection 
          transits={currentTransits} 
          mdLord={mdLord} 
          adLord={adLord}
          mode={mode}
        />

        <UpcomingWindowsSection windows={upcomingWindows} mode={mode} />

        <SpecialEventsSection 
          elinatiShani={elinatiShani}
          sadeSati={sadeSati}
          ashtamaShani={ashtamaShani}
          mode={mode}
        />

        <MandaliPositionsSection positions={mandaliPositions} mode={mode} />

        <AffectedDomainsSection domains={affectedDomains} mode={mode} />

        {mode === 'expert' && (
          <ExpertTransitDetails transit={transit} planets={planets} houses={houses} dashas={dashas} />
        )}

        {mode === 'study' && (
          <StudyTransitSection transit={transit} dashas={dashas} questionResults={questionResults} />
        )}
      </div>
    </div>
  );
};

interface GocharaMetricProps {
  label: string;
  value: string;
  icon: React.ComponentType<{ className?: string }>;
  grade: string;
}

const GocharaMetric: React.FC<GocharaMetricProps> = ({ label, value, icon: Icon, grade }) => (
  <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
    <div className="flex items-center justify-between mb-2">
      <Icon className="w-5 h-5 text-purple-200" />
      <span className={`text-xs font-medium px-2 py-0.5 rounded ${getGradeColor(grade)}`}>
        {grade}
      </span>
    </div>
    <div className="text-2xl font-bold mb-1">{value}</div>
    <div className="flex items-center gap-1 text-sm text-purple-200">
      <span className="text-xs uppercase tracking-wider">{label}</span>
    </div>
  </div>
);

const CurrentTransitsSection: React.FC<{ transits: any[]; mdLord: string; adLord: string; mode: string }> = ({ transits, mdLord, adLord, mode }) => {
  if (!transits.length) return null;

  return (
    <section>
      <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
        <Sun className="w-5 h-5 text-orange-600" />
        Current Transit Positions
      </h3>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Planet</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Sign</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Degree</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Mandali</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Mandali Pos</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Status</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Intensity</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Affected Houses</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Affected Domains</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Dasha Sync</th>
              {mode === 'expert' && <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Description</th>}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {transits.map((t: any, idx: number) => {
              const isMdLord = t.planet?.toLowerCase() === mdLord.toLowerCase();
              const isAdLord = t.planet?.toLowerCase() === adLord.toLowerCase();
              
              return (
                <tr key={idx} className={`hover:bg-gray-50 ${isMdLord ? 'bg-amber-50' : isAdLord ? 'bg-blue-50' : ''}`}>
                  <td className="px-4 py-3 whitespace-nowrap">
                    <div className="flex items-center gap-2">
                      <span className="capitalize font-medium text-gray-900">{t.planet}</span>
                      {isMdLord && <span className="px-1.5 py-0.5 bg-amber-100 text-amber-800 text-xs font-bold rounded">MD LORD</span>}
                      {isAdLord && <span className="px-1.5 py-0.5 bg-blue-100 text-blue-800 text-xs font-bold rounded">AD LORD</span>}
                    </div>
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700 capitalize">{t.sign}</td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm font-mono text-gray-600">{t.degree?.toFixed(2) || '—'}°</td>
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span className="px-2 py-0.5 bg-purple-100 text-purple-800 text-xs font-bold rounded">{t.mandali}</span>
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm font-mono text-gray-600">{t.mandali_position || '—'}</td>
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span className={`px-2 py-0.5 rounded text-xs font-bold ${
                      t.status === 'favorable' ? 'bg-emerald-100 text-emerald-800' :
                      t.status === 'challenging' ? 'bg-red-100 text-red-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {t.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span className={`px-2 py-0.5 rounded text-xs font-bold ${
                      t.intensity === 'high' ? 'bg-red-100 text-red-800' :
                      t.intensity === 'moderate' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {t.intensity}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600">
                    {(t.affected_houses || []).map((h: number) => (
                      <span key={h} className="px-1.5 py-0.5 bg-gray-100 text-gray-700 text-xs rounded mx-0.5">{h}H</span>
                    ))}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600">
                    {(t.affected_domains || []).map((d: number) => (
                      <span key={d} className="px-1.5 py-0.5 bg-indigo-100 text-indigo-700 text-xs rounded mx-0.5">{getDomainName(d)}</span>
                    ))}
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap">
                    {t.dasha_sync ? (
                      <span className="px-2 py-0.5 bg-emerald-100 text-emerald-800 text-xs font-bold rounded flex items-center gap-1">
                        <CheckCircle className="w-3 h-3" /> Synced
                      </span>
                    ) : (
                      <span className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">No sync</span>
                    )}
                  </td>
                  {mode === 'expert' && (
                    <td className="px-4 py-3 text-sm text-gray-500 max-w-xs truncate">{t.description}</td>
                  )}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
};

const UpcomingWindowsSection: React.FC<{ windows: any[]; mode: string }> = ({ windows, mode }) => {
  if (!windows.length) return null;

  return (
    <section>
      <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
        <Calendar className="w-5 h-5 text-blue-600" />
        Upcoming Transit Windows
      </h3>
      <div className="space-y-3">
        {windows.map((w: any, idx: number) => (
          <div key={idx} className="bg-white border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-3">
                <span className="px-3 py-1 bg-blue-100 text-blue-800 text-sm font-bold rounded-full">
                  {w.planet} Transit
                </span>
                <span className="px-2 py-0.5 bg-purple-100 text-purple-800 text-xs font-bold rounded">{w.mandali}</span>
                <span className={`px-2 py-0.5 rounded text-xs font-bold ${
                  w.type === 'favorable' ? 'bg-emerald-100 text-emerald-800' :
                  w.type === 'challenging' ? 'bg-red-100 text-red-800' :
                  w.type === 'sade-sati' ? 'bg-amber-100 text-amber-800' :
                  w.type === 'elinati' ? 'bg-orange-100 text-orange-800' :
                  w.type === 'ashtama' ? 'bg-purple-100 text-purple-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {w.type.replace('-', ' ')}
                </span>
              </div>
              <div className="flex items-center gap-4 text-sm text-gray-500">
                <span>{w.duration_days} days</span>
                {w.days_until_start !== undefined && w.days_until_start > 0 && (
                  <span className="text-blue-600 font-medium">Starts in {w.days_until_start} days</span>
                )}
                {w.days_until_end !== undefined && w.days_until_end > 0 && (
                  <span className="text-amber-600 font-medium">Ends in {w.days_until_end} days</span>
                )}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-3">
              <div>
                <span className="text-xs text-gray-500 uppercase tracking-wider">Period</span>
                <div className="font-medium text-gray-900">{formatDate(w.start_date)} - {formatDate(w.end_date)}</div>
              </div>
              <div>
                <span className="text-xs text-gray-500 uppercase tracking-wider">Activation Window</span>
                <div className="font-medium text-gray-900">
                  {w.activation_window?.is_active ? '● ACTIVE' : '○ Upcoming'}
                  {w.activation_window?.days_remaining && ` (${w.activation_window.days_remaining} days)`}
                </div>
              </div>
              <div>
                <span className="text-xs text-gray-500 uppercase tracking-wider">Timing Confidence</span>
                <div className="flex items-center gap-2">
                  <span className={`px-2 py-0.5 rounded text-xs font-bold ${
                    w.timing_confidence?.overall === 'high' ? 'bg-emerald-100 text-emerald-800' :
                    w.timing_confidence?.overall === 'moderate' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {w.timing_confidence?.overall?.toUpperCase()}
                  </span>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <span className="text-xs text-gray-500 uppercase tracking-wider">Expected Influence</span>
                <div className="mt-1 space-y-1">
                  {(w.expected_influence || []).map((inf: any, i: number) => (
                    <div key={i} className="flex items-center gap-2 text-sm">
                      <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                        inf.influence === 'favorable' ? 'bg-emerald-100 text-emerald-800' :
                        inf.influence === 'challenging' ? 'bg-red-100 text-red-800' :
                        inf.influence === 'transformative' ? 'bg-purple-100 text-purple-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {inf.influence}
                      </span>
                      <span className="text-gray-700">{inf.domain_name}</span>
                      <span className="text-gray-500 text-xs">{inf.key_events?.join(', ')}</span>
                    </div>
                  ))}
                </div>
              </div>
              <div>
                <span className="text-xs text-gray-500 uppercase tracking-wider">Recommendations</span>
                <div className="mt-1 space-y-1">
                  {(w.recommendations || []).map((rec: string, i: number) => (
                    <div key={i} className="flex items-center gap-2 text-sm text-gray-700">
                      <ArrowUpRight className="w-3.5 h-3.5 text-blue-500" />
                      {rec}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {mode === 'expert' && w.timing_confidence?.factors && (
              <details className="group mt-3">
                <summary className="flex items-center gap-2 text-sm text-gray-500 cursor-pointer">
                  <ChevronRight className="w-4 h-4 group-open:rotate-90 transition-transform text-gray-400" />
                  Timing Confidence Factors
                </summary>
                <div className="mt-2 grid grid-cols-2 gap-2 text-xs">
                  {w.timing_confidence.factors.map((f: any, i: number) => (
                    <div key={i} className="p-2 bg-gray-50 rounded flex items-center gap-2">
                      <span className={`w-2 h-2 rounded ${
                        f.impact === 'positive' ? 'bg-emerald-500' :
                        f.impact === 'negative' ? 'bg-red-500' : 'bg-gray-400'
                      }`} />
                      <span>{f.factor}: {f.impact} ({f.weight})</span>
                    </div>
                  ))}
                </div>
              </details>
            )}
          </div>
        ))}
      </div>
    </section>
  );
};

const SpecialEventsSection: React.FC<{ elinatiShani: any; sadeSati: any; ashtamaShani: any; mode: string }> = ({ elinatiShani, sadeSati, ashtamaShani, mode }) => {
  const events = [
    { key: 'elinati', label: 'Elinati Shani', data: elinatiShani, color: 'orange', icon: Saturn },
    { key: 'sade', label: 'Sade Sati', data: sadeSati, color: 'amber', icon: Saturn },
    { key: 'ashtama', label: 'Ashtama Shani', data: ashtamaShani, color: 'purple', icon: Saturn }
  ].filter(e => e.data);

  if (!events.length) return null;

  return (
    <section>
      <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
        <AlertTriangle className="w-5 h-5 text-orange-600" />
        Special Saturn Events
      </h3>
      <div className="space-y-3">
        {events.map((event, idx) => (
          <div key={idx} className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-3">
                <event.icon className={`w-5 h-5 text-${event.color}-600`} />
                <span className="font-bold text-gray-900">{event.label}</span>
                <span className={`px-2 py-0.5 bg-${event.color}-100 text-${event.color}-800 text-xs font-bold rounded`}>
                  {event.data.is_active ? 'ACTIVE' : 'INACTIVE'}
                </span>
                {event.data.phase && (
                  <span className={`px-2 py-0.5 bg-${event.color}-100 text-${event.color}-800 text-xs font-bold rounded`}>
                    Phase {event.data.phase}
                  </span>
                )}
              </div>
              <div className="text-sm text-gray-500">
                {event.data.start_date && formatDate(event.data.start_date)} - 
                {event.data.end_date && formatDate(event.data.end_date)}
              </div>
            </div>
            
            {mode === 'expert' && event.data && (
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div className="p-2 bg-gray-50 rounded">
                  <span className="text-gray-500">Start: </span>
                  <span className="font-medium">{formatDate(event.data.start_date)}</span>
                </div>
                <div className="p-2 bg-gray-50 rounded">
                  <span className="text-gray-500">End: </span>
                  <span className="font-medium">{formatDate(event.data.end_date)}</span>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </section>
  );
};

const Saturn = ({ className }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <circle cx="12" cy="12" r="5" />
    <path d="M12 2a10 10 0 0 1 0 20M12 2a10 10 0 0 0 0 20" />
    <ellipse cx="12" cy="12" rx="14" ry="3" />
  </svg>
);

const AlertTriangle = ({ className }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
    <line x1="12" y1="9" x2="12" y2="13" />
    <line x1="12" y1="17" x2="12.01" y2="17" />
  </svg>
);

const MandaliPositionsSection: React.FC<{ positions: any[]; mode: string }> = ({ positions, mode }) => {
  if (!positions.length) return null;

  return (
    <section>
      <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
        <Target className="w-5 h-5 text-purple-600" />
        Mandali Positions
      </h3>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase">Mandali</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase">Planet</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase">Position</th>
              {mode === 'expert' && <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase">Interpretation</th>}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {positions.map((p: any, idx: number) => (
              <tr key={idx} className="hover:bg-gray-50">
                <td className="px-4 py-3">
                  <span className="px-2 py-0.5 bg-purple-100 text-purple-800 text-xs font-bold rounded">{p.mandali}</span>
                </td>
                <td className="px-4 py-3 capitalize font-medium">{p.planet}</td>
                <td className="px-4 py-3 font-mono text-sm">{p.position}°</td>
                {mode === 'expert' && <td className="px-4 py-3 text-gray-600">{p.interpretation || '—'}</td>}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
};

const AffectedDomainsSection: React.FC<{ domains: any[]; mode: string }> = ({ domains, mode }) => {
  if (!domains.length) return null;

  return (
    <section>
      <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
        <Users className="w-5 h-5 text-indigo-600" />
        Affected Life Domains
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        {domains.map((d: any, idx: number) => (
          <div key={idx} className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="font-bold text-gray-900 capitalize">{getDomainName(d.domain_id || d.domainId)}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-bold ${
                d.net_influence === 'positive' ? 'bg-emerald-100 text-emerald-800' :
                d.net_influence === 'negative' ? 'bg-red-100 text-red-800' :
                'bg-yellow-100 text-yellow-800'
              }`}>
                {d.net_influence}
              </span>
            </div>
            <div className="text-sm text-gray-600 mb-2">
              Planets: {(d.planets || []).join(', ') || '—'}
            </div>
            <div className="flex items-center gap-2">
              <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                <div className="h-full rounded-full bg-indigo-500" style={{ width: `${Math.round((d.confidence || 0) * 100)}%` }} />
              </div>
              <span className="text-xs text-gray-500">{Math.round((d.confidence || 0) * 100)}% confidence</span>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

const ExpertTransitDetails: React.FC<{ transit: any; planets: any; houses: any; dashas: any }> = ({ transit, planets, houses, dashas }) => (
  <details className="group border border-gray-200 rounded-lg bg-gray-50 mt-6">
    <summary className="flex items-center justify-between p-4 cursor-pointer bg-white border-b border-gray-200">
      <div className="flex items-center gap-3">
        <AlertTriangle className="w-5 h-5 text-yellow-600" />
        <span className="font-bold text-gray-900">Expert Mode: Full Transit Deterministic Details</span>
      </div>
      <ChevronDown className="w-5 h-5 text-gray-400 group-open:rotate-180 transition-transform" />
    </summary>
    <div className="p-4 space-y-4">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <ExpertMetric label="Activation Score" value={`${transit.activation_score || 0}%`} />
        <ExpertMetric label="House Activation" value={`${transit.house_activation_score || 0}%`} />
        <ExpertMetric label="BAV Support" value={`${transit.bav_support_score || 0}%`} />
        <ExpertMetric label="Vedha Obstruction" value={`${transit.vedha_obstruction_score || 0}%`} />
      </div>

      <div className="bg-white rounded-lg p-4 border border-gray-200">
        <h4 className="font-bold text-gray-900 mb-3">MD/AD Lord Transit Alignment</h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div><span className="text-gray-500">MD Lord: </span><span className="font-bold">{dashas.active_md?.capitalize() || '—'}</span></div>
          <div><span className="text-gray-500">MD Transit Strength: </span><span className="font-bold">{transit.md_lord_transit_strength || 0}%</span></div>
          <div><span className="text-gray-500">AD Lord: </span><span className="font-bold">{dashas.active_ad?.capitalize() || '—'}</span></div>
          <div><span className="text-gray-500">AD Transit Strength: </span><span className="font-bold">{transit.ad_lord_transit_strength || 0}%</span></div>
        </div>
      </div>

      <div className="bg-white rounded-lg p-4 border border-gray-200">
        <h4 className="font-bold text-gray-900 mb-3">Transit-to-Natal Aspects</h4>
        <div className="space-y-2 text-sm">
          {(transit.aspects || []).map((a: any, i: number) => (
            <div key={i} className="flex items-center gap-3 p-2 bg-gray-50 rounded">
              <span className={`px-2 py-0.5 rounded text-xs font-bold ${a.is_favorable ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'}`}>
                {a.is_favorable ? 'Favorable' : 'Challenging'}
              </span>
              <span>{a.transit_planet} {a.aspect} Natal {a.natal_planet}</span>
              <span className="text-gray-500 ml-auto">{a.orb}° orb</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  </details>
);

const StudyTransitSection: React.FC<{ transit: any; dashas: any; questionResults: any[] }> = ({ transit, dashas, questionResults }) => (
  <details className="group border border-green-200 rounded-lg bg-green-50 mt-6">
    <summary className="flex items-center justify-between p-4 cursor-pointer bg-white border-b border-green-200">
      <div className="flex items-center gap-3">
        <CheckCircle className="w-5 h-5 text-green-600" />
        <span className="font-bold text-gray-900">Study Mode: Transit Learning & Verification</span>
      </div>
      <ChevronDown className="w-5 h-5 text-gray-400 group-open:rotate-180 transition-transform" />
    </summary>
    <div className="p-4 space-y-4">
      <div className="bg-white rounded-lg p-4 border border-green-200">
        <h4 className="font-bold text-green-800 mb-3">How Transit Activation is Calculated</h4>
        <div className="space-y-2 text-sm font-mono">
          <div className="flex justify-between p-2 bg-green-50 rounded">
            <span>House Activation Score</span>
            <span>{transit.house_activation_score || 0}%</span>
          </div>
          <div className="flex justify-between p-2 bg-green-50 rounded">
            <span>BAV Support Score</span>
            <span>{transit.bav_support_score || 0}%</span>
          </div>
          <div className="flex justify-between p-2 bg-green-50 rounded">
            <span>Planet Activation Score</span>
            <span>{transit.planet_activation_score || 0}%</span>
          </div>
          <div className="flex justify-between p-2 bg-green-50 rounded">
            <span>Vedha Obstruction (deduction)</span>
            <span className="text-red-600">-{transit.vedha_obstruction_score || 0}%</span>
          </div>
          <div className="flex justify-between p-2 bg-green-100 rounded font-bold border border-green-300">
            <span>Transit Activation =</span>
            <span>{transit.activation_score || 0}%</span>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg p-4 border border-green-200">
        <h4 className="font-bold text-green-800 mb-3">Dasha-Transit Synchronization</h4>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between p-2 bg-gray-50 rounded">
            <span>MD Lord ({dashas.active_md?.capitalize()}) Transit</span>
            <span className="font-bold">{transit.md_lord_transit_strength || 0}%</span>
          </div>
          <div className="flex justify-between p-2 bg-gray-50 rounded">
            <span>AD Lord ({dashas.active_ad?.capitalize()}) Transit</span>
            <span className="font-bold">{transit.ad_lord_transit_strength || 0}%</span>
          </div>
          <div className="flex justify-between p-2 bg-green-50 rounded font-bold border border-green-300">
            <span>Sync Bonus Applied</span>
            <span className="text-emerald-600">+{transit.dasha_sync_bonus || 0}%</span>
          </div>
        </div>
      </div>

      {questionResults.length > 0 && (
        <div className="bg-white rounded-lg p-4 border border-green-200">
          <h4 className="font-bold text-green-800 mb-3">Question-Level Transit Evidence</h4>
          <div className="space-y-2 text-sm">
            {questionResults.map((qr: any, idx: number) => (
              <div key={idx} className="p-2 bg-gray-50 rounded">
                <div className="font-bold text-green-700">{qr.question_title || qr.question}</div>
                <div className="flex gap-4 text-xs text-gray-600 mt-1">
                  <span>Transit: {qr.transit?.activation_score || '—'}</span>
                  <span>Dasha: {qr.timing?.dasha_strength || '—'}</span>
                  <span className="font-bold text-indigo-600">Final: {qr.probability?.score || '—'}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  </details>
);

const ExpertMetric: React.FC<{ label: string; value: string }> = ({ label, value }) => (
  <div className="bg-white rounded-lg p-3 border border-gray-200">
    <div className="text-xs text-gray-500 uppercase tracking-wider">{label}</div>
    <div className="font-bold text-gray-900">{value}</div>
  </div>
);

function getDomainName(id: number): string {
  const domains: Record<number, string> = {
    1: 'Self', 2: 'Wealth & Family', 3: 'Siblings', 4: 'Mother & Property',
    5: 'Children & Education', 6: 'Health & Service', 7: 'Marriage & Partnership',
    8: 'Transformation', 9: 'Fortune & Religion', 10: 'Career', 11: 'Income', 12: 'Spirituality'
  };
  return domains[id] || `Domain ${id}`;
}

function getGrade(value: number): string {
  if (value >= 80) return 'EXCELLENT';
  if (value >= 65) return 'VERY GOOD';
  if (value >= 50) return 'GOOD';
  if (value >= 35) return 'WEAK';
  return 'TOO WEAK';
}

function getGradeColor(grade: string): string {
  switch (grade) {
    case 'EXCELLENT': return 'bg-emerald-100 text-emerald-800';
    case 'VERY GOOD': return 'bg-blue-100 text-blue-800';
    case 'GOOD': return 'bg-green-100 text-green-800';
    case 'WEAK': return 'bg-yellow-100 text-yellow-800';
    case 'TOO WEAK': return 'bg-red-100 text-red-800';
    default: return 'bg-gray-100 text-gray-800';
  }
}

function formatDate(dateStr: string): string {
  if (!dateStr || dateStr === 'Unknown') return 'Unknown';
  try {
    return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  } catch {
    return dateStr;
  }
}

function calculateRemaining(endDate: string): string {
  try {
    const end = new Date(endDate);
    const now = new Date();
    const days = Math.ceil((end.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
    if (days > 30) return `${Math.floor(days / 30)} months`;
    if (days > 0) return `${days} days`;
    return 'Ended';
  } catch {
    return 'Unknown';
  }
}

const MapPin = ({ className }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
    <circle cx="12" cy="10" r="3" />
  </svg>
);

const ArrowUpRight = ({ className }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <line x1="7" y1="17" x2="17" y2="7" />
    <polyline points="7 7 17 7 17 17" />
  </svg>
);

export default GocharaPresentation;

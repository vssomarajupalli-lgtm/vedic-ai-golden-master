// @ts-nocheck
import React, { useState, useMemo } from 'react';
import { 
  Plus, Trash2, ChevronDown,
  BarChart2, TrendingUp, Zap,
  Calendar, Clock, Users,
  Target, Shield, AlertTriangle,
  MapPin, Sun, Moon, Star
} from 'lucide-react';
import { ActivationTimeline } from './ActivationTimeline';
import { GocharaPresentation } from './GocharaPresentation';

interface ChartData {
  id: string;
  label: string;
  color: string;
  birthData: any;
  isPrimary: boolean;
  rawOutputs?: any;
  questionResults?: any[];
}

interface ComparisonWorkspaceProps {
  charts: ChartData[];
  onAddChart: () => void;
  onRemoveChart: (id: string) => void;
  onLoadChart: (chart: ChartData) => void;
}

const CHART_COLORS = [
  '#3b82f6', '#ef4444', '#22c55e', '#f59e0b', '#a855f7'
];

export const ComparisonWorkspace: React.FC<ComparisonWorkspaceProps> = ({
  charts,
  onAddChart,
  onRemoveChart,
}) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'planets' | 'houses' | 'dasha' | 'transit' | 'timeline' | 'gochara' | 'questions' | 'probability' | 'expert'>('overview');
  const [selectedDomains, setSelectedDomains] = useState<number[]>([1, 2, 7, 10]);
  const [comparisonMode, setComparisonMode] = useState<'side-by-side' | 'differential' | 'overlay'>('side-by-side');
  const maxCharts = 5;
  const canAddMore = charts.length < maxCharts;

  const primaryChart = charts.find(c => c.isPrimary) || charts[0];
  const otherCharts = charts.filter(c => !c.isPrimary);

  const comparisonData = useMemo(() => {
    if (!primaryChart?.rawOutputs) return null;
    
    return {
      primary: extractComparisonData(primaryChart),
      others: otherCharts.map(c => extractComparisonData(c))
    };
  }, [charts]);

  if (charts.length === 0) {
    return (
      <div className="h-full flex flex-col bg-gray-50">
        <div className="p-4 border-b border-gray-200 bg-white">
          <h1 className="text-2xl font-bold text-gray-800">Comparison Workspace</h1>
        </div>
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center p-8">
            <Users className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No Charts to Compare</h3>
            <p className="text-gray-500 mb-6">Add up to 5 charts for side-by-side deterministic comparison</p>
            <button onClick={onAddChart} className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center gap-2 mx-auto">
              <Plus className="w-5 h-5" />
              Add First Chart
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col bg-gray-50">
      <div className="p-4 border-b border-gray-200 bg-white">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-4">
            <h1 className="text-2xl font-bold text-gray-800">Comparison Workspace</h1>
            <span className="px-2 py-1 bg-gray-100 text-gray-600 text-sm rounded-full">
              {charts.length} / {maxCharts} charts
            </span>
          </div>
          <div className="flex items-center gap-2">
            {canAddMore && (
              <button onClick={onAddChart} className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 flex items-center gap-2">
                <Plus className="w-4 h-4" />
                Add Chart
              </button>
            )}
          </div>
        </div>

        <div className="flex items-center gap-4 flex-wrap mb-4">
          <div className="flex items-center gap-2 bg-gray-50 p-2 rounded-lg">
            {charts.map((chart) => (
              <ChartTab
                key={chart.id}
                chart={chart}
                isPrimary={chart.isPrimary}
                onRemove={() => charts.length > 1 && onRemoveChart(chart.id)}
                onSetPrimary={() => charts.forEach(c => c.isPrimary = c.id === chart.id)}
              />
            ))}
          </div>
        </div>

        <div className="flex items-center gap-4 flex-wrap border-t border-gray-200 pt-4">
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-500">Mode:</span>
            <select
              value={comparisonMode}
              onChange={(e) => setComparisonMode(e.target.value as any)}
              className="px-3 py-1 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option value="side-by-side">Side-by-Side</option>
              <option value="differential">Differential</option>
              <option value="overlay">Overlay</option>
            </select>
          </div>
          <div className="flex items-center gap-2 ml-auto">
            <span className="text-sm text-gray-500">Domains:</span>
            <DomainFilter 
              selected={selectedDomains}
              onChange={setSelectedDomains}
            />
          </div>
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        <nav className="w-48 border-r border-gray-200 bg-white flex flex-col">
          <div className="p-4 space-y-2">
            {[
              { id: 'overview', label: 'Overview', icon: BarChart2 },
              { id: 'planets', label: 'Planet Strength', icon: Zap },
              { id: 'houses', label: 'Bhava Strength', icon: Calendar },
              { id: 'dasha', label: 'Dasha Activation', icon: Clock },
              { id: 'transit', label: 'Transit Support', icon: Users },
              { id: 'gochara', label: 'Gochara', icon: MapPin },
              { id: 'timeline', label: 'Activation Timeline', icon: TrendingUp },
              { id: 'questions', label: 'Question Compare', icon: Target },
              { id: 'probability', label: 'Probability', icon: BarChart2 },
              { id: 'expert', label: 'Expert Evidence', icon: Shield }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                  activeTab === tab.id
                    ? 'bg-indigo-50 text-indigo-700'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <tab.icon className="w-5 h-5" />
                {tab.label}
              </button>
            ))}
          </div>
        </nav>

        <div className="flex-1 overflow-auto p-6">
          {activeTab === 'overview' && comparisonData && (
            <OverviewComparison data={comparisonData} mode={comparisonMode} />
          )}
          {activeTab === 'planets' && comparisonData && (
            <PlanetsComparison data={comparisonData} mode={comparisonMode} charts={charts} />
          )}
          {activeTab === 'houses' && comparisonData && (
            <HousesComparison data={comparisonData} mode={comparisonMode} charts={charts} />
          )}
          {activeTab === 'dasha' && comparisonData && (
            <DashaComparison data={comparisonData} mode={comparisonMode} primaryChart={primaryChart} />
          )}
          {activeTab === 'transit' && comparisonData && (
            <TransitComparison data={comparisonData} mode={comparisonMode} charts={charts} />
          )}
          {activeTab === 'gochara' && primaryChart?.rawOutputs && (
            <GocharaPresentation
              rawOutputs={primaryChart.rawOutputs}
              questionResults={primaryChart.questionResults}
              mode="professional"
            />
          )}
          {activeTab === 'timeline' && primaryChart?.rawOutputs && (
            <ActivationTimeline
              rawOutputs={primaryChart.rawOutputs}
              questionResults={primaryChart.questionResults}
              mode="professional"
              className="h-[800px]"
            />
          )}
          {activeTab === 'questions' && comparisonData && (
            <QuestionComparison data={comparisonData} mode={comparisonMode} charts={charts} />
          )}
          {activeTab === 'probability' && comparisonData && (
            <ProbabilityComparison data={comparisonData} mode={comparisonMode} primaryChart={primaryChart} others={comparisonData.others} />
          )}
          {activeTab === 'expert' && comparisonData && (
            <ExpertComparison data={comparisonData} mode={comparisonMode} charts={charts} />
          )}
        </div>
      </div>
    </div>
  );
};

interface ChartTabProps {
  chart: any;
  isPrimary: boolean;
  onRemove: () => void;
  onSetPrimary: () => void;
}

const ChartTab: React.FC<ChartTabProps> = ({ chart, isPrimary, onRemove, onSetPrimary }) => (
  <div className={`flex items-center gap-2 px-3 py-1.5 rounded-lg ${isPrimary ? 'bg-indigo-100 text-indigo-700' : 'bg-gray-100 text-gray-700'}`}>
    <div 
      className="w-3 h-3 rounded-full border-2 flex-shrink-0"
      style={{ borderColor: chart.color }}
    />
    <span className="text-sm font-medium truncate max-w-[120px]">{chart.label}</span>
    {isPrimary && <span className="text-xs px-1.5 py-0.5 bg-indigo-600 text-white rounded">Primary</span>}
    {!isPrimary && (
      <button onClick={onSetPrimary} className="text-xs text-gray-500 hover:text-indigo-600">Set Primary</button>
    )}
    <button onClick={onRemove} className="text-gray-400 hover:text-red-500 ml-1">
      <Trash2 className="w-3.5 h-3.5" />
    </button>
  </div>
);

interface DomainFilterProps {
  selected: number[];
  onChange?: (domains: number[]) => void;
}

const DomainFilter: React.FC<DomainFilterProps> = ({ selected, onChange }) => {
  const domains = [
    { id: 1, name: 'Self' }, { id: 2, name: 'Wealth' }, { id: 3, name: 'Siblings' },
    { id: 4, name: 'Home' }, { id: 5, name: 'Children' }, { id: 6, name: 'Health' },
    { id: 7, name: 'Partner' }, { id: 8, name: 'Longevity' }, { id: 9, name: 'Fortune' },
    { id: 10, name: 'Career' }, { id: 11, name: 'Gains' }, { id: 12, name: 'Loss' }
  ];

  return (
    <div className="relative">
      <button className="px-3 py-1 border border-gray-300 rounded-md text-sm flex items-center gap-2 bg-white">
        <span>{selected.length} selected</span>
        <ChevronDown className="w-4 h-4" />
      </button>
    </div>
  );
};

export function extractComparisonData(chart: ChartData) {
  const raw = chart.rawOutputs;
  if (!raw?.breakdown) return null;

  const dasha = raw.breakdown.engine_outputs?.dashas;
  const synthesis = dasha?.synthesis || {};
  const transit = raw.breakdown.engine_outputs?.transit || {};
  const masterProb = raw.breakdown.master_probability || {};
  const planets = raw.breakdown.engine_outputs?.planets || {};
  const houses = raw.breakdown.engine_outputs?.houses || {};

  return {
    id: chart.id,
    label: chart.label,
    color: chart.color,
    currentMD: synthesis.active_md || '—',
    currentAD: synthesis.active_ad || '—',
    currentPD: synthesis.active_pd || '—',
    mdStrength: synthesis.md_strength || 0,
    adStrength: synthesis.ad_strength || 0,
    pdStrength: synthesis.pd_strength || 0,
    dashaActivation: synthesis.dasha_strength || 0,
    transitStrength: transit.activation_score || 0,
    transitGrade: transit.grade || '—',
    transitBreakdown: transit.breakdown || {},
    supportingFactors: transit.supporting_factors || [],
    obstructingFactors: transit.obstructing_factors || [],
    activatedDomains: transit.activated_domains || {},
    confidenceFlags: transit.confidence_flags || [],
    probability: masterProb.final_score || 0,
    probGrade: masterProb.grade || '—',
    masterBreakdown: masterProb.breakdown || {},
    planets,
    houses,
    raw
  };
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

function formatValue(value: number | string, format?: (v: number) => string): string {
  if (typeof value === 'number') {
    return format ? format(value) : `${Math.round(value)}%`;
  }
  return String(value);
}

const SectionCard: React.FC<{ 
  title: string; 
  icon: React.ComponentType<{ className?: string }>; 
  color?: string; 
  children: React.ReactNode;
}> = ({ title, icon: Icon, color = 'blue', children }) => (
  <section className="bg-white border border-gray-200 rounded-xl overflow-hidden">
    <div className={`bg-${color}-600 text-white p-4`}>
      <h3 className="text-lg font-bold flex items-center gap-2">
        <Icon className="w-5 h-5" />
        {title}
      </h3>
    </div>
    <div className="p-6">
      {children}
    </div>
  </section>
);

const ComparisonCard: React.FC<{ 
  label: string; 
  primary: number | string; 
  others: (number | string)[];
  format?: (v: number) => string;
  grade?: string;
  primaryColor?: string;
}> = ({ label, primary, others, format, grade, primaryColor }) => (
  <div className="bg-white rounded-lg border border-gray-200 p-4">
    <h3 className="text-sm font-medium text-gray-500 mb-2">{label}</h3>
    <div className="text-3xl font-bold text-indigo-600">{formatValue(primary, format)}</div>
    {grade && (
      <span className={`text-xs font-medium px-2 py-0.5 rounded ${getGradeColor(grade)}`}>{grade}</span>
    )}
    {others && others.length > 0 && (
      <div className="mt-2 space-y-1">
        {others.map((v, i) => (
          <div key={i} className="text-sm text-gray-600">{formatValue(v, format)}</div>
        ))}
      </div>
    )}
  </div>
);

const OverviewComparison: React.FC<{ data: any; mode: string }> = ({ data, mode }) => {
  const { primary, others } = data;
  
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold text-gray-800">Overview Comparison</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <ComparisonCard 
          label="Dasha Activation" 
          primary={primary?.dashaActivation} 
          others={others?.map((o: any) => o.dashaActivation)} 
          format={(v) => `${Math.round(v)}%`}
          grade={getGrade(primary?.dashaActivation || 0)}
        />
        <ComparisonCard 
          label="Transit Strength" 
          primary={primary?.transitStrength} 
          others={others?.map((o: any) => o.transitStrength)} 
          format={(v) => `${Math.round(v)}%`}
          grade={getGrade(primary?.transitStrength || 0)}
        />
        <ComparisonCard 
          label="Final Probability" 
          primary={primary?.probability} 
          others={others?.map((o: any) => o.probability)} 
          format={(v) => `${Math.round(v)}%`}
          grade={primary?.probGrade}
        />
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <ComparisonCard 
          label="Mahadasha" 
          primary={primary?.currentMD} 
          others={others?.map((o: any) => o.currentMD)} 
        />
        <ComparisonCard 
          label="Antardasha" 
          primary={primary?.currentAD} 
          others={others?.map((o: any) => o.currentAD)} 
        />
        <ComparisonCard 
          label="Transit Grade" 
          primary={primary?.transitGrade} 
          others={others?.map((o: any) => o.transitGrade)} 
        />
      </div>
    </div>
  );
};

const PlanetsComparison: React.FC<{ data: any; mode: string; charts: ChartData[] }> = ({ data, mode, charts }) => {
  const { primary, others } = data;
  const planets = ['sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 'rahu', 'ketu'];
  
  return (
    <SectionCard title="Planet Strength Comparison" icon={Zap} color="amber">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Planet</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Sign</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">House</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Dignity</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Strength</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Grade</th>
              {charts.map(c => (
                <th key={c.id} className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider" style={{color: c.color}}>
                  {c.label} ({c.isPrimary ? 'Primary' : 'Compare'})
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {planets.map((planet) => {
              const primaryPlanet = primary?.planets?.[planet];
              const otherPlanets = others?.map(o => o.planets?.[planet]);
              
              if (!primaryPlanet) return null;
              
              return (
                <tr key={planet} className="hover:bg-gray-50">
                  <td className="px-4 py-3 whitespace-nowrap">
                    <div className="flex items-center gap-2">
                      <span className="capitalize font-medium text-gray-900">{planet}</span>
                    </div>
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                    {primaryPlanet.sign || '—'}
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span className="px-2 py-0.5 bg-indigo-100 text-indigo-800 text-xs font-bold rounded">
                      {primaryPlanet.house || '—'}H
                    </span>
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span className="px-2 py-0.5 bg-purple-100 text-purple-800 text-xs font-bold rounded capitalize">
                      {primaryPlanet.dignity || 'neutral'}
                    </span>
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span className={`px-2 py-0.5 rounded text-xs font-bold ${
                      primaryPlanet.final_score >= 70 ? 'bg-emerald-100 text-emerald-800' :
                      primaryPlanet.final_score >= 40 ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {Math.round(primaryPlanet.final_score || 0)}%
                    </span>
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span className={`text-xs font-medium px-2 py-0.5 rounded ${getGradeColor(primaryPlanet.grade || getGrade(primaryPlanet.final_score || 0))}`}>
                      {primaryPlanet.grade || getGrade(primaryPlanet.final_score || 0)}
                    </span>
                  </td>
                  {otherPlanets?.map((op, i) => (
                    <td key={i} className="px-4 py-3 whitespace-nowrap text-sm text-gray-600">
                      {op ? `${Math.round(op.final_score || 0)}% (${op.grade || getGrade(op.final_score || 0)})` : '—'}
                    </td>
                  ))}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </SectionCard>
  );
};

const HousesComparison: React.FC<{ data: any; mode: string; charts: ChartData[] }> = ({ data, mode, charts }) => {
  const { primary, others } = data;
  const houses = Array.from({ length: 12 }, (_, i) => i + 1);
  
  return (
    <SectionCard title="Bhava Strength Comparison" icon={Calendar} color="emerald">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Bhava</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Lord</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Karaka</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Strength</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Grade</th>
              {charts.map(c => (
                <th key={c.id} className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider" style={{color: c.color}}>
                  {c.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {houses.map((house) => {
              const primaryHouse = primary?.houses?.[house];
              const otherHouses = others?.map(o => o.houses?.[house]);
              
              if (!primaryHouse) return null;
              
              return (
                <tr key={house} className="hover:bg-gray-50">
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span className="px-2 py-0.5 bg-indigo-100 text-indigo-800 text-xs font-bold rounded">
                      {house}H
                    </span>
                    <span className="ml-2 text-sm text-gray-600">{primaryHouse.name || `House ${house}`}</span>
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700 capitalize">{primaryHouse.lord || '—'}</td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">{primaryHouse.karaka || '—'}</td>
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span className={`px-2 py-0.5 rounded text-xs font-bold ${
                      primaryHouse.final_score >= 70 ? 'bg-emerald-100 text-emerald-800' :
                      primaryHouse.final_score >= 40 ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {Math.round(primaryHouse.final_score || 0)}%
                    </span>
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span className={`text-xs font-medium px-2 py-0.5 rounded ${getGradeColor(primaryHouse.grade || getGrade(primaryHouse.final_score || 0))}`}>
                      {primaryHouse.grade || getGrade(primaryHouse.final_score || 0)}
                    </span>
                  </td>
                  {otherHouses?.map((oh, i) => (
                    <td key={i} className="px-4 py-3 whitespace-nowrap text-sm text-gray-600">
                      {oh ? `${Math.round(oh.final_score || 0)}% (${oh.grade || getGrade(oh.final_score || 0)})` : '—'}
                    </td>
                  ))}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </SectionCard>
  );
};

const DashaComparison: React.FC<{ data: any; mode: string; primaryChart: ChartData }> = ({ data, mode, primaryChart }) => {
  const { primary, others } = data;
  
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold text-gray-800">Dasha Activation Comparison</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <DashaComparisonCard 
          label="Mahadasha" 
          primary={primary?.currentMD} 
          primaryStrength={primary?.mdStrength} 
          others={others?.map((o: any) => ({ label: o.currentMD, strength: o.mdStrength }))} 
        />
        <DashaComparisonCard 
          label="Antardasha" 
          primary={primary?.currentAD} 
          primaryStrength={primary?.adStrength} 
          others={others?.map((o: any) => ({ label: o.currentAD, strength: o.adStrength }))} 
        />
        <DashaComparisonCard 
          label="Pratyantardasha" 
          primary={primary?.currentPD} 
          primaryStrength={primary?.pdStrength} 
          others={others?.map((o: any) => ({ label: o.currentPD, strength: o.pdStrength }))} 
        />
      </div>

      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="font-bold text-gray-900 mb-4">Dasha Synchronization</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm">
          <div><span className="text-gray-500">Primary Dasha Act:</span> <span className="font-bold ml-2">{Math.round(primary?.dashaActivation || 0)}%</span></div>
          <div><span className="text-gray-500">Primary Transit:</span> <span className="font-bold ml-2">{Math.round(primary?.transitStrength || 0)}%</span></div>
          <div><span className="text-gray-500">Primary Prob:</span> <span className="font-bold ml-2">{Math.round(primary?.probability || 0)}%</span></div>
          <div><span className="text-gray-500">Grade:</span> <span className="font-bold ml-2">{primary?.probGrade || '—'}</span></div>
        </div>
      </div>
      
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="font-bold text-gray-900 mb-4">Active Dasha Periods (Primary Chart)</h3>
        <div className="space-y-3">
          <div className="grid grid-cols-4 gap-2 text-sm bg-gray-50 p-3 rounded">
            <span className="font-medium">Mahadasha</span>
            <span>{primaryChart?.rawOutputs?.breakdown?.engine_outputs?.dashas?.synthesis?.active_md || '—'}</span>
            <span>{Math.round(primary?.mdStrength || 0)}%</span>
            <span className="font-bold text-indigo-600">{getGrade(primary?.mdStrength || 0)}</span>
          </div>
          <div className="grid grid-cols-4 gap-2 text-sm bg-gray-50 p-3 rounded">
            <span className="font-medium">Antardasha</span>
            <span>{primaryChart?.rawOutputs?.breakdown?.engine_outputs?.dashas?.synthesis?.active_ad || '—'}</span>
            <span>{Math.round(primary?.adStrength || 0)}%</span>
            <span className="font-bold text-indigo-600">{getGrade(primary?.adStrength || 0)}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

const DashaComparisonCard: React.FC<{ label: string; primary: string; primaryStrength: number; others: { label: string; strength: number }[] }> = ({ 
  label, primary, primaryStrength, others 
}) => (
  <div className="bg-white rounded-lg border border-gray-200 p-4">
    <h3 className="text-sm font-medium text-gray-500 mb-2">{label}</h3>
    <div className="text-2xl font-bold text-indigo-600">{primary || '—'}</div>
    <div className="text-sm text-gray-500 mb-2">{Math.round(primaryStrength || 0)}% strength</div>
    <div className="space-y-1 mt-2">
      {others?.map((o, i) => (
        <div key={i} className="text-xs text-gray-600">{o.label}: {Math.round(o.strength || 0)}%</div>
      ))}
    </div>
  </div>
);

const TransitComparison: React.FC<{ data: any; mode: string; charts: ChartData[] }> = ({ data, mode, charts }) => {
  const { primary, others } = data;
  
  return (
    <SectionCard title="Transit Support Comparison" icon={Users} color="blue">
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <ComparisonCard 
            label="Transit Activation" 
            primary={primary?.transitStrength} 
            others={others?.map((o: any) => o.transitStrength)} 
            format={(v) => `${Math.round(v)}%`}
            grade={primary?.transitGrade}
          />
          <ComparisonCard 
            label="Dasha Sync Bonus" 
            primary={primary?.transitBreakdown?.dasha_sync || 0} 
            others={others?.map((o: any) => o.transitBreakdown?.dasha_sync || 0)} 
            format={(v) => `${Math.round(v)}%`}
            grade={getGrade(primary?.transitBreakdown?.dasha_sync || 0)}
          />
          <ComparisonCard 
            label="House Activation" 
            primary={primary?.transitBreakdown?.house_activation || 0} 
            others={others?.map((o: any) => o.transitBreakdown?.house_activation || 0)} 
            format={(v) => `${Math.round(v)}%`}
            grade={getGrade(primary?.transitBreakdown?.house_activation || 0)}
          />
          <ComparisonCard 
            label="BAV Support" 
            primary={primary?.transitBreakdown?.bav_support || 0} 
            others={others?.map((o: any) => o.transitBreakdown?.bav_support || 0)} 
            format={(v) => `${Math.round(v)}%`}
            grade={getGrade(primary?.transitBreakdown?.bav_support || 0)}
          />
        </div>

        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h3 className="font-bold text-gray-900 mb-4">Confidence Flags</h3>
          <div className="flex flex-wrap gap-2">
            {[
              'jupiter_transit_positive',
              'saturn_transit_negative', 
              'saturn_sadesati',
              'dasha_lord_transiting',
              'all_malefics_obstructing'
            ].map(flag => (
              <span key={flag} className={`px-2 py-1 rounded text-xs font-medium ${
                primary?.confidenceFlags?.includes(flag) 
                  ? 'bg-indigo-100 text-indigo-800' 
                  : 'bg-gray-100 text-gray-600'
              }`}>
                {flag.replace(/_/g, ' ')}
                {primary?.confidenceFlags?.includes(flag) && <CheckCircle className="w-3 h-3 inline ml-1" />}
              </span>
            ))}
          </div>
        </div>

        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h3 className="font-bold text-gray-900 mb-4">Supporting / Obstructing Factors (Primary)</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <h4 className="text-sm font-medium text-emerald-600 mb-2">Supporting Factors</h4>
              <div className="space-y-1 max-h-48 overflow-y-auto">
                {primary?.supportingFactors?.slice(0, 10).map((f: any, i: number) => (
                  <div key={i} className="flex items-center gap-2 p-1 bg-emerald-50 rounded text-xs">
                    <span className="w-1.5 h-1.5 rounded bg-emerald-500" />
                    <span className="font-medium text-emerald-800">{f.factor}</span>
                    <span className="text-emerald-600 ml-auto">+{f.score}</span>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <h4 className="text-sm font-medium text-red-600 mb-2">Obstructing Factors</h4>
              <div className="space-y-1 max-h-48 overflow-y-auto">
                {primary?.obstructingFactors?.slice(0, 10).map((f: any, i: number) => (
                  <div key={i} className="flex items-center gap-2 p-1 bg-red-50 rounded text-xs">
                    <span className="w-1.5 h-1.5 rounded bg-red-500" />
                    <span className="font-medium text-red-800">{f.factor}</span>
                    <span className="text-red-600 ml-auto">{f.score}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </SectionCard>
  );
};

const QuestionComparison: React.FC<{ data: any; mode: string; charts: ChartData[] }> = ({ data, mode, charts }) => {
  const { primary, others } = data;
  
  // Get question results from primary chart
  const primaryQuestions = primaryChart?.rawOutputs?.breakdown?.engine_outputs?.natal_promise || {};
  const questions = Object.keys(primaryQuestions).slice(0, 10);
  
  return (
    <SectionCard title="Question Comparison" icon={Target} color="green">
      <div className="space-y-4">
        <p className="text-sm text-gray-500">Same question analyzed across {charts.length} charts</p>
        
        {questions.map((questionId, idx) => {
          const primaryQ = primaryQuestions[questionId];
          const otherQs = charts.map(c => c.rawOutputs?.breakdown?.engine_outputs?.natal_promise?.[questionId]).filter(Boolean);
          
          return (
            <div key={questionId} className="bg-white border border-gray-200 rounded-lg p-4">
              <h4 className="font-bold text-gray-900 mb-3 capitalize">{questionId.replace(/_/g, ' ')} - Transit Analysis</h4>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
                <div className="p-3 bg-indigo-50 rounded">
                  <div className="text-xs text-indigo-600 uppercase">Transit Support</div>
                  <div className="font-bold text-indigo-800">{primary?.activatedDomains?.[questionId] || 0}%</div>
                </div>
                <div className="p-3 bg-emerald-50 rounded">
                  <div className="text-xs text-emerald-600 uppercase">Natal Promise</div>
                  <div className="font-bold text-emerald-800">{primaryQ?.score || 0}%</div>
                </div>
                <div className="p-3 bg-amber-50 rounded">
                  <div className="text-xs text-amber-600 uppercase">Dasha Sync</div>
                  <div className="font-bold text-amber-800">{primary?.transitBreakdown?.dasha_sync || 0}%</div>
                </div>
                <div className="p-3 bg-purple-50 rounded">
                  <div className="text-xs text-purple-600 uppercase">Current MD/AD</div>
                  <div className="font-bold text-purple-800">{primary?.currentMD} / {primary?.currentAD}</div>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-500">Supporting Planets</p>
                  <p className="font-medium">{primary?.supportingFactors?.filter((f: any) => f.factor?.includes(questionId)).map(f => f.planet).join(', ') || '—'}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Timing Conclusion</p>
                  <p className="font-medium text-indigo-600">
                    {primary?.probGrade === 'EXCELLENT' || primary?.probGrade === 'VERY GOOD' ? 'Favorable timing' : 
                     primary?.probGrade === 'WEAK' || primary?.probGrade === 'TOO WEAK' ? 'Challenging timing' : 'Moderate timing'}
                  </p>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </SectionCard>
  );
};

const ProbabilityComparison: React.FC<{ data: any; mode: string; primaryChart: ChartData; others: any[] }> = ({ data, mode, primaryChart, others }) => {
  const { primary, others: otherData } = data;
  
  return (
    <SectionCard title="Probability Comparison" icon={BarChart2} color="indigo">
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <ComparisonCard 
            label="Final Probability" 
            primary={primary?.probability} 
            others={otherData?.map((o: any) => o.probability)} 
            format={(v) => `${Math.round(v)}%`}
            grade={primary?.probGrade}
          />
          <ComparisonCard 
            label="Dasha Activation" 
            primary={primary?.dashaActivation} 
            others={otherData?.map((o: any) => o.dashaActivation)} 
            format={(v) => `${Math.round(v)}%`}
            grade={getGrade(primary?.dashaActivation || 0)}
          />
          <ComparisonCard 
            label="Transit Support" 
            primary={primary?.transitStrength} 
            others={otherData?.map((o: any) => o.transitStrength)} 
            format={(v) => `${Math.round(v)}%`}
            grade={primary?.transitGrade}
          />
          <ComparisonCard 
            label="Activation Index" 
            primary={Math.round((primary?.dashaActivation || 0 + primary?.transitStrength || 0) / 2)} 
            others={otherData?.map((o: any) => Math.round((o.dashaActivation || 0 + o.transitStrength || 0) / 2))} 
            format={(v) => `${Math.round(v)}%`}
            grade={getGrade(Math.round((primary?.dashaActivation || 0 + primary?.transitStrength || 0) / 2))}
          />
        </div>

        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h3 className="font-bold text-gray-900 mb-4">Probability Breakdown</h3>
          <div className="space-y-3">
            <div className="flex items-center gap-4">
              <div className="w-32 font-medium text-gray-700">Natal Promise</div>
              <div className="flex-1 h-4 bg-gray-200 rounded overflow-hidden">
                <div className="h-full bg-emerald-600 rounded" style={{ width: `${primary?.probability || 0}%` }} />
              </div>
              <div className="w-16 text-right font-bold">{Math.round(primary?.probability || 0)}%</div>
            </div>
            <div className="flex items-center gap-4">
              <div className="w-32 font-medium text-gray-700">Dasha Weight</div>
              <div className="flex-1 h-4 bg-gray-200 rounded overflow-hidden">
                <div className="h-full bg-indigo-600 rounded" style={{ width: `${primary?.dashaActivation || 0}%` }} />
              </div>
              <div className="w-16 text-right font-bold">{Math.round(primary?.dashaActivation || 0)}%</div>
            </div>
            <div className="flex items-center gap-4">
              <div className="w-32 font-medium text-gray-700">Transit Weight</div>
              <div className="flex-1 h-4 bg-gray-200 rounded overflow-hidden">
                <div className="h-full bg-amber-600 rounded" style={{ width: `${primary?.transitStrength || 0}%` }} />
              </div>
              <div className="w-16 text-right font-bold">{Math.round(primary?.transitStrength || 0)}%</div>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg p-6">
          <h3 className="font-bold text-lg mb-4">Timing Confidence Assessment</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <div className="text-indigo-100 text-xs uppercase">Confidence Level</div>
              <div className="font-bold">{getTimingConfidence(primary)}</div>
            </div>
            <div>
              <div className="text-indigo-100 text-xs uppercase">Current MD/AD</div>
              <div className="font-bold">{primaryChart?.rawOutputs?.breakdown?.engine_outputs?.dashas?.synthesis?.active_md} / {primaryChart?.rawOutputs?.breakdown?.engine_outputs?.dashas?.synthesis?.active_ad}</div>
            </div>
            <div>
              <div className="text-indigo-100 text-xs uppercase">Grade</div>
              <div className="font-bold">{primary?.probGrade || '—'}</div>
            </div>
          </div>
        </div>
      </div>
    </SectionCard>
  );
};

function getTimingConfidence(data: any): string {
  const flags = data?.confidenceFlags || [];
  if (flags.includes('jupiter_transit_positive') || flags.includes('dasha_lord_transiting')) return 'HIGH';
  if (flags.includes('saturn_transit_negative') || flags.includes('saturn_sadesati')) return 'LOW';
  return 'MODERATE';
}

const ExpertComparison: React.FC<{ data: any; mode: string; charts: ChartData[] }> = ({ data, mode, charts }) => {
  const { primary, others } = data;
  
  return (
    <div className="space-y-6">
      <details className="group border border-gray-200 rounded-lg bg-gray-50 mt-6">
        <summary className="flex items-center justify-between p-4 cursor-pointer bg-white border-b border-gray-200">
          <div className="flex items-center gap-3">
            <AlertTriangle className="w-5 h-5 text-yellow-600" />
            <span className="font-bold text-gray-900">Expert Mode: Full Deterministic Evidence</span>
          </div>
          <ChevronDown className="w-5 h-5 text-gray-400 group-open:rotate-180 transition-transform" />
        </summary>
        <div className="p-6 space-y-6">
          {/* Breakdown Scores */}
          <div className="bg-white rounded-lg p-4 border border-gray-200">
            <h4 className="font-bold text-gray-900 mb-4">Transit Activation Breakdown</h4>
            <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
              <ExpertMetric label="Activation Score" value={`${primary?.transitStrength || 0}%`} />
              <ExpertMetric label="House Activation" value={`${primary?.transitBreakdown?.house_activation || 0}%`} />
              <ExpertMetric label="BAV Support" value={`${primary?.transitBreakdown?.bav_support || 0}%`} />
              <ExpertMetric label="Planet Activation" value={`${primary?.transitBreakdown?.planet_activation || 0}%`} />
              <ExpertMetric label="Dasha Sync" value={`${primary?.transitBreakdown?.dasha_sync || 0}%`} />
              <ExpertMetric label="Vedha Obstruction" value={`${primary?.transitBreakdown?.vedha_layer || 0}%`} />
            </div>
          </div>

          {/* Master Probability Breakdown */}
          <div className="bg-white rounded-lg p-4 border border-gray-200">
            <h4 className="font-bold text-gray-900 mb-4">Master Probability Breakdown</h4>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              {Object.entries(primary?.masterBreakdown || {}).map(([key, value]) => (
                <ExpertMetric key={key} label={key.replace(/_/g, ' ')} value={`${Math.round(value as number)}%`} />
              ))}
            </div>
          </div>

          {/* Supporting Factors */}
          <div className="bg-white rounded-lg p-4 border border-gray-200">
            <h4 className="font-bold text-gray-900 mb-4">Supporting Factors</h4>
            <div className="space-y-2">
              {primary?.supportingFactors?.slice(0, 15).map((f: any, idx: number) => (
                <div key={idx} className="flex items-center gap-3 p-2 bg-emerald-50 rounded">
                  <span className="w-2 h-2 rounded bg-emerald-500" />
                  <span className="text-sm font-medium text-emerald-800">{f.factor}</span>
                  <span className="text-sm text-emerald-600 ml-auto">+{f.score}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Obstructing Factors */}
          <div className="bg-white rounded-lg p-4 border border-gray-200">
            <h4 className="font-bold text-gray-900 mb-4">Obstructing Factors</h4>
            <div className="space-y-2">
              {primary?.obstructingFactors?.slice(0, 15).map((f: any, idx: number) => (
                <div key={idx} className="flex items-center gap-3 p-2 bg-red-50 rounded">
                  <span className="w-2 h-2 rounded bg-red-500" />
                  <span className="text-sm font-medium text-red-800">{f.factor}</span>
                  <span className="text-sm text-red-600 ml-auto">{f.score}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Activated Domains */}
          <div className="bg-white rounded-lg p-4 border border-gray-200">
            <h4 className="font-bold text-gray-900 mb-4">Activated Domains</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {Object.entries(primary?.activatedDomains || {}).map(([domain, score]) => (
                <div key={domain} className="p-3 bg-gray-50 rounded">
                  <div className="font-medium capitalize text-gray-900">{domain}</div>
                  <div className="text-2xl font-bold text-indigo-600">{Math.round(score as number)}%</div>
                </div>
              ))}
            </div>
          </div>

          {/* Confidence Flags */}
          <div className="bg-white rounded-lg p-4 border border-gray-200">
            <h4 className="font-bold text-gray-900 mb-4">Confidence Flags</h4>
            <div className="flex flex-wrap gap-2">
              {[
                'jupiter_transit_positive',
                'saturn_transit_negative', 
                'saturn_sadesati',
                'dasha_lord_transiting',
                'all_malefics_obstructing'
              ].map(flag => (
                <span key={flag} className={`px-3 py-1 rounded-full text-xs font-medium ${
                  primary?.confidenceFlags?.includes(flag) 
                    ? 'bg-indigo-100 text-indigo-800' 
                    : 'bg-gray-100 text-gray-600'
                }`}>
                  {flag.replace(/_/g, ' ')}
                  {primary?.confidenceFlags?.includes(flag) && <CheckCircle className="w-3 h-3 inline ml-1" />}
                </span>
              ))}
            </div>
          </div>
        </div>
      </details>
    </div>
  );
};

const ExpertMetric: React.FC<{ label: string; value: string }> = ({ label, value }) => (
  <div className="bg-white rounded-lg p-3 border border-gray-200">
    <div className="text-xs text-gray-500 uppercase tracking-wider">{label}</div>
    <div className="font-bold text-gray-900">{value}</div>
  </div>
);

export default ComparisonWorkspace;
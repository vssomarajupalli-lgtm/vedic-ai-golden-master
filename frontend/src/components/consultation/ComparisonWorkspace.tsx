// @ts-nocheck
import React, { useState, useMemo } from 'react';
import { 
  Plus, Trash2, ChevronDown,
  BarChart2, TrendingUp, Zap,
  Calendar, Clock, Users,
} from 'lucide-react';
import { ActivationTimeline } from './ActivationTimeline';

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
const _CHART_COLORS = [
  '#3b82f6', '#ef4444', '#22c55e', '#f59e0b', '#a855f7'
];

export const ComparisonWorkspace: React.FC<ComparisonWorkspaceProps> = ({
  charts,
  onAddChart,
  onRemoveChart,
}) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'planets' | 'houses' | 'dasha' | 'transit' | 'timeline' | 'probability'>('overview');
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
              { id: 'houses', label: 'House Strength', icon: Calendar },
              { id: 'dasha', label: 'Dasha Activation', icon: Clock },
              { id: 'transit', label: 'Transit/Gochara', icon: Users },
              { id: 'timeline', label: 'Activation Timeline', icon: TrendingUp },
              { id: 'probability', label: 'Probability', icon: BarChart2 }
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
            <OverviewComparison data={comparisonData} />
          )}
          {activeTab === 'planets' && comparisonData && (
            <PlanetsComparison data={comparisonData} />
          )}
          {activeTab === 'houses' && comparisonData && (
            <HousesComparison data={comparisonData} />
          )}
          {activeTab === 'dasha' && comparisonData && (
            <DashaComparison data={comparisonData} primaryChart={primaryChart} />
          )}
          {activeTab === 'transit' && comparisonData && (
            <TransitComparison data={comparisonData} />
          )}
          {activeTab === 'timeline' && primaryChart?.rawOutputs && (
            <ActivationTimeline
              rawOutputs={primaryChart.rawOutputs}
              questionResults={primaryChart.questionResults}
              mode="professional"
              className="h-[800px]"
            />
          )}
          {activeTab === 'probability' && comparisonData && (
            <ProbabilityComparison data={comparisonData} primaryChart={primaryChart} others={comparisonData.others} />
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
    probability: masterProb.final_score || 0,
    probGrade: masterProb.grade || '—',
  };
}

const OverviewComparison = ({ data }: any) => (
  <div className="space-y-6">
    <h2 className="text-xl font-bold text-gray-800">Overview Comparison</h2>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <ComparisonCard 
        label="Dasha Activation" 
        primary={data.primary?.dashaActivation}
        others={data.others?.map((o: any) => o.dashaActivation)}
        format={(v: number) => `${Math.round(v)}%`}
      />
      <ComparisonCard 
        label="Transit Strength" 
        primary={data.primary?.transitStrength}
        others={data.others?.map((o: any) => o.transitStrength)}
        format={(v: number) => `${Math.round(v)}%`}
      />
      <ComparisonCard 
        label="Final Probability" 
        primary={data.primary?.probability}
        others={data.others?.map((o: any) => o.probability)}
        format={(v: number) => `${Math.round(v)}%`}
      />
    </div>
  </div>
);

const ComparisonCard = ({ label, primary, others, format }: any) => (
  <div className="bg-white rounded-lg border border-gray-200 p-4">
    <h3 className="text-sm font-medium text-gray-500 mb-2">{label}</h3>
    <div className="text-3xl font-bold text-indigo-600">{primary ? format(primary) : '—'}</div>
    {others && others.length > 0 && (
      <div className="mt-2 space-y-1">
        {others.map((v: number, i: number) => (
          <div key={i} className="text-sm text-gray-600">{format(v)}</div>
        ))}
      </div>
    )}
  </div>
);

const PlanetsComparison = ({ _data }: any) => (
  <div className="space-y-4">
    <h2 className="text-xl font-bold text-gray-800">Planet Strength Comparison</h2>
    <div className="bg-white rounded-lg border border-gray-200 p-4">
      <p className="text-gray-500">Planet comparison implementation pending...</p>
    </div>
  </div>
);

const HousesComparison = ({ _data }: any) => (
  <div className="space-y-4">
    <h2 className="text-xl font-bold text-gray-800">House Strength Comparison</h2>
    <div className="bg-white rounded-lg border border-gray-200 p-4">
      <p className="text-gray-500">House comparison implementation pending...</p>
    </div>
  </div>
);

const DashaComparison = ({ data, _primaryChart }: any) => {
  const { primary, others } = data;

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold text-gray-800">Dasha Activation Comparison</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <DashaComparisonCard label="Mahadasha" primary={primary?.currentMD} primaryStrength={primary?.mdStrength} others={others.map((o: any) => ({ label: o.currentMD, strength: o.mdStrength }))} />
        <DashaComparisonCard label="Antardasha" primary={primary?.currentAD} primaryStrength={primary?.adStrength} others={others.map((o: any) => ({ label: o.currentAD, strength: o.adStrength }))} />
        <DashaComparisonCard label="Pratyantardasha" primary={primary?.currentPD} primaryStrength={primary?.pdStrength} others={others.map((o: any) => ({ label: o.currentPD, strength: o.pdStrength }))} />
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
    </div>
  );
};

const DashaComparisonCard = ({ label, primary, primaryStrength, others }: any) => (
  <div className="bg-white rounded-lg border border-gray-200 p-4">
    <h3 className="text-sm font-medium text-gray-500 mb-2">{label}</h3>
    <div className="text-2xl font-bold text-indigo-600">{primary || '—'}</div>
    <div className="text-sm text-gray-500 mb-2">{Math.round(primaryStrength || 0)}% strength</div>
    <div className="space-y-1 mt-2">
      {others?.map((o: any, i: number) => (
        <div key={i} className="text-xs text-gray-600">{o.label}: {Math.round(o.strength || 0)}%</div>
      ))}
    </div>
  </div>
);

const TransitComparison = ({ _data }: any) => (
  <div className="space-y-4">
    <h2 className="text-xl font-bold text-gray-800">Transit/Gochara Comparison</h2>
    <div className="bg-white rounded-lg border border-gray-200 p-4">
      <p className="text-gray-500">Transit comparison implementation pending...</p>
    </div>
  </div>
);

const ProbabilityComparison = ({ _data, _primaryChart, _others }: any) => (
  <div className="space-y-4">
    <h2 className="text-xl font-bold text-gray-800">Probability Comparison</h2>
    <div className="bg-white rounded-lg border border-gray-200 p-4">
      <p className="text-gray-500">Probability comparison implementation pending...</p>
    </div>
  </div>
);

export default ActivationTimeline;

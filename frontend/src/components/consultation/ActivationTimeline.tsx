import React, { useMemo } from 'react';
import { 
  Calendar, Clock, TrendingUp, TrendingDown, Minus, BarChart2, Zap,
  ChevronDown, AlertTriangle, CheckCircle
} from 'lucide-react';

interface ActivationTimelineProps {
  rawOutputs: any;
  questionResults?: any[];
  mode?: 'standard' | 'professional' | 'expert' | 'study';
  className?: string;
}

export const ActivationTimeline: React.FC<ActivationTimelineProps> = ({
  rawOutputs,
  questionResults = [],
  mode = 'standard',
  className = ''
}) => {
  const timelineData = useMemo(() => {
    if (!rawOutputs?.breakdown?.engine_outputs?.dashas) return null;
    
    const dashas = rawOutputs.breakdown.engine_outputs.dashas;
    const synthesis = dashas.synthesis || {};
    const timeline = dashas.timeline || [];
    const transit = rawOutputs.breakdown.engine_outputs.transit || {};
    const masterProb = rawOutputs.breakdown.master_probability || {};
    const lifetimeProjection = masterProb.lifetime_projection || [];
    
    return {
      synthesis,
      timeline,
      transit,
      masterProb,
      lifetimeProjection
    };
  }, [rawOutputs]);

  if (!timelineData) {
    return (
      <div className={`bg-gray-50 rounded-lg p-8 text-center ${className}`}>
        <Calendar className="w-12 h-12 text-gray-300 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">Activation Timeline</h3>
        <p className="text-gray-500">Calculate a chart to view the deterministic activation timeline.</p>
      </div>
    );
  }

  const { synthesis, timeline, transit, masterProb, lifetimeProjection } = timelineData;
  
  const currentMD = synthesis.active_md?.capitalize() || 'Unknown';
  const currentAD = synthesis.active_ad?.capitalize() || 'Unknown';
  const currentPD = synthesis.active_pd?.capitalize() || 'Unknown';
  const mdStrength = synthesis.md_strength || 0;
  const adStrength = synthesis.ad_strength || 0;
  const pdStrength = synthesis.pd_strength || 0;
  const dashaStrength = synthesis.dasha_strength || 0;
  const transitStrength = transit.activation_score || 0;
  const overallActivation = Math.round((mdStrength + adStrength + pdStrength) / 3);
  const probability = masterProb.final_score || 0;
  const probabilityGrade = masterProb.grade || 'UNKNOWN';
  
  const remainingDuration = synthesis.pd_end ? 
    calculateRemaining(synthesis.pd_end) : 'Unknown';
  const endsOn = synthesis.pd_end ? formatDate(synthesis.pd_end) : 'Unknown';

  return (
    <div className={`bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden ${className}`}>
      <div className="bg-gradient-to-r from-indigo-600 to-blue-700 p-6 text-white">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold">Deterministic Activation Timeline</h2>
            <p className="text-indigo-100 text-sm">Phase 14H.1 Design Recovery · Presentation Layer Only</p>
          </div>
          <span className={`px-3 py-1 rounded-full text-xs font-medium ${mode === 'expert' ? 'bg-yellow-200 text-yellow-900' : mode === 'professional' ? 'bg-blue-200 text-blue-900' : mode === 'study' ? 'bg-green-200 text-green-900' : 'bg-gray-200 text-gray-900'}`}>
            {mode.toUpperCase()} MODE
          </span>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <ActivationMetric 
            label="OVERALL ACTIVATION" 
            value={`${overallActivation}%`} 
            icon={Zap}
            trend={getTrend(overallActivation)}
            grade={getGrade(overallActivation)}
          />
          <ActivationMetric 
            label="PROBABILITY" 
            value={`${probability}%`} 
            icon={BarChart2}
            trend={getTrend(probability)}
            grade={probabilityGrade}
          />
          <ActivationMetric 
            label="CURRENT TRANSIT" 
            value={`${transitStrength}%`} 
            icon={Clock}
            trend={getTrend(transitStrength)}
            grade={getGrade(transitStrength)}
          />
          <ActivationMetric 
            label="DASHA STRENGTH" 
            value={`${Math.round(dashaStrength)}%`} 
            icon={TrendingUp}
            trend={getTrend(dashaStrength)}
            grade={getGrade(dashaStrength)}
          />
        </div>
      </div>

      <div className="p-6 space-y-6">
        <CurrentPeriodCard
          currentMD={currentMD}
          currentAD={currentAD}
          currentPD={currentPD}
          mdStrength={mdStrength}
          adStrength={adStrength}
          pdStrength={pdStrength}
          overallActivation={overallActivation}
          transitStrength={transitStrength}
          probability={probability}
          probabilityGrade={probabilityGrade}
          remainingDuration={remainingDuration}
          endsOn={endsOn}
        />

        <FutureWindowsSection
          lifetimeProjection={lifetimeProjection}
        />

        <ActivationTrendChart
          timeline={timeline}
        />

        {mode === 'expert' && (
          <ExpertDetailsSection
            synthesis={synthesis}
            transit={transit}
            masterProb={masterProb}
            timeline={timeline}
          />
        )}

        {mode === 'study' && (
          <StudyModeSection
            synthesis={synthesis}
            masterProb={masterProb}
            questionResults={questionResults}
          />
        )}
      </div>
    </div>
  );
};

interface ActivationMetricProps {
  label: string;
  value: string;
  icon: React.ComponentType<{ className?: string }>;
  trend: 'up' | 'down' | 'neutral';
  grade: string;
}

const ActivationMetric: React.FC<ActivationMetricProps> = ({ label, value, icon: Icon, trend, grade }) => (
  <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
    <div className="flex items-center justify-between mb-2">
      <Icon className="w-5 h-5 text-indigo-200" />
      <span className={`text-xs font-medium px-2 py-0.5 rounded ${getGradeColor(grade)}`}>
        {grade}
      </span>
    </div>
    <div className="text-3xl font-bold mb-1">{value}</div>
    <div className="flex items-center gap-1 text-sm text-indigo-200">
      <span className="text-xs uppercase tracking-wider">{label}</span>
      {trend === 'up' && <TrendingUp className="w-4 h-4 text-green-300" />}
      {trend === 'down' && <TrendingDown className="w-4 h-4 text-red-300" />}
      {trend === 'neutral' && <Minus className="w-4 h-4 text-yellow-300" />}
    </div>
  </div>
);

interface CurrentPeriodCardProps {
  currentMD: string;
  currentAD: string;
  currentPD: string;
  mdStrength: number;
  adStrength: number;
  pdStrength: number;
  overallActivation: number;
  transitStrength: number;
  probability: number;
  probabilityGrade: string;
  remainingDuration: string;
  endsOn: string;
}

const CurrentPeriodCard: React.FC<CurrentPeriodCardProps> = ({
  currentMD, currentAD, currentPD,
  mdStrength, adStrength, pdStrength,
  overallActivation, transitStrength,
  probability, probabilityGrade,
  remainingDuration, endsOn
}) => (
  <div className="bg-gray-50 rounded-lg p-6 border border-gray-200">
    <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
      <Clock className="w-5 h-5 text-indigo-600" />
      Current Activation Period
    </h3>
    
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <DashaStrengthCard
        label="MAHADASHA"
        planet={currentMD}
        strength={mdStrength}
        weight="50%"
        color="amber"
        description="Broad theme (6-20 years)"
      />
      <DashaStrengthCard
        label="ANTARDASHA"
        planet={currentAD}
        strength={adStrength}
        weight="30%"
        color="blue"
        description="Specific manifestation (1-3 years)"
      />
      <DashaStrengthCard
        label="PRATYANTARDASHA"
        planet={currentPD}
        strength={pdStrength}
        weight="20%"
        color="purple"
        description="Precision trigger (1-6 months)"
      />
      <TransitStrengthCard
        strength={transitStrength}
        probability={probability}
        probabilityGrade={probabilityGrade}
      />
    </div>

    <div className="bg-white rounded-lg p-4 border border-gray-200">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <DetailItem label="Activation Index" value={`${overallActivation}%`} description="Arithmetic mean of MD+AD+PD" />
        <DetailItem label="Transit Support" value={`${transitStrength}%`} description="Current Gochara activation" />
        <DetailItem label="Final Probability" value={`${probability}% (${probabilityGrade})`} description="Master Probability Engine" />
        <DetailItem label="Period Ends" value={endsOn} description={`Remaining: ${remainingDuration}`} />
      </div>
    </div>
  </div>
);

interface DashaStrengthCardProps {
  label: string;
  planet: string;
  strength: number;
  weight: string;
  color: string;
  description: string;
}

const DashaStrengthCard: React.FC<DashaStrengthCardProps> = ({ label, planet, strength, weight, color, description }) => {
  const colorClasses = {
    amber: 'bg-amber-50 border-amber-200 text-amber-800',
    blue: 'bg-blue-50 border-blue-200 text-blue-800',
    purple: 'bg-purple-50 border-purple-200 text-purple-800',
  };
  
  const Icon = color === 'amber' ? Zap : color === 'blue' ? TrendingUp : TrendingDown;
  
  return (
    <div className={`border rounded-lg p-4 ${colorClasses[color as keyof typeof colorClasses]}`}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs font-bold uppercase tracking-wider">{label}</span>
        <span className="text-xs font-medium px-2 py-0.5 rounded bg-white/50">{weight} weight</span>
      </div>
      <div className="flex items-baseline gap-1 mb-1">
        <span className="text-2xl font-black">{planet}</span>
        <Icon className={`w-5 h-5 ${color === 'amber' ? 'text-amber-500' : color === 'blue' ? 'text-blue-500' : 'text-purple-500'}`} />
      </div>
      <div className="text-3xl font-bold">{strength}%</div>
      <div className="text-xs text-gray-500 mt-1">{description}</div>
      <div className="mt-2 h-2 bg-white/50 rounded-full overflow-hidden">
        <div className={`h-full rounded-full transition-all ${color === 'amber' ? 'bg-amber-500' : color === 'blue' ? 'bg-blue-500' : 'bg-purple-500'}`} style={{ width: `${strength}%` }} />
      </div>
    </div>
  );
};

interface TransitStrengthCardProps {
  strength: number;
  probability: number;
  probabilityGrade: string;
}

const TransitStrengthCard: React.FC<TransitStrengthCardProps> = ({ strength, probability, probabilityGrade }) => (
  <div className="bg-emerald-50 border-emerald-200 text-emerald-800 border rounded-lg p-4">
    <div className="flex items-center justify-between mb-2">
      <span className="text-xs font-bold uppercase tracking-wider">CURRENT TRANSIT</span>
      <span className="text-xs font-medium px-2 py-0.5 rounded bg-white/50">Gochara</span>
    </div>
    <div className="flex items-baseline gap-1 mb-1">
      <span className="text-2xl font-black">{strength}%</span>
      <Zap className="w-5 h-5 text-emerald-500" />
    </div>
    <div className="text-sm">Transit Activation Score</div>
    <div className="mt-2 h-2 bg-white/50 rounded-full overflow-hidden">
      <div className="bg-emerald-500 h-full rounded-full transition-all" style={{ width: `${strength}%` }} />
    </div>
    <div className="mt-2 text-xs text-emerald-700">
      Combined with Dasha → {probability}% ({probabilityGrade})
    </div>
  </div>
);

interface DetailItemProps {
  label: string;
  value: string;
  description: string;
}

const DetailItem: React.FC<DetailItemProps> = ({ label, value, description }) => (
  <div>
    <div className="text-xs text-gray-500 uppercase tracking-wider mb-1">{label}</div>
    <div className="font-bold text-gray-900">{value}</div>
    <div className="text-xs text-gray-500">{description}</div>
  </div>
);

interface FutureWindowsSectionProps {
  lifetimeProjection: any[];
}

const FutureWindowsSection: React.FC<FutureWindowsSectionProps> = ({ lifetimeProjection }) => {
  const futureWindows = lifetimeProjection
    .filter((w: any) => new Date(w.start_date) >= new Date())
    .sort((a: any, b: any) => b.final_probability_pct - a.final_probability_pct)
    .slice(0, 5);

  if (futureWindows.length === 0) return null;

  return (
    <div>
      <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
        <TrendingUp className="w-5 h-5 text-blue-600" />
        Top Future Opportunity Windows
      </h3>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Rank</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Period</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Age</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">MD - AD - PD</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Activation</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Probability</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Grade</th>
              <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Driver</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {futureWindows.map((window: any, idx: number) => (
              <tr key={idx} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                <td className="px-4 py-3 whitespace-nowrap font-bold text-indigo-600">#{idx + 1}</td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                  {formatDate(window.start_date)} - {formatDate(window.end_date)}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                  {window.age || '—'}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-800">
                  {window.md?.capitalize()} - {window.ad?.capitalize()} - {window.pd?.capitalize()}
                </td>
                <td className="px-4 py-3 whitespace-nowrap">
                  <span className={`px-2 py-1 rounded text-xs font-bold ${window.activation_pct >= 70 ? 'bg-green-100 text-green-800' : window.activation_pct >= 50 ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800'}`}>
                    {Math.round(window.activation_pct)}%
                  </span>
                </td>
                <td className="px-4 py-3 whitespace-nowrap font-bold text-indigo-700">
                  {Math.round(window.final_probability_pct)}%
                </td>
                <td className="px-4 py-3 whitespace-nowrap">
                  <span className={`px-2 py-1 rounded text-xs font-medium ${getGradeColor(window.grade)}`}>
                    {window.grade}
                  </span>
                </td>
                <td className="px-4 py-3 text-sm text-gray-600">{window.md?.capitalize()} MD, {window.ad?.capitalize()} AD</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

interface ActivationTrendChartProps {
  timeline: any[];
}

const ActivationTrendChart: React.FC<ActivationTrendChartProps> = ({ timeline }) => {
  if (!timeline.length) return null;

  const chartData = timeline.map((t: any) => ({
    period: `${t.mahadasha?.capitalize()}-${t.antardasha?.capitalize()}`,
    activation: t.dasha_activation || 0,
    probability: (t.md_planet_strength * 0.5 + t.ad_planet_strength * 0.3 + t.pd_planet_strength * 0.2) || 0,
    isCurrent: t.mahadasha === timeline[0]?.mahadasha && t.antardasha === timeline[0]?.antardasha
  })).slice(0, 12);

  return (
    <div>
      <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
        <BarChart2 className="w-5 h-5 text-purple-600" />
        Activation Trend (Next 12 Periods)
      </h3>
      <div className="bg-white border border-gray-200 rounded-lg p-4">
        <div className="space-y-3">
          {chartData.map((data, idx) => (
            <div key={idx} className={`flex items-center gap-3 ${data.isCurrent ? 'bg-blue-50 rounded p-2' : ''}`}>
              <div className="w-32 text-xs font-medium text-gray-600">{data.period}</div>
              <div className="flex-1 h-6 bg-gray-100 rounded overflow-hidden relative">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-indigo-600 rounded" style={{ width: `${data.activation}%` }} />
                {data.isCurrent && <div className="absolute inset-0 border-2 border-blue-500 rounded" />}
              </div>
              <div className="w-20 text-right text-sm font-bold text-indigo-600">{Math.round(data.activation)}%</div>
            </div>
          ))}
        </div>
        <div className="mt-4 text-xs text-gray-500">
          Blue highlight = current period. Bars show deterministic activation percentage from DashaEngine.
        </div>
      </div>
    </div>
  );
};

interface ExpertDetailsSectionProps {
  synthesis: any;
  transit: any;
  masterProb: any;
  timeline: any[];
}

const ExpertDetailsSection: React.FC<ExpertDetailsSectionProps> = ({ synthesis, transit, masterProb, timeline }) => (
  <details className="group border border-gray-200 rounded-lg bg-gray-50">
    <summary className="flex items-center justify-between p-4 cursor-pointer bg-white border-b border-gray-200">
      <div className="flex items-center gap-3">
        <AlertTriangle className="w-5 h-5 text-yellow-600" />
        <span className="font-bold text-gray-900">Expert Mode: Deterministic Details</span>
      </div>
      <ChevronDown className="w-5 h-5 text-gray-400 group-open:rotate-180 transition-transform" />
    </summary>
    <div className="p-4 space-y-4">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <ExpertMetric label="MD Start" value={formatDate(synthesis.md_start)} />
        <ExpertMetric label="MD End" value={formatDate(synthesis.md_end)} />
        <ExpertMetric label="AD Start" value={formatDate(synthesis.ad_start)} />
        <ExpertMetric label="AD End" value={formatDate(synthesis.ad_end)} />
      </div>
      
      <div className="bg-white rounded-lg p-4 border border-gray-200">
        <h4 className="font-bold text-gray-900 mb-3">Transit Synchronization Details</h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div><span className="text-gray-500">Transit Activation:</span> <span className="font-bold ml-2">{transit.activation_score || 0}%</span></div>
          <div><span className="text-gray-500">MD Lord Transit:</span> <span className="font-bold ml-2">{transit.md_lord_transit_strength || '—'}</span></div>
          <div><span className="text-gray-500">AD Lord Transit:</span> <span className="font-bold ml-2">{transit.ad_lord_transit_strength || '—'}</span></div>
          <div><span className="text-gray-500">Sync Bonus:</span> <span className="font-bold ml-2">{transit.dasha_sync_bonus || 0}%</span></div>
        </div>
      </div>

      <div className="bg-white rounded-lg p-4 border border-gray-200">
        <h4 className="font-bold text-gray-900 mb-3">Master Probability Breakdown</h4>
        <div className="space-y-2 text-sm">
          {Object.entries(masterProb.breakdown || {}).map(([key, value]) => (
            <div key={key} className="flex justify-between py-1 border-b border-gray-100">
              <span className="text-gray-600 capitalize">{key.replace(/_/g, ' ')}</span>
              <span className="font-bold text-indigo-700">{Math.round(value as number)}%</span>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-lg p-4 border border-gray-200">
        <h4 className="font-bold text-gray-900 mb-3">Full Timeline (First 20 Periods)</h4>
        <div className="overflow-x-auto">
          <table className="min-w-full text-xs">
            <thead>
              <tr className="bg-gray-50 text-left">
                <th className="p-2">MD</th>
                <th className="p-2">AD</th>
                <th className="p-2">PD</th>
                <th className="p-2">Start</th>
                <th className="p-2">End</th>
                <th className="p-2">MD Str</th>
                <th className="p-2">AD Str</th>
                <th className="p-2">PD Str</th>
                <th className="p-2">Act %</th>
              </tr>
            </thead>
            <tbody>
              {timeline.slice(0, 20).map((t: any, idx: number) => (
                <tr key={idx} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                  <td className="p-2 capitalize">{t.mahadasha}</td>
                  <td className="p-2 capitalize">{t.antardasha}</td>
                  <td className="p-2 capitalize">{t.pratyantardasha}</td>
                  <td className="p-2">{formatDate(t.start_date)}</td>
                  <td className="p-2">{formatDate(t.end_date)}</td>
                  <td className="p-2">{Math.round(t.md_planet_strength || 0)}%</td>
                  <td className="p-2">{Math.round(t.ad_planet_strength || 0)}%</td>
                  <td className="p-2">{Math.round(t.pd_planet_strength || 0)}%</td>
                  <td className="p-2 font-bold text-indigo-600">{Math.round(t.dasha_activation || 0)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </details>
);

interface StudyModeSectionProps {
  synthesis: any;
  masterProb: any;
  questionResults: any[];
}

const StudyModeSection: React.FC<StudyModeSectionProps> = ({ synthesis, masterProb, questionResults }) => (
  <details className="group border border-green-200 rounded-lg bg-green-50">
    <summary className="flex items-center justify-between p-4 cursor-pointer bg-white border-b border-green-200">
      <div className="flex items-center gap-3">
        <CheckCircle className="w-5 h-5 text-green-600" />
        <span className="font-bold text-gray-900">Study Mode: Learning & Verification</span>
      </div>
      <ChevronDown className="w-5 h-5 text-gray-400 group-open:rotate-180 transition-transform" />
    </summary>
    <div className="p-4 space-y-4">
      <div className="bg-white rounded-lg p-4 border border-green-200">
        <h4 className="font-bold text-green-800 mb-3">How Activation Index is Calculated</h4>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between p-2 bg-green-50 rounded">
            <span>Mahadasha Strength ({synthesis.active_md})</span>
            <span className="font-bold">{Math.round(synthesis.md_strength || 0)}% × 50%</span>
          </div>
          <div className="flex justify-between p-2 bg-green-50 rounded">
            <span>Antardasha Strength ({synthesis.active_ad})</span>
            <span className="font-bold">{Math.round(synthesis.ad_strength || 0)}% × 30%</span>
          </div>
          <div className="flex justify-between p-2 bg-green-50 rounded">
            <span>Pratyantardasha Strength ({synthesis.active_pd})</span>
            <span className="font-bold">{Math.round(synthesis.pd_strength || 0)}% × 20%</span>
          </div>
          <div className="flex justify-between p-2 bg-green-100 rounded font-bold border border-green-300">
            <span>Activation Index =</span>
            <span>({Math.round(synthesis.md_strength || 0)} × 0.5) + ({Math.round(synthesis.ad_strength || 0)} × 0.3) + ({Math.round(synthesis.pd_strength || 0)} × 0.2) = {Math.round(synthesis.dasha_strength || 0)}%</span>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg p-4 border border-green-200">
        <h4 className="font-bold text-green-800 mb-3">Probability Flow</h4>
        <div className="space-y-2 text-sm font-mono">
          <div className="flex justify-between p-2 bg-green-50 rounded">
            <span>Natal Promise (40%)</span>
            <span>{Math.round(masterProb.breakdown?.natal_promise || 0)}%</span>
          </div>
          <div className="flex justify-between p-2 bg-green-50 rounded">
            <span>Planet Strength (15%)</span>
            <span>{Math.round(masterProb.breakdown?.planet_strength || 0)}%</span>
          </div>
          <div className="flex justify-between p-2 bg-green-50 rounded">
            <span>House Strength (10%)</span>
            <span>{Math.round(masterProb.breakdown?.house_strength || 0)}%</span>
          </div>
          <div className="flex justify-between p-2 bg-green-50 rounded">
            <span>Dasha Activation (10%)</span>
            <span>{Math.round(masterProb.breakdown?.dasha_activation || 0)}%</span>
          </div>
          <div className="flex justify-between p-2 bg-green-50 rounded">
            <span>Transit Trigger (5%)</span>
            <span>{Math.round(masterProb.breakdown?.transit_trigger || 0)}%</span>
          </div>
          <div className="flex justify-between p-2 bg-green-100 rounded font-bold border border-green-300">
            <span>Final Probability =</span>
            <span>{masterProb.final_score || 0}% ({masterProb.grade})</span>
          </div>
        </div>
      </div>

      {questionResults.length > 0 && (
        <div className="bg-white rounded-lg p-4 border border-green-200">
          <h4 className="font-bold text-green-800 mb-3">Question Analysis Evidence</h4>
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
    return new Date(dateStr).toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' });
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

function getTrend(value: number): 'up' | 'down' | 'neutral' {
  if (value >= 70) return 'up';
  if (value < 40) return 'down';
  return 'neutral';
}

export default ActivationTimeline;

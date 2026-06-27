import { useState } from 'react';
import { Target, Database, TrendingUp, ChevronDown, ChevronRight, Clock, Star, Calendar } from 'lucide-react';

const CollapsibleSection = ({ title, icon: Icon, children, defaultOpen = false }: { title: string, icon: any, children: React.ReactNode, defaultOpen?: boolean }) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden mb-4">
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between p-4 bg-slate-50 hover:bg-slate-100 transition-colors text-left"
      >
        <h3 className="text-lg font-bold text-slate-900 flex items-center">
          <Icon className="w-5 h-5 mr-2 text-indigo-600" />
          {title}
        </h3>
        {isOpen ? <ChevronDown className="w-5 h-5 text-slate-500" /> : <ChevronRight className="w-5 h-5 text-slate-500" />}
      </button>
      {isOpen && (
        <div className="p-4 border-t border-slate-200">
          {children}
        </div>
      )}
    </div>
  );
};

export default function LifetimeIntelligenceTab({ report }: { report: any }) {
  const exec = report.executive_summary;
  const intel = report.lifetime_intelligence;

  return (
    <div className="space-y-8 animate-in fade-in duration-500 pb-20 mt-6">
      
      {/* SECTION A: Executive Summary */}
      <div className="bg-indigo-900 text-white p-8 rounded-xl shadow-md border border-indigo-800">
        <h2 className="text-3xl font-bold mb-6 flex items-center">
          <Target className="w-8 h-8 mr-3 text-indigo-300" />
          Executive Summary
        </h2>
        
        <div className="grid md:grid-cols-4 gap-6">
          <div className="bg-indigo-800/50 p-5 rounded-lg border border-indigo-700 text-center">
            <p className="text-indigo-200 text-xs font-bold uppercase tracking-wider mb-1">Overall Grade</p>
            <p className="text-3xl font-bold text-white">{exec.overall_grade}</p>
          </div>
          <div className="bg-indigo-800/50 p-5 rounded-lg border border-indigo-700 text-center">
            <p className="text-indigo-200 text-xs font-bold uppercase tracking-wider mb-1">Lifetime Trend</p>
            <p className="text-2xl font-bold text-white flex items-center justify-center">
              <TrendingUp className="w-5 h-5 mr-2" />
              {exec.overall_lifetime_trend}
            </p>
          </div>
          <div className="bg-indigo-800/50 p-5 rounded-lg border border-indigo-700 text-center md:col-span-2">
            <p className="text-indigo-200 text-xs font-bold uppercase tracking-wider mb-1">Current Dasha</p>
            <p className="text-2xl font-bold text-white">{exec.current_mahadasha} - {exec.current_antardasha}</p>
            <p className="text-sm text-indigo-300 mt-1">{exec.current_dasha_remaining} remaining</p>
          </div>
        </div>

        <div className="mt-6 grid md:grid-cols-2 gap-4">
          <div className="bg-indigo-800/50 p-4 rounded-lg border border-indigo-700 flex justify-between items-center">
            <span className="text-indigo-200 text-sm font-semibold uppercase">Strongest Area</span>
            <span className="font-bold text-white text-lg">{exec.strongest_life_area}</span>
          </div>
          <div className="bg-indigo-800/50 p-4 rounded-lg border border-indigo-700 flex justify-between items-center">
            <span className="text-indigo-200 text-sm font-semibold uppercase">Weakest Area</span>
            <span className="font-bold text-rose-300 text-lg">{exec.weakest_life_area}</span>
          </div>
          <div className="bg-indigo-800/50 p-4 rounded-lg border border-indigo-700 flex justify-between items-center">
            <span className="text-indigo-200 text-sm font-semibold uppercase">Best Planet</span>
            <span className="font-bold text-emerald-300 text-lg">{exec.best_planet}</span>
          </div>
          <div className="bg-indigo-800/50 p-4 rounded-lg border border-indigo-700 flex justify-between items-center">
            <span className="text-indigo-200 text-sm font-semibold uppercase">Weak Planet</span>
            <span className="font-bold text-rose-300 text-lg">{exec.weak_planet}</span>
          </div>
        </div>
      </div>

      {/* SECTION B: Snapshot */}
      <h2 className="text-2xl font-bold text-slate-900 mt-12 mb-4">Lifetime Horoscope Snapshot</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm text-center">
          <p className="text-slate-500 text-xs font-bold uppercase mb-1">Overall Promise</p>
          <p className="font-bold text-slate-900">{intel.snapshot.overall_promise}</p>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm text-center">
          <p className="text-slate-500 text-xs font-bold uppercase mb-1">Current Trend</p>
          <p className="font-bold text-slate-900">{intel.snapshot.current_trend}</p>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm text-center">
          <p className="text-slate-500 text-xs font-bold uppercase mb-1">Current Opp</p>
          <p className="font-bold text-emerald-600">{intel.snapshot.current_opportunity}</p>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm text-center">
          <p className="text-slate-500 text-xs font-bold uppercase mb-1">Current Challenge</p>
          <p className="font-bold text-rose-600">{intel.snapshot.current_challenge}</p>
        </div>
      </div>

      {/* SECTION C: Life Area Intelligence */}
      <CollapsibleSection title="Life Area Intelligence" icon={Target} defaultOpen={true}>
        <div className="grid md:grid-cols-2 gap-4">
          {intel.life_areas.map((area: any, idx: number) => (
            <div key={idx} className="bg-slate-50 p-4 rounded-lg border border-slate-200">
              <div className="flex justify-between items-center mb-3 pb-2 border-b border-slate-200">
                <span className="font-bold text-slate-800 text-lg">{area.domain_name}</span>
                <span className="px-2 py-1 text-xs font-bold rounded-md bg-indigo-100 text-indigo-800">{area.grade}</span>
              </div>
              <p className="text-sm text-slate-700 mb-2">{area.interpretation}</p>
              <div className="flex justify-between items-center mt-3 pt-2">
                <span className="text-xs font-semibold text-slate-500 uppercase">Outlook</span>
                <span className="text-sm font-bold text-emerald-600">{area.long_term_outlook}</span>
              </div>
            </div>
          ))}
        </div>
      </CollapsibleSection>

      {/* SECTION D: Planet Intelligence */}
      <CollapsibleSection title="Planet Intelligence" icon={Star}>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {intel.planets.map((p: any, idx: number) => (
            <div key={idx} className="bg-slate-50 p-4 rounded-lg border border-slate-200">
              <div className="flex justify-between items-center mb-2">
                <span className="font-bold text-slate-800">{p.planet_name}</span>
                <span className="px-2 py-1 text-xs font-bold rounded-md bg-indigo-100 text-indigo-800">{p.strength_score}%</span>
              </div>
              <p className="text-sm text-slate-600">Dignity: <span className="font-medium text-slate-800">{p.dignity}</span></p>
              <p className="text-sm text-slate-600 mt-1">Nature: <span className="font-medium text-slate-800">{p.functional_nature}</span></p>
            </div>
          ))}
        </div>
      </CollapsibleSection>

      {/* SECTION E: House Intelligence */}
      <CollapsibleSection title="House Intelligence" icon={Database}>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {intel.houses.map((h: any, idx: number) => (
            <div key={idx} className="bg-slate-50 p-4 rounded-lg border border-slate-200">
              <div className="flex justify-between items-center mb-2">
                <span className="font-bold text-slate-800">{h.house_name}</span>
                <span className="px-2 py-1 text-xs font-bold rounded-md bg-indigo-100 text-indigo-800">{h.grade}</span>
              </div>
              <p className="text-sm text-slate-600">Lord: {h.lord}</p>
              {h.occupants?.length > 0 && <p className="text-sm text-slate-600 mt-1">Occupants: {h.occupants.join(', ')}</p>}
            </div>
          ))}
        </div>
      </CollapsibleSection>

      {/* SECTION G: Current Dasha Status */}
      <CollapsibleSection title="Current Dasha Status" icon={Clock}>
        <div className="bg-slate-50 p-6 rounded-lg border border-slate-200 text-center">
          <p className="text-slate-500 font-semibold uppercase tracking-wider text-sm mb-2">Active Period</p>
          <p className="text-2xl font-bold text-slate-900">{intel.current_dasha_status.current_md} - {intel.current_dasha_status.current_ad} - {intel.current_dasha_status.current_pd}</p>
          <div className="mt-4 flex justify-center space-x-4">
             <span className="px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full font-bold text-sm">Activation: {intel.current_dasha_status.current_activation}</span>
             <span className="px-3 py-1 bg-emerald-100 text-emerald-800 rounded-full font-bold text-sm">Grade: {intel.current_dasha_status.current_grade}</span>
          </div>
          <p className="mt-4 text-slate-600">{intel.current_dasha_status.interpretation}</p>
          <p className="mt-2 text-sm text-slate-500 font-bold">{intel.current_dasha_status.remaining_duration} remaining</p>
        </div>
      </CollapsibleSection>

      {/* SECTION H: Timeline */}
      <CollapsibleSection title="Lifetime Timeline (Technical)" icon={Calendar}>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-100 text-slate-700 text-sm">
                <th className="p-3 border-b">Age</th>
                <th className="p-3 border-b">Start Date</th>
                <th className="p-3 border-b">Period (MD-AD-PD)</th>
                <th className="p-3 border-b">Grade</th>
              </tr>
            </thead>
            <tbody>
              {intel.timeline.map((row: any, idx: number) => (
                <tr key={idx} className="border-b hover:bg-slate-50 text-sm text-slate-700">
                  <td className="p-3 whitespace-nowrap">{row.age} yrs</td>
                  <td className="p-3 whitespace-nowrap">{row.start_date}</td>
                  <td className="p-3 font-medium text-slate-900">{row.md.slice(0,3)} - {row.ad.slice(0,3)} - {row.pd.slice(0,3)}</td>
                  <td className="p-3">
                    <span className="px-2 py-1 text-xs font-bold rounded bg-slate-100 text-slate-800">{row.grade}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CollapsibleSection>

    </div>
  );
}

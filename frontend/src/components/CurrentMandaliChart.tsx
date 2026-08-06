import React from 'react';
import type { CurrentChartDTO } from '../types/mandali';

interface CurrentMandaliChartProps {
  data: CurrentChartDTO | null;
}

const PLANET_COLOR: Record<string, string> = {
  SU: 'bg-amber-500',
  MO: 'bg-slate-400',
  MA: 'bg-red-500',
  ME: 'bg-emerald-500',
  JU: 'bg-yellow-400',
  VE: 'bg-pink-400',
  SA: 'bg-indigo-600',
  RA: 'bg-purple-500',
  KE: 'bg-teal-600',
};

const STATUS_COLOR: Record<string, string> = {
  FAVORABLE: 'text-emerald-600',
  NEUTRAL: 'text-slate-600',
  CHALLENGING: 'text-rose-600',
};

const CurrentMandaliChart: React.FC<CurrentMandaliChartProps> = ({ data }) => {
  if (!data || !data.grid?.length) {
    return (
      <div>
        <h2 className="text-lg font-semibold text-slate-900 mb-2">Current Gochara Moon-Centered Rasi Mandali</h2>
        <p className="text-sm text-slate-500">No current gochara mandali data available yet.</p>
      </div>
    );
  }

  return (
    <div>
      <h2 className="text-lg font-semibold text-slate-900 mb-1">{data.chart_name || 'Current Gochara Moon-Centered Rasi Mandali'}</h2>
      <p className="text-sm text-slate-500 mb-4">
        Current transit planets placed in the Moon-centered Mandali grid.
      </p>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {data.grid.map((cell) => (
          <div
            key={cell.mandali_number}
            className="border border-slate-200 rounded-lg p-3 bg-slate-50"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-indigo-700">{cell.mandali_name}</span>
              <span className="text-[10px] text-slate-400">#{cell.mandali_number}</span>
            </div>
            <div className="flex flex-wrap gap-1">
              {cell.planets.length === 0 ? (
                <span className="text-[11px] text-slate-300">—</span>
              ) : (
                cell.planets.map((code, i) => (
                  <span
                    key={`${code}-${i}`}
                    className={`inline-flex items-center justify-center w-8 h-8 rounded-full text-[10px] font-bold text-white ${PLANET_COLOR[code] || 'bg-slate-400'}`}
                    title={code}
                  >
                    {code}
                  </span>
                ))
              )}
            </div>
          </div>
        ))}
      </div>

      {data.placements?.length > 0 && (
        <div className="mt-4 overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="text-left text-xs uppercase tracking-wide text-slate-500 border-b border-slate-200">
                <th className="py-2 pr-4">Planet</th>
                <th className="py-2 pr-4">Mandali</th>
                <th className="py-2 pr-4">Rasi</th>
                <th className="py-2">Status</th>
              </tr>
            </thead>
            <tbody>
              {data.placements.map((p) => (
                <tr key={p.planet} className="border-b border-slate-100">
                  <td className="py-2 pr-4 font-medium text-slate-900">{p.planet}</td>
                  <td className="py-2 pr-4 text-slate-600">{p.mandali?.name || p.mandali?.number}</td>
                  <td className="py-2 pr-4 text-slate-600">{p.rasi || '—'}</td>
                  <td className={`py-2 ${STATUS_COLOR[p.status] || 'text-slate-600'}`}>{p.status || '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default CurrentMandaliChart;
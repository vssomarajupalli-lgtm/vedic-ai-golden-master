import React from 'react';
import type { NatalChartDTO } from '../types/mandali';

interface NatalMandaliChartProps {
  data: NatalChartDTO | null;
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

const NatalMandaliChart: React.FC<NatalMandaliChartProps> = ({ data }) => {
  if (!data || !data.grid?.length) {
    return (
      <div>
        <h2 className="text-lg font-semibold text-slate-900 mb-2">Natal Moon-Centered Rasi Mandali</h2>
        <p className="text-sm text-slate-500">No natal mandali data available yet.</p>
      </div>
    );
  }

  return (
    <div>
      <h2 className="text-lg font-semibold text-slate-900 mb-1">{data.chart_name || 'Natal Moon-Centered Rasi Mandali'}</h2>
      <p className="text-sm text-slate-500 mb-4">
        Moon-centered 12-Mandali grid (9 padas each) from the calculated birth chart.
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
    </div>
  );
};

export default NatalMandaliChart;
import React from 'react';
import type { TransitionSummaryDTO } from '../types/mandali';

interface PlanetTransitionTableProps {
  data: TransitionSummaryDTO | null;
}

const PlanetTransitionTable: React.FC<PlanetTransitionTableProps> = ({ data }) => {
  const items = data?.summary_items || [];

  if (!items.length) {
    return (
      <div>
        <h2 className="text-lg font-semibold text-slate-900 mb-2">Planet Transition Summary</h2>
        <p className="text-sm text-slate-500">No transition summary data available yet.</p>
      </div>
    );
  }

  return (
    <div>
      <h2 className="text-lg font-semibold text-slate-900 mb-1">Planet Transition Summary</h2>
      <p className="text-sm text-slate-500 mb-4">
        Estimated timing for each transit planet to enter its next Mandali.
      </p>

      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="text-left text-xs uppercase tracking-wide text-slate-500 border-b border-slate-200">
              <th className="py-2 pr-4">Planet</th>
              <th className="py-2 pr-4">Current Rasi</th>
              <th className="py-2 pr-4">Current Mandali</th>
              <th className="py-2 pr-4">Next Mandali</th>
              <th className="py-2 pr-4">Est. Entry</th>
              <th className="py-2">Days Left</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.planet} className="border-b border-slate-100">
                <td className="py-2 pr-4 font-medium text-slate-900">{item.planet}</td>
                <td className="py-2 pr-4 text-slate-600">
                  {item.current_rasi || '—'}
                  {item.current_nakshatra && (
                    <span className="block text-[11px] text-slate-400">
                      {item.current_nakshatra} Pada {item.current_pada}
                    </span>
                  )}
                </td>
                <td className="py-2 pr-4 text-slate-600">{item.current_mandali || '—'}</td>
                <td className="py-2 pr-4 text-slate-600">{item.next_mandali || '—'}</td>
                <td className="py-2 pr-4 text-slate-600">{item.estimated_entry_date || '—'}</td>
                <td className="py-2 font-medium text-slate-700">{item.days_remaining ?? '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default PlanetTransitionTable;
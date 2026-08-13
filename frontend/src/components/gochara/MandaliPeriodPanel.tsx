import React from 'react';
import type { MandaliPeriodEntry, MandaliGocharReport } from '../../types/mandali';
import { planetColor, planetCodeForName, statusTone, mandaliStatusTone } from './rasiGrid';

interface MandaliPeriodPanelProps {
  data: MandaliGocharReport | null;
}

/**
 * Mandali-based transit periods (Report B rows).
 *
 * Shows the NEW Rāśi-Mandali period for each planet: Moon-centred Mandali,
 * Nakshatra, Pada, entry/exit, duration, status and next Mandali.
 * This is NOT the conventional Rāśi transit period — it is the Mandali period.
 */
const MandaliPeriodPanel: React.FC<MandaliPeriodPanelProps> = ({ data }) => {
  const periods: MandaliPeriodEntry[] = data?.periods || [];

  if (!periods.length) {
    return (
      <div>
        <h2 className="text-lg font-semibold text-slate-900 mb-2">Rāśi-Mandali Transit Periods</h2>
        <p className="text-sm text-slate-500">No Mandali transit period data available yet.</p>
      </div>
    );
  }

  return (
    <div>
      <h2 className="text-lg font-semibold text-slate-900 mb-1">Rāśi-Mandali Transit Periods</h2>
      <p className="text-sm text-slate-500 mb-4">
        Moon-centred Mandali-based transit window for each planet (Report B). Not the conventional Rāśi period.
      </p>

      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="text-left text-xs uppercase tracking-wide text-slate-500 border-b border-slate-200">
              <th className="py-2 pr-3">Planet</th>
              <th className="py-2 pr-3">Current Mandali</th>
              <th className="py-2 pr-3">Nakshatra</th>
              <th className="py-2 pr-3">Pada</th>
              <th className="py-2 pr-3">Entry</th>
              <th className="py-2 pr-3">Exit</th>
              <th className="py-2 pr-3">Duration</th>
              <th className="py-2 pr-3">Status</th>
              <th className="py-2">Next Mandali</th>
            </tr>
          </thead>
          <tbody>
            {periods.map((p) => (
              <tr key={p.planet} className="border-b border-slate-100">
                <td className="py-2 pr-3">
                  <span className="inline-flex items-center gap-2 font-medium text-slate-900">
                    <span
                      className={`inline-flex items-center justify-center w-5 h-5 rounded-full text-[9px] font-bold text-white ${planetColor(planetCodeForName(p.planet))}`}
                    >
                      {planetCodeForName(p.planet)}
                    </span>
                    {p.planet}
                  </span>
                </td>
                <td className="py-2 pr-3 text-slate-600">{p.mandali_name || `Mandali ${p.mandali_number}`}</td>
                <td className="py-2 pr-3 text-slate-600">{p.nakshatra || '—'}</td>
                <td className="py-2 pr-3 text-slate-600">{p.pada ?? '—'}</td>
                <td className="py-2 pr-3 text-slate-600 whitespace-nowrap">{p.entry_date || '—'}</td>
                <td className="py-2 pr-3 text-slate-600 whitespace-nowrap">{p.exit_date || '—'}</td>
                <td className="py-2 pr-3 text-slate-600">
                  {p.duration_days !== undefined && p.duration_days >= 0 ? `${p.duration_days}d` : '—'}
                </td>
                <td className="py-2 pr-3">
                  <span className={`inline-block px-2 py-0.5 rounded text-[11px] font-semibold ${statusTone(p.status)}`}>
                    {p.status === 'IN_PROGRESS' ? 'IN PROGRESS' : p.status}
                  </span>
                </td>
                <td className="py-2">
                  <span className={mandaliStatusTone(p.mandali_status)}>
                    {p.next_mandali?.name || `Mandali ${p.next_mandali?.number ?? '—'}`}
                  </span>
                  {p.days_remaining !== undefined && p.days_remaining >= 0 && (
                    <span className="block text-[10px] text-slate-400">{p.days_remaining}d remaining</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default MandaliPeriodPanel;
import React from 'react';
import type { MandaliGocharReport, MandaliPeriodEntry, RasiGocharEntry } from '../../types/mandali';
import { planetCodeForName, planetColor, statusTone } from './rasiGrid';

interface ComparisonProps {
  data: MandaliGocharReport | null;
}

/**
 * Side-by-side comparison of the two independent gochar systems:
 *  - Report A  → conventional Rāśi-based gochar (Rāśi boundaries)
 *  - Report B  → Rāśi-Mandali gochar (Moon-centred 9-pada Mandali arcs)
 *
 * Pure renderer. Both systems come from the backend `comparison` block.
 * The regular Rāśi gochar is never replaced — it is shown here for contrast.
 */
const Comparison: React.FC<ComparisonProps> = ({ data }) => {
  if (!data || !data.comparison) return null;

  const reportA: RasiGocharEntry[] = data.comparison.report_a || [];
  const reportB: MandaliPeriodEntry[] = data.comparison.report_b || [];

  if (!reportA.length && !reportB.length) {
    return (
      <div>
        <h2 className="text-lg font-semibold text-slate-900 mb-2">Regular vs Rāśi-Mandali Gochar</h2>
        <p className="text-sm text-slate-500">No comparison data available yet.</p>
      </div>
    );
  }

  const planets = Array.from(
    new Set<string>([...reportA.map((r) => r.planet), ...reportB.map((r) => r.planet)])
  );

  const findA = (planet: string) => reportA.find((r) => r.planet === planet);
  const findB = (planet: string) => reportB.find((r) => r.planet === planet);

  return (
    <div>
      <h2 className="text-lg font-semibold text-slate-900 mb-1">Regular Gochar vs Rāśi-Mandali Gochar</h2>
      <p className="text-sm text-slate-500 mb-4">
        Both systems displayed side by side — the differences between the conventional Rāśi
        boundaries and the Moon-centred Mandali arcs are immediately visible.
      </p>

      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="text-left text-xs uppercase tracking-wide text-slate-500 border-b border-slate-200">
              <th className="py-2 pr-3">Planet</th>
              <th className="py-2 pr-3 bg-blue-50/60">Regular Rāśi</th>
              <th className="py-2 pr-3 bg-blue-50/60">Regular Period</th>
              <th className="py-2 pr-3 bg-indigo-50/60">Mandali</th>
              <th className="py-2 pr-3 bg-indigo-50/60">Nakshatra</th>
              <th className="py-2 pr-3 bg-indigo-50/60">Pada</th>
              <th className="py-2 pr-3 bg-indigo-50/60">Mandali Period</th>
              <th className="py-2 bg-amber-50/60">Difference</th>
            </tr>
          </thead>
          <tbody>
            {planets.map((planet) => {
              const a = findA(planet);
              const b = findB(planet);
              return (
                <tr key={planet} className="border-b border-slate-100">
                  <td className="py-2 pr-3">
                    <span className="inline-flex items-center gap-2 font-medium text-slate-900">
                      <span
                        className={`inline-flex items-center justify-center w-5 h-5 rounded-full text-[9px] font-bold text-white ${planetColor(planetCodeForName(planet))}`}
                      >
                        {planetCodeForName(planet)}
                      </span>
                      {planet}
                    </span>
                  </td>
                  <td className="py-2 pr-3 bg-blue-50/40 text-slate-700">
                    {a?.current_rasi || '—'}
                  </td>
                  <td className="py-2 pr-3 bg-blue-50/40 text-slate-600 whitespace-nowrap">
                    {a ? (
                      <>
                        {a.rasi_entry || '—'} → {a.rasi_exit || '—'}
                        <span className={`ml-2 inline-block px-1.5 py-0.5 rounded text-[10px] font-semibold ${statusTone(a.status)}`}>
                          {a.status === 'IN_PROGRESS' ? 'NOW' : a.status}
                        </span>
                      </>
                    ) : (
                      '—'
                    )}
                  </td>
                  <td className="py-2 pr-3 bg-indigo-50/40 text-slate-700">
                    {b?.mandali_name || (b ? `Mandali ${b.mandali_number}` : '—')}
                  </td>
                  <td className="py-2 pr-3 bg-indigo-50/40 text-slate-700">{b?.nakshatra || '—'}</td>
                  <td className="py-2 pr-3 bg-indigo-50/40 text-slate-700">{b?.pada ?? '—'}</td>
                  <td className="py-2 pr-3 bg-indigo-50/40 text-slate-600 whitespace-nowrap">
                    {b ? (
                      <>
                        {b.entry_date || '—'} → {b.exit_date || '—'}
                        <span className={`ml-2 inline-block px-1.5 py-0.5 rounded text-[10px] font-semibold ${statusTone(b.status)}`}>
                          {b.status === 'IN_PROGRESS' ? 'NOW' : b.status}
                        </span>
                      </>
                    ) : (
                      '—'
                    )}
                  </td>
                  <td className="py-2 bg-amber-50/40">
                    <DifferenceNote a={a} b={b} />
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {data.comparison.note && (
        <p className="mt-3 text-xs text-slate-400">{data.comparison.note}</p>
      )}
    </div>
  );
};

interface DifferenceNoteProps {
  a: RasiGocharEntry | undefined;
  b: MandaliPeriodEntry | undefined;
}

/**
 * Per-planet explanation of WHY the two periods differ. Pure presentation:
 * describes the anchoring of each system (zodiacal Rāśi boundaries vs
 * Moon-centred 9-pada Mandali arcs) using only data already delivered by the
 * backend. No astrology is computed on the frontend.
 */
const DifferenceNote: React.FC<DifferenceNoteProps> = ({ a, b }) => {
  if (!a && !b) return <span className="text-slate-400">—</span>;
  if (!a) {
    return (
      <p className="text-[11px] leading-snug text-slate-600">
        Only the Rāśi-Mandali (Report B) period is available for this planet.
      </p>
    );
  }
  if (!b) {
    return (
      <p className="text-[11px] leading-snug text-slate-600">
        Only the regular Rāśi (Report A) period is available for this planet.
      </p>
    );
  }

  const aPeriod = `${a.rasi_entry || '—'} → ${a.rasi_exit || '—'}`;
  const bPeriod = `${b.entry_date || '—'} → ${b.exit_date || '—'}`;

  return (
    <p className="text-[11px] leading-snug text-slate-600 max-w-[260px]">
      Regular Rāśi gochar anchors to the zodiacal Rāśi{' '}
      <span className="font-medium text-slate-800">{a.current_rasi}</span>; the Rāśi-Mandali
      gochar anchors to the Moon-centred arc{' '}
      <span className="font-medium text-slate-800">{b.mandali_name}</span> ({b.nakshatra} Pada{' '}
      {b.pada}). Rāśi period: {aPeriod} · Mandali period: {bPeriod}.
    </p>
  );
};

export default Comparison;
import React from 'react';
import type {
  MandaliGocharReport,
  SaturnPeriodGroup,
  SaturnMandaliPeriod,
  CurrentSaturnPosition,
  LegacyRasiSaturnWindows,
  LegacySaturnGroup,
} from '../../types/mandali';
import { statusTone } from './rasiGrid';

interface SaturnPanelProps {
  data: MandaliGocharReport | null;
}

/**
 * Dedicated Saturn section for the Present Gochara Rāśi-Mandali report.
 *
 * Shows the Mandali-based Saturn special periods (Sade Sati, Ardha Ashtama,
 * Ashtama, Elinati) resolved through the actual Moon-centred Mandali grid, plus
 * Saturn's current Mandali position. The legacy Rāśi-based lifetime windows are
 * displayed separately and clearly labelled — the two calculation systems are
 * never silently merged.
 */
const SaturnPanel: React.FC<SaturnPanelProps> = ({ data }) => {
  const saturn = data?.saturn_periods;
  if (!saturn) {
    return (
      <div>
        <h2 className="text-lg font-semibold text-slate-900 mb-2">Saturn Special Periods</h2>
        <p className="text-sm text-slate-500">No Saturn period data available yet.</p>
      </div>
    );
  }

  const current = saturn.current_saturn as CurrentSaturnPosition | undefined;

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-end justify-between gap-2">
        <h2 className="text-lg font-semibold text-slate-900">Saturn Special Periods · Rāśi-Mandali</h2>
        <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-indigo-100 text-indigo-700">
          MANDALI RESOLVER
        </span>
      </div>

      {/* Current Saturn position */}
      {current && current.planet && (
        <section className="bg-white border border-slate-200 rounded-xl p-4">
          <h3 className="text-md font-semibold text-slate-900 mb-3">Current Saturn Position</h3>
          <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-3 text-sm">
            <div>
              <p className="text-xs text-slate-500">Mandali</p>
              <p className="font-medium text-slate-900">
                {current.mandali_name || current.mandali_number || '—'}
              </p>
            </div>
            <div>
              <p className="text-xs text-slate-500">Rāśi</p>
              <p className="font-medium text-slate-900">{current.rasi || '—'}</p>
            </div>
            <div>
              <p className="text-xs text-slate-500">Nakshatra</p>
              <p className="font-medium text-slate-900">{current.nakshatra || '—'}</p>
            </div>
            <div>
              <p className="text-xs text-slate-500">Pada</p>
              <p className="font-medium text-slate-900">{current.pada ?? '—'}</p>
            </div>
            <div>
              <p className="text-xs text-slate-500">Entry</p>
              <p className="font-medium text-slate-900">{current.entry_date || '—'}</p>
            </div>
            <div>
              <p className="text-xs text-slate-500">Exit</p>
              <p className="font-medium text-slate-900">{current.exit_date || '—'}</p>
            </div>
          </div>

          {Array.isArray(current.active_flags) && current.active_flags.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-2">
              {current.active_flags.map((flag: string, i: number) => (
                <span key={i} className="px-2 py-0.5 rounded text-[11px] font-medium bg-amber-100 text-amber-800">
                  {flag}
                </span>
              ))}
            </div>
          )}
        </section>
      )}

      {/* Mandali-based windows for each cycle */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <SaturnCycleCard title="Sade Sati" subtitle="12th / 1st / 2nd from Moon" group={saturn.sade_sati} />
        <SaturnCycleCard title="Ardha Ashtama Sani" subtitle="4th from Moon" group={saturn.ardha_ashtama} />
        <SaturnCycleCard title="Ashtama Sani" subtitle="8th from Moon" group={saturn.ashtama} />
        <SaturnCycleCard title="Elinati Sani" subtitle="8th from Moon" group={saturn.elinati} />
      </div>

      {/* Legacy Rāśi-based windows — kept separate and labelled */}
      <LegacyWindows legacy={saturn.legacy_windows} />
    </div>
  );
};

interface SaturnCycleCardProps {
  title: string;
  subtitle: string;
  group: SaturnPeriodGroup;
}

const SaturnCycleCard: React.FC<SaturnCycleCardProps> = ({ title, subtitle, group }) => {
  const rows: SaturnMandaliPeriod[] = [
    ...(group?.current || []),
    ...(group?.upcoming || []),
  ];

  if (!rows.length) {
    return (
      <section className="bg-white border border-slate-200 rounded-xl p-4">
        <h3 className="text-md font-semibold text-slate-900">{title}</h3>
        <p className="text-xs text-slate-500 mb-2">{subtitle}</p>
        <p className="text-xs text-slate-400">No Mandali-resolved windows available.</p>
      </section>
    );
  }

  return (
    <section className="bg-white border border-slate-200 rounded-xl p-4">
      <div className="flex items-center gap-2 mb-1">
        <span className="inline-flex items-center justify-center w-5 h-5 rounded-full text-[9px] font-bold text-white bg-indigo-600">
          SA
        </span>
        <h3 className="text-md font-semibold text-slate-900">{title}</h3>
      </div>
      <p className="text-xs text-slate-500 mb-3">
        {subtitle} · resolved through the Mandali grid (backend)
      </p>

      <div className="overflow-x-auto">
        <table className="min-w-full text-xs">
          <thead>
            <tr className="text-left text-[10px] uppercase tracking-wide text-slate-500 border-b border-slate-200">
              <th className="py-1.5 pr-2">Phase</th>
              <th className="py-1.5 pr-2">Mandali</th>
              <th className="py-1.5 pr-2">Nakshatra</th>
              <th className="py-1.5 pr-2">Pada</th>
              <th className="py-1.5 pr-2">Entry</th>
              <th className="py-1.5 pr-2">Exit</th>
              <th className="py-1.5">Status</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row, i) => (
              <tr key={i} className="border-b border-slate-100">
                <td className="py-1.5 pr-2 font-medium text-slate-800">{row.phase || '—'}</td>
                <td className="py-1.5 pr-2 text-slate-600">{row.mandali_name || row.mandali_number}</td>
                <td className="py-1.5 pr-2 text-slate-600">{row.nakshatra || '—'}</td>
                <td className="py-1.5 pr-2 text-slate-600">{row.pada ?? '—'}</td>
                <td className="py-1.5 pr-2 text-slate-600 whitespace-nowrap">{row.entry || '—'}</td>
                <td className="py-1.5 pr-2 text-slate-600 whitespace-nowrap">{row.exit || '—'}</td>
                <td className="py-1.5">
                  <span className={`inline-block px-1.5 py-0.5 rounded text-[10px] font-semibold ${statusTone(row.status)}`}>
                    {row.status === 'ACTIVE' ? 'ACTIVE' : row.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
};

interface LegacyWindowsProps {
  legacy: LegacyRasiSaturnWindows;
}

const LegacyWindows: React.FC<LegacyWindowsProps> = ({ legacy }) => {
  if (!legacy || Object.keys(legacy).length === 0) return null;

  const mechanism = legacy.mechanism;

  return (
    <details className="bg-amber-50/60 border border-amber-200 rounded-xl p-4">
      <summary className="cursor-pointer text-md font-semibold text-amber-900">
        Legacy Rāśi-Based Saturn Windows
      </summary>
      {mechanism && (
        <p className="mt-2 text-xs text-amber-700">
          Source: <span className="font-mono">{mechanism}</span> — preserved from the classic
          Universal Mandali Engine. Shown separately from the Mandali-resolved periods above.
        </p>
      )}
      <div className="mt-3 grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
        {(
          [
            ['sade_sati', legacy.sade_sati],
            ['elinati_shani', legacy.elinati_shani],
            ['ashtama_shani', legacy.ashtama_shani],
          ] as Array<[string, LegacySaturnGroup | undefined]>
        ).map(([key, value]) => {
          if (!value) return null;
          const cycles: LegacySaturnGroup['cycles'] = value.cycles || [];
          const birth = value.birth_detection;
          return (
            <div key={key} className="bg-white/70 border border-amber-100 rounded-lg p-3">
              <p className="font-semibold text-amber-900 capitalize mb-2">
                {key.replace(/_/g, ' ')}
              </p>
              {!cycles || cycles.length === 0 ? (
                <p className="text-slate-500">No cycles in legacy data.</p>
              ) : (
                <ul className="space-y-1">
                  {cycles.map((cycle) => (
                    <li key={cycle.cycle_number} className="text-slate-700">
                      Cycle {cycle.cycle_number} · {cycle.period}
                    </li>
                  ))}
                </ul>
              )}
              {birth && (
                <p className="mt-2 text-slate-500">
                  Birth: {birth.phase || '—'} phase (cycle {birth.cycle ?? '—'})
                </p>
              )}
            </div>
          );
        })}
      </div>
    </details>
  );
};

export default SaturnPanel;
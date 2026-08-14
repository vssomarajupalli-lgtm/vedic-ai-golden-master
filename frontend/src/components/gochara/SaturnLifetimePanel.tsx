import React from 'react';
import type {
  SaturnLifetimeView,
  SaturnLifetimeCycle,
  SaturnLifetimeCrossRefRow,
} from '../../types/mandali';

interface SaturnLifetimePanelProps {
  data: SaturnLifetimeView | null;
}

/**
 * Saturn Lifetime Cycles (GM-017.6) — presentation-only mirror.
 *
 * The backend (app/builders/lifetime_saturn_view.py) composes this view from the
 * existing engine outputs. The MD/AD/PD Dasha timeline supplies the reference
 * range; every complete natural Saturn period that overlaps/touches the range is
 * displayed with its natural START and END verbatim (never clipped). This
 * component only renders the delivered structure — it performs no Saturn math.
 */
const SaturnLifetimePanel: React.FC<SaturnLifetimePanelProps> = ({ data }) => {
  if (!data) {
    return (
      <div>
        <h2 className="text-lg font-semibold text-slate-900 mb-2">Saturn Lifetime Cycles</h2>
        <p className="text-sm text-slate-500">No Saturn lifetime cycle data available yet.</p>
      </div>
    );
  }

  const cycles = data.cycles || [];

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-end justify-between gap-2">
        <h2 className="text-lg font-semibold text-slate-900">Saturn Lifetime Cycles</h2>
        <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-rose-100 text-rose-700">
          PRESENTATION ONLY
        </span>
      </div>

      <div className="bg-rose-50 border border-rose-200 border-l-4 border-l-rose-600 rounded-lg p-3 text-xs text-rose-900">
        Complete natural Saturn Gochara/Mandali periods within the MD/AD/PD Dasha
        timeline{data.md_ad_pd_range?.start ? ` (${data.md_ad_pd_range.start} → ${data.md_ad_pd_range.end})` : ''}.
        Every period that overlaps/touches the timeline range is shown as its complete
        natural period — natural START and END are never clipped and the DOB is not a
        boundary. Exactly three cycles: Sade Sati (12th / 1st / 2nd from Moon), Ardha
        Ashtama Shani (4th from Moon), Ashtama Shani (8th from Moon). Read-only — no
        new calculations.
      </div>

      <div className="grid grid-cols-1 gap-4">
        {cycles.map((cycle) => (
          <SaturnLifetimeCard key={cycle.key} cycle={cycle} />
        ))}
      </div>

      <CrossReference rows={data.cross_reference?.rows || []} source={data.cross_reference?.source} />
    </div>
  );
};

interface SaturnLifetimeCardProps {
  cycle: SaturnLifetimeCycle;
}

const SaturnLifetimeCard: React.FC<SaturnLifetimeCardProps> = ({ cycle }) => {
  if (!cycle.windows || cycle.windows.length === 0) {
    return (
      <section className="bg-white border border-slate-200 rounded-xl p-4">
        <div className="flex items-center gap-2 mb-1">
          <span className="inline-flex items-center justify-center w-5 h-5 rounded-full text-[9px] font-bold text-white bg-rose-600">
            SA
          </span>
          <h3 className="text-md font-semibold text-slate-900">{cycle.title}</h3>
        </div>
        <p className="text-xs text-slate-500 mb-2">{cycle.subtitle}</p>
        <p className="text-xs text-slate-400">No governed windows available.</p>
      </section>
    );
  }

  return (
    <section className="bg-white border border-slate-200 rounded-xl p-4">
      <div className="flex items-center gap-2 mb-1">
        <span className="inline-flex items-center justify-center w-5 h-5 rounded-full text-[9px] font-bold text-white bg-rose-600">
          SA
        </span>
        <h3 className="text-md font-semibold text-slate-900">{cycle.title}</h3>
        <span className="ml-auto px-2 py-0.5 rounded text-[10px] font-semibold bg-rose-100 text-rose-700">
          {cycle.windows.length} windows
        </span>
      </div>
      <p className="text-xs text-rose-700 mb-3">
        {cycle.subtitle} · governed dates passed through from the existing engine outputs
      </p>

      <div className="overflow-x-auto">
        <table className="min-w-full text-xs">
          <thead>
            <tr className="text-left text-[10px] uppercase tracking-wide text-rose-800 bg-rose-100 border-b border-rose-200">
              <th className="py-1.5 pr-2">Phase</th>
              <th className="py-1.5 pr-2">Rāśi</th>
              <th className="py-1.5 pr-2">Mandali</th>
              <th className="py-1.5 pr-2">Start (natural)</th>
              <th className="py-1.5">End (natural)</th>
            </tr>
          </thead>
          <tbody>
            {cycle.windows.map((w, i) => (
              <tr key={i} className="border-b border-slate-100">
                <td className="py-1.5 pr-2 font-medium text-slate-800">{w.phase || '—'}</td>
                <td className="py-1.5 pr-2 text-slate-600">{w.rasi || '—'}</td>
                <td className="py-1.5 pr-2 text-slate-600">{w.mandali || '—'}</td>
                <td className="py-1.5 pr-2 text-rose-700 whitespace-nowrap">
                  {w.natural_start || w.start || '—'}
                </td>
                <td className="py-1.5 text-slate-600 whitespace-nowrap">{w.natural_end || w.end || '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
};

interface CrossReferenceProps {
  rows: SaturnLifetimeCrossRefRow[];
  source?: string;
}

const CrossReference: React.FC<CrossReferenceProps> = ({ rows, source }) => {
  return (
    <details className="bg-white border border-slate-200 rounded-xl p-4">
      <summary className="cursor-pointer text-md font-semibold text-slate-900">
        MD/AD/PD ↔ Saturn Cross-Reference
        {rows.length > 0 && (
          <span className="ml-2 px-2 py-0.5 rounded text-[10px] font-semibold bg-rose-100 text-rose-700">
            {rows.length} periods
          </span>
        )}
      </summary>
      <div className="mt-3">
        <p className="text-xs text-slate-500 mb-3">
          Read-only pairing of the Dasha timeline with overlapping Saturn windows.
          Source: <span className="font-mono">{source || 'MANDALI_RESOLVER'}</span> — the
          same backend-derived values shown as Saturn badges in the Dasha Analysis
          timeline. No new calculations.
        </p>

        {rows.length === 0 ? (
          <p className="text-xs text-slate-400">
            No MD/AD/PD period overlaps a resolved Saturn window within the governed scan range.
          </p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full text-xs">
              <thead>
                <tr className="text-left text-[10px] uppercase tracking-wide text-slate-500 border-b border-slate-200">
                  <th className="py-1.5 pr-2">Dasha Start</th>
                  <th className="py-1.5 pr-2">MD</th>
                  <th className="py-1.5 pr-2">AD</th>
                  <th className="py-1.5 pr-2">PD</th>
                  <th className="py-1.5">Saturn Period</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((row, i) => (
                  <tr key={i} className="border-b border-slate-100">
                    <td className="py-1.5 pr-2 text-slate-600 whitespace-nowrap">{row.start_date}</td>
                    <td className="py-1.5 pr-2 text-slate-800 capitalize">{row.md}</td>
                    <td className="py-1.5 pr-2 text-slate-800 capitalize">{row.ad}</td>
                    <td className="py-1.5 pr-2 text-slate-800 capitalize">{row.pd}</td>
                    <td className="py-1.5">
                      {(row.saturn_periods || []).length > 0 ? (
                        <span className="flex flex-wrap gap-1">
                          {(row.saturn_periods || []).map((sp, j) => (
                            <span
                              key={j}
                              className="px-1.5 py-0.5 rounded text-[10px] font-semibold bg-rose-100 text-rose-800 whitespace-nowrap"
                            >
                              {sp.cycle}
                              {sp.phase && sp.phase !== sp.cycle ? ` · ${sp.phase}` : ''}
                              {sp.mandali_number ? ` · Mandali ${sp.mandali_number}` : ''}
                            </span>
                          ))}
                        </span>
                      ) : (
                        <span className="text-slate-300">—</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </details>
  );
};

export default SaturnLifetimePanel;
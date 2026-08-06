import React from 'react';
import NatalMandaliChart from '../NatalMandaliChart';
import CurrentMandaliChart from '../CurrentMandaliChart';
import PlanetTransitionTable from '../PlanetTransitionTable';
import type { MandaliAnalysisDTO, MandaliAdvisoryDTO } from '../../types/mandali';

interface MandaliAnalysisSectionProps {
  mandaliAnalysis: MandaliAnalysisDTO | null;
  advisory: MandaliAdvisoryDTO | null;
}

/**
 * Composes the backend MandaliResponseDTO (charts + transition summary) and
 * the MandaliAdvisory (Sade Sati, Ashtama Shani, activations, statements)
 * into the consultation presentation. Presentation-only — no calculations.
 */
export const MandaliAnalysisSection: React.FC<MandaliAnalysisSectionProps> = ({
  mandaliAnalysis,
  advisory,
}) => {
  if (!mandaliAnalysis && !advisory) return null;

  const natal = mandaliAnalysis?.natal_chart || null;
  const current = mandaliAnalysis?.current_chart || null;
  const transition = mandaliAnalysis?.transition_summary || null;

  const referenceMoon = advisory?.reference_moon;
  const currentMandali = advisory?.current_mandali;
  const activations = advisory?.mandali_activations || [];
  const statements = advisory?.important_advisory_statements || [];
  const upcoming = advisory?.upcoming_mandali_events || [];
  const sadeSatiCycles = advisory?.sade_sati?.cycles || [];
  const ashtamaCycles = advisory?.ashtama_shani?.cycles || [];
  const elinatiCycles = advisory?.elinati_shani?.cycles || [];

  const activationStrengthColor = (strength: string) => {
    switch (strength) {
      case 'HIGH': return 'text-emerald-600';
      case 'MEDIUM': return 'text-amber-600';
      default: return 'text-slate-500';
    }
  };

  return (
    <div className="space-y-8">
      {/* Section header */}
      <div className="border-t-2 border-indigo-200 pt-6">
        <h2 className="text-xl font-bold text-slate-900 mb-1">Mandali Analysis</h2>
        <p className="text-sm text-slate-500">
          Moon-centered Mandali (Gochara) analysis computed by the backend.
        </p>
      </div>

      {referenceMoon && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div className="bg-slate-50 border border-slate-200 rounded-lg p-3">
            <p className="text-xs text-slate-500">Reference Moon Rasi</p>
            <p className="font-semibold text-slate-900">{referenceMoon.rasi || '—'}</p>
          </div>
          <div className="bg-slate-50 border border-slate-200 rounded-lg p-3">
            <p className="text-xs text-slate-500">Nakshatra</p>
            <p className="font-semibold text-slate-900">{referenceMoon.nakshatra || '—'}</p>
          </div>
          <div className="bg-slate-50 border border-slate-200 rounded-lg p-3">
            <p className="text-xs text-slate-500">Pada</p>
            <p className="font-semibold text-slate-900">{referenceMoon.pada ?? '—'}</p>
          </div>
          <div className="bg-slate-50 border border-slate-200 rounded-lg p-3">
            <p className="text-xs text-slate-500">Mandali 1 Center</p>
            <p className="font-semibold text-slate-900">{referenceMoon.mandali_1_center || '—'}</p>
          </div>
        </div>
      )}

      {/* Natal Mandali */}
      {natal && (
        <section>
          <NatalMandaliChart data={natal} />
        </section>
      )}

      {/* Current Gochara Mandali */}
      {current && (
        <section>
          <CurrentMandaliChart data={current} />
        </section>
      )}

      {/* Current active Mandali */}
      {currentMandali && (
        <section className="bg-white border border-slate-200 rounded-xl p-5">
          <h3 className="text-md font-semibold text-slate-900 mb-2">Current Mandali</h3>
          <div className="flex flex-wrap items-center gap-x-8 gap-y-2 text-sm">
            <div>
              <span className="text-slate-500">Mandali:</span>{' '}
              <span className="font-medium text-slate-900">{currentMandali.name || currentMandali.number}</span>
            </div>
            <div>
              <span className="text-slate-500">Center Nakshatra:</span>{' '}
              <span className="font-medium text-slate-900">{currentMandali.center_nakshatra || '—'}</span>
            </div>
            <div>
              <span className="text-slate-500">Center Pada:</span>{' '}
              <span className="font-medium text-slate-900">{currentMandali.center_pada ?? '—'}</span>
            </div>
          </div>

          {activations.length > 0 && (
            <div className="mt-3">
              <p className="text-sm font-medium text-slate-700 mb-2">Active Mandalis</p>
              <div className="flex flex-wrap gap-2">
                {activations.map((a, i) => (
                  <span
                    key={i}
                    className="inline-flex items-center gap-2 px-3 py-1 bg-indigo-50 text-indigo-800 rounded-full text-xs"
                  >
                    <span className="font-semibold">Mandali {a.mandali}</span>
                    <span className="text-indigo-600">{a.planets?.join(', ') || ''}</span>
                    <span className={activationStrengthColor(a.activation_strength)}>{a.activation_strength}</span>
                  </span>
                ))}
              </div>
            </div>
          )}
        </section>
      )}

      {/* Planet Transition Summary */}
      {transition && (
        <section>
          <PlanetTransitionTable data={transition} />
        </section>
      )}

      {/* Mandali Advisory */}
      {statements.length > 0 && (
        <section className="bg-white border border-slate-200 rounded-xl p-5">
          <h3 className="text-md font-semibold text-slate-900 mb-3">Mandali Advisory</h3>
          <ul className="space-y-2">
            {statements.map((s, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-slate-700">
                <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-indigo-500 flex-shrink-0" />
                <span>{s}</span>
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* Sade Sati */}
      {sadeSatiCycles.length > 0 && (
        <section className="bg-white border border-slate-200 rounded-xl p-5">
          <h3 className="text-md font-semibold text-slate-900 mb-3">Sade Sati (Saturn Transit)</h3>
          <CycleWindowList cycles={sadeSatiCycles} windowKey="sade_sati_windows" />
        </section>
      )}

      {/* Ashtama Shani */}
      {ashtamaCycles.length > 0 && (
        <section className="bg-white border border-slate-200 rounded-xl p-5">
          <h3 className="text-md font-semibold text-slate-900 mb-3">Ashtama Shani</h3>
          <CycleWindowList cycles={ashtamaCycles} windowKey="ashtama_shani_windows" />
        </section>
      )}

      {/* Elinati Shani */}
      {elinatiCycles.length > 0 && (
        <section className="bg-white border border-slate-200 rounded-xl p-5">
          <h3 className="text-md font-semibold text-slate-900 mb-3">Elinati Shani</h3>
          <CycleWindowList cycles={elinatiCycles} windowKey="elinati_shani_windows" />
        </section>
      )}

      {/* Upcoming Events */}
      {upcoming.length > 0 && (
        <section className="bg-white border border-slate-200 rounded-xl p-5">
          <h3 className="text-md font-semibold text-slate-900 mb-3">Upcoming Events</h3>
          <ul className="space-y-2">
            {upcoming.map((e, i) => (
              <li key={i} className="flex items-center justify-between text-sm">
                <span className="text-slate-700">{e.event}</span>
                <span className="text-slate-500">
                  {e.date}
                  {e.mandali ? ` · Mandali ${e.mandali}` : ''}
                </span>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
};

interface CycleWindowListProps {
  cycles: Array<Record<string, any>>;
  windowKey: string;
}

const CycleWindowList: React.FC<CycleWindowListProps> = ({ cycles, windowKey }) => {
  return (
    <div className="space-y-3">
      {cycles.map((cycle, ci) => {
        const windows: Array<Record<string, any>> = cycle[windowKey] || [];
        if (!windows.length) return null;
        return (
          <div key={ci} className="border border-slate-100 rounded-lg p-3">
            <p className="text-sm font-medium text-slate-800 mb-2">
              Cycle {cycle.cycle_number} · {cycle.period}
            </p>
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm">
                <thead>
                  <tr className="text-left text-xs uppercase tracking-wide text-slate-500 border-b border-slate-200">
                    <th className="py-1.5 pr-4">Phase</th>
                    <th className="py-1.5 pr-4">Rasi</th>
                    <th className="py-1.5 pr-4">Mandali</th>
                    <th className="py-1.5 pr-4">Start</th>
                    <th className="py-1.5">End</th>
                  </tr>
                </thead>
                <tbody>
                  {windows.map((w, wi) => (
                    <tr key={wi} className="border-b border-slate-100">
                      <td className="py-1.5 pr-4 font-medium text-slate-900">{w.phase || '—'}</td>
                      <td className="py-1.5 pr-4 text-slate-600">{w.rasi || '—'}</td>
                      <td className="py-1.5 pr-4 text-slate-600">{w.mandali ?? '—'}</td>
                      <td className="py-1.5 pr-4 text-slate-600">{w.start || '—'}</td>
                      <td className="py-1.5 text-slate-600">{w.end || '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default MandaliAnalysisSection;
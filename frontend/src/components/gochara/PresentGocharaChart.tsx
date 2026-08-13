import React from 'react';
import type { MandaliGocharReport, MandaliGocharCell } from '../../types/mandali';
import { RASI_GRID_POSITION, RASI_SEQUENCE, planetColor } from './rasiGrid';

interface PresentGocharaChartProps {
  data: MandaliGocharReport | null;
}

/**
 * Present Gochara Rāśi-Mandali chart (Report B).
 *
 * Fixed South Indian physical layout (4x4 grid, Mesha top-left running
 * counter-clockwise inward) with person-specific Rāśi numbering: Mandali 1 is
 * centred on the natal Moon, so the Rāśi labels shown in each physical box are
 * the Mandali cell Rāśis delivered by the backend. Each occupied box renders
 * the 9 Nakshatra-Pada positions and the transit planets placed by the backend.
 *
 * Pure renderer — all placement data comes from mandali_gochar_report.chart.
 */
const PresentGocharaChart: React.FC<PresentGocharaChartProps> = ({ data }) => {
  if (!data || !data.chart?.length) {
    return (
      <div>
        <h2 className="text-lg font-semibold text-slate-900 mb-2">Present Gochara Rāśi-Mandali Chart</h2>
        <p className="text-sm text-slate-500">No present gochara mandali chart data available yet.</p>
      </div>
    );
  }

  const referenceMoon = data.reference_moon;
  const cellsByRasi = new Map<string, MandaliGocharCell>();
  for (const cell of data.chart) {
    cellsByRasi.set(cell.rasi, cell);
  }

  return (
    <div>
      <div className="flex flex-wrap items-end justify-between gap-2 mb-3">
        <h2 className="text-lg font-semibold text-slate-900">Present Gochara Rāśi-Mandali Chart</h2>
        {referenceMoon && (
          <p className="text-sm text-slate-500">
            Mandali 1 centred on natal Moon:{' '}
            <span className="font-medium text-slate-700">
              {referenceMoon.rasi} · {referenceMoon.nakshatra} Pada {referenceMoon.pada}
            </span>
          </p>
        )}
      </div>
      <p className="text-sm text-slate-500 mb-4">
        Moon-centred 12-Mandali grid · 9 Nakshatra-Pada slots per box · current transit planets placed by the backend.
      </p>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 sm:gap-3">
        {Array.from({ length: 4 }, (_, row) =>
          Array.from({ length: 4 }, (_, col) => {
            const isCentre = row >= 1 && row <= 2 && col >= 1 && col <= 2;
            const rasi = RASI_SEQUENCE.find(
              (r) => RASI_GRID_POSITION[r].row === row && RASI_GRID_POSITION[r].col === col
            );
            const cell = rasi ? cellsByRasi.get(rasi) : undefined;
            return <GridCell key={`${row}-${col}`} rasi={rasi} cell={cell} isCentre={isCentre} />;
          })
        )}
      </div>
    </div>
  );
};

interface GridCellProps {
  rasi: string | undefined;
  cell: MandaliGocharCell | undefined;
  isCentre: boolean;
}

const GridCell: React.FC<GridCellProps> = ({ rasi, cell, isCentre }) => {
  if (isCentre) {
    return <div className="hidden sm:block" aria-hidden="true" />;
  }

  if (!rasi || !cell) {
    return (
      <div className="border border-slate-200 rounded-lg p-2 sm:p-3 bg-white min-h-[96px]">
        <div className="text-[11px] font-semibold text-slate-400">{rasi || '—'}</div>
        <div className="text-[10px] text-slate-300">No Mandali data</div>
      </div>
    );
  }

  const occupied = cell.padas.filter((s) => s.planets.length > 0);

  return (
    <div className="border border-slate-300 rounded-lg p-2 sm:p-3 bg-white shadow-sm">
      <div className="flex items-center justify-between mb-1.5">
        <span className="text-[11px] sm:text-xs font-bold text-indigo-700 truncate">
          {cell.mandali_name}
        </span>
        <span className="text-[9px] text-slate-400">M{cell.mandali_number}</span>
      </div>
      <div className="grid grid-cols-3 gap-1">
        {cell.padas.map((slot) => (
          <div
            key={slot.position}
            title={`${slot.nakshatra} Pada ${slot.pada} · abs ${slot.absolute_pada}`}
            className={`rounded border px-0.5 py-0.5 text-center min-h-[30px] ${
              slot.planets.length > 0
                ? 'bg-indigo-50 border-indigo-300'
                : 'bg-slate-50 border-slate-200'
            }`}
          >
            <div className="text-[8px] sm:text-[9px] text-slate-500 leading-tight">
              {slot.nakshatra.slice(0, 3)}.{slot.pada}
            </div>
            <div className="flex flex-wrap justify-center gap-0.5 mt-0.5">
              {slot.planets.map((code) => (
                <span
                  key={`${code}-${slot.position}`}
                  className={`inline-flex items-center justify-center w-4 h-4 sm:w-5 sm:h-5 rounded-full text-[8px] sm:text-[9px] font-bold text-white ${planetColor(code)}`}
                  title={code}
                >
                  {code}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
      {occupied.length === 0 && (
        <div className="text-[10px] text-slate-300 text-center mt-1">No transits</div>
      )}
    </div>
  );
};

export default PresentGocharaChart;
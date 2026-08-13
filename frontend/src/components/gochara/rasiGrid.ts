// Pure presentation helpers for the Present Gochara Rāśi-Mandali chart.
// No astrology calculations — the backend is authoritative. The frontend only
// renders the data delivered in engine_outputs.mandali_gochar_report.

// Canonical Rāśi order (matches backend rasi_sequence_registry.json).
export const RASI_SEQUENCE: string[] = [
  'Mesha', 'Vrishabha', 'Mithuna', 'Karkata',
  'Simha', 'Kanya', 'Tula', 'Vrishchika',
  'Dhanus', 'Makara', 'Kumbha', 'Meena',
];

// Fixed South Indian physical chart layout: a 4x4 grid where each Rāśi occupies
// a fixed physical position (Mesha top-left, then counter-clockwise inward).
// row/col are 0-based. The 2x2 centre cells are never used.
export const RASI_GRID_POSITION: Record<string, { row: number; col: number }> = {
  Mesha:      { row: 0, col: 0 },
  Vrishabha:  { row: 0, col: 1 },
  Mithuna:    { row: 0, col: 2 },
  Karkata:    { row: 0, col: 3 },
  Simha:      { row: 1, col: 3 },
  Kanya:      { row: 2, col: 3 },
  Tula:       { row: 3, col: 3 },
  Vrishchika: { row: 3, col: 2 },
  Dhanus:     { row: 3, col: 1 },
  Makara:     { row: 3, col: 0 },
  Kumbha:     { row: 2, col: 0 },
  Meena:      { row: 1, col: 0 },
};

// Short planet codes used by the backend chart (e.g. "SU", "RA").
export const PLANET_CODE: Record<string, string> = {
  Sun: 'SU', Moon: 'MO', Mars: 'MA', Mercury: 'ME',
  Jupiter: 'JU', Venus: 'VE', Saturn: 'SA', Rahu: 'RA', Ketu: 'KE',
};

export const PLANET_COLOR: Record<string, string> = {
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

export function planetColor(code: string): string {
  return PLANET_COLOR[code] || 'bg-slate-400';
}

export function planetCodeForName(name: string): string {
  const key = (name || '').trim();
  return PLANET_CODE[key] || key.slice(0, 2).toUpperCase();
}

export function rasiNumber(name: string): number {
  const idx = RASI_SEQUENCE.indexOf((name || '').trim());
  return idx + 1; // 0 => unknown/absent
}

export function statusTone(status: string): string {
  switch (status) {
    case 'IN_PROGRESS':
    case 'ACTIVE':
      return 'bg-emerald-100 text-emerald-800';
    case 'UPCOMING':
      return 'bg-blue-100 text-blue-800';
    case 'COMPLETED':
      return 'bg-slate-100 text-slate-600';
    case 'NOT_FOUND':
    case 'INACTIVE':
      return 'bg-rose-100 text-rose-700';
    default:
      return 'bg-slate-100 text-slate-600';
  }
}

export function mandaliStatusTone(status: string): string {
  if (status === 'FAVORABLE') return 'text-emerald-600';
  if (status === 'CHALLENGING') return 'text-rose-600';
  return 'text-slate-600';
}
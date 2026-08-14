"""
Phase 3D — MD/AD/PD ↔ Saturn Gochar-Mandali cross-reference builder.

Pure, deterministic composition layer. Given:
  - the Dasha timeline rows (engine_outputs.dashas.timeline, ISO dates), and
  - the Mandali-resolved Saturn special periods
    (engine_outputs.mandali_gochar_report.saturn_periods, MANDALI_RESOLVER),

it computes which Dasha periods overlap which resolved Rāśi-Mandali Saturn
windows and exposes a user-facing badge structure.

Governance (Phase 3D):
  - Display ONLY Sade Sati (Mandali 12→1→2), Ardha Ashtama Shani (Mandali 4),
    Ashtama Shani (Mandali 8). Elinati stays internal-only.
  - Saturn dates come ONLY from the Mandali resolver (MANDALI_RESOLVER).
    NOT_FOUND windows have no real dates and never produce a badge.
  - The scan range is never extended; no dates are invented.
  - Dasha dates are used exactly as supplied (no recalculation).

This module performs no astrology. It only reads two deterministic engine
outputs and reports date-window overlap.
"""

from typing import Any, Dict, List, Optional
from datetime import date, datetime

# Display names per resolver cycle key (user-facing red badges).
CYCLE_DISPLAY = {
    "Sade Sati": "Sade Sati",
    "Ardha Ashtama": "Ardha Ashtama Shani",
    "Ashtama": "Ashtama Shani",
}

# Only these cycles are ever surfaced. Elinati (alias of Ashtama, Mandali 8)
# remains internal-only for compatibility.
DISPLAYABLE_CYCLES = ("Sade Sati", "Ardha Ashtama", "Ashtama")

_SATURN_GROUP_KEYS = ("sade_sati", "ardha_ashtama", "ashtama")

# Governed Mandali per cycle phase (presentation labels; engine advisory
# ``mandali`` integers are internal placeholders and are never used here).
_ADVISORY_WINDOW_KEYS = {
    "sade_sati": ("sade_sati_windows", {"Rising": 12, "Peak": 1, "Setting": 2}),
    "ashtama_shani": ("ashtama_shani_windows", {"Ashtama": 8}),
}


def timeline_display_range(dasha_timeline):
    """Derive the MD/AD/PD reference range from the Dasha timeline.

    start = first row start_date; end = last known finite boundary (the final
    open-ended period's start_date when its end is "Unknown"). Returns
    (date, date) or (None, None) when the timeline is unavailable.
    """
    rows = list(dasha_timeline or [])
    if not rows:
        return None, None
    start = None
    end = None
    for row in rows:
        s = _parse_iso_date(row.get("start_date"))
        if s is not None and (start is None or s < start):
            start = s
        e = _parse_iso_date(row.get("end_date"))
        if e is not None and (end is None or e > end):
            end = e
    if start is None:
        return None, None
    if end is None:
        end = _parse_iso_date(rows[-1].get("start_date"))
    return start, end



def _parse_iso_date(value: str) -> Optional[date]:
    """Parse ISO date (YYYY-MM-DD). Returns None when unparseable."""
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def _parse_dmy_date(value: str) -> Optional[date]:
    """Parse DD.MM.YYYY (canonical date format). Returns None when unparseable."""
    if not value or value in ("—", "-", "--"):
        return None
    try:
        return datetime.strptime(value, "%d.%m.%Y").date()
    except (ValueError, TypeError):
        return None


def _windows_overlap(row_start: date, row_end: Optional[date],
                     win_start: date, win_end: Optional[date]) -> bool:
    """Closed-interval overlap between a Dasha period and a Saturn window.

    An unbounded end (None, e.g. a Dasha row ending 'Unknown') is treated as
    open-ended: a window whose start is at or after the row start overlaps it.
    """
    if row_start is None or win_start is None:
        return False
    if row_end is not None and win_end is not None:
        return row_start <= win_end and win_start <= row_end
    if win_end is not None:
        return win_start >= row_start
    if row_end is not None:
        return win_start <= row_end
    return True


def _collect_resolved_windows(saturn_periods: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Collect only resolver windows that carry real entry/exit dates.

    Rules:
      - Only MANDALI_RESOLVER mechanism rows are eligible.
      - NOT_FOUND rows carry '—' entry/exit and are skipped (never invent dates).
      - Only the three displayable groups are considered (Elinati excluded).
    """
    windows: List[Dict[str, Any]] = []
    groups = saturn_periods or {}
    for group_key in _SATURN_GROUP_KEYS:
        group = groups.get(group_key) or {}
        for row in list(group.get("current", [])) + list(group.get("upcoming", [])):
            mechanism = str(row.get("mechanism", ""))
            if mechanism != "MANDALI_RESOLVER":
                continue
            entry = _parse_dmy_date(row.get("entry"))
            exit_ = _parse_dmy_date(row.get("exit"))
            if entry is None or exit_ is None:
                continue
            cycle = row.get("cycle", "")
            if cycle not in DISPLAYABLE_CYCLES:
                continue
            windows.append({
                "cycle": CYCLE_DISPLAY.get(cycle, cycle),
                "phase": row.get("phase", ""),
                "mandali_number": row.get("mandali_number"),
                "mandali_name": row.get("mandali_name", ""),
                "entry": row.get("entry"),
                "exit": row.get("exit"),
                "status": row.get("status", ""),
                "mechanism": mechanism,
            })
    return windows


def _collect_advisory_windows(
    advisory, display_range=None,
):
    """Collect range-selected LifetimeCycleProjector Sade Sati + Ashtama windows.

    GM-017.6: the lifetime advisory (engine_outputs.mandali_advisory) supplies
    the complete natural Saturn periods. Only the governed displayable cycles
    (Sade Sati, Ashtama Shani) are collected; Elinati stays internal-only. When
    a display_range is provided, only windows overlapping it are retained. All
    dates are passed through verbatim — nothing is clipped or invented.
    """
    windows: List[Dict[str, Any]] = []
    if not advisory:
        return windows
    range_start, range_end = display_range or (None, None)
    for group_key, (window_key, mandali_by_phase) in _ADVISORY_WINDOW_KEYS.items():
        group = (advisory.get(group_key) or {}) or {}
        for cycle in list(group.get("cycles", []) or []):
            if not isinstance(cycle, dict):
                continue
            for w in list(cycle.get(window_key, []) or []):
                if not isinstance(w, dict):
                    continue
                entry = _parse_dmy_date(w.get("start"))
                exit_ = _parse_dmy_date(w.get("end"))
                if entry is None:
                    continue
                if range_start is not None and range_end is not None:
                    win_end = exit_ if exit_ is not None else range_end
                    if entry > range_end or win_end < range_start:
                        continue
                phase = w.get("phase", "")
                mandali_number = mandali_by_phase.get(phase)
                if mandali_number is None:
                    continue
                cycle_name = "Sade Sati" if group_key == "sade_sati" else "Ashtama Shani"
                windows.append({
                    "cycle": cycle_name,
                    "phase": phase,
                    "mandali_number": mandali_number,
                    "mandali_name": f"Mandali {mandali_number} ({w.get('rasi', '—')})",
                    "entry": str(w.get("start", "—")).strip(),
                    "exit": str(w.get("end", "—")).strip(),
                    "status": "",
                    "mechanism": "LIFETIME_PROJECTION",
                })
    return windows


def build_dasha_saturn_cross_reference(
    dasha_timeline: List[Dict[str, Any]],
    saturn_periods: Dict[str, Any],
    advisory: Optional[Dict[str, Any]] = None,
    display_range: Optional[tuple] = None,
) -> Dict[str, Any]:
    """Compute the MD/AD/PD ↔ Saturn cross-reference (single source of truth).

    Returns a deterministic structure:
      {
        "source": "MANDALI_RESOLVER",
        "displayed_cycles": [...],
        "rows": { "<ISO start_date>": [ {badge...}, ... ], ... }
      }

    Rows with no overlapping Saturn window are omitted from ``rows``.

    GM-017.6: the resolver windows (saturn_periods) are always used; when an
    ``advisory`` is supplied, its range-selected Sade Sati + Ashtama windows
    (LifetimeCycleProjector, complete natural periods) are added so the Saturn
    annotations can overlap the relevant MD/AD/PD rows. This is read-only
    overlap matching — no new calculation.
    """
    windows = _collect_resolved_windows(saturn_periods)
    windows += _collect_advisory_windows(advisory, display_range)
    rows: Dict[str, List[Dict[str, Any]]] = {}
    matched_rows = 0
    for dasha_row in dasha_timeline or []:
        start = _parse_iso_date(dasha_row.get("start_date"))
        if start is None:
            continue
        end = _parse_iso_date(dasha_row.get("end_date"))
        matches: List[Dict[str, Any]] = []
        for win in windows:
            win_start = _parse_dmy_date(win["entry"])
            win_end = _parse_dmy_date(win["exit"])
            if win_start is None or win_end is None:
                continue
            if _windows_overlap(start, end, win_start, win_end):
                matches.append(win)
        if matches:
            rows[dasha_row.get("start_date")] = matches
            matched_rows += 1

    return {
        "source": "MANDALI_RESOLVER",
        "displayed_cycles": ["Sade Sati", "Ardha Ashtama Shani", "Ashtama Shani"],
        "matched_rows": matched_rows,
        "resolved_window_count": len(windows),
        "rows": rows,
    }
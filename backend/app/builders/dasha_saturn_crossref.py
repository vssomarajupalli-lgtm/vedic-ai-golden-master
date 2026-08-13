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


def build_dasha_saturn_cross_reference(
    dasha_timeline: List[Dict[str, Any]],
    saturn_periods: Dict[str, Any],
) -> Dict[str, Any]:
    """Compute the MD/AD/PD ↔ Saturn cross-reference (single source of truth).

    Returns a deterministic structure:
      {
        "source": "MANDALI_RESOLVER",
        "displayed_cycles": [...],
        "rows": { "<ISO start_date>": [ {badge...}, ... ], ... }
      }

    Rows with no overlapping Saturn window are omitted from ``rows``.
    """
    windows = _collect_resolved_windows(saturn_periods)
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
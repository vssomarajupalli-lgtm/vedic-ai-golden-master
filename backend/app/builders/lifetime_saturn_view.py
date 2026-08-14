"""
GM-017.6 — Saturn Lifetime Cycles presentation view.

Pure, deterministic presentation composition. Reads ONLY existing engine outputs
and reformats them for display. This module performs no astrology and runs no
calculations:

  - The MD/AD/PD Dasha timeline (engine_outputs.dashas.timeline) supplies the
    reference range (first row start -> last known boundary). The range is a
    SELECTION WINDOW, never a clipping boundary.
  - A governed Saturn period is displayed when it overlaps/touches the range:
        include if  period_start <= range_end  AND  period_end >= range_start.
    Every included period is shown as its COMPLETE natural period. Natural
    START and END are retained verbatim (natural_start / natural_end) — they
    are never clipped to the range and the DOB is never a boundary.
  - Exactly 3 cycles are presented:
        Sade Sati           (Mandali 12 -> 1 -> 2)
        Ardha Ashtama Shani (Mandali 4)
        Ashtama Shani       (Mandali 8)
    Elinati Shani stays internal-only and is never rendered.
  - Sade Sati and Ashtama Shani windows come from the advisory lifetime
    projection (mandali_advisory.<key>.cycles[].<key>_windows). Ardha Ashtama
    comes from the Mandali resolver
    (mandali_gochar_report.saturn_periods.ardha_ashtama) — the governed engine
    provides no historical Ardha Ashtama series, so only the resolver's
    existing current/upcoming windows are ever shown.
  - The displayed Mandali number is the GOVERNED value for the cycle, mapped
    from the governed phase semantics (Sade Sati Rising=12th from Moon=12,
    Peak=Moon rasi=1, Setting=2nd from Moon=2; Ashtama=8th from Moon=8). The
    advisory's own ``mandali`` integer is an internal placeholder and is never
    shown; it is only used as a fallback when a phase is unrecognized. Nothing
    is recomputed — the phase and Rasi are taken verbatim from the governed
    data and the number is a fixed definitional label.
  - The MD/AD/PD <-> Saturn cross-reference is a read-only passthrough of the
    existing engine_outputs["dasha_saturn_cross_reference"] paired with the
    existing Dasha timeline labels. It is never recomputed here.

The output is presentation-only: it never feeds scores, probabilities,
formulas, calibration, or the canonical JSON.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime

from app.builders.dasha_saturn_crossref import timeline_display_range

_DMY = "%d.%m.%Y"
_ISO = "%Y-%m-%d"

# Exactly these three cycles are surfaced (in this order). Elinati stays internal.
# The governed Mandali mapping is the single source of truth for the displayed
# Mandali number (LCP-07 / LCP-08 / LCP-09 semantics). It is applied in the
# presentation only; the engine bytes are never altered.
_CYCLE_SOURCES = (
    {
        "key": "sade_sati",
        "window_key": "sade_sati_windows",
        "title": "Sade Sati",
        "subtitle": "12th / 1st / 2nd from Moon",
        "mandali_by_phase": {"Rising": "12", "Peak": "1", "Setting": "2"},
    },
    {
        "key": "ardha_ashtama",
        "window_key": None,
        "title": "Ardha Ashtama Shani",
        "subtitle": "4th from Moon",
        "mandali_by_phase": {},
    },
    {
        "key": "ashtama_shani",
        "window_key": "ashtama_shani_windows",
        "title": "Ashtama Shani",
        "subtitle": "8th from Moon",
        "mandali_by_phase": {"Ashtama": "8"},
    },
)

_NON_DATE_TOKENS = {"", "—", "-", "--", "unknown", "none"}


def _parse_date(value: Any, *formats: str) -> Optional[datetime]:
    """Parse a date string against the supplied formats. None when unparseable."""
    if not value:
        return None
    s = str(value).strip()
    if s.lower() in _NON_DATE_TOKENS:
        return None
    for fmt in formats:
        try:
            return datetime.strptime(s, fmt)
        except (ValueError, TypeError):
            continue
    return None


def _view_range(dasha_timeline: Any) -> tuple:
    """Derive (range_start_dt, range_end_dt) from the MD/AD/PD timeline.

    Returns (None, None) when the range cannot be derived (then no selection
    is applied — every governed window is passed through verbatim).
    """
    start_d, end_d = timeline_display_range(dasha_timeline)
    if start_d is None:
        return None, None
    start_dt = datetime.combine(start_d, datetime.min.time())
    end_dt = datetime.combine(end_d, datetime.min.time()) if end_d is not None else None
    return start_dt, end_dt


def _select_window(
    phase: Any,
    rasi: Any,
    mandali_label: Any,
    start: Any,
    end: Any,
    range_start: Optional[datetime],
    range_end: Optional[datetime],
) -> Optional[Dict[str, Any]]:
    """Select a governed window by MD/AD/PD range overlap; keep natural dates.

    A window is included when it overlaps/touches the range:
        start <= range_end  AND  end >= range_start
    An open-ended (unparseable) end overlaps whenever its start is within the
    range. The natural START and END are returned verbatim and are never
    clipped to the range or to the DOB. When no range is available the window
    is always included (no dates are ever invented).
    """
    natural_start = str(start).strip() if start else "—"
    natural_end = str(end).strip() if end else "—"
    start_dt = _parse_date(start, _DMY, _ISO)
    if start_dt is None:
        return None
    end_dt = _parse_date(end, _DMY, _ISO)
    if range_start is not None and range_end is not None:
        if end_dt is not None:
            if start_dt > range_end or end_dt < range_start:
                return None
        else:
            if start_dt > range_end:
                return None
    return {
        "phase": phase if phase else "—",
        "rasi": rasi if rasi else "—",
        "mandali": str(mandali_label) if mandali_label not in (None, "") else "—",
        "start": natural_start,
        "end": natural_end,
        "natural_start": natural_start,
        "natural_end": natural_end,
    }


def _collect_ardha_ashtama(
    saturn_periods: Dict[str, Any],
    range_start: Optional[datetime],
    range_end: Optional[datetime],
) -> List[Dict[str, Any]]:
    """Ardha Ashtama windows from the Mandali resolver (Mandali 4)."""
    group = (saturn_periods or {}).get("ardha_ashtama", {}) or {}
    rows = list(group.get("current", []) or []) + list(group.get("upcoming", []) or [])
    windows: List[Dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        if str(row.get("mechanism", "")) != "MANDALI_RESOLVER":
            continue
        label = row.get("mandali_name") or row.get("mandali_number")
        win = _select_window(
            phase=row.get("phase"),
            rasi=row.get("rasi"),
            mandali_label=label,
            start=row.get("entry"),
            end=row.get("exit"),
            range_start=range_start,
            range_end=range_end,
        )
        if win is not None:
            windows.append(win)
    return windows


def _collect_projection_windows(
    advisory: Dict[str, Any],
    key: str,
    window_key: str,
    range_start: Optional[datetime],
    range_end: Optional[datetime],
    mandali_by_phase: Dict[str, str],
) -> List[Dict[str, Any]]:
    """Sade Sati / Ashtama windows from the advisory lifetime projection.

    The displayed Mandali is the GOVERNED value for the cycle, resolved from the
    governed phase semantics via ``mandali_by_phase``. The advisory window's own
    ``mandali`` integer is an internal placeholder and is only used as a
    fallback for unrecognized phases (it is never the primary display label).
    """
    group = (advisory or {}).get(key, {}) or {}
    cycles = group.get("cycles", []) or []
    windows: List[Dict[str, Any]] = []
    for cycle in cycles:
        if not isinstance(cycle, dict):
            continue
        for w in cycle.get(window_key, []) or []:
            if not isinstance(w, dict):
                continue
            phase = w.get("phase")
            governed = mandali_by_phase.get(phase) if phase else None
            mandali_label = governed if governed is not None else w.get("mandali")
            win = _select_window(
                phase=phase,
                rasi=w.get("rasi"),
                mandali_label=mandali_label,
                start=w.get("start"),
                end=w.get("end"),
                range_start=range_start,
                range_end=range_end,
            )
            if win is not None:
                windows.append(win)
    return windows


def _build_cross_reference(engine_outputs: Dict[str, Any]) -> Dict[str, Any]:
    """Read-only passthrough of the existing MD/AD/PD <-> Saturn cross-reference.

    The cross-reference itself (engine_outputs["dasha_saturn_cross_reference"]) is
    the backend single source of truth. Here it is paired with the existing Dasha
    timeline labels so a plain read-only table can be rendered. Nothing is
    recomputed.
    """
    xref = engine_outputs.get("dasha_saturn_cross_reference", {}) or {}
    rows_map = xref.get("rows", {}) or {}
    timeline = ((engine_outputs.get("dashas", {}) or {}).get("timeline", [])) or []

    labels: Dict[str, Dict[str, str]] = {}
    for rec in timeline:
        if not isinstance(rec, dict):
            continue
        start_date = rec.get("start_date")
        if not start_date:
            continue
        labels[str(start_date)] = {
            "md": rec.get("mahadasha", "unknown"),
            "ad": rec.get("antardasha", "unknown"),
            "pd": rec.get("pratyantardasha", "unknown"),
        }

    labeled_rows: List[Dict[str, Any]] = []
    for start_date, badges in rows_map.items():
        lbl = labels.get(str(start_date), {})
        labeled_rows.append({
            "start_date": start_date,
            "md": lbl.get("md", "unknown"),
            "ad": lbl.get("ad", "unknown"),
            "pd": lbl.get("pd", "unknown"),
            "saturn_periods": badges,
        })

    return {
        "source": xref.get("source", "MANDALI_RESOLVER"),
        "displayed_cycles": xref.get("displayed_cycles", []),
        "matched_rows": xref.get("matched_rows", 0),
        "rows": labeled_rows,
    }


def build_saturn_lifetime_view(
    engine_outputs: Dict[str, Any], dob: str = ""
) -> Dict[str, Any]:
    """Compose the Saturn Lifetime Cycles presentation view.

    Args:
        engine_outputs: The existing pipeline engine_outputs dict (mandali_advisory,
            mandali_gochar_report, dashas, dasha_saturn_cross_reference).
        dob: Native birth date (ISO YYYY-MM-DD or DD.MM.YYYY). Display metadata
            only — it is never a presentation boundary.

    Returns:
        A presentation-only dict (never feeds scores or the canonical JSON).
    """
    dob_dt = _parse_date(dob, _ISO, _DMY)
    dob_display = dob_dt.strftime(_DMY) if dob_dt else (str(dob).strip() or "Unknown")

    advisory = engine_outputs.get("mandali_advisory", {}) or {}
    mgr = engine_outputs.get("mandali_gochar_report", {}) or {}
    saturn_periods = mgr.get("saturn_periods", {}) or {}

    timeline = ((engine_outputs.get("dashas", {}) or {}).get("timeline", [])) or []
    range_start, range_end = _view_range(timeline)
    range_display = {
        "start": range_start.strftime(_DMY) if range_start else None,
        "end": range_end.strftime(_DMY) if range_end else None,
    }

    cycles: List[Dict[str, Any]] = []
    for spec in _CYCLE_SOURCES:
        key = spec["key"]
        if spec["window_key"] is None:
            windows = _collect_ardha_ashtama(saturn_periods, range_start, range_end)
        else:
            windows = _collect_projection_windows(
                advisory, key, spec["window_key"], range_start, range_end,
                spec["mandali_by_phase"],
            )
        windows.sort(key=lambda w: _parse_date(w["natural_start"], _DMY) or datetime.min)
        cycles.append({
            "key": key,
            "title": spec["title"],
            "subtitle": spec["subtitle"],
            "windows": windows,
        })

    return {
        "source": "existing engine outputs (no new calculations)",
        "dob": dob_display,
        "md_ad_pd_range": range_display,
        "cycles": cycles,
        "cross_reference": _build_cross_reference(engine_outputs),
    }

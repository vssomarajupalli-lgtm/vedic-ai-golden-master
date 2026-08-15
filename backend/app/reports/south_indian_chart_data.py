"""
South-Indian chart presentation data (PURE PASSTHROUGH).

This module exposes already-existing canonical natal data to the report
rendering layer. It performs NO astrology calculations:

- The D1 Lagna Rasi is read verbatim from the uploaded canonical content
  (vargas.D1.planets.Lagna.sign / ascendant), which is authoritative.
- Natal planet Rasi / degree / house are read verbatim from the canonical
  planet rows (sign, degree, house).
- Nakshatra / Pada for each natal planet are read verbatim from the existing
  backend Mandali natal placements (mandali_analysis.natal_chart.placements).
- Rahu and Ketu are included strictly from the canonical/backed data.
- The only derived numbers are the standard South-Indian house numbering for a
  supplied anchor Rasi (1..12) and the fixed 4x4 grid cell coordinates. These
  are presentation geometry identical to the React reference implementation,
  never an astrology calculation.

Nothing here changes engines, formulas, Mandali/Gochara/Saturn/Dasha logic, or
the canonical JSON. It is a read-only view used only by the HTML/PDF templates.
"""

from typing import Any, Dict, List, Optional

# Canonical Rasi order used by the project presentation layer (matches the
# React reference RASI_SEQUENCE and the backend rasi registry).
RASI_SEQUENCE: List[str] = [
    "Mesha", "Vrishabha", "Mithuna", "Karkata",
    "Simha", "Kanya", "Tula", "Vrishchika",
    "Dhanus", "Makara", "Kumbha", "Meena",
]

# Fixed South-Indian 4x4 physical layout (Meena physically top-left).
# The 4 centre cells (rows 1-2, cols 1-2) are always empty.
# Rows are given top-to-bottom, cells left-to-right; "" = empty centre cell.
SI_GRID: List[List[str]] = [
    ["Meena", "Mesha", "Vrishabha", "Mithuna"],
    ["Kumbha", "", "", "Karkata"],
    ["Makara", "", "", "Simha"],
    ["Dhanus", "Vrishchika", "Tula", "Kanya"],
]

# Canonical sign name mapping (lowercase English -> canonical Rasi name). This
# mirrors the React reference canonicalSignToRasi() and is a name mapping, not
# an astrology computation.
SIGN_TO_RASI: Dict[str, str] = {
    "aries": "Mesha", "taurus": "Vrishabha", "gemini": "Mithuna",
    "cancer": "Karkata", "leo": "Simha", "virgo": "Kanya",
    "libra": "Tula", "scorpio": "Vrishchika", "sagittarius": "Dhanus",
    "capricorn": "Makara", "aquarius": "Kumbha", "pisces": "Meena",
}

# Planet display name -> short code used by the backend charts.
PLANET_CODE: Dict[str, str] = {
    "Sun": "SU", "Moon": "MO", "Mars": "MA", "Mercury": "ME",
    "Jupiter": "JU", "Venus": "VE", "Saturn": "SA", "Rahu": "RA", "Ketu": "KE",
}


def _canonical_rasi(sign: str) -> str:
    """Map any supplied sign fragment to its canonical Rasi name, verbatim."""
    if not sign:
        return ""
    s = str(sign).strip()
    if s in RASI_SEQUENCE:
        return s
    return SIGN_TO_RASI.get(s.lower(), s)


def _rasi_index(rasi: str) -> int:
    if not rasi:
        return -1
    r = _canonical_rasi(rasi)
    return RASI_SEQUENCE.index(r) if r in RASI_SEQUENCE else -1


def _house_from_anchor(rasi: str, anchor_index: int) -> int:
    """South-Indian house number for a Rasi box starting from an anchor Rasi.

    Anchor Rasi is House 1; houses run in the fixed canonical Rasi order.
    Presentation geometry only (mirrors the React houseFromRasi()).
    """
    ri = _rasi_index(rasi)
    if ri < 0 or anchor_index < 0:
        return 0
    diff = (ri - anchor_index) % 12
    return diff + 1


def _find_d1_lagna(canonical_content: Dict[str, Any]) -> Dict[str, Any]:
    """Locate the authoritative D1 Lagna Rasi inside the canonical content.

    Preference order (identical to the React resolveLagnaRasi()):
      vargas.D1.planets.Lagna.sign
      vargas.D1.planets.lagna.sign
      vargas.D1.ascendant.sign
    No fallback to the pipeline's default ascendant_sign (which is a
    normalizer default, not the real Lagna).
    """
    try:
        vargas = canonical_content.get("vargas", {}) or {}
        d1 = vargas.get("D1", vargas.get("d1", {})) or {}
        planets = d1.get("planets", {}) or {}
        d1_lagna = planets.get("Lagna", planets.get("lagna", {})) or {}
        sign = d1_lagna.get("sign") or ""
        degree = d1_lagna.get("degree")
        if sign:
            return {"rasi": _canonical_rasi(sign), "degree": degree}
        asc = d1.get("ascendant", {}) or {}
        sign = asc.get("sign") or ""
        if sign:
            return {"rasi": _canonical_rasi(sign), "degree": asc.get("degree")}
    except Exception:
        pass
    return {"rasi": "", "degree": None}


def _natal_placements_by_planet(report: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Read the existing backend Mandali natal placements keyed by planet name.

    Source: report.mandali_analysis.natal_chart.placements
    (each entry: planet, rasi, nakshatra, pada, mandali). Passthrough only.
    """
    try:
        placements = report["mandali_analysis"]["natal_chart"]["placements"] or []
    except Exception:
        return {}
    out: Dict[str, Dict[str, Any]] = {}
    for p in placements:
        if not isinstance(p, dict):
            continue
        name = str(p.get("planet", "")).strip()
        if name:
            out[name] = {
                "rasi": p.get("rasi") or "",
                "nakshatra": p.get("nakshatra") or "",
                "pada": p.get("pada") if p.get("pada") is not None else "",
            }
    return out


def _natal_planets(
    canonical_content: Dict[str, Any],
    placements: Dict[str, Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    """Compose the per-planet natal snapshot (pure passthrough).

    Planet identity, sign, degree and house come from the canonical planets
    block. Nakshatra/Pada come from the backend Mandali natal placements.
    """
    try:
        canonical_planets = canonical_content.get("planets", {}) or {}
    except Exception:
        canonical_planets = {}

    result: Dict[str, Dict[str, Any]] = {}
    for key, row in canonical_planets.items():
        if not isinstance(row, dict):
            continue
        k = str(key).strip().lower()
        planet_name = k.capitalize()
        code = PLANET_CODE.get(planet_name) or planet_name[:2].upper()
        rasi = _canonical_rasi(row.get("sign", ""))
        placement = placements.get(planet_name, {})
        result[k] = {
            "name": planet_name,
            "code": code,
            "rasi": rasi or placement.get("rasi", ""),
            "degree": row.get("degree") or "",
            "house": row.get("house") if row.get("house") is not None else "",
            "nakshatra": placement.get("nakshatra", ""),
            "pada": placement.get("pada", ""),
        }
    return result


def _reference_moon(report: Dict[str, Any]) -> Dict[str, Any]:
    """Natal Moon reference already computed by the backend gochar report."""
    try:
        rm = report["mandali_gochar_report"]["reference_moon"] or {}
    except Exception:
        rm = {}
    if not isinstance(rm, dict):
        return {}
    return {
        "rasi": rm.get("rasi") or "",
        "nakshatra": rm.get("nakshatra") or "",
        "pada": rm.get("pada") if rm.get("pada") is not None else "",
        "absolute_pada": rm.get("absolute_pada"),
    }


def _house_map(anchor_index: int) -> Dict[str, int]:
    """House number per canonical Rasi for a given anchor (1..12, 0 = none)."""
    return {rasi: _house_from_anchor(rasi, anchor_index) for rasi in RASI_SEQUENCE}


def build_south_indian_chart_data(
    canonical_content: Dict[str, Any],
    report: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """
    Build the report-level South-Indian chart presentation snapshot.

    Pure passthrough of already-existing data (see module docstring).
    Returns None only if there is no usable natal planetary data at all.
    """
    if not isinstance(canonical_content, dict) or not isinstance(report, dict):
        return None

    lagna = _find_d1_lagna(canonical_content)
    placements = _natal_placements_by_planet(report)
    natal_planets = _natal_planets(canonical_content, placements)

    # Graceful degradation: no usable natal data at all -> None so the report
    # simply omits the presentation section (matches empty-pipeline tests).
    if not lagna.get("rasi") and not natal_planets:
        return None

    # Natal planets keyed for easy template iteration (canonical order).
    ordered_planets = []
    for key in sorted(natal_planets.keys()):
        ordered_planets.append(natal_planets[key])

    lagna_index = _rasi_index(lagna.get("rasi", ""))
    moon = _reference_moon(report)
    moon_index = _rasi_index(moon.get("rasi", ""))

    return {
        "natal_lagna": lagna,
        "natal_planets": ordered_planets,
        "planets_by_rasi": _planets_by_rasi(ordered_planets),
        "grid": SI_GRID,
        "rasi_sequence": RASI_SEQUENCE,
        "house_by_rasi_lagna": _house_map(lagna_index),
        "house_by_rasi_moon": _house_map(moon_index),
        "reference_moon": moon,
    }


def _planets_by_rasi(natal_planets: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group natal planets by their canonical Rasi (passthrough reshape)."""
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for p in natal_planets:
        rasi = p.get("rasi") or ""
        if rasi:
            grouped.setdefault(rasi, []).append(p)
    return grouped
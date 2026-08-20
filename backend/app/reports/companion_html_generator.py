"""Question Engine companion HTML renderer (P2).

Additive HTML presentation layer over the existing P1 companion JSON
payload. Performs NO new calculations: it only groups and renders data
that already exists:

  - client identity, catalogue, evaluated results and NOT EVALUATED
    entries (P1 payload)
  - MD/AD/PD dasha timeline (engine_outputs.dashas.timeline — Dasha engine)
  - question-level dasha timing (already inside each P1 result:
    current_dasha_status + future_opportunities, verbatim from the master
    lifetime projection)
  - special Saturn / Mandali periods via the existing governed view
    (app.builders.lifetime_saturn_view.build_saturn_lifetime_view), which
    reads only engine outputs (mandali_advisory / mandali_gochar_report /
    dasha_saturn_cross_reference)

The default main-report template pipeline is completely untouched.
"""

import os
from datetime import datetime
from typing import Any, Dict, List

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.builders.lifetime_saturn_view import build_saturn_lifetime_view

_DATE_FORMATS = ("%d.%m.%Y", "%Y-%m-%d", "%d %b %Y")
_NON_DATE_TOKENS = {"", "—", "-", "--", "unknown", "none"}

_SATURN_OVERLAP_LABELS = {
    "sade_sati": "Sade Sati",
    "ardha_ashtama": "Ardha Ashtama Shani",
    "ashtama_shani": "Ashtama Shani",
}


def _parse_date(value: Any) -> Any:
    """Parse a date against the canonical DMY / ISO formats. None when unparseable."""
    if value is None:
        return None
    s = str(value).strip()
    if s.lower() in _NON_DATE_TOKENS:
        return None
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def _reference_date(pipeline_output: Dict[str, Any]) -> Any:
    """Deterministic reference date for Current/Upcoming/Completed status.

    Prefers the pipeline's enforced target_date_utc; falls back to the reported
    Dasha synthesis target date. Never a wall-clock read.
    """
    raw = pipeline_output.get("target_date_utc")
    if raw:
        try:
            return datetime.fromisoformat(str(raw).replace("Z", "+00:00")).date()
        except ValueError:
            pass
    synthesis = ((pipeline_output.get("engine_outputs", {}) or {}).get("dashas", {}) or {}).get("synthesis", {}) or {}
    return _parse_date(synthesis.get("target_date"))


def _classify_window_natural(start: Any, end: Any, reference: Any) -> str:
    """Classify a window against the reference date using only existing dates."""
    if reference is None:
        return ""
    start_dt = _parse_date(start)
    if start_dt is None:
        return ""
    end_dt = _parse_date(end)
    if end_dt is None:
        return "Current" if start_dt <= reference else "Upcoming"
    if reference < start_dt:
        return "Upcoming"
    if reference > end_dt:
        return "Completed"
    return "Current"


class CompanionHTMLGenerator:
    """Renders the question-companion payload into a standalone HTML document."""

    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(current_dir, "templates")

        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )

    def generate(
        self,
        payload: Dict[str, Any],
        pipeline_output: Dict[str, Any] = None,
    ) -> str:
        template = self.env.get_template("question_companion.html")
        context = self._build_context(payload)
        runtime_input = pipeline_output if pipeline_output is not None else {}
        runtime = self._build_runtime_context(runtime_input)
        self._attach_saturn_overlaps(payload, runtime.get("saturn_cycles", []))
        context.update(runtime)
        return template.render(**context)

    @staticmethod
    def _build_context(payload: Dict[str, Any]) -> Dict[str, Any]:
        catalog = payload.get("question_catalog", []) or []
        results = payload.get("question_results", []) or []
        un_evaluated = payload.get("question_un_evaluated", []) or []

        # Preserve the registry's domain order for stable grouping.
        domain_order: List[str] = []
        for record in catalog:
            name = record.get("domain_name")
            if name is not None and name not in domain_order:
                domain_order.append(name)

        evaluated_by_domain: Dict[str, List[Dict[str, Any]]] = {}
        for result in results:
            evaluated_by_domain.setdefault(result.get("domain"), []).append(result)

        un_evaluated_by_domain: Dict[str, List[Dict[str, Any]]] = {}
        for entry in un_evaluated:
            un_evaluated_by_domain.setdefault(entry.get("domain"), []).append(entry)

        sections = []
        for name in domain_order:
            evaluated = evaluated_by_domain.get(name, [])
            not_evaluated = un_evaluated_by_domain.get(name, [])
            if not evaluated and not not_evaluated:
                continue
            sections.append({
                "domain": name,
                "evaluated": evaluated,
                "un_evaluated": not_evaluated,
            })

        # Stable anchors + clickable navigation items for the left index,
        # generated dynamically from the actual companion data.
        nav_groups: List[Dict[str, Any]] = []
        for si, section in enumerate(sections):
            section["anchor"] = f"group-{si}"
            nav_items = []
            for ei, result in enumerate(section["evaluated"]):
                aid = f"q-{si}-{ei}"
                result["anchor"] = aid
                nav_items.append({
                    "anchor": aid,
                    "label": result.get("question_title") or f"Question {ei + 1}",
                    "kind": "question",
                })
            for ui, entry in enumerate(section["un_evaluated"]):
                aid = f"qn-{si}-{ui}"
                entry["anchor"] = aid
                nav_items.append({
                    "anchor": aid,
                    "label": f"[NOT EVALUATED] Question {entry.get('question_id')}",
                    "kind": "un_evaluated",
                })
            nav_groups.append({
                "anchor": section["anchor"],
                "label": section["domain"],
                "questions": nav_items,
            })

        # Formula method references: unique registry formula_key per evaluated
        # domain (authoritative catalogue metadata, no new sources).
        formula_methods: List[Dict[str, Any]] = []
        for section in sections:
            if not section["evaluated"]:
                continue
            keys = sorted({
                record["formula_key"] for record in catalog
                if record.get("domain_name") == section["domain"] and record.get("formula_key")
            })
            formula_methods.append({"domain": section["domain"], "methods": keys})

        client = payload.get("client_profile", {}) or {}
        metadata = payload.get("metadata", {}) or {}

        return {
            "client": {
                "name": client.get("name", "Unknown"),
                "dob": client.get("dob", ""),
                "tob": client.get("tob", ""),
                "pob": client.get("pob", ""),
            },
            "metadata": {
                "report_id": metadata.get("report_id", ""),
                "generated_at": metadata.get("generated_at", ""),
            },
            "summary": {
                "total": len(catalog),
                "evaluated": len(results),
                "not_evaluated": len(un_evaluated),
            },
            "sections": sections,
            "nav_groups": nav_groups,
            "formula_methods": formula_methods,
        }

    @staticmethod
    def _overlaps(win_start: Any, win_end: Any, period_start: Any, period_end: Any) -> bool:
        """True when the Future Opportunity window overlaps a Saturn period."""
        ws = _parse_date(win_start)
        we = _parse_date(win_end)
        ss = _parse_date(period_start)
        if ws is None or we is None or ss is None:
            return False
        se = _parse_date(period_end)  # open-ended (None) => no upper bound
        if se is not None and ws > se:
            return False
        return we >= ss

    @staticmethod
    def _attach_saturn_overlaps(payload: Dict[str, Any], saturn_cycles: List[Dict[str, Any]]) -> None:
        """Attach governing Saturn overlap labels to each Future Opportunity window.

        Pure existing-date comparison: a window is labeled for a Saturn period
        only when the two intervals overlap (day precision). No new calculation.
        """
        cycles = [
            (label, [(w.get("start"), w.get("end")) for w in (c.get("windows", []) or [])])
            for c in saturn_cycles
            if (label := _SATURN_OVERLAP_LABELS.get(c.get("key")) or c.get("title", ""))
        ]
        for result in payload.get("question_results", []) or []:
            for window in result.get("future_opportunities", []) or []:
                ws, we = window.get("start_date"), window.get("end_date")
                window["saturn_overlaps"] = [
                    label for label, periods in cycles
                    if any(
                        CompanionHTMLGenerator._overlaps(ws, we, ps, pe)
                        for ps, pe in periods
                    )
                ]

    @staticmethod
    def _build_runtime_context(pipeline_output: Dict[str, Any]) -> Dict[str, Any]:
        engine_outputs = pipeline_output.get("engine_outputs", {}) or {}
        reference = _reference_date(pipeline_output)

        # 1. Existing MD/AD/PD dasha timeline (Dasha engine output, verbatim).
        dasha_timeline: List[Dict[str, Any]] = []
        for record in ((engine_outputs.get("dashas", {}) or {}).get("timeline", [])) or []:
            dasha_timeline.append({
                "start": record.get("start_date", ""),
                "end": record.get("end_date", ""),
                "md": record.get("mahadasha", ""),
                "ad": record.get("antardasha", ""),
                "pd": record.get("pratyantardasha", ""),
                "activation": record.get("dasha_activation"),
            })

        # 2. Existing special Saturn / Mandali periods via the governed view
        #    (the same authoritative view the main report renders). Read-only.
        dob = (pipeline_output.get("metadata", {}) or {}).get("dob", "")
        saturn_view = build_saturn_lifetime_view(engine_outputs, dob)

        saturn_cycles: List[Dict[str, Any]] = []
        for cycle in saturn_view.get("cycles", []) or []:
            windows: List[Dict[str, Any]] = []
            for w in cycle.get("windows", []) or []:
                windows.append({
                    "phase": w.get("phase", ""),
                    "rasi": w.get("rasi", ""),
                    "mandali": w.get("mandali", ""),
                    "start": w.get("natural_start", ""),
                    "end": w.get("natural_end", ""),
                    "status": _classify_window_natural(
                        w.get("natural_start"), w.get("natural_end"), reference,
                    ),
                })
            saturn_cycles.append({
                "key": cycle.get("key", ""),
                "title": cycle.get("title", ""),
                "subtitle": cycle.get("subtitle", ""),
                "applicable": bool(windows),
                "windows": windows,
            })

        xref = saturn_view.get("cross_reference", {}) or {}
        saturn_xref = {
            "rows": xref.get("rows", []) or [],
            "matched_rows": xref.get("matched_rows", 0),
        }

        return {
            "reference_date": reference.isoformat() if reference else "",
            "dasha_timeline": dasha_timeline,
            "md_ad_pd_range": saturn_view.get("md_ad_pd_range", {}) or {},
            "saturn_cycles": saturn_cycles,
            "saturn_xref": saturn_xref,
        }


companion_html_generator = CompanionHTMLGenerator()
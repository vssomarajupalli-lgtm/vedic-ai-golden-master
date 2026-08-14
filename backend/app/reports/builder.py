from typing import Any, Dict, List
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from app.schemas.mandali_response import MandaliResponseDTO
from app.formatters.display_formatter import DisplayFormatter
from app.builders.lifetime_saturn_view import build_saturn_lifetime_view

class ReportBuilder:
    """
    Builds a structured, user-facing report from the raw pipeline outputs.
    """
    def build_json_report(self, pipeline_outputs: Dict[str, Any], machine_index: Dict[str, Any], questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Transforms the complex pipeline output into a clean, hierarchical JSON report.
        """
        # Normalize machine_index: accept None, Dict, or List[Dict] (real payloads are
        # delivered as a list of page table blocks). Rejects invalid types gracefully.
        if machine_index is None:
            mi: Dict[str, Any] = {}
        elif isinstance(machine_index, dict):
            mi = machine_index
        elif (
            isinstance(machine_index, list)
            and machine_index
            and isinstance(machine_index[0], dict)
        ):
            mi = machine_index[0]
        else:
            mi = {}

        engine_outputs = pipeline_outputs.get("engine_outputs", {})
        master_prob = pipeline_outputs.get("master_probability", {})
        pipeline_meta = pipeline_outputs.get("metadata", {}) or {}

        # --- Mandali Integration ---
        # Accepts either the dataclass (direct callers) or a dict (pipeline output).
        mandali_dto: MandaliResponseDTO | Any = engine_outputs.get("mandali_response_dto")
        if is_dataclass(mandali_dto) and not isinstance(mandali_dto, type):
            mandali_analysis = asdict(mandali_dto)
        else:
            mandali_analysis = mandali_dto or {}

        mandali_advisory = engine_outputs.get("mandali_advisory", {}) or {}
        mandali_gochar_report = engine_outputs.get("mandali_gochar_report", {}) or {}

        report = {
            "metadata": {
                "report_id": pipeline_meta.get("request_id"),
                "generated_at": pipeline_meta.get("timestamp_utc")
                or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "client_info": {
                    "name": pipeline_meta.get("name"),
                    "dob": pipeline_meta.get("dob"),
                    "tob": pipeline_meta.get("tob"),
                    "pob": pipeline_meta.get("pob"),
                    "latitude": pipeline_meta.get("latitude"),
                    "longitude": pipeline_meta.get("longitude"),
                    "timezone": pipeline_meta.get("timezone"),
                    "consultation_date": pipeline_meta.get("consultation_date"),
                    "ascendant_sign": pipeline_meta.get("ascendant_sign"),
                },
            },
            "master_summary": {
                "final_score": master_prob.get("final_score"),
                "grade": master_prob.get("grade"),
            },
            "mandali_analysis": mandali_analysis,
            "mandali_gochar_report": mandali_gochar_report,
            "natal_promise": engine_outputs.get("natal_promise", {}),
            "dasha_periods": engine_outputs.get("dashas", {}),
            "active_yogas": engine_outputs.get("yogas", {}).get("active_yogas", []),
            "strength_scores": {
                "planets": engine_outputs.get("planets", {}),
                "houses": engine_outputs.get("houses", {}),
            },
            "structured_questions": questions,
            "important_advisory": mandali_advisory.get("important_advisory_statements", []),
            "upcoming_mandali_events": mandali_advisory.get("upcoming_mandali_events", []),
            "current_mandali": mandali_advisory.get("current_mandali"),
        }

        # --- Additive Restoration (GM-017E) ---
        # Re-emit the historical FinalReportSchema display fields consumed by the
        # existing Results frontend. Derived entirely from the existing pipeline
        # output via the existing DisplayFormatter. No new calculations, engines,
        # formulas, weights, or calibration are introduced. All existing keys above
        # are preserved for the Consultation / Gochara frontend.
        native = {}
        if isinstance(machine_index, dict):
            native = machine_index.get("native_info", {}) or {}
        elif isinstance(machine_index, list):
            for item in machine_index:
                if isinstance(item, dict) and item.get("native_info"):
                    native = item["native_info"]
                    break

        client_profile_data = {
            "name": pipeline_meta.get("name") or native.get("name", "Unknown"),
            "dob": pipeline_meta.get("dob") or native.get("dob", "Unknown"),
            "tob": pipeline_meta.get("tob") or native.get("tob", "Unknown"),
            "pob": pipeline_meta.get("pob") or native.get("pob", "Unknown"),
            "latitude": pipeline_meta.get("latitude") or native.get("lat") or native.get("latitude") or 0.0,
            "longitude": pipeline_meta.get("longitude") or native.get("lon") or native.get("longitude") or 0.0,
            "timezone": pipeline_meta.get("timezone") or native.get("tz") or native.get("timezone") or "UTC",
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

        exec_summary = DisplayFormatter.format_executive_summary(pipeline_outputs)
        lifetime_intel = DisplayFormatter.format_lifetime_dashboard(
            pipeline_outputs, client_metadata=client_profile_data
        )
        gochara = DisplayFormatter.format_gochara_report(pipeline_outputs)

        report["client_profile"] = client_profile_data
        report["executive_summary"] = exec_summary.model_dump()
        report["lifetime_intelligence"] = lifetime_intel.model_dump()
        report["question_responses"] = questions or []
        report["gochara_report"] = gochara.model_dump()
        report["formula_verification"] = pipeline_outputs

        # --- GM-017.6 Saturn Lifetime Cycles (presentation-only) ---
        # Pure presentation view: DOB is the display start, the existing natural
        # END of every governed Saturn window is retained, and the MD/AD/PD <->
        # Saturn cross-reference is passed through read-only. Derived entirely
        # from existing engine outputs via the presenter. It never feeds scores,
        # formulas, calibration, or the canonical JSON.
        report["saturn_lifetime_cycles"] = build_saturn_lifetime_view(
            engine_outputs, dob=pipeline_meta.get("dob") or ""
        )
        return report
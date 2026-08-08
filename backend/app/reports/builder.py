from typing import Any, Dict, List
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from app.schemas.mandali_response import MandaliResponseDTO

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
        return report
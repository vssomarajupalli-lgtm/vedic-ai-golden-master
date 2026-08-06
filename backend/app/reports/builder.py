from typing import Any, Dict, List
from dataclasses import asdict
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

        # --- Mandali Integration ---
        mandali_dto: MandaliResponseDTO | None = engine_outputs.get("mandali_response_dto")

        report = {
            "metadata": {
                "report_id": pipeline_outputs.get("metadata", {}).get("request_id"),
                "generated_at": pipeline_outputs.get("metadata", {}).get("timestamp_utc"),
                "client_info": mi.get("native_info", {}),
            },
            "master_summary": {
                "final_score": master_prob.get("final_score"),
                "grade": master_prob.get("grade"),
            },
            "mandali_analysis": asdict(mandali_dto) if mandali_dto else {},
            "natal_promise": engine_outputs.get("natal_promise", {}),
            "dasha_periods": engine_outputs.get("dashas", {}),
            "active_yogas": engine_outputs.get("yogas", {}).get("active_yogas", []),
            "strength_scores": {
                "planets": engine_outputs.get("planets", {}),
                "houses": engine_outputs.get("houses", {}),
            },
            "structured_questions": questions,
        }
        return report
from typing import Dict, Any, List
from datetime import datetime, timezone

from app.reports.schemas import FinalReportSchema
from app.reports.schemas import FinalReportSchema
from app.formatters.display_formatter import DisplayFormatter

class ReportBuilder:
    """
    Orchestrates the conversion of raw PipelineRunner output into 
    the human-readable FinalReportSchema using isolated extractors.
    """
    
    def __init__(self):
        pass

    def build_json_report(self, pipeline_data: Dict[str, Any], machine_index: Dict[str, Any], questions: List[Dict[str, Any]] = None) -> FinalReportSchema:
        """
        Builds the complete immutable report schema (Phase 16E format).
        """
        
        # Extract basic client info if available
        native = {}
        if machine_index:
            if isinstance(machine_index, list):
                for item in machine_index:
                    if isinstance(item, dict) and "native_info" in item:
                        native = item["native_info"]
                        break
            elif isinstance(machine_index, dict):
                native = machine_index.get("native_info", {})
                
        metadata = pipeline_data.get("metadata", {})
        client_profile_data = {
            "name": metadata.get("name") or native.get("name", "Unknown"),
            "dob": metadata.get("dob") or native.get("dob", "Unknown"),
            "tob": metadata.get("tob") or native.get("tob", "Unknown"),
            "pob": metadata.get("pob") or native.get("pob", "Unknown"),
            "latitude": metadata.get("latitude") or native.get("lat") or native.get("latitude") or 0.0,
            "longitude": metadata.get("longitude") or native.get("lon") or native.get("longitude") or 0.0,
            "timezone": metadata.get("timezone") or native.get("tz") or native.get("timezone") or "UTC",
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
            
        exec_summary = DisplayFormatter.format_executive_summary(pipeline_data)
        lifetime_intel = DisplayFormatter.format_lifetime_dashboard(pipeline_data, client_metadata=client_profile_data)
        
        # Tech lifetime analysis is usually present inside questions or we can dump it here.
        # For now, it's just raw dashas.
        tech_analysis = pipeline_data.get("dashas", {}).get("timeline", [])
        
        # Formula verification
        formula_ver = pipeline_data
            
        gochara = DisplayFormatter.format_gochara_report(pipeline_data)
        question_reps = DisplayFormatter.format_question_responses(questions or [], pipeline_data)
            
        return FinalReportSchema(
            generated_at=client_profile_data["generated_at"],
            client_profile=client_profile_data,
            executive_summary=exec_summary,
            lifetime_intelligence=lifetime_intel,
            question_responses=question_reps,
            gochara_report=gochara,
            formula_verification=formula_ver
        )

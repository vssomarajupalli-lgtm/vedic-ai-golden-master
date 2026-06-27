from typing import Dict, Any
from app.reports.schemas import ReportSectionData
from app.reports.sections.base import BaseReportSection

class MasterProbabilitySection(BaseReportSection):
    def extract(self, pipeline_data: Dict[str, Any]) -> ReportSectionData:
        master = pipeline_data.get("master_probability", {})
        score = master.get("final_score", 0.0)
        grade = master.get("grade", "UNKNOWN")
        lifetime_projection = master.get("lifetime_projection", [])
        
        return ReportSectionData(
            title="Master Probability Analysis",
            summary_text=f"The overall chart strength is rated as {grade} with a final score of {score:.1f}/100.",
            data_points={
                "final_score": score, 
                "grade": grade,
                "lifetime_projection": lifetime_projection
            }
        )

class YogaAnalysisSection(BaseReportSection):
    def extract(self, pipeline_data: Dict[str, Any]) -> ReportSectionData:
        yogas_block = pipeline_data.get("engine_outputs", {}).get("yogas", {})
        active_yogas = yogas_block.get("active_yogas", [])
        
        data_points = {y.get("yoga_name", "Unknown"): y.get("strength", 0) for y in active_yogas}
        
        summary = f"Detected {len(active_yogas)} classical Parashari Yogas."
        if active_yogas:
            top_yoga = sorted(active_yogas, key=lambda x: x.get("strength", 0), reverse=True)[0]
            summary += f" The strongest is {top_yoga.get('yoga_name')}."
            
        return ReportSectionData(
            title="Yoga Analysis",
            summary_text=summary,
            data_points={"active_yogas": active_yogas, "summary_map": data_points}
        )

class NatalPromiseSection(BaseReportSection):
    def extract(self, pipeline_data: Dict[str, Any]) -> ReportSectionData:
        promise = pipeline_data.get("engine_outputs", {}).get("natal_promise", {})
        
        # Format the domains for easy rendering
        formatted_domains = {}
        for domain, details in promise.items():
            formatted_domains[domain] = {
                "score": details.get("score", 0),
                "grade": details.get("promise", "UNKNOWN"),
                "primary_house": details.get("primary_house", "")
            }
            
        return ReportSectionData(
            title="Life Domains Analysis",
            summary_text="Evaluation of the 8 core areas of life based on planetary and house strengths.",
            data_points=formatted_domains
        )

class ExecutiveSummarySection(BaseReportSection):
    def extract(self, pipeline_data: Dict[str, Any]) -> ReportSectionData:
        # A lightweight synthesis of top domains and current dasha
        promise = pipeline_data.get("engine_outputs", {}).get("natal_promise", {})
        dasha_synthesis = pipeline_data.get("engine_outputs", {}).get("dashas", {}).get("synthesis", {})
        
        top_domains = sorted(
            promise.items(), 
            key=lambda x: x[1].get("score", 0), 
            reverse=True
        )[:3]
        
        top_names = [d[0].capitalize() for d in top_domains]
        # Phase 9 Step 2: Extract directly from engine_outputs -> dashas -> synthesis
        md_str = str(dasha_synthesis.get('active_md', 'Unknown')).capitalize()
        ad_str = str(dasha_synthesis.get('active_ad', 'Unknown')).capitalize()
        pd_str = str(dasha_synthesis.get('active_pd', 'Unknown')).capitalize()
        
        dasha_str = f"{md_str}-{ad_str}-{pd_str}"
        
        return ReportSectionData(
            title="Executive Summary",
            summary_text=f"The most prominent life domains are {', '.join(top_names)}. The current active timeline is the {dasha_str} Dasha.",
            data_points={
                "top_domains": top_names,
                "current_dasha": dasha_str,
                "mahadasha": md_str,
                "antardasha": ad_str,
                "pratyantardasha": pd_str
            }
        )

class GenericSection(BaseReportSection):
    """Fallback extractor for simple blocks like planet/house strengths."""
    def __init__(self, key: str, title: str):
        self.key = key
        self.title = title

    def extract(self, pipeline_data: Dict[str, Any]) -> ReportSectionData:
        data = pipeline_data.get("engine_outputs", {}).get(self.key, {})
        return ReportSectionData(
            title=self.title,
            summary_text=f"Detailed analysis of {self.title.lower()}.",
            data_points={"raw_data": data}
        )

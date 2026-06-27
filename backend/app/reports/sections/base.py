from abc import ABC, abstractmethod
from typing import Dict, Any
from app.reports.schemas import ReportSectionData

class BaseReportSection(ABC):
    """
    Interface for extracting data from the massive PipelineRunner payload
    into a standardized ReportSectionData block.
    """
    
    @abstractmethod
    def extract(self, pipeline_data: Dict[str, Any]) -> ReportSectionData:
        """
        Safely parses the pipeline_data dictionary. Must not raise KeyErrors
        if expected data is missing (for backwards compatibility).
        """
        pass

from dataclasses import dataclass
from .natal_chart import NatalChartDTO
from .current_chart import CurrentChartDTO
from .transition_summary import TransitionSummaryDTO

@dataclass(frozen=True)
class MandaliResponseDTO:
    """The final DTO passed to the frontend for Mandali-related data."""
    schema_version: str
    natal_chart: NatalChartDTO
    current_chart: CurrentChartDTO
    transition_summary: TransitionSummaryDTO
from dataclasses import dataclass, field
from typing import List, Dict, Any
from .mandali_chart_cell import MandaliChartCell

@dataclass(frozen=True)
class CurrentTransitPlanetPlacement:
    """Represents the position of a single transit planet within the Mandali grid."""
    planet: str
    rasi: str
    nakshatra: str
    pada: int
    mandali: Dict[str, Any]  # e.g., {"number": int, "name": str}
    status: str # FAVORABLE | NEUTRAL | CHALLENGING

@dataclass(frozen=True)
class CurrentChartDTO:
    """DTO for the Current Gochara Moon-Centered Rasi Mandali chart."""
    chart_name: str = "Current Gochara Moon-Centered Rasi Mandali"
    placements: List[CurrentTransitPlanetPlacement] = field(default_factory=list) # Raw placements for TransitEngine
    grid: List[MandaliChartCell] = field(default_factory=list) # Formatted grid for frontend
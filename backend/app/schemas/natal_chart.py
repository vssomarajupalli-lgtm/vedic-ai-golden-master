from dataclasses import dataclass, field
from typing import List, Dict, Any
from .mandali_chart_cell import MandaliChartCell

@dataclass(frozen=True)
class NatalPlanetPlacement:
    """Represents the position of a single natal planet within the Mandali grid."""
    planet: str
    rasi: str
    nakshatra: str
    pada: int
    mandali: Dict[str, Any]  # e.g., {"number": int, "name": str}

@dataclass(frozen=True)
class NatalChartDTO:
    """DTO for the Natal Moon-Centered Rasi Mandali chart."""
    chart_name: str = "Natal Moon-Centered Rasi Mandali"
    placements: List[NatalPlanetPlacement] = field(default_factory=list) # Raw placements for potential backend use
    grid: List[MandaliChartCell] = field(default_factory=list) # Formatted grid for frontend
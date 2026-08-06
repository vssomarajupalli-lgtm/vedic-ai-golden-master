from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class PlanetTransitionSummaryItem:
    """A single item in the planet transition summary."""
    planet: str
    current_rasi: str
    current_nakshatra: str
    current_pada: int
    current_mandali: str
    next_mandali: str
    estimated_entry_date: str
    days_remaining: int

@dataclass(frozen=True)
class TransitionSummaryDTO:
    """DTO for the Planet Transition Summary."""
    summary_items: List[PlanetTransitionSummaryItem] = field(default_factory=list)
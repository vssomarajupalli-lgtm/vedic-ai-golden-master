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
    start_date: str  # When the planet entered its current transit (DD.MM.YYYY)
    estimated_entry_date: str  # When the planet is expected to enter the next Mandali
    days_remaining: int
    duration_days: int  # estimated_entry_date - start_date, in days

@dataclass(frozen=True)
class TransitionSummaryDTO:
    """DTO for the Planet Transition Summary."""
    summary_items: List[PlanetTransitionSummaryItem] = field(default_factory=list)
from typing import List, Dict, Any
from datetime import datetime

from app.schemas.transition_summary import PlanetTransitionSummaryItem, TransitionSummaryDTO
from app.engines.mandali_grid_construction import MandaliGrid
from app.engines.canonical_reference_data import CanonicalReferenceData

class TransitionSummaryBuilder:
    """
    Responsible for calculating and composing the Planet Transition Summary.
    It owns the unique business logic for determining 'Next Mandali',
    'Estimated Entry Date', and 'Days Remaining'.
    """
    def __init__(self, ref_data: CanonicalReferenceData):
        self._ref_data = ref_data

    def build(self, current_transit_raw: List[Dict[str, Any]], mandali_grid: MandaliGrid, target_date: datetime) -> TransitionSummaryDTO:
        """
        Builds the Planet Transition Summary DTO.
        
        Args:
            current_transit_raw: List of raw current transit planet dictionaries from Canonical JSON.
            mandali_grid: The MandaliGrid object.
            target_date: The consultation date for 'days_remaining' calculation.
        Returns:
            TransitionSummaryDTO containing a list of PlanetTransitionSummaryItem.
        """
        summary_items = []
        for tp in current_transit_raw:
            planet_name = tp["planet"]
            
            current_rasi = tp["rasi"]
            current_nakshatra = tp["nakshatra"]
            current_pada = tp["pada"]
            
            absolute_pada = self._ref_data.get_absolute_pada(current_nakshatra, current_pada)
            current_mandali_num = mandali_grid.find_mandali_for_pada(absolute_pada)
            current_mandali_obj = mandali_grid.get_mandali(current_mandali_num)
            current_mandali_name = f"Mandali {current_mandali_obj.number} ({current_mandali_obj.rasi_name})"

            next_mandali_num = (current_mandali_num % 12) + 1 # Mandali 12's next is Mandali 1
            next_mandali_obj = mandali_grid.get_mandali(next_mandali_num)
            next_mandali_name = f"Mandali {next_mandali_obj.number} ({next_mandali_obj.rasi_name})"

            estimated_entry_date_str = tp["end_date"] # Assuming end_date of current transit is entry to next
            days_remaining = -1
            try:
                end_date_dt = datetime.strptime(estimated_entry_date_str, "%d.%m.%Y")
                target_date_naive = target_date.replace(tzinfo=None)
                delta = end_date_dt - target_date_naive
                days_remaining = max(0, delta.days)
            except (ValueError, TypeError):
                pass # Keep days_remaining as -1 if date parsing fails

            summary_items.append(PlanetTransitionSummaryItem(
                planet=planet_name.capitalize(),
                current_rasi=current_rasi,
                current_nakshatra=current_nakshatra,
                current_pada=current_pada,
                current_mandali=current_mandali_name,
                next_mandali=next_mandali_name,
                estimated_entry_date=estimated_entry_date_str,
                days_remaining=days_remaining,
            ))
        return TransitionSummaryDTO(summary_items=summary_items)

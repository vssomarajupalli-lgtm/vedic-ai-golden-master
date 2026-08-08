from typing import List, Dict, Any, Optional
from app.schemas.mandali_chart_cell import MandaliChartCell

class MandaliChartLayoutBuilder:
    """
    Builds a list of MandaliChartCell objects representing the chart layout.
    This builder is generic and can be used for both natal and current transit charts.
    It contains NO astrology calculations, only composition/layout logic.
    """
    CHART_ORDER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    def build(
        self,
        placements: List[Dict[str, Any]],
        mandali_names: Optional[Dict[int, str]] = None,
    ) -> List[MandaliChartCell]:
        """
        Builds a list of MandaliChartCell objects representing the chart layout.
        
        Args:
            placements: A list of planet placement dictionaries.
                        Each dict must have 'planet' (str) and 'mandali' (dict with 'number' and 'name').
            mandali_names: Optional mapping of mandali number (1-12) to its display name
                        (e.g. "Mandali 2 (Mithuna)"). Used so empty cells carry the
                        correct Moon-centered Rasi instead of a fixed sign order.
        Returns:
            A list of MandaliChartCell objects, ordered by CHART_ORDER.
        """
        cells: Dict[int, MandaliChartCell] = {}
        for i in range(1, 13):
            name = (mandali_names or {}).get(i, f"Mandali {i}")
            cells[i] = MandaliChartCell(mandali_number=i, mandali_name=name, planets=[])

        for p in placements:
            mandali_num = p["mandali"]["number"]
            if mandali_num in cells:
                cell = cells[mandali_num]  # frozen dataclass - must replace, not mutate
                # Use short planet names for chart display
                updated_planets = cell.planets + [p["planet"][:2].upper()]
                cells[mandali_num] = MandaliChartCell(
                    mandali_number=cell.mandali_number,
                    mandali_name=p["mandali"]["name"],  # Update with more detail if available
                    planets=updated_planets,
                )

        return [cells[i] for i in self.CHART_ORDER]

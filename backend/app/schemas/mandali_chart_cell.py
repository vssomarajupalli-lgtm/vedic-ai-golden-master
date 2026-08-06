from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class MandaliChartCell:
    mandali_number: int
    mandali_name: str
    planets: List[str] = field(default_factory=list) # Short planet names
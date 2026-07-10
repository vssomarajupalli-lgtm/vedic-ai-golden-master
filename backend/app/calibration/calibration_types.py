from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class CalibrationProfile:
    """
    Strongly typed container for a complete calibration profile.
    """
    metadata: Dict[str, Any] = field(default_factory=dict)
    sections: Dict[str, Any] = field(default_factory=dict)
    master_probability: Dict[str, Any] = field(default_factory=dict)
    planet_strength: Dict[str, Any] = field(default_factory=dict)
    house_strength: Dict[str, Any] = field(default_factory=dict)
    rasi_strength: Dict[str, Any] = field(default_factory=dict)
    varga: Dict[str, Any] = field(default_factory=dict)
    dasha: Dict[str, Any] = field(default_factory=dict)
    ashtakavarga: Dict[str, Any] = field(default_factory=dict)
    natal_promise: Dict[str, Any] = field(default_factory=dict)
    transit: Dict[str, Any] = field(default_factory=dict)

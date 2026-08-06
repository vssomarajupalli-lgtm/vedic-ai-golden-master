"""
MandaliGenerator — Compatibility Facade (ADR-004 / GM-013A.1)
==============================================================

Restores the historical public API surface for the Moon-centered Gochara
Mandali generator WITHOUT duplicating geometry or responsibilities.

Governance:
- All 12-Mandali grid construction is delegated to the canonical owner:
  MandaliGridConstruction/MandaliGrid (mandali_grid_construction.py, Capability 7.3).
- All transit→Mandali resolution is delegated to MandaliGrid.find_mandali_for_pada
  (governed by MGC-05 no-overlap/no-gap guarantee).
- get_absolute_pada is the only pure-math helper retained here because no canonical
  registry implements longitude→absolute pada conversion; it is kept deterministic
  per the historical API contract (108 padas / 360 deg = 10/3 deg per pada).

This module performs NO duplicate geometry, NO longitude-orbit math state, NO
astrological interpretation, and NO strength calculation.
"""

from __future__ import annotations

import math

from app.engines.canonical_reference_data import (
    get_canonical_reference_data,
    CanonicalReferenceData,
)
from app.engines.mandali_grid_construction import (
    MandaliGrid,
    MandaliGridConstruction,
)


class MandaliGenerator:
    """
    Moon-centered Gochara Mandali generator (compatibility API).

    Historical public API preserved:
      - get_absolute_pada(longitude_deg) -> absolute pada index (1-108)
      - generate_mandali_grid(moon_absolute_pada) -> {1..12: {"center", "padas"}}
      - resolve_transit_mandali(transit_longitude, moon_absolute_pada) -> int (1-12)

    All grid construction is delegated to the canonical canonical owner.
    """

    def __init__(
        self,
        ref_data: CanonicalReferenceData | None = None,
        grid_constructor: MandaliGridConstruction | None = None,
    ):
        """Build the facade, defaulting to the canonical singleton data and constructor."""
        self._ref_data = ref_data or get_canonical_reference_data()
        self._grid_constructor = grid_constructor or MandaliGridConstruction(
            ref_data=self._ref_data
        )

    @staticmethod
    def get_absolute_pada(longitude_deg: float) -> int:
        """
        Convert a planetary longitude (0.0-360.0) into its absolute Nakshatra
        Pada index (1-108). 360° / 108 = 10/3° per pada.
        """
        long_mod = longitude_deg % 360.0
        pada_float = long_mod / (10.0 / 3.0)
        return int(math.floor(pada_float)) + 1

    @classmethod
    def generate_mandali_grid(cls, moon_absolute_pada: int) -> dict:
        """
        Build the 12-Mandali static grid centered entirely on the Natal Moon.

        Delegated to the canonical MandaliGridConstruction; the historical dict
        shape ({Mandali -> {"center", "padas"}}) is preserved for compatibility.
        """
        generator = cls()
        grid: MandaliGrid = generator._grid_for_pada(moon_absolute_pada)
        result = {}
        for mandali in grid.mandalis:
            result[mandali.number] = {
                "center": mandali.center_pada,
                "padas": list(mandali.padas),
            }
        return result

    @classmethod
    def resolve_transit_mandali(
        cls, transit_longitude: float, moon_absolute_pada: int
    ) -> int:
        """
        Resolve a Transit planet's longitude into its Mandali Number (1-12) relative
        to the Natal Moon, using the canonical grid and its no-gap/no-overlap guarantee.
        """
        generator = cls()
        grid_entry: MandaliGrid = generator._grid_for_pada(moon_absolute_pada)
        transit_pada = generator.get_absolute_pada(transit_longitude)
        return grid_entry.find_mandali_for_pada(transit_pada)

    def _grid_for_pada(self, moon_absolute_pada: int) -> MandaliGrid:
        """Resolve an absolute pada index to its nakshatra/pada, then build the Mario grid."""
        ref = self._ref_data
        entry = ref.get_pada_entry(moon_absolute_pada)
        return self._grid_constructor.build_grid(entry.nakshatra, entry.pada)
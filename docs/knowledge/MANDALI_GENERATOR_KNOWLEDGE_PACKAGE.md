# MANDALI GENERATOR KNOWLEDGE PACKAGE

## 1. Executive Summary
The `MandaliGenerator` is a spatial arithmetic utility used to calculate Moon-centered Gochara Transit Boundaries. It dynamically constructs a 12-block static grid (Mandalis) relative to the exact Nakshatra Pada of the Natal Moon, allowing the `TransitEngine` to accurately map transiting planets to relative astrological zones.

## 2. Purpose
Standard transit analysis often uses raw house boundaries (Rasis) which can be inaccurate for Gochara. This engine generates a highly precise 108-pada (Nakshatra quarter) grid, ensuring that transit effects are localized exactly relative to the Moon's true longitude, independent of abstract sign boundaries.

## 3. Responsibilities
- Translate an absolute planetary longitude (0.0 to 360.0) into its absolute Nakshatra Pada index (1 to 108).
- Generate a 12-Mandali spatial grid, where Mandali 1 is perfectly centered on the Natal Moon's Pada.
- Resolve a transiting planet's absolute longitude into its relative Mandali index (1 to 12).

## 4. Architecture
- **Pure Utility:** A stateless class with `@staticmethod` and `@classmethod` functions. Contains no internal state or orchestration logic.

## 5. Inputs
- `longitude_deg` (float): Planetary longitude.
- `moon_pada` (int): The calculated Nakshatra pada of the Natal Moon.
- `transit_longitude` (float): Longitude of a transiting planet.

## 6. Outputs
- `get_absolute_pada`: `int` (1 to 108)
- `generate_mandali_grid`: `dict` mapping Mandali 1-12 to a center pada and list of 9 inclusive padas.
- `resolve_transit_mandali`: `int` (1 to 12)

## 7. Data Contracts
- Grid dict format: `{ 1: { "center": int, "padas": list[int] } }`

## 8. Formula Dependencies
- 108 padas / 360 degrees = 3.333333 degrees per pada.
- `pada_float = longitude_deg / (10.0 / 3.0)`
- 1 Mandali = exactly 9 Padas. The 9 padas include the center pada, 4 padas before, and 4 padas after.

## 9. Engine Dependencies
- **Upstream:** None.
- **Downstream:** Consumed entirely by the `TransitEngine`.

## 10. Business Rules
- 12 Mandalis must cover exactly 108 Padas with absolutely no overlaps and no gaps.
- Mandali 1 is always the zone containing the Natal Moon.

## 11. Deterministic Rules
- Employs strict modulo arithmetic `((pada - 1) % 108) + 1` to handle the 360-to-0 degree wrap-around at the Aries point.

## 12. Execution Flow
1. `TransitEngine` passes the Moon's longitude to `get_absolute_pada`.
2. `TransitEngine` passes a transiting planet's longitude and the `moon_pada` to `resolve_transit_mandali`.
3. The generator creates the 12-block grid on the fly.
4. It iterates the grid and returns the Mandali number containing the transit pada.

## 13. Implementation Files
- `backend/app/engines/mandali_generator.py`

## 14. Supporting Documents
- Defined in `GOCHARA_MANDALI_GOVERNANCE_v1.md`.

## 15. Governance References
- Implementation of the Moon-Centered Gochara Transit Boundaries.

## 16. Technical Debt
- **Historical Implementation:** Historically, transits were evaluated using standard Rasi house boundaries.
- **Existing Implementation:** The `MandaliGenerator` is fully implemented and correctly maps longitudes to a 108-pada continuous grid, fulfilling the Phase 7 Governance requirements.
- **Future Moon Mandali architecture:** This is intended to eventually replace all naive house-based Gochara logic, but its usage is currently isolated to the `TransitEngine`.

## 17. Future Roadmap
- Expand the Mandali generator to support Kakshya (sub-divisions of Ashtakavarga) mapping for ultra-precise transit timing.

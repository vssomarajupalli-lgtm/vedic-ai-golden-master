# FUNCTIONAL NATURE ENGINE KNOWLEDGE PACKAGE

## 1. Executive Summary
The `FunctionalNatureEngine` determines the temporal (functional) role of planets based strictly on the Ascendant (Lagna) sign. It translates classical Parashari rules into a static dictionary mapping, labeling each visible planet as benefic, malefic, neutral, yogakaraka, or maraka relative to the specific chart.

## 2. Purpose
While planets have inherent natural natures (e.g., Jupiter is a natural benefic), their actual operational behavior in a specific chart is dictated by the houses they own. This engine provides the structural blueprint of these functional roles so downstream engines can evaluate planet and house strength accurately.

## 3. Responsibilities
- Map the Ascendant sign to a predefined Parashari functional matrix.
- Return the functional role (`benefic`, `malefic`, `neutral`), `is_yogakaraka` boolean, and `is_maraka` boolean for each planet.

## 4. Architecture
- **Stateless Engine:** The engine contains a massive static `_MAP` dictionary. It accepts a Lagna string, performs a quick lookup with alias resolution (e.g., converting "mesha" to "aries"), and returns the sub-dictionary.
- **Rule:** It intentionally excludes Rahu and Ketu, as they act according to their dispositor, which must be resolved by higher-order logic.

## 5. Inputs
- `lagna` (String): The Ascendant sign.

## 6. Outputs
- `dict`: A mapping of planet names to their functional properties.

## 7. Data Contracts
Returns an object of the shape:
```json
{
  "planet": {
    "functional_role": "string",
    "is_yogakaraka": boolean,
    "is_maraka": boolean
  }
}
```

## 8. Formula Dependencies
- **Classical Parashari mapping:** The underlying logic dictates that lords of trines (1, 5, 9) are benefics, lords of 3, 6, 11 are malefics, and lords of 2, 8, 12 are neutral/maraka depending on their other house ownership.

## 9. Engine Dependencies
- **Upstream:** None (Relies entirely on the parsed JSON `lagna` string).
- **Downstream:** Theoretically required by `PlanetStrengthEngine` and `HouseStrengthEngine`.

## 10. Business Rules
- Must gracefully handle both English ("aries") and Sanskrit ("mesha") terminology via an `alias_map`.
- Fails gracefully by returning an empty dictionary if the lagna is unknown.

## 11. Deterministic Rules
- Pure dictionary lookup O(1) time complexity. No floating-point math.

## 12. Execution Flow
1. Receives `lagna` string.
2. Normalizes string (lowercase, strip).
3. Translates Sanskrit alias to English.
4. Looks up and returns the dictionary from `_MAP`.

## 13. Implementation Files
- `backend/app/engines/functional_nature_engine.py`

## 14. Supporting Documents
- None.

## 15. Governance References
- Classical Parashari Lagna mapping rules.

## 16. Technical Debt
- **Ghost Engine:** The engine is currently unintegrated. Both `PlanetStrengthEngine` and `HouseStrengthEngine` bypass this engine, instead hardcoding their evaluations using `NATURAL_BENEFICS` and `NATURAL_MALEFICS` constants. This results in inaccurate strength evaluations for charts where natural malefics (like Saturn for a Libra Ascendant) act as immense functional benefics (Yogakaraka).

## 17. Future Roadmap
- Must be integrated into the `PipelineRunner` and injected into the `PlanetStrengthEngine` to dynamically override natural natures during the Dignity and Aspect calculation phases.

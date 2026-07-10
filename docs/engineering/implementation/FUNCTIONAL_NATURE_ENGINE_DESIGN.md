# FUNCTIONAL NATURE ENGINE DESIGN

**Goal:** Design the Functional Nature Engine to determine functional benefics, malefics, and yogakarakas based on Lagna (Ascendant), adhering strictly to DR-007 boundaries.

---

## 1. Current State Audit

*   **What currently exists:**
    The system currently uses purely natural benefics and malefics (`NATURAL_BENEFICS` and `NATURAL_MALEFICS` defined in `astrology_constants.py`).
*   **Where Lagna is extracted:**
    Lagna is extracted from the canonical source and stored in the root `metadata` object (e.g., `"lagna": "Mesha"`).
*   **How PlanetStrengthEngine currently handles planet nature:**
    `PlanetStrengthEngine` strictly uses *natural* aspects (`benefic_aspects_count`, `malefic_aspects_count`) mapped from the raw JSON to determine aspect modifications.
*   **Functional benefic/malefic logic:**
    Currently, there is **zero** functional benefic/malefic logic implemented. The system treats all planets solely by their natural dispositions and dignities.

---

## 2. Classical Mapping Inventory

Based on the Brihat Parashara Hora Shastra (BPHS), planetary functional nature is defined by house lordship relative to the Lagna.
*   **Benefics (Shubha):** Lords of Trikonas (1, 5, 9).
*   **Malefics (Papa):** Lords of Trishadayas (3, 6, 11).
*   **Neutrals/Mixed (Sama):** Lords of Kendras (4, 7, 10) undergo Kendradhipati Dosha (natural benefics become neutral/malefic, natural malefics become neutral/benefic). Lords of 2, 8, 12 are neutral and depend on their other house lordship or conjunctions.
*   **Yogakaraka:** A single planet owning both a Kendra and a Trikona.

### Mapping by Lagna (Parashari Baseline)

*   **Aries (Mesha):**
    *   *Benefics:* Sun (5), Jupiter (9), Moon (4), Mars (1)
    *   *Malefics:* Mercury (3, 6), Venus (2, 7 - Maraka), Saturn (10, 11)
    *   *Yogakaraka:* None
*   **Taurus (Vrishabha):**
    *   *Benefics:* Saturn (9, 10), Sun (4), Mercury (2, 5)
    *   *Malefics:* Jupiter (8, 11), Venus (1, 6), Moon (3)
    *   *Yogakaraka:* Saturn
*   **Gemini (Mithuna):**
    *   *Benefics:* Venus (5), Mercury (1, 4)
    *   *Malefics:* Mars (6, 11), Jupiter (7, 10), Sun (3)
    *   *Yogakaraka:* None
*   **Cancer (Kataka):**
    *   *Benefics:* Mars (5, 10), Jupiter (9), Moon (1)
    *   *Malefics:* Venus (11), Mercury (3, 12), Saturn (7, 8)
    *   *Yogakaraka:* Mars
*   **Leo (Simha):**
    *   *Benefics:* Mars (4, 9), Sun (1), Jupiter (5)
    *   *Malefics:* Venus (3, 10), Saturn (6, 7), Mercury (2, 11)
    *   *Yogakaraka:* Mars
*   **Virgo (Kanya):**
    *   *Benefics:* Venus (2, 9), Mercury (1, 10)
    *   *Malefics:* Mars (3, 8), Jupiter (4, 7), Moon (11)
    *   *Yogakaraka:* None
*   **Libra (Tula):**
    *   *Benefics:* Saturn (4, 5), Mercury (9), Venus (1, 8)
    *   *Malefics:* Mars (2, 7), Jupiter (3, 6), Sun (11)
    *   *Yogakaraka:* Saturn
*   **Scorpio (Vrishchika):**
    *   *Benefics:* Jupiter (2, 5), Moon (9), Sun (10)
    *   *Malefics:* Mercury (8, 11), Venus (7, 12), Saturn (3, 4)
    *   *Yogakaraka:* None
*   **Sagittarius (Dhanu):**
    *   *Benefics:* Mars (5), Sun (9), Jupiter (1, 4)
    *   *Malefics:* Venus (6, 11), Mercury (7, 10), Saturn (2, 3)
    *   *Yogakaraka:* None
*   **Capricorn (Makara):**
    *   *Benefics:* Venus (5, 10), Mercury (9), Saturn (1)
    *   *Malefics:* Mars (4, 11), Jupiter (3, 12), Moon (7)
    *   *Yogakaraka:* Venus
*   **Aquarius (Kumbha):**
    *   *Benefics:* Venus (4, 9), Saturn (1), Mars (10)
    *   *Malefics:* Jupiter (2, 11), Moon (6), Sun (7)
    *   *Yogakaraka:* Venus
*   **Pisces (Meena):**
    *   *Benefics:* Moon (5), Mars (2, 9), Jupiter (1, 10)
    *   *Malefics:* Sun (6), Venus (3, 8), Saturn (11, 12), Mercury (4, 7)
    *   *Yogakaraka:* None

---

## 3. Engine Placement

**Recommendation: A. `functional_nature_engine.py`**

*Reasoning:* `PlanetStrengthEngine` is responsible for calculating individual operational strength (Bala) derived from dignity, house placement, and state. Functional Nature is a global, structural map dependent entirely on the Ascendant (Lagna) rather than the planet's individual placement.
Separating this into `functional_nature_engine.py` ensures the Single Responsibility Principle and allows the resulting map to be injected broadly across *multiple* engines by the `PipelineRunner`.

---

## 4. Input Contract

The engine will be stateless and expose an evaluation method accepting simple primitives.

```python
{
    "lagna": "Mesha"  # Extracted from canonical metadata.lagna
}
```

---

## 5. Output Contract

The engine will return a dictionary mapping each planet to its functional nature, allowing O(1) lookups by other engines.

```python
{
    "sun": {
        "functional_role": "benefic",
        "is_yogakaraka": false,
        "is_maraka": false
    },
    "moon": {
        "functional_role": "benefic",
        "is_yogakaraka": false,
        "is_maraka": false
    },
    "mars": {
        "functional_role": "neutral",  # Lagna lord & 8th lord mixed
        "is_yogakaraka": false,
        "is_maraka": false
    },
    "mercury": {
        "functional_role": "malefic",
        "is_yogakaraka": false,
        "is_maraka": false
    },
    # ...
}
```

---

## 6. Engine Boundary Validation

*   **No direct engine calls:** `FunctionalNatureEngine` will not import or instantiate `PlanetStrengthEngine`, `NatalPromiseEngine`, or any other calculation engine.
*   **PipelineRunner injection only:** The `PipelineRunner` will instantiate `FunctionalNatureEngine`, run it immediately after extracting the Lagna, and then pass the resulting functional map downward into `PlanetStrengthEngine`, `NatalPromiseEngine`, etc.
*   **Compliance:** This design is perfectly aligned with **DR-007**.

---

## 7. Impact Analysis

The introduction of this engine will profoundly enhance the astrological accuracy of downstream engines:

*   **PlanetStrengthEngine:** Will consume the map to adjust aspect scoring. (e.g., an aspect from functional malefic Jupiter for a Taurus Lagna will carry a penalty instead of a natural benefic bonus).
*   **NatalPromiseEngine:** Will consume the map when evaluating house lords. A house ruled by a functional malefic will have a lower baseline promise than one ruled by a functional benefic.
*   **YogaEngine:** Critical dependency. Raja Yogas specifically require conjunctions/aspects between functional benefics (Kendra + Trikona lords).
*   **DashaEngine:** A Mahadasha of a functional benefic (e.g., Venus for Capricorn Lagna) will receive a significant timing_multiplier boost, whereas a functional malefic Dasha will be dampened.
*   **Future Gochara (Transit Engine):** Will differentiate between transits of functional benefics vs. functional malefics over key houses.

---

## 8. Canonical Data Check

A review of `canonical_content.json` (specifically `birth_data` and `planets`) reveals that functional nature, yogakaraka status, and maraka status are **absent** from the extracted source data.

*   **Conclusion:** Following **DR-003 (Extraction First)**, since the data is absent from the source payload, it must be mathematically derived by the `FunctionalNatureEngine`.

---

## 9. Risk Assessment

*   **Astrology Conflicts (Nodes):** Rahu and Ketu do not rule houses in the standard Parashari scheme.
    *   *Mitigation:* They will inherit the functional nature of their dispositor (the lord of the sign they occupy). This requires `FunctionalNatureEngine` to optionally accept the planet positions to determine node dispositors, or we leave nodes out of the base mapping and let the `PlanetStrengthEngine` handle them dynamically. *Proposed: Nodes are excluded from the static Lagna map.*
*   **Architecture Conflicts:** The `PipelineRunner` execution order must be explicitly defined. `FunctionalNatureEngine` must execute *before* `PlanetStrengthEngine`.
*   **Domain Expert Clarification Required:**
    *   Do we want to implement Maraka (death-inflicting / severe obstruction) logic for the 2nd and 7th lords directly in this engine? (Included as a boolean in the output contract proposal).

## User Review Required
> [!IMPORTANT]
> Please review the engine placement recommendation (A) and the Node handling strategy (excluding Rahu/Ketu from the static Lagna map). Await your approval before proceeding to implementation.

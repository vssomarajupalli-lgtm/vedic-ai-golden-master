# FUNCTIONAL NATURE ENGINE FINAL DESIGN

**Goal:** Design the Functional Nature Engine to determine functional benefics, malefics, and yogakarakas based on Lagna (Ascendant), strictly preserving architectural boundaries.

---

## 1. Classical Mapping & Revised Classification Logic

Based on Brihat Parashara Hora Shastra (BPHS), functional nature is strictly determined by house lordship relative to the Lagna, with specific override rules.

### Core Rules:
1.  **Lagna Lord Override:** The lord of the Ascendant (1st house) is the protector of the chart and is **ALWAYS a functional benefic**, regardless of its secondary house ownership (even if it owns the 6th, 8th, or 12th).
2.  **Trikona Lords:** Lords of the 5th and 9th houses are functional benefics.
3.  **Trishadaya Lords:** Lords of the 3rd, 6th, and 11th houses are functional malefics.
4.  **Maraka Lords:** Lords of the 2nd and 7th houses are death-inflicting (marakas) and act as functional malefics unless they are the Lagna lord.
5.  **Neutral/Mixed Lords:** Lords of the 8th and 12th houses are neutral and yield results based on their other house, placement, or conjunctions. Natural benefics owning Kendras (4, 7, 10) lose their beneficence (Kendradhipati Dosha).
6.  **Yogakaraka:** A single planet that simultaneously rules a Kendra (1, 4, 7, 10) and a Trikona (1, 5, 9). It becomes exceedingly auspicious.

### Verified Mapping by Lagna (Incorporating Lagna Lord Rule)

*   **Aries (Mesha):**
    *   *Benefics:* Mars (Lagna Lord), Sun (5), Jupiter (9)
    *   *Malefics:* Mercury (3, 6), Venus (2, 7 - Maraka), Saturn (10, 11)
    *   *Neutrals:* Moon (4)
    *   *Yogakaraka:* None
*   **Taurus (Vrishabha):**
    *   *Benefics:* Venus (Lagna Lord), Saturn (9, 10 - Yogakaraka), Mercury (5)
    *   *Malefics:* Jupiter (8, 11), Moon (3)
    *   *Neutrals:* Sun (4), Mars (7 - Maraka, 12)
    *   *Yogakaraka:* Saturn
*   **Gemini (Mithuna):**
    *   *Benefics:* Mercury (Lagna Lord), Venus (5)
    *   *Malefics:* Mars (6, 11), Jupiter (7, 10 - Kendradhipati Dosha), Sun (3)
    *   *Neutrals:* Moon (2 - Maraka), Saturn (8, 9)
    *   *Yogakaraka:* None
*   **Cancer (Kataka):**
    *   *Benefics:* Moon (Lagna Lord), Mars (5, 10 - Yogakaraka), Jupiter (9)
    *   *Malefics:* Venus (11), Mercury (3, 12), Saturn (7, 8)
    *   *Neutrals:* Sun (2 - Maraka)
    *   *Yogakaraka:* Mars
*   **Leo (Simha):**
    *   *Benefics:* Sun (Lagna Lord), Mars (4, 9 - Yogakaraka), Jupiter (5)
    *   *Malefics:* Venus (3, 10), Saturn (6, 7), Mercury (2, 11)
    *   *Neutrals:* Moon (12)
    *   *Yogakaraka:* Mars
*   **Virgo (Kanya):**
    *   *Benefics:* Mercury (Lagna Lord), Venus (9)
    *   *Malefics:* Mars (3, 8), Jupiter (4, 7 - Kendradhipati Dosha), Moon (11)
    *   *Neutrals:* Sun (12), Saturn (5, 6)
    *   *Yogakaraka:* None
*   **Libra (Tula):**
    *   *Benefics:* Venus (Lagna Lord), Saturn (4, 5 - Yogakaraka), Mercury (9)
    *   *Malefics:* Mars (2, 7), Jupiter (3, 6), Sun (11)
    *   *Neutrals:* Moon (10)
    *   *Yogakaraka:* Saturn
*   **Scorpio (Vrishchika):**
    *   *Benefics:* Mars (Lagna Lord), Jupiter (5), Moon (9), Sun (10)
    *   *Malefics:* Mercury (8, 11), Venus (7, 12), Saturn (3, 4)
    *   *Neutrals:* None
    *   *Yogakaraka:* None
*   **Sagittarius (Dhanu):**
    *   *Benefics:* Jupiter (Lagna Lord), Mars (5), Sun (9)
    *   *Malefics:* Venus (6, 11), Mercury (7, 10), Saturn (2, 3)
    *   *Neutrals:* Moon (8)
    *   *Yogakaraka:* None
*   **Capricorn (Makara):**
    *   *Benefics:* Saturn (Lagna Lord), Venus (5, 10 - Yogakaraka), Mercury (9)
    *   *Malefics:* Mars (4, 11), Jupiter (3, 12), Moon (7)
    *   *Neutrals:* Sun (8)
    *   *Yogakaraka:* Venus
*   **Aquarius (Kumbha):**
    *   *Benefics:* Saturn (Lagna Lord), Venus (4, 9 - Yogakaraka), Mars (10)
    *   *Malefics:* Jupiter (2, 11), Moon (6), Sun (7)
    *   *Neutrals:* Mercury (5, 8)
    *   *Yogakaraka:* Venus
*   **Pisces (Meena):**
    *   *Benefics:* Jupiter (Lagna Lord), Moon (5), Mars (9)
    *   *Malefics:* Sun (6), Venus (3, 8), Saturn (11, 12), Mercury (4, 7)
    *   *Neutrals:* None
    *   *Yogakaraka:* None

### Node Handling (Rahu/Ketu)
*Approved:* Rahu and Ketu are explicitly **excluded** from this static Lagna mapping. They do not own houses in the standard Parashari framework. Downstream engines will handle their functional nature dynamically based on their dispositor or conjunctions.

---

## 2. Strict Architectural Boundaries

*Correction Applied:* **Planet Strength ≠ Functional Nature**.
`PlanetStrengthEngine` calculates absolute positional and mathematical strength (dignity, combust, rasi bala). `FunctionalNatureEngine` calculates relative auspiciousness for the native.
*   The `FunctionalNatureEngine` will **NOT** alter planet strength calculations.
*   Aspect scores inside `PlanetStrengthEngine` will continue to rely solely on *natural* benefics/malefics to calculate objective mathematical strength.

---

## 3. Input / Output Contract

### Input
The engine is stateless and executes purely off the Lagna.
```python
{
    "lagna": "Mesha"  # Extracted from canonical metadata.lagna
}
```

### Output
Returns a static lookup dictionary mapping the 7 visible planets to their functional properties.
```python
{
    "sun": {
        "functional_role": "benefic",
        "is_yogakaraka": false,
        "is_maraka": false
    },
    "mars": {
        "functional_role": "benefic",  # Protected by Lagna Lord Rule
        "is_yogakaraka": false,
        "is_maraka": false
    },
    "venus": {
        "functional_role": "malefic",
        "is_yogakaraka": false,
        "is_maraka": true
    },
    # ... Only 7 planets returned. Nodes excluded.
}
```

---

## 4. Downstream Consumption Model

The `PipelineRunner` coordinates the independent outputs.

```text
               PipelineRunner
               /            \
PlanetStrengthEngine     FunctionalNatureEngine
       ↓                          ↓
 { "mars": {score: 80} }  { "mars": {role: "benefic"} }
               \            /
                \          /
                 ↓        ↓
             Downstream Engines
     (NatalPromise, Dasha, Yoga, Transit)
```

1.  **PipelineRunner:** Executes both engines in parallel (or sequentially, since they have no dependencies on each other).
2.  **NatalPromiseEngine:** Consumes both `planet_strength` AND `functional_nature`. If a house lord is a functional benefic, its impact on the house's promise is elevated.
3.  **YogaEngine:** Consumes `functional_nature` to validate Raja Yogas (conjunction of functional kendra/trikona lords) regardless of their base strength.
4.  **DashaEngine:** Consumes `functional_nature`. A Mahadasha of a functional benefic acts as a highly favorable timing multiplier, even if the planet's mathematical strength is only moderate.
5.  **TransitEngine (Future):** Evaluates Gochara effects differently when the transiting planet is a functional benefic vs functional malefic for the lagna.

# ASTROLOGICAL RATIONALE: PROPERTY FORMULAS

## 1. Core Methodology Overview
The current implementation of `AST_PROPERTY_BASE` evaluates the 4th House, 4th Lord, and Mars. 

**Reviewer Assessment:** INCOMPLETE FOR MODERN CONTEXT. The implementation correctly identifies the karakas for the literal land/structure, but entirely ignores the financial capacity required to execute a real estate transaction in the modern world.

## 2. Answers to Specific Review Questions

### Why is Jupiter absent?
**Current State:** Jupiter was omitted to restrict the payload to fixed assets (Mars).
**Astrological Critique:** This is a major omission. Jupiter is the Dhanakaraka (significator of wealth and expansion). Purchasing property requires significant liquid capital and financial blessing. Without Jupiter, the system can identify a desire for property, or the inheritance of a structure, but cannot validate the financial expansion required to buy a new home.

### Why are wealth-supporting indicators excluded?
**Current State:** The 2nd house and 11th house were excluded.
**Astrological Critique:** Incorrect methodology for predicting a *purchase*. The 4th house shows the asset itself. However, the 11th house is the fulfillment of desires and large gains, and the 2nd house is accumulated bank balance. A property purchase is a transaction that drains the 2nd house (savings) to convert it into the 4th house (fixed asset). Predicting the *timing* of a purchase requires seeing the 11th/2nd/4th houses active simultaneously.

### Why is Mars sufficient as property karaka?
**Current State:** Mars is the sole karaka mapped to the Base.
**Astrological Critique:** It is not sufficient. Mars represents Bhoomi (bare land, construction, real estate). Venus represents luxury, comfort, interior design, and vehicles. If a user asks about buying a luxury home or a car (which both fall under the 4th house), Venus is the primary karaka. Mars alone restricts the evaluation to raw real estate and agricultural land.

## 3. Exclusion Analysis

| Excluded Signal | Why Considered | Why Rejected | Future Formula Ownership |
|-----------------|----------------|--------------|--------------------------|
| **Jupiter** | Dhanakaraka (Wealth). | Assumed handled by Wealth domain. | Must be added to `AST_PROP_TIMING` to validate financial capacity during the purchase window. |
| **11th House/Lord** | Fulfillment of desire. | Deemed out of scope for 4th house focus. | Must be added to `AST_PROP_TIMING` alongside the 4th house. |
| **Venus** | Vehicles, luxury homes. | Kept Mars as the pure real estate karaka. | Belongs in a new `AST_VEHICLE_BASE` variant. |

## 4. Methodology Breakdown

### Core House Logic (Proposed Revision)
- **4th House:** The fixed asset, home, peace of mind, vehicles.
- **2nd House:** The liquid capital required to fund the asset.
- **11th House:** The realization of the desire to own the asset.
- **8th / 12th House:** Disputes, loss of property, or moving away from the home.

### Core Karaka Logic (Proposed Revision)
- **Mars:** Land, construction, real estate.
- **Venus:** Vehicles, luxury, aesthetic comfort of the home.
- **Jupiter:** Financial capacity to purchase.

### Core Dasha Logic
- Dashas of the 4th lord or planets in the 4th house trigger property events.
- To validate a *purchase*, the Dasha must simultaneously activate the 4th and 11th/2nd/9th lords (showing a financially supported acquisition).

### Core Transit Logic
- Jupiter transiting over the 4th house or 4th lord brings the blessing of an asset.
- Saturn transiting the 4th house causes delays in purchase or structural repairs/burdens related to the home.

### Future Mandali Impact
- The 4th house from the Moon represents the emotional comfort of the home. Transits affecting the Moon-based 4th house trigger changes in residence or emotional dissatisfaction with the current living situation, regardless of the D1 physical ownership status.

## 5. FINAL RECOMMENDATION
**MODIFY CURRENT MODEL.**
1. Add Jupiter and the 11th house to `AST_PROP_TIMING` to mathematically validate that the user has the financial capacity to buy the property during that timeline.
2. Ensure Mars is strictly used for real estate questions, and create a parallel variant mapping for Vehicle questions using Venus.

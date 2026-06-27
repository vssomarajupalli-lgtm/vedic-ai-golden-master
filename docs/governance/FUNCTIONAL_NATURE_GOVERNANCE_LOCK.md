# FUNCTIONAL NATURE GOVERNANCE LOCK

**Date:** 2026-06-16
**Status:** LOCKED / AUTHORITATIVE
**Subject:** Conversion of `FunctionalNatureEngine` from Inferred Engine to Static Governance Lookup

---

## 1. Purpose
This document formally locks the Parashari Functional Nature classifications used by the Vedic AI System. It permanently reclassifies the `FunctionalNatureEngine` from an "inference engine" to a **Static Governance Lookup Table**. 

By locking this matrix at the governance level, the system ensures that mathematical determinism is preserved, downstream engines (like Dasha and Gochara) can safely consume structural planetary behaviors without violating the "No Inventing Predictions" mandate (DR-004), and the rules of Parashari astrology are respected.

---

## 2. Source Authority
The mapping locked in this document relies on standard **Brihat Parashara Hora Shastra (BPHS)** principles regarding functional benefics, malefics, yogakarakas, and marakas derived solely from the native's Ascendant (Lagna) sign.

---

## 3. Why Extraction is Impossible
An extensive extraction feasibility audit determined that the source Telugu PDFs do not contain an explicit tabular definition of functional benefics, malefics, yogakarakas, or marakas. 

Because this structural data is entirely absent from the PDF payload, the `JsonNormalizer` cannot extract it. Therefore, adhering strictly to the "Extraction over Inference" rule (DR-003) would leave the system mathematically blind to standard astrological structure.

---

## 4. Why a Governance Lookup is Permitted
Because the functional nature of a planet is a mathematically deterministic constant derived 100% reliably from the Lagna (and not a heuristic guess or probabilistic inference), it is eligible to be classified as a **Static System Constant**. 

By shifting this mapping from "engine calculation" to "governance lookup array," it operates identically to how the system knows that "Aries comes before Taurus." It is no longer considered an "invented prediction," but rather a foundational structural law.

---

## 5. Downstream Usage Rules
1. **Consumption:** Engines (such as `DashaEngine`, `GocharaEngine`, `NatalPromiseEngine`) are actively encouraged to consume the `functional_nature` output provided by `PipelineRunner`.
2. **Immutability:** Downstream engines may READ these classifications to adjust multipliers or determine favorable/unfavorable timing, but they may NEVER modify or override the functional nature of a planet.
3. **No Dynamic Adjustment:** A planet's functional nature classification (benefic, malefic, yogakaraka, maraka, neutral) is determined solely by the Lagna and never changes.

However, downstream engines may combine functional nature with strength, dignity, house placement, dasha activation, and gochara activation when evaluating results.

---

## 6. Rahu & Ketu Treatment
**Rahu and Ketu are strictly excluded from this mapping.**
Under standard Parashari rules, the lunar nodes have no independent functional nature. They act as proxies, mimicking the functional nature of:
1. Their dispositor (the lord of the sign they occupy).
2. The planets they are conjoined with.
3. The planets aspecting them.

Any engine requiring the functional nature of Rahu or Ketu must dynamically resolve it at runtime by querying the `functional_nature` of their structural dispositor from the D1 chart.

---

## 7. Future Modification Policy
This matrix is structurally locked. 
**NO MODIFICATIONS ARE PERMITTED** to this lookup table unless explicit, written consent is granted by the Astrological Governance Board (subject matter experts). Any adjustments to these constants fundamentally alter the behavioral mathematics of the entire system.

---

## 8. Relationship To Mandali Gochara

The Functional Nature Governance Matrix remains valid under the Mandali Gochara system.

Mandali-based transit calculations may use
functional nature as a modifier when interpreting
planetary transit effects.

The introduction of Mandali zones does not alter
the benefic, malefic, yogakaraka, maraka,
or neutral classification of any planet.

---

## 9. Authoritative Lagna Mapping Matrix

The following matrix represents the locked, immutable Parashari functional classifications for all 12 ascendants:

### 1. Aries (Mesha)
* **Benefic:** Mars, Sun, Jupiter
* **Neutral:** Moon
* **Malefic:** Mercury, Venus, Saturn
* **Yogakaraka:** None
* **Maraka:** Venus

### 2. Taurus (Vrishabha)
* **Benefic:** Venus, Saturn, Mercury
* **Neutral:** Sun, Mars
* **Malefic:** Moon, Jupiter
* **Yogakaraka:** Saturn
* **Maraka:** Mars

### 3. Gemini (Mithuna)
* **Benefic:** Mercury, Venus
* **Neutral:** Moon, Saturn
* **Malefic:** Sun, Mars, Jupiter
* **Yogakaraka:** None
* **Maraka:** Moon

### 4. Cancer (Kataka)
* **Benefic:** Moon, Mars, Jupiter
* **Neutral:** Sun
* **Malefic:** Mercury, Venus, Saturn
* **Yogakaraka:** Mars
* **Maraka:** Sun

### 5. Leo (Simha)
* **Benefic:** Sun, Mars, Jupiter
* **Neutral:** Moon
* **Malefic:** Mercury, Venus, Saturn
* **Yogakaraka:** Mars
* **Maraka:** Mercury

### 6. Virgo (Kanya)
* **Benefic:** Mercury, Venus
* **Neutral:** Sun, Saturn
* **Malefic:** Moon, Mars, Jupiter
* **Yogakaraka:** None
* **Maraka:** Jupiter

### 7. Libra (Tula)
* **Benefic:** Venus, Saturn, Mercury
* **Neutral:** Moon
* **Malefic:** Sun, Mars, Jupiter
* **Yogakaraka:** Saturn
* **Maraka:** Mars

### 8. Scorpio (Vrishchika)
* **Benefic:** Mars, Sun, Moon, Jupiter
* **Neutral:** None
* **Malefic:** Mercury, Venus, Saturn
* **Yogakaraka:** None
* **Maraka:** Venus

### 9. Sagittarius (Dhanu)
* **Benefic:** Jupiter, Sun, Mars
* **Neutral:** Moon
* **Malefic:** Mercury, Venus, Saturn
* **Yogakaraka:** None
* **Maraka:** Mercury, Saturn

### 10. Capricorn (Makara)
* **Benefic:** Saturn, Venus, Mercury
* **Neutral:** Sun
* **Malefic:** Moon, Mars, Jupiter
* **Yogakaraka:** Venus
* **Maraka:** Moon

### 11. Aquarius (Kumbha)
* **Benefic:** Saturn, Venus, Mars
* **Neutral:** Mercury
* **Malefic:** Sun, Moon, Jupiter
* **Yogakaraka:** Venus
* **Maraka:** Sun, Jupiter

### 12. Pisces (Meena)
* **Benefic:** Jupiter, Moon, Mars
* **Neutral:** None
* **Malefic:** Sun, Mercury, Venus, Saturn
* **Yogakaraka:** None
* **Maraka:** Mars, Mercury

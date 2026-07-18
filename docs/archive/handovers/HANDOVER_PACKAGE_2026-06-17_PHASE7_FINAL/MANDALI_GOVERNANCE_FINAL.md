---
archive_title: "MANDALI GOVERNANCE FINAL"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\handovers"
archive_reason: "Superseded by current documentation architecture"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# MANDALI GOVERNANCE FINAL
**Document State:** Final (Phase 7 Lockdown)
**Date:** 2026-06-17

## Core Decision: Governance Locked
**MANDALI DOES NOT CHANGE INTERPRETATION.**
**MANDALI ONLY CHANGES BOUNDARIES.**

* **Old:** Planet enters Rasi → effect starts
* **New:** Planet enters Mandali → effect starts
* **Note:** The astrological interpretation and probability impacts remain identical.

## Mandali Mathematics
The Mandali system relies on the absolute precision of Nakshatra Padas rather than 30-degree Rasi sign bounds.

* **Absolute Pada mathematics:** The ecliptic is divided strictly by Nakshatra Padas (3°20' each) instead of Rasi signs.
* **108 Pada model:** The entire zodiac comprises 108 distinct Padas.
* **12 Mandali model:** The zodiac is divided into 12 Mandalis, serving as micro-precision analogs to the 12 Rasi signs.
* **Moon-centered construction:** Each Mandali is constructed dynamically around the exact Nakshatra Pada occupied by the natal Moon.
* **Structure:** Backward 4 Padas + Center Pada + Forward 4 Padas.
* **Size:** Total 9 Padas per Mandali (exactly 30 degrees).
* **Continuity:** No overlap, no gaps between Mandalis.

## Sade Sati Rule (12/1/2)
Sade Sati calculation is dynamically shifted to Mandali bounds.
* A planet transiting the **12th Mandali**, **1st Mandali**, or **2nd Mandali** from the Moon's center Pada triggers the Sade Sati effect.
* The boundaries are mathematically absolute and do not rely on standard sign ingress/egress.

## Transit Engine Integration
The `TransitEngine` now exclusively consumes the `MandaliGenerator` outputs for Gochara snapshot triggers. Whenever a planet's absolute longitude crosses a Mandali boundary, the engine fires the respective transit events.

## Dhanishta 2 Center Example
If the natal Moon is in **Dhanishta 2nd Pada**, the resulting 1st Mandali is constructed as follows:

1. Shravana 2nd Pada (Backward 4)
2. Shravana 3rd Pada (Backward 3)
3. Shravana 4th Pada (Backward 2)
4. Dhanishta 1st Pada (Backward 1)
5. **Dhanishta 2nd Pada (Center)**
6. Dhanishta 3rd Pada (Forward 1)
7. Dhanishta 4th Pada (Forward 2)
8. Shatabhisha 1st Pada (Forward 3)
9. Shatabhisha 2nd Pada (Forward 4)

---
archive_title: "GOCHARA_ENGINE_MASTER"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\gocharm_lagacy"
archive_reason: "Superseded by current documentation architecture"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# GOCHARA_ENGINE_MASTER

## 1. PURPOSE
This file is the authoritative gochara specification for the Samartha Astro-AI system.
All detailed transit logic, Saturn-based micro gochara behavior, and dasha-linked transit printing rules must remain here.

## 2. CORE GOCHARA MODEL
The gochara engine must use Moon nakshatra pada based logic rather than simple rasi-only logic.
The center reference point is the native Moon pada, and the surrounding zones extend backward and forward from that point across the 27-pada framework.

## 3. AUTHORITY RULE
If any gochara-related rule inside another file conflicts with this file, this file must prevail.
CALCULATION_ENGINE_ARCH_V2.md and SYSTEM_RULES_CORE.md should only reference this file and must not duplicate the full logic.

## 4. REQUIRED GOCHARA OUTPUTS
The engine must support:
* Present planetary transit coverage for all planets.
* Elinati Shani period calculation with start and end dates.
* Dasha-linked gochara results.
* Mahadasha, Antardasha, and Pratyantardasha overlap display.
* Printable past and upcoming transit-linked results.

## 5. PLANET AND BHAVA STRENGTH MODEL
The engine must include planet strength and bhava strength calculations.
The strength model must support:
* Exaltation.
* Own sign.
* Moolatrikona.
* Uchchabala.
* Swarashi bala.
* Optional friend, neutral, and enemy sign handling.
* Percent-based scoring output.

## 6. SCORE RULE
Where question or result scoring is needed, the engine must support the weighted framework used by the project:
Final Question Score = (0.40 × S_lord) + (0.30 × S_karaka) + (0.15 × S_D9) + (0.10 × S_varga) + (0.05 × 20) + Bonus
If the final score exceeds 100, cap it at 100.
If the lord is in vargottama position, add a 5% bonus.

## 7. SUPPRESSED CONTENT
The following modules must not be reintroduced into compiled output:
* Avakahada Chakra.
* Ghata Chakra.
* Panchadha Maitri Chakra.
* Jaimini Karakas.
* Jaimini Arudhas.

## 8. JSON OUTPUT
The engine must produce JSON-ready structured output for frontend and future PWA use.
The JSON should support birth profile, transit snapshot, strength values, and timeline windows.

## 9. PRINTING RULES
Every compiled report must begin with the birth details page.
All visible dates must be formatted as DD.MM.YYYY.
The engine must support both split PDF reports and a single unified master PDF.

## 10. IMPLEMENTATION PRIORITY
The gochara engine should be implemented in small testable units:
1. Birth profile ingestion.
2. Natal Moon calculation.
3. Saturn transit resolver.
4. Pada-based belt mapping.
5. Zone detection.
6. Zone scoring.
7. Elinati Shani builder.
8. Dasha overlap mapping.
9. JSON builder.
10. Final report output.
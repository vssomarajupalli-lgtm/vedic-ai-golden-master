# GOCHARA_OUTPUT_TEMPLATES

## 1. PURPOSE
This file defines the output structure for gochara reports, PDF rendering, and frontend presentation.

## 2. REQUIRED OUTPUT MODES
The system must support:
* Four isolated segment PDF files.
* One single unified master document PDF.
* Web and PWA display output.

## 3. PAGE 1 RULE
Every output mode must begin with a standard birth details page.
That page must include:
* Native name.
* Date of birth.
* Time of birth.
* Place of birth.
* Latitude.
* Longitude.
* Runtime execution timestamp.

## 4. REPORT SECTIONS
The template system must support these report sections:
* 12 Bhava Strength report.
* Planetary strengths and gochara report.
* 200 Mega Prashna Grid report.
* Samartha True Micro Gochara report.

## 5. DATE AND FORMAT RULES
All displayed dates must be in DD.MM.YYYY format.
Machine-style date strings must not appear in final user-facing layouts.

## 6. PAGE BREAK RULES
Tables and question rows should avoid breaking across pages where possible.
Header rows should repeat on new pages where needed.
Page numbering must be consistent in each output mode.

## 7. BRANDING RULE
Every report must reserve a clean branding slot for Samartha Vastu / Samartha Astro-AI presentation.
The branding area must remain lightweight and suitable for fast local rendering.

## 8. CONTENT SUPPRESSION
Do not include the following in any final report template:
* Avakahada Chakra.
* Ghata Chakra.
* Panchadha Maitri Chakra.
* Jaimini Karakas.
* Jaimini Arudhas.

## 9. OUTPUT CONTRACT
Each report template must be compatible with JSON-backed rendering, PDF generation, and future PWA layout binding.
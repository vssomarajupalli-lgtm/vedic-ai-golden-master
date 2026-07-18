---
archive_title: "PHASE 14H.1 COMPLETION REPORT: QUESTIONNAIRE DISPLAY SPECIFICATION V1"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\bkl-006_legacy"
archive_reason: "Classified as CP-001 (Zero Dependency Historical Artifact) per BKL-006 Chief Architect Decision Register"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# PHASE 14H.1 COMPLETION REPORT: QUESTIONNAIRE DISPLAY SPECIFICATION V1

**Snapshot Date:** 2026-06-21
**Project Status:** Phase 14H.1 Complete
**Module Name:** Questionnaire UI & Structured Display Layer

---

## 1. Objectives

The objective of Phase 14H.1 was to decouple the UI formatting layer from the core math and routing engines. It strictly required building a static, configurable UI for question selection and enforcing a highly structured, 7-section display card layout for final question results. The strict mandate was that no mathematical engines (`NatalPromiseEngine`, `DashaEngine`, `FormulaEvaluator`, or `QuestionRouter`) could be modified to support UI adjustments.

## 2. Files Created

*   **`backend/app/formatters/display_formatter.py`**
    *   Creates a `DisplayFormatter` interface to handle presentation transformations.
    *   Calculates the "Activation Index" as a simple arithmetic average of MD, AD, and PD.
    *   Maps internal grading nomenclatures (e.g., `PRESENT` → `Very Weak`) strictly for UI use.
*   **`frontend/src/config/questionnaireSchema.ts`**
    *   Defines the static JSON UI schema controlling the domain categories and question definitions.
*   **`frontend/src/components/Questionnaire/QuestionSelection.tsx`**
    *   React component providing a multi-select, collapsible menu based on HTML5 details.
*   **`frontend/src/components/Questionnaire/QuestionResultCard.tsx`**
    *   React component that renders the complex 7-section layout (Promise Assessment, Dasha Activation, Final Conclusion, Timing Window, Supporting Factors, Attention Factors, Mandali Commentary) with hard borders and distinct color blocks.

## 3. Files Modified

*   **`backend/app/schemas/question.py`**
    *   Introduced `StructuredQuestionResponse` alongside Pydantic models for `PromiseAssessmentDisplay`, `DashaActivationDisplay`, `FinalConclusionDisplay`, and `TimingWindowDisplay`.
*   **`backend/app/api/v1/endpoints/queries.py`**
    *   Created the `/ask-structured-question` endpoint to pipe `FormulaEvaluator` math results directly into `DisplayFormatter` without hitting the LLM payload compiler.

## 4. Governance Verification

A strict Pre-Commit Governance Audit was conducted with the following verified outcomes:

*   **NatalPromiseEngine:** NOT MODIFIED.
*   **DashaEngine:** NOT MODIFIED.
*   **FormulaEvaluator:** NOT MODIFIED.
*   **QuestionRouter:** NOT MODIFIED.
*   **Scoring Mathematics:** NOT MODIFIED.
*   **Activation Index Usage:** Confirmed as exclusively isolated to the display layer and JSON payload output. The Activation Index does NOT influence probability routing, `FormulaEvaluator` boolean checks, or Final Assessment states (`FAVORABLE`, `MIXED`, `UNFAVORABLE`).
*   **Question Engine Rule:** The structure `Question Engine = Natal Promise + Dasha Activation` remains intact and compliant with the Phase 15 governance freeze. No new weighted aggregations were introduced into the math pipeline.

## 5. UI Architecture

The frontend adopts a responsive 2-pane configuration:
*   **Left Sidebar / Menu Panel:** Renders the collapsible `QuestionSelection` component. Manages the active state of all user checkbox selections.
*   **Main Display Panel:** Maps through the structured results from the backend and displays sequential `QuestionResultCard` components, allowing a user to read batch analyses simultaneously.

## 6. Questionnaire Structure

Driven by `questionnaireSchema.ts`, the UI is organized hierarchically by domain. Example structure:

▶ **1. Marriage**
*   1.1 Marriage Promise
*   1.2 Marriage Timing
*   ...

▶ **2. Career**
*   2.1 Career Promise
*   2.2 Promotion
*   ...

▶ **3. Wealth**
*   3.1 Wealth Promise
*   ...

## 7. Output Specification

Results output in rigid, visual blocks:

*   **A. Promise Assessment:** Extracts the final promise score (%) and string grade mapping directly from `NatalPromiseEngine`.
*   **B. Current Dasha Activation:** Extracts precise Mahadasha, Antardasha, and Pratyantardasha scores and summarizes them into an Activation Index.
*   **C. Final Conclusion:** Imports the final boolean state (`FAVORABLE`, `MIXED`, `UNFAVORABLE`) from the `FormulaEvaluator`.
*   **D. Timing Window:** Highlights the dominant planetary rulers spanning the targeted window.
*   **E. Supporting Factors:** Renders parsed positive indicators from isolated payload variables.
*   **F. Attention Factors:** Renders parsed negative indicators from isolated payload variables.
*   **G. Mandali Commentary:** Hardcoded placeholder ready for Phase 15 logic integration.

## 8. Git Commit Reference

**Branch:** `feature/phase-14h1-questionnaire-ui` (Assumed)
**Commit Summary:** `feat: implement phase 14h.1 structured question UI display layer`
*   *Note: Working tree is verified clean of mathematical engine modifications.*

## 9. Next Recommended Phase

**Phase 15 - Mandali Engine Overlay**
With the display layer correctly configured and completely decoupled from core engines, the architecture is now ready to receive the **MandaliEngine**. The MandaliEngine should be built as a standalone Layer 4 advisory module that outputs JSON to populate "Section G. Mandali Commentary", operating entirely independently of the Question Engine.

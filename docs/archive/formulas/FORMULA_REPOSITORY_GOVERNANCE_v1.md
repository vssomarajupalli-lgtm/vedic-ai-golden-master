---
archive_title: "FORMULA REPOSITORY GOVERNANCE v1"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\formulas"
archive_reason: "Superseded by current documentation architecture"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# FORMULA REPOSITORY GOVERNANCE v1

## 1. Core Principle
The Formula Repository is a strictly governed architectural boundary. Its primary mandate is to prevent the dispersal of astrological logic across the codebase. It enforces the rule: **"Calculate once in the Engine, evaluate once in the Formula, format once in the Composer."**

## 2. Prohibited Behaviors

### 2.1 No Mathematical Logic Duplication
Formulas must **never** calculate planetary positions, house strengths, or dasha periods. 
- **Violation:** A formula script that calculates the distance between the Moon and the Sun to determine Tithi.
- **Correction:** The formula must request the `Tithi` variable from the `NatalPromiseEngine`.

### 2.2 No Hardcoded Astrology Rules Inside UI
The frontend React interface, including the Question Browser and any subsequent components, must remain 100% ignorant of astrology rules.
- **Violation:** React UI showing a warning: `if (saturn_in_7th) showWarning("Delay in Marriage");`
- **Correction:** React UI renders the `answer_text` provided by the Answer Composer. The Formula Repository dictates if the warning is present.

### 2.3 No Engine Recalculation
Mathematical Engines are expensive operations.
- **Violation:** A formula triggering `DashaEngine.calculate()` multiple times for different sub-queries.
- **Correction:** The `PipelineRunner` executes `DashaEngine.calculate()` once. The Formula extracts from the resulting payload.

### 2.4 No Duplicated Formulas
Each astrological scenario must map to a unique `formula_key`.
- **Violation:** Having `marriage_timing_v1` and `marriage_timing_v2` running simultaneously without deprecation logic.
- **Correction:** The `FormulaValidator` ensures unique keys. Versioning must be handled via the registry mapping, not by duplicating identical mathematical logic.

---

## 3. Answer Composer Boundary Governance

The Answer Composer (the LLM interface) is the most volatile component of the system due to the non-deterministic nature of generative AI. To prevent astrological hallucinations, the Formula Repository acts as a strict firewall.

### 3.1 Strict Context Injection
The LLM prompt is constructed *only* from the payload defined by the Formula.
If the Formula for "Career Growth" does not explicitly include the 7th house (Marriage), the LLM is physically incapable of discussing the user's marriage because the 7th house data is simply not in the context window.

### 3.2 Evaluation Overriding is Prohibited
The LLM is a formatting tool, not a computational engine.
If the Formula Repository evaluates `confidence_layers` and determines the result is `Favorable = False`, the LLM prompt is hardcoded with the instruction: *"The mathematical evaluation is UNFAVORABLE. You must communicate this unfavorable outcome."* The LLM cannot decide the aspect is actually favorable based on its own internal weights.

### 3.3 Tone and Template Enforcement
The `answer_template` variable within the formula dictates the tone and structure.
- Formulas dealing with Risk Assessment must enforce templates that require objective, non-fatalistic language.
- Formulas dealing with Timing Assessment must enforce templates that restrict timeframes to the specific Dasha boundaries provided by the engine.

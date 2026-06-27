# FORMULA LIBRARY EXPANSION ARCHITECTURE v1

## 1. Overview
This architecture dictates how the Vedic AI System will scale from its 8 initial seed formulas to support the entire canonical Question Registry (hundreds of natural language queries). It establishes a rigid hierarchical taxonomy and an inheritance-based schema to prevent formula explosion while maintaining compatibility with future frontend reporting features.

## 2. Formula Scaling Strategy: The Taxonomy
To prevent governance drift and duplicate maintenance, the formula library will adopt the **Formula Family + Inheritance Model**. 

### 2.1 The Hierarchy
Formulas are structured in a strict top-down taxonomy:
1. **Master Category:** The highest domain (e.g., `Marriage`, `Career`).
2. **Subcategory:** A logical grouping (e.g., `Marriage Timing`, `Marriage Quality`).
3. **Formula Family (Base):** A generalized mathematical formula containing the core signals and rules shared across all variants (e.g., `MAR_TIMING_BASE`).
4. **Formula Variant (Child):** A specific implementation that inherits from the Base but adds or overrides 1-2 specific confidence layers (e.g., `MAR_TIMING_EARLY`, `MAR_TIMING_DELAY`).
5. **Question Mapping:** The Question Router maps many natural language `question_id` inputs to a single Formula Variant (Many:1 mapping).

### 2.2 The Inheritance Schema Model
To support this hierarchy, the `FormulaSchema` will be conceptually expanded in future phases to support a `parent_formula` key. 
- **Inheritance Logic:** A Variant inherits all `required_signals`, `required_engines`, and `required_confidence_layers` from its Base.
- **Extension:** The Variant can append specific signals or layers to the inherited lists.
- **Result:** This ensures that if the baseline definition of "Marriage Promise" changes, updating the Base formula cascades the fix to all dozen variants automatically.

## 3. Canonical Report & Future Presentation Compatibility
The Formula Library must serve not only the generative LLM Answer Composer but also highly structured, deterministic frontend views.

### 3.1 "Evaluate Once, Consume Many"
The pipeline generates a single deterministic payload: the `FormulaEvaluationResult`. 
This object must act as the absolute source of truth for:
- **LLM Answer Composer:** Converting the payload to generative text.
- **Canonical Astrologer Report (PDF):** A structured data dump of the chart.
- **Frontend UI Components:** Visual dashboards showing Planetary Strength, Bhava Strength, and MD/AD timelines.

### 3.2 Evidence Traceability
Because all downstream consumers read the exact same `FormulaEvaluationResult`, the system guarantees that the LLM's narrative will perfectly match the numerical data displayed in the PDF and UI components. No downstream consumer is permitted to recalculate astrology.

## 4. Future Mandali Compatibility
The architecture is designed to natively support future Moon-centered Mandali Gochara overlays.
- **Mandali Hooks:** Base Formulas can define `future_gochara_required = true`. 
- **Overlay Evaluation:** When implemented, the Formula Evaluator will simply request additional signals from the `TransitEngine` (e.g., "Moon transiting 7th house") and append them to the `isolated_signals` payload. 
- No architectural overhaul will be needed; Mandali transit data becomes just another boolean gate in the standard formula evaluation pipeline.

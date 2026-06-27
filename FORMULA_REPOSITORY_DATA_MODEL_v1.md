# FORMULA REPOSITORY DATA MODEL v1

## 1. Overview
This document defines the abstract data model for the Formula Repository. These structures govern how a deterministic formula extracts data from the Mathematical Engines and resolves it into a comprehensive astrological assessment, without requiring any raw logic inside the Answer Composer.

---

## 2. Core Formula Record Model

Every formula in the repository adheres to the following structural record:

- **`formula_key`**: Unique string identifier (e.g., `MAR_TIMING_001`). Must exactly match the key emitted by the Question Registry.
- **`formula_name`**: Human-readable name (e.g., "Primary Marriage Timing Assessment").
- **`formula_category`**: High-level classification (e.g., `Timing Assessment`, `Natal Assessment`).
- **`required_engines`**: List of computational engines that MUST successfully execute for this formula to be valid (e.g., `[NatalPromiseEngine, DashaEngine, TransitEngine]`).
- **`required_signals`**: The specific astrological variables to be plucked from the engines (e.g., `7th House`, `Venus`, `Lagnesh`).
- **`required_dasha_layers`**: The depth of time-tracking required (e.g., `Mahadasha`, `Antardasha`, `Pratyantardasha`).
- **`required_vargas`**: Divisional charts required for synthesis (e.g., `D1`, `D9`, `D10`).
- **`required_confidence_layers`**: A checklist of astrological conditions.
- **`future_gochara_required`**: Boolean flag indicating if Moon-centered Mandali (transit forecasting) is necessary.
- **`answer_template_key`**: Pointer to the structural linguistic boundary for the Answer Composer.

---

## 3. The Confidence Model

The system evaluates an astrological event not by a single boolean, but by accumulating evidence across multiple structural layers. No numeric scoring is implemented at this stage; instead, the architecture relies on conditional presence.

### 3.1 Layer Contributions
1. **Natal Promise**: The baseline. Does the D1/Varga chart support the event? (e.g., 7th lord is well-placed). If the natal promise is denied, subsequent layers cannot override it to "positive."
2. **Dasha Activation**: The timing mechanism. Is the current Mahadasha or Antardasha connected to the required signals?
3. **Yoga Support**: Are there specific named mathematical combinations (Yogas) that amplify or rescue the assessment?
4. **Ashtakavarga Support**: Does the relevant house possess sufficient bindus (>28) to sustain the event?
5. **Transit Support**: Is the current sky (TransitEngine) triggering the natal promise?

---

## 4. Answer Template Model

The Formula Repository binds the LLM to predefined structural templates to prevent generative hallucinations. 

- **`answer_template_key`**: The ID linking the formula to a linguistic framework.
- **`positive_template`**: Activated when the majority of confidence layers are fulfilled. Enforces an affirmative but non-absolute tone.
- **`neutral_template`**: Activated when confidence layers are mixed. Enforces a balanced tone discussing delays or required effort.
- **`challenging_template`**: Activated when the natal promise is weak or dashas are adverse. Enforces objective, remedial-focused language (never fatalistic).

---

## 5. Gochara Preparation

The `future_gochara_required` flag acts as the bridge to future predictive mechanics.

### 5.1 Moon-Centered Mandali Governance
When `future_gochara_required` is `true`, the formula acknowledges that the question (e.g., "When will I get a job?") cannot be answered purely by static Dasha analysis. It requires predicting when a planet will cross a specific degree.
- Without implementing the code now, this flag signals to the future `PipelineRunner` that the `TransitEngine` must shift its reference frame from the Lagna (Ascendant) to the Moon (Chandra) to evaluate the Gochara (transit) effects mathematically over a future timeline array.

---

## 6. Seed Formula Blueprints

### MAR_PROS_001 (Marriage Prospects)
- **Category**: Natal Assessment
- **Required Signals**: 7th House, 7th Lord, Venus
- **Required Vargas**: D1, D9
- **Confidence Layers**: 7th Lord dignity, Venus dignity, D9 Lagnesh strength.
- **Future Gochara**: `false`

### MAR_TIMING_001 (Marriage Timing)
- **Category**: Timing Assessment
- **Required Signals**: 7th House, 7th Lord, Venus, Lagna Lord
- **Required Dasha Layers**: Mahadasha, Antardasha
- **Confidence Layers**: Dasha lord aspecting 7th, Dasha lord is Venus, Jupiter transit over 7th/Lagna.
- **Future Gochara**: `true`

### MAR_DELAY_001 (Delay in Marriage)
- **Category**: Risk Assessment
- **Required Signals**: Saturn, 7th House, 8th House
- **Required Vargas**: D1
- **Confidence Layers**: Saturn aspecting 7th, 7th lord in 8th/12th, Venus in papakartari.
- **Future Gochara**: `false`

### CAR_GROWTH_001 (Career Growth)
- **Category**: Timing/Natal Assessment
- **Required Signals**: 10th House, 10th Lord, 11th House (Gains)
- **Required Vargas**: D1, D10
- **Confidence Layers**: 10th Lord strength in D10, Ashtakavarga bindus in 10th > 28, positive dasha.
- **Future Gochara**: `true`

### CAR_CHANGE_001 (Job Change)
- **Category**: Timing Assessment
- **Required Signals**: 5th House (change), 9th House (transition), 10th House
- **Required Dasha Layers**: Antardasha, Pratyantardasha
- **Confidence Layers**: Dasha lords connected to 5th/9th, Transit Saturn/Jupiter activating 10th.
- **Future Gochara**: `true`

### CAR_FOREIGN_001 (Foreign Career)
- **Category**: Multi-factor Assessment
- **Required Signals**: 9th House, 12th House, 10th House, Rahu
- **Required Vargas**: D1, D10
- **Confidence Layers**: 10th Lord connected to 12th, Rahu influence on 10th, Dasha activating 9th/12th.
- **Future Gochara**: `false`

### WEA_SAVING_001 (Savings Potential)
- **Category**: Strength Assessment
- **Required Signals**: 2nd House, 2nd Lord, Jupiter
- **Required Vargas**: D1
- **Confidence Layers**: 2nd Lord dignity, Jupiter strength, absence of malefic aspects on 2nd.
- **Future Gochara**: `false`

### WEA_SUDDEN_001 (Sudden Financial Gains)
- **Category**: Multi-factor Assessment
- **Required Signals**: 8th House, 11th House, Rahu, 2nd House
- **Required Vargas**: D1
- **Confidence Layers**: 8th Lord connected to 11th, Rahu in 8th/11th, Dasha activating the yoga.
- **Future Gochara**: `false`

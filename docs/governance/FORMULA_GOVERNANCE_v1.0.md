# FORMULA GOVERNANCE v1.0

## 1. Core Principle
The Formula Repository is a strictly governed architectural boundary. Its primary mandate is to prevent the dispersal of astrological logic across the codebase. It enforces the rule: **"Calculate once in the Engine, evaluate once in the Formula, format once in the Composer."**

As the Formula Library expands to encompass the complete canonical Question Registry, the following immutable governance rules apply:
1. **Evaluate Once, Consume Many:** Formulas must only extract and evaluate deterministic signals. No downstream presentation layer (LLM Composer, PDF Report, UI) may perform astrological calculations.
2. **Strict Reuse:** A new formula variant may only be created if the mathematical logic (confidence layers) required to answer the question differs from an existing variant. 
3. **No Semantic Formulas:** Formulas must not be created purely to change the linguistic tone of an answer. Tone variations must be handled by mapping multiple questions to the same formula but mapping to different presentation templates via the Answer Composer.

## 2. Formula Family Governance
A **Formula Family** acts as the foundational baseline for a specific domain inquiry (e.g., `MAR_TIMING_BASE`).
- **Creation Rule:** A new Formula Family may ONLY be created when the root astrological target (the core primary houses and karakas) changes. For example, moving from "Marriage Timing" (7th house) to "Career Timing" (10th house) justifies a new Family.
- **Reuse Mandate:** If a new Question ID targets the exact same domain and astrological parameters as an existing Family, a new Family MUST NOT be created. 
- **Inheritance Mandate:** All subsequent variations of a Family must inherit from the Base to ensure global fixes cascade successfully.

## 3. Formula Variant Governance
A **Formula Variant** is a child formula that inherits from a Family Base but adds or overrides specific layers (e.g., `MAR_TIMING_DELAY`).
- **Creation Rule:** A Variant may ONLY be created if the *mathematical evaluation logic* (the `required_confidence_layers` or `required_signals`) fundamentally differs from the Base. 
- **Justifiable Differences:** Adding a rule to check for Saturn's aspect on the 7th house (delay) justifies a Variant.
- **Unjustifiable Differences:** A change in linguistic tone (e.g., "Will I marry late?" vs "At what age will I tie the knot?") DOES NOT justify a new Variant. Both must map to the same Variant. Semantic variations are strictly the domain of the Answer Composer templates.

## 4. Prohibited Behaviors
### 4.1 No Mathematical Logic Duplication
Formulas must **never** calculate planetary positions, house strengths, or dasha periods. 
- **Violation:** A formula script that calculates the distance between the Moon and the Sun to determine Tithi.
- **Correction:** The formula must request the `Tithi` variable from the `NatalPromiseEngine`.

### 4.2 No Hardcoded Astrology Rules Inside UI
The frontend React interface, including the Question Browser and any subsequent components, must remain 100% ignorant of astrology rules.
- **Violation:** React UI showing a warning: `if (saturn_in_7th) showWarning("Delay in Marriage");`
- **Correction:** React UI renders the `answer_text` provided by the Answer Composer. The Formula Repository dictates if the warning is present.

### 4.3 No Engine Recalculation
Mathematical Engines are expensive operations.
- **Violation:** A formula triggering `DashaEngine.calculate()` multiple times for different sub-queries.
- **Correction:** The `PipelineRunner` executes `DashaEngine.calculate()` once. The Formula extracts from the resulting payload.

### 4.4 No Duplicated Formulas
Each astrological scenario must map to a unique `formula_key`.
- **Violation:** Having `marriage_timing_v1` and `marriage_timing_v2` running simultaneously without deprecation logic.
- **Correction:** The `FormulaValidator` ensures unique keys. Versioning must be handled via the registry mapping, not by duplicating identical mathematical logic.

## 5. Answer Composer Boundary Governance
The Answer Composer (the LLM interface) is the most volatile component of the system due to the non-deterministic nature of generative AI. To prevent astrological hallucinations, the Formula Repository acts as a strict firewall.

### 5.1 Strict Context Injection
The LLM prompt is constructed *only* from the payload defined by the Formula.
If the Formula for "Career Growth" does not explicitly include the 7th house (Marriage), the LLM is physically incapable of discussing the user's marriage because the 7th house data is simply not in the context window.

### 5.2 Evaluation Overriding is Prohibited
The LLM is a formatting tool, not a computational engine.
If the Formula Repository evaluates `confidence_layers` and determines the result is `Favorable = False`, the LLM prompt is hardcoded with the instruction: *"The mathematical evaluation is UNFAVORABLE. You must communicate this unfavorable outcome."* The LLM cannot decide the aspect is actually favorable based on its own internal weights.

### 5.3 Tone and Template Enforcement
The `answer_template` variable within the formula dictates the tone and structure.
- Formulas dealing with Risk Assessment must enforce templates that require objective, non-fatalistic language.
- Formulas dealing with Timing Assessment must enforce templates that restrict timeframes to the specific Dasha boundaries provided by the engine.

## 6. Template Governance
Templates govern the linguistic boundaries applied by the Answer Composer.
- **Creation Rule:** A new template (`.txt` file) is justified ONLY when the fundamental structure of the narrative must change (e.g., shifting from a `timing_assessment` format to a `strength_assessment` format).
- **Reuse Mandate:** Templates must remain generic (e.g., `favorable`, `mixed`, `unfavorable`) and be reused across hundreds of formulas. 
- **Proliferation Control:** Creating specific templates for individual formulas (e.g., `marriage_delay_favorable.txt`) is strictly forbidden.

## 7. Question Mapping Governance
The `QuestionRegistry` connects natural language queries to Formula Variants.
- **Many-to-One Mapping:** Multiple `question_id` inputs must aggressively map to the same Formula Variant whenever the astrological math is identical.
- **Duplicate Prevention:** The `QuestionRegistryLoader` enforces uniqueness on `question_id` and actively tracks formula reuse to prevent duplicate mappings.

## 8. Canonical Evidence Governance
All generated Formulas must comply with the **"Evaluate Once, Consume Many"** principle.
- Formulas must output standard `FormulaEvaluationResult` payloads.
- Formulas must never embed logic meant exclusively for the LLM. The extracted evidence must be perfectly compatible with the Canonical JSON Export, Future Astrologer PDFs, and UI Strength Dashboards. No downstream system is permitted to recalculate astrology.

## 9. Future Mandali Compatibility
All new Formulas must be evaluated for compatibility with future Moon-centered Mandali overlays.
- A formula must not contain logic that hard-blocks dynamic Gochara.
- Timeline-based formulas must support the `future_gochara_required` flag, ensuring that when the Mandali engine is activated, transit data can seamlessly integrate as additional boolean confidence layers without requiring an architectural rewrite.

## 10. Mitigation of Maintenance Risks
To prevent "formula explosion" and massive maintenance burdens, the system implements the following risk mitigations:
- **Duplicate Logic Risk:** Mitigated by Inheritance. Base formulas encapsulate 80% of the standard logic. Child variants only append the 20% niche logic.
- **Template Sprawl Risk:** Mitigated by generalized categories (`timing_assessment`, `multifactor_assessment`, `strength_assessment`). We do not create a unique text template for every single formula.
- **Evaluator Complexity Creep:** The Formula Evaluator must permanently remain mathematically blind. It is forbidden from substituting variables, resolving dynamic arrays, or executing custom python functions per formula.

## 11. Registry Coverage Roadmap
Expansion will proceed in a phased, domain-driven sequence.
- **Phase A: Core Relationship & Wealth (Current Focus)** - Marriage (Domain 7), Career (Domain 10), Wealth (Domain 2)
- **Phase B: Health, Litigation, and Property** - Health (Domain 6), Property/Vehicles (Domain 4), Litigation/Enemies (Domain 6)
- **Phase C: Education, Travel, and Spirituality** - Education (Domain 4/5/9), Travel (Domain 3/9/12), Spirituality (Domain 9/12)
- **Phase D: Mandali Gochara Integration** - Retrofit the Base formulas across all domains to trigger `future_gochara_required`.

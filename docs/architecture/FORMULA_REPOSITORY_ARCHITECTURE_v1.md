# FORMULA REPOSITORY ARCHITECTURE v1

## 1. Overview
The Formula Repository serves as the deterministic translation layer connecting the `Question Registry` (what the user is asking) to the `Mathematical Engines` (how the system calculates the truth), and ultimately to the `Answer Composer` (how the system communicates the truth). 

A `question_id` (e.g., "7.2 Marriage Timing") resolves to a `formula_key`. The Formula Repository dictates exactly which engine variables must be evaluated for that key, ensuring rigid, repeatable astrological logic without LLM hallucination.

---

## 2. Formula Repository Structure
Every formula in the repository is defined by a strict schema. This schema guarantees that the system fetches all necessary data before generating a response.

### 2.1 Formula Definition Schema
```json
{
  "formula_key": "marriage_timing_primary",
  "category": "Timing Assessment",
  "required_engines": [
    "DashaEngine",
    "TransitEngine"
  ],
  "required_houses": [7, 2, 11],
  "required_planets": ["Venus", "Jupiter"],
  "required_dashas": {
    "depth": 3,
    "favorable_lords": ["7th_lord", "Venus"]
  },
  "required_vargas": ["D1", "D9"],
  "future_gochara_required": true,
  "confidence_layers": [
    "primary_dasha_activation",
    "jupiter_transit_aspect",
    "d9_lagna_activation"
  ],
  "answer_template": "timing_prediction_v1"
}
```

### 2.2 Schema Definitions
- **`formula_key`**: The unique identifier for the astrological rule set.
- **`required_engines`**: Enforces which engines must be run. Prevents running unnecessary engines.
- **`required_houses` / `required_planets` / `required_vargas`**: The precise mathematical entities needed for the logic.
- **`required_dashas`**: Specifies the Mahadasha/Antardasha depth required.
- **`future_gochara_required`**: Boolean flag. If true, activates predictive transit mapping.
- **`confidence_layers`**: A checklist of conditions. The more layers activated, the higher the confidence of the prediction.
- **`answer_template`**: Dictates the structural bounds of the LLM response to prevent meandering or hallucinatory prose.

---

## 3. Formula Categories
Formulas are strictly categorized to dictate their evaluation flow and engine priority:

1. **Natal Assessment**: Static snapshot evaluation (e.g., "Is there a Yoga for wealth?"). Primary engine: `NatalPromiseEngine`, `YogaEngine`.
2. **Timing Assessment**: Chronological prediction (e.g., "When will I get married?"). Primary engine: `DashaEngine`.
3. **Transit Assessment**: Current/future active energy (e.g., "How is Saturn's return affecting me?"). Primary engine: `TransitEngine`.
4. **Risk Assessment**: Malefic influence checks (e.g., "Is there danger of job loss?"). Focuses on 6th/8th/12th houses and malefic dashas.
5. **Strength Assessment**: Quantitative power evaluation (e.g., "How strong is my career?"). Primary engine: `AshtakavargaEngine`, Shadbala.
6. **Multi-factor Assessment**: Complex synthesis requiring 3+ engines (e.g., "Will I have a successful business abroad?").

---

## 4. Formula Loader Architecture
To maintain the boundary between definitions and runtime execution, the repository utilizes a dedicated loader architecture.

### 4.1 `FormulaRegistry`
The static JSON or YAML file containing all authoritative formula definitions.

### 4.2 `FormulaValidator`
A boot-time validation module. 
- Asserts that no two formulas have the same `formula_key`.
- Validates that all `required_engines` actually exist in the current system.
- Ensures `answer_template` references a valid prompt template.

### 4.3 `FormulaRepositoryLoader`
The runtime module that the `QuestionRouter` calls. 
- Takes the `formula_key`.
- Returns the complete validated JSON schema.
- Throws `FormulaNotFoundError` if the key is obsolete or invalid.

---

## 5. Engine Dependency Mapping
The Formula Repository dictates dependency flow. It maps how formulas consume outputs **without re-performing calculations**.

### The "Evaluate Once, Consume Many" Pattern
1. **Pipeline Runner** evaluates the Natal Chart once.
2. The outputs are cached in the `ChartProcessResponse`.
3. The **Formula Loader** extracts only the specified variables.
   - If `formula` requires D1 7th House, it plucks it from the `NatalPromiseEngine` output.
   - If `formula` requires current Mahadasha, it plucks it from `DashaEngine` output.
4. **Result:** The mathematical engines are purely computational and completely blind to the user's question. The formula acts as a specialized query language extracting only what is needed.

---

## 6. Answer Composer Boundary
The Formula Repository strictly bounds the LLM via the `answer_template`.

**Allowed Data for Composer:**
- The boolean results of the `confidence_layers`.
- The specific planets, houses, and dashas requested by the formula.
- The pre-calculated mathematical strengths.

**Prohibited Behavior (Hallucination Prevention):**
- The LLM is **never** provided the raw birth coordinates to calculate its own astrology.
- The LLM is **never** allowed to override the `confidence_layers` boolean result. If the formula says the timing is "Weak", the LLM must output "Weak".
- The LLM cannot pull in unrequested planets. (e.g., If the formula is for Marriage, the LLM cannot hallucinate a reading about the 4th house of property unless the formula explicitly includes it).

---

## 7. Future Gochara Integration
When `future_gochara_required` is `true`, the architecture bridges into predictive Moon-centered Mandali logic.

### Interaction with Moon-centered Mandali
- The formula will flag `future_gochara_required: true`.
- The system will dynamically switch the transit reference point from the Lagna (Ascendant) to the Moon (Chandra Lagna).
- The `TransitEngine` will generate a chronological array of future hits (e.g., Jupiter passing over natal Moon).
- This integration is purely structural right now; the Formula Repository reserves the flag for the future Phase implementation of Gochara mechanics, ensuring backward compatibility.

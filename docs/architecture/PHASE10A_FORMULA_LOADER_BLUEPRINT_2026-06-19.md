# PHASE 10A FORMULA LOADER BLUEPRINT

**Date:** 2026-06-19
**Context:** Phase 10A Pre-Implementation Review

## Objective
Review and lock the architectural design of the Formula Loader before executing the implementation. This blueprint defines how astrological logic is decoupled from Python execution.

---

## 1. Where Formula IDs Should Live
Formula IDs (e.g., `MAR_PROMISE_001`, `CAR_PROMISE_001`, `FIN_WEALTH_001`) must not exist as hardcoded functions inside the Python engines. They must live in external configuration files grouped by domain. This ensures that the codebase remains mathematically generic, while the configuration files act as the "astrological brain" of the system.

## 2. Recommended Storage Format
**YAML** is the strictly recommended format for the Formula Repository.
*   **Why YAML over JSON?** YAML inherently supports `# comments`, allowing astrologers to annotate why specific Bhavas or Yogas are included in a formula. It is significantly more human-readable and maintainable for complex hierarchical data than JSON.
*   **Why YAML over Python Registry?** A Python registry (`formulas.py`) invites the temptation to write executable logic inside the definitions, violating architectural decoupling.

## 3. Exact Folder Structure Recommendation
```text
backend/app/config/
├── formulas/
│   ├── marriage.yaml       # Contains MAR_PROMISE_001, MAR_TIMING_001, etc.
│   ├── career.yaml         # Contains CAR_PROMISE_001, etc.
│   ├── wealth.yaml         # Contains FIN_WEALTH_001, etc.
│   └── health.yaml         # Contains HEA_HEALTH_001, etc.
├── routing/
│   └── question_map.yaml   # Maps Question IDs to Formula IDs
```

## 4. How Formula Loader Should Retrieve Variables
The `FormulaLoader` class is purely a parsing and validation layer; it **does not compute** or fetch data directly from the engines.
1.  The `pipeline_runner.py` completes execution and generates the master `engine_outputs` payload containing `house_results`, `planet_results`, `varga_results`, `yoga_results`, `dasha_results`, and `dosha_results`.
2.  The `QuestionEngine` receives a Question ID.
3.  The `QuestionEngine` queries the `FormulaLoader` for the required Formula Blueprint.
4.  The `FormulaLoader` returns the parsed YAML dictionary (e.g., `{"primary_bhava": 7, "primary_karaka": "venus"}`).
5.  The `QuestionEngine` then acts as the synthesis orchestrator, extracting those specific values from the `engine_outputs` dictionary and applying the Phase 9 mathematics.

## 5. Question ID to Formula ID Mapping
The mapping must be stored independently of the formulas in `backend/app/config/routing/question_map.yaml`. This allows a single question to trigger multiple independent formulas.

**Example Matrix:**
```yaml
MAR_001:  # "Will I get married?"
  - MAR_PROMISE_001
  - MAR_TIMING_001
  - DOS_KUJA_001

CAR_001:  # "Will I have a prominent career?"
  - CAR_PROMISE_001
  - CAR_TIMING_001
```

## 6. Future Adaptability (Gochara, Ashtakavarga, Doshas)
The Formula Loader MUST be built as a generic schema parser. It should only validate that the YAML file adheres to a broad structural schema using standard Python libraries (like `pydantic` or `marshmallow` if available, or basic dict validation). 
Because the Loader does not execute astrology, it is inherently future-proof. When a new future node (e.g., `required_kakshya: "jupiter"`) is added to the YAML, the Loader simply parses it as a dictionary key and hands it off to the `QuestionEngine`. It natively supports Mandali Gochara, Ashtakavarga, and new Yogas without requiring structural loader modifications.

---

## 7. Exact Implementation Blueprint (Phase 10A Execution Steps)

**Step 1: Create the Config Directories**
*   Create `backend/app/config/formulas/` and `backend/app/config/routing/`.

**Step 2: Create Baseline YAML Files**
*   Create `marriage.yaml` containing the `MAR_PROMISE_001` blueprint based on the approved Phase 9 Step 3F governance.
*   Create `question_map.yaml` containing the `MAR_001 -> MAR_PROMISE_001` mapping.

**Step 3: Build the FormulaLoader Class**
*   Create `backend/app/engines/formula_loader.py`.
*   Implement `load_formula(formula_id: str) -> dict`.
*   Implement `get_formulas_for_question(question_id: str) -> list[str]`.
*   Implement caching to prevent reading the disk on every execution.

**Step 4: Verification**
*   Write a unit test to verify that calling `get_formulas_for_question("MAR_001")` successfully retrieves the `MAR_PROMISE_001` dictionary structure from disk.

**Constraints:** Do not integrate the loader into `QuestionEngine` yet. This phase is exclusively building the loader and configuration files.

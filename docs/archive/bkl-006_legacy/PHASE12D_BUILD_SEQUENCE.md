# PHASE 12D: FORMULA REPOSITORY BUILD SEQUENCE

This document outlines the strict chronological sequence for implementing the Formula Repository. Execution must occur in this exact order to preserve the "Evaluate Once, Consume Many" governance model.

---

## Stage 1: Foundational Scaffolding
**Goal:** Create the directory structure and abstract models without touching any existing engines.
1. Create `backend/app/core/formula_repository/` and the `registry/` subfolder.
2. Define the Pydantic `FormulaSchema` to rigidly match the Data Model from Phase 12B.
3. Write the initial empty `__init__.py` files to establish the Python package.

## Stage 2: Registry Seed Implementation
**Goal:** Translate the structural blueprints from Phase 12B into actual data files.
1. Implement the `MAR_PROS_001`, `MAR_TIMING_001`, and `MAR_DELAY_001` blueprints into a dictionary or configuration structure within `registry/marriage_formulas.py` (or equivalent data file).
2. Implement the Career and Wealth seed formulas in their respective registry files.
3. Ensure no computational logic exists within these files; they must be pure data objects.

## Stage 3: The Loader and Validator Core
**Goal:** Build the mechanisms to safely load and verify the registry data.
1. Build `FormulaValidator` (`validator.py`).
2. Write unit tests for `FormulaValidator` proving it catches duplicate keys and invalid signal definitions.
3. Build `FormulaRepositoryLoader` (`loader.py`).
4. Write unit tests proving the Loader correctly fetches and caches a formula, and gracefully throws a `FormulaNotFoundError` for missing keys.

## Stage 4: The Evaluator Logic
**Goal:** Build the engine that plucks data and resolves the Confidence Model matrix.
1. Build `FormulaEvaluator` (`evaluator.py`).
2. Implement the `extract_signals()` method to pull requested variables from a mocked `ChartProcessResponse`.
3. Implement the Graceful Degradation logic (capping at `MIXED` if an engine is missing).
4. Implement the strict `FAVORABLE` / `MIXED` / `UNFAVORABLE` resolution matrix.
5. Write exhaustive unit tests covering data extraction, null payload handling (Risk-FR-05), and degradation states.

## Stage 5: System Integration
**Goal:** Connect the isolated repository to the Question Router and Answer Composer.
1. Update `backend/app/core/question_router.py` to invoke the `FormulaRepositoryLoader` after successfully validating a `question_id`.
2. Update the `PipelineRunner` (`pipeline_runner.py`) to pass the `ChartProcessResponse` to the `FormulaEvaluator`.
3. Inject the `FAVORABLE`/`MIXED`/`UNFAVORABLE` result and the specifically requested signals into the LLM context generation within the Answer Composer.
4. Implement the Future Gochara hook points (`future_gochara_required` flagging logic) in the `PipelineRunner` without calculating actual future transits.

## Stage 6: Final Validation
**Goal:** End-to-end verification.
1. Run the entire backend test suite.
2. Perform manual end-to-end execution via the Question Browser UI for each of the 8 seed formulas.
3. Verify the LLM response adheres strictly to the generated templates and does not hallucinate unrequested planetary data.

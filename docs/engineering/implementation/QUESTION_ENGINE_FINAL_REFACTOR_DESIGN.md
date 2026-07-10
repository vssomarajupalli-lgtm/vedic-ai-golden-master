# QUESTION ENGINE FINAL REFACTOR DESIGN

## 1. Existing Flow
1. API/Caller invokes `QuestionEngine.answer(question, pipeline_output)`.
2. `QuestionEngine` routes the question to a domain.
3. `QuestionEngine` extracts the domain's natal promise score.
4. `QuestionEngine` instantiates `MasterProbabilityEngine` directly (Violation of DR-007).
5. `QuestionEngine` recalculates the master probability using the domain score.
6. `QuestionEngine` extracts Dasha timing evidence and collapses it.
7. `QuestionEngine` formats a text string and returns a dict with the text and probability scores.

**Issues:** 
- Violates Engine Isolation.
- Recalculates probability inside a routing/composition engine.
- Fails to adequately expose Transit Activation separately alongside Dasha and Natal Promise (DR-008).

## 2. New Flow
1. API/Caller invokes `PipelineRunner.answer_question(question, pipeline_output)`. `PipelineRunner` acts as the sole orchestrator.
2. `PipelineRunner` calls `QuestionEngine.route_domain(question)` to get the target domain.
3. `PipelineRunner` extracts the domain's `Natal Promise`, `Dasha Activation`, and `Transit Activation` directly from the `pipeline_output`.
4. `PipelineRunner` recalculates the domain-specific `Final Probability` using its own `self.master_engine`. (Alternatively, `MasterProbabilityEngine` could precalculate this during standard generation, but dynamic evaluation in the orchestrator is safer).
5. `PipelineRunner` calls `QuestionEngine.compose_response(domain, natal_promise, dasha_activation, transit_activation, final_probability)`.
6. `QuestionEngine` returns a structured dictionary distinguishing Potential, Activation, and Timing Windows (DR-008).

## 3. Objects Passed Between PipelineRunner and QuestionEngine
**From PipelineRunner -> QuestionEngine (`compose_response`):**
* `domain` (str): e.g., "marriage"
* `natal_promise` (dict): The specific domain block from `engine_outputs["natal_promise"]`.
* `dasha_activation` (dict): The Dasha layer output.
* `transit_activation` (dict): The Transit layer output.
* `final_probability` (dict): The newly evaluated probability score for this specific domain.

**From QuestionEngine -> PipelineRunner:**
* A structured dictionary containing: `answer_text` and separated objects for `natal_promise`, `dasha_activation`, `transit_activation`, and `probability`.

## 4. API Impact
* `backend/app/api/v1/endpoints/queries.py` will be updated to instantiate `PipelineRunner` and call `pipeline_runner.answer_question(request.question_text, request.engine_outputs)` instead of calling `QuestionEngine` directly.
* Note: `queries.py` currently incorrectly unpacks a tuple (`answer, used_yogas = question_engine.answer(...)`). This will be fixed to expect the standardized dict.

## 5. Test Impact
* `backend/tests/test_question_engine.py`: Needs refactoring. Tests must test `route_domain` and `compose_response` directly, without relying on internal `MasterProbabilityEngine` calls.
* `backend/tests/test_real_charts.py`: `TestRajuQuestionEngine` must be updated to call `PipelineRunner.answer_question()` instead of manually instantiating `QuestionEngine`.

from typing import Any, Dict, List, Tuple
from datetime import datetime

from app.core.question_router import QuestionRouter
from app.formulas.loader import FormulaRepositoryLoader
from app.formulas.signal_translator import SignalTranslator
from app.formulas.evaluator import FormulaEvaluator
from app.formatters.display_formatter import DisplayFormatter
from app.core.logging import log

class QuestionAnsweringService:
    def __init__(self):
        self.router = QuestionRouter()
        self.formula_loader = FormulaRepositoryLoader()

    def answer_structured_question(self, question_id: str, pipeline_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes a single structured question against a full pipeline output and returns the formatted result.
        """
        log.info(f"Answering structured question via service: {question_id}")

        engine_outputs = pipeline_output.get("engine_outputs", {})
        
        route_result = self.router.route_question(question_id)
        if route_result["status"] == "error":
            raise ValueError(f"Question routing failed for {question_id}: {route_result['message']}")

        metadata = route_result["metadata"]
        domain = route_result["registry_record"]["domain_name"].lower()
        question_title = metadata.get("question_name", "Astrological Query")

        formula = self.formula_loader.get_formula(route_result["formula_key"])
        if not formula:
            raise ValueError(f"Formula not found for key: {route_result['formula_key']}")

        isolated_signals = SignalTranslator.translate(formula.required_signals, engine_outputs)
        evaluation_result = FormulaEvaluator.evaluate(formula, engine_outputs, isolated_signals)

        target_date_iso = pipeline_output.get("target_date_utc")
        target_date_utc = datetime.fromisoformat(target_date_iso) if target_date_iso else None

        formatted_result = DisplayFormatter.format_question_result(
            question_title=question_title,
            domain=domain,
            natal_promise=engine_outputs.get("natal_promise", {}),
            dasha_activation=engine_outputs.get("dashas", {}),
            lifetime_projection=pipeline_output.get("master_probability", {}).get("lifetime_projection", []),
            final_state=evaluation_result.final_state,
            isolated_signals=evaluation_result.isolated_signals,
            client_metadata=pipeline_output.get("metadata", {}).get("client_info", {}),
            target_date_utc=target_date_utc
        )
        
        return formatted_result.dict()

    def evaluate_many(
        self,
        question_ids: List[str],
        pipeline_output: Dict[str, Any],
    ) -> Tuple[List[Dict[str, Any]], List[str]]:
        """
        Evaluates a list of question IDs against one full pipeline output and
        returns both the successfully formatted results and the IDs that failed.

        Each question is isolated by its own try/except (mirrors the existing
        per-question pattern in the /generate-report endpoint) so a single
        failure never aborts the batch. The companion data layer uses this to
        evaluate the full supported catalogue in one pass over the engine output.
        """
        results: List[Dict[str, Any]] = []
        failed_ids: List[str] = []
        for question_id in question_ids:
            try:
                results.append(self.answer_structured_question(
                    question_id=question_id,
                    pipeline_output=pipeline_output,
                ))
            except Exception as e:
                log.warning(f"Companion evaluation failed for question {question_id}: {str(e)}")
                failed_ids.append(question_id)
        return results, failed_ids

question_service = QuestionAnsweringService()

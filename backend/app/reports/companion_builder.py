"""Question Engine companion payload builder (P1).

Additive JSON data layer over the existing Question Engine pipeline output.

This module exposes the full regimented question catalogue and the evaluated /
NOT EVALUATED split to the /generate-report endpoint via the opt-in
``report_type=question-companion`` query parameter. It performs NO new
calculations: evaluation reuses ``question_service`` (the same routing, formula
evaluation and formatting used by the main report), and the client identity is
reused verbatim from the single authoritative chain used by the main report
(``pipeline_meta`` -> ``ReportBuilder.client_profile`` + ``report.metadata``).

Support rule (no new source of truth):
  - Evaluated  (65): registry domain_ids 2,4,5,6,7,8,10,12
    (Property, Marriage, Career, Wealth, Health, Children, Education,
    Spirituality) - domains the NatalPromise engine covers.
  - NOT EVALUATED (18): registry domain_ids 9,11,13
    (Litigation, Travel, Compatibility) - no NatalPromise domain coverage.
    These entries carry NO score/grade/probability/timing fields.
"""

from typing import Any, Dict, List

from app.core.registry_loader import QuestionRegistryLoader
from app.reports.builder import ReportBuilder
from app.services.question_service import question_service
from app.core.logging import log

COMPANION_REPORT_TYPE = "question-companion"
NOT_EVALUATED_STATUS = "NOT EVALUATED"
NOT_EVALUATED_REASON = "INSUFFICIENT ENGINE DOMAIN COVERAGE"

# domain_ids the NatalPromise engine covers (single authoritative support rule).
SUPPORTED_DOMAIN_IDS = {2, 4, 5, 6, 7, 8, 10, 12}


def _load_catalog() -> List[Dict[str, Any]]:
    """Loads the 83-entry question catalogue from the registry."""
    return QuestionRegistryLoader().load_registry()


class QuestionCompanionBuilder:
    """Builds the additive question-companion JSON payload."""

    def build(self, pipeline_output: Dict[str, Any], machine_index: Any) -> Dict[str, Any]:
        catalog = _load_catalog()

        # 1. Deterministic support split (registry-driven, registry-ordered).
        supported: List[Dict[str, Any]] = []
        un_evaluated: List[Dict[str, Any]] = []
        for record in catalog:
            if record["domain_id"] in SUPPORTED_DOMAIN_IDS:
                supported.append(record)
            else:
                un_evaluated.append({
                    "question_id": record["question_id"],
                    "domain": record["domain_name"],
                    "status": NOT_EVALUATED_STATUS,
                    "reason": NOT_EVALUATED_REASON,
                })

        # 2. Evaluate every supported question in one pass over the engine output.
        question_results: List[Dict[str, Any]] = []
        failed_ids: List[str] = []
        try:
            question_results, failed_ids = question_service.evaluate_many(
                question_ids=[record["question_id"] for record in supported],
                pipeline_output=pipeline_output,
            )
        except Exception as outer_e:
            log.error(
                f"Question companion batch evaluation failed wholesale: {str(outer_e)}"
            )
            failed_ids = [record["question_id"] for record in supported]

        # 3. Any per-question failure is surfaced as NOT EVALUATED (honest, no
        # fabricated score), appended to the un_evaluated list in registry order.
        failed_by_id = {record["question_id"]: record for record in supported}
        for qid in failed_ids:
            record = failed_by_id.get(qid)
            if record is None:
                continue
            un_evaluated.append({
                "question_id": qid,
                "domain": record["domain_name"],
                "status": NOT_EVALUATED_STATUS,
                "reason": "EVALUATION FAILED",
            })

        # 4. Client identity: single authoritative chain from the main report.
        # Reuses ReportBuilder so the identity is byte-for-byte the same source
        # as the default /generate-report JSON output (pipeline_meta ->
        # client_profile + metadata). No second identity source is introduced.
        identity_report = ReportBuilder().build_json_report(
            pipeline_outputs=pipeline_output,
            machine_index=machine_index,
            questions=[],
        )

        return {
            "report_type": COMPANION_REPORT_TYPE,
            "client_profile": identity_report.get("client_profile", {}),
            "metadata": {
                "report_id": identity_report.get("metadata", {}).get("report_id"),
                "generated_at": identity_report.get("metadata", {}).get("generated_at"),
                "client_info": identity_report.get("metadata", {}).get("client_info", {}),
            },
            "question_catalog": catalog,
            "question_results": question_results,
            "question_un_evaluated": un_evaluated,
        }


companion_builder = QuestionCompanionBuilder()
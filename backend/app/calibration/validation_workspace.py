import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, List
from pydantic import ValidationError
from .validation_models import (
    ValidationCase, ValidationWorkspaceData, AccuracyMetrics, 
    MatchStatus, CalibrationRecommendation, CalibrationHistoryRecord, RegressionAnalysis,
    ModuleResult, ComparisonRecord
)

log = logging.getLogger(__name__)

class ValidationWorkspace:
    def __init__(self, workspace_file: str = "validation_workspace.json"):
        self.workspace_file = workspace_file
        self.data = ValidationWorkspaceData()
        self.load_workspace()

    def load_workspace(self):
        if os.path.exists(self.workspace_file):
            try:
                with open(self.workspace_file, 'r', encoding='utf-8') as f:
                    raw = json.load(f)
                    self.data = ValidationWorkspaceData(**raw)
            except (json.JSONDecodeError, ValidationError) as e:
                log.error("Error loading workspace: %s", e)
                self.data = ValidationWorkspaceData()

    def save_workspace(self):
        with open(self.workspace_file, 'w', encoding='utf-8') as f:
            f.write(self.data.model_dump_json(indent=2))

    def create_case(self, case_id: str, native_name: str, canonical_json_path: str, birth_details: Dict[str, str], reviewer: str) -> ValidationCase:
        if case_id in self.data.cases:
            return self.data.cases[case_id]
        
        case = ValidationCase(
            case_id=case_id,
            native_name=native_name,
            canonical_json_path=canonical_json_path,
            birth_details=birth_details,
            reviewer=reviewer,
            validation_date=datetime.utcnow().isoformat()
        )
        self.data.cases[case_id] = case
        self.save_workspace()
        return case

    def record_comparison(self, case_id: str, module_name: str, expected: Any, actual: Any, status: MatchStatus, comments: str = ""):
        if case_id not in self.data.cases:
            raise ValueError(f"Case {case_id} not found.")
        
        case = self.data.cases[case_id]
        if hasattr(case.comparison, module_name):
            mod_result = getattr(case.comparison, module_name)
            mod_result.expected = expected
            mod_result.actual = actual
            mod_result.status = status
            mod_result.comments = comments
            self.save_workspace()
        else:
            raise ValueError(f"Module {module_name} not found in comparison record.")

    def update_case_engine_results(self, case_id: str, pipeline_output: Dict[str, Any]):
        if case_id in self.data.cases:
            self.data.cases[case_id].actual_engine_results = pipeline_output
            self.save_workspace()

    def calculate_accuracy(self) -> AccuracyMetrics:
        metrics = AccuracyMetrics()
        
        module_keys = ["planet_strength", "house_strength", "varga", "ashtakavarga", "functional_nature", "yogas", "dasha", "gochara", "mandali", "natal_promise", "master_probability", "question_engine"]
        
        module_stats = {k: {"match": 0, "total": 0} for k in module_keys}
        
        for case in self.data.cases.values():
            for mk in module_keys:
                mod_res: ModuleResult = getattr(case.comparison, mk)
                if mod_res.status != MatchStatus.NA:
                    metrics.total_applicable += 1
                    module_stats[mk]["total"] += 1
                    
                    if mod_res.status == MatchStatus.MATCH:
                        metrics.total_matches += 1
                        module_stats[mk]["match"] += 1
                    elif mod_res.status == MatchStatus.PARTIAL:
                        metrics.total_partial += 1
                        module_stats[mk]["match"] += 0.5  # Partial gives half weight
                    elif mod_res.status == MatchStatus.MISMATCH:
                        metrics.total_mismatches += 1
        
        if module_stats["planet_strength"]["total"] > 0:
            metrics.planet_strength_accuracy = (module_stats["planet_strength"]["match"] / module_stats["planet_strength"]["total"]) * 100
        if module_stats["house_strength"]["total"] > 0:
            metrics.house_strength_accuracy = (module_stats["house_strength"]["match"] / module_stats["house_strength"]["total"]) * 100
        if module_stats["yogas"]["total"] > 0:
            metrics.yoga_accuracy = (module_stats["yogas"]["match"] / module_stats["yogas"]["total"]) * 100
        if module_stats["question_engine"]["total"] > 0:
            metrics.question_accuracy = (module_stats["question_engine"]["match"] / module_stats["question_engine"]["total"]) * 100
        if module_stats["master_probability"]["total"] > 0:
            metrics.master_probability_accuracy = (module_stats["master_probability"]["match"] / module_stats["master_probability"]["total"]) * 100
            
        if metrics.total_applicable > 0:
            metrics.overall_accuracy = ((metrics.total_matches + (0.5 * metrics.total_partial)) / metrics.total_applicable) * 100
            
        return metrics

    def record_recommendation(self, param: str, old_val: Any, new_val: Any, reason: str, supporting: List[str]):
        rec = CalibrationRecommendation(
            parameter_name=param,
            old_value=old_val,
            new_value=new_val,
            reason=reason,
            supporting_cases=supporting
        )
        self.data.recommendations.append(rec)
        self.save_workspace()
        return rec

    def record_regression_analysis(self, param: str, improved: List[str], unchanged: List[str], regressed: List[str]):
        for rec in self.data.recommendations:
            if rec.parameter_name == param and rec.approval_status == "PENDING":
                rec.regression_check = RegressionAnalysis(
                    improved_cases=improved,
                    unchanged_cases=unchanged,
                    regressed_cases=regressed
                )
                self.save_workspace()
                return True
        return False

    def approve_recommendation(self, param: str, version: str, rollback_info: str = ""):
        for rec in self.data.recommendations:
            if rec.parameter_name == param and rec.approval_status == "PENDING":
                rec.approval_status = "APPROVED"
                
                history = CalibrationHistoryRecord(
                    calibration_version=version,
                    date=datetime.utcnow().isoformat(),
                    parameter=rec.parameter_name,
                    old_value=rec.old_value,
                    new_value=rec.new_value,
                    reason=rec.reason,
                    affected_cases=rec.supporting_cases,
                    approval="APPROVED",
                    rollback_information=rollback_info
                )
                self.data.history.append(history)
                self.save_workspace()
                return True
        return False

import os
import json
import traceback
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.pipeline_runner import PipelineRunner
from app.calibration.validation_workspace import ValidationWorkspace
from app.calibration.validation_models import MatchStatus

class BatchValidationRunner:
    def __init__(self, workspace_path: str = "validation_workspace.json", data_dir: str = "validation/ground_truth"):
        self.workspace = ValidationWorkspace(workspace_path)
        self.data_dir = data_dir
        self.pipeline = PipelineRunner()
        self.summary = {
            "total_cases": 0,
            "successful_cases": 0,
            "failed_cases": 0,
            "pending_comparisons": 0,
            "completed_comparisons": 0,
            "validation_coverage": 0.0,
            "failures": []
        }

    def _discover_datasets(self) -> List[str]:
        case_files = []
        if not os.path.exists(self.data_dir):
            return []
            
        for root, _, files in os.walk(self.data_dir):
            for file in files:
                if file.endswith(".json") and file.startswith("CASE_") and not file.endswith("_benchmark.json"):
                    case_files.append(os.path.join(root, file))
        return sorted(case_files)

    def _load_benchmark(self, json_path: str) -> Optional[Dict[str, Any]]:
        base = os.path.splitext(json_path)[0]
        bench_path = f"{base}_benchmark.json"
        if os.path.exists(bench_path):
            try:
                with open(bench_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return None

    def run_batch(self):
        case_files = self._discover_datasets()
        self.summary["total_cases"] = len(case_files)
        
        print(f"Starting Batch Validation: {len(case_files)} cases found.")
        
        for idx, file_path in enumerate(case_files, 1):
            case_id = os.path.basename(file_path).replace(".json", "")
            print(f"[{idx}/{len(case_files)}] Processing {case_id}...")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    payload = json.load(f)
                
                metadata = payload.get("metadata", {})
                native_name = metadata.get("name", case_id)
                birth_details = {
                    "dob": metadata.get("dob", ""),
                    "tob": metadata.get("tob", ""),
                    "pob": metadata.get("pob", "")
                }
                
                # 1. Create Case in Workspace
                case = self.workspace.create_case(
                    case_id=case_id,
                    native_name=native_name,
                    canonical_json_path=file_path,
                    birth_details=birth_details,
                    reviewer="BatchRunner"
                )
                
                # 2. Execute Pipeline
                result = self.pipeline.process(payload)
                
                # 3. Store Engine Outputs
                engine_outputs = result.get("engine_outputs", {})
                actual_results = {
                    "planet_strength": engine_outputs.get("planet_strength", {}),
                    "house_strength": engine_outputs.get("house_strength", {}),
                    "varga": engine_outputs.get("varga", {}),
                    "ashtakavarga": engine_outputs.get("ashtakavarga", {}),
                    "functional_nature": engine_outputs.get("functional_nature", {}),
                    "yogas": engine_outputs.get("yogas", {}),
                    "dasha": engine_outputs.get("dasha", {}),
                    "gochara": engine_outputs.get("transit", {}), # transit engine handles gochara
                    "mandali": engine_outputs.get("mandali", {}),
                    "natal_promise": result.get("natal_promise", {}),
                    "master_probability": result.get("master_probability", {}),
                    "question_engine": result.get("question_engine", {})
                }
                
                self.workspace.update_case_engine_results(case_id, actual_results)
                
                # 4. Mode B: Populate Comparisons if Benchmark Exists
                benchmark = self._load_benchmark(file_path)
                if benchmark:
                    for mod_key, mod_actual in actual_results.items():
                        expected = benchmark.get(mod_key)
                        if expected is not None:
                            status = MatchStatus.MATCH if expected == mod_actual else MatchStatus.MISMATCH
                            self.workspace.record_comparison(case_id, mod_key, expected, mod_actual, status)
                            
                self.summary["successful_cases"] += 1
                case.validation_status = "COMPLETED" if benchmark else "PENDING_COMPARISON"
                if benchmark:
                    self.summary["completed_comparisons"] += 1
                else:
                    self.summary["pending_comparisons"] += 1
                self.workspace.save_workspace()
                print(" -> Pipeline OK. Workspace Updated.")
                
            except Exception as e:
                self.summary["failed_cases"] += 1
                err = traceback.format_exc()
                self.summary["failures"].append({"case_id": case_id, "error": str(e), "traceback": err})
                print(f" -> FAILED: {str(e)}")
                if case_id in self.workspace.data.cases:
                    self.workspace.data.cases[case_id].validation_status = "FAILED"
                    self.workspace.data.cases[case_id].notes = str(e)
                    self.workspace.save_workspace()
                    
        if self.summary["total_cases"] > 0:
            self.summary["validation_coverage"] = (self.summary["successful_cases"] / self.summary["total_cases"]) * 100
            
        metrics = self.workspace.calculate_accuracy()
        
        self.workspace.save_workspace()
        
        with open("batch_summary.json", 'w', encoding='utf-8') as f:
            json.dump(self.summary, f, indent=2)
            
        with open("validation_statistics.json", 'w', encoding='utf-8') as f:
            json.dump(metrics.model_dump(), f, indent=2)
            
        print("\nBatch Validation Completed.")
        print(f"Total: {self.summary['total_cases']}, Success: {self.summary['successful_cases']}, Failed: {self.summary['failed_cases']}")

if __name__ == "__main__":
    runner = BatchValidationRunner()
    runner.run_batch()

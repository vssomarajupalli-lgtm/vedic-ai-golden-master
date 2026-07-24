import os
import json
from copy import deepcopy
from typing import Dict, Any, List, Tuple

from app.calibration.batch_runner import BatchValidationRunner
from app.calibration.calibration_manager import CalibrationManager
from app.pipeline_runner import PipelineRunner
from app.engines.planet_strength_engine import PlanetStrengthEngine
from app.engines.house_strength_engine import HouseStrengthEngine
from app.engines.varga_engine import VargaEngine
from app.engines.dasha_engine import DashaEngine
from app.engines.rasi_strength_engine import RasiStrengthEngine
from app.engines.ashtakavarga_engine import AshtakavargaEngine
from app.engines.transit_engine import TransitEngine
from app.engines.mandali_generator import MandaliGenerator
from app.engines.yoga_engine import YogaEngine
from app.engines.question_engine import QuestionEngine
from app.engines.functional_nature_engine import FunctionalNatureEngine
from app.engines.master_probability_engine import MasterProbabilityEngine
from app.engines.natal_promise_engine import NatalPromiseEngine

class ProfileComparator:
    def __init__(self, profile_a: str, profile_b: str, data_dir: str = "validation/ground_truth"):
        self.profile_a = profile_a.replace('.json', '')
        self.profile_b = profile_b.replace('.json', '')
        self.data_dir = data_dir

    def _create_runner_for_profile(self, profile_id: str) -> PipelineRunner:
        mgr = CalibrationManager(profile_id)
        runner = PipelineRunner()
        runner.planet_engine = PlanetStrengthEngine(calibration=mgr)
        runner.house_engine = HouseStrengthEngine(calibration=mgr)
        runner.varga_engine = VargaEngine(calibration=mgr)
        runner.dasha_engine = DashaEngine(calibration=mgr)
        runner.rasi_engine = RasiStrengthEngine(calibration=mgr)
        runner.av_engine = AshtakavargaEngine(calibration=mgr)
        runner.transit_engine = TransitEngine(calibration=mgr)
        runner.mandali_generator = MandaliGenerator()  # Does not take calibration
        runner.yoga_engine = YogaEngine(calibration=mgr)
        runner.question_engine = QuestionEngine(calibration=mgr)
        runner.functional_nature = FunctionalNatureEngine(calibration=mgr)
        runner.master_engine = MasterProbabilityEngine(calibration=mgr)
        runner.natal_engine = NatalPromiseEngine(calibration=mgr)
        return runner

    def run_comparison(self):
        print(f"Comparing Profiles: {self.profile_a} vs {self.profile_b}")
        
        # 1. Run Batch A
        runner_a = BatchValidationRunner(workspace_path="workspace_a.json", data_dir=self.data_dir)
        runner_a.pipeline = self._create_runner_for_profile(self.profile_a)
        runner_a.run_batch()
        metrics_a = runner_a.workspace.calculate_accuracy().model_dump()
        
        # 2. Run Batch B
        runner_b = BatchValidationRunner(workspace_path="workspace_b.json", data_dir=self.data_dir)
        runner_b.pipeline = self._create_runner_for_profile(self.profile_b)
        runner_b.run_batch()
        metrics_b = runner_b.workspace.calculate_accuracy().model_dump()
        
        # 3. Delta Analysis
        delta = {}
        for k in metrics_a.keys():
            if isinstance(metrics_a[k], float):
                delta[k] = metrics_b[k] - metrics_a[k]
            elif isinstance(metrics_a[k], int):
                delta[k] = metrics_b[k] - metrics_a[k]
        
        # 4. Regression Analysis
        improved = []
        unchanged = []
        regressed = []
        
        cases_a = runner_a.workspace.data.cases
        cases_b = runner_b.workspace.data.cases
        
        for case_id in cases_a:
            if case_id not in cases_b:
                continue
                
            case_a = cases_a[case_id]
            case_b = cases_b[case_id]
            
            score_a = 0
            score_b = 0
            regressed_modules = []
            
            mods_a = case_a.comparison.model_dump()
            mods_b = case_b.comparison.model_dump()
            
            for m in mods_a:
                sa = mods_a[m]["status"]
                sb = mods_b[m]["status"]
                
                va = 1 if sa == "MATCH" else (0.5 if sa == "PARTIAL MATCH" else 0)
                vb = 1 if sb == "MATCH" else (0.5 if sb == "PARTIAL MATCH" else 0)
                
                score_a += va
                score_b += vb
                
                if vb < va:
                    regressed_modules.append(m)
                
            if score_b > score_a:
                improved.append(case_id)
            elif score_b < score_a or len(regressed_modules) > 0:
                regressed.append({
                    "case_id": case_id, 
                    "reason": "Accuracy dropped in specific modules",
                    "modules": regressed_modules
                })
            else:
                unchanged.append(case_id)

        # 5. Calibration Decision
        overall_a = metrics_a.get("overall_accuracy", 0)
        overall_b = metrics_b.get("overall_accuracy", 0)
        
        approved = False
        if overall_b > overall_a and len(regressed) == 0:
            approved = True
            
        summary = {
            "profile_a": self.profile_a,
            "profile_b": self.profile_b,
            "decision": "APPROVE" if approved else "REJECT",
            "overall_a": overall_a,
            "overall_b": overall_b,
            "delta": delta,
            "regressions": regressed
        }
        
        # 6. Generate JSONs
        with open("comparison_summary.json", 'w') as f:
            json.dump(summary, f, indent=2)
        with open("comparison_delta.json", 'w') as f:
            json.dump(delta, f, indent=2)
        with open("comparison_statistics.json", 'w') as f:
            json.dump({"metrics_a": metrics_a, "metrics_b": metrics_b}, f, indent=2)
            
        # 7. Generate MD report
        md = f"""# Calibration Profile Comparison Report

## Profiles
- **Profile A (Baseline)**: `{self.profile_a}`
- **Profile B (Candidate)**: `{self.profile_b}`

## Recommendation
**{'✅ APPROVE' if approved else '❌ REJECT'}**

## Accuracy Metrics
| Metric | Profile A | Profile B | Delta |
|--------|-----------|-----------|-------|
| Overall Accuracy | {overall_a:.2f}% | {overall_b:.2f}% | {delta.get('overall_accuracy', 0):+.2f}% |
| Planet Strength | {metrics_a.get('planet_strength_accuracy',0):.2f}% | {metrics_b.get('planet_strength_accuracy',0):.2f}% | {delta.get('planet_strength_accuracy', 0):+.2f}% |
| House Strength | {metrics_a.get('house_strength_accuracy',0):.2f}% | {metrics_b.get('house_strength_accuracy',0):.2f}% | {delta.get('house_strength_accuracy', 0):+.2f}% |
| Question Engine | {metrics_a.get('question_accuracy',0):.2f}% | {metrics_b.get('question_accuracy',0):.2f}% | {delta.get('question_accuracy', 0):+.2f}% |
| Master Probability | {metrics_a.get('master_probability_accuracy',0):.2f}% | {metrics_b.get('master_probability_accuracy',0):.2f}% | {delta.get('master_probability_accuracy', 0):+.2f}% |

## Regression Analysis
- **Improved Cases**: {len(improved)}
- **Unchanged Cases**: {len(unchanged)}
- **Regressed Cases**: {len(regressed)}

"""
        if regressed:
            md += "### Regressions\n"
            for r in regressed:
                md += f"- **{r['case_id']}**: {r['reason']} (Modules: {', '.join(r['modules'])})\n"
                
        with open("comparison_report.md", 'w', encoding='utf-8') as f:
            f.write(md)
        print("Comparison Complete. Decision:", "APPROVE" if approved else "REJECT")
        print("Generated: comparison_summary.json, comparison_delta.json, comparison_statistics.json, comparison_report.md")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        comp = ProfileComparator(sys.argv[1], sys.argv[2])
        comp.run_comparison()
    else:
        print("Usage: python profile_comparator.py <profile_a> <profile_b>")

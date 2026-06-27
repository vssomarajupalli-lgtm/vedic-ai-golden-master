import os
import json
import sys

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.pipeline_runner import PipelineRunner
from app.engines.question_engine import QuestionEngine

def load_ground_truth(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_canonical_payload(chart_id):
    # Attempt to derive filename from chart_id
    filename = f"{chart_id.replace('CASE_001_', '').lower()}_canonical_content.json"
    
    # Get project root (d:\vedic-ai-system)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    path = os.path.join(project_root, 'extracted_json', filename)
    if not os.path.exists(path):
        # Fallback to known Raju JSON for testing
        path = os.path.join(project_root, 'extracted_json', 'raju_canonical_content.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_validation(truth_file):
    truth = load_ground_truth(truth_file)
    chart_id = truth.get("chart_id")
    payload = load_canonical_payload(chart_id)
    
    runner = PipelineRunner()
    results = runner.process(payload)
    engine = QuestionEngine()
    
    domains_tested = 0
    passed = 0
    
    print("==================================================")
    print(f"  VALIDATION RUN: {chart_id}")
    print("==================================================")
    
    for domain, domain_data in truth.get("domains", {}).items():
        if not domain_data or "promise" not in domain_data:
            continue
        
        domains_tested += 1
        actual_occurred = domain_data["promise"]["occurred"]
        
        # Simulate question
        question = f"How is my {domain}?"
        routed_domain = engine.route_domain(question)
        
        if routed_domain != domain:
            print(f"[{domains_tested}] {domain.capitalize()}")
            print(f"    Error: Routing failed. Expected {domain}, got {routed_domain}")
            print("    Result:    ❌ FAIL\n")
            continue
            
        # Get components
        engine_outputs = results.get("engine_outputs", {})
        natal_promise = engine_outputs.get("natal_promise", {}).get(domain, {})
        dasha_activation = engine_outputs.get("dashas", {}).get(domain, {})
        transit_activation = engine_outputs.get("transits", {}).get(domain, {})
        final_probability = engine_outputs.get("probabilities", {}).get(domain, {})
        
        answer = engine.compose_response(
            question=question,
            domain=domain,
            natal_promise=natal_promise,
            dasha_activation=dasha_activation,
            transit_activation=transit_activation,
            final_probability=final_probability
        )
        
        score = answer["natal_promise"]["score"]
        promise_grade = answer["natal_promise"]["promise"]
        predicted_occurred = score >= 50.0
        
        is_pass = (actual_occurred == predicted_occurred)
        if is_pass:
            passed += 1
            
        actual_str = "Occurred (True)" if actual_occurred else "Denied (False)"
        predicted_str = "Occurred (True)" if predicted_occurred else "Denied (False)"
        result_icon = "✅ PASS" if is_pass else "❌ FAIL"
        
        print(f"[{domains_tested}] {domain.capitalize()}")
        print(f"    Actual:    {actual_str}")
        print(f"    Predicted: {predicted_str} | Score: {score:.1f} ({promise_grade})")
        print(f"    Result:    {result_icon}\n")

    accuracy = (passed / domains_tested * 100) if domains_tested > 0 else 0.0
    print("--------------------------------------------------")
    print(f"Accuracy: {accuracy:.1f}% ({passed}/{domains_tested})")
    print("==================================================")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_validation(sys.argv[1])
    else:
        default_path = os.path.join(os.path.dirname(__file__), 'ground_truth', 'cases_01_20', 'CASE_001_RAJU.json')
        run_validation(default_path)

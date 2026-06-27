import json
from app.pipeline_runner import PipelineRunner
from app.api.v1.endpoints.queries import ask_structured_question
from app.schemas.question import QuestionRequest

runner = PipelineRunner()
canonical_payload = json.load(open("../extracted_json/canonical_content.json"))
engine_outputs = runner.process(canonical_payload)
registry = json.load(open("app/config/question_registry.json"))

domains_to_check = ["marriage", "career", "education", "property", "children", "wealth"]

print("=== CASE_001 VALIDATION AFTER PATCH ===")
for domain in domains_to_check:
    # Find a question for the domain
    q_id = None
    for item in registry:
        if item.get("domain_name", "").lower() == domain:
            q_id = item["question_id"]
            break
            
    if not q_id:
        print(f"[{domain.upper()}] No question found in registry.")
        continue
        
    req = QuestionRequest(question_id=q_id, engine_outputs=engine_outputs)
    try:
        res = ask_structured_question(req)
        r = res.results[0]
        
        promise = r.promise_assessment
        dasha = r.dasha_activation
        conclusion = r.final_conclusion
        
        print(f"[{domain.upper()}]")
        print(f"1. Natal Promise Score: {promise.promise_score}")
        print(f"2. Natal Promise Grade: {promise.promise_grade}")
        print(f"3. MD: {dasha.mahadasha}")
        print(f"4. AD: {dasha.antardasha}")
        print(f"5. PD: {dasha.pratyantardasha}")
        print(f"6. Activation Index: {dasha.activation_index}")
        print(f"7. Formula Result: {conclusion.assessment}")
        print("-----------------------------------")
    except Exception as e:
         print(f"[{domain.upper()}] (QID: {q_id}) Error: {str(e)}")

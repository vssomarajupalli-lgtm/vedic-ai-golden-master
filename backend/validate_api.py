from main import app
from fastapi.testclient import TestClient
import json

client = TestClient(app)

print("=== Health Check ===")
r = client.get('/api/v1/explanations/health')
print(r.status_code, r.json())

print("\n=== Generate Explanation ===")
pipeline_output = {
    'metadata': {'ascendant_sign': 'aries'},
    'master_probability': {
        'final_score': 61, 'grade': 'MODERATE',
        'breakdown': {'natal_promise': 45, 'transit': 78, 'dasha': 65}
    },
    'engine_outputs': {
        'natal_promise': {'marriage': 45},
        'transit': {'activation_score': 78},
        'dasha': {'strength': 65}
    },
    'target_date_utc': '2026-07-29T10:00:00Z'
}

r = client.post('/api/v1/explanations/generate', json={
    'question_id': '7.1',
    'question_text': 'Will I get married?',
    'pipeline_output': pipeline_output,
    'target_date_utc': '2026-07-29T10:00:00Z'
})
print('Status:', r.status_code)
data = r.json()
print(json.dumps(data, indent=2))

print("\n=== Verify Response Structure ===")
required = ['question', 'domain', 'routed', 'explanation', 'citations', 'evidence_summary', 'confidence', 'metadata', 'processing_time_ms']
for field in required:
    present = field in data
    if present:
        print(f"  {field}: OK")
    else:
        print(f"  {field}: MISSING")

print("\n=== Citation Validation ===")
for i, c in enumerate(data['citations']):
    print(f"  Citation {i}: type={c.get('type')}, evidence_level={c.get('evidence_level')}, path={c.get('path')}, value={c.get('value')}")

print("\n=== Evidence Summary ===")
es = data['evidence_summary']
print(f"  total: {es['total_citations']}, by_type: {es['by_type']}, highest: {es['highest_evidence_level']}")

print("\n=== Confidence ===")
print(f"  {data['confidence']} (valid: {data['confidence'] in ['HIGH', 'MEDIUM', 'LOW']})")
import json
import sys
sys.path.insert(0, '.')
from app.pipeline_runner import PipelineRunner
from app.api.v1.endpoints.charts import process_chart
from app.schemas.chart import ChartProcessRequest
from app.parsers.json_normalizer import JsonNormalizer

try:
    with open('../extracted_json/canonical_content.json', 'r', encoding='utf-8') as f:
        canonical = json.load(f)
    with open('../extracted_json/machine_index.json', 'r', encoding='utf-8') as f:
        machine = json.load(f)
except FileNotFoundError as e:
    print(f"Error loading files: {e}")
    sys.exit(1)

print('\n--- 1. JsonNormalizer output summary ---')
normalizer = JsonNormalizer()
raw_data = dict(canonical)
raw_data['_machine_index'] = machine
normalized = normalizer.normalize(raw_data)
print('Keys present:', list(normalized.keys()))
print('Metadata:', normalized['metadata'])
print('Planets count:', len(normalized['planets']))
print('Houses count:', len(normalized['houses']))

print('\n--- 2. PlanetStrengthEngine output ---')
pipeline = PipelineRunner()
outputs = pipeline.process(raw_data)
eng_outs = outputs['engine_outputs']
for p, data in eng_outs['planets'].items():
    flags = data.get('confidence_flags', [])
    print(f"{p}: score={data.get('final_score')}, flags={flags}")

print('\n--- 3. HouseStrengthEngine output ---')
for h, data in eng_outs['houses'].items():
    print(f"House {h}: score={data.get('final_score')}")

print('\n--- 4. NatalPromiseEngine output ---')
for d, data in eng_outs['natal_promise'].items():
    print(f"{d}: score={data.get('score')}, breakdown={data.get('breakdown')}")

print('\n--- 5. MasterProbabilityEngine output ---')
print(json.dumps(outputs['master_probability'], indent=2))

print('\n--- 6. Exact JSON returned by PipelineRunner ---')
print('Keys:', list(outputs.keys()))
print('Engine output keys:', list(outputs['engine_outputs'].keys()))

print('\n--- 7. Exact JSON returned by /process-chart ---')
yogas = outputs.get('engine_outputs', {}).get('yogas', {}).get('active_yogas', [])
final_resp = {
    'status': 'success',
    'final_score': outputs.get('master_probability', {}).get('final_score', 0.0),
    'probability_grade': outputs.get('master_probability', {}).get('grade', 'UNKNOWN'),
    'breakdown': outputs.get('master_probability', {}).get('breakdown', {}),
    'yogas': yogas
}
print(json.dumps(final_resp, indent=2))

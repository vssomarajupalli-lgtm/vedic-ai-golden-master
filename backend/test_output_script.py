import json
import sys

with open('D:/HoroscopeCleaner_Final/OUTPUT/raju_canonical_content.json', 'r', encoding='utf-8') as f:
    raw_payload = json.load(f)

sys.path.append('d:/vedic-ai-system/backend')
from app.pipeline_runner import PipelineRunner

runner = PipelineRunner()
output = runner.process(raw_payload)

print('\n--- REFACTORED DASHA SYNTHESIS ---')
dasha_output = output['engine_outputs'].get('dashas', {})
synthesis = dasha_output.get('synthesis', {})
print(json.dumps(synthesis, indent=2))

import json
import sys

with open('D:/HoroscopeCleaner_Final/OUTPUT/raju_canonical_content.json', 'r', encoding='utf-8') as f:
    raw_payload = json.load(f)

sys.path.append('d:/vedic-ai-system/backend')
from app.engines.dasha_engine import DashaEngine
engine = DashaEngine()
res = engine.evaluate(raw_payload, {})
print("Raw evaluate:", res)

import json
import os
import sys

# Ensure D:\vedic-ai-system\backend is in path
sys.path.insert(0, os.path.abspath("."))

from app.api.v1.endpoints.queries import ask_structured_question
from app.schemas.question import QuestionRequest

question_id = "7.1" # Marriage Promise

# Mock payload
payload = {
    "question_id": question_id,
    "engine_outputs": {
        "natal_promise": {
            "marriage": {
                "score": 85,
                "promise": "STRONG"
            }
        },
        "dashas": {
            "synthesis": {
                "active_md": "venus",
                "active_ad": "jupiter",
                "active_pd": "moon",
                "md_strength": 80.0,
                "ad_strength": 90.0,
                "pd_strength": 75.0
            }
        }
    }
}

req = QuestionRequest(**payload)

try:
    response = ask_structured_question(req)
    print(response.model_dump_json(indent=2))
except Exception as e:
    import traceback
    traceback.print_exc()

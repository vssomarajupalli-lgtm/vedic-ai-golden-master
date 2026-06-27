import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Create a minimal FastAPI app context for testing the router if main is not fully mocking ready
# Alternatively we can test the router directly since it's just a FastAPI APIRouter
from fastapi import FastAPI
from app.api.v1.endpoints.queries import router

app = FastAPI()
app.include_router(router)

client = TestClient(app)

# Dummy engine output to pass pydantic validation
dummy_engine_output = {
    "breakdown": {
        "metadata": {"ascendant_sign": "aries"},
        "dashas": {},
        "natal_promise": {}
    }
}

@patch('app.api.v1.endpoints.queries.pipeline_runner.answer_question')
def test_ask_question_with_valid_id(mock_answer_question):
    # Setup mock to return a predictable response
    mock_answer_question.return_value = {"answer_text": "Mocked deterministic answer based on Marriage Timing."}
    
    payload = {
        "question_id": "7.2",
        "engine_outputs": dummy_engine_output
    }
    
    response = client.post("/ask-question", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["resolved_question_id"] == "7.2"
    assert data["answer_text"] == "Mocked deterministic answer based on Marriage Timing."
    
    # Verify the fallback question_text injection happened correctly 
    # since we didn't pass question_text in the payload.
    mock_answer_question.assert_called_once()
    args, kwargs = mock_answer_question.call_args
    assert kwargs["question"] == "Marriage Timing"
    
@patch('app.api.v1.endpoints.queries.pipeline_runner.answer_question')
def test_ask_question_with_invalid_id(mock_answer_question):
    payload = {
        "question_id": "99.99_UNKNOWN",
        "engine_outputs": dummy_engine_output
    }
    
    response = client.post("/ask-question", json=payload)
    
    # Should safely reject with 422
    assert response.status_code == 422
    data = response.json()
    assert "99.99_UNKNOWN" in data["detail"]
    assert "not found in registry" in data["detail"]
    mock_answer_question.assert_not_called()

def test_ask_question_missing_both_id_and_text():
    payload = {
        "engine_outputs": dummy_engine_output
    }
    
    response = client.post("/ask-question", json=payload)
    
    # Should safely reject with 400
    assert response.status_code == 400
    data = response.json()
    assert "Must provide either question_text or question_id" in data["detail"]

@patch('app.api.v1.endpoints.queries.pipeline_runner.answer_question')
def test_ask_question_legacy_free_text(mock_answer_question):
    mock_answer_question.return_value = {"answer_text": "Mocked NLP response"}
    
    payload = {
        "question_text": "When will I get married?",
        "engine_outputs": dummy_engine_output
    }
    
    response = client.post("/ask-question", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["resolved_question_id"] is None
    assert data["answer_text"] == "Mocked NLP response"
    
    # Verify it passed the exact text to the engine
    mock_answer_question.assert_called_once()
    args, kwargs = mock_answer_question.call_args
    assert kwargs["question"] == "When will I get married?"

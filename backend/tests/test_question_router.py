import pytest
import os
import json
import tempfile
from app.core.registry_loader import QuestionRegistryLoader
from app.core.question_router import QuestionRouter

@pytest.fixture
def temp_registry():
    fd, path = tempfile.mkstemp(suffix=".json")
    yield path
    os.close(fd)
    os.remove(path)

def create_mock_registry(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)

def test_router_valid_question_id():
    # Uses the real config mapped from 11A
    router = QuestionRouter()
    
    response = router.route_question("7.2")
    assert response["status"] == "success"
    assert response["formula_key"] == "MAR_TIMING_001"
    assert "registry_record" in response
    assert response["metadata"]["timing_required"] is True

def test_router_missing_question_id():
    router = QuestionRouter()
    
    response = router.route_question("99.99_UNKNOWN")
    assert response["status"] == "error"
    assert response["error_type"] == "missing_registry_entry"
    assert "99.99_UNKNOWN" in response["message"]

def test_router_malformed_question_id():
    router = QuestionRouter()
    
    # Passing None
    response = router.route_question(None)
    assert response["status"] == "error"
    assert response["error_type"] == "malformed_question_id"
    
    # Passing int
    response = router.route_question(7)
    assert response["status"] == "error"
    assert response["error_type"] == "malformed_question_id"
    
    # Passing empty string
    response = router.route_question("")
    assert response["status"] == "error"
    assert response["error_type"] == "malformed_question_id"

def test_router_handles_duplicate_registry_safely(temp_registry):
    bad_data = [
        {
            "question_id": "7.1", "domain_id": 7, "domain_name": "Marriage", 
            "question_name": "Marriage Prospects", "formula_key": "MAR_PROS_001", 
            "timing_required": False, "future_gochara_required": False
        },
        {
            "question_id": "7.1", "domain_id": 7, "domain_name": "Marriage", 
            "question_name": "Marriage Timing", "formula_key": "MAR_TIMING_001", 
            "timing_required": True, "future_gochara_required": True
        }
    ]
    create_mock_registry(temp_registry, bad_data)
    loader = QuestionRegistryLoader(file_path=temp_registry)
    
    # Router should catch the duplicate error during init
    router = QuestionRouter(loader=loader)
    
    # Calling route_question should return safe error, not crash
    response = router.route_question("7.1")
    assert response["status"] == "error"
    assert response["error_type"] == "registry_configuration_error"
    assert "Duplicate question_id detected" in response["message"]

def test_integration_router_resolves_full_chain():
    """
    Integration Test: Verify Router successfully resolves:
    Question ID -> Registry Entry -> Formula Key
    """
    router = QuestionRouter()
    
    # Execution
    target_id = "10.2"
    result = router.route_question(target_id)
    
    # Verification
    assert result["status"] == "success"
    
    # 1. Question ID resolution
    record = result["registry_record"]
    assert record["question_id"] == target_id
    assert record["domain_name"] == "Career"
    
    # 2. Formula Key resolution
    assert result["formula_key"] == "CAR_CHANGE_001"
    
    # 3. Metadata resolution
    assert result["metadata"]["timing_required"] is True

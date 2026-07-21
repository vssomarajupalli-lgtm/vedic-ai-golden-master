import pytest
import os
import tempfile
import json
from app.core.registry_loader import QuestionRegistryLoader, RegistryValidationError

@pytest.fixture
def temp_registry_file():
    fd, path = tempfile.mkstemp(suffix=".json")
    yield path
    os.close(fd)
    os.remove(path)

def test_load_valid_registry():
    # Uses default path which should be pointing to the real question_registry.json
    loader = QuestionRegistryLoader()
    data = loader.load_registry()
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Check if get_question works
    q = loader.get_question("7.2")
    assert q is not None
    assert q["question_name"] == "Marriage Timing"

def test_missing_file_raises_error():
    loader = QuestionRegistryLoader(file_path="/path/that/does/not/exist.json")
    with pytest.raises(FileNotFoundError):
        loader.load_registry()

def test_missing_fields_raises_error(temp_registry_file):
    # Missing 'domain_name' and 'timing_required'
    bad_data = [
        {
            "question_id": "99.1",
            "domain_id": 99,
            "question_name": "Broken Node",
            "formula_key": "BROKEN_001",
            "future_gochara_required": False
        }
    ]
    with open(temp_registry_file, 'w') as f:
        json.dump(bad_data, f)
        
    loader = QuestionRegistryLoader(file_path=temp_registry_file)
    with pytest.raises(RegistryValidationError, match="missing required fields"):
        loader.load_registry()

def test_duplicate_question_id_raises_error(temp_registry_file):
    bad_data = [
        {
            "question_id": "7.1",
            "domain_id": 7,
            "domain_name": "Marriage",
            "question_name": "Marriage Prospects",
            "formula_key": "MAR_PROS_001",
            "timing_required": False,
            "future_gochara_required": False
        },
        {
            "question_id": "7.1", # Duplicate
            "domain_id": 7,
            "domain_name": "Marriage",
            "question_name": "Marriage Timing",
            "formula_key": "MAR_TIMING_NORMAL",
            "timing_required": True,
            "future_gochara_required": True
        }
    ]
    with open(temp_registry_file, 'w') as f:
        json.dump(bad_data, f)
        
    loader = QuestionRegistryLoader(file_path=temp_registry_file)
    with pytest.raises(RegistryValidationError, match="Duplicate question_id"):
        loader.load_registry()

def test_duplicate_formula_key_is_allowed(temp_registry_file):
    """Multiple questions mapping to the same formula_key is valid."""
    data = [
        {
            "question_id": "7.1",
            "domain_id": 7,
            "domain_name": "Marriage",
            "question_name": "Marriage Prospects",
            "formula_key": "MAR_PROS_001",
            "timing_required": False,
            "future_gochara_required": False
        },
        {
            "question_id": "7.2", 
            "domain_id": 7,
            "domain_name": "Marriage",
            "question_name": "Marriage Timing",
            "formula_key": "MAR_PROS_001",
            "timing_required": True,
            "future_gochara_required": True
        }
    ]
    with open(temp_registry_file, 'w') as f:
        json.dump(data, f)
        
    loader = QuestionRegistryLoader(file_path=temp_registry_file)
    registry = loader.load_registry()
    assert len(registry) == 2

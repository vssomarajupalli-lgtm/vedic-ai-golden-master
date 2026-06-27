import pytest
from app.core.search_layer import SearchLayer
from app.core.question_router import QuestionRouter

def test_search_empty():
    search = SearchLayer()
    result = search.resolve("   ")
    assert result["status"] == "error"
    assert result["error_type"] == "empty_search"

def test_search_keyword_match():
    search = SearchLayer()
    result = search.resolve("I want to know about my marriage")
    assert result["status"] == "success"
    assert result["matched_domain_id"] == 7
    # Should contain 7.1, 7.2, etc. (based on our seed config)
    assert "7.1" in result["question_ids"]
    assert "7.2" in result["question_ids"]

def test_search_alias_match():
    search = SearchLayer()
    result = search.resolve("When will I get a job?")
    assert result["status"] == "success"
    assert result["matched_domain_id"] == 10
    assert "10.1" in result["question_ids"]
    assert "10.2" in result["question_ids"]

def test_search_misspelling_match():
    search = SearchLayer()
    result = search.resolve("marrage timing")
    assert result["status"] == "success"
    assert result["matched_domain_id"] == 7

def test_search_unknown_keyword():
    search = SearchLayer()
    result = search.resolve("When will I buy a car?")  # "car" is not in our simple dictionary yet
    assert result["status"] == "error"
    assert result["error_type"] == "unknown_keyword"

def test_search_multi_match_keyword():
    search = SearchLayer()
    # Matches "job" (10) and "money" (2)
    result = search.resolve("Will my job give me money?")
    assert result["status"] == "error"
    assert result["error_type"] == "multiple_domain_matches"

def test_integration_search_to_router():
    """
    Integration Test:
    Free Text -> Search Layer -> Question IDs -> Question Router
    """
    search = SearchLayer()
    router = QuestionRouter(loader=search.loader) # share the loader instance
    
    # 1. Search Phase
    search_result = search.resolve("tell me about my wife")
    assert search_result["status"] == "success"
    
    # User gets a list of IDs. Suppose they implicitly/automatically select the first one 
    # or the UI presents them and they tap the first one. We simulate routing the first matched ID.
    target_id = search_result["question_ids"][0] # e.g. "7.1"
    
    # 2. Router Phase
    router_result = router.route_question(target_id)
    assert router_result["status"] == "success"
    assert router_result["registry_record"]["domain_id"] == 7
    assert "formula_key" in router_result

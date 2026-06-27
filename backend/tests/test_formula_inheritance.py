import pytest
from app.formulas.loader import formula_repository_loader

def test_formula_inheritance_merging():
    """
    Tests that a Child Variant successfully merges required signals
    and confidence layers from its Base Family.
    """
    # Force reload in case tests run out of order
    formula_repository_loader._load_registry()
    
    # Base: MAR_TIMING_BASE
    base = formula_repository_loader.get_formula("MAR_TIMING_BASE")
    assert "7th_house" in base.required_signals
    
    # Child: MAR_TIMING_DELAY
    child = formula_repository_loader.get_formula("MAR_TIMING_DELAY")
    
    # Should contain its own signals
    assert "saturn" in child.required_signals
    # AND inherited signals
    assert "7th_house" in child.required_signals
    assert "lagna_lord" in child.required_signals
    
    # Should contain inherited engines
    assert "TransitEngine" in child.required_engines
    assert "DashaEngine" in child.required_engines
    
    # Should contain inherited dasha layers
    assert "mahadasha" in child.required_dasha_layers
    
    # Should contain its own confidence layers
    assert "saturn_aspect_7th" in child.required_confidence_layers
    # AND inherited confidence layers
    assert "dasha_lord_aspect_7th" in child.required_confidence_layers
    
    # Should inherit boolean flags
    assert child.future_gochara_required is True

def test_many_to_one_question_mapping():
    """
    Tests that multiple Question IDs map to the same Formula Variant.
    """
    from app.core.registry_loader import QuestionRegistryLoader
    loader = QuestionRegistryLoader()
    loader.load_registry()
    
    q1 = loader.get_question("7.1")
    q2 = loader.get_question("7.2")
    
    assert q1["formula_key"] == "MAR_TIMING_NORMAL"
    assert q2["formula_key"] == "MAR_TIMING_NORMAL"
